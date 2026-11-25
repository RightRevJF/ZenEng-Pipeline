# Is home the electrical hub? Tonic resistance H on the extensive margin (R03-I2). Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Backlog idea R03-I2 (status testing: unsettled on covers in run 03, β −0.019, p .19, halves −0.010 and −0.027), now testable on all 9,588 within-artist songs because tonight's full Hooktheory notes cover the songs not in Discogs-VI. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim (run 03, unchanged in direction)
Make the chord graph an electrical circuit with move counts as conductances. If every chord has low resistance to the home chord, there are many parallel routes home. **Extrapolation:** an arranger can take detours without getting lost, so within an artist's own songs, songs whose home is central (low H) are more often taken up by another artist.

## Measure H (frozen; run 03's rules, read from the raw annotations)
1. **Tokens per clip:** tonic = `keys[0].tonic_pitch_class` (0 if none); harmony events sorted by `onset`; token = ((root − tonic) mod 12)·9 + qual(root_position_intervals), with run 03's qual table (see `fifths_path/PREDICTION.md`; anything else → 8); consecutive equal tokens merged.
2. **Moves pooled over the song's clips:** M[a,b] = the number of moves a → b, counting every s[i] → s[i+1] in each clip's merged sequence plus the wrap s[−1] → s[0] when the two differ.
3. **Conductance** C = M + Mᵀ with the diagonal set to 0. Distinct chords n = number of distinct tokens; links = number of unordered pairs with C > 0.
4. **Drop the song** if n < 3. **T** = the token with root 0 (token // 9 == 0) with the largest row sum of C; ties go to the smaller token. **No such token: drop the song.**
5. Keep the connected piece of C containing T (`scipy.sparse.csgraph.connected_components`, undirected); **drop the song if it has fewer than 3 chords.**
6. On that piece: Q = diag(C·1) − C; Q† = `numpy.linalg.pinv(Q)`; ω_xy = Q†_xx + Q†_yy − 2Q†_xy; π_x = (C·1)_x / Σ C.
7. **H = Σ_x π_x ω_xT / Σ_x Σ_y π_x π_y ω_xy.** No factor ½. H < 1 means home is more central than the average chord.

**Unit tests** (unit weights; must reproduce exactly): 5-cycle H = 1; star with T at the hub H = 0.6; star with T on a leaf H = 1.4; and the same stars written as token clips [[0,18],[0,27],[0,45]] → 0.6 and [[18,0],[18,27],[18,45]] → 1.4.

*Chair:* 9,009 of the 9,588 songs have H (dropped: 278 with under 3 distinct chords, 266 with no root-0 chord, 35 with T's piece under 3 chords); 10th / 50th / 90th percentiles 0.624 / 0.818 / 1.143.

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists; halves `r['half']`. Songs with no H drop; artists are not re-filtered.

## Outcome
**Primary: y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign = NaN are dropped from every model.

## Columns
- z(H) over the songs with a value (population SD).
- z(`ch_rep`), z(`ch_ic_mean`) over the 9,588 rows.
- **Size, as in run 03** (H tracks size: raw ρ −0.49 with distinct chords, *chair*): dummies for distinct chords = 4, …, 11 and 12+ (3 is the reference), and links (a count, entered linearly).
- Run 04's control block, `common.controls(rows)`.
- Artist fixed effect.

## Model
LPM via `common.lpm`; the same within each artist half; conditional logit via `common.cond_logit` with the same columns, not demeaned (install statsmodels or maximise the exact likelihood with scipy; print drops and convergence; no convergence, no pass).

## Gate (notes only; before `load_outcomes`; failing records "stopped") — run 03's gate
1. **Clip-to-clip, residualised:** among songs with H defined and 2+ clips, compute H on clip 1 alone and on clip 2 alone (load_rows order; both must be defined). Stack the 2P values; OLS on a constant, that clip's distinct-chord dummies (4…11, 12+) and that clip's links; Spearman between the clip-1 and clip-2 residuals **≥ 0.20**. *Chair: 0.203 on 3,512 pairs (raw 0.259).* This is the narrowest pass of the night; the script must follow the rule exactly and stop if it falls below 0.20.
2. **Overlap:** H_res = residual of song H after OLS on a constant, the distinct-chord dummies, links and ln(clips per song). |Spearman| of H_res with the 17 data-pack measures, `n_ch`, `beats`, clips per song, distinct chords and links **≤ 0.7**, and R² of H on that size block **≤ 0.8**. *Chair: largest |ρ| 0.081 (beats); R² 0.156.*

Chair's verdict: passes (narrowly on stability).

## Prediction
**β(H) on y_foreign = −0.6 percentage points per SD** (home more central, more uptake), within artist.

## Rules
- **Pass:** β < 0, p < .00714, β < 0 in both halves, conditional logit < 0 and converged.
- **Kill:** β > −0.2. A kill closes R03-I2.
- **Opposite sign** (β > 0, p < .00714): killed; reported as a new hypothesis, not a pass.
- **Unsettled:** anything else.

## Power (notes side; the script prints power again from its own SE before any β)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²). *Chair:* residual share 0.652 on 9,009 songs, **SE ≈ 0.54 pp; power at −0.6 and p < .00714 = 0.06** (0.20 at p < .05). Clip-to-clip agreement near 0.20 means a true effect shows attenuated. The kill line fires about 23% of the time if −0.6 is true, 64% if zero.

## Reported, deciding nothing
- H without z(`ch_ic_mean`).
- Songs whose T piece is not the whole graph dropped.
- ρ(H, A) (*chair* +0.28; A is `arrow_of_time`'s measure).
- β(H) on y; intensive margin (z(log(1 + covers)) among songs with y = 100, non-null covers and a first_year, same columns plus `first_year`); y_foreign with "karaoke"/"tribute" sets removed.

## Order
1. Unit tests. 2. Rows, tokens, H, distinct chords, links. 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes`. 6. Counts. 7. Clustered SE and power. 8. β, halves, conditional logit, verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- One-step, symmetrised graph (V→I counts as I→V); home relies on `keys[0]`.
- The matched songs' H was already tested on covers in run 03; the extensive contrast is new but the songs are not unseen. y_foreign is not lasting love. Low power. Hits only. The McGill hold-out is untouched.
