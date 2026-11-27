# iiv_singletons: the ii-V share on songs never joined to an outcome. AFTER SEEING RESULTS. Frozen before its outcome is joined

Run 08, 27 November 2026, written by the orchestrator after `iiv_chunk` passed (β +0.073, SE 0.018) and `heritability` passed. **Labelled after seeing results: a pass here is a lead that needs confirmation on songs not yet used, never a finding.** Status: **COUNTED** (power below is over 0.2). The pass's test total becomes K = 6 counted (the five frozen earlier plus this one; `iiv_source` is an estimate), so α = .05/6 = .00833. The earlier five keep their verdicts under the new bar: their passes have p far under .0083, and range kills do not depend on α.

## Measure
`measures.py: listener_measures()["IIV"]`, exactly as in `iiv_chunk` (share of changes from a minor seventh to a dominant seventh a fourth up), song value = unweighted mean over its charts, computed by `posthoc08.singleton_rows()` with `measures.chart_row`.

## Songs
The run 08 matched songs whose composer key has only ONE matched song (`common.load_design(within=False)`, `within` false): 2,733, of which 2,707 have IIV and every control. None of them has ever been joined to an outcome (they are outside the within-composer design every other test used). Same exclusions as the design (seen cliques, McGill hold-out, stop artists).

## Outcome and model
y_cov standardised over these songs (`common.load_outcomes`, after the guard). One song per composer, so there is no composer fixed effect: plain OLS (`posthoc08.ols_hc1`, HC1 robust SEs) of y_cov on z(IIV), z(w_chr), z(ch_rep), z(V), z(ln_chg), z(ln_bars), genre dummies and first-year decade dummies. This compares songs ACROSS composers: it holds genre and era but not who wrote the song. Halves by `common.halves(composer)`. Second model: `models08.poisson_fe` on n_sets with one group (a plain Poisson pseudo-likelihood), same columns.

## Prediction
**β = +0.07 SD of y_cov per SD of IIV** (the within-composer estimate from `iiv_chunk`, carried over unchanged).

## Rules (K = 6, α = .00833, two-sided)
- **Pass:** p < .00833, β > 0, β > 0 in both halves, Poisson coefficient > 0. A pass is a lead (after seeing results).
- **Kill (range kill):** +0.07 outside β ± 1.96 SE.
- **Unsettled:** anything else.

## Power (printed by test.py before the estimate)
`posthoc08.fake_power_ols`, β = +0.07, α = .05/7 (computed before K was settled at 6; slightly conservative), 300 draws, y = β z + noise on the real rows and columns: **power 0.69**, SE 0.022.

## What it cannot say
Across composers, a famous songwriter's tunes and an obscure one's are compared, so a composer's fame is not held. IIV is still partly the jazz idiom; genre is held as a coarse bin.
