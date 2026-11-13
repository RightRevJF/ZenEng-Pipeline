# Run 3, Part 2: predictions (written and pushed before the runs)

Part 2 draws each chart (438, 440) and reads every chord at the note. It reruns songs 40, 42 and 43, main and control, each made twice, at the seeds of record. The comparison is with Part 1 on both draws. The charts are drawn once a song from the song's own seed, so main and control share them:

| Song | Bars with two or more changes: before → drawn (target; kept middle half 0–0.33) | Bars holding the last bar's chord: before → drawn (target; kept 0.08–0.44) | Inversions (440) |
|---|---|---|---|
| 40 | 0 → 0.300 (0.300) | 0.091 → 0.209 (0.206) | none drawn (the kept 54%) |
| 42 | 0 → 0.074 (0.068) | 0.059 → 0.235 (0.275) | Cm/Eb ×2, Bb/D, Dm/A (4 of 57 changes) |
| 43 | 0 → 0.287 (0.291) | 0.025 → 0.088 (0.181: the holds the cadences allow) | Dm/A, G/D, Em/B (3 of 96) |

| # | Fix | Reading | Part 1 (main / control) | Predicted for Part 2 |
|---|---|---|---|---|
| 1 | 438 | The chart's shares inside the kept middle halves | outside (no two-change bar; holds 2–9%) | Inside on all three songs (by construction) |
| 2 | 440 | Bass on the root at changes; every third or fifth with a step beside it; at most one in twelve | 100% root | At least 92% root; every inversion with a step on one side |
| 3 | at note | Chord tones in the first verse and chorus, read at the note | 0.632 / 0.608 / 0.641 (40, 42, 43, main) | Within three points of Part 1 on each song: the walk reads the chord at the note too |
| 4 | at note | First-beat chord tones and the chorus's first-beat third (outer) | Part 1's reread | Each within 0.03 of Part 1; a reading |
| 5 | 438 | Survivors | 799 / 890, 799 / 843, 810 / 828 | Down by up to 120 on songs 40 and 43 (designed notes and key words now meet a second chord in a bar); song 42 within 60 |
| 6 | 438 | Key-word deaths (134), song 40 | Part 1's | Up, but under 60 |
| 7 | 438 | Song 43's design deaths ('blue movie') | 107 / 102 | Within two spreads |
| 8 | all | Separation, agreed 30, songs 40, 42, 43, across (main / control) | 0.746 / 0.761 | No real change (within twice the main–control difference) |
| 9 | 440 | Notes a second or seventh from the bass (reread, outer) | Part 1's | Up by under two points on songs 42 and 43, where inversions put the third or fifth under the voice |
| 10 | Part 1 | Part 1's fixes reproduce: song 43 main at ZE_PART=1 from the final files | 911539fed64d | The same order |
