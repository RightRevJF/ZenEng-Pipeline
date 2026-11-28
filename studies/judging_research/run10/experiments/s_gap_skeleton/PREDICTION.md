# s_gap_skeleton: S_gap: Jason's S = 1 + g/π on the beat skeleton's pitch-class graph (G10-3), the one counted S

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: G10-3 (the Geometer); merged with R10-I3 GAP and L3's g, which run as estimates inside this folder. **Status: COUNTED** (rank 2 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`measures_geometer.py`, `measure(t)`, key `S_gap` (helpers `skeleton`, `_counts`, `_gap`).
1. Skeleton: the notes of the expanded first setting whose onset is on a beat (|beatpos − round(beatpos)| < 1e-4), in order, as MIDI pitches.
2. Nodes: the skeleton's distinct pitch classes (MIDI mod 12). c(a,b) = count of steps a → b; W = c + cᵀ (self-loops kept).
3. λ₂ = the second-largest eigenvalue of D^−½ W D^−½ (D = row sums of W); g = 1 − λ₂.
4. **S_gap = 1 + g/π.** No parameters. NaN if the skeleton has under 8 notes or under 3 pitch classes (none in split A).
By Cheeger, g/2 ≤ h ≤ √(2g), h the conductance of the best two-way cut of the pitch classes; on major tunes the Fiedler cut most
often splits the tonic triad from the other degrees (the Geometer's check).

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`S_gap`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.75** (n 3999; bar 0.5, R09-5); R² on the 13 baselines 0.155; largest baseline ρ pc_entropy -0.22, n_pc -0.19, range +0.13. Passes; not stopped.

Why it is tested: Jason's S, never powered before (run 07's chord version had power 0.01). Measured on the skeleton so that it is
not range renamed (R² 0.15 on the baselines, against 0.63 for the full-surface GAP).

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,511 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **−**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(S_gap) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: n_pc** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(S_gap) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = −0.03 SD of z(y_cov) per SD of S_gap** (a small gap = a clear two-region implied harmony = more covers). y_love: negative.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power s_gap_skeleton`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.673** | 0.047 | 0.923 | 0.0092 | 14,511 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- holding pc_entropy as well as n_pc (extra reading; predicted −)
- **GAP estimate (R10-I3, the Inventor):** key `GAP`, `measures_inventor.py` `_gap` on the cyclic, symmetrised, octave-distinct pitch graph of the full surface (self-loops kept), with range, n_pitch and ln_notes frozen; predicted −0.03; uncounted (alpha null)
- **g estimate (L3, the Listener; duplicate of GAP, ρ 0.97):** key `gap`, `measures_listener.py` `_gap`, same extras; predicted −; uncounted
- all 13 baselines held except n_pc already frozen (predicted −)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `s_gap_skeleton_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power s_gap_skeleton_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run s_gap_skeleton` (writes result.json; refuses unless this file is committed and pushed).
