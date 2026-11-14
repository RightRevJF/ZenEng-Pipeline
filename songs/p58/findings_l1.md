## Findings (619–)

*Numbering: the paper asked for new findings from 610, but 610–618 are already taken by the v137 run's findings (the fix list since v137), which Window 158 does not mention. These run from 619; the paper's own fixes would then start after the last of them.*

### 619. 605 lifts recurrence at eight bars to the kept level, but at four bars it stops at 11%, with every bar it can reach already following the template.

**Problem:** The calibration drove the template's rate to its ceiling (1.0: every bar of a later four-bar unit in a drawn line is given the template's bar) and still reached about half the kept figure at four bars. A template bar is kept exactly only where the line's syllables fall into that bar in the same number. The verse's lines carry 14 to 16 syllables in two bars against template bars of other counts, so 360/370 keep the bar within one onset (one dropped or one added), which is near the template but not the same rhythm.

**Evidence** (within sections, every complete build; exactly the same rhythm, then Jaccard 0.6 or more; main / control):

| Bars apart | v137 | Luthier v1 | Kept |
|---|---|---|---|
| 1 | 0% / 0%; 3.1% / 3.0% | 0% / 0%; 2.7% / 2.4% | 3.2%; 15.3% |
| 2 | 10.7% / 11.1%; 31.4% / 30.4% | 11.7% / 11.1%; 30.4% / 28.0% | 11.1%; 29.0% |
| 4 | 6.1% / 6.6%; 23.6% / 23.2% | 11.3% / 11.5%; 33.4% / 32.9% | 20.1%; 38.5% |
| 8 | 2.4% / 2.3%; 10.2% / 8.7% | 17.9% / 19.1%; 47.3% / 47.4% | 24.9%; 42.2% |
| 16 | 6.6% / 6.9%; 24.1% / 24.0% | 12.5% / 11.9%; 33.3% / 31.7% | 24.2%; 42.6% |

- **The test:** neighbours under 8% passes; eight apart within 8 points passes (7.0 / 5.8 under); four apart misses (8.8 / 8.6 under).
- **Counts:** bars given the template 13,141 / 13,159. The rate reached 1.0 in the second round and stayed there (the four-bar readings in the rounds ran 6% to 15%).

**Fix:** Let a bar that follows the template take the template's count of syllables as well as its onsets: draw the line's split of syllables between its bars from the template where the words allow. Or read 605's four-bar test on Jaccard (kept 38.5%), which the template meets within 6 points.

**Check:** Bars four apart the same in 20% of pairs within 8 points.

### 620. 605's coupling gain comes to the kept figure, and the judge is not worse for it.

**Problem:** None.

**Evidence** (main / control):

| Reading | v137 | Luthier v1 | Kept |
|---|---|---|---|
| Gain under the kept couplings, bits a bar: mean | 0.026 / 0.032 | 0.118 / 0.123 | 0.16 held out (0.209 fitted) |
| 25th / 50th / 75th | −0.028 / 0.020 / 0.066 and −0.023 / 0.024 / 0.074 | 0.041 / 0.105 / 0.180 and 0.051 / 0.114 / 0.189 | — |
| 557, both windows | −1.79 / −1.86 (v136); −1.54 / −1.57 (v137) | −1.44 / −1.54 | 0 |

The gain is within 0.08 of 0.16 on both runs. The judge's score beside density peers is no worse: it is a tenth nearer on the main run and the same on the control.

**Fix:** None.

**Check:** As 605's.

### 621. 606's palette does not reach the second half: the bits saved a gap and an interval do not move.

**Problem:** Each build drew a kept song's palette (1,000 / 1,000). Every drawn line's gaps came from the mixed table (17,601 / 17,648 lines), and every move was tilted toward the palette. Still, a build's first half saves no more on its second than under v137.

- The palette reweights the table's shares, but the gaps sung are set mostly by the syllables, the spans and the copies.
- The move tilt is one factor among many in a move's weight.
- What moved is the size of moves: the verse's mean interval fell to the kept figure (623).

**Evidence** (bits saved a symbol on the second half, mean over complete builds; main / control):

| Symbol | v137, at 0.85 | Luthier v1, at 0.85 | Luthier v1, best share | Kept, at 0.85 |
|---|---|---|---|---|
| A gap | 0.148 / 0.142 | 0.141 / 0.147 | 0.159 / 0.165 (0.7) | 0.29 |
| An interval | 0.001 / 0.012 | −0.007 / 0.032 | 0.036 / 0.044 (0.5) | 0.18 |

- **The model:** the kept mean palette is the corpus model (gap classes; intervals −7..+7, clipped), mixed with the first half's own shares and tested on the second half.
- **Reading check:** on song 48's v134 builds this reading gives 0.081 a gap and 0.030 an interval at the best share, against Table FD's 0.125 and 0.049; the corpus bits agree within 0.13. The paper's exact reading may differ in detail.

**Fix:** Let the palette set the shares rather than tilt them: the gap classes of 578 and 600 replaced by the palette's at 0.7 (not reweighted around the position tables), and the move categories (repeat, step, third, fourth or fifth, larger) drawn at the palette's shares in AIM. Then read again whether a song's halves agree.

**Check:** As 606's.

### 622. 578 and 600 on the mixed tables: the chorus's drawn lines still pass; the verse misses as under v137.

**Problem:** As 610, 611 and 618: the verse's spans are where v137 left them (drawn lines at 0.69 / 0.75 / 0.81 of the slot in both dense cells, against the kept 0.77–0.90), so the verse still sings half sixteenths.

**Evidence** (main / control; kept for the lines' cells):

- **Chorus 1, drawn lines:** sixteenths 14.2% / 15.9% (9.7% / 9.2%); eighths 57.6% / 52.6% (59.4% / 59.5%); quarters 16.2% / 18.2% (16.9% / 17.1%).
- **Verse 1:** sixteenths 48.4% / 49.5% (37.6% / 35.5%); eighths 39.9% / 37.5% (48.5% / 50.5%).
- **Dense lines' longest equal-gap run:** median 4 / 4.

**Fix:** As 618.

**Check:** As 600's.

### 623. v137's tests on this run: 602 and 603 pass, and 603's mean interval now passes too; 601 is worse, because the template sets where long lines end.

**Problem:** A long line whose bars follow the template ends where the template ended, whatever class 601 drew. Class 0 rose at every rate.

**Evidence** (main / control):

- **601, class 0 by the rate as sung:** under 8 0.777 / 0.867 (kept 0.65); 8 to 10 0.743 / 0.760 (0.51); 10 and over 0.610 / 0.627 (0.34). v137: 0.596 / 0.600, 0.627 / 0.616, 0.625 / 0.634.
- **602:** the verse window ends on the tonic 19.1% / 18.3% (kept 19%; tonic not in the chord, B in every build). The chorus's window ends on the hook (designed) in 998 / 999 builds.
- **603:** leaps past a fifth 2.0% / 1.8% (kept 2%); mean interval 1.88 / 1.96 (kept 1.94 ± 0.15; v137 2.13 / 2.16).

**Fix:** For 601: where a long line follows the template, draw the template's class at 601's share when the template is drawn (the template's lines are the section's first), or leave the class to the template and read 601 on lines that do not follow it.

**Check:** As 601's.

### 624. 604: the hook's net gain shrinks a little; the engine's own part of the chorus comes about four tenths nearer.

**Problem:** None; a reading.

**Evidence** (score less the band's kept mean: total, on designed lines, from the form, the rest; main / control):

| Section | v137 | Luthier v1 |
|---|---|---|
| Verse 1 | −0.76 / −0.69: 0, +0.11, −0.87 and 0, +0.09, −0.78 | −0.76 / −0.81: 0, +0.11, −0.87 and 0, +0.09, −0.90 |
| Chorus 1 | −2.32 / −2.46: +0.84, −0.33, −2.84 and +0.88, −0.38, −2.96 | −2.12 / −2.27: +0.68, −0.35, −2.45 and +0.76, −0.38, −2.66 |

**Fix:** None.

**Check:** Printed.

### 625. 608's baselines: kept against kept finds nothing, as it should; on one song the engine is easier to tell than the paper's held-out figures.

**Problem:** None; a reading, printed once (the judge was not refitted). With song 48 alone on the engine side, its builds are split in half, not held out by song, so these figures run higher than the paper's 0.62, 0.78 and 0.77.

**Evidence** (L2 logistic, C = 0.3, twenty splits; mean, sd):

- **Kept against kept, songs split four ways:** 0.513 (0.040). Inside 0.45 to 0.55.

| Engine against kept | Luthier v1 main | Luthier v1 control | v137 control |
|---|---|---|---|
| Density alone (notes a bar, empty bars) | 0.716 (0.014) | 0.705 (0.012) | 0.706 (0.011) |
| The 39 measures | 0.958 (0.006) | 0.960 (0.006) | 0.952 (0.008) |
| The 37 others, density regressed out | 0.904 (0.008) | 0.921 (0.009) | 0.905 (0.011) |

**Fix:** None. For the paper: the engine side wants several songs to be held out; one song cannot give it.

**Check:** As 608's.

### 626. The run: survivors and deaths, and the pick, which waits on the kept quartile.

**Problem:** 607's pick needs the kept songs' lower quartile of the coupling gain, which the tables file does not give. The writer chose to run and report the pick when the figure arrives. Every survivor's gain and judge score are kept (read/l1_pick_candidates.json), so the pick needs no rerun.

**Evidence** (main / control):

- **Survivors:** 850 / 891 (v137 887 / 911). Orders da01fc0096fb / 1ddae17ce4bc. Seed and designs as v134.
- **Limit deaths:** 97 / 62 (v137 29 / 28). Run_max 64 / 11; spectral 38 / 22; rhythm band 33 / 34; the longest notes in eight bars 27 / 12; memory 24 / 17.
- **The chorus above the verse:** 38 / 28. Bridge opening unrelated 9 / 18.
- **Join deaths:** 2 / 1 at ('Verse 1', 3). The main run sits at 577's limit, which asks for under two.
- **Survivors' coupling gain:** 89.5% / 90.1% at or over 0; 52.6% / 56.1% at or over 0.10; 28.6% / 34.1% at or over 0.16. The present pick's own gain is 0.146 / 0.336.

**Fix:** None. The quartile is to be supplied.

**Check:** As 607's.
