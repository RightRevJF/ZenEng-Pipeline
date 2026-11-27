# Card 1: Chevyrev & Kormilitzin, "A Primer on the Signature Method in Machine Learning"

## 1. Citation and copy read
Chevyrev, I. & Kormilitzin, A. *A Primer on the Signature Method in Machine Learning.* arXiv:1603.03788. **Read: v2 HTML (https://arxiv.org/html/1603.03788v2), stamped "arXiv:1603.03788v2 [stat.ML] 17 Jan 2025".** I read all of it in ten passes: §1 theory (1.1–1.5), §2 applications (2.1–2.3) and the full bibliography (81 refs). The paper has no appendices. Category: stat.ML (primary). I could not see any cross-lists. **Not reached:** the abs page's "Submission history" and "Subjects" lines. WebFetch served the paper body for that URL. The v1 date is only inferred from the ID (March 2016). I checked that the v1 HTML exists (older structure) but did not read it.

## 2. Main construction and theorems
- **Path and signature.** For a piecewise-smooth path X:[a,b]→ℝ^d, the signature is the infinite list of iterated integrals S^{i1…ik} = ∫_{a<t1<…<tk<b} dX^{i1}…dX^{ik}, one for each word in the letters {1..d}, with S^∅ = 1. The authors call it "a natural generalization of polynomials" to paths.
- **Level 1** is the increment X_b − X_a (d numbers). **Level 2** has d² numbers. The diagonal terms are S^{ii} = (ΔX^i)²/2, so they are redundant. The off-diagonal terms carry the geometry.
- **Lévy area** A = ½(S^{12} − S^{21}) is the signed area between the path and the straight chord joining its endpoints. Counter-clockwise loops count positive and clockwise loops negative. Moves where both channels go up together give a positive contribution, and opposite moves a negative one. The sum S^{12} + S^{21} = S^1·S^2 is the area of the increment rectangle (a shuffle identity).
- **Chen's identity (Thms 1.2/1.3).** The signature of a concatenated path is the tensor product of the pieces' signatures. **Corollary 1:** for a piecewise-linear path, S = exp(Δ1) ⊗ … ⊗ exp(Δn).
- **Shuffle product (Thm 1.1, Ree).** A product of two signature terms is a sum of higher terms. This means polynomials in signature terms are linear in the signature, which is the basis of universal approximation (Prop. 2, via Stone–Weierstrass).
- **Time-reversal (Thm 1.4).** S(X)⊗S(reversed X) = 1. Retracing a path cancels it.
- **Invariances.** The signature is invariant to translation and to reparametrisation (time-warping). This is proved by a change of variables. It is **blind to speed**: it ignores durations unless time is added as a channel.
- **Uniqueness.** The paper states, without proving it here (Hambly–Lyons for bounded-variation paths; Boedihardjo et al. for rough paths), that S(X) = S(Y) exactly when X and Y are tree-like equivalent. In other words, the signature loses only parametrisation and back-tracked excursions. Prop. 1 is proved: if the first coordinate is time (strictly monotone), the signature determines the path.
- **Factorial decay.** Level-k terms are bounded by C^k/k! (left as an exercise, Eq. 11). Low levels therefore carry most of the information, and the series behind the Picard/CDE motivation converges.
- **Log-signature (Def. 6, Thm 1.5 stated without proof).** log S is a Lie series that holds the same information with no redundancy. Its level-2 coefficient is the Lévy area, and its level-3 terms are "areas of areas".
- **Transforms (§2.1).** Interpolation (linear or rectilinear), cumulative sum, base-point, time-augmentation (area against time relates to the mean) and lead-lag, which doubles the points (lead 1,3,3,8,8,6,6; lag 1,1,3,3,8,8,6). **Its Lévy area is half the quadratic variation** Σ(ΔX)² in magnitude, with the sign set by channel order: 16.5 for {1,3,8,6}. LL∘BP∘CS yields the variance.
- **Level-2 for points p0…pn in 2D** (my derivation from Cor. 1; it reproduces the paper's example). Let Δ_k = p_k − p_{k−1} and x̃ = x − x0, ỹ = y − y0. Then:
  - S^{ij} = Σ_k [ (p_{k−1}^i − p_0^i)·Δ_k^j + ½ Δ_k^i Δ_k^j ]
  - A = ½ Σ_k (x̃_{k−1}·ỹ_k − x̃_k·ỹ_{k−1}). This is the shoelace formula for the polygon closed by its chord.
- **Worked check (Eq. 37–39).** For x = 0..5, y = 8,4,5,1,10,3 the paper gives S = (1, 5, −5, 12.5, −10.5, −14.5, 12.5) and A = 2. My code reproduces these values.

## 3. Is the measure from the notes?
No, the method is generic: any ordered sequence of vectors becomes a path. A chord chart becomes a path once you embed each chord as a point. Options are the root on the circle of fifths as (cos, sin), the DFT coefficients of the 12-bit pitch-class set, or a scalar tension value. Successive chords are then joined by straight segments, with durations optionally added as a time channel. Every choice here is ours, not the paper's.

## 4. Effect sizes / how checked
Mathematics: the shuffle identity, Chen's identity, reparametrisation invariance, time-reversal and Props 1–2 are proved. Factorial decay is set as an exercise. Uniqueness up to tree-like equivalence, Thm 1.5 and the moment-problem results are cited, not proved. The assumptions are bounded variation or piecewise smoothness, and compact path sets for approximation. Empirical content is one demonstration: pen-digit data (UCI; 8 resampled (x, y) points per digit) with level-2 signatures (7 features). The results are qualitative only: scatter plots separate '0' from '8' by enclosed area, and a UMAP plot clusters the digits. **No accuracy, held-out test or effect size is reported.** The §2.3 application survey is citation only.

## 5. Lasting love and covers
The paper says nothing about music popularity, longevity or covers, and its bibliography contains no music papers except sound compression (Lyons & Sidorova 2005). *Extrapolation (mine):* the shuffle and approximation results suggest that low-level signature terms form a complete, ordered basis of features, so any order-dependent harmonic property that predicts covers should be approximable by a linear model on a truncated signature. Factorial decay suggests levels 2–3 suffice for short charts.

## 6. Methods or measures for this pass's experiments
General notes:
- Because of reparametrisation invariance, the signature ignores durations and repeated consecutive chords, which matches (e). Durations enter only through a time channel.
- Transposition rotates (cos, sin)-type embeddings. Lévy area is a determinant and survives rotation, so planar areas are key-invariant.
- Normalise time to [0,1] so that tempo drops out.

**M1. Pitch-set fifths-plane area.** z_k = F5(chord) = Σ_{p∈set} e^{−2πi·5p/12}, and the path is (Re z, Im z). The measure is A per chord, using the shoelace formula above.
- *Music:* whether the full chord content (not just the root) turns consistently flatward or sharpward around the fifths circle.
- *Invariance:* key yes (transposition rotates z by 5t·30°). Tempo yes.
- *Risk:* **High for chirality (c).** The root-only version equals the origin-swept area minus the triangle (origin, first chord, last chord). It is therefore chirality minus a term that reads only the endpoints (cf. a). Report its partial correlation with chirality, or skip it if r > 0.9.

**M2. Third-cycle × fifth-cycle coupling.** φ3 and φ5 are the phases of F3 and F5. Unwrap each step to (−π, π], use the path (φ3, φ5), and take A per chord. Skip chords where |F| = 0, such as augmented triads for F3 (or carry the previous phase).
- *Music:* whether moves along the major-third axis (mediants, Coltrane-type moves, tritone substitutes) happen before or after moves along the fifths. It is a lead-lag between two harmonic dimensions.
- *Invariance:* key yes (transposition translates both phases). Tempo yes.
- *Risk:* moderate. It is new relative to (b)–(e) but may track chord-vocabulary richness. Control for the number of distinct chords.

**M3. Harmonic arch (time-augmented).** τ = cumulative duration / total duration, and u = the unwrapped root position in fifths relative to the first chord. Each step is the shortest move in −5..+6 fifths. The measure is A of (τ, u): the area between the root trajectory and the straight first-to-last line.
- *Music:* whether the tune travels away from home and back in the middle, such as the bridge to a distant key, and in which direction.
- *Invariance:* key yes. Tempo yes. It is sensitive to harmonic rhythm.
- *Risk:* it integrates the interior, unlike the downhill measures in (a), but must be checked against them. Drift by ii-V chains may echo (d).

**M4. Tension roughness and tension arch.** Use a key-invariant scalar per chord: h_k = 1 − |F5(set)|/|set|, so tightly fifth-stacked chords score low.
- (i) Lead-lag area = ½ Σ (Δh)² per chord change.
- (ii) Time-augmented area of (τ, h), which is positive if tension bulges mid-song.
- *Invariance:* key yes, because |F_k| is transposition-invariant. Tempo yes.
- *Risk:* (i) is quadratic variation, and with zero repetition it mostly scales with the number of chord changes and the vocabulary (b). Normalise per change. (ii) is cleaner.

**M5. Root–quality ordering.** The path is (u_k, q_k), where q = +1 for a major third over the root, −1 for a minor third, and 0 for neither (all read from the 12-bit set). The measure is A per chord.
- *Music:* whether quality changes lead or follow root motion. m7→7 a fourth up contributes a fixed signed unit, so this generalises the ii-V pattern to any root–quality ordering.
- *Invariance:* key yes. Tempo yes.
- *Risk:* **High for the ii-V share (d).** Test its incremental validity over ii-V share, not alone.

Code sketch:
```python
x, y = P[:, 0] - P[0, 0], P[:, 1] - P[0, 1]
A = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])
```
Libraries: iisignature, esig, signatory. A level-3 log-signature of the M1/M2 paths is a cheap extension.

## 7. Leads
1. Morrill, Fermanian, Kidger & Lyons, "A generalised signature method for multivariate time series", arXiv:2006.00873. It tests which augmentations and normalisations actually help.
2. Király & Oberhauser, "Kernels for sequentially ordered data", JMLR 2019, arXiv:1601.08169 (the ID is from memory, not the bibliography). A signature kernel would let us compare whole songs.
3. Reizenstein, "Calculation of iterated-integral signatures and log signatures", arXiv:1712.02757. It covers practical computation and log-signature bases.
4. Hambly & Lyons, "Uniqueness for the signature of a path of bounded variation", Ann. Math. 2010, DOI 10.4007/annals.2010.171.109 (DOI from memory). It shows exactly what information about a chord path is lost.
5. Diehl & Schmitz, "Two-parameter sums signatures and corresponding quasisymmetric functions", arXiv:2210.14247. It is a signature analogue of time-warping alignment for comparing a standard with its covers.
