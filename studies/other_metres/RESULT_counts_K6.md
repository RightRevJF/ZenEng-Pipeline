# Three counts on rhythm sung again (K6): the result

28 November 2026. Rule file first: PREDICTION_counts_K6.md (6b9d725). Every figure is printed from RESULT_counts_K6.json by the command that wrote this page. Pop 3/4, song 55's words, seeds 4, 5, 6. No engine or planner change.

## Count 1: K6 at each gate in turn
| Tonight's package: builds; meeting K6's rhythm line, in 100; meeting all six | Seed 4 | Seed 5 | Seed 6 |
|---|---|---|---|
| Living | 631; 72.3; 69.9 | 827; 80.5; 80.4 | 601; 76.5; 74.9 |
| Removed by the old charge | 315; 78.4; 75.6 | 413; 83.8; 83.5 | 300; 79.3; 77.7 |
| Past the old charge | 316; 66.1; 64.2 | 414; 77.3; 77.3 | 301; 73.8; 72.1 |
| Past the joint gate | 316; 66.1; 64.2 | 414; 77.3; 77.3 | 301; 73.8; 72.1 |
| Past 956's ceiling (the pool) | 210; 64.3; 63.3 | 146; 76.7; 76.7 | 256; 75.8; 74.2 |

## Count 2: is it old?
| The pool meeting K6's rhythm line; all six, in 100 (pool's median of rhythm again) | Seed 4 | Seed 5 | Seed 6 |
|---|---|---|---|
| Before tonight (RESULT_pop_3_4_b's package) | 49.0; 44.9 (0.348) | 45.0; 37.7 (0.348) | 45.5; 41.7 (0.348) |
| Arm 1 (749.251, 749.253) | 50.0; 46.4 (0.347) | 45.9; 44.7 (0.333) | 54.6; 52.5 (0.35) |
| Tonight's package (with 749.252, 749.254, 749.255) | 64.3; 63.3 (0.35) | 76.7; 76.7 (0.381) | 75.8; 74.2 (0.381) |
| The old charge's cost before tonight: removed half; kept half meeting the line | 68.9; 49.0 | 57.8; 45.0 | 61.5; 45.5 |

## Count 3: a unit taking an earlier unit's rhythm
| Two-bar units taking the rhythm of an earlier unit exactly | Two back | One back |
|---|---|---|
| Pop 3/4 clips (446 clips of six bars or more), all units | 0.231 | 0.156 |
| The same, by clip: 10th, 25th, 50th, 75th, 90th | [0.0, 0.0, 0.125, 0.5, 0.8] | [0.0, 0.0, 0.0, 0.25, 0.667] |
| The engine's pool, tonight's package, seeds 4, 5, 6 | [0.014, 0.012, 0.012] | [0.003, 0.002, 0.002] |
| The engine's pool before tonight | [0.029, 0.019, 0.025] | |

## Plainly
- **Count 1: the old charge is the step that thins the repeats, at every seed.** The half it removes meets K6's rhythm line in 78.4, 83.8 and 79.3 in 100; the half it keeps in 66.1, 77.3 and 73.8. The joint gate removes no build at any seed. The ceiling changes it by two in 100 or less either way. Had the pool been the living builds, the six would stand at 69.9, 80.4 and 74.9: still under 76.2 at seeds 4 and 6. So the old charge is a cost, and not the whole shortfall.
- **Count 2: it is old, and tonight's forms made it better, not worse.** Before tonight the pool met all six in 44.9, 37.7 and 41.7 in 100 at these seeds; with arm 1, 46.4, 44.7, 52.5; with the source forms and the ceiling, 63.3, 76.7, 74.2. The source forms (749.252, 749.254) are where it rose: a line drawn for all the words it will carry is sung again more nearly as it was.
- **Count 3: the engine hardly ever sings a two-bar rhythm again exactly, and pop does it about one time in four.** In the pop clips a two-bar unit takes the exact rhythm of the unit two before in 0.231 of cases (one before: 0.156); in the engine's pool, 0.014, 0.012 and 0.012. 818 fires at 0.8, but what it gives is the earlier line's notes refitted to new words, which is rarely the same rhythm: the count of syllables differs and the refit moves notes. So the engine's "0.8" and the clips' 0.23 are not the same kind of number, as I feared, and on the like-for-like measure the engine is far **under** pop, not over. The clips vary widely (by clip, the 10th and 25th are 0 and the 90th 0.8).
- What I have not counted: what the old charge is made of outside 4/4 (which readings it charges, against whose figures). If it charges repetition against a 4/4 song's targets, your "4/4-fitted gate judging a 3/4 song" is right; I would read that from the code and the record before saying so.
- All counts by the planner's own run; tonight's-package runs give their records' picks and the record's own step counts. No engine or planner change.

## My expectation, against the result
- Count 1, "the old charge thins the repeats by 5 to 15 in 100; the other gates change little": right (6.2, 3.2, 2.7 from living to kept; seeds 5 and 6 a little under my range).
- Count 2, "it is old; the source forms are not the cause": right, and more: they are the cure so far.
- Count 3, "the clips 25 to 45 in 100; the engine near the clips' median or under": the clips are 0.231 (just under my range); the engine is far under, about one in a hundred. I did not expect a gap that wide.
