# 749.259, a section remembers its bars: the form, the fit and the marks, before any code or run

28 November 2026, 09:46 ET. From RESULT_count_bars_again.md (a section of ours uses 10 different bar rhythms in its first 16 bars, a pop 3/4 clip 6). Accepted and numbered by the songwriting session (09:31 ET), with how the weight is fitted and the test.

**The form (`LUTHIER_BAR_MEMORY=<weight>`, unset by default):** when a line's rhythm is drawn from the kept windows inside a section, each bar of a candidate window whose rhythm (its onsets within the bar) has already been sung in that section multiplies the window's chance by the weight, as 923 favours a figure already sung. A section starts with no memory; every line set in it, however it was made, adds its bars.
*Settled, mine to answer for:*
- A candidate's bars are read from its own notes from the line's first bar line on; a pickup before the bar line is not counted (it falls in a bar that is not yet complete).
- It acts where the kept windows are drawn and weighed one by one: every metre's draw outside 4/4's all-windows path (912), which is not touched. So 4/4 does not change even with the switch set. The weighted rule (760) and lines sung again are as now.
- The weight enters before the cut to the twelve best, with the stress score and the kept count.

**The fit, decided by the songwriting session before any run, so it is not chosen on the test:**
- Song 55's words, the package of RESULT_seeds_456, at the **seen** seeds 1, 2 and 3, over the grid of weights **2, 4, 8, 16, 32, 64** (written now; none added after).
- For each weight: in each pool build, the median over its sections of 16 sung bars or more of the different bar rhythms in the first 16; then the median over the pool; then the mean over the three seeds. **The weight taken is the one nearest the clips' 6; a tie goes to the smaller weight.**
- The grid's figures and the weight taken are committed in a fit file before any fresh seed runs. Nothing else is tuned.

**The test: fresh seeds 10, 11 and 12, on both seen lyrics (song 55's and song 49's words), 1,000 builds each, the package with the weight taken:**
1. Every mark on the pool's median at each seed: notes a bar 2.38 to 3.85; onsets on a beat 0.508 or more; K3 off the beat 0.26 or under; range 12 or more; pitches 7 or more; K5 0.303 or under; K6 rhythm again within sections 0.349 to 0.871 and figure again 0.667 or under; the share drawn fresh at most 0.076; the chord mark; source lines at least 0.40; late lines at most 0.15 (pool); the pool at least 10. Read as in PREDICTION_seeds_456.
2. The pool on the six like marks at least 76.2 in 100 at each seed, **on both lyrics**.
3. Watched: different bar rhythms in 16 bars against the clips' 6 (4 to 8); exact two-bar repeats against 0.231; K3's first beat (borrowed, lead sheets); 838 (flag over 450); the pick.
4. **If both lyrics pass at all three seeds, pop 3/4 is ready, and songs 68 and 69 run together** (when the songwriting session says so). If not, it is reported as missed.
5. The switch acts only where set: the five 6/8 lyrics on song 69's package come out byte for byte the same with it unset; every switch unset, 54, 55, 52 and song 53's Essen arm byte for byte; room files after. Song 69's package does not change.

A reading tool gains one figure before the run (not the engine): `pool_count.py` prints the different bar rhythms in a section's first 16 bars.

## What I expect
- The fit lands at a weight of 8 or 16.
- With it, K6 rhythm again within sections rises to 0.5 to 0.65 on the pool's median and the six-mark share clears 76.2 on song 55's words at all three seeds. On song 49's words I am less sure: its sections are shorter. **Both lyrics at all three seeds: a little better than an even chance.**
- What it may cost: K3 off the beat rises (a remembered bar chosen over a better-fitting one), staying under 0.26; fewer different rhythms may raise deaths on 840 for title lines a little. If a mark breaks, I expect it to be one of those two, or the share of living builds falling.
