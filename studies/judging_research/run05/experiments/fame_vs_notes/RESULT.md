# Fame against the notes, across artists: result

Run 05, 25 November 2026. The rule is `PREDICTION.md` in this folder (frozen in commit 1f6c36d before any outcome was joined). The script is `test.py` and the numbers are in `result.json`. The script followed the rule's order: it built the rows and the two predictor blocks from the notes, reproduced the rule's fold sizes, ran the whole pipeline on a random fake outcome, and only then read the outcome. No rule was changed afterwards. It runs in under a minute on one core.

**Verdict: KILL.** Across artists, the notes predicted who gets taken up by another artist far better than the two fame proxies did, and adding the notes to the fame proxies raised the prediction a great deal. Both kill clauses fire, by wide margins. But read "What it cannot say" before reading anything into this. The fame proxies turned out to be poor proxies, and the notes' advantage comes almost entirely from artist-level style, not from differences between songs.

## What was predicted

This test compares songs **across** artists on purpose. Card 2 (Interiano et al. 2018) found that a "superstar" flag predicted chart success much better than audio features did. The Skeptic predicted the same here. Crude fame signals would predict y_foreign (did a performer with no shared name release the song) better than the 17 note measures, and the notes would add almost nothing once fame was known.

- **Fame block (a):** ln(the artist's number of songs among the 13,198 Hooktheory songs) and ln(clips per song). Both are traces of how much Hooktheory users care about an artist or song.
- **Notes block (b):** the 17 data-pack measures.
- **Both (c):** (a) and (b) together.
- **The models:** each block was fitted as a logistic regression with 5-fold cross-validation, keeping each artist's songs in one fold. The script then measured how well each block ranks taken-up songs above the others (AUC: 0.5 is a coin toss, 1.0 is perfect).
- **The Skeptic's numbers:** AUC(fame) about 0.62 or more, AUC(notes) 0.56 or less, so D = AUC(fame) − AUC(notes) about +0.06. The gain from adding notes, Δ = AUC(both) − AUC(fame), would be below 0.01.

**The rule.** The interval for each number came from resampling artists 2,000 times. Its level was 99.3%, the run's .05/7 threshold.
- **Pass:** the lower end of D's interval is above 0 and Δ < 0.01.
- **Kill:** Δ ≥ 0.01 with Δ's interval above 0, or D ≤ 0.
- **Unsettled:** anything else.

## Checks before the outcome (notes only)

- **Rows:** 9,588 songs by 1,741 artists, out of 13,198 songs. All of these reproduced exactly: the 14 songs with no rhythm row, the fold sizes (2,069 / 2,072 / 1,739 / 1,772 / 1,936) and the halves (886 / 855 artists).
- **Overlap:** neither fame proxy is a note measure under another name. The largest |Spearman| with any of the 17 measures was +0.12 (ln artist songs against `mel_ic_mean`). Against `ch_rep` it was −0.06. The two proxies correlate at +0.15 with each other.
- **Fake outcome:** on a pure-noise outcome the code ran cleanly. AUCs were all about 0.50, and the bootstrap matched sklearn's AUC on explicit resamples to 1e-16.
  - **A weakness this exposed:** with no signal at all, the rule said KILL, because D came out slightly below 0 by chance (−0.015). The "D ≤ 0" clause has no interval, so it fires about half the time in a world with nothing to find. That does not matter tonight, because D is far below zero with its whole interval below zero. Future rules should still put an interval on that clause.

## The outcome

- **Songs:** 9,586 songs by 1,741 artists. 2 songs were dropped because the original artist had no release of its own in the version group.
- **Taken up:** 2,130 songs (22.2%) were taken up by another artist.

## How firm (printed before the estimates)

- **Bootstrap SEs:** 0.033 for D and 0.025 for Δ. These are larger than the rule's synthetic guesses (0.02 and 0.005), because artists differ more than the simulation assumed.
- **The rule's power:** a fame-only world passed 6 of 6, and a world where the notes add 0.045 AUC was killed 6 of 6. The result tonight is far outside the boundary region, so power is not a concern for the verdict.

## Results

| | AUC | 95% artist-bootstrap range | Log-loss (base rate alone: 0.530) |
|---|---|---|---|
| (a) Fame | **0.481** | 0.414 to 0.541 | 0.538 |
| (b) Notes | **0.693** | 0.668 to 0.716 | 0.490 |
| (c) Both | **0.678** | 0.648 to 0.705 | 0.496 |

- **D = AUC(fame) − AUC(notes) = −0.211**, 99.3% interval −0.311 to −0.136. The Skeptic predicted about +0.06.
- **Δ = AUC(both) − AUC(fame) = +0.196**, 99.3% interval +0.132 to +0.269. The Skeptic predicted below 0.01.
- **By artist half:**

| | Half 0 (4,616 songs, 886 artists) | Half 1 (4,970 songs, 855 artists) |
|---|---|---|
| AUC fame / notes / both | 0.459 / 0.703 / 0.683 | 0.504 / 0.683 / 0.674 |
| D | −0.245 | −0.179 |
| Δ | +0.225 | +0.170 |

- **No convergence warnings** in any fit.

## Verdict, by the rule written first

**KILL.** Both kill clauses hold:
- Δ = +0.196 is at least 0.01, and its interval lies above 0 (lower end +0.132).
- D = −0.211 is at most 0, and its interval also lies entirely below 0.

The pass clause fails on both counts. Both halves agree. The Skeptic's claim, that across artists this outcome follows fame and not the notes, is killed **as measured with these fame proxies**.

## Reported, deciding nothing

**Placebo: the notes shuffled among each artist's own songs** (200 shuffles). The shuffle keeps each artist's typical notes but breaks the link to the particular song.
- Δ stays at +0.190 on average (95th percentile +0.197), against the real +0.196.
- So about **97% of the notes' gain is artist-level**: style, genre, era and transcription habits.
- Only about 0.006 AUC is tied to the individual song, and 6% of shuffles reached the real value.
- In plain words: the notes tell you what kind of artist this is, and that is what predicts uptake across artists.

**The same rule on y** (in Discogs-VI at all, 9,588 songs, 2,226 matched) gives the same picture:
- AUC fame 0.485, notes 0.689, both 0.675;
- D −0.205 (interval −0.301 to −0.133);
- Δ +0.190 (interval +0.126 to +0.261);
- by the rule, kill.

**Within artist, the Skeptic's part 2.** This is a linear probability model with an artist effect, the 17 z-scored measures and run 04's controls. The 14 songs' missing rhythm values were set to 0.
- **Partial R²:** clips-per-song dummies 0.0017; the 17 measures 0.0032.
- **Ratio:** fame to notes is **0.53**. The Skeptic predicted at least 5.
- **Both are tiny.** The whole within-artist model explains 2.8% of the within-artist variation.

**Interaction, the Skeptic's part 3.** This is run 04's model, clustered by artist.
- **`ch_rep` × z(ln artist songs):** +0.09 pp (SE 0.34, p .80). The Skeptic predicted it would be above 0. It is indistinguishable from zero.
- **`ch_rep` in the same model:** +0.98 pp (SE 0.50, p .048).
- **Without the interaction:** `ch_rep` is +1.00 (SE 0.49, p .044), which reproduces run 04's figure for this outcome.
- **Among the least prolific artists** (3 or fewer songs, the artist-level median; 2,457 songs, 1,063 artists): `ch_rep` is +0.79 (SE 1.13, p .48). This used run 04's model without the interaction term, which is how I read "the same model" in a subset. It has the same sign and is too noisy to say more.
- **So:** nothing suggests the loop lead is carried by prolific artists.

### Post-hoc diagnostics (added after the outcome was seen; decide nothing)

AUC(fame) came out **below 0.5**, which needed an explanation.

**The number of songs is not a fame signal here.** The 15 most-transcribed "artists" (50 or more songs; 1,470 songs) are mostly video-game studios and composers, library music and fan projects. Examples are Nintendo, Kevin MacLeod, ZUN, Sega and Toby Fox. 10 of the 15 have no song taken up by another artist, while the Beatles and Taylor Swift sit at the other extreme. The share taken up by number of artist songs:

| Songs by artist | 2 | 3 | 4-5 | 6-9 | 10-19 | 20-49 | 50+ |
|---|---|---|---|---|---|---|---|
| Share taken up | 20% | 23% | 23% | 23% | 24% | 28% | 15% |

The relation rises and then falls, and a straight-line model cannot follow that.

**The cross-validation folds make it worse.** The few huge "artists" are unevenly spread across folds. The fame block's AUC in the five test folds was 0.57, 0.55, 0.55, 0.51 and **0.36**. Fitted on the other folds, the slope points the wrong way in fold 4. The univariate AUCs of the raw proxies are 0.49 (artist songs) and 0.52 (clips per song).

**Where the notes' signal comes from.** The note measures that predict best across artists are rests and phrasing:
- `rest_share` (AUC 0.65 raw, 0.73 on artist means, 0.51 within artist);
- `phrase_mean` (0.34 raw, 0.24 on artist means, 0.51 within artist);
- `phrase_on_downbeat`;
- `mel_ic_mean`.

Sung melodies breathe, with rests and short phrases. Game and instrumental themes often do not. So the cross-artist notes signal looks largely like "a vocal pop song rather than a game or instrumental theme". Within an artist, every single measure sits between 0.48 and 0.52.

## What it cannot say

- **It does not show that good songs get taken up.** The notes' advantage is about 97% artist-level (placebo). Across artists the notes mainly record style and source: vocal pop against game, library and instrumental music. The rule's own warning applies in full: a kill can mean "the notes carry style, and style predicts uptake".
- **It does not show that fame does not matter.** The fame proxies failed as proxies. Hooktheory song counts mix superstars with game studios and library composers, so the test compared the notes against a broken fame measure. Card 2's superstar effect is untouched. A real test needs chart or streaming data (`DATA.md` lists it as missing).
- **Not a within-artist test.** It does not touch tonight's other six tests or run 04's findings. Within artist, both fame-like and note signals are tiny (partial R² 0.002 and 0.003).
- **The rule's D ≤ 0 clause has no interval** and fires by chance on pure noise. It did not decide anything tonight, because the interval clause fires too, but it should be fixed in future rules.
- **The songs were seen before.** They were used in run 04. y_foreign is not lasting love, and the songs are hits only. No cause is shown. The McGill hold-out is untouched: song 59, songs/p69 and studies/holdout59 were not read.

## Credits

Notes and chords: Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022), CC BY-NC-SA 3.0. Version groups: Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024), CC BY-SA 4.0.
