"""Run 07, lakh_repetition: the rule is PREDICTION.md in this folder (priority 1 of 8; p < .05/8 two-sided).
Run only after PREDICTION.md and ../common.py are committed; common.run_test's guard refuses otherwise.
python3 -I test.py  ->  result.json in this folder"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C

N_TESTS = 8; ALPHA = 0.05 / N_TESTS
MEAS, EXTRA, PRED, SIGN = "ch_rep", (), 1.0, 1

S = C.add_shapes(C.lakh_songs())
R = C.run_test(HERE, S, MEAS, EXTRA, PRED, SIGN, ALPHA, kill=lambda b: b <= 0)
if R["verdict"] == "PASS" and not R["cond_logit"]["converged"]:
    R["verdict"] = "UNSETTLED (conditional logit did not converge)"
R["n_tests"] = N_TESTS
# ---- reported, deciding nothing (PREDICTION.md)
def early_late(s):
    """W01-J6a, reported only: foreign version sets dated within 5 years of the clique's first year, and more than 10 years after."""
    if not np.isfinite(s["y_foreign"]): return np.nan, np.nan
    if s.get("clique") is None: return 0.0, 0.0
    fy = s.get("first_year"); sets = s.get("_sets") or []
    if fy is None: return np.nan, np.nan
    own = {C.nrm(nm) for e in sets for nm in e[0] if any(C.nrm(x) == s["artist_key"] for x in e[0])}
    ys = [e[1] for e in sets if len(e[0]) > 0 and not any(C.nrm(nm) in own for nm in e[0]) and e[1] is not None]
    return 100.0 * any(y <= fy + 5 for y in ys), 100.0 * any(y > fy + 10 for y in ys)
for s in S: s["y_early"], s["y_late"] = early_late(s)
R["readings"]["W01_J6a_early"] = C.fit(S, MEAS, EXTRA, outcome="y_early")
R["readings"]["W01_J6a_late"] = C.fit(S, MEAS, EXTRA, outcome="y_late")
json.dump(R, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
print(json.dumps(R, indent=1, default=float))
print("VERDICT:", R["verdict"])
