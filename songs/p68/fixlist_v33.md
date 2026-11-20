# Luthier list for v33 (since v32)

20 November 2026. Luthier v32 (fixes 924–927) is reviewed (`lib/luthier/REVIEW_stage19.md`) and merged into main at 91db1a6. Every kept table, the four song records, `soundness.json` and `neighbour_v32.json` reproduce. Song 53 does not: the hymn engine stops with an error (749.105). The engine is sound by the rule on the picks and on the pools (a random pool pick fails 1.0 times in 100). Song 58 is rebuilt from its v32 record (tenth edition, E major, aimed at Bird Dog; 44 of 44 document checks pass). Five new items (749.105 to 749.109). Next finding 749.110; next fix 928.

## The two questions, in short

1. **The cap of three is right; the gate as built is too heavy.** Three is the aimed song's own longest run and the kept 10th, and song 54's pick sings three. But the gate passes over 647 of 1,000 builds in song 54 (342 in 55, 278 in 58), mostly one note over, and mostly where the draw never looks: a copied or borrowed line's join, and a melisma. The builds it removes repeat their figures more. Test runs where they are made and keep the gate as a backstop (749.106).
2. **Keep range and leaps in the floor.** Without them the floor passes over 6 of song 55's 44 builds instead of 7, and the pick is the same. Range plays no part in the seven; they are surprising and repeat little (749.107).

## Items

### 749.105 (a fault) The hymn engine cannot run
**Problem.** 926 sets `Engine.RUN_CAP` inside `Engine.__init__`, and `Engine.runs_ok` reads it from the class. `Hymn` never runs `Engine.__init__`, so its first call to `Engine.runs_ok` fails. The cap is also class state: in one process, every engine reads the cap of the last 4/4 engine made, so a hymn or a second song built after an aimed song would take that song's cap.
**Evidence.** `python3 lib/luthier/metre_engine.py songs/p63/spec53.json 3000` stops: `AttributeError: type object 'Engine' has no attribute 'RUN_CAP'` (from `Hymn.draw_line`). The committed `spec53.run.json` and `spec53.parts.json` could not be remade. With `RUN_CAP = 3` set on the class, `spec53.run.json` reproduces byte for byte.
**Fix.** Set `RUN_CAP = 3` on the class, and make the cap the instance's own: `runs_ok(ps, cap)` called with `self.RUN` everywhere in `Engine`, and 3 in `Hymn`.
**Check.** `spec53.run.json` and `spec53.parts.json` byte for byte. In one process, song 58 built and then song 53: song 53's record unchanged.

### 749.106 Test a run of one pitch where it is made, not after the build
**Problem.** 926's weight stops a run inside a fresh line and carries the run in from the line before. The other paths that write pitches are tested only inside themselves: a copy (`how` copy), a line sung again (712), a line that borrows an earlier line of its section (818, at 0.8, also on lines marked fresh), the held note 839 lifts, and the melisma, whose second note is the step below and can land on the next note's pitch. The whole-build gate then removes the build. It removes the builds that repeat most, and a copy at a join is the near repeat 749.104 finds missing.
**Evidence.** Deaths by 926 of 1,000: 342 (55, cap 5), 647 (54, cap 3), 278 (58, cap 9). On 300 tries per song (`studies/review19/runs.py`), where the killing run is made:

| | 54 | 55 | 58 |
|---|---|---|---|
| Across a join, a copied or borrowed line in it | 102 | 58 | 26 |
| Across a join, lines marked fresh (818's borrow the likeliest path; trace it) | 52 | 43 | 36 |
| Made by a melisma | 32 | 2 | 2 |
| Inside one line | 14 | 0 | 0 |

In song 54, 162 of the 200 builds removed are one note over. Four-interval figures sung again, builds removed against builds alive (`runs2.py`): 0.585 against 0.568 (54), 0.482 against 0.452 (55), 0.705 against 0.624 (58). The paper's pool builds with few bars on a figure already sung rose from 50 to 57 in 100.
**Fix.** One test, `runs_ok` on the run carried in plus the line, on every path that writes a line's pitches. Where a copy fails it, move the copy's first note a scale step toward its next note, as 839 lifts a held note, rather than drawing the line fresh. A melisma takes the step above, or is not placed, where the step below would make a run past the cap. Keep the whole-build gate as a backstop. Trace the 52 "fresh" joins in song 54 before saying which path makes them.
**Check.** Deaths by 926 under 10 in 100 in each song. Every pick's longest run, as sung, at or under its aimed song's. The pools' four-interval figures sung again at or above v31's medians.

### 749.107 Keep range and leaps in the page floor's mean
**Problem.** v32 asks whether range and leaps should come out now that the floor passes over 7 of 44 builds in song 55.
**Evidence.** `studies/review19/floor.py`. With the two parts out and the floor refit to the kept 10th on the other eight (−0.711), it passes over 6 of 44, and the first build past it, the pick, is the same. The seven's mean parts, in kept spreads with plus the plain way: surprise −1.72, different intervals −1.39, leaps −1.30, repeated figures −1.24, range +0.03. The floor passes over nothing in songs 54 and 58.
**Fix.** None. Leave the ten parts. What the floor finds in song 55 is what 749.104 and 749.106 address.
**Check.** After 749.104 and 749.106, read again how many builds the floor passes over in song 55. Fewer is the sign they worked.

### 749.108 Let the steps follow the aimed song
**Problem.** 927 weights a step 1.2 and a leap of a fourth or more 1.6 in every song. The aim's tilt (920) is there, but a narrow register pushes steps up by itself, so the songs' steps do not follow their aims. Leaps follow in order but overshoot in songs 55 and 54.
**Evidence.** Every living build's median against the aimed song (`studies/review19/aimpool.py`):

| | 55 | 54 | 58 |
|---|---|---|---|
| Moves by step: builds, aim | 0.397, 0.452 | 0.459, 0.595 | 0.471, 0.398 |
| Moves by leap: builds, aim | 0.159, 0.111 | 0.138, 0.120 | 0.052, 0.057 |
| Range: builds, aim | 16, 19 | 14, 14 | 10, 9 |

Song 58, aimed at the fewest steps, steps most.
**Fix.** Fit the step and leap weights per song, as 885 fitted the words' weights: a few short trial runs (200 builds), scaling each until the builds' median meets the aim. Range already follows, through 927.
**Check.** In each song, the builds' median step and leap shares within a quarter of the kept middle half's width of the aim. Across the three songs, the builds' order on steps follows their aims' order.

### 749.109 Let the repeats and the rhythm follow the aimed song
**Problem.** The aim reaches range, runs and repeated notes. It does not reach how often bars are sung again, how many different rhythms a song uses, or rhythm scaling. These sit where the words and the rhythm draw put them, whatever the aim. Song 58 aims at a kept song whose bars repeat more than nine kept songs in ten, and repeats them less than nine in ten. The paper's sentence that song 58 "now sounds like it" is true of its range and runs and the reverse of its repetition and rhythm.
**Evidence.** Song 58's pick against Bird Dog: bars on a figure already sung 0.184 (0.698), on a rhythm already sung 0.282 (0.774), distinct rhythms over bars 0.718 (0.226), all three beyond the kept 10th to 90th on the far side from Bird Dog; rhythm scaling 0.563 (0.704); pitch scaling 0.656 (0.906). Every living build's median: 0.28, 0.41, 0.59; rhythm scaling 0.571. Song 54 misses its aim the same way on rhythm (bars on a rhythm already sung 0.534 against 0.775; distinct rhythms 0.466 against 0.225). Song 55 sits near its aim. Rhythm scaling across the three: 0.587, 0.582, 0.571 against aims of 0.684, 0.403, 0.704.
**Fix.** This is the next step 749.103 names. With 749.106 in (so the run gate stops removing the copies), try `AIM_REPEATS` again: the figure borrow and the rhythm borrow set from the aimed song. Read rhythm scaling against each song's aim, not the kept median. Bird Dog repeats much and its rhythm scaling is high, so kept songs show that the two can go together. Correct the sentence in the paper.
**Check.** In each song, the builds' medians on bars on a figure already sung, bars on a rhythm already sung and distinct rhythms over bars on the aim's side of the kept median, and within half the kept middle half's width of the aim. The rule still holds on the pools.

## Small things
- **One record, two readings.** `page_gate.builds_figures_again_quartiles` is read as sung. `every_build_figures_again_quartiles` and `every_build_first_120_…` are read before melismas. In song 58 their medians are 0.504 and 0.630, which looks like a gate passing over repetition but is partly the reading. Read all of them as sung, or label which is which.
- **The 749.104 study.** `where.py` reads 167 kept tunes (`min_notes=100`) where `soundness.py` reads 160, and `pool.py` reads builds before melismas while the kept tunes carry theirs. Neither changes the finding, which is the right one.

## Carried
- **749.103** Variety counted on both sides: 1.18 against the kept 10.5 (0.77 under v31); pooled width 0.47 against the 0.75 asked. 749.108 and 749.109 are its next steps.
- **749.104** The near repeat: the study is done and its finding stands; the fix waits on 749.106, which stops removing it.
- **749.101** Varied returns at the kept share (goes with 749.104).
- **749.61** 6/8: song 52, no kept 6/8 table.

## Order of work
1. 749.105 (the fault). 2. 749.106 (it frees the repeats the others need). 3. 749.109 with 749.104 and 749.101. 4. 749.108. 5. Reread 749.103 and 749.107. Rerun `neighbour.py` and `studies/review19/` after each; the rule must hold throughout.

## Songs

| Song | Folder | Under v32 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 337 s; key E; aimed at Bird Dog; range 10; a four-bar turn; tenth edition rebuilt from this record |
| 55, Your Yard Man | p65 | 244 s; key A; aimed at Don't Ask Me Why; range 14 (aim 19); the floor passes over 7 of 44 |
| 54, The Man Mama Prayed I'd Be | p64 | 307 s; key E; aimed at Could I Have This Dance; run cap 3; 22 builds past the words' gate |
| 53, Sung to Sleep | p63 | cannot be built (749.105) |
| 52, The Room Next Door | p62 | no aim; melody unchanged |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, the seven kept tables, `studies/soundness/soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones. `spec53.run.json` must be remade, not left standing.
