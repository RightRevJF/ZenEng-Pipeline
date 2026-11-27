# iiv_confirm09: run 08's frozen confirmation of the ii-V share, on songs never joined to an outcome. COUNTED

Run 09, 27 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. The test itself was written in
run 08 (`run08/first_principles.md` section 5); this file applies it to the run 09 design without changing its measure, model,
prediction or kill. **Status: COUNTED. K = 1, α = .05 (two-sided).**

## Measure
`IIV` = run 08 `measures.listener_measures()["IIV"]`, unchanged: on the change tokens ((root, 12-bit bitmap) with consecutive
repeats merged), the share of changes that go from a minor seventh (bits 3 and 10, not 4) to a dominant seventh (bits 4 and 10, not 3)
whose root is a fourth up ((r2 − r1) mod 12 = 5). Chart filter as run 08 (≥ 8 events, ≥ 6 change tokens). Song value = the
unweighted mean over the song's measured charts (`measures09.py`, stored in `$DL/choco/measures_run09.json`).

## Songs
The run 09 design (`common09.load_design()`): 1,283 Discogs-VI cliques never joined to an outcome, matched to ChoCo charts by title
plus name (298) or by a unique title of two or more words (985). 1,271 have IIV and every column (the other 12 have no chart passing
the filter). Genre (partition-based, design songs): jazz 443, biab 422, pop 271, wikifonia 96, other 51. Charts: Real Book and BiaB internet corpus
(Band-in-a-Box files), iReal Pro and Wikifonia charts that matched nothing in run 08, and transcriptions of one recording (Isophonics,
uspop2002, rock corpus, Robbie Williams, JAAH, Weimar).

## Outcome
y_cov = log(1 + number of distinct artist sets) standardised over the analysed songs (`common09.load_outcomes`, after the guard);
covers = n_artist_sets − 1 (reported).

## Model (the iiv_singletons model, `harness09.run_unseen`)
Plain OLS with intercept, HC1 robust SEs (`posthoc08.ols_hc1`), across composers, of y_cov on z(IIV), z(w_chr), z(ch_rep), z(V),
z(ln_chg), z(ln_bars), z(no_bars), genre dummies and first-year decade dummies.
- **The one change to run 08's model (the chair's timebase rule, stated plainly):** ln_bars has no meaning on charts timed in seconds.
  It is set to missing on them; the song value is the mean over its bar-timed charts; a song with none (recordings only) gets the mean
  ln_bars of the analysed songs that have one, and the indicator column no_bars = 1 (0 otherwise). Nothing else changes.
- Halves: `common09.halves(composer key)` (md5 of the design's composer key: the name-matched person key, else the clique's first
  Discogs-VI writer, else 'solo:<clique>'), y re-standardised within each half, same columns.
- Second model: `posthoc08.poisson_plain` on n_sets with the same columns.
- Reported, deciding nothing: CR1 SEs clustered by composer key (some keys hold many songs: 'traditional' 89, 'thebeatles' 34).

## Prediction
**β = +0.05 SD of y_cov per SD of IIV** (run 08's +0.057 on unseen singletons, shrunk for the winner's curse; frozen in run 08).

## Rules (K = 1, α = .05, two-sided)
- **Pass:** p < .05, β > 0, β > 0 in both halves, Poisson coefficient > 0.
- **Kill (range kill):** +0.05 lies outside β ± 1.96 SE.
- **Unsettled:** anything else.

## Power (printed again by test.py before the outcome is joined)
Fake outcomes on the real rows and frozen columns (`harness09.fake_power`: y = 0.05 z + noise, OLS HC1, no decade dummies, 300 draws,
seed 11): **power 0.367 at α .05** (0.277 at .025), N 1,271, fake SE 0.032. The range kill fires in 4% of draws when +0.05 is true
and in 35% when the effect is zero. Monte Carlo error on the power about ±0.028.

**Run 08's own condition relaxed, stated plainly:** run 08 wrote "run it only at fake-outcome power 0.5 or more". Its power here is
0.367. The chair counts it under the brief's ruling (R06-5: the power floor is 0.2); 0.5 was run 08's recommendation, not a ruling.
A non-pass at this power is weak evidence; only a range kill or a pass says much.

## Frozen readings (estimates: each passes nothing and kills nothing; power printed before the outcome)
1. **Non-jazz genres** (genre ≠ jazz: biab, pop, wikifonia, other; N 831), run 08's frozen interpretive reading, predicted **+0.04**;
   power 0.19 at .05, under the floor, so an estimate. If +0.04 lies outside its 95% range, the finding is labelled "jazz repertoire".
   Caution: the BiaB internet corpus mixes jazz with pop, folk and country, and its genre is the partition.
2. **Real Book and BiaB charts only** (R09-L1's counted form, merged here at the Skeptic's ruling; every column read from those charts
   only; N 553), predicted **+0.035** (+0.07 × writer agreement 0.64, shrunk for title-only matches); power 0.113. This reads harmony
   written outside the iReal community, which is not the same as before covering (the Real Book was taken from canonical recordings).
3. Name-matched songs only (297), chart provenance only (1,075), jazz genre only (440): reported without a prediction.

## What it cannot say
Across composers, so a composer's fame is not held. 985 of the songs are matched by title alone; a wrong match dilutes β toward 0.
"Upstream" charts here are mostly not upstream of covering (see chair.md).
