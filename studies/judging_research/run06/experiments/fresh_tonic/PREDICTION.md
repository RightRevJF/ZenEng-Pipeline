# Fresh songs, test 4: tonic resistance H on songs whose outcome has never been seen. Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Idea R03-I2 (status testing). No outcome has been opened by the chair or by any brainstorm agent (see `../fresh_repetition/PREDICTION.md`). Figures marked *chair* come from notes-only checks.

**Shared rules:** `../fresh_repetition/PREDICTION.md` and `../common.py`, unless this file says otherwise.

**Tonight counts six tests. Each needs p < .05/6 = .00833, two-sided (z = 2.638).**

## Why it is tested, though retirement was recommended
Run 05 left H unsettled (−0.23 pp per SD against a prediction of −0.6; kill line −0.2) and its first principles recommended retiring it (gate 0.203, power 0.09). Retiring an idea is Jason's decision, and he has not made it. His standing rule is that every idea that can be tested on the data at hand is tested, and tonight's fresh songs are new data that R03-I2 has never met. So it runs, ranked low. If Jason retires it, this test is moot and the threshold stays as frozen.

## Measure H (frozen in run05/experiments/tonic_resistance/PREDICTION.md; `common.H_song`)
Run 03's key-relative tokens (`common.tokens_rel`); moves pooled over the song's clips, with the wrap when last ≠ first; conductance C = M + Mᵀ, diagonal 0; drop if fewer than 3 distinct tokens, no root-0 token, or home's connected piece has fewer than 3 chords; T = the root-0 token with the largest row sum (ties to the smaller token); **H = Σ_x π_x ω_xT / Σ_x Σ_y π_x π_y ω_xy** with effective resistances ω from the pseudo-inverse Laplacian.

**Unit tests** (must reproduce): 5-cycle 1.0; star with T at the hub 0.6; T on a leaf 1.4; the same stars as token clips 0.6 and 1.4.

*Chair:* the seen rows reproduce run 05 exactly (9,009 of 9,588 with H; percentiles 0.624 / 0.818 / 1.143); seen mean 0.870, **SD 0.2583** (the z scale).

## Rows
The shared battery rows with H: **5,144 rows = 4,147 seen + 997 fresh** (*chair*), fresh rows by 527 artists; 298 fresh battery rows have no H (mostly fewer than 3 distinct chords).

## Columns
z_fresh(H), z_seen(H), z(ch_rep), **run 03's size columns: distinct-token dummies 4 … 11 and 12+ (3 the reference) and links** (as run 05), then the shared controls. ch_ic_mean is left out (shared rule).

## Prediction
**β(z_fresh) on y_foreign = −0.6 pp per SD** (home more central, more uptake), run 05's claim.

## Rules
- **Pass:** β < 0, two-sided p < .00833, β < 0 in both halves, conditional logit < 0 and converged.
- **Kill:** β ≥ 0. A kill closes R03-I2 (its seen reading already sat at the kill line).
- **Opposite sign** (β > 0, p < .00833): killed; reported as a new hypothesis.
- **Unsettled:** anything else.

## Power (fake outcomes, `../power_fake.py`)
| | SE (pp) | Pass rate if −0.6 is true | Kill fires if true | Kill fires if 0 | Power at p < .05 |
|---|---|---|---|---|---|
| calibrated | 0.85 | 0.042 | 26% | 48% | 0.11 |
| homogeneous | 1.12 | 0.050 | 30% | 50% | 0.08 |

H has a long right tail on fresh songs (z up to 13.5). In the homogeneous fake null, 1.4% of draws were significant at p < .00833 (nominal 0.8%), so the SE runs a little small; the halves rule guards against a single artist carrying it.

## Gate
Run 05's gate on the seen rows, exactly as `run05/experiments/tonic_resistance/PREDICTION.md` states it (residualised clip-to-clip ≥ 0.20; *chair* 0.203 on 3,512 pairs; overlap and size R² as there). Stop if it fails. *Chair:* on fresh songs the same residualised agreement is 0.182 on 243 pairs (raw 0.213). This is reported, not gated: the gate belongs to the measure and was passed on the seen songs, and 243 pairs give it an SE of about 0.06.

## Reported, deciding nothing
- z_seen; β on y; W01-J6a early and late uptake; karaoke/tribute removed; clique-collision drop; the fresh-only within-artist model.
- Fresh rows whose home piece is not the whole graph dropped. ρ(H, A) on the fresh rows.

## Order
1. Unit tests. 2. Seen reproduction (9,009; percentiles). 3. Gate on the seen rows (stop if it fails). 4. Notes-side power (bound 1.20 pp). 5. `common.validate_match`. 6. `common.load_battery_outcomes`. 7. Counts. 8. Clustered SE, power. 9. β, halves, logit, verdict. 10. Reported. 11. `result.json`.

## What it cannot say
As the shared file. The narrowest gate of run 05, now on chords-only clips with few distinct chords (the commonest fresh sizes are 3 to 6 tokens).
