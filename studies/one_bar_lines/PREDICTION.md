# Inside a line given one bar: a reading, its rule written first (749.171)

26 November 2026 (late). The item as the list for v47 set it: under 958 and the kept-shares trial of 749.153, the lines given one bar fit their words better within themselves, the other lines do not move, and the whole fit still falls; kept songs say a change of pace costs nothing (749.172). So the cost is inside the one-bar lines, in a way the line-by-line fit does not catch. Seen before writing: `studies/busy_sections/RESULT_shares.md`, `studies/pace_and_fit/RESULT.md`. Nothing below has been counted.

**The lines read.** Lines of 6 to 8 syllables sung within one bar. In kept songs: a line of 6 to 8 notes whose last onset is less than a bar after its first. In the builds: verse lines of 6 to 8 syllables given a one-bar slot under the trial form (`LUTHIER_VERSE_CLOSER=shares`), songs 49 and 54 written through by v53 with it, then each record's fitted spec, 600 builds, read as sung.

**Read, line by line, and the middle over lines** (a weighty syllable is one of the top tier of the words' weights, as the engine and `make_kept_word_weight.py` both tier them; a note's length is the time to the next onset in its line, the last note's its own length):
- **a.** The spread of note lengths in the line (standard deviation over mean).
- **b.** The share of the line's weighty syllables that fall on a beat.
- **c.** The weighty syllables' length against the line's others: the mean length of weighty syllables over the mean length of the rest.
- **d.** The share of weighty syllables a sixteenth long or less.
- **e.** Where the line starts in its bar (on the first beat; before it; after it), reported.

**Rule.** "The engine's one-bar lines give their weighty syllables no length" is named if, in both songs, the builds' middle of **c** is under the kept 25th by line and the builds' **d** is over the kept share by 10 points or more. "They are flat" (every note the same length) is named if **a** is under the kept 25th in both songs. "The weight is off the beat" is named if **b** is under the kept share by 10 points or more in both. Any, all or none.

**What follows.** For whatever is named, one form, marks first: in a one-bar slot the rhythm is drawn from kept one-bar windows for that syllable count with the words' weights on, where the present draw falls back on a weighted rule or a two-bar window squeezed. I do not know yet which the engine does there; the reading will say.

**What I expect.** "Flat" named: a line of 7 syllables in one bar of 4/4 has little room, and I expect the engine to fill it with even eighths (spread near 0.2) where kept singers push and hold (0.4 to 0.5). c named with it, as a consequence. b not named: on even eighths the weighty syllables fall on beats about as often as kept. I have been wrong about every cause I guessed today but two, so I hold this loosely.
