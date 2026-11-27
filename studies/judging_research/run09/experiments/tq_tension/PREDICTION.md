# tq_tension: tension breathing TQ, the lead-lag area of the tritone channel (G09-1; card 1). ESTIMATE

Run 09, 27 November 2026. Frozen by the chair before any outcome is joined. **Status: ESTIMATE** (power 0.037 at α .05, K = 1;
its author and the Skeptic froze it as an estimate). Passes nothing, kills nothing.

## Measure (the Geometer's `g09_tq.py`, copied into `measures09.py`: `TQ`)
h_k = 1 if the k-th token's pitch-class set holds a tritone (some i with bits i and i + 6), else 0, on the Geometer's tokens
(non-empty bitmaps, repeats merged). Lead-lag path: lead = h_{k+1} and lag = h_k at doubled points. By card 1 (lead-lag transform),
its Lévy area is half the quadratic variation: |A| = ½ Σ (h_k − h_{k−1})². **TQ = |A| / (number of changes)**; nan if fewer than 6
tokens (the identity is asserted on every chart). Song value = mean over measured charts.

## Songs, outcome, model
As `iiv_confirm09`: 1,271 songs; y_cov; plain OLS HC1 on z(TQ), **z(IIV)**, z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars),
z(no_bars), genre and decade dummies (IIV and V held at the Skeptic's ruling: TQ tracks dominant density, ρ with IIV 0.55 here);
halves by composer key; `posthoc08.poisson_plain` second model.

## Prediction
**β = +0.01 SD per SD of TQ, holding IIV and V** (the Geometer's round 2).

## Power (printed again before the outcome)
0.037 at .05 (N 1,271, fake SE 0.036). It cannot be killed or passed at this size.

## Frozen reading
TQ without IIV, predicted **+0.03** (G09-1's first prediction); power 0.13.

## Kill, were it counted
+0.01 outside the 95% range.
