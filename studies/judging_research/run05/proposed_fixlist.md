# Proposed list from the judging research, run 05 (for the maintainer)

25 November 2026. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run05 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, DATA.md, first_principles.md, and the eight folders under experiments/.

Nothing here is in the engine. Labels R05-1 to R05-5 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (edbb6e0) before proposing, read only.**
- `songs/p68/fixlist_v46.md` is still the latest list (next finding 749.171). It now carries "Proposed code to test (v47)", including the `loop_less` flag (749.159, proposed 960) and `lib/luthier/proposed_v47_trial.py`.
- `lib/luthier/REVIEW_stage30.md` is still the latest review.
- None of run 04's items (R04-1 to R04-4) appears on main yet; `studies/judging_data/` is unchanged since 22 November.
- 749.169 (a hold-out ledger) is open: the data-pack README still has no ledger.
- `studies/covers/study_covers_discogs.py` line 26 still sets `original=1.0`, so R02-3 is open.
- New on main: `studies/plain_and_pink` (749.170). Nothing on main proposes persistent homology, chord-change direction, melody range or a fame comparison, so nothing below repeats a closed item.

Published as the Doc "Proposed fix list: judging research, run 05" (https://claude.ai/artifact/Uihh8u39QUGNC4mFoNmYry); the night's report is the Doc "Judging research, run 05" (https://claude.ai/artifact/FFmtD1g9RKS9xczCyUPsqQ).

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R05-1 | The full Hooktheory notes are public at a fetchable address; put that in `make.py` and the README, with a "seen" ledger | Data-pack note (replaces R04-1) | No |
| R05-2 | Fresh within-artist songs: re-match the clips the data pack leaves out to Discogs-VI | Data request (replaces R03-1) | No |
| R05-3 | 749.159 / v47 `loop_less`: keep it a reading; add one notes-only reading of chord-change direction | Reading caveat on an open trial (updates R04-3) | Reading only, no gate |
| R05-4 | Persistent homology, harmonic freedom, the fifths path, tonic resistance: recorded as failed | Record | No |
| R05-5 | The Hooktheory corpus is not hits only; across-artist studies should mark game and library sources | Data caveat | No |
| Carried | R04-2, R03-2, R03-4 (updated), R02-3, R02-4, J6c; 749.169 noted; R04-4 closed | | |

## In short

Run 05 found the notes of every Hooktheory song at a public address (Sheet Sage's own GitHub repository), so every measure from the notes could be tested on all 9,588 within-artist songs for the first time. Seven tests were frozen before any outcome was joined (commit 1f6c36d), at p < .05/7. None passed. Four were killed: the certified loop margin from persistent homology (−0.20 points per SD against +0.8 predicted), harmonic freedom (−0.23), the fifths path (+0.01) and a fame-versus-notes comparison (whose fame proxy turned out to be broken). Three were unsettled: the direction of chord changes (+0.84, p .035), melody range (−0.42, p .11) and tonic resistance (−0.23).

An eighth test, frozen after seeing those (commit 2bfd4ca), carried chord-change direction to 3,212 songs by single-song artists. It came out the opposite way (−1.75, p .009) and was killed. So nothing tonight gives the engine a new reading. The useful results for the maintainer are the data address (R05-1), the route to fresh songs (R05-2), and a caveat on the loop-less trial (R05-3).

## Items

### R05-1 The full Hooktheory notes: a fetchable source, and a "seen" ledger
**Status.** Data-pack note. Replaces R04-1, which is half resolved.

**Problem.** `make.py` reads `Hooktheory.json.gz` from a local clone; the README says the raw download is not in the repo. R04-1 asked for the notes of all clips in the pack. Tonight the file was found at `https://raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz` (20,075,896 bytes; sha256 917b7cd58f5f4e07d6c36acf7bfad958c99ee05472dab3555399141094698e0c), reachable from the research's cloud machine. It holds 26,175 clips; all 16,563 clips behind the 9,588 within-artist rows are in it. So the research no longer needs `hooktheory_clips_all.json.gz` in the pack, but the next reader should not have to rediscover this.

**Evidence.** `run05/searches.md`; `run05/experiments/common.py` (`RAW_SHA256`, `raw_clips()`); every run 05 test read it.

**Fix.**
1. In `make.py`'s docstring and the README's "What is not here" section, name the address and the sha256 above.
2. Add a "seen" ledger to the README: which songs have been joined to which outcome by which test. At minimum: the 9,588 within-artist rows against "in Discogs-VI at all" and y_foreign (run 04: chord repetition, chord surprise, information rate; run 05: seven new measures); the 3,212 single-song-artist songs against y_foreign (run 05, `arrow_singletons`).
- Licence: CC BY-NC-SA 3.0, credit Hooktheory and Sheet Sage. The raw file stays out of the repo.

**Check.** The sha256 in the README matches a fresh download. The ledger lists run 04's and run 05's commits.

### R05-2 Fresh within-artist songs: re-match the clips the data pack leaves out
**Status.** Data request. Replaces R03-1 (updated). Never run.

**Problem.** Every song with an outcome on disk has now been looked at against its outcome. Effects run at about 1 point per SD on a 22% outcome, which one test on seen songs at .05/7 cannot settle (`run05/first_principles.md`, section 6). Tonight's two leads (chord repetition on being taken up, R04-FV; direction, within artist only) need songs nobody has tested.

**Evidence.** The raw file has 26,175 clips; the data pack's surprise file has 21,998 (about 4,177 more clips, 314 of them with no YouTube id). The 10,118 songs not matched to Discogs-VI were matched only by the covers study's title-and-artist rule, never by a second pass. `run05/DATA.md`.

**Fix.** Run the match of `studies/covers/covers_match_discogs.py` once more over every Hooktheory song not yet matched, with Discogs-VI 20240701 `main.zip` (zenodo.org/records/13983028, 1.4 GB, CC BY-SA 4.0), adding a leading-"the" strip and the alias fixes run 04 noted. Commit the new matches as a separate file, flagged "unseen", with no measure joined. Before any test uses it, the research commits a small frozen battery (chord repetition, direction, melody range) at one threshold. If the maintainer prefers, the research can do the re-match itself on a coming night: Zenodo is reachable from its machine.

**Check.** The new file names its match rule and counts. No test touches it before its rule is committed. The hold-out ledger (749.169) gets a line.

### R05-3 749.159 and the v47 `loop_less` flag: keep it a reading, and read direction too
**Status.** A caveat on an open trial. Reading only, no gate. Updates R04-3.

**Problem.** 749.159's support is cover counts among songs already versioned (749.157: −0.042, narrow; 749.158: −0.028, unsettled). On being taken up at all, chord repetition leans the other way (+1.19, and +1.00 for other artists only, run 04, unsettled; tonight's models held it and saw the same lean on the same songs). Tonight also tried chord-change direction (does the progression go round, I–V–vi–IV, or step back and forth, I–IV–I–IV). Within artist it leaned towards being taken up (+0.84, p .035, unsettled); across single-song artists it leaned hard the other way (−1.75, p .009, killed). Direction is unrelated to repetition (ρ +0.01), so `loop_less` may or may not change it.

**Evidence.** `run05/experiments/arrow_of_time/RESULT.md`, `run05/experiments/arrow_singletons/RESULT.md`, `run04/experiments/foreign_versions/RESULT.md`; `studies/loop_less_reading/reading_v47.json` on main.

**Fix.** No change to the trial's build. In the v47 trial's report, beside the chord-repetition reading, add one notes-only reading: the direction A = 1 − Σ min(n_ij, n_ji) / Σ n_ij of each written section's chord changes (consecutive equal chords collapsed, at least 6 changes), with and without `loop_less`, against the kept median of that kind. Report it; gate nothing on it. Keep R04-3's sentence that the extensive margin leans the other way and is unsettled.

**Check.** The trial report carries both readings and the sentence. No gate is added from tonight's results.

### R05-4 Shapes from persistent homology, harmonic freedom, the fifths path, tonic resistance: recorded
**Status.** Record only. Nothing to change in the engine.

**Problem.** These were proposed as possible readings of a song's notes. None should become an engine reading or gate.

**Evidence.**
- `loop_margin`: the certified H1 loop margin of the chord-chroma sliding-window cloud (TopPT, card 1), −0.20 points per SD (SE 0.44), killed; its family (loop thickness, second bar, melody margin, melody plus chords) stopped on the notes.
- `harmonic_freedom`: −0.23 (SE 0.41), killed.
- `fifths_path`: +0.015 (SE 0.32), killed; diatonicity, merged into it, +0.34 (p .32), reported only. Closes R03-F1.
- `tonic_resistance`: −0.23 (SE 0.44), unsettled, 0.03 short of its kill line; gate 0.203 against 0.20. The review recommends retiring it.
- `melody_range`: −0.42 (SE 0.26, p .11), unsettled; on covers among versioned songs it leans the other way (+0.063, p .042, reported). Not a reading yet.

**Fix.** None in the engine.

**Check.** None needed.

### R05-5 The Hooktheory corpus is not hits only
**Status.** Data caveat for across-artist studies. No engine change.

**Problem.** Ranked by songs on Hooktheory, the top "artists" are game studios and library composers (Nintendo, Kevin MacLeod, ZUN and others). Tonight's fame test used that count as an artist-fame proxy and it scored worse than chance (AUC 0.48), while the note measures' advantage (0.69) was about 97% artist-level style (sung pop against instrumental themes). Within-artist tests are untouched by this, but any across-artist comparison on Hooktheory songs mixes pop with game and library music.

**Evidence.** `run05/experiments/fame_vs_notes/RESULT.md`.

**Fix.** Add a flag for game, film and library sources to the data pack (a short hand list of artist slugs is enough), and have across-artist studies report their estimate with those sources left out.

**Check.** The covers study's across-artist −0.071 is reported with and without the flagged sources (a reading, not a new test of J1).

## Carried

- **R04-2, cover counts by other artists only, then reread 749.157.** Open and unchanged. Tonight confirmed again that karaoke and tribute sets decide no song's y_foreign.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R03-4, a power floor.** Open; Jason decides. Updated: tonight the notes-side power bound overstated the standard error by a third or more (melody range: real power 0.49 at the night's bar, bound 0.10). The review suggests taking power from a fake-outcome run before the real one.
- **R02-3, the "first performer" flag is 1 for every song.** Open and unchanged (line 26).
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand.
- **749.169, the hold-out ledger.** Not ours to do; R05-1 asks for a "seen" ledger beside it. Run 05 did not use the hold-out (`run05/experiments/HOLDOUT_LOG.md`).
- **Dropped:** R04-1 (replaced by R05-1: the notes are reachable now); R03-1 (replaced by R05-2); R04-3 (folded into R05-3); R04-4 (a record with no action; R05-4 continues it).

## Not proposed

- **Chord-change direction as a reading or gate:** unsettled within artist and killed across new songs (opposite sign).
- **Melody range as a gate:** unsettled, and its two margins lean opposite ways.
- **Any fame adjustment:** the fame proxy on hand is broken; a real one needs chart data.

## Sources

- Park, An, Kim & Kim (2025, v4 2026), Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings, arXiv 2512.06324. https://arxiv.org/abs/2512.06324
- Interiano, Kazemi, Wang, Yang, Yu & Komarova (2018), Musical trends and predictability of success in contemporary songs in and out of the top charts, Royal Society Open Science 5:171274. https://doi.org/10.1098/rsos.171274
- Run 05 on judging-research: commits 1f6c36d (predictions), 3df4b7f (seven results), 2bfd4ca (eighth prediction), 537f894 (eighth result, first principles).
- On main: `songs/p68/fixlist_v46.md`; `lib/luthier/proposed_v47.py`; `studies/loop_less_reading/reading_v47.json`; `studies/judging_checks/within_artist/RESULT.md`; `studies/judging_data/README.md` and `make.py`; `studies/covers/study_covers_discogs.py`; `studies/covers/covers_match_discogs.py`.
- Data: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
