# ZenEng fix list after v114

*Song 43, Blue Movie, on v113 and v114 · findings 348–353 (v114's fixes took 340–347) · with the tests of 310–347 on its own runs (321)*

v114's last fix is 347 (Window 134). This list starts at 348. v113's 337 and 338 and v114's 340–347 were ported, and a new song was written on them: song 43, Blue Movie, from the writer's sonnet. It is up-tempo dance-pop at 118, four on the floor, in A minor for a light tenor, 80 bars, with one design gate on the chorus.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Nothing blocked the port, and no two fixes conflicted.

## Songs since v114

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 43 | Blue Movie | v113–v114 on a new song: dance-pop, q = 118, A minor (the first minor-key song on these fixes), 80 bars. Designs: the chorus figure falling a step, the lift, the chanted post-chorus (Q15 A). Lyric density kept (342, Q14 A). 1,000 main and 1,000 control, each twice. Survivors 811 and 819; orders df5dff409ad9 and e2d6fa8c04c5, both reproduced. Record: the judge's first (Q18 A), no hand edits. | 348–353 |

## The tests of 310–347 on song 43 (main run; held means held in the control too)

| Fix | Read against | Main | Held? |
|---|---|---|---|
| 310 | kept 0.04-0.23 | under floor 1.6%; parallel 0.164 (kept 0.14); paired lines 3940, partner given up 0 | yes |
| 311 | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | yes |
| 312 | kept 75th 3.6% | verse 2.7%, chorus 3.2%; leap knob 1.0 | yes |
| 313 | kept 25-70% (median 50%) | share [0.125, 0.5, 0.75]; in range 84%; given up 2353 (58.8%); left out 70 | yes |
| 314 | kept verse share 40-57%; the rule (a check) | range [10.0, 15.0, 18.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.316, 0.526, 0.611]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 86%; floor 1% | yes |
| 315 | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.011, 0.162, 0.38]; stop none | yes |
| 316 | a reading (335: tries and redraws) | redraws 0/4573; entries on 0.273, after 0.652, pickup 0.074 | reading |
| 317 | the paper's 317: nine in ten | the design gate (Q15 A) passed 93.0% (control 90.2%) | yes |
| 318 | a reading | up-tempo dance-pop, q = 118, four on the floor, straight; sixteenth onsets [0.031, 0.052, 0.081] | printed |
| 322 | kept 0.04-0.23 | paired 3940 (1554 of another length); given up 0 (0.0%); parallel 0.164; under floor 1.6% | yes |
| 323 | kept 25-70% | one-over bars copied without the weakest onset 459; left out 70; verse 2 in range 84% | yes |
| 324 | the rule's own statement (a check) | 991 tonic endings, on the nearest to the centre 1.0 | yes |
| 325 | the rule's own statement (a check) | design failures for the registers 0; the last line on the tonic 100% | yes |
| 326 | the paper's 317 | the design gate (Q15 A) passed 93.0% (control 90.2%) | yes |
| 327 | a reading (335: a count kept songs do not have) | join deaths 0 | reading |
| 328 | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.031, 0.052, 0.081] | printed |
| 329 | kept 8-13; the rule (a check) | sung [13.0, 17.0, 17.0] vs drawn [15.0, 18.0, 19.0]; chorus window [8.0, 10.0, 13.0]; range not among the heaviest give-aways | yes |
| 330 | kept 0.04-0.23 | likeness 0.164; copies failed and the stresses kept 531; given up after the stresses 0; partners given up 0 (0.0%) | yes |
| 331 | kept 25-70% (median 50%) | rate 0.939; verse 2 share [0.125, 0.5, 0.75] (5th, median, 95th) | yes |
| 332 | v110's counts (the paper's test) | key-word deaths 14 (v110 89); frozen none | reading |
| 333 | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | yes |
| 334 | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.031, 0.052, 0.081] | printed |
| 336 | a reading | under floor 1.6%; content median 0.7; order median 1.82; measures outside the kept middle half 1 of 46 | reading |
| 337 | a reading (main against control) | deaths by cause, main against control: all within two spreads except the design gate (69 against 98, spread 12.4) | printed |
| 338 | kept 25-70% (median 50%) | verse 2 share [0.125, 0.5, 0.75]; rate 0.939; copies given up 2353 | yes |
| 340 | a reading (Window 134: 11.0 and 10.4) | gap 8.95 (Window 134: 11.0, 10.4); costliest [('gap_eighth', 2.76), ('outside_scale', 1.59), ('unit3_returns', 1.48), ('on_offbeat_eighth', 0.8), ('on_beats_2_4', 0.5), ('distinct_pitches', 0.48), ('on_beat3', 0.44), ('chord_tones_on_downbeat', 0.36)] | printed |
| 341 | kept 54% pushed, 31% in runs | sixteenth onsets 4713: pushed 22%, in runs 69%; sixteenth gaps cost 0.13 | **no** |
| 342 | kept 3.6-4.1 (a reading) | builds' notes a bar [3.875, 4.375, 4.625] (kept 3.6-4.1) | printed |
| 343 | kept 4.04 | distinct lengths 4.0 at the median; cost 0.06; palette dropped for 40 lines | yes |
| 344 | kept 7.1% | outside the scale 1.3% (kept 7.1%); cost 1.59 | **no** |
| 345 | kept 72% | cost verse -0.0, chorus -0.05; chord tones on long notes 62% | yes |
| 346 | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.8, 'distinct_pitches': 0.48, 'unit2_returns': 0.05, 'unit3_returns': 1.48, 'unit4_to_unit2': -0.01} | **no** |
| 347 | the kept mean (340's judge) | over half a point: [('gap_eighth', 2.76), ('outside_scale', 1.59), ('unit3_returns', 1.48), ('on_offbeat_eighth', 0.8), ('on_beats_2_4', 0.5)]; gap 8.95 | **no** |

319: the instrumental lines are read in the consistency check (all inside their instruments). 320: no figure here comes from a rescoring. 321: this table. 335: every row names what it is read against. The control's columns are in the test report and in songs/p45.

## The fixes

### 348. Fix 341 does not make sixteenths pushes.

**Problem:** Weighting a run down and a push up leaves the shape of the sixteenths almost where it was.

**Evidence:** Of onsets on a sixteenth position: 22% pushed and 69% in runs (control 13% and 79%), against the kept 54% and 31%. The share of sixteenth gaps itself is at the kept figure (cost 0.13 points). Runs come from dense drawn lines, where the rhythm table outweighs a factor of 0.25, and from returning lines, whose words are fitted by splitting events on the sixteenth grid.

**Fix:** In a drawn line, a sixteenth-position onset is allowed only as a push (the next onset an eighth or more later). A returning line's words are fitted by splitting on the eighth grid unless there is no room.

**Check:** 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point.

### 349. Fix 344's weight cannot reach the kept share of notes outside the scale.

**Problem:** The knob rose by its largest step each round (1 to 8) and the walk still offered almost no outside notes. The key profile weights an outside pitch class near zero, and half of builds are drawn at a share of zero.

**Evidence:** Outside the scale 1.3% of notes (control 1.5%), kept 7.1%; cost 1.59 points (1.42), the second heaviest.

**Fix:** Place the drawn share directly: the chosen notes (unstressed, a step from their neighbours, against no chord tone a semitone away, as fix 200 places them) move to the song's sung extra pitch class.

**Check:** The mean within two points of the kept 7.1%; cost under half a point.

### 350. Four-line sections never return line 1 at line 3.

**Problem:** The six-line verse and bridge plans are cut to four lines, and the cut drops their returns (ABCDAB becomes ABCD). Fix 346 aims only units 2 and 4.

**Evidence:** Unit 3 returning unit 1: kept windows 31.5%, builds 0.8%; cost 1.48 points (control 1.57), the third heaviest.

**Fix:** Draw four-line plans from the kept unit-return rates, unit 3 returning unit 1 at the kept 31.5%, with units 2 and 4 as 346 has them.

**Check:** No unit return costs over half a point.

### 351. Fix 338's rate and fix 303's check pull against each other.

**Problem:** Read on unaimed builds, the rate climbs to 0.94. At that rate 303's one-onset check gives up most copies, and the share reaches 50% only across the lines that are given up.

**Evidence:** Rate 0.94 (control 0.95); copies given up for 2,353 of 4,000 verse 2 lines (59%; control 2,336). Verse 2's share is 50% at the median in both runs, so 338's test holds.

**Fix:** A bar that fails 303's check is left out of that copy, and the rest of the line keeps its copied bars, instead of the whole line being given up. The rate is then read again.

**Check:** Copies given up under one line in ten; the share within ten points of 50%.

### 352. The pick rule rewards repetition (255's open question).

**Problem:** The composite's terms for compressibility and memory favour a melody that repeats itself. Its first inside the judge's top half was the most repetitive build in the run.

**Evidence:** The pick by 255 repeats a note on 51% and 48% of moves (kept 75th percentile 40%; run median 25–27%), judge 1.69. The judge's first is judge 4.55 with content 4.54, above the kept median, and composite rank 415 of 811. The writer took the judge's first (Q18 A).

**Fix:** The pick is the judge's first. Or it is the composite's first among builds whose readings are inside the kept middle half (repeats among them) and whose measures cost under half a point (347).

**Check:** The pick's repeats inside the kept middle half, and the pick in the judge's top tenth of survivors.

### 353. The paper has no rule for a minor key.

**Problem:** Every table the search reads is major-keyed. Read on a minor tonic, a minor song's natural notes count as outside the scale.

**Evidence:** Song 43, in A minor, was read on C. Its endings were set on A by the song's own rules. The kept windows' outside-scale mean of 7.1% suggests the kept minor songs were read the same way, but the paper does not say.

**Fix:** State how a minor song is read (on its relative major, or on its tonic with the minor scale), and how the kept minor songs were read.

**Check:** The paper names the rule. A minor song's degree and outside-scale readings sit in the kept range.

## Order of work

1. **352** (the pick rule): it decides which build becomes the song, and 255's question was carried to research by v113.
2. **348** (sixteenths as pushes, structurally) and **350** (four-line plans with unit returns): together they carry about 4 of song 43's 9 points.
3. **349** (outside notes placed directly).
4. **351** (a failed bar left out of a copy, not the line).
5. **353** (the rule for a minor key).

## Regression line

After these fixes, song 43 reruns at PYTHONHASHSEED 0, N 1000, main and control. Each run must reproduce its frozen order twice: today's are df5dff409ad9 and e2d6fa8c04c5 (seed 20261553), and they will change with the code.

What song 43 must keep:

- the locked lyric, every syllable sung;
- the chorus design: 'blue movie' falling a step, 'starring nobody but you' lifting back, the chant;
- the design gate at nine in ten or more;
- all 39 consistency checks.

After 348–353: sixteenths 44% pushed or more; outside notes within two points of 7.1%; no unit return over half a point; copies given up under one line in ten; the pick inside the kept repeats.

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

## Blind-pick tally

Song 43's blind pick is offered after delivery. The tally stands at 28 songs until it is answered: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40 and 41 are not yet offered.
