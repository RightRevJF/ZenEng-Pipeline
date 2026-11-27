# Deducing a missing cell, step 2: result (27 Nov 2026). The method passes its check. The pop 3/4 stress table is deduced and labelled so.

Rule and bar: `PREDICTION_deduce.md` (commit 5cd85c3, before anything was computed). Figures: `deduce_check.json` (`python3 studies/other_metres/deduce_check.py`), `trial_tables/3-4_pop_sung.stress.json` (`deduce_stress.py`).

## The check: pop 3/4 = standard 3/4 × (pop 4/4 ÷ standard 4/4), against the counted pop 3/4 table
Songs: standard 3/4 538, standard 4/4 3,076 (lead sheets); pop 4/4 9,913, pop 3/4 267 (Hooktheory, outside the filter).

| figure | standard 3/4 | style factor in 4/4 | **predicted pop 3/4** | counted pop 3/4: median (middle half) | inside | sign | error over width |
|---|---|---|---|---|---|---|---|
| Notes a bar | 2.33 | ×1.38 | **3.23** | 2.94 (2.38 to 3.85) | yes | right | 0.20 |
| Onsets on a beat | 0.836 | ×0.69 | **0.576** | 0.643 (0.508 to 0.800) | yes | right | 0.23 |
| Onsets on the first beat | 0.379 | ×0.57 | **0.218** | 0.282 (0.214 to 0.364) | yes, by 0.004 | right | 0.43 |
| Bars on a rhythm already sung | 0.846 | ×0.64 | **0.543** | 0.625 (0.465 to 0.787) | yes | right | 0.26 |

**By the bar: all four inside the counted middle half; all four signs right; median error 0.24 of the middle half's width (under 0.5). The method passes.**

What it shows about the assumption: the equation overshoots the style shift every time (it predicts pop 3/4 a little busier, a little less on the beat and a little less repetitive than it is). Style loosens 3/4 somewhat less than it loosens 4/4. The first-beat figure is the weakest, inside by 0.004. So a deduced figure should be read as leaning too far toward pop, by about a quarter of a middle half.

Beside it, deciding nothing: with the kept Billboard songs as the pop 4/4 cell the predictions are 2.84, 0.562, 0.210 and 0.767; the first three agree with Hooktheory's, and the last differs because whole songs repeat more than sections, which is why the rule named Hooktheory.

## The deduced cell: where stressed syllables fall in pop 3/4
The same equation on the stress tables (standard 3/4 and 4/4 from the lead sheets' words; pop 4/4 from the kept Billboard songs' words), share by share, renormalised within a weight:

| stressed syllables | first beat | another beat | off the beat |
|---|---|---|---|
| Standard 3/4 (counted) | 0.652 | 0.277 | 0.072 |
| Standard 4/4 (counted) | 0.355 | 0.440 | 0.205 |
| Pop 4/4 (counted) | 0.204 | 0.352 | 0.444 |
| **Pop 3/4 (deduced)** | **0.50** | **0.29** | **0.21** |

Unstressed, pop 3/4 deduced: 0.09, 0.45, 0.46 (standard 3/4: 0.14, 0.59, 0.28).

So in a pop song in three, half the stressed syllables fall on the first beat where a standard waltz has two thirds, and a fifth fall off the beat where a waltz has one in fourteen. By the check above this probably leans a little too far from the waltz.

The table file is labelled DEDUCED with its inputs, replaces the borrowed one for pop-style lyrics, and is to be replaced in turn when pop songs in 3/4 with words are counted.

## What I expected
Signs right in all four, rhythm again the doubt; three chances in five. It passed; the weak figure was the first beat, not the repetition.
