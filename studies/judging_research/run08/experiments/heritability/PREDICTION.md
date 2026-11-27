# heritability: harmonic heritability of covers (R08-I2; card 2). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea R08-I2 (the Inventor, revised in round 3). Under neutral copying, songs with similar changes by *other* composers have unrelated cover residuals; if fitness rides on the changes, chord-space neighbours are alike, with no measure to guess. No outcome has been opened by the chair or by any brainstorm agent. Status: **COUNTED** (one of K = 5).

## The neighbour rule (frozen now; `measures.neighbours`, stored in `$DL/choco/measures_run08.json` → `neighbours`)
- Each design song's representative chart = the first of its sorted chart ids with at least one interval trigram.
- Tokens: interval-coded chord trigrams ((r2 − r1) mod 12, (r3 − r2) mod 12, q1, q2, q3) on the change sequence ((root, bitmap), repeats merged), as a set.
- Binary tf-idf over the design songs (idf = ln((N+1)/(df+1)) + 1), L2-normalised; similarity = cosine.
- A neighbour of i must be another design song with **another composer key, no shared name token** (common.tokens over all the song's charts' artists strings), **no shared title variant**, and **trigram-set Jaccard < 0.4** with i (contrafacts of one parent dropped, round 3), and cosine > 0.
- Neighbours = the 10 most similar (ties by clique id); the first 5 give the second model.
- Notes-side checks (`measure_gates.json`): 5,852 songs have neighbours (5,812 have ten); mean top-10 cosine 0.259 (10th–90th percentile 0.107–0.473); 31% of neighbours share the coarse genre against 17% by chance.

## Outcome and statistic
- r = residual of y_cov (standardised log(1 + distinct artist sets), `common.load_outcomes` after the guard) on composer fixed effects, genre dummies and 5-year first-year bins (unknown its own bin).
- ρ_nb = corr(r_i, mean of r over i's 10 neighbours) over the songs with neighbours (`models08.rho_nb`).
- **Null:** r permuted within **composer-genre × decade** cells (decade = `common.decade_bins` of the first year, an outcome-side variable read only after the commit), 10,000 permutations, seed 2026 (`models08.perm_null`). The permutation keeps each cell's values, so the null is centred on the cell-level (scene) part of ρ_nb, not on 0. **The test reads the excess = ρ_nb − mean(null)** (`models08.excess_test`); p = (1 + #{|null − mean| ≥ |excess|}) / 10,001, two-sided; the 95% range = excess ± 1.96 · SD(null).
- Halves: the excess over the songs i of each composer half (`common.halves`), neighbours from anywhere, from the same permutations.
- Second model: the excess with the 5 nearest neighbours.

## Prediction
**Excess ρ_nb = +0.06** (the Inventor's figure for this null, lowered from +0.10 once siblings are removed). The neutral null predicts 0.

## Rules (K = 5, α = .01, two-sided)
- **Pass:** p < .01, excess > 0, both halves' excess > 0, the K = 5 excess > 0 (`common.verdict`).
- **Kill (range kill):** +0.06 outside the 95% range. An excess near 0 is a ceiling reading: the changes carry no shared fitness that other composers' tunes inherit.
- **Unsettled:** anything else.

## Power (printed again by test.py before the estimate)
`power_run08.heritability_sim`: fake y = composer effect (share 0.3, **assumption**) + a · f + noise, f = z(x + neighbour mean of x), x iid; a = 0.35 (raw ρ_nb 0.053, the grid point nearest 0.06); null SD from 200 permutations; p by the normal approximation on excess / null SD; 100 draws; power = p < .01 with excess > 0.
- **Frozen status: power 0.65**, with pseudo-decade cells (composer × genre × a pseudo-decade: each composer a random base decade, each song base ± round(N(0, 1)); the real decades are outcome-side and unknown). Mean excess 0.034, null SD 0.0117; the kill fires on 61% of draws under this fake field and on 100% under a zero field.
- Without the decade (composer × genre cells): power 0.81, mean excess 0.048, null SD 0.0139, kill if the field is true 11%; composer share 0.5: power 0.84.
- **A warning written before the outcome:** the decade cells hold part of a real song-level field in the null, so the excess runs below raw ρ_nb, and a true field like the simulated one would often land under +0.06. A range kill here is weaker evidence than its 100% firing under zero suggests; read the excess with that in mind.

## Reported, deciding nothing
The excess on songs with first year ≥ 1950 (2,000 permutations); the excess when the cells are genre × decade only (the Inventor's first form, 2,000 permutations).

## What it cannot say
Neighbours share idiom as well as changes (31% same genre); the permutation within composer-genre × decade cells holds the scene only coarsely. A positive ρ_nb says covers cluster in chord space beyond composer, genre and era, not which feature carries it.
