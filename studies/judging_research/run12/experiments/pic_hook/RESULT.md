# pic_hook: result (counted, rank 3 of 3)

**Verdict: UNSETTLED.**

**Counted against the author's withdrawal.** The Listener withdrew PIC as counted in round 2. That withdrawal rested on power computed without the within-artist share (0.18; 0.173 recomputed). With the share (0.38), power at .0167 was 0.587, so the chair counted it under the power rule.

## The rule, written first
- Prediction: β = +0.03 on z(PIC), within artist, run 04's controls, step_share, mel_ic_mean, ln_notes and pc_entropy held.
- Pass: p < 0.0167, β > 0, both halves > 0, conditional logit > 0.
- Killed: +0.03 outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out (result.json)
- **β = +0.0152, SE 0.0125, p 0.23**; 95% range −0.009 to +0.040. 9,542 songs, 1,741 artists.
- Halves: +0.014 (p .44) and +0.015 (p .40). Conditional logit +0.073 (SE 0.061, p .23; 3,620 songs, 463 groups).
- Sign, halves and logit right; p far above 0.0167, so no pass. +0.03 inside the range, so no kill.
- K: 3 at freezing (α .0167); windows_lakh_after brings K to 4 (α .0125). Nothing changes.

## Readings (uncounted)
- PIC_REL (same extras): +0.017 (SE 0.014, p .21).
- PIC, round-1 form (ln_notes, pc_entropy only): +0.010 (SE 0.009, p .29).

## How firm
Consistent in direction everywhere, and about half the predicted size. The realised SE (0.0125) was a little above the fake SE (0.0113), which supports the share used in the power. The test was well powered for +0.03 and did not find it; it cannot rule out an effect of about +0.015.

## What it cannot say
These songs are re-spent (SEEN for chord and run 11 melody measures). PIC is tied to mel_ic_mean (ρ −0.63), which is held, so the estimate is what context gain adds beyond plain surprisal. Clips are not whole songs.

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
