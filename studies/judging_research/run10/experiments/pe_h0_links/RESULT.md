# pe_h0_links: result (plain language)

**Verdict by the rule written first: KILLED.** The predicted +0.03 lies just outside the 95% range (top edge +0.0293). The sign was right, but the effect is about half the predicted size. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: does a tune whose melodic skeleton is "evenly knit" get recorded by more distinct artists? The measure, pe_h0 (card 1's construction), builds a map of which on-beat pitches lead to which, keeps the weakest links that hold the map together (the H0 barcode), and asks how evenly strong those links are. Checked on 14,511 split-A tunes, with pitch-class entropy (McBride & Leroi's measure) held fixed. Prediction: **+0.03** standard deviations of cover-count (y_cov) per standard deviation of pe_h0. Pass needed p < .05/9 = 0.00556, a positive effect in both halves, and a positive Poisson coefficient. Kill: +0.03 outside the 95% range. Power was printed before the outcome was joined: **0.723**. The chance that a true +0.03 would be killed by this rule was 0.057.

## What came out
- Estimate **+0.016**, standard error 0.0069, p = 0.022. 95% range **+0.002 to +0.029**.
- Halves: +0.014 (N 7,128, p 0.15) and +0.019 (N 7,383, p 0.053). Both positive.
- Second model (Poisson): +0.028, SE 0.016, p = 0.078. Positive.
- Love reading (y_love, log tunebooks, N 7,449; predicted +): +0.007, SE 0.0088, p = 0.43, range -0.010 to +0.024. Halves +0.008 (N 3,607) and +0.005 (N 3,842). Right sign, too small to read.
- Context: the tunes have 5.45 distinct recording artists on average; 68.5% have at least one.

Sign, halves and Poisson all agree with the prediction, but p is four times the threshold, so no pass. The range stops at +0.0293, a hair under +0.03, so the kill rule applies.

## How firm
The kill is narrow. It rules out the predicted +0.03 (only just), not the idea. A smaller positive effect, about +0.01 to +0.02, fits the data well and is not ruled out: every piece points the same way. Fairly read: the evenly-knit skeleton may help a little, less than predicted, and this pass cannot tell that apart from chance at the corrected threshold.

## Renaming check
Does this measure just repeat others? From `measure_gates10.json`: two-setting stability 0.676 (n 3,999; bar 0.5); R² on the 13 baselines 0.152; the largest baseline correlations are pc_entropy +0.26, n_pitch +0.25, range +0.22. Among the counted measures, its largest overlap is irr_skel (+0.38). Not a rename. With all 13 baselines held the estimate is unchanged (+0.016, reading 3 below), so the baselines do not explain it.
One caution: without pc_entropy held, the sign flips (reading 2). pc_entropy is the REP measure, which passed tonight with a strong negative sign, and pe_h0 rises with it. So the positive effect only appears once entropy is held fixed, as the spec required.

## Frozen readings (estimates only; none passes or kills anything)
1. **Card 1's literal form, pe_h0_inv** (link length 1/p instead of -ln p; pc_entropy held; predicted +; N 14,511): **+0.014**, SE 0.0067, p = 0.040, range +0.001 to +0.027. Same story as the test.
2. **pe_h0 without pc_entropy held** (predicted +; N 14,511): **-0.007**, SE 0.0067, p = 0.28, range -0.020 to +0.006. Wrong sign, near zero.
3. **All 13 baselines held** (predicted +; N 14,511): **+0.016**, SE 0.0071, p = 0.023, range +0.002 to +0.030. The prediction sits on the top edge.

## What it cannot say
- It cannot rule out a positive effect smaller than +0.03.
- The outcome counts artists in TheSession.org's recordings list, which members submit; it reflects what that community logs, not all recordings.
- Most tunes are traditional, so there is no composer to hold fixed; old, well-known tunes may differ in ways the notes do not show.
- The measure reads only the first setting of each tune; its stability (0.68) means transcriber differences add noise, which pulls the estimate toward zero.
- The first-poster effect could not be held (the design carries no username).
- Split A has now been joined to the outcome by eight tests; any new idea from this result should be tested on unseen tunes.
