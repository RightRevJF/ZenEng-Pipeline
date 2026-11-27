"""Run 08, chrep_confirm: W01-J1 (chord repetition against covers count), a fresh confirmation. Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'ch_rep', [], pred=-0.04, alpha=ALPHA, frozen_power=0.487, counted=True,
           readings=[("size_held", "ch_rep", ["V", "ln_chg", "ln_bars"], None), ("writer_match_only", "ch_rep", [], H.writer_only), ("t0_1950_on", "ch_rep", [], H.t0_1950)], estimate_reason=None)
