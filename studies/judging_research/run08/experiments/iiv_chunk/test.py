"""Run 08, iiv_chunk: R08-L3 (the ii-V chunk). Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'IIV', ['w_chr', 'ch_rep', 'V', 'ln_chg', 'ln_bars'], pred=0.04, alpha=ALPHA, frozen_power=0.387, counted=True,
           readings=[("without_w_chr", "IIV", ["ch_rep", "V", "ln_chg", "ln_bars"], None), ("writer_match_only", "IIV", ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars"], H.writer_only)], estimate_reason=None)
