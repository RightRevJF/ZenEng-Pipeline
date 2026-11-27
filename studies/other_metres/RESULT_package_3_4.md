# The 3/4 repair for v54 (749.226 to 749.229), first reading: result (27 Nov 2026). Six marks met; the pitch count and the commonest pitch missed. Not built.

Rule: `PREDICTION_package_3_4.md` (commit 1f890fd, before any code or run; the band of 52 accepted by the songwriting session at 14:12 ET). Figures: `package_3_4.json` (`python3 studies/other_metres/package_read.py NAME=DIR ...`; the records are outside the repository). Song 53's words, the lead-sheet table, padded, seed 1, 1,000 builds, all four switches on.

| | the package | the mark (52 like-length waltzes) | |
|---|---|---|---|
| Living builds; pool | 636; 171 | 30; 10 | **R1 met** |
| Notes a bar, over 128 bars of sung phrases | 2.09 | 1.76 to 2.51 | **R2 met** |
| Onsets on a beat | 0.832 | 0.717 or more | **R3 met** |
| Stressed syllables on the first beat | 0.622 | 0.583 or more | **R3 met** |
| Range | 14 | 13.75 or more | **R4 met** |
| Distinct pitches | **8** | 9 or more | **R4 missed** |
| Commonest pitch, whole tune | **0.313** | 0.275 or under | **R5 missed** |
| Bars on a figure already sung | 0.825 | 0.874 or under (the 90th: about five songs) | **R6 met** |
| Bars on a rhythm already sung | 0.900 | 0.813 to 0.951 | **R6 met** |
| Inside the voice (60 to 74 in a mezzo's 57 to 77); a leap past an octave | yes; none | | **R7 met** |
| Deaths on 780; on 840 | 0; 0 | each under one in ten | **R8 met** |

Byte for byte, every switch unset: 54, 55, 52, and both 3/4 trial records.

## Reported
- **Other deaths:** 838 (the refrain's lift) 364; nothing else.
- **One switch off at a time** (200 builds each):

| off | living; pool | notes a bar | on a beat | first-beat stress | range | pitches | commonest | figures again |
|---|---|---|---|---|---|---|---|---|
| none (1,000 builds) | 636; 171 | 2.09 | 0.832 | 0.622 | 14 | 8 | 0.313 | 0.825 |
| the plan (749.226) | 106; 21 | 4.19 | 0.537 | 0.408 | 14 | 9 | 0.362 | 0.750 |
| the range (749.227) | 150; 53 | 2.09 | 0.832 | 0.622 | 9 | 6 | 0.317 | 0.858 |
| the title's room (749.229) | 124; 29 | the same as with it on | | | | | | |
| the copy's join (749.228) | 124; 29 | the same as with it on | | | | | | |

  The plan moves density, beats and stresses. The range part moves the range from 9 to 14 and the pitches from 6 to 8, and leaves the commonest pitch where it was. The title's room and the copy's join do nothing on this lyric (no title line lacked room; no copy began too soon), so this trial does not test them: R8 is met without them.
- **Length:** 286 seconds, past the kept 75th of 243.

## Why R4's pitch count and R5 missed: what the reading names
From the chosen record's fitted spec, 600 builds, the 380 living read as sung:
- Range at or over 14 in 15.5 builds of 100; nine pitches or more in 36; commonest pitch at or under 0.275 in 48; **all three in 10**. Such builds exist, about one in ten.
- **The pick's floor reads the range alone** (as 954 does): of 171 in the pool, 32 are at or over the floor, and the first of them is taken. It was not asked for pitches or for the commonest pitch, and got neither.
- **The room at the top is hardly used.** The register plan raised the tops to 77 and left the centres at 64 with the floor at 60. Notes by pitch: 60, 64, 65, 67 carry 75 in 100 of them; everything above 69 carries 7. The draw pulls to the centre and to chord tones (C, E, G are 60 in 100), and a centre a third above the floor keeps the tune in the bottom half of its register.

## What I expected
R1 to R3, R7, R8 met, R4's pitch count the likeliest miss, R5 in question. That is how it fell.

## The one revised form the stopping rule allows: two candidates, for the songwriting session to choose before any run
- **A. At the pick:** the floor reads all three like-length figures. The pick is the first pool build with range at or over the 25th, distinct pitches at or over the 25th, and the commonest pitch at or under the 75th; where none, as now. *What it is worth:* R4 and R5 would then be met by construction wherever such a build is in the pool (about one living build in ten), so a pass would show only that the other marks survive the choice.
- **B. At the draw:** the register plan moves the centres with the tops (each centre to the middle of its floor and new top, as the kept register table's centre sits between its floor and top), so the draw is pulled to the middle of the room it was given. *What it is worth:* it tests whether the engine can write a waltz of kept range and pitch use, not merely find one; it may miss.
I lean to B with A's pick rule left off, because a mark met by selection on that mark tells less. But the choice of form is the mark-setter's.
