# Card 1: Ollivier, Ricci curvature of Markov chains on metric spaces

## 1. Citation and copy read

Yann Ollivier (2009). "Ricci curvature of Markov chains on metric spaces." *Journal of Functional Analysis* 256(3), 810-864. arXiv math/0701886.

**Copy read:** arXiv v4 PDF (30 July 2007), https://arxiv.org/pdf/math/0701886v4 (no HTML version exists). **Read in full, with one caveat:** the fetch tool passes the PDF through a summarising reader, in two chunks. Together they covered the introduction, Sections 1-8, every numbered item (1-51) and the bibliography, but not as a verbatim scan. I did not see the published JFA version.

## 2. Claim and data

**Construction.** Start with a set of states that has a distance d, and a random walk that gives each state x a one-step distribution m_x. Take two states x and y. Ask how much it costs to move the pile of probability m_x onto the pile m_y, where moving a unit of mass a distance r costs r. That cheapest cost is the transport (Wasserstein) distance W1(m_x, m_y). Ollivier's coarse Ricci curvature is

  kappa(x,y) = 1 - W1(m_x, m_y) / d(x,y).

- **Positive:** the next-step clouds from x and y sit closer together than x and y do. Walks started nearby tend to come together.
- **Zero:** like a flat grid. A translation carries one cloud exactly onto the other.
- **Negative:** like a tree or a hyperbolic group (Example 15). Nearby walkers drift apart.

**Assumptions.** d must be a genuine symmetric metric. Each m_x needs a finite mean distance. The walk does **not** have to be reversible.

**Main results** (paraphrased; kappa means a lower bound on kappa(x,y) over all pairs):
- **Prop. 19 (local to global).** If d is a graph shortest-path distance, the smallest curvature over adjacent pairs equals the smallest over all pairs.
- **Prop. 20, Cor. 21 (contraction and mixing).** If kappa > 0, one step shrinks the transport distance between any two distributions by at least the factor (1 - kappa). So there is a unique stationary distribution, and every start reaches it geometrically fast, at rate (1 - kappa)^n.
- **Prop. 23-24 (Bonnet-Myers).** With positive curvature the diameter is at most 2 x (largest mean jump) / kappa.
- **Prop. 25 (mixing walks).** Averaging walks averages their curvature lower bounds. So making a walk lazy mixes in a walk with curvature 0.
- **Prop. 28-29, Cor. 30 (spectral gap).** M is the averaging operator, Mf(x) = E_{m_x} f.
  - On a **finite** space, reversible or not, every eigenvalue of M except the trivial 1 has modulus at most 1 - kappa. So **spectral gap g >= kappa**.
  - The stronger Lichnerowicz-type statement needs reversibility: the Laplacian eigenvalue is at least kappa, and Poincare-type variance bounds hold.
- **Prop. 31, Thm 32 (concentration).** The variance of any 1-Lipschitz function under the stationary law is at most about sigma^2/(n kappa). Here sigma is the local spread of a step and n a "local dimension". Tails are Gaussian out to a set range and exponential beyond it.
- **Also:** a modified log-Sobolev inequality (Thm 40); exponential concentration at zero curvature given an attracting point (Thm 44); stability under Gromov-Hausdorff limits (Sec. 6); L2 diameter bounds (Sec. 7).

**Examples.** Lazy discrete cube: 1/N. Kac's walk on SO(N): about 1/N^2, giving O(N^2 log N) mixing. Ising dynamics: positive at high temperature. Some bounds are sharp, others lose factors of 2-4 (Sec. 3.3).

**Worked example.** Computed with an exact linear program: `run03/card_1_orc.py`. Metric = shortest path on the undirected chord graph. Measures = rows of P, or the lazy rows 0.5·I + 0.5·P.

| Chord graph | kappa per edge, non-lazy | kappa per edge, lazy 1/2 | gap g of the lazy chain |
|---|---|---|---|
| Directed 3-cycle I→IV→V→I | 0 | **0.5** | 0.5 |
| Directed 4-cycle I→V→vi→IV→I | 0 | **0** | 0.29 |
| Hub I ↔ 4 spokes (IV, V, vi, ii) | 0 | **0.25** | 0.5 |
| 4-cycle plus I→IV shortcut | 0 (non-lazy g = 0, period 2) | 0, except I-IV 0.25 | 0.34 |
| All 4 chords inter-connected | 0.667 | 0.667 | 0.667 |

**Hand check, lazy hub edge I-IV:** m_I = ½ on I, ⅛ per spoke; m_IV = ½ on IV, ½ on I. The ½ at I and the ⅛ at IV stay put; the ⅜ on V, vi, ii each travels 2 steps to IV, cost ¾; so kappa = ¼.

**What the table shows.** A triangle gives positive curvature. A 4-cycle gives zero. Here g >= min kappa holds every time, as Prop. 29 predicts.

## 3. Is the measure from the notes?

Not as published (pure mathematics). It becomes a notes-only measure once P is the walk and a chord-graph distance is d: no audio, popularity or lyrics enter.

## 4. What is proved and what is assumed

Everything in the paper is a theorem, so there are no effect sizes. Two things matter for us.

- **The bounds point one way.** Positive curvature *forces* a large gap, fast mixing and concentration. A large gap does *not* force positive curvature. The 4-cycle has lazy g = 0.29 with kappa = 0.
- **The bound needs the minimum.** It uses the smallest curvature anywhere in the graph, so one bad edge makes it vacuous.

**My check.** I made 300 random weighted directed graphs with 4-7 nodes (connected, no dead ends), using the lazy walk:
- g >= min kappa held in all 300.
- min kappa was positive in only 69 of them.
- Mean edge curvature and lazy g had a rank correlation of about 0.50, so they are related but not the same.

Ollivier notes his concentration and log-Sobolev constants are loose; the variance bound is sharp in several examples. Nothing addresses a noisy, estimated P.

## 5. Lasting love and covers

The paper says nothing directly about songs, love or covers.

**Extrapolation (labelled, untested).**
- **Positive curvature:** chord walks where neighbouring chords lead to overlapping next chords. Shared destinations, triangles and a strong home chord all produce this. Such a song forgets where it started quickly, and any smooth "harmonic feature" settles near its average wherever you drop in. That might mean easy to learn and easy to re-harmonise.
- **Zero or negative curvature:** cycles of four or more, and branching tree-like moves. Neighbouring chords send you to different places, so position in the progression carries information for longer.
- **Link to covers.** Our one finding is that less within-section repetition predicts more covers. One might guess that low-curvature (more "directional") walks get covered more. The paper gives no reason to expect either sign.

## 6. Methods for tonight's experiments

**Defaults to fix in advance:** laziness alpha = 1/2 and d = unweighted shortest path on the undirected support of P. With those fixed, no free settings remain. Use an exact LP for W1 (scipy `linprog` or POT `ot.emd2`). With 6 chords there are about 15 pairs, so this takes milliseconds.

**M1. Move-weighted mean curvature, kbar.**
- For every observed chord change x→y, compute kappa(x,y) with m = lazy rows.
- Average over changes, weighted by count. Also report the unweighted mean over edges.
- This is the main candidate predictor.

**M2. Minimum curvature, kmin, plus the slack.**
- kmin is the smallest edge kappa. By Prop. 19 it equals the minimum over all pairs; I verified this on all 300 test graphs.
- Report g_lazy - kmin, which Prop. 29 guarantees is at least 0. A large slack means the song mixes fast for global reasons, such as a hub, not local ones.

**M3. Laziness-free version, kLLY.**
- Compute kappa at alpha = 1/2 and alpha = 0.9, and divide each by (1 - alpha).
- If the two agree, report the Lin-Lu-Yau limit. Bourne et al. show kappa_alpha is linear in alpha on [1/2, 1] for graph walks.
- This removes the arbitrary 1/2.

**M4. Curvature along the timeline.**
- Give each chord change in the sequence its edge kappa.
- Average within sections and compare with the repetition measure, to check this is not repetition renamed (as was done for g).

**Pitfalls on tiny graphs.**
- **Laziness is required.** Non-lazy walks on cycles, stars and other bipartite or periodic graphs return kappa ≤ 0 and g = 0 purely from parity, as in table rows 2-4. Compare g and kappa on the same lazy chain. If the earlier g used the non-lazy P, recompute it: the lazy eigenvalues are alpha + (1 - alpha)·lambda.
- **Dead ends.** A chord with no outgoing move, such as the last chord of a clip, has an undefined row. Wrap each clip back to its first chord, or give the row a self-loop, and state the rule.
- **Degree and triangle effects.** Curvature on a sparse graph mostly counts triangles and shared neighbours (Jost-Liu). Hubs with many spokes pull values down. Control for the number of distinct chords and edges, or residualise on them.
- **Discreteness and ties.** Values come in small fractions, such as 0, ¼, ½ and ⅔, so rank tests carry many ties. Use tie-aware Spearman correlation or permutation tests. A tie between optimal couplings does not change the W1 value.
- **Noise.** Each row rests on about 3 observed moves. Report split-half reliability for kbar against the 0.58 found for g before trusting it.
- **Non-reversibility.** The definition and the finite-space gap bound are fine for non-reversible chains. Concentration and variance results that need reversibility (Cor. 30, part of Thm 40) do not transfer unless you use the reversibilised chain (P + P*)/2.

## 7. Leads

1. **Lin, Lu, Yau (2011), "Ricci curvature of graphs"** (Tohoku Math. J.). The laziness-free limit; basis for M3.
2. **Jost, Liu (2014), "Ollivier's Ricci curvature, local clustering and curvature-dimension inequalities on graphs"** (Discrete Comput. Geom.). Curvature bounds from triangle counts; explains the degree pitfall.
3. **Bauer, Jost, Liu (2012), "Ollivier-Ricci curvature and the spectrum of the normalized graph Laplacian"** (Math. Res. Lett.). Two-sided eigenvalue bounds, including the top end that matters for periodic songs.
4. **Bourne, Cushing, Liu, Münch, Peyerimhoff (2018), "Ollivier-Ricci idleness functions of graphs"** (SIAM J. Discrete Math.). Curvature is piecewise linear in laziness; justifies M3.
5. **Ollivier (2010), "A survey of Ricci curvature for metric spaces and Markov chains"** (Adv. Stud. Pure Math. 57). The author's follow-up, with open problems.

Leads come from prior knowledge, not fetched tonight. The paper also cites Sammer (2005 thesis) on transport and spectral gaps.
