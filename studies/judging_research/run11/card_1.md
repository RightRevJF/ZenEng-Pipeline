# Card 1: A sharp higher-order Cheeger inequality (arXiv:2609.35369)

## 1. Citation and copy read

- Yunpeng Li (School of Data Science, CUHK-Shenzhen). "A sharp higher-order Cheeger inequality." arXiv:2609.35369, 2026. Pure mathematics (spectral graph theory).
- Copy read: abstract page https://arxiv.org/abs/2609.35369 and full text via https://arxiv.org/pdf/2609.35369, fetched 2026-11-28. Neither the abstract page as returned nor the PDF text showed a version number or submission date, so the version is **unknown** (most likely the current one).
- The HTML copies (https://arxiv.org/html/2609.35369 and .../2609.35369v1) were **blocked**: the fetch tool's permission request timed out. They were not retried.
- Caveat: the fetch tool returns a condensed paraphrase, not raw text. I got every numbered statement, the constants, the sharpness example and the bibliography, but proofs only as outlines.
- Oddity: the bibliography lists the author's *earlier* paper, "A polylogarithmic higher-order Cheeger inequality", under the **same** id 2609.35369. Probably v1 was the weaker paper and a later version was retitled; unconfirmed.
- The paper discloses AI help (ChatGPT/Codex), notes that L. C. Lau reports the same bound independently, and is an unrefereed 2026 preprint.

## 2. Main construction and theorem

**Setting.** Any finite undirected *weighted* graph: nonnegative symmetric weights, every vertex with positive degree. Self-loops are allowed and count once in the degree. Regularity is not needed. The Laplacian is the **normalized** one, L = D^-1/2 (D - A) D^-1/2, with eigenvalues 0 = λ1 ≤ λ2 ≤ ... ≤ λn ≤ 2. The combinatorial Laplacian D - A is never used.

**Conductance of a set S:** the weight leaving S divided by vol(S), the sum of the degrees in S. It is measured one-sided, even when S holds more than half the volume.

**k-way conductance φ_k(G):** choose k disjoint nonempty vertex sets (they need not cover the graph), take the worst conductance among them, and minimise over all choices. A small φ_k means the graph has k "rooms", each joined to the rest only by thin doorways.

**Theorem 1.1.** There is an absolute constant C such that, for every such graph and every 1 ≤ k ≤ n, φ_k(G) ≤ C √(λ_k · log(k+1)).

Combined with the known lower bound λ_k/2 ≤ φ_k (Lee, Oveis Gharan and Trevisan 2014, cited and not reproved here), this gives:

  **λ_k / 2 ≤ φ_k ≤ C √(λ_k log(k+1)).**

What is new: the index on λ is exactly k (earlier bounds needed λ_2k, or delivered only a fraction of the k sets), and the loss is only √log k. Earlier versions of the factor were O(k²) (LOT), (log k)^(3/2) (Lau's 2026 book manuscript), and a polylog bound in the author's own earlier paper.

**Constants.** The value of C is **not computed**. Internally the threshold is τ = C0 √(λ_k log(k+1)), and C0 is fixed by inequalities that involve ε = 1/64, δ = ε/4 and a partitioning constant that is never evaluated. So no usable number comes out for small graphs.

**Proof outline.** Minimising cut minus τ·volume (a min-cut) gives "τ-stable" sets that leak little (Lemmas 3.2–3.3). Random-ball cuts of the k-eigenvector embedding (Charikar et al.; Lemmas 4.1–4.2) and O(log k) rounds of selection in a shrinking subspace (Lemmas 5.1–5.2) build the rooms. A dyadic maximal inequality and a local-eigenvalue count then yield exactly k sets (Lemmas 6.1–6.3). The proof shows existence only; it gives no practical algorithm.

## 3. Is the measure from the notes?

The measure is pure graph theory, but it can be computed from the notes alone. For one melody:

1. Make one node per distinct pitch (MIDI number), or per pitch class for the folded version.
2. For each pair of consecutive notes (a, b), add 1 to C[a][b]. Set W = C + Cᵀ.
3. Set degree d_v = row sum of W, then build L = I - D^-1/2 W D^-1/2 and take its eigenvalues.

A melody is a walk through its own pitch set, so this graph is always connected and λ2 > 0. No timing, harmony or lyrics are used.

## 4. What is proved and what is assumed

- **Proved:** the upper bound above for all weighted graphs and all k. Proposition 7.1 shows the √log k factor is **sharp**. The example is the k-dimensional hypercube with weight ζ^(Hamming distance), where ζ = log 2 / log k (loops included). There, λ2 = ... = λ(k+1) = 2ζ/(1+ζ), and hypercontractivity forces every family of k disjoint sets to contain one with conductance at least 1/2. So φ_k/√λ_k ≥ √(log k / (8 log 2)) for k ≥ 3.
- **Assumed:** positive degrees only. No regularity is assumed, and there is no limit on size or weights.
- **Not covered:** explicit constants, an efficient algorithm, the combinatorial Laplacian, directed graphs, and the top of the spectrum (λn, bipartiteness).

## 5. Lasting love and covers

**Directly: nothing.** It is a theorem about graphs.

**Extrapolation (labelled, untested):** The folk-melody lead ("small λ2, two rooms, more cover artists") read λ2 as a stand-in for a two-room shape. For k = 2 that reading was already justified by the classical Cheeger inequality. This paper justifies the same reading for **any** number of rooms, with almost no loss: on melody graphs of about 5 to 20 pitches, √log(k+1) is at most about 1.5. So if "rooms" matter to listeners, the small eigenvalues λ2, λ3, λ4 are honest proxies for 2, 3 and 4 rooms. The paper cannot say whether rooms make a song loved or covered. It also cannot check Jason's S = 1 + g/π.

## 6. Measures for this pass (Hooktheory melodies)

Shared free settings. Fix these before looking at the cover or popularity data, and report the others as robustness checks:
(a) pitch versus pitch class. Make pitch the primary choice, since it keeps register.
(b) Repeated notes. Either drop them, or keep them as self-loops. The paper allows loops: they add to degree but never to cut, so they lower conductance. Make "drop" the primary choice.
(c) Transitions across rests or phrase gaps. Make "keep" the primary choice. That keeps the graph connected.
(d) Clip length. Store n (distinct pitches) and m (transitions) with every measure, and only compare like with like.

**M1. Size-adjusted λ2 (the "two rooms" gap).**
- Recipe: compute λ2 of L. Divide it by λ2 of the plain path graph with the same n, which is 1 - cos(π/(n-1)). The path is the thinnest connected walk through n pitches.
- Report the ratio, and the within-n rank as a second version.
- Guarantee: λ2/2 ≤ φ2 ≤ √(2 λ2) (classical; k = 2 case).
- Free setting: the choice of baseline. Avoid it by also reporting the rank inside groups of melodies with the same n.

**M2. Exact conductances φ2 and φ3 by brute force.**
- Melody graphs are small (n is rarely above 15), so there is no need for the spectrum here. List all 2^n subsets and compute the conductance of each. Then find the best pair (and triple) of disjoint subsets, minimising the worst conductance.
- Report φ2, φ3, and the "tightness" φ_k / √λ_k.
- Guarantee: λ_k/2 ≤ φ_k always holds, and Theorem 1.1 says the tightness stays below C√log(k+1).
- No free settings beyond (a) to (d). This is the direct "doorway thinness" that the spectral numbers only bracket.

**M3. Number of rooms k\* and λ3/λ2.**
- Recipe: sort the eigenvalues. Set k\* = the k in 1..n-1 that maximises the gap λ(k+1) - λk. Also report λ3/λ2.
- A ratio near 1 means a third room is as separate as the second. A large ratio means exactly two rooms.
- Free setting: a fixed bound θ, as in "count the eigenvalues below θ". The largest-gap rule avoids it.
- Guarantee: by the theorem, small λ_k forces k genuinely separate rooms, and a large λ(k+1) rules out k+1 rooms (lower bound).

**M4. The spectral split and how often the tune crosses it.**
- Recipe:
  1. Take the second eigenvector of L and divide each entry by √d_v.
  2. Sort the pitches by that value, and try each prefix as room A. Keep the prefix with the lowest conductance (the sweep cut).
  3. Walk the melody in time order. Record the crossing rate (the share of consecutive note pairs that change room) and the number of visits (runs within one room).
  4. Also note whether room A is mostly the high register or the low.
- For k\* ≥ 3, use k-means on the first k\* rescaled eigenvectors. Fix the seed and the number of restarts.
- Guarantee: the sweep cut's conductance is at most √(2 λ2), so it is never much worse than the best split. Theorem 1.1 promises k good rooms exist, but it gives no recipe for finding them.
- Free setting: none for k = 2.

**M5. Near-bipartiteness, 2 - λn (from outside this paper).**
- Recipe: take the largest eigenvalue λn and report 2 - λn. It is small when the melody almost always jumps between two pitch groups, as in a seesaw or alternating figure.
- The "dual Cheeger" bound (Trevisan; Bauer–Jost) makes this precise. This paper does **not** cover it.
- No free settings.

## 7. Leads

1. J. R. Lee, S. Oveis Gharan, L. Trevisan, "Multiway spectral partitioning and higher-order Cheeger inequalities", J. ACM 61(6), 2014. arXiv:1111.1055. (The source of λ_k/2 ≤ φ_k, of the hypercube example, and of the spectral-clustering guarantees.)
2. A. Louis, P. Raghavendra, P. Tetali, S. Vempala, "Many sparse cuts via higher eigenvalues", STOC 2012. arXiv:1111.0965, doi:10.1145/2213977.2214079.
3. K. Makarychev, Y. Makarychev, L. Shan, A. Vijayaraghavan, "Higher-order Cheeger inequality for partitioning with buffers", SODA 2024. arXiv:2308.10160, doi:10.1137/1.9781611977912.80.
4. L. C. Lau, *Algorithmic Spectral Graph Theory*, book manuscript, 2026 (no id given; Thm 7.17 is the cut-improvement source).
5. Not cited by this paper, but needed for M5: L. Trevisan, "Max cut and the smallest eigenvalue", STOC 2009 / SIAM J. Comput. 2012. arXiv:0806.1978.
