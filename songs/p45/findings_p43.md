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
