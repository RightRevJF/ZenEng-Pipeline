"""Run 09, tq_tension: G09-1, tension breathing TQ (card 1, lead-lag area = half the quadratic variation), holding IIV. ESTIMATE.
Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

K = 1; ALPHA = 0.05 / K
H.run_unseen(HERE, "TQ", ["IIV"] + H.STD, pred=0.01, alpha=ALPHA, K=K, counted=False, frozen_power=0.037,
             estimate_reason="under the power floor: power 0.037 < 0.2 at .05; its author and the Skeptic froze it as an estimate", readings=[
    dict(label="TQ_without_IIV", meas="TQ", extra=H.STD, pred=0.03, note="G09-1's first prediction, before IIV is held")])
