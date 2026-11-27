# iiv_chunk: the ii-V chunk (R08-L3). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea R08-L3 (the Listener; music cognition: players memorise changes as known chunks). No outcome has been opened by the chair or by any brainstorm agent. Status: **COUNTED** (one of K = 5).

## Measure
`measures.py: listener_measures()["IIV"]`: on the change sequence ((root, bitmap) tokens, repeats merged), IIV = share of changes that go from a minor seventh (bitmap has the minor 3rd and minor 7th, no major 3rd) to a dominant seventh (major 3rd and minor 7th, no minor 3rd) whose root is a fourth up (root + 5). No settings. Song value = unweighted mean over measured charts.

Gates (`measure_gates.json`): two-chart stability 0.772 (residual on size 0.708), iReal against Wikifonia 0.584; within-composer ρ ch_rep −0.021, V +0.217: **passes**. Within-composer ρ with w-bar (mean chromatic W1 step) −0.34, so w-bar is held (the Skeptic).

## Songs
The run 08 design; drop songs without a measured chart → **5,858 songs, 1,199 composers**.

## Outcome and model
y_cov; `common.ols_fe` of y_cov on z(IIV), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), genre dummies, first-year decade dummies; composer FE, CR1 by composer. Halves by `common.halves`. Second model: `models08.poisson_fe` on n_sets, same columns.

## Prediction
**β = +0.04 SD of y_cov per SD of IIV** (the Listener's round 3, lowered from +0.06).

## Rules (K = 5, α = .01, two-sided)
- **Pass:** p < .01, β > 0, both halves > 0, Poisson coefficient > 0.
- **Kill (range kill):** +0.04 outside β ± 1.96 SE.
- **Unsettled:** anything else.

## Power (printed again by test.py before the estimate)
`common.fake_power`, β = +0.04, α = .01, 300 draws: composer share 0.3 (**assumption**) **power 0.387**, SE 0.0178; composer share 0.5 (sensitivity) power 0.553, SE 0.0150. Kill fires about 61% of the time if the effect is 0 (normal approximation).

## Reported, deciding nothing
IIV without w_chr; writer-match songs only. The Listener's second reading (late covers holding log(K10 + 1)) is reported in `../cover_timeline/` (its gamma for IIV), deciding nothing.

## What it cannot say
IIV is the jazz idiom (Medium Swing +0.73 SD above Pop); genre is held, and the test is within composer, but a composer who writes jazz and pop tunes is compared across his own styles. Chord spelling (m7 vs 6, dominant vs sus) varies by chart writer.
