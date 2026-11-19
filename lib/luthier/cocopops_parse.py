"""Parse the CoCoPops Billboard .hum / .varms.hum files (Window 42) into one note table.

Per note: song, title, chart peak / weeks, year, key (tonic pc, mode), section label, bar, beat-in-bar, absolute
beat, MIDI pitch, duration (beats), syllable, rhyme letter, the chord sounding (roman as written, root degree,
quality, borrowed flag, tension by the engine's table), lead instrument, and for the varms files the mean
valence, mean arousal and rms at that note.
    python3 lib/luthier/cocopops_parse.py corpora/CoCoPops/Billboard/Data → corpora/cocopops_notes.csv.gz   (895, 749.70; see kept_corpus.py)
"""
from __future__ import annotations
import re, sys, json
from pathlib import Path
import pandas as pd

NOTE_PC = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}
TENSION = {1: 0, 6: 1, 3: 1, 4: 2, 2: 2, 5: 3, 7: 3}
MAJOR = {0, 2, 4, 5, 7, 9, 11}


def kern_pitch(tok: str):
    m = re.search(r"([a-gA-G]+)([#-]*)", tok)
    if not m: return None
    letters, acc = m.group(1), m.group(2)
    L = letters[0]
    if L.islower(): octave = 3 + len(letters)        # c = C4 (60): midi = 12*(octave+1)
    else: octave = 4 - len(letters)                  # C = C3 (48)
    return 12 * (octave + 1) + NOTE_PC[L.lower()] + acc.count("#") - acc.count("-")


def recip_dur(tok: str):
    m = re.match(r"(\d+)(\.*)", tok)
    if not m: return None
    n = int(m.group(1)); d = m.group(2).count(".")
    if n == 0: return 8.0
    base = 4.0 / n
    tot, add = base, base
    for _ in range(d): add /= 2; tot += add
    return tot


def roman_parse(tok: str):
    """'2vi', '1V7', '-VII', '1Im7', '1II7', 'iv', 'viio' → (degree, quality, accidental, is_seventh)."""
    t = re.sub(r"^\d+\.*", "", tok)          # strip recip
    t = t.replace("[", "").replace("]", "").replace("_", "")
    m = re.match(r"^([#-]*)(VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i)(.*)$", t)
    if not m: return None
    acc, num, rest = m.group(1), m.group(2), m.group(3)
    deg = ROMAN[num.upper()]
    minor = num.islower()
    qual = "dim" if "o" in rest and not minor and False else ("dim" if rest.startswith("o") or rest.startswith("ø") else ("min" if minor else "maj"))
    if rest.startswith("o"): qual = "dim"
    if "+" in rest: qual = "aug"
    seventh = "7" in rest
    return deg, qual, acc, seventh


def parse_file(path: Path) -> list[dict]:
    lines = path.read_text(errors="ignore").splitlines()
    meta = {}
    for l in lines:
        m = re.match(r"!!!(\w+):\s*(.*)", l)
        if m: meta[m.group(1)] = m.group(2).strip()
    types = None; rows = []
    key_pc, mode = None, "major"; section = None; bar = 0; beat_in_bar = 0.0; abs_beat = 0.0
    cur_chord = None; lead = None; bpb = 4
    kern_idx = None; silbe_idx = None; rhyme_idx = None
    pending_tie = None
    for l in lines:
        if not l or l.startswith("!"): continue
        cols = l.split("\t")
        if l.startswith("**"):
            types = cols
            # the first **kern is the lead; its **silbe / **rhyme follow it
            kern_idx = next((i for i, t in enumerate(types) if t == "**kern"), None)
            silbe_idx = next((i for i, t in enumerate(types) if t == "**silbe" and (kern_idx is None or i > kern_idx)), None)
            rhyme_idx = next((i for i, t in enumerate(types) if t == "**rhyme" and (kern_idx is None or i > kern_idx)), None)
            continue
        if types is None: continue
        if l.startswith("*"):
            # spine manipulators: keep it simple — if the column count changes, re-derive indices by walking
            if any(c in ("*^", "*v", "*-", "*+") for c in cols):
                new = []
                for t, c in zip(types, cols):
                    if c == "*^": new += [t, t]
                    elif c == "*-" or c == "*v" and new and new[-1] == t and False: pass
                    else: new.append(t)
                # handle *v merges: collapse consecutive merged columns of the same type
                if "*v" in cols:
                    merged, i = [], 0
                    while i < len(cols):
                        if cols[i] == "*v":
                            j = i
                            while j + 1 < len(cols) and cols[j + 1] == "*v": j += 1
                            merged.append(types[i]); i = j + 1
                        else: merged.append(types[i]); i += 1
                    new = merged
                if "*-" in cols: break
                types = new
                kern_idx = next((i for i, t in enumerate(types) if t == "**kern"), None)
                silbe_idx = next((i for i, t in enumerate(types) if t == "**silbe" and (kern_idx is None or i > kern_idx)), None)
                rhyme_idx = next((i for i, t in enumerate(types) if t == "**rhyme" and (kern_idx is None or i > kern_idx)), None)
                continue
            for c in cols:
                m = re.match(r"^\*([A-Ga-g][#-]*):$", c)
                if m:
                    k = m.group(1); key_pc = (NOTE_PC[k[0].lower()] + k.count("#") - k.count("-")) % 12; mode = "minor" if k[0].islower() else "major"
                m = re.match(r"^\*>Label>(.+)$", c)
                if m: section = m.group(1).lower()
                m = re.match(r"^\*M(\d+)/(\d+)$", c)
                if m: bpb = int(m.group(1)) * 4 / int(m.group(2))
            continue
        if l.startswith("="):
            m = re.match(r"=(\d+)", l)
            if m: bar = int(m.group(1))
            beat_in_bar = 0.0
            continue
        if len(cols) != len(types): continue
        # chord on this row?
        h = cols[0] if types[0] == "**harm" else next((c for c, t in zip(cols, types) if t == "**harm"), ".")
        if h not in (".", "") and not h.startswith("!"):
            rp = roman_parse(h)
            if rp:
                deg, qual, acc, sev = rp
                pcs_major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
                borrowed = bool(acc) or (mode == "major" and ((deg in (2, 3, 6) and qual == "maj") or (deg in (1, 4, 5) and qual == "min")))
                cur_chord = {"roman": re.sub(r"^\d+\.*", "", h), "deg": deg, "qual": qual, "acc": acc, "seventh": sev, "borrowed": borrowed, "tension": TENSION.get(deg, 2) + (1 if borrowed else 0)}
            li = next((i for i, t in enumerate(types) if t == "**leadinstrument"), None)
            if li is not None and cols[li] not in (".", ""): lead = cols[li]
        if kern_idx is None: continue
        k = cols[kern_idx]
        if k in (".", ""): continue
        tok = k.split()[0]
        dur = recip_dur(tok)
        if dur is None: continue
        is_rest = "r" in tok
        p = None if is_rest else kern_pitch(tok)
        syl = cols[silbe_idx] if silbe_idx is not None else "."
        rhy = cols[rhyme_idx] if rhyme_idx is not None else "."
        def mean_of(idx):
            if idx is None or cols[idx] in (".", ""): return None
            try: return sum(float(x) for x in cols[idx].split()) / len(cols[idx].split())
            except ValueError: return None
        vi = next((i for i, t in enumerate(types) if t == "**valence"), None); ai = next((i for i, t in enumerate(types) if t == "**arousal"), None); ri = next((i for i, t in enumerate(types) if t == "**rms"), None)
        tie_cont = "]" in tok or "_" in tok
        if not is_rest and p is not None:
            if tie_cont and rows and rows[-1]["pitch"] == p:
                rows[-1]["dur"] += dur            # a tied continuation lengthens the previous note
            else:
                rows.append({"song": path.stem.replace(".varms", ""), "title": meta.get("OTL"), "peak": meta.get("BillboardPeak"), "weeks": meta.get("BillboardWeeksOnChart"),
                             "year": (meta.get("BillboardChartDate") or "")[:4], "key_pc": key_pc, "mode": mode, "section": section, "bar": bar, "beat": beat_in_bar, "abs_beat": abs_beat,
                             "pitch": p, "dur": dur, "syl": syl if syl != "." else "", "rhyme": rhy if rhy != "." else "", "lead": lead,
                             "roman": cur_chord["roman"] if cur_chord else None, "chord_deg": cur_chord["deg"] if cur_chord else None, "chord_qual": cur_chord["qual"] if cur_chord else None,
                             "borrowed": cur_chord["borrowed"] if cur_chord else None, "tension": cur_chord["tension"] if cur_chord else None,
                             "valence": mean_of(vi), "arousal": mean_of(ai), "rms": mean_of(ri)})
        beat_in_bar += dur; abs_beat += dur
    return rows


if __name__ == "__main__":
    root = Path(sys.argv[1]); allrows = []; n = 0
    for f in sorted(root.glob("*.hum")):
        try:
            r = parse_file(f)
        except Exception as e:
            print("skip", f.name, e); continue
        if len(r) >= 30: allrows += r; n += 1
    D = pd.DataFrame(allrows)
    out = Path(__file__).resolve().parent.parent.parent / "corpora"; out.mkdir(exist_ok=True); D.to_csv(out / "cocopops_notes.csv.gz", index=False)
    print("songs", n, "notes", len(D)); print(D.head(12).to_string())
