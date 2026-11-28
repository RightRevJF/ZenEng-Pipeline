# fifths_lakh: the Parseval split of pitch-class concentration; is the fifths axis what matters? (R12-G1)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. No outcome was opened, and only a dry run on a synthetic outcome was made. Idea: **R12-G1 FIFTHS (Geometer), in its round-2 form.** **Status: ESTIMATE, stopped at the gate.**

E5_L's overlap with REP_L is ρ = −0.708, over the 0.70 bar. That bar was written before outcomes and treats REP's twins as the baseline of this pass, as pc_entropy is on Hooktheory; the Geometer's own check gave −0.71. Separately, its power at .05/3 is 0.070, under the floor. It is run as an uncounted estimate, labelled "stopped; partly renames REP". K = 3, α = .05/3 = 0.0167 for the counted tests.

## The measure (frozen; `build_lakh12.py`)
- **p:** the skyline's duration-weighted pitch-class profile, the same one as REP_L.
- **Fourier coefficients:** f_k = Σ p_j e^(−2πijk/12).
- **Concentration:** C_L = 12Σp² − 1 = 2Σ_{k≤5}|f_k|² + |f_6|².
- **E5_L** = 2|f_5|², the energy on the fifths axis. **REST_L** = C_L − E5_L.
- **TOP_L** = max p, the largest pitch-class share. The Geometer holds it in round 2.

Gate: stability 0.566 (159 pairs); largest overlap REP_L −0.708; **fails on overlap**.

## Songs, outcome, model
- **Songs:** Lakh within-artist songs, **5,848, in 1,661 artists**.
- **Outcome:** y_foreign.
- **Model:** OLS of z(y_foreign) on z(E5_L), with **z(REST_L) and z(TOP_L) held**, plus artist FE, run 07's controls with year bins, and the Skeptic's Lakh controls (LNEV, NPB, ACT, NFILES).
- CR1 SEs by artist; conditional logit for the sign; halves md5(artist) mod 2.
- **Wald test (the Geometer's "is it C renamed?").** E5_L, REST_L and TOP_L enter one model on their **raw** scale, and the test reads b_E5 − b_REST with its cluster-robust SE.

## Prediction
- **β(z E5_L) = +0.02** (range +0.01 to +0.03), with REST_L and TOP_L held.
- **b_E5 > b_REST** on the raw scale.

## Verdict rules (they would apply if it were counted)
- **Pass:** all of the following hold:
  - p < 0.0167;
  - β > 0;
  - both halves > 0;
  - the conditional logit > 0;
  - b_E5 − b_REST > 0.
- **Killed:** either condition kills it.
  - +0.02 lies outside β̂ ± 1.96 SE.
  - b_E5 − b_REST + 1.96 SE < 0.

The Geometer's "b_E5 ≤ b_REST" kill is put in the range form of R07-3: a kill needs evidence, not only a point estimate.

## Power (within-artist share 0.46; 300 draws, seed 12)
- **α 0.0167:** power **0.070**, median fake SE 0.0193.
- **α 0.05:** power 0.137.

## Readings (uncounted)
- **Hooktheory:** G_E5 (m_geometer on the clips) with G_REST and tonic_share held; y_foreign within artist with run 04's controls; predicted sign +. Clip stability 0.311; overlap pc_entropy −0.61. These songs are re-spent, which is why the Geometer made this the uncounted side.
- **Lakh:** E5_L with REST_L only held.

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run fifths_lakh`
