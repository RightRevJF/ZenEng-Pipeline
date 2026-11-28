# core_typical: core_ic: a typical skeleton (L2 in the Skeptic's form; card 2's typicality test)

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: L2 (the Listener), counted as core_ic at the Skeptic's request; TSG runs as an estimate inside this folder. **Status: COUNTED** (rank 5 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`measures_listener.py`, `measure(t)`, key `core_ic` (helpers `_seqs`, `_bigram`, `corpus`, `_corp_for`, `_lp`).
1. Skeleton: the pitch classes relative to the tonic ((MIDI − tonic_pc) mod 12) of the notes whose onset is on a beat (|beatpos − round| < 1e-6), in order, repeats NOT merged.
2. Corpus model: a bigram over the 12 relative classes, summed over the skeletons of all split-A first settings of the tune's TYPE,
   leave-one-out (the tune's own first-setting counts subtracted). p(b | a) = (count + 1) / (row total + 12).
3. **core_ic = mean over the skeleton's transitions of −log₂ p(b | a)**, in bits. No fitted settings (add-one only).
The listener's `measure` returns None (tune not in the test) when the merged surface has under 16 notes, the skeleton under 8,
there are no off-beat notes, or the pitch graph is degenerate: 98 split-A tunes.
For split C (confirmation only) the corpus is split A in full; a C tune is not in it, so nothing is subtracted.

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`core_ic`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.569** (n 4000; bar 0.5, R09-5); R² on the 13 baselines 0.209; largest baseline ρ pc_entropy +0.36, tonic_share -0.32, n_pc +0.27. Passes; not stopped.

Why it is tested: Card 2's skeptical reading made testable: if what is conserved is the typical, does a typical skeleton spread?
pc_entropy is frozen (ρ +0.36, simplicity's direction), so a pass must beat REP. The Listener's TSG was mostly −surf_ic (ρ −0.73 here),
and off-beat notes are where transcribers differ; it runs as an estimate.

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,413 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **−**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(core_ic) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: pc_entropy** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(core_ic) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = −0.03 SD of z(y_cov) per SD of core_ic** (a more predictable, typical skeleton spreads). y_love: negative.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power core_typical`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.510** | 0.043 | 0.810 | 0.0112 | 14,413 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- **TSG estimate (L2's original):** key `tsg` = core_ic − surf_ic, pc_entropy frozen, predicted −0.03; uncounted
- `surf_ic` alone (mean corpus surprisal of off-beat notes under the type's surface bigram, merged repeats), pc_entropy frozen; predicted at most weakly +
- holding n_pc as well (extra reading; predicted −)
- all 13 baselines held (predicted −)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `core_typical_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power core_typical_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run core_typical` (writes result.json; refuses unless this file is committed and pushed).
