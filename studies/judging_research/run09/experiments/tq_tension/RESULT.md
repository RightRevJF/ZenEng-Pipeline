# tq_tension: result (ESTIMATE; passes nothing, kills nothing)

Run once after the rules were committed (predictions 379e219, results 687e735). Figures are copied from `result.json`.

## The measure in plain words
For each chord change, ask one question: does the chord contain a tritone (two notes six semitones apart, the "tense" interval)? That gives a 0/1 line along the song. TQ asks how often that line flips between tense and not tense, per chord change. The mathematics behind it is the lead-lag transform of path signatures (card 1): pair each value with the next one, and the area the path sweeps out equals half the quadratic variation, i.e. half the count of flips. The code checks this identity on every chart. So TQ is, in effect, "how much does a song breathe in and out of tension".

## What was predicted (written first)
Holding the ii-V measure (IIV) and V, each extra SD of TQ goes with +0.01 SD more covers. Frozen reading: without IIV held, +0.03. Printed power beforehand: 0.037 (reading 2: 0.13), at the 0.05 level. The author and Skeptic froze it as an estimate.

## What came out (1,271 songs)
- Main: b = -0.007, SE 0.030, p = 0.81, 95% range -0.065 to +0.051.
- Halves (by composer key): -0.002 (N 719, SE 0.040) and -0.027 (N 552, SE 0.046). Both small, both negative.
- Second model (Poisson on number of artist sets): -0.014, SE 0.062, p = 0.82.
- Clustering by composer (extra check): -0.007, p = 0.81.
- Frozen reading, TQ without IIV (predicted +0.03, power 0.13): b = -0.007, SE 0.028, p = 0.81, range -0.062 to +0.049; halves -0.006 and -0.017; Poisson +0.020, p = 0.75.

## Renaming check
Overlap with the controls on the design songs (Spearman): ch_rep -0.29, V 0.36 (gate is 0.8, passed). With IIV 0.55: this is why IIV is held; much of TQ tracks dominant-chord density.

## Verdict by the frozen rule
Power was 0.037, far under the 0.2 floor, so this is an estimate. It passes nothing and kills nothing. The predicted +0.01 sits inside the 95% range (and so does +0.03 for the second reading), but so does zero and so do effects of about +/-0.05, so that is not support.

## What it cannot say
Nothing here shows tension breathing matters, nor that it does not. The range is wide relative to the effects the prediction was about; a test this size could not have told +0.01 from 0 whatever happened. The measure counts only whether a tritone is present, not how it resolves. The outcome (log of 1 + number of distinct artist sets that covered the song) depends on chart writers, whose agreement with each other is imperfect, which dilutes any real effect.
