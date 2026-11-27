# gap_writer08: the ii-V read by another chart writer, and the iReal gap (R09-L1's lead). SEEN SONGS: A LEAD, NOT IN K

Run 09, 27 November 2026. Frozen by the chair before this file's outcome fields are read. **Status: LEAD ON SEEN SONGS.** These are
run 08 songs whose outcomes were opened in run 08, and the idea was written after run 08's ii-V results, so under the maintainer's
correction it is never in K. It passes nothing and kills nothing; it says which story the next unseen batch should test.

## Songs (notes-side match; `measures09.py`, section SEEN08)
Run 08's 8,640 songs (from `data/choco_songs_discogs_run08.json`, fields `clique` and `charts` only, read before the guard). A run 09
real-book or BiaB internet-corpus chart (≥ 8 chords, not in the run 09 design) is an UPSTREAM chart of a run 08 song when its raw
title (brackets removed, cut at " - ") has at least two words and the union of its `common.variants()` hits the title variants of the
charts of exactly one run 08 song (2,940 charts matched; 2,802 no match, 163 not unique, 1,060 one-word titles, 810 already in the run
09 design). **Songs: the 1,181 run 08 songs with at least one measured iReal Pro chart and at least one measured upstream chart.**

## Measures
- IIV as run 08 (`measures.listener_measures`).
- **IIV_up** = mean IIV over the song's upstream charts (real-book and BiaB pooled); **IIV_ireal** = mean over its iReal Pro charts
  (ireal-forum, ireal-playlists); **GAP = IIV_ireal − IIV_up**. ln_n_ireal = log(number of its measured iReal charts), a notes-side
  stand-in for how much the tune is played (not an outcome).
- Controls: w_chr, ch_rep, V, ln_chg, ln_bars from the upstream charts AND the same five from the iReal charts (ten columns).

## Outcome and model
After `common09.guard(this folder)`: n_artist_sets, first_year and the composer key are read from the run 08 data file. y_cov =
log(1 + n_artist_sets) standardised over these songs. Plain OLS HC1 on z(IIV_up), z(GAP), the ten controls, z(ln_n_ireal), genre
dummies (run 08's genre rule, recomputed from the charts: `common.genre_of`, most common) and first-year decade dummies. Halves:
`common09.halves(run 08 composer key)`. Second model: `posthoc08.poisson_plain` (on each reported coefficient in turn).

## Predictions (the Listener's, frozen)
- **Song story** (the song carries its ii-Vs whoever writes the chart): **b_up = +0.045** (+0.07 × writer agreement 0.64), **b_gap ≈ 0**.
- **Writer story** (iReal writers add the ii-Vs that players play): **b_up ≤ +0.01** and **b_gap ≥ +0.03**.
- Frozen labels: the song story is excluded if +0.045 lies outside b_up's 95% range; the writer story is excluded if b_up's lower
  bound is above +0.01 or b_gap's upper bound is below +0.03. The result reads "song story", "writer story", "neither excluded" or
  "both excluded".

## Power at .05 (printed before the outcome; informational, a lead has no floor)
b_up at +0.045: 0.207 (N 1,181, fake SE 0.041). b_gap at +0.03: 0.117 (fake SE 0.036). Neither story is likely to be excluded.

## Readings (deciding nothing)
1. Without ln_n_ireal (the Listener: chart count may lie on the path from covers to chart).
2. IIV_up alone with the upstream controls.
3. IIV_ireal alone with the iReal controls, same songs (the comparison: does the iReal reading predict more than the upstream one?).

## What it cannot say
"Upstream" means outside iReal, not before covering: the Real Book was compiled from canonical recordings and BiaB files are
user-made. Title-only matching can attach a chart of another song with the same title. Seen songs: a pattern here is a lead.
