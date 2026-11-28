# core_typical: core_ic: a typical skeleton (low corpus surprisal of the on-beat notes)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R10-L2 (with R10-L2b TSG as a reading)**. **Status: ESTIMATE** (uncounted; not in K; decides nothing). Printed against α = .05/5 = 0.01 for reference only.

## The measure (frozen)

Module `run11/experiments/measures/m_chair_run10.py`, cache key **`R_CORE_IC`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

Skeleton = the clip's notes whose onset is exactly on a beat (beatpos an integer), as tonic-relative pitch classes; core_ic =
the mean of −log2 p_corpus(x_i | x_i−1) over the skeleton's bigrams, add-one, corpus = the skeleton bigrams of every raw Hooktheory
clip with a melody, mode-split, leave-one-out (as R_SLG). ≥ 16 collapsed surface notes and ≥ 8 skeleton notes. Run 10's R10-L2.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.386** (3,415 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure mel_ic_mean +0.59 (bar 0.70); R² on the 13 baselines 0.41; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.130, with all 13 baselines held 0.181.

## Why it is tested

Transmission keeps the strong-beat frame; a skeleton that walks the common paths is already known before it is heard. Run 10's
deduction, re-tested fresh. The Listener (round 1) asked that, if built, it be an estimate with mel_ic_mean frozen, since the
pack's mel_ic_mean already measures corpus surprisal on these seen songs (ρ +0.59). ESTIMATE, not in K: power at .05/5 is under the
0.2 floor.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **8,879 songs, 1,728 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(R_CORE_IC) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: pc_entropy, mel_ic_mean** (z-scored). Why these: pc_entropy (run 10's frozen extra) and mel_ic_mean (the Listener's condition). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = -0.03 SD of z(y_foreign) per SD of R_CORE_IC** (sign −: a lower-surprisal (more typical) on-beat skeleton goes with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- The harness is run with `counted: false`, so the verdict is **estimate** whatever the result. The estimate, its range, the halves and the logit are reported; the rule that would kill it if it were counted is the same (the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate above about +0.005 at the fake SE 0.0178).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power core_typical`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.190** | 0.030 | 0.397 | 0.0178 | 8,879 | 1,728 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `R_CORE_IC` with extras [none]; predicted sign −
- `all_13_baselines_and_mel_ic_mean_held`: `R_CORE_IC` with the frozen extras plus ln_notes, density, n_pitch, n_pc, range, int_entropy, n_int, step_share, leap_share, unison_share, tonic_share, bar_rep; predicted sign −
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign −
- `run10_form_pc_entropy_only`: measure `R_CORE_IC` with extras [pc_entropy]; predicted sign −
- `R_SURF_IC`: measure `R_SURF_IC` with extras [pc_entropy, mel_ic_mean]; predicted sign −
- `R_TSG_R10-L2b`: measure `R_TSG` with extras [pc_entropy, mel_ic_mean]; predicted sign − (measure failed the standing gate (stopped); printed for the record, reads noise)

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run core_typical` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
