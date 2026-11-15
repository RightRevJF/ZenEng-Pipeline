---
title: "The rhythm layer"
subtitle: "Rhythm surprise, syncopation, rests and phrases against YouTube views and loved moments"
author: "Study for the ZenEng engine · Words and music: Jason Bryant"
date: "15 November 2026"
---

# The answer

Rhythm matters as much as pitch, and it follows the same rule: familiar rhythms overall, a fresh one at the moment that counts.

- **Views:** adding rhythm to the model brings the note measures to 4.8% of the explained variation in log views across 10,828 songs, beyond the controls. Rhythm's own share is 1.5%. Among songs by the same artist, the strictest test, the rhythm block adds 0.38% (p < .001), more than melody and chords together added on their own (0.30%).
- **Familiar rhythms:** less surprising rhythms go with more views, both across songs and within artists.
- **Note density and pickups:** busier melodies (more notes a beat) do better, and so do phrases that start before the downbeat, with a pickup.
- **Syncopation:** a moderate amount is best across songs. Within artists, more syncopation goes with fewer views.
- **Loved moments:** at the moments listeners timestamp, the rhythm is at its most surprising (+0.21 SD), right where the voice re-enters after a breath.

# The rhythm layer

Each melody note becomes a rhythm token: its position in the bar on a sixteenth grid, its length class, and whether a rest of half a beat or more came before it. The surprise model (orders 0 to 3, trained by folds so a song never predicts itself) gives each note's rhythm surprise and uncertainty. Across 22,800 clips the means are 2.7 and 2.2 bits.

Descriptors, with their Hooktheory medians:

- **Syncopation per note** (a note held across a stronger beat): median 0.29.
- **Share of beats with no melody:** median 0.12.
- **Rests of a beat or more:** per bar.
- **Phrase length:** spans between rests of a beat or more, median 15.5 beats.
- **Phrases starting on the downbeat:** median 0.5.
- **Notes a beat:** median 1.08.
- **Variety of note lengths:** median 1.52 bits.

# Against views

All standardised, with the pitch and chord measures and the controls in the same model:

| Measure | Across songs: β | p | Within artist: β | p |
|---|---|---|---|---|
| Rhythm surprise | −0.085 | .002 | −0.055 | .03 |
| Rhythm uncertainty | +0.011 | .49 | +0.066 | .003 |
| Syncopation per note | −0.021 (squared −0.013, p = .02) | .27 | −0.049 | .009 |
| Share of beats with no melody | +0.049 | < .001 | +0.031 | .14 |
| Phrase length | −0.049 | < .001 | +0.048 | .02 |
| Phrases starting on the downbeat | −0.041 | < .001 | −0.026 | .06 |
| Notes a beat | +0.053 | .003 | +0.049 | .03 |
| Variety of note lengths | +0.071 | < .001 | +0.008 | .73 |
| Melody surprise | −0.107 | < .001 | −0.048 | .02 |
| Chord surprise | −0.065 | < .001 | −0.057 | .002 |

Across songs n = 10,828; within artist n = 7,671 songs by 1,466 artists.

Holding in both models: familiar rhythms, denser melodies, pickups into phrases, and not too much syncopation. Phrase length flips sign between the two models, so it supports no conclusion. Rests help across songs but not clearly within artists.

# At the moments people love

Against the rest of the same clip, rhythm surprise rises two beats before the timestamp (+0.16, 95% CI 0.07 to 0.24) and peaks at it (+0.21, 0.13 to 0.30), falling away after. This fits the earlier finding of a breath and then the voice's re-entry. Part of it is built in, though: a note after a rest is itself a less common rhythm token.

# Our songs

| Song | Rhythm surprise | Syncopation | Rests | Phrase (beats) | Notes a beat |
|---|---|---|---|---|---|
| Nothing Important | 85th percentile | 39th | 92nd | 4.9 (8th) | 48th |
| Blue Movie | 64th | 35th | 84th | 6.1 (14th) | 44th |
| Keeping Time | 57th | 27th | 88th | 6.0 (14th) | 41st |
| Before It's Done | 51st | 28th | 80th | 6.9 (19th) | 68th |
| The Room Next Door (song 52) | 76th | 28th | 50th | no breaks of a beat | 84th |
| Sung to Sleep, verse (song 53) | 26th | 0 | 26th | no breaks of a beat | 12th |
| Sung to Sleep, refrain | 44th | 0 | 0 | no breaks of a beat | 15th |

- **The engine's pop songs:** their rhythms are more surprising than most popular songs, and their phrases are short and broken by many rests. Both run against the more-viewed direction. Their syncopation is moderate.
- **Song 52:** busy (84th percentile density), with fairly surprising rhythms.
- **Sung to Sleep:** plain, sparse and unsyncopated, as a hymn tune is, with no breath of a beat or more anywhere. That last point matters for the "breath, then re-entry" rule.

# What this means for the engine

1. **Keep rhythms familiar.** Score rhythm surprise against the corpus and aim at or below the median. Luthier's pop songs run above it.
2. **Use pickups.** Start most phrases before the downbeat.
3. **Keep syncopation moderate.** Some is good; a lot works against a song.
4. **Don't starve the melody.** Very sparse lines do worse; aim near or above about one note a beat in pop styles.
5. **Spend rhythmic surprise at the best moments,** with the breath before them (749.19). In hymns that means a real breath at chosen line ends, which Sung to Sleep never has.

# Cautions

As before: views measure exposure as well as music, and the clips are user transcriptions of sections. Note offsets in Hooktheory may be drawn legato, which would make rests shorter than sung. Song 52's 6/8 was read on a grid of three quarters. The effects are small.

Scripts: studies/rhythm in the repository.
