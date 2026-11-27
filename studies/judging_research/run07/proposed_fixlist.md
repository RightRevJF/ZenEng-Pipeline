# Proposed list from the judging research, run 07 (for the maintainer)

26 November 2026, the 18:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run07 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, first_principles.md, searches.md, and the nine folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 07" (https://claude.ai/artifact/6VHFj6aQHoz8wUxRTwcMow); the pass's report is the Doc "Judging research, run 07" (https://claude.ai/artifact/CMbhxVrSd5NP6gBPqRTWLR).

Nothing here is in the engine. Labels R07-1 to R07-4 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (aed861b) and the thread before proposing, read only.**
- `songs/p68/fixlist_v53.md` is the latest list (next finding 749.223 at its head); it carries no research item. `lib/luthier/REVIEW_stage35.md` is the latest review.
- `studies/judging_checks/run06/CHECK.md`: R06-1 done (the fresh table is in the pack as `hooktheory_fresh_covers_discogs.json`, marked seen; the README has the seen ledger and the Hooktheory address); R06-2 agreed and in force; R06-4 not reachable from the maintainer's machine either; R06-5 "I would say yes", Jason rules; R02-3 mended (`study_covers_discogs.py` now reads the earliest versions); R04-2 read (`studies/judging_checks/first_performers/RESULT.md`: −0.026 among first performers, unsettled).
- `coord/songwriting.md` (17:15 ET) and `coord/maintainer.md` (17:35 ET, to the judging research): R06-2 in force; R06-4 blocked on both machines; the maintainer offers to fetch a Chordonomicon mirror from Zenodo or GitHub if one is named. No ask is open for the research.
- Nothing on main proposes Lakh MIDI songs, Gromov hyperbolicity, sliding-window persistence or a spectral gap on whole songs, so nothing below repeats a closed item.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R07-1 | 5,901 Lakh whole songs matched to Discogs-VI: a commit-ready table and a seen-ledger line | Data-pack note | No |
| R07-2 | Chord repetition reversed on whole songs; "which way covers lean on loops" stays open | Reading caveat (continues R06-2) | Reading only, no gate |
| R07-3 | Two method rulings for Jason: the 0.2 power floor (R06-5), and kill only outside the 95% range | Method | No |
| R07-4 | Recorded: tree-likeness, spectral gap, chirality, arrow, triad fidelity killed; loop period and burstiness unsettled | Record | No |
| Carried | R06-4 (updated), R05-5, R03-2, R02-4, J6c | | |

## In short

The research found a corpus of whole songs with names that its machine can reach: the Lakh Pianoroll Dataset (Zenodo, CC BY 4.0), named through the Million Song Dataset metadata in the Gold-Caps set (Zenodo, CC BY 4.0). After removing songs already seen on Hooktheory, McGill hold-out songs, MIDI files shared by different titles and karaoke or tribute acts, 5,901 fresh songs by 1,678 artists with two or more songs remained. Eight tests were frozen (commit 9227e71) before the Discogs-VI match (by the maintainer's reduction and rule), each at p < .05/8; a ninth, written after seeing results, was frozen at 6165846. None passed: seven killed, two unsettled. Chord repetition, the lean behind 749.157 to 749.185, came out −1.93 per SD (SE 1.34) against +1.0 predicted.

For the engine nothing changes. R06-2's advice stands and is firmer: judge any loop gate on the kept songs' rate alone.

## Items

### R07-1 The Lakh songs: matched, and now seen
**Status.** Data-pack note. New.

**Problem.** The pack holds no whole songs with notes except the McGill hold-out. Tonight the research built 5,901 from the Lakh Pianoroll Dataset and matched them to Discogs-VI; they are now spent.

**Evidence.** `run07/experiments/common.py` (`lakh_songs`, `add_shapes`, `load_outcomes`; the exclusions and the match rule in its header); `run07/experiments/lakh_notes.py` (bar chroma and half-bar triads from the pianorolls). 2,387 of 5,901 matched; 2,343 taken up by another artist (39.7%). A further 3,436 songs by single-song artists were joined in `cv_w_singletons` (719 matched). 155 Lakh tracks are McGill hold-out songs by title and artist and were excluded before anything was read. The table is `studies/judging_research/data/lakh_songs_discogs_run07.json` (2.8 MB; CC BY-SA 4.0 as derived from Discogs-VI).

**Fix.**
1. If wanted, copy the table into the pack as `lakh_covers_discogs.json`, marked seen.
2. Add two seen-ledger lines: the 5,901 within-artist Lakh songs (run 07, 9227e71 and 0908976) and the 3,436 single-song-artist Lakh songs (run 07, 6165846).
3. Note the sources and addresses: `lpd_5_cleansed.tar.gz` and `metadata.zip` from Zenodo 5646574; `gold-caps_lmd-matched_general_v0.json` from Zenodo 10178563; `msd_bb_matches.csv` from Zenodo 3258042.

**Check.** The ledger lists both sets; the table's keys reproduce from `common.lakh_songs()`.

### R07-2 Chord repetition reversed on whole songs: the loop question stays open
**Status.** A caveat on readings. Reading only, no gate. Continues R06-2.

**Problem.** The positive lean of chord repetition on "taken up at all" (+1.00 seen, +1.32 fresh, Hooktheory) did not carry to whole MIDI songs: −1.93 (SE 1.34, p .15), both halves negative, logit −0.12. On main, the covers-count lean is unsettled among first performers (−0.026). No reading of repetition on either margin is settled.

**Evidence.** `run07/experiments/lakh_repetition/RESULT.md`; `run06/experiments/fresh_repetition/RESULT.md`; `studies/judging_checks/first_performers/RESULT.md`. MIDI repetition correlates only 0.32 with Hooktheory's on 1,487 shared songs, so this is a different construct, not a replication failure of the same one.

**Fix.** Keep citing covers for neither side of any loop gate (749.185 and successors). Do not cite run 06's "+ on taken up" lean as a direction.

**Check.** The next loop-gate report carries no cover-based mark.

### R07-3 Two method rulings for Jason
**Status.** Method. Replaces R06-5. Jason decides.

**Problem.** At .05/N with power near zero, a pass is nearly impossible even if a prediction is true (tonight: about 6% that any of eight would pass), and kill lines at zero fire about half the time on noise. The maintainer agreed with the 0.2 floor (run 06 check).

**Evidence.** `run07/experiments/power_fake.json`; `run07/first_principles.md`, section 2. Tonight's realised base rate was 39.7% against the 20% the simulations assumed, so the true power was lower still.

**Fix.**
1. Count toward .05/N only tests whose fake-outcome power is 0.2 or more; freeze and report the rest as estimates.
2. Kill a test only when its prediction lies outside its own 95% range (tonight that would kill ch_rep, H4m, A and F, and leave g, CH, P\* and B unsettled).
3. Simulate power at the realised base rate of the outcome.
The same rules would serve any 749 reading with several marks.

**Check.** Jason's ruling recorded in the research's next chair.md.

### R07-4 Recorded: tonight's measures
**Status.** Record only.

**Evidence** (pp of y_foreign per SD, within artist, 5,901 songs):
- Tree-likeness H4m (average Gromov four-point gap of 4-bar windows): +1.41 (SE 0.92) against −0.5; killed.
- Spectral gap g (Jason's S = 1 + g/π) on whole songs: +0.26 (SE 0.86) against −0.3; killed, weakly.
- Chirality CH: +0.30 (SE 0.76) against −0.6; killed, weakly (−0.30 on Hooktheory).
- Arrow A: −1.36 (SE 0.76) against +0.6; killed (third batch against).
- Triad fidelity F: −2.10 (SE 1.04, p .044) against +0.5; killed; likely reads the MIDI arranger.
- Loop period P\*: +0.05 (SE 0.74); unsettled. Burstiness B: +0.57 (SE 0.97); unsettled.
- Contrast cv_w on single-song artists (after seeing results): −0.13 (SE 0.81) against +1.5; killed.

**Fix.** None in the engine. None of these should become an engine reading or gate.

**Check.** None needed.

## Carried

- **R06-4, a larger chords corpus with names.** Updated. Lakh gave the size but blurs the measures (MIDI arrangements, triad templates on full parts). Chordonomicon remains blocked on both machines (Hugging Face storage host; no names). No Zenodo or GitHub mirror of `chordonomicon_v2.csv` has been found; the research will name one if it finds it.
- **R05-5, the Hooktheory corpus is not hits only.** Open and unchanged.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand.
- **Dropped:** R06-1 (done on main); R06-2 (in force; R07-2 continues it); R06-3 (a record; R07-4 continues it); R06-5 (replaced by R07-3); R05-1 (done on main); R04-2 (read on main, first performers); R02-3 (mended on main).

## Not proposed

- **Any tree-likeness, spectral-gap, chirality or arrow reading in the engine:** all failed on fresh songs.
- **Chord repetition as a gate in either direction:** reversed on whole songs, unsettled everywhere.
- **Triad share as a reading:** its lean most likely reads the arranger's voicing.

## Sources

- Gilbert, A. C. and Yim, J.-H. (2024), Hyperbolicity, slimness, and minsize, on average, arXiv 2412.05746. https://arxiv.org/abs/2412.05746
- Perea, J. A. and Harer, J. (2015), Sliding windows and persistence, Found. Comput. Math.; arXiv 1307.6188. https://arxiv.org/abs/1307.6188
- Lakh Pianoroll Dataset (Dong et al. 2018), Zenodo 5646574, CC BY 4.0; Gold-Caps LMD-matched (Jonason, Casini & Sturm 2023), Zenodo 10178563, CC BY 4.0; Hit Song Prediction (Zangerle et al. 2019), Zenodo 3258042; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0; Hooktheory via Sheet Sage (CC BY-NC-SA 3.0), used only to exclude seen songs.
- Run 07 on judging-research: 9227e71 (predictions), cd17b08 (logit sign-check fix), 0908976 (results), 6165846 (ninth prediction).
- On main: `songs/p68/fixlist_v53.md`; `lib/luthier/REVIEW_stage35.md`; `studies/judging_checks/run06/CHECK.md`; `studies/judging_checks/first_performers/RESULT.md`; `coord/songwriting.md`; `coord/maintainer.md` (branch luthier-v8-stage1).
