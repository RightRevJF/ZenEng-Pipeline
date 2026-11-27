"""Run 08 iiv_source (after seeing results; an estimate). Rules in PREDICTION.md. Run once: python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, common as C, posthoc08 as P
R = P.source_rows(); print("songs", len(R), flush=True)
pw = P.fake_power_ols(R, "IIV", P.EXTRA, 0.07, 0.05 / 6, composer_fe=True); print("POWER (before the outcome):", pw, flush=True)
C.load_outcomes(R, HERE); y = np.array([s["y_cov"] for s in R]); g = np.array([s["composer"] for s in R]); out = dict(test="iiv_source", estimate=True, power=pw)
for lab, suf in (("wikifonia_only", ""), ("ireal_only", "_ireal")):
    for s in R:
        for m in ["IIV"] + P.EXTRA: s["_" + m] = s[m + suf]
    X = np.column_stack([C.zs([s["_" + m] for s in R]) for m in ["IIV"] + P.EXTRA] + [C.dummies(C.decade_bins(R))])
    b, se, p, N, G = C.ols_fe(y, X, g); out[lab] = dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(N), G=int(G))
from scipy import stats
out["spearman_wikifonia_vs_ireal_IIV"] = float(stats.spearmanr([s["IIV"] for s in R], [s["IIV_ireal"] for s in R])[0])
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1); print(json.dumps(out, indent=1))
