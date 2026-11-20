# The bar fit: results

Two trials outside the engine, each with its rule written first (PREDICTION.md, PREDICTION2.md). 150 tries a song. Song 59 is the hold-out: read, not counted.

## Trial 1: keep the source's bars when a line returns. Not built.

Read before melismas; the engine's refit, then the bar fit.

| | Song 55 | Song 54 | Song 58 | Song 59 |
|---|---|---|---|---|
| Bars on a figure already sung (aim) | 0.461, 0.474 (0.453) | 0.553, 0.596 (0.525) | 0.481, 0.541 (0.698) | 0.452, 0.511 (0.320) |
| Bars on a rhythm already sung (aim) | 0.593, 0.630 (0.528) | 0.670, 0.733 (0.775) | 0.617, 0.699 (0.774) | 0.614, 0.663 (0.495) |
| Returning lines' repeats over fresh lines' | 0.118, 0.051 | 0.045, 0.028 | -0.060, -0.111 | 0.060, 0.051 |
| Stressed syllables on a beat | 0.572, 0.551 | 0.526, 0.472 | 0.637, 0.562 | 0.626, 0.581 |
| The words' fit, whole (kept 10th 0.152) | 0.269, 0.101 | 0.263, 0.106 | 0.307, 0.086 | 0.298, 0.162 |

- Check 1 (bars move toward the aim): **fails.** The bars do return (rhythm up 0.04 to 0.08 everywhere), but read before melismas songs 55 and 54 were already at or over their aims, so more is the wrong way for them.
- Check 2 (no extra repeats): **fails by a little.** Song 55's returning lines are 0.051 over its fresh lines (0.118 before; 0.03 asked). Song 54 meets it.
- Check 3 (the words still sit): passes as written. But the rule missed the real cost: **the words' fit falls under the kept 10th in every song.**

**What it shows.** The bars and the words trade against each other. The engine's refit moves notes to put the new words' stresses where kept songs sing them; keeping the bars undoes that. A kept song has both because its later verses are written to the first verse's stresses. That points at the lyric, not the tune.

## Trial 2: a line sung again takes its source's melismas. Passes; built as 942.

Read as sung on the same builds; melismas as the engine places them, then carried.

| | Song 55 | Song 54 | Song 58 | Song 59 |
|---|---|---|---|---|
| Bars on a figure already sung | 0.318, 0.337 | 0.473, 0.500 | 0.472, 0.474 | 0.366, 0.403 |
| Bars on a rhythm already sung | 0.435, 0.459 | 0.596, 0.619 | 0.606, 0.611 | 0.523, 0.523 |
| The words' fit, whole | 0.224, 0.233 | 0.244, 0.250 | 0.303, 0.303 | 0.266, 0.274 |

Both checks hold. The gain is small (two to three hundredths) and costs nothing. On the hold-out it moves bars on a figure already sung away from its aim (0.320).
