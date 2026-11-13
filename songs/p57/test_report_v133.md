# ZenEng v133: song 47, The Singer Doesn't Stop, run again as a regression — test report

*Words and music: Jason Bryant. The spec is ZenEng v133 (Module 27.77, Window 153). Ported as ruled: 558 (a line of nine notes or more at 5.5 notes a bar and over draws its gaps as runs of the kept lengths, zeneng_v133_density.json; 551's cap standing) and 560; 557 and 562 are read. Song 47 was run once under v133, main and control, at its v131 seed (gen_v133.py, melody_v133_p57.py). The paper was not edited. New findings are numbered from 566.*

## The answer in brief

- **558's check is met.** In lines of nine notes or more at eight notes a bar and over, the median longest run of equal gaps is 5 (main) and 4 (control), against the kept 4; no line passes 551's cap. The dense windows now repeat a gap 48% of the time (kept 46%), where v132 had 54% (567).
- **557, the judge beside density peers.** A window scores 1.75 and 1.69 under its band's kept mean (v132 1.96 and 1.94); 31% and 27% lie under the band's kept 5th percentile (v132 39% and 38%). The raw score is −0.86 and −0.80 (568).
- **560 does not stop the join deaths** (152 and 152): the return fits its own 15 syllables and enters earlier than its 14-syllable source, so the source's bound is read on the wrong entry (566).

| Run | Survivors | Order | Joins | Bridge's build | Align, bridge's fifth line | Calibration rounds |
|---|---|---|---|---|---|---|
| v132 main / control | 703 / 729 | 96d5b3800c78 / 5b78bdf10482 | 142 / 148 | 96 / 98 | 10 / 3 | 9 / 7 |
| v133 main / control | 650 / 681 | c896fc192aa5 / 969ce00e8852 | 152 / 152 | 110 / 96 | 34 / 44 | 10 / 8 |

The v133 runs were made once each.

## Findings (566–)

### 566. 560 as ported does not stop the join deaths: the return fits its own words and comes in earlier than its source.

**Problem:** 560 bounds the third verse line so that its last onset leaves the breath before its own entry one slot later. Every source met the bound, and the deaths at verse 1's fourth line went on. The fourth line has 15 syllables and its source 14, so the return is fitted to its own words and takes an extra note in front: it enters a sixteenth or an eighth before the source did. The bound read the source's entry; the return used its own.

**Evidence** (main / control):

- Join deaths at ('Verse 1', 3): 152 / 152 (v132 142 / 148). 560 drew 276 / 281 lines with its bound, and redrew almost none.
- In a 200-build test of plan ABCC, every join death had the return entering earlier than its source: 6 ticks earlier in 14 deaths, 12 ticks in 4. No build died where the return kept the source's entry.

**Fix:** Fit the return with the breath as its earliest entry. When the line before it is its source, the return is fitted with tmin = the source's last onset + the breath − the slot's start, as a drawn line is. If no fit is found, the source is drawn again with its last onset an eighth earlier for each syllable the return adds.

**Check:** No join deaths at a line that returns the line before it.

### 567. 558 meets its check: the dense lines' longest runs are at the kept median, and their windows repeat their gaps at the kept rate.

**Problem:** None; a reading.

**Evidence** (lines of nine notes or more at 5.5 notes a bar and over, by the line's own rate; longest run 50th / 75th / 95th; main / control):

| Rate | Kept | v132 | v133 |
|---|---|---|---|
| 8 and over | 4 / 6.5 / 12 | 6 / 8 / 10 and 6 / 8 / 10 | 5 / 6 / 8 and 4 / 6 / 8 |
| 5.5 to 8 | 4 / 6 / 10 | 6 / 6 / 6 (82 and 85 lines) | 3 / 4 / 7 and 3.5 / 4.25 / 7 (23 and 32 lines) |

- Lines over 551's cap: 0.02% / 0%.
- First verse and chorus windows at 5.5 notes a bar and over: longest equal-gap run, mean 7.91 / 7.89 (v132 8.45 / 8.42; kept 6.30); a gap equal to the one before 0.481 / 0.477 (v132 0.538 / 0.546; kept windows of the band 0.456).
- The drawn run length could not be met 46,330 / 47,801 times over the drawing; the gap is then left free.

**Fix:** None.

**Check:** Printed.

### 568. 557: beside its density peers, the song reads a fifth of a point nearer the kept songs than at v132.

**Problem:** None; a reading.

**Evidence** (first verse and chorus windows; half in 5.5 and over, half in 3.5 to 4.5; main / control):

| Run | Score | Less the band's kept mean | Under the band's kept 5th | Under its 25th |
|---|---|---|---|---|
| v131 | −1.00 / −0.99 | −1.89 / −1.88 | 36% / 35% | 76% / 78% |
| v132 | −1.06 / −1.05 | −1.96 / −1.94 | 39% / 38% | 80% / 80% |
| v133 | −0.86 / −0.80 | −1.75 / −1.69 | 31% / 27% | 74% / 71% |

- Song 46 beside its peers (Table ES): −1.96 / −2.13, 37% / 40%.

**Fix:** None.

**Check:** Printed.

### 569. The port costs survivors: the joins, the bridge's build and the bridge's fifth line.

**Problem:** Survivors fell from 703 / 729 to 650 / 681. The joins are 566's. The bridge's build gate kills 110 / 96 (v132 96 / 98). The new loss is at the bridge's fifth line, a plan return: align deaths there rose from 10 / 3 to 34 / 44. The fifth line has 10 syllables. Under plans ABCABC and ABCDBE it returns the second line, which has 7. This session did not find why the rise came with 558. In a 250-build test without calibration, the rate is the same with 558 on or off (4 and 10 builds), so the calibration's knobs may carry it.

**Evidence:** Deaths, main / control: join 152 / 152; the bridge's build 110 / 96; align ('prefit', 'Bridge', 4, 'plan') 34 / 44; limits 53 / 24.

**Fix:** None yet. On the next run, print the align deaths by plan and by syllables added, and run once with 558 off and the calibration on.

**Check:** The cause named.

### 570. 562's reading: the longest lines draw class 0 eleven points over the kept share.

**Problem:** Read on reachable lines only (562), lines of 6 to 12 notes stand within two points of the kept classes, but lines of 13 notes and over end in the bar where the next line begins 63% / 62% of the time against a kept 52%.

**Evidence** (reachable lines in two-bar slots, class 0 / 1; main / control): 13 and over 0.628 / 0.372 and 0.619 / 0.381 (kept 0.517 / 0.483); 9 to 12 0.426 and 0.415 (kept 0.419); 6 to 8 0.166 and 0.153 (kept 0.170).

**Fix:** None yet; watched on song 48. If it holds, the class is drawn from the kept shares for the line's own rate as well as its notes.

**Check:** Class 0 within ten points of the kept share for 13 notes and over.

### Also read

- 553: ten and eight rounds; verse 1 / verse 2 chord tones on the beat 0.732 / 0.736 and 0.705 / 0.715.
- 552: 501 redrawn 29 / 15; given up 66 / 68.
