# key_travel: key travel on the circle of fifths (R08-L1 merged with R08-I1; card 1). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. **The pass's mathematics** (card 1: Rabin, Delon & Gousseau, circular optimal transport). Ideas R08-L1 (the Listener, TRAV5, counted) and R08-I1 (the Inventor, E, now this test's second reading). No outcome has been opened by the chair or by any brainstorm agent. Status: **COUNTED** (one of K = 5).

## Measure
`measures.py: listener_measures()["TRAV5"]` (the Listener's `checks_r1.py`, copied):
1. each chord's tones get equal shares of its duration; tones are pooled into 4-bar windows, window = floor(bar) // 4 (bar = floor of the chart time);
2. each window's 12-bin distribution is moved to the circle of fifths (bin 7·pc mod 12);
3. TRAV5 = mean over consecutive windows of the circular W1 (card 1 Eq. 12, Σ|D − median D|, D = F − G, in fifth-steps).
TRAVL1 (the same windows under plain L1, card 1's trade-off partner) is held, so TRAV5 reads mass moving *round* the circle, not reweighting. One setting (4 bars). Song value = unweighted mean over measured charts. Unit tests in `measures.unit_tests()` (card 1's C→F and C→Db).

Gates (written before any outcome; `measure_gates.json`): two-chart stability 0.738 (residual on size 0.619), iReal against Wikifonia 0.515; within-composer ρ with ch_rep −0.285, with V +0.208 (gate: stability ≥ 0.5, |ρ| ≤ 0.8): **passes**. ρ with TRAVL1 +0.82 within composer (held, so the SE is wide).

## Songs
The run 08 design, 5,907 within-composer songs; drop songs without TRAV5 or a control → **5,829 songs, 1,198 composers**.

## Outcome and model
y_cov (standardised log(1 + distinct artist sets); `common.load_outcomes` after the guard). `common.ols_fe` of y_cov on z(TRAV5), z(TRAVL1), z(ch_rep), z(V), z(ln_chg), z(ln_bars), genre dummies, first-year decade dummies (`common.design_matrix(rows, "TRAV5", ["TRAVL1","ch_rep","V","ln_chg","ln_bars"])`); composer FE, CR1 by composer. Halves by `common.halves(composer)`. Second model: `models08.poisson_fe` on n_sets, same columns.

## Prediction
**β = +0.05 SD of y_cov per SD of TRAV5** (the Listener's round 3, lowered from +0.07 once genre is held). Tunes that tour key areas are covered more.

## Rules (K = 5, α = .01, two-sided)
- **Pass:** p < .01, β > 0, β > 0 in both halves, Poisson coefficient > 0.
- **Kill (range kill):** +0.05 outside β ± 1.96 SE.
- **Unsettled:** anything else.

## Power (printed again by test.py before the estimate)
`common.fake_power`, β = +0.05, α = .01, 300 draws: composer share 0.3 (**assumption**) **power 0.213**, SE 0.0278; composer share 0.5 (sensitivity) power 0.323, SE 0.0235. Kill fires on 3.7% of draws if +0.05 is true and about 44% if the effect is 0 (normal approximation). The power sits just over the 0.2 floor; with 300 draws its Monte Carlo error is about ±0.024.

## Second reading (reported, deciding nothing; frozen)
**E** (the Inventor's key excursion: duration-weighted bar profiles with carry-over, non-overlapping 4-bar windows from the first bar, mean circular W1 on the fifths circle from each window to the whole chart; `inventor_measures()["E"]`), holding spread (the chart's fifths-circle spread, card 1 (d)), TRAVL1, ch_rep, V, ln_chg, ln_bars: predicted **+0.08** (the Inventor's figure). Also reported: TRAV5 without TRAVL1; writer-match songs only.

## What it cannot say
TRAV5 is partly a jazz detector (the Skeptic: Medium Swing +0.63 SD above Pop); genre is held, but style within genre is not. Chart writers spell keys differently; cross-source agreement 0.52.
