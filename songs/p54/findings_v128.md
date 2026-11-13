## Findings (500–)

### 500. 465 holds its class on most lines, but the engine's slots cannot reach the kept shares, and empty bars barely move.

**Problem:** The drawn class is held to the end on 90% or more of lines on four songs. But the classes a slot can reach are not the kept ones. Class 2 needs every note of the line inside the slot's first bars, which 308's cap forbids for long lines in two-bar slots. Class 0 needs the next line to pick up, and that ask is given up when its tries run out.

**Evidence** (Part 1, main runs; kept 6–8 notes: 0.26 / 0.61 / 0.11 / 0.02):

| Song | Class given up | Entry asks given up | 6–8 notes: class 0 / 1 / 2 | 9–12 notes: class 2 (kept 0.13) | Four beats or more to the next line, 9–12 notes (kept 0.36) |
|---|---|---|---|---|---|
| 40 | 7.4% | 1,079 | 0.085 / 0.849 / 0.066 | 0.043 | 0.087 |
| 42 | 27% | 737 | 0.469 / 0.492 / 0.040 | 0.028 | 0.197 |
| 43 | 2.2% | 201 | 0.145 / 0.780 / 0.075 | 0.007 | 0.131 |
| 44 | 4.2% | 390 | 0.313 / 0.617 / 0.070 | 0.017 | 0.175 |
| 45 | 11% | 552 | 0.014 / 0.937 / 0.048 | 0.000 | 0.037 |

- Empty bars in the window (Window 147): 0.190 → 0.202 (main), 0.146 → 0.175 (control), against 0.52 and 0.74.
- On song 42, 3–5-note lines sit in long slots and land two bars back in 49% of cases (kept 11%).

**Fix:** Draw 465's class by the slot's length (the table's second part, by beats of the slot) as well as by notes, so that the share drawn is the share kept lines of that slot have. Let 465 read the class on the slot the lyric gives, and print where the form's slots make the kept shares unreachable.

**Check:** On bands of 200 lines or more, each class within ten points of the kept share for its slot length; class given up under one line in twenty on every song.

### 501. 458's bounds are in seconds, and the slow songs cannot reach them.

**Problem:** The kept rate is about three notes a second across the sung span, at a kept median tempo of 125 quarter notes a minute. Song 42 is at 76 a minute and song 45 at 72, below the kept 5th percentile of 79. There, every drawn line falls short of the bound, and 414 falls back to the kept 5th–95th.

**Evidence** (median notes a second, drawn lines, 6–8 notes; kept 25th–75th 2.4–3.8):

| Song | Tempo | 6–8 notes | 9–12 notes |
|---|---|---|---|
| 40 | 116 | 3.44 | 3.22 |
| 42 | 76 | 1.77 | 2.10 |
| 43 | 118 | 2.86 | 3.28 |
| 44 | 112 | 2.72 | 3.06 |
| 45 | 72 | 1.40 | 2.03 |

**Fix:** Read 458 in onsets a beat between the first and last onset (the table's third figure, about 1.6 a beat at the median), or scale its seconds by the song's tempo against the kept median.

**Check:** Drawn lines' median inside the kept middle half on every song with 200 lines or more in a band.

### 502. Song 45's floor "as far as its lift allows" still breaks the lift.

**Problem:** The floor was allowed to fall to the chorus top less eight, but no lower than keeps the register's centre a semitone above the verse's median plus three. The lift (377) is read on the drawn notes' median, and with a lower floor that median falls under the line often.

**Evidence:**
- Design deaths, main / control:
  - Run 2 Part 2 (floor at the verse's median plus three): 16 / 109.
  - Run 2 Part 3 (top less eight): 140 / 109.
  - Run 3 Part 1: 160 / 217.
- Survivors rose from 537 / 455 to 614 / 633, from 494's fallback, which cut rhythm deaths from 54 to 8.

**Fix:** Keep 392's floor at the verse's median plus three (the lift as it stands), or test the lift on the register's centre rather than the drawn median if a lower floor is wanted.

**Check:** Song 45's design deaths under one in twenty on both draws.

### 503. 478 and 484 hold, but the paired test falls to 18 and 19, because verse 2 now carries more chord tones than verse 1.

**Problem:** With 435's rate aimed down to about 0.55, more of verse 2 is walked. That walk carries 398's chord-tone knobs (DRAWN398), set for verse 1's drawn notes. Verse 2's chord tones on the beat now stand four to five points above verse 1's.

**Evidence** (reread, pooled):

| Run | Draw | Under 0.15, of 27 | Chord tones on the beat, V1 / V2 | Pitch kept | Repeat V1 / V2 | Step V1 / V2 |
|---|---|---|---|---|---|---|
| Run 2 Part 3 | main | 19 | 0.668 / 0.655 | 0.877 | 0.326 / 0.290 | 0.431 / 0.479 |
| Run 2 Part 3 | control | 21 | 0.672 / 0.666 | 0.866 | 0.314 / 0.271 | 0.420 / 0.482 |
| Part 1 | main | 18 | 0.670 / 0.713 | 0.754 | 0.272 / 0.297 | 0.444 / 0.445 |
| Part 1 | control | 19 | 0.681 / 0.721 | 0.762 | 0.278 / 0.298 | 0.420 / 0.438 |

- Verse 2 less verse 1 (kept sd): chord tones +0.26, on the beat +0.23, on the downbeat +0.20.
- bar_rhythm_repeats is −0.35, the largest on every run.

**Fix:** Aim verse 2's chord tones on the beat at verse 1's on the same builds with one knob in the sing-again walk, as 478 aims its repeats and steps. Leave 398's knobs to verse 1's drawn notes.

**Check:** The paired test at 20 of 27 or more on both draws, with pitch kept inside 0.72–0.79.

### 504. 489's band knobs act on the section's band of syllables, but the excess of equal gaps is in windows dense with melismas.

**Problem:** A section's band (SEC_BAND) is its syllables a bar. The windows read are by notes a bar, melismas included. Song 40's chorus is in the 4.5–5.5 band by syllables, and its windows read 5.5 or more. So the band knob for the dense band is never aimed on the windows that need it.

**Evidence** (equal gaps at 5.5–9 notes a bar; kept 0.435):

| Run | Main | Control |
|---|---|---|
| Run 2 Part 3 | 0.546 | 0.567 |
| Part 1 | 0.518 | 0.493 |

- Song 45: 0.500 → 0.502.
- The longest run of equal gaps, pooled: 5.26 → 5.40 (main) and 4.79 → 5.09 (control); neither change is real (479).
- Knobs moved off one only in the bands the judged sections hold, for example 4.5–5.5 on song 40.

**Fix:** Key 452's band knobs by the line's own notes a bar as drawn (after melismas), or read the windows by the section's band.

**Check:** Equal gaps, runs of equal gaps and zigzags inside the kept figures for each density band on every song.

### 505. 490's run weight does not bring drawable runs within ten points on both draws of any song.

**Problem:** The run weight and 389's rate move together on one reading. Where 389's rate is at its bound, the weight goes on climbing, as on song 40's 3.5–4.5 band (rate 1.0, weight 1.59). Bands not in the judged sections are read on few onsets in the calibration (486), and the final runs differ from the calibration's reading.

**Evidence** (Part 1; drawable runs, main / control, kept by band):
- Song 40, 3.5–4.5: 0.419 / 0.326 against 0.291.
- Song 42, 3.5–4.5: 0.155 / 0.163 against 0.291.
- Song 43: 0.189 / 0.165 and 0.209 / 0.196 against 0.291 and 0.317.
- Song 44, 3.5–4.5: 0.287 / 0.112 against 0.291, so the two draws land 17 points apart on the same band.
- Song 45: its bands are within ten points or near it, and it fails 405's clause on rhythm deaths (8 and 12 against none).
- 405 holds on both draws on no song (song 40's control and song 44's main hold).

**Fix:** Aim the run weight alone (389's rate held at one where drawable lines exist), on all sections of the band, and read it on 60 unaimed builds or more.

**Check:** Drawable runs within ten points on bands of 200 onsets or more, on every song.

### 506. The v128 judge in the engine matches the paper on three songs, not on songs 43 and 44.

**Problem:** On the builds the paper read (Run 2 Part 2, main runs, every complete build), the engine's verse-1 means match the paper's to 0.01 on songs 40, 42 and 45. They differ by 0.16 on song 43 and 0.19 on song 44. Song 44's verse 2 matches. Both are minor songs, which suggests a frame or window difference for their first verses.

**Evidence:**

| Song | Verse 1, engine | Verse 1, paper | Verse 2, engine | Verse 2, paper |
|---|---|---|---|---|
| 40 | −0.961 | −0.96 | −1.208 | −1.21 |
| 42 | −1.078 | −1.08 | −1.203 | −1.20 |
| 43 | −0.704 | −0.86 | −0.605 | −0.68 |
| 44 | −1.894 | −2.08 | −1.951 | −1.95 |
| 45 | −2.309 | −2.31 | −2.118 | −2.11 |

- Pooled, verse 1 −1.348 against −1.42, chorus 1 −0.947 against −1.01.

**Fix:** For the paper: give the tonic, scale and window it read song 43's and song 44's first verses on, or the two songs' per-build scores.

**Check:** 476's test within 0.05 on all five songs.

### 507. The v128 judge's table has no kept 5th percentile, which 471's floor rule reads.

**Problem:** 471 moves the floor to the refit when the share of builds under the refit's kept 5th percentile is under a third on every song. zeneng_v128_judge.json gives the kept mean (1.53), sd (2.0) and 25th percentile (0.23) only.

**Evidence:** Under the normal stand-in (1.53 − 1.645 × 2.0 = −1.76), Part 1's main runs have:

| Song | Share under −1.76 |
|---|---|
| 40 | 21% |
| 42 | 27% |
| 43 | 10% |
| 44 | 37% |
| 45 | 48% |

Under the kept 25th percentile, it is 73–99% on every song. The floor stays on the v108 judge.

**Fix:** For the paper: post the kept 5th percentile of the v128 judge.

**Check:** 471's share read on the posted figure.

### 508. 494 falls back thousands of times a run; song 45's joins before a copy come from 452.

**Problem:** None for 494 itself: song 45's rhythm deaths fell from 54 to 8 (control 54 to 12). The joins before a copy, which 494 was to explain, follow 452's equal-gap weight.

**Evidence:**
- Fallbacks at once (main): song 40 3,233; song 42 3,974; song 43 1,421; song 44 3,414; song 45 5,812.
- Side runs, song 45, main:

| Run | Survivors | Joins before a copy | Align deaths |
|---|---|---|---|
| Part 1 | 614 | 53 | 62 |
| 452 off | 559 | 17 | 136 |
| 455 off | 614 (identical; see 509) | 53 | 62 |

**Fix:** Read 452's weight on the copy's entry: let a line that a copy follows keep the gap its breath needs, before the equal-gap weight is applied.

**Check:** Song 45's joins before a copy within two spreads of the 452-off side run, with 452's readings held.

### 509. 455 is inert once 490 is in.

**Problem:** As ported, 490's run weight takes the place of 455's coupling to the run reading. 455's sixteenth-gap weight then stays at one: the side run with 455 off is the same run (order, survivors, deaths).

**Evidence:** Song 45, main, Part 1 against 455 off: 614 survivors and identical deaths in both.

**Fix:** For the paper: say whether 455 should aim the band's sixteenth-gap share (its own figure, the kept table's first share) or be withdrawn.

**Check:** A side run with 455 off differs from the run of record when 455 is kept.

### 510. The range rose with 467's knob withdrawn, and 408's contour kind was not aimed.

**Problem:** The paper's 27.72 says 408 is to aim the contour's kind, and that the range is to be read for its source before it is aimed again. The session's list withdrew 408's width knob and did not ask for the kind. The kind was not ported, and the range's source is still unread.

**Evidence:**
- Range (Window 147), main: 9.06 → 9.24 pooled; songs 40, 42 and 43: 9.49 → 10.00, 10.62 → 10.60, 10.18 → 10.65.
- Turns: 0.600 → 0.623.
- Range is the costliest of the 30 on both draws (0.71 and 0.72 points).

**Fix:** Port 408's contour kind (257's kinds drawn toward the kept turns), and read the range's source (the walk's interval sizes against 398's chord tones), as the paper asks.

**Check:** Turns within 0.04 of the kept 0.584 at the mean, with range printed beside its sources.

### 511. Every separation change in Part 1 is within twice the draws' difference (479).

**Problem:** None; a reading.

**Evidence:**
- Songs 40, 42 and 43: 0.752 / 0.750 → 0.746 / 0.761, a change of +0.003 against twice the difference, 0.030.
- Five songs: 0.800 / 0.795 → 0.780 / 0.798.
- Pitch: 0.735 / 0.708 → 0.724 / 0.722. Rhythm: 0.656 / 0.679 → 0.650 / 0.681.

**Fix:** None.

**Check:** Printed on later runs.

### 512. Kept songs pass most of the song-mean tests less than half the time (496).

**Problem:** None new; 496's reading. A kept song read the way each test reads a build mean passes at these rates (170 CoCoPops songs):

| Test | Kept pass rate |
|---|---|
| 354 / 357 / 365 / 372, the four gap shares each within five points | 1.2% |
| 355, onsets on a sixteenth within two points of 9.4% | 6.5% |
| 344 / 349 / 358 / 385, outside the scale within two points | 12.9% |
| 424, fourths and fifths | 27.6% |
| 400 / 408, turns within 0.04 | 30% |
| 398, chord tones | 46.5% |
| 401, four note lengths | 49.4% |
| 310 / 322 / 330, likeness | 56.5% |
| 312, leaps past a fifth | 62.4% |
| 329 / 453, range | 64.7% |
| 409 / 456, the last note on the tonic | 0% |
| 390 / 413 / 361 / 371 / 350, unit returns | 0% |

**Fix:** For the paper: restate the 354-family test on the mean of many builds against the kept collections' spread of song means. A test no kept song passes should be read only as a mean of builds.

**Check:** Each test's kept pass rate printed beside it (the tables of tests).

### 513. 440's step beside an inversion is drawn against the neighbours as they stand, and a later inversion can take the step away.

**Problem:** The chart's inversions are drawn one at a time. An inversion drawn next to one already drawn can move that one's neighbour bass off the step it was drawn for. On song 43, Dm/A and G/D stand side by side in the chorus.

**Evidence:**
- Song 43: 7 of 96 changes inverted (7.3%, under one in twelve). Three of the seven (each Dm/A) have no step on either side in the song as drawn, so 440 fails.
- Song 42: 4 inversions of 57 changes (7.0%), each with a step.
- Song 40: none (the kept 54% of songs).

**Fix:** Test the step on the finished chart and drop any inversion that has lost its step, or forbid two inversions side by side.

**Check:** 440 holds on every chart drawn.

### 514. Part 2's charts cost nothing and gave song 43 back most of its design deaths.

**Problem:** None; a reading. With held bars and second chords in a bar, song 43's 'blue movie' sequence from the chorus top finds its chord tones more often. Song 40's key-word deaths fell too.

**Evidence** (Part 1 → Part 2, main / control):

| Song | Survivors | Design deaths | Key-word deaths |
|---|---|---|---|
| 40 | 799 / 890 → 783 / 892 | — | 11 / 1 → 2 / 0 |
| 42 | 799 / 843 → 801 / 838 | — | — |
| 43 | 810 / 828 → 872 / 918 | 107 / 102 → 23 / 26 | — |

- Separation, songs 40, 42 and 43: 0.746 / 0.761 → 0.739 / 0.734, not a real change (−0.017 against 0.030).
- Harmony (CoCoPops alone): 0.528 / 0.480 → 0.532 / 0.520.

**Fix:** None.

**Check:** Printed.

### 515. Read at the note, the melody over the chord moves differently on the two draws.

**Problem:** None that a test fails. Reading the chord at the note changes which notes count as chord tones. The two draws disagree in sign on song 40 by more than the change itself, so by 479 no change is real.

**Evidence:**

| Song 40 | Main (Part 1 → Part 2) | Control (Part 1 → Part 2) |
|---|---|---|
| Chord tones | 0.632 → 0.659 | 0.668 → 0.615 |
| First-beat chord tones | 0.739 → 0.796 | 0.808 → 0.743 |

- Song 43, chord tones: 0.641 → 0.616 (main) and 0.631 → 0.629 (control).
- The paired second-verse test on the three songs: 18 / 16 → 21 / 21.

**Fix:** None; read the at-note figures on both draws in later runs.

**Check:** Printed.

### 516. The routine's bass passes 445–448 in 36 of the 42 eight-bar windows; four of the six that fail are where the drums leave the kick out, and two are a move short.

**Problem:** 448's share of bass notes on a kick (35–59%) cannot be met where the kick sits out most of the window: song 40's intro, the bridges of songs 43 and 44, song 43's last post-chorus. The routine follows the record's drums, and with no kick to fall on, the share falls to 19–29%. Two other windows miss by a move: song 40's second verse (steps 5%) and its last chorus (repeats 14%).

**Evidence** (windows passing every test, old → new):

| Song | Old bass | New bass |
|---|---|---|
| 40 | 0 of 15 | 13 of 16 |
| 43 | 0 of 12 | 11 of 13 |
| 44 | 0 of 13 | 12 of 13 |

- The old bass fails 445 in every window: one bar rhythm throughout.
- Songs 43 and 44's old basses hold one pitch class a bar, with octaves at 89% and 71% of moves, as Window 144 found.
- The new: pitch classes a bar 2.75–3.5; on the bar's first note 47–58%; repeats 23–27%; steps 12–14%; octaves 3–5%; a bass note on every kick; 40–52% of notes on a kick; a step into the next bar in 43% of changes; the root at every change.

**Fix:** Read 448's share on the bars that have a kick, or state that a section without the kick is read against 446 and 447 alone.

**Check:** 448 read on kicked bars, holding in every window.

### 517. The new bass is plainer than the median pop and rock pattern in two ways.

**Problem:** None that a test fails; a reading against 444's quartiles. The routine's figure is two cells and two fills over eight bars, which puts its distinct bar rhythms at the kept 25th percentile. Its repeats sit under the median, because the draw spreads its weight over fifths, thirds and notes of passage.

**Evidence:**

| Measure | Pop and rock (25, 50, 75) | Songs 40, 43, 44 (window medians) |
|---|---|---|
| Distinct bar rhythms in eight bars | 2 / 3 / 5 | 2, 2, 2 |
| Repeated notes | 0.20 / 0.36 / 0.61 | 0.26, 0.27, 0.23 |
| Bar rhythm the same as the bar before | 0 / 0.14 / 0.57 | 0.00, 0.14, 0.14 |

- Song 43 is dance-pop, read against pop and rock as 444 says for a pop song. Beside the Lucerne dance-electronic medians (6.5 notes a bar, 3.6 pitch classes, 26% repeats, 29% steps), its new bass has 7.5, 2.75, 27% and 12%.

**Fix:** None required. If the paper wants the median pattern, a third cell in the second four bars (A B A C A B D E) would bring distinct rhythms to three.

**Check:** Printed.

### 518. The rebuilt records keep each song's own chart; Part 2's charts are not in any record.

**Problem:** Part 3 was to have no melody rerun, so the records of songs 40, 43 and 44 keep their picks of record and the charts those picks were drawn on (one chord a bar). The bass routine reads the chord at each half-bar (it takes a record's half-bar chart where one exists), so a record carrying Part 2's chart would be read the same way. But a melody drawn on the old chart cannot be put over a new one without being drawn again.

**Evidence:**
- The three records carry no chords2.
- 440's root at every change holds on each: old 93%, 95% and 91%; new 100%.

**Fix:** When a song is next delivered, draw its pick on the 438 chart and rebuild the record from both.

**Check:** A record with a half-bar chart, its bass read at the note.

## Order of work

1. **502, 503:** song 45's floor back at the lift, and verse 2's chord tones aimed at verse 1's (the paired test).
2. **500, 501:** 465 by the slot's length, and 458 in beats; then read empty bars again.
3. **504, 505, 508, 509:** the stream's band knobs keyed by the line's own density; the run weight alone; 452 at a copy's entry; 455's target or its withdrawal.
4. **510:** 408's contour kind and the range's source, as the paper asks.
5. **513:** 440's step tested on the finished chart.
6. **516, 518:** 448 read on kicked bars; songs drawn on their 438 charts and their records rebuilt with both.
7. **506, 507, 512:** for the paper: song 43's and 44's frame, the judge's kept 5th percentile, the 354-family test.
8. **511, 514, 515, 517:** readings.

## Regression line

After these fixes, the songs rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders:

| Song | Code | Main / control |
|---|---|---|
| 40 | Part 2 (ZE_PART=2) | 391a3901ad4b / 863d750da1de |
| 42 | Part 2 (ZE_PART=2) | 86baa9e50f35 / beda0441ddad |
| 43 | Part 2 (ZE_PART=2) | 9fab8a9e1e46 / 59dc135f6465 |
| 44 | Part 1 (ZE_PART=1) | 22afd6a4b716 / 3a2d47b70eef |
| 45 | Part 1 (ZE_PART=1) | b9571f3c3145 / 8284b2ec8ff1 |

- ZE_PART=0 reproduces Run 2's Part 3 (song 45 main: daaa5c98509f).
- ZE_PART=1 reproduces Part 1 (song 43 main: 911539fed64d).
- The rebuilt records are bass_v128.py's output from the songs' own records (songs 40, 43, 44); it is deterministic (each section's seed).

## Blind-pick tally

The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40, 41, 43, 44 and 45 have not yet been offered.
