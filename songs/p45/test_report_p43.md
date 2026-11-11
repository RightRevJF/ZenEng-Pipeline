# ZenEng v113–v114: song 43, Blue Movie — test report

*Words and music: Jason Bryant. v113's fixes 337–339 and v114's 340–347 ported; findings numbered from 348 (v114's fixes took 340–347).*

## What was run

v113's 338 was ported onto the tested v112 search as melody_v113_p40.py, and v114's 340–347 onto that as melody_v114_p40.py. Song 43 is built on it (gen_p43.py): a new song, its lyric from the writer's sonnet, intake Q1–Q18 one question at a time, the full lyric shown before any music. The song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Nothing blocked the port, and no two fixes conflicted.

| Run | Survivors | Order | Rerun order | Reproduced |
|---|---|---|---|---|
| main (seed 20261553) | 811 | df5dff409ad9 | df5dff409ad9 | yes |
| control (seed 20261553) | 819 | e2d6fa8c04c5 | e2d6fa8c04c5 | yes |

## The table of tests (321)

Held in both the main run and the control: 22 of 26 with a test. Not held: 341, 344, 346, 347.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 1.6%; parallel 0.164 (kept 0.14); paired lines 3940, partner given up 0 | under floor 0.0%; parallel 0.168 (kept 0.14); paired lines 3965, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 2.7%, chorus 3.2%; leap knob 1.0 | verse 2.4%, chorus 3.3%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.125, 0.5, 0.75]; in range 84%; given up 2353 (58.8%); left out 70 | share [0.143, 0.5, 0.75]; in range 85%; given up 2336 (58.4%); left out 27 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [10.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.316, 0.526, 0.611]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 86%; floor 1% | range [10.0, 14.0, 17.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.471, 0.609]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 82%; floor 2% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.011, 0.162, 0.38]; stop none | amplitude 5.0; arch [0.002, 0.168, 0.384]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 0/4573 = 0.0; entries {'starts_on_downbeat': 0.273, 'starts_after_downbeat': 0.652, 'starts_as_pickup': 0.074} | redraws 0/4551 = 0.0; entries {'starts_on_downbeat': 0.272, 'starts_after_downbeat': 0.652, 'starts_as_pickup': 0.076} | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.93} | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.902} | yes |
| 318 | the feel named; sixteenths printed | a reading | up-tempo dance-pop, q = 118, four on the floor, straight; sixteenth onsets [0.031, 0.052, 0.081] | up-tempo dance-pop, q = 118, four on the floor, straight; sixteenth onsets [0.026, 0.041, 0.062] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 3940 (1554 of another length); given up 0 (0.0%); parallel 0.164; under floor 1.6% | paired 3965 (1582 of another length); given up 0 (0.0%); parallel 0.168; under floor 0.0% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 459; left out 70; verse 2 in range 84% | one-over bars copied without the weakest onset 355; left out 27; verse 2 in range 85% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 991 tonic endings, on the nearest to the centre 1.0 | 995 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.93} | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.902} | yes |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 0 (v109 92); refits {'327: sung-again line fitted after its downbeat': 51, '327: copy fitted again after its downbeat': 51} | join deaths 0 (v109 92); refits {'327: sung-again line fitted after its downbeat': 56, '327: copy fitted again after its downbeat': 56} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.031, 0.052, 0.081] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.026, 0.041, 0.062] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [0.0, 2.0, 2.0]); chorus window [8.0, 10.0, 13.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'gap_sixteenth', 'gap_eighth', 'on_offbeat_eighth']; extremes sung low 100%, high 100% | sung [13.0, 17.0, 17.0] vs drawn [14.0, 17.0, 19.0] (gap [0.0, 1.0, 2.0]); chorus window [8.0, 10.0, 13.0]; heaviest give-aways ['outside_scale', 'gap_sixteenth', 'empty_bars', 'gap_eighth', 'on_beats_2_4']; extremes sung low 100%, high 100% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.164; copies failed and the stresses kept 531; given up after the stresses 0; partners given up 0 (0.0%) | likeness 0.168; copies failed and the stresses kept 496; given up after the stresses 0; partners given up 0 (0.0%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.939; verse 2 share [0.125, 0.5, 0.75] (5th, median, 95th) | rate 0.954; verse 2 share [0.143, 0.5, 0.75] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 14 (v110 89); frozen none | key-word deaths 3 (v110 42); frozen none | reading |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.031, 0.052, 0.081] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.026, 0.041, 0.062] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 1.6%; content median 0.7, at kept 25th 36.2%, at kept median 3.8%; order median 1.82, at kept 25th 98.4%, at kept median 61.3%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 0.0%; content median 0.96, at kept 25th 41.8%, at kept median 3.1%; order median 1.89, at kept 25th 98.6%, at kept median 63.3%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | reading |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A) 69/98 (spread 12.4, a difference); bridge opening unrelated (208; 279) 37/26 (spread 7.8, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 29/25 (spread 7.2, no difference); chorus opening another tune (227; 279) 19/24 (spread 6.5, no difference); key word on a chord tone (134; 279) 14/3 (spread 4.1, a difference); the judge's floor (254; 279) 12/0 (spread 3.4, a difference) | design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A) 69/98 (spread 12.4, a difference); bridge opening unrelated (208; 279) 37/26 (spread 7.8, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 29/25 (spread 7.2, no difference); chorus opening another tune (227; 279) 19/24 (spread 6.5, no difference); key word on a chord tone (134; 279) 14/3 (spread 4.1, a difference); the judge's floor (254; 279) 12/0 (spread 3.4, a difference) | printed |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.125, 0.5, 0.75]; rate 0.939; copies given up 2353 | verse 2 share [0.143, 0.5, 0.75]; rate 0.954; copies given up 2336 | yes |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 8.95 (Window 134: 11.0, 10.4); costliest [('gap_eighth', 2.76), ('outside_scale', 1.59), ('unit3_returns', 1.48), ('on_offbeat_eighth', 0.8), ('on_beats_2_4', 0.5), ('distinct_pitches', 0.48), ('on_beat3', 0.44), ('chord_tones_on_downbeat', 0.36)] | gap 9.62 (Window 134: 11.0, 10.4); costliest [('gap_eighth', 3.42), ('unit3_returns', 1.57), ('outside_scale', 1.42), ('on_beats_2_4', 1.18), ('on_sixteenth', 0.74), ('on_offbeat_eighth', 0.65), ('distinct_pitches', 0.51), ('on_beat3', 0.45)] | printed |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 4713: pushed 22%, in runs 69%; sixteenth gaps cost 0.13 | sixteenth onsets 3574: pushed 13%, in runs 79%; sixteenth gaps cost -0.53 | **no** |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [3.875, 4.375, 4.625] (kept 3.6-4.1) | builds' notes a bar [3.75, 4.25, 4.625] (kept 3.6-4.1) | printed |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 4.0 at the median; cost 0.06; palette dropped for 40 lines | distinct lengths 4.0 at the median; cost -0.1; palette dropped for 42 lines | yes |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 1.3% (kept 7.1%); cost 1.59 | outside the scale 1.5% (kept 7.1%); cost 1.42 | **no** |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse -0.0, chorus -0.05; chord tones on long notes 62% | cost verse 0.02, chorus -0.09; chord tones on long notes 66% | yes |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.8, 'distinct_pitches': 0.48, 'unit2_returns': 0.05, 'unit3_returns': 1.48, 'unit4_to_unit2': -0.01} | costs {'on_offbeat_eighth': 0.65, 'distinct_pitches': 0.51, 'unit2_returns': 0.05, 'unit3_returns': 1.57, 'unit4_to_unit2': -0.01} | **no** |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('gap_eighth', 2.76), ('outside_scale', 1.59), ('unit3_returns', 1.48), ('on_offbeat_eighth', 0.8), ('on_beats_2_4', 0.5)]; gap 8.95 | over half a point: [('gap_eighth', 3.42), ('unit3_returns', 1.57), ('outside_scale', 1.42), ('on_beats_2_4', 1.18), ('on_sixteenth', 0.74), ('on_offbeat_eighth', 0.65), ('distinct_pitches', 0.51)]; gap 9.62 | **no** |

Notes. 322's and 332's tests are written for song 40 and are read here as readings. 319 has nothing to read here: the instrumental lines are written by the arrangement, and the consistency check reads their ranges.

## 340: the eight costliest measures (main run)

| Measure | Cost (points) | Kept mean | Builds' mean |
|---|---|---|---|
| gap_eighth | 2.76 | 0.465 | 0.606 |
| outside_scale | 1.59 | 0.071 | 0.013 |
| unit3_returns | 1.48 | 0.315 | 0.008 |
| on_offbeat_eighth | 0.8 | 0.371 | 0.431 |
| on_beats_2_4 | 0.5 | 0.21 | 0.232 |
| distinct_pitches | 0.48 | 6.382 | 6.975 |
| on_beat3 | 0.44 | 0.124 | 0.141 |
| chord_tones_on_downbeat | 0.36 | 0.722 | 0.564 |

The whole gap: 8.95 points (control 9.62), against Window 134's 11.0 and 10.4 for songs 40 and 42.

## 336's readings (main run, control in brackets)

| Reading | Song 43 | Kept |
|---|---|---|
| builds under the floor | 1.6% (0.0%) | 5% |
| content judge, median | 0.7 (0.96) | 4.16 |
| builds at the kept 25th / median, content | 36.2% / 3.8% (41.8% / 3.1%) | 75% / 50% |
| order judge, median | 1.82 (1.89) | 1.58 |
| content measures (of 46) with the median outside the kept middle half | 1 (1) | — |

## The pick

The rule of record (255: the composite's first inside the judge's top half) chose build 840d7b4af214. A note is repeated on 51% of its verse moves and 48% of its chorus moves, where the kept 75th percentile is 40% and the run's median is 25–27%; the chorus's first two lines sit on C4. The writer chose the judge's first instead (Q18 A): build dc24946f27cb, judge 4.55 (content 4.54, above the kept median of 4.16), composite rank 415 of 811. It is the record, with no hand edits. Finding 352.

## What the dense lyric costs (342)

The writer kept the lyric as written (Q14 A: 3.94 syllables a bar against the kept 3.6–4.1 notes a bar). The builds sing 4.4 notes a bar at the median. On 340's judge, gaps of an eighth cost 2.76 points in the main run and 3.42 in the control, the heaviest single cost: that is the price of the density, as 342 asks the report to say.

## Readings the paper does not give

- **The frame for a minor key.** The engine's tables and the judge's measures are major-keyed: the key profile, the window measures (`outside_scale` and the degree shares count against the major scale on the tonic), the PPM. The song is read on its relative major (C), and its endings are set on its own tonic (A). Finding 353.
- **338.** Every calibration round draws 30 builds as the run draws them. Verse 2's share for the rate is read there, and so are the knobs of 341, 344, 345 and 346.
- **341.** A sixteenth-position onset followed by a sixteenth is weighted 0.25 and one held an eighth or more is weighted 1.5. Sixteenth gaps take a knob set toward the kept 11% of gaps.
- **343.** Each section kind's palette: three, four or five lengths (one in four, two in four, one in four), the eighth always among them, the rest drawn at 288's class rates. A line with no rhythm in its palette is drawn without it and counted (40 lines in the main run).
- **344.** A build's outside-scale share is zero in half of builds, else a nonzero kept window's share. The share weights the song's sung extra pitch classes (here G♯ and F♯) through a knob.
- **345.** Long notes are a beat or more, read on the walk's provisional durations.
- **346.** The distinct-pitch aim weights a pitch already sung in the section. The unit returns are aimed at 17% (line 2 returning line 1) and 19% (line 4 returning line 2), in sections of two-bar lines.
- **340.** The judge is an L2 logistic regression (C = 1, balanced classes) on the 46 content measures, z-scored over the 314 kept windows and the builds' verse and chorus windows. A measure's cost is its weight times the kept mean less the builds' mean, over its spread.
- **337.** The spread of the difference between two counts x and y of 1,000 builds is the square root of x(1 − x/1000) + y(1 − y/1000).
- **The design (Q15 A).** The figure's rhythm is drawn from four placements with "mo" on beat 1 or 3 (232). The figure starts on the song's highest scale note unless a note would fall a tritone from its chord's root; then it starts a step lower (172 builds).

## Findings

### 348. Fix 341 does not make sixteenths pushes.

- *Problem.* Weighting a run down and a push up leaves the shape of the sixteenths almost where it was.
- *Evidence.* Of onsets on a sixteenth position: 22% pushed and 69% in runs (control 13% and 79%), against the kept 54% and 31%. The share of sixteenth gaps itself is at the kept figure (cost 0.13 points). Runs come from dense drawn lines, where the rhythm table outweighs a factor of 0.25, and from returning lines, whose words are fitted by splitting events on the sixteenth grid.
- *Fix.* In a drawn line, a sixteenth-position onset is allowed only as a push (the next onset an eighth or more later). A returning line's words are fitted by splitting on the eighth grid unless there is no room.
- *Check.* 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point.

### 349. Fix 344's weight cannot reach the kept share of notes outside the scale.

- *Problem.* The knob rose by its largest step each round (1 to 8) and the walk still offered almost no outside notes. The key profile weights an outside pitch class near zero, and half of builds are drawn at a share of zero.
- *Evidence.* Outside the scale 1.3% of notes (control 1.5%), kept 7.1%; cost 1.59 points (1.42), the second heaviest.
- *Fix.* Place the drawn share directly: the chosen notes (unstressed, a step from their neighbours, against no chord tone a semitone away, as fix 200 places them) move to the song's sung extra pitch class.
- *Check.* The mean within two points of the kept 7.1%; cost under half a point.

### 350. Four-line sections never return line 1 at line 3.

- *Problem.* The six-line verse and bridge plans are cut to four lines, and the cut drops their returns (ABCDAB becomes ABCD). Fix 346 aims only units 2 and 4.
- *Evidence.* Unit 3 returning unit 1: kept windows 31.5%, builds 0.8%; cost 1.48 points (control 1.57), the third heaviest.
- *Fix.* Draw four-line plans from the kept unit-return rates, unit 3 returning unit 1 at the kept 31.5%, with units 2 and 4 as 346 has them.
- *Check.* No unit return costs over half a point.

### 351. Fix 338's rate and fix 303's check pull against each other.

- *Problem.* Read on unaimed builds, the rate climbs to 0.94. At that rate 303's one-onset check gives up most copies, and the share reaches 50% only across the lines that are given up.
- *Evidence.* Rate 0.94 (control 0.95); copies given up for 2,353 of 4,000 verse 2 lines (59%; control 2,336). Verse 2's share is 50% at the median in both runs, so 338's test holds.
- *Fix.* A bar that fails 303's check is left out of that copy, and the rest of the line keeps its copied bars, instead of the whole line being given up. The rate is then read again.
- *Check.* Copies given up under one line in ten; the share within ten points of 50%.

### 352. The pick rule rewards repetition (255's open question).

- *Problem.* The composite's terms for compressibility and memory favour a melody that repeats itself. Its first inside the judge's top half was the most repetitive build in the run.
- *Evidence.* The pick by 255 repeats a note on 51% and 48% of moves (kept 75th percentile 40%; run median 25–27%), judge 1.69. The judge's first is judge 4.55 with content 4.54, above the kept median, and composite rank 415 of 811. The writer took the judge's first (Q18 A).
- *Fix.* The pick is the judge's first. Or it is the composite's first among builds whose readings are inside the kept middle half (repeats among them) and whose measures cost under half a point (347).
- *Check.* The pick's repeats inside the kept middle half, and the pick in the judge's top tenth of survivors.

### 353. The paper has no rule for a minor key.

- *Problem.* Every table the search reads is major-keyed. Read on a minor tonic, a minor song's natural notes count as outside the scale.
- *Evidence.* Song 43, in A minor, was read on C. Its endings were set on A by the song's own rules. The kept windows' outside-scale mean of 7.1% suggests the kept minor songs were read the same way, but the paper does not say.
- *Fix.* State how a minor song is read (on its relative major, or on its tonic with the minor scale), and how the kept minor songs were read.
- *Check.* The paper names the rule. A minor song's degree and outside-scale readings sit in the kept range.

## Where this leaves the song

The song is written and delivered: 811 of 1,000 builds survived (control 819), 1.6% under the judge's floor, content median 0.70. Of the tests with a pass or fail, 23 of 27 held. 341, 344, 346 and 347 did not: the gap is 8.95 points (control 9.62), against Window 134's 11.0 and 10.4.
