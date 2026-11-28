# Run 10 brainstorm: rounds 1 and 2 assembled

27 November 2026, the 18:17 ET pass (TheSession.org tunes, melody only). Assembled by the chair before any outcome was joined; the
seven files below are reproduced in full and in order (round 1: Geometer, Listener, Inventor; round 2: Skeptic, Geometer, Listener,
Inventor). **Where the four agreed:** every measure is read from the notes with nothing fitted, and every one passed the 0.5 stability bar
between two settings; the beat skeleton (card 2's conserved strong beats) is the right place for transition-graph measures, because it cut
renaming sharply; Jason's S belongs in the count once, in the Geometer's skeleton form (G10-3), while the full-surface spectral gaps
(the Inventor's GAP and the Listener's g, ρ 0.97 with each other and mostly range) become estimates with range, n_pitch and ln_notes frozen;
each measure that leans on a simplicity baseline gets that baseline frozen (n_pc for irr_skel and S_gap, pc_entropy for pe_h0 and core_ic,
bar_rep and ln_notes for slg, n_bars and ln_notes for cut_ab, range and n_pitch for ARCH_PE); a replication of McBride & Leroi's
pc_entropy effect (REP) is counted first so that the nulls can be read; and a first-poster fixed effect is wanted as an uncounted reading.
**Where they split:** the Skeptic judged the Listener's TSG to be mostly off-beat surprisal (where transcribers differ) and had core_ic
counted instead, which the Listener accepted, turning "balance of expectation and surprise" into card 2's typicality test; the Skeptic
called LOCK's dancing mechanism the weakest, and the Inventor answered that it needs only card 2's conserved beats, so LOCK stays as
written; the Geometer's extra kill for pe_h0 (the 1/p reading's sign) was dropped as one test counted twice; the Listener and the Skeptic
disagreed in emphasis on whether "second half" reads form for cut_ab (dilution, the Listener; confound, the Skeptic), settled by freezing
n_bars and ln_notes and adding a strict-AABB subset. The Skeptic proposed K = 9; the chair's selection, gates and order are in chair.md.

---

<!-- round1_geometer.md, full text -->

# Run 10, round 1: the Geometer

27 November 2026, the 18:17 ET pass. Notes only. I opened no outcome: I did not call `common10.load_outcomes`, and I did not open recordings.csv, tune_popularity.csv, data/*.json or any covers/versions/HOLDOUT file. All checks used split A, subsampled to 3,000 tunes (seed 10). Stability uses `common10.stability` on the first 3,000 split-A tunes that have a second setting. Code: `/home/claude/scripts/geometer/measures_geometer.py` (`measure(t) -> dict`, for the chair to freeze), with the checks in `checks_final.py`, `cand.py`, `cand2.py` and `fiedler.py` in the same folder. Total compute was about 4 minutes.

**Shared choice: the skeleton.** All three measures read the **beat skeleton**: the notes whose onset falls on a beat of the meter (beatpos an integer), taken in order. Card 2 found strong beats conserved across settings and variation piling up on weak beats. Using the skeleton changed stability little but cut renaming a lot. For the spectral gap, R² on the baselines fell from 0.56 (full surface) to 0.15; for tree reduction, from 0.19 to 0.07.

## G10-1: Weak links, the persistent entropy of the H0 barcode (card 1, M4)

1. **Mechanism.** H0 of the Vietoris-Rips filtration on a shortest-path metric is exactly the minimum spanning tree. Its finite bars are the lengths of the links that hold the tune's pitch vocabulary together, and their evenness says whether every pitch is bound to the tune by a habitual move or some hang by a rare thread.
2. **Measure.**
   - Nodes: the skeleton's distinct MIDI pitches. c(a,b) counts steps from a to b.
   - p_sym = (c + cᵀ)/total, with self-loops dropped.
   - Length = −ln p_sym, the transition's surprisal. I use this rather than card 1's 1/p because the card itself warns that 1/p is unbounded. 1/p is kept as the reading `pe_h0_inv`.
   - l_i = the MST edge lengths, which are the finite H0 bars; the infinite bar is dropped.
   - **pe_h0 = −Σ qᵢ ln qᵢ / ln(#bars)**, with qᵢ = lᵢ/Σl.
   - Nothing is fitted. It is invariant to transposition and to the overall count scale.
3. **Data.** TheSession split A (about 14,500 tunes), the first setting.
4. **Prediction.** **+0.03 SD of z(y_cov) per SD**, and positive for y_love.
   - What the mathematics says: a low-evenness tune has a few long bars, meaning pitches reached only by rare moves.
   - Card 2: rare pitches mutate most. So such a tune is the one that drifts or breaks when passed on.
   - *Extrapolation:* a uniformly knit skeleton travels intact between players, and intact travel is what lets a tune be learned and recorded.
5. **Kill.** +0.03 lies outside the 95% range (R07-3). The mechanism is also dead if the card's literal 1/p reading takes the opposite sign.

## G10-2: Retracing, the tree reduction of the skeleton walk (IRR revived on melody)

1. **Mechanism.** Free reduction deletes every back-track (x y x → x). A walk on a tree reduces to its geodesic, so what survives is the walk's word in the fundamental group of its own transition graph: how much the skeleton circulates round the graph's H1 loops instead of coming back the way it went. This is the same invariance as the path signature's uniqueness up to tree-like pieces.
2. **Measure.**
   - Take the skeleton and merge repeated pitches, giving length m.
   - Stack-reduce, giving length k.
   - **irr_skel = (k − 1)/(m − 1)**.
   - No parameters.
3. **Data.** As for G10-1.
4. **Prediction.** **−0.03 per SD** for y_cov, and negative for y_love.
   - Run 09 found the opposite of its prediction on chords: back-and-forth went with more covers (−0.060, a lead).
   - A melody whose way back is its way out (scale up then down, arpeggio up then down, neighbour notes) halves what must be remembered.
   - *Extrapolation:* that makes the tune easier to learn by ear.
5. **Kill.** −0.03 lies outside the 95% range. A positive estimate whose range excludes −0.03 would also show that run 09's chord lead does not transfer to melody.

## G10-3: Jason's S = 1 + g/π, a Cheeger bottleneck of the implied harmony

1. **Mechanism.** g = 1 − λ₂ of the random walk on the skeleton's pitch-class graph. Cheeger's inequality gives g/2 ≤ h ≤ √(2g), where h is the conductance of the best two-way cut.
   - The cut is mostly harmonic. On 1,000 major-mode tunes the Fiedler cut most often splits the tonic triad {1,3,5} from {2,4,6,7}, and the other common cuts are also chord regions.
   - So a small g means the skeleton dwells in one chord region before crossing: a slow, legible implied harmony.
2. **Measure.**
   - W = c + cᵀ on the skeleton's pitch classes, with self-loops kept.
   - λ₂ = the second-largest eigenvalue of D^−½ W D^−½.
   - **S_gap = 1 + (1 − λ₂)/π**.
   - No parameters.
3. **Data.** As for G10-1.
4. **Prediction.** **−0.03 per SD** of S for y_cov, and negative for y_love.
   - *Extrapolation:* a tune whose melody spells out a clear two-region harmony is easy for accompanists and learners to grasp.
   - Never powered before: run 07's chord version had power 0.01.
5. **Kill.** −0.03 lies outside the 95% range. If the sign is right but the effect vanishes once n_pc and pc_entropy are held (a reading), it was renaming.

## Measure-side checks (split A, 3,000 tunes)

| Measure | Stability (Spearman between two settings, n = 3,000) | Within reel / jig / polka / hornpipe | R² on the 13 baselines | R² on baselines plus type | Largest baseline ρ |
|---|---|---|---|---|---|
| pe_h0 (G10-1) | **0.679** | 0.66 / 0.66 / 0.69 / 0.71 | **0.141** | 0.145 | pc_entropy +0.25, n_pitch +0.20 |
| pe_h0_inv (card's 1/p reading) | 0.591 | 0.54 / 0.59 / 0.58 / 0.58 | 0.093 | 0.103 | ln_notes −0.13 |
| irr_skel (G10-2) | **0.762** | 0.72 / 0.81 / 0.78 / 0.75 | **0.071** | 0.091 | pc_entropy +0.17, n_pitch +0.14 |
| S_gap (G10-3) | **0.755** | 0.75 / 0.79 / 0.77 / 0.70 | **0.145** | 0.155 | pc_entropy −0.22, n_pc −0.19 |

The within-type columns used 600, 600, 466 and 444 tunes respectively.

**Overlap among the three measures (Spearman).**
- pe_h0 with irr_skel: 0.37.
- pe_h0 with S_gap: 0.01.
- irr_skel with S_gap: 0.05.

So the three are nearly separate. All pass the stability bar of 0.5 (R09-5) and stay well below renaming.

**Reserves I checked but did not propose:**
- **Rips H1 count on the skeleton (card 1, M2):** stability 0.62, R² 0.18. Its Spearman with the cycle rank is only 0.28, so here the topology is not just the count of cycles.
- **Circular transport on the fifths circle between the tune's first and second halves:** stability 0.67, R² 0.13.
- **Full-surface spectral gap:** stability 0.82, but R² 0.64 (range and n_pitch); it renames.
- **The 1/p metric (card 1's literal choice):** it is the least stable variant, as the card warned.

---

<!-- round1_listener.md, full text -->

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

---

<!-- round1_inventor.md, full text -->

# Run 10, round 1: the Inventor

27 November 2026. Notes only. I opened no outcome, called no outcome loader, and read no recordings, popularity, data/*.json or HOLDOUT file. Code is in `/home/claude/scripts/inventor/` (`measures_inventor.py` has `measure(t) -> dict`; the checks are in `checks.py`, `gapn.py` and `gapres.py`). Every measure is computed on `mel`, with no fitted settings.

## Proposals

**R10-I1. ARCH: the statue's arches (persistent entropy of the contour barcode; card 1's persistent entropy, card 1's lead 3, and the stability theorem of Cohen-Steiner, Edelsbrunner and Harer, 2007).**
- **Mechanism.** Treat the melody as a function: pitch against note order, with repeated pitches merged. Its sublevel and superlevel H0 barcode pairs every valley with a ridge, so each bar is one arch of the contour, of a given height.
- **Measure.** ARCH_PE is the persistent entropy of all finite bars, divided by log(number of bars).
- **What the mathematics predicts.** The stability theorem says a change of size e moves every bar by at most e. A step-sized ornament or variant therefore only adds or moves short bars, and the long bars are the part that survives transmission (card 2's skeleton). A low ARCH_PE means a few big arches carry the shape: a statue rather than a texture.
- **Prediction (extrapolation).** −0.03 SD of z(y_cov) per SD. y_love is also expected negative.
- **Kill.** −0.03 lies outside the 95% range.

**R10-I2. LOCK: the dancer's footfall (biomechanics; card 2's conservation gradient).**
- **Mechanism.** Where the melody turns, a dancer feels the step. If those turns sit on beats, which are the slots card 2 finds most conserved, the tune's shape lives where transmission protects it.
- **Measure.** LOCK = P(on a beat | contour turning point) − P(on a beat | any note-run start). A turning point is a strict local maximum or minimum after repeated pitches are merged. A note is on a beat when its beatpos is a whole number.
- **Prediction (extrapolation).** +0.03. y_love is also expected positive.
- **Kill.** +0.03 lies outside the 95% range.

**R10-I3. GAP: two rooms and a doorway (Jason's S = 1 + g/pi, never tested on melodies before; Cheeger's inequality).**
- **Mechanism.** Build the graph of transitions between octave-distinct pitches. It is cyclic (last note to first, because a dance tune goes round), symmetrised, and counts self-loops. Its gap g is λ2 of the normalised Laplacian.
- **What the theorem says.** Cheeger's inequality, g/2 ≤ h ≤ √(2g), means a small g forces a cut that the melody rarely crosses.
- **What the cut is.** In 88% of tunes the Fiedler vector orders the pitches by height, |ρ| ≥ 0.8. So the cut is a register cut: a low room and a high room, as in an Irish A part and its high B part.
- **Prediction (extrapolation, from architecture).** A legible two-room plan is remembered and taken up: −0.03 per SD of g (S is monotone in g). y_love is also expected negative. The test holds range, n_pitch and ln_notes as frozen extra controls.
- **Kill.** −0.03 lies outside the 95% range.

## Measure-side checks (split A)

Stability uses `common10.stability`: the first 3,000 tunes that have a second setting. Renaming uses `common10.renaming` on a random 3,000 tunes (seed 10). The checks took about 1.5 minutes of compute.

| measure | stability ρ (n = 3,000) | R² on the 13 baselines | largest baseline ρ | after removing baselines: stability |
|---|---|---|---|---|
| ARCH_PE | **0.80** | 0.35 | range −0.33, n_pitch −0.32, step_share −0.32 | 0.75 |
| LOCK | **0.74** | **0.01** | pc_entropy +0.08 | (≈0.74) |
| GAP (S) | **0.82** | 0.65 | range −0.59, n_pitch −0.54, leap_share +0.39 | 0.68 (0.77 after range, n_pitch, ln_notes only; R² 0.35) |

All three pass the 0.5 bar. The three measures are nearly independent of each other: ρ is −0.03 for LOCK with ARCH_PE, −0.02 for LOCK with GAP, and +0.43 for ARCH_PE with GAP.

## Notes

- **Rejected readings.** These were rejected on the notes alone; no outcome was seen.
  - ARCH_TOP, the share held by the longest bar: R² 0.79, mostly ln_notes.
  - GAP on pitch classes: stability 0.75, R² 0.55.
  - GAP divided by the gap of a k-node path: R² 0.63, which only moves the renaming from range onto n_int and int_entropy.
- **Canalisation, a descriptive check.** ARCH_PE on the on-beat skeleton agrees with ARCH_PE on the full surface only at ρ = 0.42. The stability theorem protects the long bars, not their entropy, because ornaments add many short bars. If ARCH dies, the next form to try is bottleneck distance on the long bars only.
- **LOCK by type.** LOCK is positive in every type, with a mean of about 0.04 to 0.09 (slides highest). Turning points favour beats everywhere, so the type fixed effect matters.
- **GAP renaming.** GAP is the most renamed of the three. It is worth a counted test only with its extra controls frozen; otherwise it is mostly range.

---

<!-- round2_skeptic.md, full text -->

# Run 10, round 2: the Skeptic

No outcome opened. Check: `/home/claude/scripts/skeptic/xcheck.py` (1,500 split-A tunes).

**General.** Year, type, meter and mode are fixed effects. The live confounds are simplicity (McBride & Leroi), length and form, and the first poster's notation of weak beats. Where a measure leans on n_pc or pc_entropy in simplicity's direction, freeze that baseline. tunes.csv has `username`: run a first-poster fixed effect as an uncounted reading for surface measures. y_love (10+ tunebooks only) has power below 0.6.

**Duplicates.** Inventor GAP and Listener g: rho 0.97, both mostly range (R² 0.65). Geometer S_gap (skeleton pitch classes) is distinct (|rho| < 0.3, R² 0.15). **Count G10-3 as the one S**, n_pc frozen (rho −0.22). R10-I3 and L3's g become estimates with range, n_pitch and ln_notes frozen.

**Each proposal.**
- **G10-1 pe_h0 (+).** Clean (R² 0.14); simplicity pushes the other way (pc_entropy +0.25). Drop the "1/p opposite sign" kill: rho 0.87 makes it one test.
- **G10-2 irr_skel (−).** Clean (R² 0.07), but n_pc +0.13 aligns with "simpler spreads": freeze n_pc.
- **L1 SLG (+).** Partly repetition and length (bar_rep +0.34, ln_notes +0.32). Count only with both frozen.
- **L2 TSG (−).** Mostly minus surf_ic (rho −0.76), and off-beat surprisal is where transcribers differ (card 2). **Count core_ic (−) instead**, pc_entropy frozen (n_pc +0.27, simplicity's direction): card 2's typicality test. TSG becomes an estimate.
- **L3 CUT_AB (+).** Reads form: rho −0.21 with written bars, −0.16 with ln_notes; "second half" differs between two- and three-part tunes. Freeze n_bars and ln_notes; report strict-AABB reels and jigs separately.
- **R10-I1 ARCH_PE (−).** Renamed by range, n_pitch and step_share (R² 0.35); rho 0.42 with GAP; written-out ornaments add short bars. Freeze range and n_pitch; add the poster reading.
- **R10-I2 LOCK (+).** Cleanest (R² 0.01). Weakest mechanism: rarely danced to. Count as written.

**Proposed K = 9:** pe_h0, irr_skel, S_gap, SLG, core_ic, CUT_AB, ARCH_PE, LOCK, REP. Each must clear the 0.2 power floor with its frozen controls in.

**REP (replication baseline, counted, written first).** z(pc_entropy), McBride & Leroi's own measure, on y_love and y_cov. Predicted **−0.03** (simpler spreads); density (notes per bar) negative as companion. Stability 0.83 (n_pc 0.70).
- REP unsettled at power 0.2 or more: the known effect is invisible on this design, and every null above means little.
- REP passes: any measure correlated with pc_entropy must beat it with pc_entropy frozen.

---

<!-- round2_geometer.md, full text -->

# Run 10, round 2: the Geometer answers the Skeptic

No outcome was opened. The power figures below come from fake outcomes (`common10.power`, 100 draws, α = .05/9) on all 14,511 split-A rows, with the frozen control in the model. Script: `/home/claude/scripts/geometer/power_r2.py`.

- **G10-1 pe_h0: kept.** I accept dropping the 1/p kill: the two versions correlate 0.87, so they are one test, and pe_h0_inv stays as a reading only. Simplicity points the other way here (pc_entropy +0.25 against a predicted +), but I freeze pc_entropy anyway so the result is clean if REP passes. Power with it frozen: 0.72.
- **G10-2 irr_skel: kept.** n_pc is frozen as you ask. Power 0.77.
- **G10-3 S_gap: kept, and counted as the only S.** n_pc is frozen. Power 0.64. pc_entropy goes in as an uncounted reading.
- **First-poster fixed effect:** accepted as an uncounted reading. All three measures use only on-beat notes, which are the ones transcribers agree on most (card 2).
- **No measure was revised.** `measure(t)` is unchanged, and all four keys are finite for all 14,511 tunes.

## Final (to freeze)

| Key | Predicted sign and size on y_cov (SD per SD) | Frozen extra control | Fake power |
|---|---|---|---|
| pe_h0 | **+0.03** (y_love +) | pc_entropy | 0.72 |
| irr_skel | **−0.03** (y_love −) | n_pc | 0.77 |
| S_gap | **−0.03** (y_love −) | n_pc | 0.64 |

pe_h0_inv is a reading only and is not counted.

---

<!-- round2_listener.md, full text -->

# Run 10, round 2: the Listener answers the Skeptic

**L1 SLG: kept, and I accept both frozen controls.** With bar_rep and ln_notes held, a pass means the tune's own grammar matters beyond plain repetition.

**L2: revised.** I accept the Skeptic's point: TSG mostly reads surf_ic (rho −0.76), and off-beat notes are where transcribers differ. **core_ic (−) is counted** with pc_entropy frozen. TSG becomes an estimate. A pass on core_ic says "typical skeleton spreads", which is card 2's typicality reading, not "balance".

**L3 CUT_AB: kept, and I accept n_bars and ln_notes frozen.** Note that n_bars is a `baseline()` key but is not in `BASE`. I add an `aabb` flag for a separate, uncounted report on strict AABB reels and jigs: 16 written bars that expand to 32. That subset is about 12% of tunes, so it has low power. The three-part mismatch is real but it dilutes the effect rather than reversing it. Whatever the halves are, a high CUT_AB still means "register marks the part".

**g / S: estimate only.** I agree with counting G10-3 as the one S.

**REP: agreed.** Since core_ic leans on pc_entropy, it must beat REP with pc_entropy frozen.

## Final keys (`measure(t)` in /home/claude/scripts/listener/measures_listener.py; `FINAL` dict)
| key | status | sign | size (SD of z(y) per SD) | frozen extra controls |
|---|---|---|---|---|
| slg | counted | + | +0.03 (y_cov; y_love +) | bar_rep, ln_notes |
| core_ic | counted | − | −0.03 (y_cov; y_love −) | pc_entropy |
| cut_ab | counted | + | +0.03 (y_cov; y_love +) | n_bars, ln_notes |
| tsg | estimate | − | — | pc_entropy |
| gap (S) | estimate | − | — | range, n_pitch, ln_notes |
| aabb | subset flag for cut_ab report | | | |

---

<!-- round2_inventor.md, full text -->

# Run 10, round 2: the Inventor answers the Skeptic

No outcome was opened. The check is in `/home/claude/scripts/inventor/r2check.py`: 3,000 split-A tunes, seed 10.

- **ARCH_PE: kept unchanged. I accept freezing range and n_pitch.** These two explain only 0.10 of its variance; the full baselines explain 0.35. The confounds run against my prediction. ARCH_PE has ρ −0.32 with both range and n_pitch, and −0.14 with pc_entropy. So "simpler spreads" would push ARCH_PE positive, while I predict negative. Freezing them can only make the test harder. I also accept the first-poster reading, uncounted.
- **LOCK: kept as written.** Its mechanism does not need dancers. It needs only card 2's finding that beats are the conserved slots. The renaming R² is 0.004 on range and n_pitch.
- **GAP: I accept the demotion to an estimate,** with range, n_pitch and ln_notes frozen. G10-3 is the one counted S.
- **REP: I support it as written.**

## Final keys

| key | sign | size (SD of z(y_cov) per SD) | frozen extra controls | status |
|---|---|---|---|---|
| ARCH_PE | − | 0.03 | range, n_pitch | counted |
| LOCK | + | 0.03 | none | counted |
| GAP | − | 0.03 | range, n_pitch, ln_notes | estimate |

y_love is expected to take the same signs.

---
