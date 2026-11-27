# vr4c_momentum: harmonic momentum, the variance ratio of the fifths root walk with the ii dropped (R09-I2 revised). ESTIMATE

Run 09, 27 November 2026. Frozen by the chair before any outcome is joined. **Status: ESTIMATE** (power 0.12 at α .05, K = 1;
withdrawn from the count by its author). Passes nothing, kills nothing.

## Measure (the Inventor's recipe B and `r09_vr4c.py`, copied into `measures09.py`: `vr4`, `vr4c`)
On run 08's change events: drop each event that is a m7 immediately followed by a d7 a fourth up (the ii of a ii-V). Take the roots,
merge consecutive equal roots, and form the steps s = ((7·r2 − 7·r1) mod 12), minus 12 if > 6 (−5..+6 fifths). Need ≥ 8 steps.
**VR4c = mean over k of (s_k + … + s_{k+3})² / (4 · mean s_k²)**. VR = 1 is a random walk, → 0 a loop that keeps coming home, > 1 a
chain that keeps going (a fifths chain gives 4; I–vi–ii–V gives 0). By card 1 this is the lead-lag area of the path sampled every
fourth change over 4 × that at every change. Song value = mean over measured charts.

## Songs, outcome, model
As `iiv_confirm09`: 1,245 songs with VR4c; y_cov; plain OLS HC1 on z(VR4c), **z(IIV)**, z(w_chr), z(ch_rep), z(V), z(ln_chg),
z(ln_bars), z(no_bars), genre and decade dummies; halves; Poisson second model.

## Prediction
**β = +0.02 SD per SD of VR4c, holding IIV and V** (the Inventor's round 2). *Extrapolation:* players carry tunes whose harmony travels.

## Power (printed again before the outcome)
0.12 at .05 (N 1,245, fake SE 0.032).

## Frozen reading
VR4 before the ii is dropped (round 1's measure), same columns, no prediction.

## Kill, were it counted
+0.02 outside the 95% range.
