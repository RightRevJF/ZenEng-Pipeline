# Proposed list from the judging research, run 02 (for the maintainer)

22 November 2026. Proposed by Jason Bryant from the judging research (studies/judging_research/run02 on the judging-research branch: report.md, card_1.md to card_4.md, debate.md, chair.md, first_principles.md). Nothing here is in the engine. Labels R02-1 to R02-4 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide. Carried items from week 01 (J1 to J6) are updated below.

Checked on origin/main (d2d740a) before proposing, read only: `lib/luthier/chord_writer.py` still reads `loops` and `distinct_bars` only in its held-out test (lines 219 and 225), with no rule on within-section chord repetition, so J1 is not in the engine; `songs/p68/fixlist_v45.md` (latest list; next finding 749.153) and `lib/luthier/REVIEW_stage29.md` (latest review) have no item on covers or chord repetition, and nothing from week 01's list has been taken up or closed; `studies/covers/study_covers_discogs.py`, `discogs_cliques.py` and `covers_study_report.md`; `studies/shape/same_artist/PREDICTION.md` and `studies/shape/chords/PREDICTION.md`.

## In short

The one note finding that holds (chords that move within a section get more covers, J1) has only ever been tested across different artists, so the performer's fame, voice, era and genre travel with the harmony. Run 02's first-principles review names that as the main obstacle. R02-1 is the test that settles it: compare each artist's songs only with the same artist's other songs. Until it runs, J1's change to the structure draw should wait; its reading can go ahead. R02-2 and R02-3 are housekeeping in `studies/covers` that the test needs: keep the per-version Discogs data when it is fetched again, and fix a control that is set to 1 for every song. R02-4 retires four of week 01's proposals (J2 to J5) that failed or were never tested.

This run's papers add two cautions. Covers pile onto famous performers and mostly stay inside a genre (Ortega 2021), so a raw cover count partly measures fame. And even where only musicians choose (Irish tunebooks), melody explains about 3 points of the differences against 16 for the prestige of recordings (McBride & Leroi 2026), so any note effect will be small.

## Items

### R02-1 The mirror of a cover: chord repetition within each artist's own songs
**Status.** Lead. Never run. Needs Jason's go-ahead and data fetched again.
**Problem.** J1 proposes weighting the structure draw (800) toward kept sections that loop less. Both results behind it compare different artists' songs. The repo's same-artist study (`studies/shape/same_artist`, 19 November) held the artist fixed but tested 21 other tune and chord measures against G; within-section chord repetition and covers alone were not among them. So no note finding that holds has been tested with the performer held still. If the effect belongs to performers, eras or genres rather than to the notes, J1 would move the engine toward a habit of certain artists, not toward what gets covered.
**Evidence.** `studies/covers/covers_study_report.md`: chord repetition within a section against covers −0.124 (p .003, 780 songs, SHS100K) and −0.071 (p < .001, 2,360 songs, Discogs-VI), standard errors clustered by artist but no artist fixed effect. `studies/shape/RESULT.md`: the artist accounts for about 0.14 of the differences in covers among kept hits, so most of the variation lies between songs of the same artist and a within-artist test has room to work. First-principles review, run 02, sections 5 and 6.
**Fix.** Before any change to the structure draw: on the 2,360 Discogs-VI songs, artists with two or more songs, regress log(1 + covers) on within-section chord repetition with a fixed effect for each artist, plus first year and log views. Artists split in two by a hash of the name. Compute power first and print it. Prediction, written now: −0.04 or stronger, pooled p < .05, same sign in both halves. Weaker than −0.02 (under 30% of the between-artist −0.071): the finding belongs to performers, eras or genres, and J1's draw change is withdrawn. In between: unsettled, report and wait for the fresh McGill leg (J6b). Report covers in the first five years and after year ten as well, deciding nothing on the contrast.
**Check.** The between-artist model reproduces −0.071 on the same rows before the fixed effect is added. The prediction file is committed before the outcome is joined. Song 59 is not read.

### R02-2 Keep each version's year, artists and release id when Discogs-VI is fetched again
**Status.** Housekeeping; checked by reading the committed script.
**Problem.** `studies/covers/discogs_cliques.py` reads each version's title, artists, release date, release id and writers, then keeps only the count of distinct performing artists and the earliest year. So neither covers by period (J6a) nor covers across genres (run 02's second idea) can be computed from what is committed, and the Discogs-VI download is no longer on disk.
**Evidence.** First-principles review, run 02, the one check: no committed file under `studies/covers` reads genre or style; release ids are read and discarded. The Discogs data dump is CC0 and carries genres and styles by release id.
**Fix.** When Discogs-VI is fetched again, write a small derived table for the matched songs only: per song, each version's year, performing artists and release id. Commit that table (not the download). Join genres and styles from the Discogs dump by release id in a separate step.
**Check.** From the new table, the per-song cover counts and first years reproduce `covers_discogs_results.json` (2,360 songs, chord repetition −0.071) exactly. The table holds no audio, notes or `.pkl` files.

### R02-3 The "first performer" flag in the Discogs-VI study is 1 for every song
**Status.** Fault in a study script; checked by reading it.
**Problem.** `study_covers_discogs.py` sets `original=1.0` for every row (line 26), so `--originals` (line 31) filters nothing. A Discogs-VI run "on originals" would be the full run again, and a model that holds "first performer or not" on Discogs-VI holds a constant. The run 02 chair's model listed it as a control.
**Evidence.** The script on main, lines 26 and 31. The report's originals replication (705 songs, −0.126) is on SHS100K, where the flag is computed, so no published figure is wrong; the risk is to the next study.
**Fix.** Either compute the flag (the Hooktheory artist is among the artists of the earliest-dated version in the group) or remove it and say in the report that the originals check exists for SHS100K only.
**Check.** The script prints how many songs are originals; if computed, the originals run differs in n from the full run.

### R02-4 Retire J2 to J5 from the proposed list
**Status.** Recommended by run 02's first-principles review. Jason decides.
**Problem.** Four of week 01's proposals ask for new readings of Luthier's builds on measures that have failed or were never tested. Each adds work for the maintainer and another chance of a lucky pass.
**Evidence.**
- J2 (plain chords, varied path): its base term was chord surprise −0.030, p .06 on Discogs-VI; the interaction was never tested.
- J3 (earn the surprise): the Cheung-style term failed on Discogs-VI (+0.009, p .54) after passing on SHS100K.
- J4 (reach the surprise smoothly): untested anywhere; it was a debate proposal.
- J5 (short, early, stepwise hook): rests on folk memory (faithful copying), not on musicians choosing songs, and five shape runs on about 3,100 songs found nothing in the tune. Run 02's card 2 (simpler Irish tunes spread a little better among players) does not change this: melody adds about 3 points beyond prestige, with no harmony measured and no replication.
**Fix.** Drop J2 to J5 from the proposed list. No engine change follows, since none was taken up.
**Check.** None needed.

## Carried

- **J1 Chords that move within a section.** Updated: replicated across artists only (above). The rule-first reading (within-section repetition of chosen builds, songs 52 to 58 and 60, against the kept distribution) can go ahead now. The weighting of the structure draw (800) waits for R02-1.
- **J2 to J5.** Retired in R02-4.
- **J6a Early covers.** Updated: folded into R02-1's report of covers by period. Run 02's chair proposed early covers with the original performer's fame and chart run held; the first-principles review warns that the first covers of a hit are often quick budget cover albums, the most fame-driven covers of all, and that chart weeks and peak are partly caused by the notes, so they belong in a sensitivity check, not the main model. Both early and late covers are reported, and nothing is decided on their contrast.
- **J6b Fresh songs.** Kept as the fresh leg after R02-1, on McGill Billboard (`studies/harmony/billboard_sections.json`, 739 songs) joined to Discogs-VI, dropping songs already in the 2,360. Power about 20 to 35%, so a null settles nothing.
- **J6c The ceiling (MusicLab).** Unchanged; no paper this run bears on it.

## Not proposed

- **The spectral gap of the chord map** (run 02's third idea: how quickly a walk on a song's chord-to-chord map forgets where it started). It passed a check that it is not chord repetition renamed (on 721 McGill songs, rank correlation −0.26 with repetition, near zero with chord count and section count), but its stability within a song is untested and it has met no outcome. Parked in the research, no reading proposed.
- **Melodic pitch-class entropy and card 2's other tune measures.** A sixth try at the tune; not proposed.
- **Covers across genres** as part of the yardstick. It changes the yardstick, which is Jason's decision, and needs R02-2 first.
- **Love against chart exposure** (card 3). A long chart run is partly caused by love, so the test cannot separate wear-out from being loved.

## Sources

1. Ortega, J. L. (2021). Cover versions as an impact indicator in popular music: a quantitative network analysis. PLoS ONE 16(4), e0250212. https://doi.org/10.1371/journal.pone.0250212
2. McBride, J. M., & Leroi, A. M. (2026). Population ecology of tunes. arXiv:2609.09501. https://arxiv.org/abs/2609.09501
3. Madison, G., & Schiölde, G. (2017). Repeated listening increases the liking for music regardless of its complexity. Frontiers in Neuroscience 11, 147. https://doi.org/10.3389/fnins.2017.00147
4. Di Marco, N., Loru, E., Galeazzi, A., Cinelli, M., & Quattrociocchi, W. (2026). Decoding the evolution of melodic and harmonic structure of Western music through the lens of network science. Scientific Reports 16, 11121. https://doi.org/10.1038/s41598-026-42872-7
5. The repo's covers study: studies/covers/covers_study_report.md and study_covers_discogs.py (main).
6. The repo's same-artist study: studies/shape/same_artist/PREDICTION.md and studies/shape/RESULT.md (main).
7. Week 01's proposed list: studies/judging_research/week01/proposed_fixlist.md (judging-research branch).
8. The run's report: studies/judging_research/run02/report.md; Doc "Judging research, run 02": https://claude.ai/artifact/GfyEnWfC6eiyGHe6gFsGng

Published as the Doc "Proposed fix list: judging research, run 02": https://claude.ai/artifact/VR74RsLgCXDEzjPTZ13gDi
