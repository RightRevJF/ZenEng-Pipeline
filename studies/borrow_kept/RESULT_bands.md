# The pitch scaling by bands of scale, and by the line's join: the result (749.215)

26 November 2026. Rule in `PREDICTION_bands.md`, written first. `bands_read.py`, `bands_kept.json`, `bands_builds.json` (300 builds a song; v50 records' specs and the pair's refitted specs).

**Named: the band of 8 to 16 notes, and the join.** Both as expected this time.

| Builds' middle | kept (25th, 50th, 75th) | 55 | 54 | 58 | 49 | 50 | 59 |
|---|---|---|---|---|---|---|---|
| Local slope, 4 to 8 notes, v50 | 1.01, 1.18, 1.29 | 1.02 | 1.03 | 1.12 | 1.05 | 1.06 | 1.09 |
| the pair | | 1.23 | 1.19 | 1.21 | 1.13 | 1.14 | 1.20 |
| **8 to 16 notes**, v50 | 0.82, 0.96, **1.09** | 0.88 | 0.86 | 0.84 | 0.83 | 0.81 | 0.98 |
| the pair | | **1.12** | **1.19** | **1.13** | 1.08 | **1.12** | **1.14** |
| 16 to 32 notes, v50 | 0.62, 0.83, 1.05 | 0.62 | 0.69 | 0.69 | 0.62 | 0.64 | 0.81 |
| the pair | | 1.01 | 1.04 | 1.02 | 0.90 | 0.93 | 1.00 |
| over 32 notes, v50 | 0.50, 0.69, 0.97 | 0.90 | 0.84 | 0.91 | 0.93 | 0.79 | 0.80 |
| the pair | | 0.75 | 0.83 | 0.75 | 0.86 | 0.82 | 0.84 |
| Move inside a line, mean semitones, the pair | 1.54, 1.80, 2.12 | 1.77 | 1.81 | 1.95 | 2.08 | 1.92 | 1.97 |
| **Move across a join**, mean semitones, v50 | **2.67**, 3.41, 4.36 | 3.02 | 2.80 | 2.94 | 2.76 | 2.71 | 2.83 |
| the pair | | **2.41** | **2.37** | **2.58** | **2.55** | **2.29** | **2.24** |
| Across a join, a fourth or more, share, the pair | 0.19, 0.31, 0.44 | 0.18 | 0.16 | 0.18 | 0.18 | 0.16 | 0.14 |
| Across a join, no move, share, the pair | 0.11, 0.21, 0.30 | 0.31 | 0.30 | 0.28 | 0.23 | 0.29 | 0.29 |

- **The band 8 to 16 is over the kept 75th in five songs of six** (song 49 just under). 4 to 8 is inside the kept middle half in all six; 16 to 32 is under the kept 75th in all six, near it in four.
- **The join is named:** the pair's move across a join is under the kept 25th in all six, while the move inside a line is inside the kept middle half in all six. Under the pair a line starts closer to where the last one ended than kept lines do: too often on the very same note, too seldom a fourth or more away.

**Why the pair changed the join.** Under v50 most lines were borrowed, and a borrowed line starts on its source's first note wherever the line before it ended: a jump, by accident of the borrowing. A fresh line's first note is drawn from the last note of the line before by the same odds as any move inside a line. With far fewer borrowed lines, the joins shrank. (`studies/line_joins` found v50's joins near kept; that was the borrow doing the join's work.)

**What follows.** A form: a fresh line's first note drawn by the kept moves across a join, in place of the moves inside a line. Marks first.
