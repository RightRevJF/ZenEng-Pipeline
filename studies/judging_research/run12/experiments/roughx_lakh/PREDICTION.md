# roughx_lakh: overtone roughness of what sounds together, octaves removed (P11-4)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. No outcome was opened, and only a dry run on a synthetic outcome was made. Idea: **R12-I2 ROUGH_X (Inventor, round-2 form)**. **Status: ESTIMATE.** It passes its gate, but its power at .05/3 is 0.013, far under the floor. K = 3, α = .05/3 = 0.0167 for the counted tests.

## The measure (frozen; `build_lakh12.py`, key `ROUGH_X`)
At every beat (every 24th step), take the distinct pitches sounding on tracks 1-4. Then:
- **Partials:** n = 1..6 at n·f₀, with amplitude 0.88^(n−1).
- **Pair roughness (Sethares):** d = min(a, a′)·5·(e^(−3.51 s Δf) − e^(−5.75 s Δf)), with s = 0.24/(0.0207 f_low + 18.96).
- **Note-pair roughness:** the sum of d over the 36 partial pairs.
- **ROUGH_X:** the sum over all beats and over note pairs whose interval is **not** a multiple of 12, divided by the number of such pairs.
- **REG:** the mean over beats of the mean sounding pitch.
- **OCT:** the share of octave-multiple pairs.

Near-duplicate files are counted once.

## Gate (written before outcomes; `measure_gates12.json`)
- **The Inventor's own gate** is two-file stability with register held: the Spearman between the two files' residuals of ROUGH_X on REG, from an OLS over all kept files. Result: **0.354** (159 non-duplicate pairs; bar 0.20). **Passes**, so it is not "stopped".
- **Bare stability** is 0.299, and the largest overlap with an existing measure is NPB −0.13. **Passes.**

## Songs, outcome, model
- **Songs:** Lakh within-artist songs with every column finite, **5,699 songs, 1,627 artists**.
- **Outcome:** y_foreign.
- **Model:** OLS of z(y_foreign) on z(ROUGH_X) with artist FE, run 07's controls with year bins, and the Skeptic's Lakh controls (LNEV, NPB, ACT, NFILES).
- **Held, following the Inventor's round-2 list:** z(REG), z(OCT) and run 07's chord measures z(ch_rep, CH, A, H4m, cv_w, g, lnP, F, B). V and ln_chg are already in the base controls.
- Conditional logit for the sign; halves md5(artist) mod 2.

## Prediction
**β = −0.01.** Voicings whose overtones beat less travel further.

## Verdict rules (they would apply if it were counted)
- **Pass:** p < 0.0167, β < 0, both halves < 0, and the conditional logit < 0.
- **Killed:** −0.01 lies outside β̂ ± 1.96 SE.

## Power (within-artist share 0.46; 300 draws, seed 12)
- At α 0.0167: power **0.013**, median fake SE 0.0210.
- At α 0.05: power 0.03.

## Readings
The bare form (run 07's controls only), predicted sign −. That is the Inventor's round-1 form, whose prediction was −0.02.

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run roughx_lakh`
