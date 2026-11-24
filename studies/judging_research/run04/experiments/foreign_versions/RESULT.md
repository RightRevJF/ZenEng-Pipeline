# Is the chord-repetition sign on "versioned at all" carried by other artists? Result

Run 04, 24 November 2026, the sixth test of the night. **Label: after seeing results.** The rule is `PREDICTION.md` in this folder, frozen in commit 4410a0e before this outcome was built. The script is `test.py` and the numbers are in `result.json`.

`test.py` is `../move_extensive/test.py` with only the outcome changed. The rows, gate, columns, z-scores, model, CR1 standard errors, halves and conditional logit are the same code, byte for byte. Only the constants (threshold .05/6, prediction +0.9, kill line +0.3), the outcome construction, the printed counts and the reported items differ. I checked the code on a random fake outcome (no outcome file read) before the one real run. No rule was changed afterwards. It runs in about 30 seconds.

## Verdict, by the rule written first

**UNSETTLED (p ≥ .0083).**

- β(`ch_rep`) on y_foreign = **+1.00 percentage points per SD** (SE 0.49, p .044).
- That is above the kill line of +0.3, so this is **not a kill**.
- It **misses the pass** only on p: .044 is not below .0083.
- The other pass conditions are met. Both halves are positive. The conditional logit is positive (+0.13) and converged.

## What was predicted

- **Question.** Move_extensive found +1.19 pp per SD for `ch_rep` on "the song is in Discogs-VI" (p .018). A Discogs-VI group needs only two distinct performer sets, so that sign could come from two places:
  - other artists recording loop-based songs;
  - the original artist's own credit variants ("Artist" and "Artist, Guest").
- **Outcome.** For each matched song:
  - An **own set** is a version whose performer list contains the song's artist (matched by normalised name).
  - O is all the names that appear in own sets.
  - A **foreign set** is a non-empty performer list that shares no name with O.
  - **y_foreign** = 100 if at least one foreign set exists, otherwise 0. **y_self** = y − y_foreign.
- **Prediction (two-part story):** β(`ch_rep`) on y_foreign = **+0.9**.
- **Artefact story:** under +0.3, with the rest of the effect on y_self.
- **Rules:**
  - **Pass:** β > 0, p < .0083 (.05/6), β > 0 in both halves, and a conditional logit > 0 that converged.
  - **Kill:** β < +0.3.
  - **Unsettled:** anything else.

## What came out

### Counts (printed before any β)

Rows: the same 9,588 songs by 1,741 artists, and every notes-side count reproduced. The gate passed as before (it was re-run unchanged).

- **Dropped: 2** (the limit is 25). Both are matched songs with no own set under the name rule:
  - *Kings of Convenience, "I'd Rather Dance With You"*: the group's versions are by Mary J. Blige and others.
  - *Beach Boys, "Surf's Up"*: the slug gives "beachboys", but Discogs has "thebeachboys". This is a miss by the matching rule.
  - Both songs are dropped from every model below, which leaves **9,586 songs**.
- **y = 100: 2,224 songs.**
- **y_foreign = 100: 2,130**, which is 95.8% of the matched songs.
- **y_self = 100: 94.** Only 94 matched songs have nothing but the artist's own credit variants.
- Diagnostic only: 175 performer names normalise to an empty string, mostly non-Latin names. A check made after the run found that none of them is in any song's own-name set O, so they change no y_foreign value.

### Power (printed before β)

- Clustered SE 0.494 pp (the rule expected 0.50 or less).
- Power at +0.9 with p < .0083: **0.21** (rule: about 0.20).
- The kill line fires with probability 0.11 if +0.9 is true, and 0.73 if the true effect is 0 (rule: 0.12 and 0.73).

### Primary model

Linear probability model, within artist, CR1 standard errors clustered by artist. My hand-coded CR1 matches statsmodels to 3e-14.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **`ch_rep` on y_foreign** | **+0.997** | 0.494 | 0.044 | +0.03 to +1.97 |

### Halves

| | Songs | Artists | y_foreign = 1 | `ch_rep` β (SE, p) |
|---|---|---|---|---|
| Half 0 | 4,616 | 886 | 1,046 | +0.45 (0.63, .48) |
| Half 1 | 4,970 | 855 | 1,084 | +1.43 (0.75, .058) |

Both halves are positive. Half 0 is small and far from significant.

### Conditional logit

statsmodels `ConditionalLogit` on y_foreign, grouped by artist:

- **Sample:** it drops 1,277 artists and 5,946 songs whose songs are all 0 or all 1, and keeps 464 artists and 3,640 songs.
- **`ch_rep`:** +0.132 log-odds per SD (SE 0.059, p .025).
- **Converged:** yes, by the score test, max |score|/nobs < 1e-5.
- **Cross-check:** my own fit of the exact likelihood (subset recursion, Newton) gives +0.132 as well.
- **One nuisance column:** the parentheses-flag control has no finite estimate, as in move_extensive. The two optimisers stop at −21 and −52. This is why the largest difference between the two fits is 31, and why Newton ran to its 50-step cap. The tested coefficients agree to about 1e-4.

## How firm

- **Against the kill (the artefact story as stated):** moderately firm.
  - The estimate is +1.00, almost exactly the two-part prediction.
  - The 95% range runs from +0.03 to +1.97, so the artefact story's "under +0.3" sits near its lower end but is not excluded.
  - The split itself counts against the artefact story more plainly than β does. Only 94 of 2,224 matched songs are own-variants-only, so y_foreign is almost the same outcome as y. Most of move_extensive's +1.19 has to sit in y_foreign (+1.00 of it).
- **For a pass:** not there. The p-value is .044 against .0083, and half 0 is weak.
- **Overall:** this is a lead at most. It is also after seeing results and on the same songs, so even a pass would only have been a lead needing fresh songs.

## What it cannot say

- **Not love, not a cover count.** "A foreign set exists" is the closest this data has to "another artist recorded it".
- **Aliases count as foreign.** Name matching misses aliases, so some of the artist's own variants count as foreign: a band member solo (Brian Wilson for the Beach Boys is the kind of case), name spellings, "The" prefixes. That bias favours the two-part story, so this result is weaker than it looks. The Beach Boys drop shows that the matching rule does miss.
- **Not fresh.** It uses the same 9,586 songs as move_extensive and was designed after seeing that result.
- **Low power.** Power was 0.21, so the miss on p does not mean the effect is absent.
- **No cause.** It shows association only. Era is held only through the artist fixed effect.

## Reported, deciding nothing

These items were fixed in the rule as reports. None of them changes the verdict.

| Item | Songs with y = 1 | `ch_rep` β (SE, p) | `ch_ic_mean` β (SE, p) |
|---|---|---|---|
| **β on y_self** | 94 | +0.19 (0.15, .19) | +0.33 (0.15, .025) |
| y on the same 9,586 rows | 2,224 | +1.19 (0.50, .018) | −0.10 (0.41, .82) |
| Foreign, looser ("a not in the set") | 2,134 | +1.00 (0.49, .042) | −0.46 (0.41, .27) |
| Foreign with karaoke or tribute sets removed | 2,130 | +1.00 (0.49, .044) | −0.43 (0.41, .30) |
| **`ch_ic_mean` on y_foreign** (primary model) | 2,130 | — | −0.43 (0.41, .30), 95% range −1.24 to +0.39 |

- **Additivity check:** β_foreign + β_self = β(y) on the same rows. It holds for every column, with a largest difference of 2.7e-15 (tolerance 1e-9). For `ch_rep`: +0.997 + 0.194 = +1.191.
- **How the karaoke/tribute variant was built:** own sets and O stay as in the primary outcome. Foreign sets with any name containing "karaoke" or "tribute" are then removed before y_foreign is decided. No song changed: the count stays at 2,130.
- **The y_self estimate for `ch_ic_mean`** (+0.33, p .025) rests on 94 songs. It answers no question in the rule and is not a finding.
- **Post-hoc diagnostic, not in the rule:** the empty-name check above, in which 0 songs were affected.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups and performer credits: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0. Run 04 did not read song 59, songs/p69, studies/holdout59 or any McGill hold-out file.
