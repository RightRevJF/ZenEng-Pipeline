# transposed_rep: transposed repetition T (R08-G2). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea R08-G2 (the Geometer). Its author **withdrew it from the count** in round 3 ("estimate only": it reads jazz). No outcome has been opened by the chair or by any brainstorm agent. Status: **ESTIMATE** (passes nothing, kills nothing), whatever its power.

## Measure
`measures.py: geometer_measures()["T_rep"]` (the Geometer's `g_measures.py`): on the change sequence of (root, bitmap) tokens (repeats merged), each 3-gram is reduced to its transposition class (q1, Δ1, q2, Δ2, q3); O = share of 3-grams whose class was heard earlier; L = share heard earlier at the same pitch level (L is exactly ch_rep on this sequence; within-composer ρ 1.00); **T = O − L**. No settings.

Gates (`measure_gates.json`): two-chart stability 0.645, iReal against Wikifonia 0.418; within-composer ρ ch_rep −0.178, V +0.246: passes. On the design, 74% of T's song variance lies within composer (the Skeptic's 27% was over iReal artist strings, before the composer match).

## Songs, outcome, model
The run 08 design, **5,858 songs, 1,199 composers**. y_cov; `common.ols_fe` of y_cov on z(T_rep), z(ch_rep) (= L), z(V), z(ln_chg), z(ln_bars), genre and decade dummies; composer FE, CR1. Halves; second model `models08.poisson_fe` on n_sets.

## Prediction
**β = +0.05 SD of y_cov per SD of T** (the Geometer).

## Rules as frozen (reported against α = .01; an estimate decides nothing)
Pass-like: p < .01, β > 0, both halves > 0, Poisson > 0. Kill-like: +0.05 outside β ± 1.96 SE.

## Power
`common.fake_power`, β = +0.05, α = .01, 300 draws: composer share 0.3 (**assumption**) power 0.790, SE 0.0148; 0.5: power 0.940, SE 0.0125. Had its author not withdrawn it, it would have been the most powerful y_cov test tonight; the withdrawal stands (run 07's rule: withdrawals are respected).
