# Proposed list from the judging research, run 09 (for the maintainer)

27 November 2026, the 10:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run09 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, first_principles.md, DATA.md, searches.md, and the ten folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 09" (https://claude.ai/artifact/BXZRqqxiFxoeCbm6EK9sRz); the pass's report is the Doc "Judging research, run 09" (https://claude.ai/artifact/RH7H79gxTgx5RopbDNi3XS).

Nothing here is in the engine. Labels R09-1 to R09-5 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (3b3e762) and the thread before proposing, read only.**
- `songs/p68/fixlist_v54.md` is the latest list (findings from 749.226, the 3/4 plan); it carries no research item. `lib/luthier/REVIEW_stage35.md` is still the latest review.
- The maintainer's check of run 08 (`studies/judging_checks/run08/CHECK.md`, 07:45 post): R08-1 taken up (`choco_covers_discogs.json`, on the maintainer's branch; not yet on main), R08-2 agreed as a reading with the kept songs' own ii-V share by genre read first, R08-3 in force, R08-6 not reachable. One correction asked: run 08's post said K = 6; the frozen rules say K = 5, and a test written after seeing results should not be counted. **Accepted**: run 08's count is K = 5, and this pass keeps every after-seeing-results test out of K (K = 1).
- The songwriting session (04:45 post, to the research): the same K correction; R08-2 a reading at most, no gate; R08-6 not from its machine either. No other ask is open for the research.
- Nothing on main proposes the Real Book or Band-in-a-Box partitions, path signatures or a late cover window, so nothing below repeats a closed item.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R09-1 | 1,283 more ChoCo songs matched and now seen; the year split of run 08's songs also seen | Data-pack note | No |
| R09-2 | The ii-V lead is now "jazz repertoire": R08-2 narrowed to jazz and songbook styles | Reading, rule first (replaces R08-2) | Reading only |
| R09-3 | ii-V tunes gained new artists after their charts were written (a lead): hold prior artist sets in any late-cover reading | Method note (extends R08-4) | No |
| R09-4 | Data request: a Discogs release dump newer than July 2024, or unseen jazz chord charts with composers | Data request (replaces R08-6) | No |
| R09-5 | Three method proposals: power 0.5 for confirmations, title-plus-writer matches, a binding cross-writer gate | Method | No |
| Carried | R08-3, R08-4, R08-5 (superseded in part), R06-4, R05-5, R03-2, R02-4, J6c | | |

## In short

This pass parsed the ChoCo partitions run 08 left aside (Band-in-a-Box internet files, the Real Book, and transcriptions of single recordings) and matched them to Discogs-VI by run 08's own rules: 1,283 unseen songs, mostly by title alone and across composers. The one counted test, run 08's frozen confirmation of the ii-V lead, came out at −0.0005 SD per SD (SE 0.028; power 0.367): unsettled. Its frozen non-jazz reading (−0.049) excluded +0.04, so by run 08's rule the lead is labelled "jazz repertoire". Five geometric estimates from path signatures decided nothing.

Two leads on run 08's seen songs bear on the chart-writer worry. The ii-V share read from a Real Book or Band-in-a-Box chart predicted covers better than the iReal reading of the same songs (+0.064 against +0.020). And, written after seeing results, ii-V tunes gained more new artists in 2023 to 2024, after ChoCo's charts were collected, holding earlier artists and recent momentum (+0.044, SE 0.012). So the lead looks like a property of tunes jazz players keep taking up, not only the chart copying the covers.

For the engine nothing changes. The writer's styles are pop, rock, folk and hymn, where the ii-V lead is absent.

## Items

### R09-1 More ChoCo songs: matched, and now seen
**Status.** Data-pack note. New.

**Problem.** The pack's seen ledger does not yet list this pass's 1,283 songs, nor the fact that run 08's songs have now been read by year of each artist set.

**Evidence.** `run09/experiments/common09.py` (the match: run 08's two rules unchanged, with the exclusions in its header); `run09/experiments/parse09.py`; `run09/DATA.md`. The joined table is `studies/judging_research/data/choco_new_songs_discogs_run09.json` (0.55 MB; CC BY-SA 4.0 as derived from Discogs-VI; ChoCo CC BY 4.0).

**Fix.**
1. If wanted, copy the table into the pack beside `choco_covers_discogs.json`, marked seen.
2. Add seen-ledger lines: the 1,283 run 09 songs (rules 379e219, results 687e735); and run 08's 8,565 songs read by artist-set year, 2023 to 2024 against earlier (rules 4055742 and 780e2c2).
3. Note: every ChoCo partition with matchable songs is now spent. What remains is Billboard (the McGill source, never to be used), Chordify (Billboard ids), RWC-Pop and classical or folk sets.

**Check.** The ledger lists both; `build_design09()` reproduces the table's cliques.

### R09-2 The ii-V share: a reading for jazz and songbook styles only (replaces R08-2)
**Status.** Reading, rule first. Narrows R08-2, which both sessions agreed as a reading deciding nothing.

**Problem.** Run 08 froze an interpretive reading: if the non-jazz estimate's range excluded +0.04, the lead would be labelled "jazz repertoire". It did (−0.049, range −0.114 to +0.015). Every non-jazz reading so far is small or negative (run 08 +0.021; late window +0.024).

**Evidence.** `run09/experiments/iiv_confirm09/RESULT.md` and `result.json`; `run08/experiments/iiv_singletons/RESULT.md`; `run09/experiments/late_momentum08/RESULT.md`.

**Fix.** Drop R08-2's pop, rock and folk report. Keep the reading only for a lyric that asks for a jazz or songbook style: the kept songs' own ii-V share for that style read first (the maintainer's addition), then the drafts against the kept 10th to 90th. No gate.

**Check.** None until such a lyric arrives.

### R09-3 New artists after the charts: hold prior artist sets
**Status.** Method note. Extends R08-4.

**Problem.** The fair question about a chart measure is whether it predicts take-up the chart could not have copied. On run 08's songs (seen; written after seeing results), the ii-V share predicted artist sets first dated 2023 to 2024, after ChoCo's charts were collected: +0.051 (SE 0.012) holding earlier sets, and +0.044 (SE 0.012) holding sets from 2018 to 2022 as well; within composer +0.058; halves and Poisson positive. Outside jazz +0.024, unsettled.

**Evidence.** `run09/experiments/late_window08/RESULT.md`, `late_momentum08/RESULT.md` (rules pushed before their outcomes: 4055742, 780e2c2).

**Fix.** Any reading that uses covers by period holds earlier artist sets and recent momentum, and says whether a measure predicts take-up after the source of the measure (a chart, a draft) existed. A lead only: nothing for the engine.

**Check.** None needed.

### R09-4 A data request: later artists, or unseen jazz charts
**Status.** Data request. Replaces R08-6, which neither machine could meet.

**Problem.** The late-window lead needs artists after July 2024 to become a finding, or unseen jazz tunes with chords and composers. Neither is on this machine; data.discogs.com is not reachable from here.

**Evidence.** `run09/DATA.md` ("Still missing"); `run09/first_principles.md`, section 5 and the addendum.

**Fix.** If the maintainer's machine reaches either: (a) a Discogs monthly release dump newer than July 2024 (`discogs_YYYYMM01_releases.xml.gz`, CC0) or a newer Discogs-VI release on Zenodo; or (b) about 1,100 jazz tunes with title, composer and chord symbols from a source outside ChoCo (2,200 for power 0.8). If neither, "not reachable" in the thread closes it.

**Check.** A named file with its sha256, or "not reachable".

### R09-5 Three method proposals
**Status.** Method. The sessions settle; Jason may overrule.

**Problem.** (1) Run 08 asked for power 0.5 before its confirmation ran; this pass counted it at 0.367 under the ruled 0.2 floor, and the likeliest result at that power (unsettled) is what came. (2) 985 of 1,283 songs were matched by title alone; the 298 matched by title plus a name gave +0.063 (SE 0.063), consistent with dilution. (3) Stability was read mostly on Band-in-a-Box against Real Book near-copies; two chart writers agree only 0.28 to 0.72.

**Evidence.** `run09/chair.md` (the K table, the gates); `run09/first_principles.md`, section 2; `run09/experiments/iiv_confirm09/result.json` (the name-matched reading).

**Fix.** Proposed: (1) a confirmation of an earlier pass runs only at fake-outcome power 0.5, pooling unseen batches until it reaches it; (2) title-only matches are a reading, not the main sample, when a name is available anywhere in the source; (3) a measure is stopped if its agreement between two chart writers is under 0.5. These replace R08-5's two questions (the K rule worked this pass: K = 1 was consistent).

**Check.** Recorded in the next chair.md.

## Carried

- **R08-3, chord repetition: no covers lean either way.** In force (both sessions); unchanged.
- **R08-4, early covers drive late covers sublinearly.** Open as a method note; R09-3 extends it.
- **R08-5, K and a held-back batch.** Superseded in part by R09-5; the held-back batch is still proposed for any new corpus.
- **R06-4, a larger chords corpus with names.** Now carried by R09-4 (b).
- **R05-5, the Hooktheory corpus is not hits only.** Open and unchanged.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand.
- **Dropped:** R08-1 (taken up by the maintainer); R08-2 (replaced by R09-2); R08-6 (replaced by R09-4).

## Not proposed

- **Any signature or voice-leading measure as a reading** (TR, TQ, IRR, VR4c, TYP): estimates that decided nothing.
- **The ii-V share as a default or gate for the writer's songs:** absent outside jazz.
- **Holding a song's number of iReal charts in a covers reading:** it is itself a sign of being much played (gap_writer08).

## Sources

- Chevyrev, I. and Kormilitzin, A., A Primer on the Signature Method in Machine Learning, arXiv 1603.03788. https://arxiv.org/abs/1603.03788
- Lee, S. and Jeong, D., JSIR, arXiv 2610.15356; data github.com/MALerLab/JSIR (CC BY-SA 4.0). https://arxiv.org/abs/2610.15356
- ChoCo v1.0.0 (de Berardinis et al. 2023), Zenodo 7706751, CC BY 4.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), Zenodo 13983028, CC BY-SA 4.0.
- Run 09 on judging-research: 379e219 (predictions), 687e735 (results), 4055742 and 780e2c2 (after-seeing-results rules), 7fa66b2 (their results and the RESULT.md files).
- On main: `songs/p68/fixlist_v54.md`; `lib/luthier/REVIEW_stage35.md`; `coord/songwriting.md`; `coord/maintainer.md` and `studies/judging_checks/run08/CHECK.md` (branch luthier-v8-stage1).
