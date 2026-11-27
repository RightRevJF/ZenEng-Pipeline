# iiv_singletons: result (written after seeing results; counted; a lead, not a finding)

**In plain words.** After `iiv_chunk` found that songs whose chords move more often through the ii-V step (minor seventh to dominant seventh a fourth up) were covered by more artists, we asked whether this also holds for 2,707 songs that had never been joined to the cover counts: songs whose composer has only one matched song. It does, at about the same size. Because the test was written after seeing the first result, and because it compares songs by *different* composers (so a famous writer's tune sits next to an obscure one's), this is a lead to confirm on fresh songs, not a finding. The pattern sits mostly in swing and ballad tunes.

**Predicted (frozen in b1b3512, before the outcome was joined).** +0.07 SD of y_cov per SD of IIV. K = 6, α = .05/6 = .00833. Pass: p < α, positive overall, in both composer halves and in the Poisson model. Kill: +0.07 outside β ± 1.96 SE.

**Power (printed before the estimate):** 0.69 (300 fake draws, α = .05/7, SE 0.022), above the 0.2 floor, so counted.

**What came out (result.json).**

| | β | SE | p | N |
|---|---|---|---|---|
| Main (OLS, HC1; genre + decade dummies) | +0.057 | 0.019 | 0.0028 | 2,707 |
| Half 0 | +0.041 | 0.026 | | 1,400 |
| Half 1 | +0.077 | 0.028 | | 1,307 |
| Poisson on n_sets (log scale, HC0) | +0.150 | 0.029 | 3e-7 | 2,707 |

95% range +0.020 to +0.094; the prediction +0.07 lies inside.

**Verdict by the frozen rule: PASS (a lead).**

**How firm.** p is about three times below α; it would fail at .001. Half 0 alone is weak (z about 1.6). The estimate is a little under the prediction. The two crashes (run_crashed*.log) happened after the outcome loaded and before any estimate; `git diff b1b3512` shows only the second-model line of test.py changed. Halves and genre readings standardise ln_sets within each subset (same quantity as y_cov, rescaled).

**Renaming check (measure_gates.json, design songs).** IIV two-chart stability 0.772 (≥ 0.5); cross-source 0.584; within-composer ρ with ch_rep −0.021, with V +0.217 (both within ±0.8): not a renamed ch_rep or V. These gates were measured on the within-composer design, not on these singletons.

**Reported readings (deciding nothing).**
- No genre dummies: +0.055 (SE 0.019).
- jazz_genres (swing, ballad; N 827): +0.087 (SE 0.034).
- other_genres (N 1,880): +0.021 (SE 0.022), not distinguishable from zero. The jazz minus other gap (about +0.066, SE about 0.040) is not settled either, but the lead rests mostly on jazz-idiom tunes.

**What it cannot say.**
- *Across composers:* who wrote the song, and how famous they are, is not held.
- *Jazz idiom:* IIV partly marks the jazz style, and genre is a coarse bin; the split above points this way.
- *Chart writers:* iReal charts are written by jazz players who may add ii-Vs to tunes they play (see `iiv_source`, which could not settle this).
- *Name matching:* a "singleton" may be a composer whose other songs sit under a different spelling.
- *Selection:* an obscure composer's tune that has a chart at all is probably already in the jazz repertoire.
