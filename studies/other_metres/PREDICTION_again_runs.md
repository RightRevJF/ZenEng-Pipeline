# A line sung again mends its own run of one pitch: the form, the four seen lyrics, then song 58's words held out. Before any code or run

28 November 2026, 00:27 ET. From the count in RESULT_why_join_refuses.md: every refusal at the join, on all four seen lyrics, is a run of one pitch over the cap of three that the copy itself made (the source's longest run is two or three; the copy's four to six).

**The form (`LUTHIER_AGAIN_RUNS=1`, unset by default):** when a line is sung again and its pitches are set, each note that would be the fourth (or later) of one pitch in a row moves a scale step toward the next note of a different pitch (up or down as that note lies; where there is none, away from the note before the run), kept inside the line's register. The line is then tested at the join as now, and refused as now if a run remains. The source is untouched. Its number is the songwriting session's.

## Step A: the four seen lyrics (song 52; the words of songs 61, 50 and 49)
The package: `LUTHIER_TABLE_6_8=../../studies/other_metres/trial_tables/6-8_folk_sung LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.001 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_TITLE_840=1 LUTHIER_REST_TABLE=1 LUTHIER_PICKUP_WINDOWS=0 LUTHIER_AGAIN_RUNS=1`; seed 1, 1,000 builds.
Every mark, pick and living median: living 30 and pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389; on the first beat 0.211; 731 at 0.40; deaths on 780 and 840 under one in ten; in the voice, no leap; title lines on time 75 in 100; silence before each title line 3 eighths or under; the share of tries to sing a marked line again that are drawn fresh at most 0.076 (300 builds).
Watched, as the songwriting session asked, not a mark: 840 on each lyric against 0, 0.07, 0.68 and 0.67 in ten now.
Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## Step B, only if all four pass: song 58's words, "Same Time Tomorrow", held out, read once
`songs/p68/lyric58.json` with metre 6/8, genre folk, 54 beats a minute, a trial copy. The same package and marks; its share limit is the higher of 0.076 and 1.5 times its own share from one more run without `LUTHIER_AGAIN_INSIDE`, `LUTHIER_AGAIN_REFIT` and `LUTHIER_AGAIN_RUNS`. Nothing is changed and run again on it tonight.

## What I expect
- The share falls on all four, to under 0.03: the count says the run is the only thing refusing these lines, and a step mends most runs. Song 61's words under 0.076: four chances in five.
- A line that is now kept where it was drawn fresh changes the song's notes a little; the figure marks have room on all four (the nearest is song 61's words' 840 at 0.07 and song 49's words' notes a bar at 3.75).
- All four passing: two chances in three. Song 58's words then passing: one in two. Each held-out lyric so far has found one fault the seen ones hid.
