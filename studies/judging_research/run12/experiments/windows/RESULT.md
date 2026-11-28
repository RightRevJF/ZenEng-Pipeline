# windows: result (uncounted estimate, rank 7)

**Status: ESTIMATE.** It passes and kills nothing (REP power 0.060 at .0167; ch_rep's prediction is 0). Run record: the first run attempt was cut by a 2-minute tool timeout before any result was written; the second, complete run is this result.

## The rule, written first
Δ = β_L − β_E (FE Poisson log-rate per SD, covers at ages 8+ minus ages 0-3, offset from frozen g, h). Printed: whether each prediction lies outside Δ ± 1.96 SE_boot (500-resample paired artist bootstrap). Predictions: REP Δ = −0.02 (Listener); ch_rep Δ = 0 (Inventor). Readings: Inventor's β_L = −0.05; Listener's |β_E| > |β_L| = "exposure, not quality".

## What came out (1,419 songs, 326 artists, t0 ≤ 2005; 7,777 early and 43,270 late covers)
**REP**
- β_E **+0.077** (SE 0.056); β_L **+0.041** (SE 0.049).
- **Δ = −0.036**; SE_boot 0.069 (467 of 500 refits succeeded), range −0.172 to +0.100; analytic SE 0.059 (p .54).
- −0.02 inside; 0 inside; −0.05 inside β_L's range. |β_E| > |β_L| on the points only.
- 1970+: Δ −0.052 (analytic SE 0.070). β_L with log(r + N_E) held: +0.013 (SE 0.035).

**ch_rep**
- β_E **+0.062** (SE 0.073); β_L **−0.180** (SE 0.049).
- **Δ = −0.242. The frozen bootstrap failed**: some resamples returned NaN, so se_boot, lo and hi are NaN. The stored flags `prediction_outside_range: True` and `reading_delta_zero_outside_range: True` come from comparisons with NaN and are **void**.
- The only usable spread is the **analytic joint sandwich SE, 0.072** (p .0007, analytic): on it, 0 lies outside (−0.382 to −0.101). This is not the frozen spread.
- Inventor's β_L −0.05 is outside β_L ± 1.96 SE_L (valid; analytic SE_L).
- 1970+: Δ −0.097 (SE 0.068, p .15); β_L −0.106. β_L with log(r + N_E) held: −0.207 (SE 0.049).

## How firm
REP: nothing. Realised SEs are about three times the simulated 0.022. ch_rep: a large late-window association on the analytic SE, but uncounted, frozen spread unavailable, SEEN songs, and Δ shrinks to −0.097 in the 1970+ reading.

## What it cannot say
It cannot yet separate launch luck from fitness; Lakh pooling is next pass. It is outside the pass's K (3 at freezing; 4 with windows_lakh_after).

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
