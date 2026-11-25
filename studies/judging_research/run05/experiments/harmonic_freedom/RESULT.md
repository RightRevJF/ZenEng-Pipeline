# Harmonic freedom: does a tune that many chords fit get taken up by other artists? Result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 1f6c36d before any outcome was joined. The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order: it checked the unit values, built the measure from the notes, ran the gate, and printed the power, all before reading any outcome. I checked the code on a random fake outcome first (no outcome file read), and no rule was changed afterwards. It runs in about a minute in one process.

**Verdict: killed.** The estimate is slightly negative (−0.23 percentage points per SD), below the kill line of +0.2.

## What was predicted

The idea comes from evolution: a genotype with many "neutral neighbours" spreads easily. Here, a melody that many plain chords fit would leave a coverer room to re-harmonise it in their own style. So, within an artist's own songs, tunes with more of this harmonic freedom should more often be released by another artist.

- **The measure (I2):** for each chord in a clip that is one of the seven plain triads of the key, count how many of those seven triads fit the melody notes under it at least as well as the written chord does. Fit is the share of melody time on the triad's three notes. Take log₂ of that count (bits of freedom) and average over the chords, weighted by melody time. Chords with less than half a beat of melody, sevenths, and borrowed or altered chords are skipped.
- **Held fixed:** the number of distinct melody notes per chord (`pcs_span`, because a sparse melody lets many triads fit), chord repetition (`ch_rep`), chord surprise (`ch_ic_mean`), run 04's controls (chord count, clips per song, length, title flags), and the artist.
- **Outcome:** `y_foreign`, whether a performer sharing no name with the original artist released the song (run 04's rule).
- **Predicted:** **+0.6 percentage points per SD** of I2.
- **To pass:** β > 0 with p < .00714 (.05 split over tonight's seven tests), β > 0 in both artist halves, and a converged conditional logit above 0. **β below +0.2 is a kill.**

## The measure and the gate (notes only, before the outcome)

- **Unit values reproduced:** one beat of C over a C chord gives 1.585 bits (C, F and A minor all fit); C–E–G over a C chord gives 0 bits (only C fits), with 3 distinct notes.
- **Songs:** 9,049 of the 9,588 songs have a value; the 10th, 50th and 90th percentiles are 0.81, 1.49 and 2.02 bits. These match the chair's figures exactly.
- **Chords used:** of 278,880 chord spans, 160,381 (57.5%) were scored. 94,967 were skipped as not a plain diatonic triad and 23,532 for too little melody. No key lacked a seven-note scale. The share scored is the same in both halves (57.6% and 57.4%).
- **Gate 1, clip-to-clip** (clip 1 against clip 2 of the same song, 3,796 pairs): 0.267. The threshold is 0.20, so it **passed**.
- **Gate 2, overlap:** the largest |Spearman| with the 17 data-pack measures, chord count, length, clips per song and `pcs_span` was −0.343 (`pcs_span`). The threshold is 0.7, so it **passed**. `ch_rep` was +0.203 and `mel_ic_mean` −0.255.

## The outcome

N = 9,047 songs by 1,718 artists (two songs with an undefined `y_foreign` dropped). **2,039 songs (22.5%) were released by another artist.**

## Power (printed before the estimate)

| | SE (pp) | Power at +0.6, p < .00714 | at p < .05 |
|---|---|---|---|
| Notes-side bound (in the rule) | 0.562 | 0.05 | 0.19 |
| Clustered SE from this run | **0.412** | **0.11** | 0.31 |

The real SE came out smaller than the bound, as in run 04. Power is still very low: a pass was unlikely even if the prediction were true.

## Results

**Primary model: linear probability, within artist, CR1 clustered by artist.** My CR1 matches statsmodels' cluster SE to within 1e-15.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **I2, harmonic freedom** | **−0.23** | 0.41 | 0.58 | −1.04 to +0.58 |
| `pcs_span` (control) | −0.39 | 0.40 | 0.32 | |
| `ch_rep` (control, decides nothing) | +1.12 | 0.52 | 0.033 | |
| `ch_ic_mean` (control) | −0.39 | 0.45 | 0.38 | |

**Artist halves:**

| | Songs | Artists | Released by another | β | SE | p |
|---|---|---|---|---|---|---|
| Half 0 | 4,355 | 877 | 997 | −0.06 | 0.59 | 0.92 |
| Half 1 | 4,692 | 841 | 1,042 | −0.33 | 0.57 | 0.57 |

**Conditional logit** (statsmodels, grouped by artist, columns not demeaned):

- **Drops:** 1,275 artists and 5,604 songs whose songs are all taken up or all not. It keeps 443 artists and 3,443 songs.
- **I2:** −0.037 log-odds per SD (SE 0.050, p 0.46). Converged (max |score|/nobs < 1e-5).
- **Nuisance:** as in run 04, the parentheses-in-title control has no finite estimate (titles with "(" are almost never taken up within their artist). It does not touch I2.

## Verdict, by the rule written first

**KILL.** β = −0.23 pp is below +0.2. The sign is negative in the primary model, in both halves and in the conditional logit, but p = 0.58 is nowhere near .00714, so this is not the rule's "opposite sign" class and is no new hypothesis.

- **How firm:** moderately firm against the prediction. The predicted +0.6 sits just outside the 95% range (upper end +0.58). A small positive effect, up to about +0.5 pp, is not ruled out.
- **What it means, by the rule:** within an artist's songs, a melody that more plain chords fit does not go with a higher chance of being released by another artist, on this outcome.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | Songs | β (SE, p) |
|---|---|---|
| Only chords with 3 or more distinct melody notes (clip-to-clip 0.232 on 2,728 pairs) | 7,894 | −0.39 pp (0.38, .30) |
| Without `pcs_span` | 9,047 | −0.11 pp (0.37, .77) |
| On y (in Discogs-VI at all) | 9,049 | −0.15 pp (0.40, .71) |
| Intensive margin, z(log(1 + covers)) among versioned songs, plus first year (SD per SD) | 2,126 | +0.012 (0.017, .49) |
| y_foreign with "karaoke"/"tribute" performer sets removed | 9,047 | −0.23 pp (0.41, .58), identical |

- **Karaoke/tribute removal changed nothing:** only 61 of the 95,489 performer sets in the version file name karaoke or tribute, and none of them was the only foreign release of a song in this model.
- **Share of chords scored:** 57.6% in half 0, 57.4% in half 1.

Every variant leans the same way as the primary estimate (slightly negative or about zero), and none comes near significance.

## What it cannot say

- **What the fit measures:** it uses pitch classes and duration only, not metre or which notes fall on strong beats; a passing note counts as much as a held one.
- **Which chords are scored:** only plain diatonic triads (57.5% of chord spans). Songs built on sevenths or borrowed chords are judged on their remaining chords.
- **What the outcome measures:** release by another artist is not lasting love. Missing credits, retitles and failed matches mix uncovered songs with unmatched ones, and that noise weakens any effect.
- **Low power:** 0.11 at the frozen threshold. The kill rests on the estimate falling below +0.2, not on proof of zero; an effect smaller than about +0.5 pp could still hide here.
- **Not fresh songs:** run 04 used the same songs for other measures. This measure is new to them.
- **No cause:** association only.
- **McGill hold-out:** untouched. This test did not read song 59, songs/p69, studies/holdout59 or any hold-out file.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
