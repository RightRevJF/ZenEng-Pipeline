# Luthier fix list for v21 (since v20)

18 November 2026. The Doc: https://claude.ai/artifact/RQxAdg4csitmXzea4T5r7k (this file is its copy in brief; the Doc has each finding's Problem, Evidence, Fix, Check).

All seven stages of the v8 plan are written (Luthier v20, fixes to 866) and merged at 0f5d1b6; every stage's commands reproduce the committed records.
Song 58, "Same Time Tomorrow" (p68), is the first song written end to end from its lyric with song_from_lyric.py (ac8309b). Earlier findings 740 to 749.56
are closed; their record is the Doc "Luthier fix list since v8" and songs/p67/fixlist_v8_since.md. Next finding 749.66; next fix 885.

## Open findings
- 749.57 The descant's ceiling (A5) is read in the written key; song 53's final refrain is sung in F, so the summit sounds C6.
- 749.58 Rests between lines sit at the kept 10th percentile (a quarter at 34/49, 30/49, 28/28 joins); rest shares 0.12-0.17 under the kept 0.21.
- 749.59 Melismas fall on function words (song 52: 12 of 23, "in" 6, "a" 4).
- 749.60 863 ranks the pick by low surprise and sure endings, which 865's bench rejected (-0.142, -0.026 against peak).
- 749.61 The kept band is the spread between songs: the gate takes the tail (54, 55), almost nothing (52, 6/8) or almost everything (58), by song.
- 749.62 859's old judge "stays as a gate" but chooses nothing; it is the bench's best damage detector.
- 749.63 slots.py rounds a ballad's lines down to one bar (song 58: 38 of 57 lines; 45% sixteenths against the kept 15%; 548 of 1000 builds die for want of a fit).
- 749.65 Breath against the bars. HELD OUT ON 1,479 HOOKTHEORY SONGS: DOES NOT HOLD (odds 1.34, p 0.11; four-bar length AUC 0.47); nothing to build for greatness. Discovery was: breath locked to 1, 2 or 4 bars in hits 0.57-0.62 against 0.33 in songs below no. 20; v22 mends the count (song 58 1.8 to 6.1 real breaths a minute) but not the grid (58 every 8.8 beats, 55 every 13). Note on 749.19: the 0.55-0.65 return is not supported by the notes; loosen any gate on it.
- 749.64 Line-final words stressed on the first syllable hold the weak one (song 58: 7 of 14; "morning" 3 then 15 twelfths, "reason" 6 then 24).

## Order of work
1. 749.63, 749.64, then rerun song 58 (its scores and songbook wait on them). 2. 749.60-749.62. 3. 749.58, 749.59. 4. 749.57.

## Known not met (the paper's own)
822 major endings 54 against 41; 834 met on song 55 only; 835 fourths 0.25-0.32 against 0.119; 840 song 54 0.5; 848 line-end melismas 55 and 68 against 20.

## Regression line
lyric52/54/55/58.song.json (+ .song.txt), spec52.run.json, spec53.run.json, spec53.parts.json, stage4_results.json: byte for byte, or the fix says so and commits the new record.

## What a person typed for song 58
The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre, bpm, voice, lead, mode, genre, seed. Bars a line could not be typed (749.63).

## Two proposed vectors, tested and not supported (studies/tda/)
- TDA of harmonic space (tda_mcgill.py, 733 McGill songs): distinct-chord readings are chord counts (clusters 0.996 with distinct chords); no reading against chart peak past |rho| 0.065 (all p > 0.07); beyond plain readings |rho| <= 0.05.
- Harmonic transition networks (network_mcgill.py, 721 songs): median 6 chords a graph; 416 of 680 small-world; no reading against peak, alone or beyond plain readings; hub share -0.078 (p 0.036, one of ten), against the claim; shortcuts 0.031 (p 0.41).
- Breath (studies/breath/), held out and not supported: the four-bar line lasts 9.2 s in year-end hits, 7.1 s below no. 20 (AUC 0.71); breath on the grid (749.65); the 0.55-0.65 return not supported.
