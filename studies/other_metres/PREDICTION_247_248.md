# 749.247 revised (the mend keeps the chord) and 749.248 (749.244 on every path): the forms and marks on the five seen lyrics. Before any code or run

28 November 2026, 01:17 ET. From the counts in RESULT_counts_before_69.md; both accepted, with their marks, by the songwriting session (01:06 ET). This run settles the package song 69 would run on.

## 749.247 revised (`LUTHIER_AGAIN_RUNS=2`; `=1` stays the first form; unset by default)
Where a line sung again has a run of one pitch over the cap:
- a note of the run that does not fall on a beat moves a scale step toward the next different note (the one nearest the end of the run that will end it);
- where every note that could end the run falls on a beat, that note moves to the nearer chord tone inside the register, not a scale step;
- if neither ends the run, the line is refused as now.
*Settled:* the notes that can end a run over the cap are the last four of it (moving any one leaves no more than three alike); this is tried again until no run is over the cap or nothing more can move.

## 749.248 (`LUTHIER_TITLE_840=2`; `=1` stays 749.244 alone; unset by default)
A title line does not take a rhythm that fails 840's test from 876's one bar (the line sung in one bar, the next silent) while a kept window that passes can be had: the one-bar rhythm is taken only if it passes; otherwise the line is drawn among its passing kept windows as 749.244 has it. The weighted rule is still the last resort where no kept window fits at all.

## Trial: the five seen lyrics (song 52; the words of songs 61, 50, 49 and 58), each read alone; seed 1, 1,000 builds
The package of RESULT_held_out_3_6_8.md with the two switches at 2: `LUTHIER_TABLE_6_8=../../studies/other_metres/trial_tables/6-8_folk_sung LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.001 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_TITLE_840=2 LUTHIER_REST_TABLE=1 LUTHIER_PICKUP_WINDOWS=0 LUTHIER_AGAIN_RUNS=2`. Beside it each form back at 1 in turn.

## Marks
- **Every mark as it stands, pick and living median, all five:** living 30 and pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389; on the first beat 0.211; 731 at 0.40; deaths on 780 and 840 under one in ten; in the voice, no leap; title lines on time 75 in 100; silence before each title line 3 eighths or under; the share of marked lines drawn fresh at most 0.076.
- **749.247 revised, the songwriting session's mark, per lyric:** moved notes that fall on a beat are chord tones at least as often as the source lines' own notes on a beat (0.898, 0.898, 0.938, 0.877, 0.916 on songs 52, 61, 50, 49, 58 in the last count; read again in this run).
- **Watched, not marks:** the share of lines sung again with a note moved (0.051 to 0.098 now); the count of distinct rhythms each title line drawn fresh takes over 600 builds, against the same count on the last package (counted before the run and printed beside it).
- Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

**If all five pass, song 69's package has both forms. If either misses, song 69's package is the one that passed song 58's words held out (7f8f67d), and the miss goes on the list.** Nothing runs on song 69 either way.

## What I expect
- **749.248:** 840 falls to none or near it on all five (every death was this path). Four chances in five. The title lines lose the one-bar rhythms that failed; their kept windows are untouched, so the count of distinct rhythms falls only by those.
- **749.247 revised:** most runs have a note off the beat (the copies run about four notes a bar on two beats), so most mends move an off-beat note and the on-beat chord-tone mark is read on few notes. Where an on-beat note must move to a chord tone, that is a third or more: a leap inside a line is possible but small against the octave mark. The mark met on all five: two chances in three; the doubt is a lyric where the few on-beat moves find no chord tone in the register and the line is refused, raising the share drawn fresh.
- All five on every mark: one chance in two.
