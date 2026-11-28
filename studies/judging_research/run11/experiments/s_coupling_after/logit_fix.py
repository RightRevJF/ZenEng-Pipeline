"""After the result (28 Nov 2026): the frozen test.py passed the conditional logit's groups as a list, which statsmodels refused, so the
sign-check column came back nan. This reruns ONLY that column with groups as an array; it changes no rule and cannot change the verdict; year bins are left out of this column only (singular Hessian with them)
(the kill rule does not use the second model). Output: logit_fix.json."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import test as T
from statsmodels.discrete.conditional_models import ConditionalLogit
R = T.song_rows(); O = {s["key"]: s for s in json.load(open(T.TABLE))["songs"]}
for r in R: o = O[r["key"]]; r["y_foreign"] = np.nan if o["y_foreign"] is None else float(o["y_foreign"])
R = [r for r in R if np.isfinite(r["y_foreign"])]
X = np.column_stack([T._z([r["G_COUP"] for r in R]), T.controls(R)[:, :3]])  # z(x) and the three notes-side controls; the year bins are dropped here (they made the Hessian singular)
cl = ConditionalLogit(np.array([r["y_foreign"] > 0 for r in R], float), X, groups=np.array([r["artist"] for r in R])).fit(disp=0)
out = dict(beta=float(cl.params[0]), se=float(cl.bse[0]), p=float(cl.pvalues[0]), n=len(R))
json.dump(out, open(os.path.join(HERE, "logit_fix.json"), "w"), indent=1); print(out)
