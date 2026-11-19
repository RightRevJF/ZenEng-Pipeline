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

# The learned space (19 Nov 2026). Study only; nothing built.
Spaces learned without grades from songs in neither graded set; a ridge reader fitted on one set, judged on the other. Predictions in learned/PREDICTION.md.

| test | fitted on -> judged on | partial rho with G | verdict |
|---|---|---|---|
| T1 L1 codebook (64 regions) | set 1 -> set 2 | +0.103 (p .0097); reverse +0.061 (p .041) | PASS |
| T2 L2 autoencoder code | set 1 -> set 2 | +0.020; reverse +0.030 | fail |
| T3 L3 words in | five-fold in set 2 | -0.025 (notes-only twin -0.007) | fail |

Checks on T1 after the fact: 15 other codebooks (32, 64, 128 regions x 5 seeds) all positive both ways, median +0.09 forward and +0.055 reverse; holds with chart peak held.
Against it: with set 1's grades shuffled the forward score's 95th percentile is 0.083 and 99th 0.116, so +0.10 is between them; five-fold inside set 1 reads -0.006;
on the 335 set-2 songs matched with an artist it is weaker (+0.03 to +0.10). About one part in a hundred of what makes G. Not yet known what the reader reads.

# Opening the regions map (19 Nov 2026). After the fact; nothing built.
- Genre: with seven Spotify genre families and decade held, forward +0.092 (p .021), reverse +0.044 (p .15). Some of the reading is genre; not all.
- The same regions lean great in both sets: region-by-region lean toward G, set 1 against set 2, r = +0.60 over 64 regions.
- No plain trait carries it. Region lean against pace, longest note, unevenness, span, step size, rise, repeated notes, tonic-chord notes: all under 0.2 either way; off-scale notes +0.18 / +0.16.
  Read straight off the songs, slower pace and long notes lean great in set 2 (+0.14) but not set 1 (+0.04).
- So the reader reads a pattern over many kinds of phrase, not one nameable feature. Next: a third graded set, never seen, with the reader frozen.

# The regions map on a third set (19 Nov 2026). Study only; nothing built.
1,388 Lakh clean-MIDI songs, none in sets 1 or 2; codebook and reader frozen. Prediction in third/PREDICTION.md.
Frozen reader against G: +0.008 (p .77). FAIL. Reader of set 1 alone -0.024; of set 2 alone +0.042; genre and decade held +0.009;
the 712 best-scored voice tracks -0.006. Region leans of set 3 against set 1: -0.25; against set 2: -0.02 (sets 1 and 2 against each other +0.60, unexplained and now distrusted).
Caveat stated beforehand: the voice track in this set is guessed. But the better-guessed half reads no higher, so that does not rescue it.
Verdict on the whole study: across five runs and about 3,100 songs, no shape of the tune, hand-built or learned, tells good from great on songs it has not seen.
Word-and-tune remains untested on enough well-aligned songs.
