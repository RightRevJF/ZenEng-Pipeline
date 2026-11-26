# Fresh songs, test 1 (chord repetition): result

Run 06, 26 November 2026. The rule is `PREDICTION.md` in this folder (commit 08b5167, frozen and pushed before any outcome was joined). Code: `test.py`. Full numbers: `result.json`.

## Verdict: **unsettled**
The estimate leans the predicted way and is a little larger than predicted, but it is far from tonight's bar (p .20 against the .00833 it needs). Every other pass condition held: both artist halves are positive, and the conditional logit is positive and converged. The kill line (β ≤ 0) did not fire.

## What was predicted
Run 04 found that, within an artist's own songs, the ones whose chords repeat more were a little more often released by some other artist (+1.00 percentage points per standard deviation, p .044, not enough to pass). All of those songs had already been looked at. This test asked the same question on **1,295 "fresh" songs** from the raw Hooktheory file: songs left out of the data pack, whose outcome nobody had opened. The prediction was **+1.0 pp per SD of chord repetition (ch_rep)**. The slope was estimated from the fresh songs' outcomes only, with the seen songs of the same 601 artists in the model to pin down each artist's baseline.

## What came out

| | Value |
|---|---|
| Songs in the model / artists | 5,768 (1,295 fresh + 4,473 seen) / 601 |
| Fresh songs found in Discogs-VI / with a release by another artist | 238 / 222 (17.1%; seen songs 23.8%) |
| **Estimate, fresh songs** (pp per SD of ch_rep) | **+1.32** (predicted +1.0) |
| Standard error (clustered by artist) | 1.04 |
| 95% range | −0.72 to +3.36 |
| Two-sided p | 0.20 (needed below 0.00833) |
| Artist half 0 / half 1 | +0.46 (SE 1.44) / +1.97 (SE 1.56), both positive |
| Conditional logit | +0.197 log-odds per SD (SE 0.152, p 0.19), converged; kept 226 artists, 2,687 songs |
| Power to detect +1.0 at p < .00833 | 0.047 (0.16 at p < .05) |

## How firm
Not firm. The design was nearly blind before any outcome was opened, and the script printed this before the estimate: the notes-only bound gave an SE of 1.66 pp and power of 0.02. The fake-outcome simulation in `../power_fake.json` gave an SE of 1.21 and a 3.4% chance of passing if the prediction were exactly true. The real SE came out a little smaller (1.04), so power was about 0.05. Even an effect exactly the size predicted would almost never have cleared the bar. The 95% range runs from slightly negative to more than three times the prediction. The result fits the prediction, but it also fits no effect at all.

## Checks before the outcome (all reproduced)
- The chord tokens rebuilt from the raw notes reproduce the data pack's ch_rep, chord count, melody-note count and beats on all 21,998 pack clips, with no difference.
- Counts: 1,946 fresh songs, 2,570 clips (1,765 songs with a video id). 1,825 fresh rows after dropping 120 songs with no chords and 1 duplicate. The battery has 5,768 rows (4,473 seen + 1,295 fresh) by 601 artists. Every sub-count in the rule also matched: 1,210 / 85 with and without a video id, 1,160 rows by 550 artists who also have seen songs, 932 rows by 238 artists with two or more fresh rows, and 32 songs mixing clips with and without a melody.
- The z scale is mean 0.2933 and SD 0.2295 over the 9,588 seen within-artist rows. The fresh battery rows' mean is 0.247.
- Gate: the rule says none applies, because ch_rep is the pack's own measure. The figures are reported anyway. Clip 1 against clip 2 agree at 0.395 on 432 fresh pairs (seen: 0.324 on 4,271). The largest overlap with another pack measure is ch_h_mean at −0.44, and ln_chg is +0.44 on the battery rows. A gate would have passed (stability ≥ 0.20, overlap ≤ 0.7).
- The match validation (cached in `../match_validation.json`) passed at 100% on all four checks.

## Reported, deciding nothing
| Item | Estimate (SE) | Note |
|---|---|---|
| Seen songs' slope (z_seen) | +1.74 (0.73), p .018 | a seen-song reading, already spent |
| In Discogs-VI at all (y), fresh | +1.50 (1.09), p .17 | |
| Early uptake (≤ 5 years) | +0.73 (1.01) | contrast not interpreted (run 02) |
| Late uptake (> 10 years) | +0.35 (0.75) | |
| Without fresh songs whose clique a seen song also matches | +1.18 (1.04) | 4 fresh rows dropped (see Deviations) |
| Fresh songs with a video id only | +1.43 (1.08) | 85 dropped |
| Karaoke/tribute sets removed | +1.32 (1.04) | no song changes (38 songs have such a set) |
| Fresh songs only, within artist (238 artists, 932 songs) | −0.85 (2.62) | very noisy |
| Without has_mel | +1.26 (1.05) | |

The fresh-only model, which uses no seen songs at all, points the other way, but its SE is 2.6 pp, so it says almost nothing. Most of the fresh estimate's precision comes from seen songs fixing each artist's baseline.

## What it cannot say
- y_foreign means "another performer set released it". That is not "loved long", and loop-based styles may collect remixes under other names. In practice it almost equals "in Discogs-VI at all": 222 of the 238 matched fresh songs count.
- Fresh songs are the ones the data pack left out, mostly chords-only transcriptions. They are not a random sample.
- The match is by title and artist name, so songs whose Hooktheory slug differs from the Discogs title are missed.
- "Fresh" means nobody had looked. It does not mean the outcome was absent from the repo: 222 fresh videos are already keys of the pack's covers file (the chair foresaw this, and nothing else reads them).
- Within-artist design, hit songs only, no cause. The McGill hold-out was not touched.

## Deviations
1. **Memory only:** the machine is shared, and the first two attempts were killed for lack of memory before any outcome was read. So `test.py` builds the fresh song list once and reuses it, rather than loading the raw file a second time. The logic is unchanged, and the counts are asserted and reproduce.
2. **A reported item, corrected (decides nothing):** `common.load_battery_outcomes` flags a fresh row as "clique also matched by a seen song" using every key of the pack's covers file. That file also holds 222 fresh videos, so the flag marked 223 rows, mostly fresh songs matched to their own clique. `test.py` reports that form as written (+0.91, SE 0.81, 223 rows dropped). Beside it is the intended form, built from the 13,198 seen songs' videos only (+1.18, SE 1.04, 4 rows dropped). `common.py` was not edited.
3. **Runs:** there was one notes-only run, then the full run. The full run was repeated once to add the corrected item above and a count of karaoke/tribute sets. The primary estimate, halves, logit and verdict were identical in both runs. No rule was changed.
