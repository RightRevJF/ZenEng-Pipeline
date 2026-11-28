# Proposed list from the judging research, run 12 (for the maintainer)

28 November 2026, the 10:17 ET pass. Proposed by Jason Bryant from the judging research. The source is studies/judging_research/run12 on the judging-research branch: report.md, card_1.md, card_2.md, brainstorm.md, chair.md, first_principles.md, DATA.md, searches.md, and the folders under experiments/.

Published as the Doc "Proposed fix list: judging research, run 12" (link in report.md); the pass's report is the Doc "Judging research, run 12" (https://claude.ai/artifact/WwVjsqH8kJwerpNTJD4Eou).

Nothing here is in the engine. Labels R12-1 to R12-5 are proposal labels; the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

**Checked on origin/main (4bc2514), the maintainer's branch (6b04d4f) and the thread before proposing, read only.**
- `songs/p68/fixlist_v54.md` is still the latest list on main; `lib/luthier/REVIEW_stage35.md` the latest review. Nothing there proposes cover-timing fitness, predictive information, roughness or arrangement invariants, so nothing below repeats a closed item.
- **The maintainer's run 11 check (its post at line 2093):** asked for one line on whether pitch-class entropy and the commonest-pitch share disagree on these tunes. **Answered (R12-1).**
- **The songwriting session's answer to R11-3:** its machine cannot reach the Lakh files (403). **Noted:** this machine can (LPD-5 from Zenodo), but every within-artist Lakh song is now seen (R12-5), so R11-3 still asks for new named melodies (carried, updated).
- The maintainer's 10:58 ET post (beat strength in threes from entrainment) advises against a separate physics branch because the five vectors sit here. Agreed; nothing asked of the research.

## At a glance

| Item | What | Kind | Engine touched? |
|---|---|---|---|
| R12-1 | Pitch-class entropy and the commonest-pitch share mostly agree (Spearman −0.83 over 16,563 clips) | Answer (a count) | No |
| R12-2 | Covers show no rich-get-richer: an age-adjusted cover rate is the honest outcome | Data-pack note | No |
| R12-3 | Recordings aligned to notes, for the performer's field (physics vector 3) | Data request | No |
| R12-4 | Power came out optimistic this pass; two counting rules unwritten | Method | No |
| R12-5 | Seen-ledger lines for this pass | Data-pack note | No |
| Carried | R11-2, R11-3 (updated), R10-5 (pop), R10-6 (1, 2), R09-3, R09-4, R09-5 (2), R08-3, R08-4, R05-5, R03-2, R02-4, J6c | | |

## In short

Physics vector 1 (fitness, not luck): a song's fitness was estimated from the years of its covers alone (a Bianconi-Barabási growth model with aging, frozen at b0c7824 before any notes were joined). The cover record chose no rich-get-richer at all, so fitness is an age-adjusted, shrunk cover rate (0.985 with log covers, year held). Ten tests, rules first (ac5cb9b; the after-seeing rule 2d64143), K = 4, α .0125. Nothing passed. Killed: predictive information on whole Lakh songs (−0.011 against +0.03). Unsettled: pitch-class entropy against fitness rather than counts (−0.012, p .11) and a corpus-trained context gain on clips (+0.015, p .23). The rest were estimates; Hooktheory's hint that chord repetition's link sits in late covers (Δ −0.24) was not reproduced on Lakh (+0.006, SE 0.097).

For the engine: nothing new. R11-2's reading stands; this pass's Lakh estimate leans its way (−0.022, SE 0.021).

## Items

### R12-1 Pitch-class entropy and the commonest-pitch share: mostly the same reading
**Status.** Answer to the maintainer's run 11 note. A count, notes only.

**Problem.** R11-2 (simpler pitch spread) and K5 (one pitch not sung too often) are different measures and could pull apart.

**Evidence.** On the 16,563 Hooktheory clips of the 9,588 within-artist songs (clips of 12 notes or more; duration-weighted pitch classes): Spearman between pitch-class entropy and the commonest pitch class's share −0.83 (Pearson −0.85). In 14.5% of clips the two ranks differ by more than a quarter of the range. The commonest pitch class is the tonic in 34% of clips. Computed this pass with `run11/experiments/common11.py` (`melody`), no outcome read.

**Fix.** None. Before any K5 form is built from the lift, read K5 and entropy side by side on the kept songs; where they disagree (about one clip in seven), say which the form follows.

**Check.** The two percentiles printed together for the kept songs.

### R12-2 Covers show no rich-get-richer
**Status.** Data-pack note. New.

**Problem.** Raw cover counts mix a song's appeal with its age and era. The physics question was whether they also carry a rich-get-richer feedback (covers breeding covers). They do not.

**Evidence.** `run12/experiments/fitness/fit.json`: on 2,627 matched groups, the likelihood rises steadily as the attachment constant A grows (profile 36,193 at A = 0.3 to 32,965 at A = 100; free A about 2×10⁶); fitness varies widely between songs (gamma shape 0.66). After seeing results, a refit with one age bin per year (`fitness_finebins_after`) gave the same answer (profile 35,942 at A = 0.3 to 32,869 at A = 100). FIT, the posterior mean of log fitness, correlates 0.985 with log(1 + covers) once first year is held.

**Fix.** If wanted, offer covers per year of opportunity (FIT, from frozen `fitness.py`) beside raw counts in the data pack, so any later test can use an age-adjusted outcome without its own year controls. The per-song table (`/home/claude/dl/run12/fitness.json`, about 0.4 MB, derived from Discogs-VI, CC BY-SA 4.0) can be committed under `studies/judging_research/data/` on request.

**Check.** The table's sha256 (68d2688a…3d6a) and the fit's parameters printed beside it.

### R12-3 Data request: recordings aligned to notes
**Status.** Data request. New (physics vector 3, the performer's field).

**Problem.** The performer's field needs a performer's timing and pitch deviations against the written notes, for songs that are covered. Nothing on this machine has that.

**Evidence.** `run12/DATA.md`. This machine reaches zenodo.org, raw.githubusercontent.com and huggingface.co API pages only.

**Fix.** If your machine reaches one: a set of pop or folk performances with note-level alignment to a score or MIDI, with titles and artists (so covers can be joined), and a licence that allows processing by a language model. Name the file and its licence; the research freezes its rule before any outcome. A classical-piano set with aligned performances (for example the ASAP collection on GitHub) would only pilot the measure; it has no covers outcome.

**Check.** The licence read and quoted before any download.

### R12-4 Power was optimistic this pass; two counting rules are unwritten
**Status.** Method. The sessions settle; Jason may overrule.

**Problem.** Run 11 found fake outcomes made SEs too large. This pass added the artist share (R11-4), and the real SEs came out larger than the fakes: v1_rep 0.0073 against 0.0055, PI3c 0.021 against 0.017, windows about three times. Stated powers were optimistic. Also: an after-seeing test joined K this pass, and the chair counted a test its author had withdrawn (on a power figure known to be wrong). Neither is a written rule.

**Evidence.** `run12/experiments/*/power.json` against `result.json`; `run12/first_principles.md`, section 2.

**Fix.** (1) From run 13, scale each fake SE by the ratio of real to fake SE seen in the last pass for the same data set and model, and print both. (2) Write the rule: an after-seeing test is counted in the pass's K (lowering α for all), and passes only as a lead. (3) Write the rule: a test withdrawn by its author is counted only if the chair names a measure-side error in the withdrawal before any outcome.

**Check.** Recorded in run 13's chair.md before any power is computed.

### R12-5 Seen-ledger lines
**Status.** Data-pack note.

**Fix.** If wanted, in the pack's seen ledger:
- the 1,853 within-artist Hooktheory songs with a Discogs group, joined to FIT and to early and late cover windows with pitch-class entropy and chord repetition (rules ac5cb9b, results 2d64143);
- the 9,588 within-artist Hooktheory songs joined to PIC, the corpus-trained context gain (same commits);
- run 07's within-artist Lakh songs joined to four melody measures read from the MIDI skyline (pitch-class entropy, predictive information, fifths energy, roughness) (same commits), and 1,926 of them to cover timing with chord repetition (rule 2d64143, code fix 3f22888, result 2ea76c8).

**Check.** The ledger lines name the commits.

## Carried

- **R11-2, pitch-class entropy on pop melodies: a reading.** Stands. This pass on Lakh melodies: −0.022 (SE 0.021), the same sign, an estimate. Still no gate until it passes on melodies never joined to an outcome.
- **R11-3, unseen melodies with titles and artists.** Updated: this machine reaches LPD-5, but every within-artist Lakh song is now seen (R12-5). The request stands for new named melodies by artists with two or more songs (about 11,000 for an even chance at −0.02).
- **R11-4, fake outcomes with an artist share.** Done in run 12; superseded by R12-4.
- **R11-5, seen-ledger lines.** Carried into R12-5 (still open).
- **R10-5 (pop), R10-6 (1, 2), R09-3, R09-4, R09-5 (2), R08-4, R05-5, R03-2, R02-4, J6c.** Open, unchanged.
- **R08-3, chord repetition: no covers lean either way.** In force.
- **R09-3, hold prior artist sets in late-cover readings.** Open; it bears on the windows test, which did not hold them.

## Not proposed

- **Predictive information (PI3c) as a reading:** killed (−0.011 against +0.03).
- **Roughness from overtones:** an estimate on the wrong side; mostly register.
- **Fifths energy:** stopped at its overlap gate (ρ −0.71 with pitch-class entropy).
- **Fitness against counts as a separate outcome for the engine:** with no rich-get-richer they cannot differ (R12-2).
- **Jason's S = 1 + g/π:** retired by Jason, 28 November 2026.

## Sources

- Freeman, N. and Jordan, J., Extensive condensation in a model of preferential attachment with fitness, arXiv 1812.06946. https://arxiv.org/abs/1812.06946
- Gaeta, R., Garetto, M., Ruffo, G. and Flammini, A., Reconciling the quality vs popularity dichotomy in online cultural markets, ACM TOIS (2022), arXiv 2204.13536. https://arxiv.org/abs/2204.13536
- Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Lakh MIDI (Raffel 2016) / LPD (Dong et al. 2018), CC BY 4.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
- Run 12 on judging-research: b0c7824 (fitness frozen), ac5cb9b (predictions), 2d64143 (results; the after-seeing rule), 3f22888 (code fix), 2ea76c8 (after-seeing result).
- On main: `songs/p68/fixlist_v54.md`; `lib/luthier/REVIEW_stage35.md`; `coord/songwriting.md`; `coord/maintainer.md` on luthier-v8-stage1 (run 11 check; 10:58 ET post).
