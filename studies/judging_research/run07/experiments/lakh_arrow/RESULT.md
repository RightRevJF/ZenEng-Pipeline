# The arrow of time on whole songs: result

Run 07, 26 November 2026. Test 5 of 8 (`lakh_arrow`, idea R05-A). The rule is `PREDICTION.md` in this folder, committed and pushed at 9227e71 before any outcome was joined. `test.py` ran unchanged at 19:22 to 19:24 ET, after commit cd17b08 (19:21 ET). Every figure below is copied from `result.json` unless it is marked *derived*.

## In plain language

**What was predicted.** Some songs' chords go round one way: C to G to Am to F, and back to C, without retracing. Others rock back and forth: C to F to C to F. The measure A scores the first kind near 1 and the second near 0. Run 05 suggested that, comparing songs by the same artist, the go-round-one-way songs are more often recorded by other artists. The prediction was frozen as +0.6 percentage points more uptake per standard deviation of A. The test would be killed if the estimate came out at zero or below.

**What came out.** The estimate is the other way round. Within an artist, songs whose chords move one way were *less* often taken up by other artists: −1.36 points per SD. That is not significant at the test's threshold, and not even at the ordinary .05. Both halves of the artists point the same (negative) way. Every side reading is negative too.

**Verdict: KILLED** under the rule written first (β ≤ 0). This is a firmer kill than most tonight. A kill line at zero fires half the time when nothing is there, so on its own it means little. Here, though, the estimate sits about 2.6 standard errors below the predicted +0.6 (*derived*), and an estimate that low would be rare if the prediction were true. The opposite-sign estimate does not reach p < .00625, so it is **not** put forward as a new hypothesis.

**History of this idea.** Run 05: +0.84 on seen songs, −1.75 across single-song artists. Run 06's fresh songs: +0.09. Tonight's 5,900 fresh whole songs: −1.36. The run 05 lead has not reproduced on either batch of fresh songs, and tonight it points the wrong way.

## Step 1: is A an existing measure renamed? (notes only, before the test)

Within-artist Spearman correlations (artist-demeaned ranks) of A with each existing measure, on the 5,901 songs (`C.add_shapes(C.lakh_songs())`; A is missing for 1 song):

| ch_rep | V | ln_chg | ln_bars | H4m | cv_w | g | lnP | F | B | CH | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.039 | +0.159 | −0.009 | −0.126 | −0.236 | −0.049 | −0.106 | +0.035 | +0.017 | −0.190 | +0.003 | 1 (itself) |

Pairs: 5,900 each, except lnP 5,759 and B 5,891. These are exactly the chair's figures in `../chair_gates.json`. The largest overlap with the four renaming columns is V +0.159, far inside the 0.7 line. The largest overlap with any measure is H4m −0.236. A is the test's own measure, so its correlation with itself is 1 by construction. **A is not an existing measure renamed.**

## The numbers (`result.json`)

**Power, printed before the estimate** (`common.fake_power`, 400 draws): pass rate 0.0125 if the prediction is true; false pass 0.0 under zero; mean SE 0.576 pp.

**Outcome:** 2,387 songs matched a Discogs-VI clique, none dropped for having no own set. 2,343 songs have y_foreign = 100. **Base rate of y_foreign: 39.7%.**

**The base rate is about 40%, not the 20% the power simulation assumed.** A yes/no outcome near 40% is noisier than one near 20% (variance 0.24 against 0.16 per song). That is why the real SE (0.76 pp) is about a third larger than the simulated 0.58. The test was weaker than the printed power says, and that power was already only about 1%. So a pass was close to impossible. The kill does not depend on power in the same way: it rests on the sign of the estimate, and here the sign is clear of the prediction.

| Fit | β (pp per SD of A) | SE | p (two-sided) | N | Artists |
|---|---|---|---|---|---|
| **Primary: y_foreign, within artist** | **−1.356** | 0.761 | 0.0748 | 5,900 | 1,678 |
| Half 0 | −0.685 | 1.067 | 0.521 | 2,961 | 842 |
| Half 1 | −2.031 | 1.074 | 0.0585 | 2,939 | 836 |

- **Threshold:** p < .00625 (= .05/8). The primary p is .0748.
- *Derived:* 95% interval −2.85 to +0.14. z against the predicted +0.6 is −2.57.
- **Conditional logit (sign check):** coefficient nan, p nan, converged false.
  - The logit did not produce an estimate on this test. Newton and then BFGS (maxiter 2000) were both tried. Both ended with a Hessian that could not be inverted, so statsmodels raised "need covariance of parameters". `common.cond_logit` then returned nan by design.
  - I diagnosed this afterwards, read-only; nothing was changed or re-run. The sample the logit keeps (3,150 songs in 720 artists with variation) has the same size as in `lakh_repetition`, where the logit worked. No column is constant inside those artists. I did not chase the cause further.
  - **It does not affect the verdict.** A pass needed a positive, converged logit, so the test could not pass in any case. The kill rule reads β alone.
- **The earlier logit bug.** The shared conditional-logit sign check had a programming bug: it read a missing attribute (`mle_retvals`) and so always returned nan. It was found when the first test ran and fixed at commit cd17b08, before this test ran, changing no rule. This test ran on the fixed code. The nan here is a different failure: a singular Hessian on these data, not the old bug.

**Verdict by the rule written first:**

| Rule | Result |
|---|---|
| Pass (β > 0, p < .00625, both halves > 0, logit > 0 and converged) | no |
| Kill (β ≤ 0) | **yes** (β = −1.356) |
| Opposite sign with p < .00625 (new hypothesis) | no (p = .0748) |
| **Verdict** | **KILLED** |

## Readings that decide nothing

| Reading | β | SE | p | N | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | −1.310 | 0.756 | 0.0833 | 5,900 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing flag) | −1.268 | 0.762 | 0.0962 | 5,900 | 1,678 |
| First performers only (R02-3's rule) | −0.738 | 0.765 | 0.335 | 4,754 | 1,591 |
| A with ch_rep held | −1.180 | 0.776 | 0.128 | 5,900 | 1,678 |

All four are negative and none is significant. The negative lean is not explained by fame or by chord repetition. It is weaker when only first performers are kept.

## What it cannot say

- **MIDI is not the record.** The notes come from an arranger's MIDI file, matched to the recording by audio. The chords are half-bar triad templates fitted to that file, not the song's real chords.
- **y_foreign is uptake, not love.** It records whether another artist's version is in Discogs. No measure of lasting love is used.
- **Within artist only; no cause.** The result compares songs by the same artist. It says nothing about artists against each other, and nothing about cause. Lakh leans to well-known artists, and Discogs-VI coverage is uneven.
- **Power.** The test was nearly blind to an effect of the predicted size. Even the real 40% base rate made it blinder than planned. The kill rests on the estimate falling well below the prediction, not on the test being strong.
- **No conditional-logit check.** The logit gave no estimate here, so the sign check is missing for this test.

Files: `PREDICTION.md` (frozen), `test.py` (unchanged), `run.log`, `result.json`. Nothing was committed.
