# Judging research, run 11

28 November 2026, the early pass (02:17 ET). For Jason. Research only: nothing here goes into the Luthier engine. Song 59 and the McGill hold-out were not touched. Published as the Doc "Judging research, run 11" (https://claude.ai/artifact/B8pxpQjovxqaYyJC6QBpDf); this file says the same.

## This pass in three sentences

This pass tested eight ideas on the melodies of 9,588 pop songs by 1,741 artists (Hooktheory), comparing each artist's songs with one another, with every rule written and pushed before any result was opened. One idea passed: among one artist's songs, the ones whose melody spends its time on fewer different notes were more often recorded by another artist (−0.029 standard steps per step, p .0076 against a bar of .01); your S = 1 + g/π on the melody, and three other new ideas, were killed. The pass is real by its own rules but thin: these songs had been used before, the effect is small, and it would not have cleared the bar if the power had been worked out a little more accurately, so it needs melodies never used before to count as a finding.

Last pass's corpus (TheSession.org) is withdrawn for its licence, and none of its figures is used here.

## The experiments

One of five counted tests passed; four were killed; three estimates and one late check decided nothing. The rules were committed at e1858c0 (03:10 ET) before any outcome was joined; the results are at 1ffa3b6. The outcome is whether another artist recorded the song (a Discogs-VI version by a performer sharing no name with the original), compared within each artist. Effects are in standard steps of the outcome per standard step of the measure. Five tests were counted, so the bar was p < .01.

| Test | Idea | Predicted first | Result (SE) | Verdict | Power |
| --- | --- | --- | --- | --- | --- |
| rep_entropy | fewer different notes (pitch-class entropy) | −0.03 | **−0.029** (0.011), p .0076 | **Passed** | 0.22 |
| gap_rooms | your S = 1 + g/π on the melody | −0.03 | +0.001 (0.011) | Killed | 0.22 |
| tie_rooms | each chord owns its own melody notes | +0.03 | −0.010 (0.009) | Killed | 0.33 |
| typ11_typical | the melody's time on each scale step is typical | +0.03 | +0.002 (0.009) | Killed | 0.39 |
| ant_push | the melody reaches the next chord early | +0.03 | −0.004 (0.011) | Killed | 0.28 |
| slg_selflearn | a song that teaches itself (estimate) | +0.03 | −0.010 (0.011) | Estimate | 0.23 |
| core_typical | a typical melody (estimate) | −0.03 | +0.002 (0.012) | Estimate | 0.19 |
| lockp_peaks | melody peaks land on strong beats (estimate) | +0.02 | +0.007 (0.009) | Estimate | 0.13 |
| rep_singletons_after | fewer notes, artists with one song (after seeing results) | −0.03 | −0.025 (0.016), p .12 | Lead: unsettled | 0.38 |

Power is the chance a test would pass if its prediction were exactly true, worked out on fake outcomes before the real ones were opened. "Killed" means the predicted size lies outside the result's 95% range: the effect, if any, is smaller than predicted.

**Fewer notes (passed).** Among one artist's songs, a melody that spends its time on fewer pitch classes was a little more often taken up by another artist. Both halves of the artists leaned the same way (−0.010 and −0.046) and so did the second model. Holding the other twelve simple measures kept the size (−0.029) but not the significance (p .16). It is the McBride and Leroi idea, tested here for the first time on an allowed source.

**Why it is thin.** These 9,588 songs had already been joined to other measures in runs 04 to 06, so this is a new measure on used songs. The fake outcomes used for power left out how much songs differ between artists, so the real errors came out about a third smaller than planned. That makes the kills firmer than stated. But the reviewer's rough sum says seven tests, not five, would then have been counted, the bar would have been p < .0071, and 0.0076 would have missed it. By the rule written first, it passed; by a hair.

**The late check.** On the 3,610 songs by artists with only one song here, the same measure leaned the same way (−0.025) but did not reach significance, and it turned positive (+0.040) once melody size was held. Across artists, "fewer notes" cannot yet be told apart from "a smaller melody".

**Your S, and the three other kills.** The spectral gap of the melody's pitch map came out at zero (+0.001), with or without range and length held. The melody-chord measure, the typical scale-step profile and the early reach for the next chord all sat near zero. Every reading of the rooms family (higher rooms, the crossing count, the Cheeger constant, run 10's cut) was zero or the wrong way.

**The estimates.** The self-teaching and typical-melody measures and the beat-peak measure were too weak in power or too unstable between sections to count. All three came out near zero.

## The mathematics: rooms, doorways, and how many notes

This pass's mathematics says a melody's pitch map can be split into "rooms", and the experiments say that on pop melodies the rooms do not tell songs apart.

**The map.** Draw each pitch a melody uses as a dot. Draw a line between two dots each time the melody steps from one to the other, thicker when the step repeats. Now picture a walker hopping along the lines at random. The spectral gap g is how fast the walker forgets where it started. Your S = 1 + g/π is a stretched copy of g, so a test of g is a test of S.

**The theorem.** Cheeger's inequality says a small gap means the map has two rooms joined by a thin doorway. Li's 2026 paper (card 1) proves the same for any number of rooms: if the k-th number in the map's spectrum is small, the map has k rooms, each with thin doorways, and the loss in the bound is as small as it can possibly be. That let the Geometer score all of a melody's rooms, not just the best two.

*Worked example (the gap computed on three made-up 16-note tunes, same range):*

| Tune | g | S |
| --- | --- | --- |
| D E F# E D E F# E, then G A B A G A B A (low room, then high room) | 0.21 | 1.07 |
| The same two rooms, visited twice each | 0.29 | 1.09 |
| D G E A F# B E A D G F# B E A F# G (leaping across every move) | 0.51 | 1.16 |

**What the data said.** On these pop clips, the part of g that stays the same from verse to chorus is mostly how many pitches the melody uses. Once size was held, what was left changed from section to section and predicted nothing (+0.001). Every room measure did the same. The Geometer's honest summary: the theorem is true, and on melodies this short its numbers mostly count notes.

**The measure that passed is simpler.** Fold every note to its letter name, add up the time spent on each, and ask how spread that time is (Shannon entropy, in bits). Zero bits is one note held throughout; 3.58 bits is all twelve notes evenly. Two raised to the bits is the "effective number of notes".

| Tune (16 beats) | Time per note | Entropy | Effective notes |
| --- | --- | --- | --- |
| Mary Had a Little Lamb | E 6, D 6, G 3, C 1 | 1.76 bits | about 3.4 |
| Twinkle, Twinkle (two lines) | C 4, G 4, A, F, E, D 2 each | 2.50 bits | about 5.7 |

A possible reason it matters (speculation): every extra note is one more thing to learn by ear, so a narrower tune is picked up sooner. Twinkle is loved too, so this is a lean, not a rule.

## The brainstorm

Three imaginers proposed nine measures; the Skeptic merged them to five counted tests, and the chair added three of run 10's ideas as estimates.

| Idea | Stance | Status |
| --- | --- | --- |
| GAP: your S on the whole clip melody | Geometer | Killed |
| ROOMS: all the melody's rooms (card 1) | Geometer | Withdrawn into GAP; reading zero |
| TIE: each chord owns its melody notes (bipartite spectrum) | Geometer | Killed |
| HB: the same idea, built independently | Inventor | Merged into TIE |
| SETTLE: the melody stays in its rooms | Listener | Withdrawn into GAP; reading came out the wrong way |
| TYP11: a typical scale-step profile | Listener | Killed |
| REP: fewer different notes | Listener (run 10's idea) | **Passed** |
| ANT: the melody reaches the next chord early | Inventor | Killed |
| LOCKP: melody peaks on strong beats | Inventor | Stopped at the stability gate; estimate near zero |
| BIP: near two-sided (the dual Cheeger bound) | all three | Stopped: unstable from section to section |
| Self-teaching, typical melody | run 10's ideas | Estimates near zero |

**Where they agreed.** All four took the withdrawal of run 10 as settled and retested its ideas fresh, with no run 10 figure as a prior. All agreed that GAP, ROOMS and SETTLE are one idea (they correlate 0.8 to 0.9) and counted it once, and that TIE and HB are one measure (0.96). The Geometer withdrew its first prediction (−0.04) as anchored on the withdrawn figures and froze −0.03.

**Where they split.** The Skeptic showed that GAP's stability between sections falls under the bar once size is held, and wanted that to decide; the chair kept the standing gate on the raw measure, and GAP passed it by 0.0004. The data then sided with the Skeptic. The Listener warned against its own sign for SETTLE, since musicians on Hooktheory lean toward melodies that move; the reading came out negative, as it feared.

## First principles

**The obstacle.** The one lead left is small, sits on songs already used, passes only because five tests were counted, and across artists cannot be told apart from melody size. Every allowed melody with a title and artist on this machine is now spent.

**The way through (speculation).** New melodies with titles and artists, never joined to an outcome, compared within artist, with the power sums mended first. The reviewer's choice is the Lakh MIDI files that carry a melody or vocal track (CC BY 4.0), fetched by the maintainer, leaving out every song already used. About 11,000 within-artist songs would be needed for an even chance at the expected size. Another road skips covers entirely: test learnability directly, by how quickly people can sing a tune back.

**The next test, written now.** On melodies never used, within artist: fewer different notes predicts uptake by another artist at **−0.02** (shrunk from this pass's −0.029, since first passes tend to overstate). Killed if −0.02 lies outside the 95% range. A reading with melody size held tells "fewer notes" from "smaller tunes".

**Deleted (recommended; you decide).**

- **Your S = 1 + g/π as a judge.** It has now had two fair tests on allowed data: as a scaling exponent in main's shape study, and as the melody's spectral gap here. Popular tunes do sit near the point you predicted; how near did not tell songs apart. It was worth trying, and the reviewer recommends closing it as a judge.
- **The rooms family** (higher rooms, settling, the Cheeger cut, run 10's skeleton gap, weak links, retracing, arches): zero or the wrong way.
- **TIE / HB, TYP11, ANT:** near zero. **Self-teaching:** wrong sign throughout. **Typical melody:** only carries the note count. **Beat peaks, near two-sided:** unstable.

**What is left of the geometry.** A true theorem and a vocabulary. On short clips, the stable part of every pitch-map number is size. The reviewer recommends ending the pitch-map line and spending geometry, if at all, on whole songs.

**Simplified.** One number: how few pitch classes a melody spends its time on, among one artist's songs. Its plainest twin, the count of pitch classes, leans the same way (−0.021, p .031).

**Flagged for you.**

- The power sums leave out the artist share; fixing them before the next pass is free.
- The songs have now been reused across many passes, and each pass's bar counts only its own tests.
- The stability gate compares verse with chorus, so it rewards "the same everywhere", not "real".
- The outcome is uptake by another artist, a covers reading; lasting love is still unmeasured.

## Run 10 withdrawn

Run 10's findings are withdrawn: the TheSession.org data forbids processing by large language models, and this research is run by one. The songwriting session raised it after run 10 posted; the metre atlas report on main had flagged the same clause on 14 November. This pass could not open the licence page from its machine, and accepts the two independent reports.

- No run 10 figure is evidence any more, and none is used in this report or the fix list. Split H was never opened, and the data was not downloaded again.
- The committed run 10 files hold only rules, code and summary numbers, no per-tune data. A note, `run10/WITHDRAWN.md`, now says all this; nothing else there was changed.
- Following your word to the maintainer (keep the deductions, not the data), run 10's ideas were retested here from scratch. Four of them (your S on the melody, the typical melody, self-teaching, beat peaks) came out at zero on pop songs; fewer notes passed.

## The paper

**Li, "A sharp higher-order Cheeger inequality" (2026)** [1]. It proves, for any weighted graph, that the k-th eigenvalue of the normalised Laplacian bounds how well the graph splits into k rooms, with a loss of only the square root of log k, and shows by an example that this loss cannot be removed. The constant is not computed, the proof shows the rooms exist without saying how to find them, and the paper is not yet peer reviewed; it says it was written with AI help and that L. C. Lau found the same bound independently. Here it justified reading the melody's whole spectrum as a count of rooms (the ROOMS measure). On pop clips that count turned out to be mostly the number of pitches.

Only one paper this pass. The counter-evidence slot was filled in run 10 (McBride and Fitch, read as a paper, not as evidence on that data); the next is due by run 13.

## Coming passes, the fix list, references

**Ideas that could not be tested this pass, and why.**

- **Fewer notes on melodies never used** (the next test, prediction −0.02 written in first principles): needs new melodies with titles and artists; asked of the maintainer as R11-3.
- **Surprise against the engine's fitted rhythm grammar** (the songwriting session's request): waits until the pop form of the grammar passes on its table.
- **Lasting love, as distinct from uptake:** needs plays or covers by year on songs not yet used.
- **Carried:** artists after July 2024 for the ii-V lead (no newer Discogs dump reachable); the MusicLab ceiling; genre breadth (data not on hand).

**Paywalled papers.** None this pass; the paper was free on arXiv.

**Fix list.** The proposed list for the maintainer is the Doc "Proposed fix list: judging research, run 11" (https://claude.ai/artifact/JBikezVzGw8qak7o91mnVd); the same text is in `run11/proposed_fixlist.md`.

**References.**

1. Li, Y. (2026). A sharp higher-order Cheeger inequality. arXiv:2609.35369. https://arxiv.org/abs/2609.35369
2. McBride, J. M. and Leroi, A. M. (2026). Population Ecology of Tunes. arXiv:2609.09501 (read in run 02). https://arxiv.org/abs/2609.09501
3. Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun and Liang 2022), CC BY-NC-SA 3.0; Discogs-VI 20240701 (Araz, Serra and Bogdanov 2024), CC BY-SA 4.0, https://zenodo.org/records/13983028
4. Run 11 commits on judging-research: b5f5dbe (run 10 withdrawn), e1858c0 (predictions, before any outcome), 1ffa3b6 (results of the eight; the late rule), 5d035a4 (every RESULT.md; the late result).
