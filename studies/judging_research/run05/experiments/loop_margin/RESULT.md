# The certified chord loop and uptake by other artists: result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 1f6c36d before any outcome was joined. The script is `test.py` and the numbers are in `result.json`.

The script followed the rule's order:
1. It reproduced the unit values.
2. It computed the measure on every clip from the notes alone.
3. It ran the gate.
4. It printed the notes-side power.
5. Only then did it join the outcome.

Before the real outcome, I checked the code on a random fake outcome. I also checked it on 200 more fake outcomes: the clustered SE gave p < .05 in 4.0% of them and p < .00714 in 0.5%, so it is honest. No rule was changed after the outcome was seen.

The heavy step was the per-clip margin on 16,563 clips. It took 1,299 s on 2 worker processes, with other experiments sharing the machine. The values are cached outside the repo in `/tmp/loop_margin_cache`, so a rerun of the model takes about 20 seconds.

**Verdict: KILL.** The estimate is slightly negative (−0.20 pp per SD), well below the +0.3 kill line.

## What was predicted

Within an artist's own songs, a chord loop that persistent homology can certify as a real loop goes with a higher chance of a "foreign" release. A foreign release means a performer set sharing no name with the original artist released the song (`y_foreign`). The measure is M, the certified loop margin.

- **Predicted:** **+0.8 percentage points per SD of M.**
- **Held:**
  - chord repetition (`ch_rep`) and its square
  - chord surprise (`ch_ic_mean`)
  - the number of sliding windows (ln anchors, counted before deduplication)
  - run 04's control block: chord-count bins, clips per song, ln beats and title flags
  - the artist fixed effect
- **To pass**, all four had to hold: β > 0, p < .00714 (two-sided, .05/7 for tonight's seven tests), β > 0 in both artist halves, and a converged conditional logit above 0.
- **Kill:** β below +0.3.

## The mathematics in plain words, with a worked example

Card 1 (Park, An, Kim & Kim, *TopPT*) gives a way to ask "does this signal really go round in a circle, and how sure can we be?" Here is how M applies it to a song section.

1. **The chord strip.** Every half beat, mark which of the 12 notes the current chord contains. Blur this a little over time, so the chord changes are soft edges instead of cliffs.
2. **Snapshots.** Take nine glimpses of the strip, evenly spread across 2 bars (and, separately, across 4 bars). Stack them into one long list of numbers. That list is a single point in a space with many directions. Slide the window forward a quarter beat at a time and take the next point. A section gives a cloud of up to 300 points.
3. **A loop makes a ring.** If the chords go round and come back, the window comes back to where it started, so the cloud lies on a closed ring. Persistent homology measures the ring's hole. Imagine growing a bubble around every point until the bubbles touch. The hole appears when the ring closes and disappears when the bubbles fill it in. The longer the hole survives, the more real the loop.
4. **How sure.** Card 1's subsampling bound asks how far a point could be from the rest of the cloud. It drops 1% of the points, 200 times, and measures how far the dropped points sit from the kept ones. The 95th percentile, doubled, is the uncertainty radius c. A hole is certified only if it survives longer than 2c.
5. **The margin.** M is whatever survives after subtracting 2c. It is divided by the spread of the chords, so loud or busy sections are not favoured. M = 0 means no loop could be certified.

**Worked example** (16 bars of 4/4 in C, one chord per bar; these are the rule's unit values, reproduced exactly):

| Progression | Hole lasts (4-bar window) | Uncertainty radius c | Hole minus 2c = M |
|---|---|---|---|
| **I–V–vi–IV, four times round** (C–G–Am–F) | 0.770 | 0.264 | 0.770 − 0.528 = **0.242** |
| **I–IV back and forth, eight times** (C–F–C–F) | 0.740 | 0.362 | 0.740 − 0.725 = **0.016** |
| **I alone for 16 bars** | (no movement at all) | | **no value** |

- **I–V–vi–IV** visits four different places and returns. Its 96 distinct snapshots spread fairly evenly round the ring, so the uncertainty is small and most of the hole is certified.
- **I–IV** also returns to its start, and its raw hole is nearly as long-lived. But its snapshots bunch at the two chords, with few points on the paths between them (64 distinct snapshots). The uncertainty radius is therefore large, and it eats almost the whole hole. That is the sense in which a back-and-forth is "nearly a segment, not a circle".
- **One chord held throughout** never moves, so there is nothing to measure.

The imaginers' bet was that the margin works like a safety buffer. Card 1's stability theorem says any disturbance smaller than half the margin leaves the circle intact. A cover re-dresses a song (new voicings, new tempo, new instruments), and a song whose loop survives that would be easier for other artists to take up.

## The measure on the notes (before the outcome)

- **Unit values:** I–V–vi–IV ×4 gives M = 0.242192 (226 windows, 96 after deduplication). I–IV ×8 gives 0.015590. I alone gives no value. All match the rule to 1e−6.
- **Every clip:** of 16,563 clips, 44 give no value and none give an error. 41.4% of clips certify a loop.
- **Matches the chair's run:** every clip's M equals the chair's notes-only run exactly (largest difference 0.0).
- **Songs:** 9,576 of 9,588 songs have M.
  - 48.5% of songs score 0.
  - The 10th, 50th, 75th and 90th percentiles are 0, 0.006, 0.124 and 0.242.
  - The share of songs with M > 0, by `ch_rep` tercile, is 36%, 65% and 54%. That is the inverted U the rule expected.
- **Gate 1, clip to clip:** 0.369 on 4,247 pairs, against a threshold of 0.20. **Passed.**
- **Gate 2, overlap:** the largest |Spearman| is −0.254, with chord count. Next come beats (+0.249), ln anchors (+0.247), ch_rep² (−0.224) and `mel_rep` (+0.209); `ch_rep` itself is +0.154. The threshold is 0.7. **Passed.**
- **Printed, deciding nothing:** ρ(M, A) = +0.188, where A is `arrow_of_time`'s measure. ρ(M, ln anchors) is +0.247 before deduplication and +0.116 after.
- **Notes-side power:** residual share 0.459, SE bound 0.625 pp. Power at +0.8 and p < .00714 is 0.079 (0.249 at p < .05). All of these are the chair's figures.

## The outcome

- **Songs:** N = 9,574 songs by 1,741 artists. 2,128 of them (22.2%) have a foreign release.
- **Dropped:** 12 songs with no M, and 2 with `y_foreign` undefined (clique missing or no own set).

## Power (printed before the estimate)

| | Clustered SE | Power at +0.8, p < .00714 | at p < .05 | Kill fires if +0.8 is true | Kill fires if the effect is 0 |
|---|---|---|---|---|---|
| Real data | **0.442 pp** | **0.19** | 0.44 | 13% | 75% |
| Notes-side bound in the rule | 0.63 | 0.08 | 0.25 | 21% | 68% |

As in run 04, the real SE is smaller than the notes-side bound. Power is still far below 0.5.

## Results

**Primary model:** linear probability, within artist, CR1 clustered by artist.

| | β (pp per SD of M) | SE | p | 95% range |
|---|---|---|---|---|
| **M on y_foreign** | **−0.20** | 0.44 | 0.64 | −1.07 to +0.66 |

The other tested columns in the same model decide nothing tonight: `ch_rep` +1.12 (SE 0.49), ch_rep² −0.15 (0.36), `ch_ic_mean` −0.40 (0.41), ln anchors +1.5 (2.3).

**Artist halves:**

| | Songs | Artists | Foreign | β | SE | p |
|---|---|---|---|---|---|---|
| Half 0 | 4,611 | 886 | 1,045 | **+1.39** | 0.60 | .021 |
| Half 1 | 4,963 | 855 | 1,083 | **−1.62** | 0.65 | .013 |

**Conditional logit** (statsmodels `ConditionalLogit`, grouped by artist, columns not demeaned):
- **Drops:** 1,278 artists and 5,942 songs whose songs are all foreign or all not. It keeps 463 artists and 3,632 songs.
- **z(M):** **−0.055** log-odds per SD (SE 0.053, p .29).
- **Convergence:** converged, judged by max |score|/nobs < 1e−5.

## Verdict, by the rule written first

**KILL.** β = −0.20 pp is below the +0.3 kill line. It is not in the "opposite sign" class, because p = .64 is far above .00714. The pooled estimate is negative, and so is the conditional logit.

- **How firm:** the predicted +0.8 lies outside the 95% range (−1.07 to +0.66), so the prediction as stated is rejected fairly firmly.
  - Power was only 0.19, though, and a true effect of about +0.5 pp is not ruled out.
- **What it means, by the rule:** within an artist's songs, a chord loop that card 1's method certifies does not go with more releases by other performers, once repetition and the window count are held. The "take-up face of looping" did not show up.

### Something odd: the two halves disagree

The halves point in opposite directions, and each is individually near p = .02. They differ by 3.01 pp (SE 0.89, z = 3.40, p = .0007), which is unusual for a random split of artists.

This is printed and decides nothing. It does not change the kill, which the pooled β decides on its own. It suggests M's association with foreign releases is very uneven across artists: some groups of artists may drive it one way and others the other. It may also mean the clustered SE understates the spread between artists for this measure. On the 200 fake outcomes the SE was calibrated, but fake outcomes cannot show heterogeneity across artists. Nobody should read the positive half as a finding. Pursuing it would need its own frozen rule.

## Reported, deciding nothing

These items were fixed in the rule as reports. They do not change the verdict.

| Item | β (SE, p) | N |
|---|---|---|
| The certified flag (z of the song's share of certified clips) in place of M | +0.42 (0.44, .34) | 9,574 |
| ln anchors counted after deduplication in place of before | −0.16 (0.43, .72) | 9,574 |
| Model without ch_rep² | −0.16 (0.43, .71) | 9,574 |
| y_foreign with "karaoke" or "tribute" performer sets removed | −0.20 (0.44, .64) | 9,574 |
| M on y (in Discogs-VI at all) | −0.03 (0.45, .94) | 9,576 |
| Intensive margin: z(log(1 + covers)) among versioned songs, plus `first_year`, in SD per SD | **−0.0005** (0.022, .98) | 2,224 |

- **The certified flag** is the only item with a positive sign. It is far from significant.
- **Karaoke and tribute sets:** 58 performer sets were removed, and no song's `y_foreign` changed. No song's foreign release rested on a karaoke or tribute set alone. So the Skeptic's "cover factories" worry does not touch this result. When deciding whether a set was foreign, the artist's own names were taken from all their sets.
- **Intensive margin:** the imaginers predicted ≥ 0 here, unlike `ch_rep`'s −0.042. The estimate is zero to three decimals. It is neither the predicted lift nor `ch_rep`'s penalty. M was re-standardised within these 2,224 songs.

## What it cannot say

- **The theory is qualitative here.** Card 1's guarantee is for a smooth single-valued signal. Chord chroma is a 12-channel step function, smoothed. The paper has no music application.
- **The calibration is practical, not proven.** B = 200 and b = 0.99n are the paper's practical settings, not the regime its theorem covers.
- **One section, not the song.** M describes one clip's loop. Clips are the sections Hooktheory users chose to transcribe.
- **The outcome is not lasting love.** `y_foreign` records whether some other performer set released the song in Discogs-VI. False non-matches (missing credits, retitles) only weaken an effect, so a null is weak evidence.
- **The songs are not fresh.** Run 04 used these 9,588 songs for `ch_rep` and `ch_ic_mean`.
- **Low power:** 0.19 at tonight's threshold. A small positive effect is not excluded.
- **Hits only, association only.**
- **McGill hold-out:** untouched. This test did not read song 59, songs/p69 or studies/holdout59.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0. Method: Park, An, Kim & Kim, "Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings", arXiv:2512.06324 (card 1). Persistent homology by ripser 0.6.15.
