# Luthier fix list for v21 (since v20)

18 November 2026. The Doc: https://claude.ai/artifact/RQxAdg4csitmXzea4T5r7k (this file is its copy in brief; the Doc has each finding's Problem, Evidence, Fix, Check).

All seven stages of the v8 plan are written (Luthier v20, fixes to 866) and merged at 0f5d1b6; every stage's commands reproduce the committed records.
Song 58, "Same Time Tomorrow" (p68), is the first song written end to end from its lyric with song_from_lyric.py (ac8309b). Earlier findings 740 to 749.56
are closed; their record is the Doc "Luthier fix list since v8" and songs/p67/fixlist_v8_since.md. Next finding 749.65; next fix 867.

## Open findings
- 749.57 The descant's ceiling (A5) is read in the written key; song 53's final refrain is sung in F, so the summit sounds C6.
- 749.58 Rests between lines sit at the kept 10th percentile (a quarter at 34/49, 30/49, 28/28 joins); rest shares 0.12-0.17 under the kept 0.21.
- 749.59 Melismas fall on function words (song 52: 12 of 23, "in" 6, "a" 4).
- 749.60 863 ranks the pick by low surprise and sure endings, which 865's bench rejected (-0.142, -0.026 against peak).
- 749.61 The kept band is the spread between songs: the gate takes the tail (54, 55), almost nothing (52, 6/8) or almost everything (58), by song.
- 749.62 859's old judge "stays as a gate" but chooses nothing; it is the bench's best damage detector.
- 749.63 slots.py rounds a ballad's lines down to one bar (song 58: 38 of 57 lines; 45% sixteenths against the kept 15%; 548 of 1000 builds die for want of a fit).
- 749.64 Line-final words stressed on the first syllable hold the weak one (song 58: 7 of 14; "morning" 3 then 15 twelfths, "reason" 6 then 24).

## Order of work
1. 749.63, 749.64, then rerun song 58 (its scores and songbook wait on them). 2. 749.60-749.62. 3. 749.58, 749.59. 4. 749.57.

## Known not met (the paper's own)
822 major endings 54 against 41; 834 met on song 55 only; 835 fourths 0.25-0.32 against 0.119; 840 song 54 0.5; 848 line-end melismas 55 and 68 against 20.

## Regression line
lyric52/54/55/58.song.json (+ .song.txt), spec52.run.json, spec53.run.json, spec53.parts.json, stage4_results.json: byte for byte, or the fix says so and commits the new record.

## What a person typed for song 58
The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre, bpm, voice, lead, mode, genre, seed. Bars a line could not be typed (749.63).
