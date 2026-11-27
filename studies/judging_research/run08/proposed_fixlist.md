# Proposed list from the judging research, run 08 (for the maintainer)

27 November 2026, the 02:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run08 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, first_principles.md, DATA.md, searches.md, and the ten folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 08" (https://claude.ai/artifact/9erV8FEcZTmDGVk52j5FDj); the pass's report is the Doc "Judging research, run 08" (https://claude.ai/artifact/L9hE7vxc7Ryj4tBqHxCYWK).

Nothing here is in the engine. Labels R08-1 to R08-6 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (7f564dc) and the thread before proposing, read only.**
- `songs/p68/fixlist_v53.md` is the latest list (next finding 749.223 at its head); it carries no research item. `lib/luthier/REVIEW_stage35.md` is the latest review.
- `studies/judging_checks/run07/CHECK.md` and the maintainer's 21:10 post: R07-1 taken into the pack (`lakh_covers_discogs.json`, seen); R07-2 in force; R07-3 agreed (range kill, realised base rate) and the 0.2 floor already ruled; R07-4 recorded; one correction asked (the `tree_h4m` logit gave no reading), now written into `run07/experiments/tree_h4m/RESULT.md`.
- `coord/songwriting.md` (19:55 ET, to the research): asks that the test which ran before the logit fix be named. It is `lakh_repetition` (its earlier output is `result_before_logit_fix.json`); stated in the same note. No other ask is open for the research.
- Nothing on main proposes ChoCo, iReal Pro, Wikifonia, the ii-V share, chord-space neighbours or cover timelines, so nothing below repeats a closed item.
- **A slip, stated:** while finding the latest list, a version sort printed the first 30 lines of `songs/p69/fixlist_v35.md` (song 59's folder). Nothing from it was used; it is logged in `run08/experiments/HOLDOUT_LOG.md`.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R08-1 | 8,640 ChoCo songs matched to Discogs-VI: a commit-ready table and two seen-ledger lines | Data-pack note | No |
| R08-2 | The ii-V share passed (and again on unseen songs): a reading of Luthier's chord drafts against kept songs, no gate | Reading, rule first | Reading only |
| R08-3 | Chord repetition killed on fresh songs with power: no covers lean either way | Reading caveat (continues R07-2) | Reading only, no gate |
| R08-4 | Early covers drive late covers with slope 0.91: hold early covers when reading late ones | Method note | No |
| R08-5 | Two method questions: a consistent count K, and a held-back confirmation batch | Method | No |
| R08-6 | Data request: chord charts with composers written before the covering | Data request | No |
| Carried | R06-4 (updated), R05-5, R03-2, R02-4, J6c | | |

## In short

The research found a chord corpus with songwriters that its machine can reach: ChoCo (Zenodo 7706751, CC BY 4.0), its iReal Pro and Wikifonia charts. Matched to Discogs-VI by title and a writer's name, and after removing seen songs and the McGill hold-out, it gave 8,640 unseen songs: 5,907 by 1,199 composers with two or more, and 2,733 by single-song composers. The outcome was the number of distinct artists who recorded the song (log), within composer, genre and decade held. Eight tests were frozen at e624a7e before any outcome was joined; five counted at p < .05/5 (later .05/6), each with power 0.21 to 0.65.

Two counted tests passed: the ii-V share (+0.073 SD per SD, SE 0.018) and chord-space heritability (+0.051 over a within-cell neutral null, p .0002). Written after seeing those (rule b1b3512), the ii-V share passed again on the 2,733 unseen single-composer songs (+0.057, SE 0.019), mostly in jazz genres (+0.087 against +0.021 elsewhere). Chord repetition (W01-J1) was killed (−0.003 against −0.04, power 0.49), as were key travel (circular optimal transport) and the neutral-copying slope.

For the engine nothing changes yet. The ii-V lead is most likely about tunes as jazz players use them; for pop and folk songs its estimate is small and unsettled.

## Items

### R08-1 The ChoCo songs: matched, and now seen
**Status.** Data-pack note. New.

**Problem.** The pack holds no lead-sheet chord charts with songwriters. Tonight the research built 8,640 from ChoCo and matched them to Discogs-VI; they are now spent.

**Evidence.** `run08/experiments/common.py` (`build_design`: the match rule, exclusions and composer key in its header); `run08/experiments/parse_choco.py`. Matching: 22,290 charts matched; 3,809 fell on seen cliques and 244 on McGill hold-out songs, all dropped before anything was read. The table is `studies/judging_research/data/choco_songs_discogs_run08.json` (3.4 MB; CC BY-SA 4.0 as derived from Discogs-VI; ChoCo CC BY 4.0).

**Fix.**
1. If wanted, copy the table into the pack as `choco_covers_discogs.json`, marked seen.
2. Add two seen-ledger lines: the 5,907 within-composer ChoCo songs (run 08, rules e624a7e) and the 2,733 single-composer ChoCo songs (run 08, rule b1b3512).
3. Note the source: `smashub/choco-v1.0.0.zip`, Zenodo 7706751. Its Billboard partition is the McGill charts' source: anyone using ChoCo must leave it out.

**Check.** The ledger lists both sets; `build_design()` reproduces the table's cliques.

### R08-2 The ii-V share: a reading of Luthier's chord drafts, no gate
**Status.** Reading, rule first. New. A passed experiment, read against kept songs, deciding nothing yet.

**Problem.** The ii-V share (changes from a minor seventh to a dominant seventh a fourth up, over all chord changes) is the first notes measure to pass a counted test and to pass again on unseen songs. Luthier's chord drafts have never been read on it.

**Evidence.** `run08/experiments/iiv_chunk/RESULT.md` (+0.073, SE 0.018, p 4e-5; halves +0.096 and +0.054; Poisson +0.124); `iiv_singletons/RESULT.md` (after seeing results: +0.057, SE 0.019; jazz genres +0.087, SE 0.034; other genres +0.021, SE 0.022); `cover_timeline/result.json` (holding early covers, IIV predicts nothing about late covers: +0.006, SE 0.032); `iiv_source/RESULT.md` (power 0.06: cannot separate the song from the chart writer).

**Fix.** Rule first, before any reading: compute IIV (`run08/experiments/measures.py`, `listener_measures`) on the chord drafts of the seen engine songs and on the kept songs of the same style tables; report where each song falls in the kept 10th to 90th. A gate only if a draft stands outside the kept range, and only for a lyric that asks for a jazz or songbook style. For pop, rock and folk songs: report only (their estimate is unsettled).

**Check.** A reading posted with its rule committed first; no default changes.

### R08-3 Chord repetition killed on fresh songs: no covers lean either way
**Status.** A caveat on readings. Reading only, no gate. Continues R07-2.

**Problem.** The research's one seen-song pass (W01-J1: −0.042 per SD within artist on Hooktheory) did not replicate on 5,858 fresh ChoCo songs with power 0.49: −0.003 (SE 0.014, p .84), halves +0.002 and −0.007. Run 07 found it reversed on MIDI (−1.93 pp); run 06 found +1.32 pp on "taken up at all".

**Evidence.** `run08/experiments/chrep_confirm/RESULT.md`; `run07/experiments/lakh_repetition/RESULT.md`; `studies/judging_checks/first_performers/RESULT.md`.

**Fix.** Keep citing covers for neither side of any loop gate (749.185 and successors), now firmly: on fresh, powered songs the lean is zero.

**Check.** The next loop-gate report carries no cover-based mark.

### R08-4 Early covers drive late covers, sublinearly
**Status.** Method note. New.

**Problem.** Card 2 (Evans and Giometto) shows content-free copying can make hits. On 4,020 ChoCo songs first recorded 1950 to 1994, new artists in years 10 to 29 rose with early artists (years 0 to 9) at slope 0.907 on the log scale (SE 0.030): below the pure-copying 1 and far below the predicted 1.10. A copying urn reproduces about half of the late-cover spread; at most 48% is left for anything about a song (fame, publishers, notes and errors share it).

**Evidence.** `run08/experiments/cover_timeline/RESULT.md` and `result.json`.

**Fix.** Any reading that uses late covers (by period) holds early covers; any claim that a measure drives covers says whether it predicts late covers given early ones (none did tonight).

**Check.** None needed.

### R08-5 Two method questions
**Status.** Method. The sessions settle; Jason may overrule.

**Problem.**
1. **No consistent K.** Counting only tests with power 0.2 at .05/K had no fixed point tonight (seven cleared at K = 5, five at K = 7). The chair froze K = 5 by a written rule and left two tests above the floor as estimates.
2. **Nothing held back.** Testing every idea on all 8,640 songs left only 542 unseen songs (power 0.04) for a confirmation.

**Evidence.** `run08/chair.md` (the K table); `run08/first_principles.md` sections 2 and 5.

**Fix.** Proposed: (1) K = the number of frozen tests whose power is 0.2 or more at .05 divided by the number of frozen tests (one pass, no iteration; slightly conservative). (2) Each new corpus is split once by a hash of the clique id: two thirds for the pass's tests, one third sealed for confirming a pass.

**Check.** Recorded in the next chair.md.

### R08-6 A data request: chord charts written before the covering
**Status.** Data request. New; replaces R06-4's corpus request.

**Problem.** iReal Pro charts are written by the jazz players whose recordings are the outcome, so a chart may carry the covering (ii-Vs added to tunes already played). A confirmation needs chords with title and composer from a source upstream of covers.

**Evidence.** `run08/experiments/iiv_source/RESULT.md`; `run08/DATA.md` ("Still missing").

**Fix.** If the maintainer's machine reaches any: a corpus of first-edition sheet music or publisher lead sheets with chord symbols, title and composer (several thousand songs). None was found on Zenodo or GitHub tonight. ChoCo's Real Book and Band-in-a-Box partitions (in the same zip) are not upstream either, but could serve as a check of chart-writer agreement.

**Check.** A named file, or "not reachable" in the thread.

## Carried

- **R06-4, a larger chords corpus with names.** Updated: ChoCo gave the size (8,640 matched) but is written by the covering community; R08-6 now carries the request.
- **R05-5, the Hooktheory corpus is not hits only.** Open and unchanged.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand. R08-4 gives a different ceiling (copying momentum).
- **Dropped:** R07-1 (done on main); R07-2 (in force; R08-3 continues it); R07-3 (agreed; applied tonight); R07-4 (a record; tonight's record is in the report).

## Not proposed

- **Key travel, transport economy or tonic resistance as readings:** killed, or estimates against their predictions.
- **Chord repetition as a gate in either direction:** zero on fresh, powered songs.
- **The ii-V share as a default for the writer's songs:** its lead is in jazz genres; for his styles it is unsettled.

## Sources

- Rabin, J., Delon, J. and Gousseau, Y. (2011), Transportation distances on the circle, arXiv 0906.5499. https://arxiv.org/abs/0906.5499
- Evans, T. S. and Giometto, A. (2011), Turnover rate of popularity charts in neutral models, arXiv 1105.4044. https://arxiv.org/abs/1105.4044
- ChoCo v1.0.0 (de Berardinis et al. 2023), Zenodo 7706751, CC BY 4.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), Zenodo 13983028, CC BY-SA 4.0.
- Run 08 on judging-research: e624a7e (eight predictions), b1b3512 (first eight results and two after-seeing-results predictions), cb782eb and 516fb85 (the iiv_singletons second-model fixes), e913c96 (their results), e019974 (RESULT.md files).
- On main: `songs/p68/fixlist_v53.md`; `lib/luthier/REVIEW_stage35.md`; `studies/judging_checks/run07/CHECK.md`; `coord/songwriting.md`; `coord/maintainer.md` (branch luthier-v8-stage1).
