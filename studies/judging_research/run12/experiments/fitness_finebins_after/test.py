import sys, os, math, json, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fitness")); import fitness as F
F.AGE_EDGES = list(range(0, 11)) + [11, 16, 32]
songs, info = F.load(); D = F.design(songs); nA = len(F.AGE_EDGES) - 1
out = {"age_edges": F.AGE_EDGES, "profile": {}}
for A in [0.3, 1, 3, 10, 30, 100]:
    nl = lambda th: F.negll(np.concatenate([th[:1], [math.log(A)], th[1:]]), D, True)
    r = minimize(nl, np.concatenate([[0.0], np.zeros(nA), np.full(16, -3.0)]), method="L-BFGS-B", options=dict(maxiter=4000))
    out["profile"][str(A)] = float(r.fun); print(A, r.fun, flush=True)
rf = F.fit(D, True); out["free"] = dict(negll=float(rf.fun), A=float(math.exp(rf.x[1])), r=float(math.exp(rf.x[0])))
best_finite = min(out["profile"][k] for k in ["0.3", "1", "3", "10", "30"])
out["killed"] = bool(out["profile"]["100"] - best_finite > 2); out["verdict"] = "killed" if out["killed"] else ("holds" if out["free"]["A"] > 1000 else "unsettled")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1); print(json.dumps(out, indent=1))
