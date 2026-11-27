# Harmonic chirality on whole songs: result

Run 07, 26 November 2026. The test was run once, exactly as frozen in `PREDICTION.md` (commit 9227e71), with `../common.py` at commit cd17b08. Run at 19:23 to 19:24 ET: `timeout 1500 python3 -I -W ignore test.py > run.log 2>&1`, exit 0. No rule, column, prediction or threshold was changed, and nothing was fixed in the script. Every figure below is copied from `result.json`.

## In plain words

**The question.** Put each chord's root on the circle of fifths and follow the song around it. Some songs mostly turn one way (clockwise, like the falling fifths of ii–V–I in the standards). Others mostly turn the other way (counterclockwise, like I–V–vi–IV). The idea was that, within one artist's catalogue, songs that turn clockwise are more often recorded by other artists. The prediction was **−0.6 percentage points of "covered by someone else" per standard deviation of chirality**. It counts as a pass only if the result is that sign and clears p < .00625. It is killed if the estimate comes out above −0.2.

**What happened.** The estimate came out on the other side of zero: **+0.30 points per SD**. That means slightly more covers for songs that turn counterclockwise, not fewer. It is small and far from significant (p = 0.69). Both halves of the artists point the same way as the whole (+0.31 and +0.47). So does the conditional logit (+0.024).

**Verdict: KILLED**, by the rule written first (β > −0.2). This is a weak kill. The test was nearly blind (see power below). The real noise was larger than planned. The 95% interval runs from −1.19 to +1.80 and still contains the prediction of −0.6. The estimate sits 1.19 standard errors from the prediction and 0.40 standard errors from zero. Taken by itself, the result favours "no effect" over "−0.6" by only about 2 to 1. The opposite sign is not significant (p = 0.69, not below .00625), so it does not count as a new hypothesis.

Across two runs, this measure has now come out −0.30 (run 06, seen Hooktheory songs) and +0.30 (tonight, fresh whole songs). That pattern looks like noise around zero.

## Step 1: is CH an existing measure renamed? (notes only, before the test was run)

Within-artist Spearman correlations of CH with the other measures, on the 5,901 songs. Each column is ranked over all songs, the ranks are demeaned within artist, and the Pearson correlation of the demeaned ranks is taken. This is the same method as `../chair_gates_report.py`. CH is finite on 5,900 songs, and each correlation uses 5,899 pairs (5,716 for lnP and 5,886 for B). Pooled Spearman (no artist demeaning) is shown alongside for reference.

| With | ch_rep | V | ln_chg | ln_bars | H4m | cv_w | g | lnP | F | B | CH | A |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Within artist | +0.071 | −0.067 | +0.048 | +0.046 | −0.021 | +0.032 | −0.003 | −0.042 | +0.020 | −0.026 | 1 (itself) | +0.003 |
| Pooled | +0.106 | −0.090 | +0.070 | +0.070 | −0.015 | +0.057 | +0.008 | −0.064 | +0.046 | −0.021 | 1 | +0.016 |

The within-artist values match the chair's gate numbers in `../chair_gates.json` to three decimals. **CH is not a renamed measure:** no overlap reaches |0.08|, far below the 0.7 line. CH is the test's own measure, so its entry is 1 by definition. CH is unrelated to the arrow of time A (+0.003). Distribution: mean +0.0017, SD 0.0376, 49.9% above 0, 0.9% exactly 0.

## The numbers

**Power, printed before the estimate** (`common.fake_power`, 400 draws under −0.6, 200 under 0): pass rate **0.0025**, false-pass rate 0.000, mean simulated SE 0.567 pp. The PREDICTION.md table (300 draws) gave 0.000, and the two agree within Monte Carlo error.

**Outcome join** (`outcome_info`): 2,387 of 5,901 songs matched a Discogs-VI clique, none were dropped for having no own set, and 2,343 have y_foreign = 100.

**Base rate of y_foreign: 39.7%**, not the 20% the power simulation assumed. This has three consequences:
- The noise is larger than planned. The real SE is 0.762 pp against the simulated 0.567, about 1.34 times as large. The test was therefore even less powerful than the printed 0.0025 (already almost zero) and the 8% at .05.
- The kill line catches the true value less reliably than planned. With the real SE, β̂ > −0.2 would fire about 60% of the time if the true effect were 0. It would also fire about 30% of the time if the prediction (−0.6) were exactly true.
- The effect looks smaller than planned. A fixed −0.6 pp is a smaller change against a 40% base than against a 20% base.

| | β (pp per SD) | SE | p | N | Artists |
|---|---|---|---|---|---|
| **Main (within-artist LPM, CR1 by artist)** | **+0.304** | 0.762 | 0.690 | 5,900 | 1,678 |
| Half 0 | +0.309 | 1.083 | 0.775 | 2,961 | 842 |
| Half 1 | +0.470 | 1.080 | 0.664 | 2,939 | 836 |
| Conditional logit (sign check, log-odds per SD) | +0.024 | | 0.560 | converged: yes | |

Columns held: z(CH), z(A), z(ch_rep), z(ln_chg), z(V), z(ln_bars), and five-year MSD-year bins. The conditional logit uses only the artists whose songs differ on the outcome. statsmodels dropped 958 artists (2,750 songs) whose songs were all covered or all uncovered (`run.log`).

**Rule check.** Pass needs β < 0 and p < .00625, both halves < 0, and logit < 0 and converged. All four fail. The kill line is β > −0.2, and +0.304 > −0.2, so the result is **KILLED**. It is not "opposite sign, significant", because p = 0.690.

**Note on the shared conditional logit.** The sign-check function in `common.cond_logit` had a programming bug. It read an attribute (`mle_retvals`) that statsmodels' ConditionalResults does not have, so it always returned nan. The bug was found when the first test (`lakh_repetition`) ran. It was fixed at commit cd17b08, before this test ran, and the fix changed no rule. This test ran on the fixed code, so its logit is a real estimate.

## Readings that decide nothing

| Reading | β (pp per SD) | SE | p | N | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | +0.426 | 0.773 | 0.581 | 5,900 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing flag) | +0.201 | 0.757 | 0.790 | 5,900 | 1,678 |
| First performers only | +0.801 | 0.778 | 0.303 | 4,754 | 1,591 |
| \|CH\| in place of CH (how much a song turns, either way) | +0.710 | 0.816 | 0.385 | 5,900 | 1,678 |

All four readings are positive and none is close to significant. Holding fame changes little. The run 06 first-principles question was whether any lean is about how much a song turns rather than which way. \|CH\| is no stronger than CH in any way that counts, so that question gets no answer here.

## What this cannot say

- **Power.** The test had almost no chance of passing even if the prediction were true. A kill this weak does not close the question. It only means this evidence does not support the claim.
- **MIDI is not the record.** The notes come from an arranger's MIDI file that was matched to the recording by audio. The chords are half-bar triad templates (roots only), not a transcriber's chords. A real clockwise lean in the recordings could be blurred here.
- **y_foreign is uptake, not love.** It records whether another artist has a version in Discogs-VI. It is not a measure of lasting love, and no love measure is used.
- **Within artist only, and no cause.** The comparison is between songs by the same artist. Lakh leans towards well-known artists, and Discogs-VI coverage is uneven.
