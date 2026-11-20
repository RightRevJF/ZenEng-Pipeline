# Luthier list for v34 (since v33)

20 November 2026. Luthier v33 (fixes 928–930) is reviewed (`lib/luthier/REVIEW_stage20.md`) and merged into main at a1e6d2f. Every kept table, the four song records, song 53's run and parts, `soundness.json` and `neighbour_v33.json` reproduce. 928 and 929 hold as written: song 53 builds again, and the run gate now removes no builds. The engine is sound by the rule on the picks and on the pools. Song 58 is rebuilt from its v33 record (eleventh edition, E major; 44 of 44 document checks pass). Three new items (749.110 to 749.112). Next finding 749.113; next fix 931.

## The two questions, in short

1. **The step weight at its limit is a symptom; don't widen the limits.** The weight acts only on lines drawn fresh, about 13 notes in 100. At its limits it pushes those lines past any kept song to move the whole song a little: song 58's fresh lines step 11 times in 100, song 54's 79. In song 58 the cause is the melismas: drawn at the kept upper quartile, they add 13 points of steps, and Bird Dog has none. Draw the melisma share from the aimed song, and bound the fit by the fresh lines (749.110).
2. **Song 55's tunes never reach their top.** Their highest note sits a median 4 semitones under the verse's top, and their lowest is at the floor. A line's spread acts only on fresh lines, so widening it cannot move the range. Plant the peak, where the aimed song has it, in a line the returns will copy (749.111).

## Items

### 749.110 Fit the steps where they are made, and take the melismas from the aimed song
**Problem.** 930 scales the step and leap weights until the whole song's shares meet the aim. The weights act only on lines drawn fresh. Lines that return (copies, 712, 818's borrow) carry their source's moves and change them only where they are refitted. Melismas add a step below by rule. At the limits the fit pushes the few fresh lines past anything kept, and the whole song moves a third as far. Song 58's melisma share is drawn from the kept quartiles (16.2 syllables in 100). Bird Dog has none, so the fit is pressing the fresh lines to undo steps the aimed song never sings.
**Evidence.** `studies/review20/stepfit.py`, 120 builds a weight:

| | Step weight 0.3 | 1.2 | 3.0 | 6.0 |
|---|---|---|---|---|
| Song 58: steps as sung; before melismas; in fresh lines | 0.430; 0.295; 0.113 | 0.485; 0.382; 0.312 | 0.519; 0.444; 0.512 | 0.553; 0.486; 0.659 |
| Song 54: the same | 0.280; 0.218; 0.105 | 0.382; 0.332; 0.383 | 0.492; 0.459; 0.634 | 0.567; 0.547; 0.787 |

Notes in fresh lines: 13 in 100 (58), 12 to 15 (54). Melisma second notes are 13.3 sung notes in 100 in song 58 and 7.2 in 54. Kept steps 10th to 90th: 0.265 to 0.558. Melisma shares (syllables in 100), drawn against the aimed song's (`studies/words/sung_syllables.json`): 3.8 against 10.7 (55), 8.6 against 3.6 (54), 16.2 against 0.0 (58). With the default weight of 1.2, song 58's steps before melismas are 0.382, at its aim of 0.398. Song 54's aim (0.595) is past the kept 90th.
**Fix.** (a) Draw the melisma share from the aimed song, as 925 takes its lift and 926 its run, inside the kept 10th to 90th. (b) Bound the fit by the fresh lines: stop scaling a weight once the fresh lines' share leaves the kept 10th to 90th, and write the fresh lines' shares into `moves_fit` beside the whole song's. (c) Where the aim lies past the kept 90th (song 54), accept the shortfall. The rest of the reach is in the returning lines, which is 749.104's fix.
**Check.** In each song, the fresh lines' step and leap shares inside the kept 10th to 90th. Song 58's fitted step weight inside its limits, and its builds' steps within a quarter of the kept middle half's width of the aim. The rule holds on the pools.

### 749.111 Plant the peak: the range is set by a hard top, not a reached one
**Problem.** 927 sets each part's top so floor to top spans the aimed range. The draw cuts its candidates at the top and pulls toward the centre, and only fresh lines are drawn. So a wide aim's top is seldom reached (song 55), and a narrow aim's tune presses against it (song 58). All three picks span less than their aims. The register spread was tried in the fit and does not move the range, because the returning lines copy whatever the fresh lines reached.
**Evidence.** `studies/review20/stepfit.py` and `ceiling.py`. Song 55: the builds' highest note at a median of 74 (quartiles 72, 76) against tops of 78 (verse), 76 (chorus) and 80 (bridge); their lowest at the floor (60); a build reaches a part's top 15 times in 100. Picks span 14, 12, 8 against aims of 19, 14, 9. Song 58's pick spans 7 semitones before melismas and sits on its top note 32 times, 8 notes in 100; its title is sung on one pitch. Bird Dog sits on its top twice. A quarter of song 58's builds sit on their top more than nine kept tunes in ten.

Kept tunes: share of notes on the top note, 10th to 90th, 0.3, 0.5, 1.3, 4.5, 8.7 in 100. The top is sung a median 4 times (quartiles 2, 4, 13), first reached at 0.37 of the song (0.15, 0.72), and first in a verse in 62 of 160 tunes, a chorus in 64, a bridge in 14. Don't Ask Me Why reaches its top first in a verse, at 0.04 of the song, and sings it 17 times.
**Fix.** In the section where the aimed song first reaches its top, the first line drawn fresh draws its highest stressed note at the floor plus the aimed range (within a scale step), so the lines that return carry it as kept tunes repeat theirs. Set the parts' tops a step or two above that note, so it is reached rather than pressed against. Try it outside the engine on the three songs before building it.
**Check.** In each song, the builds' span within 2 semitones of the aim in at least half the builds, and their share of notes on the top note inside the kept 10th to 90th in 9 builds in 10. The rule holds on the pools.

### 749.112 The record's stats count the fit's trial builds
**Problem.** 930's trial builds run on the same engine before `run`, and `run` does not reset `self.stats`. Every count in `melody.stats` therefore covers the trial builds as well as the run's thousand.
**Evidence.** Rounds of 80: 2, 6 and 6 rounds in songs 55, 54 and 58, so 160, 480 and 480 more builds. The paper's "first notes moved, over a thousand builds: 923, 1785, 3070" is over 1,160, 1,480 and 1,480. The 712 count in song 54 (4,855) reads 4.9 a build over 1,000, but is 3.3 over 1,480.
**Fix.** Reset `self.stats` after the fit, and keep the fit's own counts in `moves_fit`. Restate the paper's counts.
**Check.** The record's stats come from 1,000 builds. The paper's counts are per thousand.

## Answered
- **928** holds: song 53's run and parts byte for byte; the cap is each engine's own.
- **929** holds: the run gate removes 0 builds in each song (342, 647, 278 before); first notes moved instead (749.112 for the counts). Picks' runs 5, 3, 8 against 5, 3, 9.
- **930** holds as written; its limits are 749.110.
- **749.107 reread:** the floor passes over 5 of 52 builds in song 55 (7 of 44 before). Fewer, as predicted once 929 stopped removing the repeats. Keep the ten parts.
- **749.109 trial:** agreed. The borrows cannot reach the aim while a borrowed line is refitted note by note to new words. 749.104's fix comes first.

## Carried
- **749.104** Fit a section's later lines to its earlier bars, splitting and merging notes. 749.109 and 749.101 wait on it, and 749.110(c) does too.
- **749.103** Variety counted on both sides: 1.46 against the kept 10.5 (1.18 under v32); pooled width 0.50 against the 0.75 asked.
- **The two readings of repeated figures** in one record (as sung, and before melismas).
- **749.61** 6/8: song 52, no kept 6/8 table.

## Order of work
1. 749.112 (so the counts read right). 2. 749.110 (a), then (b). 3. 749.111, tried outside the engine first. 4. 749.104 with 749.109 and 749.101. Rerun `neighbour.py` and `studies/review20/` after each; the rule must hold throughout.

## Songs

| Song | Folder | Under v33 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 337 s; key E; aimed at Bird Dog; spans 8 (aim 9); on its top note 32 times; eleventh edition rebuilt from this record |
| 55, Your Yard Man | p65 | 244 s; key A; spans 14 (aim 19); the floor passes over 5 of 52 |
| 54, The Man Mama Prayed I'd Be | p64 | 307 s; key G; spans 12 (aim 14); step weight at its limit (6) |
| 53, Sung to Sleep | p63 | builds again; byte for byte |
| 52, The Room Next Door | p62 | no aim; unchanged |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, the seven kept tables, `studies/soundness/soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones.
