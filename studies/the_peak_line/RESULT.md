# The line that carries the top: the reading (the session's 749.191), and what it led to (749.192)

25 November 2026. Rule in `PREDICTION.md` (committed before the run). Numbers: `reading.json`.

## The centre is not the fault

| | Kept songs | Song 55 | Song 54 | Song 58 | Song 49 |
|---|---|---|---|---|---|
| The reach (top less the line's middle), quartiles | 2, 4, 6.5 | 3, 5, 8 | 3, 5, 7 | 3, 7, 12 | 3, 5, 7 |
| The lift (the line's middle over its part's), quartiles | 0, 2, 5 | 0, 2, 5.5 | 0, 3, 6 | 0, 0, 5 | 0, 3, 5 |
| The top note is reached: as the line's first note | 33 in 100 | 21 | 5 | 12 | 7 |
| by a step | 25 | 13 | 15 | 8 | 20 |
| by a skip (3 to 7) | 28 | 41 | 51 | 40 | 38 |
| by a leap (8 to 12) | 11 | 12 | 17 | 16 | 15 |
| **by a leap past an octave** | **3** | **12** | **12** | **23** | **21** |

The rule named the centre only if the builds' middle reach was over the kept 75th and their lift 2 semitones under the kept one, in three songs of four. It holds in one (song 58). **By the rule the centre is not named, and the change I proposed (raise the carrying line's centre) is not tried.** I was wrong: the lines that carry the planted peak sit about as high against their top, and as far above their part, as kept songs' do.

The difference is in the last row, and in the first. Kept songs begin the line on its top a third of the time, or step to it; the engine comes to it from past an octave below four to seven times as often.

## Why the engine draws an interval past an octave at all (749.192)

Reading the draw's code for how such an interval gets its weight:

- The kept interval table counts every interval of an octave **or more** in its +12 and −12 bins (`make_kept_4_4_tables.py`: `max(-12, min(12, d))`).
- The draw weighs each candidate pitch by its interval's bin, and clamps the same way (`ivp`). So **each** pitch an octave or more away is given the whole bin: the octave, the ninth, the tenth, the eleventh, the twelfth, every one at the weight kept songs give to all of them together.
- In kept songs the bins divide like this (`tables/kept_octave_tail.json`): upward, 198 octaves and 126 past it; downward, 121 and 56.

A part's register spans about 19 semitones, so there are usually four or five scale pitches past an octave in reach, and the draw is offered leaps past an octave at several times their kept share. The register's pull hides most of it, since a line keeps near its centre. The planted peak takes that pull away for one line (its top is raised), and the leaps show.

This is not a reading of figures that needs a rule to name it: it is what the code does. It is older than the plant. It explains why the octave gate was needed (749.160), why the plant brought the leaps (749.186), and why no choice among the carrying line's draws could mend it (749.189): the draws were being made with the wrong odds.

## The mend this points to

The bin shared as kept songs share it: the octave takes its kept share of the bin (0.61 up, 0.68 down) and the pitches past it share the rest between them. No gate, no redraw, no change to the plant. Its marks are in `PREDICTION_tail.md`, written before it is run.
