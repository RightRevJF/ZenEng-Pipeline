# irr_skeleton: result (ESTIMATE; passes nothing, kills nothing)

Run once after the rules were committed (predictions 379e219, results 687e735). Figures are copied from `result.json`.

## The measure in plain words
Walk through the song's chord changes and cancel every "there and straight back" move: A, B, A collapses to A. What remains is the irreducible skeleton of the progression. IRR is the skeleton's length divided by the number of changes: a vamp like C G C G scores 0, a progression that never retraces (A B C A) scores 1. The mathematics is the uniqueness theorem for path signatures (Hambly-Lyons, card 1): a signature determines a path only up to tree-like back-and-forth excursions, so a "tree-reduced path" is what the signature truly sees. The author's own caveat: the count is a simple stack reduction, roughly 1 minus twice the local back-and-forth share; the theorem supplies the name, not the proof of anything about music.

## What was predicted (written first)
+0.02 SD more covers per SD of IRR (retracings are scaffolding, the skeleton is what is remembered). Printed power: 0.067 at the 0.05 level. The author withdrew it from the count in round 2, and the chair respected that.

## What came out (1,271 songs)
- Main: b = -0.060, SE 0.029, p = 0.043, 95% range -0.117 to -0.002.
- Halves: -0.062 (N 719, SE 0.039) and -0.043 (N 552, SE 0.044). Same sign in both.
- Second model (Poisson): -0.152, SE 0.067, p = 0.023.
- Clustering by composer (extra check): -0.060, SE 0.032, p = 0.064.
- Frozen reading, chart-provenance songs only (N 1,075, no prediction, no power printed): b = -0.055, SE 0.033, p = 0.098, range -0.119 to +0.010; halves -0.067 and -0.021; Poisson -0.145, p = 0.034.

## Renaming check
Overlap on the design songs (Spearman): ch_rep -0.29, V 0.53, IIV 0.35 (gate 0.8, passed). Partly a renaming of back-and-forth repetition, as the chair noted.

## Verdict by the frozen rule
Power was 0.067, under the 0.2 floor, and the measure was withdrawn: an estimate. It passes nothing and kills nothing. The predicted +0.02 is NOT inside the 95% range.

## Something to watch, not a finding
The sign is opposite to the prediction and p is just under .05 (0.043; 0.023 in the Poisson model). It was not counted, power was 0.067, and clustering by composer gives p = 0.064 with a range that includes zero. A result this marginal, from a test designed to detect only +0.02, is as likely to be noise as signal. Mild support: both halves agree in sign and the chart-provenance subset points the same way (p = 0.098). Any follow-up would need its own frozen prediction on new songs.

## What it cannot say
It cannot say that retraced harmony helps covers or that skeletons hurt them. IRR is partly a back-and-forth (vamp) count, tangled with other simplicity measures, and the outcome depends on chart writers.
