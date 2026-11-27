# tonic_resistance: is home the electrical hub? (R03-I2, with written keys). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea **R03-I2** (status testing: unsettled in runs 03, 05, 06; retirement recommended by runs 05 to 07; Jason has not decided). Run 07 left it out because Lakh songs carry no key; **ChoCo charts carry a written key** (41,961 of 42,002), so the measure is defined as written, without a key-finder. No outcome has been opened by the chair or by any brainstorm agent. Status: **ESTIMATE, not counted.** Power 0.277 clears the floor at α = .01, but the counted set is full at K = 5 (`../../chair.md`, the K rule); it is ranked below the five counted tests because retirement is recommended. It passes nothing and kills nothing.

## Measure
`measures.py: rel_tokens()` and `H_song()` (run 06 `common.H_song`, unchanged): chart tokens = ((root − written tonic) mod 12) · 9 + run 03's quality code (the chart bitmap read as stacked intervals; `qual_bm`), consecutive repeats merged; moves pooled with the wrap (last → first); conductance C = M + Mᵀ, diagonal 0; T = the root-0 token with the largest row sum; keep T's connected piece (≥ 3 chords); **H = Σ_x π_x ω_xT / Σ_x Σ_y π_x π_y ω_xy** (effective resistances from the pseudo-inverse Laplacian). Charts without a key or with fewer than 3 distinct tokens give no H. Unit tests (`measures.unit_tests()`): 5-cycle 1.0, 3-leaf star with T at the hub 0.6, T on a leaf 1.4.

Gates (`measure_gates.json`): two-chart stability 0.651 (residual on size 0.646), iReal against Wikifonia 0.376; within-composer ρ ch_rep −0.042, V −0.082: **passes**.

## Songs, outcome, model
The run 08 design; drop songs with no H → **5,700 songs, 1,197 composers**. y_cov; `common.ols_fe` of y_cov on z(H), z(ch_rep), z(V), z(ln_chg), z(ln_bars), z(H_links) (ln distinct links of the token graph, run 03's size column), genre and decade dummies; composer FE, CR1. Halves; second model `models08.poisson_fe` on n_sets.

## Prediction
**β = −0.03 SD of y_cov per SD of H** (run 03's figure, in these units): home more central, more covers.

## Rules as frozen (reported against α = .01; an estimate decides nothing)
Pass-like: p < .01, β < 0, both halves < 0, Poisson < 0. Kill-like: −0.03 outside β ± 1.96 SE.

## Power
`common.fake_power`, β = −0.03, α = .01, 300 draws: composer share 0.3 (**assumption**) power 0.277, SE 0.0148; 0.5: power 0.453, SE 0.0125.

## Reported, deciding nothing
H without H_links.

## What it cannot say
The written key is the chart writer's; modal and modulating tunes get one tonic. Full charts have more distinct chords (median 12 per chart, 10th to 90th percentile 5 to 22) than Hooktheory clips (mostly 3 to 6), so H here is a whole-tune graph, a new unit for this idea.
