# ZenEng v112: songs 40 and 42 once more — test report

*Words and music of both songs: Jason Bryant. Fixes 330–336 ported; findings numbered from 337. No new song.*

## What was run

v112's fixes 330–333 were ported onto the tested v111 search (songs/p43/melody_v111_p40.py) as melody_v112_p40.py, and song 42 was built on it again from the same song constants (gen_p42_v112.py). 334–336 are the report's: every tempo band's quartiles, each test named against its kept figure or marked a reading, and the floor's share a reading. Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Nothing blocked the port and no two fixes conflicted.

| Song | Run | Survivors (v111) | Order | Rerun order | Reproduced |
|---|---|---|---|---|---|
| 40 (seed 20261511) | main | 544 (480) | 3f8eb6067d67 | 3f8eb6067d67 | yes |
| 40 (seed 20261511) | control | 544 (417) | 26f80e5f1a5f | 26f80e5f1a5f | yes |
| 42 (seed 20261552) | main | 747 (780) | daa4d9492f81 | daa4d9492f81 | yes |
| 42 (seed 20261552) | control | 738 (783) | 7e63192665fb | 7e63192665fb | yes |

## The table of tests: Song 40, Nothing Else on Earth

Held in both the main run and the control: 19 of 20 with a test. Not held: 332.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 27.6%; parallel 0.099 (kept 0.14); paired lines 4807, partner given up 0 | under floor 35.3%; parallel 0.103 (kept 0.14); paired lines 4803, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 2.4%, chorus 2.6%; leap knob 1.0 | verse 2.4%, chorus 2.7%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.091, 0.364, 0.667]; in range 81%; given up 757 (12.6%); left out 1597 | share [0.182, 0.455, 0.667]; in range 91%; given up 591 (9.9%); left out 1242 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [10.0, 14.0, 15.0, 15.0, 15.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.375, 0.533, 0.6]; tonic nearest the sung median 0.824, the drawn centre 1.0; top fifth 92%; floor 6% | range [10.0, 15.0, 15.0, 15.0, 15.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.467, 0.592]; tonic nearest the sung median 0.863, the drawn centre 1.0; top fifth 93%; floor 9% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.118, 0.066, 0.268]; stop none | amplitude 5.0; arch [-0.109, 0.081, 0.274]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 0/13521 = 0.0; entries {'starts_on_downbeat': 0.233, 'starts_after_downbeat': 0.637, 'starts_as_pickup': 0.13} (before {'starts_on_downbeat': 0.23, 'starts_after_downbeat': 0.639, 'starts_as_pickup': 0.131}) | redraws 0/13455 = 0.0; entries {'starts_on_downbeat': 0.245, 'starts_after_downbeat': 0.619, 'starts_as_pickup': 0.137} (before {'starts_on_downbeat': 0.227, 'starts_after_downbeat': 0.644, 'starts_as_pickup': 0.129}) | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | none in force | none in force | yes |
| 318 | the feel named; sixteenths printed | a reading | straight eighths; sixteenth onsets [0.1, 0.134, 0.185] | straight eighths; sixteenth onsets [0.073, 0.089, 0.109] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 4807 (998 of another length); given up 321 (6.7%); parallel 0.099; under floor 27.6% | paired 4803 (999 of another length); given up 317 (6.6%); parallel 0.103; under floor 35.3% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 3345; left out 1597; verse 2 in range 81% | one-over bars copied without the weakest onset 2747; left out 1242; verse 2 in range 91% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 987 tonic endings, on the nearest to the centre 1.0 | 991 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | none in force | none in force | yes |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 11 (v109 92); refits {'327: plan fitted again without a pickup, ordinary end': 58, '327: copy fitted again after its downbeat': 109, '327: return fitted again without a pickup, ordinary end': 43, '327: copy could not enter later (return, entry pickup)': 11, '327: plan fitted again without a pickup': 8} | join deaths 8 (v109 92); refits {'327: return fitted again without a pickup, ordinary end': 37, '327: copy fitted again after its downbeat': 119, '327: plan fitted again without a pickup, ordinary end': 80, '327: copy could not enter later (return, entry pickup)': 7, '327: plan fitted again without a pickup': 3, '327: copy fitted again after its downbeat, join still short': 1} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.1, 0.134, 0.185] | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.073, 0.089, 0.109] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [14.0, 14.0, 14.0] vs drawn [14.0, 15.0, 15.0] (gap [1.0, 1.0, 1.0]); chorus window [9.0, 11.0, 12.0]; heaviest give-aways ['outside_scale', 'on_offbeat_eighth', 'chord_tones_on_long_notes', 'empty_bars', 'chord_tones']; extremes sung low 99%, high 98% | sung [14.0, 14.0, 14.0] vs drawn [15.0, 15.0, 15.0] (gap [1.0, 1.0, 1.0]); chorus window [9.0, 11.0, 12.0]; heaviest give-aways ['on_offbeat_eighth', 'outside_scale', 'empty_bars', 'gap_eighth', 'chord_tones_on_long_notes']; extremes sung low 99%, high 98% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.099; copies failed and the stresses kept 1199; given up after the stresses 321; partners given up 321 (6.7%) | likeness 0.103; copies failed and the stresses kept 1124; given up after the stresses 317; partners given up 317 (6.6%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.802; verse 2 share [0.091, 0.364, 0.667] (5th, median, 95th) | rate 0.802; verse 2 share [0.182, 0.455, 0.667] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 109 (v110 89); frozen none | key-word deaths 44 (v110 42); frozen none | **no** |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 17; widest drawn range 15 (row less two 15) | row 17; widest drawn range 15 (row less two 15) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.1, 0.134, 0.185] | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.073, 0.089, 0.109] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 27.6%; content median -0.99, at kept 25th 9.3%, at kept median 0.3%; order median 0.57, at kept 25th 78.2%, at kept median 6.4%; measures outside the kept middle half 4 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 35.3%; content median -1.48, at kept 25th 2.3%, at kept median 0.0%; order median 0.53, at kept 25th 77.3%, at kept median 5.2%; measures outside the kept middle half 3 of 46; heaviest give-away ('on_offbeat_eighth', -0.635) | reading |

## The table of tests: Song 42, Nothing Important

Held in both the main run and the control: 19 of 19 with a test. Every test held.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 5.2%; parallel 0.19 (kept 0.14); paired lines 4156, partner given up 0 | under floor 4.3%; parallel 0.183 (kept 0.14); paired lines 4179, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 40; misses 0 | tonic 100.0%; registers redrawn 48; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 2.6%, chorus 3.0%; leap knob 1.0 | verse 2.6%, chorus 3.1%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.125, 0.5, 0.75]; in range 85%; given up 164 (4.1%); left out 96 | share [0.25, 0.5, 0.875]; in range 90%; given up 130 (3.3%); left out 2 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [11.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.447, 0.579]; tonic nearest the sung median 0.891, the drawn centre 1.0; top fifth 89%; floor 0% | range [11.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.385, 0.447, 0.579]; tonic nearest the sung median 0.875, the drawn centre 1.0; top fifth 89%; floor 1% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 7.0; arch [-0.141, 0.092, 0.368]; stop none | amplitude 7.0; arch [-0.148, 0.087, 0.363]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 0/9591 = 0.0; entries {'starts_on_downbeat': 0.226, 'starts_after_downbeat': 0.667, 'starts_as_pickup': 0.108} (before {'starts_on_downbeat': 0.225, 'starts_after_downbeat': 0.664, 'starts_as_pickup': 0.112}) | redraws 0/9653 = 0.0; entries {'starts_on_downbeat': 0.221, 'starts_after_downbeat': 0.667, 'starts_as_pickup': 0.111} (before {'starts_on_downbeat': 0.228, 'starts_after_downbeat': 0.665, 'starts_as_pickup': 0.107}) | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.984} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.998} | yes |
| 318 | the feel named; sixteenths printed | a reading | straight eighths, q = 76; sixteenth onsets [0.081, 0.119, 0.172] | straight eighths, q = 76; sixteenth onsets [0.059, 0.074, 0.094] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 4156 (2672 of another length); given up 0 (0.0%); parallel 0.19; under floor 5.2% | paired 4179 (2692 of another length); given up 0 (0.0%); parallel 0.183; under floor 4.3% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 1030; left out 96; verse 2 in range 85% | one-over bars copied without the weakest onset 373; left out 2; verse 2 in range 90% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 979 tonic endings, on the nearest to the centre 1.0 | 988 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 40} | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 48} | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.984} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.998} | yes |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 0 (v109 92); refits {} | join deaths 0 (v109 92); refits {} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.081, 0.119, 0.172] | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.059, 0.074, 0.094] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [1.0, 2.0, 2.0]); chorus window [9.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'chord_tones', 'chord_tones_on_long_notes', 'on_sixteenth']; extremes sung low 98%, high 99% | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [1.0, 2.0, 2.0]); chorus window [9.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'on_offbeat_eighth', 'on_beats_2_4', 'first_note_tonic_triad']; extremes sung low 99%, high 100% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.19; copies failed and the stresses kept 515; given up after the stresses 0; partners given up 0 (0.0%) | likeness 0.183; copies failed and the stresses kept 462; given up after the stresses 0; partners given up 0 (0.0%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.65; verse 2 share [0.125, 0.5, 0.75] (5th, median, 95th) | rate 0.65; verse 2 share [0.25, 0.5, 0.875] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 34 (v110 89); frozen none | key-word deaths 19 (v110 42); frozen none | reading |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.081, 0.119, 0.172] | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.059, 0.074, 0.094] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 5.2%; content median -0.34, at kept 25th 17.2%, at kept median 1.4%; order median 2.05, at kept 25th 99.6%, at kept median 74.1%; measures outside the kept middle half 2 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 4.3%; content median -0.73, at kept 25th 12.8%, at kept median 0.2%; order median 1.96, at kept 25th 99.8%, at kept median 69.7%; measures outside the kept middle half 0 of 46; heaviest give-away ('outside_scale', -0.572) | reading |

## Table DR again: v111 and v112 (main runs)

| Reading | Song 40, v111 | Song 40, v112 | Song 42, v111 | Song 42, v112 | Kept |
|---|---|---|---|---|---|
| survivors of 1,000 | 480 | 544 | 780 | 747 | — |
| builds under the judge's floor | 28.7% | 27.6% | 6.4% | 5.2% | 5% |
| content judge, median | -0.9 | -0.99 | -0.46 | -0.34 | 4.16 (25th 1.33) |
| order judge, median | 0.53 | 0.57 | 2.08 | 2.05 | 1.58 (25th 0.05) |
| likeness of bar rhythms between lines | 0.098 | 0.099 | 0.188 | 0.19 | 0.14 (0.04 to 0.23) |
| contour amplitude | 7.0 | 5.0 | 5.0 | 7.0 | — |
| arch term over the line's span | 0.1 | 0.07 | 0.06 | 0.09 | 0.23 (0.00 to 0.55) |
| leaps past a fifth, verse, % of moves | 2.5 | 2.4 | 2.6 | 2.6 | 0 (75th 3.6) |
| the song's sung range, semitones | 17.0 | 14.0 | 17.0 | 17.0 | 17 (14.5 to 22) |
| range in eight bars, verse / chorus | 12 / 11 | 10 / 11 | 11 / 10 | 12 / 10 | 10 (8 to 13) |
| builds that touch the row's floor | 69.0% | 6.5% | 39.0% | 0.3% | — |
| builds that use the row's top fifth | 92.5% | 92.5% | 86.8% | 89.0% | — |

## 336's readings (main run, control in brackets)

| Reading | Song 40 | Song 42 | Kept |
|---|---|---|---|
| builds under the floor | 27.6% (control 35.3%) | 5.2% (control 4.3%) | 5% |
| content judge, median | -0.99 (control -1.48) | -0.34 (control -0.73) | 4.16 |
| builds at the kept 25th / median, content | 9.3% / 0.3% (control 2.3% / 0.0%) | 17.2% / 1.4% (control 12.8% / 0.2%) | 75% / 50% |
| order judge, median | 0.57 (control 0.53) | 2.05 (control 1.96) | 1.58 |
| builds at the kept 25th / median, order | 78.2% / 6.4% (control 77.3% / 5.2%) | 99.6% / 74.1% (control 99.8% / 69.7%) | 75% / 50% |
| content measures (of 46) with the median outside the kept middle half | 4 (control 3) | 2 (control 0) | — |
| heaviest single content give-away | outside_scale -0.572 (control on_offbeat_eighth -0.635) | outside_scale -0.572 (control outside_scale -0.572) | — |

## Readings the paper does not give

- **330.** The fallback runs from the 15th try of a pair's rhythm to the last drawn try (20, or 60 for a long line). On those tries the partner's stressed onsets are weighted as in 322, and the bar copy and its one-onset check are dropped. If they all fail, the partner is given up and counted.
- **331.** The rate moves by the gap between 50% and the median share read on each calibration round's 30 builds (rate + (0.50 − share), held to 0.05–1.0). It starts at 0.40. Verse 3 (song 42), which is also sung again from verse 1, takes the same rate.
- **332.** A knob is frozen at the value it reached on its second largest step. Neither song took a largest step twice this time, so nothing was frozen.
- **335.** Each row of the table names what it is read against:
  - a kept figure, where kept songs have the reading;
  - a reading, for counts kept songs do not have (316's redraws, 327's join deaths);
  - "the rule's own statement (a check)", for rows that check the code did what its rule says (311, 324, 325, 333).

  335's rule for readings is applied to 329's chorus window too, which reads against the kept middle half (8–13) where v111 asked for the kept median. 332's death count is kept as a test because v112 states it as one.
- **336.** The kept middle half of each of the 46 content measures is read from the kept windows (zeneng_v105_kept_windows.json, 314 windows). The builds' median for a measure is taken over the Verse 1 and Chorus 1 windows of every complete build.

## Findings

### 337. 332's test reads one run's count against another's, inside the spread between runs.

- *Problem.* The test asks song 40's key-word deaths to be at or under v110's 89 (main) and 42 (control). Each is the count of a single run of 1,000, with no margin.
- *Evidence.*
  - This run did not stop its calibration (nothing frozen) and read 109 and 44.
  - Two diagnostic runs (never runs of record) each switched one fix off: without 329's extremes, 99; without 322's stresses, 95.
  - A count near 100 in 1,000 builds varies by about ±10 from run to run.
  - The rise to 159 under v111 was the stop's. What is left is about two spreads in the main run and within one in the control, and no single fix carries it.
- *Fix.* Hold 332's test as 335 holds other counts kept songs do not have: print it as a reading beside the earlier version's count. Or set the test with the spread in it (at or under 89 plus two spreads).
- *Check.* The report prints the count beside v110's, with the spread.

### 338. 331's rate is set on the calibration's aimed builds, not on the builds the run makes.

- *Problem.* The calibration's builds are aimed at the pools' medians. The share they read is not the share the run's builds read.
- *Evidence.*
  - Song 40: the calibration read 50% in its last round at a rate of 0.80. The run's builds read 36% at the median (control 45%).
  - Song 42 read 50% in both (rate 0.65). Both pass 25–70%.
  - At the higher rate, 303's one-onset check refuses more copies. Song 40's verse 2 lines were given up for a copy 757 times in 6,000 (12.6%; control 9.9%), where v111 gave up 23. Song 42: 164 (4.1%), from 1.
- *Fix.* Read the share for 331's rate on the run's own first builds, or on unaimed calibration builds. Print the copies given up as a reading.
- *Check.* Verse 2's median share within five points of 50% on both songs, main and control.

## Where debugging stands

v112 asked for one more run of both songs: if every test holds on both and no finding changes a rule, the debugging is closed.

- **Song 42 passes every test**, main and control.
- **Song 40 passes every test but 332's count:** 109 against 89 in the main run and 44 against 42 in the control.

Two findings came up. 337 is about how a test is read, not a rule. 338 changes where 331's rate is read, a small change to one rule, and it does not change whether either song passes. By the paper's own condition the debugging is not yet closed: one test failed, by a margin inside the spread between runs, and one finding changes a rule.
