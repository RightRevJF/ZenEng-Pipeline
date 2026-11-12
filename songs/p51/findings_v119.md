## Findings (402–419)

### 402. 386 and 267 conflict: a clash moved in a return kills the build.

**Problem:** 386 moves a returning or copied note off a semitone clash with a chord's outside tone. Fix 267 then compares the return with its source, finds a pitch changed early, and kills the build.

**Evidence:** In a 40-build smoke run of song 43, 20 of 40 builds died at 267. With 386 off, 3 died. The port stopped and asked. The writer chose Q1 A: 267 reads a return's pitches as drawn, before 386's moves. Under that, song 43's main run lost no builds to 267 and kept no clash (0 of 4,434 notes read, 1,394 notes moved).

**Fix:** Make Q1 A the rule: 267 reads the tune as drawn, and 386's moves are a harmonic correction, printed.

**Check:** No build dies at 267 because of a 386 move, and the moves are printed by kind of line.

### 403. 394's withdrawal missed occurrences that sang the passing pitch without its mark (a port fault, corrected before the runs).

**Problem:** A return can keep its source's pitches without the passing-note mark. When 394 withdrew a passing note from the source, such a return kept the outside pitch. The two then differed early, and 267 killed the build.

**Evidence:**
- In a 40-build smoke run of song 43, 10 builds died at 267 with 394 on. With 394 off, none died.
- A 200-build check printed every early difference. In each, the source's note had gone back to its scale pitch, and the return still sang the passing pitch.
- After the correction there were none.

**Fix:** An occurrence counts as having the passing note when its note at that place sings the passing pitch, marked or not. A withdrawal restores every such note.

**Check:** No 267 death where the source's note was withdrawn by 394.

### 404. 385 raises the notes outside the scale but leaves most of the target wanting.

**Problem:** 349's target is now a share of all notes. 375 still limits where they can go: only notes whose chord allows an outside pitch class without a clash. So most of the target finds no place.

**Evidence:**
- Outside the scale, main runs: 4.0% (song 40), 3.5% (42), 1.9% (43, minor), 1.4% (44) and 0.6% (45). Under v118 these were 0.0% to 1.0%.
- CoCoPops reads 7.1% and BiMMuDa 3.8%.
- On song 40's step-1 run, 349 placed 6,021 notes and left 64,768 places wanting.

**Fix:** Under 420 the share is a reading. To meet 424's 4% to 7% on every song, let 349 place an outside note where its chord allows one as a passing or neighbour note (358's rule), not only where it is a chord-free tone. Or read the share against the song's own chords.

**Check:** On all five songs, outside the scale between 3.8% and 7.1%, or within a fifth of a standard deviation of the nearer.

### 405. 389's rate by band cannot hold the dense lines, and 424's empty bars push more lines into runs.

**Problem:** A line whose syllables need sixteenths runs however its rate is drawn. Some lines have no room on the eighth grid; others fall back. The rate falls to its floor and the runs share stays high. In step 3, 424's empty bars squeeze lines into fewer bars, so more of them must run.

**Evidence:**

| Song | Bands' runs (kept 27–36%) | Rhythm deaths: v118 / step 1 / step 3 |
|---|---|---|
| 40 | main band 35% at step 1, 49% at step 3; dense band 72–75% | 45 / 18 / 35 |
| 42 | 47–53% | 14 / 9 / 9 |
| 45 | 84–91% | 176 / — / 63 (v116: 0) |

**Fix:** Read the runs share only on lines that could be placed without runs, and count the others apart. Draw 424's empty bar only for a line whose syllables fit its slot less one bar on the eighth grid.

**Check:** On drawable lines, runs within ten points of the band's kept share. Song 45's rhythm deaths within two spreads of v116's.

### 406. With 356's stop a reading, the quarter-gap knob runs to its cap; 388's side runs point at the landing draw, not 378.

**Problem:** Quarter gaps stay short of the kept table, and the g4 knob is pushed to its limit to make up the difference.

**Evidence:**
- **The knob at its cap:** g4 ended at 5.0, its cap, on five of the six step-3 runs of songs 40, 42 and 43 (4.7 on song 40's control). Quarter gaps still read 10–16% against the table's 13.6–16.6%.
- **388's side runs** (song 40, main, 1,000 builds each):

| Run | g4 | Quarter gaps | Survivors | Rhythm deaths |
|---|---|---|---|---|
| Step 1 | 5.0 | 11.3% | 802 | 18 |
| 378 off | 5.0 | 12.3% | 796 | 0 |
| Landing left to the kept table's draw | 3.6 | 13.5% | 769 | 30 |

- **What the side runs show:** 378 is not the cause, though it makes song 40's rhythm deaths. The landing draw (Window 124's line ends) holds back most of the shortfall.

**Fix:** Under 420, quarter gaps are among the disagreed measures, so the share is a reading. Draw the landing jointly with the kept table: weight the table's draw by the landing shares, rather than fixing the landing first. Read 378's deaths on song 40.

**Check:** g4 within a factor of two of one on songs 40, 42 and 43, and song 40's rhythm deaths within two spreads of the 378-off run.

### 407. Step 1's repairs raised the separation on the agreed measures; step 3 brought most of it back.

**Problem:** The step-1 repairs (385, 386, 394) add pitches and moves. On the 30 agreed measures the builds became easier to tell from both kept collections.

**Evidence:** On the 30 agreed measures, both collections pooled, songs 40, 42 and 43 across:
- v118: 0.756;
- step 1: 0.788;
- step 3: 0.765.

At step 1 the costliest measures were gaps of an eighth (0.74), distinct pitches (6.73 against 6.44) and fourths and fifths (12.1% against 8.3%).

**Fix:** A reading. Port and run repairs that add notes beside 424's aims, which hold the interval sizes.

**Check:** Separation on the 30 at or under v118's after each step.

### 408. 400's turn knob reaches its floor and the verse still turns too often on songs 44 and 45.

**Problem:** The walk's weight on turning cannot override what else sets the direction: the line's contour (257), the held designed notes, and neighbour notes.

**Evidence:**
- **Turns per move:** 0.61 to 0.63 on songs 40, 42 and 43, within 0.04 of the pooled 0.587.
- **Song 44's verse:** 0.69 to 0.70.
- **Song 45:** 0.65 to 0.69, with the knob at its floor of 0.1.

**Fix:** Aim 257's contour shapes on unaimed builds at the kept turns, beside 400's knob, or read turns per move on the drawn notes only.

**Check:** Turns per move within 0.04 of the pooled 0.587 in the verse and chorus on all five songs.

### 409. 424's last-note knob reaches its cap of ten on every run, and the window's last note stays off the tonic.

**Problem:** The window's last note is usually a line's ending, fixed by the ending rules (310, 311, 314, end_ok) or a design, or the next line's pickup. The knob weights only the walk's last note of a line ending in a window's eighth bar, and the ending draw where it is free.

**Evidence:** The window's last note on the tonic, main runs: 19% (song 40), 15% (42), 8% (43), 2% (44), 2% (45), against the pooled 29.9%. The knob ended at 10.0, its cap, on all ten runs.

**Fix:** Count the window's last note in 314's ending draw: the section-ending lines' tonic share, aimed by the same knob. Print where the window's last note comes from (an ending rule, a design, a pickup, the walk).

**Check:** The last note on the tonic between the two collections' means (27.7%, 32.9%), or within a fifth of a standard deviation of the nearer, on the songs whose endings are not designed.

### 410. 424's fourths-and-fifths knob reaches its floor.

**Problem:** Leaps of a fourth or fifth come from more than the walk's interval choice: end targets, unit returns, 386's moves and copied lines.

**Evidence:** The knob ended at 0.11 to 0.19 (0.56 to 0.58 on song 44). The share read 8.0% to 9.6% against 8.0% and 8.7%. 424's test held on fourths and fifths on all five songs.

**Fix:** None needed for the test. Print the leaps by where they arise.

**Check:** The knob stays above its floor of 0.1 on every run.

### 411. 424's empty-bar rate costs runs, redraws and rhythm deaths.

**Problem:** A line drawn to leave its slot's last bar empty is redrawn until no onset falls in that bar. On dense slots this costs many redraws and pushes the line into runs (405).

**Evidence:**
- Empty bars read 0.34 to 0.52 of eight, against the pooled 0.48. Every song is within a fifth of a standard deviation of the collections, so 424's test held on empty bars.
- On song 45 the rate reached 1.0, with 347,435 redraws and 12,113 lines given up, and empty bars read 0.34 to 0.38.
- Song 40 made 153,847 redraws.

**Fix:** Draw the empty bar into the line's span (378): a span of one bar fewer, rather than redraws against the slot.

**Check:** Empty bars still within a fifth of a standard deviation of the collections, with redraws per line under two and no rise in rhythm deaths.

### 412. Song 45's builds die at 267 again, from 392 and 398.

**Problem:** Song 45's "both" returns (rhythm and pitch kept) are read as changed early. 392 raises the chorus floor, so a return into the chorus is fitted to a register its source did not sing. 398's weights also re-pitch the notes the return draws.

**Evidence:**
- **Deaths at 267:** 154 (main) and 216 (control), against 33 under v118.
- **Side runs** (300 builds):

| Run | Deaths at 267 | Notes |
|---|---|---|
| As run | 45 | |
| 392 off | 23 | design deaths 41 (the lift fails) |
| 398 off | 28 | |
| 400 off | 38 | |
| 424 off | 46 | |

**Fix:** For a return whose source lies under the new chorus floor, keep the source's pitches and let 392's floor govern only drawn notes. Read 398's chord-tone weights only on drawn notes.

**Check:** Song 45's 267 deaths within two spreads of v118's 33, with 377's lift failures under one in twenty.

### 413. 390 gives the plan's returns their due, but the free units still return far under the kept rates.

**Problem:** On the free units the rates of unit 3 reach one on every song, and the reading stays low. The drawn returns are lost after the draw, when lines are given up or redrawn.

**Evidence:**
- **Song 43:** unit 3 returning unit 1 reads 4.9–5.3% against the pooled 30.1%.
- **Song 42:** unit 4 returning unit 2 reads 0.6–1.0% against 19.4%.
- **Song 44:** 5.6–7.4%.
- **Song 42's unit 3:** the plan gives it in half the windows.
- **Lines given up:** song 40 gave up 3,322 unit-return lines.
- **Held:** song 40 alone.

**Fix:** Count where a drawn unit return is lost (given up, redrawn, refitted), and keep the unit's rhythm when a line drawn on it is redrawn.

**Check:** Unit returns within ten points of the pooled kept rates on the free units of all five songs.

### 414. 391's widening does not keep spans on songs 40, 42 and 45.

**Problem:** Widening the span to the kept 5th–95th percentiles still leaves many lines with no rhythm that fits.

**Evidence:**
- **Spans given up after widening:** 16.6–17.9% on song 40 (6,689 widened), 9.6–10.3% on 42, and 21% on 45. Under one in twenty only on songs 43 and 44.
- **Song 45's 6–8-note lines:** median share 0.90–0.91, over the kept 53–80%.

**Fix:** Read the span with the line's density, so that a dense line in a short slot is drawn to the kept share for its syllables a second (423).

**Check:** Spans given up under one line in twenty on all five songs.

### 415. 393's lines of equal syllables are too few to read.

**Problem:** Verse 2 shares verse 1's syllable count on few lines. On one line the share is 0, ½ or 1 per build, and 331's calibration aims on that alone.

**Evidence:**
- **Lines of equal syllables:** one line on songs 40, 42 and 44, two on 43, none on 45 (read on all lines).
- **Song 40:** the share's median is 0, with copies given up on 26–36% of verse 2 lines. All lines read 0.36.

**Fix:** Read verse 2's share bar by bar where the two verses' bars carry the same number of syllables, not line by line.

**Check:** At least half of verse 2's bars read on every song, and the median within ten points of 50%.

### 416. 394 halves song 43's memory breaks but does not reach v114's.

**Problem:** Passing notes are no longer the main cause of the breaks, but something else still breaks memory on song 43.

**Evidence:**
- **Song 43:** memory breaks 77 → 32 (main) and 23 → 9 (control), against v114's 13 with a spread of 6.6.
- **Song 44:** 115 → 69.

**Fix:** Run song 43 with 386 off (its moves change returning lines) and with 389 off, to name what remains.

**Check:** Song 43's memory breaks within two spreads of v114's.

### 417. 395 changes nothing on song 45: 311 reads the tag, which ends on the 2nd by design.

**Problem:** 311 reads the song's last section. On song 45 that is the tag, which the writer designed to end open (Q15 A). The last chorus itself ends on the tonic.

**Evidence:**
- **311:** in A, the tag is on the tonic in 0% of builds.
- **324:** has no tonic ending to read (not applicable).

**Fix:** 311 reads the last chorus, and a designed tag is printed apart.

**Check:** On song 45, 311 holds on the last chorus and the tag's design is printed.

### 418. 398 works: the harmony measures are no longer far apart.

**Problem:** None. This is a reading for the paper. The harmony family had separated at 0.71–0.73.

**Evidence:**
- Chord tones 58–66% at the median, on a beat 65–71%, on a downbeat 67–75%, and notes off their chord left by step 44–51%.
- Read on CoCoPops alone (422), harmony separates at 0.529 across the five songs, against 0.712 under v118.
- One knob reached its cap: the step knob on song 42.

**Fix:** None. Keep 398, and add a second collection with chords to read it (422).

**Check:** Harmony separation at or under 0.60 on later runs.

### 419. 386 leaves five or six clashes on song 40, in lines drawn on a returning unit.

**Problem:** A few clashes survive the move. The reading takes the bar's chord; the move reads the chord at the note. Where a chord changes inside the bar, the two can differ. This was not verified.

**Evidence:** Song 40: 5 clashes in the main run and 6 in the control, of 4,196 and 3,357 notes read, almost all in lines drawn on a returning unit. No other song keeps a clash.

**Fix:** Read 386's clash and its check on the same chord (the note's), and print any note with no move.

**Check:** No clash on any song.

## Order of work

1. **412**: song 45's 267 deaths, from 392 and 398. **405 and 411**: runs and empty bars.
2. **409**: the window's last note. **404**: notes outside the scale.
3. **413, 414, 415**: the free units, the spans, and verse 2's bars.
4. **406, 408, 410**: the knobs at their limits.
5. **416, 417, 419**: readings.
6. **425's refit** on the agreed measures, from these runs.

## Regression line

After these fixes, songs 40, 42, 43, 44 and 45 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders:

- song 40: ecceeb769a3e / 8e69bdadba0a (seed 20261511);
- song 42: 5335fba54f0c / 098d5e6a641f (20261552);
- song 43: 946ed77c68c7 / 1127a1c33ae7 (20261553);
- song 44: 296c155427b2 / 483c8df70550 (20261554);
- song 45 as drawn: 3ab9743119bd / dedaebdb578e (20261555).

Step 1's runs reproduce from the final code (ZE_STEP=1; song 42: ccecd90174fa, 789 survivors).
