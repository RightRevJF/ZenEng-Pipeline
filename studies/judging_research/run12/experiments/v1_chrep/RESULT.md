# v1_chrep: result (uncounted estimate, rank 2)

**Status: ESTIMATE.** Power at .0167 was 0.193, under the 0.2 floor, so it passes nothing and kills nothing.

## The rule, written first (as if counted)
- Prediction: β_D = −0.01, D = z(FIT) − z(log1p N), on z(ch_rep), within artist, exact first-year dummies.
- Pass: p < 0.0167, β_D < 0, both halves < 0. Killed: −0.01 outside β̂_D ± 1.96 SE **and** β̂_D ≥ 0. Otherwise unsettled.

## What came out (result.json)
- **β_D = −0.0178, SE 0.0084, p 0.034**; 95% range −0.034 to −0.001. 1,853 rows, 405 artists.
- Halves: −0.025 (SE 0.013, p .046) and −0.013 (SE 0.013, p .32). Both negative.
- Had it been counted: right sign and halves, p above 0.0167, so **unsettled**. Not a kill (β̂ < 0, −0.01 inside the range). With K = 4 after windows_lakh_after (α .0125) the reading would still be unsettled.

## Readings (uncounted)
- β on z(FIT): **−0.090** (SE 0.033, p .006).
- β on z(log1p N): **−0.072** (SE 0.026, p .005).
- D with five-year bins: −0.021 (SE 0.009, p .015).
- N = 0 share 5.1%; corr(FIT, log1p N) 0.927.

## How firm
Weak. It is an estimate; p .034 would not clear even the counted bar. Both separate readings are clearly negative, but that repeats what runs 04-06 already saw on these songs (more chord repetition, fewer covers), and that seen-song finding did not replicate on fresh ChoCo charts in run 08 (W01-J1).

## What it can and cannot say
As in v1_rep, A → ∞ makes D arithmetic: digamma-versus-log curvature, plus exposure that the dummies absorb. A negative β_D says only that ch_rep's association leans slightly toward the low-count end, where FIT and log counts differ most. It does not show that chord repetition tracks fitness rather than luck. SEEN songs.

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
