# spectral_gap: result (run 07, test 3 of 8)

26 November 2026. The test ran at 19:23 ET (`timeout 1500 python3 -I -W ignore test.py > run.log`, exit 0, about 70 seconds). That was after commit cd17b08. Nothing in `PREDICTION.md`, `test.py` or `../common.py` was changed, and nothing was committed. Every figure below is copied from `result.json`, apart from the step-1 overlaps, which come from the notes alone.

## In plain words

**What was predicted.** Jason's S = 1 + g/π measures how freely a song's chords mix. Here g is the "spectral gap" of the table of chord-to-chord moves. A small g means the song has separate harmonic "rooms", such as a verse and a chorus in different places, joined by few moves. The Geometer predicted that, comparing songs by the same artist, the songs with smaller g are more often recorded by other artists. The predicted size was a fall of 0.3 percentage points per standard deviation of g, holding chord repetition (ch_rep) and the usual controls fixed.

**What came out.** The sign went the other way, and the effect was tiny. Each SD of g went with **+0.26 percentage points** more uptake by other artists. That is far inside the noise (SE 0.86, p = 0.77). The two halves of the artists disagree in sign. The conditional logit is also slightly positive, and it did not converge.

**Verdict: KILLED**, by the rule written first (β ≥ 0). **The kill is weak.** The test was nearly blind. Even if the prediction were exactly true, an estimate on the wrong side of zero would turn up about a third of the time. With no effect at all, it would turn up half the time. The data barely tell "g has the predicted small effect" apart from "g has no effect". What they do show is that there is no sizeable negative effect: an effect as large as −2 pp per SD would sit about 2.6 SE from this estimate. Under its frozen rule the prediction is killed.

## Step 1: is g an existing measure renamed? (notes only)

Within-artist Spearman correlations (ranks over all 5,901 songs, demeaned within artist; the same method as `../chair_gates_report.py`) between g and each column:

| ch_rep | V | ln_chg | ln_bars | H4m | cv_w | g | lnP | F | B | CH | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| −0.279 | +0.027 | +0.072 | +0.078 | +0.274 | −0.367 | 1 (itself) | +0.150 | −0.054 | +0.114 | −0.003 | −0.106 |

- The rows behind each figure are 5,901, except lnP (5,716), B (5,886), CH (5,899) and A (5,899).
- These match `../chair_gates.json` to three decimals.
- The largest overlap is with cv_w (−0.367), and the largest with a renaming column is with ch_rep (−0.279). Both are well inside the 0.7 line.
- The other eleven columns together explain R² = 0.30 of g's within-artist ranks (5,716 complete rows).
- **g is not an existing measure renamed.** It is the test's own measure, so the entry for g is 1 by definition.

## The numbers

**Songs.** 5,901 within-artist Lakh songs by 1,678 artists. Of these, 2,387 matched a Discogs-VI clique, and 2,343 have y_foreign = 100. No row was dropped for "matched with no own set".

**Power, printed before the estimate** (`common.fake_power`, 400 draws, seed 7):
- pass rate 0.01 if β = −0.3 is true;
- false-pass rate 0.0 if β = 0;
- mean SE 0.666 pp.

PREDICTION.md's table gave 0.007 and 0.67. The small difference is Monte Carlo noise, as that file said to expect.

**The base rate is about 40%, not 20%.**
- y_foreign averages **39.7%** (`base_rate` 39.705).
- The power simulation assumed artist baselines averaging 20%, which is run 06's calibration.
- A 0/1 outcome near 40% is noisier than one near 20%: its variance is 0.24 against 0.16.
- So the real standard error is **0.86 pp**, not the simulated 0.67.
- **The test was therefore even less powerful than the printed 0.01.** A −0.3 pp effect is also a smaller relative change on a 40% base than on a 20% base.
- With SE 0.86, a true β of −0.3 lands at β̂ ≥ 0 about 36% of the time, and β = 0 does so 50% of the time.

**Primary estimate** (within-artist linear probability model, CR1 errors by artist; columns z(g), z(ch_rep), z(ln_chg), z(V), z(ln_bars) and year bins):

| | β (pp per SD of g) | SE | p (two-sided) | N | Artists |
|---|---|---|---|---|---|
| **All songs** | **+0.257** | 0.864 | 0.766 | 5,901 | 1,678 |
| Artist half 0 | +0.692 | 1.261 | 0.583 | 2,961 | 842 |
| Artist half 1 | −0.181 | 1.205 | 0.880 | 2,940 | 836 |

**Conditional logit (sign check).** The coefficient is +0.018 (p = 0.706), **not converged**: neither Newton nor the BFGS fallback converged. Statsmodels dropped 958 artists (2,751 songs) whose songs all have the same outcome. The sign is the opposite of the prediction. Because the logit did not converge, its sign is not firm either way. The kill rule does not use the logit.

**Verdict by the frozen rules.**
- Pass needs β < 0 with p < .00625, β < 0 in both halves, and a converged logit below 0. **Not met:** β is positive, p = 0.77, the halves split, and the logit is positive and not converged.
- Kill if β ≥ 0. **Met: β = +0.257.**
- "Opposite sign with p < .00625" (a new hypothesis): **not met** (p = 0.77). No positive effect is claimed.
- → **KILLED.** It is a weak kill on a nearly blind test, as PREDICTION.md said a kill would be.

**A note on the shared logit code.** The shared conditional-logit sign check (`common.cond_logit`) had a programming bug. It read an attribute that statsmodels' result does not have, so it always returned nan. The bug was found when the first test (lakh_repetition) ran, and it was fixed at commit cd17b08, before this test ran. The fix changed no rule. This test ran on the fixed code.

## Readings that decide nothing (in `result.json`)

| Reading | β | SE | p | N | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | +0.167 | 0.864 | 0.847 | 5,901 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing-hotttnesss flag) | +0.333 | 0.861 | 0.699 | 5,901 | 1,678 |
| First performers only (R02-3's rule) | +0.342 | 0.910 | 0.707 | 4,755 | 1,591 |
| g without ch_rep | +0.733 | 0.730 | 0.315 | 5,901 | 1,678 |

All four readings are positive and far from significant. None of them reverses the picture, and none of them decides anything.

## What this cannot say

- **Power.** The test was nearly blind: the printed power was 0.01, and the real SE is even larger than the simulation assumed. The kill is weak evidence. It does not show that g is irrelevant to uptake, only that no sizeable negative effect is visible.
- **MIDI is not the record.** The notes come from an arranger's MIDI file, matched to the recording by audio. The chords are half-bar triad templates, not a transcription. A different arrangement of the same song could give a different g.
- **y_foreign is uptake, not love.** It records whether another artist's version exists in Discogs-VI. No measure of lasting love is used here (run 06's first principles).
- **Within artist only; no cause.** The result compares songs by the same artist and says nothing across artists. Lakh leans to well-known artists, and Discogs-VI coverage is uneven.
- **One unit only.** This was the one re-read allowed on a new unit (chair's ruling). The idea passed its gate on whole songs, and its prediction was then killed on the outcome. These songs' outcomes have now been seen, so any further test of g needs an independent batch.
