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
