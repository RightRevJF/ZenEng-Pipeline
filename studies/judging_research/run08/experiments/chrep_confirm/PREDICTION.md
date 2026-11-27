# chrep_confirm: chord repetition against covers, on fresh songs (W01-J1). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Idea **W01-J1** (status "passed" on seen Hooktheory songs: −0.042 SD of log covers per SD of chord repetition within artist, p .009; the McGill fresh leg −0.028, unsettled; run 07 on Lakh MIDI with another outcome, −1.93 pp, unsettled). No outcome has been opened by the chair or by any brainstorm agent. Status: **COUNTED** (one of K = 5).

## Measure
`measures.py: listener_measures()["ch_rep"]`: on each chart, chords as (root, 12-bit bitmap) tokens, consecutive repeats merged; ch_rep = share of the chart's 3-grams of changes already heard earlier in the chart. Song value = unweighted mean over the song's measured charts (charts with ≥ 8 chords and ≥ 6 changes). **Not** the same construct as W01-J1's: that was within one Hooktheory section; this is a whole lead-sheet chart (one chorus, repeats as written). Two-chart stability 0.597 (2,466 songs with two non-identical charts); iReal against Wikifonia 0.311 (`measure_gates.json`).

## Songs
The run 08 design (`common.load_design()`): 5,907 within-composer ChoCo songs in 1,199 composers. Drop rule: songs with no measured chart (49) → **5,858 songs**. Composers left with one song stay in the data and carry no weight under the composer fixed effect.

## Outcome and model
- y_cov = standardised log(1 + distinct performing-artist sets) over the analysed songs (`common.load_outcomes`, only after the guard).
- Primary: `common.ols_fe` (within composer, CR1 clustered by composer) of y_cov on z(ch_rep), genre dummies and first-year decade dummies (`common.design_matrix(rows, "ch_rep", [])`). **No size columns**: W01-J1's frozen model held only the artist and the year (and views), and a confirmation runs the model that passed. The size-held model is reported (below).
- Halves: `common.halves(composer)`, the same model in each half.
- Second model: `models08.poisson_fe` on n_sets (Poisson pseudo-likelihood, composer fixed effects concentrated out, cluster-robust SE), same columns.

## Prediction
**β = −0.04 SD of y_cov per SD of ch_rep** (W01-J1's own line: −0.04 or stronger).

## Rules (K = 5 counted tests tonight, α = .05/5 = .01, two-sided)
- **Pass:** p < .01, β < 0, β < 0 in both composer halves, Poisson coefficient < 0 (`common.verdict`).
- **Kill (range kill, R07-3):** −0.04 lies outside β ± 1.96 SE.
- **Unsettled:** anything else.

## Power (printed again by test.py before the estimate)
`common.fake_power` on these 5,858 rows and columns, at β = −0.04 and α = .01, 300 draws, seed 11:
- composer share of outcome variance 0.3 (**an assumption**; the real share is unknown before the outcome): **power 0.487**, fake SE 0.0152;
- composer share 0.5 (sensitivity): power 0.687, SE 0.0129.
- The range kill fires on 4.3% of draws if −0.04 is true (fake_power) and about 75% if the true effect is 0 (normal approximation at SE 0.0152).

## Reported, deciding nothing
β with the size block held (V, ln_chg, ln_bars), the W01-J1-reading under length; writer-match songs only; songs with first year ≥ 1950.

## What it cannot say
A pass replicates the direction on lead-sheet charts within composer, not within performer; W01-J1's construct was section-level. Chart length and written repeats move ch_rep (within-composer ρ +0.59 with ln_chg); a sign that flips with size held is a warning, not a verdict. Hits only (every song has a Discogs-VI clique).
