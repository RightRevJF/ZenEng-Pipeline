# Review 22: Luthier v36 (fixes 937–939)

Branch `luthier-v8-stage1` at 5090503, merged into main at a006166. Answers the list for v36 (749.117 to 749.119).

## Byte for byte

- The six makers write every kept table byte for byte.
- All five song records (52, 54, 55, 58, 59), song 52's and song 53's run files and `stage4_results.json` reproduce.
- `soundness.py` reproduces `soundness.json`: sound, no lean.
- `neighbour.py` reproduces `neighbour_v36.json`.

## The fixes

- **937** holds. Both pool figures carry their own names, and the earlier rows are corrected.
- **938** holds, and corrects me. 935's stat counted the limit being set, not it changing anything. `cmp935.py` shows songs 55, 54 and 58 note for note the same with and without it. My 749.119 read the stat as a change. The aim gate is gone.
- **939** works where the aim is reachable and stops where it is not:
  - **Song 59.** The fit closes on the aim: repeats 0.217 against 0.210, steps 0.400 against 0.379.
  - **Song 55.** Repeats are 0.212 against 0.158, just outside a quarter width (0.045). Its returning lines still repeat 0.275 against the fresh lines' 0.173.
  - **Song 54.** The fit keeps round 1, its starting weights (step 1.2, repeat 1.0). Repeats stay at 0.222 against 0.110 (749.121).

## Is the random pool pick's 5.1 in 100 real?

Not shown. A bootstrap over the pools (`studies/review22/pool_boot.py`) resamples each song's pool with replacement, 200 times, 2,000 random triples each. The random pool pick's rate is 5.1 in 100, but its 90% range is 2.6 to 8.6. The pools hold 57, 58 and 88 builds, and which builds land in them moves the rate that much. v34's 2.5, v35's 2.6, v35-without-934's 8.0 and v36's 5.1 all sit inside one range.

By the same bootstrap, a random pick from every build that lived fails 9.9 in 100 (90% range 9.0 to 12.5). That reading is tight enough to compare across windows. 938's check (2.5 or better) cannot be judged on one run of a thousand builds (749.120).

## The question: take 749.104 and 749.103 head on, outside the engine first?

**749.104, yes, outside the engine first.** It is the one mechanism several open items wait on:
- the near repeats kept tunes sing (the study's finding);
- bars sung again (749.109) and varied returns (749.101);
- and, now, the returning lines' extra repeats (939 leaves them 0.10 and 0.05 over the fresh lines in songs 55 and 54).

Write the rule and the prediction before the trial, as the peak trials did. Score on songs 55, 54 and 58; read song 59 without counting it.

**749.103, not head on.** Variety is the sum of the checks the aim does not set (rhythm scaling, the words' fit, onsets), and pushing on it directly would game the measure. Two things would move it honestly:
- **The aim's reach into rhythm (749.109).** It waits on 749.104.
- **More practice songs.** Three songs make pools too small to read the rule or variety apart from luck (749.120), and the third peak trial is already waiting on a second wide-aim song.

Read 749.103 as the outcome of those, not as a target.

## Song 58

Thirteenth edition, from the v36 record. E major, E3 to C♯4, 337 seconds. Range 9 (Bird Dog 9) and rhythm scaling 0.541 are under the kept 10th. The tune sits on its top note 25 times (54 under v35; Bird Dog twice). The twelfth edition is kept in `songs/p68/out/twelfth_edition_v35/`. 44 of 44 document checks pass.

## Findings

749.120 to 749.122, in `songs/p68/fixlist_v37.md`. Next finding 749.123; next fix 940.
