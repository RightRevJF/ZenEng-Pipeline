# Review of Luthier v23 (fixes 885 to 889) and v24 (fixes 890 to 898), 18 November 2026

Branch `luthier-v8-stage1` at 4a35e99 (main merged in). Reviewed together; merged into main at cc03065.
The paper: `reports/Luthier_v24.docx` (read as Markdown in `src/`, not committed).

## Reruns (PYTHONHASHSEED=0, on the branch head)

| Command | Result | Held? |
|---|---|---|
| `song_from_lyric.py songs/p68/lyric58.json 0` (894, intake) | 57 lines, 114 bars at 84 = 326 s; "about 14 fewer two-bar lines, or about 113 beats a minute"; writes nothing | yes |
| `song_from_lyric.py` songs 58, 55, 54, 52 (1000 12) | .song.json and .song.txt identical, all four (song 58 131 s) | yes |
| `mkspec52.py` + `metre_engine.py spec52.json 3000`; `mkspec53.py` + `metre_engine.py spec53.json 3000` + `hymn_parts.py`; `chord_writer.py`, `write_song.py`, `stage4_extras.py` | identical | yes |
| `cocopops_parse.py` on CoCoPops Billboard, then `make_kept_word_weight.py` and `make_kept_returns.py` (895) | `tables/kept_word_weight.json` and `tables/kept_returns.json` rewritten byte for byte (749.70 closed) | yes |
| Every .py in lib/luthier compiles | yes | yes |

The parser merges tied notes (`tie_cont`), so the kept last-note lengths are whole notes, not halves cut at the bar line. Checked before reading 887.

## 887, checked hardest: a line's last note takes a kept length

What holds. Rests between lines of a section, median: 24 twelfths in songs 54, 55 and 58 (kept median 24); exactly a quarter 10 of 49, 11 of 49, 11 of 50 (were 25, 30, 24). Rest share 0.292, 0.333, 0.236, inside the kept middle half (0.21 to 0.39). So 749.58 is closed in 4/4. Song 52 (6/8) is unchanged at 12.

What does not. 887 draws the last note's length from the kept shares, but only among lengths that leave a quarter's rest before the next line. In a two-bar slot the long kept lengths rarely fit, so they drop out and the short ones take their share. The rest reached the kept median by taking time from the held note. Line-final notes (lines ending without a melisma, the last syllable's own length, as the kept table counts them):

| | stressed: an eighth or less | stressed: a half or more | weak syllable: an eighth or less | function word: a half or more |
|---|---|---|---|---|
| kept (159 songs) | 0.22 | 0.31 | 0.40 | 0.22 |
| song 54 | 0.29 | 0.29 | (none) | 0.08 |
| song 55 | 0.54 | 0.03 | 0.60 | 0.00 |
| song 58 | 0.44 | 0.11 | 0.85 | 0.00 |

Kept songs hold the line's last word and still rest; the engine now does one or the other. This is 749.76.

## 892, checked hardest: the guitar in its own register

What holds. The guitar is voiced in its kept register and kept off the seconds either side of the sung note. Sung notes with the chordal part sounding under them: song 55 0.973, song 58 0.917 (were 0.03 and 0.01); none a second away in any song; the voicings inside the low-interval limits; roughness at sung onsets in song 58 0.675 / 0.912 (0.675 / 0.918 before). Song 58 is a different record: the verses have the guitar under the voice, and the band-only energy reads each chorus above its verse and the last chorus highest (0.73), so 9.12 is met.

What does not.
- **Song 54: the guitar is silent under 173 of its 503 sung notes (0.656).** None fall in a strum's own gap: they are bars where no voicing passed. The missing notes sit on C4, B3 and D4 (49, 49, 41 of them): with the seconds either side of a sung note inside the guitar's register (C3 to G4) struck out, no three-note voicing of the chord is left, and the fallback (under the tune) has no room either. This is 749.79.
- The check from 749.21 is still printed as if it applied: "sung notes with accompaniment above them" reads 0.441, 0.973, 0.917 against a rule (2 in 100 at most) that was measured on piano Lieder. There is no kept figure for a guitar.

## The other fixes

| Fix | Check | Reading | Held? |
|---|---|---|---|
| 885 length in the place score | builds' fit by length near the kept 0.13 | picks 0.121 (54), 0.16 (55), -0.035 (58) | builds yes; song 58's pick no (749.81) |
| 886 line-end melismas | near the song's own kept figure | 30 (kept for its line ends 29), 36 (35), 32 (32) | yes |
| 888 a long song loses the turn and takes short edges | seconds | 298, 240, 326; song 58 now 2 bars in, 4 out, no turn | yes; song 55's flags print "888: no turn" twice |
| 889 the harmony voice fitted to the kept shares | fourths near 0.119 | 0.150, 0.106, 0.116; harmony_fit misses 0.156, 0.081, 0.119 | yes |
| 890 871 for a word of any length | no weak last syllable held longer | song 58 0 of 14 ("completely" mended); song 55 1 of 6, "summers": stressed 3 twelfths, weak 6 (v22: 0 of 6) | no for song 55 (749.78) |
| 891 a stressed syllable left a sixteenth is charged | in lines sung again at or under the song's other lines | 54: 14 of 131 against 5 of 82; 55: 12 of 79 against 11 of 73; 58: 6 of 72 against 9 of 111 | 55 and 58 yes; 54 no (749.77) |
| 893 the harmony voice E2 to A5 | no note under E2 | lowest 40, 45, 40, 48; above the lead once (song 54) | yes |
| 894 one length, and the intake | flag and check agree | song 58: 326 and 326 | yes |
| 895 makers in the repo | tables byte for byte | yes (above) | yes |
| 896 kept returns measured | engine inside the kept quartiles | other-count lines keep, of their source's rhythm, 0.81 / 0.82 / 0.82 (kept 0.57, 0.68, 0.81) and of its pitches 0.82 / 0.80 / 0.74 (kept 0.63, 0.79, 0.89): pitch inside, rhythm at the kept 75th | yes |
| 897 `gates_removed` | recorded | old charge 319 / 404 / 352; joint 0; words 0 | yes |
| 898 one fit, one set of figures | judge and checks agree | song 58: 0.281 and 0.281; the docstring gives both measures, named | yes |

## Breaths, read again (887 moves where breaths fall)

`studies/breath/luthier_breath.py` (onsets) and the new `studies/breath/silences.py` (durations). Real breaths by onsets, a minute: song 58 7.6 (v22 6.1), 54 9.7, 55 7.4; human median 7. By durations, silences of a beat or more per 100 beats of the sung span: 54 12.3, 55 14.0, 58 13.0 (v22 12.1, 13.3, 12.7); CoCoPops Billboard quartiles 7.0, 9.1, 11.1 (205 songs). The median silence is now 2.0 beats in songs 55 and 58 and 2.5 in 54 (v22 1.0 in all three); CoCoPops median 2.0. So the breaths are now as long as a human singer's, and more frequent: the voice stops after nearly every line, where kept singers run some lines on (749.80). The breath-on-the-grid reading (749.65, not held out) asks for nothing.

## 749.75

Not built in v24 (POP909's last chorus is no denser than its first). Kept evidence of another kind is in `studies/last_chorus/` and the fix list for v25; and song 58 under v24 meets 9.12 as it stands (above).

## New findings

749.76 to 749.81, in `songs/p68/fixlist_v25.md` and its Doc.
