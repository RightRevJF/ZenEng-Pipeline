# Kac burstiness of chord returns: result

Run 07, 26 November 2026, test 7 of 8 (R07-I3, the Inventor). Run at 19:24 ET, after the conditional-logit fix (commit cd17b08, 19:21 ET). The rule is `PREDICTION.md` in this folder (commit 9227e71), unchanged. Nothing was edited in `test.py` or `../common.py`. Output: `result.json` and `run.log`.

## In plain words

**The idea.** Every chord in a song comes back. How often it comes back is fixed by how common the chord is. What is left over is the *pattern* of the returns. A chord can come back like clockwork, which means a loop. Or it can come back in bunches, which means it belongs to one section (a verse chord or a bridge chord) and returns when that section does. The Inventor predicted that, comparing songs by the same artist, the songs with bunchier chord returns are a little more often recorded by other artists: **+0.3 percentage points for each standard deviation of burstiness.** The song's chord vocabulary, its number of chord changes, its length and its era were held fixed.

**What came out.** The estimate is **+0.57 points per standard deviation**. That is on the predicted side and close to the predicted size, but its uncertainty is **0.97 points**, so the data are equally consistent with no effect at all, or with an effect of either sign up to about two points. Both halves of the artists lean positive. The logistic sign check is barely positive, and its fit did not converge.

**Verdict: UNSETTLED.** It is not a pass, because the estimate is nowhere near the required significance level (p = 0.56 against a threshold of 0.00625). It is not killed, because the kill rule was "the estimate is zero or negative", and it is positive. This verdict is weak. The test was nearly blind before it ran: even if the prediction were exactly true, a pass was close to impossible. Escaping the kill is only slight support. With the realised uncertainty, a positive estimate happens about 62% of the time if the prediction is true and 50% of the time if there is no effect. That is a likelihood ratio of about 1.2.

**In short:** songs whose chords come back in section-like bunches may be a little more often taken up by other artists, but this test cannot tell that apart from nothing.

## Step 1: is B an existing measure renamed? (notes only, before the outcome)

Within-artist Spearman correlation of B with each measure. Ranks are taken over the songs where both values exist, then demeaned within artist, and only artists with at least two such songs are used (N = 5,886; 5,716 for lnP). This was computed for this report and agrees with the chair's gates in `../chair_gates.json`, to within 0.001 on lnP (the chair's figure is −0.211).

| ch_rep | V | ln_chg | ln_bars | H4m | cv_w | g | lnP | F | B | CH | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| −0.281 | **+0.466** | +0.389 | +0.270 | −0.064 | −0.208 | +0.114 | −0.212 | −0.208 | 1 | −0.026 | −0.190 |

**B is not a renamed measure.** Its largest overlap is V (+0.47): songs with more distinct chords are burstier. That is below the 0.7 line, and V, ln_chg and ln_bars are all held in the model, as the Skeptic asked. The chair's other gates were split-half 0.631 and residual split-half 0.436, so B passes. It overlaps least with the other new shape measures (|ρ| ≤ 0.21).

## Step 2: the test as written

**Power, printed before the estimate** (fake outcomes, 400 draws, `run.log`): pass rate under the prediction **0.000**, false-pass rate under zero **0.000**, mean SE **0.742 pp**.

**The base rate is about 40%, not 20%.** In the real outcome, y_foreign = 100 for **39.7%** of the songs (2,343 of 5,901). Discogs-VI matched 2,387 songs, and no matched song was dropped for lacking the artist's own version. The power simulation assumed a 20% base rate (run 06's calibration). A 0/1 outcome is noisiest at 50%. At 40% the noise per song is about 1.5 times the variance assumed (0.24 against 0.16), so the SE is about 1.2 times larger. The real SE is 0.97 pp against 0.74 simulated, which is 1.3 times larger. **So the test was even less powerful than the table in PREDICTION.md says.** A power of 0.000 cannot get worse, but the chance of the estimate landing on the predicted side was lower, and the kill weaker evidence, than planned.

| | β (pp per SD of B) | SE | p (two-sided) | N | Artists |
|---|---|---|---|---|---|
| **Main: y_foreign, within artist** | **+0.568** | 0.971 | 0.559 | 5,891 | 1,678 |
| Half 0 (md5 of artist key) | +0.844 | 1.443 | 0.559 | 2,958 | 842 |
| Half 1 | +0.358 | 1.314 | 0.785 | 2,933 | 836 |

95% interval for the main β: about −1.33 to +2.47 pp (β ± 1.96 SE). The prediction (+0.3) and zero are both well inside it.

**Conditional logit (sign check), grouped by artist, same columns:** coefficient **+0.032** (log-odds per SD), p = 0.556, **converged: false**. Neither the Newton fit nor the BFGS fallback converged cleanly. statsmodels dropped 958 artists (2,743 songs) whose songs are all 0 or all 1. The sign is positive, but an unconverged fit cannot confirm it. Under `test.py`'s rule, a PASS with an unconverged logit would have been recorded as UNSETTLED. That rule did not come into play, because the main p already failed.

**The shared sign check had a bug, fixed before this test ran.** The conditional-logit check in `../common.py` read an attribute (`mle_retvals`) that statsmodels' conditional results do not have, so it always returned nan. This was found when the first test (`lakh_repetition`) ran. It was fixed at commit cd17b08, before this test ran, and no rule changed. This test used the fixed code.

## Verdict by the rule written first

| Rule | Needed | Got | Met? |
|---|---|---|---|
| β > 0 | yes | +0.568 | yes |
| two-sided p < .00625 | yes | 0.559 | **no** |
| β > 0 in both halves | yes | +0.844, +0.358 | yes |
| conditional-logit coef > 0 (converged) | yes | +0.032, not converged | sign yes, convergence no |
| Kill: β ≤ 0 | — | β = +0.568 | does not fire |

**UNSETTLED** (as in `result.json`). **How firm:** firm as a verdict, because p = 0.56 is far from the threshold and no reasonable change in method would make it a pass. As evidence it is weak, because the test had no power. The kill did not fire, which moves the odds toward the prediction by only about 1.2 to 1.

## Readings that decide nothing (in `result.json`)

| Reading | β | SE | p | N | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | +0.855 | 0.976 | 0.381 | 5,891 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing flag) | +0.401 | 0.967 | 0.678 | 5,891 | 1,678 |
| First performers only | **−0.203** | 0.985 | 0.837 | 4,746 | 1,591 |
| ch_rep also held (the Inventor's round-1 form) | +0.202 | 0.999 | 0.840 | 5,891 | 1,678 |

All four readings are far from significant. Three are positive and shrink when fame or ch_rep is held. The **first-performer reading turns slightly negative**: when the songs where the artist was not the first to record the song are removed, the lean disappears. One possible reason, which these figures cannot settle, is that some of the positive lean comes from songs that were already covers when this artist recorded them. None of these readings counts.

## What it cannot say

- **Power:** a null clears nothing. With a pass rate of 0.000 under the prediction, and an SE 1.3 times larger than planned because the base rate is about 40%, not 20%, this test could not have confirmed +0.3.
- **MIDI is not the record.** The notes come from an arranger's MIDI file that was matched to the recording by audio. Chords are half-bar triad templates, so B reads the returns of template chords in that file, not the song as written or played.
- **y_foreign is uptake, not love.** It records whether Discogs-VI lists a version by another performer. No measure of lasting love is used.
- **Within artist only; no cause.** The comparison is between songs by the same artist, with artist fixed effects. Lakh leans toward well-known artists, and Discogs-VI coverage is uneven. Burstiness is still partly vocabulary and length (V +0.47), even with those held.
