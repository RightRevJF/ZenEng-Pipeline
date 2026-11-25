# The arrow of time: do chord changes that never retrace go with uptake by other artists? Result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder (frozen and pushed in commit 1f6c36d before any outcome was joined). The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order:

1. It reproduced the unit values.
2. It built the measure from the notes.
3. It ran the gate and printed the power.
4. Only then did it join the outcome.

Before reading the real outcome, I checked the code on a random fake outcome; that run wrote nothing in this folder. No rule was changed afterwards. The script runs in about 35 seconds in one process.

**Verdict: UNSETTLED.** The estimate came out positive and a little larger than predicted: +0.84 percentage points per SD against +0.6 predicted. Both artist halves are positive and so is the conditional logit. But p = .035 does not reach tonight's line of .00714, so it is neither a pass nor a kill.

## The idea, with a worked example

Write a song's chords as a chain of moves from one chord to the next. Then ask: for every move from chord X to chord Y, how often does the song make the reverse move from Y back to X?

- **A looped I–V–vi–IV** (C, G, Am, F, round and round) moves C→G, G→Am, Am→F, F→C. It never makes any of those moves in reverse. It only goes one way round the circle, so it has a direction. Its score A is **1.00**, the maximum.
- **A I–IV vamp** (C, F, C, F…) moves C→F, then F→C, then C→F again. Every move is undone by the next one, like a pendulum. Over 16 chords (15 changes) only one move is left without a partner. Its score is **0.07**, close to the minimum of 0.

A = 1 minus the share of moves that are matched by a reverse move. In physics, a process whose moves balance their reverses this way is said to be in "detailed balance": it looks the same played backwards. The claim was that songs whose chord motion has a direction (high A) "carry a listener somewhere". Within an artist's own songs, those songs should more often be released by another artist.

## What was predicted

The test compares songs within each artist, with the artist fixed effect. It also holds these constant: chord repetition (`ch_rep`), chord surprise (`ch_ic_mean`), the log of the number of chord changes (A leans towards 1 when changes are few), chord count, clips per song, length and title flags.

The outcome is **y_foreign**: whether the song's Discogs-VI version group holds a performer set sharing no name with the original artist.

- **Predicted:** +0.6 percentage points per SD of A.
- **Pass:** all of β > 0, p < .00714 (.05/7, for tonight's seven tests), β > 0 in both artist halves, and a positive, converged conditional logit.
- **Kill:** β below +0.2.

## The measure and the gate (notes only, before the outcome)

- **Unit values reproduced exactly:**

| Progression | Changes | A | G2 |
|---|---|---|---|
| I–V–vi–IV ×4 | 15 | 1.0000 | 0.0000 |
| I–IV ×8 | 15 | 0.0667 | 0.9333 |
| I–V–I–IV ×4 | 15 | 0.0667 | 0.4667 |

- **Coverage:** 8,774 of the 9,588 songs have a value (clips with fewer than 6 chord changes have none). That matches the chair. Every clip was found in the full Hooktheory file.
- **Spread:** the 10th / 50th / 90th percentiles are 0.333 / 0.833 / 1.000, as the chair found. Of the songs with a value, 36.1% score exactly 1. That is 33.0% of all 9,588 rows, which is where the chair's "33%" comes from.
- **Gate 1, stability** (clip 1 against clip 2 of the same song, 3,294 pairs): Spearman **0.302**. It needs 0.20 or more, so it **passed**.
- **Gate 2, overlap** (is A an existing measure renamed?): the largest |Spearman| is −0.154 with ln(changes), then +0.152 with `ch_ic_mean`. Against `ch_rep` it is +0.011. The line is 0.7, so it **passed**.
- **The merged G2 measure:** ρ(A, G2), the "back-and-forth share", is −0.960. They are one contrast seen from two sides. G2 is reported below and decides nothing.

## The outcome

- **Songs in the model:** 8,772 songs by 1,726 artists. 1,940 of them (22.1%) have y_foreign = 100.
- **Dropped:** 814 songs with no A, and 2 songs whose y_foreign is undefined (version group missing, or no set of the artist's own).
- **Artists left with one song:** 123. They are demeaned to zero and add nothing.

## Power (printed before the estimate)

| | SE (pp) | Power at +0.6, p < .00714 | at p < .05 |
|---|---|---|---|
| Notes-side bound (rule) | 0.541 | 0.06 | 0.20 |
| Clustered SE, real outcome | **0.398** | **0.12** | 0.33 |

The real SE is smaller than the notes-side bound, as in run 04. Power is still far below run 03's proposed 0.5 floor. That floor is undecided, so it does not block the test.

## Results

**Primary model:** linear probability, within artist, CR1 clustered by artist.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| A | **+0.84** | 0.40 | 0.035 | +0.06 to +1.62 |

**Artist halves:**

| Half | Songs | Artists | β | SE | p |
|---|---|---|---|---|---|
| 0 | 4,242 | 878 | +0.78 | 0.57 | 0.17 |
| 1 | 4,530 | 848 | +0.84 | 0.58 | 0.15 |

**Conditional logit** (sign check; same columns, not demeaned, grouped by artist):

- **Drops:** 1,301 artists and 5,586 songs whose songs are all 0 or all 1. It keeps 425 artists and 3,186 songs.
- **Why statsmodels failed:** its `ConditionalLogit` stopped with an error while forming the covariance matrix. Some nuisance controls have no finite estimate in this sample: the nine chord-count bins all drift to about −26, and the parentheses flag to −562. Run 04 met the same problem with the parentheses flag.
- **The fit that counts:** as the rule allows, I maximised the exact conditional likelihood with scipy (BFGS, then Newton) by the same subset recursion run 04 used as its cross-check. **z(A): +0.077 log-odds per SD (SE 0.046, p .097).**
- **Convergence:** it **converged** by the run 04 test (max |score|/nobs < 1e-5; the max |score| is 1.6e-11).
- **Cross-check:** statsmodels on the same sample without the ten columns that have no finite estimate gives +0.081 (SE 0.046, p .077), also converged. The sign is the same either way.

## Verdict, by the rule written first

**UNSETTLED** (p ≥ .00714).

| Clause | Needed | Got | Met? |
|---|---|---|---|
| β | above 0 | +0.84 | yes |
| p | below .00714 | .035 | **no** |
| Both halves | above 0 | +0.78 and +0.84 | yes |
| Conditional logit | above 0, converged | +0.077, converged | yes |

The kill line (+0.2) does not fire, and the result is not in the opposite-sign class.

**How firm.** Everything points the predicted way, and the size is about what was predicted:

- the primary estimate, both halves, the conditional logit, the unweighted version and the version without ln(changes);
- the predicted +0.6 sits inside the 95% range.

But the evidence is only moderate. At p = .035 it would pass a single test at .05, not one of seven at .00714. With power of 0.12, a result like this was the most likely outcome even if the claim is true. The result neither confirms nor clears the idea.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | β (SE, p) |
|---|---|
| G2 (back-and-forth share) in place of A | −0.65 (0.41, .11), the mirror image of A, as expected from ρ = −0.96 |
| A on y (in Discogs-VI at all; all 8,774 songs with A) | +0.66 (0.39, .092) |
| A on y_foreign with karaoke and tribute sets removed | +0.84 (0.40, .035): 45 songs had such a set, but every one also had another foreign set, so no song changed |
| Without the ln(changes) column | +0.84 (0.40, .036) |
| Song value as a plain (unweighted) mean of clips | +0.84 (0.40, .034) |
| Intensive margin: SD of log(1 + covers) per SD of A, among 2,025 versioned songs (630 artists), first year held | −0.002 (0.023, .93) |

- **The intensive margin:** among songs that were versioned, A says nothing about how many versions they got.
- **The other columns** (in the model, tested nothing): `ch_rep` +1.20 (SE 0.50, p .017), `ch_ic_mean` −0.28 (SE 0.45) and ln(changes) +0.90 (SE 2.49).
  - The positive `ch_rep` sign repeats run 04's finding on the same songs. It is not new evidence.
  - A and `ch_rep` are nearly uncorrelated (ρ +0.01), so A is not standing in for repetition.
- **Songs and artists per half:** half 0 has 4,242 songs and 878 artists; half 1 has 4,530 songs and 848 artists.

## Anything odd

- **The conditional-logit failure** (above): a nuisance-control problem, not one in A. The two fits agree on A's sign and size.
- **The "33% score exactly 1" in the rule** counts all 9,588 rows, not the 8,774 songs with a value. The underlying count is identical.

## What it cannot say

- **What the outcome measures:** y_foreign is not lasting love. It means some performer set with no shared name released a version under the same title and writer. Missing credits and failed matches add noise. Featured-artist or remix "versions" could favour some chord styles.
- **Seen songs:** run 04 used these same 9,588 songs for `ch_rep` and `ch_ic_mean`. A is new on them, but the songs are not unseen.
- **Genre:** vamps are a genre habit (funk, hip-hop, some dance music). Within-artist comparison absorbs most genre, not all of it.
- **Low power:** power was 0.12, so this result neither confirms nor clears the idea. A fresh frozen test on new songs, or at a single-test threshold, would be needed to settle it.
- **No cause:** association only, and hits only.
- **McGill hold-out:** untouched. This test did not read song 59, songs/p69, studies/holdout59 or any hold-out file.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
