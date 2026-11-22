# The verse sung closer, built (958; 749.142): the checks, written before the build is run

22 November 2026. The songwriting session's Review 29 ruled that the form be built, and moved the fifth check from the builds' middle to the chosen tune. It ran the three songs under the switch and reported the chosen tunes (`studies/review29_verse_closer`).

**Seen before writing:** Window 201's trial figures (`RESULT.md` here); the session's figures for the chosen tunes under the form (words' fit 0.347, 0.272, 0.357; rhythm scaling 0.688, 0.646, 0.550; sound, no lean); song 61's record being unchanged by the form. Nothing of song 49 under the engine: its lyric file is made today from the locked lyric, and it has not been run.

**The build.** `VERSE_CLOSER = "apart"` as the default in `plan()`, as tried: in each verse, lines of 6 to 8 syllables that would take two bars are taken shortest first, never two side by side, an even count, as many as bring the verse nearest the kept middle of notes a bar (4.59), and given one bar. A lyric may switch it off (`"verse_closer": false`), as it may ask for another movement: the default is the engine's.

**The checks (the session's, 749.142), on a thousand builds a song.**
1. Rhythm scaling, the builds' middle, inside the kept quartiles (0.605 to 0.721) in two of songs 55, 54 and 58.
2. No chosen tune's words' fit more than 0.02 under the tune chosen without the form (0.341, 0.275, 0.307), in each of the three.
3. At least 7 in 10 as many builds live as without the form (342, 309, 419), in each.
4. The soundness rule on the three chosen tunes, and the pool standard (a random pool pick and the neighbour choice pass the rule 90 times in 100).
5. The guard: the verse's notes a bar over the chorus's inside the kept 10th to 90th (0.83 to 1.48).
6. The chosen tunes keep the floor (954) and the ceiling (956).

**The hold-outs, read and deciding nothing.** Song 59 (no verse line of 6 to 8 syllables: expected unchanged, byte for byte in its notes). Song 49, by the session's rule (the most recent 4/4 song not yet run by Luthier v8 with at least four verse lines of 6 to 8 syllables): run without the form and with it, and both reported. I have not seen either.

**What I expect.** The checks hold, since the session has run the form; my figures should match its figures. For song 49: its verses are 7 to 9 syllables like song 54's, so I expect two lines a verse to take one bar, its builds' rhythm scaling to rise by 0.03 to 0.06, and its chosen tune's words' fit to move by less than 0.03 either way. If song 49's chosen tune loses more than 0.02 of words' fit, that is reported as the hold-out disagreeing, and the form stands or falls on the session's reading of it, not mine.
