# Fresh songs, test 5: diatonicity (R04-G1). Result: **kill**

Run 06, 26 November 2026. Rule: `PREDICTION.md` in this folder, committed in 08b5167 before any outcome was joined (shared fresh rules in `../fresh_repetition/PREDICTION.md`, code in `../common.py`). Script: `test.py`; full numbers: `result.json`. Runtime 49 seconds.

## What was predicted
The idea (the Geometer, run 04): harmony that stays inside one major scale ("diatonic") survives being re-keyed, revoiced or inverted, so other artists should pick it up more easily. The measure, D5, is the size of the fifth Fourier coefficient of a clip's chord notes, weighted by how long each chord lasts. It is highest for harmony that stays in one key. The prediction: on songs whose outcome nobody had looked at ("fresh songs"), comparing songs by the same artist, **one standard deviation more diatonic goes with +0.5 percentage points more chance that another artist released the song** (y_foreign). The fifths path (FP), the non-triad share (NT) and chord repetition were held fixed, as the author asked.

The rule, written first: **pass** needs a positive slope with two-sided p < .00833, positive in both artist halves, and a conditional logit that is positive and converges. **Kill** if the slope is zero or below. A kill closes R04-G1.

## What came out
The slope came out slightly **negative**: −0.29 pp per SD. By the rule written first, that is a **kill**. **R04-G1 is closed.**

| | Value |
|---|---|
| Slope on fresh songs (pp per SD of D5) | **−0.29** (predicted +0.5) |
| Standard error (clustered by artist) | 1.19 |
| Two-sided p | 0.80 (needed < .00833) |
| 95% range | −2.63 to +2.04 |
| Artist half 0 / half 1 | −2.80 (SE 1.76) / +1.24 (SE 1.68): they disagree |
| Conditional logit | +0.060 (SE 0.147, p 0.68), converged |
| Rows | 5,707 songs by 601 artists: 4,472 seen + 1,235 fresh |
| Released by another artist | fresh 208 of 1,235 (16.8%); seen 1,064 of 4,472 (23.8%) |
| Power to detect +0.5 at p < .00833 | **0.014** (0.070 at p < .05) |

The conditional logit leans slightly the other way from the main model, and the two halves point in opposite directions. All of this is noise around zero.

## How firm is it
Not firm at all. The design could barely see an effect of the predicted size. The standard error of 1.19 pp is more than twice the predicted +0.5. If the prediction were true, a study like this would pass about 2% of the time. Before the outcome was joined, the fake-outcome simulation (`../power_fake.json`) showed this kill line fires about 49% of the time when there is no effect and 33% of the time when the prediction is true. So tonight's kill moves the odds against the idea only by a factor of about 1.5. The kill is still binding because the rule says so, and the idea was already ranked last. Run 05 had killed the fifths path, and run 05's first principles had recommended deleting the pair.

## Checks before the outcome (all reproduced)
- **Unit values:** C major triad 0.6440; C, F, G 0.5864; C and A♭ 0.3220; NT of I, V7, vi, IV 0.2500.
- **Seen songs:** all 9,588 have D5, with mean 0.5253 and SD 0.0948. FP percentiles 0.449 / 0.714 / 1.197; FP mean 0.7822, SD 0.3329. NT mean 0.281, SD 0.3074. ρ(D5, FP) −0.731; ρ(D5, NT) −0.215. NT's largest overlap is ch_ic_mean +0.69.
- **Shared counts:** 1,946 fresh songs, 2,570 clips, 1,825 fresh rows. The battery has 5,768 rows (4,473 seen + 1,295 fresh) by 601 artists. The model rows are 5,707 (4,472 + 1,235), with the fresh rows by 585 artists; 60 fresh rows had no FP.
- **Gate (passed):** with FP and NT held, two clips of the same song agree at 0.342 on 4,268 pairs (threshold 0.20). Without holding them, agreement is 0.502, and FP and NT explain 55% of clip D5. D5's largest overlap with the pack measures is ch_ic_mean −0.423 (limit 0.7).
- **Match validation:** the cached `../match_validation.json` passed at 100% on all four checks. It was not deleted.
- **Notes-side power:** SE bound 1.54 pp, power 0.012, printed before the outcome was joined.

## Reported, deciding nothing
| Variant | Slope (SE), p |
|---|---|
| D5 without FP and NT (run 05's printed form) | +0.03 (0.98), 0.97 |
| Seen songs' slope (z_seen; already spent) | +0.51 (0.68), 0.45 |
| On y (in Discogs-VI at all) | −0.05 (1.17), 0.96 |
| Early uptake (W01-J6a, within 5 years) | +0.74 (0.95), 0.44 |
| Late uptake (after 10 years) | −0.10 (0.94), 0.92 |
| Karaoke and tribute sets removed | −0.29 (1.19), 0.80 (no song changed) |
| Fresh rows whose clique a seen song also matches, dropped (206 rows) | −0.75 (0.95), 0.43 |
| Fresh rows with a video id only | −0.36 (1.20), 0.77 |
| Without has_mel | −0.27 (1.19), 0.82 |
| Fresh rows only, 229 artists with two or more | −0.20 (2.13), 0.93 |

Nothing here comes near significance, and the early and late readings point in different directions. As run 02 ruled, nothing is decided on their contrast.

**A point for the chair (it does not change the verdict):** of the 238 fresh battery songs that matched Discogs-VI, 223 matched a clique that a seen song also matches. 222 of the fresh videos are already keys in the pack's covers file, and the slug match and the video match agree on 99.8% of fresh songs that have a video. So most fresh positives are versions of songs already in the seen set, under another artist or title slug. The fresh outcome is less independent of the seen one than "never seen" suggests. The clique-collision drop above is the reading without them.

## What it cannot say
- A null this weak clears nothing. It does not show that diatonicity is irrelevant to uptake. It only shows that these 1,235 fresh songs did not lean the predicted way.
- With FP held, D5 asks what diatonicity adds to the fifths path, which was itself killed. Even a pass would have been a lead, not a finding.
- y_foreign means "released by another artist", not lasting love. The match goes by title and artist name. Fresh songs are the ones the data pack left out, mostly chords-only clips, so they are not a random sample. Within-artist comparison removes most of genre, not all. Hits only, no cause. The McGill hold-out was not touched.

## Deviations
None from the rule. No shared code was changed. One descriptive note: the chair's "fresh clip 1 vs clip 2 agreement of raw D5, 0.395 on 432 pairs" reproduces exactly over all 1,825 fresh rows. Over the battery's fresh rows it is 0.325 on 346 pairs, and over the model's fresh rows 0.288 on 339 pairs. This figure is reported only and decides nothing.

Data credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.

## Orchestrator's note (added after all six tests ran; no rule or verdict changes)

The "clique also matched by a seen song" flag in `common.load_battery_outcomes` was built from every key of the pack's covers file. That file was built by the maintainer over every raw Hooktheory video, so it already lists 222 of the fresh videos themselves. The flag therefore marked fresh songs matched to *their own* Discogs group, not to a seen song's. Rebuilt from the 13,198 seen songs' videos only, just 10 of the 312 matched fresh songs (across all 1,946) share a group with a seen song (4 rows in the battery, as `fresh_repetition/RESULT.md` found). So the caveat above that "most fresh positives are versions of seen songs" is wrong: the fresh outcomes are close to independent of the seen ones. The "dropped" readings above that use this flag mostly drop genuine fresh positives and should be ignored. They decided nothing.
