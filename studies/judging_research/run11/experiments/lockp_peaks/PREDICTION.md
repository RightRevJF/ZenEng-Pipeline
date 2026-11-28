# lockp_peaks: LOCKP: the footfall (contour peaks on strong beats)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R11-I3 (merges R10-I2 LOCK)**. **Status: ESTIMATE** (uncounted; not in K; decides nothing). Printed against α = .05/5 = 0.01 for reference only.

## The measure (frozen)

Module `run11/experiments/measures/m_inventor.py`, cache key **`LOCKP`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

Repeated pitches merged into their first onset; metrical weight w = 1 + [on the half-beat grid] + [on a beat] + [on the half-bar,
even bpb] + [downbeat], at b = onset mod bpb; a peak is a run higher than both neighbours (≥ 3 peaks); LOCKP = mean w at the peaks
minus mean w over all runs.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.143** (3,965 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure ln_notes +0.07 (bar 0.70); R² on the 13 baselines 0.02; **stopped**. Beside it (decides nothing): stability with the frozen extras held 0.143, with all 13 baselines held 0.136.

## Why it is tested

The dancer lifts on the strong beat. Run 10's LOCK (R10-I2) sharpened; LOCK itself is a reading here. ESTIMATE ONLY: it FAILS
the standing gate in every form (best clip-to-clip 0.143; run 10's LOCK recipe 0.112): the footfall belongs to the section, not
the song. It runs uncounted under Jason's test-everything rule, at the author's round-2 size +0.02, with no extras; it decides
nothing, and its power is under the floor in any case.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **9,379 songs, 1,740 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(LOCKP) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: none** (z-scored). Why these: none. Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = +0.02 SD of z(y_foreign) per SD of LOCKP** (sign +: contour peaks on heavier beats go with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- The harness is run with `counted: false`, so the verdict is **estimate** whatever the result. The estimate, its range, the halves and the logit are reported; the rule that would kill it if it were counted is the same (the prediction (+0.02) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate below about -0.005 at the fake SE 0.0128).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power lockp_peaks`: y = β·z(x) + N(0, 1 − β²) with β = +0.02, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.133** | 0.033 | 0.300 | 0.0128 | 9,379 | 1,740 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `all_13_baselines_and_mel_ic_mean_held`: `LOCKP` with the frozen extras plus ln_notes, density, n_pitch, n_pc, range, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, bar_rep, mel_ic_mean; predicted sign +
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign +
- `LOCK_R10-I2`: measure `LOCK` with extras [none]; predicted sign + (measure failed the standing gate (stopped); printed for the record, reads noise)
- `LOCKW`: measure `LOCKW` with extras [none]; predicted sign + (stability not gated; reading)

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run lockp_peaks` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
