# realness_covers: are songs that sit furthest from the engine taken up more? (run 13; counted, K = 4, α .0125)

**Measure (frozen).** REAL = the gap_engine discriminator's log-odds that a clip is a real song, CROSS-FITTED by artist half: the model that scores a song of half h is trained on engine sections and the real clips of half 1−h only (same recipe as gap_engine: L2 logistic, C = 1, z-scored features, median fill, equal class weights). Song value = mean over its 4/4 clips. No outcome enters training.

**Songs.** Run 04's within-artist Hooktheory rows with a 4/4 clip (about 8,678; seen songs: outcome joined to chord measures in runs 04-06, melody measures in runs 11-12; REAL is new to them).

**Outcome and model.** y_foreign (run 04's rule, `C5.load_outcomes`), OLS of z(y) on z(REAL) with artist fixed effects, run 04's controls and ln_notes (run 11 cache), CR1 SEs by artist; halves by md5(artist) mod 2; conditional logit for the sign.

**Prediction.** +0.02 SD per SD: within an artist, the song that looks least like an engine build is taken up a little more.

**Rules.** Pass: p < .0125, β > 0, both halves > 0, conditional logit > 0. Killed: +0.02 outside β ± 1.96 SE. Else unsettled. Power before the join: SE ≈ 0.011·√(9,588/N) from run 11's realised SEs on these rows (R12-4); at N = 8,678, SE ≈ 0.0116, power ≈ 0.22 at α .0125.
