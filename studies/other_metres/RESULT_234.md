# 749.234, lines that share a tune share their bars; the pop-style 3/4 trial read for the first time: result (27 Nov 2026). Every mark but K3 is met. Not built.

Rule: `PREDICTION_234_235.md` (commit 861d380, before any code or run), marks K1 to K8 of `PREDICTION_pop_3_4.md` with K6 within sections and the songwriting session's K3. Song 55's words in 3/4, rock, 133; the pop table; the plan form, form B, the title's room, the copy's join, 749.231's rule, and `LUTHIER_SHARED_BARS=1`; seed 1, 1,000 builds; two runs, the deduced stress table and the deduced, shrunk one. Figures: `pop_234.json` (`pop_read.py`); living = the living builds of 600 from each record's fitted spec.

**The shared bars.** Verses 1, 2 and 3 now all run `[3, 2, 3, 2, 3, 2, 2, 3]`; seven lines changed their count to match their group.

| | deduced table: pick; living median | shrunk table: pick; living median | the mark | |
|---|---|---|---|---|
| Living builds; pool | 316; 158 | 320; 160 | 30; 10 | **K1 met** (10 and 5 before) |
| Notes a bar | 2.61; 2.62 | 2.61; 2.62 | 2.38 to 3.85 | **K2 met** |
| Onsets on a beat | 0.565; 0.553 | 0.565; 0.561 | 0.508 or more | **K3 met** |
| **Stressed syllables on the first beat** | **0.246; 0.241** | **0.246; 0.241** | 0.45 or more | **K3 missed** |
| **Stressed syllables off the beat** | **0.348; 0.385** | **0.348; 0.374** | 0.26 or under | **K3 missed** |
| Range; distinct pitches | 17, 13; 16, 11 | the same | 12; 7 | **K4 met** |
| Commonest pitch | 0.197; 0.257 | 0.197; 0.266 | 0.303 or under | **K5 met** |
| Rhythm again, within sections | 0.40; 0.36 | 0.40; 0.36 | 0.349 to 0.871 | **K6 met** (the median by 0.011) |
| Figures again, within sections | 0.25; 0.19 | 0.25; 0.20 | 0.667 or under | **K6 met** |
| In the voice (44 to 61 in a baritone's 43 to 64); a leap | yes; none | yes; none | | **K7 met** |
| Deaths on 780; on 840, in ten | 0; 0.95 | 0; 0.75 | under one | **K8 met** (840 narrowly) |

Whole-song figures beside K6, deciding nothing: rhythm again 0.74 pick and 0.71 median; figures again 0.62 and 0.58.

Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## What it shows
- **749.234 does its work:** 316 living builds and a pool of 158 where there were 10 and 5.
- **A pop song in three, by the pop table's own figures, is nearly there on the first reading:** density, beats, range, pitch count, the commonest pitch and the repetition within sections all meet their marks on the living median and the pick. The commonest pitch, which the waltz style never met, is met here (0.26 against 0.30).
- **K3 misses badly, and the same in both tables.** A quarter of stressed syllables fall on the first beat (the deduced table says half), and more than a third fall off the beat (it says a fifth). The two tables give the same pick and the same medians: **the stress rule is not what decides where a syllable goes here.** Its pull is about half a point a syllable; the draw takes a kept window by its count first, and the pop table's windows are syncopated (64 onsets in 100 on a beat, 28 on the first). The rhythm comes from songs without words, so nothing in it knows where a stress wants to be.
- **Still 42 builds in 100 are never made** ("the syllables cannot fit the window"). Shared bars mended most of it and not all; it is the next thing to read.
- No living build meets every figure mark, because none meets K3.

## What I expected
K1 met, K2 to K5 likely, K6 uncallable, K3 likely on the shrunk table. K3 missed on both and by a wide margin; I thought the stress table would steer more than it does.

## Not built. What the next form has to answer
1. **Stress in a pop draw.** Either the stress rule's weight in the draw is read from data too (how strongly do kept songs trade a commoner rhythm for a better-placed stress: the maxent weighting the research and the songwriting session both pointed to), or K3's marks are wrong for this lyric: song 55 was written for 4/4, with four-syllable title lines of three stresses, and may not be able to put half its stresses on a first beat in three. Both should be read before a form is chosen.
2. **The builds that are never made:** which lines, and why, now that sharing is in.
