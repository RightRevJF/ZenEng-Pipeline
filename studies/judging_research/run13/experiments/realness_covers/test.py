"""realness_covers: cross-fitted realness (gap_engine's recipe, trained without the scored artists' half), then the within-artist test."""
import os, sys, json, collections
import numpy as np
from sklearn.linear_model import LogisticRegression
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common13 as C
ALPHA = 0.05 / 4; PRED = 0.02
H = json.load(open(C.FEATS)); names = sorted(next(iter(H.values()))["f"])
D = np.load("/home/claude/dl/run13/realness_inputs.npz"); Xe = D["Xe"]
assert list(D["names"]) == names
keys = list(H); Xr = np.array([[H[k]["f"][n] for n in names] for k in keys], float); half = np.array([H[k]["half"] for k in keys])
score = np.full(len(keys), np.nan)
for h in (0, 1):
    tr = half != h; X = np.vstack([Xr[tr], Xe]); y = np.r_[np.ones(tr.sum()), np.zeros(len(Xe))]
    med = np.nanmedian(X, 0); X = np.where(np.isfinite(X), X, med); mu, sd = X.mean(0), X.std(0) + 1e-12
    w = np.where(y == 1, 0.5 / y.mean(), 0.5 / (1 - y.mean()))
    m = LogisticRegression(C=1.0, max_iter=3000).fit((X - mu) / sd, y, sample_weight=w)
    Xt = Xr[half == h]; Xt = np.where(np.isfinite(Xt), Xt, med); score[half == h] = m.decision_function((Xt - mu) / sd)
byv = collections.defaultdict(list)
for k, s in zip(keys, score): byv[H[k]["vid"]].append((s, H[k]["n"]))
R, _ = C.song_table()
x = np.array([np.average([a for a, _ in byv[r["vid"]]], weights=[b for _, b in byv[r["vid"]]]) for r in R])
print("REAL computed for", len(R), "songs; median", round(float(np.median(x)), 3), flush=True)
if sys.argv[1:] != ["run"]: sys.exit(0)
info = C.load_y(R, [os.path.join(HERE, "PREDICTION.md"), os.path.join(HERE, "test.py"), os.path.join(os.path.dirname(HERE), "common13.py"),
                    os.path.join(os.path.dirname(HERE), "features13.py"), os.path.join(os.path.dirname(HERE), "gap_engine", "run.py")])
m, Rk, X = C.within(R, x, "y"); hv = []
for h in (0, 1):
    idx = [i for i, r in enumerate(R) if r["half"] == h]; hv.append(C.within([R[i] for i in idx], x[idx], "y")[0])
cl = C.cond_logit_sign(Rk, X, "y"); lo, hi = m["beta"] - 1.96 * m["se"], m["beta"] + 1.96 * m["se"]
passed = m["p"] < ALPHA and m["beta"] > 0 and all(h_["beta"] > 0 for h_ in hv) and cl.get("beta", -1) > 0
v = "passed (a lead on seen songs)" if passed else ("killed" if not (lo <= PRED <= hi) else "unsettled")
out = dict(outcome_info=info, alpha=ALPHA, prediction=PRED, main=m, range=[lo, hi], halves=hv, cond_logit=cl, verdict=v,
           reading_REAL_with_REP_held=C.within(R, x, "y", extra=("ln_notes", "REP"))[0])
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
