# Proposed list from the judging research, run 04 (for the maintainer)

24 November 2026. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run04 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, DATA.md, first_principles.md, and the six folders under experiments/.

Nothing here is in the engine. Labels R04-1 to R04-4 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (1b46833) before proposing, read only.** It is unchanged since run 03.
- `songs/p68/fixlist_v46.md` is still the latest list (next finding 749.170).
- `lib/luthier/REVIEW_stage30.md` is still the latest review.
- 749.158 (fresh songs, unsettled) and 749.159 (the loop-less trial, going ahead) are open.
- 749.169 (a hold-out ledger) is open: `studies/judging_data/README.md` has no ledger yet.
- `studies/covers/study_covers_discogs.py` line 26 still sets `original=1.0`, so R02-3 is open.
- `hooktheory_clips.json.gz` holds the notes of the 3,080 matched songs only.
- No item on main proposes Fourier-phase measures, foreign versions or the extensive margin, so nothing below repeats a closed item.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R04-1 | The notes of all 21,998 Hooktheory clips in the data pack | Data request | No |
| R04-2 | Cover counts that leave out the original artist's own credit variants; reread 749.157 on them | Data fix + rule-first reread | No |
| R04-3 | 749.159: keep the loop-less trial a reading until the two-part story is settled | Reading caveat on an open trial | Reading only, no gate |
| R04-4 | Torus geometry and the extensive-margin tests: five kills, recorded | Record | No |
| Carried | R03-1 (updated), R03-2, R03-4, R02-3, R02-4, J6c; 749.169 noted; R03-3 closed | | |

## In short

Run 04 froze five hypotheses before any outcome was joined (commit 00ab557), and all five were killed by their rules. The most useful result is the outcome tried for the first time: whether a Hooktheory song is in Discogs-VI at all, within artist, on 9,588 songs. There, chord repetition went the wrong way for J1: songs that loop more were more often versioned at all, +1.19 points per SD (p .018; conditional logit p .009; both halves positive).

A sixth test, frozen after seeing that result (commit 4410a0e), checked whether the sign came from the original artist's own "featuring" variants. It did not. Only 94 of 2,224 matched songs have no version by anyone else, and +1.00 of the +1.19 sits in versions by other artists. But p was .044 against .0083, so it is a lead and not a finding.

If the lead holds, looping less within a verse trades a lower chance of being taken up for more distinct coverers once taken up. That bears on 749.159 (R04-3). It also shows that the cover count used everywhere includes the original artist's guest variants (R04-2).

## Items

### R04-1 The notes of every Hooktheory clip, not only the matched ones
**Status.** Data request. Never run.

**Problem.** Every notes-based measure can be tested only on the 3,080 matched songs, and those have now been looked at by every test since run 02. The new outcome (in Discogs-VI at all) spans 13,198 songs, but only the per-clip summary measures exist for the 10,429 unmatched ones. Geometric measures that were unsettled or untested therefore have no fresh songs: tonic resistance, the fifths path, diatonicity and the torus measures.

**Evidence.**
- `run04/DATA.md`.
- `run04/searches.md`: the Hugging Face copy `m-a-p/HookTheory` is gated, and it was not downloaded.
- `run04/experiments/move_extensive/RESULT.md`: 9,588 within-artist rows from the summary files.

**Fix.** Add `studies/judging_data/hooktheory_clips_all.json.gz` to the data pack, built by `make.py` from Sheet Sage's `Hooktheory.json.gz` with the same fields as `hooktheory_clips.json.gz`, for all 21,998 clips with a video. It is about 7 MB at the current file's rate (1.9 MB for 5,561 clips).
- Commit it without any outcome field. The match status stays in `hooktheory_covers_discogs.json` as now.
- Licence: CC BY-NC-SA 3.0, credit Hooktheory and Sheet Sage.

**Check.**
- The file's clip count equals the surprise file's (21,998).
- For the matched clips, its notes are byte-equal to `hooktheory_clips.json.gz`.
- The README's "what has already been run" section names which songs have been seen against which outcome.

### R04-2 Count covers by other artists only, then reread 749.157 on that count
**Status.** Data fix and rule-first reread. Never run as a test.

**Problem.** `covers` in `hooktheory_covers_discogs.json` is the group's distinct performer sets less one. "Artist" and "Artist featuring Guest" are two sets (card 2; `cliques_versions.py`). So the count used by the covers study, by 749.157 and by every research test so far includes the original artist's own credit variants.

**Evidence.** `run04/experiments/foreign_versions/RESULT.md`. Within the outcome "versioned at all", 94 of 2,224 matched songs have only own-artist variants. It also notes alias misses, such as "beachboys" against "thebeachboys". The size of the effect on the count itself has not been computed. This list does not look at it, so the reread stays fresh.

**Fix.**
1. Add `covers_foreign` per song, the number of performer sets sharing no normalised name with any set that contains the original artist, and the flag `foreign_any`. Use the normalisation of `covers_match_discogs.py` plus a leading-"the" strip, written into `make.py`.
2. Commit a rule first: the within-artist test of 749.157 unchanged except for the outcome log(1 + covers_foreign). Prediction: chord repetition −0.04 SD, p < .05, the same sign in both artist halves. Kill: weaker than −0.02.
3. Run it once.

**Check.**
- The rule is committed before the new column is joined to any measure.
- A line in 749.169's hold-out ledger names it.
- The hold-out's counts get the same column, with no test run on them.

### R04-3 The loop-less trial (749.159): keep it a reading until the two-part story is settled
**Status.** A caveat on an open trial. Reading only, no gate.

**Problem.** 749.159's support is cover counts among songs that were already versioned (749.157, 749.158). Tonight, songs that loop more were more often taken up at all (+1.19 points per SD, a kill of the predicted sign, p .018), and mostly by other artists (+1.00, p .044, after seeing results). 749.159's own problem statement already notes that weeks on the chart lean the other way.

So "loop less" may help how many people cover a song once someone does, while lowering the chance that anyone does. Neither result tonight is a finding, but together they are the first sign of a trade-off.

**Evidence.** `run04/experiments/move_extensive/RESULT.md` and `run04/experiments/foreign_versions/RESULT.md`. 749.159's problem statement in `songs/p68/fixlist_v46.md`.

**Fix.** No change to the trial's build. In its verdict, beside "more covers", write that the extensive margin leans the other way and is unsettled. Do not promote the flag to a gate on the strength of cover counts alone until R04-2's reread and a fresh-song test of the two-part story (after R04-1) are in.

**Check.** The trial's report carries the sentence. Its verdict cites R04-2 when that reread exists.

### R04-4 Geometry on the torus of phases and the extensive-margin tests: recorded
**Status.** Record only. Nothing to change in the engine.

**Problem.** The following were proposed in the research as possible readings:
- the P/L/R share and mean step on the Fourier-phase torus
- the thirds axis |a₃|/a₀
- information-rate deviation
- chord surprise as its own claim

None should become an engine reading or gate.

**Evidence.**
- `plr_share`: +0.0065 (SE 0.018), killed.
- `thirds_axis`: +0.006 (SE 0.017), both readings killed.
- `info_rate`: −0.16 points (SE 0.34), killed.
- `move_extensive` H2, chord surprise on "versioned at all": −0.10 (SE 0.41), killed.
- Winding numbers and swept area on the torus are undefined on pop loops: whole-step moves between chords of the same quality are exact half-turns in φ₃ (`run04/brainstorm.md`).

**Fix.** None in the engine. Chord surprise stays a control, not a claim.

**Check.** None needed.

## Carried

- **R03-1, fresh songs by re-matching.** Updated: tonight shows a second route to fresh evidence, the extensive margin. That route needs R04-1 for anything beyond the summary measures. The re-match still needs Discogs-VI `main.zip` (zenodo.org/records/13983028) and the raw Hooktheory file. Open.
- **R03-2, chord surprise beside repetition in 749.159.** Open, and now joined by R04-3.
- **R03-3, chord-map geometry recorded.** Closed: no further action, and R04-4 extends the record.
- **R03-4, a power floor.** Open, and Jason decides. Tonight's powers ran from 0.07 to 0.45. The two torus tests at 0.07 to 0.08 raised every other test's bar from .0167 to .01. The first-principles review suggests a lighter rule: tests under power 0.2 on already-seen songs are reported but not counted.
- **R02-3, the "first performer" flag is 1 for every song.** Open and unchanged (line 26).
- **R02-4, retire J2 to J5.** Unchanged; Jason decides.
- **J6c, the ceiling (MusicLab).** Unchanged; the data is not on hand.
- **749.169, the hold-out ledger.** Not ours to do. Run 04 did not use the hold-out (`run04/experiments/HOLDOUT_LOG.md`).

## Not proposed

- **"Loops get versioned more" as an engine rule:** a kill of the opposite prediction and a lead after seeing results, not a finding.
- **Diatonicity |a₅|/a₀:** withdrawn by its author, and parked for fresh songs.
- **Covers across genres:** still Jason's decision, and it still needs the Discogs releases dump.

## Sources

- Amiot (2013), The Torii of Phases, MCM 2013, LNCS 7937. https://arxiv.org/abs/1208.4774
- Araz, Serra & Bogdanov (2024), Discogs-VI, ISMIR 2024. https://arxiv.org/abs/2410.17400
- Run 04 on judging-research: commits 00ab557 (predictions), 5c8be4b (five results) and 4410a0e (the sixth prediction).
- On main: `songs/p68/fixlist_v46.md`; `lib/luthier/REVIEW_stage30.md`; `studies/judging_checks/within_artist/RESULT.md`; `studies/judging_data/README.md`; `studies/covers/study_covers_discogs.py`; `studies/judging_checks/within_artist/cliques_versions.py`.
- Data: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
