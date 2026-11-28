# core_typical: result on split A (plain language)

**Verdict by the rule written first: PASSED on split A. This is a lead, not a finding.** The rule written first makes the split-C confirmation the finding. On C the power fell under the 0.2 floor, so the C result is an ESTIMATE that decides nothing (see `../core_typical_C/RESULT.md`). The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: does a tune whose on-beat skeleton is typical for its type (a jig that moves like jigs usually move) get recorded by more distinct artists? core_ic is the average surprise, in bits, of each on-beat step under a simple model of how tunes of that type move, built from all other split-A tunes of the type. Low means typical. Data: 14,413 split-A tunes from TheSession.org (melody only); average 5.48 artists, 68.6% recorded. Outcome y_cov = log(1 + distinct recording artists). Prediction: **-0.03** SD of y_cov per SD of core_ic (more typical, more artists), with pc_entropy held constant. Pass needed p < 0.00556 (.05/9), the predicted sign, both halves with that sign, and a negative Poisson coefficient. Kill: -0.03 outside the 95% range. Power, printed before the outcome was joined: **0.510** (a true zero would have killed it 81% of the time).

## What came out
- Estimate **-0.035**, standard error 0.0082, p = 0.00002. 95% range **-0.051 to -0.019**. N 14,413.
- Halves: -0.029 (N 7,078, p 0.011) and -0.041 (N 7,335, p 0.0006). Both negative.
- Second model (Poisson): -0.091, SE 0.021, p = 0.00001. Negative.
- Love reading (y_love = log tunebooks, 7,400 tunes with 10 or more tunebooks; decides nothing): -0.031, SE 0.011, p = 0.005, range -0.054 to -0.009; halves -0.024 (N 3,583) and -0.042 (N 3,817). Same sign.

Every pass condition is met, and the estimate is close to the predicted size. -0.03 is inside the range, so no kill.

## How firm
Firm for split A: p is far under the bar, both halves agree, the Poisson model and the love reading agree, and the estimate holds most of its size with all 13 baselines held (-0.028). But it is one split, and the readings below say the effect is not specific to the skeleton.

## Renaming check
From `../measure_gates10.json` (split A, notes only): R² on the 13 baselines is 0.209; the largest single correlations are pc_entropy +0.36, tonic_share -0.32 and n_pc +0.27, all well under the 0.8 stop line. Among the other counted measures it is closest to slg (+0.40) and pc_entropy (+0.36). Two-setting stability is 0.569 (bar 0.5; it passes, but not by much). Not a rename by the gate, and the reading with all 13 baselines held keeps the effect (-0.028, p 0.001).

## Frozen readings (estimates only; none passes or kills anything)
1. **TSG** (L2's original: core_ic minus surf_ic; predicted -0.03): **+0.013**, SE 0.0072, p = 0.077, range -0.001 to +0.027. Wrong sign.
2. **surf_ic alone** (surprise of the off-beat notes; predicted at most weakly +): **-0.037**, SE 0.0086, p = 0.00001, range -0.054 to -0.021. Clearly negative, against the prediction, and as large as the main estimate.
3. **Holding n_pc as well** (predicted -): **-0.034**, SE 0.0082, p = 0.00003, range -0.050 to -0.018.
4. **All 13 baselines held** (predicted -): **-0.028**, SE 0.0086, p = 0.001, range -0.045 to -0.011.

Readings 1 and 2 matter: the off-beat notes show the same pattern, so what goes with more artists is a typical melody overall, not a typical skeleton in particular.

## What it cannot say
- Split A only. By the rule written first the C confirmation is the finding, and on C it could only be an estimate.
- It does not show the skeleton is special: off-beat surprise (surf_ic) predicts as well, and their difference (TSG) goes the wrong way.
- Direction: the "typical" model is built from the other tunes posted on the site. If well-known tunes have many close relatives posted under other names, they will look typical because they shaped the corpus, not because typicality helped them spread.
- The comparison is across tunes; composer fixed effects cover named composers only; the first-poster fixed effect was not available.
- The love reading uses only tunes in 10 or more tunebooks (a truncated sample).
