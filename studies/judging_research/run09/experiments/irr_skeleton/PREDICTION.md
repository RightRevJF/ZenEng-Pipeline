# irr_skeleton: the skeleton the signature sees, IRR (R09-I1; card 1, uniqueness up to tree-like paths). ESTIMATE

Run 09, 27 November 2026. Frozen by the chair before any outcome is joined. **Status: ESTIMATE** (power 0.067 at α .05, K = 1;
withdrawn from the count by its author in round 2, a withdrawal the chair respects). Passes nothing, kills nothing.

## Measure (the Inventor's recipe A, copied into `measures09.py`: `irr`)
On run 08's change tokens ((root, bitmap), repeats merged): stack = [t0]; for each later token t, if the stack has ≥ 2 entries and
stack[−2] = t, pop; else push t. **IRR = (len(stack) − 1) / n_chg**, open walk (no wrap). A B A collapses to A (a retraced excursion,
invisible to the signature by the Hambly–Lyons theorem); A B C A survives. Unit tests: a vamp C G C G C gives 0; C F C G F C gives
0.6; A B C A gives 1. Song value = mean over measured charts. Caveat (the author's): IRR ≈ 1 − 2 × the local back-and-forth share;
the theorem gives the name, the count is simple.

## Songs, outcome, model
As `iiv_confirm09`: 1,271 songs; y_cov; plain OLS HC1 on z(IRR), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), z(no_bars),
genre and decade dummies (ch_rep, V and ln_chg held at the Skeptic's ruling); halves; Poisson second model.

## Prediction
**β = +0.02 SD per SD of IRR** (the Inventor's round 2, revised from +0.03). *Extrapolation:* if a song is remembered as a shape,
retracings are scaffolding and the irreducible walk is the statue.

## Power (printed again before the outcome)
0.067 at .05 (N 1,271, fake SE 0.034).

## Frozen reading
IRR on chart-provenance songs only (N 1,075), no prediction.

## Kill, were it counted
+0.02 outside the 95% range.
