# ZenEng v111: songs 40 and 42 again — test report

*Words and music of both songs: Jason Bryant. Fixes 322–329 ported; findings numbered from 330.*

## What was run

v111's fixes 322–329 were ported onto the tested v110 search (songs/p42/melody_v110_p40.py) as melody_v111_p40.py, and song 42 was built on it again from the same song constants (gen_p42_v111.py: the same lyric, intake, designs and seed). Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Nothing blocked the port and no two fixes conflicted.

| Song | Run | Survivors (v110) | Order | Rerun order | Reproduced |
|---|---|---|---|---|---|
| 40 (seed 20261511) | main | 480 (505) | 7d491acfca47 | 7d491acfca47 | yes |
| 40 (seed 20261511) | control | 417 (537) | 07a87d6f518f | 07a87d6f518f | yes |
| 42 (seed 20261552) | main | 780 (567) | 08a4b2311f06 | 08a4b2311f06 | yes |
| 42 (seed 20261552) | control | 783 (595) | cf1a424d0021 | cf1a424d0021 | yes |

## The table of tests: Song 40, Nothing Else on Earth

Held in both the main run and the control: 13 of 17 with a test. Not held: 310, 313, 322, 323.

| Fix | Test | Main | Control | Held? |
|---|---|---|---|---|
| 310 | under the floor < 10%; likeness of bar rhythms (parallel) >= kept 0.14 at the median; no judge refitted | under floor 28.7%; parallel 0.098 (kept 0.14); paired lines 4817, partner given up 1529 | under floor 42.4%; parallel 0.112 (kept 0.14); paired lines 4761, partner given up 1368 | **no** |
| 311 | the last chorus on the tonic in every build; misses none | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | leaps past a fifth <= 3.6% of moves at the median, verse and chorus | verse 2.5%, chorus 2.7%; leap knob 1.0 | verse 2.5%, chorus 2.8%; leap knob 1.0 | yes |
| 313 | verse 2 shares 25-75% in 3 builds of 4; copies given up < 1 line in 20 | share [0.0, 0.25, 0.5]; in range 51%; given up 23 (0.4%); left out 1507 | share [0.083, 0.273, 0.5]; in range 64%; given up 17 (0.3%); left out 1272 | **no** |
| 314 | range printed; unused above/below differ by 1 at most; verse median 40-57% of the range; tonic endings nearest the centre (as 324 reads it) | range [10.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.529, 0.588]; tonic nearest the sung median 0.928, the drawn centre 1.0; top fifth 92%; floor 69% | range [10.0, 14.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.529, 0.571]; tonic nearest the sung median 0.967, the drawn centre 1.0; top fifth 92%; floor 69% | yes |
| 315 | amplitude <= 7; calibration stops on two largest steps running; arch over the span 0.0-0.55 at the median | amplitude 7.0; arch [-0.106, 0.104, 0.34]; stop ["calibration stopped after round 2: ['amp'] took the largest step two rounds running"] | amplitude 7.0; arch [-0.132, 0.064, 0.274]; stop ["calibration stopped after round 2: ['amp'] took the largest step two rounds running"] | yes |
| 316 | redraws per long line < 1.5; entry shares unchanged | redraws 0/13375 = 0.0; entries {'starts_on_downbeat': 0.23, 'starts_after_downbeat': 0.639, 'starts_as_pickup': 0.131} (before {'starts_on_downbeat': 0.23, 'starts_after_downbeat': 0.647, 'starts_as_pickup': 0.123}) | redraws 0/13343 = 0.0; entries {'starts_on_downbeat': 0.227, 'starts_after_downbeat': 0.644, 'starts_as_pickup': 0.129} (before {'starts_on_downbeat': 0.244, 'starts_after_downbeat': 0.628, 'starts_as_pickup': 0.129}) | yes |
| 317 | each design gate's pass rate printed; nine in ten or more | none in force | none in force | yes |
| 318 | the feel named; sixteenths printed | straight eighths; sixteenth onsets [0.108, 0.145, 0.212] | straight eighths; sixteenth onsets [0.08, 0.097, 0.119] | printed |
| 319 | no instrumental note outside its instrument | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | song 40: partners given up < 1 paired line in 10; likeness >= 0.14 at the median; under the floor < 1 in 10 | paired 4817 (990 of another length); given up 1529 (31.7%); parallel 0.098; under floor 28.7% | paired 4761 (990 of another length); given up 1368 (28.7%); parallel 0.112; under floor 42.4% | **no** |
| 323 | verse 2 shares 25-75% of verse 1's bar rhythms in 3 builds of 4, main and control | one-over bars copied without the weakest onset 3248; left out 1507; verse 2 in range 51% | one-over bars copied without the weakest onset 2699; left out 1272; verse 2 in range 64% | **no** |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | 976 tonic endings, on the nearest to the centre 1.0 | 988 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no build dies at a design gate for want of a note the registers could not hold; the last chorus on the tonic in every complete build | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | nine builds in ten pass each design gate | none in force | none in force | yes |
| 327 | song 40: deaths at the breath before a copy at or under v109's 92 in 1,000 | join deaths 12 (v109 92); refits {'327: copy could not enter later (return, entry pickup)': 9, '327: return fitted again without a pickup, ordinary end': 46, '327: copy fitted again after its downbeat': 116, '327: plan fitted again without a pickup, ordinary end': 67, '327: copy fitted again after its downbeat, join still short': 3, '327: plan fitted again without a pickup': 6} | join deaths 2 (v109 92); refits {'327: plan fitted again without a pickup, ordinary end': 63, '327: copy fitted again after its downbeat': 110, '327: return fitted again without a pickup, ordinary end': 42, '327: plan fitted again without a pickup': 5, '327: copy could not enter later (return, entry pickup)': 2} | yes |
| 328 | the sixteenth share printed beside its tempo band | q = 116, band 100-120: kept median 12%, quartiles not given in the paper's text (Table DQ's file not attached); song [0.108, 0.145, 0.212] | q = 116, band 100-120: kept median 12%, quartiles not given in the paper's text (Table DQ's file not attached); song [0.08, 0.097, 0.119] | printed |
| 329 | sung range within 2 of the drawn at the median; chorus window range >= 10 at the median; range not among the content judge's five heaviest give-aways | sung [14.0, 17.0, 17.0] vs drawn [15.0, 17.0, 17.0] (gap [0.0, 0.0, 0.0]); chorus window [10.0, 11.0, 12.0]; heaviest give-aways ['distinct_pitches', 'chord_tones_on_long_notes', 'chord_tones', 'empty_bars', 'step']; extremes sung low 99%, high 100% | sung [14.0, 17.0, 17.0] vs drawn [14.0, 17.0, 17.0] (gap [0.0, 0.0, 0.0]); chorus window [10.0, 11.0, 12.0]; heaviest give-aways ['distinct_pitches', 'on_offbeat_eighth', 'gap_eighth', 'chord_tones_on_long_notes', 'empty_bars']; extremes sung low 99%, high 100% | yes |

## The table of tests: Song 42, Nothing Important

Held in both the main run and the control: 14 of 17 with a test. Not held: 313, 322, 323.

| Fix | Test | Main | Control | Held? |
|---|---|---|---|---|
| 310 | under the floor < 10%; likeness of bar rhythms (parallel) >= kept 0.14 at the median; no judge refitted | under floor 6.4%; parallel 0.188 (kept 0.14); paired lines 4208, partner given up 533 | under floor 4.4%; parallel 0.184 (kept 0.14); paired lines 4178, partner given up 440 | yes |
| 311 | the last chorus on the tonic in every build; misses none | tonic 100.0%; registers redrawn 52; misses 0 | tonic 100.0%; registers redrawn 52; misses 0 | yes |
| 312 | leaps past a fifth <= 3.6% of moves at the median, verse and chorus | verse 2.6%, chorus 0.0%; leap knob 1.0 | verse 2.6%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | verse 2 shares 25-75% in 3 builds of 4; copies given up < 1 line in 20 | share [0.0, 0.375, 0.625]; in range 74%; given up 1 (0.0%); left out 82 | share [0.125, 0.375, 0.714]; in range 82%; given up 1 (0.0%); left out 1 | **no** |
| 314 | range printed; unused above/below differ by 1 at most; verse median 40-57% of the range; tonic endings nearest the centre (as 324 reads it) | range [11.0, 15.0, 17.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.385, 0.455, 0.571]; tonic nearest the sung median 0.945, the drawn centre 1.0; top fifth 87%; floor 39% | range [11.0, 15.0, 17.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.467, 0.579]; tonic nearest the sung median 0.962, the drawn centre 1.0; top fifth 87%; floor 39% | yes |
| 315 | amplitude <= 7; calibration stops on two largest steps running; arch over the span 0.0-0.55 at the median | amplitude 5.0; arch [-0.168, 0.062, 0.314]; stop none | amplitude 5.0; arch [-0.145, 0.095, 0.359]; stop none | yes |
| 316 | redraws per long line < 1.5; entry shares unchanged | redraws 0/9686 = 0.0; entries {'starts_on_downbeat': 0.225, 'starts_after_downbeat': 0.664, 'starts_as_pickup': 0.112} (before {'starts_on_downbeat': 0.216, 'starts_after_downbeat': 0.644, 'starts_as_pickup': 0.14}) | redraws 0/9645 = 0.0; entries {'starts_on_downbeat': 0.228, 'starts_after_downbeat': 0.665, 'starts_as_pickup': 0.107} (before {'starts_on_downbeat': 0.212, 'starts_after_downbeat': 0.634, 'starts_as_pickup': 0.154}) | yes |
| 317 | each design gate's pass rate printed; nine in ten or more | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.983} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.995} | yes |
| 318 | the feel named; sixteenths printed | straight eighths, q = 76; sixteenth onsets [0.077, 0.109, 0.159] | straight eighths, q = 76; sixteenth onsets [0.06, 0.074, 0.09] | printed |
| 319 | no instrumental note outside its instrument | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | song 40: partners given up < 1 paired line in 10; likeness >= 0.14 at the median; under the floor < 1 in 10 | paired 4208 (2711 of another length); given up 533 (12.7%); parallel 0.188; under floor 6.4% | paired 4178 (2693 of another length); given up 440 (10.5%); parallel 0.184; under floor 4.4% | **no** |
| 323 | verse 2 shares 25-75% of verse 1's bar rhythms in 3 builds of 4, main and control | one-over bars copied without the weakest onset 981; left out 82; verse 2 in range 74% | one-over bars copied without the weakest onset 369; left out 1; verse 2 in range 82% | **no** |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | 990 tonic endings, on the nearest to the centre 1.0 | 989 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no build dies at a design gate for want of a note the registers could not hold; the last chorus on the tonic in every complete build | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 52} | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 52} | yes |
| 326 | nine builds in ten pass each design gate | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.983} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.995} | yes |
| 327 | song 40: deaths at the breath before a copy at or under v109's 92 in 1,000 | join deaths 0 (v109 92); refits {} | join deaths 0 (v109 92); refits {} | yes |
| 328 | the sixteenth share printed beside its tempo band | q = 76, band under 80: kept median 34%, quartiles [0.26, 0.43]; song [0.077, 0.109, 0.159] | q = 76, band under 80: kept median 34%, quartiles [0.26, 0.43]; song [0.06, 0.074, 0.09] | printed |
| 329 | sung range within 2 of the drawn at the median; chorus window range >= 10 at the median; range not among the content judge's five heaviest give-aways | sung [13.0, 17.0, 21.0] vs drawn [15.0, 17.0, 21.0] (gap [0.0, 0.0, 1.0]); chorus window [8.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'chord_tones', 'on_tonic', 'chord_tones_on_long_notes']; extremes sung low 97%, high 100% | sung [13.0, 17.0, 21.0] vs drawn [15.0, 17.0, 21.0] (gap [0.0, 0.0, 1.0]); chorus window [8.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'on_beats_2_4', 'on_tonic', 'on_offbeat_eighth']; extremes sung low 98%, high 100% | yes |

Notes on the tables. 314's tonic test is read on the drawn register's centre, as 324 amends it; read on the sung median it gives 92.8% (song 40) and 94.5% (song 42). 322's and 327's tests are written for song 40; song 42's readings are printed beside them (322 on song 42: partners given up 12.7%, so it is shown as not held). 319 has nothing to read: these runs make no instrumental lines.

## Table DQ again: v110 and v111 (main runs)

| Reading | Song 40, v110 | Song 40, v111 | Song 42, v110 | Song 42, v111 | Kept |
|---|---|---|---|---|---|
| survivors of 1,000 | 505 | 480 | 567 | 780 | — |
| builds under the judge's floor | 25.8% | 28.7% | 6.4% | 6.4% | 5% |
| content judge, median | -0.89 | -0.9 | -0.58 | -0.46 | 4.16 |
| order judge, median | 0.6 | 0.53 | 2.11 | 2.08 | 1.58 |
| likeness of bar rhythms between lines | 0.094 | 0.098 | 0.188 | 0.188 | 0.14 (0.04 to 0.23) |
| contour amplitude | 5.0 | 7.0 | 7.0 | 5.0 | — |
| arch term over the line's span | 0.08 | 0.1 | 0.05 | 0.06 | 0.23 (0.00 to 0.55) |
| leaps past a fifth, verse, % of moves | 0.0 | 2.5 | 2.5 | 2.6 | 0 (75th 3.6) |
| the song's sung range, semitones | 12.0 | 17.0 | 14.0 | 17.0 | 17 (14.5 to 22) |
| range in eight bars, verse / chorus | 10 / 8 | 12 / 11 | 10 / 8 | 11 / 10 | 10 (8 to 13) |
| builds that touch the row's floor | 37.9% | 69.0% | 17.8% | 39.0% | — |
| builds that use the row's top fifth | 73.6% | 92.5% | 69.0% | 86.8% | — |

The v110 columns are read here on all of v110's complete builds (Window 131 read the first 600), so a few differ from Table DQ in the second decimal.

## Readings the paper does not give

- **322.** A stressed syllable off its partner's stressed onsets, in a bar where the partner has stresses, is weighted 0.04 (293's weight for a bar not copied). Unstressed syllables are drawn freely. The stresses are given up after 14 tries, as 310's copy is.
- **323.** The weakest onset is the one of lowest metric weight; on a tie, the later one goes. 303's one-onset check is then read against the bar without it.
- **324.** The centre of a section's drawn register is taken as its drawn median (the point the register is drawn around). The midpoint of its floor and cap differs by up to a semitone.
- **325.** Song 42's condition is that a tonic at or above the song's floor lies under some note the chorus register can end the hook on. The hook's end is drawn above the song's lowest tonic.
- **327.** Where a line cannot end with a breath before the copy that follows, the copy is fitted again without a pickup added before its source's entry. A unit's last line so fitted keeps the ordinary end (beat 4 of a one-bar line) in place of 310's beat 3. An exact copy cannot move, and that build dies as before.
- **329.** The song's extremes are taken as the lowest and highest scale notes inside the drawn range. One fresh line carries each:
  - the low note in Verse 1 or the bridge, the high note in Chorus 1 or the bridge, the two lines distinct and chosen at random per build;
  - the note is placed at the contour's highest (lowest) point that the chord allows, and the contour is bent toward it;
  - the extreme is dropped after six failed tries.
  
  No section is narrower than 13 semitones (the kept eight-bar range's 75th percentile) where the song's range allows.
- **328.** Only the under-80 band's quartiles are in the paper's text (26–43%). The other bands give medians only, since Table DQ's file is not with the paper.

## Findings

### 330. Song 40's partners are given up by the near-length pairs, not by those of another length.

- *Problem.* 322 does what it says: all 990 paired lines of another length kept their partner's stresses. But the 3,827 pairs within one syllable still copy every bar under 303's one-onset check, and 1,529 of them (40%) were given up.
- *Evidence.* Song 40: partners given up 31.7% of paired lines (control 28.7%). The likeness of bar rhythms is 0.098 (0.112) against the kept 0.14. Builds under the floor are 28.7% (42.4%), from v110's 25.8% (28.5%). On song 42, partners are given up for 12.7% (10.5%) and the floor holds at 6.4% (4.4%).
- *Fix.* A near-length partner whose bar copy fails the one-onset check falls back to 322's stressed onsets instead of being given up.
- *Check.* On song 40: partners given up under one in ten; likeness at or above 0.14; builds under the floor under one in ten. Whether the floor follows the likeness is not known.

### 331. Verse 2's copied share is held down by 293's draw, not by the cap.

- *Problem.* 323 copied the one-over bars and left verse 2's share where it was.
- *Evidence.* One-over bars copied without the weakest onset: 3,248 on song 40 and 981 on song 42. Verse 2 is inside 25–75% in 51% of song 40's builds (64% control; v110 53%) and 74% of song 42's (82%; v110 71%). Song 40's median share is 0.25, the band's floor: 293 copies each bar at 40%, so about half the builds fall under a quarter.
- *Fix.* Set 293's per-bar rate from the kept songs so that verse 2's share sits at the band's centre (a figure the paper does not give). Or read 313's test on the bars 293 chose to copy.
- *Check.* Verse 2 inside 25–75% in three builds of four on both songs, main and control.

### 332. 315's stop also stops the window knobs.

- *Problem.* The calibration returns as soon as a line knob takes its largest step two rounds running. It returns before that round's window knobs (chord tones, steps, gaps) are set and before the third round runs.
- *Evidence.* Song 40 stopped after round 2 (the amplitude took its largest step twice):
  - the window knobs had one round;
  - the verse's chord-tone knob reads 1.46 (v110 1.97), and chord tones on the beat 0.55 (0.60);
  - deaths at "key word on a chord tone" rose to 159 (control 103), from v110's 89 (42);
  - the content judge's median stayed at -0.90 (-0.89), with chord tones among its five heaviest give-aways.

  Song 42 did not stop; its key-word deaths rose from 17 to 34, which this does not explain.
- *Fix.* The stop freezes only the knob that took the largest step; the other knobs finish their rounds.
- *Check.* Song 40's key-word deaths at or under v110's 89 (main) and 42 (control), with 315's tests still held.

### 333. Fix 329 on a narrow row puts the song on the row's edges again.

- *Problem.* Song 40's row (A3–D5) is 17 semitones, the kept median range, so the drawn range fills the row. Then 329 sings both its ends.
- *Evidence.*
  - Song 40: builds touching the row's floor rose to 69% (v110 38%) and those using its top fifth to 92% (74%). The sung range is 17 (12), the chorus's eight-bar range 11 (8).
  - Range has left the content judge's five heaviest give-aways, but song 40's content median did not rise (-0.90). Distinct pitches is now the heaviest give-away.
  - Song 42 (row 21 semitones): floor 39% (18%), top fifth 87% (69%).
- *Fix.* Draw the song's range no wider than the row less two semitones, so the drawn extremes sit one semitone inside it.
- *Check.* 329's three tests still hold, and the builds touching the row's floor fall to v110's level.

### 334. The tempo bands of 328 can be printed for one band only.

- *Problem.* The report is to print the song's sixteenth share beside its tempo band's kept quartiles. The paper's text gives quartiles for the under-80 band only, and Table DQ's file is not attached.
- *Evidence.* Song 42 at ♩ = 76 sings 10.9% of its onsets on a sixteenth (control 7.4%), below the under-80 band's 26–43%. Song 40 at 116 sings 14.5% (9.7%) against the 100–120 band's median of 12%, whose quartiles are not given.
- *Fix.* Attach the count's file, or give every band's quartiles in the paper.
- *Check.* The report prints every band's quartiles.

## What this means for the two clean songs

Neither song passes.

- **Song 40** still fails its floor (310, 322) and verse 2's share (313, 323).
- **Song 42** fails only verse 2's share: 74% of main builds, one point short of three in four. It passed 82% in the control. 322's test, written for song 40, also reads short on song 42: 12.7% of partners given up.

324, 325, 326, 327 and 329 held their tests on both songs. 322 and 323 did not. Two side effects came with the port: 332 (the calibration's stop) and 333 (the edges of a narrow row).
