---
title: "What musicians re-record"
subtitle: "Cover counts (SecondHandSongs, via SHS100K) against the notes of 780 Hooktheory songs"
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

# Why it matters

Luthier's own spec names cover counts twice as the missing yardstick for telling songs that last from songs that merely charted. A cover is a musician choosing a song, so it measures songwriting more than fame, marketing or production. With views now in hand too, the engine can be judged on two separate channels:

| Channel | What it rewards in the notes |
|---|---|
| Audiences (views, 10,847 songs) | predictable melody, chords and rhythm; denser lines; pickups; moderate syncopation |
| Musicians (covers, 780 songs) | chords that move rather than loop; surprises in settled moments; some syncopation |

A song that does well on both is accessible enough to be heard and rich enough to be played. The two channels pull apart on syncopation and on repetition. That points to the engine's balance: keep the melody easy to follow, and give the harmony and rhythm the play that interests players.

# Data and method

- **Covers:** SHS100K (github.com/NovaFrost/SHS100K) is the research release of SecondHandSongs: 9,359 works with the versions sampled for each (median 8; Summertime 387). A Hooktheory song matched a work when its title and an artist among the work's performers agreed. That gave 1,039 matches, 780 with note measures and views.
- **Note measures and controls:** the same as the views and rhythm studies (cross-fitted surprise models). The controls are log views, channel subscribers, video age, duration, category, the number of Hooktheory clips, and whether the Hooktheory artist is the work's first performer. Standard errors are clustered by artist.
- **Limits:**
  - SHS100K lists only sampled works that were covered, so this compares songs covered more with songs covered less, not covered with never covered.
  - Song age is not controlled beyond the video's age, and older songs have had longer to gather covers.
  - Seventeen measures were tested; at the .05 level about one would pass by chance, and three did. The block test (p = .008) and the replication on originals carry more weight than any single term.
  - The larger LargeSHS (218,407 works, 1.5 million performances; arXiv 2511.15270) was not reachable from here. It would give five to ten times the matches and should be the replication.

# What this means for the engine

1. **Judge on two channels.** Score a candidate against both profiles: the audience profile (predictability; findings 749.18 and 749.20) and the musician profile (harmonic motion, settled-moment surprises, some syncopation). Prefer candidates that do well on both, rather than maximising either.
2. **Don't loop the harmony in every section.** Keep chord repetition within a section below the corpus median, at least in the verse or the bridge.
3. **Place chord surprises after settled stretches.** A borrowed or unexpected chord pays off for players when the bars before it were predictable.
4. **Allow some syncopation in the harmony and accompaniment rhythm,** while the sung line stays near the audience profile.

Scripts: studies/covers in the repository. The SHS100K metadata is not redistributed.
