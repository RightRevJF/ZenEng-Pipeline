"""Run 07, burstiness: the rule is PREDICTION.md in this folder (priority 7 of 8; p < .05/8 two-sided).
Run only after PREDICTION.md and ../common.py are committed; common.run_test's guard refuses otherwise.
python3 -I test.py  ->  result.json in this folder"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C

N_TESTS = 8; ALPHA = 0.05 / N_TESTS
MEAS, EXTRA, PRED, SIGN = "B", (), 0.3, 1

S = C.add_shapes(C.lakh_songs())
R = C.run_test(HERE, S, MEAS, EXTRA, PRED, SIGN, ALPHA, kill=lambda b: b <= 0)
if R["verdict"] == "PASS" and not R["cond_logit"]["converged"]:
    R["verdict"] = "UNSETTLED (conditional logit did not converge)"
R["n_tests"] = N_TESTS
# ---- reported, deciding nothing (PREDICTION.md)
R["readings"]["ch_rep_held"] = C.fit(S, MEAS, ("ch_rep",))
json.dump(R, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
print(json.dumps(R, indent=1, default=float))
print("VERDICT:", R["verdict"])
