# Harmonic chirality: result

Run 06, 26 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 08b5167 before any outcome was joined. Code: `test.py`. Numbers: `result.json`. The run took about 2 minutes.

## What was predicted
Put each chord's root on the circle of fifths. A chord progression then traces a path around that circle, and the area it sweeps has a sign. Falling-fifth progressions (ii–V–I) turn **clockwise**, which gives a negative value. I–V–vi–IV turns **counterclockwise**, which gives a positive value. The Inventor's prediction: **comparing songs by the same artist, the songs that turn clockwise are more often recorded by another artist**, by **0.6 percentage points per standard deviation** of the measure (written β = −0.6).

To pass, the test needed all of these: a negative slope with p below .00833 (tonight's shared threshold, .05/6, two-sided); a negative slope in both random halves of the artists; and a conditional logit, a second kind of model that serves as a sign check, that is negative and converged. The test would be killed if the slope came out above −0.2, meaning the wrong sign or too weak. Any other outcome is "unsettled".

## Checks before the outcome was joined
- **Unit values:** all seven hand-built progressions gave exactly the frozen values, including the open and wrapped forms and the arrow A (for example I–V–vi–IV ×4 = +0.1167, ii–V–I ×5 = −0.0549, and I–V ×2 has no value).
- **Counts:** all reproduced exactly. 8,774 of 9,588 songs have a value. They come from 1,727 artists, split 878 / 849 between the halves. The 10th, 50th and 90th percentiles are −0.083, +0.005 and +0.104. The mean is +0.0078 and the SD 0.0771. 53% of songs are above 0 and 2% are exactly 0. The open and wrapped forms correlate at ρ 0.918. Within artists, R² is 0.009.
- **Gate:** passed. Clip 1 and clip 2 of the same song agree at 0.252 over 3,294 pairs, against a minimum of 0.20. The largest overlap with an existing measure is ch_ic_mean at −0.141, against a maximum of 0.7. The overlap is +0.07 with ch_rep, +0.07 with A, −0.12 with V and −0.03 with ln_chg.
- **Power, printed before the estimate:** the fake-outcome simulation gives an SE of 0.38 pp. At that SE, power to detect −0.6 at p < .00833 is 0.15, and 0.35 at p < .05. The notes-side bound is 0.514 pp. Power is far below run 03's proposed 0.5 floor, which is printed but does not block.

## What came out

| | Estimate (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **Primary, within artist** (8,772 songs, 1,726 artists) | **−0.30** | 0.38 | 0.42 | −1.05 to +0.44 |
| Half 0 (4,242 songs, 878 artists) | −0.62 | 0.58 | 0.28 | |
| Half 1 (4,530 songs, 848 artists) | +0.03 | 0.49 | 0.96 | |
| Conditional logit (log-odds per SD; 3,186 songs, 425 artists) | −0.033 | 0.045 | 0.45 | converged |

In this sample, 1,940 songs (22.1%) were taken up by another artist (y_foreign = 100). Two songs were dropped because their outcome was undefined.

## Verdict by the rule written first: **UNSETTLED**
The slope has the predicted sign (−0.30), but p is .42, nowhere near .00833, and the halves split (−0.62 and +0.03). The kill line did not fire either: −0.30 is below −0.2. The conditional logit has the predicted sign and converged, but that cannot rescue the result. By the rule, the outcome is **unsettled (p ≥ .00833; halves split)**.

## How firm is this?
Not very. The SE is 0.38 pp, exactly what the simulation expected. The 95% range runs from about −1.0 to +0.4. It covers the prediction (−0.6), zero, and small effects in the opposite direction. Before the outcome was joined, the simulation said the kill would fire 71% of the time if CH had no effect and 15% of the time if the prediction were true. The kill did not fire. That leans slightly toward an effect, but the evidence is weak. The estimate sits about halfway between "no effect" and the prediction.

## Reported only (these decide nothing)
| Variant | Estimate | SE | p |
|---|---|---|---|
| Wrapped form of CH | −0.15 | 0.38 | 0.70 |
| \|CH\| (how much a song turns, either direction) | −0.31 | 0.38 | 0.40 |
| Without z(A) and V | −0.24 | 0.38 | 0.53 |
| Without z(ch_ic_mean) | −0.29 | 0.38 | 0.44 |
| On y (in Discogs-VI at all), 8,774 songs | −0.22 | 0.38 | 0.56 |
| Intensive margin, z(log(1+covers)) among 2,025 matched songs | −0.012 SD | 0.015 | 0.45 |
| y_foreign with karaoke/tribute sets removed (no song changed) | −0.30 | 0.38 | 0.42 |
| **CH on the fresh songs** (4,920 rows, 888 fresh; slope from fresh outcomes only) | −0.90 | 0.97 | 0.35 |

- The |CH| line matters for interpretation. It is as large as signed CH (−0.31), so whatever small lean exists may be about *how much* a song turns, not *which way*. Neither is anywhere near significant.
- On the fresh songs, the match validation passed (cached at 100% on every check). 158 of the 888 fresh songs were taken up by another artist. Both halves were negative (−0.77, −0.72), and the conditional logit was −0.091 (SE 0.135) and converged. Power there was 0.02, and the PREDICTION.md says this reading decides nothing tonight. The 4,920 rows come from 590 artists, counting seen and fresh songs together. The chair's figure of "448 artists" probably counts only artists with fresh songs; I did not check it separately.
- The arrow A had a coefficient of +0.95 (SE 0.41) in this model. That is a control column here and decides nothing.

## Deviations
- **Conditional logit.** statsmodels' `ConditionalLogit` (`run05 common.cond_logit`) failed with "need covariance of parameters". This is the same failure run 05 met on the same 3,186-song sample: the nine chord-count bins and the parentheses flag have no finite estimate. As in run 05, I took the coefficient from the exact conditional likelihood, maximised with scipy (BFGS, then Newton). The code was copied unchanged from `run05/experiments/arrow_of_time/test.py`. It converged by the run 04 test (max |score| / nobs < 1e-5). As a cross-check, I ran statsmodels without those ten columns: −0.035 (SE 0.044, p .43), also converged, with the same sign. This was a code fix only. No rule changed, and the verdict does not depend on it, because p and the halves already make the result unsettled.

## What this cannot say
- It cannot say that the direction a progression turns makes no difference. The test has low power, so a null rules nothing out.
- y_foreign means another artist released the song. It is not the same as a song being loved for a long time.
- Genre is only partly held constant. Comparing within an artist absorbs most of it, but an artist's falling-fifth ballads and plagal rock songs can still differ in ways this test does not control.
- A song's position on the circle ignores chord quality: a minor ii and a major II sit at the same point.
- These 9,588 songs were used in runs 04 and 05. CH is new to them, but the songs themselves are not unseen.
- This shows association only, not cause. The McGill hold-out was not touched.
