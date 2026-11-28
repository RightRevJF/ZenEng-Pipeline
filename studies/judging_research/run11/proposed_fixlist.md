# Proposed list from the judging research, run 11 (for the maintainer)

28 November 2026, the 02:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run11 on the judging-research branch: report.md, card_1.md, brainstorm.md, chair.md, first_principles.md, DATA.md, searches.md, and the folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 11" (https://claude.ai/artifact/JBikezVzGw8qak7o91mnVd); the pass's report is the Doc "Judging research, run 11" (https://claude.ai/artifact/B8pxpQjovxqaYyJC6QBpDf).

Nothing here is in the engine. Labels R11-1 to R11-5 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (a1011c4) and the thread before proposing, read only.**
- `songs/p68/fixlist_v54.md` is still the latest list; `lib/luthier/REVIEW_stage35.md` the latest review. Nothing there or in the thread proposes pitch-class entropy on pop melodies or the melody's spectral gap, so nothing below repeats a closed item.
- **The songwriting session's 20:22 post (to the research):** TheSession's licence forbids processing by large language models; withdraw run 10, open no split H, run no test on it, delete the dump, remove per-tune files, keep the ideas. **Done** (R11-1).
- **The maintainer's 20:29 and 20:33 posts:** the studies on main that read the dump carry WITHDRAWN.md; the data pack README on the maintainer's branch lists TheSession under sources not to use; Jason's word, "Take the deductions you gleaned from it and use those", read as: data untouched, ideas retested fresh. **Agreed and followed.** Its 20:15 check of run 10 is now moot (R11-1). On the page gate (fixes 922, 923): run 10 of this research supplied it no figure, and this pass tested none of its parts.
- The folk replication (branch folk-replication, 20:56 post): 473 open-source tunes, 18 estimates. It is the pitch-class-entropy test on an allowed folk source; it decided nothing.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R11-1 | Run 10 withdrawn (TheSession's licence): R10-1, R10-2, R10-3 and the TheSession part of R10-5 withdrawn | Withdrawal, done | No |
| R11-2 | Fewer different notes, within artist, on pop melodies: passed, thinly, on seen songs | Reading, rule first | Reading only |
| R11-3 | Unseen melodies with titles and artists: the data the next test needs | Data request | No |
| R11-4 | Fake outcomes for power should carry an artist share | Method | No |
| R11-5 | Seen-ledger lines for this pass | Data-pack note | No |
| Carried | R10-5 (pop part), R10-6 (1, 2), R09-3, R09-4, R09-5 (2), R08-3, R08-4, R05-5, R03-2, R02-4, J6c | | |

## In short

Run 10 is withdrawn for its data's licence; its ideas were retested fresh on the Hooktheory melodies (9,588 songs by 1,741 artists, compared within artist; seen songs, new measures). Five counted tests (K = 5, α .01), rules pushed at e1858c0 before any outcome, results at 1ffa3b6. Pitch-class entropy passed (−0.029 SD per SD, SE 0.011, p .0076); Jason's S on the melody (+0.001), the melody-chord table (−0.010), a typical scale-step profile (+0.002) and the early reach for the next chord (−0.004) were killed. Three estimates sat near zero. A late check on single-song artists leaned the same way (−0.025, unsettled) and turned positive with melody size held.

For the engine: one reading proposed (R11-2), no gate.

## Items

### R11-1 Run 10 withdrawn
**Status.** Done (answer to the songwriting session's 20:22 post).

**Problem.** TheSession.org's licence forbids processing the data with large language models; run 10 did.

**Evidence.** `coord/songwriting.md` 20:22 post; `tables/metre_atlas/research_report.md` on main (the clause flagged 14 November). This pass could not open the licence page itself and accepts the two reports.

**Fix.** Done on judging-research (b5f5dbe): `run10/WITHDRAWN.md`; every run 10 idea in `ideas.json` reset to "untested" with a withdrawal note. Split H was never opened. The dump is not on this machine and was not fetched again. The committed run 10 files hold no per-tune data (each result.json is about 3 KB of coefficients), so nothing needed removing; git history keeps them in any case. **Withdrawn: R10-1, R10-2, R10-3, and R10-5's "sealed 6/8 jigs" part.** R10-4 stands (it concerns run 09).

**Check.** `git show judging-research:studies/judging_research/run10/WITHDRAWN.md`.

### R11-2 Pitch-class entropy on pop melodies: a reading, thinly passed
**Status.** Reading, rule first. New. Fragile: read the caution.

**Problem.** Among one artist's songs, a melody that spends its time on fewer pitch classes was slightly more often recorded by another artist. It is McBride and Leroi's "simpler spreads", tested on an allowed source.

**Evidence.** `run11/experiments/rep_entropy/RESULT.md`: −0.029 (SE 0.011, p .0076, α .01), halves −0.010 and −0.046, conditional logit −0.164; the other twelve baselines and mel_ic_mean held −0.029 (p .16). **Cautions:** the songs were joined to other measures in runs 04 to 06; the frozen power (0.22) came from fake outcomes without an artist share, and the first-principles reviewer's rough sum says that with real errors K would have been 7 (α .0071), which p .0076 misses (R11-4); across artists (`rep_singletons_after`, after seeing results) −0.025 unsettled, +0.040 with size held.

**Fix.** For any lyric, read the kept songs' own melody pitch-class entropy first (10th, 50th, 90th), then the drafts' against it, and report drafts above the kept 90th. No gate, and none proposed until the measure passes on melodies never joined to an outcome (R11-3). The measure: `run11/experiments/common11.py`, `baseline()`, key `pc_entropy` (duration-weighted Shannon entropy of the twelve pitch classes, bits, clips of 12 or more notes).

**Check.** The kept songs' percentiles printed before any draft is read.

### R11-3 Data request: unseen melodies with titles and artists
**Status.** Data request. New.

**Problem.** Every allowed melody with a title and artist on the research's machine has now been joined to the outcome. R11-2's confirmation needs melodies never used, by artists with two or more songs; the first-principles reviewer's scaling says about 11,000 such songs for an even chance at −0.02.

**Evidence.** `run11/DATA.md`; `run11/first_principles.md`, section 5.

**Fix.** If your machine reaches them: the Lakh MIDI `lmd_matched` files (CC BY 4.0) whose MIDI has a track named melody, vocal, voice or lead, with their Million Song Dataset title and artist; leave out songs already in the Hooktheory rows, the McGill hold-out and main's shape sets (by title and artist, before anything is read); count the yield. Others to check for licence and size: POP909 (likely too small), OpenScore Lieder (CC0; art song). Commit the notes-side table without outcomes; the research freezes its rule (prediction −0.02, written in first_principles.md) before any match is made.

**Check.** The yield per artist printed; no outcome joined until the research's PREDICTION.md is pushed.

### R11-4 Fake outcomes for power should carry an artist share
**Status.** Method. The sessions settle; Jason may overrule.

**Problem.** The fake outcomes behind every "power" figure in runs 05 to 11 are drawn with no artist component, so with an artist fixed effect their errors run about a third larger than the real ones (this pass: fake 0.013 to 0.018, real 0.009 to 0.012). Power is understated, kills are firmer than stated, and K is set too low.

**Evidence.** `run11/experiments/*/power.json` against `result.json`; `run11/first_principles.md`, section 2.

**Fix.** From run 12: fake outcome = the real outcome's between-artist share drawn as an artist effect (estimated from the share of outcome variance between artists, which uses the outcome's distribution but not its relation to any measure) plus noise, or equivalently scale the fake SE by the real residual SD. Decide which before the next pass's predictions; if the first reads the outcome, the second is the safer.

**Check.** Recorded in run 12's chair.md before any power is computed.

### R11-5 Seen-ledger lines
**Status.** Data-pack note.

**Fix.** If wanted, in the pack's seen ledger: the 9,588 within-artist Hooktheory songs joined to eight more melody measures (rules e1858c0, results 1ffa3b6); the 3,610 single-song-artist songs joined to pitch-class entropy (rule 1ffa3b6, result 5d035a4).

**Check.** The ledger lines name the commits.

## Carried

- **R10-5, surprise against the fitted rhythm grammar.** The pop part stands: Hooktheory clips, fitted and tested on disjoint artist halves, once the pop form passes on its table. The TheSession part is withdrawn (R11-1).
- **R10-6 (1), the cap of eight waived when K already counts every frozen test.** Open; it did not bind this pass. **(2), confirmations only for tests reaching power 0.5.** Open (and R11-4 changes the power figures it reads). **(3), the poster's fixed effect:** dropped, TheSession is withdrawn.
- **R09-3, hold prior artist sets in late-cover readings.** Open.
- **R09-4, a Discogs dump newer than July 2024.** Open; neither machine reaches it.
- **R09-5 (2), title-plus-writer matches.** Open for chord corpora.
- **R08-3, chord repetition: no covers lean either way.** In force.
- **R08-4, early covers drive late covers sublinearly.** Open.
- **R05-5, the Hooktheory corpus is not hits only.** Open.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; data not on hand.
- **Dropped:** R10-1, R10-2, R10-3 (withdrawn, R11-1); R10-4 (a correction, accepted and done).

## Not proposed

- **Jason's S = 1 + g/π, in any form, as a reading.** Killed as a spectral gap (`gap_rooms`, +0.001) and, at Jason's request, in one more novel form: g as the coupling of melody and bass over whole Lakh songs (`s_coupling_after`, rule 344be9b, +0.017 against −0.03, killed). By Jason's rule of 28 November 2026 it is now out of consideration as a judge.
- **The melody-chord table, the typical scale-step profile, the early reach, self-teaching, the typical melody, beat peaks:** killed or near zero.
- **Any figure from run 10.**

## Sources

- Li, Y., A sharp higher-order Cheeger inequality, arXiv 2609.35369. https://arxiv.org/abs/2609.35369
- McBride, J. M. and Leroi, A. M., Population Ecology of Tunes, arXiv 2609.09501 (run 02's card 2; the idea behind R11-2). https://arxiv.org/abs/2609.09501
- Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
- Run 11 on judging-research: b5f5dbe (run 10 withdrawn), e1858c0 (predictions), 1ffa3b6 (results; the late rule), 5d035a4 (RESULT.md files; the late result).
- On main: `songs/p68/fixlist_v54.md`; `lib/luthier/REVIEW_stage35.md`; `coord/songwriting.md` (20:22 post); `coord/maintainer.md` on luthier-v8-stage1 (20:15, 20:29, 20:33 posts); branch folk-replication (`coord/folk_replication.md`).
