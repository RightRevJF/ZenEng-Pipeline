# irr_skel_retrace_C: confirmation on split C (plain language)

**Verdict by the rule written first: UNSETTLED (counted, power 0.233).** No pass and no kill. The A pass is not confirmed, so irr_skel stays a lead, not a finding. The test was run once, after its rules and power were committed.

## What was predicted (written first)
Predictions commit 641f966 (the split-A test and the rule that any A pass gets one re-run on split C); split-C confirmation rules and power commit 629b8da; results commit d823e98. Same measure, model, controls (n_pc), halves, Poisson model and readings as `../irr_skel_retrace/`. Data: 4,261 split-C tunes never before joined to an outcome (average 5.26 artists; 67.8% recorded). Prediction: the frozen **-0.03** SD of y_cov per SD of irr_skel (not A's estimate). Three tests passed on A, so α = .05/3 = 0.0167. Pass needed p < 0.0167, the predicted sign, both halves with that sign, and a negative Poisson coefficient. Kill: -0.03 outside the 95% range. Power on C, printed before the outcome was joined: **0.233**, just above the 0.2 floor, so the test counts (a true zero would have killed it 43% of the time).

## What came out
- Estimate **-0.011**, standard error 0.013, p = 0.39. 95% range **-0.036 to +0.014**. N 4,261.
- Halves: -0.013 (N 2,106, p 0.50) and -0.011 (N 2,155, p 0.56). Both negative.
- Second model (Poisson): -0.020, SE 0.028, p = 0.47. Negative.
- Love reading (2,180 tunes with 10 or more tunebooks; decides nothing): -0.021, SE 0.017, p = 0.24, range -0.055 to +0.014; halves -0.007 (N 1,060) and -0.034 (N 1,120).

Signs all point the predicted way, but p is far from 0.0167, so no pass. The range holds both zero and -0.03 (the lower edge -0.036 is just past -0.03), so no kill.

## How firm
Not firm either way. The estimate is about half of A's (-0.022) and a third of the prediction. Power was 23%, so a true -0.03 would usually have been missed here; a non-pass at this power is weak evidence against the idea. Fairly read: on new tunes the effect is smaller and not distinguishable from zero.

## Renaming check
From `../measure_gates10.json` (split A, notes only): R² on the 13 baselines 0.074; largest single correlations pc_entropy +0.18, n_pitch +0.16, range +0.13; closest counted measure pe_h0 +0.38. Not a rename by the gate. But on C, once pc_entropy or all 13 baselines are held, the estimate falls to about zero (see below). Whatever is left of irr_skel on C looks like it overlaps with simplicity.

## Frozen readings (estimates only; none passes or kills anything)
1. **Holding pc_entropy as well as n_pc** (predicted -): **-0.003**, SE 0.013, p = 0.83, range -0.028 to +0.023.
2. **All 13 baselines held** (predicted -): **-0.0035**, SE 0.013, p = 0.79, range -0.029 to +0.022. Essentially zero.

## What it cannot say
- It cannot rule out a true effect near -0.03: power was low and -0.03 is inside the range.
- It cannot confirm the A result. By the rule written first, the C verdict is the finding, and it is unsettled.
- With the baselines held the estimate is near zero, so even the A lead may be mostly simplicity under another name.
- The comparison is across tunes; composer fixed effects cover named composers only; the first-poster fixed effect was not available.
- Split H stays sealed; it could test this again, but the case for spending it here is weak.
