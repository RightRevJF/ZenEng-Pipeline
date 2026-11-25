# The arrow of time on songs by single-song artists. Result

Run 05, 25 November 2026, the night's **8th test**. The rule is `PREDICTION.md` in this folder (frozen and pushed in commit 2bfd4ca before any outcome was joined). The script is `test.py` and the numbers are in `result.json`.

> **Read this first: this test was written after seeing results.** Its rule was chosen after tonight's seven results were known, including `arrow_of_time`'s positive but unsettled within-artist estimate. So even a pass here could only have been a **lead needing confirmation on songs not yet used** (the Discogs-VI re-match), **never a finding**. It did not pass.

The script followed the rule's order:

1. It reproduced the unit values.
2. It built the measure from the notes, on songs by artists who have only one song.
3. It ran the gate and printed the power.
4. Only then did it join the outcome.

Before reading the real outcome, I checked the code on a random fake outcome; that run wrote nothing in this folder. I also checked the robust-error code against `statsmodels` on the fake outcome (identical to 13 digits). No rule was changed afterwards. The script runs in about 6 seconds.

**Verdict: KILLED** (β below the +0.2 kill line). The estimate came out on the **wrong side**: −1.75 percentage points per SD of A, against +0.6 predicted. Its p = .009 is just short of the .00625 line, so it is not in the rule's "opposite sign" class either. It is a plain kill.

## The idea, in one paragraph

A measures whether a song's chords move one way round (like I–V–vi–IV looping, A = 1) or swing back and forth (like a I–IV vamp, A ≈ 0.07). `arrow_of_time` found, within each artist's own songs, a small positive lean: songs with more "direction" were a little more often released by another artist (+0.84 pp per SD, p .035, unsettled). This test carried the same claim to 3,610 songs by artists with **exactly one** song among the 13,198 Hooktheory songs. None of them were in run 04's or tonight's rows, and nobody had joined A or y_foreign to them before. Because each artist has one song, there is no within-artist comparison: songs are compared with each other, holding as much of the style the notes carry as the data allow.

## What was predicted

- **Outcome:** y_foreign, whether the song's Discogs-VI version group holds a performer set sharing no name with the original artist (run 04's rule 4410a0e, unchanged).
- **Columns held:** all 17 data-pack measures (including chord repetition `ch_rep` and chord surprise `ch_ic_mean`), the log of the number of chord changes, run 04's controls (chord count, clips per song, length, title flags), and an intercept.
- **Model:** ordinary least squares across songs with HC1 robust errors (with one song per artist this is the same as clustering by artist).
- **Predicted:** +0.6 pp per SD of A (tonight's original frozen size, not the +0.84 seen within artist).
- **Pass (a lead only):** β > 0, p < .00625 (.05/8), β > 0 in both artist halves, and a converged logit coefficient > 0.
- **Kill:** β below +0.2. **Opposite sign:** β < 0 with p < .00625.

## The measure and the gate (notes only, before the outcome)

- **Unit values reproduced exactly:** I–V–vi–IV ×4 gives A = 1.0000; I–IV ×8 gives 0.0667; I–V–I–IV ×4 gives 0.0667. The measure code is `arrow_of_time`'s, copied unchanged.
- **Songs:** 3,610 songs by 3,610 artists; halves 1,852 / 1,758 songs. All match the reviewer's notes-only figures.
- **Coverage:** 3,229 songs have A (clips with fewer than 6 chord changes have none). Every clip was found in the full Hooktheory file.
- **Spread:** 10th / 50th / 90th percentiles 0.333 / 0.864 / 1.000; 41.3% of songs score exactly 1. ρ(A, `ch_rep`) = +0.04.
- **Gate 1, stability** (clip 1 against clip 2 of the same song, 896 pairs): Spearman **0.339**. It needs 0.20, so it **passed**.
- **Gate 2, overlap** (is A an existing measure renamed?): the largest is −0.187 with ln(changes). The line is 0.7, so it **passed**.
- **Model rows:** 3,223 songs with A and all 17 measures (6 songs lack a rhythm row).

## The outcome

- **Songs in the model:** 3,212. Of them, **464 (14.4%) have y_foreign = 100**.
- **Dropped:** 381 songs with no A, 6 with a measure missing, and 11 whose y_foreign is undefined (their version group holds no set of the artist's own).
- **Halves:** 1,631 and 1,581 songs.

## Power (printed before the estimate)

| | SE (pp) | Power at +0.6, p < .00625 | at p < .05 |
|---|---|---|---|
| Notes-side bound (rule) | 0.760 | 0.03 | 0.12 |
| HC1 SE, real outcome | **0.670** | **0.03** | 0.15 |

This test was nearly blind, as the rule said it would be. Even if +0.6 were true, the kill line would fire 28% of the time (62% if the true effect were zero).

## Results

**Primary model:** OLS across songs, HC1 robust errors.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| A | **−1.75** | 0.67 | 0.009 | −3.06 to −0.43 |

**Artist halves:**

| Half | Songs | y_foreign = 100 | β | SE | p |
|---|---|---|---|---|---|
| 0 | 1,631 | 235 | −0.24 | 0.87 | 0.78 |
| 1 | 1,581 | 229 | −3.29 | 1.01 | 0.001 |

**Logit** (sign check, same columns): z(A) **−0.128 log-odds per SD** (SE 0.052, p .013). It **converged** at the first (BFGS) stage by the rule's test (max |score| / N = 9e-6, under 1e-5).

## Verdict, by the rule written first

**KILLED** (β < +0.2 pp per SD).

| Clause | Needed for a pass | Got | Met? |
|---|---|---|---|
| β | above 0 | −1.75 | **no** |
| p | below .00625 | .009 | **no** |
| Both halves | above 0 | −0.24 and −3.29 | **no** |
| Logit | above 0, converged | −0.128, converged | **no** |

- **Kill line:** β = −1.75 is below +0.2, so the kill fires.
- **Not the "opposite sign" class:** that needs p < .00625, and p = .009 misses it. So the rule does not record a new hypothesis ("back-and-forth chords are what other artists take up"). The reported G2 version (below) crosses that line, but it decides nothing.

**How firm.**

- **Every piece points the same way, and it is the wrong way:** the primary estimate, both halves, the logit, the version without the other 15 measures, A on y, and G2 (A's mirror image).
- **The halves are uneven:** half 1 carries most of the size (−3.29). Half 0 is near zero (−0.24).
- **The kill is not an artefact of low power:** the predicted +0.6 lies well outside the 95% range (−3.06 to −0.43).
- **Within one rule:** the claim as stated, "direction goes with uptake by other artists", is not supported on these songs.

**Against `arrow_of_time`.** That test found a small positive lean *within* artists (+0.84, unsettled). This one finds a larger negative lean *across* single-song artists. The two do not have to contradict each other. Across artists, A can stand in for genre or era, and nothing here holds genre directly: back-and-forth vamps are a habit of some styles (funk, hip-hop, some dance and older pop). What it does mean is that A's sign on the outcome depends on the comparison. The within-artist hint did not carry over to new songs compared across artists.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | β (SE, p) |
|---|---|
| β(`ch_rep`) in the same model | +0.09 (0.81, .91) |
| A without the 15 other data-pack measures | −1.84 (0.67, .006); `ch_rep` there +0.13 (0.71, .85) |
| A on y (in Discogs-VI at all; all 3,223 model rows, 489 with y = 100) | −1.58 (0.68, .020) |
| G2 (back-and-forth share) in place of A | +1.94 (0.70, .005), the mirror image of A (ρ = −0.957) |
| A on y_foreign with karaoke and tribute sets removed | −1.75 (0.67, .009): one song had such a set, and it also had another foreign set, so no song changed |

- **Chord repetition, the first look outside run 04's rows:** `ch_rep` on y_foreign across these single-song artists is +0.09 (SE 0.81), essentially nothing either way. This is across artists, with a wide interval, and settles nothing about R04-FV.
- **Which columns did carry weight:** in the same model, the largest were the share of rests (+3.96, SE 0.93), a parenthesis in the title (−11.9) and song length (ln beats, −5.1). As tonight's fame test found, across artists the notes mostly carry style (rests, phrasing, sung against instrumental).

## Anything odd

- **The chord-count bins add up to the intercept.** A needs 6 or more chord changes, so no model row has fewer than 5 chords. Run 04's nine chord-count bins therefore cover every row and sum to the intercept. Run 04 never met this, because its artist fixed effect absorbed the intercept. The rule only says to drop columns with no variation. I found the problem from the notes, before the outcome was read, and made the lowest bin (5 to under 7 chords) the reference. This changes no estimate or SE of A: the model fits exactly the same values. It only makes the design full rank for the HC1 degrees-of-freedom factor and for the logit.
- **Nearly every versioned song counts as "foreign" here:** 464 of the 489 model rows in Discogs-VI. For single-song artists, y_foreign is almost the same as y (in Discogs-VI at all), and the two results agree.
- **The logit's parentheses flag** sits at −7.2: only 44 of the 3,223 model rows have one, so its estimate is thin (−11.9 pp in the linear model). This is a nuisance-control problem, not one in A, and the fit converged.

## What it cannot say

- **No finding either way.** This rule was chosen after seeing A's within-artist result, so a pass could only have been a lead. Its kill is a clean kill of the claim on these songs by the rule written first. Even so, it is one cross-artist test, and it was nearly blind (power 0.03).
- **A kill may be style swamping a real song-level effect.** Nothing holds genre directly, and across artists A can stand in for genre or era. The negative sign may reflect which styles get covered, not what direction in the chords does for a song. Confirming or clearing A at the song level needs within-artist songs not yet used (the Discogs-VI re-match).
- **What the outcome measures:** y_foreign is not lasting love. Hits and non-hits are mixed, missing credits and failed matches add noise, and the evidence is association only.
- **Seen data:** the covers study on main (15 November) used cover counts for the matched songs among these, against the 17 measures. It never used A or y_foreign.
- **McGill hold-out:** untouched. This test did not read song 59, songs/p69, studies/holdout59 or any hold-out file.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
