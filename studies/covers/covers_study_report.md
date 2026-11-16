---
title: "What musicians re-record"
subtitle: "Cover counts (SHS100K and Discogs-VI) against the notes of 780 and 2,360 Hooktheory songs"
author: "Study for the Luthier engine · Words and music: Jason Bryant"
date: "15 November 2026"
---

# The answer

Musicians and audiences reward different things in a song's notes. How often a song is covered goes with its YouTube views only weakly (r = 0.15). Beyond views and the other controls, the notes explain 4.0% of how often a song is covered (p = .008), more than they explain of views in the same songs (1.7%).

Three measures predict being covered. None of them predicts views, and syncopation points the opposite way for audiences:

1. **Chords that move.** Songs whose chord progressions repeat less within a section are covered more (β = −0.124, p = .003). Musicians re-record songs that have harmony to work with, not a loop.
2. **Chord surprises in settled moments.** The Cheung term for chords, high when the unexpected chord arrives after a predictable stretch, predicts covers (β = +0.076, p = .03). Across 10,847 songs it never predicted views.
3. **Some syncopation.** More syncopation goes with more covers (β = +0.087, p = .02). Among songs by the same artist it went with fewer views.

All three hold, a little stronger, among the 705 songs performed by their original artist: the notes add 4.7% (p = .004); chord repetition β = −0.126, Cheung term +0.076, syncopation +0.112.


# Replication on Discogs-VI (three times the songs)

The larger SecondHandSongs release (LargeSHS) is not yet downloadable: the GitHub address its paper gives does not exist. A second, independent source is. Discogs-VI (Araz, Serra & Bogdanov, ISMIR 2024; CC BY-SA 4.0, on Zenodo) found 348,796 groups of versions in Discogs' editorial metadata from shared writers and titles. Covers here are the distinct performing artists in a song's group, minus one. The data give each song's earliest release year, so song age can be controlled.

3,080 Hooktheory songs matched, 2,360 with note measures, views and a first year (median 6 covers; 2% have none). With the release year in the controls, covers and views are unrelated (r = 0.00), so they are two separate channels.

| Measure | Covers (SHS100K, 780) | Covers (Discogs-VI, 2,360) | Views (same 2,360) |
|---|---|---|---|
| Chord repetition within a section | −0.124 (p = .003) | −0.071 (p < .001) | −0.003 (p = .88) |
| Chord surprise in settled moments (Cheung) | +0.076 (p = .03) | +0.009 (p = .54) | +0.020 (p = .21) |
| Syncopation | +0.087 (p = .02) | +0.022 (p = .16) | −0.006 (p = .72) |
| Share of beats without melody (rests) | −0.073 (p = .14) | +0.041 (p = .045) | +0.017 (p = .51) |
| Variety of note lengths | +0.008 (p = .89) | +0.039 (p = .048) | −0.009 (p = .72) |
| Notes a beat | −0.028 (p = .63) | −0.036 (p = .08) | +0.087 (p < .001) |
| Chord surprise | −0.065 (p = .16) | −0.030 (p = .06) | −0.043 (p = .02) |
| Notes add, beyond controls | 4.0% (p = .008) | 1.5% (p < 10⁻⁹) | 1.4% (p < 10⁻⁷) |

What replicates:

- **Chords that move:** songs whose chords repeat less within a section are covered more. This is the one finding that holds in both sources, and it is unrelated to views.
- **Density splits the channels:** denser melodies win views but not covers. Musicians lean the other way, toward rests and varied note lengths.
- **Conventional chord choices:** they help a little on every channel.

What does not replicate: the chord Cheung term and syncopation. They pointed the same way in Discogs-VI but were too weak to count, so they are treated as unconfirmed.

The engine's musician profile is therefore revised to:

- harmony that moves within sections;
- room in the melody (rests, varied note lengths);
- conventional chord choices.

# Why it matters

Luthier's own spec names cover counts twice as the missing yardstick for telling songs that last from songs that merely charted. A cover is a musician choosing a song, so it measures songwriting more than fame, marketing or production. With views now in hand too, the engine can be judged on two separate channels:

| Channel | What it rewards in the notes |
|---|---|
| Audiences (views, 10,847 songs) | predictable melody, chords and rhythm; denser lines; pickups; moderate syncopation |
| Musicians (covers; 780 songs on SHS100K, 2,360 on Discogs-VI) | chords that move rather than loop (both sources); room in the melody, with rests and varied note lengths (Discogs-VI); settled-moment surprises and syncopation unconfirmed |

A song that does well on both is accessible enough to be heard and rich enough to be played. The two channels pull apart on syncopation and on repetition. That points to the engine's balance: keep the melody easy to follow, and give the harmony and rhythm the play that interests players.

# Data and method

- **Covers:** SHS100K (github.com/NovaFrost/SHS100K) is the research release of SecondHandSongs: 9,359 works with the versions sampled for each (median 8; Summertime 387). A Hooktheory song matched a work when its title and an artist among the work's performers agreed. That gave 1,039 matches, 780 with note measures and views.
- **Note measures and controls:** the same as the views and rhythm studies (cross-fitted surprise models). The controls are log views, channel subscribers, video age, duration, category, the number of Hooktheory clips, and whether the Hooktheory artist is the work's first performer. Standard errors are clustered by artist.
- **Limits:**
  - SHS100K lists only sampled works that were covered, so this compares songs covered more with songs covered less, not covered with never covered.
  - Song age is not controlled beyond the video's age, and older songs have had longer to gather covers.
  - Seventeen measures were tested; at the .05 level about one would pass by chance, and three did. The block test (p = .008) and the replication on originals carry more weight than any single term.
  - LargeSHS (218,407 works; arXiv 2511.15270) is not yet published at the address its paper gives, so the replication used Discogs-VI instead (section above).

# What this means for the engine

1. **Judge on two channels.** Score a candidate against both profiles: the audience profile (predictability, denser lines; findings 749.18 and 749.20) and the musician profile (harmonic motion within sections, room in the melody, conventional chord choices). Prefer candidates that do well on both, rather than maximising either.
2. **Don't loop the harmony in every section.** Keep chord repetition within a section below the corpus median, at least in the verse or the bridge.
3. **Give the melody room.** Leave rests and vary note lengths, especially in sections the band will carry, while the hook stays dense enough for the audience profile.
4. **Treat settled-moment chord surprises and syncopation as unconfirmed for players.** They passed on SHS100K but not on Discogs-VI.

Scripts: studies/covers in the repository. The SHS100K metadata is not redistributed.
