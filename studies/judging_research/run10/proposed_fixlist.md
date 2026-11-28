# Proposed list from the judging research, run 10 (for the maintainer)

27 November 2026, the 18:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run10 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, first_principles.md, DATA.md, searches.md, and the folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 10" (https://claude.ai/artifact/9awoBBxMdvjuABAcU43MJe); the pass's report is the Doc "Judging research, run 10" (https://claude.ai/artifact/C8VscPqWsT4mSLiTj7fUjD).

Nothing here is in the engine. Labels R10-1 to R10-6 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (f0f35a3) and the thread before proposing, read only.**
- `songs/p68/fixlist_v54.md` is still the latest list; `lib/luthier/REVIEW_stage35.md` the latest review. Nothing on main or in the thread proposes TheSession data, pitch-class entropy or a spectral-gap reading, so nothing below repeats a closed item.
- The maintainer's check of run 09 (12:25 post): rule first holds, figures match, K = 1 right. Two cautions: the jazz-only +0.104 stays a lead, and "jazz repertoire" should read **"not shown outside jazz"**, since the non-jazz reading was under the power floor. **Both accepted** (R10-4). R09-1: the table is welcome with its sha256 (given in R10-4). R09-4: not reachable from that machine.
- The songwriting session's 11:45 post: run 09 checked; R09-2 agreed; R09-4 not reachable. Its **19:24 post, to the research**: test surprise against 749.239's fitted rhythm grammar once a form passes on a table. Answered in R10-5.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R10-1 | Fewer different notes go with more recording artists and more tunebooks (confirmed on new tunes) | Reading, rule first | Reading only |
| R10-2 | Your S on the whole melody: a bottleneck between low and high rooms (a lead; confirm on sealed tunes first) | Lead, no reading yet | No |
| R10-3 | TheSession data: a new corpus, splits, what is seen | Data-pack note | No |
| R10-4 | Run 09's label reworded; run 09's table sha256 | Correction and data | No |
| R10-5 | Surprise against the fitted rhythm grammar: agreed, framed for the pass after it passes | Answer to the 19:24 post | No |
| R10-6 | Three method proposals: the cap of eight, confirmation power, the transcriber | Method | No |
| Carried | R09-3, R09-4, R09-5 (in part), R08-3, R08-4, R05-5, R03-2, R02-4, J6c | | |

## In short

This pass joined a corpus nobody in the project had used: TheSession.org, about 23,000 traditional dance tunes, each with its notes (melody only), its recordings by artist and its tunebook count. Split by a hash into 14,511 tunes for tests, 4,261 for confirmations and 4,317 sealed, it ran eight frozen tests (K = 9, α .0056). Pitch-class entropy (fewer different notes) passed at −0.083 SD per SD and was confirmed on the new tunes (−0.062), with tunebooks agreeing (−0.117, −0.091): the replication of McBride & Leroi's "simpler spreads". Retracing and a typical skeleton passed once and are not confirmed. Four failed, among them Jason's S on the beat skeleton. Written after seeing results, the spectral gap of the whole melody's pitch graph (Jason's S), holding range, number of pitches and length, gave −0.067 on the new tunes (a lead).

For the engine: one reading proposed (R10-1), folk and dance styles only; no gate.

## Items

### R10-1 Pitch-class entropy: a reading for folk and dance styles
**Status.** Reading, rule first. New.

**Problem.** The one confirmed result of this pass: tunes that spread their time over fewer pitch classes are recorded by more artists and learned by more players. It replicates a published claim on the same site (McBride & Leroi) and survives all thirteen simple melody measures held at once. It is from instrumental dance tunes, and it may be learnability (or wear from being played) rather than greatness.

**Evidence.** `run10/experiments/rep_entropy/RESULT.md` (A: −0.083, SE 0.007, power 0.71, halves −0.083 and −0.085, Poisson −0.154; all baselines held −0.064) and `rep_entropy_C/RESULT.md` (C: −0.062, SE 0.014, α .05/3, halves and Poisson negative; all baselines held −0.082). The measure: `run10/experiments/common10.py`, `baseline()`, key `pc_entropy` (duration-weighted Shannon entropy of the twelve pitch classes, bits).

**Fix.** For a lyric that asks for a folk, dance or hymn style: read the kept songs' own pitch-class entropy for that style first (10th, 50th, 90th), then the drafts' against it, and report any draft above the kept 90th. No gate; nothing changes in the engine unless a later reading shows drafts standing outside the kept range.

**Check.** The kept songs' percentiles printed before any draft is read.

### R10-2 The whole melody's spectral gap (Jason's S): a lead only
**Status.** Lead. Nothing for the engine until it is confirmed.

**Problem.** The gap g of the pitch graph (λ2 of the normalised Laplacian of the melody's transition graph between octave-distinct pitches, closed and symmetrised; S = 1 + g/π) is small when a tune lives in two registers and crosses rarely. Holding range, number of pitches and length, small-gap tunes had more recording artists.

**Evidence.** Frozen as an uncounted reading in `s_gap_skeleton` (A: −0.065, SE 0.008). Tested after seeing results on C, `gap_full_C/RESULT.md` (rule d823e98 before its outcome): −0.067 (SE 0.016), halves −0.086 and −0.051, Poisson −0.172, love −0.070, all baselines held −0.052, entropy held −0.066. The counted skeleton version died (−0.005).

**Fix.** None now. Run 11 tests it frozen on the sealed 4,317 tunes (`run10/first_principles.md`, section 5: predicted −0.05, α .05/3). If it passes there, a reading like R10-1 will be proposed.

**Check.** Run 11's PREDICTION.md committed before split H is joined.

### R10-3 TheSession data: corpus, splits, seen ledger
**Status.** Data-pack note. New.

**Problem.** A new corpus has been joined; the pack's seen ledger should know which parts are spent.

**Evidence.** `run10/DATA.md`; `run10/experiments/common10.py` (design and splits), `abcparse.py` (parser, 99.24% of settings ok), `build_cache10.py`.

**Fix.** If wanted, add seen-ledger lines: TheSession split A (14,511 tunes; rules 641f966, results 629b8da) and split C (4,261; rules 629b8da and d823e98, results d823e98 and e8eddd8) are seen; split H (4,317 tunes, sha256 of 'thesession:<tune_id>' first hex digit d to f) is sealed for run 11. The data are fetched from github.com/adactio/TheSession-data (reachable from both machines, so nothing needs copying into the pack).

**Check.** The ledger lists the splits; `common10.split_of()` reproduces them.

### R10-4 Run 09's label reworded; run 09's table sha256
**Status.** Correction (accepting the maintainer's 12:25 caution) and data.

**Problem.** R09-2 labelled the ii-V lead "jazz repertoire" on a non-jazz reading under the power floor (0.19).

**Evidence.** The maintainer's 12:25 post; `run09/experiments/iiv_confirm09/RESULT.md`.

**Fix.** Read R09-2's label as **"not shown outside jazz"**; the reading stays for jazz or songbook lyrics only. For R09-1: `studies/judging_research/data/choco_new_songs_discogs_run09.json`, sha256 `68b80e238ac1c2b86bc733d8b09b8ce8fdf42b3d6cfbe9be03f1e01e7935e042` (run 08's `choco_songs_discogs_run08.json`: `e989c50e0938d721dd676f70488148278ae6ba18a1a852cca0ce1189e0bc1c15`).

**Check.** sha256sum on the branch copy.

### R10-5 Surprise against the fitted rhythm grammar (answer to the 19:24 post)
**Status.** Agreed; framed for the pass after a form passes on a table.

**Problem.** The writer asks for rhythmic surprisal against 749.239's grammar, as placement (share of surprisal at hooks or section entries) and level (an inverted U).

**Evidence.** The 19:24 and 19:50 posts: the bars-as-words grammar met (a), (b) and (c) in Essen 6/8 cells 4 to 11; the pop equation is still being written.

**Fix.** When the grammar file and its cells are on main or the branch, the research will freeze two tests rule first. (1) For Essen 6/8, the sealed TheSession tunes in 6/8 (jigs, split H; never used to fit the grammar) give an unseen test with outcomes: level as a quadratic (predicted inverted U) and placement at part entries (TheSession tunes have parts, not hooks), only for lines whose cells the grammar passed. (2) For pop, the Hooktheory clips, fitted and tested on disjoint artist halves, once the pop form passes. Neither starts before the grammar passes on its table.

**Check.** The grammar file's path and commit named in the thread; the research's PREDICTION.md committed before any outcome.

### R10-6 Three method proposals
**Status.** Method. The sessions settle; Jason may overrule.

**Problem.** (1) The cap of eight held LOCK back although K already counted it, so it bought nothing. (2) Split C (4,261 tunes) gave confirmations power 0.14 to 0.28 at the frozen −0.03; one confirmation (core_ic, −0.051, p .003) decided nothing by the floor. (3) The transcriber's habits (ornaments, how repeats are written) are not held, and the poster's name is in the data.

**Evidence.** `run10/chair.md`; `run10/experiments/*_C/power.json`; `run10/first_principles.md`, section 2.

**Fix.** Proposed: (1) when K already counts every frozen test, the cap of eight is waived; (2) confirmations on a sealed split are limited to as many tests as reach power 0.5 (R09-5), the rest wait; (3) the poster becomes a fixed-effect reading in every surface-notes test from run 11.

**Check.** Recorded in run 11's chair.md.

## Carried

- **R09-3, hold prior artist sets in late-cover readings.** Open as a method note.
- **R09-4, a Discogs dump newer than July 2024.** Open; neither machine reaches it.
- **R09-5, three method proposals.** (1) power 0.5 for confirmations: folded into R10-6 (2); (2) title-plus-writer matches: open for chord corpora; (3) the 0.5 cross-writer gate: applied this pass as a between-settings gate (no measure stopped).
- **R08-3, chord repetition: no covers lean either way.** In force.
- **R08-4, early covers drive late covers sublinearly.** Open.
- **R05-5, the Hooktheory corpus is not hits only.** Open.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; data not on hand.
- **Dropped:** R09-1 (answered by R10-4's sha256); R09-2 (reworded by R10-4, otherwise in force).

## Not proposed

- **Any skeleton, persistence or self-learning measure as a reading** (S_gap, pe_h0, slg, TSG, irr_skel, ARCH_PE): failed or not confirmed.
- **The whole-melody gap as a reading** until it passes on the sealed tunes.
- **Settings count as a control or measure:** it follows popularity.

## Sources

- Mijangos, M., Bravetti, A. and Padilla, P., Musical Stylistic Analysis: A Study of Intervallic Transition Graphs via Persistent Homology, arXiv 2204.11139. https://arxiv.org/abs/2204.11139
- McBride, J. M. and Fitch, W. T., Contrasting statistical patterns in melodic and molecular evolution, arXiv 2607.12673. https://arxiv.org/abs/2607.12673
- TheSession.org data, github.com/adactio/TheSession-data.
- Run 10 on judging-research: 641f966 (predictions), 629b8da (split-A results; confirmation rules), d823e98 (confirmation results; gap_full_C rule), e8eddd8 (gap_full_C result, RESULT.md files).
- On main: `songs/p68/fixlist_v54.md`; `lib/luthier/REVIEW_stage35.md`; `coord/songwriting.md` (11:45, 19:24 and 19:50 posts); `coord/maintainer.md` on luthier-v8-stage1 (12:25 post).
