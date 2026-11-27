# transport_economy: result (run 08, R08-G1). An ESTIMATE: it passes nothing and kills nothing

## In plain words
The question was whether songs with smoother chord changes get recorded by more artists. Smoother here means each chord moves to the next by smaller steps than the same chords would if they were shuffled. The comparison is always between songs by the same composer. Before anyone saw the outcome, the Geometer predicted a small positive effect: +0.03 SD more covers for each SD of smoothness. The data point the other way. Smoother songs had slightly fewer covers, both halves of the composers agree, and so does the second model. It was frozen as an estimate (counted set full at K = 5, `../../chair.md`), so it decides nothing.

## Predicted (frozen in PREDICTION.md, commit e624a7e)
β = +0.03 SD of y_cov per SD of econ. The controls were w_chr, ch_rep, V, ln_chg, ln_bars, genre and decade, with composer fixed effects and CR1 errors. The pass-like rule was p < .01, β > 0, both halves > 0 and Poisson > 0. The kill-like rule was +0.03 lying outside β ± 1.96 SE.

## Power (printed before the outcome was joined)
Power was 0.223 at an assumed composer share of 0.3 (SE 0.0170), matching the frozen 0.223. At a share of 0.5 it was 0.323 (SE 0.0144). If the prediction were true, the kill-like rule would fire wrongly 4.3% of the time. At the final K = 6 (α = .05/6), power would drop to about 0.19, below the floor.

## What came out (5,858 songs, 1,199 composers)
- **β = −0.0353, SE 0.0155, p = 0.023**. The 95% range is −0.066 to −0.005.
- Halves: −0.0351 (SE 0.0233, p 0.13; 2,973 songs, 644 composers) and −0.0441 (SE 0.0207, p 0.034; 2,885 songs, 555 composers).
- Second model (Poisson on n_sets, median 14): −0.0831 (SE 0.0294, p 0.0047).

## Verdict by the frozen rule
The pass-like rule fails on every sign. The kill-like rule is met: +0.03 lies 4.2 SE above β and outside the range. But the test is an estimate, so **it passes nothing and kills nothing**. As a reading, the result is firm in direction: all four figures are negative. The main p (.023) does not clear .01.

## Renaming check (`../measure_gates.json`)
- Two-chart stability is 0.624 (0.622 after removing size). iReal against Wikifonia is 0.406.
- Within composer, ρ is −0.062 with ch_rep and +0.122 with V, so the gate **passes** and econ is not ch_rep or V under a new name.
- ρ with w_chr is −0.619, and w_chr sits in the model. 71% of econ's variance lies within composer.

## Reported, deciding nothing
Without w_chr (the Geometer's own second model), β = −0.0137 (SE 0.0128, p 0.28). Most of the negative estimate appears only once mean step size is held fixed. With econ and w_chr correlated at −0.62, that partial effect is harder to read.

## What it cannot say
- **Genre within composer:** the genre labels are coarse and come from iReal.
- **Chart writers:** the chords are user transcriptions, and two sources agree only moderately (0.41).
- **Jazz idiom:** iReal is mostly jazz, where smooth ii–V voice-leading is the house style.
- **Name matching:** composers come from matched name tokens, and some are performer matches.
- **Selection:** only tunes someone charted are in the sample, and these are already well-covered songs.

It is an association between songs by the same composer, not a cause.
