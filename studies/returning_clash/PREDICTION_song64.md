# The copy and the melisma's second note on sealed song 64: marks set down before anything runs on it (749.223, 749.225)

26 November 2026. Form 1 passed clean and whole alone; form 2b passed its marks; the pair passed every mark on the seen songs (`RESULT_pair.md`). Marks proposed on the thread at 22:05 and agreed by the songwriting session at 21:25 by its clock, with mark 9 added and the margins of mark 6 accepted as written; its word to run is in that post. Song 64, "Go On Ahead" (`songs/p74/lyric64.json`), named for this by the songwriting session, never run by anything.

**The form, frozen:** `LUTHIER_COPY_CLASH=1 LUTHIER_MELISMA_CLEAR=after`, as on the branch at this commit.

**The run, once:** song 64 written through by v52 and by the pair, 1,000 builds each, the seed in the lyric file. Then each record's fitted spec, 1,000 builds, read as sung, for the builds' figures. Records kept here as `lyric64.v52.song.json` and `lyric64.pair.song.json`: test records, not the song made for the writer.

**Marks. All must hold for the pair to be built (fixes 966 and 967, defaults).**
1. **The pool** no smaller than 0.8 of v52's, and at least 10.
2. **The builds' middle words' fit** no lower than v52's by more than 0.02; the chosen tune at or over its floor.
3. **Clashes other than blue notes, per 100 notes, builds:** all clashes no more than v52's; in a copied line over another chord, and on a melisma's second note, each at most a quarter of v52's (met outright where v52 has under 0.05).
4. **The chosen tune's own long-clash count** (the record's check) no higher than v52's, and none on a melisma's second note.
5. **Bars on a figure already sung,** builds' middle, no lower than v52's by more than 0.03.
6. **Pitch scaling,** builds' middle, inside the kept 10th to 90th (0.667 to 1.107) and no further from 0.905 than v52's by more than 0.05; **surprise,** builds' middle, no further over 3.18 than v52's by more than 0.15.
7. **Melismas in 100 syllables,** builds, within one point of v52's.
8. **The chosen tune read alone on the soundness checks:** no more readings outside the kept 10th to 90th than v52's chosen tune plus one.
9. **Living builds** (the written records) no fewer than 0.9 of v52's.

**If v52 leaves fewer than 30 living builds on its fitted spec,** a mark that compares builds is read on the pair's figure alone against its fixed part, and the result says so.

**What I expect.** 3, 4, 7 met, near certain. 1, 2, 5, 6, 8 met. **9 is the one I would not bet on:** through the whole engine form 1 left song 58 with 314 living builds to v52's 366, which is 0.86; the mark was in the clean reading on the seen songs, where it held, and was not in the whole-engine marks. If song 64 has many copied lines over changed chords, as songs 55 and 58 do, its living builds may fall under 0.9 the same way. If song 64 has none, form 1 changes nothing and 9 holds trivially.

If any mark fails: neither form is built, song 64 is spent, song 65 is kept.
