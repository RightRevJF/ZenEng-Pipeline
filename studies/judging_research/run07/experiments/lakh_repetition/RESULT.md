# Chord repetition on whole Lakh songs: the standing prediction. Result

Run 07, 26 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 9227e71 before any outcome was joined. The shared code is `../common.py`, the script is `test.py`, the log is `run.log` and the numbers are in `result.json`. Priority 1 of 8 tests tonight, so each needs p < .05/8 = .00625.

**Verdict: KILLED.** The rule written first says the prediction dies if the estimate is zero or below. It came out at **−1.93 percentage points per SD** (SE 1.34, p = .15), against the +1.0 predicted. Both artist halves and the conditional logit also point down. The estimate is not significant, so this is a kill by sign, not a finding that repetition hurts.

## In plain words

The idea was simple: among one artist's own songs, the ones whose chords repeat more should more often end up recorded by someone else. Two earlier runs leaned that way (+1.00 and +1.32), but neither was strong enough to pass. Tonight was the first fair test on a new batch: 5,901 whole songs from the Lakh MIDI collection, none of which had ever been matched to an outcome.

The lean did not come back. Within an artist, songs with more repeated chords were, if anything, slightly *less* often covered: about 2 points lower per standard step of repetition, where about 40 in 100 songs are covered at all. Every other way of looking at it (fame held, first performers only, any release at all, early or late covers) also came out below zero. None of these is far enough from zero to be trusted as a real negative effect. But the predicted +1.0 now looks unlikely: it sits about 2.2 standard errors above the estimate.

This repetition score is not the same thing the earlier runs measured. Here it is read from an arranger's MIDI file, and it agrees only weakly (0.32) with the Hooktheory version. So this kills the prediction *for this measure on these songs*. It does not prove that the earlier hand-transcribed lean was false.

## Step 1: is the measure an existing measure renamed? (notes only)

The test's measure *is* ch_rep, the battery's own primary, so its correlation with ch_rep is 1 by definition. It needs no renaming gate (PREDICTION.md, chair.md). For the record, here are the within-artist Spearman correlations on the 5,901 songs by 1,678 artists. They are computed on ranks over all songs, demeaned within artist, pairwise complete, and agree with `../chair_gates.json` to three decimals.

| With | ρ (within artist) | Songs |
|---|---|---|
| ch_rep | 1.000 (itself) | 5,901 |
| V | −0.598 | 5,901 |
| ln_chg | +0.267 | 5,901 |
| ln_bars | +0.185 | 5,901 |
| H4m | −0.036 | 5,901 |
| cv_w | +0.551 | 5,901 |
| g | −0.279 | 5,901 |
| lnP | −0.073 | 5,716 |
| F | +0.096 | 5,901 |
| B | −0.281 | 5,886 |
| CH | +0.071 | 5,899 |
| A | +0.039 | 5,899 |

The largest overlap with another measure is V (number of distinct chords), at −0.598. That is under the 0.7 line, and V is held in the model. Chair figures: split-half 0.742, residual split-half 0.313.

## What was predicted (frozen)

- **Measure:** ch_rep, the share of chord 3-grams already heard earlier in the song (half-bar triads, repeats collapsed; mean over the song's files). It goes into the model as z, where 1 SD = 0.183.
- **Outcome:** y_foreign = 100 if the song's Discogs-VI version group contains a release by a performer sharing no name with the artist, 0 if not or unmatched.
- **Model:** linear probability within artist, with CR1 standard errors clustered by artist. It holds z(ln_chg), z(V), z(ln_bars) and five-year year bins. A conditional logit by artist is the sign check.
- **Prediction:** **+1.0 pp per SD.**
- **Pass:** β > 0 with p < .00625, β > 0 in both artist halves, and a conditional logit above zero that converged.
- **Kill:** β ≤ 0. If the sign is opposite with p < .00625, the test is killed and the result is reported as a new hypothesis.
- **Unsettled:** anything else, including an estimate between 0 and +1.0 that is not significant.

## What came out

**Power, printed before the estimate (400 fake-outcome draws):** pass rate 0.0075 if +1.0 is true, false-pass rate 0.000 if the true value is 0, mean SE 1.035 pp. The test was nearly blind before it started.

| | β (pp per SD) | SE | p | Songs | Artists |
|---|---|---|---|---|---|
| **All songs (the test)** | **−1.93** | **1.34** | **.148** | **5,901** | **1,678** |
| Artist half 0 | −2.71 | 1.97 | .170 | 2,961 | 842 |
| Artist half 1 | −1.24 | 1.80 | .490 | 2,940 | 836 |

- **95% range for the main estimate:** −4.56 to +0.69. The prediction of +1.0 is outside it: it lies 2.19 SE above the estimate (one-sided p ≈ .014). The Skeptic's expected +0.4 is just inside: 1.74 SE above (one-sided p ≈ .04).
- **Conditional logit (sign check):** coefficient −0.122 log-odds per SD (odds ratio 0.88), p = .111, converged. Statsmodels dropped 958 artists (2,751 songs) whose songs were all covered or all uncovered, so it rests on the other 720 artists and 3,150 songs.
- **Outcome join:** 2,387 of 5,901 songs matched a Discogs-VI version group. 2,343 have y_foreign = 100, and none were dropped as matched without an own set.

**The base rate is about 40%, not 20%.** The share of songs with y_foreign = 100 is **39.7%** (2,343 of 5,901). The power simulation assumed 20%, which was run 06's calibration; run 06's fresh songs had about 18%. A yes/no outcome near 40% is noisier per song than one near 20% (variance 0.24 against 0.16). That explains why the real SE (1.34) is about 30% larger than the simulated 1.03. In practice:

- The real test was even weaker than the printed power of 0.0075.
- The kill rule's error rates in PREDICTION.md (17% chance of a kill if +1.0 is true; 50% if the true value is 0) were worked out for SE 1.03. At SE 1.34, a true +1.0 would have produced an estimate at or below zero about 23% of the time.

The base rate is high probably because Lakh leans to well-known artists, whose songs are covered more.

## Verdict by the rule written first

- β = −1.93 ≤ 0, so **the kill fires: KILLED.**
- The pass fails on every count: the sign is wrong, p = .148 is not below .00625, both halves are negative, and the logit is negative.
- The opposite sign is not significant (p = .148 > .00625), so this is **not** reported as a new hypothesis that repetition lowers uptake.

**How firm.** As a rule outcome it is unambiguous: every column agrees on the sign, and the logit converged. As evidence it is moderate. A kill would have fired by chance about 23% of the time even if +1.0 were exactly true. Still, an estimate this far below +1.0 (one-sided p ≈ .014) makes the predicted size hard to keep for MIDI ch_rep on Lakh songs. Taken with runs 04 (+1.00, p .044) and 06 (+1.32, p .20), the three batches no longer point one way.

**The logit fix.** The shared conditional-logit sign check had a programming bug. The frozen version read `r.mle_retvals`, which statsmodels' ConditionalResults does not have, so every call fell into its error branch and returned nan. The bug was found when this first test ran. It was fixed in `common.cond_logit` at commit cd17b08, before the run reported here, and no rule changed. The earlier run is kept as `result_before_logit_fix.json`. It is identical to `result.json` except for the logit column, which read coefficient nan, p nan, not converged. The verdict is KILLED in both runs, because the kill depends on β alone. The fixed code tries Newton's method first and falls back to BFGS if Newton warns that it has not converged. The earlier log shows such a warning, so the reported coefficient most likely comes from the BFGS fit. The log does not say which method was used.

## Reported, deciding nothing

| Reading | β (pp per SD) | SE | p | Songs | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | −1.67 | 1.35 | .215 | 5,901 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing flag) | −1.90 | 1.33 | .153 | 5,901 | 1,678 |
| First performers only (R02-3's rule) | −1.85 | 1.37 | .178 | 4,755 | 1,591 |
| W01-J6a early uptake (foreign set ≤ first year + 5) | −0.92 | 1.29 | .478 | 5,901 | 1,678 |
| W01-J6a late uptake (foreign set > first year + 10) | −1.56 | 1.25 | .213 | 5,901 | 1,678 |

All five readings are negative and none is near significance. Holding fame barely moves the estimate (−1.93 to −1.90). As run 02 ruled, nothing is decided on the early/late contrast.

## What it cannot say

- **MIDI is not the record.** The notes come from an arranger's MIDI file, matched to the recording by audio. The chords are half-bar triad templates, not a transcriber's chords. This ch_rep correlates only 0.32 with Hooktheory ch_rep on 1,487 shared songs. So the kill applies to this construct, not directly to the hand-transcribed lean of runs 04 and 06.
- **y_foreign is uptake, not love.** It counts whether another performer released the song. No measure of lasting love is used here.
- **Within artist only, and no cause.** The comparison is between one artist's own songs. It says nothing about artists against one another, and nothing about cause. Lakh leans to well-known artists, and Discogs-VI's coverage is uneven.
- **Power.** The test was nearly blind (pass rate 0.0075 if the prediction were true, and lower at the real 40% base rate). A kill this weak cannot rule out a small positive effect: +0.4 is still inside the 95% range.
