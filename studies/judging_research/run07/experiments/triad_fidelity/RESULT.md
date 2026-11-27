# Campfire fidelity F: result (run 07, test 8 of 8)

Run on 26 November 2026, 19:22 to 19:24 ET. The run began after commit cd17b08 (19:21 ET). The rule is `PREDICTION.md` in this folder, frozen at commit 9227e71 before any outcome was joined. No rule, column, prediction or threshold was changed, and the script ran without error.

## In plain words

**The idea.** When musicians pass a song along, they tend to keep its plain three-note chords and drop the colour in the voicings. If so, songs whose bars are mostly a plain triad should lose little in the passing and be picked up more often by other artists. The Inventor predicted that within one artist's catalogue, a song one standard deviation higher on "triad fidelity" (F) would be about **half a percentage point** more likely to have a version by another artist.

**What came out.** The sign was wrong. Within an artist, songs with *higher* triad fidelity were about **2 percentage points less** likely to have been recorded by someone else, per standard deviation of F. Both random halves of the artists gave nearly the same figure, and so did a second kind of model (a conditional logit). The rule written in advance says a negative estimate kills the idea, so **the test is KILLED.**

**How firm.** The kill is firm as a kill. The estimate is about 2 standard errors below zero and 2.5 standard errors below the prediction, and every check points the same way. It is **not** strong enough to count as a finding in the other direction. Tonight's bar is p < .00625 because eight tests are counted, and this estimate has p = .044. So it does not show that plainer chords hurt a song's uptake. It is a hint, and it can only be tested on new songs. It is also the kind of hint the Skeptic warned about: F may measure how the MIDI arranger voiced the file, not the song itself.

## The numbers (all from `result.json`)

### Step 1: is F an existing measure under a new name? (notes only, before the outcome)
Within-artist Spearman correlations of F with each measure, on artist-demeaned ranks over the 5,901 songs. Pairs with a missing value are dropped.

| ch_rep | V | ln_chg | ln_bars | H4m | cv_w | g | lnP | B | CH | A | ln_tempo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.096 | −0.213 | **−0.339** | +0.176 | +0.123 | +0.015 | −0.054 | +0.183 (5,759) | −0.208 (5,891) | +0.020 (5,900) | +0.017 (5,900) | +0.219 |

F with itself is 1.000. The largest overlap is ln_chg at −0.339, well inside the |ρ| ≤ 0.7 gate, so **F is not an existing measure renamed.** These figures match the chair's `../chair_gates.json` (lnP there is +0.182, a rounding difference from which pairs are complete). The chair's split-half is 0.888 and the residual 0.785.

### Power (printed by the script before the estimate)
`fake_power`, 400 draws: pass rate 0.0025 at .00625 if the prediction is true, false-pass rate 0.000, mean simulated SE 0.794 pp.

**The base rate was misjudged in the simulation.** The simulation assumed about 20% of songs are taken up by others (run 06's calibration). The real base rate of y_foreign here is **39.7%**. A 0/1 outcome near 40% is noisier than one near 20% (variance 0.24 against 0.16), so the real SE is **1.04 pp**, not 0.79. At that SE, a true +0.5 would sit only half a standard error from zero. The test was even blinder than printed: a pass was close to impossible, and the kill line (β ≤ 0) would fire about 32% of the time if the truth were +0.5, and 50% if it were zero. **This does not weaken the kill much here.** The kill was decided by an estimate far below zero, not one just under it.

### The counted estimate
Linear probability model within artist on z(F), with z(ln_chg), z(V), z(ln_bars) and five-year year bins. Standard errors are CR1, clustered by artist. The outcome is y_foreign (0/100).

| | β (pp per SD of F) | SE | z | p (two-sided) | N songs | artists |
|---|---|---|---|---|---|---|
| **All songs** | **−2.100** | 1.043 | −2.01 | **0.044** | 5,901 | 1,678 |
| Half 0 | −2.116 | 1.516 | −1.40 | 0.163 | 2,961 | 842 |
| Half 1 | −2.054 | 1.434 | −1.43 | 0.152 | 2,940 | 836 |

**Conditional logit** (grouped by artist, same columns): coefficient **−0.144** per SD (odds ratio 0.87), p = 0.015, **converged**. statsmodels dropped 958 artists (2,751 songs) whose songs all had the same outcome, as a conditional logit must.

Outcome join: 2,387 songs matched a Discogs-VI clique and none was dropped for lacking an own set. 2,343 songs have y_foreign = 100.

### Verdict by the rule written first
- Pass needs β > 0 with p < .00625, β > 0 in both halves, and a converged logit > 0. **β is negative, so it fails on every count.**
- Kill: β ≤ 0. **It fires (β = −2.10).**
- Opposite sign with p < .00625 would be recorded as killed plus a new hypothesis. **This does not apply:** p = .044 > .00625 (|z| = 2.01 < 2.734).

**Verdict: KILLED.** The estimate lies 2.5 SE below the predicted +0.5. Both halves agree to within 0.06 pp, and the logit agrees in sign. The prediction is clearly disfavoured on these songs. A reverse effect is only suggested, not shown.

### Readings that decide nothing (reported as frozen)
| Reading | β | SE | p | N | artists |
|---|---|---|---|---|---|
| On y (any version in Discogs-VI at all) | −2.019 | 1.044 | 0.053 | 5,901 | 1,678 |
| Fame held (Billboard flag, hotttnesss, missing flag) | −2.095 | 1.032 | 0.042 | 5,901 | 1,678 |
| First performers only (R02-3's rule) | −1.308 | 1.131 | 0.248 | 4,755 | 1,591 |
| ln_tempo held (the Skeptic's arranger check, tempo part only) | −2.180 | 1.042 | 0.036 | 5,901 | 1,678 |

All four are negative. Holding fame changes nothing, and neither does holding tempo. The first-performer subset shrinks the estimate by about a third and loses precision.

### A note on the shared code
The shared conditional-logit sign check in `../common.py` had a programming bug: it read an attribute that statsmodels' ConditionalResults does not have, so it always returned nan. This was found when the first test (`lakh_repetition`) ran, and it was fixed at commit cd17b08 before this test ran. The fix changed no rule. This test ran on the fixed code, so its logit figure is a real estimate.

## What this result cannot say
- **MIDI is not the record.** The notes come from a hobbyist's MIDI arrangement, matched to the recording by audio. F reads that arrangement's chroma, including pads, doublings and added tones. It has a +0.22 overlap with tempo, and holding tempo clears only that one part of arranger style. A voicing-free F was never built. So even the negative sign may describe how arrangers voiced the files, not the songs.
- **Triad templates.** F scores each bar against 24 plain major and minor triads. Sevenths, suspensions and power chords all count as "less faithful" whether or not a covering musician would keep them.
- **y_foreign is uptake, not love.** It records whether some other artist's version is in Discogs-VI. No measure of lasting love is used. Discogs-VI coverage is uneven.
- **Within artist only, and no cause.** The comparison is between songs by the same artist. It cannot say whether F matters across artists or what causes what. Lakh songs lean towards well-known artists.
- **Power.** Even at the printed power, this battery could not have confirmed +0.5. The kill rests on the size of the negative estimate, not on the test's design.
