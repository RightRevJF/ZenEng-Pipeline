"""Run 08, key_travel: R08-L1 merged with R08-I1 (card 1, circular W1 on the circle of fifths). Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'TRAV5', ['TRAVL1', 'ch_rep', 'V', 'ln_chg', 'ln_bars'], pred=0.05, alpha=ALPHA, frozen_power=0.213, counted=True,
           readings=[("E_second_reading", "E", ["spread", "TRAVL1", "ch_rep", "V", "ln_chg", "ln_bars"], None), ("TRAV5_without_TRAVL1", "TRAV5", ["ch_rep", "V", "ln_chg", "ln_bars"], None), ("writer_match_only", "TRAV5", ["TRAVL1", "ch_rep", "V", "ln_chg", "ln_bars"], H.writer_only)], estimate_reason=None)
