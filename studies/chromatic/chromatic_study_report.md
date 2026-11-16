---
title: "Chromatic harmony: views, covers and our songs"
subtitle: "A test of whether the engine should live in chromatic harmony (finding 749.23), 15 November 2026"
author: "Words and music: Jason Bryant"
---

# Chromatic harmony: views, covers and our songs

## The question

The maintainer's review of 28 of our songs found that the engine places one borrowed chord or one modulation well, but never *lives* in chromatic harmony: secondary dominants and borrowed chords as part of the ordinary language, modal mixture across a whole section. It suggested pushing in that direction, and noted that it had not analysed every song chord by chord. This study checks both: how chromatic our songs actually are, and whether chromatic harmony goes with what audiences watch or what musicians re-record.

## Why the engine behaves this way

Luthier v7 does it on purpose. The Departure Cost Framework (Window 19.9) charges 1 departure unit for any borrowed chord or secondary dominant and 2 for a secondary dominant resolving, a parallel-minor lift or a deceptive cadence, against a ceiling per song. The engine spends one unit where it counts and returns home. Only the synthetic modal homes (Dorian for mixed songs) and the lament schema (♭VI and ♭VII at no cost) let chromatic chords become ordinary.

## Data and method

- **Corpus:** the Hooktheory clips (CC BY-NC-SA via Sheet Sage), 25,705 clips with a key and chords, averaged per song: 10,749 songs with YouTube views; 2,355 with Discogs-VI cover counts and a first release year; 781 with SHS100K version counts. Clips with a key change were left out.
- **Home key:** each chord's notes against plain major, or natural minor plus the leading tone (so V in minor is at home and a Mixolydian ♭VII counts as borrowed).
- **Measures per song:**
  - chromatic share: the share of chord time outside the home key;
  - the kinds, as shares of chord changes: mixture (from the parallel mode), applied dominants (a major triad or dominant seventh outside the key that moves to the chord a fifth below), and other chromatic chords;
  - lives: the share of a song's sections with two or more chromatic chord changes.
- **Models:** the controls of the earlier studies (subscribers, video age, duration, music category, clips, chord events, major or minor; for covers also log views and song age or first performer). Each measure set was tested alone, then again with the earlier note measures (melody and chord surprise, uncertainty, repetition) held fixed. Standardised betas, errors clustered by artist; views also within artist.

## How chromatic popular songs are

| Measure (per song) | Median | 75th percentile | 90th percentile |
| --- | --- | --- | --- |
| Chromatic share of chord time | 4.4% | 24.7% | 40.1% |
| Mixture, share of chord changes | 0% | 8.0% | 25.0% |
| Applied dominants, share of chord changes | 0% | 0% | 6.2% |
| Sections with two or more chromatic chords | 0% | 100% | 100% |

Half of popular songs have almost no chromatic harmony; a quarter live in it.

## Results

| Outcome | Chromatic share (1 SD) | Mixture | Applied dominants | Sections that live in it |
| --- | --- | --- | --- | --- |
| Views, across songs (10,749) | −0.14 (p < .001) | −0.06 (p < .001) | −0.02 (p .06) | −0.10 (p < .001) |
| Views, same note measures held | −0.07 (p < .001) | −0.03 (p < .001) | +0.00 (p .78) | −0.04 (p < .001) |
| Views, within artist (7,597) | −0.13 (p < .001) | −0.06 (p < .001) | −0.02 (p .07) | −0.08 (p < .001) |
| Covers, Discogs-VI (2,355) | +0.01 (p .61) | −0.02 (p .19) | +0.03 (p .13) | +0.02 (p .29) |
| Covers, SHS100K (781) | +0.08 (p .10) | −0.02 (p .65) | +0.08 (p .06) | +0.07 (p .06); +0.10 (p .01) with note measures |

Standardised betas over the controls. The chromatic-share model also has a square term: for views it is positive (+0.07), so the loss is steepest from none to some and then levels off.

1. **Audiences watch chromatic songs less.** The effect is small (0.1% to 1% of the variance) but holds within one artist's songs and with the note measures held fixed. Mixture carries most of it.
2. **Musicians do not re-record chromatic songs more.** There is no effect in the larger source (Discogs-VI). The smaller source (SHS100K) leans positive for sections that live in chromatic harmony and for applied dominants, but the larger one does not confirm it. The covers finding of 749.22 is about chords that *change* within a section, not chords outside the key.
3. **Applied dominants are the safest kind.** With the note measures held they carry no views penalty, and they lean positive for covers in both sources (not significant in either).

## Our songs

Chord symbols from the scripts of 31 songs (p21 to p63), read against each song's key. This is an inventory of the chords written, not a count of bars, so it can miss a chord written another way.

- 15 songs have no chromatic chord, 9 have one, 4 have two, and 3 have three or four.
- The median song has 2.5% of its chord mentions outside the key, a little under the popular median of 4.4%.
- The commonest chromatic chord is ♭VII (9 songs). Applied-dominant shapes appear in 6 songs. Only The World Is Asking (song 49: V/ii, V/vi, V/V) and A Wire Pulled Tight (song 51) use several.

The maintainer's reading is right: the engine uses chromatic chords as single colours, mostly ♭VII.

## What it means for the engine (749.23)

- **Keep the departure budget as the default.** The audience data support rationing chromatic chords in a song meant to reach many listeners, and the musician data give no reason to spend more.
- **Add a chromatic home as a style option, not a default.** For songs whose style lives there (gospel, jazz, prog, art song, some worship), chosen at intake. A section declares its chromatic vocabulary: each chord costs 1 unit when it first enters, then nothing for the rest of that section, as the synthetic modal homes already work.
- **Within it, prefer applied dominants that resolve,** and use mixture outside the lament and groove homes sparingly.
- **Keep the sung line plain over it:** melody surprise at or below the corpus median (749.18).

Evidence grade: **B** for the views penalty (large sample, holds within artist); **C** for applied dominants and covers (one source leaning, not replicated).

## Cautions

Hooktheory is mostly popular song, so the result says nothing about hymns or art song, where chromatic harmony is ordinary. Users transcribe sections, not whole songs. Genre is only partly controlled (within artist helps). Views measure exposure as much as music.

## Files

studies/chromatic: chromatic_features.py, study_chromatic.py, chromatic_our_songs.py, chromatic_results.json, chromatic_our_songs.json.
