# windows: early covers against late covers; does the notes measure read launch or fitness? (vector 1)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. No outcome was opened, and only a dry run on a synthetic outcome was made. Idea: **WINDOWS**, the Skeptic's Merge 1 of R12-G3 THIN (Geometer), R12-L3 Late wins (Listener) and R12-I1 PROP (Inventor). **Status: ESTIMATE.** Power for REP's Δ at .05/3 is 0.060; ch_rep has a zero prediction, so no directional pass is possible. It passes nothing and kills nothing. K = 3, α = .05/3 = 0.0167 for the counted tests.

## Measures
**REP** (run 11's cache) and **ch_rep** (the pack), each in its own pair of models.

## Songs
Hooktheory within-artist rows with FIT (a Discogs-VI group with an own set) and **t0 ≤ 2005**, in artists with 2+ such songs. The simulated median is about 1,450 rows. These songs are SEEN.

## Outcome (from the versions, by fitness.py's cover rule; `common12.window_counts`)
A version is a cover if its performer set is non-empty and shares no normalised name with the original artist's own sets. Versions with no year, or a year after 2023, are dropped. A year before t0 counts at t0. t0 is fitness.json's first year. The two counts are:
- **N_E:** covers at ages 0-3.
- **N_L:** covers at ages 8 and over, up to 2023.

The loader prints how many songs' total differs from fitness.json's N.

## Model (`harness12.windows_fit`)
- For each window w, a **Poisson model with artist fixed effects**, estimated by the conditional (multinomial) likelihood. That gives the FE-Poisson β exactly; artists with no covers in the window drop out.
- The model regresses N_w on z(x), run 04's controls and **five-year first-year dummies**. Each window has its own dummies, which amounts to decade × window.
- **Offset:** log X_w, where X_w = Σ over the window's calendar years of A·g(age)·h(era), with fit.json's frozen g and h.
- I chose FE Poisson over OLS on log(1 + N_w) because it is practical here.
- **Statistic:** Δ = β_L − β_E, in log-rate per SD of x.
- **SE:** a **paired artist bootstrap**, 500 resamples with seed 12, refitting both windows on each resample. The analytic joint cluster sandwich is printed beside it; in the dry run the two agreed to 0.0001.

## Prediction (one per measure; whose)
- **REP: Δ = −0.02**, the **Listener's** round-2 prediction: quality shows more in late covers. The Inventor and the Geometer predict Δ = 0. Δ = 0 cannot pass a directional rule, so the directional −0.02 is frozen, and whether 0 lies outside Δ ± 1.96 SE is printed as a reading.
- **ch_rep: Δ = 0**, the **Inventor's** prediction; the only author to predict for ch_rep.

## Rules (an estimate passes and kills nothing; printed)
- Whether each prediction lies outside Δ ± 1.96 SE_boot.
- **Inventor's reading:** whether β_L = −0.05 (both measures) lies outside β_L ± 1.96 SE.
- **Listener's reading:** |β_E| > |β_L| would mean "exposure, not quality".

## Power (power.json; model-based fake counts as in v1_rep, "artist" era scenario, t0 ≤ 2005, β_E = −0.05, β_L = −0.07; 300 draws, seed 12)
- REP: power **0.060** at α 0.0167 and 0.147 at α 0.05.
- The median SE of Δ is 0.022.

## Readings
- 1970+ songs only, against rival versions in the 1950s and 60s (Inventor round 2).
- β_L with log(r + N_E) held (Inventor round 1).
- Whether Δ = 0 lies outside the range.
- β_E and β_L separately, with their SEs and cover totals.

## Lakh pooling
Not done this pass. The Lakh–Discogs clique link lives in an outcome file, so it is logged as next pass: see `../DATA.md`.

## How to run (once, after commit and push; about a minute)
`cd run12/experiments && python3 harness12.py run windows`
