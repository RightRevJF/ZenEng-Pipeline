# ZenEng v115: songs 40, 42 and 43 again — test report

*Words and music of all three songs: Jason Bryant. Fixes 348–354 ported; findings numbered from 355. No new song.*

## What was run

v115's fixes 348–354 were ported onto the v114 search as melody_v115_p40.py, and songs 42 and 43 were built on it again from the same song constants, lyrics, intakes and seeds (gen_p42_v115.py, gen_p43_v115.py). Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Songs 40 and 42 are read beside v112, their last runs; song 43 beside v114.

One fix could not be ported as written. 348 (a sixteenth only as a push) left song 40's Bridge line 3 (seven syllables in one bar, ending by beat 3) with no placement: 0 of 100 builds survived. The writer chose Q1 A: 348's "unless there is no room" also covers drawn lines. No other fix conflicted.

| Song | Run | Survivors (before) | Order | Rerun order | Reproduced |
|---|---|---|---|---|---|
| 40 (seed 20261511) | main | 602 (544) | 2a9550248f1b | 2a9550248f1b | yes |
| 40 (seed 20261511) | control | 663 (544) | c5344a86edce | c5344a86edce | yes |
| 42 (seed 20261552) | main | 767 (747) | 03a4f13efa50 | 03a4f13efa50 | yes |
| 42 (seed 20261552) | control | 782 (738) | 1c46ba2167ca | 1c46ba2167ca | yes |
| 43 (seed 20261553) | main | 722 (811) | 97c7c92a9619 | 97c7c92a9619 | yes |
| 43 (seed 20261553) | control | 803 (819) | 4f2f64f2a00e | 4f2f64f2a00e | yes |

## The table of tests: Song 40, Nothing Else on Earth

Held in both the main run and the control: 25 of 33 with a test. Not held: 338, 344, 346, 347, 349, 350, 351, 354.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 10.0%; parallel 0.089 (kept 0.14); paired lines 4508, partner given up 0 | under floor 9.1%; parallel 0.084 (kept 0.14); paired lines 4615, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 0.0%, chorus 2.7%; leap knob 1.0 | verse 0.0%, chorus 2.7%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.083, 0.333, 0.583]; in range 76%; given up 110 (1.8%); left out 981 | share [0.091, 0.333, 0.583]; in range 81%; given up 116 (1.9%); left out 967 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [9.0, 15.0, 15.0, 15.0, 15.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.533, 0.6]; tonic nearest the sung median 0.795, the drawn centre 1.0; top fifth 92%; floor 6% | range [10.0, 15.0, 15.0, 15.0, 15.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.533, 0.583]; tonic nearest the sung median 0.868, the drawn centre 1.0; top fifth 91%; floor 5% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.054, 0.119, 0.306]; stop none | amplitude 5.0; arch [-0.122, 0.059, 0.279]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 1635/13083 = 0.125; entries {'starts_on_downbeat': 0.223, 'starts_after_downbeat': 0.61, 'starts_as_pickup': 0.167} (before {'starts_on_downbeat': 0.233, 'starts_after_downbeat': 0.637, 'starts_as_pickup': 0.13}) | redraws 1305/13223 = 0.099; entries {'starts_on_downbeat': 0.236, 'starts_after_downbeat': 0.592, 'starts_as_pickup': 0.172} (before {'starts_on_downbeat': 0.245, 'starts_after_downbeat': 0.619, 'starts_as_pickup': 0.137}) | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | none in force | none in force | yes |
| 318 | the feel named; sixteenths printed | a reading | straight eighths; sixteenth onsets [0.081, 0.159, 0.252] | straight eighths; sixteenth onsets [0.068, 0.095, 0.123] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 4508 (958 of another length); given up 749 (16.6%); parallel 0.089; under floor 10.0% | paired 4615 (965 of another length); given up 767 (16.6%); parallel 0.084; under floor 9.1% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 2275; left out 981; verse 2 in range 76% | one-over bars copied without the weakest onset 2082; left out 967; verse 2 in range 81% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 819 tonic endings, on the nearest to the centre 1.0 | 838 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | none in force | none in force | yes |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 45 (v109 92); refits {'327: return fitted again without a pickup, ordinary end': 54, '327: copy fitted again after its downbeat': 100, '327: copy could not enter later (return, entry pickup)': 45, '327: plan fitted again without a pickup': 46} | join deaths 46 (v109 92); refits {'327: plan fitted again without a pickup': 38, '327: copy fitted again after its downbeat': 105, '327: copy could not enter later (return, entry pickup)': 46, '327: return fitted again without a pickup, ordinary end': 67} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.081, 0.159, 0.252] | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.068, 0.095, 0.123] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [13.0, 14.0, 14.0] vs drawn [15.0, 15.0, 15.0] (gap [1.0, 1.0, 1.0]); chorus window [9.0, 11.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'step', 'gap_sixteenth', 'on_tonic']; extremes sung low 96%, high 94% | sung [13.0, 14.0, 14.0] vs drawn [15.0, 15.0, 15.0] (gap [1.0, 1.0, 1.0]); chorus window [9.0, 10.0, 11.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'gap_sixteenth', 'on_offbeat_eighth', 'pitch_sd']; extremes sung low 97%, high 94% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.089; copies failed and the stresses kept 103; given up after the stresses 749; partners given up 749 (16.6%) | likeness 0.084; copies failed and the stresses kept 86; given up after the stresses 767; partners given up 767 (16.6%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.983; verse 2 share [0.083, 0.333, 0.583] (5th, median, 95th) | rate 1.0; verse 2 share [0.091, 0.333, 0.583] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 11 (v110 89); frozen none | key-word deaths 1 (v110 42); frozen none | yes |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 17; widest drawn range 15 (row less two 15) | row 17; widest drawn range 15 (row less two 15) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.081, 0.159, 0.252] | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.068, 0.095, 0.123] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 10.0%; content median 0.71, at kept 25th 40.4%, at kept median 5.3%; order median 0.44, at kept 25th 68.9%, at kept median 3.8%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 9.1%; content median -0.01, at kept 25th 17.4%, at kept median 0.1%; order median 0.29, at kept 25th 64.6%, at kept median 2.1%; measures outside the kept middle half 0 of 46; heaviest give-away ('outside_scale', -0.572) | reading |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | rhythm: no placement 125/114 (spread 14.5, no difference); the judge's floor (254; 279) 60/69 (spread 11.0, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 94/33 (spread 10.8, a difference); bridge opening unrelated (208; 279) 46/63 (spread 10.1, no difference); join: no held end and breath before the copy (212) 45/46 (spread 9.3, no difference); chorus opening another tune (227; 279) 6/9 (spread 3.9, no difference) | rhythm: no placement 125/114 (spread 14.5, no difference); the judge's floor (254; 279) 60/69 (spread 11.0, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 94/33 (spread 10.8, a difference); bridge opening unrelated (208; 279) 46/63 (spread 10.1, no difference); join: no held end and breath before the copy (212) 45/46 (spread 9.3, no difference); chorus opening another tune (227; 279) 6/9 (spread 3.9, no difference) | printed |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.083, 0.333, 0.583]; rate 0.983; copies given up 110 | verse 2 share [0.091, 0.333, 0.583]; rate 1.0; copies given up 116 | **no** |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 10.01 (Window 134: 11.0, 10.4); costliest [('on_sixteenth', 2.56), ('longest_over_median_note', 0.87), ('distinct_pitches', 0.84), ('turns_per_move', 0.78), ('outside_scale', 0.77), ('unit4_to_unit2', 0.62), ('pitch_sd', 0.55), ('pushed', 0.45)] | gap 12.89 (Window 134: 11.0, 10.4); costliest [('gap_eighth', 2.1), ('on_offbeat_eighth', 1.77), ('pitch_sd', 1.16), ('outside_scale', 1.05), ('distinct_pitches', 1.01), ('on_beats_2_4', 0.89), ('longest_over_median_note', 0.83), ('unit4_to_unit2', 0.8)] | printed |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 10996: pushed 99%, in runs 0%; sixteenth gaps cost -0.27 | sixteenth onsets 5836: pushed 100%, in runs 0%; sixteenth gaps cost 0.38 | yes |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [4.625, 4.875, 5.125] (kept 3.6-4.1) | builds' notes a bar [4.625, 4.75, 5.125] (kept 3.6-4.1) | printed |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 4.0 at the median; cost 0.07; palette dropped for 2637 lines | distinct lengths 4.0 at the median; cost 0.32; palette dropped for 2657 lines | yes |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 2.9% (kept 7.1%); cost 0.77 | outside the scale 3.0% (kept 7.1%); cost 1.05 | **no** |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse -0.03, chorus -0.06; chord tones on long notes 64% | cost verse -0.0, chorus -0.0; chord tones on long notes 68% | yes |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.36, 'distinct_pitches': 0.84, 'unit2_returns': 0.23, 'unit3_returns': 0.27, 'unit4_to_unit2': 0.62} | costs {'on_offbeat_eighth': 1.77, 'distinct_pitches': 1.01, 'unit2_returns': 0.28, 'unit3_returns': 0.25, 'unit4_to_unit2': 0.8} | **no** |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('on_sixteenth', 2.56), ('longest_over_median_note', 0.87), ('distinct_pitches', 0.84), ('turns_per_move', 0.78), ('outside_scale', 0.77), ('unit4_to_unit2', 0.62), ('pitch_sd', 0.55)]; gap 10.01 | over half a point: [('gap_eighth', 2.1), ('on_offbeat_eighth', 1.77), ('pitch_sd', 1.16), ('outside_scale', 1.05), ('distinct_pitches', 1.01), ('on_beats_2_4', 0.89), ('longest_over_median_note', 0.83), ('unit4_to_unit2', 0.8), ('turns_per_move', 0.55)]; gap 12.89 | **no** |
| 348 | of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | pushed 99%, in runs 0%; sixteenth gaps cost -0.27; lines with no room (runs allowed) 1552 | pushed 100%, in runs 0%; sixteenth gaps cost 0.38; lines with no room (runs allowed) 1569 | yes |
| 349 | the outside-scale share within two points of the kept mean; cost under half a point | kept 7.1% (4.5% minor) | outside the scale 2.9% (kept 7.1%); cost 0.77; placed 3770, places wanting 70628 | outside the scale 3.0% (kept 7.1%); cost 1.05; placed 4050, places wanting 80506 | **no** |
| 350 | no unit return costs over half a point | kept unit 3 returns 31.5% | costs {'unit2_returns': 0.23, 'unit3_returns': 0.27, 'unit4_to_unit2': 0.62}; means {'unit2_returns': 0.044, 'unit3_returns': 0.075, 'unit4_to_unit2': 0.009} | costs {'unit2_returns': 0.28, 'unit3_returns': 0.25, 'unit4_to_unit2': 0.8}; means {'unit2_returns': 0.05, 'unit3_returns': 0.077, 'unit4_to_unit2': 0.003} | **no** |
| 351 | verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median | kept 50% (25-70%) | bars left out 10319; lines given up 110 (1.8%); verse 2 share [0.083, 0.333, 0.583] | bars left out 10149; lines given up 116 (1.9%); verse 2 share [0.091, 0.333, 0.583] | **no** |
| 352 | the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats | a check; kept repeats' middle half printed | pick {'fp': '581e5307d65f', 'judge': 3.91, 'rank_by_composite': 57, 'rank_by_judge': 1, 'repeats': [0.07, 0.167]}; composite first {'fp': 'af0c70cca6a3', 'judge': -0.73, 'rank_by_composite': 1, 'rank_by_judge': 602, 'repeats': [0.439, 0.342]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | pick {'fp': '0bbabfa98a48', 'judge': 2.12, 'rank_by_composite': 639, 'rank_by_judge': 1, 'repeats': [0.125, 0.361]}; composite first {'fp': '2cdbc9e8531f', 'judge': 0.06, 'rank_by_composite': 1, 'rank_by_judge': 387, 'repeats': [0.293, 0.306]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | yes |
| 353 | a minor song's degree measures read on its tonic with the natural minor scale | the rule's own statement (a check) | a major song: n/a | a major song: n/a | n/a |
| 354 | each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point | Table DU | 4.88 notes a bar, band [4.5, 5.5]: kept [0.14, 0.55, 0.16, 0.11], builds [0.129, 0.493, 0.133, 0.097]; eighth gaps cost 0.15 | 4.75 notes a bar, band [4.5, 5.5]: kept [0.14, 0.55, 0.16, 0.11], builds [0.07, 0.589, 0.172, 0.098]; eighth gaps cost 2.1 | **no** |

## The table of tests: Song 42, Nothing Important

Held in both the main run and the control: 22 of 32 with a test. Not held: 341, 343, 344, 346, 347, 348, 349, 350, 351, 354.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 3.0%; parallel 0.135 (kept 0.14); paired lines 3570, partner given up 0 | under floor 1.4%; parallel 0.113 (kept 0.14); paired lines 3547, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 46; misses 0 | tonic 100.0%; registers redrawn 46; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 2.6%, chorus 3.0%; leap knob 1.0 | verse 2.6%, chorus 3.0%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.125, 0.444, 0.75]; in range 88%; given up 6 (0.2%); left out 8 | share [0.125, 0.375, 0.75]; in range 89%; given up 7 (0.2%); left out 1 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [11.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.36, 0.438, 0.579]; tonic nearest the sung median 0.868, the drawn centre 1.0; top fifth 87%; floor 2% | range [11.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.368, 0.438, 0.579]; tonic nearest the sung median 0.962, the drawn centre 1.0; top fifth 88%; floor 1% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.168, 0.071, 0.347]; stop none | amplitude 5.0; arch [-0.165, 0.079, 0.35]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 483/8990 = 0.054; entries {'starts_on_downbeat': 0.149, 'starts_after_downbeat': 0.532, 'starts_as_pickup': 0.319} (before {'starts_on_downbeat': 0.226, 'starts_after_downbeat': 0.667, 'starts_as_pickup': 0.108}) | redraws 404/8959 = 0.045; entries {'starts_on_downbeat': 0.152, 'starts_after_downbeat': 0.522, 'starts_as_pickup': 0.326} (before {'starts_on_downbeat': 0.221, 'starts_after_downbeat': 0.667, 'starts_as_pickup': 0.111}) | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.991} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.989} | yes |
| 318 | the feel named; sixteenths printed | a reading | straight eighths, q = 76; sixteenth onsets [0.051, 0.112, 0.206] | straight eighths, q = 76; sixteenth onsets [0.043, 0.064, 0.092] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 3570 (2586 of another length); given up 2 (0.1%); parallel 0.135; under floor 3.0% | paired 3547 (2584 of another length); given up 1 (0.0%); parallel 0.113; under floor 1.4% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 274; left out 8; verse 2 in range 88% | one-over bars copied without the weakest onset 53; left out 1; verse 2 in range 89% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 903 tonic endings, on the nearest to the centre 1.0 | 898 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 46} | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn {"325: register redrawn for a design: the last line's tonic under the hook's end (Q11 note 4)": 46} | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.991} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.989} | yes |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 1 (v109 92); refits {'327: copy could not enter later (plan, entry pickup)': 1} | join deaths 1 (v109 92); refits {'327: copy could not enter later (plan, entry pickup)': 1, '327: plan fitted again without a pickup': 1, '327: copy fitted again after its downbeat': 1} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.051, 0.112, 0.206] | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.043, 0.064, 0.092] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [0.0, 1.0, 2.0]); chorus window [8.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'gap_sixteenth', 'empty_bars', 'step', 'on_offbeat_eighth']; extremes sung low 96%, high 96% | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [0.0, 1.0, 2.0]); chorus window [8.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'gap_sixteenth', 'empty_bars', 'gap_quarter', 'on_beats_2_4']; extremes sung low 98%, high 96% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.135; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 2 (0.1%) | likeness 0.113; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 1 (0.0%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.921; verse 2 share [0.125, 0.444, 0.75] (5th, median, 95th) | rate 0.858; verse 2 share [0.125, 0.375, 0.75] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 5 (v110 89); frozen none | key-word deaths 2 (v110 42); frozen none | reading |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.051, 0.112, 0.206] | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.043, 0.064, 0.092] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 3.0%; content median 1.13, at kept 25th 44.9%, at kept median 7.4%; order median 1.64, at kept 25th 98.4%, at kept median 54.5%; measures outside the kept middle half 0 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 1.4%; content median 0.43, at kept 25th 27.3%, at kept median 0.7%; order median 1.46, at kept 25th 98.4%, at kept median 44.1%; measures outside the kept middle half 0 of 46; heaviest give-away ('outside_scale', -0.572) | reading |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | join: no held end and breath before the line (212) 96/101 (spread 13.3, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 75/48 (spread 10.7, a difference); bridge opening unrelated (208; 279) 21/39 (spread 7.6, a difference); the judge's floor (254; 279) 24/9 (spread 5.7, a difference); design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4) 8/10 (spread 4.2, no difference); chorus opening another tune (227; 279) 3/8 (spread 3.3, no difference) | join: no held end and breath before the line (212) 96/101 (spread 13.3, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 75/48 (spread 10.7, a difference); bridge opening unrelated (208; 279) 21/39 (spread 7.6, a difference); the judge's floor (254; 279) 24/9 (spread 5.7, a difference); design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4) 8/10 (spread 4.2, no difference); chorus opening another tune (227; 279) 3/8 (spread 3.3, no difference) | printed |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.125, 0.444, 0.75]; rate 0.921; copies given up 6 | verse 2 share [0.125, 0.375, 0.75]; rate 0.858; copies given up 7 | yes |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 8.37 (Window 134: 11.0, 10.4); costliest [('on_sixteenth', 1.4), ('pushed', 1.27), ('outside_scale', 0.74), ('on_offbeat_eighth', 0.67), ('unit4_to_unit2', 0.57), ('gap_eighth', 0.55), ('distinct_pitches', 0.52), ('chord_tones', 0.46)] | gap 10.58 (Window 134: 11.0, 10.4); costliest [('gap_eighth', 1.84), ('on_beats_2_4', 1.59), ('on_offbeat_eighth', 1.38), ('distinct_pitches', 0.85), ('unit4_to_unit2', 0.76), ('gap_sixteenth', 0.68), ('outside_scale', 0.61), ('distinct_durations', 0.57)] | printed |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 9076: pushed 99%, in runs 1%; sixteenth gaps cost 0.09 | sixteenth onsets 5039: pushed 100%, in runs 0%; sixteenth gaps cost 0.68 | **no** |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [4.0, 4.5, 4.875] (kept 3.6-4.1) | builds' notes a bar [4.0, 4.5, 4.75] (kept 3.6-4.1) | printed |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 4.0 at the median; cost 0.11; palette dropped for 101 lines | distinct lengths 4.0 at the median; cost 0.57; palette dropped for 89 lines | **no** |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 2.8% (kept 7.1%); cost 0.74 | outside the scale 2.9% (kept 7.1%); cost 0.61 | **no** |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse -0.03, chorus -0.06; chord tones on long notes 66% | cost verse 0.02, chorus 0.05; chord tones on long notes 67% | yes |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.67, 'distinct_pitches': 0.52, 'unit2_returns': 0.14, 'unit3_returns': 0.1, 'unit4_to_unit2': 0.57} | costs {'on_offbeat_eighth': 1.38, 'distinct_pitches': 0.85, 'unit2_returns': 0.18, 'unit3_returns': 0.15, 'unit4_to_unit2': 0.76} | **no** |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('on_sixteenth', 1.4), ('pushed', 1.27), ('outside_scale', 0.74), ('on_offbeat_eighth', 0.67), ('unit4_to_unit2', 0.57), ('gap_eighth', 0.55), ('distinct_pitches', 0.52)]; gap 8.37 | over half a point: [('gap_eighth', 1.84), ('on_beats_2_4', 1.59), ('on_offbeat_eighth', 1.38), ('distinct_pitches', 0.85), ('unit4_to_unit2', 0.76), ('gap_sixteenth', 0.68), ('outside_scale', 0.61), ('distinct_durations', 0.57)]; gap 10.58 | **no** |
| 348 | of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | pushed 99%, in runs 1%; sixteenth gaps cost 0.09; lines with no room (runs allowed) 0 | pushed 100%, in runs 0%; sixteenth gaps cost 0.68; lines with no room (runs allowed) 0 | **no** |
| 349 | the outside-scale share within two points of the kept mean; cost under half a point | kept 7.1% (4.5% minor) | outside the scale 2.8% (kept 7.1%); cost 0.74; placed 1834, places wanting 30491 | outside the scale 2.9% (kept 7.1%); cost 0.61; placed 1850, places wanting 27182 | **no** |
| 350 | no unit return costs over half a point | kept unit 3 returns 31.5% | costs {'unit2_returns': 0.14, 'unit3_returns': 0.1, 'unit4_to_unit2': 0.57}; means {'unit2_returns': 0.077, 'unit3_returns': 0.393, 'unit4_to_unit2': 0.014} | costs {'unit2_returns': 0.18, 'unit3_returns': 0.15, 'unit4_to_unit2': 0.76}; means {'unit2_returns': 0.07, 'unit3_returns': 0.397, 'unit4_to_unit2': 0.008} | **no** |
| 351 | verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median | kept 50% (25-70%) | bars left out 8419; lines given up 6 (0.2%); verse 2 share [0.125, 0.444, 0.75] | bars left out 7714; lines given up 7 (0.2%); verse 2 share [0.125, 0.375, 0.75] | **no** |
| 352 | the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats | a check; kept repeats' middle half printed | pick {'fp': 'bf95214a5b51', 'judge': 6.4, 'rank_by_composite': 653, 'rank_by_judge': 1, 'repeats': [0.548, 0.062]}; composite first {'fp': '59512676d559', 'judge': 1.7, 'rank_by_composite': 1, 'rank_by_judge': 294, 'repeats': [0.513, 0.091]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | pick {'fp': 'b0007408a361', 'judge': 3.76, 'rank_by_composite': 685, 'rank_by_judge': 1, 'repeats': [0.256, 0.161]}; composite first {'fp': 'c3f07ca8e7cd', 'judge': 0.97, 'rank_by_composite': 1, 'rank_by_judge': 403, 'repeats': [0.205, 0.258]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | yes |
| 353 | a minor song's degree measures read on its tonic with the natural minor scale | the rule's own statement (a check) | a major song: n/a | a major song: n/a | n/a |
| 354 | each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point | Table DU | 4.5 notes a bar, band [4.5, 5.5]: kept [0.14, 0.55, 0.16, 0.11], builds [0.097, 0.523, 0.152, 0.113]; eighth gaps cost 0.55 | 4.5 notes a bar, band [4.5, 5.5]: kept [0.14, 0.55, 0.16, 0.11], builds [0.054, 0.588, 0.175, 0.124]; eighth gaps cost 1.84 | **no** |

## The table of tests: Song 43, Blue Movie

Held in both the main run and the control: 21 of 33 with a test. Not held: 317, 326, 338, 341, 343, 344, 346, 347, 348, 349, 351, 354.

| Fix | Test | Read against | Main | Control | Held? |
|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 1.5%; parallel 0.138 (kept 0.14); paired lines 3381, partner given up 0 | under floor 0.9%; parallel 0.14 (kept 0.14); paired lines 3427, partner given up 0 | yes |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 2.6%, chorus 3.3%; leap knob 1.0 | verse 0.0%, chorus 3.5%; leap knob 1.0 | yes |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.0, 0.25, 0.5]; in range 61%; given up 41 (1.0%); left out 3 | share [0.0, 0.25, 0.571]; in range 65%; given up 51 (1.3%); left out 3 | yes |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [10.0, 15.0, 17.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.364, 0.438, 0.6]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 85%; floor 2% | range [9.0, 14.0, 17.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.375, 0.429, 0.6]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 82%; floor 2% | yes |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.016, 0.166, 0.393]; stop none | amplitude 5.0; arch [-0.034, 0.131, 0.358]; stop none | yes |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 6/4526 = 0.001; entries {'starts_on_downbeat': 0.273, 'starts_after_downbeat': 0.64, 'starts_as_pickup': 0.087} (before {'starts_on_downbeat': 0.273, 'starts_after_downbeat': 0.652, 'starts_as_pickup': 0.074}) | redraws 0/4578 = 0.0; entries {'starts_on_downbeat': 0.274, 'starts_after_downbeat': 0.638, 'starts_as_pickup': 0.088} (before {'starts_on_downbeat': 0.272, 'starts_after_downbeat': 0.652, 'starts_as_pickup': 0.076}) | reading |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.913} | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.897} | **no** |
| 318 | the feel named; sixteenths printed | a reading | up-tempo dance-pop, q = 118, four on the floor, straight; sixteenth onsets [0.064, 0.118, 0.183] | up-tempo dance-pop, q = 118, four on the floor, straight; sixteenth onsets [0.048, 0.07, 0.097] | printed |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 3381 (1323 of another length); given up 0 (0.0%); parallel 0.138; under floor 1.5% | paired 3427 (1320 of another length); given up 0 (0.0%); parallel 0.14; under floor 0.9% | yes |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 66; left out 3; verse 2 in range 61% | one-over bars copied without the weakest onset 44; left out 3; verse 2 in range 65% | yes |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 983 tonic endings, on the nearest to the centre 1.0 | 996 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.913} | {"design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)": 0.897} | **no** |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 0 (v109 92); refits {'327: sung-again line fitted after its downbeat': 41, '327: copy fitted again after its downbeat': 43, '327: plan fitted again without a pickup, ordinary end': 2} | join deaths 0 (v109 92); refits {'327: sung-again line fitted after its downbeat': 55, '327: copy fitted again after its downbeat': 56, '327: plan fitted again without a pickup, ordinary end': 1} | reading |
| 328 | the sixteenth share beside its band | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.064, 0.118, 0.183] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.048, 0.07, 0.097] | printed |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 17.0, 19.0] (gap [0.0, 1.0, 2.0]); chorus window [8.0, 10.0, 13.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'gap_sixteenth', 'on_tonic', 'first_note_tonic_triad']; extremes sung low 100%, high 100% | sung [13.0, 17.0, 17.0] vs drawn [14.0, 17.0, 19.0] (gap [0.0, 1.0, 2.0]); chorus window [9.0, 10.0, 13.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'gap_sixteenth', 'gap_quarter', 'first_note_tonic_triad']; extremes sung low 100%, high 100% | yes |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.138; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | likeness 0.14; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | yes |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 1.0; verse 2 share [0.0, 0.25, 0.5] (5th, median, 95th) | rate 1.0; verse 2 share [0.0, 0.25, 0.571] (5th, median, 95th) | yes |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 16 (v110 89); frozen none | key-word deaths 3 (v110 42); frozen none | reading |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.064, 0.118, 0.183] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.048, 0.07, 0.097] | printed |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 1.5%; content median 0.88, at kept 25th 39.6%, at kept median 5.4%; order median 1.72, at kept 25th 98.6%, at kept median 56.5%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 0.9%; content median 0.33, at kept 25th 24.1%, at kept median 0.4%; order median 1.65, at kept 25th 98.0%, at kept median 53.1%; measures outside the kept middle half 0 of 46; heaviest give-away ('outside_scale', -0.572) | reading |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A) 86/103 (spread 13.1, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 129/46 (spread 12.5, a difference); bridge opening unrelated (208; 279) 13/25 (spread 6.1, no difference); key word on a chord tone (134; 279) 16/3 (spread 4.3, a difference); the judge's floor (254; 279) 13/6 (spread 4.3, no difference); join: no held end and breath before the line (212) 13/4 (spread 4.1, a difference) | design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A) 86/103 (spread 13.1, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 129/46 (spread 12.5, a difference); bridge opening unrelated (208; 279) 13/25 (spread 6.1, no difference); key word on a chord tone (134; 279) 16/3 (spread 4.3, a difference); the judge's floor (254; 279) 13/6 (spread 4.3, no difference); join: no held end and breath before the line (212) 13/4 (spread 4.1, a difference) | printed |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.0, 0.25, 0.5]; rate 1.0; copies given up 41 | verse 2 share [0.0, 0.25, 0.571]; rate 1.0; copies given up 51 | **no** |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 8.56 (Window 134: 11.0, 10.4); costliest [('outside_scale', 2.62), ('on_sixteenth', 1.49), ('on_beat3', 0.61), ('chord_tones_on_downbeat', 0.54), ('last_note_tonic', 0.53), ('distinct_durations', 0.5), ('pushed', 0.49), ('empty_bars', 0.48)] | gap 9.62 (Window 134: 11.0, 10.4); costliest [('outside_scale', 2.86), ('distinct_durations', 0.98), ('on_beat3', 0.84), ('gap_eighth', 0.71), ('gap_sixteenth', 0.69), ('on_offbeat_eighth', 0.66), ('distinct_pitches', 0.66), ('last_note_tonic', 0.62)] | printed |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 9672: pushed 100%, in runs 0%; sixteenth gaps cost -0.03 | sixteenth onsets 5723: pushed 100%, in runs 0%; sixteenth gaps cost 0.69 | **no** |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [3.75, 4.375, 4.75] (kept 3.6-4.1) | builds' notes a bar [3.75, 4.188, 4.625] (kept 3.6-4.1) | printed |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 5.0 at the median; cost 0.5; palette dropped for 40 lines | distinct lengths 5.0 at the median; cost 0.98; palette dropped for 49 lines | **no** |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 0.9% (kept 7.1%); cost 2.62 | outside the scale 0.9% (kept 7.1%); cost 2.86 | **no** |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse 0.01, chorus 0.08; chord tones on long notes 61% | cost verse -0.01, chorus 0.2; chord tones on long notes 65% | yes |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.21, 'distinct_pitches': 0.42, 'unit2_returns': 0.02, 'unit3_returns': 0.09, 'unit4_to_unit2': -0.01} | costs {'on_offbeat_eighth': 0.66, 'distinct_pitches': 0.66, 'unit2_returns': 0.04, 'unit3_returns': 0.04, 'unit4_to_unit2': -0.01} | **no** |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('outside_scale', 2.62), ('on_sixteenth', 1.49), ('on_beat3', 0.61), ('chord_tones_on_downbeat', 0.54), ('last_note_tonic', 0.53), ('distinct_durations', 0.5)]; gap 8.56 | over half a point: [('outside_scale', 2.86), ('distinct_durations', 0.98), ('on_beat3', 0.84), ('gap_eighth', 0.71), ('gap_sixteenth', 0.69), ('on_offbeat_eighth', 0.66), ('distinct_pitches', 0.66), ('last_note_tonic', 0.62), ('on_beats_2_4', 0.56)]; gap 9.62 | **no** |
| 348 | of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | pushed 100%, in runs 0%; sixteenth gaps cost -0.03; lines with no room (runs allowed) 0 | pushed 100%, in runs 0%; sixteenth gaps cost 0.69; lines with no room (runs allowed) 0 | **no** |
| 349 | the outside-scale share within two points of the kept mean; cost under half a point | kept 7.1% (4.5% minor) | outside the scale 0.9% (kept 4.5%); cost 2.62; placed 1060, places wanting 33193 | outside the scale 0.9% (kept 4.5%); cost 2.86; placed 1042, places wanting 36517 | **no** |
| 350 | no unit return costs over half a point | kept unit 3 returns 31.5% | costs {'unit2_returns': 0.02, 'unit3_returns': 0.09, 'unit4_to_unit2': -0.01}; means {'unit2_returns': 0.112, 'unit3_returns': 0.151, 'unit4_to_unit2': 0.131} | costs {'unit2_returns': 0.04, 'unit3_returns': 0.04, 'unit4_to_unit2': -0.01}; means {'unit2_returns': 0.108, 'unit3_returns': 0.165, 'unit4_to_unit2': 0.139} | yes |
| 351 | verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median | kept 50% (25-70%) | bars left out 10662; lines given up 41 (1.0%); verse 2 share [0.0, 0.25, 0.5] | bars left out 10379; lines given up 51 (1.3%); verse 2 share [0.0, 0.25, 0.571] | **no** |
| 352 | the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats | a check; kept repeats' middle half printed | pick {'fp': '3f2c11d69f6d', 'judge': 4.93, 'rank_by_composite': 118, 'rank_by_judge': 1, 'repeats': [0.216, 0.1]}; composite first {'fp': 'a049edab7e02', 'judge': 0.78, 'rank_by_composite': 1, 'rank_by_judge': 503, 'repeats': [0.714, 0.484]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | pick {'fp': '3acaf32ede6e', 'judge': 3.91, 'rank_by_composite': 707, 'rank_by_judge': 1, 'repeats': [0.41, 0.333]}; composite first {'fp': '6f2c75550c23', 'judge': 0.61, 'rank_by_composite': 1, 'rank_by_judge': 528, 'repeats': [0.143, 0.241]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | yes |
| 353 | a minor song's degree measures read on its tonic with the natural minor scale | the rule's own statement (a check) | a minor song: the window measures on its tonic with the natural minor scale | a minor song: the window measures on its tonic with the natural minor scale | yes |
| 354 | each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point | Table DU | 4.38 notes a bar, band [3.5, 4.5]: kept [0.11, 0.5, 0.17, 0.18], builds [0.11, 0.468, 0.147, 0.148]; eighth gaps cost 0.01 | 4.19 notes a bar, band [3.5, 4.5]: kept [0.11, 0.5, 0.17, 0.18], builds [0.068, 0.539, 0.172, 0.148]; eighth gaps cost 0.71 | **no** |

## Table DQ: before and after (main runs)

| Reading | 40, v112 | 40, v115 | 42, v112 | 42, v115 | 43, v114 | 43, v115 |
|---|---|---|---|---|---|---|
| survivors of 1,000 | 544 | 602 | 747 | 767 | 811 | 722 |
| builds under the judge's floor | 27.6% | 10.0% | 5.2% | 3.0% | 1.6% | 1.5% |
| content judge, median | -0.99 | 0.71 | -0.34 | 1.13 | 0.7 | 0.88 |
| order judge, median | 0.57 | 0.44 | 2.05 | 1.64 | 1.82 | 1.72 |
| likeness of bar rhythms between lines | 0.099 | 0.089 | 0.19 | 0.135 | 0.164 | 0.138 |
| contour amplitude | 5.0 | 5.0 | 7.0 | 5.0 | 5.0 | 5.0 |
| arch term over the line's span | 0.07 | 0.12 | 0.09 | 0.07 | 0.16 | 0.17 |
| leaps past a fifth, verse, % of moves | 2.4 | 0.0 | 2.6 | 2.6 | 2.7 | 2.6 |
| the song's sung range, semitones | 14.0 | 14.0 | 17.0 | 17.0 | 17.0 | 17.0 |
| range in eight bars, verse / chorus | 10 / 11 | 10 / 11 | 12 / 10 | 11 / 10 | 10 / 10 | 10 / 10 |
| builds that touch the row's floor | 6.5% | 6.2% | 0.3% | 1.9% | 1.4% | 1.8% |
| builds that use the row's top fifth | 92.5% | 92.4% | 89.0% | 87.3% | 85.8% | 84.7% |

## 340: the eight costliest measures (points; kept mean, builds' mean)

- **Song 40, Nothing Else on Earth, main** (gap 10.01): on_sixteenth 2.56 (0.094, 0.169); longest_over_median_note 0.87 (3.535, 2.605); distinct_pitches 0.84 (6.382, 6.943); turns_per_move 0.78 (0.584, 0.688); outside_scale 0.77 (0.071, 0.029); unit4_to_unit2 0.62 (0.188, 0.009); pitch_sd 0.55 (2.910, 2.603); pushed 0.45 (0.123, 0.159)
- **Song 40, Nothing Else on Earth, control** (gap 12.89): gap_eighth 2.1 (0.465, 0.589); on_offbeat_eighth 1.77 (0.371, 0.426); pitch_sd 1.16 (2.910, 2.516); outside_scale 1.05 (0.071, 0.030); distinct_pitches 1.01 (6.382, 6.990); on_beats_2_4 0.89 (0.210, 0.234); longest_over_median_note 0.83 (3.535, 2.772); unit4_to_unit2 0.8 (0.188, 0.003)
- **Song 42, Nothing Important, main** (gap 8.37): on_sixteenth 1.4 (0.094, 0.139); pushed 1.27 (0.123, 0.184); outside_scale 0.74 (0.071, 0.028); on_offbeat_eighth 0.67 (0.371, 0.410); unit4_to_unit2 0.57 (0.188, 0.014); gap_eighth 0.55 (0.465, 0.523); distinct_pitches 0.52 (6.382, 6.878); chord_tones 0.46 (0.639, 0.570)
- **Song 42, Nothing Important, control** (gap 10.58): gap_eighth 1.84 (0.465, 0.588); on_beats_2_4 1.59 (0.210, 0.247); on_offbeat_eighth 1.38 (0.371, 0.425); distinct_pitches 0.85 (6.382, 7.027); unit4_to_unit2 0.76 (0.188, 0.008); gap_sixteenth 0.68 (0.107, 0.054); outside_scale 0.61 (0.071, 0.029); distinct_durations 0.57 (4.035, 4.411)
- **Song 43, Blue Movie, main** (gap 8.56): outside_scale 2.62 (0.071, 0.009); on_sixteenth 1.49 (0.094, 0.142); on_beat3 0.61 (0.124, 0.142); chord_tones_on_downbeat 0.54 (0.722, 0.541); last_note_tonic 0.53 (0.277, 0.063); distinct_durations 0.5 (4.035, 4.704); pushed 0.49 (0.123, 0.172); empty_bars 0.48 (0.468, 0.151)
- **Song 43, Blue Movie, control** (gap 9.62): outside_scale 2.86 (0.071, 0.009); distinct_durations 0.98 (4.035, 4.710); on_beat3 0.84 (0.124, 0.148); gap_eighth 0.71 (0.465, 0.539); gap_sixteenth 0.69 (0.107, 0.068); on_offbeat_eighth 0.66 (0.371, 0.399); distinct_pitches 0.66 (6.382, 6.965); last_note_tonic 0.62 (0.277, 0.052)

## The pick (352)

| Song | Run | Pick (judge's first) | Its rank on the composite | Composite's first | Its rank on the judge | Pick's repeats, verse / chorus |
|---|---|---|---|---|---|---|
| 40 | main | 581e5307d65f | 57 | af0c70cca6a3 | 602 | 0.07 / 0.167 |
| 40 | control | 0bbabfa98a48 | 639 | 2cdbc9e8531f | 387 | 0.125 / 0.361 |
| 42 | main | bf95214a5b51 | 653 | 59512676d559 | 294 | 0.548 / 0.062 |
| 42 | control | b0007408a361 | 685 | c3f07ca8e7cd | 403 | 0.256 / 0.161 |
| 43 | main | 3f2c11d69f6d | 118 | a049edab7e02 | 503 | 0.216 / 0.1 |
| 43 | control | 3acaf32ede6e | 707 | 6f2c75550c23 | 528 | 0.41 / 0.333 |

Kept repeats' middle half: verse 0.14–0.39, chorus 0.13–0.40. 255's pick is printed in each run file. Song 43's recorded take (v114, Q18 A) is unchanged; nothing was re-recorded.

## Readings the paper does not give

- **348 (Q1 A).** A drawn line with fewer eighth-grid positions than syllables may place short notes on sixteenth positions (counted: 1,552 lines on song 40, none on 42 or 43). Returning lines are aligned on the eighth grid first, then on the sixteenth.
- **349.** After the end rule, each note but the last may move a semitone to one of the song's sung extra pitch classes if fix 200's rule allows it: no clash with the chord, no tritone to its root, no tritone or interval over 9 to either neighbour. Places tried and wanting are counted.
- **351.** A bar of a copy that fails 303's check is drawn fresh; the rest of the line keeps the copy.
- **353.** For song 43, the window measures (degree shares, the outside-scale share, the tonic ending) read on A with the natural minor scale. 286's Table B readings and the PPM still read on the engine's frame (C).
- **354.** The four gap knobs (s16, g8, g4, glong) move by at most a factor of 1.6 a round toward Table DU's band for the unaimed builds' notes a bar. Song 40 and 42 sit in the 4.5–5.5 band; song 43 in 3.5–4.5.
- **The spread (337).** Song 43's survivors fell 811 → 722; the spread between the two counts is about 19.

## Findings

### 355. Fix 348 leaves no sixteenth runs, and its test cannot see it.

**Problem:** With a sixteenth-position onset allowed only as a push, the runs are gone. 348's test sets only a floor on pushes and a ceiling on runs, so it holds while the shape is still far from the kept one.

**Evidence:** Of onsets on a sixteenth position, 99–100% were pushed and 0–1% were in runs on all six song-runs, against the kept 54% and 31%. In the main runs, the share of onsets on a sixteenth position rose past the kept 9.4%: 16.9% on song 40, 13.9% on song 42 and 14.2% on song 43. It is now the costliest measure on songs 40 and 42 (2.56 and 1.40 points) and the second costliest on song 43 (1.49). "Rhythm: no placement" killed 125 of song 40's builds in the main run and 114 in the control. Q1 A let 1,552 drawn lines with no room run sixteenths, but these are bridge lines, which the window measures do not read.

**Fix:** In a drawn line, draw runs at the kept rate: about one in three sixteenth-position onsets inside a run of two or more. The other sixteenth-position onsets stay pushes. Make 348's test two-sided.

**Check:** Pushed within 10 points of 54% and runs within 10 points of 31%. The share of onsets on a sixteenth position within two points of 9.4%, costing under half a point. Rhythm-placement deaths under 5%.

### 356. The v115 rhythms break 286's rhythm limits and cost song 43 a tenth of its survivors.

**Problem:** v115's rhythms carry more information than the kept band allows, and builds now die or pick up soft breaks on 286's rhythm band.

**Evidence:** Soft breaks on the rhythm band rose from 2 to 139 on song 40, from 6 to 116 on song 42 and from 0 to 150 on song 43, in the main runs. On song 43, the rhythm band's bits rose at the median from 2.26 to 2.49, and 6.2% of survivors now sit above the soft top of 2.93 (before, none). In the same runs:

- memory breaks rose from 65 to 323;
- breaks on the most lengths in eight bars rose from 6 to 46;
- distinct note lengths rose from 4.07 to 4.78, against the kept 4.04;
- 343's test failed for the first time (median distinct lengths 5, cost 0.50 in the main run and 0.98 in the control).

Song 43's survivors fell from 811 to 722, about 4.7 times 337's spread of 19. Three of the six picks carry the rhythm-band soft break (songs 40, 42 and 43, main runs). The cause is not yet separated: either 348's pushes (a push adds a length of a sixteenth and its partner) or 354's knobs (g4 at 2.6–2.9 and glong at 0.9–1.9 in the main runs).

**Fix:** Read the rhythm band's bits and the distinct lengths in 338's calibration. Stop a 354 knob from moving further when either leaves the kept middle half. Then run song 43 once with 348 off and once with 354 off, so the share each one causes is known.

**Check:** Rhythm-band soft breaks back within 337's spread of v114's counts. 343 held. Song 43's survivors within the spread of 811.

### 357. Fix 354's knobs reach the gap targets in no run.

**Problem:** The calibration moves each gap knob at most by a factor of 1.6 a round. In the control the knobs move at full step every round and still miss. In the main run the knob that meets the sixteenth-gap target overshoots the sixteenth onsets (355).

**Evidence:** 354 held on none of the six song-runs:

- **Song 40:** in the main run, eighth gaps were 49.3% against the band's 55% (5.7 points off).
- **Song 42:** the gap shares were all within five points, but eighth gaps cost 0.55 in the main run.
- **Song 43:** the main run held; in the control, eighth gaps cost 0.71.

In the controls of songs 42 and 43, s16 ended at 4.096, which is 1.6 cubed: full step on each of three rounds. g8 ended near 0.55. Even so, sixteenth gaps were 5.4% and 6.8% against Table DU's 14% and 11%, and eighth gaps were 58.8% and 53.9% against 55% and 50%, costing 1.84 on song 42 and 0.71 on song 43. Song 40's control did the same (s16 3.67, eighth-gap cost 2.1). Without runs (355), each sixteenth gap needs a sixteenth-position onset of its own, so the sixteenth gaps and the sixteenth onsets cannot both reach their kept figures.

**Fix:** After 355, let the calibration keep going while a knob is still moving at full step, up to six rounds, and print the rounds. Aim the sixteenth-gap knob and the sixteenth-onset share together: stop s16 when the onset share passes its kept figure.

**Check:** Each gap share within five points of Table DU's target for the song's notes a bar, and eighth gaps under half a point, in both the main run and the control.

### 358. Fix 349's placement is held back by fix 200's rule.

**Problem:** An outside note is placed only where fix 200's harmonic rule allows it: no clash with the chord, no tritone to the root, and no tritone or interval over 9 to either neighbour. Almost every place fails those tests, so the share stays well under the kept figure whatever its weight.

**Evidence:**

- **Song 40:** 3,770 notes were placed and 70,628 places were wanting. The outside-scale share was 2.9% (control 3.0%) against the kept 7.1%, costing 0.77 (1.05).
- **Song 42:** 2.8% (2.9%), costing 0.74 (0.61).
- **Song 43:** 0.9% against the kept 4.5% for a minor song. It is the costliest measure there (2.62, control 2.86). 344's knob rose at full step to 8.0 without effect.

**Fix:** Also allow an outside note that moves by step to both neighbours (a chromatic passing or neighbour note), on a weak eighth or a sixteenth, whatever the chord. Keep fix 200's rule for notes on the beat.

**Check:** The outside-scale share within two points of 7.1% (4.5% for a minor song), costing under half a point. No rise in tritone-from-root breaks beyond 337's spread.

### 359. Fix 353 reads the minor song's builds on its tonic, but the kept side is unchanged.

**Problem:** The window measures of a minor song are now read on its own tonic with the natural minor scale. The judge's kept means are still one set for every song, and so are 349's targets apart from the 4.5%.

**Evidence:** On song 43, the judge read the outside-scale share against the kept 0.071, while 349 sets 4.5% for a minor song. The share of lines ending on the tonic fell from 14.4% (read on C under v114) to 6.9% (read on A), against the kept 27.7%. It now costs 0.53 in the main run and 0.62 in the control, where under v114 it was not among the eight costliest measures. In song 43's control, the content judge's median fell from 0.96 to 0.33.

**Fix:** Read the kept windows of minor-key songs by the same rule (on their tonic, natural minor) and keep a second set of means for minor songs. The judge reads a minor song against that set. If the kept minor windows are too few to fit, say how many there are.

**Check:** For a minor song, the judge's kept means for the outside-scale share and the tonic ending come from the minor set. The tonic-ending cost is under half a point.

### 360. Fix 351 lowers verse 2's share, and 331's rate cannot raise it.

**Problem:** A bar left out of a copy is a bar that does not return. Far fewer lines are now given up, but verse 2 returns less of verse 1. The copy rate that 331 moves is already at its ceiling.

**Evidence:** Copies given up fell from 2,353 lines to 41 on song 43, and are 110 (1.8%) on song 40 and 6 (0.2%) on song 42. Bars left out came to 10,319, 8,419 and 10,662 in the three main runs. Verse 2's median share fell on every song:

| Song | Main run | Control |
|---|---|---|
| 40 | 0.36 → 0.33 | 0.45 → 0.33 |
| 42 | 0.50 → 0.44 | 0.50 → 0.38 |
| 43 | 0.50 → 0.25 | 0.50 → 0.25 |

331's rate ended at 0.983 and 1.0 on song 40 and at 1.0 on song 43. 351's test failed on all three songs, and 338's on songs 40 and 43 (on song 43 for the first time).

**Fix:** Before leaving a bar out, fit it again as 327 does (the copy kept, the bar's rhythm refitted to the words). Leave it out only if that fails. Count left-out bars against verse 2's share when 331 sets the rate.

**Check:** Verse 2's median share within 10 points of 50%. Lines given up under one in ten. Bars left out printed.

### 361. Unit returns are drawn only in sections whose lines are all two bars (the port).

**Problem:** My port of 346 and 350 treats a unit as a line. It draws a return only where every line of the section is two bars. Song 40's sections are not, so it draws none.

**Evidence:**

- **Song 40:** no unit return was drawn in either run. Unit 4 returning unit 2 reads 0.9% (control 0.3%) against the kept 18.8%, costing 0.62 (0.80).
- **Song 42:** line 4 returned line 2 in 123 builds; the measure reads 1.4% (0.8%), costing 0.57 (0.76).
- **Song 43:** unit 3 now returns unit 1 at 15.1% (v114 none). Its cost fell from 1.48 to 0.09, and unit 4 returning unit 2 costs −0.01.

350 held only on song 43.

**Fix:** Draw unit returns on the section's two-bar units, read on the bar grid, whatever the line lengths. A unit that starts inside a line copies the earlier unit's rhythm and contour from that point.

**Check:** No unit return over half a point on songs 40 and 42. Unit returns printed by unit, not by line.

### 362. The judge's first breaks soft limits and sits outside the kept repeats.

**Problem:** 352 makes the pick the judge's first. On these runs the judge's first is far from the composite's first, usually carries a soft break, and its repeats fall outside the kept middle half.

**Evidence:**

- **The two orders disagree.** The composite's first ranked 294th to 602nd of the judge's order; on song 40's main run it was last of 602. The judge's first ranked 57th to 707th on the composite. The picks' composite scores were 0.45–0.75, against 0.86–0.90 for the composite's first.
- **Soft breaks.** Five of the six picks carry a soft break: the rhythm band on three, plus spectral, surprisal and memory.
- **Repeats.** In five of six runs, a pick's verse or chorus repeat falls outside the kept middle half (verse 0.14–0.39, chorus 0.13–0.40): song 40 verse 0.07 (control 0.125); song 42 verse 0.548 and chorus 0.062; song 43 chorus 0.10 (control verse 0.41).
- **Lift.** On song 40's main pick, the chorus has no lift over the verse (median 0, top 0). On song 43's control pick, the chorus sits 4 semitones under the verse at the median.

**Fix:** Pick the judge's first among the survivors with no soft break, a repeat inside the kept middle half, and the chorus lifted over the verse at the median. Print how many survivors qualify. If none do, take the judge's first and say so.

**Check:** The pick has no soft break and its repeats fall inside the kept middle half. Its rank on the composite is printed.

### 363. 317's test is read without 337's spread.

**Problem:** A design gate's pass rate is read against nine in ten with no spread, so a run can fail it on noise.

**Evidence:** Song 43's design gate passed 91.3% in the main run (v114 93.0%) and 89.7% in the control (v114 90.2%). The control is 0.3 points under the line, against a spread of about one point at 1,000 builds. 317 and 326 failed on song 43 for the first time. Design deaths rose from 69 to 86 (main) and from 98 to 103 (control), inside the spread.

**Fix:** Read 317 with 337's spread. A rate is under nine in ten when it is more than one spread below 0.9.

**Check:** 317 is printed with its spread. It holds on song 43 at today's rates and fails at 88% or lower.
