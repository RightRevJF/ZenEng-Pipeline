# Card 1 — Helmholtz-Hodge Decomposition on Graphs (arXiv 2412.09434)

## 1. Citation and copy read

- **Author:** Peter March (Department of Mathematics, Rutgers University). Single author.
- **Title:** "Helmholtz-Hodge Decomposition on Graphs." arXiv:2412.09434 (submitted December 2024, going by the identifier).
- **Category, version, exact date: NOT CONFIRMED.** The abstract page (arxiv.org/abs/2412.09434) and the versioned HTML (…/html/2412.09434v2) were blocked by the permission system, so I could not see the listing. The HTML page shows no version, date or licence line. From the subject matter it is probably math.CO, but that is a guess.
- **Copy read:** the unversioned HTML at arxiv.org/html/2412.09434, read in five WebFetch passes:
  - the abstract, table of contents and sections 1–2;
  - section 3;
  - the unheaded final section (items 4.1–4.13);
  - the bibliography and the introduction's comparisons with other work;
  - a close re-read of Example 4.5, Proposition 4.6 and the proof of Theorem 4.12.
  The paper is short and has no appendices. The fetch tool summarises rather than quoting, so some formulas may be off by a sign or a label. The edge values of the Example 4.5 field relied on a figure the tool could not see.
- I checked the dimension claims myself with a short script (section 4 below).

## 2. Main construction and theorems

**Setting.** G is a finite, simple, undirected, unweighted graph, assumed connected. A "vector field" X gives a real number to each *directed* edge (i,j). The two directions are independent, so the space of fields has dimension 2|E|.

The paper builds this on a "tangent graph": its nodes are the directed edges of G. There are **no incidence matrices, no edge weights, no triangles or 2-cells, and no least squares** in the usual sense. This is not the familiar clique-complex Hodge Laplacian (Lim 2020; HodgeRank). The paper sets itself against that approach.

**Operators.**
- Gradient: ∇φ(i,j) = φ(j) − φ(i).
- Divergence: div X(i) = Σ over out-edges u of [X(reverse of u) − X(u)]. This is the adjoint of ∇.
- Laplacian: Δ = div∘∇. Its kernel is the constant functions, so the gradients form a space of dimension |V|−1.
- Every field splits into a symmetric part s and an antisymmetric part a:
  - sX = ½(X + reversed X);
  - aX = ½(X − reversed X).
  Symmetric fields always have zero divergence.

**Circulation.** The circulation of X round a simple circuit is the sum of X along it, in order.
- X is "circulation-free" if every simple circuit, in both directions, sums to zero. These fields form the space Z.
- **Curl** is defined as the orthogonal projection onto Z⊥ (Definition 4.8). It keeps every circulation of X, it has zero divergence, and it is orthogonal to the harmonic fields.
- "Harmonic" means circulation-free and divergence-free.
- The paper stresses that this curl is non-local: it depends on all the cycles at once.

**Claimed theorem (4.12).**
- The fields split orthogonally as gradient ⊕ curl ⊕ harmonic.
- The sequence 0 → zero-mean functions → (∇) fields → (curl) fields → (div) zero-mean functions → 0 is claimed to be exact.
- Claimed dimensions: dim(harmonic) = |V|−1 and dim(curl) = 2(|E|−|V|+1), twice the first Betti number. The printed statement has a typo; the proof gives this form.

**Other results in section 3.** Graph versions of the divergence theorem and Green's first, second and third identities (with Green's functions Δ⁻¹(e_i − 1/|V|)), and a Helmholtz theorem: fields = im ∇ ⊕ ker div (Proposition 3.13).

**Worked examples.**
- Trees: every field is circulation-free.
- Unicyclic graphs: dim Z⊥ = 2.
- A square with one diagonal (Example 4.5).

**Open questions it poses.**
- How the harmonic space splits between symmetric and antisymmetric fields.
- A local formula for the curl.
- A graph version of Maxwell's equations.

## 3. Is the measure from the notes?

No. This is pure mathematics, with no data and no music. To use it on songs, one would need:
- a graph whose nodes are chords and whose edges are observed chord moves;
- an edge field taken from the counts, either the net flow F or the two-way counts n_ij and n_ji as separate directed values.

## 4. Proved vs assumed; examples; my check

**Proved soundly (by short arguments):**
- the Green-type identities;
- im ∇ ⊕ ker div;
- curl keeps circulations and has zero divergence;
- the three-part orthogonal split. This one holds automatically, because Z = gradients ⊕ harmonic.

**Assumed:** the graph is connected, simple, unweighted and undirected, with unit inner products.

**The dimension claims fail in my check.** I set up the paper's definitions as the fetch reported them and computed ranks for every simple circuit in both directions:

| Graph | β₁ | dim Z⊥ (curl) found / claimed | dim harmonic found / claimed |
|---|---|---|---|
| 4-cycle | 1 | 2 / 2 | 3 / 3 |
| square + diagonal | 2 | 5 / 4 | 2 / 3 |
| K₄ | 3 | 9 / 6 | 0 / 3 |

**Why it fails.** For symmetric fields the circuit sums are *unsigned*. The outer square no longer equals the sum of the two triangles, so each new cycle adds its own constraint. The induction in the proof of 4.12 misses this, and the paper's own Example 4.5 contradicts itself:
- its symmetric solution (a = −b, c = −d, e = 0) implies rank 5, not the stated 4;
- its extra field Y, as I reconstruct it, is a gradient with non-zero divergence, so it is not harmonic.

Also, ker(curl) = Z, which contains the harmonic fields. So the sequence is not exact unless the harmonic space is zero. These problems need the original PDF to confirm, but the counterexamples are simple.

**Numerical examples:** none beyond these small hand-worked graphs.

## 5. Lasting love and covers

The paper says nothing about music, popularity or covers.

**Extrapolation:**
- If directed harmony matters, the useful split is "downhill to a home chord" (gradient) versus "going round" (cycle). The paper offers a different language for the cycle part.
- Its symmetric half is a new idea: circulation of the two-way traffic n_ij + n_ji. It has no obvious musical meaning and is not a candidate for covers.

## 6. Methods or measures for tonight

**The key fact for us.** The net flow F_ij = n_ij − n_ji is antisymmetric.
- On antisymmetric fields, March's harmonic part is always zero. An antisymmetric field with no circulation is a gradient, and a gradient with no divergence is zero.
- His curl then equals projection onto the cycle space.
- So for F, the paper gives exactly the classical split with **no 2-cells filled**: F = ∇φ + C, where C is a circulation flow of dimension β₁ = |E| − |V| + 1.
- In Lim/HodgeRank terms, with no triangles filled, "curl" is empty and "harmonic" is the whole cycle space. The labels differ; the numbers are the same.
- Don't use the symmetric machinery: it is unproven and its dimension claims are wrong.

**Recipe per song:**
1. Nodes are the distinct chords. Put an undirected edge {i,j} wherever n_ij + n_ji > 0, with consecutive equal chords already collapsed.
2. Edge flow: F_ij = n_ij − n_ji.
3. Solve the least-squares problem φ = argmin Σ_edges (φ_j − φ_i − F_ij)². This is the graph Laplacian L φ = −Bᵀ F, where B is the edge-by-node incidence matrix; take the pseudo-inverse and fix mean(φ) = 0.
4. Split F into G = Bφ (gradient) and C = F − G (cycle part). C has zero divergence: inflow equals outflow at every chord.

**Parameter-free numbers:**
- **Gradient share:** g = ||G||² / ||F||², with cycle share 1 − g. Define it only when ||F|| > 0. It is undefined for a song in which every move is reversed.
- **Potential range:** max φ − min φ, divided by the total number of moves, so songs of different lengths compare. Also record which chord sits at the bottom (the "home" chord) and whether it is the tonic. That doubles as a check that the method makes sense.
- **β₁ = |E| − |V| + 1**, the number of independent loops. It is a pure size covariate.
- **Net-flow fraction:** ||F||₁ / Σ n_ij. This is close to the arrow measure A, so report g *conditional on* A.
- **Optional, for comparison only:** fill the chord-graph triangles (the clique complex). Then the cycle part splits further into triangle curl and harmonic loops, which shows whether circulation lives in 3-chord loops or longer ones.

**Pitfalls:**
- **Pure 4-chord loops are all cycle.** I–V–vi–IV repeated is a 4-cycle with constant flow: g = 0 and φ is flat. That holds whether or not triangles are filled, because the loop has no triangles.
- **Trees are all gradient.** With 3 chords and no closed loop, β₁ = 0 and g = 1 automatically. g is informative only when β₁ ≥ 1, so stratify by β₁ or restrict to β₁ ≥ 1.
- **Small graphs (3–6 chords):** g takes few distinct values and is noisy. Bootstrap by resampling sections, or compare with a null that shuffles the chord order within the song.
- **Length:** ||F||² grows with the number of chord changes. Shares are fine; raw norms are not.
- **Entropy production Σ (n_ij − n_ji) ln(n_ij / n_ji)** is infinite when one direction is never played, which is common. It needs a pseudocount, which is a parameter, or should be restricted to edges played in both directions. Schnakenberg's result writes it as a sum over cycles of (cycle flux × cycle affinity). So it is the natural partner to C, and a gradient-only flow on a tree gives zero affinity in the Markov sense. Report it with and without a pseudocount of 0.5.
- **Non-locality** (the paper's point): the loop part is a property of the whole graph. Removing one rare chord can change β₁ and g a lot. Run a sensitivity check that drops chords seen only once.

## 7. Leads

1. **Jiang, Lim, Yao and Ye (2011), "Statistical ranking and combinatorial Hodge theory," *Mathematical Programming*.** The standard least-squares gradient/curl/harmonic split of pairwise flows (HodgeRank). It is the exact template for ranking chords by potential.
2. **Lim (2020), "Hodge Laplacians on Graphs," *SIAM Review*.** A clear account of the clique-complex version: incidence matrices and which triangles to fill.
3. **Strang, "Applications of the Helmholtz-Hodge Decomposition to Networks and Random Processes," PhD thesis, Case Western Reserve University (around 2020; year unconfirmed).** March's main source. It uses cycles beyond triangles and applies the split to random processes, the closest fit to chord Markov chains.
4. **Schnakenberg (1976), "Network theory of microscopic and macroscopic behavior of master equation systems," *Reviews of Modern Physics*.** The cycle decomposition of entropy production, linking the C part to Σ (n_ij − n_ji) ln(n_ij / n_ji).
5. **Schaub, Benson, Horn, Lippner and Jadbabaie (2020), "Random walks on simplicial complexes and the normalized Hodge 1-Laplacian," *SIAM Review*.** Weighted and normalised versions, which matter when chord counts are very uneven.
