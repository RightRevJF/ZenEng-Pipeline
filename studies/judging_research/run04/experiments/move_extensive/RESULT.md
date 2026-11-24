# Repeated chords, plain chords, and whether a song is in Discogs-VI at all: result

Run 04, 24 November 2026. The rule is `PREDICTION.md` in this folder (frozen in commit 00ab557 before any outcome was joined). The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order: it built the rows from the notes, ran the gate, and only then read the outcome's key set. I wrote the code and checked it on a random fake outcome before reading the real one, and no rule was changed afterwards. It runs in about 30 seconds.

**Verdicts: H1 is killed and H2 is killed.** For H1 the estimate goes the wrong way. For H2 it is close to zero.

## What was predicted

The comparison is within an artist's own songs, with the artist fixed effect, chord count, clips per song, length and title genericness held. The outcome is whether the song's video id is a key of `hooktheory_covers_discogs.json`, meaning the song sits in a Discogs-VI version group.

- **H1 (R04-L1):** more chord repetition within sections (`ch_rep`) goes with a lower chance of being in Discogs-VI. Predicted: **−1.0 percentage points per SD**.
- **H2 (R02-chordsurprise):** more chord surprise (`ch_ic_mean`) goes with a lower chance of being in Discogs-VI. Predicted: **−1.0 pp per SD**.

To pass, a hypothesis needed all of these: β < 0, p < .01 (two-sided, .05/5 for tonight's five hypotheses), β < 0 in both artist halves, and a conditional-logit coefficient < 0. A β above −0.3 pp is a kill.

## Rows and gate (notes only, before the outcome)

- Rows: 9,588 songs by 1,741 artists who have 2 or more songs, out of 13,198 songs and 5,351 artists. Every one of the chair's counts was reproduced exactly: the chord-count bins, the clip classes, the word counts, 109 titles with parentheses, 960 repeated titles, and halves of 886 and 855 artists.
- **Gate 1, clip-to-clip** (clip 1 against clip 2, 4,271 pairs): `ch_rep` 0.324 and `ch_ic_mean` 0.496. The threshold is 0.20, so it **passed**.
- **Gate 2, overlap** (is either measure an existing measure under a new name?): the largest |Spearman| for `ch_rep` was −0.44 (`ch_h_mean`), and for `ch_ic_mean` it was +0.48 (`ch_h_mean`). The two measures correlate at −0.33 with each other. The threshold is 0.7, so it **passed**. For the 14 songs with no rhythm row, the rhythm correlations leave them out.
  - *Printed, deciding nothing:* `ch_ic_mean` against `ch_ic_sd` is +0.78. That field is outside the model.

## The outcome

N = 9,588 songs and 1,741 artists. **2,226 songs (23.2%) are in Discogs-VI.** As a diagnostic only: 311 of the file's 3,080 keys are not among the 13,198 surprise-file songs.

## Power (printed before any β)

| | Clustered SE | Power at −1.0 pp, p < .01 | at p < .05 | Notes-side figures in the rule |
|---|---|---|---|---|
| H1 `ch_rep` | 0.503 pp | **0.28** | 0.51 | SE 0.65, power 0.15 |
| H2 `ch_ic_mean` | 0.410 pp | **0.45** | 0.69 | SE 0.57, power 0.20 |

The real SEs came out smaller than the notes-side bound, because within an artist the outcome varies less than its overall rate suggests. Both power figures are still below run 03's proposed 0.5 floor. That floor is undecided, so it does not block the test.

## Results

**Primary model: linear probability, within artist, CR1 clustered by artist.** My hand-coded CR1 matches statsmodels' cluster SE to within 1e-13.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| H1 `ch_rep` | **+1.19** | 0.50 | 0.018 | +0.21 to +2.18 |
| H2 `ch_ic_mean` | **−0.10** | 0.41 | 0.81 | −0.90 to +0.70 |

**Artist halves:**

| | Half 0 (4,617 songs, 886 artists) | Half 1 (4,971 songs, 855 artists) |
|---|---|---|
| `ch_rep` | +0.93 (SE 0.62, p .13) | +1.36 (SE 0.78, p .08) |
| `ch_ic_mean` | −0.51 (SE 0.58, p .38) | +0.25 (SE 0.58, p .67) |

**Conditional logit** (statsmodels `ConditionalLogit`, grouped by artist, columns not demeaned):

- **Drops:** 1,270 artists and 5,910 songs whose songs are all in or all out. It keeps 471 artists and 3,678 songs.
- **`ch_rep`:** +0.151 log-odds per SD (SE 0.058, p .009).
- **`ch_ic_mean`:** −0.014 (SE 0.051, p .78).
- **Convergence:** BFGS converged. statsmodels does not return the optimiser's own flag, so convergence was judged by scipy's test on the same scale: max |score|/nobs < 1e-5.
- **Cross-check:** I wrote my own fit of the same likelihood (subset recursion, Newton). It gives `ch_rep` +0.1509 and `ch_ic_mean` −0.0141, the same as statsmodels to about 1e-4.
- **One nuisance problem:** the parentheses-flag control has no finite estimate. In this sample, songs with "(" in the title are essentially never matched within their artist, so the two optimisers stop at different large negative values (−14 and −52). That leaves the two tested coefficients unchanged, and since both verdicts are kills from the primary β it does not affect them.

## Verdicts, by the rule written first

- **H1 (`ch_rep`): KILL.** β = +1.19 pp is above −0.3 and on the wrong side of zero. It does not fall in the rule's separate "opposite sign" class, because p = .018 is not below .01. Both halves and the conditional logit also come out positive.
  - **How firm:** firm against the prediction. The predicted −1.0 lies far outside the 95% range (+0.21 to +2.18).
  - **What it means, by the rule:** chords that repeat do not go with a lower chance of being versioned at all. The within-artist cover-count result (−0.042) is untouched.
- **H2 (`ch_ic_mean`): KILL.** β = −0.10 pp is above −0.3.
  - **How firm:** fairly firm. The predicted −1.0 lies just outside the 95% range (−0.90 to +0.70). Power was 0.45, so a true effect of about −0.5 pp could still be hiding.
  - **What it means, by the rule:** this kills "plainly", chord surprise as a claim of its own, on this outcome. It does not kill J1.

### Not a finding: a positive sign for chord repetition

The positive `ch_rep` estimate is consistent across the primary model, both halves and the conditional logit, and the conditional logit reaches p = .009 on its own. It **does not meet the rule's opposite-sign test** (primary p = .018 > .01), so it is not counted as a new hypothesis tonight. If anyone wants to pursue it, it needs its own frozen rule.

There is a known way it could be an artefact. The rule warns that false "versions" from featured artists and remixes favour looping songs, which is exactly high `ch_rep`. So this sign could come from how the matching works rather than from how people treat the music.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdicts.

| Item | `ch_rep` β (SE, p) | `ch_ic_mean` β (SE, p) |
|---|---|---|
| Each term with the other left out | +1.23 (0.47, .009) | −0.44 (0.38, .25) |
| Without the title flags | +1.15 (0.51, .025) | −0.11 (0.41, .79) |
| ln(clips) linear instead of clip dummies | +1.19 (0.50, .018) | −0.10 (0.41, .81) |
| LPM on the conditional-logit sample (3,678 songs, 471 artists) | +2.85 (1.17, .015) | −0.09 (1.01, .93) |

- **Share in Discogs-VI by clips per song:**

| Clips per song | Songs | Share in Discogs-VI |
|---|---|---|
| 1 | 5,317 | 21.9% |
| 2 | 2,533 | 25.4% |
| 3 | 1,123 | 25.0% |
| 4+ | 615 | 22.3% |

- **Songs and artists per half:** half 0 has 4,617 songs and 886 artists; half 1 has 4,971 songs and 855 artists.

## What it cannot say

- **What the outcome measures:** being in Discogs-VI means two performer sets released the song under the same normalised title with a shared writer. That is a record of re-release, not lasting love.
- **False non-matches:** songs that were never covered are mixed with songs that have missing credits, retitles or failed matches. Noise unrelated to the notes only weakens an effect, so a null is weak evidence.
- **Noise that tracks the notes:** compilation "versions", translated covers, and featured-artist or remix versions can create an effect. The last of these would push toward the positive `ch_rep` sign seen here.
- **Era:** era is held only through the artist fixed effect. Drift across a career is not held.
- **Power below 0.5:** for H2 in particular, a smaller true effect is not ruled out.
- **No cause:** this is association only.
- **McGill hold-out:** untouched. Run 04 did not read song 59, songs/p69, studies/holdout59 or any hold-out file.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
