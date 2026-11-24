# Card 1: Amiot, "The Torii of Phases"

## 1. Citation and copy read
Emmanuel Amiot, "The Torii of Phases." Published in *Mathematics and Computation in Music* (MCM 2013, LNCS 7937, Springer). Preprint arXiv:1208.4774, math.HO, submitted 23 Aug 2012.
Copy read: https://arxiv.org/html/1208.4774. This is v1, the only version on arXiv. I read the whole text: all sections, footnotes, thanks and references. The HTML header carries an older date line (21 May 2009). The acknowledgments thank Music Theory Online reviewers for an earlier draft, so the LNCS text may differ slightly from this one. I did not check the abs page or the PDF against the published version.

## 2. Construction and results
- **DFT.** A pc-set A ⊂ Z_12 is treated as its 0/1 indicator. Its coefficients are a_k = Σ_x A(x) e^{-2πikx/12}. Any real-valued distribution works the same way. Since a_{12-k} = conj(a_k) (Lemma 1, stated without proof), only k = 0..6 carry information.
- **Phase.** φ_k = arg a_k, taken mod 2π. It is undefined when a_k = 0.
- **Lemma 2 (proved, one line).** Transposing by t multiplies a_k by e^{-2πikt/12}. The magnitude stays the same and φ_k shifts by -2πkt/12. On the torus this means φ_3 moves by -πt/2 and φ_5 by -5πt/6. Inversion A → -A conjugates every a_k, so every phase flips sign.
- **Theorem 1 (cited from Amiot 2007, not proved here).** Two sets have equal |a_k| for all k exactly when they have the same interval content (this includes Z-related pairs). So magnitudes encode chord quality, and phases encode which transposition you have, i.e. harmony.
- **The 3-5 torus (Definition 1).** All 24 major and minor triads have identical magnitudes (|a_3| = √5, |a_5| = √(2+√3) ≈ 1.932). They therefore differ only in phase, and each sits at a point (φ_3, φ_5) on the flat torus T² = (R/2πZ)². The paper tabulates all 24 points.
- **Distance.** Flat-torus geodesic: d = sqrt(Δφ_3² + Δφ_5²), with each Δ wrapped into (-π, π]. Example from the paper: Cm to D is 3.26. The paper also offers a stretched variant d = ‖(0.7365·Δφ_5, Δφ_3)‖ that makes the three P, L and R neighbours equidistant. The 0.7365 factor is stated without derivation.
- **Tonnetz (shown numerically, not proved).** C major's nearest triads are Am (1.065), Cm (1.229) and Em (1.229), which are its R, P and L neighbours. Next come F (1.656) and Fm (1.824). Amiot reads this layout as the dual Tonnetz. He calls the match between phase-closeness and parsimonious voice leading "more than a coincidence, but less than mandatory." A Callender example shows chords that are close in voice leading but far apart in phase.
- **Gestures (illustrated).** Letting t vary continuously traces a closed geodesic through all 12 major (or minor) triads. Over one full octave it winds 3 times around φ_3 and 5 times around φ_5. Points in between are not pc-sets but real-valued distributions (one fractional point lies near F minor).
- **Theorem 2 (cited, sketch only).** Same interval content holds exactly when 1̂_B = 1̂_A·û, with |û(k)| = 1 for all k ("spectral units"). Their k-th roots split an inversion into fractional moves (illustrated only).
- **Zero coefficients.** For the augmented triad, a_3 = 3 but a_5 = 0. Amiot lets the undefined φ_5 take every value, so each augmented triad becomes a circle; this circle works as a free connector between triads and recovers Douthett and Steinbach's Cube Dance. The diminished triad has no zero coefficients, so it is a point; diminished triads trace a line lying between the major and minor lines. The diminished seventh has a_3 = a_5 = 0 and would cover the whole torus, so for Schumann's "Bittendes Kind" the paper switches to the (φ_4, φ_5) torus.
- **Status.** Only Lemma 2 is proved in the text. Everything else is cited, computed, or shown in figures (Plotkin's chord sequence; the 7 diatonic triads making a small winding path).

## 3. Measure from the notes?
Yes. Every quantity is a deterministic function of the pitch-class content. There is no audio, listener data or popularity data.

## 4. Effect size / how checked
This is pure mathematics plus illustration. There are no statistics and no corpus. The theorems are proved or cited, and the musical claims rest on worked examples (one Schumann passage, a few textbook progressions) and the author's own hearing. Amiot himself calls for testing on larger corpora as future work.

## 5. Relevance to songs that last and get covered
Nothing on popularity. **Extrapolation:** the torus is a key-free geometry where Tonnetz-smooth progressions take short steps. If covered songs balance familiarity and surprise, step-length mean, variance and rare long jumps are candidate predictors (cf. the odd Schumann chord lying far from its neighbours).

## 6. Recipes for tonight
Input: chords as pc-sets (root plus intervals), melody pcs with durations, and the key.
1. **Chord point.** Compute a_3 and a_5 with the sign convention above, then P_i = (arg a_3, arg a_5). Use `numpy.angle` and the 0/1 indicator; doublings are ignored unless you weight by duration.
2. **Step length.** s_i = sqrt(w(φ3_{i+1}-φ3_i)² + w(φ5_{i+1}-φ5_i)²), where w(x) = ((x+π) mod 2π) - π. Features: mean, SD, max, and the share of steps under 1.25 (a P/L/R move). Optionally use the 0.7365 weight on φ_5.
3. **Winding numbers.** Unwrap each coordinate by summing the wrapped steps, then W_k = (Σ Δφ_k)/2π. Because of the wrap, a step of exactly ±π is ambiguous; this happens for φ_3 under a tritone root move. Flag such steps rather than resolving them.
4. **Signed area.** Using the unwrapped path, A = ½ Σ (φ3_i·Δφ5_i − φ5_i·Δφ3_i). Add a closing step back to the first chord so the result does not depend on the origin.
5. **Distance to centre.** Build the song profile by weighting each chord's pcs by its duration (the melody can be added the same way). Take the profile's (φ_3, φ_5) and average the chords' torus distance to it. Using the key's scale vector instead needs the key. Caution: for a diatonic scale |a_3| = 1 is weak, so its φ_3 is unstable. Weighting Δφ_k by |a_k| is safer.
6. **Magnitudes.** Report |a_5|/a_0 of the song profile (diatonicity; 1 for a single pc, 3.732/7 for the diatonic scale) and |a_3|/a_0 (pull towards the augmented, or hexatonic, axis). These are fully transposition-invariant.
7. **Undefined phases.** If |a_k| < 1e-9·a_0 (augmented triad: a_5; diminished seventh: both; any single chord whose coefficient vanishes), mark that coordinate missing. In step lengths, either use only the defined coordinate (the circle reading, distance = |Δφ_3|) or drop the step and count it separately. Never use the arbitrary angle numpy returns.
- **Invariance.** Transposition adds the same constant to every phase. So step lengths, windings, area, distance-to-own-profile and magnitudes are all transposition-invariant and need no key. Raw chord positions and distance to the tonic are not. Inversion flips the sign of windings and area but leaves lengths unchanged.

**Worked example** (python, matching the paper's table):

| Chord | φ_3 | φ_5 |
|---|---|---|
| C | 0.464 | 0.785 |
| G | 2.034 | 1.309 |
| Am | -0.464 | 1.309 |

d(C, G) = 1.656, the same as d(C, F); d(C, Am) = 1.065; d(C, Cm) = d(C, Em) = 1.229.
Other values: augmented C has a_3 = 3 and a_5 = 0; C diminished sits at (π/2, -π/2); the C diatonic profile sits at (0, π/3).

## 7. Leads
1. **Tymoczko, D. (2008).** "Set-Class Similarity, Voice Leading, and the Fourier Transform." *JMT* 52(2). Explains how Fourier magnitudes relate to voice-leading distance; useful for justifying the |a_k| features.
2. **Quinn, I. (2006–07).** "General Equal-Tempered Harmony." *Perspectives of New Music* 44(2)/45(1); the card's source lists it as *JMT*. The origin of the Fourier chord-quality "landscape" (diatonicity |a_5|).
3. **Callender, C. (2007).** "Continuous Harmonic Spaces." *JMT* 51(2). Fourier spaces for real-valued and weighted pc distributions, which suits duration-weighted chord profiles.
4. **Douthett, J. & Steinbach, P. (1998).** "Parsimonious Graphs." *JMT* 42(2). Cube Dance and other parsimonious graphs, a discrete check on the torus distances.
5. **Hoffman, J. (2008).** "On Pitch-Class Set Cartography: Relations between Voice-Leading Spaces and Fourier Spaces." *JMT* 52(2). Where phase-space distance and voice-leading distance agree or diverge.
