# 749.241, the gap after a line's last note is counted only as far as the line's own limit: the form and marks, before any code or run

27 November 2026, 20:42 ET. From the count in RESULT_why_again_fresh.md; numbered by the songwriting session (20:40 ET).

**The form (`LUTHIER_AGAIN_REFIT=2`; `=1` stays the last trial's form; unset by default; with `LUTHIER_AGAIN_INSIDE=1`):** when a line sung again has more syllables than its source has notes, the routine splits the widest gap to make a note. The gap after the last note now runs to the line's own latest start for a last syllable (the slot's end less the line end's room), not to an eighth before the slot's end. So no note is split off past the limit. The last trial's refit (the source's late notes left out) stays with it.

**Trials, each read alone; seed 1, 1,000 builds:** as the last trial, with the switch at 2.
- 6/8, song 52 and song 61's words: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=rest LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1`.
- Pop 3/4, song 55's words, as the pop trial stood, with `LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2`.

**Marks, as they stand:** S1 to S7 and U1 to U4 on both 6/8 lyrics (living median and pick); K1 to K8 in pop (K3 at 0.45 and 0.26; K6 within sections); the lyric's "again" drawn fresh (712) at most **1,569 on song 52, 1,830 on song 61's words, 846 in pop**, over 1,000 builds.

Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

**What I expect, from the count:** in 300 builds the limit turned away 1,319 tries in pop and 479 on song 61's words, of 1,707 and 761 drawn fresh. If every one of those is now taken, 712 falls to about 1,300 a thousand builds in pop and about 940 on song 61's words. Some will fail another way (the widest gap may be too narrow to split), so: song 61's words under 1,830, three chances in four; pop under 846, one chance in four (the join alone turns away more than that). K6's rhythm again within sections in pop comes back toward its mark; I give it one chance in two. Song 61's words still miss 840 and first-beat onsets, which this form does not touch.
