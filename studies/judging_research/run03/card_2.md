# Card 2: Resistance curvature on graphs (Devriendt and Lambiotte 2022)

## 1. Citation and copy read

Karel Devriendt and Renaud Lambiotte, "Discrete curvature on graphs from the effective resistance", *Journal of Physics: Complexity* 3 (2022) 025008, doi 10.1088/2632-072X/ac730d; arXiv 2201.06385.

Copy read: arXiv PDF v3 (23 Sep 2022), https://arxiv.org/pdf/2201.06385v3. The page has about 118k characters. I covered all of it through the WebFetch tool in several passes: Sections 1 to 6, Appendices A to F and the full 88-item bibliography. One caveat: the fetch tool returns paraphrase, not verbatim text. So the definitions and statements below come through that summary layer. I checked the key formulas myself by recomputing them in python (Section 2). The companion paper (arXiv 2302.06021) was blocked, so I did not read it.

## 2. Claim and data

**Construction.** Treat a weighted undirected graph as an electrical network, with each link weight c_ij acting as a conductance. Let Q be the Laplacian and Q† its pseudoinverse. The effective resistance between two nodes is

ω_ij = Q†_ii + Q†_jj − 2 Q†_ij.

This is a true distance (Theorem 1). For a link, the product c_ij·ω_ij (the "relative resistance") equals the chance that the link appears in a random spanning tree (Theorem 2). It lies between 0 and 1, and it equals 1 exactly when the link is a bridge, meaning removing it splits the graph. Foster's theorem says these products add up to n − β, where β is the number of connected pieces.

- **Node curvature:** p_i = 1 − ½ Σ_j c_ij ω_ij.
- **Link curvature:** κ_ij = 2(p_i + p_j)/ω_ij.

**Main results, in plain terms.**
- Bounds: 1 − d_i/2 ≤ p_i ≤ ½, where d_i is the number of neighbours. The lower bound is reached exactly when every link at i is a bridge. A sharper upper bound is 1 − β(G_i∖{i})/2.
- The node curvatures always sum to β, so they sum to 1 on a connected graph.
- Every cut node has p ≤ 0. Corollary: any graph with a cut node is either a path or has a node with negative curvature.
- Link curvature lies between (4 − d_i − d_j)/ω_ij and 2/ω_ij.
- **Other curvatures:** p_i equals the expected classical "combinatorial" curvature of node i over random spanning trees. Ollivier-Ricci curvature, computed with resistance as the distance and a lazy walk in the small-step limit, is ≥ κ_ij. Forman curvature divided by ω_ij is ≤ κ_ij. Both hold with equality on bridges.
- **Standard shapes:** a tree has p_i = 1 − d_i/2. A path has p = ½ at the two ends and 0 inside. A cycle has p = 1/n and κ = 4c/(n−1). Any node-transitive graph, the complete graph included, has p = 1/n, with κ = 2c × link density (so κ = 2 for K_n). Infinite lattices are flat. Infinite regular trees with degree d have p = 1 − d/2.
- **Other characterisations:** diffusion limits (Proposition 1); equilibrium form p = Ω⁻¹u/(uᵀΩ⁻¹u), where Ω is the matrix of all resistances and u is the all-ones vector; p as the circumcentre of a simplex built from the graph, with squared radius σ² = ½pᵀΩp; and p as the maximiser of ½fᵀΩf over vectors f that sum to 1.
- **Random geometric graphs:** a heuristic plus simulations put curvature near 0 in the bulk, dipping negative and then positive near the edge. Not proved.
- **Ricci flow:** dω_ij/dt = −2(p_i+p_j), a gradient flow (Propositions 4 and 5). It blows up at time n/(2µ_max) on node-transitive graphs.
- **Erdős–Rényi:** mean link curvature is about +2 when sparse, turns negative near the giant-component threshold (average degree about 1), and returns to +2 when complete.

**Assumptions:** the graph is simple, undirected and has positive weights. Self-loops are explicitly excluded. Disconnected graphs are allowed (resistance between pieces is infinite).

**Worked example** (python, unit weights, 4 chords):

| graph | node curvature p | link κ | Kirchhoff index Σω |
|---|---|---|---|
| 4-cycle (I–V–vi–IV–I) | ¼, ¼, ¼, ¼ | 1.333 each | 5 |
| path I–V–vi–IV | ½, 0, 0, ½ | 1 (ends), 0 (middle) | 10 |
| star, I hub with 3 leaves | −½ (hub), ½ ×3 | 0 each | 9 |
| K4 | ¼ ×4 | 2 each | 3 |

A song-like example: "I V vi IV" played three times, then "I ii V I", symmetrised with counts as weights. It gives p = (I 0, V 0, vi 0.27, IV 0.27, ii 0.45). The hub chords I and V come out flat. The loop chords are positive. The detour chord ii is the most positive, because it hangs off the hubs like a leaf. The spectral gap of P is 0.17. Unweighted, I and V move to 0.045, so weights matter.

## 3. Is the measure from the notes?

The measure is pure graph theory. It becomes a "from the notes" measure only through the graph we build: chords become nodes and move counts become weights, with no audio, lyrics or popularity. It sees only one-step chord succession. It ignores longer order, rhythm and melody, and it ignores direction once the graph is symmetrised. Repeated chords (self-loops) are invisible, because a self-loop cancels out of the Laplacian.

## 4. What is proved and what is assumed

**Proved:** the metric property, the spanning-tree probability, the bounds, the sum rule, the cut-node results, the values on trees, cycles and transitive graphs, the Ollivier and Forman inequalities, the expected-combinatorial-curvature identity, and the equivalent characterisations and flow propositions.

**Heuristic or numerical only:** convergence to smooth curvature in random geometric graphs, and the Erdős–Rényi sign change.

**Not in the paper:** there is no bound linking resistance curvature to the spectral gap, to diameter (a Bonnet–Myers-type result) or to the Kirchhoff index. The only eigenvalue that appears is µ_max, in the flow blow-up time. The authors also note they found no "scalar = trace of Ricci" sum formula. The later companion paper is said to add theorems of the diameter and spectral-gap kind, but I could not read it, so treat that as unverified.

## 5. Lasting love and covers

The paper says nothing about music or popularity. **Extrapolation, labelled:** positive curvature means a chord graph with redundant routes, like loops and cliques where every chord is reachable more than one way. Negative curvature marks hub chords that are the only bridge to several dead-end chords, a tree-like or "hub and spoke" shape. One could guess that covers favour progressions that are easy to re-voice and reorder (positive, uniform curvature). One could equally guess they favour songs with a distinctive detour chord (a strongly positive leaf beside a negative hub). The mathematics does not favour either guess.

## 6. Methods or measures it suggests for tonight's experiments

**Recipe, with no free settings beyond the graph build:**
1. Build M[a,b] = number of moves from chord a to chord b, pooled over clips. Drop the diagonal (self-loops add nothing anyway). Set C = M + Mᵀ.
2. Keep the largest connected component, or record β and compute curvature per component. Σp = β, so mixing pieces corrupts every summary.
3. Q = diag(C·1) − C; Q† = pinv(Q); ω_ij = Q†_ii + Q†_jj − 2Q†_ij; p = 1 − ½·rowsum(C∘ω); κ_ij = 2(p_i+p_j)/ω_ij on links.
4. Compute per-song summaries: **min p** (the most hub-like chord), **sd of p** (unevenness), **fraction of bridges** (count of links with c·ω = 1; this is tree-likeness), **κ of the I–V or tonic links**, and the curvature of the tonic itself.

**Pitfalls:**
- **Mean p is useless:** it is exactly 1/n, so it only counts chords.
- **Size and density dominate:** on 3,000 simulated loop-based songs (3 to 10 chords, 19 moves), sd of p had a rank correlation of 0.73 with chord count and −0.75 with density. Chord count and density together explained R² = 0.59 of sd p, 0.68 of min p, and 0.91 of a scale-free Kirchhoff index (Σω × total weight / number of pairs). Always partial out n and density, or compare songs with equal n.
- **Weight scale:** p does not change if all weights are multiplied by the same factor, but κ scales with them. Use p, or κ × total weight. Pooling more clips changes relative weights, not just scale.
- **Small graphs give few distinct values:** with n ≤ 4 there are only a few possible curvature patterns, so treat them as categories.
- **Direction is lost:** V→I and I→V become the same link. The spectral gap g uses direction; curvature does not.

**Relation to g and the Kirchhoff index:** in the simulation, g correlated only weakly with curvature summaries (ρ ≈ −0.18 to 0.25), and chord count and density explained just R² = 0.24 of g. So curvature is mostly a different axis from the gap, and much more a function of size. The Kirchhoff index Kf = Σ_{i<j} ω_ij = n·tr(Q†) is almost completely set by n and density here. Kf is a global "how spread out" number; p shows where in the graph the spread is. A useful test: does min p or the bridge fraction predict covers after controlling for n, density, g and the repetition measure, within artist?

## 7. Leads

1. **Devriendt, Ottolini, Steinerberger (2024), "Graph curvature via resistance distance"**, *Discrete Applied Mathematics*. The follow-up, reported to contain diameter and spectral-gap theorems for this curvature.
2. **Steinerberger (2022), "Curvature on graphs via equilibrium measures"** (ref 75). A close relative based on the same equilibrium idea (Ωp ∝ u), with Bonnet–Myers-style results.
3. **Ollivier (2010), "A survey of Ricci curvature for metric spaces and Markov chains"** (ref 64). Links curvature to the spectral gap of a Markov chain, which is the bridge to our P.
4. **Klein and Randić (1993), "Resistance distance"** (ref 49). The origin of resistance distance and the Kirchhoff index.
5. **Topping, Di Giovanni, Chamberlain, Dong, Bronstein (2022), "Understanding over-squashing and bottlenecks on graphs via curvature"** (ref 78). Negative curvature marks bottlenecks; a model for reading hub chords.
