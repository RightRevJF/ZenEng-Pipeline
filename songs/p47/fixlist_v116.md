# ZenEng fix list after v116

*Songs 40, 42 and 43 rerun on v116, with 356's diagnostic runs on song 43 · findings 365–371 (v116's fixes took 355–364) · with the tests of 310–363 on each song's own runs (321)*

v116's last fix is 364. This list starts at 365. Fixes 355–358 and 360–363 were ported, and songs 40, 42 and 43 were run again with the same lyrics, intakes and seeds. Each song made 1,000 main and 1,000 control builds, each twice; every run reproduced its order. Song 43 also ran with fix 348 off and with fix 354 off, on v116's code and on v115's.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Two fixes could not be ported as written: 359 needs each kept window's key and 364 needs its song, and the kept-window table has neither. The writer chose Q1 A: 359 stays as v115, and 364 groups kept windows by song as runs of adjacent windows with the same year (finding 369). No two fixes conflicted.

## Songs since v116

| Song | Title | What it tested | Survivors, main / control (v115) | Orders, main / control | Fixes found |
|---|---|---|---|---|---|
| 40 | Nothing Else on Earth | v116 on the v115 song: q = 116, 110 bars, straight eighths; the bar-grid unit returns (361) | 701 / 746 (602 / 663) | 4b1447040f6f / b9d46b6ec95e, both reproduced | 365–371 |
| 42 | Nothing Important | v116 on the v115 song: q = 76, 68 bars, one design gate (Q11 note 4) | 759 / 796 (767 / 782) | 80e060723e2c / 1c4ded5ba440, both reproduced | 365–371 |
| 43 | Blue Movie | v116 on the v115 song: dance-pop, q = 118, A minor, 80 bars, the chorus design (Q15 A); 356's two diagnostic runs | 798 / 819 (722 / 803) | a7c8c1fa5f14 / 0d9995e53e79, both reproduced | 365–371 |

## The tests of 310–363 (held means held in the main run and the control)

| Fix | Read against | Song 40 | Song 42 | Song 43 |
|---|---|---|---|---|
| 310 | kept 0.04-0.23 | yes | yes | yes |
| 311 | the rule's own statement (a check) | yes | yes | yes |
| 312 | kept 75th 3.6% | yes | yes | yes |
| 313 | kept 25-70% (median 50%) | yes | yes | yes |
| 314 | kept verse share 40-57%; the rule (a check) | yes | yes | yes |
| 315 | kept 0.00-0.55; the cap (a check) | yes | yes | yes |
| 316 | a reading (335: tries and redraws) | reading | reading | reading |
| 317 | the paper's 317: nine in ten | yes | yes | yes |
| 318 | a reading | printed | printed | printed |
| 319 | n/a here | n/a | n/a | n/a |
| 320 | a check | yes | yes | yes |
| 321 | a check | yes | yes | yes |
| 322 | kept 0.04-0.23 | yes | yes | yes |
| 323 | kept 25-70% | yes | yes | yes |
| 324 | the rule's own statement (a check) | yes | yes | yes |
| 325 | the rule's own statement (a check) | yes | yes | yes |
| 326 | the paper's 317 | yes | yes | yes |
| 327 | a reading (335: a count kept songs do not have) | reading | reading | reading |
| 328 | a reading | printed | printed | printed |
| 329 | kept 8-13; the rule (a check) | yes | yes | yes |
| 330 | kept 0.04-0.23 | yes | yes | yes |
| 331 | kept 25-70% (median 50%) | yes | yes | yes |
| 332 | v110's counts (the paper's test) | yes | reading | reading |
| 333 | the rule's own statement (a check) | yes | yes | yes |
| 334 | a reading | printed | printed | printed |
| 335 | a check | yes | yes | yes |
| 336 | a reading | reading | reading | reading |
| 337 | a reading (main against control) | printed | printed | printed |
| 338 | kept 25-70% (median 50%) | **no** | yes | **no** |
| 340 | a reading (Window 134: 11.0 and 10.4) | printed | printed | printed |
| 341 | kept 54% pushed, 31% in runs | **no** | **no** | **no** |
| 342 | kept 3.6-4.1 (a reading) | printed | printed | printed |
| 343 | kept 4.04 | yes | yes | yes |
| 344 | kept 7.1% | yes | yes | **no** |
| 345 | kept 72% | yes | yes | yes |
| 346 | kept 0.37, 6.4, 0.17/0.19 | **no** | **no** | **no** |
| 347 | the kept mean (340's judge) | **no** | **no** | **no** |
| 348 | kept 54% pushed, 31% in runs | **no** | **no** | **no** |
| 349 | kept 7.1% (4.5% minor) | yes | yes | **no** |
| 350 | kept unit 3 returns 31.5% | yes | **no** | yes |
| 351 | kept 50% (25-70%) | **no** | yes | **no** |
| 352 | a check; kept repeats' middle half printed | amended by 362 | amended by 362 | amended by 362 |
| 353 | the rule's own statement (a check) | n/a | n/a | yes |
| 354 | Table DU | **no** | **no** | **no** |
| 355 | kept 54% / 31%; 9.4% | **no** | **no** | **no** |
| 356 | v112 (40, 42), v114 (43) | **no** | **no** | **no** |
| 357 | Table DU | **no** | yes | **no** |
| 358 | kept 7.1% (4.5% minor) | yes | yes | yes |
| 359 | not ported (Q1 A) | n/a | n/a | not ported |
| 360 | kept 50% (25-70%) | **no** | yes | **no** |
| 361 | kept 31.5%, 18.8% | **no** | **no** | **no** |
| 362 | a check | yes | yes | yes |
| 363 | the paper's 317 with 337's spread | yes | yes | yes |

364 (separability, read across the songs): within the songs 0.968, 0.940 and 0.942 (the same code on v115: 0.965, 0.939, 0.948; Window 136: 0.966, 0.954, 0.942); across songs 0.906 (0.900; 0.909). The full tables, with each run's figures, are in the test report.

## What held

- **358.** Notes outside the scale reached 6.4%, 5.8% and 3.9% (kept 7.1%, minor 4.5%), with tritone-from-root breaks unchanged. It held on all three songs.
- **362.** Every pick breaks no soft limit; between 507 and 669 survivors qualified in each run. The pick was the judge's first, second or third.
- **363.** Song 43's design gate passed 92.1% and 91.2%, with a spread of about one point.
- **Survivors.** Song 40: 701 and 746 (v115 602 and 663). Song 43: 798 and 819 (722 and 803), back beside v114's 811. Rhythm-placement deaths: none on any song.
- **356's diagnostics, on v115's code.** Fix 348 made v115's rhythm-band and memory breaks; fix 354 made none of them (finding 367).

## The fixes

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

## Order of work

1. **365 and 366** (one calibration for the gaps; runs by a draw): together they decide the rhythm measures that cost the most on every run.
2. **369** (the key and the song on the kept-window table): it unblocks 359 and puts 364 on the paper's grouping.
3. **367 and 368** (the rhythm band's quartiles; the memory breaks on song 43).
4. **370** (the refit within the reading's tolerance) and **371** (unit returns on the bar grid at calibrated rates).

## Regression line

After these fixes, songs 40, 42 and 43 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders: song 40 4b1447040f6f / b9d46b6ec95e (seed 20261511); song 42 80e060723e2c / 1c4ded5ba440 (seed 20261552); song 43 a7c8c1fa5f14 / 0d9995e53e79 (seed 20261553). They will change with the code.

What the three songs must keep: the locked lyrics, every syllable sung; song 42's design and song 43's chorus design at nine in ten or more, read with the spread (363); the last chorus on the tonic in every complete build; the pick with no soft break (362); no rhythm-placement deaths.

After 365–371: each gap share within five points of Table DU, main and control; runs within ten points of 31%; 354's knobs moving on song 43; song 43's memory breaks within two spreads of v114's; 359 and 364 read on the table's own key and song; verse 2's share within ten points of 50%; unit returns within ten points of the kept rates.

## Readings the paper does not give

- **355.** The run knob weights a sixteenth-position onset followed by a sixteenth, on a log scale. A second knob weights every onset on a sixteenth position toward the kept 9.4%.
- **356.** The rhythm band's middle half (1.98–2.53) is taken from a normal band fitted to 286's soft limits as its 5th and 95th percentiles. The distinct lengths' middle half is the kept windows' quartiles.
- **357.** A round past the third runs only if a knob moved at full step in the round before.
- **358.** The passing note is a semitone move to a pitch class outside the scale, off the beat, one or two semitones from both neighbours. 215's tritone move leaves it alone, so a copied line keeps it.
- **360.** The refit draws the line again once, with any onset off the copy forbidden in the failed bars.
- **361.** Sections of two-bar lines (songs 42 and 43) keep 350's line plans; song 40 takes the bar grid. A paired line keeps its partner.
- **364.** Kept songs are runs of adjacent windows with the same year: 182 songs. Two-fold, by halves of the kept songs and of the builds; AUC.

## Blind-pick tally

The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40, 41 and 43 are not yet offered. No song was recorded on v116, so there is no new blind pick.
