# Card 2 — FALLBACK PAPER READ (not the assigned one)

**Read first:** I could not read the assigned paper (arXiv 2603.03634). Following the instructions, I read the fallback paper (arXiv 2506.12546v1) in full.

## 1. Citation and what was read

**Assigned paper (not read beyond the abstract).**
- Marco Antonio Cruz-de-la-Rosa and Fernando Guerrero-Poblete, "An approach to non-equilibrium Markov chains through cycle matrices", arXiv 2603.03634v1, math.PR. Only one version exists, v1, submitted 2026-03-04.
- Here is everything I know about it, all from the abstract. It proves that the kernel of the incidence matrix of the chain's interaction graph is isomorphic to the space of antisymmetric matrices whose rows sum to zero. That kernel is the space spanned by the graph's cycles. It then introduces "cycle matrices" as a basis for the matrices that describe non-equilibrium.
- Why it was not read:
  - The abs page lists no HTML version.
  - The fetch of https://arxiv.org/html/2603.03634 was blocked because the permission request timed out.
  - https://arxiv.org/pdf/2603.03634 (tried once) returned only the title and abstract.
- Nothing below comes from that paper.

**Paper actually read.**
- Marc Homs-Dones, Robert S. MacKay, Bazil Sansom and Yijie Zhou, "Circular Directional Flow Decomposition of Networks", arXiv 2506.12546v1. The HTML page is dated 28 Aug 2025.
- The arXiv category was not shown on the HTML page. My fetch of the abs page was blocked by the same permission timeout, so the category and version history are unconfirmed. Keywords: DAG, circular, balanced, cycle, weighted directed network.
- How I read it: the fetch tool summarises, so I read the page in seven passes. They covered every section (1–7), the reference list, and Appendices A–G. The second half was read with an offset, and the last pass covered the closing paragraph.
- Caveat: the tool paraphrases, so the formulas below are reconstructed from its summaries. The listing of Algorithm 2 is not in the HTML; only a prose description is given.

## 2. Main construction and theorems

This paper does **not** do Schnakenberg or Kalpazidou cycle affinities, or entropy production. It is a flow-network paper, but it sits right next to that work.

**Setup.** Take a weighted directed graph with weights w_ij ≥ 0, where self-loops are allowed.
- A **circular** (balanced) flow c has in-weight equal to out-weight at every node.
- A **directional** flow d is acyclic.

**The decomposition (CDFD).** A CDFD writes w = c + d with 0 ≤ c, d ≤ w on each edge.
- **Circularity** is Σc/Σw, a number in [0,1]. Directionality is 1 − circularity.
- The decomposition is **not unique**. When two cycles share an edge, either one can take the shared capacity. In the paper's toy example, circularity can be anywhere from 3/8 up to 6/8.

**Theorem 1 (min-cost flow).** Every directional part solves a minimum-cost flow problem, and every such solution is a directional part.
- The problem: minimise Σκ_ij x_ij over flows x that match w's net imbalance (in minus out) at every node, with 0 ≤ x ≤ w.
- The costs κ are positive, and different κ give different directional parts.
- The argument: if an optimum contained a cycle, removing flow around that cycle would lower the cost.

**Theorem 2.** The set of all decompositions is a contractible polytope complex. It need not be convex (Appendix C gives a counterexample). The achievable circularities therefore form an interval with no gaps.

**Two canonical choices.**
- **Maximal circularity** (all κ = 1). It is computable in polynomial time, but it is an extreme point: it can saturate some cycles and starve others. Finding the *minimum* circularity is NP-hard (Appendix E reduces it to the Hamiltonian cycle problem).
- **Balanced Flow Forwarding (BFF).** This is the Markov-chain bridge.
  - Define w̄_ij = w_ij / w_i^out.
  - Theorem 3: the circular out-flow is the largest vector x ≤ w^out with x w̄ = x. That is a scaled stationary distribution of the random walk on w.
  - The algorithm repeats three steps: strip sink nodes, take that maximal invariant vector per strongly connected component, and subtract it.
  - The result is unique, keeps each node's routing proportions, and puts positive flow on every cycle.

**What is assumed.** The graph is finite and has non-negative weights. Time and dynamics play no role. There is no irreducibility assumption, because strongly connected components are handled one at a time.

## 3. Is the measure from the notes?

No. This is a mathematics paper with no music data in it. To apply it to songs, it needs only a directed weight matrix, and the chord-transition counts n_ij fit exactly. That would make the measure purely from the notes.

## 4. Proved vs assumed; numerical examples

**Proved:** Theorems 1–4, the NP-hardness result, the BFF properties (unique, independent of the order of choices, every cycle gets flow) and its polynomial running time.

**Assumed or heuristic:** the choice between maximal circularity and BFF. This depends on the application and is argued, not proved.

**Numbers reported.**
- In weighted Erdős–Rényi graphs, circularity is about flat in network size n. The maximal and BFF values differ by about 0.1, and directedness falls roughly as a power law in the average weight. Only asymptotic (large-n) results are proved.
- In the Sarafu community currency (about 400k transactions), circularity is 0.880 (BFF) and 0.899 (maximal).
- In Sarafu, circulation is dominated by 2-cycles, and every method counts these fully.
- BFF correlates with trophic incoherence (no correlation coefficient is given). The Finn cycling index and the Luo–Magee measure both saturate or mislead in places.

## 5. Lasting love and covers

The paper says nothing about either.

*Extrapolation:* the paper's lesson that a raw count of cycles misleads, and that 2-cycles behave differently from longer cycles, carries over to songs. For songs, "circulating" structure means progressions that return, and "directional" structure means through-going lines.

## 6. Methods and measures for tonight

**(a) A single song is almost entirely "circular".**
- A chord sequence is one walk, so its count matrix is balanced at every chord except the first (+1 out) and the last (+1 in).
- So the CDFD directional part is one start→end path. Maximal circularity is 1 − d(start, end)/N, where d is the shortest path from the start chord to the end chord in the song's chord graph and N is the number of chord changes.
- Example: I V vi IV played four times gives 0.8. If the song wraps (its last chord can lead back to its first), circularity is exactly 1.
- **So CDFD circularity on one song mostly measures where the song starts and ends.** Don't use it as a song-level measure. It becomes informative only when pooled across songs, for example a corpus-level graph built per artist.

**(b) Last night's A is a CDFD step.**
- Σ min(n_ij, n_ji) is the mass removed when you peel off every 2-cycle (back-and-forth moves).
- A is the share of flow left over. That leftover is the net current r_ij = max(n_ij − n_ji, 0).
- r is still balanced, apart from the ±1 at the start and end chords. So r splits into cycles of length ≥ 3 plus one path.
- This is the same split as in the Sarafu example: 2-cycles carry no net current.

**(c) Parameter-free numbers to compute on r**, with the song made cyclic (add the last→first move):
1. **Number of independent cycles.** This is the cyclomatic number E − V + C of the undirected support of r: edges minus chords plus connected pieces. It is an integer, and is 0 when the song is pure back-and-forth.
2. **Dominant-cycle share**, i.e. the flux on the heaviest cycle divided by Σr. **This is non-unique, so report a range.** Peel cycles greedily in two orders: heaviest-first gives the maximum, and BFF-proportional allocation gives a canonical middle value. The paper's main warning is that a single peeling order is arbitrary.
3. **Longest carrying cycle**, i.e. the length of the dominant cycle: 3, 4, … chords.
4. **BFF circularity on the raw n_ij.** This is the canonical unique value, and its stationary vector also gives per-chord circulating weight.

**(d) Entropy production, and why the pseudocount matters.**
- The planned σ uses (n_ij − n_ji) ln((n_ij + c)/(n_ji + c)) / N.
- Most song edges are one-way (n_ji = 0). Each such edge contributes n_ij ln((n_ij + c)/c), which is dominated by ln(1/c).
- So σ ≈ A · ln(typical n/c) plus small two-way terms. **Expect σ to correlate very strongly with A.** It adds information only through edges that run both ways.
- σ is not parameter-free. Check whether song rankings change across c = 0.1, 0.5 and 1.
- Schnakenberg's form rewrites the same σ as a sum over cycles: cycle current × cycle affinity, where the affinity is ln of the product of forward counts over backward counts around the cycle. With zero backward counts the affinity is infinite, so the pseudocount problem does not go away.
- σ and A are unchanged if the song is played backwards. They measure how irreversible a song is, not which way it runs.

**(e) Finite-count bias.**
- Even with no true arrow (reversible), each traversed chord pair with m = n_ij + n_ji gives a split of about Binomial(m, ½). Its symmetric-KL term then averages about 1 (it behaves like a χ²₁ statistic).
- So plug-in σ ≈ (true σ) + K/N, where K is the number of chord pairs used. At N = 8–15 this inflates σ by roughly 0.3–0.6 nats.
- Corrections:
  - Subtract K/N.
  - Better: a per-song z-score against a sign-flip null. Redraw each pair's split as Binomial(m, ½) about 1,000 times.
  - Always control for N and K. Last night's reversal on fresh songs may be a length or chord-count artefact.

**(f) Prediction (extrapolation).** A song carried by one clear cycle of 3–4 chords should score:
- high A,
- cyclomatic number 1–2,
- dominant share above 0.7.

This "loop" profile is easy to transfer and so might be covered more often. Fresh single-artist songs may already be mostly loops, which would flatten any contrast. Test the dominant-cycle share against covers **within N- and K-matched strata.**

## 7. Leads

1. **Schnakenberg, J. (1976).** "Network theory of microscopic and macroscopic behavior of master equation systems", *Rev. Mod. Phys.* The original cycle-affinity form of entropy production.
2. **Kalpazidou, S. (1995; 2nd ed. 2006).** *Cycle Representations of Markov Processes*, Springer. Gives a unique, probabilistic cycle decomposition (cycle skipping), which avoids the non-uniqueness problem.
3. **Jiang, D.-Q., Qian, M. and Qian, M.-P. (2004).** *Mathematical Theory of Nonequilibrium Steady States*, Lecture Notes in Mathematics 1833. Circulation decomposition with exact entropy-production formulas.
4. **Roldán, É. and Parrondo, J. M. R. (2010).** "Estimating dissipation from single stationary trajectories", *Phys. Rev. Lett.* How to estimate entropy production (as a KL divergence) from one short sequence, including finite-data issues.
5. **Altaner, B. et al. (2012).** "Network representations of nonequilibrium steady states: cycle decompositions, symmetries, and dominant paths", *Phys. Rev. E* 85, 041133. Cited by the fallback paper, and addresses dominant cycles directly.

Leads 1–4 come from my own knowledge, not from the paper's bibliography. Lead 5 is in the paper's bibliography.
