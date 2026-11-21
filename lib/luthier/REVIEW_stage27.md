# Review 27: Luthier v42 (Window 199)

21 November 2026. v42 (950 to 953) is merged into main at 6df7ef6.

## Reproduced

- The seven kept-table makers and `make_kept_rhythm_room.py`: byte for byte, `kept_words_to_shape.json` included. 952 mends 749.131.
- Songs 52, 54, 55, 58 and 59, song 53's run and stage 4: the music byte for byte. Each of songs 54, 55, 58 and 59 differs in one line: the record names the words-to-shape table it read as `b243b89e5d`, the table before 952 added the shrunk family middles. The table now in the repo hashes `53edc7875f`. The records were written at d9b7493 and not rewritten after 39e385e changed the table. Only song 60's asking moves with that change, so the notes are right and the stamp is stale (749.136).
- Song 60 on v42: byte for byte with `songs/p70/lyric60.v42.song.json`. The delivered record is untouched.
- `soundness.json` and `neighbour_v42.json`: byte for byte. The neighbour choice fails the rule 1.5 times in 100 (0.1 to 2.9); a random pool pick 2.7 (0.6 to 5.0).
- `lyric_room.py --check`: every room file is this engine's. 953 mends 749.132.

## 950 holds

Planting the peak as a note, one fresh chorus line at a time, is the right shape of fix, and the six trials show how it was found: the fourth found that builds die at 838 (the chorus's lift), and the fifth stopped the planted line's centre moving. The builds' middle range rises to 17, 15, 17, 17. The top now sits in the choruses, where Window 196 found kept songs put it 75 times in 100. Song 58 shows it plainly: its top, E4, comes six times, all in choruses, where under v41 every top note was in the bridge.

The cost is fewer builds living (342, 309, 419, 376), still over the floor the trials set.

## 951: a fair use in kind, a judge in degree

The maintainer asked whether 951 is a fair use of the asking or a judge by another name. My answer is both. It depends on how tight the band is.

**Fair in kind.** The asking is fixed from the words before any build is made. It does not say one tune is better than another, and 872 still orders the builds that meet it. Reading a song's own target is not a new judge.

**A judge in degree.** The words predict range with a held-out error of about 5 semitones (sd 4.99, held-out rank correlation 0.418). Only 35 kept songs in 100 land within 2 semitones of what their own words ask (`studies/review27_range_spread`). After 951, all five of Luthier's chosen tunes do. Their spread around the asking is sd 0.73 against kept songs' 5. So the choice treats a loose prediction as an exact target. In song 54 it also buys range with another reading: the words' fit falls from 0.282 to 0.163, just over the floor of 0.152. Trading one reading against another, with nothing to say range matters more, is what a judge does.

**What 951 was for.** It was meant to fix a bias, not set a target. Under 872 alone the chosen tunes ran short of the asking on average (mean -2.9, song 58 at -8.9, past the kept 10th of -6.5). So I tried a floor in place of the band: the first build whose range is at least the asking less 3.36 semitones, the kept 25th of range less the asking. Above the floor, 872 decides.

| Song | Asking | 872 alone | 951 | Floor | Words' fit: 872, 951, floor |
|---|---|---|---|---|---|
| 54 | 18.8 | 14 | 17 | 16 | 0.282, 0.163, 0.275 |
| 58 | 19.9 | 11 | 19 | 19 | -, 0.361, 0.361 |
| 55 | 18.0 | 17 | 17 | 17 | 0.341, 0.341, 0.341 |

Songs 60 and 59 are unchanged by either rule: the first build already spans 19. The floor is sound on songs 55, 54 and 58, with 11 checks outside the middle half against 951's 15. Song 54 keeps nearly all its words' fit for one semitone less. I recommend the floor (749.135).

## 952 holds

The maker writes the family middles, the engine stops when one is missing, and the shrunk middles (soul 0.232, country 0.329, others 0.319) answer 749.133. Only song 60's asking moves.

## 953 holds

Every room file names its engine and tables, and `--check` passes. The song records need the same check (749.136).

## The pools grew sounder, and why is untraced

The neighbour choice fails 1.5 times in 100 against Window 198's 3.0, and a random pool pick 2.7 against 8.2. One likely cause: under v41 the builds spanned 14 or 15 against the kept middle of 17, so range leaned low in many pool members. The planted peak moves them to the kept middle. Leaving range out of the rule and rereading the pools would show whether that is all of it (749.137).

## The commonest pitch (749.134)

The study's rule was written first, and it confirms the fault. Songs 54 and 58 are over the kept 90th in the verse, songs 55 and 58 in the chorus. I agree the ceiling should be tried against the pool standard before it is built. Note that a wider range did not spread song 58's verse: it sits at 0.497 at 19 semitones as at 12.

## Rhythm scaling

Rhythm scaling is still the one check leaning past the quartiles, low in all three songs (song 58: 0.557 against a kept 10th of 0.574). The lyric's room check measures the cause and the engine does nothing with it yet. It is the largest remaining gap (749.138).

## Song 58, seventeenth edition

Built from the v42 record: A major, A2 to E4, 19 semitones as sung against an ask of 19.9. The words' fit is 0.361. The top note, E4, comes six times, all in choruses. All 44 document checks pass. The sixteenth edition is kept in `songs/p68/out/sixteenth_edition_v41/`.

## List for v43

749.135 to 749.138 (`songs/p68/fixlist_v43.md`).
