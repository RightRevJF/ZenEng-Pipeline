# Review 27: how tightly may the choice follow the range the words ask?

`spread.py` holds each of the 160 kept songs out by artist (the study's own GroupKFold, 5 folds), predicts its range from its words, and compares the sung range with the prediction.

- Held-out error: sd 4.99 semitones; absolute error quartiles 1.3, 3.5, 5.8 (90th 8.1).
- Kept songs within 2 semitones of their own asking: 35 in 100 (within 3: 44; within 4: 58).
- Range less the asking, kept 10th, 25th, 50th, 75th, 90th: -6.5, -3.36, -0.3, +3.58, +7.0.
- Luthier's chosen tunes, range less the asking (songs 55, 54, 58, 60, 59): 872 alone -1, -4.8, -8.9, 0, +0.2 (mean -2.9, sd 3.5); with 951 -1, -1.8, -0.9, 0, +0.2 (mean -0.7, sd 0.73).

## The floor trial

One line of `metre_engine.py` changed in a separate worktree (not committed): among the builds past every gate, the first in the order built whose range is at least the asking less 3.36 (the kept 25th of range less the asking); where none is, the nearest. Songs 54, 58 and 55 rerun at their usual seeds.

| Song | Asking | 872 alone | 951 | Floor | Words' fit: 872, 951, floor |
|---|---|---|---|---|---|
| 54 | 18.8 | 14 | 17 | 16 | 0.282, 0.163, 0.275 |
| 58 | 19.9 | 11 | 19 | 19 | -, 0.361, 0.361 |
| 55 | 18.0 | 17 | 17 | 17 | 0.341, 0.341, 0.341 |

Soundness on songs 55, 54 and 58 with the floor: sound; one lean beyond the quartiles (rhythm scaling, low), as under 951; checks outside the middle half in all three songs 11 (951: 15); song 54 alone 4 outside the middle half (951: 8).
