## Findings (580–)

### 580. 547: a judge that has not seen song 48 tells it from the kept songs as it tells song 40, and more easily than songs 43, 46 and 47.

**Problem:** None; a reading.

**Evidence** (the judge of record's 39 measures; L2 logistic, C = 0.3, sides weighted alike; first verse and chorus windows, 400 complete builds a run; the kept windows, zeneng_v132_kept_windows.json, split in half by piece, eight splits; AUC mean ± spread; main / control):

| Song | Fitted on | Separation |
|---|---|---|
| 48 | 40–47 | 0.806 ± 0.022 / 0.786 ± 0.021 |
| 40 | the other six | 0.807 / 0.823 |
| 42 | the other six | 0.781 / 0.794 |
| 43 | the other six | 0.733 / 0.752 |
| 44 | the other six | 0.877 / 0.909 |
| 45 | the other six | 0.916 / 0.962 |
| 46 | the other six | 0.704 / 0.727 |
| 47 | the other six | 0.741 / 0.631 (± 0.039) |

**Fix:** None. Printed for each new song with 554's within-song separation when that is read.

**Check:** Printed.

### 581. 557: beside its density peers, song 48 reads with songs 46 and 47.

**Problem:** None; a reading. The raw score is the nearest to the kept songs of any song read so far, but its windows are half sparse choruses (under 3.5 notes a bar), which the judge scores high; beside their peers they are not.

**Evidence** (main / control): raw score −0.71 / −0.74, 47% / 46% under the kept songs' 5th percentile (−0.86); less the band's kept mean −1.83 / −1.97; under the band's kept 5th 34% / 38%, under its 25th 67% / 70%. Windows by band: 5.5 and over 50% / 50%; under 3.5 25% / 37%; 3.5 to 4.5 25% / 13%. Song 46 beside its peers −1.96 / −2.13; song 47 (closed) −1.77 / −1.72.

**Fix:** None.

**Check:** Printed.

### 582. 558 holds on a song it was not tuned on: the dense verses' streams are at the kept figures.

**Problem:** None; a reading.

**Evidence** (main / control): lines of nine notes or more at eight a bar and over, longest equal-gap run 50th / 75th / 90th / 95th: 4 / 5 / 6 / 7 and 4 / 5 / 6 / 7 (kept 4 / 6.5 / – / 12); over 551's cap 0.04% / 0%. The verse windows (5.5 notes a bar and over): longest equal-gap run, mean 5.56 / 5.27 (kept 6.30); a gap equal to the one before 0.422 / 0.407 (kept 0.456). The run length could not be met in 57,608 of 209,879 draws (27%) and 56,899 of 210,045 (27%).

**Fix:** None.

**Check:** Printed.

### 583. The sparse chorus is now the even one: its windows run equal gaps past the kept 95th one time in five.

**Problem:** The chorus lines have five to eight syllables in two bars, under 3.5 notes a bar, where kept windows rarely repeat a gap (0.325). 558 draws runs only in lines of nine notes or more at 5.5 a bar and over, so these lines keep the weighted general table, and their streams are even: the pick's first three chorus lines alternate two pitches on near-even eighths.

**Evidence** (first verse and chorus windows under 3.5 notes a bar; main / control): longest equal-gap run over the kept 95th (6.35) in 18.4% / 23.2% of windows (kept 5%); mean 4.60 / 5.26 (kept median 3); a gap equal to the one before 0.431 / 0.490 (kept 0.325). At 3.5 to 4.5: 0.486 / 0.496 (kept 0.404).

**Fix:** Draw every line's gaps as runs of the kept lengths for its own rate (zeneng_v133_density.json's "all lines" by band, under 3.5 and 3.5 to 4.5 included), with 551's cap from the all-lines 95th (4 under 3.5, 5 at 3.5 to 4.5).

**Check:** Windows under 3.5 notes a bar over the kept 95th at most 10%; a gap equal to the one before within five points of 0.325.

### 584. 570 persists: the longest lines draw class 0 thirteen points over the kept share.

**Problem:** Read on reachable lines (562), lines of 13 notes and over end in the bar where the next line begins 65% / 64% of the time (kept 52%); song 47 had 68%. The shorter lines stand within four points.

**Evidence** (class 0 / 1, reachable lines; main / control): 13 and over 0.654 / 0.346 and 0.638 / 0.362 (kept 0.517 / 0.483); 6 to 8 0.202 and 0.195 (kept 0.170); 3 to 5 0.115 and 0.118 (kept 0.110).

**Fix:** Draw class 0 for lines of 13 notes and over from the kept shares for the line's own rate as well as its notes (570's proposal), or read the reachable share apart for these lines, whose next line is often their own return.

**Check:** Class 0 within ten points of the kept share for 13 notes and over.

### 585. 572's last join recurs once a run, inside v135's amended test (577).

**Problem:** None under 577. As on song 47, one build in a thousand a run dies where the return of the line before it finds no fit after the breath and the source's one redraw is not enough.

**Evidence:** join deaths 1 / 1 in 1,000 / 1,000 builds, at ('Verse 1', 3); 560 drew 293 / 281 lines with its bound and redrew 9 / 30.

**Fix:** None; 577's second redraw of the source comes with v135.

**Check:** Under two join deaths in a thousand at a line that returns the line before it (577): passes on v134.

### 586. The writer's chorus above the verse: the default register draw put the first pick's chorus three semitones under its verse.

**Problem:** On the first run (no register design) the pick's chorus sat about three semitones under the verse, its register drawn at the kept 3rd percentile; 63% of survivors had the chorus over the verse. The writer, who had asked for choruses that open over the band, chose a design (B): the chorus's register centre four semitones or more over the verse's, its median (the hook aside) two or more. The run was made again with it, and that pick is the pick of record.

**Evidence:** first run (not of record): survivors 933 / 941, orders 7a1b7254e66c / 1911f0edb99a. With the design: 918 / 926, orders 5440fb310f58 / ce6f70d21d6a; the design's gate passes 95.4% / 96.2%; the pick's chorus lifts nine semitones over the verse (median G♯4 over B3).

**Fix:** None to the default; the design is a writer's choice. For the paper: the kept chorus-minus-verse figure is read on the median and lets a chorus sit under its verse; a song type that promises an open chorus may want the design by default.

**Check:** Printed.

### 587. 552, 553 and 566 on song 48.

**Problem:** None; readings.

**Evidence** (main / control): 501 redrawn 24 / 11, given up 163 / 153, 552's reads 399 / 379; the calibration ran 6 / 7 rounds, verse 1 / verse 2 chord tones on the beat 0.628 / 0.635 and 0.620 / 0.639; 566 fitted 293 / 281 returns after the breath.

**Fix:** None.

**Check:** Printed.

### 588. 550 at intake: both verses and the bridge flagged; the writer kept the dense form.

**Problem:** None; a reading. Every verse line sits under its kept median slot (share 1.0) and four of the bridge's six (0.67), over the kept sections' 90th (0.63). Shown to the writer at the form (A); the song was written as the dense case asked for.

**Evidence:** sections' shares: Verse 1 1.0, Verse 2 1.0, Bridge 0.667; choruses and tag 0. No line under a tenth of kept lines of its syllables (527).

**Fix:** None.

**Check:** Printed.
