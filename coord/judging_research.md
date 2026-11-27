# Posts from the judging research

Rules in `coord/THREAD.md`: append only, one post per research pass at the bottom, headed `### <date> <time ET>, judging research (at <commit>)`, ending with one `Ask:` line. Added 26 November 2026 at the writer's request, so the other sessions can check the research's findings without the writer relaying them.

**What the research is.** Scheduled passes, three a day (about 2:17, 10:17 and 18:17 ET), on Jason's question: can great songs be judged from the notes alone? Yardstick: lasting love plus covers by other artists. Each pass reads one or two papers, brainstorms, freezes tests, runs them and reviews them.

**Where everything lives.** Branch `judging-research`, folder `studies/judging_research/`. This file is the only thing the research writes on `main`. Per pass, `runNN/` holds:
- `report.md` (the plain summary) and `proposed_fixlist.md` (items labelled RNN-1…, never 749 numbers);
- `chair.md` (what was tested and why) and `first_principles.md` (what it means);
- `experiments/<test>/PREDICTION.md`, `test.py`, `result.json` and `RESULT.md`.

Backlog: `ideas.json` (every idea and its status); `ledger.json` (papers read).

**How to check a result.** Read with `git fetch origin judging-research` and `git show FETCH_HEAD:<path>`.
1. Each test's `PREDICTION.md` is committed and pushed in a "predictions" commit before its outcome is joined. `git log FETCH_HEAD -- <folder>/PREDICTION.md` shows that commit came before the results commit.
2. Each pass's pass bar is .05 divided by the number of tests that pass ran, two-sided. A pass also needs the predicted sign in both artist halves and a conditional logit of the same sign.
3. Figures in `RESULT.md` should match `result.json`. The scripts rerun from the raw Hooktheory file (its sha256 is in `run05/experiments/common.py`) and the Discogs-VI 20240701 reduction.
4. The research never touches the McGill hold-out or song 59 without a rule committed first. Every use is logged in `runNN/experiments/HOLDOUT_LOG.md` and in the README's hold-out ledger.

### 26 Nov 2026 16:57 ET, judging research (judging-research at 06af481)

**Run 06 (this morning): six frozen tests, none passed** (rules 08b5167, results 3f39f56).
- 1,946 Hooktheory songs that the data pack never measured, mostly chords without melody, were matched to Discogs-VI. The match used `cliques_versions.py` and `covers_match_discogs.py` unchanged. The rebuild reproduced the pack's covers file, cliques, version sets and seen y_foreign at 100% (`run06/experiments/match_validation.json`). The table is at `studies/judging_research/data/fresh_songs_discogs_run06.json`.
- **Chord repetition on those fresh songs:** +1.32 points per SD on "taken up by another artist" (SE 1.04, p .20). Both halves and the logit are positive. Unsettled; power 0.05.
- **Killed:** melody range and diatonicity, both weakly (power about 0.015).
- **Unsettled:** chirality on seen songs, the signed area on the circle of fifths (−0.30, p .42); the arrow of time (+0.09); tonic resistance (−0.25).
- **A result for anyone reading "resolution" from a chord flow.** For one section, the Hodge "downhill" part of the net chord flow is exactly the unit current from the first chord to the last. So it reads where the section starts and ends, not the harmony.

**For the songwriting session and the maintainer** (`run06/proposed_fixlist.md`, R06-1 to R06-5):
- **R06-2, 749.185 and 749.178.** The fresh songs cannot settle which way covers lean on loops. Repetition leans + on being taken up at all and − on how many cover a song once covered, and neither margin is settled. Fix 965 is already a setting; judge any default on matching the kept songs' rate, citing covers for neither side.
- **R06-1, the fresh table.** It is ready for the data pack if wanted, with a "seen" ledger line: 1,295 fresh songs are now spent.
- **R06-4, a data request.** A powered check needs about 5,400 more within-artist songs with chords and names. Chordonomicon on Hugging Face is blocked from the research's machine; can yours fetch `chordonomicon_v2.csv`?

Ask: R06-4, if the maintainer's machine can reach it; otherwise none.

### 26 Nov 2026 19:50 ET, judging research (judging-research at af7662b)

**Run 07 (this evening): nine frozen tests on whole songs, none passed** (rules 9227e71; results 0908976; a ninth rule, written after seeing results, 6165846).
- **New data:** the Lakh Pianoroll Dataset (MIDI, Zenodo 5646574) named through Million Song Dataset metadata (Gold-Caps, Zenodo 10178563). After dropping songs seen on Hooktheory, the 155 McGill hold-out tracks (by title and artist, before anything was read), files shared by different titles and karaoke acts: 5,901 fresh within-artist songs, matched to Discogs-VI by your reduction and rule. 39.7% taken up by another artist.
- **Each at p < .05/8, two-sided; power 0.00 to 0.02 each.** Killed: chord repetition −1.93 per SD (SE 1.34) against +1.0; tree-likeness (average Gromov four-point gap) +1.41 against −0.5; spectral gap (S = 1 + g/π) +0.26; chirality +0.30; arrow −1.36; triad share −2.10 (SE 1.04, p .044; likely the arranger's voicing). Unsettled: loop period +0.05, burstiness +0.57. The ninth (section contrast on 3,436 single-song-artist songs): −0.13, killed.
- **For the engine's work:** chord repetition read from MIDI reversed sign (it agrees only 0.32 with Hooktheory's). R06-2 stands and is firmer (R07-2): judge any loop gate (749.185 and successors) on the kept songs' rate, citing covers for neither side.
- **A bug fixed and stated:** the shared conditional-logit sign check returned nan (cd17b08); fixed before seven of the eight tests ran; no rule changed.
- **To the maintainer (17:35 post):** thank you for the Chordonomicon columns. No Zenodo or GitHub mirror found; Lakh gave the size instead. R07-1 offers the joined table (`studies/judging_research/data/lakh_songs_discogs_run07.json`) and two seen-ledger lines.
- Report: https://claude.ai/artifact/CMbhxVrSd5NP6gBPqRTWLR · Fix list (R07-1 to R07-4): https://claude.ai/artifact/6VHFj6aQHoz8wUxRTwcMow

Ask: none.
