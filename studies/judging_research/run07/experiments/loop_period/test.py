"""Run 07, loop_period: the rule is PREDICTION.md in this folder (priority 6 of 8; p < .05/8 two-sided).
Run only after PREDICTION.md and ../common.py are committed; common.run_test's guard refuses otherwise.
python3 -I test.py  ->  result.json in this folder"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C

N_TESTS = 8; ALPHA = 0.05 / N_TESTS
MEAS, EXTRA, PRED, SIGN = "lnP", ("ln_tempo",), 0.6, 1

S = C.add_shapes(C.lakh_songs())
R = C.run_test(HERE, S, MEAS, EXTRA, PRED, SIGN, ALPHA, kill=lambda b: b <= 0)
if R["verdict"] == "PASS" and not R["cond_logit"]["converged"]:
    R["verdict"] = "UNSETTLED (conditional logit did not converge)"
R["n_tests"] = N_TESTS
# ---- reported, deciding nothing (PREDICTION.md)
R["readings"]["seconds_form"] = C.fit(S, "lnPsec", ())
pc = np.array([s["Pcat"] for s in S], float)
D = np.column_stack([np.where(np.isfinite(pc), (pc == k).astype(float), np.nan) for k in (2, 8, 16, 0)])
_, X = C.design(S, "ln_tempo")
y = np.array([s["y_foreign"] for s in S], float); g = np.array([s["artist_key"] for s in S])
b, se, p, n, G = C.lpm(np.column_stack([D, X]), y, g)
cat = {f"P{k}_vs_P4": dict(b=float(b[i]), se=float(se[i]), p=float(p[i])) for i, k in enumerate(("2", "8", "16", "other"))}
cat.update(N=n, G=G, order_2_lt_4_lt_8_le_16=bool(b[0] < 0 < b[1] <= b[2]))
R["readings"]["categorical_form"] = cat
json.dump(R, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
print(json.dumps(R, indent=1, default=float))
print("VERDICT:", R["verdict"])
