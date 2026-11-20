# Luthier list for v37 (since v36)

20 November 2026. Luthier v36 (fixes 937–939) is reviewed (`lib/luthier/REVIEW_stage22.md`) and merged into main at a006166. Every kept table, all five song records, song 53's run, `soundness.json` and `neighbour_v36.json` reproduce. 937 and 938 hold. 938 corrects my 749.119: 935's stat counted a limit set, not a change, and songs 55, 54 and 58 build note for note the same. 939 closes song 59 on its aim and leaves songs 55 and 54 short. Song 58 is rebuilt from its v36 record (thirteenth edition, E major; 44 of 44 document checks pass). Three new items (749.120 to 749.122). Next finding 749.123; next fix 940.

## The question, in short

**Take 749.104 head on, outside the engine first. Don't take 749.103 head on.** 749.104 (fitting a section's later lines to its earlier bars) is the one mechanism that 749.109, 749.101 and the returning lines' extra repeats all wait on. Write its rule and prediction first, score it on songs 55, 54 and 58, and read song 59 without counting it.

749.103 is the sum of the checks the aim does not set. Pushing on it directly would game the measure. It should move through the aim's reach into rhythm (749.109, after 749.104) and through more practice songs, and be read as the outcome.

## Items

### 749.120 Read the pool figures with their spread
**Problem.** The random pick from the engine's pool is read on pools of 57 to 88 builds. Which builds land in a pool moves the rate more than the fixes do, so 938's check (2.5 in 100 or better) cannot be judged on one run.
**Evidence.** `studies/review22/pool_boot.py`: each pool resampled with replacement, 200 times, 2,000 random triples each. Random pool pick 5.1 in 100, 90% range 2.6 to 8.6. v34's 2.5, v35's 2.6, v35-without-934's 8.0 and v36's 5.1 all fall in that range. A random pick from every build that lived: 9.9 in 100, 90% range 9.0 to 12.5. The neighbour choice moves the same way (400 draws, 2 to 20 failures).
**Fix.** Have `neighbour.py` print each figure's bootstrap 90% range beside it, and write checks against the last window's range, not its point. For window-to-window comparison, use the every-build figure, or run the three songs at 3,000 builds so the pools are larger.
**Check.** Every pool figure in the paper carries its range, and a fix's check says whether the new figure falls outside the last window's range.

### 749.121 Fit each weight against its own band
**Problem.** 939's bisection tests the fresh lines against the kept 10th to 90th on all three moves at once, and moves all three weights together. When one weight's aim lies past the band (song 54's steps, 0.595 against the kept 90th of 0.558), its overshoot pulls the other weights back with it. Song 54's fit keeps round 1, its starting weights.
**Evidence.** Song 54's `moves_fit`. Round 2 (step 2.883, repeat 0.263) took the fresh lines' steps to 0.793, outside the band. The bisection then drew all three weights back together, and the kept round is round 1 (step 1.2, repeat 1.0). Builds' repeated notes 0.222 against an aim of 0.110. Its repeat aim is also under the kept 10th (0.157).
**Fix.** Test each weight's fresh-line share against its own band, and bisect each weight on its own. A weight whose aim lies past the band stops at the band's edge, and the others go on toward their aims.
**Check.** Song 54's kept round is not round 1. Its builds' repeated notes are at or under the kept 25th (0.210), and its steps are at the band's edge.

### 749.122 Put the returning lines' repeats into 749.104's trial
**Problem.** 939 scales the refit's split notes and lead-ins by the repeat weight, and the returning lines still repeat more than the fresh lines they come from. What remains is made in the refit: the 882 choice of which notes split or drop, and a dropped note between two equal pitches. That is the machinery 749.104 replaces.
**Evidence.** `studies/v36_trials/trace_v36.json`: repeats in fresh lines 0.173 and 0.200, in returning lines 0.275 and 0.250 (songs 55 and 54). Song 55's builds: 0.212 against an aim of 0.158.
**Fix.** In 749.104's trial rule, say how a split or dropped note takes its pitch, and include the returning lines' repeats in the trial's check. Trace which refit step makes the excess before deciding.
**Check.** In the trial, returning lines' repeated notes no more than 0.03 over the fresh lines' in songs 55 and 54.

## Answered
- **937** holds: both figures named, earlier rows corrected.
- **938** holds: 935 changes no build of songs 55, 54 or 58. The aim gate is gone. My premise was wrong; the stat counted a limit set, not a change.
- **939** holds in song 59 (repeats 0.217 against 0.210) and song 58 (0.403 against 0.373). Songs 55 and 54 are 749.121 and 749.122.

## Carried
- **749.104** Take it head on, outside the engine first (see above), with 749.122 inside it. 749.109 and 749.101 follow it.
- **749.103** Read as the outcome of 749.104, 749.109 and more practice songs, not as a target. Song 59: 3 checks of 21 outside the kept middle half (2 under v35).
- **749.111** The third trial needs a second wide-aim practice song. I can write one with the writer, and it would also widen the pools (749.120).
- **749.116**, **749.61**.

## Order of work
1. 749.120 (the ranges, so the rest reads right). 2. 749.121. 3. 749.104's trial with 749.122, outside the engine. 4. A new practice song with a wide aim, then 749.111's third trial. After each: `neighbour.py` with ranges, `studies/review20/`, `studies/holdout59/` (song 59 read, never fitted to).

## Songs

| Song | Folder | Under v36 |
|---|---|---|
| 59, Before the Bread Goes Cold (hold-out) | p69 | repeats 0.217 against 0.210; range 17 against 24; 3 checks of 21 outside the kept middle half |
| 58, Same Time Tomorrow | p68 | key E; range 9; top note 25 times; thirteenth edition from this record |
| 55, Your Yard Man | p65 | repeats 0.212 against 0.158 |
| 54, The Man Mama Prayed I'd Be | p64 | repeats 0.222 against 0.110; the fit kept round 1 |
| 53, 52 | p63, p62 | byte for byte |

## Regression line
The records of songs 52, 54, 55, 58 and 59, song 52's and song 53's run files, the seven kept tables, `soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones.
