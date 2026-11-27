"""Run 08, transposed_rep: R08-G2 (transposed repetition T). Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'T_rep', ['ch_rep', 'V', 'ln_chg', 'ln_bars'], pred=0.05, alpha=ALPHA, frozen_power=0.79, counted=False,
           readings=[], estimate_reason='withdrawn from the count by its author (brainstorm round 3)')
