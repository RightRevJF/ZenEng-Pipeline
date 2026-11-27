"""Run 07, tree_h4m: the rule is PREDICTION.md in this folder (priority 2 of 8; p < .05/8 two-sided).
Run only after PREDICTION.md and ../common.py are committed; common.run_test's guard refuses otherwise.
python3 -I test.py  ->  result.json in this folder"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C

N_TESTS = 8; ALPHA = 0.05 / N_TESTS
MEAS, EXTRA, PRED, SIGN = "H4m", ("cv_w", "ch_rep"), -0.5, -1

S = C.add_shapes(C.lakh_songs())
R = C.run_test(HERE, S, MEAS, EXTRA, PRED, SIGN, ALPHA, kill=lambda b: b >= 0)
if R["verdict"] == "PASS" and not R["cond_logit"]["converged"]:
    R["verdict"] = "UNSETTLED (conditional logit did not converge)"
R["n_tests"] = N_TESTS
# ---- reported, deciding nothing (PREDICTION.md)
R["readings"]["bare_no_extras"] = C.fit(S, MEAS, ())
R["readings"]["cv_w_coefficient"] = C.fit(S, "cv_w", ("H4m", "ch_rep"))
json.dump(R, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
print(json.dumps(R, indent=1, default=float))
print("VERDICT:", R["verdict"])
