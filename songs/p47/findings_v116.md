## Findings

### 365. Two calibrations aim the same gaps, and the eighth gaps are now the costliest measure.

**Problem:** The gaps between onsets are set twice. 249's pool knobs (gap16, gap8, gap4) are set on aimed builds toward the pool's medians. 354's knobs (s16, g8, g4, glong) are set on unaimed builds toward Table DU. Each calibration moves its own knobs against the other's.

**Evidence:**

- **The pool knobs at their floors.** In all six runs, 249's gap16 knob ended at its floor of 0.02 (under v115 it was 0.06–0.33). Its gap8 knob ended at or near its floor of a third (0.33–0.44).
- **The 354 knobs moving against them.** Over the rounds the g8 knob fell (song 40 main 1.04 → 0.83, control to 0.54), yet the eighth-gap share read on the unaimed builds rose (song 40 main 53% → 63%).
- **Eighth gaps over the target on two songs.** In the main runs they were 63.8% on song 40 and 58.2% on song 43, against Table DU's 55% and 50%.
- **The costliest measure everywhere.** Eighth gaps cost the most on all six runs: 2.68, 1.79 and 1.78 points in the main runs, 5.21, 3.45 and 2.75 in the controls.
- **Knock-on on song 40.** Song 40's off-beat eighth now costs 2.53 (v115 0.36), and its content median on the judge of record fell from 0.71 to 0.22.

357 held only on song 42. The calibration stopped after three rounds on song 40's main run, because no knob was moving at full step.

**Fix:** One calibration per measure. Retire the gap pairs (gap16, gap8, gap4) from 249's aimed calibration and leave the gaps to 354's knobs, read on unaimed builds.

**Check:** 249's gap knobs no longer move. Each gap share is within five points of Table DU's in the main run and the control on all three songs.

### 366. A run is taken wherever its weight is above zero, so the run knob cannot set the share.

**Problem:** A line's rhythm takes the first drawn landing with any placement at all. When the run weight is above zero, a landing that fits only with a run is accepted on the first try. When the weight was zero, such a landing failed, and another landing was drawn that fits without one. The share of runs is therefore set by which landings are drawn, not by the size of the weight.

**Evidence:** The run knob of 355 fell from 0.01 to between 1×10⁻⁷ and 3×10⁻⁴ over the rounds, by up to five orders of magnitude. Runs stayed at 52%, 41% and 46% in the main runs (39%, 48% and 39% in the controls), against the kept 31%. In a 20-build test on song 43, with every other knob as calibrated, a knob of 5×10⁻⁵ gave 58% in runs and a knob of exactly 0 gave none. Song 43 had no rhythm-placement deaths under v115, so placements without a run existed. 355 held on no song. Only song 40's control met all three of its figures (54% pushed, 39% in runs, 8.2% on a sixteenth).

**Fix:** Decide runs by a draw, not a weight. Each line is drawn as "may run" at a rate set on unaimed builds toward the kept 31%. A line that may not run is placed with a run weight of zero, and falls back to runs only when no landing fits (counted).

**Check:** Runs within ten points of 31% and pushes within ten of 54% in the main run and the control. Fallback lines printed.

### 367. 356's stop fires on song 43 before any 354 knob moves, on a band the tables do not give.

**Problem:** 356 stops the 354 knobs when the rhythm band's bits leave the kept middle half. The tables give only the band's 5th and 95th percentiles (286: 1.58 and 2.93). The port took the middle half of a normal band fitted to them (1.98–2.53), and song 43's unaimed builds read 2.68 before the first step.

**Evidence:**

- **Song 43:** the 354 knobs stopped in round 1 at 1.0, in the main run.
- **The 354-off diagnostic:** it reproduced the main run exactly (order a7c8c1fa5f14, 798 survivors).
- **Songs 40 and 42:** the stop never fired.
- **356's diagnostics on v115's code**, which is where the breaks were made: v115's song 43 had 722 survivors, 150 rhythm-band breaks and 323 memory breaks.
  - With 348 off: 797 survivors, 0 rhythm-band breaks, 78 memory breaks.
  - With 354 off: 688 survivors, 122 rhythm-band breaks, 292 memory breaks.
  - So fix 348 made v115's rhythm breaks; fix 354 made none of them.
- **Under v116** the rhythm-band breaks are back near before: 1 (v112 2) on song 40, 12 (6) on song 42 and 7 (v114 0) on song 43.

**Fix:** Give the rhythm band's kept quartiles: the POP909 pairs of 286, or the 314 kept windows read by the same code. Read 356's stop against them. Until then, the stop is a reading and does not move the knobs.

**Check:** 356's band is printed with its source. On song 43 the 354 knobs move in round 1, or the stop is shown to fire against the kept quartiles.

### 368. Song 43's memory breaks are still about double v114's, and the cause lies outside fixes 348 and 354.

**Problem:** One of v116's own fixes is breaking 286's memory limit on song 43. The diagnostics rule out 348 (with 355) and 354.

**Evidence:** Memory breaks were 125 in song 43's main run against v114's 65 (a spread of 13, so 4.6 spreads), and 68 against 32 in the control. With 348 and 355 off they were 132; with 354 off, 125 (354 is inert here, 367). Song 40's memory breaks fell (17 against v112's 60) and song 42's fell (47 against 77). The memory reading is melodic (the horizon over the verse and the chorus). The fixes that touch the pitches on song 43 are 358, which placed 4,896 chromatic passing notes, and 361.

**Fix:** Run song 43 twice more, with 358 off and with 361 off (both switches are in the port), to find the share of each.

**Check:** Memory breaks on song 43 within two spreads of v114's 65, or the fix responsible is named.

### 369. Fixes 359 and 364 need two columns the kept-window table does not have.

**Problem:** 359 reads a minor song against the 70 kept minor windows, and 364 holds out kept songs. The kept-window table (zeneng_v105_kept_windows.json) carries year and section, but no key and no song. 359 was not ported. 364 grouped windows by song as runs of adjacent windows with the same year (the writer's Q1 A).

**Evidence:**

- **The inferred grouping finds 182 kept songs.** On the v115 builds it gives within-song separation of 0.965, 0.939 and 0.948, and 0.900 across songs. The paper's own figures are 0.966, 0.954 and 0.942, and 0.909. So the grouping is close, but it is not the paper's grouping.
- **Under v116** the same code reads 0.968, 0.940 and 0.942 within the songs, and 0.906 across them. The builds are no harder to tell from kept windows than under v115.
- **The cost of 359 not being ported.** Song 43's outside-scale share holds 349's minor target (3.9% against 4.5%), yet costs 0.84 on a judge fitted against all 314 windows (mean 7.1%).

**Fix:** Add two columns to the kept-window table: the key's mode, and a song identity. Then port 359 as written, and read 364 on the paper's grouping.

**Check:** 359's costs on song 43 are read against the 70 minor windows. 364's figures for v115 reproduce the window's 0.966, 0.954, 0.942 and 0.909.

### 370. Fix 360's refit rarely keeps a bar, and verse 2's share has not moved.

**Problem:** A failed bar is fitted again with the copy's onsets required. Verse 2's syllables seldom match verse 1's bar for bar, so the strict fit usually fails too.

**Evidence:**

| Song | Bars kept by the refit | Verse 2's median share (v115) | 331's rate |
|---|---|---|---|
| 40 | 1,103 of 12,135 (9%) | 0.33 (0.33) | 1.0 |
| 42 | 1,024 of 8,000 (13%) | 0.50 (0.44) | 0.81 |
| 43 | 502 of 10,195 (5%) | 0.29 (0.25) | 1.0 |

360's test held on song 42 only. 338's failed on songs 40 and 43.

**Fix:** Refit within the reading's own tolerance: the copy's onsets, with one onset added or dropped at the bar's weakest place, as 323 does for a bar one over the cap.

**Check:** Verse 2's median share within ten points of 50% in the main run on all three songs. Bars kept by the refit printed.

### 371. Unit returns drawn at the kept rates read well under them.

**Problem:** The kept rates are readings: a return counts only when a unit's onsets overlap by 60% and its contour correlates by 0.6. Drawing a return at the kept rate yields fewer counted returns than that rate. Some draws are lost before they are made. My port also kept 350's line plans in sections of two-bar lines, rather than the bar grid.

**Evidence:**

- **Song 40 (bar grid):** 1,363 returns drawn in the main run. 419 fell under a paired line (310 kept its partner) and 93 were given up. Unit 3 returning unit 1 reads 14.8% against 31.5%; unit 4 returning unit 2 reads 3.9% against 18.8%.
- **Songs 42 and 43 (line plans):**
  - Unit 4 returning unit 2 reads 0.9% and 12.9%.
  - Unit 3 returning unit 1 reads 42.7% on song 42 (11 points over) and 14.8% on song 43.

361 held on no song.

**Fix:** Draw unit returns on the bar grid in every section, at rates set on unaimed builds toward the kept readings (as 355's knobs are), not at the readings themselves. A drawn unit return takes precedence over 310's pairing for the bars it covers.

**Check:** Unit 3 returning unit 1 and unit 4 returning unit 2, each within ten points of the kept rate on all three songs.
