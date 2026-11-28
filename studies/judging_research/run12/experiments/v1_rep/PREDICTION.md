# v1_rep: does pitch-class entropy predict fitness better than it predicts cover counts? (Jason's vector 1)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. I opened no outcome file: I called neither `C5.load_outcomes` nor `common12.load_hook`, and I did not read `/home/claude/dl/run12/fitness.json` or `data/*.json`. I did not run `harness12.py run` on this folder; a dry run on a synthetic outcome (random numbers) was the only run. Idea: **V1, Jason's mandated vector-1 test (P11-1)**, with the Skeptic's round-2 design. **Status: COUNTED** (rank 1 of 3). K = 3, α = .05/3 = 0.0167 (two-sided p).

## The measure (frozen)
**REP** = run 11's frozen recipe, cache key `REP` in `/home/claude/dl/run11/measures_run11.json`. It is the Shannon entropy in bits of each Hooktheory clip's duration-weighted melody pitch-class distribution, and the song value is the n_mel-weighted mean over clips. Gate (run 11): clip stability 0.389 passes; REP is exempt from the overlap gate.

## Songs
Run 04's within-artist Hooktheory rows (9,588 songs, 1,741 artists) that have a FIT value in `fitness.json`, which means they have a Discogs-VI group with an own set. The orchestrator's outcome-side count is 2,091 such rows, 1,853 of them in artists with two or more. The test keeps artists with 2+ such rows. **These songs are SEEN**: runs 04-06 joined their outcome to chord measures, and run 11 joined it to REP (REP passed on y_foreign there). FIT has never been joined to any notes measure.

## Outcome
**D = z(FIT) − z(log(1 + N))**, with both z-scores taken over the test rows. D is **not** re-standardised.
- FIT is the posterior mean of log η from the frozen `fitness/fitness.py` (commit b0c7824).
- N is the timed cover count that fitness.py uses and that fitness.json carries.

Because the design is linear and the rows are the same, β_D = β(z FIT) − β(z log1p N) exactly. A paired comparison of the two standardised betas is therefore just this one regression.

## Model and controls (`harness12.py`, kind `v1`)
- OLS of D on z(REP), with **artist fixed effects**, run 04's controls (`C5.controls`) and **exact first-year dummies** (t0 from fitness.json).
- Frisch-Waugh, with CR1 SEs clustered by artist.
- **Halves:** md5(artist slug) mod 2.
- **No second model.** D is continuous, and the conditional logit applies only to binary outcomes.

## Prediction
**β_D = −0.01**: REP's leaning sign, negative. In words, pitch-class entropy predicts fitness better than it predicts log counts, in the direction it leaned before.

## Verdict rules (written once)
- **Pass:** all three of the following hold:
  - p < 0.0167;
  - β_D < 0;
  - both artist halves have β_D < 0.
- **Killed** ("predicts fitness no better than counts", Jason's words): −0.01 lies outside β̂_D ± 1.96 SE **and** β̂_D ≥ 0.
- **Unsettled:** otherwise. This includes a β̂_D far below −0.01, which is better than predicted and not a kill.

**Plain statement.** The frozen fit puts A → ∞ (2×10⁶): cover timing shows no rich-get-richer beyond song-to-song rate differences. Within a first year, FIT is then a strictly increasing function of N alone, and the exposure term depends only on the year, which the dummies absorb. So D is **arithmetic**: the curvature of digamma(r + N) against log(1 + N), which weighs the step from 0 to 1 cover about twice as heavily, plus exposure handled by the year dummies. **A kill indicts the estimator's power to separate fitness from counts, not the notes.** A pass says REP's association sits disproportionately at the low-count end (0 vs a few covers), where FIT and log counts differ most. It cannot show fitness beyond luck.

## Power (power.json; fake outcomes before any outcome)
The power is model-based, because D's distribution is set by the frozen model's arithmetic. Setup, on the real rows:
- **Selection:** which songs have a group comes from an artist-clustered probit, tuned to 2,091/9,588 and to y's within-artist share of 0.38 (`outcome_side_shares.json`).
- **First years:** these are fake. Two scenarios:
  - "artist": an era drawn per artist from 1960-2012, plus 0-8 years per song;
  - "recent": 1985-2012, plus 0-3 years.
- **Fitness:** η ~ Gamma(r = 0.663, r), with artist correlation tuned to log-covers' within-artist share (target 0.427; achieved 0.39).
- **Counts:** N ~ Poisson(η E(t0)), with E taken from fit.json's A, g and h, and FIT = digamma(r + N) − log(r + E).
- **Fake outcome:** the model's own D plus −0.01·z(REP), with the same model and dummies.
- The simulated sd of D is 0.39, against the real 0.38 implied by FIT–log1p N Pearson 0.927.

300 draws, seed 12; the power is the lower of the two scenarios.

| α | power ("artist") | power ("recent") | **power used** |
|---|---|---|---|
| .05/3 = 0.0167 | 0.293 | 0.300 | **0.293** |

The median fake SE is 0.0055, with a median of 1,845 rows. Kill rate if the true β_D = 0: 0.42. Monte Carlo error is about ±0.026.

## Readings (uncounted; frozen)
- β on z(FIT) and β on z(log1p N), separately, in the same design;
- D with five-year first-year bins in place of exact years;
- the share of test rows with N = 0;
- corr(FIT, log1p N) on the test rows.

## How to run (once, after this file, spec.json, power.json, common12.py and harness12.py are committed and pushed)
`cd run12/experiments && python3 harness12.py run v1_rep` writes result.json. The run refuses unless the guard's files are committed, unmodified and pushed to origin/judging-research.

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
