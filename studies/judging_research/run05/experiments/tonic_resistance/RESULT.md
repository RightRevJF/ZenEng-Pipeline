# Is home the hub of the chord map, and are such songs taken up by other artists? Result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder (frozen and pushed in commit 1f6c36d before any outcome was joined). The measure was first defined in run 03's `tonic_resistance`; where the two differ, tonight's rule governs. The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order. It built the measure from the notes, ran the gate, and printed the power before reading any outcome. I checked the code on a random fake outcome before reading the real one (`python3 test.py --fake`, which reads no outcome file), and no rule was changed afterwards. It runs in about 40 seconds in one process.

**Verdict: unsettled.** The estimate points the predicted way but is small and far from significant. It lands just past the kill line (−0.23 against −0.2), so the idea is not killed. It is not supported either.

## What was predicted

Draw each song's chords as a map: every chord is a stop, and every move between two chords is a road (more moves, a wider road). **H** measures how easy it is to get home to the tonic chord from everywhere else, compared with getting between two typical chords. H below 1 means home is the hub.

The claim was that within an artist's own songs, songs whose home is the hub (low H) are more often released by another artist. The outcome is run 04's **y_foreign**: did a performer with no name in common with the original artist release a version. Predicted: **−0.6 percentage points per SD of H**.

To pass, it needed all of these: β < 0, p < .00714 (.05 split over tonight's seven tests), β < 0 in both artist halves, and a conditional-logit coefficient < 0 that converged. β above −0.2 would be a kill.

## The measure and the gate (notes only, before the outcome)

- **Unit tests:** all five exact (5-cycle 1.0; star with home at the hub 0.6; home on a leaf 1.4; the same two stars written as chord clips, 0.6 and 1.4).
- **Songs:** 9,009 of the 9,588 songs have an H. 278 were dropped for having fewer than 3 distinct chords, 266 for having no chord on the home root, and 35 because home's connected piece had fewer than 3 chords. The 10th, 50th and 90th percentiles are 0.624, 0.818 and 1.143. All of these match the chair's figures exactly.
- **Gate 1, do two clips of the same song agree?** H was computed on clip 1 alone and on clip 2 alone, with size held. The Spearman correlation is **0.2030** on 3,512 pairs (raw 0.259). The line is 0.20, so it **passed, narrowly**, matching the chair's 0.203.
- **Gate 2, is H an existing measure under a new name?** After size is held, H's largest correlation with any other measure is −0.081 (with length in beats). Size explains 15.6% of H. The lines are 0.7 and 80%, so it **passed** easily.

## Power (printed before any β)

- **From the notes alone:** SE about 0.54 pp, power 0.06 at p < .00714 (0.20 at p < .05). This matches the chair.
- **From the real clustered SE:** SE 0.44 pp, **power 0.09** at p < .00714 (0.27 at p < .05).
- **How often the lines fire:** the kill line would fire 18% of the time if −0.6 were true, and 67% of the time if the true effect were zero.

## The outcome

9,007 songs by 1,736 artists. **2,001 songs (22.2%) have a version by another artist.** Two songs with an H were dropped because their y_foreign is undefined (no own performer set in the version group).

## Results

**Primary model:** a linear probability model within artist, clustered by artist.

| | β (pp per SD of H) | SE | p | 95% range |
|---|---|---|---|---|
| **H** | **−0.23** | 0.44 | 0.61 | −1.09 to +0.64 |

**Artist halves:**

| Half | Songs | Artists | β | SE | p |
|---|---|---|---|---|---|
| 0 | 4,343 | 884 | −0.50 | 0.64 | .44 |
| 1 | 4,664 | 852 | −0.06 | 0.60 | .92 |

**Conditional logit** (grouped by artist, columns not demeaned):

- **Coefficient:** −0.032 log-odds per SD (SE 0.044, p .48). It converged.
- **Sample:** it keeps 3,367 songs in 439 artists. It drops 5,640 songs in 1,297 artists whose songs are all in or all out.
- **Nuisance problem:** the parentheses-in-title control has no stable estimate, as in run 04. Songs with "(" in the title almost never get a foreign version within their artist. This does not affect H.

## Verdict, by the rule written first

**UNSETTLED.** β is negative, and negative in both halves and in the conditional logit, but p = .61 is nowhere near .00714.

- **Why not a kill:** β = −0.23 is just below the −0.2 kill line, by 0.03 pp. That is well inside the noise (SE 0.44), so it is luck which side of the line it fell. The rule is applied as written.
- **How firm:** not firm in either direction. The 95% range runs from −1.09 to +0.64. It holds the predicted −0.6, and it holds zero. With power 0.09, this test could not have confirmed a −0.6 effect, and agreement of only 0.20 between clips means any true effect shows up weakened.
- **What it means:** R03-I2 stays open. Run 03 also found unsettled on cover counts (β −0.019). Tonight's extensive-margin result has the same sign and is equally weak.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | β (SE, p) | Songs |
|---|---|---|
| Without `ch_ic_mean` | −0.26 pp (0.44, .56) | 9,007 |
| Dropping the 321 songs where home's piece is not the whole map | −0.22 pp (0.44, .62) | 8,686 |
| On y (in Discogs-VI at all) | +0.02 pp (0.44, .96) | 9,007 |
| Number of covers, among the 2,082 versioned songs (with first year held) | −0.017 SD per SD (0.014, .21) | 2,082 |
| y_foreign with karaoke and tribute performer sets removed | −0.23 pp (0.44, .61) | 9,007 |

- **Overlap with tonight's arrow of time:** ρ(H, A) = +0.28 on 8,373 songs, as the chair found.
- **Karaoke and tribute sets:** 47 of the model's songs have such a set, but every one of them also has another foreign performer. Removing these sets therefore changes no outcome, and the estimate is identical.
- **The other columns, for context:** `ch_rep` +1.46 pp (SE 0.66, p .027) and `ch_ic_mean` −0.56 pp (SE 0.46, p .22).

## What it cannot say

- **Low power (0.09):** a null clears nothing, and this small negative estimate proves nothing.
- **A thin measure:** two clips of the same song agree at only 0.20, the narrowest gate of the night. H is a noisy reading of each song.
- **Graph limits:** the map counts single steps only and treats V→I the same as I→V. "Home" relies on the first key Hooktheory lists.
- **Not unseen songs:** the matched songs' H was already tested on cover counts in run 03. The extensive contrast is new, but the songs are not.
- **What the outcome measures:** y_foreign is "another performer released a version", not lasting love. It covers hits only and shows no cause.
- **McGill hold-out:** untouched. Run 05 did not read song 59, songs/p69 or studies/holdout59.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
