# Luthier fix list for v23 (since v22)

18 November 2026. Luthier v21 (fixes 867–878) and v22 (879–884) are reviewed (lib/luthier/REVIEW_stage8.md, REVIEW_stage9.md) and merged into main at
8dea87c; every record reproduces byte for byte. Song 58's scores and songbook are redone from its v22 record. This list holds the findings open after v22:
ten new (749.66 to 749.75) and two carried (749.58, 749.61). Next finding 749.76; next fix 885.

## 749.57 to 749.64 against the v22 records

| Finding | Fix | Closed? |
|---|---|---|
| 749.57 descant ceiling | 878 | yes: song 53's summit sounds A5 as sung |
| 749.58 rests between lines | 870 | no: median rest a quarter in songs 52, 54, 55 (58: 15 twelfths); rest share under the kept middle half in 52, 54, 58. Carried |
| 749.59 melismas on function words | 875 | yes: 0 in all four songs |
| 749.60 the pick by rejected readings | 872 | yes |
| 749.61 the band | 873 | 4/4 yes; 6/8 no (song 52: 0 of 76 builds pass the joint gate). Carried |
| 749.62 the old judge chose nothing | 874 | yes (see 749.68) |
| 749.63 slots | 869 | yes: song 58 sixteenths 5.3 in 100, no fit deaths |
| 749.64 weak endings | 871 | yes for two-syllable words (0 of 13); widened as 749.71 |
| 749.65 breath on the grid (the session's) | none | closed the day it was filed: the lead did not hold out on 1,479 Hooktheory songs; nothing to build. v21 mended the breath count (song 58: 1.8 to 6.1 real breaths a minute; human median 7) |

## New findings

### 749.66 A split in a line sung again leaves a stressed syllable a sixteenth long
**Problem.** 882 adds a note by halving the note it splits, and chooses where by the place table alone. When it splits the note under a stressed syllable, that syllable is left a sixteenth.
**Evidence.** `review9_stressed16.py`. Stressed syllables a sixteenth long in lines sung again, v21 then v22: song 54 3 of 137 then 19 of 134 (its other lines 4 of 82); song 55 5 then 9 of 81; song 58 5 then 3 of 75. Song 58's pick, Verse 2 line 1, "sure the crowd was on its way": the source's two pickups dropped (772), two notes split back in, "crowd" 3 twelfths before four sixteenths.
**Fix.** Split the note under the lighter syllable, or charge length in 882's score: a stressed syllable keeps at least an eighth unless kept songs give it less at that place.
**Check.** Stressed syllables a sixteenth long in lines sung again at or under the same song's other lines.

### 749.67 Lines sung again keep less of their source, and no kept figure bounds it
**Problem.** 882 trades a return's likeness to its source for the words' fit at `again_cost` 8, and neither the cost nor the loss is set against kept songs.
**Evidence.** `review9_again_check.py`, lines sung again whose count differs from their source, share of the source kept in order, v21 then v22: song 58 pitches 0.86 then 0.76, rhythm 0.84 then 0.74; song 55 0.74 then 0.68, 0.80 then 0.71; song 54 0.80 then 0.78, 0.81 then 0.79. The README's own: song 58's builds' place under the old 4/4 judge 0.83 to 0.62.
**Fix.** Measure how much of verse 1's line a kept song's verse 2 line keeps (in order, pitch and rhythm, whole songs with section labels), and set `again_cost` so builds sit inside the kept quartiles.
**Check.** The returns' kept share inside the kept quartiles in songs 54, 55 and 58.

### 749.68 In 4/4 the joint gate and the words' gate pass nearly every build
**Problem.** After the old charge's least half, the joint gate and the words' gate take almost nothing away, so the pick is the first build made in the least half.
**Evidence.** Joint gate: song 58 308 of 308, song 54 428 of 434, song 55 363 of 366. Words' gate (at least 0.092): every build after the other gates in all three; builds' fit quartiles 0.24 to 0.38. Song 58's pick is build 0.
**Fix.** Say in the paper that in 4/4 the old charge is the only gate that chooses, or set the gates where they bind (the words’ gate at the kept 25th, 0.202, would take about a quarter of song 54’s builds).
**Check.** The record says which gate removed how many builds, and at least one gate besides the old charge removes some in 4/4.

### 749.69 One song, two lengths, both past the kept 75th
**Problem.** Song 58's flag says 337 s and its checks say 343 s (the flag is counted before the turn is added). Either is far past the kept 75th (243 s); under v20 it ran 229 s. The lines' second bars (869) and the kept rests (870) added two minutes, and the lyric (57 lines) is long for 84.
**Evidence.** `lyric58.song.json`: flags and checks.
**Fix.** One length, counted once, after the form is final. At intake, say how long the lyric will run at the chosen tempo, so the writer can shorten the lyric or raise the tempo.
**Check.** The flag and the check agree; the intake prints the expected length.

### 749.70 The new kept tables and the stage 8 and 9 results have no maker that runs in the repo
**Problem.** `tables/kept_word_weight.json` and the scaling figures in the gate come from `way3_words_study.py` and `way2_scaling_study.py`, whose paths are on the maintainer's machine (`/home/claude/zeneng/corpus/nine`, `/home/claude/zeneng/corpus/v20`, `/home/claude/rightrevjf/...`); the table's write is commented out; no committed script writes `stage8_results.json` or `stage9_results.json` (`way2_scaling_study.py` writes `dfa_results.json`).
**Evidence.** The scripts as committed.
**Fix.** Repo-relative paths, the table's write switched on, a maker for each results file, and a note on where to fetch each corpus.
**Check.** A session regenerates the tables and both results files byte for byte, or says which corpus it could not fetch.

### 749.71 871 reads only words stressed on their first syllable
**Problem.** A longer word ending a line can still give its stressed syllable a sixteenth.
**Evidence.** Song 58, Bridge line 4, "completely": stressed "-plete-" 3 twelfths, the last syllable 6, at the line's end.
**Fix.** Apply 871 to the line's last stressed syllable, whatever the word's length.
**Check.** No line-final word holds an unstressed syllable longer than its stressed one, beyond the kept rate.

### 749.72 Two fits for one pick, two sets of kept figures
**Problem.** The record prints the words' fit twice with different values, and the kept figures differ between the docstring and the README.
**Evidence.** Song 58: checks 0.29 (melismas' second notes left out), `judge7.pick_words_fit` 0.325 (computed before melismas). `word_weight.py`'s docstring: kept 0.18 / 0.28 / 0.37, 87 in 100 beat the shuffled control; README and checks: 0.20 / 0.29 / 0.38 (0.202 / 0.291 / 0.384), 89 in 100.
**Fix.** One fit, on the notes as sung, in both places; one set of kept figures.
**Check.** The two fields agree; the docstring matches the table.

### 749.73 Under a low voice the guitar drops out
**Problem.** `band.py` voices each chord below the sung note (`cap = min(sung) - 1`) inside the guitar's kept register. With a baritone at B2 to C4 no three-note voicing fits, so the guitar plays only where he rests. A guitar's open chords sit around and above a man's voice all the time; the rule that the accompaniment stays under the sung tune (749.21) comes from piano Lieder.
**Evidence.** Song 58: the guitar sounds under 6 of 469 sung notes; of its 276 strums, 165 fall in the 106 sung bars (848 eighths) and the rest in the intro, turn and outro. The verses are bass and drums under the voice.
**Fix.** For a guitar with a low voice, allow the voicing around and above the voice (or in the guitar's own low register, E2 up), and keep the under-the-tune rule for piano.
**Check.** In song 58 the guitar sounds under most sung notes, inside the low-interval limits, with no voicing a second from the sung note.

### 749.74 The harmony voice has no range of its own
**Problem.** 829 draws the harmony voice below the lead with no floor, so under a baritone it goes below a bass's usual range.
**Evidence.** Song 58: lowest D2; 3 notes below E2, 9 below G2, of 192.
**Fix.** Give the harmony voice a range (a kept range for the voice named, or the lead's range moved by its interval), and take it above the lead where below has no room.
**Check.** No harmony note below the range set for it.

### 749.75 Every chorus is at level 1.0, so the last chorus is not the song's top
**Problem.** 9.12 asks for each chorus above its verse and the last chorus or bridge the top. `band.levels` gives every chorus 1.0, and the band-only energy read puts the two-bar turn highest because the guitar plays only where the voice rests (749.73).
**Evidence.** Song 58 levels: choruses 1.0, bridge 0.94; energy read: choruses 0.54, last chorus 0.54, turn 0.64.
**Fix.** Raise the last chorus over the others (a part added, the harmony on every line, the drums opened up), and read the arc after 749.73.
**Check.** The last chorus or the bridge reads highest.

## Carried

- **749.58** rests between lines (above). The cause: 870 draws a kept rest only for fresh lines and only where the slot leaves room; lines sung again and copies keep their source's join.
- **749.61** 6/8: song 52, 0 of 76 builds pass the joint gate (quartiles 4.54 to 5.07 against 3.57).

## Order of work

1. 749.73, 749.75 (what a listener hears first in song 58: verses with no guitar, a last chorus no bigger than the first). 2. 749.66, 749.67 (882). 3. 749.68, 749.69, 749.71, 749.74. 4. 749.70, 749.72. 5. 749.58, 749.61.

## Songs

| Song | Folder | Made by | Under v22 |
|---|---|---|---|
| 58, Same Time Tomorrow | p68 | song_from_lyric.py | 615 of 1000 survive; pick 225b8c372faa (build 0); 343 s; scores and songbook redone from this record |
| 55, Your Yard Man | p65 | song_from_lyric.py | 732 of 1000; joint gate 363 of 366 |
| 54, The Man Mama Prayed I'd Be | p64 | song_from_lyric.py | 868 of 1000; joint gate 428 of 434 |
| 53, Sung to Sleep | p63 | hand spec, hymn mode | tune pick unchanged; descant summit A5 as sung |
| 52, The Room Next Door | p62 | hand spec and from its lyric | from the lyric 76 of 1000; none past the joint gate |

## Known not met (the paper's own)

Rhythm scaling under the kept middle half on songs 54 and 58 (58: 0.471); the descant's summit at note 23 of 34, not in the last quarter; song 52 has no build past the joint gate; songs 54 and 58 run past the kept lengths; the fit by length near nothing (58: 0.019 against a kept median of 0.132).

## Regression line

`lyric52/54/55/58.song.json` (+ `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`: byte for byte, or the fix says so and commits the new record.
