# typ_typical: distance from the repertoire's expected signature, TYP (R09-I3 revised; card 1). ESTIMATE

Run 09, 27 November 2026. Frozen by the chair before any outcome is joined. **Status: ESTIMATE** (power 0.067 at α .05, K = 1;
withdrawn from the count by its author). Passes nothing, kills nothing.

## Measure (the Inventor's recipe C, copied into `measures09.py`: `areas`, `typicality`)
- At each change token k (run 08 tokens): τ_k = cumulative duration before the token / total duration (uncollapsed events);
  u_k = running sum of the fifths steps (−5..+6; a quality-only change has step 0); h_k = 1 − |Σ_{p∈set} e^{−2πi·5p/12}| / |set|
  (set relative to the root); q_k = +1 if bit 4, else −1 if bit 3, else 0.
- Rectilinear path: hold (τ moves to the next onset, the others fixed), then jump; end at τ = 1; translate to start at 0.
- The six level-2 Lévy areas A_ij = ½ Σ (x̃ⁱ_{k−1} x̃ʲ_k − x̃ⁱ_k x̃ʲ_{k−1}); the three without τ divided by n_chg. A chart with an
  empty-bitmap token has no areas.
- **Reference (the Inventor's round 2, the Skeptic's point):** within the chart's COARSE GENRE (`common09.coarse_genre`: jazz, pop,
  biab, wikifonia, other), over every chart of `common09.load_charts()` with six finite areas (reference sizes: jazz 14,651; pop
  7,346; biab 4,965; wikifonia 2,398; other 2,155). F_j = (rank + 0.5)/n per area (ties broken by sorted chart id).
- **TYP = mean over the six areas of |2F_j − 1|** (0 = at the centre of the genre's shapes, 1 = at its edge). Song value = mean over
  measured charts. TYPM (Mahalanobis on normal scores, the genre's covariance) is the second reading.

## Songs, outcome, model
As `iiv_confirm09`: 1,271 songs; y_cov; plain OLS HC1 on z(TYP), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), z(no_bars),
genre and decade dummies (V held: ρ with V 0.58 here); halves; Poisson second model.

## Prediction
**β = −0.02 SD per SD of TYP** (typical songs covered more). *Extrapolation, from evolution:* stabilising selection on copies.

## Power (printed again before the outcome)
0.067 at .05 (N 1,271, fake SE 0.034).

## Frozen reading
TYPM, predicted −0.02 (power 0.087).

## Kill, were it counted
−0.02 outside the 95% range.
