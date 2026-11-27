# late_window08: does the ii-V share predict artists who took a song up AFTER its charts were written? AFTER SEEING RESULTS

Run 09, 27 November 2026, written by the orchestrator after every frozen test of this pass had been run and after the first-principles review (`run09/first_principles.md`, section 6) named the way through: use time. **Labelled after seeing results, and on SEEN songs: a lead, never a finding, never in K.** The pass's K stays 1.

## Why
The obstacle: an iReal Pro chart is written by players of a tune as it is played now, so a much-recorded standard's chart can carry the ii-V moves its performers added (the arrow runs from covers to chart). Covers recorded AFTER the charts were collected cannot have shaped them. ChoCo v1.0.0 was assembled in 2022 and published in 2023 (Zenodo 7706751); its iReal Pro forum charts were collected before that. Discogs-VI 20240701 holds releases up to mid-2024.

## Songs
Run 08's songs with IIV, DRES and the five iiv_singletons columns, exactly the rows of `iiv_dres08` (`harness09.dres_rows()`, 8,565 songs; their total cover counts were opened in run 08, so these songs are SEEN; the split of their artist sets by year has not been looked at by this research).

## Outcome (read only after this file and test.py are committed and pushed; `common09.guard`)
From `/home/claude/shape/discogs_versions.jsonl` (the maintainer's `cliques_versions.py` reduction of Discogs-VI 20240701): for each song's clique, each artist set's earliest dated year.
- **n_new** = artist sets whose earliest year is **2023 or 2024** (after the charts were collected).
- **n_prior** = artist sets whose earliest year is **2022 or earlier**. Sets with no year are left out of both.
- **y_new** = log(1 + n_new), standardised over the analysed songs.

## Model
Plain OLS with HC1 SEs (posthoc08.ols_hc1) of y_new on z(IIV), z(log(1 + n_prior)), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), the run 08 genre dummies and first-year decade dummies (harness09.Xmat). Holding prior artist sets is the point: the question is whether, among songs equally taken up before the charts, those with more ii-Vs gained more new artists after. Halves: `common09.halves(composer)` with run 08's composer key. Second model: Poisson pseudo-likelihood on n_new (posthoc08.poisson_plain), same columns.
Readings (decide nothing): (a) without log(1 + n_prior); (b) within composer (run 08's model, composer fixed effects, songs whose composer has two or more); (c) non-jazz genres only (run 08 genre not in swing, ballad, latin, blues, waltz); (d) the share of songs with n_new > 0 is printed.

## Prediction
**+0.03 SD of y_new per SD of IIV** (first principles, section 5), positive in both halves and in the Poisson model.

## Rules (a lead; seen songs; after seeing results)
- **Lead supported:** p < .05, β > 0, both halves > 0, Poisson > 0.
- **Lead not supported:** +0.03 lies outside β ± 1.96 SE.
- Otherwise **unsettled**.
A supported lead would say: the ii-V share predicts takers-up the charts could not have copied, which points away from chart-writer leakage. It would still be seen songs, mostly jazz, and would need a newer Discogs dump (artists after July 2024) on songs not yet used to become a finding.

## Power (printed by test.py before the outcome is read)
Fake outcomes on the real rows with the columns available before the outcome (the n_prior column cannot be built before the outcome, so power is computed without it): `harness09.fake_power`, β = +0.03, α = .05, 300 draws. A floor-of-zero outcome (most songs will gain no new artist in eighteen months) carries less information than this simulation assumes, so the true power is lower than printed.

## What it cannot say
Momentum: a song being recorded more lately will be both charted with care and recorded again; holding n_prior absorbs only part of that. Eighteen months of Discogs data is thin and Discogs lags new releases. Seen songs.
