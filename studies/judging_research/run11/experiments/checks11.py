"""Notes-side checks for a measure module (no outcome is read): python3 checks11.py <module.py> [pred] [extra1,extra2]
For each KEY: songs with a value, clip-1/clip-2 stability (Spearman), largest Spearman with the 13 baselines and the 17 pack
measures, R^2 on the 13 baselines, and power by fake outcomes for the given predicted beta at alpha .05/6 (100 draws)."""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
import common11 as C

f = sys.argv[1]; pred = float(sys.argv[2]) if len(sys.argv) > 2 else -0.03
extra = [e for e in (sys.argv[3].split(",") if len(sys.argv) > 3 else []) if e]
s = importlib.util.spec_from_file_location("m", f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
R = C.rows(); C.song_values(R, lambda mel, a: C.baseline(mel), C.BASE); C.song_values(R, m.clip_measure, m.KEYS)
out = {}
for k in m.KEYS:
    S = [r for r in R if np.isfinite(r.get(k, np.nan)) and all(np.isfinite(r.get(e, np.nan)) for e in extra)]
    pr = [r[k + "_c12"] for r in S if r.get(k + "_c12")]
    st = float(stats.spearmanr([p[0] for p in pr], [p[1] for p in pr]).correlation) if len(pr) > 10 else float("nan")
    rn = C.renaming(S, k); top = sorted(((c, v) for c, v in rn.items() if c != "R2_on_13_baselines"), key=lambda t: -abs(t[1]))[:4]
    pw = C.power(S, k, pred, 0.05 / 6, extra, draws=100)
    out[k] = dict(n=len(S), stability=round(st, 3), clip_pairs=len(pr), top_overlap=[(c, round(v, 2)) for c, v in top],
                  R2_on_13_baselines=round(rn["R2_on_13_baselines"], 3), power_at_pred=pw["power"], pred=pred, extra=extra,
                  fake_se=round(pw["median_fake_se"], 4))
print(json.dumps(out, indent=1))
