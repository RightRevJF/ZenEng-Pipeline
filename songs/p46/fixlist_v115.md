# ZenEng fix list after v115

*Songs 40, 42 and 43 rerun on v115 · findings 355–363 (v115's fixes took 348–354) · with the tests of 310–354 on each song's own runs (321)*

v115's last fix is 354. This list starts at 355. v115's fixes 348–354 were ported, and songs 40, 42 and 43 were run again with the same lyrics, intakes and seeds before any new song. Each song made 1,000 main and 1,000 control builds, each twice; every run reproduced its order.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. One fix could not be ported as written: 348 left song 40's Bridge line 3 with no placement (0 of 100 builds). The writer chose to let drawn lines with no room run sixteenths (Q1 A). No two fixes conflicted.

## Songs since v115

| Song | Title | What it tested | Survivors, main / control (before) | Orders, main / control | Fixes found |
|---|---|---|---|---|---|
| 40 | Nothing Else on Earth | v115 on the v112 song: q = 116, 110 bars, straight eighths | 602 / 663 (v112: 544 / 544) | 2a9550248f1b / c5344a86edce, both reproduced | 355–363 |
| 42 | Nothing Important | v115 on the v112 song: q = 76, 68 bars, one design gate (Q11 note 4) | 767 / 782 (v112: 747 / 738) | 03a4f13efa50 / 1c46ba2167ca, both reproduced | 355–363 |
| 43 | Blue Movie | v115 on the v114 song: dance-pop, q = 118, A minor, 80 bars, the chorus design (Q15 A); the first run with the minor reading (353) | 722 / 803 (v114: 811 / 819) | 97c7c92a9619 / 4f2f64f2a00e, both reproduced | 355–363 |

## The tests of 310–354 (held means held in the main run and the control)

| Fix | Read against | Song 40 | Song 42 | Song 43 |
|---|---|---|---|---|
| 310 | kept 0.04-0.23 | yes | yes | yes |
| 311 | the rule's own statement (a check) | yes | yes | yes |
| 312 | kept 75th 3.6% | yes | yes | yes |
| 313 | kept 25-70% (median 50%) | yes | yes | yes |
| 314 | kept verse share 40-57%; the rule (a check) | yes | yes | yes |
| 315 | kept 0.00-0.55; the cap (a check) | yes | yes | yes |
| 316 | a reading (335: tries and redraws) | reading | reading | reading |
| 317 | the paper's 317: nine in ten | yes | yes | **no** |
| 318 | a reading | printed | printed | printed |
| 319 | n/a here | n/a | n/a | n/a |
| 320 | a check | yes | yes | yes |
| 321 | a check | yes | yes | yes |
| 322 | kept 0.04-0.23 | yes | yes | yes |
| 323 | kept 25-70% | yes | yes | yes |
| 324 | the rule's own statement (a check) | yes | yes | yes |
| 325 | the rule's own statement (a check) | yes | yes | yes |
| 326 | the paper's 317 | yes | yes | **no** |
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
| 341 | kept 54% pushed, 31% in runs | yes | **no** | **no** |
| 342 | kept 3.6-4.1 (a reading) | printed | printed | printed |
| 343 | kept 4.04 | yes | **no** | **no** |
| 344 | kept 7.1% | **no** | **no** | **no** |
| 345 | kept 72% | yes | yes | yes |
| 346 | kept 0.37, 6.4, 0.17/0.19 | **no** | **no** | **no** |
| 347 | the kept mean (340's judge) | **no** | **no** | **no** |
| 348 | kept 54% pushed, 31% in runs | yes | **no** | **no** |
| 349 | kept 7.1% (4.5% minor) | **no** | **no** | **no** |
| 350 | kept unit 3 returns 31.5% | **no** | **no** | yes |
| 351 | kept 50% (25-70%) | **no** | **no** | **no** |
| 352 | a check; kept repeats' middle half printed | yes | yes | yes |
| 353 | the rule's own statement (a check) | n/a | n/a | yes |
| 354 | Table DU | **no** | **no** | **no** |

The full tables, with each run's figures, are in the test report.

## The fixes

### 355. Fix 348 leaves no sixteenth runs, and its test cannot see it.

**Problem:** With a sixteenth-position onset allowed only as a push, the runs are gone. 348's test sets only a floor on pushes and a ceiling on runs, so it holds while the shape is still far from the kept one.

**Evidence:** Of onsets on a sixteenth position, 99–100% were pushed and 0–1% were in runs on all six song-runs, against the kept 54% and 31%. In the main runs, the share of onsets on a sixteenth position rose past the kept 9.4%: 16.9% on song 40, 13.9% on song 42 and 14.2% on song 43. It is now the costliest measure on songs 40 and 42 (2.56 and 1.40 points) and the second costliest on song 43 (1.49). "Rhythm: no placement" killed 125 of song 40's builds in the main run and 114 in the control. Q1 A let 1,552 drawn lines with no room run sixteenths, but these are bridge lines, which the window measures do not read.

**Fix:** In a drawn line, draw runs at the kept rate: about one in three sixteenth-position onsets inside a run of two or more. The other sixteenth-position onsets stay pushes. Make 348's test two-sided.

**Check:** Pushed within 10 points of 54% and runs within 10 points of 31%. The share of onsets on a sixteenth position within two points of 9.4%, costing under half a point. Rhythm-placement deaths under 5%.

### 356. The v115 rhythms break 286's rhythm limits and cost song 43 a tenth of its survivors.

**Problem:** v115's rhythms carry more information than the kept band allows, and builds now die or pick up soft breaks on 286's rhythm band.

**Evidence:** Soft breaks on the rhythm band rose from 2 to 139 on song 40, from 6 to 116 on song 42 and from 0 to 150 on song 43, in the main runs. On song 43, the rhythm band's bits rose at the median from 2.26 to 2.49, and 6.2% of survivors now sit above the soft top of 2.93 (before, none). In the same runs:

- memory breaks rose from 65 to 323;
- breaks on the most lengths in eight bars rose from 6 to 46;
- distinct note lengths rose from 4.07 to 4.78, against the kept 4.04;
- 343's test failed for the first time (median distinct lengths 5, cost 0.50 in the main run and 0.98 in the control).

Song 43's survivors fell from 811 to 722, about 4.7 times 337's spread of 19. Three of the six picks carry the rhythm-band soft break (songs 40, 42 and 43, main runs). The cause is not yet separated: either 348's pushes (a push adds a length of a sixteenth and its partner) or 354's knobs (g4 at 2.6–2.9 and glong at 0.9–1.9 in the main runs).

**Fix:** Read the rhythm band's bits and the distinct lengths in 338's calibration. Stop a 354 knob from moving further when either leaves the kept middle half. Then run song 43 once with 348 off and once with 354 off, so the share each one causes is known.

**Check:** Rhythm-band soft breaks back within 337's spread of v114's counts. 343 held. Song 43's survivors within the spread of 811.

### 357. Fix 354's knobs reach the gap targets in no run.

**Problem:** The calibration moves each gap knob at most by a factor of 1.6 a round. In the control the knobs move at full step every round and still miss. In the main run the knob that meets the sixteenth-gap target overshoots the sixteenth onsets (355).

**Evidence:** 354 held on none of the six song-runs:

- **Song 40:** in the main run, eighth gaps were 49.3% against the band's 55% (5.7 points off).
- **Song 42:** the gap shares were all within five points, but eighth gaps cost 0.55 in the main run.
- **Song 43:** the main run held; in the control, eighth gaps cost 0.71.

In the controls of songs 42 and 43, s16 ended at 4.096, which is 1.6 cubed: full step on each of three rounds. g8 ended near 0.55. Even so, sixteenth gaps were 5.4% and 6.8% against Table DU's 14% and 11%, and eighth gaps were 58.8% and 53.9% against 55% and 50%, costing 1.84 on song 42 and 0.71 on song 43. Song 40's control did the same (s16 3.67, eighth-gap cost 2.1). Without runs (355), each sixteenth gap needs a sixteenth-position onset of its own, so the sixteenth gaps and the sixteenth onsets cannot both reach their kept figures.

**Fix:** After 355, let the calibration keep going while a knob is still moving at full step, up to six rounds, and print the rounds. Aim the sixteenth-gap knob and the sixteenth-onset share together: stop s16 when the onset share passes its kept figure.

**Check:** Each gap share within five points of Table DU's target for the song's notes a bar, and eighth gaps under half a point, in both the main run and the control.

### 358. Fix 349's placement is held back by fix 200's rule.

**Problem:** An outside note is placed only where fix 200's harmonic rule allows it: no clash with the chord, no tritone to the root, and no tritone or interval over 9 to either neighbour. Almost every place fails those tests, so the share stays well under the kept figure whatever its weight.

**Evidence:**

- **Song 40:** 3,770 notes were placed and 70,628 places were wanting. The outside-scale share was 2.9% (control 3.0%) against the kept 7.1%, costing 0.77 (1.05).
- **Song 42:** 2.8% (2.9%), costing 0.74 (0.61).
- **Song 43:** 0.9% against the kept 4.5% for a minor song. It is the costliest measure there (2.62, control 2.86). 344's knob rose at full step to 8.0 without effect.

**Fix:** Also allow an outside note that moves by step to both neighbours (a chromatic passing or neighbour note), on a weak eighth or a sixteenth, whatever the chord. Keep fix 200's rule for notes on the beat.

**Check:** The outside-scale share within two points of 7.1% (4.5% for a minor song), costing under half a point. No rise in tritone-from-root breaks beyond 337's spread.

### 359. Fix 353 reads the minor song's builds on its tonic, but the kept side is unchanged.

**Problem:** The window measures of a minor song are now read on its own tonic with the natural minor scale. The judge's kept means are still one set for every song, and so are 349's targets apart from the 4.5%.

**Evidence:** On song 43, the judge read the outside-scale share against the kept 0.071, while 349 sets 4.5% for a minor song. The share of lines ending on the tonic fell from 14.4% (read on C under v114) to 6.9% (read on A), against the kept 27.7%. It now costs 0.53 in the main run and 0.62 in the control, where under v114 it was not among the eight costliest measures. In song 43's control, the content judge's median fell from 0.96 to 0.33.

**Fix:** Read the kept windows of minor-key songs by the same rule (on their tonic, natural minor) and keep a second set of means for minor songs. The judge reads a minor song against that set. If the kept minor windows are too few to fit, say how many there are.

**Check:** For a minor song, the judge's kept means for the outside-scale share and the tonic ending come from the minor set. The tonic-ending cost is under half a point.

### 360. Fix 351 lowers verse 2's share, and 331's rate cannot raise it.

**Problem:** A bar left out of a copy is a bar that does not return. Far fewer lines are now given up, but verse 2 returns less of verse 1. The copy rate that 331 moves is already at its ceiling.

**Evidence:** Copies given up fell from 2,353 lines to 41 on song 43, and are 110 (1.8%) on song 40 and 6 (0.2%) on song 42. Bars left out came to 10,319, 8,419 and 10,662 in the three main runs. Verse 2's median share fell on every song:

| Song | Main run | Control |
|---|---|---|
| 40 | 0.36 → 0.33 | 0.45 → 0.33 |
| 42 | 0.50 → 0.44 | 0.50 → 0.38 |
| 43 | 0.50 → 0.25 | 0.50 → 0.25 |

331's rate ended at 0.983 and 1.0 on song 40 and at 1.0 on song 43. 351's test failed on all three songs, and 338's on songs 40 and 43 (on song 43 for the first time).

**Fix:** Before leaving a bar out, fit it again as 327 does (the copy kept, the bar's rhythm refitted to the words). Leave it out only if that fails. Count left-out bars against verse 2's share when 331 sets the rate.

**Check:** Verse 2's median share within 10 points of 50%. Lines given up under one in ten. Bars left out printed.

### 361. Unit returns are drawn only in sections whose lines are all two bars (the port).

**Problem:** My port of 346 and 350 treats a unit as a line. It draws a return only where every line of the section is two bars. Song 40's sections are not, so it draws none.

**Evidence:**

- **Song 40:** no unit return was drawn in either run. Unit 4 returning unit 2 reads 0.9% (control 0.3%) against the kept 18.8%, costing 0.62 (0.80).
- **Song 42:** line 4 returned line 2 in 123 builds; the measure reads 1.4% (0.8%), costing 0.57 (0.76).
- **Song 43:** unit 3 now returns unit 1 at 15.1% (v114 none). Its cost fell from 1.48 to 0.09, and unit 4 returning unit 2 costs −0.01.

350 held only on song 43.

**Fix:** Draw unit returns on the section's two-bar units, read on the bar grid, whatever the line lengths. A unit that starts inside a line copies the earlier unit's rhythm and contour from that point.

**Check:** No unit return over half a point on songs 40 and 42. Unit returns printed by unit, not by line.

### 362. The judge's first breaks soft limits and sits outside the kept repeats.

**Problem:** 352 makes the pick the judge's first. On these runs the judge's first is far from the composite's first, usually carries a soft break, and its repeats fall outside the kept middle half.

**Evidence:**

- **The two orders disagree.** The composite's first ranked 294th to 602nd of the judge's order; on song 40's main run it was last of 602. The judge's first ranked 57th to 707th on the composite. The picks' composite scores were 0.45–0.75, against 0.86–0.90 for the composite's first.
- **Soft breaks.** Five of the six picks carry a soft break: the rhythm band on three, plus spectral, surprisal and memory.
- **Repeats.** In five of six runs, a pick's verse or chorus repeat falls outside the kept middle half (verse 0.14–0.39, chorus 0.13–0.40): song 40 verse 0.07 (control 0.125); song 42 verse 0.548 and chorus 0.062; song 43 chorus 0.10 (control verse 0.41).
- **Lift.** On song 40's main pick, the chorus has no lift over the verse (median 0, top 0). On song 43's control pick, the chorus sits 4 semitones under the verse at the median.

**Fix:** Pick the judge's first among the survivors with no soft break, a repeat inside the kept middle half, and the chorus lifted over the verse at the median. Print how many survivors qualify. If none do, take the judge's first and say so.

**Check:** The pick has no soft break and its repeats fall inside the kept middle half. Its rank on the composite is printed.

### 363. 317's test is read without 337's spread.

**Problem:** A design gate's pass rate is read against nine in ten with no spread, so a run can fail it on noise.

**Evidence:** Song 43's design gate passed 91.3% in the main run (v114 93.0%) and 89.7% in the control (v114 90.2%). The control is 0.3 points under the line, against a spread of about one point at 1,000 builds. 317 and 326 failed on song 43 for the first time. Design deaths rose from 69 to 86 (main) and from 98 to 103 (control), inside the spread.

**Fix:** Read 317 with 337's spread. A rate is under nine in ten when it is more than one spread below 0.9.

**Check:** 317 is printed with its spread. It holds on song 43 at today's rates and fails at 88% or lower.

## Order of work

1. **355, 357 and 356** (the rhythm of sixteenths, the gap knobs, and the rhythm limits): one knot. Runs at the kept rate should let the gap targets be met without the sixteenth onsets overshooting, and the rhythm-band breaks should be read again after that.
2. **362** (the pick): it decides which build becomes the song; five of six picks carry a soft break.
3. **360** (verse 2's share after 351).
4. **358 and 359** (outside notes, and the kept side of a minor song).
5. **361** (unit returns on two-bar units; a port fix).
6. **363** (317 read with its spread).

## Regression line

After these fixes, songs 40, 42 and 43 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders: song 40 2a9550248f1b / c5344a86edce (seed 20261511); song 42 03a4f13efa50 / 1c46ba2167ca (seed 20261552); song 43 97c7c92a9619 / 4f2f64f2a00e (seed 20261553). They will change with the code.

What the three songs must keep: the locked lyrics, every syllable sung; song 42's design and song 43's chorus design at nine in ten or more (read with the spread, 363); the last chorus on the tonic in every complete build.

After 355–363: pushes and runs within 10 points of 54% and 31%; the four gap shares within five points of Table DU; rhythm-band breaks back within the spread of v114's; outside notes within two points of 7.1% (4.5% minor); verse 2's share within 10 points of 50%; no unit return over half a point; the pick with no soft break and its repeats inside the kept middle half.

## Readings the paper does not give

- **348 (Q1 A).** A drawn line with fewer eighth-grid positions than syllables may place short notes on sixteenth positions. Returning lines are aligned on the eighth grid first, then on the sixteenth.
- **349.** After the end rule, a note may move a semitone to one of the song's sung extra pitch classes where fix 200's rule allows it. The last note never moves.
- **351.** A bar of a copy that fails 303's check is drawn fresh; the rest of the line keeps the copy.
- **353.** Song 43's window measures read on A with the natural minor scale. 286's Table B readings and the PPM still read on the engine's frame (C).
- **354.** The four gap knobs move by at most a factor of 1.6 a round toward Table DU's band for the unaimed builds' notes a bar.

## Blind-pick tally

The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40, 41 and 43 are not yet offered. No song was recorded on v115, so there is no new blind pick.
