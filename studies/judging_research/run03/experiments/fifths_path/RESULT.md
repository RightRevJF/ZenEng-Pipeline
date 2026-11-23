# Steps around the circle of fifths: result

Run 03, 23 November 2026. Rule frozen before any outcome was opened (`PREDICTION.md`, commit 09ce7bd). `test.py` ran it once, as written; numbers in `result.json`.

## What was predicted
Each chord gets a place on the circle of fifths (C, G, D, A, …). A song is a path around it, and **FP** is the average step size. The guess: among one artist's own songs, **smaller, plainer steps go with more covers**, at **−0.02 SD** of log covers per SD of FP, holding chord repetition and chord surprise. Six tests ran tonight, so a pass needed p < .0083.

## Worked example (computed by the script)
Steps are in radians; 0.524 is one notch on the circle, as in C to G.

| Loop | Steps (the last wraps to the start) | FP |
|---|---|---|
| I–V–vi–IV | I→V 0.524, V→vi 0, vi→IV 1.047, IV→I 0.524 | **0.524** |
| I–IV–V | I→IV 0.524, IV→V 1.047, V→I 0.524 | **0.698** |

The famous four-chord loop steps more gently than the three-chord one. V and vi sit at the same place, so that move counts as no step.

## Gate (before any outcome was read): **passed**
- **Two clips of a song agree:** Spearman **0.356**, 1,281 songs (needs ≥ 0.20; chair 0.356).
- **Overlap with other measures:** largest **+0.22**, chord surprise (needs ≤ 0.7; chair +0.22).
- **Checks:** all twelve unit values reproduced; V7 shares I's phase; augmented and diminished-seventh chords have no phase. FP percentiles 0.428 / 0.663 / 1.047 match the chair. No song undefined; 406 of 60,579 moves skipped for no phase (chair 426 of 68,314: the totals differ, the spread matches exactly).

## What came out

| | Songs | Artists | Estimate | SE | p |
|---|---|---|---|---|---|
| **All (decides)** | 1,924 | 420 | **−0.017** | 0.018 | 0.36 |
| Half 0 | 932 | 205 | −0.011 | 0.024 | 0.64 |
| Half 1 | 992 | 215 | −0.021 | 0.029 | 0.47 |

Printed before the estimate: **SE 0.018** (chair ~0.016), **power 0.06** (chair ~0.08).

## Verdict: **unsettled**
The estimate leans the predicted way and both halves agree, but p = 0.36 is far from .0083. It is not a kill, because −0.017 is below −0.01. The 95% range (−0.052 to +0.019) holds both zero and the predicted −0.02.

**How firm:** very weak. At power 0.06, a true effect of the predicted size would pass about 6 times in 100. "Unsettled" here means "not shown either way."

## Reported, deciding nothing

| Reading | Estimate | p |
|---|---|---|
| Covers within 5 years | −0.004 | 0.89 |
| Covers after 10 years | −0.021 | 0.18 |
| Without chord surprise | −0.028 | 0.13 |

Without chord surprise the estimate is more negative, as expected if the two share some plainness. 11.3% of kept moves are zero steps.

## What it cannot say
The circle places chords, not their job in the key, so V7→I counts as no step. A null clears nothing at this power. The rule was written after two other results, so a pass would only have been a lead. Not causal; hits only; the McGill hold-out was not touched.

## Ideas for later (not tried)
Weight each step by how long its chords last, or add the thirds circle (f3). Each needs its own frozen rule and fresh songs.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022). CC BY-NC-SA 3.0.
- **Covers and versions:** Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024). CC BY-SA 4.0.
