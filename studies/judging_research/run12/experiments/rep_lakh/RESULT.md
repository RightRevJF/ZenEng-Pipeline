# rep_lakh: result (uncounted estimate, rank 5)

**Status: ESTIMATE.** Power at .0167 was 0.070, far under the 0.2 floor. It replicates nothing and refutes nothing.

## The rule, written first (as if counted)
- Prediction: β = −0.02 on z(REP_L) (run 11's −0.03 shrunk), within artist, run 07's and the Skeptic's Lakh controls.
- Pass: p < 0.0167, β < 0, both halves < 0, conditional logit < 0. Killed: −0.02 outside β̂ ± 1.96 SE.

## What came out (result.json)
- **β = −0.022, SE 0.021, p 0.30**; 95% range −0.063 to +0.019. 5,848 songs, 1,661 artists; 40% taken up.
- Halves: −0.020 (p .50) and −0.023 (p .43).
- **The conditional logit failed** ("need covariance of parameters…"; β, SE, p NaN), so the sign check on it is missing.
- Had it been counted: unsettled (p far above .0167; −0.02 inside the range).

## Readings (uncounted)
- Bare (run 07's controls only): −0.013 (SE 0.019, p .49).
- ln events held only: −0.025 (SE 0.021, p .23).
- H1 (event pitch-class entropy, all controls): −0.033 (SE 0.024, p .18; 5,261 songs).

## How firm
Not firm. The point lands on the prediction and every form leans negative, which is what run 11's pass on Hooktheory clips would lead one to expect, but the SE is about the size of the effect. A zero effect is as compatible with these numbers as −0.02.

## What it cannot say
It cannot confirm run 11's REP pass on fresh songs; that pass still needs unseen melodies. REP_L shares variance with V (ρ 0.63) and the other controls, which is why the power was low. The skyline is a proxy for the melody.

Credit: Lakh MIDI / LPD (CC BY 4.0); Discogs-VI 20240701 (CC BY-SA 4.0).
