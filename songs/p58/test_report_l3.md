---
title: "The Ratios Hold: test report, Luthier v3"
subtitle: "Words and music: Jason Bryant"
---

# What was run

Song 48 under Luthier v3, in the two runs the paper asked for, each read against Luthier v2. Same lyric, seed (20261113+448), designs and judge of record (v132's, not refitted, read beside density peers). Each run made 1,000 builds, main and control.

- **Run A, the rhythm:** 652 (bars whole), 653 (a line whole), 654 (the template keeps its span), 655 (the palette capped, and the band's spare), 656 (the class as sung).
- **Run B, the pitch:** run A plus 650 (the right note) and 651 (the song's figures).

Tables: luthier_v3_tables.json as reissued on 13 November (655's cap, the ruling on 652 with 653, the band's spare). Engine: melody_l3_p58.py, written by gen_l3_p58.py from melody_l2_p58.py. ZE_PART_L3=1 is run A, 2 is run B, and 0 is Luthier v2.

| Run | Survivors | Order |
|---|---|---|
| A main / control | 752 / 750 | c6ee6ce5c6a4 / da3ddf5aaf62 |
| B main / control | 569 / 562 | 2276b48371d3 / 7d544b83f0f7 |

# Song 48 by version

Main / control. The judge sits beside density peers, so a kept song reads 0. The pick is the refit's first clean survivor with a gain of 0.14 or more (630).

| Version | Verse 1 | Chorus 1 | Both (under peers' 5th) | Survivors | Gain, bits a bar | Bars sung in a kept song | Sung note the easier / beats every neighbour | Bars on a figure already sung |
|---|---|---|---|---|---|---|---|---|
| Luthier v2 | -0.78 / -0.92 | -1.48 / -1.64 | -1.13 / -1.28 (16% / 17%) | 627 / 629 | 0.055 / 0.052 | 35% / 34% | 82% / 81%; 59% / 56% | 30% / 29% |
| v3 run A | -1.29 / -1.32 | -1.56 / -1.64 | -1.42 / -1.48 (23% / 25%) | 752 / 750 | 0.060 / 0.070 | 44% / 44% | 82% / 81%; 58% / 56% | 30% / 30% |
| v3 run B | -1.03 / -0.76 | -1.36 / -1.59 | -1.20 / -1.18 (19% / 19%) | 569 / 562 | 0.056 / 0.073 | 45% / 43% | 88% / 88%; 71% / 70% | 46% / 45% |
| Kept | 0 | 0 | 0 (5%) | | 0.14 (median) | 81% | 89%; 73% | 49% |

Picks: run A 1a7a8eb6d99a (gain 0.225) / 1e0edb1b2857 (0.153); run B a6cb970ba33e (0.21) / ca4cb4476d09 (0.282).

# Each fix's test

| Fix | Test | Run A | Run B | Result |
|---|---|---|---|---|
| 650 | Sung note beats a neighbour on ease, 89% within 3 points | 81.7% / 80.9% (off) | 88.2% / 88.1% | Pass (B) |
| 650 | Beats every neighbour, 73% within 5 | 57.8% / 56.0% (off) | 71.1% / 70.4% | Pass (B) |
| 650 | Judge beside peers no worse | | -1.20 / -1.18 against v2's -1.13 / -1.28 | Mixed: main worse by 0.07, control better by 0.10 |
| 651 | Bars of 3+ notes on a figure already sung, 49% within 8 | 30% / 30% (off) | 46.4% / 44.6% | Pass, the rate at its ceiling (678) |
| 652 | Bars sung in a kept song, 81% within 8 | 44% / 44% | 45% / 43% | Fail (670) |
| 652 | Dense lines' median longest run of equal gaps (read) | 4 (75th 6) | 4 (75th 6) | Read; kept median 4 |
| 653 | Entries before / on / after at the kept shares within 10 | Dense cells pass; 3.5 to 4.5 fails | Same | Partial (671) |
| 653 | Spans at kept quartiles within 0.05, under 5.5 | 0.41 against 0.50, and others | Same | Fail (671) |
| 653 | Rhythm deaths for want of a placement, under 20 a thousand | 43 / 40 | 51 / 50 | Fail (672) |
| 654 | 605's test at four bars, 20% within 8 | 8.1% / 8.7% | 7.6% / 8.9% | Fail (673) |
| 654 | Gain under the kept couplings 0.12 or more | 0.060 / 0.070 | 0.056 / 0.073 | Fail (673) |
| 655 | 578's test on the chorus's drawn lines, against the build's own palette within 10 | Sixteenths 23% against 13% | 23% against 12% | Fail, just (674) |
| 655 | Builds spared by the band, counted | 26 / 39 | 28 / 43 | Counted |
| 655 | First half saves 0.29 bits a gap on the second, within 0.1 | 0.18 / 0.17 | 0.17 / 0.18 | Fail (674) |
| 656 | As 635's: class 0 on lines that follow no template at 579's share | 65% / 66% against 51% (8 to 10) | 67% / 69% | Fail (675) |
| 657 | Survivors within a tenth of the version before | 752 / 750: up from v2, just short of v1 | 569 / 562 against A | A passes against v2; B fails (676, 677) |
| 659 | No knob aims distinctness or a chart measure | None does | None does | Pass |

# What each calibration set

- **650's power:** 1.68 / 1.71, reached in six rounds from 1.0. The readings climbed from 0.87 to 0.88 and settled.
- **651's rate:** 0.97 / 0.99, climbing every round from 0.44 / 0.46. The reading rose from 0.40 to 0.45.
- **605's template rate:** 1.0, as under v1 and v2.

# How the ports were made

- **653:** For each drawn line in a two-bar slot, one kept line of its cell is drawn once per build. Its span share stands in 600's place. Its breath stands in 631's, held to the cell's 75th for lines on the downbeat or off it. Its entry is the line's first onset where the first syllable allows. Otherwise the line takes the nearest entry of the same kind, and if none is in reach the try draws as before (1,171 tries in run A main).
- **652:** A dense line in a two-bar slot, not on copied bars, is sung as a pickup (only as many eighths as there are leading unstressed syllables) plus two whole kept bars. The split between the bars is drawn by the bars' times sung and the stresses on their places. The last bar is within an eighth of the kept line's last onset where one fits, or otherwise the fitting bar that ends latest. 308's cap holds, the join between bars stays within 3 to 24 twelfths, and no melisma is added. Lines on the template's bars keep the template.
- **654:** Template and unit-return bars keep their span whatever their source did.
- **655:** The cap is applied to the palette's shares before 634 mixes them, and the excess is spread over the classes still under their caps. The band's spare reads each palette song's reading from the reissued tables, only to decide inside or outside the soft band.
- **656:** When a line of 13 notes or more in a two-bar slot misses its drawn span, its class having been given up, and its last onset falls in its last bar, the class is drawn again from 579's shares at the rate as placed. The next line's entry follows the class.
- **650:** The token, the kept model and the song so far are as the tables file defines them. The walk carries the song so far, with the line's own tokens added as it goes. The weight applies to every move, a line's first note and slurred notes. The per-note reading is the file's, every fifth note from the fifth.
- **651:** At the first note of a bar of three notes or more that the line sings alone, with none of its notes fixed, the bar takes, at the calibrated rate, a figure from an earlier bar of the same count. The figure is set on the chord: its start is drawn near the note before, weighted by the chord, and every note must be in the scale and the register with no clash. 634's classes of move give way to it.
- **Not ported:** 658 to 660 are the paper's.

# Findings

## 670 The whole bars land only where they are drawn
**Problem.** 652 draws whole kept bars only in lines of 5.5 notes to the slot's bar and over. Most of the song's bars are not in such lines, and those are still assembled one gap at a time.
**Evidence.** Bars whose rhythm a kept song sings: 44% / 44% in run A and 45% / 43% in run B (Luthier v2 35% / 34%; kept 81%; the test is within eight points). The dense counts rose: 7 notes 31% (v2 11%), 8 notes 21% (v2 6%). The shortfall is in 3- and 4-note bars, the chorus's bars, drawn under 5.5: 4 notes 13% against a kept 88%, and 3 notes 70% / 63% against 90%. 2,379 of 2,724 dense lines were sung in whole bars; 345 fell back.
**Fix (proposed).** Every drawn bar is taken whole from the kept bars of its count, inside 653's entry and breath, at every density. 551, 558, 578 and 600 then shape no drawn bar.
**Check.** Bars sung in a kept song at 81% within eight points, by count of notes as well as overall.

## 671 653's spans fall short in the sparse cells, and its entries in one cell
**Problem.** Below 5.5 notes to the bar, the kept line's span is drawn but rarely met, and the line ends early.
**Evidence.** Spans to the next line's first onset, run A (kept in brackets): 3.5 to 4.5, off the downbeat, 0.41 median (0.50); on it, 0.51 (0.62); under 3.5, 0.30 (0.375 and 0.50); 4.5 to 5.5, 0.49 (0.66). All are more than 0.05 out. Breaths in the same cells run long: 57 against 45, and 48 against 36. "No rhythm at the drawn span (a try)" rose from 5,780 under Luthier v1 to 54,992; the drawn span was met 3,494 times and given up 3,807 times. Entries in the dense cells are at the kept shares within ten points (6.5 to 7.5: 40 / 24 / 36 against 49 / 22 / 30; 7.5 and over: 45 / 30 / 26 against 36 / 31 / 33). The 3.5 to 4.5 cell is not: 21 / 17 / 63 against 33 / 18 / 50.
**Fix (proposed).** As 670: a line whose bars are whole kept bars meets a kept line's span because the bars carry it. Until then, read the span test with the share of spans met beside it.
**Check.** 653's span and entry tests in every cell under 5.5.

## 672 The breath carried into a copy kills the verse sung again
**Problem.** Rhythm deaths for want of a placement are 43 / 40 in a thousand (v2 112 / 118; the test asks under 20). Every one is in Verse 2, at its first lines.
**Evidence.** By line: Verse 2:0 33, Verse 2:1 7, Verse 2:2 3 (run A main); B 36, 14, 1. Verse 2 sings Verse 1's bars again (293), Verse 1's first line now often enters early with a pickup (653), and the line before it, the chorus's last line, carries a sparse cell's long breath forward as a least distance (60 to 75 twelfths). The copy cannot both keep its source's entry and leave that breath.
**Fix (proposed).** The breath before a line sung again is the lesser of the drawn breath and what its source's entry allows, but no less than 212's 18. Or: 653's breath binds only a drawn line's own end, not the next line's start where that line is a copy.
**Check.** Deaths for want of a placement under 20 in a thousand.

## 673 The template still does not return
**Problem.** 654 lifted 631's condition from the template's bars, and the bars four apart are still not the same rhythm.
**Evidence.** Same rhythm four bars apart within a section: 8.1% / 8.7% in run A and 7.6% / 8.9% in run B (v1 18%, v2 7%; kept 20%). Pooled by section in run A: Verse 5.1%, Chorus 9.6%, Bridge 8.5% (v1: 8.5%, 12.7%, 11.9%). The gain under the kept couplings: 0.06 / 0.07 and 0.056 / 0.073 (the test asks 0.12). 605 gave 12,163 bars the template's bar, and 633 split syllables anew on 4,545 lines. 633 changes a template bar whenever a line's count differs, and Verse 1 is 15, 14, 14, 14, so its second half never matches its first. The melisma pass then splits onsets on the copied bars.
**Fix (proposed).** A line on the template's bars takes them exactly where its count matches the template's within one, with the extra syllable as a melisma on the template's longest note, or a dropped onset at its weakest. No melisma is added to a copied bar.
**Check.** 605's test at four bars (20% within eight points) and the gain at 0.12 or more.

## 674 The palette's sixteenths are still over, and the half-to-half saving fell
**Problem.** The chorus's drawn lines sing more sixteenths than the build's own capped palette gives the cell, and capping the palette took away some of what 634 had won.
**Evidence.** 3.5 to 4.5, run A main: sixteenths sung 23% against the capped palette's 13% for the cell (over ten points); eighths 55% against 58%; quarters 11% against 17% (within ten). The cap applied to 11,857 lines and left 5,162 alone. Bits saved first half to second at 0.85: 0.18 / 0.17 a gap (v2 0.24 / 0.24; kept 0.29). The band spared 26 and 39 builds in run A, and 28 and 43 in run B.
**Fix (proposed).** Draw the gap from the capped palette alone (not 0.7 the palette and 0.3 the cell), so the line follows its song; with 670 the bars carry the song's palette.
**Check.** 578's test against the build's own palette within ten points; bits saved 0.29 within 0.1.

## 675 656 does not bring the class to the kept share
**Problem.** Read as 635's test, lines that follow no template still end in the next line's bar too often.
**Evidence.** Lines that follow no template, 8 to 10 notes a bar: class 0 in 65% / 66% (run A), 67% / 69% (run B), against a kept 51%; 10 and over: 66% against 34%. Template lines fell below the kept share: 8 to 10, 38% against 51%; under 8, 24% against 65%. 656 drew again in 1,194 and 1,170 lines (run A).
**Fix (proposed).** No change asked yet. With 671's spans met, the class follows the span; read again then.
**Check.** As 635's.

## 676 Survivors: run A gained, run B lost
**Problem.** 657 asks survivors within a tenth of the version before.
**Evidence.** Run A 752 / 750 (v2 627 / 629; v1 850 / 891); a tenth of v1 is 765 / 802, so A is just short of v1 and well over v2. Run B 569 / 562: the pitch lost 183 / 188 builds. Limit breaks among deaths, A to B: run_max 53 to 206, spectral 41 to 105, rhythm band 78 to 68. The chorus-above-verse design's deaths rose from 37 to 83 / 111.
**Fix.** See 677.
**Check.** Survivors within a tenth of run A.

## 677 The right note pulls toward repeated notes
**Problem.** 650 passes its test, but the kept model's commonest tokens are repeats, so the power that makes the sung note easier also makes it the same note.
**Evidence.** Sung note easier than a neighbour: 88.2% / 88.1% (kept 89%; Luthier v2 82%); easier than every neighbour: 71.1% / 70.4% (kept 73%), both within the test, at a power of 1.68 / 1.71. Repeated notes in the verse window: 0.455 in run B against 0.373 in run A (kept 0.273); in the chorus window 0.306 against 0.240. Run_max is the limit that rose.
**Fix (proposed).** Hold the share of repeats at the window's kept share while the power is calibrated, as 603 holds leaps: the repeat class's weight is scaled so its share of the move weight stays at the aimed value. Or calibrate the power jointly with a repeat damping.
**Check.** 650's two shares within the test; verse repeats within the kept quartiles; survivors within a tenth of run A.

## 678 The song's figures reach the kept share at the rate's ceiling
**Evidence.** Bars of three notes or more on a figure already sung: 46.4% / 44.6% (kept 48.8%; quartiles 35% to 62%; Luthier v2 30%); the test passes. The calibrated rate is 0.97 / 0.99, at its bound: few bars qualify (a bar sung by one line alone, three notes or more, none fixed), and nearly all that qualify take a figure. A reading.

## 679 The judge: run A lost the verse, run B won most of it back
**Evidence.** Both windows beside density peers: v2 -1.13 / -1.28; A -1.42 / -1.48; B -1.20 / -1.18. Verse 1: v2 -0.78 / -0.92; A -1.29 / -1.32; B -1.03 / -0.76. Chorus 1: v2 -1.48 / -1.64; A -1.56 / -1.64; B -1.36 / -1.59. In run A the verse's costliest measures became gap_eighth (0.39) and pitch_bits (0.25), where v2's was gap_sixteenth (0.89). The whole dense bars sing eighths (verse eighths 55% against 49% for its cells; sixteenths 35% against 37%). B's verse cost is pitch_bits (0.49 / 0.52) and repeat (0.28 / 0.29), which is 677. A reading.
