# Luthier list for v35 (since v34)

20 November 2026. Luthier v34 (fixes 931–933) is merged into main at b6bf0e9. Every kept table and every record (songs 52 to 58) reproduces byte for byte. v34 was not reviewed in depth: the writer asked for a hold-out test instead. Song 59, "Before the Bread Goes Cold", was written on v34 as merged, with no engine change during the song and the pick taken as drawn. Its readings are in `studies/holdout59/` (RESULT.md). Four new items (749.113 to 749.116), and new evidence for three carried ones. Next finding 749.117; next fix 934.

## The hold-out in short

Song 59 is a new lyric: heartland rock, 120 bpm, baritone, guitar, major, rock tables. It aims at Two Hearts (Phil Collins, 1989). Record: key A, 240 s, 138 of 1,000 builds survive.
- **Sound.** No check past the kept 10th to 90th. The three-song rule passes on every three of songs 55, 54, 58 and 59.
- **Too central.** 3 of the 21 checks read on kept songs are outside the kept middle half. Only 1 kept song in 147 is as central. Songs 55, 54 and 58 are at 6, 6 and 5.
- **Near its aim only where the aim is ordinary.** Its builds sit 0.16 of a kept middle-half width from Two Hearts at the median (55, 54, 58: 0.46, 0.62, 0.55), because Two Hearts sits near the kept middle. Where Two Hearts leaves it, the builds stay in the middle: range 17 against 24, repeated notes 0.336 against 0.21, rhythm scaling 0.676 against 0.593. Median share of the way from the kept middle to the aim: −0.10 (55, 54, 58: 0.91, 0.30, 0.09).

## Items

### 749.113 Repeated notes run high against every aim
**Problem.** In all four songs the builds repeat a pitch more often than the aimed song does, by 0.06 to 0.13. This holds whether the aim sits under or over the kept median. The 920 tilt and the 930 fit do not reach it.
**Evidence.** Every living build's median against the aim (`studies/review19/aimpool.json` at v34; `studies/holdout59/aimpool59.json`): 0.265 against 0.158 (55), 0.222 against 0.110 (54), 0.437 against 0.373 (58), 0.336 against 0.210 (59). Kept median 0.312.
**Fix.** First trace where the repeats are made: in fresh lines, in lines that return (712, 818, copies), or across joins. Then fit the repeated-note weight with the step and leap weights (930), bounded by the fresh lines as 932 does.
**Check.** In each of the four songs, the builds' median repeated-note share within a quarter of the kept middle half's width of the aim. The rule holds on the pools.

### 749.114 Long lines at a quick tempo fail in the rhythm draw
**Problem.** Song 59's verse lines run 11 to 14 syllables at 120 bpm. Every verse line is given a three-bar slot "past the kept two-bar windows" (760's weighted placement), and half the builds die before a pitch is drawn.
**Evidence.** Song 59's record: deaths "rhythm: the syllables cannot fit the window" 500 of 1,000; 138 builds survive. The flags name every verse line of both verses. None of songs 55, 54 or 58 loses builds this way.
**Fix.** Trace which lines fail and at which step before changing anything. Then read how kept songs set long lines at 110 to 130 bpm (syllables a bar, rests, three-bar phrases), and let a long line take a three-bar window built from kept windows rather than failing.
**Check.** In song 59, rhythm-draw deaths under 10 in 100, and the verse's notes a bar inside the kept 10th to 90th.

### 749.115 The step fit reads too few builds when many die
**Problem.** 930's rounds draw 80 trial builds and read those that pass the gates. When most builds die (749.114), a round reads too few to fit on, and the fit wanders.
**Evidence.** Song 59's `moves_fit`: rounds read 16, 17, 16, 13, 9 and 14 builds of 80. The step medians bounce 0.33 to 0.43 as the weights move, and the kept round (2) leaves the step weight at 1.208, the default.
**Fix.** Draw each round until 40 builds pass the gates (with a cap, say 400 tries), and record the tries and builds read a round.
**Check.** Every round reads at least 40 builds in all four songs. Song 59's fitted weights are stable when the fit is rerun with a different trial seed.

### 749.116 The break reads louder than the last chorus
**Problem.** Song 59 has an eight-bar break (830): the lead guitar plays verse 1's tune over the full band. In the demo's energy reading the break is the loudest section, above the last chorus, though its level in the record is 0.86 against the last chorus's 1.0.
**Evidence.** Song 59's documents: "the last chorus or the bridge the top (9.12)" not met; last chorus 0.47, break 0.64. The lead guitar adds a fourth band track to the full groove.
**Fix.** Under the break, thin the band to the break's level (the rhythm guitar to fewer strums or softer), so the lead takes the space rather than adding to it.
**Check.** In song 59, the last chorus or the bridge reads as the top of the arc.

## Carried, with the hold-out's evidence
- **749.103** Variety. Out of sample, song 59 is more central than 146 of 147 kept songs (3 checks outside the middle half). The songs are sound but too alike to the middle.
- **749.111** The peak. Out of sample, song 59's builds span 17 against an aim of 24. The tops were set for 22, the baritone's span plus one. v34's trial says to place the peak note directly next; song 59 is a further test case.
- **749.109** Repeats and rhythm following the aim. Song 59's rhythm scaling sits at 0.676 against 0.593, the far side of the kept median from its aim.
- **749.104** (with 749.101 and 749.109 waiting on it), **749.61**.

## A rule for song 59
Keep song 59 as the hold-out. Read it after every fix, beside songs 55, 54 and 58, but never fit a weight or a setting to it. Its lyric and settings stay as they are (`songs/p69/lyric59.json`).

## Order of work
1. 749.115 (so the fit reads enough builds). 2. 749.114. 3. 749.113. 4. 749.116. 5. 749.111 with the peak placed directly. Rerun `neighbour.py`, `studies/review20/` and `studies/holdout59/` after each.

## Regression line
The records of songs 52, 54, 55, 58 and 59 (`.song.json`), song 52's and song 53's run files, the seven kept tables, `studies/soundness/soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones.
