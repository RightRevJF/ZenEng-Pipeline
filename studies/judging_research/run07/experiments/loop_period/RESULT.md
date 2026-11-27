# Loop period P*: result

Run 07, 26 November 2026, test 6 of 8 (`loop_period`). Run by an experimenter at 19:24 ET, after commit cd17b08. Rules, prediction and threshold unchanged from `PREDICTION.md` (commit 9227e71). Nothing was committed.

## In plain language

**The idea.** You learn a song by learning one cycle of it. A song that repeats every 2 bars (a vamp) gives another musician little to carry over. A song whose 4- to 16-bar phrase comes back is worth learning and covering. The measure is the loop period P*: the bar lag (2 to 16) at which the song's chords best match themselves. The prediction was that, comparing songs by the same artist, songs with longer loops are more often recorded by other artists. The size was +0.6 percentage points per standard deviation of ln P*, with tempo held so that half-time and double-time writing does not count.

**What came out.** There is no sign of the effect. Within artist, longer loops go with **+0.05 points** more uptake per SD. That is essentially zero, and the uncertainty is fifteen times larger than the estimate. The two random halves of the artists disagree: one half says +1.3, the other −1.3. The logit check points the other way, at almost exactly zero.

**Verdict: UNSETTLED.** The test did not pass: it was nowhere near the significance it needed. It was not killed either, because the kill rule was "β ≤ 0", and the estimate landed just above zero. This is a weak verdict, not a firm one. The estimate is a hair above the kill line. Under a true effect of zero, the kill fires half the time, so "not killed" here says almost nothing. What the data do say is that an effect as large as +0.6 cannot be told apart from zero with these songs. The 95% interval runs from about −1.4 to +1.5 points per SD.

**What the other readings show (they decide nothing).** None comes close to significance. Signs are mixed: with fame held, +0.18; on any Discogs entry at all (y), −0.14; first performers only, −0.71. The seconds form, which half- or double-time writing cannot move, gives −0.44. In the categorical form, the Listener's predicted order (2 < 4 < 8 ≤ 16 bars) does not appear: 8-bar and 16-bar loops come out slightly *below* 4-bar loops.

## The numbers (all from `result.json`)

### Step 1: is the measure an existing one renamed? (notes only)
Within-artist Spearman correlations of lnP: ranks demeaned by artist, on the 5,759 of the 5,901 songs that have lnP (at least 34 sounding bars). Computed by the experimenter; the chair's figures from `../chair_gates.json` are beside them.

| Column | ρ with lnP (experimenter) | Chair |
|---|---|---|
| ch_rep | −0.074 | −0.073 |
| V | −0.030 | −0.030 |
| ln_chg | −0.155 | −0.154 |
| ln_bars | +0.022 | +0.022 |
| H4m | +0.157 | +0.156 |
| cv_w | −0.245 | −0.244 |
| g | +0.151 | +0.150 |
| lnP | 1 (itself) | |
| F | +0.183 | +0.182 |
| B | −0.212 | −0.211 |
| CH | −0.042 | −0.042 |
| A | +0.035 | +0.035 |
| (ln_tempo, held) | +0.055 | +0.054 |
| (lnPsec, its own seconds variant) | +0.920 | |

**Not a renaming.** The largest overlap with any existing measure is cv_w, at −0.245. With the four gated columns (ch_rep, V, ln_chg, ln_bars) the largest is ln_chg, at −0.155, far inside the |ρ| ≤ 0.7 gate. The two calculations differ only in the third decimal.

### Power (printed before the estimate)
`common.fake_power`, 400 draws, gave these results:
- pass rate if the prediction is true: **0.0225**;
- false pass if the effect is zero: 0.000;
- mean SE: 0.601 pp.

**The base rate was wrong in the simulation.** The real base rate of y_foreign is **39.7%** (`base_rate` 39.705, over the 5,901 songs; 2,343 songs with y_foreign = 100, 2,387 matched in Discogs-VI, none dropped). The power simulation assumed 20%. A 0/100 outcome near 40% is noisier than one near 20%: its variance is 0.24 against 0.16. That is why the real SE (0.745) is about 24% larger than the simulated one (0.601). The real power was therefore even lower than the 2% printed. The prediction of +0.6 pp is also smaller next to a 40% base than it looked next to 20%. The test was nearly blind, as `PREDICTION.md` said, and in fact somewhat blinder.

### Primary estimate (within-artist LPM, CR1 by artist)
| | β (pp per SD of lnP) | SE | p (two-sided) | N songs | Artists |
|---|---|---|---|---|---|
| **All** | **+0.054** | 0.745 | 0.942 | 5,759 | 1,676 |
| Half 0 | +1.314 | 1.091 | 0.229 | 2,893 | 841 |
| Half 1 | −1.308 | 1.014 | 0.197 | 2,866 | 835 |

- z = 0.07; the threshold is |z| > 2.734 (p < .00625).
- Columns held: z(ln_tempo), z(ln_chg), z(V), z(ln_bars), and year-bin dummies.

### Conditional logit (sign check)
- Coefficient **−0.0079** (log-odds per SD), p = 0.861.
- **Converged: yes.**
- statsmodels dropped 972 artists (2,699 songs) with no variation in the outcome.
- The shared sign check had a programming bug when the first test ran: it read a missing attribute (`mle_retvals`) and always returned nan. It was fixed at commit cd17b08 before this test ran, and no rule changed. This run used the fixed code.

### Verdict by the rule written first
- **Pass** needs β > 0 and p < .00625, both halves > 0, and a logit > 0 that converged. It failed every part except β > 0: p = 0.942, half 1 is negative, and the logit is negative.
- **Kill** needs β ≤ 0. Not met: β = +0.054.
- **Therefore UNSETTLED.**

How firm: firmly not a pass. The non-kill is fragile, since the estimate sits 0.07 SE above the kill line. In practice the result is a null that cannot rule out the predicted +0.6, or an effect of the opposite sign of similar size.

### Readings that decide nothing
| Reading | β | SE | p | N | Artists |
|---|---|---|---|---|---|
| On y (in Discogs-VI at all) | −0.137 | 0.754 | 0.856 | 5,759 | 1,676 |
| Fame held (Billboard flag, hotttnesss, missing flag) | +0.183 | 0.747 | 0.806 | 5,759 | 1,676 |
| First performers only | −0.711 | 0.782 | 0.363 | 4,636 | 1,584 |
| Seconds form, lnPsec, no ln_tempo | −0.436 | 0.779 | 0.576 | 5,759 | 1,676 |

**Categorical form** (first file's P*, against P* = 4; ln_tempo and the battery's controls held; N 5,756, 1,676 artists):

| P* | β (pp) | SE | p |
|---|---|---|---|
| 2 bars | −0.080 | 2.166 | 0.971 |
| 8 bars | −2.478 | 1.978 | 0.210 |
| 16 bars | −1.030 | 2.801 | 0.713 |
| other lag | +3.581 | 2.534 | 0.158 |

The predicted order 2 < 4 < 8 ≤ 16 holds: **false**.

## What this cannot say
- **Power.** The power was about 2% even if the prediction were exactly true, and lower at the real 40% base rate. A null clears nothing: loop period may matter by an amount this sample cannot see.
- **MIDI is not the record.** The notes come from an arranger's MIDI file, matched to the recording by audio, not from the recording itself. P* is computed from bar chroma of that arrangement. Chords elsewhere in the battery are half-bar triad templates. An arranger who loops a section, or writes in half time, changes P*.
- **y_foreign measures uptake, not love.** It records whether another artist recorded a version listed in Discogs-VI. Lasting love is not measured here at all.
- **Within artist only; no cause.** The comparison is between songs by the same artist, and it is a correlation. Lakh songs lean towards well-known artists, and Discogs-VI coverage is uneven.

## Files
`PREDICTION.md` (frozen), `test.py` (unchanged), `run.log` (this run, 19:24 ET, after cd17b08), `result.json`, this file. The overlap script was run outside the repo, from the experimenter's scratchpad.
