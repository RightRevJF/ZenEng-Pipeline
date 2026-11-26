# Fresh songs, test 3: melody range. Result

Run 06, 26 November 2026. Rule: `PREDICTION.md` in this folder, plus the shared rules in `../fresh_repetition/PREDICTION.md` and `../common.py`, all frozen in commit 08b5167 before any outcome was joined. Script: `test.py`. Numbers: `result.json`. Runtime: about 1 minute.

## Verdict: **kill** (β ≥ 0)

The prediction said songs with a narrower melody range get taken up by other artists more often. On the fresh songs the slope came out on the wrong side of zero: **+0.69 percentage points per SD, not −0.7.** The frozen rule says "Kill: β ≥ 0", so this idea is killed for tonight. It is a weak kill. The test could barely see an effect of the predicted size (power about 1.5%). Under the fake-outcome check, a kill like this happens about half the time when there is no effect, and about a third of the time when the prediction is true.

## What was predicted
Within one artist's own songs, a narrower melody range goes with more uptake by another artist (y_foreign: a version of the song in Discogs-VI by performers who are not the original artist). The prediction was **−0.7 pp per SD** of the capped, folded melody range (SD 5.45 semitones), using only songs whose outcome nobody had looked at ("fresh" songs). To pass it needed all of the following: a negative slope, two-sided p < .00833 (six tests tonight), a negative slope in both artist halves, and a negative, converged conditional logit.

## What came out

| | Value |
|---|---|
| Rows (seen + fresh), artists | 4,746 (4,342 + 404), 563 |
| Fresh songs taken up by another artist (y_foreign = 100) | 69 of 404 (17.1%); seen 1,051 of 4,342 (24.2%) |
| **β(z_fresh), pp per SD** (predicted −0.7) | **+0.69** |
| Clustered SE | 1.58 pp |
| Two-sided p | 0.66 |
| 95% range | −2.40 to +3.78 |
| Artist half 0 / half 1 | +3.28 (SE 2.39) / −1.70 (SE 1.92): split |
| Conditional logit (log-odds per SD) | +0.062 (SE 0.242, p 0.80), converged |
| Power at −0.7 and p < .00833 (from this SE) | 0.015 (0.073 at p < .05) |

Every pass condition failed except convergence: the slope is positive, p is far above .00833, the halves disagree, and the logit is positive. The "opposite sign" rule (β > 0 with p < .00833) does not apply, because p is 0.66. So this is not evidence that wide-range songs get taken up more. It is simply a slope that leans the wrong way, with a range that runs from −2.4 to +3.8.

## How firm
- **Very little.** The SE (1.58 pp) is more than twice the predicted effect. Before the outcome was joined, the notes-side bound was 2.47 pp and the fake-outcome SE was 1.78 pp. Either way the power was 1 to 2%.
- Only 404 fresh songs have a melody, and their artists have few other songs.

## Checks that ran before the outcome (all reproduced)
- Unit values: 0, 4, 7, 12 → 12; 0, 4, 19, 12 → 7; C-major scale → 16.
- Fresh songs 1,946 / 2,570 clips; fresh rows 1,825; battery 5,768 = 4,473 + 1,295, 601 artists.
- Seen rows 9,588, all with a value; 10th/50th/90th percentiles 7 / 11 / 21. The cap drops 285 seen rows and 9 of the 413 fresh battery rows with a melody. z scale: mean 11.873, SD 5.452 (rule: 11.87, 5.45). Uncapped SD 17.475.
- Gate (run 05's, `gate(rows, "L2")` on the 9,588 seen rows): clip 1 vs clip 2 agreement 0.290 on 4,271 pairs (needs at least 0.20). The largest overlap is mel_ic_mean at +0.555 (needs at most 0.7); overlap with ch_rep is −0.093. **Passed.**
- Match validation (cached `../match_validation.json`): 100% on all four checks. Passed.

## Reported, deciding nothing
| Variant | β (SE), pp per SD | p |
|---|---|---|
| Run 05's form: uncapped, on run 05's SD of 17.5 (SE unreliable: the artefact rows carry the slope) | −0.47 (0.33) | 0.16 |
| Unfolded range, same 36-semitone cap | +2.02 (1.39) | 0.14 |
| z_seen (seen songs; already spent) | −0.83 (0.48) | 0.08 |
| β on y (in Discogs-VI at all) | −0.28 (1.56) | 0.86 |
| Early uptake (foreign version within 5 years) | +0.91 (1.48) | 0.54 |
| Late uptake (foreign version after 10 years) | +1.42 (1.15) | 0.22 |
| Karaoke/tribute sets removed | +0.69 (1.58) (no row changed) | 0.66 |
| Fresh rows whose Discogs group a seen song also matches, dropped | +1.50 (1.43) | 0.29 |
| Fresh rows with a video id only | −0.26 (1.48) | 0.86 |
| Fresh-only within-artist model (198 songs, 54 artists) | +3.31 (2.31) | 0.15 |

Two things stand out, and neither decides anything:
- The uncapped form and the seen songs both lean negative (−0.47, −0.83), which is run 05's direction. The capped fresh slope does not. With SEs this size, the difference between them is noise.
- **Most of the fresh "taken up" songs share their Discogs group with a seen song.** Of the 77 matched fresh rows here, 65 match a group that a seen song also matches. Once those are dropped, only 12 fresh y_foreign = 1 rows are left. Many fresh songs may be a second slug or section of a song already in the pack, so the fresh outcome is less independent than "never seen" suggests. (Across all 1,295 fresh battery rows the count is 223 of 238 matched.)

## What it cannot say
- y_foreign is uptake by other performers, not lasting love. The match is by title and artist name.
- Fresh songs with a melody are a small, unusual subset (most fresh clips are chords only). Hooktheory's octave field is the transcriber's choice, and one clip is one section.
- Within-artist comparison absorbs most of genre, not all of it. Hits only; no cause. The McGill hold-out was not touched.
- A kill at this power does not show that range is irrelevant. It shows that tonight's fresh songs did not lean the predicted way.

## Deviations (none change a rule)
1. **The maximum-value check.** PREDICTION.md says "on the 9,588 seen rows the maximum is 1,030 semitones". 1,030 is in fact the maximum over all 13,198 seen songs (clip and song values alike). Over the 9,588 within-artist rows the song maximum is 674.08. This figure is descriptive only. The script checks it over the 13,198 songs and prints both. Every count and value that the test uses reproduced exactly.
2. **Conditional logit columns.** `has_mel` is 1 on every row, so, as the rule says, it "drops out". The LPM drops it automatically. For the conditional logit, the script passes only the columns that vary within the artists it keeps (it dropped has_mel and nothing else), because a constant column cannot be identified there.
3. **Fresh clip agreement.** The chair's 0.396 on 52 pairs is over all 1,825 fresh rows, and the script reproduces it there. On the 1,295 fresh battery rows it is 0.431 on 44 pairs. Both are reported only.
4. **Readings of reported items that the rule left open.** "Run 05's exact form" uses the uncapped L2 on run 05's z scale but leaves out mel_ic_mean, which the shared rule bars from fresh models. "Unfolded range in place of L2c" applies the same 36-semitone cap to the unfolded range. The fresh-only model uses fresh rows with L2c by artists with two or more such rows.
5. Before the real outcome was joined, the script was checked end to end on a random fake outcome (`FAKE_Y`, written outside the repo). No outcome file was read in that run.

## Orchestrator's note (added after all six tests ran; no rule or verdict changes)

The "clique also matched by a seen song" flag in `common.load_battery_outcomes` was built from every key of the pack's covers file. That file was built by the maintainer over every raw Hooktheory video, so it already lists 222 of the fresh videos themselves. The flag therefore marked fresh songs matched to *their own* Discogs group, not to a seen song's. Rebuilt from the 13,198 seen songs' videos only, just 10 of the 312 matched fresh songs (across all 1,946) share a group with a seen song (4 rows in the battery, as `fresh_repetition/RESULT.md` found). So the caveat above that "most fresh positives are versions of seen songs" is wrong: the fresh outcomes are close to independent of the seen ones. The "dropped" readings above that use this flag mostly drop genuine fresh positives and should be ignored. They decided nothing.
