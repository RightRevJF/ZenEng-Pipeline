"""Run 08, tonic_resistance: R03-I2 (tonic resistance, now with the chart's written key). Frozen by the chair before any outcome is joined; the rules are in PREDICTION.md here.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import harness08 as H

K = 5; ALPHA = 0.05 / K
H.run_ycov(HERE, 'H', ['ch_rep', 'V', 'ln_chg', 'ln_bars', 'H_links'], pred=-0.03, alpha=ALPHA, frozen_power=0.277, counted=False,
           readings=[("without_links", "H", ["ch_rep", "V", "ln_chg", "ln_bars"], None)], estimate_reason='not counted: power 0.28 clears the floor, but the counted set is full at K = 5 (chair.md, the K rule)')
