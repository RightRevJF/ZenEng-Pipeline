"""Checks on the judging research, B: within-section chord repetition, Luthier's sections against McGill's kept sections. See PREDICTION.md.
python3 studies/judging_checks/nights_1_2/loops.py -> loops.json. No outcome is read."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
def merge(seq):
    out = []
    for x in seq:
        if not out or out[-1] != x: out.append(x)
    return out
def rep3(seq):
    seen = set(); rep = tot = 0
    for i in range(len(seq) - 2):
        g = tuple(seq[i:i + 3]); tot += 1; rep += g in seen; seen.add(g)
    return rep / tot if tot else None
B = json.load(open(os.path.join(ROOT, "studies", "harmony", "billboard_sections.json"))); kept = {"verse": [], "chorus": [], "bridge": []}; nch = {"verse": [], "chorus": [], "bridge": []}
for s in B:
    s.pop("peak", None); s.pop("date", None); seen = set()
    for sec in s["sections"]:
        if sec["letter"] in seen or sec["label"] not in kept: continue
        seen.add(sec["letter"]); m = merge([r + ("7" if v else "") for b in sec["bars"] for r, v in zip(b["rn"], b["sev"]) if r is not None])
        if len(m) >= 4: kept[sec["label"]].append(rep3(m)); nch[sec["label"]].append(len(m))
out = dict(kept={k: dict(sections=len(v), p10_25_50_75_90=[round(float(x), 3) for x in np.percentile(v, (10, 25, 50, 75, 90))], merged_chords_quartiles=[float(x) for x in np.percentile(nch[k], (25, 50, 75))]) for k, v in kept.items()}, songs={})
def place(k, x): q = out["kept"][k]["p10_25_50_75_90"]; return "over the kept 90th" if x > q[4] else "over the kept 75th" if x > q[3] else "at or over the kept middle" if x >= q[2] else "under the kept middle" if x >= q[1] else "under the kept 25th"
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("60", "songs/p70/lyric60.v44.song.json"), ("59", "songs/p69/lyric59.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); out["songs"][tag] = {}; done = set()
    for name, kind, bars in R["form"]:
        if kind not in kept or kind in done or name not in R["roman"]: continue
        done.add(kind); m = merge([t for bar in R["roman"][name] for t in str(bar).split()])
        if len(m) >= 4: x = rep3(m); out["songs"][tag][kind] = dict(section=name, merged_chords=len(m), repetition=round(x, 3), place=place(kind, x), chords=" ".join(m[:24]))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "loops.json"), "w"), indent=1)
