# Review of stage 6a (Luthier v17, fixes 838 to 843), 18 November 2026

Branch `luthier-v8-stage1` at 423a651, a fast-forward from main (5b and 5c were merged at b36129e). Merged.
The branch was cut before the 5b/5c review, so 749.53 and 749.54 are new to the maintainer; 6a leaves them as they were.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| `song_from_lyric.py` songs 54, 52 (1000, 12) | .song.txt and .song.json identical | yes |
| `song_from_lyric.py` song 55 | .song.txt identical; .song.json differs in one reading only, see 749.55 | partly |
| 838: the pick's lift within two of the plan | song 54 plan 2, lift 3; song 55 plan 0, lift -1; song 52 plan 0, lift 1 | yes |
| 839 (749.8): no later chorus the same as the first in every bar | song 52's Chorus 2 lifts lines 1 and 4 (60 to 62 on "falls", 60 to 64 on "wall"); line 0 and the title line apart | yes, see 749.56 |
| 840: the title on the beat | song 54 0.25 against kept 0.73, as the paper says | not met on song 54 |
| 749.53 on 6a's records | line-final sixteenths: song 54 14 of 58, song 55 14 of 56, song 52 23 of 36; song 52 still has 10 phrases over eight seconds | open |

## 749.55 Song 55's committed record reads a lift its own gate would refuse

**Problem.** The committed lyric55.song.json prints the chorus's lift as -2.5 semitones; the committed code reads the same notes as -1.0 (as stage6a_results.json says).
**Evidence.** The rerun differs from the committed record in that one reading. A lift of -2.5 against the plan's 0 would fail 838's gate (within 2), which the pick passed.
**Fix.** Rewrite the record with the committed code.
**Check.** The README's command rebuilds lyric55.song.json byte for byte.

## 749.56 839 lifts a "held" note that 832 has cut to a sixteenth

**Problem.** 839 picks the held note by the gap to the next onset, so it takes a line's last note; 832 has often made that note a sixteenth (749.53).
**Evidence.** Song 52's Chorus 2: both lifted notes ("falls", "wall") are 3 twelfths long. The rule I proposed (vary68) lifted a held note, one long enough to hear.
**Fix.** Read "held" from the note's sung length after 832, or mend 749.53 first.
**Check.** Every lifted note is a beat long or more.

## Fixes 844 and 845 (c762df8), merged the same day

| Check | Result | Held? |
|---|---|---|
| `song_from_lyric.py` songs 52, 54, 55 (1000, 12) | .song.txt and .song.json identical, all three | yes |
| `metre_engine.py songs/p62/spec52.json 3000` | identical: 2506 survivors, order d609db9d0ac1, pick 36cf66ee1827 | yes |
| 844 (749.53) on songs 55 and 52 | no line-final note under an eighth (shortest 6), no join under a quarter's rest, no phrase over eight seconds (song 52 median 3.7 s, longest 4.8) | yes, 749.53 closed |
| 845 (749.54) and 749.55 | the records are made again; song 55 now reads its lift -1.0, as its gate does | yes, both closed |
| 749.56 after 844 | song 52's Chorus 2 lifts "falls" (an eighth now) and "wall" (a half) | partly: one lifted note is still short |

Song 52's hand spec still carries the retired gate "the chorus above the verse" (370 deaths). It is the hand spec's record, so I leave it.
