# The title's room asks only that a passing window exists (749.244 does the rest): the form, the four seen lyrics, then song 58's words held out. Before any run

28 November 2026, 00:07 ET. From the count in RESULT_counts_49.md: on all four seen lyrics every title line has kept windows that pass 840's test at the bars the density rule gave it, and the title's room adds four to six bars a song for nothing the draw does not now do.

**The form (no new code: `LUTHIER_TITLE_ROOM=0.001` in place of 0.9):** a title line takes more bars only until some kept window puts half its stresses on a beat (a share over nothing), not until 0.9 of them do. 749.244 then draws the line among the passing windows. Where no window passes at any bar count, the old rule's fallback stands.

## Step A: the four seen lyrics (song 52; song 61's words; song 50's words; song 49's words)
The package with that one value changed: `LUTHIER_TABLE_6_8=../../studies/other_metres/trial_tables/6-8_folk_sung LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.001 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_TITLE_840=1 LUTHIER_REST_TABLE=1 LUTHIER_PICKUP_WINDOWS=0`; seed 1, 1,000 builds.
- Every mark, pick and living median: living 30 and pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389; on the first beat 0.211; 731 at 0.40; deaths on 780 and 840 under one in ten; in the voice, no leap; title lines on time 75 in 100; silence before each title line 3 eighths or under.
- **The 712 mark, as the songwriting session wrote it at 23:58 ET for runs from now on, read as a share:** the share of tries to sing a marked line again that are drawn fresh (300 builds, why_again_fresh.py) is at most the higher of 1.5 times the lyric's own share before 749.240 and the highest share among the seen lyrics under the last package, which is **0.076** (share_712.json; song 52 0.0736, song 61's words 0.076, song 50's words 0.0521). For the four seen lyrics the limit is therefore 0.076 (their own earlier shares times 1.5 are under it where known).
- Reported: 749.243's moves (with the title's bars back a section's density changes, so it may move differently).

## Step B, only if all four pass: song 58's words, "Same Time Tomorrow", held out, read once
The last unseen spent folk lyric (songs/p68/lyric58.json; metre 6/8, genre folk, 54 beats a minute; a trial copy). The same package and marks; its 712 limit is the higher of 0.076 and 1.5 times its own share from one more run without `LUTHIER_AGAIN_INSIDE` and `LUTHIER_AGAIN_REFIT`. Nothing is changed and run again on it afterwards tonight.

## What I expect
- **Song 49's words:** five bars back; notes a bar about 3.68, met. Its title lines are five and six syllables with two stresses in two bars, with 37 of 41 and 55 of 70 windows passing: 840 stays at none.
- **The other three:** four to six bars back each, notes a bar up by about 0.15 to 0.2 (3.86 to about 4.05 on songs 52 and 50; still under 4.33). Their title lines go from four bars to two with fewer passing windows (10 of 35 on song 52; 27 of 65 on song 50's words): they are drawn among those, so 840 should hold, but the title line will sound less roomy. First-beat onsets fall a little as notes a bar rises (one first beat a bar): from 0.235 to 0.267 they have room.
- **The risk:** song 52's bridge title line (ten syllables, six stressed) at three bars: its one-bar part has 3 passing windows of 9. And song 61's words' first verse, eased by 749.243, may be eased differently.
- All four passing: one chance in two. Song 58's words then passing: one in two; it has six title lines and 57 lines, the longest lyric yet.
