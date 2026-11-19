# Luthier fix list for v26 (since v25)

18 November 2026. Luthier v25 (fixes 899–903) is reviewed (`lib/luthier/REVIEW_stage12.md`) and merged into main at 9b149f6; every record and the new table
reproduce byte for byte. Song 58 is rebuilt from its v25 record (third edition; every document check passes). Two new findings (749.82, 749.83), two answers,
one carried (749.61). Next finding 749.84; next fix 904.

## The v25 list against the v25 records

| Finding | Fix | Closed? |
|---|---|---|
| 749.76 line ends | 899 | yes: stressed line ends an eighth or less 0.27 / 0.34 / 0.19, a half or more 0.18 / 0.21 / 0.27 (kept 0.24, 0.27) |
| 749.80 breaths | 899 | yes: silences of a beat or more 9.5 / 9.5 / 10.4 per 100 beats (kept 7.0 to 11.1); median silence 3.0 / 2.0 / 2.5 beats; run-on 0.23 / 0.33 / 0.20 (kept 0.27) |
| 749.78 weak endings | 901 | answered against the finding, and I agree (below) |
| 749.79 guitar | 900 | yes: under sung notes 1.0 in all three 4/4 songs |
| 749.77 returns | none | agreed, with a kept figure (below) |
| 749.81 small things | 902 | yes |
| 749.75 last chorus | 903 | yes: printed as kept songs meet it |
| 749.61 6/8 | none | carried |

## 901, recounted

With `make_kept_line_ends.line_ends` (`studies/kept_checks/recount_901.py`): 664 line ends on a word's weak syllable after its stressed one; the weak syllable outlasts the stressed one in 0.49, the stressed one is under a quarter in 0.73 (the maintainer's 619, 0.47, 0.72). With tied notes read (749.82): 794, 0.42, 0.64. The retirement of 871 and 890 stands. My 749.64, 749.71 and 749.78 assumed a held weak syllable was a fault; kept singers do it at four to five line ends in ten.

## 749.77, with a kept figure for returning lines

`studies/kept_checks/stressed16_returns.py`: stressed syllables a sixteenth long inside lines, first verse and chorus against the later ones: 0.121 and 0.117 as parsed, 0.109 and 0.108 with ties read; the later-minus-first difference by song, median 0. By song the rate runs 0 / 0.034 / 0.13 / 0.33 (25th, 50th, 75th, 90th). Song 54's lines sung again (0.137) sit at the kept 75th. Kept songs do not shorten stressed syllables in returning lines, and neither, measured this way, does song 54 beyond the kept spread. Closed.

## New findings

### 749.82 The CoCoPops parser drops every note that begins a tie
**Problem.** `cocopops_parse.recip_dur` reads a duration only at the start of the kern token, so a note written `[8B` (the first note of a tie) has none and is skipped with its syllable. Its tied end (`2B]`) is then kept as a melisma note, or merged into an earlier note of the same pitch. Every kept table built from `corpora/cocopops_notes.csv.gz` since 895 reads the songs this way.
**Evidence.** 7,833 sung kern notes in the Billboard files begin a tie. Chiquitita: "sor- [8B -row. 2B]" is read as "sor-" and a melisma; "sorrow" never closes and its line end is unread. With the first note of each tie read (`studies/kept_checks/parse_ties.py`, the same parser with `[` set aside), the tables move: kept_line_ends: line ends read 5,242 to 5,542, last syllable unread 697 to 264; held a half or more (function, weak, stressed) 0.353, 0.196, 0.273 to 0.18, 0.115, 0.29; an eighth or less 0.259, 0.424, 0.236 to 0.358, 0.481, 0.182; lines run on 0.269 to 0.295. kept_word_weight: fit percentiles 0.092 / 0.202 / 0.291 / 0.384 / 0.435 to 0.152 / 0.248 / 0.318 / 0.402 / 0.446; fit by length, median 0.132 to 0.209; songs above their shuffled words 0.893 to 0.944; stressed last notes counted 1,791 to 2,833. kept_returns barely moves (verse, other count, rhythm kept 0.574 / 0.681 / 0.806 to 0.558 / 0.688 / 0.819).
**Fix.** Read the duration after a leading `[` (and `(`, `{`, `&`), keeping the tie merge; rebuild `kept_word_weight.json`, `kept_returns.json` and `kept_line_ends.json`; rerun the songs. The words' gate (the kept 10th) moves from 0.092 to 0.152.
**Check.** The parser reads every sung kern note (none dropped for want of a duration); the three tables are rebuilt and committed; the records say which table version they read.

### 749.83 The phrase check counts a breath only at a full beat of silence
**Problem.** The band check from 749.21, "sung phrases over eight seconds", splits phrases at a beat of silence. Since 899 lets lines run on as kept lines do, it now reports long phrases that kept singers sing the same way, taking a breath in half a beat.
**Evidence.** Phrases over eight seconds: songs 54, 55, 58: 7, 7, 5 (v24: 0). `studies/breath/phrases.py`, phrases over 12 beats: split at a beat, kept 0.130 (songs 0.222, 0.211, 0.109); split at half a beat, kept 0.046 (songs 0.057, 0.038, 0.019), and each kept song's longest phrase has a median of 12 beats (songs 16.5, 15.0, 13.2).
**Fix.** Split phrases at half a beat of silence, and print the share over 12 beats (or 8 seconds) beside the kept figure rather than as a count with no reference.
**Check.** The check reads the half-beat rule and prints the kept figure; the songs sit inside the kept spread.

## Carried
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known not met (the paper's own)
Rest share under the kept middle half in the picks of songs 55 and 54 (0.171, 0.20); long distances between lines short of the kept (a two-bar slot); a fifth of song 54's strums are two notes; songs 54 and 58 past the kept lengths (the lyrics).

## Order of work
1. 749.82, then rerun everything that reads the kept tables. 2. 749.83. 3. 749.61.

## Songs

| Song | Folder | Under v25 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 326 s; third edition rebuilt from this record |
| 55, Your Yard Man | p65 | 240 s; last chorus 20 bars against 16 |
| 54, The Man Mama Prayed I'd Be | p64 | 298 s; last chorus 16 bars against 12 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, and the three kept tables: byte for byte, or the fix says so and commits the new ones (749.82 will).
