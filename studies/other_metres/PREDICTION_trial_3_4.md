# The 3/4 draw on the lead-sheet tables: a trial on song 53's words (27 Nov 2026; marks set down before any run)

Marks from the songwriting session (`coord/songwriting.md`, 11:15 ET), in its words where quoted. The writer's own 3/4 song (68, `songs/p78`) is reserved and is not run here.

## The form
`LUTHIER_TABLE_3_4=<table>` (unset by default): a 3/4 lyric's plan, draw and joint gate read the named kept table in place of Essen's `3-4_sung`. The lead-sheet table is `studies/other_metres/trial_tables/3-4_leadsheet_sung.json` with its rows beside it (538 Wikifonia lead sheets; `make_leadsheet_table.py`; kept out of `tables/`, since nothing is built). No gate lines are added. Everything else is the v53 engine as it writes 3/4.

## The lyric
`songs/p63/lyric53.json`, made from `lyric_locked.md` word for word: "Sung to Sleep", 3/4, 92 quarters a minute, genre folk, four verses each followed by the refrain, hymn mode off. The intake names no voice; the hand edition sat in E-flat with its top at E-flat5, so I set the voice to mezzo (57 to 77) and the lead to piano, and say so. Seed 1. 1,000 builds, both arms.

## Two arms, the same seed
Essen (the engine as it is) and Wikifonia (the switch).

## Marks
**The Wikifonia arm:**
- **T1.** "Living builds 30 or more in 1,000 and pool 10 or more."
- **T2.** The chosen tune's notes a bar inside Wikifonia's middle half (2.06 to 2.70).
- **T3.** Its onsets on a beat inside Wikifonia's middle half (0.731 to 0.939).
- **T4.** Its stressed syllables on the bar's first beat "no lower than Wikifonia's 25th": 0.583 (by song, 504 songs with 20 stressed syllables or more; `trial_tables/3-4_leadsheet_stress_by_song.json`, made before the run). Read on the tune as sung, one note a syllable.

**Against the Essen arm:**
- **T5.** Words' fit (the chosen tune's) no lower by more than 0.02.
- **T6.** The commonest pitch's share (verses pooled, refrains pooled), the range, and 959's leap "no worse than the Essen arm's": each share no higher by more than 0.02 (a margin, said now, so a tie in the third decimal is not a miss); the range no further under its floor; no leap past an octave in a line where the Essen arm has none.

**Reported, deciding nothing:** deaths by gate in both arms; each chosen tune's joint-gate distance against both references.

**Byte for byte:** with the switch unset, songs 54 and 55 written through are v53's records, and song 52 (6/8) its own.

## If it passes
"The Wikifonia tables become what a 3/4 lyric draws from, as a setting, with no gate lines." Then the writer's song 68 is the real test.

## What I expect
T2 and T3 met (the draw follows its table). T1 in doubt: in 6/8 the same engine keeps 22 builds in 1,000 and none passes the joint gate, and I do not know that 3/4 is better; Common Metre lines of 8 and 6 syllables against a table whose bars hold two notes may leave few windows. I put the trial passing whole at two chances in five.
