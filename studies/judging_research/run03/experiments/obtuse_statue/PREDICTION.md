# The obtuse statue: minimum resistance curvature p_min, frozen before any outcome is joined

Run 03, 23 November 2026, by the chair. **After seeing results:** frozen after the bridge and curvature outcomes were read (Jason's rule: what can be tested tonight is tested tonight). A pass is a lead needing confirmation on unused songs, never a finding. No cover count, version, release, `first_year` or versions file was opened. "Chair" = a notes-only check on the 2,672 songs with ≥ 3 chords.

## Claim (G3; card 2, the circumcentre)
With resistances as squared lengths, a chord graph is a simplex; the node curvatures p are the barycentric coordinates of its circumcentre. If min p < 0 the circumcentre lies outside, beyond a hub chord: the statue is obtuse. **Extrapolation (the Geometer):** a hub chord means plain harmony centred on one chord, in line with chord surprise (−0.042), so within an artist, more obtuse songs are covered more.

## Rows, graph and model
Exactly as `experiments/bridge/PREDICTION.md`: the same rows, chord token, merging, wrap rule, moves M pooled over the song's clips, data-pack measures weighted by `n_mel`, the `within()` model, CR1 clustered SE, md5 artist halves. Songs where p_min is undefined are dropped before the rule of two or more songs per artist.

## Measure (Devriendt & Lambiotte 2022)
- A = 1 wherever M[a,b] + M[b,a] > 0 and a ≠ b (**unit weights**, undirected support).
- Keep the **largest connected piece** (most chords; ties to the piece with the lowest label from `scipy.sparse.csgraph.connected_components`). Drop the song if it has fewer than 3 chords (chair: 2 songs).
- Q = diag(A·1) − A; Q† = `numpy.linalg.pinv(Q)`; ω_ij = Q†_ii + Q†_jj − 2Q†_ij.
- p_i = 1 − ½ Σ_j A_ij ω_ij. Assert Σ p = 1 within 1e-8.
- **p_min = min_i p_i.** More negative = more obtuse.
- **Size** is removed inside the model by the same block as the curvature test: distinct-chord dummies (4…11, 12+), distinct links, log(clips per song).
- **Unit tests** (card 2): 4-cycle ¼; path of 4 min 0; star with 3 leaves −½; K4 ¼ (chair: all exact).

## Gate (before any outcome; failing either records "stopped", no outcome joined)
Raw p_min is mostly size (ρ −0.83 with distinct chords; chair), so the gate reads p_res, the residual of p_min after OLS on a constant plus the size block.
1. **Clip-to-clip:** for songs with 2+ clips, compute p_min on clip 1 and clip 2 alone (surprise-file order; each clip needs at least 3 chords in its largest piece); residualise the stacked values on a constant, that clip's distinct-chord dummies and links; Spearman between the two clips' residuals must be **≥ 0.20**. *Chair: 0.154 (1,166 pairs); raw, size included, 0.306.*
2. **Overlap:** |Spearman ρ| of p_res with each of the 17 data-pack measures, distinct chords, links and clips must be **≤ 0.7**, and R² of standardised p_min on the size block **≤ 0.8**. *Chair: largest |ρ| 0.075 (links); R² 0.65.*

Chair's verdict on the gate: **fails clip-to-clip (0.154 < 0.20); the chair expects this test to be recorded "stopped"**, with no outcome joined. The residual form was fixed before the chair computed it. If the script's gate passes, the rest applies unchanged.

## Model columns
p_min, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, the nine distinct-chord dummies.

## Prediction
**β = −0.02 SD of log(1 + covers) per SD of p_min**, within artist (the Geometer's figure): more negative p_min, more covers.

## Power
Printed before β: power = Φ(0.02/SE − 2.638) + Φ(−0.02/SE − 2.638). Chair: the size block leaves only 0.25 of p_min's within-artist variance, so SE ≈ 0.027 and **power ≈ 0.03**.

## Rules
Tonight counts six tests, so each needs **p < .05/6 = .0083, two-sided**.
- **Pass:** β < 0, p < .0083, and β < 0 in both artist halves.
- **Kill:** β > −0.01.
- **Unsettled:** anything else, including a split between halves.
- **Opposite sign** (β > 0, p < .0083): a new hypothesis, not a pass.
- If stopped, the other tests still need p < .0083.

## Reported, deciding nothing
Covers within 5 years and more than 10 years after `first_year`, as in the bridge experiment; β without `ch_ic_mean`; the model with disconnected songs dropped; ρ with tonic resistance H (chair +0.51) and with the bridge indicator B.

## What it cannot say
- **Power near zero:** even a true effect would almost never pass; only a kill informs, weakly.
- **After seeing results:** a pass is a lead for unused songs only.
- **Small graphs:** on 3 to 11 chords p mostly counts leaves and cut nodes; unit weights ignore move counts; direction is lost.
- **No cause; hits only; McGill untouched.**
