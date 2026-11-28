# ant_push: ANT: the push (the melody reaches the next chord's new tone early)

Run 11, 28 November 2026 (the 02:17 ET pass). Frozen by the chair before any outcome is joined: no outcome file was opened, `common11.load_outcomes` and `C5.load_outcomes` were not called, and `harness11.py run` was not run. Idea: **R11-I2**. **Status: COUNTED** (rank 5 of 5). K = 5, α = .05/5 = 0.01 (two-sided p).

## The measure (frozen)

Module `run11/experiments/measures/m_inventor.py`, cache key **`ANT`** (cache `/home/claude/dl/run11/measures_run11.json`, built by `build_cache11.py` from `measures/*.py`; the test reads the cache).

Over consecutive chord spans (h0, h1) of the clip (chords sorted by onset, root present; ≥ 4 pairs), a hit is a pair where
some melody note has onset in [t − 0.5, t) beats, t = h1's onset, on a pitch class in pcs(h1) \ pcs(h0) (pcs = root plus the
cumulative root_position_intervals, mod 12). ANT = hits / pairs.

Gate (standing Hooktheory gate of runs 05-06, on the raw measure; `measure_gates11.json`): clip-1 vs clip-2 Spearman **0.252** (3,981 pairs; bar 0.20); largest |Spearman| with a baseline or pack measure density +0.27 (bar 0.70); R² on the 13 baselines 0.11; **passes**. Beside it (decides nothing): stability with the frozen extras held 0.213, with all 13 baselines held 0.177.

## Why it is tested

Of two coupled oscillators the leader drives (phase lead). A melody that anticipates the next chord's new tone carries the
harmonic rhythm itself, so a cover artist with another groove still gets the changes from the tune. Not renamed (within-artist R²
0.12 on all 30 measures, the Skeptic). Risk, accepted by the author: the push is style-coded and depends on where the transcriber
puts the chord change; artist fixed effects absorb only part of that.

## Songs

The 9,588 within-artist Hooktheory songs (run 04's rows: 1,741 artists with two or more songs), with the measure and the frozen extras defined: **9,363 songs, 1,740 artists** (`harness11.design`). **These songs are SEEN:** their outcome was joined to chord measures in runs 04-06 (chord repetition within artist about −0.04) and to a few melody measures (run 05-06). This measure is new to them; the songs are re-spent. No run 10 figure is used as evidence (run 10 is withdrawn: `run10/WITHDRAWN.md`).

## Outcome

**y_foreign**, within artist: 100 if the song's Discogs-VI group holds a version by a performer set sharing no name with the original artist's sets, else 0 (run 04's rule 4410a0e via `C5.load_outcomes`); dropped rows are nan.

## Model and controls (`common11.fit`)

OLS of z(y_foreign) on z(ANT) with **artist fixed effects** and run 04's controls (chord-count bins, clips-per-song dummies, ln beats, title-word and title flags; `C5.controls`), plus the **frozen extras: density** (z-scored). Why these: density (notes per bar: more notes put more onsets in any half-beat window; residual stability 0.213). Frisch-Waugh; CR1 SEs clustered by artist; β = SD of y per SD of x within artist. **First year cannot be held on this (extensive) margin:** songs not in Discogs-VI have none. The intensive reading holds it. Second model: conditional logit (artist groups) of the binary outcome on the same columns, sign only (`common11.second`). Halves: md5(artist slug) mod 2 (`row['half']`, run 04's).

## Prediction

**β = +0.03 SD of z(y_foreign) per SD of ANT** (sign +: more anticipated chord changes go with more uptake), within artist.

## Verdict rules (`common11.verdict`)

- **Pass:** p < 0.01 (.05/5), the predicted sign, both artist halves with that sign, and the conditional logit with that sign.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE), i.e. roughly an estimate below about +0.003 at the fake SE 0.0138 (R07-3).
- **Unsettled:** otherwise.
- Counted because its power at .05/5 is at least 0.2 (R06-5) and it is within the counted set (chair.md).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness11.py power ant_push`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 11, α = 0.01.

| power | kill_if_true | kill_if_zero | median fake SE | n | artists |
|---|---|---|---|---|---|
| **0.280** | 0.027 | 0.610 | 0.0138 | 9,363 | 1,740 |

Monte Carlo error about ±0.024 near these values. K = 5, α = .05/5 = 0.01 (chair.md has the K table and rule).

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `bare_no_extras`: measure `ANT` with extras [none]; predicted sign +
- `all_13_baselines_and_mel_ic_mean_held`: `ANT` with the frozen extras plus ln_notes, n_pitch, n_pc, range, int_entropy, n_int, step_share, leap_share, unison_share, pc_entropy, tonic_share, bar_rep, mel_ic_mean; predicted sign +
- `intensive_covers_first_year_held`: intensive margin: among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, run 04's controls, the frozen extras and first year (linear); predicted sign +
- `sync_per_note_held`: `ANT` with the frozen extras plus sync_per_note; predicted sign +
- `CT_held`: `ANT` with the frozen extras plus CT; predicted sign +

## How to run (after this file, spec.json, power.json and common11.py are committed and pushed)

`cd run11/experiments && python3 harness11.py run ant_push` (writes result.json; refuses unless this file and common11.py are committed, unmodified and pushed to origin/judging-research). Run it once. statsmodels must be installed first (the conditional logit needs it; without it the second model fails and a counted test cannot pass).
