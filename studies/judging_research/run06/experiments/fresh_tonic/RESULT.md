# Fresh songs, test 4: tonic resistance H. Result

Run 06, 26 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 08b5167 before any outcome was joined. The shared rules are in `../fresh_repetition/PREDICTION.md` and `../common.py`. Code: `test.py`. Numbers: `result.json`.

**Verdict: unsettled** (p ≥ .00833, and the two artist halves split). Nothing passed and nothing was killed.

## What was predicted
Picture a song's chords as an electrical circuit: each chord is a point, and each move between two chords is a wire. H measures how hard it is to get home (the tonic chord) from the other chords, compared with the average chord. A low H means home sits at the centre of the song, with many short routes back to it. The prediction (idea R03-I2, carried over from run 05) was this: **among one artist's own songs, the songs with a more central home (lower H) are more often recorded by another artist.** The predicted size was **−0.6 percentage points per standard deviation of H**. The test used only "fresh" Hooktheory songs, which are songs left out of the data pack and whose cover outcome nobody had looked at before tonight.

## What came out

| | Value |
|---|---|
| Rows (songs) in the model | 5,144 (4,147 seen + 997 fresh), 598 artists |
| Fresh songs released by another artist (y_foreign = 100) | 171 of 997 (17.2%); seen songs 23.9% |
| **Estimate, β(z_fresh)** | **−0.25 pp per SD** (predicted −0.6) |
| Clustered SE | 0.75 pp |
| Two-sided p | 0.74 (needed < .00833) |
| 95% range | −1.71 to +1.21 pp |
| Artist half 0 / half 1 | +0.25 (SE 0.96) / −0.78 (SE 1.06): **split** |
| Conditional logit | −0.065 log-odds per SD (SE 0.12, p 0.59), converged |
| Power to detect −0.6 at p < .00833 (from this SE) | 0.034 (0.13 at p < .05) |

The estimate leans the predicted way, but it is about a third of an SE from zero, so it is consistent with no effect and with effects in either direction. Under the rule as written:
- **Pass** needed β < 0, p < .00833, β < 0 in both halves, and a converged logit below 0. The p-value and the halves both fail.
- **Kill** needed β ≥ 0. β is −0.25, so the kill does not fire.
- **Unsettled** covers everything else, so the verdict is unsettled.

## How firm this is
- **Very weak.** With an SE of 0.75 pp, a true effect of −0.6 would pass about 3% of the time. The test is close to blind, as `PREDICTION.md` warned: the fake-outcome power was 0.042 (calibrated) or 0.050 (homogeneous), and the SE came out between the two fake worlds (0.85 and 1.12).
- The kill line (β ≥ 0) would have fired 21% of the time if −0.6 were true and 50% of the time if the true effect were zero. That it did not fire tells us little.
- The fresh songs' clip-to-clip agreement on H is low: 0.182 on 243 pairs, against 0.203 on the seen songs. Low agreement shrinks any true effect toward zero.

## Steps, in the frozen order
1. **Unit tests:** reproduced exactly (5-cycle 1.0; star with home at the hub 0.6; home on a leaf 1.4; the same stars written as chord clips 0.6 and 1.4).
2. **Seen reproduction:** 9,009 of 9,588 seen songs have H; the 10th/50th/90th percentiles are 0.624 / 0.818 / 1.143; mean 0.870, SD 0.2583. The shared counts reproduce: 1,946 fresh songs, 2,570 clips, 1,825 fresh rows, 5,768 battery rows (1,295 fresh) by 601 artists. The H rows reproduce: 5,144 = 4,147 seen + 997 fresh, fresh rows by 527 artists, 298 fresh battery rows with no H. Everything matched.
3. **Gate on the seen songs (passed):** residualised clip-to-clip agreement was 0.2030 on 3,512 pairs (needs ≥ 0.20; raw 0.259). The largest overlap with another measure was beats at −0.081 (needs ≤ 0.7). Overlap with ch_rep was +0.002. R² on the size block was 0.156 (needs ≤ 0.8). On the fresh songs the agreement was 0.182 on 243 pairs (raw 0.213), which was reported but not gated.
4. **Notes-side power:** the SE bound was 1.196 pp (frozen as 1.20). Power at .00833 was 0.017.
5–6. **Match validation:** passed at 100% on all four checks (the cached `../match_validation.json`, not deleted). The outcome was then joined through `common.load_battery_outcomes`. No rows were dropped as NaN.

## Reported, deciding nothing

| Item | β (pp per SD) | SE | p |
|---|---|---|---|
| z_seen (seen songs, already spent) | −0.37 | 0.61 | 0.55 |
| On y (in Discogs-VI at all) | +0.45 | 1.04 | 0.67 |
| Early uptake (foreign version within 5 years) | −0.66 | 0.71 | 0.35 |
| Late uptake (foreign version after 10 years) | +0.30 | 0.63 | 0.64 |
| Karaoke/tribute sets removed (36 rows have such a set; 0 flip) | −0.25 | 0.75 | 0.74 |
| Fresh rows whose clique a seen song also matches dropped (167 fresh rows) | −0.03 | 0.65 | 0.97 |
| Fresh rows with a video id only | +0.15 | 0.83 | 0.86 |
| Without has_mel | −0.24 | 0.75 | 0.75 |
| Fresh rows whose home piece is not the whole graph dropped (28 rows) | −0.34 | 0.77 | 0.66 |
| Fresh-only within-artist model (702 rows, 232 artists) | +0.41 | 0.71 | 0.56 |

ρ(H, A) on the fresh rows is +0.15 (779 rows). The fresh rows have 181 with y = 100 and 171 with y_foreign = 100. Every reading has |β| < 1 SE, and the signs disagree across items. None of them points anywhere.

## What it cannot say
- It cannot say H does not matter. The test could not have detected the predicted size, and a null result clears nothing.
- The model counts releases by another artist found by title and artist name in Discogs-VI. That is not lasting love, and it shows no cause.
- The fresh songs are not a random sample. Most are chords-only clips with few distinct chords. A loop of 3 to 6 chords gives a small circuit, and H is noisy on small circuits.
- Within-artist comparison absorbs most genre differences, but not all. The McGill hold-out was not touched.
- The idea was already at its kill line on the seen songs in run 05 (−0.23). Tonight's fresh reading (−0.25) sits in the same place: a small lean the predicted way, far from significant. Whether to retire R03-I2 is Jason's decision.

## Deviations and notes
- **No rule was changed, and no shared code was edited.** No bug fix was needed.
- `common.H_song` does not return the size of home's connected piece. The reported item "home piece not the whole graph" needed it, so `test.py` computes it with the same rules (`tpiece`).
- I added one unit test: a 5-cycle written as a chord clip, which also gives 1.0.
- `PREDICTION.md` says fresh z reaches 13.5. That holds over all 1,825 fresh rows (max 13.6). Within the 997 battery rows the max is 11.15. The fresh gate figure (0.182 on 243 pairs) is likewise over all fresh rows. Over the battery fresh rows alone it is 0.119 on 183 pairs (reported only).
- z(ch_rep) enters as one column covering seen and fresh rows, as in `../power_fake.py`.
- In the conditional logit the nuisance column `parens` had no stable estimate. The tested coefficient is unaffected, and convergence was confirmed.
- Runtime is about 90 seconds. `python3 test.py --notes-only` runs steps 1–4 and writes nothing.

## Orchestrator's note (added after all six tests ran; no rule or verdict changes)

The "clique also matched by a seen song" flag in `common.load_battery_outcomes` was built from every key of the pack's covers file. That file was built by the maintainer over every raw Hooktheory video, so it already lists 222 of the fresh videos themselves. The flag therefore marked fresh songs matched to *their own* Discogs group, not to a seen song's. Rebuilt from the 13,198 seen songs' videos only, just 10 of the 312 matched fresh songs (across all 1,946) share a group with a seen song (4 rows in the battery, as `fresh_repetition/RESULT.md` found). So the caveat above that "most fresh positives are versions of seen songs" is wrong: the fresh outcomes are close to independent of the seen ones. The "dropped" readings above that use this flag mostly drop genuine fresh positives and should be ignored. They decided nothing.
