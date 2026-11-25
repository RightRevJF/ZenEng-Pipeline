# The maintainer's line test (studies/lyric_lines on luthier-v8-stage1 at add5ae8): checked by the songwriting session

25 November 2026. Not merged here: the branch is the maintainer's to merge once the writer says so.

## Reproduced
- The rule (PREDICTION.md, 325ce68, 10:53) is committed before the result (add5ae8, 11:10), and the result follows it as written: Holm over six, both halves, the reversal rule uncorrected.
- `check_rhyme.py` on CoCoPops's 214 Billboard files: byte for byte (201 songs, 5,497 line ends, precision 0.746, recall 0.739, F1 0.742).
- `build.py` over WASABI's 2,079,510 songs (read here from a raw stream of the zip member, not the zip): 59,445 rows, 689 listed, as the maintainer's. `analyze.py`: 356 artists, 672 listed, every coefficient, p and half to the third decimal; 50,831 songs where the maintainer's has 50,834 (three rows fewer after the filter; not traced; no verdict moves).

## One check added, after seeing the result (a reading, not a test)
The leads say listed songs have more lines that return (repeat_share +0.20), likely because famous songs are typed out in full. `you_lines` counts every line, returns included, so it could carry that habit. Read again on first-sung lines only, and with repeat_share as a covariate:

| Reading | Per SD | p | Halves (p) |
|---|---|---|---|
| `you_lines`, as tested | -0.125 | .004 | -0.164 (.005), -0.076 (.24) |
| `you_lines`, with repeat_share | -0.125 | .004 | |
| "you" lines among first-sung lines only | -0.104 | .017 | -0.135 (.02), -0.064 (.33) |
| the same, with repeat_share | -0.109 | .012 | |
| "I" plus "you" among first-sung lines | +0.065 | .13 | +0.04, +0.10 |

The reversal is not the transcription habit: it holds on first-sung lines and with repeats held constant. It is modest (25 against 28 lines in 100) and carried more by one half than the other.

## Verdict
The test is sound and its verdicts stand: nothing passes; `you_lines` reversed. The caution written into `lib/luthier/lyric_people.py` is right. One more it could carry: `feel_late` and `end_weight` found nothing, so "a feeling named late" and "weight at the stanza's end" are advice from chills research only.
