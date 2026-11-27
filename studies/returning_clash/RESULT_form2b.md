# Form 2b, the melisma's second note cleared after the pick: the result (749.225)

26 November 2026. Marks in `PREDICTION_form2b.md`, committed before any run. `clean2b_a.json`, `clean2b_b.json` (each v52 record's fitted spec, 1,000 builds, read as it will be sung); `form2b_records.json` (the six songs written through with `LUTHIER_MELISMA_CLEAR=after`, against their records).

**All five marks are met.**

| | 55 | 54 | 58 | 49 | 50 | 59 |
|---|---|---|---|---|---|---|
| B1. Clashes on a melisma's second note per 100 notes, builds, v52; 2b | 0.42; 0 | 0.30; 0 | 0.43; 0 | 0.34; 0 | 0.57; 0 | 0.51; 0 |
| B1. In the chosen tune, v52; 2b | 1; 0 | 1; 0 | 2; 0 | 0; 0 | 6; 0 | 0; 0 |
| B5. All clashes per 100 notes, builds | 1.10; 0.68 | 0.56; 0.26 | 0.62; 0.18 | 0.64; 0.30 | 0.57; 0.00 | 0.57; 0.06 |
| B4. Melismas in 100 syllables, builds | 8.49; 8.47 | 7.60; 7.59 | 5.38; 5.34 | 4.23; 4.21 | 8.56; 8.52 | 7.41; 7.37 |
| B4. Of them at a line's end | 0.313; 0.313 | 0.241; 0.241 | 0.343; 0.339 | 0.274; 0.274 | 0.261; 0.261 | 0.180; 0.180 |
| In the chosen tune: second notes raised; melismas dropped | 1; 0 | 1; 0 | 1; 1 | 0; 0 | 6; 0 | 0; 0 |

- **B1 met:** none left, in the builds or in any chosen tune.
- **B2 met:** every written record has v52's chord plan, pick, pool and living builds, and v52's note on every syllable's first note. What differs is the melody's melisma notes and what follows from them (the checks, and in three songs the parts and harmony that track the tune).
- **B3 met:** the three are sound, with the one lean past a quartile (rhythm scaling low), as v52. Their rhythm scaling as sung: 0.604, 0.562, 0.568 (v52 0.604, 0.562, 0.566).
- **B4 met:** the share falls by 0.04 of a point at most. Nearly every clashing second note can take the step above; in the six chosen tunes, nine are raised and one melisma is dropped.
- **B5 met.**

**What form 2b is, beside form 2.** The same mend of the same notes, without touching the draw of melismas or what the engine reads when it chooses. So nothing else moves, and the miss of form 2 (a changed pick in song 55 landing on the edge of the rhythm-scaling line) cannot arise.

**Form 1 with form 2b** has not been run together. Form 1 changes builds and so the pick in some songs; form 2b then clears whatever tune is chosen. Each has passed alone.

**A slip of mine, found by the byte-for-byte check and mended before this was committed.** In adding the switch I put a comment in the middle of a line of `melismas()`, which cut off the two statements after it: the record's `melisma_share_drawn` and `melisma_line_end_share_kept_for_this_song` were not written. Notes were not affected (the statement that sets them came before the comment), so the six written records above have the right notes and lack those two fields; the 1,000-build readings do not pass through that line. With the comment moved to the line's end, songs 54 and 55 written through with the switches off are byte for byte v52's. It is the second time I have made this slip (749.184), so from now on a comment goes on its own line or at a line's end, never inside one.
