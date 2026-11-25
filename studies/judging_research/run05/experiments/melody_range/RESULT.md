# Any voice can sing it (folded melody range) and uptake by other artists: result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 1f6c36d before any outcome was joined. The script is `test.py` and every number is in `result.json`. The script followed the rule's order. It checked the unit values, built the measure from the notes and ran the gate. It printed the notes-side power, and only then joined the outcome. Before the real run I checked the code on a random fake outcome, which read no outcome file. No rule was changed after the outcome was seen. The script runs as one process in under a minute.

**Verdict: UNSETTLED.** The estimate points the predicted way: narrower range, more uptake. It falls short of the night's significance line (p = .11 against .00714), and it is not weak enough to kill.

## What was predicted

The claim is that the original artist's voice is fixed, while other singers take up songs an ordinary voice fits. The comparison is within an artist's own songs, so a narrower melody range should go with a higher chance that another artist releases the song.

- **Measure L2, the folded melody range:** for each clip (one section), take the melody notes and fold any written leap of more than an octave back inside an octave. This removes octave errors in the transcription. The value is the span in semitones between the 5th and 95th percentiles of pitch, weighted by note length. The song value is the average over its clips.
- **Outcome, y_foreign:** did a performer set sharing no name with the original artist release the song (run 04's rule).
- **Held in the model:** melody leapiness (`mel_ic_mean`, since leaps widen range), chord repetition (`ch_rep`), chord surprise (`ch_ic_mean`), run 04's controls (chord count, clips per song, length, title flags) and the artist fixed effect.
- **Prediction:** **−0.7 percentage points per SD** of range.
- **To pass, it needed all of these:**
  - β < 0;
  - p < .00714 (.05 split over tonight's seven tests);
  - β < 0 in both artist halves;
  - a converged conditional logit below 0.
- **Kill:** β above −0.2.

## Measure and gate (notes only, before the outcome)

- **Unit values reproduced exactly:**
  - pitches 0, 4, 7, 12 give 12;
  - 0, 4, 19, 12 (a G written an octave high) give 7;
  - the C-major scale gives 16.
- **Rows:** 9,588 songs by 1,741 artists, and every song has a value. The 10th, 50th and 90th percentiles are 7, 11 and 21 semitones. Folded and unfolded range agree at Spearman +0.942. All of these match the chair's figures.
- **Gate 1, two clips agree** (clip 1 against clip 2 of the same song, 4,271 pairs): 0.290. It needs 0.20 or more, so it **passed**.
- **Gate 2, not a renamed measure:** the largest overlap is with `mel_ic_mean` at +0.555. It needs 0.7 or less, so it **passed**. That is why `mel_ic_mean` is held in the model.

## The outcome

N = 9,586 songs by 1,741 artists. Two matched songs had no usable version group and were dropped, as the rule says. **2,130 songs (22.2%) were released by another artist.**

## Power (printed before any β)

| | SE (pp) | Power at −0.7, p < .00714 | at p < .05 |
|---|---|---|---|
| Notes-side bound (in the rule) | 0.49 | 0.10 | 0.30 |
| Real clustered SE | **0.26** | **0.49** | 0.76 |

The real SE came out much smaller than the bound, as in run 04. This test was therefore better placed than planned: roughly an even chance of passing if −0.7 were true.

## Results

**Primary model: linear probability, within artist, CR1 clustered by artist.** My CR1 matches statsmodels to within 1e-15.

| | β (pp per SD) | SE | p | 95% range |
|---|---|---|---|---|
| **L2, folded range** | **−0.42** | 0.26 | 0.11 | −0.94 to +0.10 |

**Artist halves:** the sign is the same in both, and neither half is significant on its own.

| | Songs | Artists | Foreign release | β (SE, p) |
|---|---|---|---|---|
| Half 0 | 4,616 | 886 | 1,046 | −0.33 (0.26, .20) |
| Half 1 | 4,970 | 855 | 1,084 | −0.52 (0.38, .17) |

**Conditional logit** (statsmodels, grouped by artist, columns not demeaned):

- **Drops:** 1,277 artists and 5,946 songs whose songs are all in or all out. It keeps 464 artists and 3,640 songs.
- **L2:** −0.095 log-odds per SD (SE 0.066, p .15). It converged (max |score|/nobs below 1e-5).

## Verdict, by the rule written first

**UNSETTLED (p ≥ .00714).**

- **What held:** β is negative, both halves are negative, and the conditional logit is negative and converged.
- **What failed:** p = .11 is far from .00714.
- **Why it is not a kill:** −0.42 is below the −0.2 line.
- **How firm:** the 95% range (−0.94 to +0.10) includes the predicted −0.7. It also includes zero.
  - Power was about 0.49, so a true −0.7 would often look like this.
  - A null would sometimes look like this too.
  - Of tonight's possible outcomes, this one clears nothing and kills nothing.

## Reported, deciding nothing

| Item | β (SE, p) |
|---|---|
| Unfolded range in place of L2 | −0.55 (0.37, .13) |
| Model without `mel_ic_mean` | −0.61 (0.28, .026) |
| L2 on y (in Discogs-VI at all), 2,224 songs | −0.01 (0.42, .97) |
| Intensive margin: z(log(1 + covers)) among the 2,224 versioned songs, with `first_year` added | **+0.063 SD per SD** (0.031, .042); the Listener predicted −0.02 |
| y_foreign with karaoke or tribute sets removed | −0.42 (0.26, .11). No song changed, still 2,130 |

- **Without `mel_ic_mean`:** the estimate grows to −0.61, and part of the range effect is shared with leapiness. In the primary model `mel_ic_mean` itself is −0.76 (SE 0.31, p .015). Both say a plainer, narrower tune goes with more foreign uptake, but neither is significant at tonight's line.
- **Intensive margin:** this goes the other way. Among songs that were versioned, wider range goes with slightly more covers (p .042, not significant at .00714). It decides nothing.

### Something odd: y and y_foreign disagree

The two outcomes differ on only 94 songs (in Discogs-VI, but released only by the artist's own name variants). Even so, β on y is about 0 (SE 0.42), while β on y_foreign is −0.42 (SE 0.26).

I ran a diagnostic after the result was in, and it decides nothing. β on those 94 songs (y_self) is +0.41 (SE 0.35). Two electronic artists drive the y version: Madeon (22 songs) and Armin van Buuren (12) account for 60% of its clustered variance, which fits self-remixes and re-releases.

The primary y_foreign SE is also concentrated: one artist with 4 songs (Portishead) accounts for 30% of its clustered variance. With that much weight on a few artists, the clustered SE of 0.26 may understate the real uncertainty. That makes the unsettled verdict, if anything, softer.

## What it cannot say

- **Transcription:** Hooktheory's octave field is the transcriber's choice. Folding fixes single leaps written an octave off. A whole clip written an octave off does not change the range, so it needs no fix.
- **Sections:** range is taken within each section (clip). A song whose verse and chorus sit in different registers is scored per section, not across the whole song.
- **The outcome:** y_foreign records release by another artist, not lasting love.
- **Seen songs:** the songs were used in run 04, though this measure is new.
- **Sample:** the songs are hits on Hooktheory only. The evidence is association only.
- **The diagnostic:** the influence check was added after the result and decides nothing.
- **McGill hold-out:** untouched. Song 59, songs/p69 and studies/holdout59 were not read.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
