## Findings (480–496)

### 480. 465 and 458 could not be ported: their kept figures are not in hand.

**Problem:** 465 draws where a line's span ends in its slot by the kept share for its length. 458 draws a span's bounds from kept lines' syllables a second across the sung span. Neither figure is in the tables page (zeneng_v88_tables through zeneng_v127_run1) or in the paper.

**Evidence:**
- The tables were searched for any figure by bar of the slot or by syllables a second across the span. Only 378's share-of-the-slot quartiles by notes (v118) and the song-level syllables a second (v120, 423) are there.
- The session asked and the writer chose Q1 A: Part 2 ran without them. They are in neither Part 2 nor Part 3.

**Fix:** Post two kept tables, from the lines Window 138 read:
- by notes in the line (3–5, 6–8, 9–12, 13+), the share of lines whose last onset falls in each bar of their slot, counted from the end;
- the quartiles of syllables a second across the sung span, by notes in the line.

**Check:** Both ported, and spans given up under one line in twenty on all five songs.

### 481. The paper's reread and the engine read song 43 (A minor) on different tonics, and the refit scores it differently.

**Problem:** Window 146's and 147's code reads every song as major on a fixed tonic. Song 43 is read on C. The engine reads a minor song on its own tonic with the natural minor scale (353), so song 43 is read on A. The degree measures (on_tonic, on_third, on_fifth, last_note_tonic, first_note_tonic_triad) differ, and with them the refit's score.

**Evidence:** Run 1's main runs, first 400 complete builds, refit content:

| Song | Mean (engine) | Mean (Window 147) | Under the kept 5th percentile (engine) | Under it (Window 147) |
|---|---|---|---|---|
| 40 | −1.20 | −1.23 | 72% | 74% |
| 43 | −0.50 | −0.84 | 52% | 62% |

**Fix:** Read a minor song on its own tonic in both, as 353 does, or say which frame the refit was fitted in.

**Check:** The engine's and the paper's refit means agree within 0.05 on all five songs.

### 482. Window 146's code halves the order score in the refit's combined score; the port follows 470's text.

**Problem:** 470 keeps the combining of content and order unchanged: the v108 judge's (content + order) / 2 per window, averaged over the windows. Window 146's code ranks by refit content + order / 2. Its comment calls the order score a sum over two windows, but the engine stores it as a mean.

**Evidence:**
- The engine's judge(): order = mean over Verse 1 and Chorus 1 of the order judge, and combined = (content + order) / 2 for each window.
- Window 146: c12 = (new12 + old_order / 2) / 2 × 2.

**Fix:** Confirm 470's combining for the refit's pick. The port uses the mean of (refit content + order) / 2, as written.

**Check:** The refit's pick on Run 1 under the paper's formula and under the port's printed side by side.

### 483. 467's "register's widening" was read as the walk's spread about the register's median.

**Problem:** 329's widening already makes each register at least 13 semitones wide, against window ranges of 6–10.6. The walk's Gaussian about the section's median (M.RSD) keeps the windows narrow, not the register's bounds. So the port aims a knob on that spread.

**Evidence:** The range knob (rg467) ended at 1.08–2.12 on songs 40–43 and at its cap of 3.0 on songs 44 and 45. Range moved only from 8.90 to 9.06 pooled.

**Fix:** For the paper: say whether 467 means 329's minimum width or the walk's spread. See 491 for what aiming either can do.

**Check:** Printed.

### 484. 434 and 435: verse 2 now sits beside verse 1 as kept second verses do, but it keeps more of verse 1's pitches than kept songs do.

**Problem:** 435 keeps verse 1's pitch where both verses strike at a rate of 0.75. The walk between those kept pitches often lands on verse 1's pitch too, so the measured share overshoots.

**Evidence** (Window 147's reading, five songs pooled):

| Run | Under 0.15 kept sd, of 27 (test 20) | Chord tones on the beat, verse 1 / verse 2 | Pitch kept | Repeated notes, verse 2 |
|---|---|---|---|---|
| Run 1 | 14 | 0.679 / 0.870 | 0.607 | 0.398 |
| Part 1 | 19 | 0.681 / 0.672 | 0.834 | 0.244 |
| Part 2 | 21 | 0.680 / 0.675 | 0.839 | — |
| Part 3 | 19 | 0.668 / 0.655 | 0.877 | — |

- The kept second verse keeps 0.72–0.79 of verse 1's pitch, and repeats 0.30 of its notes.
- 434's test passed at Part 2 (21 of 27) and fell back at Part 3 (19), as Part 3's pitch aims moved verse 1.

**Fix:** Aim 435's rate on unaimed builds at the kept 0.75 for the pitch kept (Window 142's pair()), not at a fixed rate a place.

**Check:** Pitch kept inside 0.72–0.79, with the paired test at 20 of 27 or more after every later part.

### 485. Separation's own spread is as large as the changes it is asked to judge: Run 1's 0.719 was a low draw.

**Problem:** The check reads one main run's first 400 complete builds for each song. The control runs read differently by about 0.03. They are the same code except for 243's main-run rule, so the difference is the nearest measure in hand of separation's own spread.

**Evidence:** Separation on the agreed 30, songs 40, 42 and 43 across, main and control:

| Run | Main | Control | Mean | Five songs, main / control |
|---|---|---|---|---|
| Run 1 | 0.719 | 0.751 | 0.735 | 0.759 / 0.780 |
| Part 1 | 0.745 | 0.772 | 0.759 | 0.769 / 0.785 |
| Part 2 | 0.750 | 0.768 | 0.759 | 0.773 / 0.774 |
| Part 3 | 0.752 | 0.750 | 0.751 | 0.800 / 0.795 |

- On both draws, Part 1 raised separation by about 0.025.
- Parts 2 and 3 left the three songs about where Part 1 put them. Part 3 raised the five songs' figure to 0.80.

**Fix:** Read the check on the main and control runs together. Treat a change as real only beyond twice the main-control difference.

**Check:** Both draws printed, and the check read on their mean, against Run 1's mean of 0.735.

### 486. Part 1 raised separation without drawing the first verse or chorus differently.

**Problem:** 434, 435 and 459 act on verse 2. But the calibration reads every section's runs for 389's rates (by band) and verse 2's share for 331's rate. Verse 2's lines share bands with verse 1's, so the rates verse 1 is drawn with moved.

**Evidence:**
- Separation of the three songs rose on both draws: from 0.719 to 0.745 (main) and from 0.751 to 0.772 (control).
- Pitch rose from 0.717 to 0.733 and form from 0.452 to 0.491.
- The range cost rose from 0.63 to 0.72.

**Fix:** Read 389's band rates on the sections the judge reads (Verse 1, Chorus 1) and their copies, or by section kind, so that a change to verse 2 does not move verse 1's draw.

**Check:** A rerun with only 434 and 435 changed leaves Verse 1's and Chorus 1's readings within a fifth of a kept sd.

### 487. 464 and 459 work.

**Problem:** None; a reading.

**Evidence:**
- **464:** song 45 lost no build at 267 in any part. Its survivors rose from 551 to 693 (control 563 to 773).
- **459:** verse 2's bars read (medians) rose from 25%, 50%, 17%, 17% and 33% to 64%, 88%, 50%, 50% and 88%. 313, 331, 393 and 415 now hold on songs 40, 43, 44 and 45.

**Fix:** None.

**Check:** Printed on later runs.

### 488. The refit's pick differs from the v108 judge's on every run, and the floor stays on the v108 judge.

**Problem:** None; 471 and 472's readings.

**Evidence:**
- **Picks** (Part 1, main runs, survivors with no soft break): the picks differ on all ten runs.
  - The v108 pick's rank under the refit: 294 (song 40), 35, 77, 2 and 5.
  - The refit's pick's rank under the v108 judge: 4, 20, 107, 25 and 13.
- **The floor:** complete builds under the refit's kept 5th percentile (−0.51) were 57–96% at Part 1. Song 43 fell under a third at Parts 2 and 3 (32% and 26%), but no part had every song under a third, so the floor stays on the v108 judge (471).

**Fix:** None.

**Check:** Printed on later runs.

### 489. 452 brings the even stream toward kept songs, except in the densest windows and on songs 44 and 45.

**Problem:** At 5.5 or more notes a bar, and on song 45 (5.7 notes a bar), the syllables leave too few rhythms that avoid equal gaps. On songs 44 and 45 the zigzags come from the contour and the neighbour notes, which the zigzag knob does not reach.

**Evidence** (Window 147's reading, first verse and chorus):

| Measure | Kept (Billboard / Rolling Stone) | Part 1 | Part 2 | Part 3 |
|---|---|---|---|---|
| Gap equal to the one before | 0.387 / 0.364 | 0.507 | 0.437 | 0.425 |
| Longest run of equal gaps | 4.87 / 4.38 | 6.37 | 5.41 | 5.26 |
| Zigzag of three moves | 0.315 / 0.333 | 0.391 | 0.361 | 0.351 |

- **At 5.5–9 notes a bar** (Part 2): equal gaps 0.555 against a kept 0.435, and the longest run 6.98 against 6.17.
- **Song 45:** both knobs at their floor of 0.05, and equal gaps 0.50.
- **Song 44:** zigzags 0.42 and 0.39.

**Fix:** Let the run knob (er452) and the equal-gap knob act by band of density, and aim zigzags in 257's contour shapes beside the walk (with 408).

**Check:** All three inside the kept figures for each density band on every song.

### 490. 455 leaves the drawable runs where they were.

**Problem:** The sixteenth-gap weight moves with 389's rate, but the runs come from the kept table's transitions from one sixteenth to the next. A weight on every sixteenth gap scales all sixteenths together.

**Evidence:**
- Drawable lines' runs (Part 2, main runs):
  - song 40's 5.5-and-over band: 51% against a kept 36% (band weight 0.13);
  - song 42's under-3.5 band: 10% against 27%;
  - song 44's 4.5–5.5 band: 22% against 32%.
- 405 held on song 43 alone.

**Fix:** Aim a weight on a sixteenth that follows a sixteenth onset (a run) by band, apart from the sixteenth gap.

**Check:** Drawable runs within ten points on all bands of 200 onsets or more.

### 491. Part 3's pitch aims cost survivors and memory: the tighter contour raises memory breaks, and the wider chorus floor breaks song 45's lift.

**Problem:** 408's contour knob ended at 0.20–0.66 of its width. A tighter pull holds turns down, but the tune becomes less memorable. 467's floor (chorus top less eight) lets song 45's chorus fall under the verse, which the lift design (377) forbids. The range knob at its cap moved range little: the spread is not where the range is lost.

**Evidence:**
- **Turns:** 0.621 → 0.600, against kept 0.584–0.594.
- **Memory breaks** (Part 2 → Part 3):
  - song 43: 49 → 99 (control 78 → 52);
  - song 44: 50 → 129 (control 62 → 83). Its limits deaths rose from 39 to 115 and its survivors fell from 713 to 640.
- **Song 45:**
  - the lift's design deaths: 16 → 140 (control 109); survivors 642 → 537 (control 625 → 455);
  - range: 5.98 → 7.28.
- **Range, pooled:** 8.90 → 9.06, with pitch spread unmoved at 2.49. The range knob is at its cap of 3.0 on songs 44 and 45.
- **Separation on pitch, songs 40, 42 and 43:** rose from 0.720 to 0.735.

**Fix:**
- 408: aim the contour's kind (257) rather than its width.
- 467: lower song 45's floor only as far as the lift allows (the chorus's median over the verse's by Q14 A's three).
- Range: read where the narrowing comes from (the walk's interval sizes and 398's chord tones, Run 1's 467) before aiming it.

**Check:** Memory breaks within two spreads of Part 2's, song 45's design deaths under one in twenty, and range within a fifth of a kept sd of 10.9 on songs 40, 42 and 43.

### 492. 461 with 450 brings the first beat toward kept songs.

**Problem:** None, apart from the knob at its cap.

**Evidence:**
- **The chorus's first-beat third:** 0.163 → 0.229, against kept 0.247 and 0.294. Its knob is at its cap of 10 on songs 43 and 45.
- **A second or seventh from the bass:** 0.231 → 0.212, against kept 0.18 and 0.19.
- **First-beat chord tones:** 0.682 → 0.692, against kept 0.69–0.74.
- **The first beat on the root:** 0.213 → 0.201, against kept 0.23–0.26, so it moved away.

**Fix:** None. Raise the third's knob cap only if the paper wants the chorus at 27% on songs 43 and 45.

**Check:** Printed on later runs.

### 493. The window's last note, read on walked windows (456), reaches the collections on song 40 alone.

**Problem:** None new; 456's reading.

**Evidence:** Windows whose last note the walk chose, and their tonic share:
- song 40: 1,333 windows, 21% (control 24%), held;
- song 43: 827 windows, 17% (control 24%, held);
- song 45: 494 windows, none on the tonic;
- songs 42 and 44: no walked windows.

**Fix:** None. Song 45's walked chorus ends are pinned off the tonic by its design.

**Check:** Printed.

### 494. Song 45's new rhythm deaths are 457's; its joins before a copy are neither 406's nor 457's.

**Problem:** At Part 2 song 45 lost 69 builds for want of a rhythm and 103 at a join before a copy. At Part 1 it lost 6 and 31.

**Evidence** (side runs, song 45, main, Part 2's code):

| Run | Survivors | Rhythm deaths | Joins before a copy | Joins before a line | Align |
|---|---|---|---|---|---|
| Part 2 | 642 | 69 | 103 | 66 | 24 |
| 406 off | 697 | 59 | 111 | 44 | 10 |
| 457 off | 687 | 6 | 109 | 81 | 24 |

**Fix:** For 457, fall back from the strict copy as soon as no entry and landing fit, as 389 does for runs. The joins before a copy come from 452 or 455; side runs with each off are the next step.

**Check:** Song 45's rhythm deaths and joins before a copy within two spreads of Part 1's.

### 495. Empty bars keep falling below both collections.

**Problem:** None new; 465's reading still waits for its table (480).

**Evidence:**
- Empty bars in the window: 0.27 (Part 1), 0.17 (Part 2) and 0.19 (Part 3), against Billboard 0.52 and Rolling Stone 0.74 in Window 147's reading.
- Their cost on the 30 is 0.25–0.30.

**Fix:** 465, once its table is posted (480).

**Check:** Empty bars within a fifth of a kept sd of the nearer collection.

### 496. Six tests cannot be passed by kept songs read the same way.

**Problem:** These tests are read on a song's mean over its builds. A kept song, read the same way on its two windows, mostly fails them.

**Evidence:**
- **400 and 408, turns within 0.04:** about 30% of kept songs pass.
- **424, fourths and fifths:** about 30%.
- **424 and 456, the last note on the tonic:** none can pass, since two windows read 0, 0.5 or 1.
- **453, range in the middle half, window by window:** half pass, by the middle half's definition.
- **415 and 459, the median share within ten points:** Rolling Stone's own median is 0.375, so it fails by 12.5 points.
- **390 and 413, unit returns within ten points:** a kept song reads 0, 0.5 or 1.

The details are in the report.

**Fix:** For the paper: state these tests on the mean of many builds, beside the kept collections' spread of song means.

**Check:** Each test's kept pass rate printed beside it.

## Order of work

1. **480:** the two kept tables, then 465 and 458.
2. **485, 486:** read separation on both draws, and read 389's rates on the judged sections.
3. **491:** undo or rework Part 3's contour width and song 45's floor before Run 3. **494:** 457's fallback.
4. **484, 489, 490:** 435's rate aimed, the even stream by band, runs by band.
5. **481, 482, 483:** the paper's frame for minor songs, the refit's combining, 467's meaning.
6. **487, 488, 492, 493, 495, 496:** readings.

## Regression line

After these fixes, songs 40, 42, 43, 44 and 45 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders at Part 3 (ZE_PART=3) are in the test report's table. Parts 1 and 2 reproduce from the final files with ZE_PART=1 and ZE_PART=2.
