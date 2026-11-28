# typ11_typical: TYP11: a typical melody by exposure (scale-degree time profile against the corpus)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R11-L2**. **Status: COUNTED** (rank 4 of 5). K = 5, α = .05/5 = 0.01 (two-sided p).

## The measure (frozen)

Module `run11/experiments/measures/m_listener.py`, cache key **`TYP11`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

prof[(pitch − tonic_pc) mod 12] += dur over the clip's notes; the corpus profile is the same sum over every raw Hooktheory clip
with a melody (sorted key order), kept separately for major keys (first two scale steps sum to 4) and the rest; TYP11 = Pearson r
of prof[1:12] with corpus[1:12] for the clip's mode (the tonic bin dropped, so it is not tonic_share). A corpus statistic, not a
tuned setting.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.212** (4,266 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure n_int +0.25 (bar 0.70); R² on the 13 baselines 0.16; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.207, with all 13 baselines held 0.183.

## Why it is tested

Listeners carry a long-memory schema of how much time a pop melody spends on each scale degree; a melody that matches it is heard
as already known on first exposure and is easy to hold. Zeroth-order (where the time goes), not mel_ic_mean's sequential surprisal
(|ρ| < 0.19). The Skeptic's risk, stated: 'typical' may mean the corpus's dominant style; the TYP_KK11 reading (listener profile,
Krumhansl–Kessler) separates the two: if TYP11 lives and TYP_KK11 is zero, it measures style, not schema.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **9,588 songs, 1,741 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(TYP11) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: mel_ic_mean** (z-scored). Why these: mel_ic_mean (the seen pack measure; the Skeptic's route by which seen-ness could enter). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = +0.03 SD of z(y_foreign) per SD of TYP11** (sign +: a melody whose time profile over scale degrees matches the corpus goes with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- **Pass:** p < 0.01 (.05/5), the predicted sign, both artist halves with that sign, and the conditional logit with that sign.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate below about +0.004 at the fake SE 0.0133 (R07-3).
- **Unsettled:** otherwise.
- Counted because its power at .05/5 is at least 0.2 (R06-5) and it is within the counted set (chair.md).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power typ11_typical`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.387** | 0.037 | 0.660 | 0.0133 | 9,588 | 1,741 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `TYP11` with extras [none]; predicted sign +
- `all_13_baselines_and_mel_ic_mean_held`: `TYP11` with the frozen extras plus ln_notes, density, n_pitch, n_pc, range, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, bar_rep; predicted sign +
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign +
- `pc_entropy_held`: `TYP11` with the frozen extras plus pc_entropy; predicted sign +
- `tonic_share_held`: `TYP11` with the frozen extras plus tonic_share; predicted sign +
- `TYP_KK11`: measure `TYP_KK11` with extras [mel_ic_mean]; predicted sign + (clip stability 0.198, just under the gate; reading)
- `TYP_all_12_bins`: measure `TYP` with extras [mel_ic_mean]; predicted sign +

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run typ11_typical` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
