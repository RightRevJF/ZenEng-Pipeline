# Melismas carried with a line sung again: the rule, written before the trial

**What the first trial showed.** Read before melismas, songs 55 and 54 already sing their bars again as often as the songs they aim at. The shortfall seen in every window is in the tune as sung, after the melismas are placed. A copied line takes its source's melismas (919). A line sung again to new words (712) does not: its melismas are drawn afresh, so each one is a bar that no longer matches.

**The idea.** A line sung again takes its source's melismas, syllable for syllable, where the two lines have the same number of syllables, as a copied line does.

**Trial, outside the engine.** `trial2.py` reads the same builds twice: with melismas placed as the engine places them, and with the "again" lines treated as copies for the melismas only. No note of any build changes.

**The check, on songs 55, 54 and 58** (song 59 read beside them, deciding nothing):

1. As sung, the builds' median share of bars on a figure already sung rises in at least two of the three songs, and on a rhythm already sung likewise, and neither falls by more than 0.01 in any song.
2. The words' fit, whole, read as sung, falls by no more than 0.01 in any song (the notes are the same; only which syllables carry two notes changes).

It passes if both hold.
