"""Run 09, vr4c_momentum: R09-I2 revised, harmonic momentum VR4c (variance ratio of the fifths root walk, ii of each ii-V dropped),
holding IIV. ESTIMATE. Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

K = 1; ALPHA = 0.05 / K
H.run_unseen(HERE, "VR4c", ["IIV"] + H.STD, pred=0.02, alpha=ALPHA, K=K, counted=False, frozen_power=0.12,
             estimate_reason="under the power floor: power 0.12 < 0.2 at .05; withdrawn from the count by its author", readings=[
    dict(label="VR4_uncollapsed", meas="VR4", extra=["IIV"] + H.STD, pred=None, note="round 1's VR4, before the ii was dropped")])
