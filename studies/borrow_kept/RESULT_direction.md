# What makes the pair's tunes hold their direction: the result (749.218)

26 November 2026. Rule in `PREDICTION_direction.md`, written first, under the stopping rule agreed on the thread. `direction_read.py`, `direction_kept.json`, `direction_builds.json` (300 builds a song; v50 records' specs and the pair's refitted specs).

**Nothing is named. Inside a line the pair does not hold its direction more than kept songs; if anything the engine, v50 and the pair alike, holds it less. By the stopping rule, this line closes for the version.**

| Inside a line, builds' middle | kept (25th, 50th, 75th) | 55 | 54 | 59 | 58 | 49 | 50 |
|---|---|---|---|---|---|---|---|
| a. Turns after a leap, v50 | 0.35, 0.56, 0.72 | 0.50 | 0.52 | 0.52 | 0.54 | 0.55 | 0.56 |
| the pair | | 0.50 | 0.54 | 0.54 | 0.58 | 0.64 | 0.57 |
| b. Turns after two steps one way, v50 | 0.24, 0.38, 0.59 | 0.52 | 0.53 | 0.44 | 0.60 | 0.60 | 0.46 |
| the pair | | 0.47 | 0.50 | 0.50 | 0.54 | 0.62 | 0.54 |
| c. Turns after three or more one way, v50 | 0.38, 0.55, 0.66 | 0.54 | 0.52 | 0.65 | 0.45 | 0.35 | 0.46 |
| the pair | | 0.50 | 0.59 | 0.63 | 0.51 | 0.50 | 0.56 |
| d. Moves toward the line's middle from a fourth off, v50 | 0.57, 0.70, 0.83 | 0.87 | 0.84 | 0.71 | 0.83 | 0.90 | 0.77 |
| the pair | | 0.81 | 0.77 | 0.75 | 0.76 | 0.83 | 0.80 |
| e. A line's travel, first note to last, mean semitones, v50 | 2.9, 3.7, 4.8 | 2.7 | 3.1 | 3.1 | 3.1 | 2.8 | 2.7 |
| the pair | | 3.2 | 3.3 | 3.6 | 3.5 | 3.4 | 3.3 |
| e. Longest run of moves one way in a line, v50 | 1.98, 2.32, 2.71 | 1.59 | 1.72 | 1.79 | 1.74 | 1.80 | 1.66 |
| the pair | | 1.59 | 1.88 | 1.85 | 1.75 | 1.86 | 1.82 |

- **a, b, c:** the pair turns as often as kept songs after a leap and after runs one way, inside the kept middle half everywhere (b sits at the turning side of it). Not named.
- **d:** the pair goes back toward a line's middle as often as kept songs or more. Not named.
- **e:** a line's travel is inside the kept middle half and under the kept middle; the longest run one way is **under the kept 25th in every song, under v50 and the pair alike**: the engine's lines change direction more than kept lines, not less. A standing thing, the opposite of what was looked for.

**What I had wrong.** I expected that with the on-beat snap to the chord gone, a line would run on one way. It does not. The songwriting session's picture (no turn after a leap) is not borne out either.

**What is left standing, as description only.** Inside a line the pair is as kept or more broken; the lines sit further apart than the kept middle (between-line spread 2.1 to 2.3 against 1.54, 749.213); the joins are small (749.215). A tune of lines that each stay near their own height, at heights further apart than kept, would be steeper at the scale of one to two lines without any line holding its direction. That is consistent with every reading here and was not tested; the one test of line heights today (749.214, B and C) did not name it. It is noted for whoever takes this up in a later version.

**The line is closed for this version.** The pair (`LUTHIER_BORROW_KEPT=count_true`, `LUTHIER_CHORD_TIE=1`) and the join (`LUTHIER_JOIN_MOVES=1`) stay as switches, off, with their findings. v50 is the engine.
