"""Run 09, irr_skeleton: R09-I1, the tree-reduced skeleton share IRR (card 1: the signature is blind to retraced excursions). ESTIMATE.
Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

K = 1; ALPHA = 0.05 / K
H.run_unseen(HERE, "IRR", H.STD, pred=0.02, alpha=ALPHA, K=K, counted=False, frozen_power=0.067,
             estimate_reason="under the power floor: power 0.067 < 0.2 at .05; withdrawn from the count by its author", readings=[
    dict(label="IRR_chart_provenance_only", meas="IRR", extra=H.STD, pred=None, keep=lambda s: s["provenance"] == "chart")])
