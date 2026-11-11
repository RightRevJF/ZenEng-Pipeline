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
