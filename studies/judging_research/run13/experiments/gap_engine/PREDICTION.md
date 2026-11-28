# gap_engine: what do real songs have that the engine's builds lack? (run 13; no outcome)

Written before the engine features are computed against the real ones (the real clips' features exist: build_hook13.py, notes only).

**Data.** Real: the 14,747 4/4 Hooktheory clips of run 04's within-artist rows (features13, first 8 bars). Engine: survivors of the committed metre engine on songs 50, 54, 55, 58, 60, 61, 62 and 66 (1,500 builds each; up to 150 survivors a song, every section with 12 or more notes in its window), plus each song's actual pick (song.json) as a reading.

**Discriminator.** L2 logistic regression (C = 1) on z-scored features (missing → median), classes weighted equally; grouped 8-fold CV, groups = artist (real) and song (engine), so each engine song is held out once; out-of-fold AUC.

**Per feature.** AUC real-vs-engine and medians; sign agreement across the eight engine songs; the "gap list" = features with |AUC − 0.5| ≥ 0.15 and the same sign in at least 7 of 8 songs, ranked.

**Numeric predictions (written first).**
- P1: out-of-fold AUC ≥ 0.90 (the engine's builds are easy to tell from real songs by notes alone).
- P2: the commonest pitch class's share: engine median > real median (world music finding 10).
- P3: bar rhythm repetition minus bar interval repetition: real median > engine median (finding 7: real music repeats rhythm more than pitch; the engine remembers pitch, not rhythm).
- P4: in real clips, median bar rhythm repetition exceeds median bar interval repetition (finding 7's sign, on pop).
- P5: real median phrase range (phrases cut at a gap of a beat or more) between 7 and 11 semitones (finding 9: about 9).
Each is reported true or false. Gaps found become candidate rules for the maintainer, read against kept songs first (no gate).
