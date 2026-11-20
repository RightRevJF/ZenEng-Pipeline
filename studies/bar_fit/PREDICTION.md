# The bar fit (749.104, with 749.122): the rule, written before the trial

**The fault.** When a line returns to new words, the engine refits its source's notes to the new syllables (712, 882): it chooses, over the whole line, which notes to split, drop or lead into by where the new words' stresses fall. That serves the words, and it moves notes all along the line, so the returning line's bars are seldom the source's bars. Kept tunes sing a bar again far more than Luthier's songs do, and the returning lines repeat a pitch more than the fresh lines they come from.

**The idea.** Keep the source's bars. Change only as many notes as the syllable counts differ by, and only where it costs the bar least:

- same count: the source's notes as they are;
- more syllables: split the longest notes (earliest on a tie). The new second half does not repeat the pitch: it steps toward the next note, or, where the next note is the same pitch, to the scale neighbour nearer the line's register centre;
- fewer syllables: drop the shortest notes that are not on a beat, not the line's first or last, preferring a note that repeats the one before it, and never one whose two neighbours are the same pitch (that would make a repeat);
- a source pickup the new line cannot use (it would begin before the line may) is dropped first, as now.

The notes then pass through the engine's own chord and register corrections, unchanged.

**Trial, outside the engine.** `trial.py` replaces `Engine.again` on an engine built from each song's record; nothing in `lib/luthier` changes. 150 tries a song. Read on the builds that pass the gates, before melismas are placed (melismas are 749.104's second half and are not in this trial).

**The check, on songs 55, 54 and 58** (song 59 is read beside them and decides nothing):

1. **Bars return.** The builds' median share of bars on a figure already sung, and on a rhythm already sung, each closes at least a third of its gap to the aimed song in at least two of the three songs, and in no song moves away from the aim by more than 0.02.
2. **No extra repeats** (749.122). In songs 55 and 54 the returning lines' repeated notes are no more than 0.03 over the fresh lines'.
3. **The words still sit.** In each song the builds' median share of stressed syllables on a beat stays at or over the kept 25th (0.446), and the builds that pass the gates are at least two thirds as many as with the engine's own refit.

The idea passes if all three hold. If 1 or 2 holds and 3 fails, the bars were bought with the words, and it is not built as it stands.
