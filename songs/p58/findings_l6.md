# Luthier fix list since v6

This list is cumulative since the spec's last version (Luthier v6, Module 27.87, Window 163). It covers song 48, The Ratios Hold, rerun once on Luthier v6 (711, 712, 713, 714, 715 and 717 ported onto v4 in one pass; 710 and 718 read), main and control, same seed and designs; and song 49, The World Is Asking, run under v6 the same way. The pick is luthier_judge4.pick, not edited or refitted. The judge of v132 is printed and picks nothing. Words and music: Jason Bryant. Findings run from 720, as the paper asked. Each has Problem, Evidence, Fix and Check.

## The songs

| Song | Title | Path | Runs, main / control | Judge of v132 beside density peers (printed), verse / chorus | Pick (715), main / control | Blind pick |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | The Ratios Hold | Luthier v6 at the v134 seed and designs; gen_l6_p58.py on v4 | 21a41b55f90a / 3021b2a276db (731 / 724) | −1.22 / −1.27; −1.81 / −1.81 | d90e96033615 / 41a342a191fe | Annotated |
| 49 | The World Is Asking | Luthier v6; gen_l6_p59.py on song 48's v6 file | ef9d3a2a2039 / bf016d1e7243 (660 / 662) | −1.27 / −1.21; −1.61 / −1.60 | 625a95a05b1f / 8ab6722be0f2 | offered |

## The port check (715, 710)

luthier_judge4.py (sha256 069ee14a…) was saved beside luthier_judge4_data.json and called as given. On song 48's clean survivors it reproduces every listed pick: v4 f867204f03ac (507 eligible of 562) and 5d7d02f8a36c (478 of 520); run B d12fc936a701 (98 of 242). Run B by the full list of kept rhythms reads 58.3% / 57.1% against the paper's 60% / 57% (720).

## Song 48: the readings asked for

Main / control.

| Fix | Reading | Target | v4 | v6 | Result |
| --- | --- | --- | --- | --- | --- |
| 710 | Bars whose rhythm a kept song sings (full list) | 81% within 8, both sides | 75.5% / 75.4% | 75.5% / 76.1% | Pass |
| 711 | Eighths against the build's own capped palette: verse; chorus; bridge | within 10 | 51.8 v 67.8; 71.0 v 58.7; 64.2 v 64.1 | 55.2 v 67.0; 62.7 v 58.6; 60.1 v 63.7 | Chorus and bridge pass; verse fails by 12 (725) |
| 711 | Bits saved a gap, first half on second | 0.29 within 0.1 | 0.11 / 0.11 | 0.12 / 0.12 | Fail (725) |
| 711 | Dense lines' longest run of equal gaps | median 4 within 1 | 5 / 6 | 5 / 5 | Pass |
| 712 | Deaths for want of a placement | under 20 a thousand | 39 / 52 | 13 / 5 | Pass |
| 713 | Sung note the easier of a pair | 89% within 3 | 86.2% / 86.3% | 86.7% / 86.2% | Pass, at the edge |
| 713 | Easier than every neighbour | 73% within 5 | 62.6% / 62.9% | 66.5% / 65.6% | Fail (724) |
| 713 | Repeats: verse window (kept 75th 43.6%); chorus (36.7%) | under | 32.8 / 31.8; 23.8 / 22.4 | 39.2 / 39.8; 26.4 / 27.5 | Pass on the mean; 39% / 42% of verse windows over |
| 713 | Mean ease, the judge's reader | 3.3 to 4.35 | 3.93 / 3.95 | 3.97 / 4.00 | Pass |
| 713 | The power's rounds | printed | | stops at round 3 at 1.41 / round 2 at 1.19 | Printed (724) |
| 714 | Entries before / on / after, by cell | kept within 10 | see 721 | see 721 | Fail (721) |
| 715 | Eligible of clean; within 0.02 of the least | printed | 507 of 562 / 478 of 520; 59 / 78 | 344 of 458 / 316 of 434; 128 / 128 | Printed |
| 717 | Bars (3+ notes) on a figure some kept song sings | 56% within 15 | 19.1% / 19.8% | 40.6% / 41.1%, rate 1.0 | Main 0.4 short, control at the edge (722) |
| 651 | Bars on a figure already sung | 49%, kept middle half | 46.1% / 46.8% | 45.4% / 45.8% | Pass |
| 718 | Pick's charge and place; median build's | beside 22% and 10% | 0 at 86.8%; 0.087 at 64% | 0 at 86.8% / 0 at 86.8%; 0.034 / 0.036 at 83.6% | Printed (727) |
| 657 | Survivors | within a tenth of 752 / 750 | 723 / 702 | 731 / 724 | Pass |

Readings most often charged (main): bits saved a gap low 174, pitch figure bits saved by structure low 168, bars sung in another kept song high 144, rhythm bits a bar low 99, pitch figures sung in another kept song low 53, repeated notes high 46. Under v4 the first was pitch figures sung in another kept song low, in 479 of 562.

## Song 49: the readings asked for

Main / control.

| Fix | Reading | Target | v4 | v6 | Result |
| --- | --- | --- | --- | --- | --- |
| 710 | Bars whose rhythm a kept song sings | 81% within 8, both sides | 83.9% / 84.3% | 82.3% / 82.8% | Pass |
| 711 | Eighths against own palette: verse; chorus; bridge | within 10 | 62.0 v 54.0; 69.3 v 53.7; 75.7 v 53.7 | 64.4 v 54.5; 63.6 v 54.2; 66.4 v 54.2 (ctl 64.7 v 52.7; 62.9 v 52.5; 67.0 v 52.5) | Main verse and chorus at the edge, bridge fails; control all fail by 10 to 15 (725) |
| 711 | Bits saved a gap | 0.29 within 0.1 | 0.086 / 0.087 | 0.066 / 0.071 | Fail (725) |
| 711 | Dense lines' longest run | 4 within 1 | 4 / 4 | 5 / 5 | Pass |
| 712 | Deaths for want of a placement | under 20 | 65 / 48 | 60 / 55 | Fail, all at Verse 1 line 4 (726) |
| 713 | Easier of a pair; than every neighbour | 89 within 3; 73 within 5 | 87.1 / 87.1; 67.7 / 67.6 | 87.0 / 86.9; 69.3 / 69.0 | Pass; pass |
| 713 | Repeats: verse window (kept 75th 36.2%); chorus (36.7%) | under | 26.2 / 27.6; 24.0 / 24.3 | 36.7 / 38.3; 25.9 / 27.5 | Verse over (723); chorus passes |
| 713 | Mean ease, the judge's reader | 3.3 to 4.35 | 3.93 / 3.91 | 3.88 / 3.89 | Pass |
| 713 | The power's rounds | printed | | round 3 at 1.19 / round 2 at 1.08 | Printed |
| 714 | Entries by cell | kept within 10 | 3.5–4.5: 24 / 30 / 46 | 3.5–4.5: 22 / 33 / 45 (kept 33 / 18 / 50); 4.5–5.5: 48 / 26 / 27 (26 / 24 / 50) | Fail (721) |
| 715 | Eligible; within 0.02 | printed | 528 of 571 / 542 of 576; 32 / 40 | 470 of 575 / 455 of 557; 230 / 235 | Printed |
| 717 | Figures some kept song sings | 56% within 15 | 23.2% / 23.6% | 42.0% / 43.0%, rate 1.0 | Pass at the edge (722) |
| 651 | Figures already sung | 49%, middle half | 45.3% / 45.9% | 46.8% / 46.6% | Pass |
| 718 | Pick; median build | printed | median 0.121 at 57% / 0.111 at 60% | 0 at 86.8% / 0 at 86.8%; 0.020 at 84.3% / 0.020 at 84.3% | Printed (727) |
| | Survivors | | 628 / 618 | 660 / 662 | |

Readings most often charged (main): bits saved a gap low 286, pitch figures sung in another kept song low 236, rhythm bits a bar low 167, bars sung in another kept song high 80, repeated notes high 51.

## How the ports were made

- **711:** a kept bar's weight is its times sung times the geometric mean, over its gaps, of the build's capped palette share for the gap's class over the kept mean palette's share (606's table of the 159 kept songs' mean palette, the six classes 655 caps renormalized as 655 renormalizes them, so the two shares stand on one footing). A bar of one note takes a factor of one. The stress weight on a bar's places stays, as in the v4 port.
- **712:** a line sung again within one syllable of its source takes the source's onsets, melismas included, before any drawing (in the look-ahead and in the line). With one syllable fewer, the odd note is a melisma begun on the source's longest note. With one more, the source's own melisma note is sung as a syllable, or, with none, the longest note is split at its middle (as 682). Otherwise 680 draws the line in whole kept bars with as many of its source's bars fixed as fit, all first, then each smaller set, earliest bars first; the source's entry and last onset stand in for 653's kept line. A line drawn in whole bars takes no added melisma. Where neither fits, the line is drawn as before, counted.
- **713:** the repeat's share of a move's weight is lowered to the kept windows' 75th percentile for the section's density where it stands above, and left alone below; 683's factor is no longer calibrated. The power stops at the first round, after a raise, whose reading rose by under half a point, and stays at that round's value; the ease guard may still lower it under 3.3 bits. Mean ease in the calibration is read by luthier_judge4's own trigram and cache.
- **714:** where 653's kept line enters after its bar line, the first bar must be a kept bar whose first onset is the entry; if none fits, the line is drawn as before (song 48: 1,037 of 1,879 such lines in whole bars; song 49: 1,681 of 2,369).
- **715:** pick() over the clean survivors (no soft break), every note given as (onset, pitch, section), melisma notes included, onsets as the engine writes them from bar 0. Had no build been eligible, the least charge would have picked; it did not happen.
- **717:** after 651, a bar of three notes or more that took no figure already sung draws a kept figure of its count by times sung, at the rate R717, and places it on the chord as 651 places its figures. The rate moves by 1.5 times the gap to 56% each round, read by the judge's reader (a figure any kept song sings).
- **710:** read with the full list on every complete build and on survivors; 680's draw stays on rhythms two songs sing.

## Order of work

1. 721: the pickup's stress rule and verse 2's inherited entries keep entries off the kept shares.
2. 723: 717's kept figures carry repeats past 713's ceiling.
3. 722: 717's rate saturates at 1.0.
4. 725: bits saved a gap stay a third of the kept figure; the dense verse's sixteenths.
5. 726: song 49's template bar against 308's cap (699 stands).
6. 724: the power's stop reads noise.
7. 720, 727: readings.

## Findings

### 720. Run B by the full list reads 58% where the paper reads 60%

**Problem:** 710's port check asks the session's reading of run B to be the paper's 60% / 57%. The control matches; the main run is 1.7 points short.

**Evidence:** Every complete build, a bar counted where its rhythm is anywhere in luthier_v6_kept_bars.json: 58.3% / 57.1%. Survivors: 58.7% / 57.9%; clean survivors 58.8% / 58.5%. The judge's own barlist reader gives the same 58.3% / 57.1%. The v4 runs read 75.5% / 75.4%, as the paper's 75%.

**Fix (proposed):** Say which builds the paper's 60% reads, or accept the reading within two points.

**Check:** r710.py on run B gives the paper's figure for the set it names.

### 721. Entries before the bar line stay far under the kept shares

**Problem:** 714 sets the first onset of a line whose kept line enters after the bar line, but lines entering before the bar line are now rarer than under v4, and lines on the bar line about twice the kept share. Two causes. The pickup of 680 carries only the unstressed syllables before the line's first stress (the v4 port's reading of "a pickup as 653's kept line had it"), so a line whose first syllable is stressed cannot enter before. And 712 now gives verse 2 verse 1's entries, which have few pickups.

**Evidence:** Song 48, entries before / on / after by cell: 3.5–4.5, 14 / 37 / 49 against a kept 33 / 18 / 50; 6.5–7.5, 19 / 48 / 33 against 49 / 22 / 30; 7.5 and over, 11 / 47 / 42 against 36 / 31 / 33 (v4: 24 / 43 / 33 and 31 / 38 / 31). Verse 1's fresh lines at 7.5 and over enter before in 1%. Verse 2's lines sung again entered before in 43% under v4 and 13% to 16% under v6. Song 49: 3.5–4.5, 22 / 33 / 45 against 33 / 18 / 50; 4.5–5.5, 48 / 26 / 27 against 26 / 24 / 50. Of lines whose kept line enters after, 55% (song 48) and 71% (song 49) found a kept first bar starting there; the rest were drawn as before.

**Fix (proposed):** Rule whether a kept line's pickup may carry a stressed first syllable (the paper could supply the kept share of pickups that begin on a stressed syllable), or draw 653's kept line from the lines whose first syllable's stress matches, so the shares are met among lines that can take them.

**Check:** 714's test, entries at the kept shares of the cell within ten points.

### 722. 717's rate pins at 1.0 and the reading stops at the test's floor

**Problem:** Every eligible bar takes a kept figure, and the share of bars on a kept figure still reads 41% to 43% against 56%. The eligible bars are too few: 651 runs first and gives its bars the song's own figures, which are kept figures only by chance, and designed, fixed and copied bars take neither.

**Evidence:** Rate 1.0 in all four runs from the second round. Song 48: 6,936 of 7,350 eligible bars took a kept figure (414 not placeable on the chord); reading 40.6% / 41.1% (v4 19.1% / 19.8%). Song 49: 6,386 of 6,642; 42.0% / 43.0% (v4 23.2% / 23.6%). 651's share stays inside its middle half (45% to 47%).

**Fix (proposed):** Let 651 draw, among the figures already sung, those a kept song also sings first; or let 717 take its turn before 651 at its rate, with 651 drawing from what is then sung.

**Check:** 717 at 56% within fifteen points with the rate under one; 651's test still passes.

### 723. 717's kept figures bring repeated notes past 713's ceiling

**Problem:** 713 holds repeats from above in the walk's move weights, but 717 sets a kept figure whole, and kept figures repeat often. On song 49 the verse window rose over its kept 75th.

**Evidence:** Within a bar, kept figures repeat a note in 31% of their moves at three notes, 37% at four, 44% at five, 49% at six (by times sung; the commonest three-note figure is a repeated note twice, 269 times in 67 songs). Song 49's verse window (3.5 to 4.5 notes a bar): 36.7% / 38.3% against a kept 75th of 36.2%, 47% / 53% of builds over; 26.2% / 27.6% under v4. Song 48's verse: 39.2% / 39.8% under its 43.6%, but 39% / 42% of builds over (v4 9% / 8%). The judge charges repeated notes high in 46 (song 48) and 51 (song 49) builds.

**Fix (proposed):** Count a kept figure's repeats against the window's ceiling when it is drawn (draw among kept figures of the count with a weight that holds the repeat share under the ceiling), or apply 713's ceiling to 717 as to the walk.

**Check:** Repeated notes in each window under the kept 75th for its density; 717's test.

### 724. 713's stop judges half a point on one round's noise

**Problem:** The calibration reads the per-note share on thirty builds a round. Between rounds at the same power it moves by half a point to a point, so the stop fires at the first raise and the power ends near where it began. The second share then falls short on song 48.

**Evidence:** Song 48 main: rounds at powers 1.00, 1.21, 1.41 read 0.866, 0.871, 0.866; stopped at round 3; at 1.41 the next three rounds read 0.869, 0.867, 0.871. Control stopped at round 2 at 1.19. Song 49: stopped at round 3 at 1.19 and round 2 at 1.08; at a held 1.08 the control read 0.880 to 0.865. Song 48: easier than every neighbour 66.5% / 65.6% (fails 73% within five); song 49: 69.3% / 69.0% (passes). Under v4 the power had run to 5.7.

**Fix (proposed):** Judge the half point on pooled rounds or on more builds (a hundred or more), or give the stop rule in standard errors.

**Check:** 650's two shares within their bounds; the power's rounds printed.

### 725. Bits saved a gap stay at a third of the kept figure

**Problem:** 711 brought the chorus's eighths to its palette, but the bits a build's first half saves on its second did not move. On song 48 the verse sings sixteenths at nearly three times its palette's share: a dense verse (over seven notes a bar) can only be sung in kept bars that hold sixteenths, whatever the weight. On song 49 the drawn lines sing quarters at a third to a half of the palette's share.

**Evidence:** Song 48: bits saved 0.124 / 0.121 at 0.85 (v4 0.113 / 0.109; kept 0.29). Verse: sixteenths 36% against 13%, eighths 55% against 67%. Chorus: eighths 63% against 59% (v4 71%). Bridge: sixteenths 31% against 13%. Song 49: bits saved 0.066 / 0.071 (v4 0.086 / 0.087); quarters 8% to 14% against 24%; eighths 63% to 67% against 53% to 55%. The judge charges bits saved a gap low more than any other reading on both songs (174 and 286 builds).

**Fix (proposed):** Say what carries a song's own gap habit from its first half to its second. Whole kept bars weighed by a palette share draw each line afresh; a rate at which a drawn bar is a bar the song has already sung (as 651 does for figures) would carry it. Read 578's test on dense lines against the palette of kept songs at the line's density.

**Check:** Bits saved 0.29 within 0.1; 711's palette test within ten points.

### 726. Song 49's deaths stay at Verse 1's fifth line (699 stands)

**Problem:** 712 cleared song 48's verse sung again. Song 49's placement deaths are not there: every one is at Verse 1 line 4, where the template's first bar holds 8 of the line's 9 notes, over 308's cap.

**Evidence:** 60 / 55 a thousand, all at ('Verse 1', 4) (v4 65 / 48). Song 48: 13 / 5, in Verse 2 lines 0 to 3.

**Fix (proposed):** As 699: 308's cap applies to drawn bars, not to the template's bars.

**Check:** Deaths for want of a placement under 20 in a thousand on song 49.

### 727. The ruler: every pick at the ceiling, the median build near it (718, a reading)

**Problem:** None; a reading.

**Evidence:** All four picks have no charge and stand at the 86.8% place, the highest a build can reach. The median build: song 48 0.034 / 0.036 at 83.6%; song 49 0.020 / 0.020 at 84.3%, against the median kept song's 0.16. A kept song with a twentieth of its notes moved stands at 22%, a tenth at 10%. Builds within 0.02 of the least charge: 128 / 128 and 230 / 235, so the pick is decided among them by distance from the kept medians (song 48 2.40 / 2.19; song 49 2.55 / 1.99). The judge of v132, printed: song 48 −1.52 / −1.54 both windows; song 49 −1.44 / −1.41.

**Fix:** None.

**Check:** Printed.

Song 49's pick of record stays eaf2dcc068b6 (v4) until the writer decides whether its documents are rebuilt from the v6 pick, 625a95a05b1f. Its blind pick is offered; the tally is updated when he answers.

## Regression line

Songs 40–47 are closed (523, 571). Song 48's record stands on v134 (5440fb310f58 / ce6f70d21d6a). Its reruns: v136 473ea72c00d9 / 54d5fcc4eae6; v137 104d263b6bd6 / 25552792b7c3; Luthier v1 da01fc0096fb / 1ddae17ce4bc; Luthier v2 e6f259b64c38 / a6023c8db5cb; Luthier v3 run A c6ee6ce5c6a4 / da3ddf5aaf62, run B 2276b48371d3 / 7d544b83f0f7; Luthier v4 e897f1e17e02 / 8924d5f25684; Luthier v6 21a41b55f90a / 3021b2a276db. Song 49: Luthier v4 a467ceb242b7 / e8691d73b008; Luthier v6 ef9d3a2a2039 / bf016d1e7243.

## Blind-pick tally

30 songs: Annotated top 13, Remembered top 8, Middle 8, Refrain 1. Song 49 offered, not yet answered. Not yet offered: songs 40, 41, 43, 44, 45 and 46.
