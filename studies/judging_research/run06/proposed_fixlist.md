# Proposed list from the judging research, run 06 (for the maintainer)

26 November 2026. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run06 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, DATA.md, first_principles.md, and the six folders under experiments/.

Nothing here is in the engine. Labels R06-1 to R06-5 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (073efd6) before proposing, read only.**
- `songs/p68/fixlist_v51.md` is the latest list (next finding 749.197 at its head, addenda to 749.199). It carries no item from this research. `lib/luthier/REVIEW_stage35.md` is the latest review.
- 749.169 is done: `studies/judging_data/README.md` now has a hold-out ledger. Song 50 is spent on fix 964; 63 (reserved for 749.185, the loop gate with a chance), 64 and 65 are sealed.
- The loop-less flag (960, 749.159) is a setting, off by default; 749.178 failed its seen-song checks; 749.185 waits.
- None of run 05's items (R05-1 to R05-5) appears on main. The README and `make.py` still name no fetchable address for `Hooktheory.json.gz` and keep no "seen" ledger. `studies/covers/study_covers_discogs.py` line 26 still sets `original=1.0`, so R02-3 is open.
- Nothing on main proposes chirality, Hodge decompositions or a fresh-song battery, so nothing below repeats a closed item.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R06-1 | The fresh-song re-match is done (100% reproduction of the pack); commit-ready table and a "seen" ledger line | Data-pack note (replaces R05-2; updates R05-1) | No |
| R06-2 | 749.185 / 749.178: the fresh songs cannot settle "which way covers lean"; judge the loop gate on the kept rate alone | Reading caveat on a waiting trial (replaces R05-3) | Reading only, no gate |
| R06-3 | Recorded: chirality unsettled; melody range and diatonicity killed; the Hodge "downhill" share is the excerpt's ends | Record (continues R05-4) | No |
| R06-4 | A larger chords corpus with names, for a powered confirmation | Data request | No |
| R06-5 | Count only tests with power of 0.2 or more | Method (updates R03-4) | No |
| Carried | R05-1 (updated), R05-5, R04-2, R03-2, R02-3, R02-4, J6c | | |

## In short

Run 06 matched 1,946 Hooktheory songs the data pack had never measured (mostly chords without melody) to Discogs-VI, with the maintainer's own reduction script and match rule, after its tests were frozen (commit 08b5167). The rebuild reproduced the pack's covers file, groups, version sets and seen y_foreign at 100%. Six tests at p < .05/6 = .0083: none passed. Killed: melody range (+0.69 against −0.7) and diatonicity (−0.29 against +0.5), both weakly, since power was near 0.015. Unsettled: chirality on seen songs (−0.30 against −0.6, p .42), chord repetition on fresh songs (+1.32 against +1.0, SE 1.04, p .20, both halves and the logit positive), the arrow of time (+0.09) and tonic resistance (−0.25).

For the engine nothing changes. The useful results are the re-match (R06-1), the plain fact that the fresh songs are too few to settle the loop question (R06-2), and the data and method items that follow from it.

## Items

### R06-1 The fresh songs: matched, reproduced, and now seen
**Status.** Data-pack note. Replaces R05-2 (done by the research) and updates R05-1.

**Problem.** R05-2 asked for a re-match of the Hooktheory songs the pack leaves out. Tonight the research did it on its own machine: Discogs-VI 20240701 `main.zip` from Zenodo, reduced by `studies/judging_checks/within_artist/cliques_versions.py` unchanged, matched by `studies/covers/covers_match_discogs.py`'s rule keyed by (artist slug, song slug). The fresh songs are now spent: every within-artist Hooktheory song with chords has been joined to y_foreign.

**Evidence.** `run06/experiments/match_validation.json`: 3,080 of 3,080 keys, cliques, cover counts and version sets equal to the pack; seen y_foreign equal for 13,198 of 13,198 songs. Fresh: 1,946 songs, 312 matched, 294 taken up by another artist. Only 10 of the 312 share a Discogs group with a seen song (a faulty flag first reported 223; corrected in four RESULT files). The table is committed at `studies/judging_research/data/fresh_songs_discogs_run06.json` (337 KB; credits both sources).

**Fix.**
1. If the maintainer wants the fresh songs in the data pack, copy that table (or rebuild it with the two scripts above) as `hooktheory_fresh_covers_discogs.json`, marked seen.
2. Add a "seen" ledger beside the hold-out ledger in the README, as R05-1 asked, now with three lines: the 9,588 within-artist rows (runs 04 and 05), the 3,212 single-song-artist songs (run 05, `arrow_singletons`), and the 1,295 fresh battery songs (run 06, commits 08b5167 and 3f39f56).
3. In `make.py` and the README, name the fetchable address of `Hooktheory.json.gz` (`raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz`, sha256 917b7cd5…8e0c) and note that the pack's covers file already holds 222 fresh videos (it was built over every raw video), so that file is itself an outcome for them.

**Check.** The ledger lists the three spent sets. A fresh download's sha256 matches.

### R06-2 749.185 and 749.178: judge the loop gate on the kept rate alone
**Status.** A caveat on a waiting trial. Reading only, no gate. Replaces R05-3.

**Problem.** 749.178 lets the loop-less form become the default only once the fresh songs settle which way covers lean. They cannot. On being taken up at all, chord repetition leans positive in every reading (+1.19 and +1.00 on seen songs, run 04; +1.32 on fresh songs tonight), all unsettled; on how many cover a song once covered it leans negative (749.157, −0.042; 749.158, −0.028, unsettled). The fresh songs gave a standard error of 1.04 points; a powered test needs about 5,400 new within-artist songs (run06/first_principles.md, section 5). The direction reading R05-3 asked for is no longer worth adding: the arrow of time faded on fresh songs (+0.09, SE 1.17).

**Evidence.** `run06/experiments/fresh_repetition/RESULT.md`, `fresh_arrow/RESULT.md`; `studies/judging_checks/within_artist/RESULT.md` and `fresh_songs/RESULT.md` on main.

**Fix.** When 749.185 runs, judge it by whether the engine's loop share matches the kept songs' rate, and cite the cover evidence for neither side. Keep the sentence that the two margins lean opposite ways and neither is settled. Drop R05-3's direction reading.

**Check.** 749.185's report carries the sentence and no cover-based mark.

### R06-3 Recorded: chirality, melody range, diatonicity, and the Hodge downhill share
**Status.** Record only. Nothing to change in the engine.

**Problem.** These were proposed as possible readings of a song's notes. None should become an engine reading or gate.

**Evidence.**
- `chirality`: the signed area a progression sweeps on the circle of fifths. −0.30 points per SD (SE 0.38, p .42), halves −0.62 and +0.03; unsettled. Its unsigned size gave the same lean (−0.31).
- `fresh_range`: melody range capped at three octaves, +0.69 (SE 1.58), killed. Closes run 05's L2.
- `fresh_diatonic`: −0.29 (SE 1.19), killed. With run 05's fifths path, closes the pair.
- `fresh_tonic`: tonic resistance −0.25 (SE 0.75), unsettled a third time; retirement recommended.
- The Hodge gradient ("downhill to home") share of a chord walk's net flow: for one walk it is the unit current from the first chord to the last (‖G‖² equals the effective resistance between them), so it reads only where an excerpt is cut. Stopped on the notes (stability 0.19). Any engine reading of "resolution" from a flow split would read section boundaries, not the harmony.

**Fix.** None in the engine.

**Check.** None needed.

### R06-4 A larger chords corpus with artist and title, for one powered confirmation
**Status.** Data request. New.

**Problem.** The one lead that has survived four nights (chord repetition on being taken up) needs about 5,400 unseen within-artist songs for power 0.5 at one test (about 11,000 for 0.8). Hooktheory has none left.

**Evidence.** `run06/DATA.md`. Chordonomicon (Kantarelis et al. 2024, 666,000 songs, CC BY-NC 4.0, `huggingface.co/datasets/ailsntua/Chordonomicon`, file `chordonomicon_v2.csv`, about 264 MB) is listed and not gated, but its download redirects to a storage host the research machine cannot reach, and its card names Spotify ids, not artist and title.

**Fix.** If the maintainer's machine can fetch it: download `chordonomicon_v2.csv`, report its columns, and if it carries names (or the maintainer can map Spotify ids to names without storing API statistics), match it to Discogs-VI by the existing rule into a file marked unseen, with no measure joined. The research's prediction for it is already written (`run06/first_principles.md`, section 5: chord repetition +1.0 points per SD, one test at .05, killed if at or below zero, run only with power 0.5 or more).

**Check.** The file names its source, licence, match rule and counts, and a hold-out-ledger line is written before any test touches it.

### R06-5 Count only tests with power of 0.2 or more
**Status.** Method. Updates R03-4 (a power floor). Jason decides.

**Problem.** Tonight five fresh tests had power of 0.014 to 0.047, and counting them cut the one well-powered test's bar from .05 to .0083 (chirality's power from 0.35 to 0.15). Their kill lines fire about half the time when there is no effect.

**Evidence.** `run06/experiments/power_fake.json`; `run06/first_principles.md`, section 2.

**Fix.** For the research: count toward .05/N only tests whose fake-outcome power is 0.2 or more; report the rest as estimates, frozen and committed the same way. For the maintainer, the same rule for any 749 reading with several marks.

**Check.** Jason's ruling recorded in the research's next chair.md.

## Carried

- **R05-1, the fetchable Hooktheory address and a "seen" ledger.** Open; folded into R06-1's fix, points 2 and 3.
- **R05-5, the Hooktheory corpus is not hits only.** Open and unchanged.
- **R04-2, cover counts by other artists only, then reread 749.157.** Open. Tonight again no karaoke or tribute set decided any song's y_foreign.
- **R03-2, chord surprise beside repetition in 749.159.** Open.
- **R02-3, the "first performer" flag is 1 for every song.** Open (line 26).
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand.
- **R03-4, a power floor.** Replaced by R06-5.
- **Dropped:** R05-2 (done by the research; R06-1); R05-3 (the direction reading; the arrow faded on fresh songs, R06-2); R05-4 (a record; R06-3 continues it).

## Not proposed

- **Chirality as a reading or gate:** unsettled, and its unsigned size leans the same way, so the "which way" claim is not supported.
- **Chord repetition as a gate in either direction:** its two margins still lean opposite ways and neither is settled.
- **Any engine reading from a Hodge or flow split of a section:** the downhill part reads boundaries (R06-3).

## Sources

- March, P. (2024), Helmholtz-Hodge Decomposition on Graphs, arXiv 2412.09434. https://arxiv.org/abs/2412.09434
- Homs-Dones, MacKay, Sansom & Zhou (2025), Circular Directional Flow Decomposition of Networks, arXiv 2506.12546. https://arxiv.org/abs/2506.12546
- Kantarelis et al. (2024), Chordonomicon, arXiv 2410.22046. https://arxiv.org/abs/2410.22046
- Run 06 on judging-research: commits 08b5167 (predictions), 3f39f56 (results).
- On main: `songs/p68/fixlist_v51.md`; `lib/luthier/REVIEW_stage35.md`; `studies/judging_data/README.md` and `make.py`; `studies/judging_checks/within_artist/`; `studies/covers/covers_match_discogs.py`; `studies/covers/study_covers_discogs.py`.
- Data: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
