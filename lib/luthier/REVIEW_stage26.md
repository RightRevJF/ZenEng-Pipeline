# Review 26: Luthier v40 and v41 (Windows 197 and 198)

20 November 2026. v40 (945, the lyric's room) and v41 (946 to 949) are merged into main at d498055.

## Reproduced

- The seven kept-table makers and `make_kept_rhythm_room.py`: byte for byte, with one exception. `make_kept_words_to_shape.py` rebuilds `kept_words_to_shape.json` without its `repeated_notes_by_family` block, which no script in the repo writes (749.131). The committed table was restored.
- Songs 52, 54, 55, 58 and 59, song 53's run, and stage 4: byte for byte.
- Song 60 on v41: byte for byte with `songs/p70/lyric60.v41.song.json`. The delivered record is untouched.
- `soundness.json` and `neighbour.json` (1,000 inner draws): byte for byte.
- `lyric_room.py` on all five lyrics: every verdict reproduces, but the readings move a little. The committed room files are v40's, read before 946 to 948 changed the builds. Song 55's bars unsung read 0.143 now against 0.124; song 60's 0.169 against 0.167 (749.132).

## v40 and v41

**The rhythm-memory study corrects my 749.123, and I accept it.** Slow change in how busy the singing is (+0.68) and bars with nothing sung (+0.58) carry rhythm scaling in kept songs; near or far repeats do not. The lyric's room check is the right place to catch it, because the words decide most of it. It has been added to the method at the lyric stage, beside the mouth tests. Song 60 reads in the kept middle half on all three readings.

**946 holds.** Kept lines now read as Luthier's do. Kept songs say a line again in 0.08, 0.32 and 0.52 of their lines (10th, middle, 90th), and Luthier's lyrics a little less. The held-out links are stronger (+0.58, +0.52, +0.42). Measured rightly, the builds already repeat about as much as the words ask, so the repetition ask needs no acting on.

**947 holds, with two cautions (749.133).** The rule tested three movements, and repeated notes passed at 2.2 shuffles in 100. Across three tests, a corrected bar would be 1.7. The soul and country families have 18 kept songs each. Taking the soul middle (0.207) whole moves song 60 a long way on 18 songs. A shrunk middle, part family and part overall, is the safer default until the families are larger.

**948 holds.** Song 60's join deaths fall from 791 to 0 and its survivors rise from 84 to 367; no other record changes.

**949 holds.** The neighbour range is now the pools' own: 3.0 in 100 (1.3 to 5.6).

**One new reading worth adding (749.134).** Under v41, song 58's verses sit on one note, E3, for 57 of every 100 sung notes, and song 60's verses (v41 record) on one note for 46. The longest run is only 6 in both, so the chant check (a run over 9.5) passes them. The share of a section's commonest pitch catches what the run misses; it needs kept quartiles and a rule.

**Range.** Song 58 is the widest gap: its words ask 19.9 semitones, and the pick spans 12 as sung (its builds 15), all its top notes in the bridge. It is the natural first case for planting the peak (749.111).

## Song 58, sixteenth edition

From the v41 record: A major, A2 to A3, 12 semitones as sung against an ask of 19.9. Rhythm scaling 0.558. All 44 document checks pass. The fifteenth edition is kept in `songs/p68/out/fifteenth_edition_v39/`.
