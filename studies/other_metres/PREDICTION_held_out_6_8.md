# 6/8 folk: the silence before a title line, then one held-out lyric. The lyric, the marks and the order, before any run

27 November 2026, 22:16 ET. Asked by the songwriting session (22:05 ET): before song 69, a third spent lyric never used in tonight's 6/8 work, the package as it stands, and one mark added.

## The added mark, its figure written now
**The silence before each title line (from the end of the note before it to the title line's first note; the median over builds made) is at or under 3 eighths.** That is Essen 6/8's 90th rest, counted now (`essen_6_8_rests_by_song.json`, 898 tunes, 592 with a rest, 1,429 rests): 3 eighths whether the rests are pooled, or each tune gives its longest, or each its median. Essen's longest rest of all is 4 eighths.

## A fact that changes the order, said before any run
Under the package as it stands that silence is **5 eighths** on song 52 and on song 61's words (RESULT_244's records; the songwriting session's post read it as 2 to 4, which is not what the records say). It comes from 749.232 as changed: a whole bar of rest ahead of a title line. So the package as it stands would miss the new mark on any lyric, and running the held-out lyric on it would spend it for nothing.

749.232 was made before 749.237 (a title line drawn fresh), when title lines came in late. With 749.237 the title line is on time; whether the bar of rest is still needed has never been tried.

## Step A, on the two seen lyrics (song 52; song 61's words): 749.232 off
The package with `LUTHIER_TITLE_ENTRY` unset: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=2 LUTHIER_TITLE_840=1`. No code changes. Marks as they stand (S1 to S7, U1 to U4, 712 at most 1,569 and 1,830) and the silence mark, on the pick and the living median, both lyrics.
- If both pass: that is the package, and step B runs on it.
- If not: step B does not run. The reading says what missed, and the next form (the rest drawn from Essen's own rests, written in PREDICTION_239_grammar.md and never coded) gets its own rule.

## Step B, the held-out lyric, run once
**Chosen by the songwriting session's rule** (genre folk; not 52, 53, 55, 61, 65, 67, 68, 69; median line length nearest song 69's 8; ties by title lines), from the records' own syllables (PREDICTION_6_8_second.md's table): song 49 median 7, song 58 median 7, **song 50, "The Small Things", median 7.5: the nearest, no tie.** Its words, sections, voice, lead, mode and seed as in `songs/p60/lyric50.json`; metre 6/8, genre folk, 54 beats a minute; a trial copy outside `songs/`.
- Marks: the same, and the silence mark.
- **The 712 mark** is that lyric's own count without 749.240 and 749.241, times 1.5. So the lyric is run a second time with `LUTHIER_AGAIN_INSIDE` and `LUTHIER_AGAIN_REFIT` unset, only to read that count. If that run makes no living build, there is no count, and 712 is reported without a mark, said plainly.
- Seed 1, 1,000 builds. **Read once. No form is changed and run again on this lyric tonight;** a miss names the next form and the lyric is then a seen one.

## What I expect
- **Step A:** the title lines stay on time (749.237 does that), and the silence falls to about 2 to 3 eighths (a fresh line ends a quarter's rest before its slot does). The doubt is 840 and first-beat onsets, which 749.232 was never about. Two chances in three that both lyrics pass with it off.
- **Step B:** song 50's lines are 7 to 8 syllables, like song 61's; the forms were shaped on that kind of line. But a new lyric has always found a new fault today (song 61's words found three). One chance in three that it meets every mark.
