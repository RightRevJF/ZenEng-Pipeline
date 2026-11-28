# cut_ab_parts: result (plain language)

**Verdict by the rule written first: UNSETTLED.** No pass, and no kill. It missed the pass by a whisker: p = 0.0058 against a threshold of 0.0056. Everything else the pass rule asks for came out right. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: in a tune whose pitch map splits cleanly in two (the Cheeger cut, its natural bottleneck), does that split line up with the halves of the tune in time (A part low, B part "up the neck"), and are such tunes recorded by more distinct artists? The measure, cut_ab, is how strongly a note's side of the split tracks whether it is in the first or second half. Checked on 14,413 split-A tunes, with the number of bars and the (log) number of notes held fixed. Prediction: **+0.03** standard deviations of cover-count (y_cov) per standard deviation of cut_ab. Pass needed p < .05/9 = 0.00556, a positive effect in both halves, and a positive Poisson coefficient. Kill: +0.03 outside the 95% range. Power was printed before the outcome was joined: **0.700**.

## What came out
- Estimate **+0.019**, standard error 0.0070, p = 0.0058. 95% range **+0.006 to +0.033**.
- Halves: +0.012 (N 7,078, p 0.22) and +0.026 (N 7,335, p 0.0068). Both positive.
- Second model (Poisson): +0.060, SE 0.016, p = 0.00013. Positive.
- Love reading (y_love, log tunebooks, N 7,400; predicted +): **+0.024**, SE 0.0094, p = 0.012, range +0.005 to +0.042. Halves +0.027 (N 3,583) and +0.022 (N 3,817). Both positive, as predicted.

Sign, both halves and Poisson all agree. Only p falls short, by 0.0002. The prediction (+0.03) lies inside the range, so no kill.

## How firm
Close to a pass but not one, and the rule is the rule: it is unsettled and does not go to split C. Every reading points the predicted way, including the love reading, which is independent of how the cover count is built. Fairly read: a promising lead, somewhat smaller than predicted, that deserves a fresh test on tunes not yet joined to an outcome (split H).

## Renaming check
Does this measure just repeat others? From `measure_gates10.json`: two-setting stability 0.773 (n 4,000; bar 0.5); R² on the 13 baselines 0.178; the largest baseline correlations are range +0.26, n_pitch +0.21, ln_notes -0.14. Among the counted measures, its largest overlap is slg (-0.17). Not a rename. With all 13 baselines held (plus n_bars) the estimate barely moves, +0.017 (reading 4).

## Frozen readings (estimates only; none passes or kills anything)
1. **Strict AABB reels and jigs only** (16 written bars that play as 32, where "second half" is cleanly the B part; predicted +; N 1,444): **+0.062**, SE 0.021, p = 0.0029, range +0.021 to +0.102. About three times the main estimate, in the subset where the measure should work best. Uncounted: it is one of four readings, so its p is not a pass.
2. **cheeger** (how narrow the bottleneck is; range, n_pitch and ln_notes held; predicted -; N 14,413): **-0.065**, SE 0.0079, p = 1.7e-16, range -0.081 to -0.050. The predicted sign and the strongest figure in this folder. Caution: the gate file gives only its stability (0.806), not a renaming check, so how much of it is range or pitch count beyond the three held is not known. A lead, not a finding.
3. **h0_max** (card 1's H0 check: the longest link's share; range, n_pitch and ln_notes held; predicted +; N 14,413): +0.011, SE 0.0075, p = 0.14, range -0.004 to +0.026. Right sign, nothing learned.
4. **All 13 baselines held** (predicted +; N 14,413): **+0.017**, SE 0.0074, p = 0.022, range +0.003 to +0.032.

## What it cannot say
- "Second half" is a crude stand-in for "the B part" in three-part tunes and irregular forms; that dilutes the measure (reading 1 suggests by a lot).
- It cannot say the split causes anything: register may mark the parts in tunes that are popular for other reasons.
- The outcome counts artists in TheSession.org's recordings list, which members submit; it reflects what that community logs.
- Most tunes are traditional, so there is no composer to hold fixed; 98 split-A tunes could not be scored.
- The first-poster effect could not be held (the design carries no username).
- The AABB and cheeger figures were frozen as readings, not tests; they cannot be promoted after the fact, and split A has now been seen.
