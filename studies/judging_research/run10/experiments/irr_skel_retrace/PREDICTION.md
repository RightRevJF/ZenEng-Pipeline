# irr_skel_retrace: irr_skel: retracing, the tree reduction of the skeleton walk (G10-2; IRR revived on melody)

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: G10-2 (the Geometer); the backlog's IRR (R09-I1) on a melody. **Status: COUNTED** (rank 4 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`measures_geometer.py`, `measure(t)`, key `irr_skel` (helpers `skeleton`, `_irr`).
1. Skeleton as in S_gap (on-beat MIDI pitches).
2. Merge consecutive equal pitches: a sequence of length m.
3. Free reduction by a stack: push each pitch, but if the stack has 2 or more entries and stack[−2] equals it, pop instead (x y x → x). Final length k.
4. **irr_skel = (k − 1) / max(m − 1, 1).** No parameters. NaN if the skeleton has under 8 notes.
A walk on a tree reduces to its geodesic; what survives is the walk's word in the fundamental group of its own transition graph.

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`irr_skel`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.767** (n 4000; bar 0.5, R09-5); R² on the 13 baselines 0.074; largest baseline ρ pc_entropy +0.18, n_pitch +0.16, range +0.13. Passes; not stopped.

Why it is tested: The backlog's IRR, which in run 09 on chords went the other way from its prediction (back-and-forth with more
covers, −0.060, a lead). Clean (R² 0.07); n_pc is frozen because n_pc leans in simplicity's direction.

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,511 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **−**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(irr_skel) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: n_pc** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(irr_skel) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = −0.03 SD of z(y_cov) per SD of irr_skel** (a melody whose way back is its way out is easier to learn). y_love: negative.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power irr_skel_retrace`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.753** | 0.050 | 0.917 | 0.0090 | 14,511 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- holding pc_entropy as well as n_pc (extra reading; predicted −)
- all 13 baselines held (predicted −)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `irr_skel_retrace_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power irr_skel_retrace_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run irr_skel_retrace` (writes result.json; refuses unless this file is committed and pushed).
