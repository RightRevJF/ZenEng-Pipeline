# Card 1: Rabin, Delon and Gousseau, "Transportation Distances on the Circle"

## 1. Citation and copy read

- **Journal version:** J. Rabin, J. Delon, Y. Gousseau, "Transportation Distances on the Circle," *Journal of Mathematical Imaging and Vision* 41 (2011), 147-167. The DOI 10.1007/s10851-011-0284-0 is from memory and was not checked against the publisher.
- **Copy read:** arXiv:0906.5499v3 [math.FA], dated 2 June 2010, as the PDF at https://arxiv.org/pdf/0906.5499. This copy is titled "Transportation Distances on the Circle and Applications," lists the authors as Delon, Rabin, Gousseau, and has HAL number 00399832.
- **Coverage:** I read the whole PDF in five passes: abstract, sections 1-5, Appendix A with all proofs, and all 41 references.
- **Not reached:** ar5iv.labs.arxiv.org, ar5iv.org and arxiv.org/html were all blocked because a permission request went unanswered.
- **Caveat:** the published JMIV text may differ from v3. I did not see it.

## 2. Main construction and theorems

**Setting.**
- The circle has perimeter 1, and d is the geodesic (shorter-arc) distance.
- f and g are discrete probability distributions on the circle.
- The cost of moving mass from x to y is h(d(x,y)), with h convex and increasing.
- F is the cumulative distribution of f. It is extended periodically by F(y+1) = F(y) + 1, and F⁻¹ is its pseudo-inverse.

**Theorem 1 (convex costs).**
- The optimal transport cost is MK_c(f,g) = inf over α of ∫₀¹ h(|F⁻¹ − (G − α)⁻¹|).
- In words: cut the circle at a suitable point and solve the problem on the line. On the line the optimal plan is the monotone rearrangement. The free shift α stands for the choice of cut point.

**Wp case.**
- With h(t) = t^λ, the distance is MK_λ = (inf_α ∫|F⁻¹ − (G−α)⁻¹|^λ)^{1/λ}.
- This is a metric for λ ≥ 1, citing Villani.
- For general convex h, it can be computed to precision ε in O((N+M) log 1/ε) time. That result is cited from Delon, Salomon and Sobolevski [DSS10], not proved in this paper.

**W1 closed form.**
- W1(f,g) = inf_α ∫₀¹ |F − G − α|.
- F − G is piecewise constant, so the best α is a **weighted median** of the values of F − G. Each value is weighted by the length of the interval on which it holds.
- This gives an exact O(N) algorithm, citing Cabrelli-Molter 1998 and Gurwitz 1990.

**Histograms with N equal bins (the circular EMD, "CEMD").**
- CEMD = Σ_i |F[i] − G[i] − μ|, where μ is the plain median of the N numbers F[i] − G[i] (Eq. 12).
- An equivalent form is CEMD = min_k ‖F_k − G_k‖₁ (Eq. 13). Here F_k is the cumulative histogram restarted at bin k, so the minimum runs over the N cyclic restarts.

**Proof (Appendix A).**
- Start with P equal point masses. Birkhoff's theorem reduces the problem to choosing a permutation.
- *Lemma 1:* when h is strictly convex, any two optimal paths are either disjoint or overlap in the same direction, and neither contains the other.
- *Proposition 1:* some source point lies on no other optimal path. That point is where the circle can be cut.
- *Corollary 1:* the same holds for convex h that is not strictly convex, by approximating h with strictly convex functions.
- After the cut, the problem is a line problem in the shift α = F(x) − G(x). The objective is continuous, coercive and piecewise affine, so it attains its minimum.
- Continuity then extends the result to coincident points, to rational masses, and to arbitrary masses. Moving mass ε changes the cost by at most ε·h(1/2).

**What the paper does not claim.**
- It makes no uniqueness claim. The figure caption says the cut is "non-necessarily unique".
- It does not state that the objective is convex in α. For λ = 1 this is elementary (a sum of |D_i − α| terms), but that is my observation.
- It has no theorem on locally optimal plans or cyclic shifts. The only cyclic-shift content is the min over k in Eq. 13. Results of that kind, if they exist, would be in [DSS10] (lead 1).
- It does not treat barycentres of several histograms.

**Concave costs (section 2.3).**
- Theorem 1 does not apply, shared mass stays where it is, and no fast general algorithm is known.
- The 0/1 cost gives exactly the L1 distance.
- The truncated cost min(d,2) gives the L1 distance minus a correction that is nonzero only where the two histograms cross.

## 3. Is the measure from the notes?

The measure is generic: it applies to any distribution on a circle. It applies directly to a 12-bin pitch-class distribution:

- **Chromatic circle:** use bin i = pitch class (C=0, C#=1, …).
- **Circle of fifths:** use bin i = 7·pc mod 12 (C, G, D, A, …).
- **Units:** the bins are equally spaced, so the weighted median reduces to the ordinary median of 12 numbers. Multiply by 12 to get distances in semitone steps or fifth steps.
- **Origin of the input:** the distribution is built entirely from the notes, as chord tones weighted by count or by duration. The paper itself never mentions music.

## 4. What is proved, assumed and tested

**Proved:** Theorem 1 for discrete measures with convex increasing h, including the appendix argument.

**Cited, not proved:**
- the metric property (Villani);
- the O(N) median algorithm;
- the ε-approximation complexity for general convex h [DSS10].

**Experiments.** All results are shown as plotted curves, with no numeric tables and no statistical tests.

- **Hue transfer.** The circular map is (H_t − α)⁻¹ ∘ H_u, with α the median of H_u − H_t. The results are judged by looking at the images.
- **SIFT orientation histograms.** The paper only cites [RDG09] for the claim that CEMD handles binning and shift effects better than bin-to-bin distances.
- **Colour retrieval.**
  - Dataset: 126 photos in 14 classes, each a 360-bin hue histogram.
  - Scoring: recall and precision-recall curves.
  - Result: CEMD beats L1 and non-circular EMD.
- **Perturbations of 22 photos.**
  - Under gamma changes, CEMD wins.
  - Under white-balance changes, L1 wins.
- **Synthetic two-class Gaussian mixtures.**
  - Setup: 100 bins, 1,000 histograms per class.
  - When the peaks shift, convex costs win, and larger λ does better.
  - When the peak weights change, concave costs and L1 do better.
  - The authors call this a trade-off and recommend W1 as the compromise.
- **Checking:** class labels serve as ground truth. There is no cross-validation and there are no repeated runs.

## 5. Lasting love and covers

Nothing. The paper is about imaging, and music, listeners and longevity do not appear.

## 6. Methods and measures for this pass

All numbers below come from my own script, run locally: /tmp/claude-0/-home-claude-zeneng-pipeline/2978acbe-3f66-550d-80a2-03607e24a861/scratchpad/cemd.py.
- Each chord tone gets equal weight. Results are in steps of 1 semitone or 1 fifth.
- I checked Eq. 12 against Eq. 13 and against brute force over all permutations. All three agree on every case below.

**(a) Circular W1 between successive chords, chromatic circle.**
1. Turn each chord into a 12-bin probability vector h.
2. Take cumulative sums to get F and G.
3. Compute D = F − G and μ = median(D).
4. W1 = Σ|D − μ|.
5. Summarise each song by the mean, the variance, and the share of zero-cost steps over its chord sequence.

How this differs from Tymoczko's voice-leading:
- For two chords with the same number of equally weighted notes, it equals the minimal L1 voice-leading divided by the number of voices.
- It departs from voice-leading when the chords differ in size, when notes are doubled, or when notes are weighted by duration, because transport can split mass.

**(b) The same on the circle of fifths.** Re-index each chord with i → 7i mod 12 first.

| C major to | chromatic W1 | chromatic W2 | fifths W1 | fifths W2 |
|---|---|---|---|---|
| F {F,A,C} | 1.000 | 1.291 | 1.000 | 1.000 |
| G {G,B,D} | 1.000 | 1.291 | 1.000 | 1.000 |
| Am | 0.667 | 1.155 | 0.667 | 1.155 |
| Db | 1.000 | 1.000 | 3.000 | 3.109 |
| F# | 2.000 | 2.160 | 3.333 | 3.559 |
| G7 (4 notes) | 1.083 | — | 0.917 | — |

How to read the table:
- **F and G:** C to F has each voice moving 0, 1 and 2 semitones, giving 3/3 = 1. On the fifths circle each tone moves one step.
- **Db:** the two circles disagree. Db is a near-neighbour on the chromatic circle but three fifth-steps away on the circle of fifths. Bin-to-bin L1 scores C-F, C-G and C-Db at 0.667, 0.667 and 1.0, so it cannot tell these chords apart.
- **G7:** this is a mass-splitting case, which an ordinary voice-leading count does not cover.

**(c) Sections.**
1. Pool the pitch classes over a section, weighting by duration where the data has it.
2. Compute CEMD between verse and chorus, and between the first and second half of the song.
3. For a transposition-blind version, take the minimum over the 12 rotations of g.
- Example: pooled I-V-vi-IV against pooled ii-V-I-I gives 0.333 on the chromatic circle and 0.167 on the fifths circle.
- The paper's trade-off result suggests reporting L1 alongside W1. W1 picks up modulation-like shifts, while L1 picks up reweighting of the same notes.

**(d) Harmonic centre.**
- W1(h, δ_m) is the h-weighted mean geodesic distance from m.
- Its minimiser is the circular weighted median, which serves as the song's centre. The minimum value is the song's harmonic spread.
- Chord travel is W1(chord, δ_m).
- Example, pooled I-V-vi-IV:
  - Chromatic circle: the median is C, with spread 2.667.
  - Fifths circle: G and D **tie** at 1.667, and C scores 2.0.
  - Chord distances to G on the fifths circle are C 1.33, G 1.67, Am 2.0 and F 1.67.
- Two cautions: the median need not be unique, and it need not be the tonic. Treat it as a measure of dispersion, not as a key-finder.

**(e) Other things the theorems make computable.**
- *Harmonic path length:* the sum of successive W1 values, divided by W1 between the first and last chord.
- *W2 between chords:* W2 penalises large leaps more heavily.
- *The optimal α itself:* the median shift indicates which way the mass rotates.

## 7. Leads

1. J. Delon, J. Salomon, A. Sobolevski, "Fast transport optimization for Monge costs on the circle," *SIAM J. Appl. Math.* 70 (2010). This is the general convex-cost algorithm. The arXiv id I recall, 0902.3527, is unverified.
2. C. Cabrelli, U. Molter, "The Kantorovich metric for probability measures on the circle," *J. Comput. Appl. Math.* 57 (1995) 345-361.
3. O. Pele, M. Werman, "A linear time histogram metric for improved SIFT matching," ECCV 2008. This covers truncated and bin-to-bin alternatives.
4. J. Rabin, J. Delon, Y. Gousseau, "Circular Earth Mover's Distance for the comparison of local features," ICPR 2008.
5. D. Tymoczko, "The geometry of musical chords," *Science* 313 (2006), DOI 10.1126/science.1126287. This is the voice-leading baseline to compare against.
