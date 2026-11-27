# Card 1: Gilbert & Yim, "Hyperbolicity, slimness, and minsize, on average"

## 1. Citation and copy read
Anna C. Gilbert and Joon-Hyeok Yim (Yale), "Hyperbolicity, slimness, and minsize, on average", arXiv:2412.05746v1 [math.PR, math.CO], 7 Dec 2024. The abstract page lists only v1. I read the arXiv HTML (LaTeXML) at https://arxiv.org/html/2412.05746. The rendered text is about 800k characters, mostly MathML, so I read it in 10 passes covering every 100k-character section from start to end, plus one pass on the abstract page. Everything was read: introduction, Sections 2 to 6, the appendix (Section 7) and all 18 references. Two parts came through garbled: Figure 1, a diagram of the implications, and the average-value columns of Table 1. I took those facts from the theorems instead.

## 2. Main construction and theorems
**Objects.** A finite metric space or graph with shortest-path distance d.
- **Gromov product:** ⟨x,y⟩_w = ½[d(x,w)+d(y,w)−d(x,y)].
- **Four-point function:** for x,y,z,w set P=d(x,y)+d(z,w), Q=d(x,z)+d(y,w), R=d(x,w)+d(y,z). Then fp = ½(max − median of P,Q,R). A space is δ-hyperbolic if fp ≤ δ for every quadruple. A tree gives 0.
- **Slimness of a geodesic triangle:** the smallest δ such that every point on one side lies within δ of the other two sides.
- **Thinness:** the same idea, but matching points at equal distance from a vertex.
- **Minsize:** the smallest diameter of a triple of points with one point on each side.
- **Insize:** the diameter of the three "tangent points" fixed by the Gromov products.

**Averages.** Points are drawn i.i.d. from any distribution that gives positive weight to every point. Uniform sampling is not required. E δ_hyp is E[fp] over four i.i.d. points. E ζ_slim, E τ_thin, E ι_insize and E η_minsize are the means over three i.i.d. points. When several shortest paths exist, each side of a triangle is chosen uniformly among them. Remark 3.8 shows why: if you take the best triangle instead, the 4-cycle wrongly looks tree-like.

**What is proved.**
- **Worst case (Theorems 2.7 and 2.8, collected from the literature).** All five notions agree up to constants such as 2, 3 and 4. Graphs add +½.
- **Average case, the direction that holds:**
  - Corollary 3.6: Eζ ≤ Eτ ≤ 4Eζ, and Eη ≤ Eι ≤ 3Eη. Figure 3 shows both constants are tight.
  - Theorem 3.7: E δ_hyp ≤ 2Eζ, E δ_hyp ≤ Eι ≤ Eτ, and E δ_hyp ≤ 2Eη. Graphs add +½ to the first two.
  - The proof bounds fp of one quadruple by the four triangles inside it, then takes expectations.
- **Average case, the direction that fails (Section 4):**
  - Graph G_n (cycle-like paths of length about 2√n joining every pair of n hubs): E δ_hyp → 0, while average slimness and average minsize are about √n. Small average four-point delta does not imply small average slimness.
  - Graph H_{M,n}: average slimness → M while average minsize → 0, so these two can also come apart.
  - Example 4.3: Gaussian points in high dimension have average fp → 0 only because distances concentrate. Euclidean space is not hyperbolic, while slimness and minsize both tend to √2/2.
  - Example 4.4: on three points, fp is identically 0, because any four draws must repeat a point.
- **Random graphs (Section 5):**
  - Random d-regular graphs: average fp = o(ω(n)). The proof needs only the variance of the shortest-path length: E fp ≤ 2·sd(distance), followed by Markov's inequality. Average slimness and minsize are at least ½log_{d−1}n − (3/2)log_{d−1}log_{d−1}n − C_d. Most triangles are therefore fat.
  - Erdős–Rényi graph ER(n, λ/n) with λ ≥ 4.67: average slimness and minsize are Ω(log n), while average fp = o(log n). This answers an open question in the Narayan–Saniee–Tucci paper.
  - Tools: neighbourhood-growth bounds, traffic counting, and a new colour-pigeonhole lemma (Lemma 5.9, proved in the appendix).

**Assumed.** Exact distances, i.i.d. sampling, the i.i.d. random-graph models, and (for ER) λ ≥ 4.67 so the diameter is controlled.

**No algorithm, cost analysis or sampling-size result.** The Discussion notes that the existing tree-fitting bounds (Chatterjee–Sloman; Yim–Gilbert) are loose. It leaves open the case λ near 1 and expanders.

## 3. Is the measure from the notes?
No. This is pure metric geometry and probability, with nothing musical in it. To use it, a song has to become a **finite metric space** (bars as points, with a distance between bar chroma vectors) or a **graph** (bar types as nodes, with edges for observed transitions). Slimness and minsize need geodesics, so they need the graph form.

## 4. Proved versus assumed; empirical content
Every claim is a theorem with a proof. There are no experiments, no data and no simulations. The only data-like part is the Gaussian thought experiment, which comes with a warning that a small average delta on high-dimensional finite data can mislead. Nothing was checked empirically, so nothing needs re-checking.

## 5. Lasting love and covers
Nothing, directly or indirectly. The paper says nothing about music, audiences, popularity or covers. Any link to the yardstick would be our hypothesis, for example that clearly hierarchical forms age well. The paper does not support it.

## 6. Methods and measures for this pass
**Primary score (point-cloud form, no fitted settings).**
- Take the bars of a song whose chroma is not empty and L2-normalise each 12-d chroma vector c_i.
- Use d(i,j) = ‖c_i − c_j‖. This is a true metric. Cosine distance is not a metric, so do not use it.
- Let D = max d(i,j), the diameter.
- Draw K quadruples, each of four **distinct** bar indices, uniformly at random. Use the exact average when C(n,4) ≤ K.
- **H = (2/K) Σ_k fp(q_k) / D**, which lies in [0,1].
- It lies in [0,1] because fp ≤ D/2 always holds. The paper uses this bound, and it follows from fp ≤ the cross distances.

**Sample size.** The paper gives nothing on this. Because each term lies in [0,1], Hoeffding's inequality gives a standard error of at most 1/(2√K). K = 20,000 gives at most 0.0035, which is ample. The cost is O(n²) for the distance matrix plus O(K) for the quadruples, which is trivial for 21,425 songs.

**Pitfalls.**
1. **Scale.** fp grows with the diameter, so normalise. A single odd bar (a fill, or a sparse pickup) inflates D and lowers H. As a sensitivity check, also report the version divided by the mean pairwise distance.
2. **Repetition.** If any two of the four bars have identical chroma, fp is exactly 0 (the Example 4.4 effect). Heavily repeated songs therefore score as "tree-like" just for being repetitive. Report a second version, H_types, computed after merging identical bar vectors. It needs at least 4 distinct types.
3. **Sampling with replacement**, as in the paper's i.i.d. definition, makes duplicates more likely in short songs. That biases H by length, so sample distinct indices.
4. **Order blindness.** H depends only on the multiset of distances. **Shuffling bars leaves it exactly unchanged**, so a shuffled-bar null is useless for this form. Usable nulls:
   - Draw n bars i.i.d. from the corpus pool, or from the song's own pitch-class marginal.
   - Use a time-aware version in which points are consecutive 4-bar windows (48-d), so shuffling does change it.
5. **Concentration.** As the Gaussian example and the regular-graph proof (E fp ≤ 2·sd of distance) show, a low H can simply mean the distances are tightly bunched. Report the coefficient of variation of the off-diagonal distances next to H, and check that H says something the spread does not.
6. **Ties.** Ties at the median are harmless, since the formula handles them. Chord-label distances that take only a few values give many ties and many zeros.

**Secondary (graph form, where the paper's theorems apply directly).**
- Nodes are distinct bar types (or chord labels). Add an unweighted edge for each observed bar-to-bar transition and use the shortest-path metric.
- Compute average fp, average slimness and average minsize over random triples, choosing among shortest paths uniformly as the paper does.
- Normalise each by the graph diameter. Here the shuffled-bar null does change the score.
- The paper's main lesson becomes a test: songs with low fp but high slimness are "tree-like only on average", which is the G_n pattern.
- Cost: a triangle with side length L costs about O(L³) for minsize and O(L²) for slimness. That is fine at song size.

## 7. Leads
1. S. Chatterjee, L. Sloman, "Average Gromov hyperbolicity and the Parisi ansatz", *Advances in Mathematics* 376:107417, 2021. This is the source of average hyperbolicity and its tree embedding. (arXiv id not shown.)
2. J.-H. Yim, A. C. Gilbert, "Fitting trees to ℓ1-hyperbolic distances", NeurIPS 36, 2023/2024. Gives an algorithm to fit a tree to data that is tree-like on average, which could yield an explicit tree for a song's form. (arXiv id not shown.)
3. O. Narayan, I. Saniee, G. H. Tucci, "Lack of hyperbolicity in asymptotic Erdős–Rényi sparse random graphs", *Internet Mathematics* 11(3):277–288, 2015.
4. I. Tishby, O. Biham, R. Kühn, E. Katzav, "The mean and variance of the distribution of shortest path lengths of random regular graphs", *J. Phys. A* 55(26):265005, 2022. Relevant to the distance-spread control.
5. A. Malyshev, "Expanders are order diameter non-hyperbolic", arXiv:1501.07904, 2015.

(No DOIs appeared in the bibliography. Also cited: van der Hofstad, "The giant in random graphs is almost local", arXiv:2103.11733.)
