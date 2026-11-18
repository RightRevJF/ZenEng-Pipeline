"""Held-out check of the one reading that related to chart success (nesting: repetition standing out at 2, 4, 8, 16 and 32 bars) on the McGill
Billboard songs NOT in CoCoPops, from chords alone (a bar = the set of chords sounding in it). Also: chords-alone nesting against full nesting on the
CoCoPops songs, to see whether the chords carry the reading. python3 replicate_mcgill.py -> replicate_mcgill.json"""
import sys, os, json, re, glob
import numpy as np
from scipy.stats import spearmanr, rankdata
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import measure as Mz   # readings()
S = json.load(open(os.path.join(H, "..", "harmony", "billboard_sections.json")))
cocoids = set()
for f in glob.glob("/home/claude/data/cocopops/CoCoPops/Billboard/Data/*.hum"):   # the songs with a melody (the .harm files are chords only)
    for l in open(f, errors="ignore"):
        m = re.match(r"!!!SampleID#:\s*(\d+)", l)
        if m: cocoids.add(m.group(1).zfill(4))
def chord_ssm(song):
    bars = []; held = None
    for sec in song["sections"]:
        for b in sec["bars"]:
            ch = {held} if held else set()
            for r in b["rn"]:
                if r: ch.add(r); held = r
            bars.append(ch)
    n = len(bars); M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = bars[i], bars[j]; M[i, j] = (len(a & b) / len(a | b)) if (a or b) else (1.0 if i == j else 0.0)
    return M
rows = []
for s in S:
    m = re.match(r"\d+", str(s.get("peak") or ""))
    if not m: continue
    M = chord_ssm(s)
    if len(M) < 24: continue
    r = Mz.readings(M); r.update(id=s["id"], peak=int(m.group(0)), held_out=s["id"].zfill(4) not in cocoids); rows.append(r)
out = {}
for name, sel in (("held out (not in CoCoPops)", [r for r in rows if r["held_out"]]), ("in CoCoPops", [r for r in rows if not r["held_out"]])):
    x = np.array([r["nesting"] for r in sel], float); y = -np.array([r["peak"] for r in sel], float)
    X = np.column_stack([rankdata([r["bars"] for r in sel]), rankdata([r["sameness"] for r in sel]), np.ones(len(sel))]); res = lambda v: rankdata(v) - X @ np.linalg.lstsq(X, rankdata(v), rcond=None)[0]
    out[name] = dict(songs=len(sel), nesting_vs_peak=[round(float(z), 3) for z in spearmanr(x, y)], controlling_bars_sameness=[round(float(z), 3) for z in spearmanr(res(x), res(y))],
                     median_peak_by_nesting={int(k): [int(sum(x == k)), float(np.median(-y[x == k]))] for k in sorted(set(x))})
D = json.load(open(os.path.join(H, "measure.json")))["songs"]; full = {}
for s in D:
    if s["group"] != "BB": continue
    f = "/home/claude/data/cocopops/CoCoPops/Billboard/Data/" + s["file"]
    sid = next((re.match(r"!!!SampleID#:\s*(\d+)", l).group(1).zfill(4) for l in open(f, errors="ignore") if l.startswith("!!!SampleID#")), None)
    if sid: full[sid] = s["nesting"]
pair = [(full[r["id"].zfill(4)], r["nesting"]) for r in rows if r["id"].zfill(4) in full]
out["chords alone against melody and chords, same songs"] = dict(songs=len(pair), rho=round(float(spearmanr([a for a, b in pair], [b for a, b in pair])[0]), 3))
json.dump(out, open(os.path.join(H, "replicate_mcgill.json"), "w"), indent=1); print(json.dumps(out, indent=1))
