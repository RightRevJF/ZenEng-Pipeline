"""Sung syllables from CoCoPops (CC BY-NC 4.0; derived counts only): every melody note with its syllable, bar, position in the bar
(quarters), length, pitch, section and line start, for 4/4 songs.
Billboard (214 songs): the first **kern melody spine and the **silbe beside it; note lengths from kern; lines from **phrase 'newline';
rhyme letters from **rhyme. RollingStone (the 80 .hum files with **stress, after de Clercq and Temperley's RS200): onset-only melody on a
time-base grid (*tbN), so lengths are onset-to-onset; stress 1 (primary), 2 (secondary), 0, from Tan, Lustig and Temperley's algorithm.
Fetch: git clone --depth 1 https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops.git into /home/claude/data/cocopops."""
import glob, os, re, json
D = "/home/claude/data/cocopops/CoCoPops"
STEP = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
def kern_pitch(tok):
    m = re.search(r"([a-gA-G])\1*", tok)
    if not m: return None
    letters = m.group(0); L = letters[0]
    octv = 4 + (len(letters) - 1) if L.islower() else 3 - (len(letters) - 1)
    acc = tok[m.end():m.end() + 3]
    return 12 * (octv + 1) + STEP[L.lower()] + acc.count("#") - acc.count("-")
def dur(tok):
    m = re.search(r"(\d+)(\.*)", tok)
    if not m: return None
    n = int(m.group(1)); d = 4.0 / n if n else 8.0
    return d * (2 - 0.5 ** len(m.group(2)))
def update_spines(spines, toks):
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
    return new
def parse(path, rs=False):
    spines = None; out = []; bar = 0; pos = 0.0; meter = None; label = None; tb = 0.25
    newline = False; pending = None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("!"): continue
        toks = line.split("\t")
        if line.startswith("**"): spines = toks[:]; continue
        if spines is None: continue
        if line.startswith("*"):
            if any(t in ("*^", "*v", "*-", "*+", "*x") for t in toks): spines = update_spines(spines, toks); continue
            for sp, t in zip(spines, toks):
                m = re.match(r"^\*M(\d+)/(\d+)$", t)
                if m: meter = (int(m.group(1)), int(m.group(2)))
                if sp == "**kern" and t.startswith("*tb"):
                    d = dur(t[3:]);  tb = d if d else tb
            for t in toks:
                m = re.match(r"^\*>(?:Label>)?([A-Za-z].*)$", t)
                if m and not t.startswith("*>["): label = m.group(1); break
            continue
        if line.startswith("="):
            m = re.match(r"=(\d+)", toks[0]); bar = int(m.group(1)) if m else bar + 1; pos = 0.0; continue
        if len(toks) != len(spines): continue
        try: ki = spines.index("**kern"); si = spines.index("**silbe", ki)
        except ValueError: continue
        sti = spines.index("**stress") if "**stress" in spines else None
        phi = spines.index("**phrase") if "**phrase" in spines else None
        rhi = spines.index("**rhyme") if "**rhyme" in spines else None
        k = toks[ki]; s = toks[si]
        if phi is not None and toks[phi] == "newline": newline = True
        step = tb if rs else (dur(k) if k not in (".",) and dur(k) else 0.0)
        if k != "." and not k.startswith("r") and "r" != k.strip("0123456789.") and re.search(r"[a-gA-G]", k):
            tie_cont = k.endswith("]") or k.endswith("_")
            p = kern_pitch(k)
            if tie_cont or s in ("_", "."):
                if out and not rs and (tie_cont or s == "_"): out[-1]["q"] += step
                if s == "_" and not tie_cont and out: out[-1]["melisma"] = out[-1].get("melisma", 1) + 1
            else:
                st = None
                if sti is not None and toks[sti] not in (".", ""):
                    try: st = int(toks[sti])
                    except ValueError: st = None
                out.append(dict(bar=bar, pos=round(pos, 4), q=step if not rs else None, p=p, syl=s, stress=st, meter=meter,
                                label=label, line_start=newline, rhyme=(toks[rhi] if rhi is not None and toks[rhi] != "." else None)))
                newline = False
        pos += step
    if rs:   # onset-to-onset lengths within the song
        for a, b in zip(out, out[1:]):
            a["q"] = (b["bar"] - a["bar"]) * (a["meter"][0] * 4 / a["meter"][1] if a["meter"] else 4) + b["pos"] - a["pos"]
        if out: out[-1]["q"] = 1.0
    return out
if __name__ == "__main__":
    res = {}
    for f in sorted(glob.glob(f"{D}/Billboard/Data/*.hum")):
        res["BB:" + os.path.basename(f).split(".")[0]] = parse(f)
    for f in sorted(glob.glob(f"{D}/RollingStone/Data/*.hum")):
        if "**stress" in open(f).read(): res["RS:" + os.path.basename(f).split(".")[0]] = parse(f, rs=True)
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sung_syllables.json"), "w"))
    print(len(res), sum(len(v) for v in res.values()))
    for k in ("BB:OtisRedding_TheDockOfTheBay_1968", "RS:2Pac_CaliforniaLove_1996"):
        print(k, [(n["bar"], n["pos"], n["q"], n["p"], n["syl"], n["stress"], n["line_start"]) for n in res[k][:12]])
