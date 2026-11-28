# slg_selflearn: SLG: self-learnability gain (the tune teaches itself better than the corpus does)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R10-L1**. **Status: ESTIMATE** (uncounted; not in K; decides nothing). Printed against α = .05/5 = 0.01 for reference only.

## The measure (frozen)

Module `run11/experiments/measures/m_chair_run10.py`, cache key **`R_SLG`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

On the clip's unison-collapsed sequence of tonic-relative pitch classes, the mean over the second half (i ≥ ⌊n/2⌋) of
log2 p_self(x_i | x_i−1) − log2 p_corpus(x_i | x_i−1); add-one bigrams ((count + 1)/(row + 12)); p_self from the clip's own earlier
notes; p_corpus from every raw Hooktheory clip with a melody, mode-split as TYP11 (Hooktheory has no tune types, so mode replaces
run 10's tune type), leave-one-out (the clip's own counts subtracted). ≥ 16 collapsed notes and ≥ 8 on-beat notes. Run 10's
Listener recipe (R10-L1), copied, not imported (run 10's module reads TheSession data).

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.247** (3,415 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure mel_rep +0.44 (bar 0.70); R² on the 13 baselines 0.47; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.217, with all 13 baselines held 0.153.

## Why it is tested

What a musician learns by ear is what the song teaches about itself: a melody whose own past predicts its future better than
the genre does is learned in a few hearings. Run 10's deduction (R10-L1), re-tested fresh; its run 10 figures are withdrawn and
not evidence. ESTIMATE, not in K: its power at .05/5 clears the floor (see below), but the counted set is full (the run 08 K rule,
ranking order in chair.md); it ranks sixth because its Hooktheory corpus is the chair's wrap rather than a recipe argued through
this pass's two rounds, and its main renamer, mel_rep (ρ +0.44), is not held in the frozen form (it is a reading).

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **8,879 songs, 1,728 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(R_SLG) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: bar_rep, ln_notes** (z-scored). Why these: bar_rep, ln_notes (run 10's frozen form, kept). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = +0.03 SD of z(y_foreign) per SD of R_SLG** (sign +: a melody whose own past predicts it better than the corpus does goes with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- The harness is run with `counted: false`, so the verdict is **estimate** whatever the result. The estimate, its range, the halves and the logit are reported; the rule that would kill it if it were counted is the same (the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate below about -0.001 at the fake SE 0.0158).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power slg_selflearn`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.227** | 0.023 | 0.487 | 0.0158 | 8,879 | 1,728 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `R_SLG` with extras [none]; predicted sign +
- `all_13_baselines_and_mel_ic_mean_held`: `R_SLG` with the frozen extras plus density, n_pitch, n_pc, range, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, mel_ic_mean; predicted sign +
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign +
- `mel_rep_held`: `R_SLG` with the frozen extras plus mel_rep; predicted sign +
- `R_SLGW`: measure `R_SLGW` with extras [bar_rep, ln_notes]; predicted sign +

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run slg_selflearn` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
