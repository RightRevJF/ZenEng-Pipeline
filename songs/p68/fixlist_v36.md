# Luthier list for v36 (since v35)

20 November 2026. Luthier v35 (fixes 934–936) is reviewed (`lib/luthier/REVIEW_stage21.md`) and merged into main at 78f8ee4. Every kept table, all five song records (52, 54, 55, 58, 59), song 53's run, `soundness.json` and `neighbour_v35.json` reproduce. 934 holds. 935 mends song 59's rhythm deaths (500 to 52). 936 meets its check in two songs of four. Song 58 is rebuilt from its v35 record (twelfth edition, A major; 44 of 44 document checks pass). Three new items (749.117 to 749.119). Next finding 749.120; next fix 937.

## The two questions, in short

1. **936 is not the cause; it lowers the failures.** The 2.5 in 100 is the neighbour choice. A random pick from the engine's pool fails 2.6 in 100 (2.5 in v34), and the papers have used the wrong label since v32 (749.117). With 936 taken out of v35, the neighbour choice fails 4.8 in 100 and a random pool pick 5.4. The rise came with 934 and 935; 935 acts in every build of songs 55 and 54, not only song 59 (749.119).
2. **Song 59 at 2 of 21 is a step the wrong way.** It is now more central than every one of the 147 kept songs. Two Hearts sits near the kept middle, so closing on it moves the song inward, and the checks the aim does not set stay in the middle anyway. That is 749.103, now shown on the hold-out.

## Items

### 749.117 Label the two pool figures rightly
**Problem.** Since v32 the papers' "a random pool pick fails the rule" has been the neighbour choice's figure from `neighbour.py` (the pool build nearest a randomly drawn kept song). The random pick from the engine's pool, which 749.96's standard asks for, is a separate figure.
**Evidence.** `neighbour_vNN.json`, `neighbour.rule_fails_share` against `a_random_pick_from["the engine's pool …"].rule_fails_share`. v32: 1.0 against 4.6 in 100; v33: 0.3 against 2.6; v34: 0.5 against 2.5; v35: 2.5 against 2.6. The papers quoted the first under the second's name. Both meet 749.96's bar (90 in 100).
**Fix.** Report both, each under its own name, in the paper and the README, and correct the v32 to v35 rows.
**Check.** Every pool figure in the paper matches its key in `neighbour_vNN.json`.

### 749.118 Let the repeat weight reach the lines that return, and let the fit go forward again
**Problem.** 936's weight acts where a fresh line is drawn. A line that returns refits its source to new words, and the refit sets a split note or a lead-in to the same pitch at fixed shares the weight never reaches. So in the songs aimed low on repeats (55, 54), the returning lines hold the whole song's repeats up. Second, after a round leaves the kept band, the fit steps halfway back toward the last round inside the band. Every later round outside does the same, so the fit walks back to its start.
**Evidence.** Builds' repeated notes against the aim: 0.222 against 0.158 (55), 0.215 against 0.110 (54); a quarter of the kept width is 0.045. `studies/v35_traces/trace.json` after the fix: repeats in fresh lines 0.17 and 0.179, in returning lines 0.289 and 0.247 (55, 54). `Engine.again`: a split note takes the pitch before it 4 times in 10, and a lead-in is level 32 times in 100. Song 54's `moves_fit`: round 2 met the aim (repeats 0.152, steps 0.592) with its fresh lines outside the band. Rounds 3 to 6 went halfway back toward round 1 each time, and the kept round (6: repeat 0.92, step 1.268) is nearly round 1.
**Fix.** (a) Draw a refitted line's new pitch (a split note, a lead-in) through the same move weights as a fresh note, or scale its fixed repeat shares by the repeat weight. (b) Make the fit a bisection: after a round back inside the band, move forward again toward the aim, and keep the best inside round. Song 54's repeat aim (0.110) is under the kept 10th (0.157); the bound will stop it short of the aim, and that is right.
**Check.** In songs 55 and 54, returning lines' repeated notes no more than 0.03 over the fresh lines'. Song 55's builds within a quarter of the kept width of its aim; song 54's at or under the kept 25th. Songs 58 and 59 stay within a quarter width.

### 749.119 Measure 934 and 935 apart, and narrow 935 to its case
**Problem.** 935 was made for one line in song 59. It acts in every build of songs 55 and 54 as well, and it is gated on the song having an aim, which a rhythm rule should not depend on. The pools' failure rates rose with 934 and 935 together, and which of them did it is not measured.
**Evidence.** The records' stats: "935: a line gives way to a short line before a copy" 1,000 in 1,000 builds for songs 55, 54 and 59, none for 58. `studies/review21/`: with 936 taken out of v35, the neighbour choice fails 4.8 in 100 and a random pool pick 5.4 (v34: 0.5 and 2.5).
**Fix.** Two trials through `neighbour.py`: v35 with 935 off, and v35 with v34's fit sizes (934 off). Find which one moves the rates. If 935 costs elsewhere, narrow it to the case the trace found (a line of one bar or less, of few syllables, before a line that comes in early), and take the aim gate off.
**Check.** With 935 kept, the random pool pick fails no more than in v34 (2.5 in 100), and song 59's rhythm deaths stay under 10 in 100.

## Answered
- **934** holds: 40 builds a round; song 59's fit stable across two seeds (0.78, 0.37, 0.231 against 0.72, 0.349, 0.261).
- **935** holds for song 59 (rhythm deaths 500 to 52, survivors 138 to 325). The trace was right where my list was wrong: the long verse lines were not at fault.
- **936**: in two songs of four (749.118).
- **749.111, the second trial:** agreed. Next, plant only where the aim is wider than the kept middle, and keep the peak a step under the voice's top. In song 59, planted near the top, only 11 builds in 100 survived.

## Carried
- **749.116** The band under the break (song 59's break still reads above its last chorus).
- **749.103** Variety. On the hold-out, song 59 is more central than every kept song (2 of 21 outside the middle half; a kept song's median is 10). The checks the aim does not set stay in the middle.
- **749.111** with the next trial's rule as above. Song 58's v35 pick spans 9 semitones and sits on its top note 54 times (Bird Dog twice): the narrow aim's ceiling is worse, not better. **749.104's fix** (with 749.101 and 749.109). **749.61**.

## Order of work
1. 749.117 (the labels). 2. 749.119 (measure, then narrow 935). 3. 749.118. 4. 749.116. 5. 749.111's third trial. After each: `neighbour.py`, `studies/review20/`, `studies/holdout59/` (song 59 read, never fitted to).

## Songs

| Song | Folder | Under v35 |
|---|---|---|
| 59, Before the Bread Goes Cold (hold-out) | p69 | key A; 325 builds survive; 2 checks of 21 outside the kept middle half |
| 58, Same Time Tomorrow | p68 | 337 s; key A; G♯2 to F♯3; twelfth edition from this record |
| 55, Your Yard Man | p65 | repeated notes 0.222 against an aim of 0.158 |
| 54, The Man Mama Prayed I'd Be | p64 | repeated notes 0.215 against 0.110 |
| 53, 52 | p63, p62 | byte for byte |

## Regression line
The records of songs 52, 54, 55, 58 and 59, song 52's and song 53's run files, the seven kept tables, `soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones.
