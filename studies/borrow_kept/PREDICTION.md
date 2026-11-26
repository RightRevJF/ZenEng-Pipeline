# The borrow at the kept rate: a trial form, its marks written first (749.207)

26 November 2026. Seen before writing: `studies/line_repeats` (749.206: kept verse lines repeat a nearby line 11.5 in 100; the engine's borrow, 818, fires 0.8 and holds the height two lines back; with the borrow off that share falls inside the kept middle half), the ladder, and the list for v51's addenda 7 and 8. Nothing of this form has been run.

**The form.** Where a fresh line may sing the line two before (or the line before) again, the chance is the kept share of that part's lines that repeat one of those two lines, in place of the fitted 0.8. A verse takes the verses' share, a chorus the choruses', any other part the share over all parts. Table `tables/kept_line_repeat.json`, made by `lib/luthier/make_kept_line_repeat.py` with the repeat measure of `studies/line_repeats` (the strict one; the best of three alignments, addendum 8, is recorded beside it as a description). Switch `LUTHIER_BORROW_KEPT=1`, off; spec key `borrow_kept`, absent from every record. With it off, songs 54 and 55 byte for byte.

**Read two ways (749.179).** The clean reading: each v50 record's fitted spec, 1,000 builds, the form off and on (songs 55, 54, 58, 49, 50, 59; song 59 read, never fitted). The whole engine: the six songs written through, form on.

## Marks, clean reading (all must hold for the form to go to a sealed song)

Verses, the middle over builds, form on:
1. **Height two lines back:** the share of non-repeating verse lines within a step of the line two before, inside the kept middle half by song (0.167 to 0.51) in at least five songs of six. (v50: one of six.)
2. **Between-line spread** inside the kept middle half (0.863 to 2.377, `studies/ladder/kept.json`; the text first said 1.08 to 2.11 from memory, corrected 26 November on the list for v51, addendum 11: the file governs, as written) in at least four songs of six, and **the first notes' spread** nearer the kept middle than v50 in at least five.
3. **The share on the commonest pitch** lower than v50 in at least four songs of six, and verses over the 0.44 ceiling no more often than v50 in any song (a margin of 1 in 100), and **30 in 100 or fewer in songs 50, 58 and 49**.
4. **Bars on a figure already sung** (818's own purpose): the builds' middle no lower than the kept 25th in at least four songs of six. If it falls under in three or more, the form fails here whatever else it gains, and the result says the two kept counts pull against each other.
5. **Clashes** (a note a beat long or more, off the chord and a semitone from a chord tone), per 100 notes, no more than v50's plus 0.2 in every song. **On-beat chord tones** no further from kept 0.64 than v50's in at least five songs.
6. **Living builds** in 1,000 no fewer than 0.9 of v50's in every song.

## Marks, whole engine

7. Soundness of the three (55, 54, 58) holds; the pool pick by `neighbour.py` 6.5 in 100 or under; pools no smaller than 0.8 of v50's (25, 22, 24).
8. The words' fit within 0.02 of v50 in every song; range floors and the planted peak's range kept.
9. **Song 50's pool 10 or more** (v50: 5).
10. Surprise at or under the popular-corpus median, and the two scaling readings no worse than v50 by more than their run-to-run spread, in at least five songs of six.

## What I expect

Marks 1, 2, 3 and 6 met. **Mark 4 is the one I think most likely to fail**: 0.8 was raised from 0.6 in fix 919 exactly so that bars on a figure already sung would meet the kept median, so taking the chance down to about 0.12 should lose some of it; my guess is the builds' middle falls from near 0.47 to 0.35 to 0.40, and whether that clears the kept 25th I do not know. Mark 9 I put at even odds.

If the clean marks are met, the writer is asked to name a sealed song (64 or 65). If mark 4 fails alone, the next reading is what "sing it again" changes: a true repeat at the kept rate may hold both counts where an altered one at 0.8 holds only one.
