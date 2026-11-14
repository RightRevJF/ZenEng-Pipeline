# Test report: Luthier v7 on songs 48 and 49

Words and music: Jason Bryant. 14 November 2026.

The spec is Luthier v7 (Module 27.88, Window 164). Fixes 730 to 736 were ported onto the Luthier v6 engine in one pass (gen_l7_p58.py; song 49 by gen_l7_p59.py; every patch asserted to match once); 737, 738 and 739 are readings (read_l7.py, read739.py). Each song was rerun once, main and control, at the same seed and designs. Nothing blocked the port. Song 49's pick of record stays e2b80cdc3a1c.

## Runs

| Run | Seed | Code | Built | Survivors | Order | Calibration rounds | Power (650) | Palette power (735) | Rate 717 | Pick (730) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Song 48 main | 20261561 | 397d54330a8a | 1000 | 775 | db3ed0fc13ab | 6 | 1.000 (stop round 3) | 1.00 | 1.00 | aab38d0971e1 |
| Song 48 control | 20261561 | 397d54330a8a | 1000 | 752 | 44de852103a9 | 7 | 1.424 (stop round 5) | 1.00 | 1.00 | ed90305e255a |
| Song 49 main | 20261562 | 71b17cdd5e1a | 1000 | 664 | cb0a317e10d9 | 8 | 1.000 (stop round 3) | 1.80 | 1.00 | 2f8263b62ee4 |
| Song 49 control | 20261562 | 71b17cdd5e1a | 1000 | 666 | 9787becabe8d | 10 | 1.000 (stop round 3) | 1.60 | 1.00 | 962791062353 |

## The port check (730)

luthier_judge5.py (sha256 fac5abf2…) was saved beside luthier_judge4.py and its data and called as given. On the Luthier v6 runs' clean survivors it gives every listed pick: song 48 3bf00742c210 (263 eligible of 458) and e5bb0fda1502 (254 of 434); song 49 2a630947f684 (323 of 575) and 8a996bd122a8 (311 of 557). e2b80cdc3a1c is eligible at a window place of 0.631. The session's reader for 739 gives the kept 25th, 50th and 75th percentiles of all nineteen readings exactly as the tables file does.

## Song 48: each fix's test

Main / control.

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The pick's most-repeating window | place 0.552 to 0.934 | 0.847 / 0.695 | Pass |
| 730 | Eligible (under 715; under 730) of clean; within 0.02 of the least | printed | 440, 382 of 488 / 476, 424 of 512; 112 / 121 | Printed |
| 731 | Entries before / on / after, stressed openings | 20 / 42 / 38 within 10 | 54 / 22 / 25; 54 / 21 / 25 | Fail (742) |
| 731 | The same, unstressed openings | 43 / 10 / 47 within 10 | 25 / 38 / 36; 26 / 38 / 36 | Fail (742) |
| 732 | Bars (3+ notes) on a kept figure, rate under one | 56% within 15 | 47.3% / 48.0%, rate 1.0 | Value passes; the rate is at one (743) |
| 732 | 651's share still passes | middle half 35% to 62% | 37.0% / 37.1% | Pass, near the floor |
| 733 | Each window under the kept 75th in three builds in four | 75% | verse 1 82 / 80, chorus 95 / 94, verse 2 93 / 93, bridge 82 / 83, last chorus 97 / 97 | Pass |
| 733 | Longest run of one pitch | kept 4 to 7 | median 8 / 8 (pick 8 / 6) | Printed: over |
| 734 | Easier of a pair; easier than every neighbour | 89 within 3; 73 within 5 | 86.0 / 86.6; 65.6 / 66.7 | Pass; fail (745) |
| 734 | The power's rounds, with standard errors | printed | main back to 1.00 at round 3; control one raise counted (1.42), back to 1.42 at round 5 | Printed |
| 735 | Drawn lines (under 6.5 notes a bar) against the palette: 16th; 8th; quarter | within 10 | 14.9 v 11.3; 62.8 v 58.5; 13.6 v 17.9 (power 1.0) | Pass |
| 735 | Bits saved a gap (the judge's reader, median) | 0.13 to 0.36 | 0.102 / 0.106 | Fail (744) |
| 735 | Gaps from the kept mean palette (median) | 0.19 or more | 0.218 / 0.218 | Pass |
| 736 | Deaths for want of a placement | under 20 (song 49's test) | 4 / 5 | Pass |
| 737 | Bars sung in a kept song, every complete build | 81% within 8 | 75.1% / 74.9% | Pass |
| 738 | Lines of 6.5 notes a bar and over against the kept cell: 6.5–7.5 | within 10 | 29.7 v 28.5; 61.1 v 56.8; 5.2 v 4.6 | Pass |
| 738 | The same, 7.5 and over | within 10 | 35.6 v 50.4; 58.0 v 36.9; 2.6 v 2.9 | Fail (744) |
| 657 | Survivors | | 775 / 752 (v6 731 / 724) | |

## Song 49: each fix's test

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The pick's most-repeating window | 0.552 to 0.934 | 0.916 / 0.818 | Pass, but the pick chants (740) |
| 730 | Eligible (715; 730) of clean; within 0.02 | printed | 523, 462 of 558 / 533, 452 of 576; 268 / 254 | Printed |
| 731 | Stressed openings | 20 / 42 / 38 | 27 / 31 / 42; 26 / 31 / 43 | Fail on the bar line (742) |
| 731 | Unstressed openings | 43 / 10 / 47 | 29 / 27 / 44; 29 / 27 / 44 | Fail (742) |
| 732 | Kept figures, rate under one | 56% within 15 | 49.1% / 49.5%, rate 1.0 | Value passes; the rate is at one (743) |
| 732 | 651's share | 35% to 62% | 39.1% / 39.1% | Pass |
| 733 | Each window under the kept 75th, three in four | 75% | 84 / 82, 95 / 97, 96 / 94, 95 / 97, 84 / 86, 95 / 97 | Pass |
| 733 | Longest run of one pitch | kept 4 to 7 | median 8 / 8 (pick 16 / 14) | Printed: over (740) |
| 734 | Easier of a pair; than every neighbour | 89 within 3; 73 within 5 | 86.5 / 86.5; 68.0 / 68.1 | Pass; pass at the edge |
| 734 | The power's rounds | printed | both back to 1.00 at round 3 | Printed (745) |
| 735 | Drawn lines against the palette: 16th; 8th; quarter | within 10 | 19.4 v 7.5; 63.8 v 53.7; 10.3 v 24.0 (power 1.80 / 1.60) | Fail (744) |
| 735 | Bits saved a gap | 0.13 to 0.36 | 0.082 / 0.088 | Fail (744) |
| 735 | Gaps from the kept mean palette | 0.19 or more | 0.171 / 0.172 | Fail (744) |
| 736 | Deaths for want of a placement | under 20 | 39 / 27, all at Verse 1 line 4 | Fail (741) |
| 737 | Bars sung in a kept song | 81% within 8 | 82.0% / 82.4% | Pass |
| 738 | Lines of 6.5 notes a bar and over | within 10 | none in this song | |
| | Survivors | | 664 / 666 (v6 660 / 662) | |

## 739: the nineteen readings for the pick and the median build

Outside the kept middle half (the pick; the median clean build):

- **Song 48 main (aab38d0971e1):** least-repeating window 0.09 (under); spread between windows 0.40 (over); longest run 8 (over); range 22 (over); pitch-class entropy 2.76 (over); gaps of an eighth 62% (over); gaps of a quarter or more 19% (under); onsets on a bar's first beat 14% (under). Median build: longest run 8, range 22, sixteenths 23%, quarters 19%, first-beat onsets 12%, the two largest sections' medians 7 apart.
- **Song 48 control (ed90305e255a):** range 22, distinct pitches 15, entropy 2.76, sixteenths 25%, quarters 18%, first-beat onsets 12%, sections 9 apart. Median build as main.
- **Song 49 main (2f8263b62ee4):** least-repeating window 0.42 (over); longest run 16 (over); steps 53% (over); leaps 6% (under); entropy 2.74 (over); first-beat onsets 10% (under); sections 7 apart (over). Median build: longest run 8, first-beat onsets 12.5%.
- **Song 49 control (962791062353):** least-repeating window 0.07 (under); longest run 14 (over); first-beat onsets 14% (under). Median build: longest run 8, first-beat onsets 13%.

What 728's rule (every window under the kept 75th, among builds eligible under 715) would have picked: song 48 54db4425f286 / ed90305e255a (278 / 296 builds); song 49 ef3a04a2c45c / 672e402c17eb (348 / 361 builds).

## How the ports were made

- **730:** luthier_judge5.pick over the clean survivors, as 715's; the record keeps each build's window places.
- **731:** 653's kept line is drawn from the table's lines whole for the line's cell whose first-syllable stress matches the line's first syllable as this engine stresses it (lines of unknown stress set aside; the whole cell where none match, which did not happen). In 680 a stressed opening's pickup runs to the next stressed syllable; in the old draw the first syllable may stand before the bar line. 714's exact first onset stays.
- **732:** 717 draws first, at its rate; a bar that takes no kept figure goes to 651, which draws from every bar the song has sung (as it did).
- **733:** the window is the section's first eight bars; its repeats so far are read from the lines placed and the line's notes so far; at or over 713's ceiling for the section's density, 717 draws among kept figures with no repeated note.
- **734:** the calibration's unaimed builds are a hundred a round. A raise counts when the reading rises by more than two standard errors of the difference from the round before. After two raises in turn that do not count, the power returns to the last value that counted (the starting 1.0 if none did) and stays.
- **735:** 711's ratio is raised to a power Q, searched in the calibration (up by 1.6 at first; reversed and narrowed to the square root of the step when the largest gap grows) while drawn lines under 6.5 notes a bar stand more than ten points from the build's capped palette in the sixteenth, eighth or quarter.
- **736:** 313 keeps a copied bar whatever its count; 680 takes a copied bar over the cap as a fixed bar; in the old draw a copied bar's own count is that bar's cap.
- **737, 738, 739:** read by read_l7.py and read739.py; 739's readers reproduce the tables file's kept percentiles.

## Order of work

1. 740: the judge still admits a chant across two lines.
2. 742: entries on the bar line where a pickup does not fit; the old draw's entry weights for stressed openings.
3. 741: song 49's deaths are a want of room, not the template's bar.
4. 744: the palette's power cannot move the gaps; bits saved and 738's densest lines.
5. 743: 717's rate at one.
6. 745: the power returns to its start.

## Findings

### 740. The judge reads repeats by window, and its pick still chants across two lines

**Problem:** 730 places the most-repeating window among kept windows. A window repeats in a share of its moves, so a chant that fills one window's first two lines and nothing else can stand under the upper quartile. Song 49's pick under v7 does.

**Evidence:** Song 49 main, the pick 2f8263b62ee4: Bridge lines 1 and 2, "I don't have proof, I have a door / I'm leaving open just a crack," sing sixteen G3s in a row. Its bridge window repeats in 55% of its moves, the 0.916 place, under the 0.934 limit; its other windows lie at 0.42 to 0.45. The control pick 962791062353 runs fourteen E3s from Chorus 2's last line into the bridge. Kept songs' longest run of one pitch: median 6, 90th percentile 9.5, 95th 11.25. The median clean build's longest run is 8 on both songs. The line on sixteen G3s is the writer's own blind pick for the song.

**Fix (proposed):** Add the longest run of one pitch to the pick's eligibility, inside the kept middle half (4 to 7.25) or under the kept 90th (9.5); or read a window by its longest run as well as its share.

**Check:** No pick with a run of one pitch past the kept 90th, on songs 48 and 49.

### 741. Song 49's deaths are a want of room, not the template's bar

**Problem:** 736 lets a copied bar keep its count, and it did (727 copied bars over 308's cap kept, song 49 main), but song 49's deaths remain at Verse 1 line 4. The line that dies has no copied bar over the cap.

**Evidence:** Deaths for want of a placement 39 / 27 a thousand (v6 60 / 55), all at Verse 1 line 4, "I grew up trusting what I could touch" (9 syllables). In 150 builds drawn again with the line watched, it failed four times: three times with no copied bar at all, with its last onset held to 48 or 51 twelfths by the next line's entry and breath, or with room only to the slot's end at 72; once with a single copied note. The next line, "The nail, the bread, the roof of tin," now draws pickups more often (731).

**Fix (proposed):** Where a line's syllables cannot fit before the next line's entry less its breath, let the next line's pickup shorten (or its breath give way, as 681 does before a line sung again) before the line is given up.

**Check:** Deaths for want of a placement under 20 in a thousand on song 49.

### 742. Entries by stress miss both ways: pickups that do not fit fall on the bar line, and the old draw prefers a pickup

**Problem:** The kept line is now drawn by the first syllable's stress, but the entries as sung do not follow it. Unstressed openings land on the bar line three or four times as often as kept lines do, and song 48's stressed openings come in early in over half their lines.

**Evidence:** Song 48: unstressed openings 25 / 38 / 36 against 43 / 10 / 47; stressed 54 / 22 / 25 against 20 / 42 / 38, but the stressed lines are two lines of the lyric, "Dear one, you will..." and "Something something was singing." Song 49: unstressed 29 / 27 / 44; stressed 27 / 31 / 42. Two mechanisms. (1) In 680 a pickup that does not fit after the previous line's breath is dropped, and the line then starts on the bar line: on song 48, unstressed lines that start on the bar line had 24 twelfths or less from the previous line's last onset in 71% of cases, lines that start before it in 49%. (2) When 680 falls back, the old draw weighs a first onset before the bar line 1.0, on it 0.35, after it 0.5; with 731 a stressed first syllable may now take that pickup.

**Fix (proposed):** Where the kept line's pickup does not fit, shorten it to what fits, or draw the kept line again among lines of the stress whose entry fits; and weigh the old draw's first onset by the kept shares for the line's stress.

**Check:** 731's test, each kind within ten points.

### 743. 717's rate still stands at one

**Problem:** Taking 717's turn before 651 raised the share of bars on a kept figure into the test, but the rate is still at its limit in all four runs, which 732's test asks it not to be.

**Evidence:** Song 48: 47.3% / 48.0% (v6 40.6% / 41.1%); song 49: 49.1% / 49.5% (v6 42.0% / 43.0%); rate 1.0 from the second round in every run. 651's share fell to 37% (song 48) and 39% (song 49), near its lower quartile of 35%. Of the bars eligible, 96% took a kept figure (song 48 main 14,130 of 14,762; song 49 main 11,208 of 11,706); 733 restricted the draw to figures without a repeat 3,291 and 2,379 times.

**Fix (proposed):** None from here beyond 722's: the eligible bars cap the reading. Either accept the rate at one, or let a bar of a template line or a copied bar take a kept figure too.

**Check:** 717 at 56% within fifteen points with the rate under one.

### 744. The palette's power cannot move the gaps

**Problem:** 735 raises 711's ratio to a power until the drawn lines meet their palette. On song 48 they already did, and the power stayed at one; on song 49 the power searched from 1.0 to 1.8 and the sung gaps did not move. Bits saved a gap stay under the kept middle half on both songs.

**Evidence:** Song 49, drawn lines under 6.5 notes a bar, sung against palette: sixteenths 19% against 7.5%, eighths 64% against 54%, quarters 10% against 24%, at every power the search tried (round by round the sung shares stay within two points). Bits saved a gap 0.082 / 0.088 (median; kept middle half 0.13 to 0.36); gaps 0.17 from the kept mean palette (0.19 asked). Song 48: drawn lines within ten points at power 1.0; bits saved 0.102 / 0.106; distance 0.218. Lines of 7.5 notes a bar and over (738): sixteenths 36% against the kept cell's 50%, eighths 58% against 37%. Song 49's lines carry eight or nine syllables in two bars, and a whole kept bar of four or five notes holds eighths whatever the weight: the gaps follow the counts, and the counts follow the words.

**Fix (proposed):** Draw the line's split of notes over its bars (the counts) with the palette in view, not only the bars of a given count; or let the palette choose between a pickup and a later entry, which moves a note out of the bar. Read bits saved against kept songs of the build's notes a sung bar.

**Check:** Bits saved a gap inside 0.13 to 0.36; 735's test.

### 745. The power returns to where it began

**Problem:** With a hundred builds a round, a raise counts only when the reading rises by more than about 0.007, and the reading hardly moves with the power. In three runs of four the power went back to 1.0; the share against every neighbour fails on song 48.

**Evidence:** Standard error 0.0024 to 0.0030 a round. Song 48 main: powers 1.00, 1.18, 1.41 read 0.869, 0.868, 0.871: neither raise counts; back to 1.0. Control: 1.21 does not count, 1.42 counts (0.866 to 0.878), 1.56 and 1.83 do not; back to 1.42. Song 49: both back to 1.0. Easier than every neighbour: song 48 65.6% / 66.7% (fails 73% within five), song 49 68.0% / 68.1% (passes at the edge). Across powers 1.0 to 1.8 the first share stays between 0.861 and 0.884.

**Fix (proposed):** None to the stop, which works as written. The paper may rule that 650's second share is out of reach of the power under 713's ceiling and whole kept bars, and read it as a reading.

**Check:** 650's two shares printed with the power's rounds.

## Regression line

Songs 40–47 are closed (523, 571). Song 48's record stands on v134 (5440fb310f58 / ce6f70d21d6a). Its reruns: v136 473ea72c00d9 / 54d5fcc4eae6; v137 104d263b6bd6 / 25552792b7c3; Luthier v1 da01fc0096fb / 1ddae17ce4bc; Luthier v2 e6f259b64c38 / a6023c8db5cb; Luthier v3 run A c6ee6ce5c6a4 / da3ddf5aaf62, run B 2276b48371d3 / 7d544b83f0f7; Luthier v4 e897f1e17e02 / 8924d5f25684; Luthier v6 21a41b55f90a / 3021b2a276db; Luthier v7 db3ed0fc13ab / 44de852103a9. Song 49: Luthier v4 a467ceb242b7 / e8691d73b008; Luthier v6 ef9d3a2a2039 / bf016d1e7243 (pick of record e2b80cdc3a1c); Luthier v7 cb0a317e10d9 / 9787becabe8d.

## Blind-pick tally

31 songs: Annotated top 14, Remembered top 8, Middle 8, Refrain 1. Not yet offered: songs 40, 41, 43, 44, 45 and 46.
