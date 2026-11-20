# The bar fit where the words allow: the rule, written before the trial

**What the first trial showed.** Keeping a returning line's bars makes the bars return, and costs the words: the words' fit fell under the kept 10th. The engine's own refit seats the words and moves the bars.

**The idea.** Do both, line by line. For each line that returns, make both fits. Score each the way the engine already scores a refit: by where kept songs sing each syllable's weight in the bar and how long they give it. Keep the bars where the words sit as well as they do under the engine's refit; otherwise take the engine's refit.

Two forms, differing only in how much the words may give up for the bars:

- **Strict:** the bar fit is taken only where its words score is at least the engine's refit's.
- **One note's worth:** the bar fit is taken where its words score is no more than one moved note's charge below the engine's refit's (the charge the engine already sets on moving a note, 882).

**Trial, outside the engine.** `trial3.py` wraps `Engine.again`; nothing in `lib/luthier` changes. 150 tries a song, the same draws for each form. Read as sung (melismas placed, with 942).

**The check, on songs 55, 54 and 58** (song 59 read beside them, deciding nothing). A form passes if:

1. **Bars return.** The builds' median share of bars on a rhythm already sung rises in at least two of the three songs and falls by more than 0.01 in none; and bars on a figure already sung falls by more than 0.01 in none.
2. **The words hold.** The words' fit, whole, falls by no more than 0.02 in any song, and stressed syllables on a beat by no more than 0.03.
3. **No extra repeats.** The returning lines' repeated notes over the fresh lines' does not rise in songs 55 and 54.
4. **Builds survive.** At least nine tenths as many builds pass the gates.

If both forms pass, the one with the larger gain in bars is built. If neither passes, nothing is built.

Also reported, deciding nothing: the share of returning lines in which the bar fit was taken.
