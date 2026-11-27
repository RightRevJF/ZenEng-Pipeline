"""Run 08, transport_economy: R08-G1 (card 1, transport economy). Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'econ', ['w_chr', 'ch_rep', 'V', 'ln_chg', 'ln_bars'], pred=0.03, alpha=ALPHA, frozen_power=0.223, counted=False,
           readings=[("without_w_chr_authors_second_model", "econ", ["ch_rep", "V", "ln_chg", "ln_bars"], None)], estimate_reason='not counted: power 0.22 clears the floor, but the counted set is full at K = 5 (chair.md, the K rule)')
