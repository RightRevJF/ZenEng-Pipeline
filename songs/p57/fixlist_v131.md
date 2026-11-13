# ZenEng fix list since v131 (song 47)

*Cumulative since the spec's last version (v131, Module 27.75): song 47, The Singer Doesn't Stop, written with dense, wordy verse lines at the other AI's suggestion. Words and music: Jason Bryant. Findings from 550; each has Problem, Evidence, Fix and Check. 554 is a reading with no fix.*

## The songs

| Song | Title | Path | Runs of record, main / control | Pick | Blind pick |
|---|---|---|---|---|---|
| 47 | The Singer Doesn't Stop | v131 (540, 541, 542 ported; 525's kept slots; 527 at intake; 526 before any refit); G major, ♩ = 84; every line in a two-bar slot; designed hook and bridge build; second bridge lifted a step in the record; bass by the routine | f363d4e78346 / 7fba0ac398c0 (711 / 760 survivors; each made twice) | ff83ac7a0247 (362/472), no hand edits | not yet offered |

## Order of work

1. 551: draw the dense lines' gaps from the kept dense table, with runs capped at the kept 95th.
2. 552: read 501 against the rate the slot allows, not redrawn.
3. 550: read 527 by the section as well as the line.
4. 556: draw class 0 only where the next line can take a pickup.
5. 555: give a copy's source the designed line's entry when a design follows the copy.
6. 553: let the calibration run to ten rounds while 503's knob is still stepping.
7. 554: print the unseen judge's separation and the within-song separation for every new song.

## Findings
### 550. Dense lines in two-bar slots pass 527 line by line, and the song still reads far from the kept songs.

**Problem:** Every line's slot is one that kept lines of its syllable count take (14 syllables in two bars: 37%; 15: 27%; 16 and over: 10%), so 527 flagged nothing. But four such lines in a row leave the verse with no rests and a stream far more even than kept songs. 527 reads a line, never its section.

**Evidence** (Window 147, song 47's first verse and chorus; main / control; kept: Billboard, Rolling Stone):

| Measure | Kept | Song 47 |
|---|---|---|
| Empty bars | 0.515, 0.736 | 0.033 / 0.030 |
| Gaps equal to the gap before | 0.387, 0.364 | 0.466 / 0.460 |
| Longest run of equal gaps | 4.87, 4.38 | 7.06 / 6.81 |
| Notes a bar | 3.94, 4.14 | 5.65 / 5.62 |
| Most onsets in a beat | 2.63, 2.80 | 3.38 / 3.46 |
| The window's last note on the tonic | 0.28, 0.33 | 0.03 / 0.05 |

- Song 46 (three-bar slots on its long lines): empty bars 0.52, the longest equal-gap run 4.99.

**Fix:** Read 527 by the section as well as the line: the share of a section's lines in slots under the kept median slot for their syllables, against the kept songs' share. Show the writer the section, not only the line.

**Check:** On the next song, every section with three or more lines inside the kept middle half for that share; empty bars in the kept middle half.

### 551. The stream in dense lines (534) is now read, and it is too even and too full of runs.

**Problem:** Song 47 gives 534 its dense windows: 400 first-verse windows at 5.5–9 notes a bar. The stream stays even and the runs stay frequent, with 505's run weight for that band driven to 0.06.

**Evidence** (5.5–9 notes a bar, song 47 alone; kept, main, control):

| Measure | Kept | Main | Control |
|---|---|---|---|
| equal_gap_run_max | 6.17 | 8.48 | 8.20 |
| gap_same_as_before | 0.435 | 0.518 | 0.507 |
| zigzag_of_three | 0.328 | 0.361 | 0.380 |
| Drawable runs (505) | 0.361 | 0.508 | 0.471 |

- 505's run weight at 5.5 and over: 0.057 / 0.082; the run rate still 15 points over the kept.
- At 3.5–4.5 notes a bar the same song reads 5.6 / 5.4 against 4.6.

**Fix:** In a line of more than two syllables a beat, draw the gaps from the kept dense table directly (the table for the band), not by weights on the general table, and cap a run of equal gaps at the kept 95th for the band.

**Check:** At 5.5–9 notes a bar, equal_gap_run_max and gap_same_as_before within the kept middle half; drawable runs within five points of 0.361.

### 552. 542 names the bound: 501 is given up, not 465, and only on dense lines.

**Problem:** Counted apart, the give-ups at half the tries are 501's in nine cases of ten. 501 redraws dense lines tens of thousands of times: a line of 13 or more notes in a two-bar slot sings 2.36–2.73 onsets a beat against the kept 5th–95th of 1.04–2.67.

**Evidence** (main / control):

- Given up at half the tries: 501 alone 719 / 689; 465 alone 75 / 59; both 1 / 0; neither 0 / 1.
- 501 redrawn 21,668 / 20,684 (song 46: 1,357 / 1,664). Inside 7,442 / 7,553.
- Onsets a beat (25th, 50th, 75th), 13 and over notes: 2.36, 2.55, 2.73 (kept 1.33, 1.59, 2.00).

**Fix:** Read 501 on the line's span as drawn (378) and the slot together: a line whose syllables cannot fit the kept rate in its slot is read against the rate its slot allows, and counted as such, not redrawn.

**Check:** 501 given up under one line in twenty on a song with dense lines, its redraws within twice song 46's.

### 553. 541 steps the right way but ends short: three rounds of steps, then the calibration stops.

**Problem:** The gap kept its sign for three rounds and the knob fell from 1.0 to 0.28 (×0.775, ×0.6, ×0.6). The calibration ends at six rounds, and the first three were inside two points on the few builds read, so they took no step.

**Evidence:**

| Draw | Verse 1 / verse 2, chord tones on the beat (engine's window) | Paired test, song 47 (of 27) |
|---|---|---|
| Main | 0.683 / 0.710 | 17 |
| Control | 0.760 / 0.754 | 19 |

- The rounds (main): 0.481 / 0.492, 0.575 / 0.580, 0.686 / 0.705 (no step); 0.722 / 0.772 (×0.775); 0.719 / 0.771 (×0.6); 0.733 / 0.765 (×0.6).
- Window 147's reading of the pair (40, 42, 43, 46, 47 pooled): verse 1 / verse 2 0.681 / 0.699 (main), and 22 of 27 under 0.15.

**Fix:** Let the calibration run past six rounds while 503's gap is over two points and its knob is still stepping, up to ten.

**Check:** Verse 2 within two points of verse 1 on both draws; the paired test at 20 of 27 on both.

### 554. 526: the judge that has not seen the song reads it as it reads the others; a judge fitted on its builds tells it apart almost perfectly.

**Problem:** None; a reading, and a caution about it. Fitted on songs 40–46 and tested on song 47's builds, the judge separates them about as well as it separates song 43 or song 46 from the kept songs. Fitted on song 47's own builds, the agreed-30 judge separates them better than any earlier song's: the unseen judge measures the earlier songs' faults, and song 47's are new ones.

**Evidence** (AUC against the held-out kept half; eight splits, mean and spread; main / control):

| Song | Judge that has not seen it (37 measures, C = 0.3) | Within the song (agreed 30, its own builds) |
|---|---|---|
| 47 | 0.729 ± 0.027 / 0.709 ± 0.040 | 0.942 / 0.948 |
| 40 | 0.785 / 0.797 | 0.870 / 0.867 |
| 42 | 0.787 / 0.825 | 0.886 / 0.884 |
| 43 | 0.719 / 0.770 | 0.845 / 0.862 |
| 44 | 0.868 / 0.925 | — |
| 45 | 0.867 / 0.910 | — |
| 46 | 0.739 / 0.790 | 0.824 / 0.847 |

- The standing judge (v129): content mean −0.39 / −0.52; under −0.72, 36% / 42% (song 46: 38% / 39%).
- Within song 47, pitch separates at 0.853 / 0.856 and rhythm at 0.836 / 0.842 (song 46: 0.759, 0.560).
- Table EN's figures for songs 40–46 (the other AI's reading): 0.75, 0.79, 0.71, 0.86, 0.88, 0.73. This session's are within 0.04.

**Fix:** None. Print both readings for each new song: the unseen judge's, and the within-song separation, with the families.

**Check:** Printed.

### 555. A designed line on a slot's downbeat after a copied line dies when the copy's source ended late.

**Problem:** The second bridge's sixth line ("But You do") is designed to begin on its slot's downbeat. The line before it is a copy of the first bridge's fifth line, which was drawn to end before a fresh line, not before a fixed one. Where the source ran late, there is no breath, and the build dies.

**Evidence:**

- Join deaths before a line: 113 / 97 (song 46: 0 / 0).
- The bridge's design gate: 90.1% pass (317's nine in ten held, by 0.1 point); its deaths 84 / 97.
- The hook's design gate: 100% / 100%.

**Fix:** When a designed line follows a copy, give the copy's source the designed line's entry as its own next line's (247's prefit) when the source is drawn.

**Check:** No join deaths before a designed line; the design gate's pass rate over nine in ten by more than a spread.

### 556. 525 makes the classes reachable, and the short and middle lines still miss class 0.

**Problem:** With the kept shares for two-bar slots (zeneng_v131_kept_slots.json), no class the kept lines never take is drawn, but class 0 is drawn far under its kept share at every length: 0–6% for 3–12 notes against the kept 11–42%, and 31% for 13 and over against 52%. Class 0 needs the next line to begin in the bar where this one ends, which here means a pickup into it, and the next line is often a copy or a design that cannot take one.

**Evidence** (classes 0 / 1 / 2 / 3, main; kept, 525, by notes and two-bar slot):

| Notes | Lines | Drawn | Kept |
|---|---|---|---|
| 3–5 | 2,400 | 0.000 / 0.694 / 0.306 / 0 | 0.110 / 0.700 / 0.189 / 0 |
| 6–8 | 6,348 | 0.055 / 0.886 / 0.059 / 0 | 0.170 / 0.766 / 0.064 / 0 |
| 9–12 | 2,446 | 0.056 / 0.941 / 0.002 / 0 | 0.419 / 0.571 / 0.010 / 0 |
| 13 and over | 2,406 | 0.310 / 0.690 / 0 / 0 | 0.517 / 0.483 / 0 / 0 |

- Out of reach, by slot (main): Chorus line 3, class 2, 863; Bridge line 5, class 2, 516; Bridge line 3, class 0, 446; verse 1's first three lines, classes 0–1, 282 each.

**Fix:** Count, for each line, whether the line after it can take a pickup (a fresh line can; a copy or design whose entry is on or after its downbeat cannot), and draw class 0 only where it can, from the kept share renormalized over what is reachable.

**Check:** Each class within ten points of the kept share among the lines whose next line can take a pickup.

## Regression line

Songs 40–46 are closed (523), each rerun once in this session; each reproduced its order of record, main / control: 40 d508b254a8f4 / 04342d35cd1d; 42 9fd23492dad3 / 529bf7a1c186; 43 af58ce3be702 / a095303f51b7; 44 2f43a0bc93d6 / 7d4dd7b83e26; 45 6dc6710923f0 / 9a1c46f67b24; 46 120253ea25cb / 635084318e00. Song 47: f363d4e78346 / 7fba0ac398c0, each made twice.

## Blind-pick tally

28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Not yet offered: songs 40, 41, 43, 44, 45, 46 and 47.
