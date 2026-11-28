# irr_skel_retrace: result on split A (plain language)

**Verdict by the rule written first: PASSED on split A. This is a lead, not a finding.** The rule written first makes the split-C confirmation the finding, and that confirmation (counted) came out UNSETTLED (see `../irr_skel_retrace_C/RESULT.md`). So irr_skel is not confirmed. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: in a tune's on-beat skeleton, does a melody that goes back the way it came (x y x, cancelled out like a walk on a tree) get recorded by more distinct artists? irr_skel is the share of the skeleton walk left after cancelling every step that is immediately undone; low means lots of retracing. Data: 14,511 split-A tunes from TheSession.org (melody only). Outcome y_cov = log(1 + distinct recording artists); on average a tune here has 5.45 artists and 68.5% have at least one recording. Prediction: **-0.03** SD of y_cov per SD of irr_skel (more retracing, more artists), with n_pc (number of pitch classes) held constant. Pass needed p < 0.00556 (.05/9), the predicted sign, both halves with that sign, and a negative Poisson coefficient. Kill: -0.03 outside the 95% range. Power, printed before the outcome was joined: **0.753** (a true zero would have killed it 92% of the time).

## What came out
- Estimate **-0.022**, standard error 0.0069, p = 0.0014. 95% range **-0.036 to -0.008**. N 14,511.
- Halves: -0.029 (N 7,128, p 0.004) and -0.015 (N 7,383, p 0.11). Both negative.
- Second model (Poisson): -0.061, SE 0.015, p = 0.00007. Negative.
- Love reading (y_love = log tunebooks, 7,449 tunes with 10 or more tunebooks; decides nothing): -0.023, SE 0.0088, p = 0.010, range -0.040 to -0.005; halves -0.019 (N 3,607) and -0.028 (N 3,842). Same sign as predicted.

Every pass condition is met. The prediction (-0.03) sits inside the range, so no kill.

## How firm
Firm for split A alone, but only as a lead. The effect is small (about two-thirds of the predicted size) and one half is not significant by itself. It also shrinks as more simplicity measures are held (-0.022, then -0.016 with pc_entropy, then -0.014 with all 13 baselines), so part of it rides on how simple the tune is. The C confirmation is what decides, and there the estimate was -0.011 and unsettled.

## Renaming check
Does irr_skel just repeat another measure? From `../measure_gates10.json` (split A, notes only): R² on the 13 baselines is 0.074; the largest single correlations are pc_entropy +0.18, n_pitch +0.16 and range +0.13, far under the 0.8 stop line. Among the other counted measures it is closest to pe_h0 (+0.38). Two-setting stability is 0.767 (bar 0.5). Not a rename by the gate. But the readings below show the estimate falls by about a third once all 13 baselines are held (-0.014, p 0.041), so a share of it overlaps with simplicity.

## Frozen readings (estimates only; none passes or kills anything)
1. **Holding pc_entropy as well as n_pc** (predicted -): **-0.016**, SE 0.0070, p = 0.018, range -0.030 to -0.003.
2. **All 13 baselines held** (predicted -): **-0.014**, SE 0.0071, p = 0.041, range -0.028 to -0.0006.

Both keep the sign; both are weaker than the main estimate.

## What it cannot say
- Split A only. The rule written first says the A pass is a lead; the C confirmation came out unsettled, so this is not a finding.
- The comparison is across tunes. Composer fixed effects cover named composers only; most tunes are traditional. The first-poster fixed effect was not available this pass.
- Part of the effect overlaps with the simplicity baselines; what is left after holding all 13 is small.
- Recording counts come from TheSession's own recordings list, not all recordings that exist.
- The love reading uses only tunes in 10 or more tunebooks (a truncated sample).
