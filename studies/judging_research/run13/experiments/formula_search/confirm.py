"""formula_search, step 2: the three selected formulas, frozen in selected.json (committed before this runs), tested once on HALF 1."""
import os, sys, json, hashlib
import numpy as np
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common13 as C
S = json.load(open(os.path.join(HERE, "selected.json"))); ALPHA = 0.05 / 4
R, names = C.song_table(); mu, sd = S["mu"], S["sd"]
H1 = [r for r in R if r["half"] == 1]
def zv(n, rows): return (np.array([r[n] for r in rows], float) - mu[n]) / sd[n]
def value(spec, rows):
    if spec[0] == "base": return zv(spec[1], rows)
    if spec[0] == "diff": return zv(spec[1], rows) - zv(spec[2], rows)
    return zv(spec[1], rows) * zv(spec[2], rows)
n1 = sum(1 for r in H1 if r["ln_notes"] is not None); se_pred = 0.011 * (9588 / n1) ** 0.5; z = norm.isf(ALPHA / 2)
plan = []
for s in S["selected"]:
    pred = 0.5 * s["discovery"]["beta"]; pw = float(norm.cdf(abs(pred) / se_pred - z) + norm.cdf(-abs(pred) / se_pred - z))
    plan.append(dict(name=s["name"], prediction=pred, power_before_join=pw, counted=pw >= 0.2, se_assumed=se_pred))
print("before the join:", json.dumps(plan, indent=1), flush=True)
if sys.argv[1:] != ["run"]: sys.exit(0)
info = C.load_y(H1, [os.path.join(HERE, "PREDICTION.md"), os.path.join(HERE, "confirm.py"), os.path.join(HERE, "selected.json"),
                     os.path.join(os.path.dirname(HERE), "common13.py"), os.path.join(os.path.dirname(HERE), "features13.py")])
out = dict(outcome_info=info, alpha=ALPHA, tests=[])
for s, pl in zip(S["selected"], plan):
    x = value(s["spec"], H1); m, Rk, X = C.within(H1, x, "y")
    q = [int(hashlib.md5((r["artist"] + "b").encode()).hexdigest(), 16) % 2 for r in H1]
    qs = []
    for h in (0, 1):
        sub = [r for r, qq in zip(H1, q) if qq == h]; qs.append(C.within(sub, value(s["spec"], sub), "y")[0])
    cl = C.cond_logit_sign(Rk, X, "y"); sg = np.sign(s["discovery"]["beta"])
    lo, hi = m["beta"] - 1.96 * m["se"], m["beta"] + 1.96 * m["se"]
    passed = pl["counted"] and m["p"] < ALPHA and np.sign(m["beta"]) == sg and all(np.sign(x_["beta"]) == sg for x_ in qs) and cl.get("beta") is not None and np.sign(cl["beta"]) == sg
    killed = pl["counted"] and not (lo <= pl["prediction"] <= hi)
    v = "passed (a lead on seen songs)" if passed else "killed" if killed else ("unsettled" if pl["counted"] else "estimate")
    out["tests"].append(dict(name=s["name"], plan=pl, main=m, range=[lo, hi], quarter_halves=qs, cond_logit=cl, verdict=v))
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
