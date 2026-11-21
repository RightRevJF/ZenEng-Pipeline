# The shape from the song: the rule for adopting the redesign, written before the full runs

**The change (944).** Luthier stops drawing one kept song and taking its numbers. A song's shape comes from the song:

- how much it repeats, and how wide it ranges: from its own words, by the link found in the kept songs as a body (studies/words_to_shape, tested on songs held out);
- the chorus's lift over the verse: the kept middle (the paper's "the top is the chorus's", which holds in three kept songs in four; `sections.py`);
- how it moves by step, by leap and by repeated note: the middle of what kept melodies do. The paper's rule that verses step and choruses leap was tested and does **not** hold in kept songs (`sections.py`: each in 44 songs in 100), so it is not built; the paper's invariants (Module 0.4: every melody's steps and leaps fall in one band) are the theory that stands. The writer may ask for smooth, leaping or chant; the default is the engine's.

**What must hold for it to be adopted,** on songs 55, 54 and 58 (song 59 read beside them, never fitted to):

1. The picks pass the soundness rule.
2. The pools hold: the neighbour choice and the random pool pick each fail the rule no more often than the top of Window 194's 90% range (3.5 and 6.1 in a hundred).
3. Movement lands where the engine put it: in at least three of the four songs, the builds' median shares of steps, leaps and repeated notes are each within a quarter of the kept middle half's width of the kept middle.
4. Range follows the words: in at least three of the four songs, the builds' median range is within 3 semitones of what the words ask.

**A second step, judged apart: repetition from the words.** The two borrows fitted to what the song's own words ask for bars sung again (943's fit, now aimed at the song and not at another song). It is adopted only if 1 and 2 still hold with it, and the builds move nearer the words' asking in at least three of the four songs. Window 195 found that more borrowing lowers rhythm scaling and broke the pools; if it does so again, the borrows stay as they are and the words' asking is recorded but not acted on.

**Expected and not a fault.** Without the draw the four songs will be more alike in shape, because their lyrics are alike in size and in how much they repeat. The paper's own finding (Module 0.4 amended, Window 68) is that the repertoire keeps the typical. The count of checks on which a song stands outside the kept middle half is reported, and is not a test.
