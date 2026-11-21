# A check of the lyric's room: result

Rule in PREDICTION.md, written first. `lib/luthier/lyric_room.py`, forty quick tunes a lyric.

| Song | Bars with nothing sung (kept 0.12, 0.19, 0.28) | Change in how busy the singing is (kept 0.34, 0.42, 0.56) | Rhythm scaling (kept 0.61, 0.66, 0.72) | Seconds | Syllables a line: verse, chorus |
|---|---|---|---|---|---|
| 55 Your Yard Man | 0.12 | 0.27 low | 0.59 low | 244 | 7.4, 5.6 |
| 54 The Man Mama Prayed I'd Be | 0.07 low | 0.25 low | 0.57 low | 307 | 8.4, 7.5 |
| 58 Same Time Tomorrow | 0.08 low | 0.19 low | 0.55 low | 337 | 7.5, 6.5 |
| 59 Before the Bread Goes Cold (hold-out) | 0.17 | 0.41 | 0.68 | 240 | 12.0, 5.5 |
| 60 Everything That Moves (not read before) | 0.17 | 0.43 | 0.71 | | |
| 54, cut to two verses and two choruses | 0.14 | 0.40 | 0.60 | | |

("low" is under the kept 25th.)

1. **It agrees with the long way:** 8 verdicts of 8 match the rhythm study's. Met.
2. **It answers to the words:** song 54 cut to two verses reads 0.14 of its bars unsung where the whole lyric reads 0.07. Met. Its contrast rises too (0.25 to 0.40), because a shorter song is given a turn and a break.
3. **It is quick:** about two minutes a lyric. Met.

**It passes, and is added to what is run when a lyric is locked,** beside the mouth tests and before any music. It changes no song and no record.

**What it shows about the five songs.** The two songs with room and contrast in their words (59 and 60) have a kept song's rhythm scaling without anything done to the engine. The three without it (55, 54, 58) do not. Songs 54 and 58 are simply long: 307 and 337 seconds, against 243 for the kept upper quartile.
