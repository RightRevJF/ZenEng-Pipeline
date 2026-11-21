# Plant the peak in the chorus: the rule for a third trial, written before it is run

**The fault.** Since Window 198 every song's words ask a range of 18 to 20 semitones, and the builds span 14 or 15. The parts' tops are set to the asking, but a top is a ceiling the draw is cut at, and the tune seldom climbs to it.

**Seen before writing:** the first two trials (RESULT.md, RESULT2.md): planting helps a wide aim (song 55's builds within 2 semitones of the aim twice as often; the hold-out from none to 73 in 100) and harms a narrow one; the songs as built also miss the top-note check (53 to 88 builds in 100 inside the kept band). Window 196's `sections.py`: in kept songs the chorus's highest note is at or over the verse's in 75 in 100. Window 198's asks and the builds' ranges.

**The idea, now with the engine's own reason for where.** No song is drawn, so there is no kept song to say where the peak goes. The theory that held is "the top is the chorus's". So: the first line of the first chorus that is drawn fresh sings its highest stressed note at the song's floor plus the range its words ask (inside the voice). The chorus's top is that note; the verse's and the bridge's tops are two semitones under it, so the peak is the chorus's. Lines that return carry it.

Two ways of placing it, as in the second trial: the line **redrawn** in a raised register until its highest stressed note is the peak (60 tries at most); or the line drawn once and **moved** whole by scale steps.

**Trial, outside the engine.** `trial3.py`, 100 tries a song, songs 55, 54, 58 and 60 (the songs that may be fitted to); song 59 read beside them and deciding nothing.

**The check.** A way of placing passes if, in at least three of the four songs:

1. **The range follows the words:** the builds span within 2 semitones of the asking in at least half the builds.
2. **The peak is a peak:** the share of notes on the top note is inside the kept 10th to 90th in at least 8 builds in 10.
3. **Builds survive:** at least 7 in 10 as many pass the gates as built now.
4. **The words still sit:** the words' fit, whole, read before melismas, falls by no more than 0.02.

If both pass, the one with more builds inside the range is built. If neither, nothing is built and the result says which check failed.
