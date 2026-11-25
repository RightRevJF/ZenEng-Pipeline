# Steps around the circle of fifths, and whether another artist takes the song up: result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder (frozen in commit 1f6c36d before any outcome was joined). The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order: it checked the measure on made-up chord progressions, built the measure from the notes, ran the gate, printed the power, and only then read the outcome. I checked the code on a random fake outcome first (no outcome file read), and no rule was changed afterwards. It runs in about a minute on one process.

**Verdict: killed.** The estimate is essentially zero (+0.01 percentage points per SD), above the kill line of −0.2. This also closes R03-F1, as the rule says.

## What was predicted

Each chord can be placed on the circle of fifths (the angle of its 5th Fourier coefficient, after Amiot). A song's chords then trace a path around that circle, and FP is the average size of a step along it, in radians. A I–V–vi–IV loop steps small (FP 0.52); I–IV–V steps a little larger (0.70); chromatic jumps step large.

The prediction: **within an artist's own songs, a song whose chords take smaller steps is more likely to be released by another artist** (y_foreign: its Discogs-VI version group holds a performer set that shares no name with the original artist). Predicted size: **−0.6 percentage points per SD of FP**. Chord repetition (`ch_rep`), chord surprise (`ch_ic_mean`), chord count, clips per song, length, title flags and the artist were all held.

To pass, it needed all of: β < 0, p < .00714 (two-sided; .05 shared over tonight's seven tests), β < 0 in both artist halves, and a converged conditional logit below zero. β above −0.2 is a kill.

## The measure, checked before the outcome

- **Made-up progressions:** every step size the rule lists came out exactly (I→V, I→IV, I→vi, ii→V = 0.524; I→iii, I→♭VII, I→i, IV→V = 1.047; I→♭VI 2.094; I→♭II 2.618; V→vi and I→ii = 0; V7 sits where I does; augmented and diminished-seventh chords have no place). The worked examples gave FP 0.524 and 0.698, as written.
- **Songs:** all 9,588 songs (1,741 artists) have a value. Of 229,464 chord moves, 2,512 were skipped because a chord had no place on the circle. 11.3% of the kept moves are zero steps. The middle 80% of songs run from 0.449 to 1.197 rad (median 0.714), exactly the chair's figures.
- **Gate 1, does the measure agree with itself?** FP from a song's first clip against its second clip: Spearman 0.407 on 4,268 pairs. The line is 0.20, so it **passed**.
- **Gate 2, is it an old measure under a new name?** The largest overlap was +0.286 with chord surprise (`ch_ic_mean`), then +0.231 with the number of distinct chords and +0.211 with links. The line is 0.7, so it **passed**.
- **Diatonicity (D5):** it correlates −0.731 with FP, so it was not tested on its own; it is reported below.

## The outcome

9,588 songs; 2 were dropped because y_foreign could not be decided (by run 04's rule: the version group is missing, or it lists no set by the original artist). That leaves **9,586 songs by 1,741 artists, of which 2,130 (22.2%) were released by another artist**. 2,226 songs are in Discogs-VI at all.

## Power (printed before the estimate)

| | SE (pp per SD) | Power at −0.6, p < .00714 | at p < .05 |
|---|---|---|---|
| Notes-side bound in the rule | 0.52 | 0.06 | 0.21 |
| Real clustered SE | **0.32** | **0.21** | 0.47 |

As in run 04, the real SE came out smaller than the bound, because within an artist the outcome varies less than its overall rate suggests. Power is still low.

## Results

**Primary model** (linear probability, within artist, standard errors clustered by artist):

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **FP** | **+0.01** | 0.32 | 0.96 | −0.61 to +0.64 |
| `ch_rep` (held) | +1.00 | 0.50 | | |
| `ch_ic_mean` (held) | −0.43 | 0.43 | | |

**Artist halves:**

| Half | Songs | Artists | β (SE, p) |
|---|---|---|---|
| 0 | 4,616 | 886 | +0.37 (0.45, .41) |
| 1 | 4,970 | 855 | −0.33 (0.45, .46) |

The halves point opposite ways, each well inside its noise.

**Conditional logit** (grouped by artist, columns not demeaned): FP −0.004 log-odds per SD (SE 0.050, p .94). It converged (max |score|/nobs below 1e-5). It drops 1,277 artists and 5,946 songs whose songs are all taken up or none are, and keeps 464 artists and 3,640 songs. As in run 04, the parentheses-in-title control runs off to a large negative value (−21), because titled-in-parentheses songs are essentially never taken up within their artist; it does not touch FP.

## Verdict, by the rule written first

**KILL.** β = +0.01 pp is above the kill line of −0.2. It was not "opposite sign" (it is not positive at p < .00714). Under the rule, a kill here also closes R03-F1, which had stayed "testing" only while unsettled.

**How firm:** moderate. The estimate sits right at zero, and with the real SE the kill line fires about 73% of the time if there is no effect, but only about 10% of the time if −0.6 were true. Still, the predicted −0.6 lies just at the edge of the 95% range (−0.61 to +0.64), so an effect of that size is not ruled out at the usual 5% level; effects of −0.3 or smaller are comfortably compatible with the data. What the test does say clearly is that there is no sign of the predicted lean: the primary estimate, the conditional logit and the pooled halves all sit at zero.

**What it means:** how far a song's chords move around the circle of fifths does not, within an artist's own catalogue, tell you whether another artist released it. Run 03's lean on cover counts (−0.017, unsettled) does not carry over to the extensive margin.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | β (SE, p) | Songs |
|---|---|---|
| D5 (diatonicity) in place of FP; its author predicted positive | +0.34 pp per SD (0.34, .32) | 9,586 |
| FP without chord surprise held | −0.06 (0.31, .84) | 9,586 |
| FP on y (in Discogs-VI at all) | −0.08 (0.33, .81) | 9,588 |
| FP on the intensive margin: z(log(1 + covers)) among the versioned songs, with `first_year` added | −0.026 SD per SD (0.020, .19) | 2,226 (651 artists) |
| FP on y_foreign with karaoke and tribute sets removed | +0.01 (0.32, .96); no song changed (still 2,130) | 9,586 |

- **ρ(FP, D5)** = −0.731.
- **Share of zero steps:** 11.3% of all kept moves; 11.0% averaged over songs.
- The intensive-margin estimate leans the way run 03's cover-count test did (run 03: −0.017, p .36), at a similar size and again well short of any threshold. It is a report, not a test, and those songs overlap run 03's.
- D5 leans the way its author guessed (more diatonic, more uptake), but at p .32 it is noise.

## What it cannot say

- **Coarse geometry:** a chord's place on the fifths circle is its centre of gravity, not its function. I, ii and V7 share a place, as do V and vi, so V7→I and V→vi count as no step.
- **Modulations:** the key is taken from each clip's first key marking; key changes inside a clip are not followed.
- **The songs are not unseen:** the matched songs' FP was already tested on cover counts in run 03, and run 04 used all 9,588 songs for `ch_rep` and `ch_ic_mean`. The extensive contrast for FP is new.
- **The outcome:** y_foreign records that some other performer released the song, not lasting love. False non-matches (missing credits, retitles) are mixed in with songs nobody covered, which weakens any effect.
- **Low power:** 0.21 at the real SE. A true effect of around −0.3 pp or smaller could hide here.
- **No cause; hits only.**
- **McGill hold-out:** untouched. This test did not read song 59, songs/p69, studies/holdout59 or any hold-out file.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
