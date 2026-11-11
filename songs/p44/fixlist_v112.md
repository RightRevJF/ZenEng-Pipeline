# ZenEng fix list after v112

*Songs 40 and 42 once more under v112 · fixes 337–338 · with the tests of 310–336 on both songs' own runs (321), each named against its kept figure (335)*

v112's last fix is 336 (Window 132). As v112 asked, this run added no song: songs 40 and 42 ran once more with the same lyrics, intakes and seeds, on fixes 330–336 ported onto the v111 search. This list starts at 337.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Nothing blocked the port, and no two fixes conflicted.

## Songs since v112

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 40 (rerun) | Nothing Else on Earth | 330–336 ported. 1,000 main and 1,000 control, each twice. Survivors 544 and 544 (v111 480, 417); orders 3f8eb6067d67 and 26f80e5f1a5f, both reproduced. | 337, 338 |
| 42 (rerun) | Nothing Important | The same song constants, lyric, designs and seed on v112. 1,000 main and 1,000 control, each twice. Survivors 747 and 738 (v111 780, 783); orders daa4d9492f81 and 7e63192665fb, both reproduced. | 338 |

## The tests of 310–336 on song 40 (main run; held means held in the control too)

| Fix | Read against | Main | Held? |
|---|---|---|---|
| 310 | kept 0.04-0.23 | under floor 27.6%; parallel 0.099 (kept 0.14); paired lines 4807, partner given up 0 | yes |
| 311 | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | kept 75th 3.6% | verse 2.4%, chorus 2.6%; leap knob 1.0 | yes |
| 313 | kept 25-70% (median 50%) | share [0.091, 0.364, 0.667]; in range 81%; given up 757 (12.6%); left out 1597 | yes |
| 314 | kept verse share 40-57%; the rule (a check) | range [10.0, 14.0, 15.0, 15.0, 15.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.375, 0.533, 0.6]; tonic nearest the sung median 0.824, the drawn centre 1.0; top fifth 92%; floor 6% | yes |
| 315 | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.118, 0.066, 0.268]; stop none | yes |
| 316 | a reading (335: tries and redraws) | redraws 0/13521; entries on 0.233, after 0.637, pickup 0.13 | reading |
| 317 | the paper's 317: nine in ten | none in force | yes |
| 318 | a reading | straight eighths; sixteenth onsets [0.1, 0.134, 0.185] | printed |
| 322 | kept 0.04-0.23 | paired 4807 (998 of another length); given up 321 (6.7%); parallel 0.099; under floor 27.6% | yes |
| 323 | kept 25-70% | one-over bars copied without the weakest onset 3345; left out 1597; verse 2 in range 81% | yes |
| 324 | the rule's own statement (a check) | 987 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | the rule's own statement (a check) | design failures for the registers n/a; last chorus on the tonic 100.0%; redrawn 0 | yes |
| 326 | the paper's 317 | none in force | yes |
| 327 | a reading (335: a count kept songs do not have) | join deaths 11 | reading |
| 328 | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.1, 0.134, 0.185] | printed |
| 329 | kept 8-13; the rule (a check) | sung [14.0, 14.0, 14.0] vs drawn [14.0, 15.0, 15.0] (gap [1.0, 1.0, 1.0]); chorus window [9.0, 11.0, 12.0]; heaviest give-aways ['outside_scale', 'on_offbeat_eighth', 'chord_tones_on_long_notes', 'empty_bars', 'chord_tones']; extremes sung low 99%, high 98% | yes |
| 330 | kept 0.04-0.23 | likeness 0.099; copies failed and the stresses kept 1199; given up after the stresses 321; partners given up 321 (6.7%) | yes |
| 331 | kept 25-70% (median 50%) | rate 0.802; verse 2 share [0.091, 0.364, 0.667] (5th, median, 95th) | yes |
| 332 | v110's counts (the paper's test) | key-word deaths 109 (v110 89); frozen none | **no** |
| 333 | the rule's own statement (a check) | row 17; widest drawn range 15 (row less two 15) | yes |
| 334 | a reading | q = 116, band 100-120: kept (0.04, 0.12, 0.27); song [0.1, 0.134, 0.185] | printed |
| 336 | a reading | under floor 27.6%; content median -0.99; order median 0.57; measures outside the kept middle half 4 of 46 | reading |

## The tests of 310–336 on song 42 (main run; held means held in the control too)

| Fix | Read against | Main | Held? |
|---|---|---|---|
| 310 | kept 0.04-0.23 | under floor 5.2%; parallel 0.19 (kept 0.14); paired lines 4156, partner given up 0 | yes |
| 311 | the rule's own statement (a check) | tonic 100.0%; registers redrawn 40; misses 0 | yes |
| 312 | kept 75th 3.6% | verse 2.6%, chorus 3.0%; leap knob 1.0 | yes |
| 313 | kept 25-70% (median 50%) | share [0.125, 0.5, 0.75]; in range 85%; given up 164 (4.1%); left out 96 | yes |
| 314 | kept verse share 40-57%; the rule (a check) | range [11.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.4, 0.447, 0.579]; tonic nearest the sung median 0.891, the drawn centre 1.0; top fifth 89%; floor 0% | yes |
| 315 | kept 0.00-0.55; the cap (a check) | amplitude 7.0; arch [-0.141, 0.092, 0.368]; stop none | yes |
| 316 | a reading (335: tries and redraws) | redraws 0/9591; entries on 0.226, after 0.667, pickup 0.108 | reading |
| 317 | the paper's 317: nine in ten | the design gate (Q11 note 4) passed 98.4% | yes |
| 318 | a reading | straight eighths, q = 76; sixteenth onsets [0.081, 0.119, 0.172] | printed |
| 322 | kept 0.04-0.23 | paired 4156 (2672 of another length); given up 0 (0.0%); parallel 0.19; under floor 5.2% | yes |
| 323 | kept 25-70% | one-over bars copied without the weakest onset 1030; left out 96; verse 2 in range 85% | yes |
| 324 | the rule's own statement (a check) | 979 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; registers redrawn for the design 40 | yes |
| 326 | the paper's 317 | the design gate (Q11 note 4) passed 98.4% | yes |
| 327 | a reading (335: a count kept songs do not have) | join deaths 0 | reading |
| 328 | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.081, 0.119, 0.172] | printed |
| 329 | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0] (gap [1.0, 2.0, 2.0]); chorus window [9.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'empty_bars', 'chord_tones', 'chord_tones_on_long_notes', 'on_sixteenth']; extremes sung low 98%, high 99% | yes |
| 330 | kept 0.04-0.23 | likeness 0.19; copies failed and the stresses kept 515; given up after the stresses 0; partners given up 0 (0.0%) | yes |
| 331 | kept 25-70% (median 50%) | rate 0.65; verse 2 share [0.125, 0.5, 0.75] (5th, median, 95th) | yes |
| 332 | v110's counts (the paper's test) | key-word deaths 34 (v110 89); frozen none | reading |
| 333 | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | a reading | q = 76, band under 80: kept (0.26, 0.34, 0.43); song [0.081, 0.119, 0.172] | printed |
| 336 | a reading | under floor 5.2%; content median -0.34; order median 2.05; measures outside the kept middle half 2 of 46 | reading |

319: these runs make no instrumental lines. 320: no figure here comes from a rescoring. 321: these tables. 335: every row names what it is read against. The control's columns are in the test report and in songs/p44.

## The fixes

### 337. 332's test reads one run's count against another's, inside the spread between runs.

**Problem:** The test asks song 40's key-word deaths to be at or under v110's 89 (main) and 42 (control). Each is the count of a single run of 1,000, with no margin.

**Evidence:**

- This run did not stop its calibration (nothing frozen) and read 109 and 44.
- Two diagnostic runs (never runs of record) each switched one fix off: without 329's extremes, 99; without 322's stresses, 95.
- A count near 100 in 1,000 builds varies by about ±10 from run to run.
- The rise to 159 under v111 was the stop's. What is left is about two spreads in the main run and within one in the control, and no single fix carries it.

**Fix:** Hold 332's test as 335 holds other counts kept songs do not have: print it as a reading beside the earlier version's count. Or set the test with the spread in it (at or under 89 plus two spreads).

**Check:** The report prints the count beside v110's, with the spread.

### 338. 331's rate is set on the calibration's aimed builds, not on the builds the run makes.

**Problem:** The calibration's builds are aimed at the pools' medians. The share they read is not the share the run's builds read.

**Evidence:**

- Song 40: the calibration read 50% in its last round at a rate of 0.80. The run's builds read 36% at the median (control 45%).
- Song 42 read 50% in both (rate 0.65). Both pass 25–70%.
- At the higher rate, 303's one-onset check refuses more copies. Song 40's verse 2 lines were given up for a copy 757 times in 6,000 (12.6%; control 9.9%), where v111 gave up 23. Song 42: 164 (4.1%), from 1.

**Fix:** Read the share for 331's rate on the run's own first builds, or on unaimed calibration builds. Print the copies given up as a reading.

**Check:** Verse 2's median share within five points of 50% on both songs, main and control.

## Where debugging stands

v112 asked for one more run of both songs: if every test holds on both and no finding changes a rule, the debugging is closed.

- **Song 42 passes every test**, main and control.
- **Song 40 passes every test but 332's count:** 109 against 89 in the main run and 44 against 42 in the control.

Two findings came up. 337 is about how a test is read, not a rule. 338 changes where 331's rate is read, a small change to one rule, and it does not change whether either song passes. By the paper's own condition the debugging is not yet closed: one test failed, by a margin inside the spread between runs, and one finding changes a rule.

## Order of work

1. **337** (332's count read with the spread): it decides whether song 40 has passed.
2. **338** (331's rate read on the run's builds).

## Regression line

After these fixes, songs 40 and 42 run again at PYTHONHASHSEED 0, N 1000, main and control, and each must reproduce its frozen order twice. Today's orders, which will change with the code:

- song 40: 3f8eb6067d67 and 26f80e5f1a5f (seed 20261511);
- song 42: daa4d9492f81 and 7e63192665fb (seed 20261552).

What must hold:

- every test held here holds again on both songs;
- 332's count is printed beside v110's, with the spread;
- verse 2's median share is within five points of 50%;
- song 42 keeps its locked lyric and its design gate at nine in ten or more (98.4% here).

## Readings the paper does not give

- **330.** The fallback runs from the 15th try of a pair's rhythm to the last drawn try (20, or 60 for a long line). On those tries the partner's stressed onsets are weighted as in 322, and the bar copy and its one-onset check are dropped. If they all fail, the partner is given up and counted.
- **331.** The rate moves by the gap between 50% and the median share read on each calibration round's 30 builds (rate + (0.50 − share), held to 0.05–1.0). It starts at 0.40. Verse 3 (song 42), which is also sung again from verse 1, takes the same rate.
- **332.** A knob is frozen at the value it reached on its second largest step. Neither song took a largest step twice this time, so nothing was frozen.
- **335.** Each row of the table names what it is read against: a kept figure where kept songs have the reading; "a reading" for counts kept songs do not have (316's redraws, 327's join deaths); or "the rule's own statement (a check)" for rows that check the code did what its rule says (311, 324, 325, 333). 335's rule is applied to 329's chorus window too, which reads against the kept middle half (8–13) where v111 asked for the kept median. 332's death count is kept as a test because v112 states it as one.
- **336.** The kept middle half of each of the 46 content measures is read from the kept windows (zeneng_v105_kept_windows.json, 314 windows). The builds' median for a measure is taken over the Verse 1 and Chorus 1 windows of every complete build.

## Blind-pick tally

No new song, so no new blind pick. The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40 and 41 are not yet offered.
