# How a line repeats an earlier line: a reading, its rule written first (749.203, next step)

26 November 2026. Seen before writing: the ladder (`studies/ladder/RESULT.md`), and the code of fix 818: a fresh line, from a part's third line on, sings the line two before it again (or the one before) with the chance the song's borrow is fitted to, which is 0.8 in every record I have looked at. Nothing of kept songs' repeats has been read.

**The question.** The engine repeats a line at the same pitch, and often. Do kept songs repeat as often, and at the same pitch?

**What counts as a repeat.** Two lines of the same part, each of four notes or more. Their notes are read as steps of the song's scale (so a figure a third higher is the same figure), aligned from the first note over the shorter line's length. The later line repeats the earlier if their scale-step intervals agree in at least four places of five. Its **height** is the middle difference between the aligned notes, in scale steps: 0 is the same pitch.

**Read, in kept songs and in the builds** (v50 fitted specs, 300 builds; songs 55, 54, 58, 49, 50, 59), for verses and for choruses:
- of the lines from a part's second on, the share that repeat the line before or the line two before (the engine's own two choices), and the share that repeat any earlier line of the part;
- of those repeats, the share at height 0, and the spread of the other heights.

**Rule.**
1. **"At another height" is named** if at least 25 in 100 of kept verses' repeats are at a height other than 0, and in at least four songs of six the builds' are under 10 in 100.
2. **"Too often" is named** if in at least four songs of six the builds' share of verse lines that repeat the line before or two before is over the kept 75th by song.
Either, both or neither.

**What follows if named.** 1: a borrowed line is sung at a height drawn from the kept heights, moved by scale steps. 2: the borrow's chance is set by the kept share of lines that repeat, in place of being fitted to the share of bars on a figure already sung. Marks first, for whichever it is.

**What I expect.** Both. Kept repeats at another height perhaps 30 to 45 in 100 (sequences are ordinary in tunes), and the engine's near none. The engine repeating about twice as often as the kept middle. I hold the second more firmly than the first; if kept repeats are nine in ten at the same pitch, then the mend is the chance and not the height.
