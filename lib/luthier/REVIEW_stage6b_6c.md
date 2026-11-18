# Review of stages 6b and 6c (Luthier v18 and v19, fixes 844 to 857), 18 November 2026

Branch `luthier-v8-stage1` at 55bbf7a, a fast-forward from main. Merged.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| `metre_engine.py songs/p63/spec53.json 3000 && hymn_parts.py songs/p63/spec53.json` | spec53.run.*, spec53.parts.json and .parts.txt identical | yes |
| `song_from_lyric.py` songs 54, 55, 52 (1000, 12) | .song.txt and .song.json identical, all three | yes |
| 855: every part on the tune's times | S, A, T, B: 65 notes each at the tune's onsets | yes |
| 852: no parallel perfect intervals | none in similar or parallel motion; one octave by contrary motion, soprano and bass at the join of refrain lines 2 and 3 (A to D, note 29 to 30), as hymnals allow at a line's join | yes |
| 852: spacing, crossings, chord tones | soprano to alto and alto to tenor never over an octave; no crossing; A, T, B always chord tones | yes |
| 852: motion against the tune within fifteen points | A contrary 0.02 against kept 0.13; T 0.13 against 0.24; B 0.40 against 0.34 | yes, at the edge for A |
| 857 (749.55) | the records rebuild byte for byte | yes, closed |
| 856 (749.56) | song 52's Chorus 2: nothing is lifted now; its lines move in eighths, so no note is a quarter long. Chorus 2 differs from Chorus 1 only where a melisma was added | yes, closed; 839 is idle on song 52 |
| 848: melismas at a line's end | 55 in 100 on song 54 against the kept 20, as Window 175 says | not met |

## 749.57 The descant's ceiling is read in the written key, not the sung one

**Problem.** `descant(top_limit=81)` caps the descant at A5 in the spec's key. Song 53 is written in D and sung in E-flat, with verse 4 and its refrain in F, and
the final refrain is where the descant is sung.
**Evidence.** The descant runs 73 to 81 written, so its summit sounds C6 in the final refrain (84), three semitones over the cap. The other parts stay inside their ranges after the move.
**Fix.** Give the spec the key it is sung in (or the transposition of each stanza), and read every range in sounding pitch.
**Check.** The descant's summit sounds at A5 or under in the key of the stanza it is sung over.

## 749.58 Rests between lines sit at the kept tenth percentile

**Problem.** 844 makes a quarter's rest the floor after a line, from the kept 10th percentile. The engine places the next line at that floor nearly every time.
**Evidence.** Rests between lines inside a section: song 54 34 of 49 exactly a quarter, song 55 30 of 49, song 52 28 of 28; median a quarter in all three, where
kept songs rest 15 at the 25th percentile and 24 at the median (`kept_line_endings.json`). Rest share inside sung sections: song 54 0.122 (0.181 on 6a, before 844),
song 55 0.167, song 52 0.13, all under the kept lower quartile of 0.21. 841 decided "no rule" before 844 moved these.
**Fix.** Draw the rest after a line from the kept rests (a floor of a quarter, then the kept shape above it), where the slot leaves room.
**Check.** The median rest between lines within the kept quartiles, and the rest share inside the kept middle half.

## 749.59 Melismas fall on function words

**Problem.** 848 places melismas on word-final syllables over notes a quarter long or more. It does not read the word, so short words get them.
**Evidence.** Melismas on function words: song 52 12 of 23 ("in" 6, "a" 4, "on", "and"), song 54 6 of 40, song 55 2 of 14. Song 52's Chorus line 5 has three
melismas in five syllables, on "there's", "a" and "in".
**Fix.** Measure the kept share of melismas on function words and weight 848 by it (or by the syllable's stress).
**Check.** The function-word share within ten points of the kept.
