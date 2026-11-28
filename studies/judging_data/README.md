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

## The fresh songs (judging research, run 06; R06-1)

`hooktheory_fresh_covers_discogs.json`: the 1,946 Hooktheory songs in Sheet Sage's file that the rest of this pack never measured (mostly chords without melody), matched to Discogs-VI by the pack's own rule on the research's machine; 312 matched, 294 taken up by another artist. **Seen, not a hold-out:** run 06 joined them to six measures. Copied unchanged from `studies/judging_research/data/fresh_songs_discogs_run06.json` on the judging-research branch. Checked here against the maintainer's own clique table: all 312 matched cliques agree on artist and title, and none of the 1,634 unmatched would match by exact title and artist. Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).

Note: `hooktheory_covers_discogs.json` was built over every raw video, so it already holds outcomes for 222 of the fresh songs' videos. It is an outcome for them too.

## The Lakh songs (judging research, run 07; R07-1)

`lakh_covers_discogs.json`: 5,901 whole songs from the Lakh Pianoroll Dataset (LPD-5 cleansed; MIDI arrangements), named through the Million Song Dataset metadata, by artists with two or more songs in the set, matched to Discogs-VI 20240701 by this pack's reduction and title-and-artist rule on the research's machine; 2,387 matched, 2,343 taken up by another artist (39.7 in 100). Songs already on Hooktheory, the McGill hold-out's songs (by title and artist, before anything was read), MIDI files shared by different titles, and karaoke or tribute acts were left out. Copied unchanged from `studies/judging_research/data/lakh_songs_discogs_run07.json` on the judging-research branch (af7662b). Derived from Discogs-VI: CC BY-SA 4.0. Not rebuilt here: the raw Lakh files were not fetched to this machine, so the table's keys have not been reproduced from `common.lakh_songs()`; the check of run 07 (`studies/judging_checks/run07/CHECK.md`) says what was and was not verified.

**Seen, not a hold-out, two sets:**
- the 5,901 within-artist Lakh songs: joined to "taken up by another artist" and eight measures in run 07 (rules 9227e71, results 0908976);
- 3,436 further Lakh songs by single-song artists: joined in run 07's ninth test, whose rule (6165846) was written after the first eight results were seen. These are not in the table.

A caution for any later use: the measures in this table are read from an arranger's MIDI file. Chord repetition read this way agrees only 0.32 with Hooktheory's on 1,487 shared songs.

Sources: `lpd_5_cleansed.tar.gz` and `metadata.zip`, Zenodo 5646574 (CC BY 4.0); `gold-caps_lmd-matched_general_v0.json`, Zenodo 10178563 (CC BY 4.0); `msd_bb_matches.csv`, Zenodo 3258042.

## Where the raw files are

- Sheet Sage's `Hooktheory.json.gz` (20 MB): `https://raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz`, sha256 `917b7cd58f5f4e07d6c36acf7bfad958c99ee05472dab3555399141094698e0c` (the maintainer's copy and the research's agree).
- Discogs-VI 20240701 `main.zip` (1.4 GB): `https://zenodo.org/records/13983028`.

## The seen ledger (R05-1, R06-1)

What has been joined to an outcome and by whom, so nobody takes a spent set for a fresh one.

| Set | Songs | Joined to measures in | Outcome |
|---|---|---|---|
| Within-artist rows (artists with two songs or more) | 9,588 | judging research runs 04 and 05; `studies/judging_checks/within_artist` | covers; taken up by another artist |
| Single-song-artist songs | 3,212 | judging research run 05 (`arrow_singletons`) | taken up by another artist |
| Fresh battery songs (of the 1,946 above, those with another song by the same artist) | 1,295 | judging research run 06 (commits 08b5167, 3f39f56) | taken up by another artist |

Every within-artist Hooktheory song with chords is now spent. A powered check of chord repetition needs about 5,400 unseen within-artist songs (run 06); none are on hand.

## How to join

A song is a YouTube video id. `hooktheory_covers_discogs.json` is keyed by it; each clip in the two measure files carries it as `vid`, and each clip in `hooktheory_clips.json.gz` as `video`. A song's measure is the mean over its clips, weighted by `n_mel` (as `studies/covers/study_covers_discogs.py` does). The artist is the clip's `artist` slug. The covers study's rows are the songs with a group, measures in both files, and a first year (2,360 when views are also required).

## What has already been run on these files

- The covers study (`studies/covers/covers_study_report.md`): chord repetition against covers −0.071 across artists.
- The within-artist test (`studies/judging_checks/within_artist`): −0.042, p .009, rule committed first.
- The fresh-songs test on the hold-out (`studies/judging_checks/fresh_songs`): −0.028, range −0.11 to +0.05, 438 songs; same direction, not settled.

## A floor on power for counted tests (R06-5; ruled 26 November 2026)

The writer left the ruling to the maintainer, who rules yes. **A test counts toward the shared bar (.05 over the number of tests) only if its power is 0.2 or more**, reckoned from fake outcomes or from the test's own standard error against its written prediction, before the real outcome is joined. Tests under the floor are still frozen and committed with their predictions, and are reported as estimates: they pass nothing and kill nothing. The same floor holds for the maintainer's readings with several marks.

Why: in run 06 five tests with power of 0.014 to 0.047 cut the one test that could have seen something from a bar of .05 to .0083, and at that power a "kill" fires about half the time on nothing.

## The hold-out rule

The McGill cover counts were joined once, for one test whose rule was committed first. They stay useful only while they are not explored. Before any new measure is tried against them: write its rule and its pass mark, commit it, then run it once; and count every such test in the report, since each one spends the hold-out a little.

## The hold-out ledger (749.169)

Write a line here **before** running anything against a hold-out, so no test is run twice by two hands.

| Date | Who | Hold-out | Test (its rule, committed first) | Result |
|---|---|---|---|---|
| 22 Nov 2026 | the maintainer | McGill cover counts | chord repetition against covers, fresh songs (`studies/judging_checks/fresh_songs`, rule f25209f): the test of record | −0.028, range −0.11 to +0.05; not settled |
| 22 Nov 2026 | the songwriting session | McGill cover counts | the same question, its own model (`studies/fresh_songs`, rule 59182c6) | −0.060, range −0.154 to +0.034; not settled |
| 25 Nov 2026 | maintainer | Song 63 (the engine's banked lyric) | The gentler loop gate, 749.178: `studies/v48_trials/PREDICTION.md` section 3; run once, and only if the seen-song checks hold | **Not run.** The seen-song checks failed (`studies/v48_trials/RESULT.md`). Song 63 is still sealed. |
| 25 Nov 2026 | the writer (ruling, via the songwriting session) | Song 50 (the engine's banked folk lyric, 4/4, 88) | The third form of 749.182, the way back inside the line (749.189, `songs/p68/fixlist_v50.md`): run once by the engine with the form on, and only if every seen-song check of 749.189 holds; the same marks | **Approved, not yet run.** The maintainer writes the run's own line here before running it. |
| 25 Nov 2026 | maintainer | Song 50 | The same (749.189). The third form had been run on the seen songs before the list reached me (`studies/the_draw/RESULT_line.md`, its rule at `PREDICTION_line.md`). | **Not run.** The seen-song checks fail by the list's marks as by mine: living builds under v47's in songs 55, 49 and 61; the clean reading over 17.5 in five songs of six. Song 50 is still sealed. |
| 25 Nov 2026 | maintainer | Song 50 | The shared octave bin with the plant given 240 draws (749.192, `studies/the_peak_line/PREDICTION_tail_tries.md`): once, only if the seen-song marks hold | **Not run.** Mark 5 fails on the seen songs (builds holding a leap 17.9, 18.1, 24.2 in 100 in songs 55, 58, 59). Song 50 is still sealed. |
| 25 Nov 2026 | maintainer, on the writer's word ("Yes. Try it!") | Song 50 | The octave bin shared, 60 draws, frozen (749.191): `studies/the_peak_line/PREDICTION_song50.md`, four marks. Run once: v47 and the form. | **Run, once. All four marks hold:** living builds 154 to 243; builds' words' fit 0.248 and 0.248; the chosen tune's range 17 (floor 14.55) and the builds' middle range 16 against 15; gate off, 15.4 builds in 100 holding a leap (17.5 asked; v47 40.3). Built as fix 964 (`studies/the_peak_line/RESULT_song50.md`). **Song 50 is spent: a seen song from here on.** The session's later note that song 50 stays sealed was overtaken by the writer's word to me. |
| 25 Nov 2026 | the writer (ruling, via the songwriting session) | Song 64 ("Go On Ahead", `songs/p74/lyric64.json`; banked tonight, never run) | The carrying line's centre (749.191, `songs/p68/fixlist_v50.md`): run once by the engine with the form on, only if every seen-song check of 749.191 holds; the same marks | **Not run; still sealed, now unreserved.** The reading of 749.191 did not name the centre (`studies/the_peak_line/RESULT.md`), so no centre form was tried. (This row said song 50 stayed sealed; the writer's later word to the maintainer spent it, above.) |
| 25 Nov 2026 | the songwriting session | Song 65 ("Hold It All Together", `songs/p75/lyric65.json`; disco-funk, 4/4, 116, alto; banked tonight, never run) | None yet | **Banked, sealed, unreserved.** |
| 26 Nov 2026 | the writer (via the songwriting session) | Song 66 ("They Did the Right Thing", `songs/p76/lyric66.json`; dark indie folk-rock, 4/4, 72, minor, tenor; banked today, never run) | The maintainer's drafting fix (the borrow and again() form of 749.208), when it is built: offered as that fix's fresh test song, then made for real with the writer's design notes (`songs/p76/intake.py`) | **Banked, sealed, reserved for the drafting fix.** |
| 26 Nov 2026 | the writer (via the songwriting session) | Song 67 ("A Door in the Coral", `songs/p77/lyric67.json`; hazy indie, 4/4, 70, baritone; banked today, never run; every verse line 7 syllables) | Made for real once the drafting fix lands (after song 66's test), as the first song written to the matched-count craft note | **Banked, sealed, reserved to be made after the fix.** |
| 26 Nov 2026 | maintainer, on the road agreed with the songwriting session (`coord/songwriting.md`, 12:55) within the writer's ruling C | Song 66 ("They Did the Right Thing") | The pair (the borrow by the count as a true repeat, with the chord tie), frozen: `studies/borrow_kept/PREDICTION_song66.md`, seven marks. Run once: v50 and the pair. | **Run, once. Six marks of seven hold; mark 7 fails:** the builds' middle pitch scaling 1.062 against v50's 0.912 (kept middle 0.905; the margin 0.03). Pool 33 and 46; words' fit 0.260 and 0.293; verses over the ceiling 17.0 and 2.7 in 100; true repeats 0.052 and 0.053; clashes 0.26 and 0.24; surprise 3.43 and 3.12. **The pair is not built. Song 66 is spent** (`studies/borrow_kept/RESULT_song66.md`). |
| 26 Nov 2026 | maintainer, on the songwriting session's word (`coord/songwriting.md`, 15:05) | Song 63 ("We Saved You a Plate") | The loop gate with a chance, 749.185: `studies/loop_chance/PREDICTION_song63.md`. Run once by v50 with `LUTHIER_LOOP=chance`; the setting from the switch, the lyric file untouched. | **Run, once. Both deciding marks hold:** pool 10 (the mark: 10 or more; exactly at it), builds' middle words' fit 0.361 (floor 0.152). Built as fix 965, a setting. Read after and deciding nothing: v50 without the form gives a pool of 14 on a different chord draft. **Song 63 is spent** (`studies/loop_chance/RESULT_song63.md`). |
| 26 Nov 2026 | maintainer, on the songwriting session's word (`coord/songwriting.md`, 21:25) | Song 64 ("Go On Ahead") | The copy and the melisma's second note (749.223, 749.225), frozen as a pair: `studies/returning_clash/PREDICTION_song64.md`, nine marks. Run once: v52 and the pair. | **Run, once. All nine marks hold.** Clashes 0.545 to 0 per 100 notes, all of them on a melisma's second note; pool 14 and 14; living builds 307 and 307; the same chosen build. **The song has no copied line over a changed chord, so it tested fix 967 (the melisma's second note) and gave fix 966 (the copy) nothing to do.** Song 64 is spent (`studies/returning_clash/RESULT_song64.md`). |
| 28 Nov 2026 | the songwriting session, on the writer's word ("B", 12:23 ET) | Song 68 ("Save Me from My Muse", `songs/p78/lyric68.json`; 3/4 pop-punk, tenor, 180) | The pop 3/4 package of the maintainer's 12:12 ET post (`songs/p68/fixlist_v54.md`, "The pop 3/4 package"), the metre engine at `luthier-v8-stage1` 992a687e, unchanged. Run once at the lyric's own seed (1), 1,000 builds, by the planner's own routine with `studies/other_metres/pool_count.py`. Read once: every figure mark on the pool's median and on the pick (notes a bar 2.38 to 3.85; onsets on a beat 0.508 or more; K3 off the beat 0.26 or under; range 12 or more; pitches 7 or more; K5 0.303 or under; K6 rhythm again 0.349 to 0.871, figure again 0.667 or under); the six-mark share of the pool (76.2); the pick in the voice with no leap past an octave in a line; K3's first beat watched. **The pick is the song, whatever the reading. A miss is recorded as a miss, and nothing is rerun under a changed form.** | **Run, once (12:26 ET; record written by the same call at 12:30, same pick bc986befea6b; a first attempt void at the band step, KeyError 'pop-punk', so the run copy `lyric68.run.json` has genre rock, and the melody reads genre only through FAMILY, the same either way).** The pool's median meets every figure mark: notes a bar 3.843, onsets on a beat 0.545, off the beat 0.215, range 17, pitches 10, K5 0.263, K6 rhythm 0.402 and figure 0.196. **The six-mark share is 45.5 in 100, against 76.2: missed** (notes a bar met by 53.1 in 100, the lyric dense at 180). **The pick misses K6's rhythm line by 0.001** (0.348 against 0.349); range 14 (C4 to D5), commonest 0.238, first beat 0.42 (watched), off the beat 0.215, no leap past an octave. Bar rhythms in 16 bars: 6.0 (the clips' 6); exact two-bar repeats 0.208 (the clips' 0.231). Melisma share drawn 0.162. `songs/p78/run68_pool_reading.json`. **Song 68 is spent.** |

Two readings spent on one question, by accident. Hold-out songs for the engine (59 for everything; 65 and 67 banked, not yet run by anything; 64 spent on fixes 966 and 967, 26 November; 63 spent on fix 965, 26 November; 66 spent on the pair, 26 November, which failed its pitch-scaling mark; 50 spent on fix 964) are listed in `lib/luthier/README.md`.
| 68 | Save Me from My Muse | 3/4 punk waltz, tenor | banked, unrun; the real 3/4 test after the trial on song 53's words | 2026-11-27 |
| 69 | Learned It from My Hands | 6/8 folk protest ballad, baritone | banked, unrun; the real 6/8 test after the package passes on songs 52 and 61 | 2026-11-27 |
| 70 | Strangers Till the Chorus | 3/4 pop anthem (stomp-and-clap), alto | banked, unrun; written by the test-songs window | 2026-11-28 |
| 71 | Never Keep Perfect Time | 6/8 mythic folk ballad, tenor | banked, unrun; written by the test-songs window | 2026-11-28 |
