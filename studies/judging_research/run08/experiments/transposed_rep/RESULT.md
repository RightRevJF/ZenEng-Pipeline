# transposed_rep: result (run 08, R08-G2). An ESTIMATE: it passes nothing and kills nothing

## In plain words
T measures how often a song repeats a three-chord pattern at a *different* pitch, beyond exact repeats at the same pitch. Musicians call this a sequence. The Geometer predicted that songs with more sequences get recorded by more artists: +0.05 SD per SD of T, comparing songs by the same composer. The author then withdrew the test from the count in round 3, because T mostly picks up jazz idiom, so it was frozen as an estimate whatever its power. Its power was high (0.79), the highest of any y_cov test that night. The effect came out small and uncertain. It was positive, but smaller than predicted, and one half of the composers shows nothing.

## Predicted (frozen in PREDICTION.md, commit e624a7e)
β = +0.05 SD of y_cov per SD of T. The controls were ch_rep (which equals L, exact repetition), V, ln_chg, ln_bars, genre and decade, with composer fixed effects and CR1 errors. The pass-like rule was p < .01, β > 0, both halves > 0 and Poisson > 0. The kill-like rule was +0.05 lying outside β ± 1.96 SE.

## Power (printed before the outcome was joined)
Power was 0.790 at an assumed composer share of 0.3 (SE 0.0148), matching the frozen 0.79. At a share of 0.5 it was 0.940 (SE 0.0125). If the prediction were true, the kill-like rule would fire wrongly 2.7% of the time.

## What came out (5,858 songs, 1,199 composers)
- **β = +0.0142, SE 0.0145, p = 0.33**. The 95% range is −0.014 to +0.043.
- Halves: −0.0002 (SE 0.0228, p 0.99; 2,973 songs, 644 composers) and +0.0259 (SE 0.0169, p 0.12; 2,885 songs, 555 composers).
- Second model (Poisson on n_sets, median 14): +0.0469 (SE 0.0221, p 0.034). This figure is in log-count units, not SD of y_cov, so it cannot be compared directly with the +0.05 prediction.

## Verdict by the frozen rule
The pass-like rule fails: p .33 is not below .01, and the first half is not positive. The kill-like rule is met, but narrowly: +0.05 lies 2.5 SE above β, just past the range's upper end of 0.043. Because the test is an estimate, **it passes nothing and kills nothing**. As a reading, the test had good power, and a +0.05 effect would most likely have shown up. The data fit a smaller positive effect or none.

## Renaming check (`../measure_gates.json`)
- Two-chart stability is 0.645 (0.621 after removing size). iReal against Wikifonia is 0.418.
- Within composer, ρ is −0.178 with ch_rep and +0.246 with V, so the gate **passes**.
- 74% of T's variance lies within composer.

## Reported, deciding nothing
No other readings were frozen.

## What it cannot say
- **Jazz idiom:** this is the author's own reason for withdrawing. Transposed ii–V chains are standard in jazz, so T may measure "how jazz" a tune is.
- **Genre within composer:** the genre labels are coarse.
- **Chart writers:** the chords are user transcriptions, and two sources agree only moderately (0.42).
- **Name matching:** composers come from matched name tokens.
- **Selection:** only charted, already-covered tunes are in the sample.

It is an association, not a cause.
