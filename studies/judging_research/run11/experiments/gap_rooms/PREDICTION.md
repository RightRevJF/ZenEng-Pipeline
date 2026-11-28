# gap_rooms: GAP: Jason's S on the clip melody (two rooms and a doorway)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R11-G1 (= R10-I3; merges R10-C1, R10-L3, R10-G3, R11-G2, R11-L1)**. **Status: COUNTED** (rank 1 of 5). K = 5, α = .05/5 = 0.01 (two-sided p).

## The measure (frozen)

Module `run11/experiments/measures/m_geometer.py`, cache key **`G_GAP`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

λ2 of the normalised Laplacian L = I − D^-1/2 W D^-1/2 of the clip's octave-distinct pitch-transition graph: one node per
distinct MIDI-like pitch (12·octave + pc); W = C + Cᵀ, C[a,b] = count of consecutive notes a→b over the whole clip (transitions
across rests kept); repeated notes kept as self-loops; cyclic (the last note joined to the first); at least 3 distinct pitches.
Identical to m00 `GAP` (run 10's R10-I3 recipe). Jason's S = 1 + λ2/π is a monotone transform, so S and G_GAP are one test.
Song value = the n_mel-weighted mean over the song's clips with a value.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.200** (4,239 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure n_pitch -0.61 (bar 0.70); R² on the 13 baselines 0.57; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.158, with all 13 baselines held 0.089.

## Why it is tested

Card 1 (Li 2026), k = 2 case = the classical Cheeger inequality: λ2/2 ≤ φ2 ≤ √(2λ2). A small gap means the melody lives in two
pitch rooms joined by a thin doorway, a shape with parts a singer can hold and carry. The Geometer withdrew his round-1 −0.04
(anchoring on withdrawn run 10 figures) and froze −0.03. Merged here as readings (one idea: |ρ| with G_GAP 0.79 to 0.80): G_ROOMS (R11-G2,
the higher-order room profile), SETTLE (R11-L1, the sweep-cut crossings) and run 10's Cheeger constant (R10-C1); run 10's CUT_AB (R10-L3)
belongs with them (the Fiedler cut read against time; it fails the gate). As further gate-failed readings printed for the record, run 10's other pitch-graph and contour geometry (R10-G1 pe_h0, R10-G2
retracing, R10-G3 skeleton S, R10-I1 arches) ride here too.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **9,566 songs, 1,740 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(G_GAP) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: range, n_pitch, ln_notes** (z-scored). Why these: range, n_pitch, ln_notes (the Geometer's frozen size block: the stable part of λ2 is mostly size, R² 0.57 on the 13 baselines). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = -0.03 SD of z(y_foreign) per SD of G_GAP** (sign −: a smaller gap, i.e. thinner doorways between pitch rooms, goes with more uptake by other artists), within artist.

## Verdict rules (`common11.verdict`)

- **Pass:** p < 0.01 (.05/5), the predicted sign, both artist halves with that sign, and the conditional logit with that sign.
- **Killed:** the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate above about +0.000 at the fake SE 0.0154 (R07-3).
- **Unsettled:** otherwise.
- Counted because its power at .05/5 is at least 0.2 (R06-5) and it is within the counted set (chair.md).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power gap_rooms`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.220** | 0.023 | 0.473 | 0.0154 | 9,566 | 1,740 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `G_GAP` with extras [none]; predicted sign −
- `all_13_baselines_and_mel_ic_mean_held`: `G_GAP` with the frozen extras plus density, n_pc, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, bar_rep, mel_ic_mean; predicted sign −
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign −
- `G_ROOMS`: measure `G_ROOMS` with extras [range, n_pitch, ln_notes]; predicted sign +
- `G_ROOMS_holding_G_GAP`: measure `G_ROOMS` with extras [range, n_pitch, ln_notes, G_GAP]; predicted sign +
- `SETTLE`: measure `SETTLE` with extras [n_pitch, range]; predicted sign +
- `R_CHEEGER_R10-C1`: measure `R_CHEEGER` with extras [range, n_pitch, ln_notes]; predicted sign − (stopped as a test: n_pitch rho -0.715; reading)
- `R_CUT_AB_R10-L3`: measure `R_CUT_AB` with extras [ln_notes]; predicted sign + (measure failed the standing gate (stopped); printed for the record, reads noise)
- `R_SGAP_R10-G3`: measure `R_SGAP` with extras [n_pc]; predicted sign − (measure failed the standing gate (stopped); printed for the record, reads noise)
- `R_PE_H0_R10-G1`: measure `R_PE_H0` with extras [pc_entropy]; predicted sign + (measure failed the standing gate (stopped); printed for the record, reads noise)
- `R_IRR_R10-G2`: measure `R_IRR` with extras [n_pc]; predicted sign − (measure failed the standing gate (stopped); printed for the record, reads noise)
- `R_ARCH_R10-I1`: measure `R_ARCH` with extras [range, n_pitch]; predicted sign − (measure failed the standing gate (stopped); printed for the record, reads noise)

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run gap_rooms` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
