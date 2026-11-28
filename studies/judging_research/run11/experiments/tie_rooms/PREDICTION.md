# tie_rooms: TIE: melody-harmony rooms (bipartite spectrum of the pc × chord graph)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R11-G3 (merges R11-I1 HB)**. **Status: COUNTED** (rank 2 of 5). K = 5, α = .05/5 = 0.01 (two-sided p).

## The measure (frozen)

Module `run11/experiments/measures/m_geometer.py`, cache key **`G_TIE`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

B[pc, chord] = beats of overlap between each melody note's [onset, onset + dur] and each chord's [onset, offset); a chord is
(root_pitch_class, root_position_intervals), inversion ignored, chords without a root skipped; ≥ 2 chords, ≥ 2 rows and ≥ 2 columns.
N = Dr^-1/2 B Dc^-1/2 with singular values 1 = s1 ≥ s2 ≥ …; TIE = Σ_{k≥2} s_k² / (min(rows, cols) − 1) (= Cramér's V² of the
duration table). B is the biadjacency of an exactly bipartite graph whose normalised Laplacian has eigenvalues 1 ∓ s_k.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.265** (4,258 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure ln_notes -0.34 (bar 0.70); R² on the 13 baselines 0.34; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.216, with all 13 baselines held 0.207.

## Why it is tested

Card 1, Theorem 1.1 on the bipartite melody-harmony graph: s_k near 1 = λ_k small = k chords each owning a room of melody notes
(λ_k/2 ≤ φ_k ≤ C√(λ_k log(k+1))). Such a tune carries its harmony inside it, so another artist can strip or re-arrange the backing
and keep the song. The Inventor's HB (R11-I1) is the same mathematics (ρ 0.96) and is merged here as a reading; the Geometer's recipe
decides because it weights a held note under every chord it overlaps.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **9,576 songs, 1,741 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(G_TIE) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: ln_notes, density, n_pc** (z-scored). Why these: ln_notes, density, n_pc (the Skeptic: Cramér's V² is biased upward in sparse tables; residual stability with these held 0.216). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = +0.03 SD of z(y_foreign) per SD of G_TIE** (sign +: chords that each own their melody notes go with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- **Pass:** p < 0.01 (.05/5), the predicted sign, both artist halves with that sign, and the conditional logit with that sign.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate below about +0.002 at the fake SE 0.0142 (R07-3).
- **Unsettled:** otherwise.
- Counted because its power at .05/5 is at least 0.2 (R06-5) and it is within the counted set (chair.md).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power tie_rooms`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.330** | 0.027 | 0.603 | 0.0142 | 9,576 | 1,741 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `G_TIE` with extras [none]; predicted sign +
- `all_13_baselines_and_mel_ic_mean_held`: `G_TIE` with the frozen extras plus n_pitch, range, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, bar_rep, mel_ic_mean; predicted sign +
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign +
- `CT_held`: `G_TIE` with the frozen extras plus CT; predicted sign +
- `G_TIE_BC_bergsma`: measure `G_TIE_BC` with extras [ln_notes, density, n_pc]; predicted sign +
- `HB`: measure `HB` with extras [ln_notes, density, n_pc]; predicted sign +

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run tie_rooms` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
