# Luthier list for v32 (since v31)

20 November 2026. Luthier v31 (fixes 922–923) is reviewed (`lib/luthier/REVIEW_stage18.md`) and merged into main at 4f88e4b. The page table, every record, `soundness.json` and `neighbour_v31.json` reproduce. The engine is sound by the rule, on the picks and on the pools (a random pool pick passes 96 times in 100). Song 58 is rebuilt from its v31 record (ninth edition, D major, a four-bar turn; 44 of 44 document checks pass). Three new items (749.102 to 749.104). 749.98 to 749.101 are carried unanswered. 749.94 is retired: its measure was wrong (749.103). Next finding 749.105; next fix 924.

## The two questions, in short

1. **A floor is the right use**, and the only one the studies support. It removes 2 builds of 94 in song 55, none in 54 or 58, and changes no pick. It is insurance, not an improvement, and should read the notes as sung (749.102).
2. **The figure memory does not pull the songs toward the middle.** A random pool pick stands outside the middle half on 19 song-checks under v30 and under v31. The 15 against 17 is the neighbour choice, a different reading. It buys little: the builds' figures sung again rise from 0.425 to 0.450 at the median (kept 0.560). Keep it.

What it exposed is that 749.94 counted lean as variety (749.103).

## Items

### 749.102 Read the page gate on the notes as sung
**Problem.** The floor reads each build's notes before 848 places its melismas. The words' gate reads them as sung (914), and the kept tunes in `kept_page_gate.json` were read with their melismas. A melisma's second note is the step below, so leaving it out changes steps, repeated figures, surprise and the share on the tonic against the table's.
**Evidence.** `metre_engine.Engine.run`: `PGm.read([n["p"] for n in c["notes"]], ...)`, where the words' gate uses `self.as_sung(c["notes"])`. The melisma share drawn is 4 to 16 syllables in 100, so the difference is small but one-sided.
**Fix.** Read the floor on `self.as_sung(c["notes"])`, as 914 does for the words' gate.
**Check.** `judge7["page_gate"]` says it read as sung, and the pick's page readings equal those in the record's style checks.

### 749.103 Count variety on both sides, not checks outside the middle half
**Problem.** 749.94 asked for at least 21 song-checks outside the kept middle half. That count rewards a lean as much as variety. Nearly all of the pools' readings outside the middle half sit on one side of their check. So correcting a lean (as 923 partly does for figures) lowers the count while making the songs more like kept songs. The measure was mine, and it was wrong.
**Evidence.** `neighbour_v31_spread.json`. Twice the smaller side, summed over the 21 checks: 0.77 under v31 (0.88 under v30). Three kept songs read the same way give about 4.0 at the median, 2.0 at the 5th percentile. That simulation treats the checks as independent; `neighbour.py` should draw kept triples itself.

The pools' middle half against the kept songs' middle half, all three songs pooled, has a median width of 0.51; within one song, 0.27 to 0.38. The narrowest checks:

| Check | Width against kept |
|---|---|
| notes a bar | 0.18 |
| rhythm scaling | 0.23 |
| range | 0.27 |
| stressed line ends held a half note | 0.30 |
| onsets on the beat | 0.33 |
| longest phrase | 0.33 |
| repeated notes | 0.35 |

**Fix.** Retire 749.94's count. `neighbour.py` reports two-sided variety (now written), with kept triples drawn from the kept rows for its reference. For the narrow checks, let each song take its value from its aimed kept song, as 920 does for the moves: notes a bar from that song's density, range through 749.100, line-end lengths and phrase lengths from its own readings.
**Check.** Two-sided variety at or above the kept triples' 5th percentile, and the pooled width at a median of 0.75 or more. The rule still holds on the pools.

### 749.104 Kept tunes repeat their figures early; the songs repeat them late
**Problem.** The songs' four-interval figures sung again are now near the kept lower quartile over the whole song. Early in the song they are still short: kept tunes sing their own figures again within the first verse. The figure memory closes about a fifth of the whole-song gap and does not reach the bar-level figures at all.
**Evidence.** Four-interval figures sung again in the first 120 notes: builds' medians 0.164, 0.241, 0.328; picks 0.112, 0.216, 0.276. The kept quartiles are 0.241, 0.362, 0.455. Over the whole song the builds' median is 0.450 with the memory, 0.425 without; kept median 0.560. Bars on a figure already sung (rhythm and intervals together) are under the kept 25th in 49 pool builds in 100, under v30 and v31 alike. Of the lines the song means to sing to an earlier line's tune (`how` "again": 26, 36, 23), about 3 a build cannot be fitted and are drawn fresh (712: 3.2, 3.2, 3.5 a build).
**Fix.** First a study: where kept tunes' repeated figures sit. Is it the same line position across the lines of a verse, verse against verse, or chorus returns? How often is a line sung to an earlier line's tune with notes split or merged to fit new syllables? Then fit "again" lines the way kept songs do (split or merge a note for an extra or missing syllable) rather than drawing them fresh. Do this before raising any note-level pull.
**Check.** In the pools, four-interval figures sung again in the first 120 notes inside the kept middle half in at least half the builds, and bars on a figure already sung under the kept 25th in no more than 35 in 100.

## Carried (unanswered in v31)
- **749.98** Draw the lift from the song the aim is drawn from. Song 58 still aims at "Bird Dog" (range 9, no lift) with a lift of 9; leaps 0.03 (kept 10th 0.04).
- **749.99** Let a pitch repeat as kept songs repeat it (longest run 4 in all three; kept median 6).
- **749.100** The melody steps more, leaps less and spans less than kept songs (steps over the kept 75th in 55 pool builds in 100, leaps under the 25th in 49, range under the 25th in 44). Watch 922 when it goes in: range and leaps are two of the floor's ten parts. If the floor starts to bind against the wider melody, take those two out of its mean.
- **749.101** Repetition: varied returns at the kept share (goes with 749.104).
- **749.61** 6/8: song 52, no build past the joint gate.

## Retired
- **749.94** Replaced by 749.103.

## Order of work
1. 749.103 (the measure, so the rest reads right). 2. 749.98. 3. 749.100, watching 922. 4. 749.104 with 749.101. 5. 749.99. 6. 749.102. Rerun `neighbour.py` after each; the rule must hold throughout.

## Songs

| Song | Folder | Under v31 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 337 s; key D; a four-bar turn; plainer than 79 kept tunes in 100; ninth edition rebuilt from this record |
| 55, Your Yard Man | p65 | 244 s; key C; range 9 (its aim: 19); plainer than 67 in 100 |
| 54, The Man Mama Prayed I'd Be | p64 | 307 s; key A; plainer than 57 in 100 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, the seven kept tables (with `kept_page_gate.json`), `studies/soundness/soundness.json`, and the shared fields of `neighbour.json`: byte for byte, or the fix says so and commits the new ones.
