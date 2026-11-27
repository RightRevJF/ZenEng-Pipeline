# vr4c_momentum: result (ESTIMATE; passes nothing, kills nothing)

Run once after the rules were committed (predictions 379e219, results 687e735). Figures are copied from `result.json`.

## The measure in plain words
Follow the song's roots as steps around the circle of fifths. Drop the "ii" of each ii-V (a minor 7th followed by a dominant 7th a fourth up), merge repeated roots, and compare two ways of measuring wandering: the squared total of every four consecutive steps, against four times the average squared single step. The ratio (VR4c) is about 1 for a random walk, near 0 for a loop that keeps coming home (I-vi-ii-V), and up to 4 for a chain that keeps travelling (a run of fifths). The mathematics is the lead-lag area of card 1: the area of the path sampled every fourth change compared with the area at every change, a variance-ratio idea from quadratic variation. Needs at least 8 steps; 1,245 songs qualify.

## What was predicted (written first)
+0.02 SD per SD of VR4c, holding IIV and V (tunes whose harmony travels get carried by players). Printed power: 0.12 at the 0.05 level. The author withdrew it from the count.

## What came out (1,245 songs)
- Main: b = +0.026, SE 0.027, p = 0.33, 95% range -0.027 to +0.079.
- Halves: +0.022 (N 705, SE 0.035) and +0.034 (N 540, SE 0.042). Same sign.
- Second model (Poisson): +0.062, SE 0.086, p = 0.47.
- Clustering by composer (extra check): +0.026, p = 0.33.
- Frozen reading, VR4 before the ii is dropped (N 1,246, no prediction): b = +0.011, SE 0.026, p = 0.66, range -0.040 to +0.062; halves +0.016 and +0.007; Poisson +0.061, p = 0.46.

## Renaming check
Overlap on the design songs (Spearman): ch_rep -0.35, V 0.58, IIV 0.35 (gate 0.8, passed). V and IIV are held in the model.

## Verdict by the frozen rule
Power was 0.12, under the 0.2 floor: an estimate. It passes nothing and kills nothing. The predicted +0.02 lies inside the 95% range, and the estimate (+0.026) is close to it with the predicted sign, but zero is also inside the range (p = 0.33).

## What it cannot say
It cannot say that travelling harmony is more covered: the estimate is no larger than its own noise. It also cannot rule out an effect up to about +0.08. Dropping the ii made little difference (+0.026 against +0.011, both within noise), so no claim about the ii can be drawn. The root walk ignores rhythm and chord quality, and chart-writer disagreement dilutes any real effect.
