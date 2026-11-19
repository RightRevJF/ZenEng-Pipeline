# Song as a shape — first run (19 Nov 2026). Study only; nothing built.
Yardstick: still loved (Spotify 2021 within era) + covered (SecondHandSongs within era). 1,102 songs of 2005 or earlier.
Partial Spearman with the yardstick, holding year, note count, source. Predictions in PREDICTION.md, written first.

| measure | predicted | half A | half B | pooled | verdict |
|---|---|---|---|---|---|
| M1 return | + | +0.020 | -0.060 | -0.019 | fail |
| M2 varied return | + | -0.040 | -0.020 | -0.032 | fail |
| M3 curvature | - | +0.064 | +0.107 | +0.084 (p .005) | fail: opposite sign |
| M4 persistence | + | -0.001 | -0.113 | -0.058 | fail: opposite sign (whole songs -0.130, p .006) |
| M5 room used | - | +0.009 | +0.046 | +0.027 | fail |
| M6 loops | + | -0.015 | -0.000 | -0.009 | fail |
| M7 word and tune (128 songs) | + | +0.188 | +0.061 | +0.128 (p .15) | fail: right sign, not significant |

M7 unshuffled (not the form predicted): +0.22, p .013; with love alone +0.24, p .006.
No measure passed. Two leads to carry to fresh songs: (a) great songs turn more and persist less (M3, M4, opposite to prediction);
(b) word-and-tune coupling leans the predicted way but 128 songs cannot settle it.

# Second run, fresh songs (19 Nov 2026). Study only; nothing built.
634 songs from the Yu et al. lyrics-melody set (Lakh + Reddit MIDI), none used in the first run, 2005 or earlier. Predictions in second/PREDICTION.md, written first.

| measure | predicted | half A | half B | pooled | verdict |
|---|---|---|---|---|---|
| M7 word and tune over shuffled | + | +0.101 | -0.050 | +0.033 | fail |
| M7r word and tune, unshuffled | + | +0.095 | -0.076 | +0.016 | fail |
| M3 curvature | + | -0.022 | +0.017 | -0.003 | fail |
| M4 persistence | - | -0.000 | -0.106 | -0.048 | fail |

Neither lead from the first run held. Caveat on M7 only: in this set the words sit on the tune above their own shuffles in 21% of songs
(87% in the kept corpus), so the material is a poorer test of word-and-tune than of the tune's shape. M3 and M4 need no such excuse: they did not repeat.

# Word and tune on the Rolling Stone songs (19 Nov 2026). Study only; nothing built.
Only 80 of the 200 Rolling Stone files carry words; 44 are on the yardstick and fresh. Predictions in rolling_stone/PREDICTION.md.
M7 pooled -0.07 (halves -0.40, +0.31); M7r +0.15 (halves -0.21, +0.68); M7s -0.10. All fail; the halves contradict each other.
The material is good (84% of songs fit their words above a shuffle) but 44 songs settle nothing either way.
