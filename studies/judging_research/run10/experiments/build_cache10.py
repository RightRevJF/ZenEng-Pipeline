"""Notes-side measure cache for run 10 (splits A and C; H is never computed this pass). No outcome is read here.
Writes /home/claude/dl/thesession/measures_run10.json: {tune_id: {split, baseline..., every proposal's keys}}."""
import sys, os, json, time, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "measures"))
import numpy as np
import common10 as C
import measures_geometer as MG, measures_listener as ML, measures_inventor as MI
T = C.tunes(); out = {}; t0 = time.time(); fails = {"geo": 0, "lis": 0, "inv": 0}
for i, (tid, t) in enumerate(T.items()):
    if t["split"] not in ("A", "C"): continue
    r = {"split": t["split"]}; r.update(C.baseline(t["mel"], t["tonic_pc"]))
    for tag, mod in (("geo", MG), ("lis", ML), ("inv", MI)):
        try:
            m = mod.measure(t)
        except Exception as ex:
            m = None
        if m is None: fails[tag] += 1; continue
        for k, v in m.items():
            if isinstance(v, (int, float)) and v is not None and math.isfinite(float(v)): r[k] = float(v)
    out[str(tid)] = r
    if i % 3000 == 0: print(i, round(time.time() - t0, 1), flush=True)
json.dump(out, open("/home/claude/dl/thesession/measures_run10.json", "w"))
print("done", len(out), fails, round(time.time() - t0, 1))
