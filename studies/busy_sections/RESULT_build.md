# The verse sung closer, built (958): result

22 November 2026. Checks in `PREDICTION_build.md`, written before the build was run. A thousand builds a song.

**The six checks on the fitted songs are met. The new hold-out, song 49, disagrees on the words' fit.**

| Songs 55, 54, 58 | Without the form (v44) | With it (v45) |
|---|---|---|
| 1. Rhythm scaling, the builds' middle (kept quartiles 0.605 to 0.721) | 0.592, 0.576, 0.555 | **0.678, 0.620**, 0.592 |
| 2. The chosen tune's words' fit (may fall 0.02) | 0.341, 0.275, 0.307 | 0.347, 0.272, 0.357 |
| 3. Builds that live (7 in 10 to be kept) | 342, 309, 419 | 281, 304, 405 |
| 4. The three chosen tunes | sound; one lean (rhythm scaling, low); 12 checks outside the middle half | sound; **no lean**; 10 |
| 4. Pools: a random pick fails the rule; the neighbour choice | 2.2; 2.0 in 100 | 0.0; 0.0 |
| 5. Verse over chorus, notes a bar (kept 0.83 to 1.48) | | 1.17, 1.11, 1.06 |
| 6. Floor and ceiling kept by the chosen tunes | yes | yes (ranges 17, 19, 17 as sung) |
| The chosen tune's rhythm scaling | | 0.688, 0.646, 0.550 |

Every figure is the one the songwriting session reported from its own run. Song 58's chosen tune stays under the kept 10th of rhythm scaling (0.550 against 0.574), as the session found; that is 749.144.

**The hold-outs.**

| | Song 59 | Song 49, without the form | Song 49, with it |
|---|---|---|---|
| Verse lines given one bar | none (no line of 6 to 8 syllables) | | lines 1 and 3 of each verse |
| The chosen tune's rhythm scaling | 0.690 | 0.612 | **0.668** |
| Bars with nothing sung (kept 0.12 to 0.28) | 0.212 | 0.083 | **0.207** |
| The chosen tune's words' fit | 0.320 | 0.326 | **0.210** |
| The builds' middle words' fit | | 0.264 | 0.224 |
| The chosen tune's range (asked 17.9; floor 14.6) | 19 | 20 | 16 |
| Builds that live | 376 | 344 | 356 |
| Seconds | 240 | 291 | 280 |

Song 59's notes are the same, note for note, as expected.

Song 49 is the first test of the lever on a song nothing was fitted to. Its rhythm scaling rises into the kept middle half and its bars of rest into the kept range, as hoped. But its chosen tune's words' fit falls by 0.116, where the check allows the fitted songs 0.02, and its builds' middle falls by 0.040. Its chosen tune is still over the kept floor (0.152) and under the kept 25th (0.248). One chosen tune is one draw from a pool of 14, so the 0.116 is noisy; the builds' fall of 0.040 is not, and it is larger than song 54's (0.028).

**Against what I expected.** I expected song 49's rhythm scaling to rise by 0.03 to 0.06 (it rose 0.056) and its chosen tune's words' fit to move by under 0.03 (it fell 0.116). I was wrong on the second.

**What I make of it.** Song 49's verse lines are all 8 syllables (one of 9). Eight syllables in a bar are eighth notes end to end. That is the case I flagged in Window 201 and the session set aside because song 54's chosen tune did not show it. The hold-out shows it. `studies/lever_range` adds that kept songs put an 8-syllable verse line in one bar 9 times in 100 (13 at a middle tempo, 21 at a slow one), a 7-syllable line 18 and a 6-syllable line 28; the form gives two to four of a verse's eight lines one bar whatever their length.

**What stands.** 958 is built as the session ruled, and by the rule written first it stands or falls on the session's reading of the hold-out, not mine. My reading: the lever is right and its reach is too long. The next trial should weight which lines are taken by how often kept lines that long take one bar at the song's tempo, so that 8-syllable lines are taken seldom and 6-syllable lines first, and should be judged on songs 54 and 49 for the words' fit.
