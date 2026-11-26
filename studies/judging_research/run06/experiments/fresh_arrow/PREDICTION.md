# Fresh songs, test 2: the arrow of time A on songs whose outcome has never been seen. Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Idea R05-A (status testing). No outcome has been opened by the chair or by any brainstorm agent (see `../fresh_repetition/PREDICTION.md` for the full list). Figures marked *chair* come from notes-only checks.

**Shared rules:** the fresh songs, the rows, the outcome, the validation step and the model are frozen in `../fresh_repetition/PREDICTION.md` and coded in `../common.py`. Everything there applies here unless this file says otherwise.

**Tonight counts six tests. Each needs p < .05/6 = .00833, two-sided (z = 2.638).**

## Why this test
Run 05 found A leaning the predicted way within artist on seen songs (+0.84 pp per SD, SE 0.40, p .035, not enough to pass), then the opposite way across single-song artists (−1.75, p .009; `run05/experiments/arrow_singletons`). The Skeptic's reading: across artists A reads style. **This test asks only the within-artist question, on fresh songs**: does the +0.84 lean hold where nobody has looked?

## Measure A (frozen in run05/experiments/arrow_of_time/PREDICTION.md; `common.A_clip`)
Chord pitch-class sets (`chord_pcs`) in onset order, consecutive equal sets collapsed to s₀ … s_K; **K < 6: no value**; n_ij = moves i → j with no wrap; **A = 1 − Σ min(n_ij, n_ji) / Σ n_ij**. Song value: mean over clips with a value, weighted by K.

**Unit values** (must reproduce): I–V–vi–IV ×4 → 1.0000; I–IV ×8 → 0.0667; I–V–I–IV ×4 → 0.0667.

*Chair:* the 9,588 seen rows reproduce run 05 (8,774 with a value; percentiles 0.333 / 0.833 / 1.000); seen mean 0.7589, **SD 0.2673** (the z scale). Fresh clip 1 vs clip 2 agreement 0.244 on 253 pairs (seen 0.302).

## Rows
The shared battery rows with a value of A: **4,920 rows = 4,032 seen + 888 fresh** (*chair*), fresh rows by 448 artists, 590 artists in all.

## Columns
z_fresh(A), z_seen(A), **z(ch_rep)** (seen scale), then the shared controls (run 04's block, ln_chg, V, has_mel, fresh). ln_chg was run 05's extra column for A and is in the shared block. ch_ic_mean is left out (shared rule).

## Prediction
**β(z_fresh) on y_foreign = +0.6 pp per SD** (run 05's frozen claim; the seen estimate was +0.84).

## Rules
- **Pass:** β > 0, two-sided p < .00833, β > 0 in both halves, conditional logit > 0 and converged.
- **Kill:** β ≤ 0.
- **Opposite sign** (β < 0, p < .00833): killed, and it joins arrow_singletons as evidence that vamps are what others take up.
- **Unsettled:** anything else.

## Power (fake outcomes, `../power_fake.py`)
| | SE (pp) | Pass rate if +0.6 is true | Kill fires if true | Kill fires if 0 | Power at p < .05 |
|---|---|---|---|---|---|
| calibrated | 1.06 | 0.022 | 28% | 48% | 0.09 |
| homogeneous | 1.43 | 0.018 | 35% | 46% | 0.07 |

Notes-side bound 1.44 pp. Nearly blind: only a large effect could pass.

## Reported, deciding nothing
- G2 (the back-and-forth share, run 05's definition) in place of A.
- z_seen; β on y; W01-J6a early and late uptake; karaoke/tribute removed; fresh rows whose clique is also a seen song's dropped; the fresh-only within-artist model (as in the shared file).
- The model without z(ch_rep).

## Order
1. Unit values; seen reproduction (8,774, percentiles). 2. Rows and columns. 3. Run 05's gate on the seen rows (`gate(rows, "A", extra={"ln_chg": …})`: 0.302, largest overlap ln_chg −0.154; stop if it fails). 4. Notes-side power. 5. `common.validate_match` (stop if it fails). 6. `common.load_battery_outcomes`. 7. Counts. 8. Clustered SE, power. 9. β, halves, logit, verdict. 10. Reported. 11. `result.json`.

## What it cannot say
As the shared file. Also: A leans towards 1 when changes are few, and fresh clips are shorter (mean chord tokens 10.6 against 14.4 seen); ln_chg and the chord-count bins hold it.
