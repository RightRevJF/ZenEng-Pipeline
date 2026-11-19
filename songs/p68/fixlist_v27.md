# Luthier fix list for v27 (since v26)

18 November 2026. Luthier v26 (fixes 904–906) is reviewed (`lib/luthier/REVIEW_stage13.md`) and merged into main at c476c45. The parser, the four makers that run here and every song record reproduce byte for byte. Song 58 is rebuilt from its v26 record in A (fourth edition; 44 of 44 document checks pass). Six new findings (749.84 to 749.89), one carried (749.61). Next finding 749.90; next fix 907.

## The v26 list against the v26 records

| Finding | Fix | Closed? |
|---|---|---|
| 749.82 tie starts | 904, 905 | yes: the parse matches the session's tie-aware parse note for note; the tables rebuild byte for byte; records carry their tables' fingerprints |
| 749.83 phrase check | 906 | yes as a print: split at half a beat, the kept 0.042 beside it. What it shows is 749.88 |
| 749.61 6/8 | none | carried |

## The session's studies, checked for ties

Only two read a parse that dropped tie starts: silences and last chorus (both read `corpora/cocopops_notes.csv.gz`). Ornament (848), slots (869), degrees (846), hooks (the 0.73 behind 840) and breath by onsets each parse the corpus themselves and read tie starts. Phrases was always run on the tie-aware parse. Rerun on the mended corpus: kept silences of a beat or more per 100 beats 7.0 / 9.1 / 11.1 become 6.7 / 8.5 / 10.4; the last chorus still runs longer and louder than the first, and no higher. No conclusion changes. Table in `REVIEW_stage13.md`.

## New findings

### 749.84 The chorus lift is one draw from the kept lifts, clamped to the voice
**Problem.** The plan's lift is one draw from `register_plan.json`'s 121 kept lifts. A draw past the voice's room (`V[1] - V[0] - 12`) is clamped to it, so every lift past the room lands on the room itself. The key is then chosen to fit the span. Song 58 drew the kept tail and its key moved from C to A, with the verses at the bottom of a baritone.
**Evidence.** Kept lifts: quartiles 0, 1, 4; 90th 6; 8 or more in 8 of 100. Draws: song 54, 11 (tenor, clamped to 9); song 55, 5; song 58, 12 (baritone, clamped to 9). The choruses' median over the verses': 54, 8 semitones; 58, 10 (kept quartiles 0, 1, 4). Song 58 now sings G♯2 to D4 in A: the verses G♯2 to E3, centred on B2, six semitones under the middle of a baritone's G2 to E4. Under v25 it was in C.
**Fix.** Draw from the kept lifts the voice has room for (drop the rest, then draw), so the clamp never piles draws on one value. Then choose the key so the verse's centre sits near the voice's middle, not its floor.
**Check.** Over 200 seeds a voice's lifts follow the kept lifts within its room, with no pile at the room. Song 58's verse centre is within three semitones of the baritone's middle.

### 749.85 The pick's words fit sits low among its own builds
**Problem.** The words' gate (881) passes any build at the kept 10th or better, and the pick is the first build in order past the gates. So the pick's fit falls wherever it falls above 0.152, often far below most of its builds. Melismas (848) then take a little more from it, as they do in kept songs.
**Evidence.** Fit recomputed with each melisma's two notes joined, then as sung (898):

| Song | Builds' fit quartiles | The pick, melismas joined | The pick as sung | By length, as sung |
|---|---|---|---|---|
| 55 | 0.270, 0.314, 0.350 | 0.254 | 0.243 | 0.288 |
| 54 | 0.241, 0.281, 0.321 | 0.217 | 0.187 | 0.093 |
| 58 | 0.327, 0.381, 0.420 | 0.208 | 0.162 | −0.017 |

Kept, ties read: 10th 0.152, quartiles 0.248, 0.318, 0.402; by length, median 0.209. Three in four of song 58's builds fit their words better than the median kept song. The pick fits worse than nearly nine kept songs in ten, and on length the weightier syllables get the shorter notes. A kept melisma's first note is 0.44 of its span at the median (3,737 melismas); the engine's half is in line, so the melismas are not the fault.
**Fix.** Measure the gate on the notes as sung (after 848), and raise it to the kept 25th (0.248). Or, among builds past the other gates, take the first in order at or above the builds' median fit.
**Check.** Each 4/4 pick's fit as sung sits in the kept middle half, and so does its fit by length.

### 749.86 `register_plan.json` cannot be remade from the repo, and it now sets the key
**Problem.** `kept_plan.py` imports `common` from `/home/claude/zeneng/corpus/nine`, which is not in the repo. 905 fingerprints the table, but no one else can rebuild it. As 749.84 shows, it decides the lift, and through the lift the key. `kept6a.json` at the repo root is its stray output.
**Evidence.** `python3 lib/luthier/kept_plan.py`: `ModuleNotFoundError: No module named 'common'`. Every other maker reproduces its table here byte for byte.
**Fix.** Move what `kept_plan.py` needs into the repo (reading `kept_corpus`), and drop `kept6a.json`.
**Check.** `kept_plan.py` writes `register_plan.json` byte for byte on a fresh clone.

### 749.87 The 4/4 maker on the old parse does not quite give back `surprise_quartiles`
**Problem.** The README says `make_kept_4_4_tables.py` "reproduces the old tables from the old parse". It does for every field but one.
**Evidence.** On main's parse: main [2.73, 2.956, 3.146], remade [2.741, 2.963, 3.152]. The `source` text differs, as expected.
**Fix.** Find the step that differs (a smoothing constant, a song list or a rounding), or note it in the README.
**Check.** The old tables come back byte for byte, or the README names the one field.

### 749.88 Phrases run long in all three 4/4 picks, and 906 only prints it
**Problem.** With breaths read at half a beat, as kept singers take them, the picks' phrases over 12 beats run at about twice the kept share. Their longest phrases sit at or past the kept 75th. Nothing steers it: 899 draws each line's rest alone, so run-ons can chain.
**Evidence.** Over 12 beats: 54, 0.057; 55, 0.082; 58, 0.077 (kept 0.042). Longest, in beats: 13.2, 15.5, 15.0 (each kept song's longest by quartile: 8, 12, 15.5). `studies/breath/phrases.py` agrees (kept 0.046 on its wider, unclipped count).
**Fix.** When 899 draws a line's rest and the phrase running into it is already past 8 beats, draw from the kept rests of half a beat or more.
**Check.** Each 4/4 pick's share over 12 beats is at or under 0.06, and its longest phrase is at or under the kept 75th (15.5 beats).

### 749.89 Two of the constants listed as not rebuilt, recounted
**Problem.** The README lists ENTRY (771), the 731 and 840 thresholds, WORD_PITCH (847), ONE_BAR (876) and the 877 counts as not rebuilt. Two can be recounted from the mended notes table.
**Evidence.** `studies/kept_checks/silence_counts.py`, one definition on both parses. 877: silences of two bars or more number 1, 2, 3 per song by quartile, unchanged. 876: a silence of one bar to two, per eight bars, median 0.386 old, 0.35 with ties read (about a tenth less). The 0.73 behind 840 comes from a tie-aware parse and stands. ENTRY and WORD_PITCH need the stress spine, which the notes table does not carry.
**Fix.** Keep 877. Lower ONE_BAR by a tenth (0.1 to 0.09), or recount it by its own definition. Give 771 and 847 makers that read the hum files with the 904 rule, so they can be rebuilt like the rest.
**Check.** Each constant has a maker, or a line in the README saying where it came from and that it was checked against the mended parse.

## Carried
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known not met (the paper's own)
Songs 54 and 58 past the kept lengths (the lyrics). Song 58's rest share inside sung sections 0.278, near the kept 75th (0.33).

## Order of work
1. 749.84 and 749.85 (what a listener hears first in song 58: verses at the bottom of the voice, words on the wrong notes). 2. 749.88. 3. 749.86, 749.89. 4. 749.87. 5. 749.61.

## Songs

| Song | Folder | Under v26 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 326 s; key A (was C); lift 9; fit as sung 0.162; fourth edition rebuilt from this record |
| 55, Your Yard Man | p65 | 240 s; key C; lift 5; fit as sung 0.243 |
| 54, The Man Mama Prayed I'd Be | p64 | 298 s; key D (was G); lift 9; fit as sung 0.187 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, and the six kept tables: byte for byte, or the fix says so and commits the new ones (749.84, 749.85 and 749.88 will change the 4/4 records).
