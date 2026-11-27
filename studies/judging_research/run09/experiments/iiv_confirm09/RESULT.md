# iiv_confirm09: result (plain language)

**Verdict by the rule written first: UNSETTLED.** No pass, and no kill. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 379e219; results commit 687e735. The question: do songs with more "ii-V" chord moves (a minor seventh chord moving to a dominant seventh a fourth up) get covered by more distinct artists? This was checked on 1,271 songs never before joined to an outcome. Prediction: **+0.05** standard deviations of cover-count per standard deviation of ii-V share. Pass needed p < .05, a positive effect in both halves, and a positive second-model (Poisson) coefficient. Kill: +0.05 outside the 95% range. Power was printed before the outcome was joined: **0.367** (below run 08's own 0.5 suggestion, above the 0.2 floor). A non-pass at this power is weak evidence.

## What came out
- Estimate **-0.0005**, standard error 0.028, p = 0.986. 95% range **-0.055 to +0.054**.
- Halves: -0.015 (N 719) and +0.020 (N 552). Not both positive.
- Second model (Poisson): +0.100, SE 0.075, p = 0.18.
- Clustering by composer (reported, decides nothing): SE 0.030, p = 0.987.

The estimate is essentially zero. It fails the pass rule (p, one half negative). It escapes the kill only because the range is wide: +0.05 sits just inside the top edge (+0.054).

## How firm
Not firm. The data are consistent with no effect and also with the predicted size. Power was about 37%, so a true +0.05 would usually have been missed. Fairly read: the lead did not reproduce, and it is not ruled out.

## Renaming check
Does this measure just repeat others? In the measure gate file, its rank correlation with chord repetition (ch_rep) is -0.28 pooled (-0.18 within genre), and with distinct chords (V) +0.50 pooled (+0.45 within genre). Moderately related, not a rename; both are held constant in the model.

## Frozen readings (estimates only; none passes or kills anything)
1. **Non-jazz genres** (N 831), predicted +0.04, power 0.19: estimate **-0.049**, SE 0.033, p = 0.14, range -0.114 to +0.015. Halves -0.021 and -0.068; Poisson -0.065 (p = 0.20). +0.04 lies outside the range, so by the frozen rule the label is **"jazz repertoire"**. Caution: this is under the power floor, and the BiaB corpus mixes jazz with pop, folk and country.
2. **Real Book and BiaB charts only** (N 553), predicted +0.035, power 0.113: estimate **-0.001**, SE 0.042, p = 0.98, range -0.084 to +0.082. Halves +0.017 and -0.002; Poisson +0.059 (p = 0.37). Prediction inside the range; nothing learned.
3. **Unframed readings (no prediction, no power; they decide nothing):**
   - Name-matched songs only (N 297): +0.063, SE 0.063, p = 0.32; halves +0.119 and -0.008.
   - Chart provenance only (N 1,075): +0.003, SE 0.030, p = 0.91.
   - **Jazz genre only (N 440): +0.104, SE 0.048, p = 0.031**, range +0.010 to +0.199; halves +0.060 and +0.147; Poisson +0.388 (p = 0.003); composer-clustered p = 0.047. This is the only nominally significant figure. It is one of five readings, was not predicted, and is a post hoc subgroup picked out by the contrast with the non-jazz reading. Treat it as a lead for a new test on new songs, not a finding.

## What it cannot say
- The comparison is across composers, so a composer's fame is not held fixed.
- 985 of the 1,271 songs are matched to charts by title alone; wrong matches pull the effect toward zero.
- "Upstream" charts here are mostly not upstream of covering (the Real Book came from canonical recordings).
- Low power means this cannot confirm or reject a true effect near +0.05.
- The jazz-only pattern may be a genre difference, a chance finding, or a matching artifact.
