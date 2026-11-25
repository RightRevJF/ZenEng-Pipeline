# Run 05: data not on hand

25 November 2026, by the chair. These are ideas from `ideas.json` (status untested, testing or parked) that cannot be tested tonight because the data they need is not on this machine. Each names the exact missing file. Ideas left out for any other reason (withdrawn, stopped at a gate, repetition renamed) are listed in `chair.md`.

## Resolved tonight
**R04-1, the notes of every Hooktheory song: resolved.** Sheet Sage's `Hooktheory.json.gz` was found at `raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz`. It is 20,075,896 bytes, sha256 917b7cd5…e0c (checked by `common.raw_clips()`), CC BY-NC-SA 3.0, and is kept outside the repo at `/home/claude/dl/hooktheory/`; it is never committed. It holds 26,175 clips, including all 16,563 behind run 04's 9,588 within-artist rows. The gated Hugging Face copies were not touched.

This unblocked R03-I2 (tonic resistance) and R03-F1 (fifths path) on the extensive margin, and R04-G1 (diatonicity), merged into the fifths path. All three are in tonight's tests. It also unblocked R03-G1 (shuffle-relative curvature), which was left out for another reason (`chair.md`).

## Still missing

| Idea | Why it cannot run tonight | Missing file(s) |
|---|---|---|
| **R04-FV** The two-part story (ch_rep on y_foreign) on fresh songs (testing; unsettled, +1.00, p .044) | All 9,588 within-artist songs were used for this in run 04. Fresh songs exist in the raw file: 4,177 of its clips are outside the data pack's 13,198 songs, many with harmony only. But they have never been matched to Discogs-VI, so they have no y or y_foreign. | Discogs-VI 20240701 `main.zip` (zenodo.org/records/13983028, 1.4 GB), to re-match those clips' songs by title and artist (fix-list R03-1). The raw Hooktheory file above is now on hand, so this is the only missing piece. |
| **W01-J6a** Early covers as the target (parked) | Already run by the maintainer on the matched songs (early −0.028, late −0.030). A new reading needs dated covers for songs not yet looked at. Unmatched songs have no versions or first year. | Version lists with years for newly matched songs, from the same re-match: Discogs-VI 20240701 `main.zip` with the raw Hooktheory file (now on hand). |
| **W01-J6c** Measure the ceiling with MusicLab (untested) | No MusicLab data is on disk. | The per-song download and rating data of the MusicLab experiment (Salganik, Dodds & Watts, Science 2006). The release file name was not checked, so it should be pinned when fetched. |
| **R02-breadth** Cross-genre cover breadth (parked) | Needs genres per version. `discogs_versions_matched.json` has release ids but no genres. It also changes the yardstick, which is Jason's call. | The Discogs monthly releases dump matching Discogs-VI, `discogs_20240701_releases.xml.gz` (data.discogs.com). |
| **Card 2's lead and the fame test's next step** (new; not in `ideas.json`) | Tonight's fame proxies are Hooktheory traces: the artist's song count and clips per song. A real fame measure would separate fame from genre and era. | Chart history per song (for example the Billboard Hot 100 weekly charts) or artist-level popularity data, joined by artist and title. No file has been chosen. |

Not a data gap, for the record:
- **The McGill whole-song charts** (`studies/harmony/billboard_sections.json`) are on hand. Their only covers outcome is the hold-out, reserved for a measure that has passed first.
- **Perea & Harer (2015) and Gakhar & Perea (2023)** could not be read tonight (PDF only; `paywalled.md`). They are free on arXiv, so this is a reading gap, not a data gap.
