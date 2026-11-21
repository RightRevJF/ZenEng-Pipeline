# The shape from the song (944): result

Rule in PREDICTION.md, written before the full runs. Song 59 read, never fitted to.

**What changed.** No kept song is drawn. Range from the song's own words (`tables/kept_words_to_shape.json`); steps, leaps, repeated notes, longest run and melismas at the kept middle, with a writer's override (`"movement": "smooth" | "leaping" | "chant"` in the lyric file); the chorus's lift at the kept middle.

**The theory tested first (`sections.py`, PREDICTION_sections.md).** On 137 kept songs: the verse steps more than the chorus in 44 in 100; the chorus leaps more in 44 in 100. Neither holds; kept songs move the same way in verse and chorus. The chorus's top is at or over the verse's in 75 in 100: that holds.

| Check | Result |
|---|---|
| 1. The picks pass the soundness rule | Met (1, 2, 8 checks of 23 outside the kept middle half) |
| 2. The pools no worse than the top of v37's ranges | Neighbour choice 1.5 in 100 (0.5 to 5.5): met. Random pool pick 7.8 (4.1 to 11.4) against a line at 6.1: **not met**; inside the standard's bar of ninety passes |
| 3. Movement within a quarter width of the kept middle in three songs of four | Met in four |
| 4. Range within 3 semitones of the words' asking in three of four | Met in three (song 54: 14 against 17.3) |

**Kept all the same, and why.** The change was made because the writer ruled that the engine may not take its shape from one other song. The rule says what that costs: the random pool pick is worse. The cause is one check. With the draw's scatter gone, all three songs stand low on rhythm scaling together (builds 0.59, 0.57, 0.55, 0.68 against kept quartiles 0.61, 0.66, 0.72). `SHAPE_FROM = "a kept song"` restores the draw and v37's records.

**Repetition from the words: tried, not acted on.** The borrows fitted to what each song's words ask (`own_with_borrows_from_words.json`, `neighbour_with_borrows_from_words.json`): the builds moved toward the asking, and the pools broke again (neighbour choice 5.2 in 100, random pool pick 10.3). The borrows stay at 0.8 and 0; the words' asking is in the record.

**Next.** Rhythm scaling is low in every Luthier song. The session's 749.123 names the likely cause: Luthier repeats by whole sections from far back; kept songs repeat nearby.
