# ZenEng fix list after v111

*Songs 40 and 42 run again under v111 · fixes 330–334 · with the tests of 310–329 on both songs' own runs (321)*

v111's last fix is 329 (Window 131). As v111 asked, this run added no song: songs 40 and 42 ran again with the same lyrics, intakes and seeds, on fixes 322–329 ported onto the v110 search. This list starts at 330.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Nothing blocked the port, and no two fixes conflicted.

## Songs since v111

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 40 (rerun) | Nothing Else on Earth | 322–329 ported. 1,000 main and 1,000 control, each twice. Survivors 480 and 417 (v110 505, 537); orders 7d491acfca47 and 07a87d6f518f, both reproduced. | 330–333 |
| 42 (rerun) | Nothing Important | The same song constants, lyric, designs and seed on v111. 1,000 main and 1,000 control, each twice. Survivors 780 and 783 (v110 567, 595); orders 08a4b2311f06 and cf1a424d0021, both reproduced. | 331–334 |

## The tests of 310–329 on song 40 (main run; held means held in the control too)

| Fix | Main | Held? |
|---|---|---|
| 310 | under floor 28.7%; parallel 0.098 (kept 0.14); paired lines 4817, partner given up 1529 | **no** |
| 311 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | verse 2.5%, chorus 2.7%; leap knob 1.0 | yes |
| 313 | share [0.0, 0.25, 0.5]; in range 51%; given up 23 (0.4%); left out 1507 | **no** |
| 314 | range [10.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.529, 0.588]; tonic nearest the sung median 0.928, the drawn centre 1.0; top fifth 92%; floor 69% | yes |
| 315 | amplitude 7.0; arch [-0.106, 0.104, 0.34]; the calibration stopped after round 2 (the amplitude's largest step twice) | yes |
| 316 | redraws 0/13375 = 0.0; entries on 0.23, after 0.639, pickup 0.131 (before 0.23, 0.647, 0.123) | yes |
| 317 | none in force | yes |
| 318 | straight eighths; sixteenth onsets [0.108, 0.145, 0.212] | printed |
| 322 | paired 4817 (990 of another length); given up 1529 (31.7%); parallel 0.098; under floor 28.7% | **no** |
| 323 | one-over bars copied without the weakest onset 3248; left out 1507; verse 2 in range 51% | **no** |
| 324 | 976 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | none in force | yes |
| 327 | join deaths 12 (v109 92); copies fitted again 119 (116 joins then held, 3 still short), could not move 9 | yes |
| 328 | q = 116, band 100-120: kept median 12%, quartiles not given in the paper's text (Table DQ's file not attached); song [0.108, 0.145, 0.212] | printed |
| 329 | sung [14.0, 17.0, 17.0] vs drawn [15.0, 17.0, 17.0] (gap [0.0, 0.0, 0.0]); chorus window [10.0, 11.0, 12.0]; heaviest give-aways ['distinct_pitches', 'chord_tones_on_long_notes', 'chord_tones', 'empty_bars', 'step']; extremes sung low 99%, high 100% | yes |

## The tests of 310–329 on song 42 (main run; held means held in the control too)

| Fix | Main | Held? |
|---|---|---|
| 310 | under floor 6.4%; parallel 0.188 (kept 0.14); paired lines 4208, partner given up 533 | yes |
| 311 | tonic 100.0%; registers redrawn 52; misses 0 | yes |
| 312 | verse 2.6%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | share [0.0, 0.375, 0.625]; in range 74%; given up 1 (0.0%); left out 82 | **no** |
| 314 | range [11.0, 15.0, 17.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.385, 0.455, 0.571]; tonic nearest the sung median 0.945, the drawn centre 1.0; top fifth 87%; floor 39% | yes |
| 315 | amplitude 5.0; arch [-0.168, 0.062, 0.314]; stop none | yes |
| 316 | redraws 0/9686 = 0.0; entries on 0.225, after 0.664, pickup 0.112 (before 0.216, 0.644, 0.14) | yes |
| 317 | the design gate (Q11 note 4) passed 98.3% of builds | yes |
| 318 | straight eighths, q = 76; sixteenth onsets [0.077, 0.109, 0.159] | printed |
| 322 | paired 4208 (2711 of another length); given up 533 (12.7%); parallel 0.188; under floor 6.4% | **no** |
| 323 | one-over bars copied without the weakest onset 981; left out 82; verse 2 in range 74% | **no** |
| 324 | 990 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | design failures for the registers 0; last chorus on the tonic 100.0%; registers redrawn for the design 52 | yes |
| 326 | 98.3% (control 99.5%) | yes |
| 327 | join deaths 0 (v109 92) | yes |
| 328 | q = 76, band under 80: kept median 34%, quartiles [0.26, 0.43]; song [0.077, 0.109, 0.159] | printed |
| 329 | sung [13.0, 17.0, 21.0] vs drawn [15.0, 17.0, 21.0] (gap [0.0, 0.0, 1.0]); chorus window [8.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'chord_tones', 'on_tonic', 'chord_tones_on_long_notes']; extremes sung low 97%, high 100% | yes |

319: these runs make no instrumental lines. 320: no figure here comes from a rescoring. 321: these tables. 322's test is written for song 40; on song 42 it reads 12.7% of partners given up. The control's columns are in the test report and in songs/p43.

## The fixes

### 330. Song 40's partners are given up by the near-length pairs, not by those of another length.

**Problem:** 322 does what it says: all 990 paired lines of another length kept their partner's stresses. But the 3,827 pairs within one syllable still copy every bar under 303's one-onset check, and 1,529 of them (40%) were given up.

**Evidence:** Song 40: partners given up 31.7% of paired lines (control 28.7%). The likeness of bar rhythms is 0.098 (0.112) against the kept 0.14. Builds under the floor are 28.7% (42.4%), from v110's 25.8% (28.5%). On song 42, partners are given up for 12.7% (10.5%) and the floor holds at 6.4% (4.4%).

**Fix:** A near-length partner whose bar copy fails the one-onset check falls back to 322's stressed onsets instead of being given up.

**Check:** On song 40: partners given up under one in ten; likeness at or above 0.14; builds under the floor under one in ten. Whether the floor follows the likeness is not known.

### 331. Verse 2's copied share is held down by 293's draw, not by the cap.

**Problem:** 323 copied the one-over bars and left verse 2's share where it was.

**Evidence:** One-over bars copied without the weakest onset: 3,248 on song 40 and 981 on song 42. Verse 2 is inside 25–75% in 51% of song 40's builds (64% control; v110 53%) and 74% of song 42's (82%; v110 71%). Song 40's median share is 0.25, the band's floor: 293 copies each bar at 40%, so about half the builds fall under a quarter.

**Fix:** Set 293's per-bar rate from the kept songs so that verse 2's share sits at the band's centre (a figure the paper does not give). Or read 313's test on the bars 293 chose to copy.

**Check:** Verse 2 inside 25–75% in three builds of four on both songs, main and control.

### 332. 315's stop also stops the window knobs.

**Problem:** The calibration returns as soon as a line knob takes its largest step two rounds running. It returns before that round's window knobs (chord tones, steps, gaps) are set and before the third round runs.

**Evidence:** Song 40 stopped after round 2 (the amplitude took its largest step twice):
- the window knobs had one round;
- the verse's chord-tone knob reads 1.46 (v110 1.97), and chord tones on the beat 0.55 (0.60);
- deaths at "key word on a chord tone" rose to 159 (control 103), from v110's 89 (42);
- the content judge's median stayed at -0.90 (-0.89), with chord tones among its five heaviest give-aways.

Song 42 did not stop; its key-word deaths rose from 17 to 34, which this does not explain.

**Fix:** The stop freezes only the knob that took the largest step; the other knobs finish their rounds.

**Check:** Song 40's key-word deaths at or under v110's 89 (main) and 42 (control), with 315's tests still held.

### 333. Fix 329 on a narrow row puts the song on the row's edges again.

**Problem:** Song 40's row (A3–D5) is 17 semitones, the kept median range, so the drawn range fills the row. Then 329 sings both its ends.

**Evidence:**
- Song 40: builds touching the row's floor rose to 69% (v110 38%) and those using its top fifth to 92% (74%). The sung range is 17 (12), the chorus's eight-bar range 11 (8).
- Range has left the content judge's five heaviest give-aways, but song 40's content median did not rise (-0.90). Distinct pitches is now the heaviest give-away.
- Song 42 (row 21 semitones): floor 39% (18%), top fifth 87% (69%).

**Fix:** Draw the song's range no wider than the row less two semitones, so the drawn extremes sit one semitone inside it.

**Check:** 329's three tests still hold, and the builds touching the row's floor fall to v110's level.

### 334. The tempo bands of 328 can be printed for one band only.

**Problem:** The report is to print the song's sixteenth share beside its tempo band's kept quartiles. The paper's text gives quartiles for the under-80 band only, and Table DQ's file is not attached.

**Evidence:** Song 42 at ♩ = 76 sings 10.9% of its onsets on a sixteenth (control 7.4%), below the under-80 band's 26–43%. Song 40 at 116 sings 14.5% (9.7%) against the 100–120 band's median of 12%, whose quartiles are not given.

**Fix:** Attach the count's file, or give every band's quartiles in the paper.

**Check:** The report prints every band's quartiles.

## Order of work

1. **332** (the calibration's stop freezes one knob, not all): it changes every later reading on song 40, so it goes first.
2. **330** (the near-length partners fall back to 322's stresses): song 40's floor.
3. **331** (293's rate from the kept songs): one count, and both songs' verse 2.
4. **333** (the drawn range inside the row).
5. **334** (the tempo count's file).

## Regression line

After these fixes, songs 40 and 42 rerun at PYTHONHASHSEED 0, N 1000, main and control, and each must reproduce its frozen order twice. Today's orders, which will change with the code:

- song 40: 7d491acfca47 and 07a87d6f518f (seed 20261511);
- song 42: 08a4b2311f06 and cf1a424d0021 (seed 20261552).

What must hold:

- every test that held here holds again: 311, 312, 314, 315, 316, 324, 325, 326, 327 and 329 on both songs, and 310 on song 42;
- song 40: under the floor under one in ten, the likeness of bar rhythms at 0.14 or more, and key-word deaths at or under v110's 89;
- verse 2 in range in three builds of four on both songs;
- the row's floor touched no more often than under v110;
- song 42 keeps its locked lyric and its design gate at nine in ten or more (98.3% here).

## Readings the paper does not give

- **322.** A stressed syllable off its partner's stressed onsets, in a bar where the partner has stresses, is weighted 0.04 (293's weight for a bar not copied). Unstressed syllables are drawn freely. The stresses are given up after 14 tries, as 310's copy is.
- **323.** The weakest onset is the one of lowest metric weight; on a tie, the later one goes. 303's one-onset check is then read against the bar without it.
- **324.** The centre of a section's drawn register is taken as its drawn median (the point the register is drawn around). The midpoint of its floor and cap differs by up to a semitone.
- **325.** Song 42's condition is that a tonic at or above the song's floor lies under some note the chorus register can end the hook on. The hook's end is drawn above the song's lowest tonic.
- **327.** Where a line cannot end with a breath before the copy that follows, the copy is fitted again without a pickup added before its source's entry. A unit's last line so fitted keeps the ordinary end (beat 4 of a one-bar line) in place of 310's beat 3. An exact copy cannot move, and that build dies as before.
- **329.** The song's extremes are taken as the lowest and highest scale notes inside the drawn range. One fresh line carries each: the low note in Verse 1 or the bridge, the high note in Chorus 1 or the bridge, the two lines distinct and chosen at random per build. The note goes at the contour's highest (lowest) point that the chord allows, and the contour is bent toward it; the extreme is dropped after six failed tries. No section is narrower than 13 semitones (the kept eight-bar range's 75th percentile) where the song's range allows.
- **328.** Only the under-80 band's quartiles are in the paper's text (26–43%). The other bands give medians only, since Table DQ's file is not with the paper.

## Blind-pick tally

No new song, so no new blind pick. The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40 and 41 are not yet offered.
