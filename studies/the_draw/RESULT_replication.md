# The peak climbed to: result of the second test

25 November 2026. Checks in `PREDICTION_replication.md` (written and committed before the runs). Songs 49, 60 and 59, the whole engine, a thousand builds.

**It fails again, on two lines: song 49's check 2 by one build, and the hold-out's share of builds with the peak planted (75 in 100 where 80 were asked). By the rule it is not built. It goes to the session and the writer with both results.**

| Check | Song 49 | Song 60 | Song 59 (hold-out) |
|---|---|---|---|
| 1. Living builds (v47) | 316 (287) | 242 (178) | 301 (207) |
| 2. The octave gate passes over (the line) | **36** (35) | 35 (41) | 49 (59) |
| 3. The peak planted, of v47's | 444 of 471: 94 in 100 | 731 of 825: 89 | **504 of 668: 75** |
| 3. Chosen tune's range (floor) | 17 (14.6) | 20 (15.6) | 19 (15.5) |
| 4. Builds' middle words' fit (v47) | 0.250 (0.243) | 0.295 (0.289) | 0.280 (0.289) |

## The two tests together, six songs

| | 55 | 54 | 58 | 49 | 60 | 59 |
|---|---|---|---|---|---|---|
| Living builds, v47 → the form | 223 → 269 | 256 → 268 | 294 → 375 | 287 → 316 | 178 → 242 | 207 → 301 |
| The octave gate passes over | 69 → 33 | 66 → 26 | 111 → 56 | 70 → 36 | 82 → 35 | 119 → 49 |
| cut by, in 100 | 52 | 61 | 50 | 49 | 57 | 59 |
| The peak planted, of v47's, in 100 | 85 | 90 | 91 | 94 | 89 | 75 |
| Chosen tune's range | 16 → 19 | 17 → 19 | 17 → 19 | 17 → 17 | 19 → 20 | 19 → 19 |

What is not in doubt: more builds live in all six songs (5 to 45 in 100 more); the gate's cost falls by half, give or take, in all six; no chosen tune loses range and four gain; the words' fit does not move; the first three songs stay sound and their pools are sounder (a random pool pick fails the rule 2.9 times in 100 against 6.5).

What failed: I set the gate's cut at "a half at least" and the form cuts it by a half, so it lands on both sides of my line (52, 61, 50, 49, 57, 59). And in the hold-out the peak is planted in a quarter fewer builds, past the fifth I allowed, though its chosen tune keeps its range of 19.

## My reading, kept apart from the rule

The rule says no, twice, and I do not build against it. But the two misses are of different kinds. The first is a threshold drawn where the effect happens to sit; a line at "a third" would have passed all six, and I cannot draw it there now. The second is real information: asking the peak's line to climb makes the plant fail more often, and in one song of six by enough to cross the allowance. Neither miss shows harm in anything the writer would hear.

So the ruling is not mine to make. Either:
- **build it** on the strength of the six-song table, the rule's two misses stated in the paper; or
- **hold it**, and try the next form with the rule written first: when the climb fails its 60 draws, plant the peak the old way (so no build goes without its peak), which should mend the hold-out's 75 and may give back a little of the gate's cut.

The form is in the code behind a switch that is off (`LUTHIER_PEAK_CLIMB=1`). With it off the engine writes v47's notes (song 54, byte for byte).
