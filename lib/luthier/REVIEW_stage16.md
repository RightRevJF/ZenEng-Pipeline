# Review 16: Luthier v29 (fixes 916–917)

Branch `luthier-v8-stage1` at efc5f89, main merged in at c365a48.

## Byte for byte

The song reruns reproduce every committed record. `soundness.py` on the v29 records writes `soundness.json` byte for byte as committed:
- no lean past the kept 10th or 90th;
- two leans past the middle half, the two the rule allows: rhythm scaling, low (0.539 / 0.577 / 0.524), and pitch scaling, high (1.042 / 1.091 / 1.180).

Sound by the rule as adopted.

## 916

As written. Every turn of 877 stays; a song past the kept 75th of lengths gets two-bar turns; the bars in and out are read again once the turns are in. Song 58 now has a two-bar turn after chorus 1 and runs 331 seconds. Its key is C, no capo, and the chorus lifts 9 semitones over the verse. The document scripts had the turn and the last chorus's bar count written in; both are now read from the record.

## Does a pass by three thousandths hold?

No. The pick is the first build in order past the gates, so it is in effect one draw from the gated pool. `studies/soundness/margin.py` rebuilds each song's 1,000 builds and gates, reproduces the three picks (rhythm scaling 0.539, 0.577, 0.524), and reads every pool build as `soundness.py` does.

| | 55 | 54 | 58 |
|---|---|---|---|
| pool size | 84 | 83 | 93 |
| pool's rhythm scaling, median | 0.560 | 0.570 | 0.539 |
| share of the pool under the kept 10th (0.574) | 0.80 | 0.59 | 0.94 |

A fresh draw of the three songs leans past the kept 10th 44 times in 100. Three kept songs drawn at random lean that way on a given check about once in 1,000. The bound is not sharp either: by bootstrap over the 160 kept songs, the kept 10th runs 0.560 to 0.588 (5th to 95th). The pass came from which builds happened to come first. Pitch scaling is safe: a fresh draw leans past the 90th 4 times in 1,000.

## The cure for rhythm scaling: four-bar turns

Kept songs' turns are four bars long 38 times in 100; 916 makes every turn two bars once a song runs long. With every turn four bars (a trial copy of `song_from_lyric.py`; `margin_turns_of_four.json`):

| | 55 | 54 | 58 |
|---|---|---|---|
| pool's rhythm scaling, median | 0.607 | 0.593 | 0.581 |
| share under the kept 10th | 0.02 | 0.19 | 0.35 |

The chance of a lean falls from 0.44 to 0.001.

## What the pools show beyond that

`studies/soundness/neighbour.py` reads every build on the 21 kept-read checks, with four-bar turns:
- **The builds sit near the middle before any gate.** A pick drawn at random from every build that lived has a median of 20 song-checks outside the middle half across the three songs. From the engine's pool it is 17. Three kept songs have about 30.
- **Choosing toward a kept song does not widen it.** Taking the pool build nearest a randomly drawn kept song gives a median of 16. The narrowness is in the builds, not the choice (749.94).
- **A random pick from the engine's pool fails the rule 13 times in 100** (three kept songs: 6.8). It fails by piling up leans past the middle half: rhythm scaling 0.39, bars on a figure already sung (low) 0.27, pitch scaling 0.15, distinct rhythms and bars on a rhythm already sung 0.14 each (749.97).
- **Rhythm borrowing helps one lean and hurts another.** With 818's rhythm borrow at 0.2 as well, the rhythm-repetition leans fall to 0.07, but the figure lean rises to 0.45. The fail rate goes from 0.13 to 0.11.

## Merged

`origin/luthier-v8-stage1` into main at c365a48, no fast-forward. Song 58 rebuilt from the v29 record (seventh edition).
