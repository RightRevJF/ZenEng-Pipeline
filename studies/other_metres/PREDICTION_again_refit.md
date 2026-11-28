# A line sung again that would overrun is refitted inside its slot (not dropped); shared bars join the 6/8 package. The form and marks, before any code or run

27 November 2026, 20:15 ET. Step 2 of the order agreed with the songwriting session (20:06 ET), which numbered the limit itself 749.240 and set this trial's added mark.

## What the code does now (read, not guessed)
Outside 4/4 a line sung again takes its source's onsets as they stand, then splits the widest gap or drops the narrowest until the count matches its syllables. Onsets of the source that lie past the copy's own slot are kept, which is how the copy overruns (a source of three bars copied into two; a source that began late).

## The form (`LUTHIER_AGAIN_REFIT=1`, with `LUTHIER_AGAIN_INSIDE=1`; unset by default)
When a line is sung again, the source's notes that begin later than the copy's own latest start for a last syllable (its slot's end less the line end's room) are left out before the count is matched. The notes kept are the source's own, onset and pitch; the syllables left over are fitted by the splitting the code already does. If it still cannot be fitted inside, 749.240 applies as before (drawn fresh; 818 does not apply). The same holds for 818, which sings again by the same routine.

**Shared bars (749.234, `LUTHIER_SHARED_BARS=1`) join the 6/8 package,** so a copy is planned in its source's bars to begin with.

## Trials, each read alone; seed 1, 1,000 builds
- **6/8:** song 52 and song 61's words: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=rest LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=1 LUTHIER_SHARED_BARS=1`.
- **Pop 3/4:** song 55's words as the pop trial stood, with `LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=1`.

## Marks
- All as they stand: S1 to S7 and U1 to U4 (6/8, living median and pick, both lyrics); K1 to K8 (pop), K3 at 0.45 and 0.26, K6 within sections.
- **Added by the songwriting session:** the lyric's "again" drawn fresh (712), over 1,000 builds, no more than 1.5 times its count before 749.240: **1,569 on song 52 (was 1,046); 1,830 on song 61's words (was 1,220); 846 in pop (was 564).**
- Reported: builds never made; the bars shared bars changes on each 6/8 lyric; the silence before each title line.
- Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## What I expect
- The 712 mark: met in pop (K6's rhythm again within sections comes back over its mark with it). On song 61's words I think it lands near the line, either side: shared bars removes the three-bars-into-two case, and what remains are sources that began late.
- Builds never made stay at none: the limit is still there.
- Song 61's words still miss notes a bar (the plan; step 3) and probably first-beat onsets; so the 6/8 package as a whole is still a miss, and this trial is read on the 712 mark and K6. Shared bars may move notes a bar on either lyric, in a direction I cannot call.
- Two chances in three for the 712 mark in pop; one in two on song 61's words.
