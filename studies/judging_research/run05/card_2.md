# Card 2: Interiano et al. 2018 (chart success from audio descriptors, with and without a "superstar" flag)

Role tonight: counter-evidence for the Skeptic.

## 1. Citation and copy read
Interiano, M., Kazemi, K., Wang, L., Yang, J., Yu, Z., & Komarova, N. L. (2018). Musical trends and predictability of success in contemporary songs in and out of the top charts. *Royal Society Open Science* 5: 171274. doi:10.1098/rsos.171274.

Copy read: the full-text PDF in the University of California eScholarship repository (escholarship.org/uc/item/96b901t6, PDF at escholarship.org/content/qt96b901t6/qt96b901t6.pdf), plus its landing page. It carries the RSOS citation and 47 references, so I take it to be the published article.

Read: abstract, introduction, data, methods, results, discussion, all six figure captions, Table 1, the data-accessibility statement and the whole reference list.

Not read, or not fully:
- PMC (pmc.ncbi.nlm.nih.gov/articles/PMC5990848), Europe PMC and the RSOS publisher page were all blocked by unanswered permission prompts. The RSOS page is where any electronic supplementary material would be listed.
- The PDF itself mentions no supplement and no code. It says only that the data are public (Official Charts, AcousticBrainz). I could not confirm on the publisher page that no supplement exists.
- The figures were read as captions and text only. The accuracy-by-training-year curves (Fig. 5b, Fig. 6) are not given as numbers anywhere in the text, so I have no values for them beyond what the text says.
- The PDF was read through a fetch tool that answers questions about the page. All numbers below were asked for specifically and come from the text or Table 1.

## 2. Claim and data
**Claim.** Over 30 years of UK releases, high-level audio descriptors show long trends (less happy, less bright, slightly more sad, fewer male voices). Hits differ from the average song. Audio descriptors alone predict chart entry well above chance, but adding a "superstar" flag for the artist raises accuracy a good deal. Prediction draws mainly on the year just before, which the authors read as a sign that musical fashion is short-lived.

**Corpus.**
- UK Official Charts Top 100, weeks of 6 Jan 1985 to 19 Jul 2015: 148,190 chart entries, 30,081 unique songs.
- Matched to MusicBrainz (copy of 19 Apr 2016) and AcousticBrainz (dumps of 22 Apr 2016, 1,641,765 unique recordings).
- 14,536 of the 30,081 charting songs matched (under half).
- Non-charting songs: every available AcousticBrainz song from a UK-distributed release, first occurrence only. About 16,245 a year on average (2,805 in 1985, 27,095 in 2008).
- Abstract: "more than 500 000 songs". No exact total is given.
- Bias check on matching: one year (2005), 100 vs 100 songs, three genres, chi-square not significant. That is a small pilot.

**Success.** Appearing in the UK Top 100 at all, in any week. Peak position and weeks on chart are not used.

**Features.** 18 AcousticBrainz high-level descriptors. These are outputs of pretrained Essentia classifiers run on audio, not notes.
- 12 binary, each with a posterior probability: timbre dark/bright, tonal/atonal, danceable, voice/instrumental, vocal gender, and mood acoustic, electronic, relaxed, sad, party, happy, aggressive.
- 6 categorical: MIREX mood clusters, four genre taxonomies (electronic, Tzanetakis, Dortmund, RosaMerica) and ISMIR04 rhythm (ballroom dance classes).
- The authors note that the classifiers' accuracy on large collections is unknown.

**Superstar variable.** An artist is a superstar if at least one of their songs charted in the past 5 years. A 1-year version was also tried and was less predictive in pilot work. Shares by year: 0.51 to 0.68 of charting songs were by superstars, against 0.0009 to 0.02 of non-charting songs.

**Random forest set-up.**
- R randomForest. Neural nets (one and two layers) did about the same and are not reported.
- Balanced classes: all charting songs for a year, plus an equal random sample of non-charting songs (e.g. 585 of 16,058 in 2013).
- Test set: 2014 songs, 526 charting plus 526 drawn from 13,592 non-charting. Drawn once and held fixed. Chance accuracy is therefore 0.50.
- Results are averages of 10 runs.
- Scheme 1: one forest per training year (1985 to 2013), each tested on 2014. Inputs were either all categorical or the binary features as probabilities ("continuous").
- Scheme 2: accuracy-weighted ensemble of scheme 1 forests; a song is a hit if the combined probability is over 0.5.
- Scheme 3: one forest on pooled years with year as a continuous input.
- Not reported: tree count, mtry, out-of-bag error, cross-validation, AUC, sensitivity, specificity, confidence intervals, variable importance.

**How the two models were compared.** The same schemes were run twice on the same 2014 test set, once with the 18 audio features only and once with the superstar flag added. The only metric is accuracy. There is **no superstar-only model**.

**Table 1, accuracy on 2014 songs (features only, then with superstar):**

| Scheme | Features only | + superstar |
|---|---|---|
| 1, categorical, trained 2013 | 0.71 | 0.82 |
| 1, continuous, trained 2013 | 0.74 | 0.85 |
| 2, 2009 to 2013 | 0.73 | 0.86 |
| 2, 2004 to 2013 | 0.73 | 0.85 |
| 2, all years | 0.69 | 0.86 |
| 3, 2009 to 2013 | 0.75 | 0.85 |
| 3, 2004 to 2013 | 0.70 | 0.86 |
| 3, all years | 0.70 | 0.85 |

The paper's "15%" gain is relative (0.85 vs 0.74), i.e. 11 percentage points. The discussion says features alone never beat 0.74, although Table 1 shows 0.75 once.

**Time scale of fashion.** Without superstar, accuracy falls as the training year moves back from 2014. With superstar it falls much more slowly. Pooling more, older years did not help. The authors conclude that only the previous year's data matter much and that "musical fashion is relatively short-lived". No number of years is given. Test years 2004 and 1994 gave lower accuracy and a weaker trend (graph only). All of this rests on one test year, differences of about 0.01 to 0.05, and no significance test.

**Descriptive side results.** Hits are happier, brighter, less sad, more party-like, less relaxed and more danceable than average, and lately more female-voiced and less aggressive. Several of these run against the overall trend. Dance and pop chart most, classical and jazz least, and rock declines from the early 2000s.

## 3. Is the measure from the notes?
No. None of the 18 features is symbolic. They are classifier guesses from recorded audio about mood, timbre, voice, production style and genre. Pitch sequence, intervals, chord progression and form are never measured.

Closest to the notes:
- **Tonal vs atonal**: a crude pitch-organisation flag, from audio.
- **ISMIR04 rhythm**: a ballroom dance-style class (tempo and groove), not a rhythm pattern.
- **Danceability**: driven by beat regularity and tempo, so partly rhythmic.
- **Mood happy/sad**: in audio models these lean partly on mode and tempo, but also on timbre and production.

Everything else (bright/dark timbre, vocal gender, electronic/acoustic, the four genre labels) is about sound and performance, which Jason's stance sets aside.

## 4. Effect size and how it was checked
**Numbers.** On a balanced 2014 test set (chance 0.50):
- audio features alone: 0.69 to 0.75;
- features plus superstar: 0.82 to 0.86;
- gain from superstar: about 0.11 to 0.17 in accuracy.

**What the superstar flag alone would do (my calculation, not in the paper).** With 51 to 68% of hits by superstars and 0.1 to 2% of non-hits, the rule "hit if superstar" alone would score about (0.51 + 0.98)/2 = 0.75 to (0.68 + 0.999)/2 = 0.84 on a balanced set. So the flag by itself probably matches or beats the whole audio model. On top of it, the audio features may add only a few points. The paper never runs this comparison, which is the one that matters most for the Skeptic.

**Checks done.**
- A true forward hold-out: train on earlier years, test on 2014, with 1994 and 2004 as extra test years (graphs only).
- Balanced classes; 10 repeat runs.
- Genre enters only as predictors; there is no genre-stratified or within-genre prediction.
- Year enters by training per year, or as a covariate in scheme 3.

**Checks not done.** No grouping by artist, so the same artists can sit in training and test. No uncertainty on accuracies, no AUC, no importance scores, no superstar-only or artist-held-out model.

**What makes the musical contribution look LARGER than it is:**
- The non-chart pool is every UK release in AcousticBrainz, including classical, jazz and obscure material. Telling "pop production" from "not pop" is easy, so much of the 0.74 is genre and production style, not song quality.
- Audio features can encode artist identity (voice, sound). Without artist-grouped splits, the "musical" model may partly be recognising known artists.
- Volunteer-submitted AcousticBrainz data and under-half matching of hits may skew the samples.

**What makes it look SMALLER:**
- 18 coarse, noisy classifier outputs throw away melody, harmony, lyrics and form. Any real content signal would be badly under-measured.
- Accuracy on a balanced set is a blunt metric.
- With the superstar flag present, the forest can lean on it and hide subtler musical signal (the authors say so).

## 5. What it says about lasting love and covers
**How it cuts against judging from the notes alone.**
- A single bit about the artist's recent chart record raises accuracy by about 11 points, and probably does as well alone as all the audio features combined. Who made the song carries a large share of what predicts its success.
- The audio features that do predict are largely genre, mood and production. They behave like fashion: their value decays within a few years. That fits a view that success follows the moment and the market, not a fixed quality in the material.
- The authors cite Salganik et al. (2006): quality limits the extremes, but social influence makes outcomes largely unpredictable. A notes-only model has a ceiling.

**Where it fails to apply.**
- Chart entry is a week-one, market outcome. It is not lasting love and not covers. A cover is a decision by another artist, often decades later, and the paper's own fashion result suggests the short-term chart signal is the wrong one for long-run survival.
- Audio descriptors are not notes. The paper says nothing directly about melody, harmony or form. It neither supports nor refutes a symbolic measure.
- The comparison is between artists. It cannot show whether, holding the artist fixed, better-written songs do better. That is exactly the project's main design.

**What it implies for the project's numbers.**
- In this project the artist accounts for about 14% of variation in covers. The paper's results lead us to expect this: artist standing is a big, easy predictor, and the artist fixed effect is right to remove it.
- Within artist, note measures explain about 0.04 SD of covers per SD, i.e. about 0.16% of variance. Against the artist's 14%, that is about 90 times smaller. The paper's pattern (audio adds only a little once the artist is known) is consistent with that small size. The Skeptic can argue that such an effect is too small to call "judging from the notes".
- The paper does not show the within-artist effect is zero, because it never tests within artist. A small, real within-artist effect is compatible with it.
- Warning for our design: if a note measure works mainly by tracking genre or era (as the paper's audio features do), it will look larger between artists than within. A within-artist test with year controls guards against that.

## 6. Methods or measures it suggests for tonight's experiments
1. **A superstar analogue from data on hand.**
   - Between artists: log number of the artist's songs on Hooktheory, and log total clips. These are absorbed by the artist fixed effect, so use them only in models without it, to show how much "fame" alone predicts.
   - A lagged, within-artist version: for matched songs with a first release year, flag whether the artist already had a different song in Discogs-VI from the 5 years before this one. Exclude the focal song. Also try song-level fame: clips or sections per song, and whether the song is the artist's most-transcribed.
   - Kill: if adding notes to a fame-only model raises held-out AUC by less than 0.01, with a bootstrap-over-artists interval covering zero, the notes add nothing beyond fame.
2. **Artist versus notes, done as prediction.** Fit (a) artist effect only, (b) notes only, (c) both. Report AUC and log-loss, not accuracy, because our base rate is not 50/50.
   - Split two ways: held-out songs from seen artists (artist effect usable) and held-out artists (grouped CV; notes must stand alone).
   - Report the gain in AUC from notes over the artist effect, and the variance share from a random-intercept model (artist ICC vs the variance the note terms explain).
   - Run a placebo that shuffles note features within artist 500 times.
   - Kill: the real gain falls inside the shuffled distribution.
3. **The genre and era trap.** Add first-release-year bins, genre or source type (pop, rock, anime, game) and a Hooktheory-popularity term. Repeat the main within-artist estimate within the largest genres.
   - Kill: the note effect drops by more than half or loses significance once year and genre are held.
4. **Typicality and the fashion time scale, in notes.** For each song, build chord-bigram and melodic-interval distributions. Measure distance from:
   - songs first released in the same year plus or minus 2;
   - the same artist's other songs (leave one out);
   - songs from 5 to 10 years earlier.

   Test linear and inverted-U forms (optimal differentiation), within artist. Then vary the reference window (1, 3, 5, 10, 20 years) and see which window best predicts covers. The paper predicts that short windows matter for chart entry; for lasting covers one would expect long windows, or "timeless" songs near the long-run centre.
   - Kill: no window beats a placebo with shuffled release years, or typicality adds nothing once year is held.
5. **Time at risk.** Older songs have had longer to be covered. Hold first release year fixed in every model and report effects by decade. The paper's decay of signal across years warns that a pooled effect can hide era-specific ones.

## 7. Leads
1. Salganik, M. J., Dodds, P. S., & Watts, D. J. (2006). Experimental study of inequality and unpredictability in an artificial cultural market. *Science* 311: 854-856. https://doi.org/10.1126/science.1121066 . The cleanest causal evidence that social influence, not content alone, drives success; cited by this paper.
2. Askin, N., & Mauskapf, M. (2017). What makes popular culture popular? Product features and optimal differentiation in music. *American Sociological Review* 82(5): 910-944. https://doi.org/10.1177/0003122417728662 . Typicality relative to contemporaries, with artist and label controls; the model for test 4.
3. Pachet, F., & Roy, P. (2008). Hit song science is not yet a science. Proc. ISMIR 2008. Direct counter-evidence: a large feature set failed to predict hits beyond chance.
4. Berger, J., & Packard, G. (2018). Are atypical things more popular? *Psychological Science* 29(7): 1178-1184. https://doi.org/10.1177/0956797618759465 . Lyric atypicality relative to genre predicts chart success; content-level, not audio.
5. Ordanini, A., & Nunes, J. C. (2016). From fewer blockbusters by more superstars to more blockbusters by fewer superstars. *International Journal of Research in Marketing* 33: 297-313. Measures how concentrated success is among artists over time, which bears on how much the artist effect should dominate.

DOIs for leads 1, 2 and 4 are from memory and were not fetched tonight.
