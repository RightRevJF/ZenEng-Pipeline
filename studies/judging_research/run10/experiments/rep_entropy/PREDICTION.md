# rep_entropy: REP: simpler tunes spread (McBride & Leroi's pitch-class entropy), the replication baseline

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: REP (the Skeptic, round 2; McBride & Leroi, run 02 card 2). **Status: COUNTED** (rank 1 of 9). K = 9, α = .05/9 = 0.00556 (two-sided p).

## The measure (frozen)

`pc_entropy` from `common10.baseline(mel, tonic_pc)` (cache key `pc_entropy`): the Shannon entropy, in bits, of the
duration-weighted pitch-class distribution of the expanded first setting (each note adds its duration in quarter notes to the
class MIDI mod 12). No parameters. It is one of the 13 renaming baselines, so the renaming gate does not apply to it.

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`pc_entropy`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.83** (n 4000; bar 0.5, R09-5); R² on the 13 baselines 0.732; largest baseline ρ n_pc +0.72, n_pitch +0.48, tonic_share -0.40. Passes; not stopped.

Why it is tested: McBride & Leroi found on this same site that simpler tunes (fewer distinct pitches, fewer notes) spread a little
better. If that known effect cannot be seen on this design at power 0.71, every null below means little; if it passes, every
measure that leans on pc_entropy has to beat it with pc_entropy frozen (pe_h0_links and core_typical do freeze it).

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,511 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **−**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(pc_entropy) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: none** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(pc_entropy) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = −0.03 SD of z(y_cov) per SD of pc_entropy** (simpler spreads). y_love: negative.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (-0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power rep_entropy`: y = β·z(x) + N(0, 1 − β²) with β = -0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.713** | 0.017 | 0.920 | 0.0093 | 14,511 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- `density` (notes per bar, measure reading, no extra; predicted −)
- `n_pc` (measure reading; predicted −)
- `ln_notes` (measure reading; predicted −; McBride & Leroi's 'fewer notes')
- pc_entropy holding density (extra reading; predicted −)
- all 13 baselines held (pc_entropy with the other 12 frozen; predicted −)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by the number of run-10 tests that passed on A (and so go to C). It runs from a sibling folder `rep_entropy_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power rep_entropy_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

`cd run10/experiments && python3 harness10.py run rep_entropy` (writes result.json; refuses unless this file is committed and pushed).
