# Proposed list from the judging research, run 03 (for the maintainer)

23 November 2026. Proposed by Jason Bryant from the judging research (studies/judging_research/run03 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, experiments/bridge, experiments/curvature, first_principles.md). Nothing here is in the engine. Labels R03-1 to R03-4 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

Checked on origin/main (1b46833) before proposing, read only: `songs/p68/fixlist_v46.md` (latest list; next finding 749.170) and `lib/luthier/REVIEW_stage30.md` (latest review). R02-1 is done (the within-artist test, `studies/judging_checks/within_artist`, read as 749.157); R02-2 is done (`studies/judging_data/discogs_versions_matched.json`); 749.158 (fresh songs, unsettled) and 749.159 (the loop-less trial, step one done in `studies/loop_less_reading`, trial going ahead) are open from this research; 749.169 (a hold-out ledger in `studies/judging_data/README.md`) is open and the README has no ledger yet. `studies/covers/study_covers_discogs.py` still sets `original=1.0` on every row (line 26), so R02-3 is still open. No item on main proposes curvature, bridges or the spectral gap, so nothing below repeats a closed item.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R03-1 | Fresh songs by re-matching the 10,429 unmatched Hooktheory songs, then one two-term test (repetition and surprise) | Data request + rule-first test | No |
| R03-2 | Read chord surprise beside repetition in 749.159's trial | Reading added to an open trial | Reading only, no gate |
| R03-3 | Keep chord-map geometry out of the engine and the research on Hooktheory clips | Record of two kills | No |
| R03-4 | A power floor before any outcome is joined | Method, Jason decides | No |
| Carried | R02-3 open; R02-4 and J6c unchanged; J1 as 749.159; 749.169 noted | | |

## In short

Tonight tested two geometric measures of the chord map against covers, within artist, rules committed first (ad201ad). Both were killed: a song with a bridge (a chord move nothing else can replace) was covered slightly more, not less (+0.021 against −0.025 predicted), and Ollivier curvature of the chord walk added nothing once size, repetition and surprise were held (−0.0002). The spectral gap failed its stability check on Hooktheory clips (0.17 between clips of one song). None of this was ever in the engine, so nothing is to be undone; R03-3 records it so nobody builds on it.

What does bear on the engine: chord repetition and chord surprise travel together (songs that loop less also surprise more, ρ −0.29 across songs) and push covers in opposite directions within artist. A loop-less draw (749.159) could therefore raise chord surprise without anyone seeing it. R03-2 asks only for a reading. R03-1 is how to get fresh songs to test the pair properly.

## Items

### R03-1 Fresh songs from Hooktheory itself: re-match, then one two-term test
**Status.** Data request and lead. Never run. Needs the maintainer's matching rule committed first.
**Problem.** Every song on disk with cover counts has now been looked at, and the McGill hold-out has been read twice (749.169). The only fresh test so far had power 0.13 to 0.22 (749.158). 749.157 asks that chord surprise get its own rule-first test before it is used anywhere, but there is no unexplored set to run it on.
**Evidence.** Of 13,198 Hooktheory songs (YouTube ids) with chord measures in `studies/judging_data/hooktheory_surprise.json.gz`, 2,769 are matched to a Discogs-VI group and 10,429 are not (counted tonight from the data pack). Among the matched, only 50 (1.8%) have no cover, so the matched set is chosen by having been versioned at all. Tonight's curvature model (within artist, 1,924 songs, 420 artists; chord-count dummies, links, clips and first year held) gave chord repetition −0.061 (p .0003) and chord surprise −0.089 (p .0001). This was not a stated test: same songs, a model built for another question.
**Fix.** (1) Write and commit a matching rule (title and artist normalisation, as `studies/covers/covers_match_discogs.py`, applied to the 10,429 unmatched songs against Discogs-VI 20240701, Zenodo 13983028), run it blind to cover counts, and commit the per-song list of new matches only (video id, clique, artist), not the counts. (2) Only if at least 2,000 newly matched songs fall in artists with two or more songs: commit a rule, then join covers once. Model: log(1 + covers), artist fixed effect, first year, chord-count dummies, log clips, chord repetition and chord surprise together. Prediction written now: repetition −0.04 and surprise −0.04, each p < .025 and the same sign in both artist halves (md5 of the artist slug). Kill: repetition weaker than −0.02. Surprise weaker than −0.02 kills "plainly", not J1. (3) Songs not found in Discogs-VI are not "zero covers"; they stay out.
**Check.** Power printed before the estimate (about 0.56 at 2,000 within-artist songs, 0.76 at 3,000; scaled from tonight's SE of 0.017 on 1,924). The match list is committed before the counts exist on the machine. A line in the hold-out ledger of 749.169 names the test.

### R03-2 Read chord surprise beside repetition in the loop-less trial (749.159)
**Status.** A reading added to an open trial. No gate.
**Problem.** 749.159 draws verse and bridge structures from kept sections below the kept median of repetition. Within artist, plainer chords go with more covers (chord surprise −0.042, p .03, not pre-stated; 749.157). If sections that loop less are also more surprising, the trial could trade one for the other unseen.
**Evidence.** Across 2,769 matched songs, notes only: chord repetition and chord surprise correlate −0.29; chord surprise correlates +0.52 with the number of distinct chords (first_principles.md, run 03). The within-artist test's own line: all seventeen measures together gave repetition −0.061 and surprise −0.065 (`studies/judging_checks/within_artist/RESULT.md`).
**Fix.** In the trial's report, beside verse and bridge repetition, print the chosen builds' chord surprise (`ch_ic_mean` by the covers study's model, or the nearest the engine computes) and distinct chords per section, flag on against flag off, with the kept quartiles. No gate: chord surprise has not passed a rule-first test.
**Check.** The report shows both numbers for the four songs run. If surprise rises past the kept 75th percentile with the flag on, say so in the trial's verdict; the maintainer decides what follows.

### R03-3 Chord-map geometry on Hooktheory clips: two kills and one failed gate, recorded
**Status.** Record only. Nothing to change in the engine.
**Problem.** Bridges, Ollivier curvature and the spectral gap of the chord map were proposed in this research as possible new readings. None should become an engine reading or gate.
**Evidence.** `run03/experiments/bridge/RESULT.md`: +0.021 (SE 0.016, p .21), killed by its rule (above −0.01); halves +0.034 and +0.008. `run03/experiments/curvature/RESULT.md`: −0.0002 (SE 0.029), killed (≤ 0; without surprise +0.020). Chair's gate (no outcome): the spectral gap's clip-to-clip agreement 0.17, 0.21 after size; on McGill it stays stable (0.58) and untested.
**Fix.** None in the engine. In the research, no further geometry built from pooled Hooktheory clip maps; the spectral gap stays a McGill-only measure.
**Check.** None needed.

### R03-4 A power floor before any outcome is joined
**Status.** Method proposal. Jason decides.
**Problem.** Tonight's tests had power 0.24 and 0.06. Each look spends the corpus, and a low-power kill rule can kill a true small effect (the curvature rule would have killed a true +0.02 about one time in four).
**Evidence.** The two PREDICTION.md files and result.json files of run 03; 749.158 (power 0.13).
**Fix.** No outcome is joined for a test whose printed power at its own predicted size is under 0.5; such a test waits for more songs.
**Check.** Each PREDICTION.md states its expected power, and test.py stops before the join if it is under 0.5.

## Carried

- **R02-1.** Done (749.157). Closed here.
- **R02-2.** Done (`studies/judging_data/discogs_versions_matched.json`). Closed here.
- **R02-3 The "first performer" flag is 1 for every song.** Open, unchanged: `study_covers_discogs.py` line 26 still sets `original=1.0`. Fix as proposed in run 02 (compute it or remove it).
- **R02-4 Retire J2 to J5.** Unchanged; not taken up on main; Jason decides.
- **J1 Chords that move.** Now 749.159 (the loop-less trial); R03-2 adds a reading to it.
- **J6b Fresh songs.** Now 749.158 (unsettled). R03-1 proposes the next fresh set.
- **J6c The ceiling (MusicLab).** Unchanged.
- **749.169 The hold-out ledger.** Not ours to do; noted that run 03 did not use the hold-out (`run03/experiments/HOLDOUT_LOG.md`).

## Not proposed

- **The bridge flag and traffic on bridges:** killed (R03-3).
- **Mean Ollivier curvature and shuffle-relative curvature:** killed, or chord repetition renamed (ρ −0.52).
- **The spectral gap and S = 1 + g/π on Hooktheory songs:** failed stability; S only rescales g.
- **Tonic resistance (I2), the obtuse statue (G3), melody transport (I1):** untested in the research; ranked for later nights, nothing for the maintainer yet.
- **Covers across genres:** still Jason's decision and still needs genres from the Discogs dump.

## Sources

- Ollivier (2009), Ricci curvature of Markov chains on metric spaces, J. Funct. Anal. 256, 810–864. https://arxiv.org/abs/math/0701886
- Devriendt & Lambiotte (2022), Discrete curvature on graphs from the effective resistance, J. Phys. Complexity 3, 025008. https://arxiv.org/abs/2201.06385
- Run 03 on judging-research: commits ad201ad (predictions) and f098d67 (results).
- On main: `songs/p68/fixlist_v46.md`; `lib/luthier/REVIEW_stage30.md`; `studies/judging_checks/within_artist/RESULT.md`; `studies/loop_less_reading/RESULT.md`; `studies/judging_data/README.md`; `studies/covers/study_covers_discogs.py`.
- Data: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
