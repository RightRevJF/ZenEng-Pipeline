# slg_selflearn: result (plain language)

**Verdict by the rule written first: KILLED.** The estimate came out with the wrong sign, and the predicted +0.03 lies well outside the 95% range. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: is a tune that "teaches you its own grammar" recorded by more distinct artists? The measure, slg (self-learnability gain), asks how much better the second half of a tune is predicted by what its own first half taught, compared with what tunes of its type usually do. Checked on 14,413 split-A tunes, with bar repetition and the (log) number of notes held fixed, since both partly drive the measure. Prediction: **+0.03** standard deviations of cover-count (y_cov) per standard deviation of slg. Pass needed p < .05/9 = 0.00556, a positive effect in both halves, and a positive Poisson coefficient. Kill: +0.03 outside the 95% range. Power was printed before the outcome was joined: **0.413**, the lowest of the nine. The chance that a true +0.03 would be killed by this rule was 0.070.

## What came out
- Estimate **-0.011**, standard error 0.0081, p = 0.17. 95% range **-0.027 to +0.005**.
- Halves: -0.012 (N 7,078, p 0.31) and -0.010 (N 7,335, p 0.39). Both negative.
- Second model (Poisson): -0.013, SE 0.020, p = 0.52. Negative.
- Love reading (y_love, log tunebooks, N 7,400; predicted +): +0.009, SE 0.011, p = 0.42, range -0.013 to +0.032. Halves +0.006 (N 3,583) and +0.011 (N 3,817). Right sign, too small to read.

Every part of the cover test goes the wrong way. The range tops out at +0.005, far below +0.03.

## How firm
Fairly firm against the idea as written. Power was modest (0.41), but the kill does not depend on missing a small effect: the estimate sits on the wrong side of zero, and a true +0.03 would have been killed only 7% of the time. Fairly read: self-learnability, as measured here, does not go with more recording artists.

## Renaming check
Does this measure just repeat others? From `measure_gates10.json`: two-setting stability **0.548** (n 4,000; bar 0.5, the nearest of the nine); R² on the 13 baselines 0.273; the largest baseline correlations are ln_notes +0.34, bar_rep +0.32, leap_share +0.14. Among the counted measures it overlaps most with core_ic (+0.40), the largest overlap of any pair. core_ic passed on split A tonight with a negative sign, so part of slg's wrong sign may be that shared typicality. With all 13 baselines held the estimate stays negative (-0.009). Without bar_rep and ln_notes held it is clearly negative (-0.025; reading 2), so the raw link is mostly repetition and length.

## Frozen readings (estimates only; none passes or kills anything)
1. **slg_win** (share of second-half notes where the tune's own model beats the type model; same extras; predicted +; N 14,413): **+0.025**, SE 0.0083, p = 0.0024, range +0.009 to +0.042. Positive, the opposite of the test. Uncounted and one of three readings; its stability is 0.585. It suggests that winning often by a little and winning on average by a lot are different things here. A lead at most.
2. **slg without bar_rep and ln_notes held** (predicted +; N 14,413): **-0.025**, SE 0.0074, p = 0.00065, range -0.040 to -0.011. Wrong sign.
3. **All 13 baselines held** (predicted +; N 14,413): **-0.009**, SE 0.0089, p = 0.31, range -0.026 to +0.008. Wrong sign, near zero.

## What it cannot say
- It kills the measure as built (mean log gain, add-one bigrams), not every idea of "learning a tune"; slg_win points the other way.
- The measure is the least stable of the nine (0.55), so transcriber noise is high and pulls the estimate toward zero.
- The type model is trained on split A itself (leave-one-out), so "what tunes of its type usually do" is defined by the same sample.
- The outcome counts artists in TheSession.org's recordings list, which members submit; most tunes are traditional, with no composer to hold fixed.
- The first-poster effect could not be held (the design carries no username).
