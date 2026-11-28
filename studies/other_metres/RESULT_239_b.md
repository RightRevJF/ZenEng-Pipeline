# 749.239, the second equation (bars as words): the held-out check. Essen 6/8 MISSED narrowly, at the thin edges; pop 3/4 MISSED in the middle. Not used in either table as the rule stands.

27 November 2026, 19:27 ET. Rule: PREDICTION_239_b.md (commit 396bbaa, before any code). Code: grammar_b.py (a study file; no engine code). Figures printed from grammar_b_essen68.json and grammar_b_pop34.json by the command that wrote this file.

## Essen 6/8, two-bar cells (deciding)
(a) 11 of 12: met. (b) 9 of 12: **missed**. (c) 9 of 12: **missed**.

| Notes in two bars | Windows | Averages inside | Counted carry | Top five shared |
|---|---|---|---|---|
| 3 | 28 | **no** | **0.436** | **2** |
| 4 | 39 | yes | 0.651 | 3 |
| 5 | 238 | yes | 0.672 | 4 |
| 6 | 589 | yes | 0.755 | 4 |
| 7 | 915 | yes | 0.758 | 3 |
| 8 | 1198 | yes | 0.837 | 4 |
| 9 | 860 | yes | 0.82 | 4 |
| 10 | 679 | yes | 0.865 | 4 |
| 11 | 374 | yes | 0.766 | 4 |
| 12 | 180 | yes | 0.633 | **2** |
| 13 | 55 | yes | **0.245** | 3 |
| 14 | 22 | yes | **0.025** | **0** |

- Against the first equation: (b) from 0 cells of 12 to 9; (c) from 0 to 9.
- **In the cells from 5 to 12 notes, the ones lines use, (b) holds in 8 of 8 and (c) in 7 of 8.** The misses are cells 3, 13 and 14 on (b), and 3, 12 and 14 on (c).
- **By the rule as written it is a miss:** (b) asks every cell, (c) asks 8 in 10 and has 9 in 12.
- Three bars, reported: (a) 10, (b) 0, (c) 4 of 13 cells. The chain is weaker than the pair: the counted windows carry 0.25 to 0.46 in the busy cells.

## Hooktheory pop 3/4, two-bar cells (deciding)
(a) 9 of 11: **missed**. (b) 4 of 11: **missed**. (c) 4 of 11: **missed**.

| Notes in two bars | Windows | Averages inside | Counted carry | Top five shared |
|---|---|---|---|---|
| 2 | 175 | **no** | 0.833 | 3 |
| 3 | 209 | yes | 0.777 | 3 |
| 4 | 497 | yes | 0.713 | 4 |
| 5 | 521 | yes | **0.567** | **2** |
| 6 | 542 | yes | **0.551** | 4 |
| 7 | 334 | yes | **0.39** | **0** |
| 8 | 276 | yes | **0.324** | **0** |
| 9 | 118 | yes | **0.314** | **1** |
| 10 | 96 | **no** | **0.28** | **1** |
| 11 | 30 | yes | **0.34** | **2** |
| 12 | 170 | yes | 0.803 | **2** |

- The miss is in the middle (7 to 11 notes), where the counted windows carry about a third. Not a thin-cell matter.
- Three bars, reported: (a) 12, (b) 1, (c) 5 of 14 cells.

## Fitted parts (in the files): the repeat share R by the first bar's note count
- Essen 6/8: {"1": 0.0025, "2": 0.0229, "3": 0.0462, "4": 0.2601, "5": 0.0783, "6": 0.0667, "7": 0.0, "8": 0.087, "9": 0.0}.
- Pop 3/4: {"1": 0.2332, "2": 0.196, "3": 0.1864, "4": 0.1968, "5": 0.2339, "6": 0.5621, "7": 0.0909, "8": 0.0, "9": 0.0, "10": 0.0, "11": 0.0, "12": 0.8734}. Pop repeats its bar about one time in five; Essen seldom. That difference is the style, counted.

## Uncounted bars
The share held for bars never counted (U), from the files: in Essen 0.002 to 0.012 for bars of one to six notes, 0.066 at seven, 0.26 at eight (23 bars counted). In pop 0.004 to 0.07 for one to four notes, 0.15 at five, 0.22 at seven. The one-bar place form, on what it is used for: of its chance on uncounted bars, the held-out half's new bars carry between nothing and 0.45 by count. It is a weak guide to new bars. Where U is small it matters little; in the dense bars, where lines fail to fit, it would matter.

## My expectation
Essen: I gave one chance in three for all three, two in three for the cells from 5 to 12. (b) holds in all of 5 to 12; (c) misses once there (cell 12). Pop: one in five; it missed.

## What follows, by the rule
- **Essen:** the miss is at the edges, so by the rule file this is a question for the songwriting session, not a new equation: whether the deciding cells should be those with enough windows to judge and that lines use, set before the next run, or whether the bar stands and the equation must reach the edges too. I do not move the bar.
- **Pop:** the equation lacks something real. Next: the pair itself (a bar's chance given the very bar before it, where that pair is counted, falling back to this equation where it is not), and the song's own repeating: pop repeats bars across a phrase (A B A B), which a first-order chain cannot see.
