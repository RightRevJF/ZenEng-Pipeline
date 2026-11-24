# Run 04: data not on hand

24 November 2026, by the chair. These are ideas from `ideas.json` (status untested, testing or parked) that could not be tested tonight because the data they need is not on this machine. Each one names the exact missing file. Ideas left out for any other reason (a failed gate or withdrawal) are listed in `chair.md`.

| Idea | Why it cannot run tonight | Missing file(s) |
|---|---|---|
| **R03-I2** Tonic resistance (testing; unsettled, −0.019) | A fresh test needs the notes of songs whose covers have not been looked at. On the extensive margin (13,198 songs) it needs the chord notes of every Hooktheory song. `hooktheory_clips.json.gz` holds only the 3,080 matched songs, and testing on those alone would compare by match status. | Sheet Sage's `hooktheory/Hooktheory.json.gz` (github.com/chrisdonahue/sheetsage-data; `make.py` reads it from `/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz` on the maintainer's machine), or the gated Hugging Face dataset `m-a-p/HookTheory`. The data-pack README notes the raw download is not in the repo. |
| **R03-F1** Fifths path (testing; unsettled, −0.017) | Same as R03-I2. | Same file. |
| **R03-G1** Shuffle-relative Ollivier curvature (parked) | On the only rows with notes, its outcome was already seen (run 03 curvature test, β −0.011). A fresh test needs the notes of the unmatched songs. Its family (geometry built from pooled clip maps) was also flagged for deletion in run 03. | Same file. |
| **R04-G1** Diatonicity |a₅|/a₀ (parked) | Withdrawn by its author tonight. Kept for fresh songs, which need the same notes. | Same file (if revived). |
| **W01-J6a** Early covers as the target (parked) | Already run by the maintainer on the matched songs (early −0.028, late −0.030). A new reading needs dated covers for songs not yet looked at, and unmatched songs have no versions or first year. Tonight's covers tests report early and late covers, deciding nothing. | Version lists with years for newly matched songs. That needs the re-match of R03-1: Discogs-VI 20240701 `main.zip` (zenodo.org/records/13983028, 1.4 GB) together with the raw Hooktheory file above. |
| **W01-J6c** Measure the ceiling with MusicLab (untested) | No MusicLab data is on disk: a search of the whole disk found nothing. | The per-song download and rating data of the MusicLab experiment (Salganik, Dodds & Watts, Science 2006). I have not checked its release file name, so it should be pinned when it is fetched. No copy is in the repo, in `studies/judging_data/` or in `/home/claude/scratch/`. |
| **R02-breadth** Cross-genre cover breadth (parked) | Needs genres per version. `discogs_versions_matched.json` carries release ids for joining genres, but not the genres themselves. It also changes the yardstick, which is Jason's call. | The Discogs monthly releases dump matching Discogs-VI, `discogs_20240701_releases.xml.gz` (data.discogs.com). |

Not a data gap, for the record:
- **The McGill whole-song charts** (`studies/harmony/billboard_sections.json`) are on hand.
- **Their only covers outcome is the hold-out**, which is reserved for a measure that has passed first.
- **R02-gap:** this is why it stays untested. On Hooktheory it failed its measure gate in run 03 (see `chair.md`).
