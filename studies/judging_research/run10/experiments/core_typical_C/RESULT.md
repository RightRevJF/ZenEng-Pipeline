# core_typical_C: confirmation on split C (plain language)

**Verdict by the rule written first: ESTIMATE (not counted; power 0.14, under the 0.2 floor).** It passes nothing and kills nothing, however suggestive the numbers. The A pass stays a lead. The sealed split H can confirm it next pass. The test was run once, after its rules and power were committed.

## What was predicted (written first)
Predictions commit 641f966 (the split-A test and the rule that any A pass gets one re-run on split C); split-C confirmation rules and power commit 629b8da; results commit d823e98. Same measure, model, controls (pc_entropy), halves, Poisson model and readings as `../core_typical/`. For C tunes the "typical" model is built from all split-A tunes (notes only). Data: 4,234 split-C tunes never before joined to an outcome (average 5.28 artists; 67.9% recorded). Prediction: the frozen **-0.03** SD of y_cov per SD of core_ic (not A's estimate). Three tests passed on A, so α = .05/3 = 0.0167. Pass would need p < 0.0167, the predicted sign, both halves with that sign, and a negative Poisson coefficient. Kill: -0.03 outside the 95% range. Power on C, printed before the outcome was joined: **0.140**, under the 0.2 floor (R06-5). By the rule, that makes this an estimate whatever comes out.

## What came out
- Estimate **-0.051**, standard error 0.017, p = 0.0028. 95% range **-0.084 to -0.018**. N 4,234.
- Halves: -0.041 (N 2,092, p 0.11) and -0.052 (N 2,142, p 0.022). Both negative.
- Second model (Poisson): -0.091, SE 0.040, p = 0.021. Negative.
- Love reading (2,173 tunes with 10 or more tunebooks; decides nothing): -0.042, SE 0.022, p = 0.055, range -0.086 to +0.001; halves -0.039 (N 1,056) and -0.031 (N 1,117).

Plainly: every pass condition would have been met (p 0.003 under 0.0167, sign, both halves, Poisson), and -0.03 is inside the range. But the test was declared too weak to count before the outcome was joined, so it decides nothing.

## How firm
Suggestive, not settled. It points the same way as A, on tunes never used before. But at 14% power, a result that clears the bar tends to overstate the true size; -0.051 is larger than both the prediction and A's -0.035, which fits that pattern. The honest reading: A passed, and C gives no reason to doubt it, but the confirmation the rule requires has not happened. Split H, still sealed, is the place to do it next pass, with power set before its outcome is joined.

## Renaming check
From `../measure_gates10.json` (split A, notes only): R² on the 13 baselines 0.209; largest single correlations pc_entropy +0.36, tonic_share -0.32, n_pc +0.27; closest counted measures slg +0.40 and pc_entropy +0.36; stability 0.569 (bar 0.5). Not a rename by the gate. On C, holding all 13 baselines keeps most of the estimate (-0.037, p 0.033).

## Frozen readings (estimates only; none passes or kills anything)
1. **TSG** (core_ic minus surf_ic; predicted -0.03): **+0.018**, SE 0.013, p = 0.16, range -0.007 to +0.044. Wrong sign, as on A.
2. **surf_ic alone** (off-beat surprise; predicted at most weakly +): **-0.054**, SE 0.016, p = 0.001, range -0.086 to -0.021. Clearly negative, against the prediction, as on A.
3. **Holding n_pc as well** (predicted -): **-0.052**, SE 0.017, p = 0.002, range -0.086 to -0.019.
4. **All 13 baselines held** (predicted -): **-0.037**, SE 0.017, p = 0.033, range -0.071 to -0.003.

As on A, the off-beat notes carry the same pattern, so the lead is "a typical melody", not "a typical skeleton".

## What it cannot say
- It cannot confirm core_typical: by the rule written first, a test under the 0.2 power floor is an estimate, so the A pass stays a lead.
- The size is likely overstated at this power.
- It does not show the skeleton is special (readings 1 and 2).
- Direction: the "typical" model comes from tunes posted on the site; well-known tunes may look typical because they and their relatives shaped it.
- The comparison is across tunes; composer fixed effects cover named composers only; the first-poster fixed effect was not available.
