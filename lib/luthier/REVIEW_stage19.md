# Review 19: Luthier v32 (fixes 924–927)

Branch `luthier-v8-stage1` at 63e6fff, merged into main at 91db1a6. Answers the list for v32 (749.98 to 749.102); 749.104 is a study, not built.

## Byte for byte

- The six makers write every kept table byte for byte, `kept_readings.json` included (it gains `song_names` and `lifts`; rows unchanged).
- The four song records (`lyric52/54/55/58.song.json` with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json` and `stage4_results.json` reproduce.
- `soundness.py` reproduces `soundness.json`: sound; 4, 4, 8 checks outside the middle half; one lean past the middle half, rhythm scaling low.
- `neighbour.py` reproduces every field of `neighbour_v32.json`.
- **Not reproduced: song 53.** `metre_engine.py songs/p63/spec53.json 3000` stops with `AttributeError: type object 'Engine' has no attribute 'RUN_CAP'`. `Hymn` does not run `Engine.__init__`, where 926 sets the cap, and `Engine.runs_ok` reads it from the class. With `RUN_CAP = 3` set on the class (one line), `spec53.run.json` reproduces byte for byte (749.105). The cap is also class state, so in one process every engine reads the cap of the last 4/4 engine made.

## The fixes

- **924** reads the floor as sung, as asked. The record says so (`read_as`).
- **925** takes the aimed song's lift where it is known (138 of 160). Song 58 now plans Bird Dog's 0 and sings 2, inside the gate's two.
- **926** follows the aimed song's longest run (5, 3, 9; the picks 5, 3, 9). The cap is right; how it is enforced is the trouble (question 1).
- **927** moves the tops to the aimed range: the picks span 14, 15, 10 against aims of 19, 14, 9, and every living build's median 16, 14, 10. Range now follows the aim. The steps do not (749.108).

## Question 1: is 926's across-lines gate too heavy at a cap of three?

The cap is not too low. Three is the aimed song's own longest run and the kept 10th percentile, and song 54's pick sings exactly three. The gate as built is too heavy, at every cap and most at three.

**What it removes.** It passes over 342, 647 and 278 builds of 1,000 in songs 55, 54 and 58. Traced on 300 tries per song (`studies/review19/runs.py`):

| Where the run that kills the build is made | 54 (cap 3) | 55 (cap 5) | 58 (cap 9) |
|---|---|---|---|
| Across a join, a copied or borrowed line in it | 102 | 58 | 26 |
| Across a join, lines marked fresh | 52 | 43 | 36 |
| Made by a melisma | 32 | 2 | 2 |
| Inside one line | 14 | 0 | 0 |
| Dead builds, of 300 | 200 | 103 | 64 |

In song 54, 162 of the 200 are one note over (a run of four).

**Why so many.** The draw's weight stops a run inside a fresh line and carries the run in from the line before (926's `_runin`). The other paths that write pitches are tested only inside themselves: a copy (`how` copy), a line sung again (712), a line that borrows an earlier line of its section (818, at 0.8, which also reaches lines marked fresh and is the likeliest path for the 52), and the melisma, whose second note is the step below and can land on the next note's pitch. The gate then reads the whole build as sung and removes it.

**What it costs.** The builds it removes repeat their figures more. Four-interval figures sung again, builds removed by 926 against builds alive (before melismas, 200 tries): 0.585 against 0.568 in song 54, 0.482 against 0.452 in 55, 0.705 against 0.624 in 58. A copy at a join is the near repeat that 749.104 finds missing. This is the likeliest cause of the paper's pool builds with few bars on a figure already sung rising from 50 to 57 in 100.

**Answer.** Keep the cap and the gate as a backstop. Test runs where they are made: every copying path tested with the run carried in, and on a failure the copy's first note moved a scale step toward its next note (as 839 lifts a held note) rather than the line drawn fresh. A melisma's second note takes the step above, or is not placed, where the step below would make a run past the cap (749.106).

## Question 2: should range and leaps come out of the page floor's mean?

No. Taken out (the floor refit to the kept 10th on the other eight parts, −0.711), the floor passes over 6 of song 55's 44 builds instead of 7, and the pick is the same build. Range plays no part in the seven it removes: their mean range sits at the kept mean (+0.03 of a kept spread, the plain way). They are surprising and repeat little:

| Part (kept spreads, + is plainer) | The 7 passed over | All 44 read |
|---|---|---|
| Surprise | −1.72 | −0.73 |
| Different intervals | −1.39 | −0.81 |
| Leaps | −1.30 | −0.65 |
| Repeated figures | −1.24 | −1.06 |
| Range | +0.03 | +0.36 |

Leaps are one of four parts that put them under, not the cause. The floor passes over nothing in songs 54 and 58. It is now doing what it was put in for, and what it finds in song 55 is the shortfall of 749.104 and 749.106. Leave the ten parts as they are (749.107).

## What else the review found

- **The steps do not follow the aim (749.108).** Every living build's median against the aimed song: steps 0.397 against 0.452 (55), 0.459 against 0.595 (54), 0.471 against 0.398 (58). Song 58, aimed at the fewest steps, steps most. Leaps follow in order (0.159, 0.138, 0.052 against 0.111, 0.120, 0.057) but 55 and 54 overshoot. `MOVE_STEP` 1.2 and `MOVE_LEAP` 1.6 are one setting for every song, and a narrow register pushes steps up on its own.
- **The repeats and the rhythm do not follow the aim (749.109).** Song 58 aims at Bird Dog, whose bars repeat more than nine kept songs in ten. Its pick repeats them less than nine in ten: bars on a figure already sung 0.184 (Bird Dog 0.698), on a rhythm already sung 0.282 (0.774), distinct rhythms over bars 0.718 (0.226). Every living build's median: 0.28, 0.41, 0.59. Song 54 misses its aim the same way on rhythm (0.534 against 0.775). Rhythm scaling sits at 0.571 to 0.587 whatever the aim (0.684, 0.403, 0.704). The paper's sentence that song 58 "now sounds like it" holds for range, runs and repeated notes, and is the reverse for its repetition and rhythm. It should be corrected.
- **Two readings in one record read differently.** `page_gate.builds_figures_again_quartiles` is read as sung (924); `every_build_figures_again_quartiles` and `every_build_first_120_…` are read before melismas. In song 58 they give medians of 0.504 and 0.630, which looks like a gate passing over repetition but is partly the reading. Read both as sung, or label them.
- **The study for 749.104** is sound and its finding is the right one: songs 55 and 54 repeat from whole sections back, and the near answer is missing. Two small differences from the other studies: `where.py` reads 167 kept tunes (`min_notes=100`) where `soundness.py` reads 160, and `pool.py` reads builds before melismas while the kept tunes carry theirs (as 749.102 was). Neither changes the finding.
- **Variety** rose from 0.77 to 1.18 (two-sided, pools against the kept 10.5); 749.103 is not met, as the paper says.

## Song 58

Tenth edition, from the v32 record: key E (D before), aimed at Bird Dog, range 10, a four-bar turn after chorus 1; 337 seconds. The ninth edition is kept in `songs/p68/out/ninth_edition_v31/`. 44 of 44 document checks pass.

## Findings

749.105 to 749.109, in `songs/p68/fixlist_v33.md`. Next finding 749.110; next fix 928.
