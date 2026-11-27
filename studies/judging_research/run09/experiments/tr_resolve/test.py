"""Run 09, tr_resolve: G09-2 merged with R09-L2 (dominants resolving down a fifth or a semitone, per change, on the ii-collapsed path).
ESTIMATE (power under the 0.2 floor at K = 1). Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

K = 1; ALPHA = 0.05 / K
H.run_unseen(HERE, "TR", H.STD, pred=0.035, alpha=ALPHA, K=K, counted=False, frozen_power=0.193,
             estimate_reason="under the power floor: power 0.193 < 0.2 at .05/K, K = 1", readings=[
    dict(label="DRES_per_bar_second_reading", meas="DRES", extra=H.STD, pred=0.035, note="R09-L2's DRES, bar-timed charts only"),
    dict(label="TR_holding_IIV", meas="TR", extra=["IIV"] + H.STD, pred=None,
         note="the Geometer's contrast (a lead): TR near 0 while IIV stays positive would read the ii-V as chart-writer decoration"),
    dict(label="TR_non_jazz", meas="TR", extra=H.STD, pred=0.02, keep=lambda s: s["genre"] != "jazz", note="G09-2's non-jazz reading"),
    dict(label="TR_chart_provenance_only", meas="TR", extra=H.STD, pred=None, keep=lambda s: s["provenance"] == "chart")])
