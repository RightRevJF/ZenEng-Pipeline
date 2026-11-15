---
title: "Surprise against expectation and YouTube views"
subtitle: "10,847 Hooktheory songs"
author: "Study for the ZenEng engine · Words and music: Jason Bryant"
date: "15 November 2026"
---

# The answer

How predictable a song's melody and chords are relates to its YouTube views about ten times more strongly than its shape does. Songs whose melody and chords follow the common patterns of popular music more closely get more views. The effect holds even when songs are compared only with other songs by the same artist.

Across songs, the note measures add 3.3% to the explained variation in log views. That is on top of the 45.6% already explained by channel size, video age, duration, category and how often the song was transcribed (p < 10⁻¹³⁹). Within artists, the strictest test, they add 0.3% (p < .001). For comparison, shape added 0.16% to 0.21% of PDMX views.

# The data and the measures

- **Songs:** 21,998 Hooktheory clips (melody and chords, transcribed by users, via Sheet Sage) from 13,198 YouTube videos. The YouTube Data API returned views for 10,855 of them and channel sizes for 6,130 channels. After dropping videos without a public subscriber count, 10,847 songs remain.
- **Surprise model:** an IDyOM-style model written for this project. It uses variable-order chains of up to three earlier events, trained on the other songs in five folds by video, so a song never predicts itself. For each note and chord it gives:
  - **surprise:** information content in bits, how unexpected the event was;
  - **uncertainty:** entropy, how open the moment was before the event.

  The melody averages 3.1 bits of surprise and 2.7 of uncertainty; the chords average 4.1 and 3.3.
- **The Cheung term:** high when surprises come in predictable moments and plain events in open ones. Cheung et al. found listeners took most pleasure from exactly that combination, in 80,000 Billboard chords.

# Results

| Measure (standardised) | Across songs: β | p | Within artist: β | p |
|---|---|---|---|---|
| Melody surprise | −0.137 | < .001 | −0.054 | .010 |
| Melody uncertainty | −0.063 | < .001 | +0.001 | .94 |
| Melody Cheung term | +0.023 | .005 | +0.025 | .06 |
| Chord surprise | −0.072 | < .001 | −0.059 | .001 |
| Chord uncertainty | +0.016 | .27 | +0.002 | .93 |
| Chord Cheung term | +0.007 | .44 | +0.024 | .08 |
| Melody repetition within the clip | −0.027 | .02 | −0.007 | .67 |
| Chord repetition within the clip | +0.047 | < .001 | +0.005 | .75 |
| Melody surprise squared (inverted U) | +0.015 | .002 | +0.004 | .56 |

Across songs, n = 10,847 (standard errors clustered by artist). Within artist, n = 7,687 songs by 1,469 artists with at least two songs.

Two things hold up in both models:

1. **Less surprising melodies and chords go with more views.** Of all the measures, chord surprise is the most stable within artists.
2. **Surprise placed in predictable moments helps a little.** The Cheung term points the same way in both models, though within artists it falls just short of the usual threshold (p = .06 and .08). The inverted-U term for melody surprise is positive across songs. So the penalty for surprise eases at the low end, but there is no sign of a "too predictable" penalty.

# Cautions

- **Views measure exposure.** The controls (channel size, age, transcription count) and the within-artist comparison remove much of fame's effect, but not all of it.
- **The model learned from the same songs it judges.** Its expectations are those of these popular songs, so a very popular idiom can read as "expected" partly because it is common in the corpus. The folds stop a song predicting itself, but not its imitators.
- **Clips are sections, not whole songs.** The transcriptions are user-made, and the counts can't be redistributed under YouTube's terms. Only scripts and results are kept.

# What this means for the engine

1. **Keep the melody and chords near the common patterns of popular music.** In the judge, reward low average surprise against a large corpus of popular songs. This is the strongest note-level effect found anywhere in our research.
2. **Spend surprise only in predictable moments.** A fresh chord or an unexpected note works after a clear, settled pattern, not inside an open, uncertain passage. This agrees with Cheung et al., though our own evidence for it is modest.
3. **Don't chase novelty for its own sake.** Nothing here rewards a high-surprise melody.
4. **Keep effects in proportion.** Even the strongest measure explains a few percent of views. The notes matter, but fame and exposure matter far more.

# Next

- Score these songs with the UMCS scorer and see whether it ranks the more-watched songs higher.
- Run the model on the engine's own songs to see where they sit against the popular corpus.

Scripts: studies/surprise in the repository.
