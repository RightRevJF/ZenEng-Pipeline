# lock_turns: LOCK: the dancer's footfall, contour turns on the beat (R10-I2). WAITS: runs first next pass

Run 10, 27 November 2026. Frozen by the chair before any outcome is joined: no outcome file was opened, `common10.load_outcomes` was not called and `harness10.py run` was not run. Idea: R10-I2 (the Inventor). **Status: COUNTED, but WAITS.** It is the ninth of nine counted tests frozen tonight (K = 9, α = .05/9 = 0.00556) and runs FIRST in the next pass (run 11), on split A, with this spec unchanged and this α (it belongs to run 10's family; run 11 does not count it in its own K). Do not run it in run 10. Reason: the standing cap of eight tests per pass (chair.md, "Order").

## The measure (frozen)

`measures_inventor.py`, `measure(t)`, key `LOCK` (helper `_runs`).
1. The expanded first setting's MIDI pitches with consecutive equal pitches merged, each run keeping its first note's beatpos;
   the tune is out (None) if it has under 16 notes or under 8 runs.
2. On a beat: |beatpos − round(beatpos)| < 1e-6.
3. Turning points: interior runs that are a strict local maximum or minimum.
4. **LOCK = mean(on a beat | turning point) − mean(on a beat | any run)**; NaN under 4 turning points. No parameters.

Cache: `/home/claude/dl/thesession/measures_run10.json` (built by `experiments/build_cache10.py` from `experiments/measures/`; splits A and C only), key **`LOCK`**. The test reads the cache; it does not recompute the measure.

Measure-side gates (chair, split A, notes only; `measure_gates10.json`): two-setting stability Spearman **0.741** (n 4000; bar 0.5, R09-5); R² on the 13 baselines 0.011; largest baseline ρ unison_share -0.08, step_share +0.08, pc_entropy +0.06. Passes; not stopped.

Why it is tested: Card 2's conservation gradient: if the melody turns where the beat is, its shape lives in the slots transmission
protects. The cleanest measure of the nine (R² 0.011; |ρ| ≤ 0.06 with every other counted measure).

## Songs

Split A of `common10.tunes()` (sha256 of 'thesession:<tune_id>', first hex digit 0–9), each tune's first ok setting, expanded (repeats played), with the measure and the frozen extras defined: **14,511 tunes** (`harness10.design`).

## Outcome

- **Primary: y_cov** = log(1 + number of distinct recording artists of the tune in recordings.csv), standardised over the rows.
- **Love reading: y_love** = log(tunebooks), on the tunes listed in tune_popularity.csv (10 or more tunebooks; a truncated sample), same model and halves; predicted sign **+**. Reported beside the test; decides nothing.

## Model and controls (common10.fit; frozen in common10.py)

OLS of z(y_cov) on z(LOCK) by Frisch–Waugh, with fixed effects for tune type, meter, mode (levels under 20 tunes pooled), first-posting year, composer (named composers with 2 or more analysed tunes), an indicator 'has a named composer', and the **frozen extra controls: none** (z-scored). Cluster-robust CR1 SEs by composer key (named) or the tune itself. Settings count is never a control. Second model: Poisson GLM of the artist count on z(LOCK) and the same columns (HC0), sign only.

Halves: md5 of the composer key (named) or of 'trad:<tune_id>', first hex digit even = half 0, odd = half 1 (`common10.half_of`).

## Prediction

**β = +0.03 SD of z(y_cov) per SD of LOCK**. y_love: positive.

## Verdict rules (common10.verdict)

- **Pass:** p < 0.00556 (.05/9), the estimate has the predicted sign, both halves have that sign, and the Poisson model has it too.
- **Killed:** the prediction (+0.03) lies outside the estimate's 95% range (β̂ ± 1.96 SE) (R07-3).
- **Unsettled:** otherwise.
- Counted because its power is at least 0.2 (R06-5).

## Power (from power.json, fake outcomes on the real rows, before any outcome)

`harness10.py power lock_turns`: y = β·z(x) + N(0, 1 − β²) with β = +0.03, the same model and extras, 300 draws, seed 10, α = 0.00556.

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.740** | 0.043 | 0.910 | 0.0089 | 14,511 |

K = 9 (every one of the nine candidates clears 0.2 at .05/9; chair.md has the K table). α = .05/9 = 0.00556.

## Readings (uncounted; frozen in spec.json; they decide nothing)

- holding range and n_pitch (extra reading; predicted +)
- reels only (subset type == reel; predicted +)
- all 13 baselines held (predicted +)

The first-poster fixed effect (the Skeptic's round 2, accepted by the authors) is not available in `harness10.py` (the design carries no username), so it is not frozen this pass; see chair.md.

## Confirmation on split C (rule written now, before any outcome)

If this test PASSES on split A, it is re-run once on split C (about 4,260 tunes, never joined to an outcome) with the identical spec except `"split": "C"`: the same measure, extras, readings, predicted sign and size, at α = .05 divided by (1 + the number of run-10 tests that went to C in run 10), since the other confirmations will already have run. It runs from a sibling folder `lock_turns_C/` holding this PREDICTION.md (with the C power added) and spec.json identical except `"split": "C"` and the C α; its power is computed on C with `harness10.py power lock_turns_C` at that α and committed and pushed before the C outcome is joined; the C verdict comes from the same `common10.verdict` (counted only at C power ≥ 0.2; otherwise an estimate, and the A pass stays a lead). **The C verdict is the finding.** If this test does not pass on A, it is not run on C. Split H stays sealed. (Notes-side preview: power on C at α .05 is in chair.md.)

## How to run (after this file is committed and pushed)

Run 11, first: `cd run10/experiments && python3 harness10.py run lock_turns` (writes result.json). Not in run 10.
