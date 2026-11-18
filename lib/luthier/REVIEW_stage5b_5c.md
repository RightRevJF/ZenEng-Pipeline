# Review of stages 5b and 5c (Luthier v15 and v16, fixes 821 to 837), 18 November 2026

Branch `luthier-v8-stage1` at e8edb79, a fast-forward from main. Merged.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| `song_from_lyric.py` on songs 54, 55, 52 (1000, 12) | .song.txt and .song.json identical, all three | yes |
| 824 (749.49): `chord_writer.py && write_song.py ... && stage4_extras.py` | every key of stage4_results.json rebuilt; all but `song52_written` identical | yes, see 749.54 |
| 821 (749.52): spelling | G#m: B, C#m, D#, E, F#; D#m/Ebm and Bbm from their signatures; C#m: E, F#m, G#, A, B; `choose_key` offers C#m | yes |
| 823 (749.51): out-of-key share, my 40 songs | major median 0.093 (kept 0.068), minor 0.145 (kept 0.107): both within five points | yes |
| 822 (749.50): endings, my 100 songs a mode | first chorus on the tonic: major 39 (kept 36), minor 30 (kept 24). The 10-bar last chorus: major 54 (kept last sections 41), minor 39 (kept 31) | yes, inside 822's ten points in minor; major 13 over |
| 835: harmony voice by class, songs 54 / 55 / 52 | fourths 0.317 / 0.222 / 0.051 against kept 0.119; thirds 0.194 / 0.298 / 0.423 against 0.295 | not met for fourths, as the paper says |
| 832: no sung phrase over eight seconds | songs 54 and 55: none. Song 52 (6/8): 10, median phrase 12.2 s, longest 21.9 s | no, see 749.53 |

## 749.53 832 clips a line's last note to a sixteenth, and in 6/8 still leaves no breath

**Problem.** 832 shortens a line's last note to leave the least breath before the next line: `max(3, min(nx - on - BREATH, 24))`. Where the next line
starts less than a breath plus an eighth after that note begins, the note becomes a sixteenth (3 twelfths), often on the line's stressed rhyme word.
In 6/8 the next line often starts only a quarter after it, so even the sixteenth leaves 9 twelfths of rest, under the least breath and under the phrase check's 12.

**Evidence.** Line-final notes of a sixteenth: song 52 from its lyric 24 of 36 (13 stressed), song 54 18 of 58 (6 stressed), song 55 18 of 56 (14 stressed).
Song 52: 23 of 35 line joins rest under a quarter, all 9 twelfths, after fresh (9), again (11) and copied (3) lines; the phrase check reads 10 phrases over
eight seconds. The 4/4 engine (l11) chose line endings from the kept ending classes (525); the metre engine carries no such table.

**Fix.** Place the next line no earlier than the last note's least length plus the least breath (770's floor read from the last note's end, not its onset),
or let 832 give way by moving a fresh line later; and an ending's length from kept line endings.

**Check.** No line-final note under an eighth unless kept songs end there that way; no sung phrase over eight seconds in song 52.

## 749.54 The written-chords record is 5b's, not 5c's

**Problem.** `write_song.py` sets `clash_rule` on, so 833 changes its melodies. The committed spec52.written_chords.json and stage4_results.json's
`song52_written` were made before 833.

**Evidence.** The README's commands give the same twelve chord drafts and the same chosen draft (3), but every melody differs: draft 1 445 survivors
and 1.981 for the committed 457 and 2.016; the chosen draft's melody 1.886 for 1.953 (`review5c_written_chords_rerun.txt`).

**Fix.** Rerun and commit them under 5c.

**Check.** The README's commands rebuild both files byte for byte.

## Song 58

The README asks whether the harmony voice and the break read right in song 58. Its lyric is at draft 4 with the writer; the engine writes it after the
lock and the mouth test, and the answer comes then.
