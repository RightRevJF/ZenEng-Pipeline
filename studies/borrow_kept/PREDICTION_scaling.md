# Why the pair's pitch scaling runs high: a reading, its rule written first (749.214)

26 November 2026. Seen before writing: `RESULT_whole.md` and `RESULT_pair_whole.md` (the builds' middle pitch scaling 0.79 to 0.88 under v50, 0.99 to 1.05 under form 2, 0.97 to 1.05 under the pair; kept 0.79, 0.91, 1.02), and that the between-line spread in verses sits at 2.1 to 2.3 against a kept middle of 1.54. Nothing below has been counted.

Pitch scaling is one slope fitted over every scale from four notes to a quarter of the song (`lib/luthier/scaling.py`). The same routine gives the slope over the shorter scales and over the longer ones apart.

**Read**, for kept songs (by song) and for the builds (300 a song, v50 records' specs and the pair's refitted specs; the six songs):
- **A.** The slope over the short scales and over the long scales, apart.
- **B.** How far a verse line's middle note is from the middle of the line before it, in scale steps (both four notes or more): the middle distance, by song.
- **C.** Build by build under the pair: how the verse's between-line spread goes with the build's pitch scaling (rank correlation), by song.

**Rule.** "The lines' heights carry it" is named if all three hold: (A) in at least four songs of six the pair's long-scale slope is over the kept 75th and its short-scale slope is not; (B) in at least four songs the pair's middle distance from the line before is over the kept 75th by song; (C) the rank correlation is 0.3 or more in at least four songs. If A holds and B or C does not, the long scales are named and the lines' heights are not. If A does not hold, nothing is named.

**What follows if named.** A form in which a fresh line's height is drawn nearer the line before it, by the kept distances, marks first. Not built here.

**What I expect.** A holds (the long scales rise, the short ones do not, since the borrow's mending changes where lines sit and not how notes follow one another). B holds, narrowly: the pair's lines about 2 steps from the line before, kept about 1 to 1.5. C I am least sure of, 0.2 to 0.4. So "named" at about even odds, with "the long scales named, the heights not" the likeliest other outcome. If the short scales have risen too, I am wrong about the cause, and the chord tie (notes following one another more freely) is the likelier place.
