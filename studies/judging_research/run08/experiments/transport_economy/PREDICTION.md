# transport_economy: transport economy (R08-G1; card 1). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea R08-G1 (the Geometer). No outcome has been opened by the chair or by any brainstorm agent. Status: **ESTIMATE, not counted.** Its power (0.223) clears the 0.2 floor at α = .01, but the counted set is full at K = 5: counting it too would make K = 6 or 7, where it and key_travel fall under the floor (0.19 at .05/6). The K rule is in `../../chair.md`. It passes nothing and kills nothing; its frozen rules are still printed against α = .01 so the reading is comparable.

## Measure
`measures.py: geometer_measures()["econ"]` (the Geometer's `g_measures.py`, econ2): on the change sequence of pitch-class sets (consecutive identical sets merged), w-bar = mean chromatic circular W1 between successive chords (each chord's tones equal weight; card 1 Eq. 12, in semitone steps); b = mean W1 over all ordered pairs of positions holding different chords (the expected step if the same changes came in random order); **econ = 1 − w-bar / b**. No settings.

Gates (`measure_gates.json`): two-chart stability 0.624 (residual 0.622), iReal against Wikifonia 0.406; within-composer ρ ch_rep −0.062, V +0.122: **passes**. ρ with w-bar −0.62 (held).

## Songs, outcome, model
The run 08 design, **5,858 songs, 1,199 composers**. y_cov; `common.ols_fe` of y_cov on z(econ), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), genre and decade dummies; composer FE, CR1. Halves; second model `models08.poisson_fe` on n_sets.

## Prediction
**β = +0.03 SD of y_cov per SD of econ** (the Geometer's round 3).

## Rules as frozen (reported against α = .01; an estimate decides nothing)
Pass-like: p < .01, β > 0, both halves > 0, Poisson > 0. Kill-like: +0.03 outside β ± 1.96 SE.

## Power
`common.fake_power`, β = +0.03, α = .01, 300 draws: composer share 0.3 (**assumption**) power 0.223, SE 0.0170; 0.5: power 0.323, SE 0.0144.

## Reported, deciding nothing
econ without w_chr (the Geometer's own second model).
