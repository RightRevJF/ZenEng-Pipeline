# Fresh songs, test 2: the arrow of time A on songs whose outcome had never been seen. Result

Run 06, 26 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 08b5167 before any outcome was joined. The shared fresh-song rules are in `../fresh_repetition/PREDICTION.md`, and the frozen code is in `../common.py`. The script is `test.py` and the numbers are in `result.json`.

The script followed the rule's order:

1. It reproduced the unit values and counts.
2. It built the columns.
3. It ran the gate.
4. It printed the power.
5. Only then did it join the outcome, through the guarded loader `common.load_battery_outcomes`. That loader reused the cached match validation (`../match_validation.json`, passed at 100% on all four checks).

Before the real run, I checked the code once on a random fake outcome. That run read no outcome file and wrote nothing in this folder. No rule was changed after the outcome was seen. The real run takes about 55 seconds.

**Verdict: UNSETTLED.** On the fresh songs the estimate is almost exactly zero: **+0.09 percentage points per SD** against the +0.6 predicted, with a standard error of 1.17 and p = .94. It is above zero, so the kill rule (β ≤ 0) does not fire. It is nowhere near the pass line (p < .00833). The two artist halves point opposite ways, and the conditional logit is a hair below zero. So by the written rule it is neither a pass nor a kill. In plain terms, the fresh songs show **no sign of the lean**, but the test was too weak to rule it out.

## What was predicted

A measures whether a song's chord changes "go one way round" (a looped I–V–vi–IV scores 1.00) or keep undoing themselves like a pendulum (a I–IV vamp scores 0.07). Run 05 found, on songs whose outcome had already been looked at, that within an artist's own songs, higher-A songs were a little more often released by another performer: +0.84 pp per SD, p = .035, not enough to pass.

Tonight asked one question: **does that lean show up on fresh songs that nobody had matched to Discogs before?**

- **Outcome:** y_foreign, whether the song's Discogs-VI version group holds a performer set sharing no name with the original artist.
- **Design:** the comparison is within artist. The slope for fresh songs is estimated separately from the slope for seen songs, so the tested number comes from fresh outcomes only.
- **Held constant:** chord repetition (ch_rep), chord count, clips per song, length, title flags, the number of chord changes, the number of distinct chords, whether there is a melody, and a fresh/seen indicator.
- **Predicted:** +0.6 pp per SD.
- **Pass:** all of the following.
  - β > 0 with two-sided p < .00833 (.05 split over tonight's 6 tests).
  - β > 0 in both artist halves.
  - The conditional logit is above zero and converged.
- **Kill:** β ≤ 0. **Opposite sign** (β < 0, p < .00833): killed. **Otherwise:** unsettled.

## Checks before the outcome (all reproduced)

| Check | Frozen figure | Got |
|---|---|---|
| Unit values A (I–V–vi–IV ×4 / I–IV ×8 / I–V–I–IV ×4) | 1.0000 / 0.0667 / 0.0667 | 1.0000 / 0.0667 / 0.0667 |
| Seen songs with a value of A | 8,774 | 8,774 |
| Seen A percentiles (10 / 50 / 90) | 0.333 / 0.833 / 1.000 | same |
| Seen mean / SD of A (the z scale) | 0.7589 / 0.2673 | same |
| Fresh songs / clips / rows; battery rows (fresh) / artists | 1,946 / 2,570 / 1,825; 5,768 (1,295) / 601 | same |
| Model rows with A | 4,920 = 4,032 seen + 888 fresh; 448 fresh artists; 590 in all | same |
| Gate: clip 1 vs clip 2 agreement (seen) | 0.302 (needs ≥ 0.20) | 0.302 on 3,294 pairs: **passed** |
| Gate: largest overlap with another measure | ln_chg −0.154 (needs ≤ 0.7) | ln_chg −0.154 (ch_rep +0.01): **passed** |
| Fresh clip agreement (reported) | 0.244 on 253 pairs | 0.244 on 253 |
| Power: notes-side SE bound | 1.44 pp | 1.438 pp |

## What came out

| | Estimate (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **Fresh songs (the test)** | **+0.09** | **1.17** | **.94** | −2.21 to +2.38 |
| Artist half 0 (455 fresh songs) | −0.77 | 1.68 | .65 | |
| Artist half 1 (433 fresh songs) | +1.41 | 1.70 | .41 | |
| Conditional logit (log-odds per SD; converged) | −0.004 | 0.124 | .97 | |
| *Seen songs in the same model (reported only)* | *+1.38* | *0.52* | *.0084* | *+0.35 to +2.40* |

- **Counts:** 4,920 songs by 590 artists; no rows were dropped.
  - Fresh songs: 888 (448 artists). 166 are in Discogs-VI at all and 158 were released by another performer (17.8%).
  - Seen songs: 4,032, of which 951 (23.6%) were released by another performer.
- **Power, judged before the estimate:** the clustered SE was 1.17 pp, so the chance of passing at p < .00833 if +0.6 were true was **0.018**, and 0.08 at p < .05. The fake-outcome simulation frozen in the rule gave the same picture (SE 1.06 to 1.43; pass rate 2%).
- **The conditional logit** used statsmodels. It kept 201 artists and 2,182 songs (359 fresh) and dropped the 389 artists whose songs were all 0 or all 1. It converged.

## Reported, deciding nothing

| Variation | Fresh estimate (SE, p) |
|---|---|
| G2, the back-and-forth share, in place of A (ρ = −0.96 with A) | −0.20 (1.05, .85): the mirror of A, again about zero |
| A on y (in Discogs-VI at all) | +0.24 (1.26, .85) |
| Early uptake (W01-J6a, foreign set within 5 years) | +0.03 (1.12, .98) |
| Late uptake (foreign set after 10 years) | −0.04 (0.94, .96) |
| Karaoke and tribute sets removed | +0.09 (1.17, .94): 32 songs had such a set, none changed |
| Fresh songs whose Discogs group is also a seen song's dropped (153 rows) | +1.29 (0.97, .18) |
| Fresh songs with a video id only (63 dropped) | −0.31 (1.17, .79) |
| Fresh songs only, artists with 2+ fresh songs (611 songs, 171 artists) | +0.78 (1.82, .67) |
| Without z(ch_rep) | +0.17 (1.17, .89) |
| Without has_mel | +0.10 (1.17, .93) |

**On the seen songs**, the same model gives +1.38 (p = .0084). This is the run 05 lean again, on a subset of the same seen songs. Those outcomes were already spent, so it confirms nothing. It also misses the line by a hair, and it is not a counted test.

## How firm, and what it cannot say

- **Nearly blind.** With an SE of 1.17 pp, even an effect of +2 pp would usually be missed at this threshold. The 95% range runs from −2.2 to +2.4. It holds the predicted +0.6, zero, and run 05's +0.84 alike. An unsettled result here clears nothing and refutes nothing.
- **The point estimate is informative only as a lean.** The fresh songs did not repeat the seen songs' +0.84 to +1.38. They came out near zero, and the conditional logit was at zero. That is mild evidence against the lean carrying over, but not enough to kill it.
- **Many fresh songs share a Discogs group with a seen song.**
  - 223 of the 1,295 fresh battery songs, and 153 of the 888 in this model, matched a Discogs group that a seen song also matches. These are often the same song under another Hooktheory page.
  - Dropping them moves the estimate to +1.29 (p = .18). That is reported only, and still far from the line.
- **What y_foreign measures.** y_foreign is uptake by other performers, not lasting love. The match is by title and artist name.
- **What the fresh songs are.** They are mostly chord-only transcriptions that the data pack left out. They are not a random sample of songs, and their clips are shorter: 10.6 chord tokens on average against 14.4 for seen songs. ln_chg and the chord-count bins hold this, but A leans towards 1 when changes are few.
- **Scope.** The comparison is within artist only, and it says nothing about cause. The McGill hold-out was not touched. Song 59, songs/p69 and studies/holdout59 were not read.

## Deviations

None. The rule ran as written. The fake-outcome dry run (`FAKE_Y`) is a code check only and wrote outside this folder.

## Orchestrator's note (added after all six tests ran; no rule or verdict changes)

The "clique also matched by a seen song" flag in `common.load_battery_outcomes` was built from every key of the pack's covers file. That file was built by the maintainer over every raw Hooktheory video, so it already lists 222 of the fresh videos themselves. The flag therefore marked fresh songs matched to *their own* Discogs group, not to a seen song's. Rebuilt from the 13,198 seen songs' videos only, just 10 of the 312 matched fresh songs (across all 1,946) share a group with a seen song (4 rows in the battery, as `fresh_repetition/RESULT.md` found). So the caveat above that "most fresh positives are versions of seen songs" is wrong: the fresh outcomes are close to independent of the seen ones. The "dropped" readings above that use this flag mostly drop genuine fresh positives and should be ignored. They decided nothing.
