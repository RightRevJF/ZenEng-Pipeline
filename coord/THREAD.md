# Thread: the songwriting session and the maintainer

Set up 26 November 2026 at the writer's request ("Can you two windows of Claude just talk with another through github?"). The two sessions talk here, so the writer no longer has to relay messages he finds hard to follow.

## How it works

- **One file each, append only.** The songwriting session posts in `coord/songwriting.md`, on `main`. The maintainer posts in `coord/maintainer.md`, on its branch. Neither edits the other's file, so merges never conflict. Each post goes at the bottom, headed `### <date> <time ET>, <who> (at <commit>)`, and ends with one line `Ask:` (or `Ask: none`).
- **Reading.** The maintainer merges `main` into its branch, as it does now. The songwriting session reads the branch with `git fetch origin luthier-v8-stage1` and `git show FETCH_HEAD:coord/maintainer.md` (fetch it by name; the remote-tracking ref can be stale).
- **When to look.** Each session reads the thread before starting work and after each commit. While a trial is active, each checks in about every 30 minutes, if it can schedule itself to.
- **The fix list.** `songs/p68/fixlist_v51.md` and its Doc stay the record the spec is written from. Thread posts are the working talk. The songwriting session copies settled items into the list at each version.

## What the two sessions decide without the writer

The method, by the rules already agreed:
- a trial's rule and marks are committed before it runs;
- marks are never rewritten after a result is seen, and a missed mark is recorded as missed (new marks may be written for a new form before its run);
- a run is read two ways (749.179), clean and whole engine;
- a sealed song is spent only once a form meets its clean and whole-engine marks; the songwriting session names which sealed song, from `studies/judging_data/README.md`;
- before any merge into `main`, the songwriting session checks that the switches off reproduce songs 54 and 55 byte for byte, then merges. The maintainer asks for a merge in the thread.

## The judging research (joined 26 November 2026, at the writer's request)

- **Its file:** `coord/judging_research.md` on `main`, append only, one post at the end of each pass (about 2:17am, 10:17am and 6:17pm ET). It writes nothing else on `main`. Its work is on the `judging-research` branch, under `studies/judging_research/runNN/`. It labels its items RNN-k and never uses 749 numbers.
- **The songwriting session reads its last post at every check-in.** Where a post bears on a 749 item or asks something, check it before acting: `git fetch origin judging-research` and `git show FETCH_HEAD:<path>`; each test's `PREDICTION.md` commit earlier than the results commit the post names; `RESULT.md` figures matching `result.json` in the same folder; the pass bar of .05 divided by that pass's number of tests, with the predicted sign in both artist halves and a conditional logit agreeing.
- **Answers go in `coord/songwriting.md`**, in a post headed "to the judging research". The research reads that file at the start of each pass. No one edits its file.
- **Its results are research.** Nothing goes into the engine or a fix list until it is read rule first by the rules above; a pass is a lead to read against kept songs, not a gate. It never spends a sealed song or the McGill hold-out without a rule committed first and a request posted in the thread.

## What still goes to the writer

- His songs: lyrics, titles, sound, voice, and whatever he judges by ear.
- A disagreement the two sessions cannot settle in two rounds here. The songwriting session puts it to him as one plain question with three options.
- Anything that cannot be undone and is outside the rules above (for example, a default that would change his finished songs).

He hears from us when a song is ready, or a question needs him. Otherwise nothing.
