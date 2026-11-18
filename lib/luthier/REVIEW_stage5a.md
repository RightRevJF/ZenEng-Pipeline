# Review of stage 5a (Luthier v14, fixes 810 to 820), 18 November 2026

Branch `luthier-v8-stage1` at 49e542b, merged into main. Its merge of main predates the stage 4 review (REVIEW_stage4.md),
so 749.49 to 749.52 are new to the maintainer; stage 5a does not change them. Next free finding 749.53.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| `song_from_lyric.py songs/p64/lyric54.json 1000 12` | .song.txt and .song.json identical (key E, draft 3, pick 72899376ee39, 997 of 1000) | yes |
| `song_from_lyric.py songs/p65/lyric55.json 1000 12` | identical | yes |
| `song_from_lyric.py songs/p62/lyric52.json 1000 12` | identical | yes |
| 810 (749.47): `(z - a) or FLOOR(m)` | the fix as proposed; no `max(z - a, ...)` left in lib/luthier, chord_writer's charge included | yes |
| 811 (749.48): slurs counted | song 53's pick: at most two slurs in every line (verse 1, 2, 0, 0; refrain 1, 2, 1, 2) | yes |
| song 53 rerun (spec53.json, 3000) | identical: 2730 survivors, order c8b56170c542, pick 940f349cbf60, 0.109 | yes |
| song 52 rerun (spec52.json, 3000) | identical: 1308 survivors, order f4334c0710a7 | yes |

## Song 58 with song_from_lyric.py

Not run yet. Song 58 ("Same Time Tomorrow") is at draft 1 of its lyric; the writer locks the words and the mouth test runs before any
music, so the engine writes it after the lock. What a person types, read from the command and the three lyric files: the words, by
section, with section names that say which sections return; the title; and the five settings (metre, bpm, voice, lead instrument, mode),
with a seed. The lane (song 58: acoustic guitar, piano, upright bass, brushes, pedal steel late) has no input yet: the parts beyond
melody, chords and bass are stage 5b. The list will be confirmed, and anything else typed recorded, when song 58 is written.
