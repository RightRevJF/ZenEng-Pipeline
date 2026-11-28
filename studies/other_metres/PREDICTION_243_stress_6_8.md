# 6/8: the stress score on (749.231's form) and 749.243 (no section denser than the table's 75th). The forms and marks, both lyrics, before any code or run

27 November 2026, 21:14 ET. From count (b) (RESULT_count_b.md); both accepted by the songwriting session (21:05 ET), which numbered the second.

## The stress score in 6/8 (`LUTHIER_STRESS_6_8=1`; the form is 749.231's, already coded)
The folk table (Essen) has no words, so it has had no stress file and the score has never been on in 6/8. For this trial a table is named that is Essen 6/8's own counts, unchanged (`trial_tables/6-8_folk_sung.json`, a copy), with a stress file beside it: the one counted from the 99 worded 6/8 lead sheets (`6-8_leadsheet_sung.stress.json`). **Borrowed, and labelled so:** lead sheets of standards, not folk song. OpenScore Lieder's 216 worded 6/8 songs replace it when counted.

## 749.243 (`LUTHIER_SECTION_DENSITY=1`, unset by default; under the plan form)
After every other planning rule, each section's syllables over its sung bars are read. Where that is over the table's 75th of notes a bar (4.33 in Essen 6/8), the section's densest line (most syllables a sung bar; the earlier on a tie) that has under four bars takes a bar more, and this repeats until the section is at or under the 75th or no line can take more. *Settled:* with shared bars on, the lines that share that line's tune take the bar with it; a title rule's slots are kept as they were set.

## Trial: song 52 and song 61's words, each read alone; seed 1, 1,000 builds
The package as 749.241 stood (`LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=rest LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1`), the named table, and both switches. **Beside it, each switch off in turn** (the songwriting session asked 200 builds; the engine writes 1,000, so 1,000 it is), to see which moves which mark.

## Marks, unchanged, on the living median and the pick; both lyrics must pass
Living 30 and pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389 or more; on the first beat 0.211 or more; 731 at 0.40 or more; deaths on 780 and 840 each under one in ten; in the voice, no leap past an octave in a line; each title line on time in 75 builds of 100; the lyric's "again" drawn fresh at most 1,569 (song 52) and 1,830 (song 61's words).

Reported: the lines 749.243 moves; each section's syllables a bar before and after; stressed syllables on the first beat.

Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## What I expect
- **The stress score:** 840 on song 61's words falls under one in ten (the score weighs exactly what 840 reads). Three chances in four. It should also lift first-beat onsets a little on both lyrics, since stressed syllables are drawn to the bar's first beat.
- **749.243:** it moves Verse 1 of song 61's words (4.58) and perhaps Verse 2 (4.33, at the line). First-beat onsets rise there. But a bar more lowers notes a bar, which is 3.744 against a floor of 3.60: one line moved costs about 0.04. It should hold.
- **Song 52:** Verse 1 is 4.17, under the 75th; 749.243 moves nothing. The stress score changes its draw, so its marks are read afresh; its pick's onsets on the beat were 0.394 against 0.389 and could slip.
- Both lyrics meeting every mark: one chance in three.
