# Run 06: data not on hand

26 November 2026, by the chair. These are ideas from `ideas.json` (status untested, testing or parked) that cannot be tested, or cannot be tested with useful power, because data is missing. Each names the exact missing file. Ideas left out for any other reason (withdrawn, stopped at a gate, renamed) are listed in `chair.md`.

## Resolved or partly resolved tonight
**R05-2 (fresh within-artist songs): partly resolved.** The Discogs-VI 20240701 `main.zip` is on disk (`/home/claude/dl/shape/discogs/main.zip`) and was reduced by the maintainer's own `cliques_versions.py` into `/home/claude/shape/discogs_cliques.json` (348,796 cliques) and `discogs_versions.jsonl`. With the raw Hooktheory file (on hand since run 05), the fresh songs can now be matched by the maintainer's rule after the tests are frozen. Five fresh tests use them tonight (`chair.md`).

What is still missing is size. The raw file has 1,946 fresh songs, and 1,295 of them have another song by the same artist. That gives SEs of 0.85 to 1.8 pp per SD, so power is 0.02 to 0.04 for effects of the size seen so far. The 4,177 raw clips outside the data pack are only 2,570 fresh clips; the other 1,607 are further clips of pack songs.

**R04-FV (ch_rep on fresh songs): on hand; tested tonight** (`experiments/fresh_repetition`), with the low power above.

**W01-J6a (early covers): partly on hand.** The versions file gives each performer set's earliest year, so newly matched fresh songs get dated versions. Tonight's fresh tests report early and late uptake beside each result, deciding nothing (run 02's ruling). A separate test is not worth spending: only the matched fresh songs (a few hundred) carry it.

## Still missing

| Idea | Why it cannot run with useful power tonight | Missing file(s) |
|---|---|---|
| **A powered fresh confirmation** (R05-2's aim; R04-FV, R05-A, R05-L2, R06-I1 on new songs) | 1,295 usable fresh songs give power of 0.02 to 0.04. Several thousand more within-artist songs with notes would be needed. | Hooktheory TheoryTab annotations beyond Sheet Sage's 2022 snapshot (`Hooktheory.json.gz`, 26,175 clips). No public newer export has been identified; Hooktheory's own API needs an account, which is Jason's call. Pin the file when one is found. |
| **W01-J6c** Measure the ceiling with MusicLab (untested) | No MusicLab data on disk. | The per-song download and rating data of the MusicLab experiment (Salganik, Dodds & Watts, *Science* 2006). The release file name is still unchecked; pin it when fetched. |
| **R02-breadth** Cross-genre cover breadth (parked) | Needs genres per version; the versions file has release ids but no genres. It also changes the yardstick, which is Jason's call. | The Discogs monthly releases dump matching Discogs-VI, `discogs_20240701_releases.xml.gz` (data.discogs.com). |
| **A real fame measure** (run 05's fame test; card 2's superstar lead) | Run 05's proxies were Hooktheory traces and ranked game studios first. | Chart history per song (for example the Billboard Hot 100 weekly charts) or artist-level popularity data, joined by artist and title. No file chosen. |

Not data gaps, for the record:
- **The McGill whole-song charts** (`studies/harmony/billboard_sections.json`) are on hand. Their only covers outcome is the hold-out, reserved for a measure that has passed first. Nothing has passed.
- **Card 2's assigned paper** (arXiv 2603.03634, cycle matrices for non-equilibrium Markov chains) could not be read (permission timeout; the PDF fetch gave only the abstract). A reading gap, not a data gap.

## Added after the experiments (the orchestrator, 26 November 2026)

**The "fresh songs are now seen" note.** After tonight, the 1,295 fresh battery songs (and all 1,946 fresh songs' matches) have been joined to y and y_foreign. They are seen songs from here on. Every within-artist Hooktheory song with chords has now been spent on chord repetition.

**Chordonomicon checked as a larger corpus (first principles' way through): not usable from here as it stands.** The Hugging Face dataset `ailsntua/Chordonomicon` (Kantarelis et al. 2024, arXiv 2410.22046; CC BY-NC 4.0; one file, `chordonomicon_v2.csv`, about 264 MB) is listed and not gated, but its download redirects to a storage host this cloud machine's proxy refuses (HTTP 403). Its card describes chords, genre, release date and Spotify IDs; it does not mention artist or title names, so matching it to Discogs-VI by the maintainer's title-and-artist rule would need Spotify lookups (no key here, and none should be stored). The exact need: a copy of `chordonomicon_v2.csv` reachable from zenodo.org or huggingface.co without the redirect, plus a table from Spotify track id to artist name and title (or a corpus that carries names). Both unverified until the file can be opened.
