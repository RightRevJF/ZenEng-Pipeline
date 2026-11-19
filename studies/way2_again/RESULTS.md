# Way 2 again, on whole songs the first run had not seen: results (18 November 2026)

Predictions: PREDICTION.md, written first. Code: run.py (way2_again_results.json, way2_again_pooled.json); the graded set is studies/way4/graded.py.
Nothing here is in the engine beyond what Luthier v21 already holds (the exponents as readings of the gate).

Whole songs of 150 notes or more: 203 CoCoPops Billboard (166 among the old kept songs), 187 Rolling Stone (124 with a chart record).
Partial Spearman, holding year and the count of notes.

| | Pitch alpha against weeks | against peak |
|---|---|---|
| The old songs (166) | 0.121 (p 0.12) | 0.103 (p 0.19) |
| NEW songs (147): CoCoPops Billboard not among the old, Rolling Stone with a record not in CoCoPops | 0.161 (p 0.053) | 0.177 (p 0.033) |
| Rolling Stone with a record (124) | 0.224 (p 0.013) | 0.177 (p 0.051) |
| All 313, holding the source too | 0.139 (p 0.014) | 0.137 (p 0.016) |
| All 313, holding also the spread and range of pitch | 0.097 (p 0.089) | 0.113 (p 0.047) |

By thirds of pitch alpha over the 313 (cut at 0.83 and 0.97): songs reaching no. 1: 19, 21 and 38 in a hundred; median peak 8, 8, 5.

| Prediction | Result | Held? |
|---|---|---|
| T1 pitch alpha against weeks shrinks under 0.10 on new songs | 0.161; against peak 0.177 | NO: it did not shrink. I was wrong, as hoped |
| T2 Rolling Stone songs do not differ from CoCoPops Billboard in pitch alpha | AUC 0.511 | yes |
| T3 rhythm alpha relates to no grade | weeks -0.07; peak -0.12 on all, -0.20 on the new songs (p 0.017) | no: a lean the other way against peak |
| T4 nearness to the kept median relates to nothing | old songs 0.13 to 0.21; new songs -0.04 to -0.19 | yes: it flips between sets |
| T5 nothing relates to rank inside the Rolling Stone list past 0.10 | pitch -0.04; rhythm -0.03; nearness in rhythm 0.13 | yes |

By the rule set beforehand a measure works only if (a) it holds on the new songs at 0.10 or more, p under 0.05, in the old direction, and (b) Rolling Stone
songs stand over CoCoPops Billboard on it or it rises with the list's rank. Pitch alpha meets (a) against peak and narrowly misses it against weeks; it
fails (b). So by the rule nothing is built. It is nonetheless the first reading in this work to keep its size and direction on songs it had not seen:
about 0.14, which is two parts in a hundred of how songs fared. Part of it goes with a wider spread of pitch. The thirds are a description made after
the fact. The critics' list does not agree with the charts here: the songs critics chose do not scale higher than the others.
