# formula_search: result (discovery on half 0; three confirmations on half 1, counted where power ≥ 0.2; K = 4, α .0125)

**The search.** 3,969 candidate formulas (61 base features, their 1,830 pairwise differences and 1,830 products, all of z-scores; notes only). Notes-side gates (stability ≥ 0.20; not a renamed REP, ch_rep or length): 1,323 passed. On half 0 (4,097 songs, 817 artists), 15 formulas had p < .001 where 1.3 were expected by chance, and **every one of the top 25 contains rhythm repetition** (the share of 2-, 3- or 4-note rhythm figures heard earlier in the 8 bars). The plain feature `rhythm_rep2` alone: +0.051 (p .0003).

**Selected and frozen before half 1 was read (selected.json, 98f80b8):**

| Formula | Half 0 | Prediction (half) | Power | Half 1 | Verdict |
|---|---|---|---|---|---|
| rhythm repetition (2-note) minus share of steps | +0.055 (SE 0.014) | +0.027 | 0.22 | **+0.017** (SE 0.014, p .21); quarter-halves +0.007, +0.029; logit +0.09 | Unsettled |
| share on the downbeat minus rhythm repetition (3-note) | −0.051 | −0.026 | 0.18 | −0.001 (SE 0.017) | Estimate |
| phrase range minus rhythm repetition (2-note) | −0.046 | −0.023 | 0.14 | −0.007 (SE 0.013) | Estimate |

**What it means.** The search found, without being told, the same variable the engine comparison flags and the world-music branch's cross-cultural count names (rhythm repeats more than pitch): **a song's rhythm figures coming back**. On the sealed half it leaned the predicted way at about 60% of the predicted size and did not clear the bar. Winner's curse took most of the discovery's size, as it usually does. It is the best lead the project has had on how a melody is built, and it is a lead, not a finding: it needs unseen melodies.

**What it cannot say.** Seen songs (the halves were used for other measures before). Three formulas were confirmed, not 1,323, so the confirmation is clean, but the discovery's size is inflated. Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0).
