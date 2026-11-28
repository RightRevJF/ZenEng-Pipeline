# Run 10, round 1: the Listener

27 November 2026. Stance: expectation, surprise, memory, exposure, and what makes a musician want to learn a tune. A tunebook entry on TheSession is a musician deciding to learn the tune. A recording by another artist is a player who learned it and then chose it for an album. Both start with a melody that is easy to carry in memory and still worth carrying.

Code: `/home/claude/scripts/listener/measures_listener.py` (`measure(t) -> dict`); checks in `check.py` in the same folder. Every corpus model is trained on split A first settings only (notes only). Each tune is left out of its own model by subtracting its first setting's counts, and the second setting is scored against the same leave-one-out model. No outcome was opened.

**How the checks were run.** All checks used split A with seed 10. Renaming was run on a random 3,000 tunes (2,982 computable) with `common10.renaming`. Stability is `common10.stability`, the Spearman between first and second settings, over the first 3,000 tunes that have two settings. Compute was about 3 CPU-minutes in all. The bar for stability is 0.5 (R09-5).

---

## L1. Self-learnability gain (SLG): a tune that teaches you its own grammar

**Mechanism.** A musician learns a tune once its own past predicts its future better than their general knowledge of the idiom does. The tune "teaches itself" and becomes worth memorising as an individual.

**Measure.**
- Write each note as its pitch class relative to the tonic, with repeated notes merged. Merging matters because repeated notes depend on how the transcriber wrote them; that is the R05-L3 lesson.
- Self model: an add-one bigram over the 12 classes, built only from the tune's own earlier notes.
- Corpus model: an add-one bigram for the tune's type (reel, jig and so on), built leave-one-out from split A.
- SLG is the mean of log2 p_self minus log2 p_corpus over the notes in the second half of the expanded tune.
- The only setting is add-one smoothing. It is negligible for the corpus model; for the self model it is the plain uninformed prior.
- A companion, `slg_win`, is the share of those notes where the self model wins.

**Prediction.** Positive. **+0.03 SD of z(y_cov) per SD**, with the same sign for y_love. Of the three, it is the closest to "learning it".

**Kill.** +0.03 lies outside the 95% range, by R07-3. That happens if the estimate is below about +0.012, which includes a null or negative result.

**Caveat.** SLG is partly repetition and length: bar_rep +0.33, ln_notes +0.33. It also rises with core_ic (+0.41): an idiosyncratic tune gains more from its own past. Bar_rep and ln_notes should be held as extra controls. If the coefficient only survives without them, SLG is the repetition baseline renamed.

| check | value |
|---|---|
| stability (Spearman, n 3,000) | **0.562** (slg_win 0.596) |
| R^2 on 13 baselines | 0.284 (slg_win 0.403) |
| largest baseline rho | ln_notes +0.33, bar_rep +0.33, leap_share +0.15 |

---

## L2. Typical skeleton, surprising surface (TSG)

**Mechanism.** Card 2 (McBride & Fitch) shows that a tune's identity lives in a skeleton of strong-beat notes, which players conserve, while variation lives on weak beats. A listener can lock onto a skeleton that follows the idiom's expectations. Surprise is then welcome on the surface, where it is cheap and ornamental: Meyer and Huron's balance of expectation and violation, placed by meter.

**Measure.**
- core_ic is the mean corpus surprisal, in bits, of the skeleton. The skeleton is the sequence of relative pitch classes of the notes that start on a beat (integer beatpos). The model is a bigram on skeleton sequences of the tune's type, leave-one-out.
- surf_ic is the mean corpus surprisal of off-beat notes under the type's surface bigram, with repeated notes merged.
- **TSG = core_ic − surf_ic.** A negative value means a typical skeleton with a surprising surface. Nothing is fitted.

**Prediction.** Negative. **−0.03 SD per SD** for y_cov, with the same sign for y_love. If the effect is real, the y_love sign should be at least as strong, because a learner meets the skeleton first.

**Kill.** −0.03 outside the 95% range, for example an estimate of −0.01 or above with SE 0.009. Two diagnostic secondaries are not counted: core_ic alone, predicted negative, and surf_ic alone, predicted at most weakly positive.

**Skeptic's reading (card 2).** If core_ic alone carries everything, the result is "typicality wins", not "balance".

| check | value |
|---|---|
| stability | **0.597** (core_ic 0.564, surf_ic 0.557) |
| R^2 on baselines | **0.152** (core_ic 0.203, surf_ic 0.259) |
| largest baseline rho | step_share +0.35, int_entropy −0.30, leap_share −0.25 |

---

## L3. Cheeger cut aligned with the parts (CUT_AB): geometry from the spectral gap

**The mathematics.** This builds on the spectral gap already in the repo (Jason's S = 1 + g/π).

1. Take the undirected pitch-transition graph. Its nodes are MIDI pitches, with the octave kept. Each edge weight is the count p(a,b) + p(b,a), which is card 1's symmetrisation. Unisons are dropped.
2. Form its normalised Laplacian. Let g be the second eigenvalue and v2 its (Fiedler) eigenvector.
3. **Cheeger's inequality** g/2 ≤ h ≤ √(2g) ties g to the graph's best bottleneck cut h, its conductance.
4. f = D^−1/2 v2 is the continuous relaxation of the minimum normalised cut, so its sign splits the pitch set into the two regions that the melody crosses most rarely.

**What it predicts (extrapolation).** On its own, g counts the pitches: R^2 0.66, rho −0.62 with range. My Listener question is different: *is the bottleneck a landmark in time?* A tune whose A and B parts live in different regions of its own pitch graph tells you which part you are in, as in the classic B part "up the neck". That gives memory a two-chamber map, and gives contrast without losing coherence.

**Measure.** CUT_AB is the |Pearson r| over the expanded notes between each note's Fiedler coordinate f(pitch) and the indicator "the note is in the second half of the tune". In AABB form, that is A against B. Nothing is fitted.

**Prediction.** Positive. **+0.03 SD per SD**, with the same sign for y_love.

**Kill.** +0.03 outside the 95% range.

**Companion: g itself.** g (equivalently S) is reported as an estimate only. It has stability 0.82 but is renamed by range and n_pitch. My expected sign for g is negative, because a stronger bottleneck means a smaller g. The card 1 check, h0_max (the longest MST edge as a share of the total, on 1/p_sym), has stability 0.56 and R^2 0.24, and is a weaker reading of the same bottleneck.

| check | value |
|---|---|
| stability | **0.772** |
| R^2 on baselines | **0.178** |
| largest baseline rho | range +0.27, n_pitch +0.21, ln_notes −0.16 |
| rho with g / Cheeger h / h0_max | −0.38 / −0.38 / −0.18 |
| g: stability, R^2 | 0.823, 0.655 (renamed) |

---

**Overlap.** The three measures are nearly orthogonal (Spearman). SLG and TSG: −0.20. SLG and CUT_AB: −0.16. TSG and CUT_AB: 0.00. They can enter one K without double counting.
