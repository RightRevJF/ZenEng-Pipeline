"""Song edges in the McGill Billboard annotations (Burgoyne, Wild and Fujinaga 2011; salami_chords.txt, 890 files, ChoCo's raw copy,
Zenodo 7706751; chart dates from billboard-2.0-index.csv). Per song: length; intro (sections labelled intro or pre-intro at the start)
in seconds and bars; time to the lead voice; whether the voice starts inside the intro; what the intro's material is (its section letter
shared with a later verse, chorus or other section, or its own); the intro's lead instrument; the ending kind (fade: any fadeout line or
label; otherwise the last section's label); the outro or coda's length; the last two chords as Roman numerals on the current tonic;
bookends (intro letter = the last section's letter). Duplicate titles are kept once. Writes edges_billboard.json (per song) and prints
tables by decade."""
import os, re, json, csv, collections, statistics as st
SRC = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw"
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n):
    p = PC[n[0]]
    for a in n[1:]: p += 1 if a == "#" else -1 if a == "b" else 0
    return p % 12
DEG = {0: "I", 1: "bII", 2: "II", 3: "bIII", 4: "III", 5: "IV", 6: "#IV", 7: "V", 8: "bVI", 9: "VI", 10: "bVII", 11: "VII"}
def rn(ch, ton):
    if ch in ("N", "X", "&pause", "*", ".") or ":" not in ch: return None
    root, _, q = ch.partition(":")
    try: d = (pc(root) - ton) % 12
    except Exception: return None
    s = DEG[d]; return s.lower() if q.startswith("min") else s
year = {}
for r in csv.DictReader(open(f"{SRC}/billboard-2.0-index.csv")):
    if r["title"]: year[r["id"].zfill(4)] = int(r["chart_date"][:4])
INSTR = re.compile(r"\((voice|guitar|piano|synthesizer|saxophone|organ|strings|trumpet|harmonica|flute|bass|drums|keyboard|horns|brass|violin|vocal|rap|spoken|banjo|steel|electric piano|clavinet)", re.I)
def bars_of(s):
    n = s.count("|")
    if n == 0: return 0
    n -= 1; m = re.search(r"\|\s*x(\d+)", s)
    return n * int(m.group(1)) if m else n
out = []; seen = set()
for sid in sorted(os.listdir(f"{SRC}/original")):
    L = open(f"{SRC}/original/{sid}/salami_chords.txt").read().splitlines()
    head = {}; rows = []; ton = None
    for l in L:
        if l.startswith("#"):
            k, _, v = l[1:].partition(":"); k = k.strip(); v = v.strip()
            if k == "tonic":
                try: ton = pc(v)
                except Exception: pass
                if rows: rows.append(("tonic", ton)); continue
            head[k] = v; continue
        if "\t" not in l: continue
        t, c = l.split("\t", 1); rows.append((float(t), c, ton))
    key = (head.get("title", "").lower(), head.get("artist", "").lower())
    if key in seen or sid not in year: continue
    seen.add(key)
    ev = [r for r in rows if r[0] != "tonic"]
    end = next((t for t, c, _ in ev if c.strip().startswith("end")), ev[-1][0])
    music = [(t, c, tn) for t, c, tn in ev if not re.match(r"\s*(silence|end|Z\b)", c)]
    if not music: continue
    start = music[0][0]
    # last musical moment: the start of trailing silence or end
    tail = [t for t, c, _ in ev if re.match(r"\s*(silence|end)", c) and t > music[-1][0]]
    stop = min(tail) if tail else end
    secs = []   # (time, letter, label)
    for t, c, tn in music:
        m = re.match(r"\s*([A-Z]'*|Z'*)\s*,\s*([a-z][a-z \-]*?)\s*,", c)
        m2 = re.match(r"\s*fadeout\s*,", c)
        if m: secs.append((t, m.group(1), m.group(2).strip()))
        elif m2: secs.append((t, "", "fadeout"))
    if not secs: continue
    lab = [s[2] for s in secs]
    intro_secs = []
    for s in secs:
        if s[2] in ("intro", "pre-intro", "intro a", "intro b", "intro-a", "intro-b"): intro_secs.append(s)
        else: break
    first_main = next((s for s in secs if s not in intro_secs), None)
    has_intro = bool(intro_secs)
    intro_end = first_main[0] if first_main else stop
    intro_lines = [c for t, c, _ in music if t < intro_end] if has_intro else []
    intro_s = intro_end - start if has_intro else 0.0
    intro_bars = sum(bars_of(c) for c in intro_lines)
    v = next((t for t, c, _ in music if "(voice" in c), None)
    voice_s = (v - start) if v is not None else None
    voice_in_intro = has_intro and v is not None and v < intro_end
    # intro material
    mat = "none"
    if has_intro:
        lets = {s[1] for s in intro_secs}
        later = [s for s in secs if s not in intro_secs and s[1] in lets]
        if not later: mat = "its own"
        else:
            labs = {s[2] for s in later}
            mat = "chorus" if "chorus" in labs else "verse" if "verse" in labs else "outro or other"
    inst = None
    for c in intro_lines:
        m = INSTR.search(c)
        if m: inst = m.group(1).lower(); break
    fade = any(s[2] == "fadeout" for s in secs) or bool(re.search(r"fade", " ".join(c for _, c, _ in music[-6:])))
    last = secs[-1]
    nonfade = [s for s in secs if s[2] != "fadeout"]
    last_lab = nonfade[-1][2] if nonfade else "fadeout"
    # outro length: from the last outro/coda/fadeout/ending section start to stop
    o = next((s for s in reversed(secs) if s[2] in ("outro", "coda", "fadeout", "ending")), None)
    outro_s = stop - o[0] if o else 0.0
    outro_bars = sum(bars_of(c) for t, c, _ in music if o and t >= o[0])
    bookend = has_intro and last[1] != "" and last[1] in {s[1] for s in intro_secs}
    # last chords
    chords = []
    for t, c, tn in music:
        for cell in re.findall(r"\|([^|]*)", c):
            for ch in cell.split():
                r = rn(ch, tn if tn is not None else 0)
                if r and (not chords or chords[-1] != r): chords.append(r)
    out.append(dict(id=sid, year=year[sid], title=head.get("title"), artist=head.get("artist"), metre=head.get("metre"), length=round(stop - start, 1),
                    intro=has_intro, intro_s=round(intro_s, 1), intro_bars=intro_bars, voice_s=None if voice_s is None else round(voice_s, 1),
                    voice_in_intro=voice_in_intro, intro_material=mat, intro_lead=inst, fade=fade, last_section=last_lab,
                    outro_s=round(outro_s, 1), outro_bars=outro_bars, bookend=bookend, last2=chords[-2:]))
json.dump(out, open("edges_billboard.json", "w"), indent=0)
print(len(out), "songs")
