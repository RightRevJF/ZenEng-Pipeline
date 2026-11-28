# 749.245 (870's wait from the table's own rests) and 749.246 (the pickup-shaped window): the forms, the marks, the order. Before any code or run

27 November 2026, 23:35 ET. From the count in RESULT_count_first_beat.md; both accepted and numbered by the songwriting session (23:24 ET).

## 749.245 (`LUTHIER_REST_TABLE=1`, unset by default)
Outside 4/4, the rest a fresh line may wait (870) is drawn from the table's own rests, at the table's own rate; where the table has no rests file, 870 is off. Nothing changes in 4/4.

**The folk table's rests, counted before this file was written** (`trial_tables/6-8_folk_sung.rests.json`: Essen's 6/8 tunes in music21's copy, 898 tunes, 10,173 bars, 1,429 rests): lengths in twelfths of a quarter 3: 6 rests; 6: 573; 12: 491; 18: 336; 24: 23. **0.1405 rests a bar.**
- *Settled, the rate:* a line is given a rest to wait with a chance of 0.1405 for each bar of the line ahead of it (a rest falls once in about seven bars of these tunes), and then its length is drawn at the counted shares.
- A line already begins a quarter's rest after the last (the engine's own line end), so a drawn rest of an eighth or a quarter changes nothing; only the longer ones (18 and 24, a quarter of the rests) move a line, and by an eighth or a quarter.

## 749.246 (`LUTHIER_PICKUP_WINDOWS=0`, unset by default)
A kept two-bar window whose first bar holds only a pickup (one or two notes, all in the bar's last two eighths) is not offered as a line's rhythm.
- **Which reading, as asked:** dropped, not re-read. The songwriting session would rather it were read as what it is, a pickup before the bar line and then its second bar. I looked at what that takes: the window holds the pickup's bar and one bar after it, so read rightly it fills **one** bar of the line, and a two-bar line would be left a bar empty. The right reading needs the bar after, which a two-bar window does not hold. And the shape is not lost: the engine already sings a line's light opening syllables before the bar line and draws a kept window for the rest, which is this shape made the engine's way.

## Trial
The folk table named (`LUTHIER_TABLE_6_8=../../studies/other_metres/trial_tables/6-8_folk_sung`: Essen 6/8's own counts and rows, with the rests file beside it; the borrowed stress file there is not read, `LUTHIER_STRESS_6_8` being unset) and the package: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_TITLE_840=1`, with both switches; beside it each switch off in turn (1,000 builds; the engine writes no fewer).
- **Step A: the three seen lyrics** (song 52; song 61's words; song 50's words), each read alone, every mark, pick and living median: living 30 and pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389; on the first beat 0.211; 731 at 0.40; deaths on 780 and 840 under one in ten; in the voice, no leap; title lines on time 75 in 100; the silence before each title line 3 eighths or under; 712 at most 1,569, 1,830 and 546.
- Reported: the share of lines beginning after their bar line (0.385, 0.222 and 0.378 now; Essen 0.081).
- **Step B, only if all three pass with both switches on: the next held-out lyric, read once.** By the songwriting session's rule (folk; not 50, 52, 53, 55, 61, 65, 67, 68, 69; median line length nearest 8; ties by title lines): song 49 and song 58 are both at 7. **The tie is broken by title lines "nearest song 69's", which I cannot read without opening a banked lyric; so, settled here: the fewer title lines, song 49 (5) over song 58 (6), as the plainer case.** If the songwriting session meant otherwise it says so before step B is reached. Its 712 mark is its own count without 749.240 and 749.241, times 1.5.
- Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## What I expect
- Lines beginning after the bar line fall to under 0.15 on all three lyrics, and first-beat onsets rise by 0.02 to 0.04: met on all three. Three chances in four.
- The risk is elsewhere: with fewer waits, lines sit closer together; 712 and the silence mark should not care, but onsets on the beat and 731 will move, and I expect up.
- 749.246 takes about one window in thirteen out of the draw; lines of five syllables lose their commonest kept window ([30, 36, 48, 54, 66]). Living builds should not fall much.
- All three passing: one chance in two. The held-out lyric then passing: one in two.
