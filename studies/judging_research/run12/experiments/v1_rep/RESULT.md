# v1_rep: result (counted, rank 1 of 3)

**Verdict: UNSETTLED.**

## The rule, written first
- Prediction: β_D = −0.01, where D = z(FIT) − z(log1p N), on z(REP), within artist, exact first-year dummies.
- Pass: p < 0.0167, β_D < 0, both artist halves < 0.
- Killed (Jason's words, "predicts fitness no better than counts"): −0.01 outside β̂_D ± 1.96 SE **and** β̂_D ≥ 0.
- Otherwise unsettled.

## What came out (result.json)
- **β_D = −0.0117, SE 0.0073, p 0.108**; 95% range −0.026 to +0.003. 1,853 rows, 405 artists (sd D 0.382).
- Halves: −0.014 (SE 0.011, p .21) and −0.011 (SE 0.011, p .34). Both negative.
- Sign right, halves right, p not under 0.0167, so no pass. −0.01 sits inside the range and β̂ < 0, so no kill.
- K: 3 at freezing (α .0167). The after-seeing windows_lakh_after test brings the pass to K = 4 (α .0125); p .108 is above both, so nothing changes.

## Readings (uncounted)
- β on z(FIT): **−0.028** (SE 0.025, p .25).
- β on z(log1p N): **−0.016** (SE 0.019, p .38). Their difference is β_D.
- D with five-year bins: −0.008 (SE 0.0065, p .21).
- Share of rows with N = 0: 5.1%. corr(FIT, log1p N) on the rows: 0.927.

## How firm
The point estimate is almost exactly the prediction, but the realised SE (0.0073) is larger than the fake SE (0.0055), and power was 0.29. Neither reading on its own is distinguishable from zero.

## What it can and cannot say
With A → ∞ in the frozen fit, FIT within a first year is a fixed increasing function of N, so D is arithmetic: the curvature of digamma(r + N) against log(1 + N), which weighs the 0-to-1-cover step about twice as heavily. A negative β_D would only say REP's association sits a little more at the low-count end. It cannot show fitness beyond luck, and a kill would have indicted the estimator, not the notes. These songs are SEEN (run 11 joined REP to y_foreign).

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
