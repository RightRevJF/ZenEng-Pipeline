# fifths_lakh: result (stopped at the gate; uncounted estimate, rank 6)

**Status: STOPPED, run as an estimate.** E5_L's overlap with REP_L (the skyline's pitch-class entropy) is ρ −0.708, over the 0.70 bar written before outcomes; power at .0167 was also only 0.070. Label: "stopped; partly renames REP".

## The rule, written first (as if counted)
- Prediction: β(z E5_L) = +0.02 (+0.01 to +0.03), REST_L and TOP_L held, within artist, Lakh controls; and b_E5 > b_REST on the raw scale.
- Pass: p < 0.0167, β > 0, both halves > 0, conditional logit > 0, b_E5 − b_REST > 0.
- Killed: +0.02 outside β̂ ± 1.96 SE, or b_E5 − b_REST + 1.96 SE < 0.

## What came out (result.json)
- **β = +0.045, SE 0.021, p 0.037**; 95% range +0.003 to +0.086. 5,848 songs, 1,661 artists.
- Halves: +0.073 (p .013) and +0.014 (p .65).
- **The conditional logit failed** (NaN; "need covariance of parameters…").
- **Raw Wald comparison:** b_E5 0.159, b_REST 0.036, **difference +0.123, SE 0.076, p 0.11**. Not significantly below zero, so the second kill clause does not fire.
- Had it been counted: unsettled (p above .0167; +0.02 inside the range).

## Readings (uncounted)
- E5_L with REST_L only held: +0.035 (SE 0.018, p .054).
- Hooktheory G_E5 (G_REST, tonic_share held): **−0.003** (SE 0.010, p .78; 9,586 songs); G_REST +0.026 (p .025).

## How firm
Not firm. The Lakh estimate is positive and larger than predicted, but it comes mostly from one artist half, the logit is missing, the Wald difference is within noise, and the Hooktheory reading points the other way.

## What it cannot say
Because E5_L is close to the negative of REP_L, a positive E5_L is largely REP's leaning negative sign seen again. It cannot show that the fifths axis matters beyond pitch-class concentration.

Credit: Lakh MIDI / LPD (CC BY 4.0); Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
