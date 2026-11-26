# The tune's tie to the chord, set by kept songs: result

25 November 2026. Form and marks in `PREDICTION.md` (committed before any run). The weights: `tables/kept_chord_tie.json` (one pass and the one correction allowed: 2.057 on the beat, 1.691 off). The clean reading: `clean.json`.

**It fails mark 1, and in a way that teaches more than a pass would have. Not built. The whole-engine runs were stopped once the clean reading had decided.**

Each v50 record's fitted spec, only the form changed, a thousand builds:

| | Song 50 | Song 58 | Song 49 | Song 55 | Song 54 | Song 59 |
|---|---|---|---|---|---|---|
| 2. On-beat notes that are chord tones, v50 → the form (kept middle half 0.53 to 0.73) | 0.94 → 0.62 | 0.92 → 0.60 | 0.92 → 0.59 | 0.88 → 0.53 | 0.94 → 0.57 | 0.92 → 0.59 |
| Off the beat (kept 0.56) | 0.52 → 0.54 | 0.51 → 0.53 | 0.52 → 0.54 | 0.48 → 0.49 | 0.50 → 0.52 | 0.51 → 0.53 |
| Long notes on the beat (kept 0.68) | 0.95 → 0.69 | 0.92 → 0.66 | 0.94 → 0.66 | 0.87 → 0.59 | 0.96 → 0.64 | 0.93 → 0.64 |
| **1. Verses over the pitch ceiling, builds in 100** (30 asked in the first three) | **65 → 54** | **56 → 50** | **56 → 51** | 16 → 33 | 15 → 42 | 24 → 38 |
| The middle verse's share on its commonest pitch (kept 0.31) | 0.50 → 0.46 | 0.46 → 0.43 | 0.47 → 0.44 | 0.34 → 0.38 | 0.35 → 0.41 | 0.35 → 0.40 |
| Living builds | 243 → 228 | 366 → 402 | 327 → 357 | 293 → 341 | 279 → 323 | 320 → 369 |

Mark 2 holds: the form does what it was fitted to do, and the tune sits on the chord on the beat about as often as kept melodies, long notes included. Mark 1 fails: the two-chord verses barely improve (54, 50, 51 where 30 was asked).

## What it teaches (749.199)

Look at the three songs that had no trouble. With the tie loosened, their verses pile on one pitch **more**: 16, 15 and 24 builds in 100 over the ceiling become 33, 42 and 38. All six songs end in the same place, 33 to 54, wherever they began.

So I had the direction of the cause the wrong way round. The tie to the chord was not what held the tune on one pitch. It was what **moved** it: under six chords, a tune made to land on each chord in turn has to travel. Take the tie away and every song shows what the two-chord songs showed all along: **left to itself, the draw sits on one pitch near the centre of its register**, about half again as much as kept melodies do (a middle verse 0.38 to 0.46 on its commonest pitch against the kept 0.31). Two chords that share a tone gave it nowhere to be moved to, so there the habit showed. The switches of an hour ago (fresh lines, the pull and the clash rule off, down to 13 to 19) were read on verses over the ceiling in those three songs alone, and I took the fall for the cure. With the tie's weights at kept odds and not at nothing, the fall is small.

This is the same thing the session found from the other side and filed as 749.165 and 749.170: the engine's tunes put too many notes on three pitches, plain and monotone together. It was left as "a change to the draw". It is the draw's own centre.

## Where each thing now stands

- **749.198 stands as a finding:** the engine is on a chord tone on the beat 88 to 95 times in 100, kept songs 64. The form brings it to the kept figure. But it cannot be built alone: the tie is doing the work of moving the tune, and loosening it without mending the draw's centre makes the verses plainer in every song.
- **749.195 (song 50's pool) is not mended.** Its cause is now three deep: the pitch ceiling takes the builds; the two-chord verse lets the habit show; the habit is the draw's.
- **Next, a reading, rule first:** how a kept verse spreads its notes over pitches against how the draw does (the share on the commonest one, two and three pitches; where they sit in the span), and which of the draw's weights sets it: the register's pull to its centre (927), the degree weights (846), the figure memory (923). Then a form for the draw, and only then the tie with it.

## Against what I expected

Mark 1 to hold: wrong, and wrong about why. Mark 2: right. I did not expect loosening the tie to make the six-chord songs worse; it is the most useful thing in the table.
