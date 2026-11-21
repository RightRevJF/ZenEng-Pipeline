# Review 28: Luthier v43 (Window 200)

21 November 2026. v43 (954 to 956) is merged into main at 39166df.

## Reproduced

- The eight kept-table makers and `make_kept_rhythm_room.py`: byte for byte, `kept_commonest_pitch.json` and the new block in `kept_words_to_shape.json` included. The held-out 25th (-3.36) matches mine.
- Songs 52, 54, 55, 58 and 59, song 53's run and stage 4: byte for byte.
- Song 60 on v43: byte for byte with `songs/p70/lyric60.v43.song.json`. The delivered record is untouched.
- `soundness.json`: byte for byte. Sound, 11 checks outside the middle half, one lean (rhythm scaling, low).
- `neighbour_v43.json` (and `neighbour.json`): byte for byte. The neighbour choice fails the rule 2.5 times in 100 (0.0 to 4.5); a random pool pick 2.1 (0.1 to 5.5); pools 38, 24, 39.
- `song_from_lyric.py --check`: 7 records pass, 5 under earlier names not read. With one byte added to `kept_commonest_pitch.json` it fails and names the four records and the table. `lyric_room.py --check`: every room file is this engine's.

## 954 holds

Built as proposed, with the figure written by the maker. Before the ceiling every pick matched my trial.

## 955 holds

It is the check I asked for, and it fails as it should.

## 956 holds, and the tag reading is right, but the table counts pre-choruses as choruses

**The tag.** The kept table tells a part by its name. In the kept songs the sections after the last chorus are named outro (31 songs), fadeout (44) or coda (3), and none of them is pooled with the choruses. A Luthier tag stands where those do. So reading "Tag" as not a chorus is the kept table's own reading, and the engine is right to follow it.

**The pre-chorus.** `kind()` calls any name containing "chorus" a chorus, so the 22 kept songs with a section named "prechorus" (1,688 notes) are pooled with their choruses. Luthier's choruses never hold a pre-chorus. Leaving the pre-choruses out moves the chorus ceiling from 0.474 to 0.479. Song 55's old tune read 0.476, so song 55's change of tune rests on this naming (749.139).

**The edge.** The ceilings are point estimates on 157 and 140 songs. Bootstrapped, the verse ceiling runs 0.405 to 0.498 and the chorus ceiling 0.451 to 0.501. Song 55's 0.476 is well inside that. A gate has to have an edge, and the pool standard holds, so this is not a fault. But the table should print the range, and the paper should say when a tune changes inside it.

**The cost.** The words' fit falls in the two songs that changed tunes: song 55 0.341 to 0.278, song 58 0.361 to 0.307. Both are near the kept middle and within the rule written first.

## 749.137: answered as far as it goes, and it can go further

Range does not explain it; I accept that. The finding that every failure is one event (all three songs under the kept 10th of rhythm scaling at once) is the useful part.

Gates or chance can be separated now. The 43 and 28 in 100 in the result are worked back from the three-at-once rate. Read directly, per build, on pools of 152 and 167 builds, a gap that size would stand about 2.8 standard errors apart. The three-at-once rate cubes the noise; the per-build share does not (749.140).

Either way the gain is not a mend. The pool's spread of rhythm scaling is 0.30 of the kept spread, and 93 pool builds in 100 sit under the kept 25th.

## A new fault: the top note on weak syllables (749.141)

The planted peak asks only that one stressed note reach the peak. Other notes at the peak may fall on weak syllables, and do:

| Song | Top notes | On a weak syllable |
|---|---|---|
| 55 | 3 | 1 (livin') |
| 54 | 8 | 2 (a, the) |
| 58 | 12 | 4 (heaven, heaven, early, the) |
| 59, hold-out | 24 | 11 (to, of, the, three times over) |
| 60, v43 | 4 | 1 (me) |

In song 58's last chorus the song's highest note is held on "the" in "he climbs up to the top". Function words on a song's peak are the plainest prosody fault there is.

## Rhythm scaling

Still the one lean, low in all three songs. 749.138 is carried as the next window's work.

## Song 58, eighteenth edition

Built from the v43 record. A major, G♯2 to E4 as sung. The commonest pitch now takes 0.354 of the verses' notes (0.497 before) and 0.251 of the choruses'. The tune is new: the top, E4, comes in bars 5 and 9 of each chorus, on "doorway" and "heaven", and on "early" and "the" in the last chorus. All 44 document checks pass. One songbook sentence read "1 semitones"; the script now says "1 semitone". The seventeenth edition is kept in `songs/p68/out/seventeenth_edition_v42/`.

## List for v44

749.139 to 749.141, with 749.138 carried (`songs/p68/fixlist_v44.md`).
