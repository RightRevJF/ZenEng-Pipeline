# iiv_source: is the ii-V share the song's, or the chart writer's? AFTER SEEING RESULTS. Frozen before this reading is run

Run 08, 27 November 2026, written by the orchestrator after `iiv_chunk` passed. **After seeing results, on SEEN songs** (they are in the `iiv_chunk` design): it re-spends their outcome. Status: **ESTIMATE** (power 0.05, under the 0.2 floor): it passes nothing and kills nothing; it is reported.

## Why
A rival story for `iiv_chunk`: iReal Pro forum charts are written by jazz players, who add ii-V approaches to tunes they play; tunes jazz players play are recorded by many artists. Then IIV would read "already in the jazz repertoire" (the outcome leaking into the chart), not the song. Wikifonia lead sheets were mostly entered from published sheet music. If IIV read from Wikifonia charts alone carries the same sign and size, the chart-writer story is weaker.

## Measure, songs, model
IIV and the controls (w_chr, ch_rep, V, ln_chg, ln_bars) are read from the song's Wikifonia charts only (`posthoc08.source_rows()`), on the 1,128 design songs that have both a Wikifonia and an iReal chart (466 composers). Same model as `iiv_chunk` (composer FE, decade dummies; genre is one bin here). Also reported: the same with IIV read from the same songs' iReal charts only, and the correlation of the two IIV readings.

## Prediction
β = +0.07 SD per SD for the Wikifonia reading (the `iiv_chunk` size). Power at α = .05/6: **0.05** (`posthoc08.fake_power_ols`, composer share 0.3, SE 0.048): an estimate only.
