"""v124 Run 1, the range question: the judge's window range and pitch spread (sd) on each song, Verse 1 and Chorus 1 windows of the survivors,
for v118 (songs/p50), v119 step 1 (songs/p51/step1; songs 40, 42, 43 only), v119 step 3 (songs/p51), Run 1, and Run 1's side runs with 398 off
and with 400 off (main runs), beside the kept means of both collections.
Usage: python3 range_v124.py OUT.json"""
import sys, os, json, pickle
import numpy as np
OUT = sys.argv[1]
SC = json.load(open("/home/claude/p52/tables/zeneng_v120_second_collection.json"))
EVM = {x["measure"]: x for x in SC["every measure: collections' gap in sd, means (CoCoPops, BiMMuDa 1958-1991, builds v118)"]}
KEPT = {m: dict(cocopops=EVM[m]["cocopops"], bimmuda=EVM[m]["bimmuda"], pooled=round((314 * EVM[m]["cocopops"] + 231 * EVM[m]["bimmuda"]) / 545, 3)) for m in ("range", "pitch_sd")}
RUNS = {"v118": "/home/claude/p50/melody_v118_p{s}_main.pkl", "v119 step 1": "/home/claude/p51/step1/melody_v119_p{s}_main.pkl", "v119 step 3": "/home/claude/p51/melody_v119_p{s}_main.pkl",
        "Run 1": "/home/claude/p52/melody_v124_p{s}_main.pkl", "Run 1, 398 off": "/home/claude/p52/melody_v124_p{s}_main_off398.pkl", "Run 1, 400 off": "/home/claude/p52/melody_v124_p{s}_main_off400.pkl"}
def read(path):
    if not os.path.exists(path): return None
    D = pickle.load(open(path, "rb")); o = {}
    for m in ("range", "pitch_sd"):
        for w, nm in (("v", "verse"), ("c", "chorus")):
            x = [b["read"][w][m] for b in D["all"] if b["read"][w] and b["read"][w].get(m) is not None]
            o[f"{m} {nm}"] = round(float(np.mean(x)), 2) if x else None
        x = [b["read"][w][m] for b in D["all"] for w in ("v", "c") if b["read"][w] and b["read"][w].get(m) is not None]
        o[m] = round(float(np.mean(x)), 2) if x else None
    o["survivors"] = len(D["all"]); o["knobs"] = {k: round(v, 3) for k, v in (D.get("line_knobs") or {}).items() if k in ("ct398", "ctb398", "ctd398", "res398", "turn400", "dpk", "widen")}
    return o
R = dict(kept=KEPT, by_song={s: {k: read(p.format(s=s)) for k, p in RUNS.items()} for s in ("40", "42", "43", "44", "45")})
for k in RUNS:
    xs = [R["by_song"][s][k] for s in R["by_song"] if R["by_song"][s][k]]
    R.setdefault("across songs read", {})[k] = dict(songs=len(xs), range=round(float(np.mean([x["range"] for x in xs])), 2) if xs else None, pitch_sd=round(float(np.mean([x["pitch_sd"] for x in xs])), 2) if xs else None)
json.dump(R, open(OUT, "w"), indent=1)
for s, d in R["by_song"].items(): print(s, {k: (v["range"], v["pitch_sd"]) if v else None for k, v in d.items()})
print(R["across songs read"], KEPT)
