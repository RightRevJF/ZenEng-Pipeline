# Judging data

Read-only inputs for the nightly judging research: what the covers study uses, so its tests can be run without fetching anything. The nightly run reads this folder and never writes to it. Made on 22 November 2026 by the maintainer (`make.py`).

| File | What it holds | Source and licence | Rebuilt by |
|---|---|---|---|
| `hooktheory_clips.json.gz` | The notes and chords of 5,561 Hooktheory clips of the 3,080 songs matched to a Discogs-VI group. Under `clips`, keyed by clip id; each has `video` (the YouTube video id), the Hooktheory `artist` and `song` slugs, `meters`, `keys`, `melody` and `harmony` as released, and `num_beats`. No audio and no alignment. | Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022; github.com/chrisdonahue/sheetsage-data). **CC BY-NC-SA 3.0**: credit Hooktheory and Sheet Sage, no commercial use, share alike. | `studies/judging_data/make.py` from `Hooktheory.json.gz` |
| `hooktheory_surprise.json.gz` | Per clip (all 21,998 clips with a video, not only the matched songs): `k` (clip id), `vid`, artist, song, and the melody and chord measures of the covers study: surprise (`*_ic_mean`), uncertainty (`*_h_mean`), the Cheung term, and repetition (`mel_rep`, `ch_rep` = the share of chord 3-grams heard earlier in the clip). | Derived from the Hooktheory notes above; CC BY-NC-SA 3.0. | `studies/surprise/surprise_hooktheory.py` |
| `hooktheory_rhythm.json.gz` | Per clip: `k` and the rhythm measures (`rhy_ic_mean`, `rhy_h_mean`, `rhy_cheung`, `sync_per_note`, `rest_share`, `phrase_mean`, `phrase_on_downbeat`, `density`, `length_variety`). | Derived from the Hooktheory notes; CC BY-NC-SA 3.0. | `studies/rhythm/surprise_rhythm.py` (run with `PYTHONPATH=studies/surprise`) |
| `hooktheory_covers_discogs.json` | Per YouTube video id: the song's Discogs-VI group (`clique`), `covers` (the group's distinct performing artist sets, less one), `versions`, `releases`, `first_year`. 3,080 songs. | Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024; zenodo.org/records/13983028). **CC BY-SA 4.0.** | `studies/judging_checks/within_artist/cliques_versions.py` (or `studies/covers/discogs_cliques.py`), then `studies/covers/covers_match_discogs.py` |
| `discogs_versions_matched.json` | Per matched Discogs-VI group: `video`, `first_year`, and every version as [performing artists, year of its earliest release, up to two Discogs release ids]. For covers by period, and for joining genres from the Discogs data dump by release id. (This is R02-2's table.) | Discogs-VI 20240701; CC BY-SA 4.0. | `studies/judging_checks/within_artist/cliques_versions.py` |
| `mcgill_covers_discogs_HOLDOUT.json` | **A hold-out. Do not explore on it.** Cover counts for 438 McGill Billboard songs that are not among the Hooktheory songs. | McGill Billboard charts (`studies/harmony/billboard_sections.json`) matched to Discogs-VI; CC BY-SA 4.0. | `studies/judging_checks/fresh_songs/test.py` |

## What is not here, and why

**YouTube views, subscribers and durations are left out.** YouTube's API terms do not allow statistics fetched through the API to be kept beyond thirty days without refreshing them, or to be handed on as a data set, and a file committed here would do both. They are fetched by `studies/surprise/fetch_youtube.py` (it needs a YouTube Data API key in `/root/.secrets/youtube_key`) and stay outside the repository. Without them, hold the artist and the first year. For the size of what that costs: the within-artist test with views held gave −0.042 for chord repetition; views and covers are unrelated once the year is held (r = −0.00), so leaving views out should move little.

The raw downloads (Sheet Sage's `Hooktheory.json.gz`, 20 MB; Discogs-VI's `main.zip`, 1.4 GB) are not here; the scripts above rebuild everything from them.

## How to join

A song is a YouTube video id. `hooktheory_covers_discogs.json` is keyed by it; each clip in the two measure files carries it as `vid`, and each clip in `hooktheory_clips.json.gz` as `video`. A song's measure is the mean over its clips, weighted by `n_mel` (as `studies/covers/study_covers_discogs.py` does). The artist is the clip's `artist` slug. The covers study's rows are the songs with a group, measures in both files, and a first year (2,360 when views are also required).

## What has already been run on these files

- The covers study (`studies/covers/covers_study_report.md`): chord repetition against covers −0.071 across artists.
- The within-artist test (`studies/judging_checks/within_artist`): −0.042, p .009, rule committed first.
- The fresh-songs test on the hold-out (`studies/judging_checks/fresh_songs`): −0.028, range −0.11 to +0.05, 438 songs; same direction, not settled.

## The hold-out rule

The McGill cover counts were joined once, for one test whose rule was committed first. They stay useful only while they are not explored. Before any new measure is tried against them: write its rule and its pass mark, commit it, then run it once; and count every such test in the report, since each one spends the hold-out a little.

## The hold-out ledger (749.169)

Write a line here **before** running anything against a hold-out, so no test is run twice by two hands.

| Date | Who | Hold-out | Test (its rule, committed first) | Result |
|---|---|---|---|---|
| 22 Nov 2026 | the maintainer | McGill cover counts | chord repetition against covers, fresh songs (`studies/judging_checks/fresh_songs`, rule f25209f): the test of record | −0.028, range −0.11 to +0.05; not settled |
| 22 Nov 2026 | the songwriting session | McGill cover counts | the same question, its own model (`studies/fresh_songs`, rule 59182c6) | −0.060, range −0.154 to +0.034; not settled |

Two readings spent on one question, by accident. Hold-out songs for the engine (59 for everything; 50 and 63 banked, not yet run by anything) are listed in `lib/luthier/README.md`.
