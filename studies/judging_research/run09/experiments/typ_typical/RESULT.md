# typ_typical: result (ESTIMATE; passes nothing, kills nothing)

Run once after the rules were committed (predictions 379e219, results 687e735). Figures are copied from `result.json`.

## The measure in plain words
Each chart's chord path (time, circle-of-fifths position, tension, major/minor quality) is summarised by six Lévy areas, which record how pairs of these dimensions sweep around each other: a level-2 path signature (card 1). Each area is compared against all charts of the same broad genre (jazz, pop, BiaB, Wikifonia, other; reference sizes 14,651 / 7,346 / 4,965 / 2,398 / 2,155). TYP is how far out the chart sits from the genre's centre, averaged over the six areas: 0 is typical, 1 is at the edge. The second reading, TYPM, does the same with one combined (Mahalanobis) distance that allows for correlated areas.

## What was predicted (written first)
-0.02 SD per SD of TYP: typical songs covered more (stabilising selection on copies). Frozen reading TYPM, also -0.02. Printed power: 0.067 (TYPM 0.087) at the 0.05 level. The author withdrew it from the count.

## What came out (1,271 songs)
- Main: b = +0.0004, SE 0.029, p = 0.99, 95% range -0.057 to +0.058.
- Halves: -0.012 (N 719, SE 0.038) and +0.022 (N 552, SE 0.046). Opposite signs, both small.
- Second model (Poisson): +0.044, SE 0.082, p = 0.59.
- Clustering by composer (extra check): +0.0004, p = 0.99.
- Frozen reading TYPM (predicted -0.02, power 0.087): b = +0.007, SE 0.028, p = 0.82, range -0.049 to +0.062; halves +0.003 and +0.026; Poisson +0.076, p = 0.38.

## Renaming check
Overlap on the design songs (Spearman): ch_rep -0.17, V 0.58 (pooled; 0.62 within genre), IIV 0.31 (gate 0.8, passed). Two-chart stability is the lowest of the batch (0.69 for TYP, 0.76 for TYPM), so the measure is itself noisy.

## Verdict by the frozen rule
Power was 0.067, under the 0.2 floor: an estimate. It passes nothing and kills nothing. The predicted -0.02 is inside the 95% range (as for TYPM), but so is zero and so is +0.05. The point estimate is essentially zero.

## What it cannot say
It cannot say that typical songs are or are not covered more. The estimate is flat, but the range is far wider than the effect predicted. TYP is only as typical as the genre labels and reference charts make it, and it is noisy between two charts of the same song. It describes a path summary, not how the song sounds.
