# Run 11: data

28 November 2026, the 02:17 ET pass.

## Used this pass
- **Hooktheory clip melodies and chords**: Sheet Sage's `Hooktheory.json.gz` (raw.githubusercontent.com/chrisdonahue/sheetsage-data, sha256 917b7cd5...e0c, checked), outside the repo at /home/claude/dl/hooktheory. CC BY-NC-SA 3.0; credit Hooktheory and Sheet Sage (Donahue, Thickstun & Liang 2022).
- **Rows:** run 04's 9,588 within-artist songs (1,741 artists), from the data pack's `hooktheory_surprise.json.gz` and `hooktheory_rhythm.json.gz` on origin/main (read only), via run05/experiments/common.py.
- **Outcome:** y_foreign (taken up by another artist) from the data pack's `hooktheory_covers_discogs.json` and `discogs_versions_matched.json` (Discogs-VI 20240701, CC BY-SA 4.0), joined only through `common11.load_outcomes` after the predictions were pushed (e1858c0).
- **Notes-side cache:** /home/claude/dl/run11/measures_run11.json (26 MB; rebuilt by `experiments/build_cache11.py`; not committed).

## Not used, and why
- **TheSession.org: withdrawn.** Its licence forbids processing by large language models (`run10/WITHDRAWN.md`). Not downloaded, not read. Split H was never opened.
- **The McGill hold-out:** chords only, no melody, so no melody measure can be tried on it. Not touched; nothing logged against it (`experiments/HOLDOUT_LOG.md`).

## Spent this pass (seen, said plainly)
- The 9,588 within-artist songs: already seen (runs 04 to 06, chord measures and a few melody and rhythm measures); this pass joined them to eight more measures (melody pitch graph, melody-chord table, scale-degree profile, anticipation, self-learnability, corpus surprisal, contour peaks, pitch-class entropy). They are now heavily re-spent.
- The 3,610 single-song-artist songs: seen in run 05 (one chord measure); this pass joined them to pitch-class entropy (rep_singletons_after, a lead written after seeing results).

## Still missing (the obstacle: no unseen melodies with names)
| Need | Missing file(s) |
|---|---|
| A confirmation of REP (pitch-class entropy) on melodies never joined to an outcome | Any corpus of pop or folk melodies with titles and artists, under a licence that allows LLM processing, not yet matched: candidates the maintainer's machine may reach: POP909 (github.com/music-x-lab/POP909-Dataset, melody tracks with song names; licence to check), the Lakh MIDI "lmd_matched" files with a vocal or melody track (colinraffel.com; CC BY 4.0), the Wikifonia lead sheets in ChoCo only where melody is kept, OpenScore Lieder (CC0) for art song |
| Lasting love as distinct from uptake | A time series of plays or covers by year (Discogs-VI has version years; a "covers after year X" outcome is possible for the matched songs but they are seen) |
| The late-window ii-V lead (R09-4) | A Discogs release dump newer than July 2024 |
| R02-breadth | `discogs_20240701_releases.xml.gz` (genres per release; data.discogs.com not reachable) |
| W01-J6c the MusicLab ceiling | The MusicLab per-song data (Salganik, Dodds & Watts 2006) |
