# Fresh songs, test 5: diatonicity |a₅|/a₀ on songs whose outcome has never been seen. Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Idea R04-G1 (the Geometer, run 04; status parked, "kept for fresh songs"). No outcome has been opened by the chair or by any brainstorm agent (see `../fresh_repetition/PREDICTION.md`). Figures marked *chair* come from notes-only checks.

**Shared rules:** `../fresh_repetition/PREDICTION.md` and `../common.py`, unless this file says otherwise.

**Tonight counts six tests. Each needs p < .05/6 = .00833, two-sided (z = 2.638).**

## Why it is tested
In run 04 its author withdrew it from the seen songs because its sign had been set after the fifths path leaned, and parked it **for fresh songs, holding the fifths path and the non-triad share**. Run 05 printed it once on the seen songs in place of the fifths path (+0.34 pp per SD, p .32, deciding nothing), and the fifths path itself was killed. Run 05's first principles recommended deleting the pair; Jason has not ruled. Tonight is the first night with fresh songs, so under Jason's rule it runs, in its author's form, ranked last.

## Claim (run 04, the Geometer; Amiot's Theorem 1 with Lemma 2)
Harmony held in one diatonic region travels: a cover can re-key, revoice or invert it, and the fifth Fourier coefficient's magnitude is unchanged by all three. **Extrapolation:** within an artist's own songs, more diatonic harmony goes with more uptake by another artist.

## Measure D5 (frozen in run05/experiments/fifths_path/PREDICTION.md; `common.D5_clip`)
v_x = Σ (offset − onset) over harmony events whose `chord_pcs` contain pitch class x (duration > 0 only); **D5 = |Σ_x v_x e^{−2πi·5x/12}| / Σ_x v_x**; no duration: no value. Song value: n_mel-weighted mean (`song_measure`; the plain mean when every n_mel is 0).

**Unit values** (must reproduce; one beat per chord, tonic C): a C major triad alone → **0.6440**; C, F, G triads → **0.5864**; C and A♭ triads → **0.3220**. Non-triad share NT (below): I, V7, vi, IV → **0.2500**.

*Chair:* all 9,588 seen rows have D5; seen mean 0.5253, **SD 0.0948** (the z scale). ρ with the fifths path FP −0.731 (over the 0.7 renaming line, hence FP is held).

## Held columns, frozen tonight
- **z(FP):** run 05's fifths path (`common.FP_song`; run 03's rules, pooled steps; the seen rows reproduce run 05's percentiles 0.449 / 0.714 / 1.197). Seen mean 0.7822, SD 0.3329. 60 fresh battery rows have no FP and drop.
- **z(NT), the non-triad share** (`common.NT_clip`): the share of harmony duration on events whose root_position_intervals are neither (4, 3) nor (3, 4); n_mel-weighted song mean. Run 04 named this control but never wrote it down; this is its frozen form. Seen mean 0.281, SD 0.3074; ρ(D5, NT) −0.215; its largest overlap with the pack measures is ch_ic_mean +0.69.
- z(ch_rep), then the shared controls. ch_ic_mean is left out (shared rule).

## Gate (notes only, on the seen rows; stop if it fails)
1. **Residual clip-to-clip:** among seen rows with two or more clips, D5, FP and NT on clip 1 alone and clip 2 alone (all finite); stack the pairs; OLS of D5 on a constant, FP and NT; Spearman of the clip-1 against the clip-2 residuals **≥ 0.20**. *Chair: 0.342 on 4,268 pairs* (raw 0.503; FP and NT explain 55% of clip D5).
2. **Overlap:** |Spearman| of song D5 with the 17 pack measures, n_ch, beats and clips per song **≤ 0.7**. *Chair: largest ch_ic_mean −0.423.* (FP is not in this list; it is held as a column instead.)

## Rows
The shared battery rows with D5, FP and NT: **5,707 rows = 4,472 seen + 1,235 fresh** (*chair*), fresh rows by 585 artists. Fresh clip 1 vs clip 2 agreement of raw D5: 0.395 on 432 pairs.

## Prediction
**β(z_fresh) on y_foreign = +0.5 pp per SD**, holding FP, NT and ch_rep. The sign is its author's. The size is the chair's translation: run 04 wrote +0.025 SD per SD on log covers, which has no direct equivalent here, and run 05's printed seen value, without FP held, was +0.34.

## Rules
- **Pass:** β > 0, two-sided p < .00833, β > 0 in both halves, conditional logit > 0 and converged.
- **Kill:** β ≤ 0. A kill closes R04-G1.
- **Opposite sign** (β < 0, p < .00833): killed; reported as a new hypothesis.
- **Unsettled:** anything else.

## Power (fake outcomes, `../power_fake.py`)
| | SE (pp) | Pass rate if +0.5 is true | Kill fires if true | Kill fires if 0 | Power at p < .05 |
|---|---|---|---|---|---|
| calibrated | 1.12 | 0.019 | 33% | 49% | 0.07 |
| homogeneous | 1.50 | 0.015 | 37% | 51% | 0.06 |

## Reported, deciding nothing
- D5 without FP and NT (run 05's printed form); z_seen; β on y; W01-J6a early and late uptake; karaoke/tribute removed; clique-collision drop; the fresh-only within-artist model.

## Order
1. Unit values. 2. Seen reproduction (D5 for 9,588; FP percentiles). 3. Gate (stop if it fails). 4. Notes-side power (bound 1.54 pp). 5. `common.validate_match`. 6. `common.load_battery_outcomes`. 7. Counts. 8. Clustered SE, power. 9. β, halves, logit, verdict. 10. Reported. 11. `result.json`.

## What it cannot say
As the shared file. D5 with FP held asks what diatonicity adds to the fifths path, which was itself killed; a pass would be a lead, not a finding.
