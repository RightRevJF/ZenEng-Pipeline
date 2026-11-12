## Findings (from 384)

### 384. A v116 generator patch for song 42 broke when 371 first reached its line.

**Problem:** Song 42's v116 generator patched a line by matching its start. The patch reset the register floor `lo` to a string. That line runs only when a unit return is drawn, and song 42's sections never drew one until 371.

**Evidence:** Song 42's first v118 smoke run crashed in the comparison of `lo` with a pitch. After the line was corrected (gen_p42_v118.py), both runs completed and reproduced their orders (e980e0dd5337 / 264d8899cc47).

**Fix:** Patch generators by whole statements, not by line starts, and run each patched path once in a smoke test before a run of record.

**Check:** Every song's smoke run passes through a unit return, a refit and a span give-up, and completes.

### 385. 375's eligible-notes target removes most of 349's notes, and the outside-scale share collapses.

**Problem:** Under 375, 349's target is read on "the notes whose chord allows an outside pitch class". So the number of notes to place is 7.1% of a small set, not 7.1% of the build. 381 is not the cause.

**Evidence:**

- **Outside the scale, main runs:** 1.0% (song 40), 0.8% (42), 0.1% (43), 0.1% (44) and 0.0% (45). Kept: 7.1%, minor 4.5%. Under v116 the shares were 6.4%, 5.8% and 3.9% on songs 40, 42 and 43.
- **The costliest measure:** it is now first on 340's list in every main run, at 1.99, 2.13, 4.86, 6.21 and 3.18 points.
- **Side runs (300 builds, main seed):**
  - Song 40: 0.9% as run; 0.9% with 381 off; 4.8% with 375 off.
  - Song 43: 0.1% as run; 0.1% with 381 off; 2.4% with 375 off.
  - With 375 off, 349 placed 1,823 notes on song 40 (350 as run) and 991 on song 43 (43 as run).

**Fix:** Keep 349's target as a share of all the build's notes. Use 375 only to choose where the notes go: place them on the notes whose chord allows an outside pitch class, and count the places wanting.

**Check:** With 375's clash test in force, the outside-scale share is within two points of 7.1% (4.5% minor), and its cost is under half a point.

### 386. 375's clash test reaches only drawn notes; returning and copied lines keep their semitone clashes.

**Problem:** 375 reads a chord's own outside tones as chord tones where fix 200's clash test is read: the walk's next note and 349's placements. A line that returns or is copied onto a bar with such a chord keeps its pitches, so it is never tested.

**Evidence:** Notes a semitone from a chord's raised tone, main runs:

| Song | Clashes | Notes read | In returning or copied lines |
|---|---|---|---|
| 43 | 746 | 4,280 | exact 289, pitch 194, rhythm 149, both 72, unit return 18 (fresh 24) |
| 44 | 736 | 4,105 | exact 301, pitch 179, rhythm 124, both 83, unit return 30 (fresh 19) |
| 45 | 98 | 1,589 | both 90, rhythm 4, unit return 2, pitch 1, exact 1 |
| 40 | 167 | 5,437 | sung again 112, unit return 31 (fresh 24) |

Song 40's clashes are on the bVII chord's own tone.

**Fix:** When a line is returned or copied onto a bar whose chord has an outside tone, read 375's clash on each note. Move a clashing note to the nearest pitch that does not clash, keeping its direction from its neighbours, as 215 moves a tritone. Print the moves.

**Check:** No sung note on a beat, or a beat or longer, a semitone from a chord's own outside tone, in drawn, returning or copied lines.

### 387. Under the kept table, 356's stop fires in round 1 and freezes the gap knobs at one.

**Problem:** 367 reads 356's stop against the pooled kept table's quartiles (1.934 to 2.735 bits a note). The builds start above the top quartile, so the stop fires before the 354 knobs move. 372's test of "every knob from one" is then met without any calibration.

**Evidence:**

- The stop fired in round 1 on the main runs of songs 42, 43 and 44 (rhythm bits 2.79 to 2.87). It fired on distinct lengths on song 40's control.
- s16, g8, g4 and glong stayed at 1.0 there.
- The gap shares then missed by more than five points. For example, on song 44's main run sixteenths were 16.4% against the kept 7.9%, and eighths 50.2% against 56.0%.
- 354, 357 and 365 held on no song.

**Fix:** Read 356's stop against the quartiles of the section's own band in the kept table, not the pooled table, since a denser band reads more bits. The tables should give the four bands' quartiles. Until then, let the stop be a reading that does not move the knobs.

**Check:** On songs 42, 43 and 44 the 354 knobs move in round 1, or the stop is shown to fire against the band's own quartiles. Each gap share is within five points of the kept table's.

### 388. Where the knobs do run, the quarter-gap knob is pushed past a factor of two.

**Problem:** Drawing from the kept table, the builds still sing too few quarter gaps. The g4 knob climbs until it hits its cap. The likely cause is that other rules shorten gaps after the draw: the span (378), the landing and the builds' density (4.1 to 4.9 notes a bar against the kept 3.6 to 4.1). This was not diagnosed.

**Evidence:**

- **Knobs past a factor of two:**
  - song 40 main: g4 4.81, run 0.30, on16 0.42;
  - song 42 control: g4 4.38, glong 3.61;
  - song 43 control: g4 5.0 (the cap), on16 2.60.
- **Song 43's control:** even with g4 at 5.0, quarter gaps read 16.6% against 17.0%.

**Fix:** Run song 40's main run with 378 off and with the landing pinned to the draw (side runs), to find which rule moves gaps after the draw. Then read 372's table after that rule rather than before it.

**Check:** On songs 40, 42 and 43, no gap knob ends more than a factor of two from one, and each gap share is within five points of the kept table's.

### 389. In the dense band, 366's "may not run" lines find no rhythm, and song 45's rhythm and join deaths jump.

**Problem:** Song 45's verses and bridge are in the "5.5 and over" band (6.25 to 6.75 syllables a bar). Their syllables need sixteenth runs to fit the slot. 366 draws most lines as "may not run" at a rate aimed at the pooled kept 31%. Those lines fail, or fall back to runs.

**Evidence:**

- **366's rate fell** to 0.078 (main) and 0.047 (control), yet runs read 47% and 52%.
- **Fallbacks:** 3,949 of 10,898 "may not run" lines fell back to runs (36%); on song 40, 3,101 of 16,137 (19%).
- **Deaths, main run:** rhythm, no placement 176 (v116: 0); join 148 (v116: 44). Survivors were 385 against v116's 476, and the run took 582 seconds against 111.
- **Side runs (300 builds):**

| Run | Survivors | Rhythm deaths | Join deaths | Seconds |
|---|---|---|---|---|
| As run | 39.7% | 53 | 35 | 325 |
| 366 off | 57.7% | 5 | 21 | 183 |
| 378 off | 35.0% | 55 | 30 | 280 |

- **The knobs collapsed:** g4 0.29, glong 0.42, run 0.08, on16 0.10.

**Fix:** Aim 366's rate at the runs share of the section's own band in the kept table, not the pooled 31%. A line that may not run, in a band whose kept table runs, falls back before it dies.

**Check:** On song 45, rhythm-placement deaths within two spreads of v116's, runs within ten points of the band's kept share, and no gap knob past a factor of two.

### 390. 371's unit returns double-count with 181's plan returns and fall short where sections are designed or copied.

**Problem:** 371 draws unit returns at a rate aimed at the kept readings, but the reading also counts returns that other rules make. 181's plan letters already return lines on song 42. On songs 43, 44 and 45, the designed, pinned and copied sections leave few units free to draw.

**Evidence:**

- **Song 42:** unit 3 returning unit 1 reads 41.5% (control 42.0%) against the kept 31.5%, with its rate cut to 0.11. Unit 4 returning unit 2 reads 1.5% against 18.8% at a rate of 0.77.
- **Song 43:** unit 3 at 3.8%.
- **Song 44:** unit 3 at 15.2% at a rate of 1.0.
- **Song 45:** 13.2% at 1.0; every rate is at its cap.
- **Song 40:** held.

**Fix:** Count the plan's returns toward 371's rate, so a return the plan already gives is not drawn again. Read the kept rates on the units the song can draw (not designed, pinned or copied), and print the share of units free.

**Check:** On the free units, each unit return within ten points of the kept rate on all five songs; the free share printed.

### 391. 378 holds on songs 40 and 44, but short lines read outside the band, and song 45 gives up 29% of spans.

**Problem:** The span is drawn first, but the reading also takes lines that were never drawn to a span: copies, and lines whose span was given up. On a ballad in the dense band, the span is given up often.

**Evidence:**

- **3–5 notes:** median share 0.889 on song 43 and 0.375 on song 42, against the kept 43–75%.
- **Song 45, 6–8 notes:** 0.816, against 53–80%.
- **Song 45 give-ups:** 1,884 of 6,441 lines (29%); with 366 off, 162 in 300 builds.
- **Song 40:** 79,446 span redraws and 3,340 give-ups.
- **Under half of full lines:** 0–4.3% (kept 4.6%).

**Fix:** Read 378's share on drawn lines only, and print copies and give-ups apart. Before giving a span up, widen it to the kept 5th–95th percentiles for its notes.

**Check:** The median share by notes inside the kept middle half on drawn lines on all five songs; give-ups under one line in twenty.

### 392. Song 45's lift, read on the drawn notes (377), still fails one complete build in six.

**Problem:** The chorus floor is set at most eight under the top and one under the verse's cap. The drawn chorus notes can still fall under the verse's median plus three.

**Evidence:**

- The lift failed in 19.1% of complete builds in the main run and 16.0% in the control.
- Drawn-note lift medians were 5.0 and 5.0, pinned 6.0 and 7.0.
- Design deaths were 110 (v116: 155).
- 317, 326 and 363 did not hold.

**Fix:** Set the chorus floor for drawn notes at the verse's drawn median plus the writer's lift, inside the song range.

**Check:** Lift failures under one complete build in twenty on drawn notes; both medians printed.

### 393. 370's refit variants barely move verse 2's share.

**Problem:** Verse 2 lines that differ from verse 1 in syllables can't be brought within one onset of the copy by one onset added or dropped.

**Evidence:**

- **Verse 2's median share:** 0.36 (song 40), 0.50 (42, held), 0.29 (43), 0.375 (44), 0.25 (45).
- **Song 44:** the variants kept the copy 563 times, one added 363 and one dropped 15. 941 bars were kept against 10,626 not kept.

**Fix:** Read verse 2's share on the lines with verse 1's syllable count, and print the rest apart. Or let 322's partner-stress fit stand as a copy for a line of another length.

**Check:** On lines of equal syllables, verse 2's median share within ten points of 50% on all five songs.

### 394. 358 makes about half of song 43's memory breaks (368).

**Problem:** A chromatic passing note placed in one occurrence of a returning tune, and not the others, breaks memory's repetition.

**Evidence:**

- Memory breaks, with 373's soft limit (0.12), main runs: v118 77; with 358 off, 36; with 361 off, 70; v114 read again, 13 (spread 9.2).
- Song 44's main run broke memory 115 times of 982.

**Fix:** A passing note placed in a tune that returns is placed in every occurrence of that tune, or in none.

**Check:** Song 43's memory breaks within two spreads of v114's with 358 on. If not, run 372 off to name the rest.

### 395. 311 and 324 read song 45's lifted last chorus on the home tonic.

**Problem:** Song 45's last chorus and tag are lifted to A (Q14 A, Q15 A), and the design ends on A. 311 and 324 read the tonic as G, so the song fails them in every build.

**Evidence:** In both runs the last chorus is on the tonic in 0.0% of builds, and there are 0 tonic endings. The design gate requires the tag on A.

**Fix:** Read 311 and 324 on the section's own key where the record lifts it.

**Check:** On song 45, 311 and 324 are read in A for the last chorus and tag and hold.

### 396. The kept rhythm table did not move separability.

**Problem:** 372 was meant to close the largest gap between the builds and kept songs, but the fresh judge still tells them apart almost perfectly.

**Evidence:** Within songs, on true songs (369):

| Song | v115 | v116 | v118 |
|---|---|---|---|
| 40 | 0.969 | 0.965 | 0.947 |
| 42 | 0.948 | 0.933 | 0.945 |
| 43 | 0.952 | 0.942 | 0.955 |
| 44 | — | 0.968 | 0.987 |
| 45 | — | 0.994 | 0.994 |

Across songs: 0.900 (v116 0.872). The yardstick is 0.57 and 0.63. 369's check held: within 0.01 of the paper's figures.

**Fix:** Rerun after 385 and 389, which cost the most on 340's list. Print separability by family of measures (pitch, rhythm, form) to name what still separates.

**Check:** Separability printed by family beside the yardstick.

## Order of work

1. **385, then 386.** 385 is a one-line target fix; 386 reads 375's clash on returning and copied lines. Together they decide the costliest measure on every run.
2. **389 with 387 and 388.** Read 366's rate, 356's stop and the gap knobs by the section's band.
3. **390.** Unit returns counted with the plan's.
4. **391, 392, 393.** The span, the lift and verse 2's share, each read on the lines it governs.
5. **394, then 395.** Memory under 358; the lifted key.
6. **396** after 385 and 389.

## Regression line

After these fixes, songs 40, 42, 43, 44 and 45 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders are:

- song 40: 9a38ef54b474 / 1bc305955b86 (seed 20261511);
- song 42: e980e0dd5337 / 264d8899cc47 (20261552);
- song 43: 210259413197 / c6bdd732cdd0 (20261553);
- song 44: 4fd00fe7a4fe / 291a923fade7 (20261554);
- song 45 as drawn: 8f661769e198 / 44039af841f3 (20261555).

The orders will change with the code. The songs must keep:

- the locked lyrics, every syllable sung;
- their designs at nine in ten, read with the spread;
- the pick with no soft break (362);
- song 45's rhythm-placement deaths back near v116's.
