# tonic_resistance: result (run 08, R03-I2 with written keys). An ESTIMATE: it passes nothing and kills nothing

## In plain words
Picture a song's chords as a network of moves, and ask how easy it is to get to the home chord from everywhere else. H is low when home is central, meaning easy to reach. The idea, carried over from run 03, was that songs with a more central home chord get recorded by more artists. The comparison is always between songs by the same composer. The frozen prediction was a small negative effect: −0.03 SD per SD of H. The data lean the other way. Songs whose home chord was *less* central had slightly more covers, both halves agree in sign, and the second model agrees. It was frozen as an estimate (counted set full at K = 5; retirement recommended by runs 05 to 07), so it decides nothing; retirement stays Jason's call.

## Predicted (frozen in PREDICTION.md, commit e624a7e)
β = −0.03 SD of y_cov per SD of H. The controls were ch_rep, V, ln_chg, ln_bars, H_links, genre and decade, with composer fixed effects and CR1 errors. The pass-like rule was p < .01, β < 0, both halves < 0 and Poisson < 0. The kill-like rule was −0.03 lying outside β ± 1.96 SE.

## Power (printed before the outcome was joined)
Power was 0.277 at an assumed composer share of 0.3 (SE 0.0148), matching the frozen 0.277. At a share of 0.5 it was 0.453 (SE 0.0125). If the prediction were true, the kill-like rule would fire wrongly 2% of the time.

## What came out (5,700 songs with an H, 1,197 composers)
- **β = +0.0207, SE 0.0119, p = 0.082**. The 95% range is −0.003 to +0.044.
- Halves: +0.0343 (SE 0.0175, p 0.050; 2,894 songs, 642 composers) and +0.0086 (SE 0.0163, p 0.60; 2,806 songs, 555 composers).
- Second model (Poisson on n_sets, median 15): +0.0505 (SE 0.0194, p 0.0091).

## Verdict by the frozen rule
The pass-like rule fails: every sign is opposite to the prediction. The kill-like rule is met: −0.03 lies 4.3 SE below β and outside the range. But the test is an estimate, so **it passes nothing and kills nothing**. As a reading, the estimate itself is weak (p .08; the range touches zero), but the predicted −0.03 is far from the data.

## Renaming check (`../measure_gates.json`)
- Two-chart stability is 0.651 (0.646 after removing size). iReal against Wikifonia is 0.376, the weakest of these three measures.
- Within composer, ρ is −0.042 with ch_rep and −0.082 with V, so the gate **passes**.
- The control H_links tracks V at ρ 0.896, but H does not (ρ −0.086 with H_links). 70% of H's variance lies within composer.

## Reported, deciding nothing
Without H_links, β = +0.0209 (SE 0.0119, p 0.080), almost the same as the main estimate.

## What it cannot say
- **Chart writers:** the written key is the chart writer's choice, and modal or modulating tunes get a single tonic.
- **Genre within composer:** the genre labels are coarse.
- **Jazz idiom:** iReal is mostly jazz, where turnarounds shape the network.
- **Name matching:** composers come from matched name tokens.
- **Selection:** only charted tunes are in the sample.
- **New unit:** full charts have more distinct chords (median 12) than the Hooktheory clips the idea was built on (3 to 6), so H measures something different here.

It is an association, not a cause.
