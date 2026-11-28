# cut_ab_parts: cut_ab: the Cheeger cut lines up with the parts (L3)

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: L3 (the Listener). **Status: COUNTED** (rank 6 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`measures_listener.py`, `measure(t)`, key `cut_ab` (helper `_gap`).
1. Undirected pitch-transition graph of the expanded first setting: nodes = distinct MIDI pitches (octave kept); W[a,b] += 1 and
   W[b,a] += 1 for each step a → b with a ≠ b (unisons dropped).
2. Normalised Laplacian L = I − D^−½ W D^−½; v₂ = the eigenvector of its second-smallest eigenvalue (numpy `eigh`); Fiedler
   coordinate f = D^−½ v₂.
3. For each note i of the expanded melody (n notes), f(pitch_i), and the indicator h_i = 1 if i ≥ n/2.
4. **cut_ab = |Pearson r(f(pitch_i), h_i)|**; NaN if f is constant over the notes. No parameters.
Not in the test (None) under the same conditions as the other Listener keys (98 split-A tunes).

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`cut_ab`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.773** (n 4000; bar 0.5, R09-5); R² on the 13 baselines 0.178; largest baseline ρ range +0.26, n_pitch +0.21, ln_notes -0.14. Passes; not stopped.

Why it is tested: Cheeger geometry asked as a Listener question: is the graph's bottleneck a landmark in time (A part low, B part
"up the neck")? It reads form (n_bars and ln_notes frozen at the Skeptic's request); "second half" differs between two- and three-part
tunes, which dilutes rather than reverses.

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,413 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **+**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(cut_ab) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: n_bars, ln_notes** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(cut_ab) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = +0.03 SD of z(y_cov) per SD of cut_ab** (register marks the part; a two-chamber map for memory). y_love: positive.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power cut_ab_parts`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.700** | 0.050 | 0.920 | 0.0092 | 14,413 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- strict AABB reels and jigs only (subset `aabb` == 1: first setting written as 16 bars that expand to 32; 1,444 split-A tunes; predicted +)
- `cheeger` (conductance of the Fiedler sweep cut) with range, n_pitch, ln_notes frozen; predicted − (a stronger bottleneck = smaller h)
- `h0_max` (card 1 H0 check: longest MST edge / total, edge length 1/p_sym) with range, n_pitch, ln_notes frozen; predicted +
- all 13 baselines held (predicted +)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `cut_ab_parts_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power cut_ab_parts_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run cut_ab_parts` (writes result.json; refuses unless this file is committed and pushed).
