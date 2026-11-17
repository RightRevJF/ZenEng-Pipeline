"""CoCoPops Billboard (github.com/Computational-Cognitive-Musicology-Lab/CoCoPops, CC BY-NC 4.0; derived counts only).
Parses every .varms.hum (100 songs with four listeners' continuous arousal and valence, 0-127, and the recording's rolling RMS in dB)
and every .hum (214 songs with melody) into bars: section label, key, the chords with their Roman numeral (**harm), absolute chord (**harte)
and share of the bar, the lead melody's notes (pitch, quarter length, onset or tie), the bar's timestamp, and per-bar mean ratings and RMS.
Fetch: git clone --depth 1 https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops.git into /home/claude/data/cocopops."""
import glob, os, re, json, sys
D = "/home/claude/data/cocopops/CoCoPops/Billboard/Data"
STEP = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
def kern_pitch(tok):
    m = re.search(r"([a-gA-G])\1*", tok)
    if not m: return None
    letters = m.group(0); L = letters[0]
    octv = 4 + (len(letters) - 1) if L.islower() else 3 - (len(letters) - 1)
    p = 12 * (octv + 1) + STEP[L.lower()]
    acc = tok[m.end():m.end() + 3]
    return p + acc.count("#") - acc.count("-")
def kern_dur(tok):
    m = re.match(r"[\[\(\{&]*(\d+)(\.*)", tok)
    if not m: return 0.0
    n = int(m.group(1)); d = 4.0 / n if n else 8.0
    return d * (2 - 0.5 ** len(m.group(2)))
def harm_dur(tok):
    m = re.match(r"(\d+)(\.*)", tok)
    if not m: return None
    n = int(m.group(1)); d = 4.0 / n if n else 8.0
    return d * (2 - 0.5 ** len(m.group(2)))
KEYRE = re.compile(r"^\*([a-gA-G][#-]?):$")
def parse(path):
    spines = None; bars = []; label = None; key = None; meter = None
    def newbar(n): return dict(bar=n, label=label, key=key, meter=meter, chords=[], notes=[], ar=[], va=[], rms=[], t=None)
    cur = None
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
            for sp, t in zip(spines, toks):
                if sp == "**harm":
                    k = KEYRE.match(t)
                    if k: key = k.group(1); cur["key"] = cur["key"] or key
                    m = re.match(r"^\*M(\d+)/(\d+)$", t)
                    if m: meter = (int(m.group(1)), int(m.group(2))); cur["meter"] = cur["meter"] or meter
            for t in toks:
                m_ = re.match(r"^\*>Label>(.+)$", t)
                if m_:
                    label = m_.group(1)
                    if not (cur["notes"] or cur["chords"]): cur["label"] = label
                    break
            continue
        if line.startswith("="):
            m = re.match(r"=(\d+)", toks[0])
            if cur is not None and (cur["notes"] or cur["chords"] or cur["ar"]): bars.append(cur)
            cur = newbar(int(m.group(1)) if m else (cur["bar"] + 1)); continue
        if len(toks) != len(spines): continue
        hi = spines.index("**harm"); ti = spines.index("**harte") if "**harte" in spines else None
        kern_i = spines.index("**kern") if "**kern" in spines else None
        t = toks[hi]
        if t != ".":
            dur = harm_dur(t); rn = re.sub(r"^\d+\.*", "", t)
            cur["chords"].append(dict(rn=rn, harte=(toks[ti] if ti is not None else None), q=dur))
        for i, (sp, t) in enumerate(zip(spines, toks)):
            if t == ".": continue
            if sp == "**timestamp" and cur["t"] is None:
                try: cur["t"] = float(t)
                except ValueError: pass
            elif i == kern_i:
                if "q" in t: continue
                d = kern_dur(t)
                if "r" in t and not re.search(r"[a-gA-G]", t): cur["notes"].append(dict(p=None, q=d, on=False)); continue
                p = kern_pitch(t)
                if p is None: continue
                cur["notes"].append(dict(p=p, q=d, on=not (t.endswith("]") or t.endswith("_") or "_" in t[:1])))
            elif sp == "**arousal": cur["ar"].append([float(x) for x in t.split() if re.match(r"^-?\d+(\.\d+)?$", x)])
            elif sp == "**valence": cur["va"].append([float(x) for x in t.split() if re.match(r"^-?\d+(\.\d+)?$", x)])
            elif sp == "**rms":
                try: cur["rms"].append(float(t))
                except ValueError: pass
    if cur and (cur["notes"] or cur["chords"]): bars.append(cur)
    return bars
if __name__ == "__main__":
    out = {}
    for f in sorted(glob.glob(f"{D}/*.hum")):
        base = os.path.basename(f).split(".")[0]
        out[base] = dict(varms=".varms." in f, bars=parse(f))
    json.dump(out, open("cocopops_bars.json", "w"))
    v = [k for k, s in out.items() if s["varms"]]
    print(len(out), "songs;", len(v), "rated;", sum(len(s["bars"]) for s in out.values()), "bars")
    b = out[v[0]]["bars"][10]; print(v[0], b["label"], b["key"], b["chords"], [(n["p"], n["q"]) for n in b["notes"]][:6], b["ar"][:2], b["t"])
