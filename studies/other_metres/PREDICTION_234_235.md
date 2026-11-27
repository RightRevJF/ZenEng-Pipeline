# 749.234 (lines that share a tune share their bars) and 749.235 (a title line does not take 870's wait): the forms, before any code or run

27 November 2026, 17:11 ET. Both accepted by the songwriting session (16:52 and 17:12 ET), which numbered them (749.233 is metre apart from style). Marks as they stand, with its changes below.

## 749.234 (`LUTHIER_SHARED_BARS=1`, unset by default; under the plan form)
Lines that sing one tune (a line and every line sung again from it or copied from it) take one bar count: the density rule's choice for **the median syllable count of the group**. *Settled:* where a title rule (the title's room, the line ahead of a title line) has raised any line of the group, the group takes the larger count; the group's slot follows the style's padding as before.

**Trial:** the pop-style trial as written in `PREDICTION_pop_3_4.md` (song 55's words in 3/4, rock, 133; the pop table; every switch of that trial), with this switch added. **Marks K1 to K8 as accepted, K6 within sections, and K3 as the songwriting session now sets it,** since the stress table is deduced and no longer the lead sheets': stressed syllables on the first beat, living median and pick, **at or over 0.45**; stressed syllables off the beat **at or under 0.26**.

**Two stress tables are read, in two runs, as asked:** the deduced table, and one "deduced, shrunk" (`3-4_pop_shrunk_sung.stress.json`): each deduced share pulled back toward the standard waltz's by the checked figures' mean ratio of counted to predicted shift. That ratio, from `deduce_check.json`: notes a bar 0.68, onsets on a beat 0.74, on the first beat 0.60, rhythm again 0.73; **mean 0.69**. So the shrunk table is the waltz's share plus 0.69 of the way to the deduced one, renormalised. The marks are the same for both runs.

The pop trial's first counts are committed beside its result as asked (`pop_3_4.json`).

## 749.235 (`LUTHIER_TITLE_NOWAIT=1`, unset by default)
A line that sings the title does not take 870's wait (the kept rest drawn before a fresh line where its slot leaves room). Nothing else changes.

**Trial:** song 52 as 749.232 stood (`LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=1`), with this switch. **Marks U1 to U4 unchanged** (the title lines on their bar line or before it in three builds of four; 840 and 780 each under one in ten; S2 to S5 and S7 on the living median and the pick). **Reported, as asked:** where a title line opens on unstressed syllables, how often it begins before its bar line, as a pickup.

Byte for byte, every switch unset, both runs: 54, 55, 52, song 53's Essen arm.

## What I expect
749.235: U2 and U3 met; the split said 840 is entry and nothing else. Four chances in five. 749.234: K1 met (the builds will be made). Then the pop marks are read for the first time: K2 to K5 likely; K6 within sections I cannot call; K3's first-beat stress at 0.45 likely met on the median under the shrunk table, less sure under the deduced one. One chance in three for all of K1 to K8 in either run.
