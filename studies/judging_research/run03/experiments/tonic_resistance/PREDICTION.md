# Is home the electrical hub? Tonic resistance H: frozen before any outcome is joined

Run 03, 23 November 2026, by the chair. **After seeing results:** frozen after the bridge and curvature outcomes were read (Jason's rule: what can be tested tonight is tested tonight). A pass is a lead needing confirmation on unused songs, never a finding. No cover count, version, release, `first_year` or versions file was opened. "Chair" = a notes-only check on the 2,672 songs with ≥ 3 chords.

## Claim (I2; Devriendt & Lambiotte 2022, the commute-time reading)
Make the chord graph a circuit with move counts as conductances. If every chord has low resistance to the tonic chord, there are many parallel routes home. **Extrapolation:** an arranger can take detours without getting lost, so within an artist, songs whose home is central are covered more.

## Rows, graph and model
Exactly as `experiments/bridge/PREDICTION.md`: the same rows, chord token, merging, wrap rule, moves M pooled over the song's clips, data-pack measures weighted by `n_mel`, the `within()` model, CR1 clustered SE, md5 artist halves. Songs where H is undefined are dropped **before** the rule of two or more songs per artist is applied.

## Measure
- C = M + Mᵀ, diagonal zero (conductance = move count, both directions).
- **T** = the chord whose token has root 0 relative to the clip's tonic (`token // 9 == 0`) with the largest C row sum; ties go to the smaller token. **No such chord: drop the song** (chair: 80 songs).
- Keep the connected piece of C that contains T; drop the song if it has fewer than 3 chords.
- Q = diag(C·1) − C on that piece; Q† = `numpy.linalg.pinv(Q)`; ω_xy = Q†_xx + Q†_yy − 2Q†_xy.
- **π_x = (C·1)_x / Σ C**, the stationary distribution of the reversible walk on C.
- **H = Σ_x π_x ω_xT / Σ_x Σ_y π_x π_y ω_xy.** No factor ½ anywhere. The denominator is the π-weighted mean resistance to a π-random chord, so H < 1 means home is more central than the average chord.
- **Unit tests** (unit weights, must reproduce): 5-cycle H = 1; star with T at the hub H = 0.6; star with T on a leaf H = 1.4 (chair: all three exact).

## Gate (before any outcome; failing either records "stopped", no outcome joined)
H tracks size (raw ρ −0.44 with distinct chords; chair), which the model holds, so the gate reads H_res, the residual of H after OLS on a constant plus the size block (distinct-chord dummies 4…11, 12+, distinct links, log clips).
1. **Clip-to-clip:** for songs with 2+ clips, compute H on clip 1 and on clip 2 alone (surprise-file order; each clip must give a defined H); residualise the stacked values on a constant, that clip's distinct-chord dummies and links; Spearman between the two clips' residuals must be **≥ 0.20**. *Chair: 0.247 (1,057 pairs); raw 0.273.*
2. **Overlap:** |Spearman ρ| of H_res with each of the 17 data-pack measures, distinct chords, links and clips must be **≤ 0.7**, and R² of standardised H on the size block **≤ 0.8**. *Chair: largest |ρ| 0.083 (`length_variety`); ch_ic_mean +0.06; R² 0.10.*

Chair's verdict on the gate: **passes**. Also printed, deciding nothing: ρ(H, p_min) = +0.51 (chair), the overlap with `obtuse_statue`.

## Model columns
H, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, the nine distinct-chord dummies.

## Prediction
**β = −0.03 SD of log(1 + covers) per SD of H**, within artist (the Inventor's figure). H has a **negative** coefficient: lower H (home central), more covers.

## Power
Printed before β: power = Φ(0.03/SE − 2.638) + Φ(−0.03/SE − 2.638). Chair: SE ≈ 0.0165 (the bridge test's 0.016 scaled by H's leftover within-artist variance, 0.66 per row), **power ≈ 0.21**. Clip-to-clip agreement of 0.25 means a true −0.03 would show nearer −0.015.

## Rules
Tonight counts six tests, so each needs **p < .05/6 = .0083, two-sided**.
- **Pass:** β < 0, p < .0083, and β < 0 in both artist halves.
- **Kill:** β > −0.01 (wrong sign or weaker than 0.01 in the predicted direction).
- **Unsettled:** anything else, including a split between halves.
- **Opposite sign** (β > 0, p < .0083): a new hypothesis, not a pass.
- The threshold stays .0083 whatever happens to the other five tests.

## Reported, deciding nothing
Covers within 5 years and more than 10 years after `first_year`, as in the bridge experiment; β without `ch_ic_mean`; songs whose T piece is not the whole graph dropped; counts per half.

## What it cannot say
- **Low power:** a null clears nothing.
- **After seeing results:** frozen once two outcomes were known; a pass is a lead for unused songs only.
- **No cause:** hits only, era and singles differ within artist.
- **Graph limits:** one step, symmetrised (V→I = I→V), 3 to 11 chords; T relies on `keys[0]`.
- **McGill:** the hold-out is untouched.
