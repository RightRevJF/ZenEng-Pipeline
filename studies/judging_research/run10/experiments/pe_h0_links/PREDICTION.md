# pe_h0_links: pe_h0: weak links, the persistent entropy of the H0 barcode of the skeleton (G10-1; card 1, M4)

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: G10-1 (the Geometer). **Status: COUNTED** (rank 3 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`measures_geometer.py`, `measure(t)`, key `pe_h0` (helpers `skeleton`, `_counts`, `_pe_h0(C, "log")`).
1. Skeleton as in S_gap (on-beat notes, MIDI pitches with octave kept).
2. c(a,b) = count of steps a → b between distinct skeleton pitches; S = c + cᵀ with the diagonal set to 0 (self-loops dropped); p_sym = S / ΣS.
3. Edge length = −ln p_sym (the transition's surprisal); absent transitions are not edges.
4. The finite H0 bars of the Vietoris–Rips filtration on the shortest-path metric are the minimum-spanning-tree edge lengths lᵢ
   (scipy `minimum_spanning_tree`); the infinite bar is dropped.
5. **pe_h0 = −Σ qᵢ ln qᵢ / ln(#bars)**, qᵢ = lᵢ / Σl. NaN if the skeleton has under 8 notes, under 3 pitches, or under 2 bars.
No parameters; invariant to transposition and to the overall count scale.

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`pe_h0`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.676** (n 3999; bar 0.5, R09-5); R² on the 13 baselines 0.152; largest baseline ρ pc_entropy +0.26, n_pitch +0.25, range +0.22. Passes; not stopped.

Why it is tested: Card 1's construction (H0 = MST of the shortest-path metric; persistent entropy as evenness). Clean (R² 0.15).
Simplicity pushes the other way (ρ +0.26 with pc_entropy against a predicted +), and pc_entropy is frozen so the test stands if REP passes.

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,511 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **+**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(pe_h0) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: pc_entropy** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(pe_h0) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = +0.03 SD of z(y_cov) per SD of pe_h0** (an evenly knit skeleton travels intact). y_love: positive.
The round-1 kill "the literal 1/p reading takes the opposite sign" is dropped (Skeptic, accepted by the Geometer: ρ 0.87, one test).

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power pe_h0_links`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.723** | 0.057 | 0.880 | 0.0092 | 14,511 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `pe_h0_inv` (card 1's literal 1/p_sym length; measure reading with pc_entropy frozen; predicted +)
- pe_h0 without the frozen pc_entropy (measure reading, no extra; predicted +)
- all 13 baselines held (predicted +)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `pe_h0_links_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power pe_h0_links_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run pe_h0_links` (writes result.json; refuses unless this file is committed and pushed).
