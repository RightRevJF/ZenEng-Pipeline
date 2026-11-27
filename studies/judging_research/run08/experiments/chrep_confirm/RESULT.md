# chrep_confirm: result

**Verdict: KILLED by the range rule written first.** The predicted size (-0.04) lies outside the estimate's 95% range.

## In plain words
The research's one passing idea, from Hooktheory songs it had already seen, was this: songs that repeat their own chord moves more get covered by fewer artists. This test checked it on 5,858 fresh songs from lead-sheet charts, comparing each songwriter only with themselves. The effect came out at about zero, and the predicted size is ruled out. A much smaller effect is still possible.

## What was predicted (commit e624a7e, before any outcome)
β = -0.04 SD of y_cov per SD of ch_rep, within composer, with genre and decade held. Pass needed: p < .01, β < 0, both composer halves < 0, and the Poisson coefficient < 0. Kill: -0.04 outside β ± 1.96 SE. The test was counted and frozen at α = .01. The verdict holds at the final .05/6, because range kills do not depend on alpha.

## What came out (result.json)
- Power, printed before the outcome was joined: 0.487 at composer share 0.3 (an assumption); 0.687 at 0.5. Both clear the 0.2 floor.
- **β = -0.003, SE 0.014, p = .84; 5,858 songs, 1,199 composers; 95% range -0.030 to +0.025.**
- Halves: +0.002 (SE 0.018) and -0.007 (SE 0.022). The signs disagree.
- Poisson on n_sets: -0.025 log points, SE 0.022, p = .26.

## How firm
-0.04 is 2.6 SE from the estimate, about 0.01 past the range's lower end. If -0.04 were true, the kill would have fired on 4.3% of fake draws. The kill is clear, but not by a wide margin.

## Renaming check (measure_gates.json)
ch_rep passes, narrowly. Its two-chart stability is 0.597 against a 0.5 bar. Agreement between iReal and Wikifonia charts is only 0.311. Its within-composer ρ with V is -0.149, so it is not a renamed V. It tracks size closely: ρ = +0.595 with ln_chg and +0.523 with ln_bars. The Geometer's L_rep is the same number (ρ = 1.0).

## Reported readings (decide nothing)
- Size held (V, ln_chg, ln_bars): -0.020, SE 0.021, p = .33. This moves toward the prediction, and its range includes -0.04.
- Writer-match songs only: -0.005, SE 0.014 (5,541 songs).
- First year 1950 or later: -0.012, SE 0.018 (4,360 songs).

## What it cannot say
- **A different measure.** This measures repetition over a whole chart; W01-J1 measured it within a section. The kill applies to this measure.
- **Noise and length.** Noisy charts pull estimates toward zero, and chart length drives ch_rep (see the size-held reading).
- **Confounds.** Genre can still vary within one composer. The charts reflect their writers' habits and, often, jazz idiom. Composer names were matched automatically.
- **Selection.** Only tunes that have charts are here, and all are hits. The comparison is within composer, not within performer.
