# Song 48 under Luthier v3: findings 670 to 679

Run A (rhythm: 652, 653, 654, 655, 656) and run B (A with the pitch: 650, 651), main and control each, 1,000 builds, seed 20261113+448, the designs as before. Orders: A c6ee6ce5c6a4 / da3ddf5aaf62; B 2276b48371d3 / 7d544b83f0f7. The judge of record is v132's, not refitted, read beside density peers.

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
