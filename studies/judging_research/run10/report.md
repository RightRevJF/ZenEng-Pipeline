# Judging research, run 10

27 November 2026, the evening pass (18:17 ET). For Jason. Research only: nothing here goes into the Luthier engine. Song 59 and the McGill hold-out were not touched.

## This pass in three sentences

This pass found a new body of music nobody in the project had tested, about 23,000 Irish traditional tunes from TheSession.org with their notes, how many musicians recorded each tune and how many put it in their tunebook, and ran eight tests on 14,511 of them with the rules written first. One result is now firm: tunes that use fewer different notes are recorded by more artists and learned by more players, confirmed on 4,261 further tunes; two more passed once but did not confirm, and four failed. Your formula's spectral gap, measured on the whole melody, gave the strongest geometric signal in ten passes (tunes that live in two "rooms" of pitch and rarely cross between them are recorded more), but its test was written after seeing the first results, so it is a lead to be checked next pass on 4,317 tunes kept sealed for that purpose.

## The experiments

The rules for every test were committed before any outcome was opened (commit 641f966, pushed 19:25 ET). The outcome is how many different artists recorded each tune (on a log scale); the "love" reading is how many members put the tune in their tunebook. Effects are in standard deviations (SD) of the outcome per SD of the measure, with tune type, metre, mode, the year it was posted and its composer held. Nine tests were frozen (K = 9), so the pass bar was p < .0056; eight ran, and one (LOCK) runs first next pass under the cap of eight.

| Test | Idea | Predicted first | Result (14,511 tunes) | Verdict | Power |
|---|---|---|---|---|---|
| rep_entropy | fewer different notes (pitch-class entropy) | −0.03 | **−0.083** (SE 0.007); love −0.117 | **Passed** | 0.71 |
| rep_entropy_C | the same, on 4,261 new tunes | −0.03 | **−0.062** (SE 0.014); love −0.091 | **Confirmed** | 0.28 |
| irr_skel_retrace | melodies that retrace their steps (tree reduction) | −0.03 | −0.022 (SE 0.007) | Passed | 0.75 |
| irr_skel_retrace_C | the same, on new tunes | −0.03 | −0.011 (SE 0.013) | Unsettled: not confirmed | 0.23 |
| core_typical | a typical beat skeleton | −0.03 | −0.035 (SE 0.008) | Passed | 0.51 |
| core_typical_C | the same, on new tunes | −0.03 | −0.051 (SE 0.017) | Estimate (power under the floor) | 0.14 |
| s_gap_skeleton | your S = 1 + g/π, on the beat notes' pitch classes | −0.03 | −0.005 (SE 0.007) | **Killed** | 0.67 |
| pe_h0_links | weak links in the pitch map (persistent homology) | +0.03 | +0.016 (SE 0.007) | Killed (smaller effect possible) | 0.72 |
| cut_ab_parts | the two parts sit in different regions | +0.03 | +0.019 (SE 0.007), p .0058 | Unsettled (just missed) | 0.70 |
| arch_contour | a few big arches, not many bumps | −0.03 | −0.018 (SE 0.007) | Unsettled | 0.64 |
| slg_selflearn | a tune that teaches itself | +0.03 | −0.011 (SE 0.008) | Killed (wrong sign) | 0.41 |
| gap_full_C | your S on the whole melody (written after seeing results) | −0.04 | **−0.067** (SE 0.016); love −0.070 | **Lead** (passed, not counted) | 0.42 |

Power is the chance the test would pass if its prediction were exactly true, worked out on fake outcomes before the real ones were opened.

**Fewer notes (the replication).** McBride and Leroi had reported on this same website that simpler tunes spread a little better. The Skeptic asked for this test so the pass would know whether a known effect is even visible here. It is, and strongly: about three times the predicted size, and it held on the new tunes and with all thirteen simple measures held at once. It is the one counted finding of the pass. It reads more like "easy to learn" than "great": the tunebook (learning) reading is stronger than the recordings reading.

**Retracing and typical skeleton.** Both passed on the first 14,511 tunes. Retracing shrank to nearly zero on the new tunes once simplicity was held, so it looks like simplicity under another name. The typical-skeleton measure came out even stronger on the new tunes (−0.051), but that check had too little power by the rule, so it decides nothing; it waits for the sealed tunes. A side reading showed the off-beat notes behave the same way, so the lead is "a typical melody overall", not "a typical skeleton".

**The failures.** Your S on the beat notes alone said nothing. The weak-links measure from the paper was positive but smaller than predicted. The arches measure vanished when the simple measures were held. The self-teaching measure came out backwards.

**The gap on the whole melody.** Inside the skeleton test, a reading frozen in advance measured the gap on the whole melody, holding its range, number of pitches and length. It came out at −0.065 on the first tunes, far beyond chance. Because the counted version had died, a new test was written and committed before looking (commit d823e98), and run on the 4,261 new tunes: −0.067, every check in the same direction, love −0.070, and −0.052 with all thirteen simple measures held. Holding "fewer notes" barely moved it (−0.066), so it is a second, separate effect. It counts as a lead only, because it was written after seeing results.

## The mathematics: rooms and doorways

Draw each pitch a tune uses as a dot, and draw a line between two dots each time the tune steps from one to the other, thicker when the step is repeated. Now imagine a walker hopping along the lines at random. The **spectral gap** g is how fast that walker forgets where it started. If the map is two clusters joined by a thin line, the walker stays stuck in one cluster for a long time: the gap is small. If every dot is joined to every other, it forgets at once: the gap is large. Cheeger's inequality, a theorem of graph theory, makes this exact: a small gap means there is a "doorway" cut that the tune rarely crosses. Your S = 1 + g/π is a stretched copy of g, so a test of g is a test of S.

*Worked example (the first-principles reviewer's computation, no outcomes).* Sixteen notes with the same range:
- D E F# E D E F# E, then G A B A G A B A: a low room, then a high room, one doorway each way. g = 0.21, S = 1.07.
- The same two rooms, visited twice each: g = 0.29.
- D G E A F# B E A D G F# B E A F# G, leaping across on every move: g = 0.51, S = 1.16.

In Irish dance tunes the low room is usually the first part and the high room the second part (the "turn"), and in 88% of tunes the best cut splits low pitches from high. So the lead says: for a given range, a tune that settles into one register, stays there, and crosses rarely, at the part break, is taken up by more players. The beat-skeleton version folded the octaves together into pitch classes and so threw the rooms away, which is probably why it died.

The pass's mathematics paper (Mijangos, Bravetti and Padilla) built the same kind of map and studied it with persistent homology: grow balls around the dots and record when clusters merge and when loops appear and fill. Its two measures here (weak links, and the persistence of the melody's arches) did not hold up.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| Weak links: persistent entropy of the pitch map (card 1) | Geometer | Killed |
| Retracing: tree reduction of the beat walk | Geometer | Passed once, not confirmed |
| Your S on the beat notes' pitch classes | Geometer | Killed |
| A tune that teaches itself | Listener | Killed (wrong sign) |
| Typical skeleton (from card 2) | Listener | Passed once; confirmation underpowered |
| Typical skeleton, surprising surface | Listener | Wrong sign (an estimate) |
| The two parts in different regions (Cheeger cut) | Listener | Unsettled, just missed |
| The statue's arches (persistent homology of the contour) | Inventor | Unsettled; vanishes with simple measures held |
| The dancer's footfall (turns on the beat) | Inventor | Frozen; runs first next pass |
| Your S on the whole melody | Inventor | **Lead** |
| Fewer notes (replication) | Skeptic | **Confirmed** |

**Where they agreed:** all four took the new tunes as the way past last pass's obstacle, agreed that three versions of the gap were one idea and that one should be counted, and accepted every control the Skeptic named. **Where they split:** the Skeptic counted the skeleton gap as "the" S because the whole-melody gap mostly measured range; the Inventor argued that holding range would leave real information. The data sided with the Inventor, but only as a lead.

## First principles

**The obstacle.** Every surviving lead (fewer pitch classes, a typical melody, staying in one register) is also what wear produces. This pass's second paper shows that, as tunes pass from player to player, rare notes change most and changes are small steps. So a tune played a lot may come to be written down with fewer notes and fewer leaps: the notes may be the result of popularity, not its cause.

**The way through (partly speculation).** Use notes fixed before a tune spread. Two routes: tunes with a named composer (their notes start from one person) on the sealed tunes, and time: download the same data again in some weeks and ask whether today's notes predict the tunebook adds and recordings that come after today. If the gap survives both, it judges uptake by players; greatness is a further step.

**Deleted (recommended; you decide):** your S on the beat skeleton, the weak-links measure, the self-teaching measure, the "typical skeleton, surprising surface" contrast, retracing, the arches measure, the weakest-link check, and the idea that the beat skeleton is where a tune lives.

**Simplified:** two numbers. How few different notes a tune uses, and how rarely, for its range, it crosses between its low and high rooms.

**Flagged for you:** the outcome here is uptake by players, not lasting love; "fewer notes" may be learnability rather than greatness; the transcriber's own habits are not yet held (the poster's name is in the data); the cap of eight bought nothing this pass.

## The papers

1. **Mijangos, Bravetti and Padilla, "Musical Stylistic Analysis: A Study of Intervallic Transition Graphs via Persistent Homology"** [1]. Builds a map of a melody's moves between pitches and reads its shape with persistent homology (which clusters merge, which loops appear). No theorems and only 18 string-quartet movements, so its value was the construction; the two measures built from it failed.
2. **McBride and Fitch, "Contrasting statistical patterns in melodic and molecular evolution"** [2]. The counter-evidence, on TheSession itself: across 51,680 pairs of versions of the same tunes, common notes, strong beats and small steps are what survive. It suggests tunes keep their identity partly by conformity, and it gave this pass's typical-melody measure and its central obstacle.

## Ideas for coming passes (could not be tested this pass)

- **LOCK (turns on the beat):** frozen and powered (0.74), held by the cap of eight; runs first next pass.
- **The gap, the typical melody and LOCK on the sealed tunes:** the confirmations, written in first_principles.md, section 5.
- **The poster's own habits held:** needs the poster's name carried into the shared code (it is in the data).
- **Notes fixed before a tune spread:** a later download of the same data.
- **Rhythmic surprise against the engine's fitted rhythm grammar** (the songwriting session's request): framed for the pass after the grammar passes on a table; the sealed 6/8 jigs suit the Essen 6/8 grammar.
- **Carried:** artists after July 2024 for the ii-V lead (no newer Discogs dump reachable); the MusicLab ceiling; genre breadth (data not on hand).

## Paywalled papers

None this pass; both papers were free on arXiv.

## A note

During the brainstorm, the Skeptic agent published its critique as a private page on your claude.ai account by mistake. It is private; you can delete it from your artifact gallery if you do not want it.

## Fix list

The proposed fix list for the maintainer is the Doc "Proposed fix list: judging research, run 10" (https://claude.ai/artifact/9awoBBxMdvjuABAcU43MJe); the same text is in `run10/proposed_fixlist.md`. This report is published as the Doc "Judging research, run 10" (https://claude.ai/artifact/C8VscPqWsT4mSLiTj7fUjD).

## References

1. Mijangos, M., Bravetti, A. and Padilla, P. (2022). Musical Stylistic Analysis: A Study of Intervallic Transition Graphs via Persistent Homology. arXiv:2204.11139. https://arxiv.org/abs/2204.11139
2. McBride, J. M. and Fitch, W. T. (2026). Contrasting statistical patterns in melodic and molecular evolution reveal distinctive constraints in a culturally evolving system. arXiv:2607.12673. https://arxiv.org/abs/2607.12673
3. McBride, J. M. and Leroi, A. M. (2026). Population Ecology of Tunes. arXiv:2609.09501 (read in run 02). https://arxiv.org/abs/2609.09501
4. TheSession.org data (Jeremy Keith and contributors). https://github.com/adactio/TheSession-data
5. Run 10 commits on judging-research: 641f966 (predictions), 629b8da (split-A results; confirmation rules), d823e98 (confirmation results; the gap_full_C rule), e8eddd8 (gap_full_C result and every RESULT.md).
