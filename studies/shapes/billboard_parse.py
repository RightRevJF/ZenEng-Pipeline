"""CoCoPops Billboard (CC BY-NC 4.0): humdrum files of songs that charted on the Hot 100, 1958-1991. Per bar: the section label,
the lead melody's duration-weighted mean pitch and its note onsets, chord changes, and, in the 100 '.varms' files, the listeners'
mean arousal and valence and the audio's RMS level. Spine splits (*^ *v) are tracked."""
import glob, os, re, csv, json
import numpy as np
D = "/home/claude/dl/shape/cocopops/CoCoPops/Billboard"
STEP = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
def kern_pitch(tok):
    m = re.search(r"([a-gA-G])\1*", tok)
    if not m or "r" in tok.replace("rq", "r").split()[0] and not re.search(r"[a-gA-G]", tok): return None
    letters = m.group(0); L = letters[0]
    octv = 4 + (len(letters) - 1) if L.islower() else 3 - (len(letters) - 1)
    p = 12 * (octv + 1) + STEP[L.lower()]
    acc = tok[m.end():m.end() + 3]
    p += acc.count("#") - acc.count("-")
    return p
def kern_dur(tok):
    m = re.match(r"[\[\(\{]*(\d+)(\.*)", tok)
    if not m: return 0.0
    n = int(m.group(1)); d = 4.0 / n if n else 8.0                      # in quarters (0 = breve)
    dots = len(m.group(2)); return d * (2 - 0.5 ** dots)
def parse(path):
    spines = None; bars = []; cur = None; label = None
    def newbar(n):
        return dict(bar=n, label=label, pitches=[], onsets=0, chords=0, ar=[], va=[], rms=[], t=None)
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("!"): continue
        toks = line.split("\t")
        if line.startswith("**"): spines = toks[:]; cur = newbar(0); continue
        if spines is None: continue
        if line.startswith("*"):
            if any(t in ("*^", "*v", "*-", "*+", "*x") for t in toks):
                new = []; i = 0
                while i < len(toks):
                    t = toks[i]
                    if t == "*^": new += [spines[i], spines[i]]; i += 1
                    elif t == "*v":
                        j = i
                        while j < len(toks) and toks[j] == "*v": j += 1
                        new.append(spines[i]); i = j
                    elif t == "*-": i += 1
                    else: new.append(spines[i]); i += 1
                spines = new; continue
            for t in toks:
                m_ = re.match(r"^\*>(?:Label>(.+)|[A-Z][^_>]*_(.+))$", t)
                if m_:
                    label = m_.group(1) or m_.group(2)
                    if not (cur["pitches"] or cur["onsets"] or cur["chords"]): cur["label"] = label   # a label at the top of the bar names it
                    break
            continue
        if line.startswith("="):
            m = re.match(r"=(\d+)", toks[0])
            if cur is not None and (cur["onsets"] or cur["chords"] or cur["pitches"] or cur["ar"]): bars.append(cur)
            cur = newbar(int(m.group(1)) if m else (cur["bar"] + 1)); cur["label"] = label; continue
        if len(toks) != len(spines): continue
        kern_i = spines.index("**kern") if "**kern" in spines else None
        for i, (sp, t) in enumerate(zip(spines, toks)):
            if t == ".": continue
            if sp == "**harm" and i == spines.index("**harm") and not t.startswith("1r") and "r" != t.strip(";"): cur["chords"] += 1
            elif sp == "**timestamp" and cur["t"] is None:
                try: cur["t"] = float(t)
                except ValueError: pass
            elif i == kern_i:
                if "r" in t and not re.search(r"[a-gA-G]", t): continue
                if "q" in t: continue                                           # grace notes
                p = kern_pitch(t); d = kern_dur(t)
                if p is None: continue
                cur["pitches"].append((p, d))
                if not (t.endswith("]") or "_" in t): cur["onsets"] += 1
            elif sp == "**arousal": cur["ar"] += [float(x) for x in t.split() if re.match(r"^-?\d+(\.\d+)?$", x)]
            elif sp == "**valence": cur["va"] += [float(x) for x in t.split() if re.match(r"^-?\d+(\.\d+)?$", x)]
            elif sp == "**rms":
                try: cur["rms"].append(float(t))
                except ValueError: pass
    if cur and (cur["onsets"] or cur["chords"]): bars.append(cur)
    out = []
    for b in bars:
        ps = b["pitches"]; w = sum(d for _, d in ps)
        out.append(dict(bar=b["bar"], label=b["label"], pitch=(sum(p * d for p, d in ps) / w) if w > 0 else None, onsets=b["onsets"], chords=b["chords"],
                        arousal=float(np.mean(b["ar"])) if b["ar"] else None, valence=float(np.mean(b["va"])) if b["va"] else None,
                        rms=float(np.mean(b["rms"])) if b["rms"] else None, t=b["t"]))
    return out
def sample():
    S = {}
    for r in csv.DictReader(open(f"{D}/Billboard_Sample.tsv", encoding="utf-8"), delimiter="\t"):
        first = lambda x: x.split(",")[0].strip() if x else None
        try: S[r["Filename"]] = dict(artist=r["Artist"], title=r["Title"], date=first(r["Chart Date"]), peak=int(first(r["Peak Position"])), weeks=int(first(r["Weeks on Chart"])), year=int(r["Filename"].rsplit("_", 1)[1]))
        except (ValueError, TypeError, IndexError): pass
    return S
if __name__ == "__main__":
    S = sample(); songs = {}
    for f in sorted(glob.glob(f"{D}/Data/*.hum")) + sorted(glob.glob(f"{D}/Data/*.harm")):
        base = os.path.basename(f).split(".")[0]
        songs[base] = dict(kind=("varms" if ".varms." in f else "hum" if f.endswith(".hum") else "harm"), bars=parse(f), meta=S.get(base))
    json.dump(songs, open("/home/claude/shape/billboard_bars.json", "w"))
    import collections
    print(collections.Counter(s["kind"] for s in songs.values()), "with meta", sum(1 for s in songs.values() if s["meta"]))
    ex = songs["AlGreen_OhMeOhMy_1975"]["bars"][:8]; print(ex)
    v = next(s for s in songs.values() if s["kind"] == "varms"); print([ (b["bar"], b["label"], round(b["pitch"] or 0, 1), b["onsets"], b["chords"], b["arousal"], b["rms"]) for b in v["bars"][:6]])
