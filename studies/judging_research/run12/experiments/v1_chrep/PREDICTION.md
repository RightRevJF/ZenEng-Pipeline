# v1_chrep: does chord repetition predict fitness better than counts? (Jason's vector 1, second measure)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. As for `v1_rep`: no outcome was opened, and only a dry run on a synthetic outcome was made. Idea: **V1 (P11-1)**. **Status: ESTIMATE.** Its power at .05/3 is 0.193, under the 0.2 floor (R06-5), so it passes nothing and kills nothing. K = 3, α = .05/3 = 0.0167 for the counted tests.

## The measure (frozen)
**ch_rep**: the data pack's chord repetition, read from the rows (`C5.FE`); the song value is the n_mel-weighted mean over clips. It is an existing pack measure, gated in runs 04-06.

## Songs, outcome, model, halves
These are identical to `v1_rep/PREDICTION.md`:
- Songs: Hooktheory within-artist rows with FIT, in artists with 2+ such rows.
- Outcome: D = z(FIT) − z(log(1 + N)), z-scored over the test rows and not re-standardised.
- Model: OLS of D on z(ch_rep), with artist FE, run 04's controls and exact first-year dummies; CR1 SEs by artist.
- Halves: md5(artist) mod 2.
- No second model, because D is continuous.

## Prediction
**β_D = −0.01**, ch_rep's leaning sign (negative).

## Verdict rules (they would apply if it were counted; as an estimate it decides nothing)
- **Pass:** p < 0.0167, β_D < 0, and both halves negative.
- **Killed:** −0.01 lies outside β̂_D ± 1.96 SE **and** β̂_D ≥ 0.
- **Unsettled:** otherwise.

The same plain statement holds as in `v1_rep`. With A → ∞, D is arithmetic: the digamma-versus-log curvature, plus exposure that the year dummies handle. A kill would indict the estimator's power to separate, not the notes.

## Power (power.json; the same model-based fake outcomes as v1_rep, 300 draws, seed 12)

| α | "artist" | "recent" | **used (lower)** |
|---|---|---|---|
| 0.0167 | 0.193 | 0.240 | **0.193** |

The median fake SE is 0.0059. The kill rate if the true β_D = 0 is 0.36. The test is under the floor at K = 3; at K = 2 its power would be 0.25 (chair.md has the K table).

## Readings
These are as in v1_rep: β on z(FIT) and on z(log1p N) separately, D with five-year bins, the share with N = 0, and corr(FIT, log1p N).

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run v1_chrep`
