# The pitch scaling by bands of scale, and by the line's join: a reading, its rule written first (749.215)

26 November 2026. Agreed on the thread (`coord/songwriting.md`, 12:55), with the songwriting session's addition of the split at the line's join. Seen before writing: `RESULT_scaling.md` (the slope over four to about nineteen notes rose from 0.85 to 0.99 under v50 to 1.11 to 1.17 under the pair, kept 0.93, 1.05, 1.14; the longer scales did not move). Nothing below has been counted.

**Read**, kept songs by song, and the builds (300 a song; v50 records' specs and the pair's refitted specs; six songs):
- **Bands.** The fluctuation of the detrended pitch series (`lib/luthier/scaling.py`'s method) at scales of 4, 8, 16, 32 notes and a quarter of the song; the local slope in each band: 4 to 8, 8 to 16, 16 to 32, over 32.
- **The join.** The middle size, in semitones, of the move between two neighbouring notes inside one line, and of the move across the join from a line's last note to the next line's first (within a section), and the share of each that is no move at all.

**Rule.** A band is **named** if the pair's builds' middle local slope is over the kept 75th by song in at least four songs of six. For the join: **the join is named** if the pair's middle move across the join is outside the kept middle half by song in at least four songs while the move inside a line is inside it; **the line's own notes are named** if it is the other way about. A form only for what is named.

**What follows** is already written on the thread, before this result: if something mendable is named, its form and marks first; if nothing mendable is named, or its form fails, the pair goes to sealed song 66 on the marks posted there.

**What I expect.** The band 8 to 16 named (the scale of one line to the next), 4 to 8 not. The join: the pair's move across a join smaller than kept, because a fresh line's first note is drawn from the last note of the line before by the same interval odds as any note, where kept songs start a line afresh; so "the join named". I hold the second more loosely than the first; I was wrong about the long scales an hour ago.
