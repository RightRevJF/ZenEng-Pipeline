# A line sung again ends inside its own slot: the form and marks, both metres, before any code or run

27 November 2026, 19:47 ET. From the count in RESULT_why_no_fit.md: in every build that stops at "the syllables cannot fit the window" (286 of 286 on song 61's words in 6/8; 127 of 127 on the pop 3/4 trial), the line ahead was sung again from another line and begins its last syllable past its own slot.

**The form (`LUTHIER_AGAIN_INSIDE=1`, unset by default):** a line made by singing another line again (the lyric's "again", and 818 in both its kinds) must begin its last syllable no later than a fresh line of its slot may: the slot's end less the line end's room. If it does not, it is not taken: the lyric's "again" is drawn fresh (712), and 818 does not apply. Copies (780) are untouched. Nothing else changes. Its number is the songwriting session's to give.

**Trials, marks unchanged, each read alone:**
- **6/8:** song 52 and song 61's words, as the last trial stood (`LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=rest LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1`) with this switch. S1 to S7 and U1 to U4, living median and pick; both lyrics must pass.
- **Pop 3/4:** song 55's words as the pop trial stood (deduced stress table, shared bars) with this switch. K1 to K8, K3 at 0.45 and 0.26.
- Seed 1, 1,000 builds each.

**Reported:** builds never made, by reason and line; how often a line the lyric marks as sung again is drawn fresh instead (the cost: the song's sameness), for each lyric, beside the same figure without the switch.

Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

**What I expect:** builds are made on song 61's words (never made falls from 95 in 100 to under 20) and on the pop trial (from 42 to under 15). The cost is real: more "again" lines drawn fresh, perhaps a third of them on song 61's words, because the plan gives a copy fewer bars than its source (749.234, shared bars, is the proper answer to that and is not on in the 6/8 package). Notes a bar and first-beat onsets on song 61's words I cannot call; they were read on 23 builds. Pop K3 stays missed (it is the ordering, 749.236). One chance in three that song 61's words meet every mark.
