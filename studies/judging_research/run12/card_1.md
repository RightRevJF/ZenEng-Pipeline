# Card 1: Freeman & Jordan, extensive condensation in preferential attachment with fitness

## Citation and copy read
Nic Freeman and Jonathan Jordan (University of Sheffield; authors confirmed). "Extensive Condensation in a model of Preferential Attachment with Fitnesses". arXiv:1812.06946 [math.PR], v1 posted 17 Dec 2018, v2 posted 23 Apr 2020. The arXiv page gives no journal reference. I read the arXiv HTML (dated April 2020, i.e. v2) in full through WebFetch: introduction, model, theorems, Sections 3 to 6, Appendix A and the 22-item bibliography. Proofs reached me as lemma-by-lemma summaries, not line by line.

## Claim and data
**Plain.** This is pure theory with no data. The model (PAC, "preferential attachment with choice") works like this:
- Vertices arrive one at a time, each with a random fitness.
- A newcomer draws R existing vertices, each with probability proportional to its current number of links.
- It links to the fittest vertex in that draw. Popularity decides who gets considered; fitness decides who gets chosen.

Results:
1. Every vertex gains links forever, but no fixed vertex keeps a positive share of all links.
2. The link-weighted fitness distribution converges to a closed-form limit, built from a branching process.
3. If R averages more than 2, condensation happens: a non-vanishing share of links sits on near-maximal fitness. At 2 or below it does not.
4. The condensation is extensive. One vertex holds a positive fraction of the graph for a while, then a fitter newcomer displaces it. The authors call this "a succession of ever fitter vertices" toppling earlier leaders.

In the classic Bianconi-Barabasi model (link probability proportional to fitness times degree), Dereich, Mailler and Moerters (2017) proved the condensation is non-extensive: no single vertex keeps a positive fraction.

**Precise.**
- *Model.* Start from one vertex with a self-loop. Fitnesses F are i.i.d. and absolutely continuous on [0,1], with essential supremum 1. R takes values in {1,2,...} with E[R] finite. Each newcomer samples R vertices with replacement, proportional to degree, and adds one edge to the fittest. The graph's law depends only on fitness ranks.
- *Definitions.* mu_n is the degree-weighted fitness measure. ell_n is the same measure using only the largest-degree vertex in a set. Condensation means lim_eps liminf E[mu_n(B_eps(1))] > 0. Extensive condensation is the same with ell_n in place of mu_n.
- *Thm 2.3.* deg_n(v) tends to infinity almost surely, while deg_n(v)/n tends to 0 in probability.
- *Thm 2.4* (needs E[R^2] finite). mu_n converges almost surely to mu, where mu([0,a]) = 1/2 P[F<=a] + 1/2 (P[L finite, max_{i<=L} C_i <= a] + 1{a=1} P[L infinite]). Here L is the number of leaves of a Galton-Watson tree with P[M=0]=1/2 and P[M=m]=1/2 P[R=m], and the C_i are i.i.d. copies of F.
- *Cor 2.5.* Condensation happens if and only if E[R] > 2.
- *Thm 2.6.* Condensation is extensive, with no persistent hub.
- *Section 6.* Under affine attachment the threshold becomes E[R] > 2+alpha. With several edges per newcomer the threshold is unchanged.

**Method.** Edges are split into half-edge "balls". Each new vertex adds two balls:
- a source ball, carrying the new vertex's own fitness;
- a cue ball, taking the maximum fitness among its R sampled candidates.

Traced backwards, this gives a branching-coalescing genealogy. A ball's fitness equals that of the fittest source among its ancestors. The genealogy behaves like a tree far back in time. In a window around time n^beta, with beta = (E[R]-2)/E[R], it coalesces and its fluid limit is logistic. The fittest source born in that window is an ancestor of a positive fraction of the graph at time n. The paper draws an analogy with selective sweeps in population genetics. It reports no simulations.

## Is the measure from the notes?
No. Fitness is an abstract, unobserved label, and the outcome is network degree. The paper says nothing about any kind of content.

## What is proved and what is assumed
**Proved rigorously:** Theorems 2.3, 2.4 and 2.6, and Corollary 2.5.

**Assumed:**
- one edge per newcomer;
- sampling exactly proportional to degree;
- i.i.d. continuous fitness, with the fittest candidate always chosen;
- finite moments of R;
- no ageing and no fitness that changes over time.

**Not proved:**
- the size of a leader's share (only a positive lower bound, never computed);
- any rate of decay;
- the conjecture in Remark 5.5 that a leader's share eventually vanishes almost surely.

**Tail of the fitness distribution:** in PAC, whether condensation happens depends on R, not on how the fitness distribution behaves near its maximum. In Bianconi-Barabasi that tail matters.

## Lasting love and covers (all extrapolation)
- Suppose a coverer considers only a few songs, weighted by how often they are already covered, and picks the best. Then PAC predicts waves:
  - A high-fitness song's share of *new* covers rises along a roughly logistic curve, holds a sizeable fraction for a time, then fades as fitter later songs win the comparisons.
  - A low-fitness song keeps a trickle of covers, since every vertex's degree grows without bound, but its share falls to zero fast.
- On this reading, lasting love means continuing to win comparisons against newer rivals. Total covers mostly reward age and early luck.
- Whether one song ever takes an extensive share depends on how many candidates a coverer compares (E[R] > 2). Under pure Bianconi-Barabasi, even the fittest song's share shrinks. Which regime we are in can be tested.
- Caveat: about 2,900 pre-selected hits with coarse release years is not one growing graph with a single arrival per step.

## METHODS OR MEASURES IT SUGGESTS FOR THIS PASS'S EXPERIMENTS
**(a) Fitness from cover years alone.** Build a song-by-year panel from Discogs-VI: k_i(t) is song i's cumulative covers before year t, and c_i(t) is its new covers in year t. Only songs already released by year t count.
1. *Bianconi-Barabasi estimator.* Treat each new cover as a choice among the songs that exist, with weight (k_i+1)exp(theta_i). Fit theta_i by conditional-logit (or Poisson) maximum likelihood. Then theta_i is log fitness.
2. *PAC estimator.* Only ranks matter. Song i wins a cover with probability of about (k_i/K) times R times s^(R-1), where s is the degree share of less-fit songs. Fit the fitness ranks plus a single R by maximum likelihood or MCMC (Plackett-Luce style).
3. *Simple proxy.* Divide covers more than 15 years after release by the number that preferential attachment alone would expect, k_i times the period's total divided by total degree. A ratio above 1 means excess fitness.
4. *Condensation test.* In rolling windows, plot the top song's share of new covers against total cover volume. A flat share with leaders changing over time fits PAC. A falling share fits Bianconi-Barabasi.

**(b) Do notes beat counts?**
- Add notes features z_i to the choice weight: (k_i+1)exp(b·z_i). Candidate features are the share of melody time on the top 2 or 3 pitch classes (or pitch-class entropy) and the chord-repetition rate.
- Fit on covers up to year T and score the log-likelihood of covers after T. Compare against a model with log(count by year T) as the only covariate, and against a model with both.
- Stratify by release decade to remove age effects.
- Also compute Spearman correlations of fitness from (a) with z_i and with the early count, bootstrapping over songs.
- *Notes analogue (metaphor only, no theoretical link).* mu_n versus ell_n is "mass near the top" versus "the single largest holder". For a melody, the matching quantities are the share on the top pitch class and the share on the top-k pitch classes, which together give a condensation index.

## Leads
1. G. Bianconi & A.-L. Barabasi, "Competition and multiscaling in evolving networks", Europhys. Lett. 54 (2001), DOI 10.1209/epl/i2001-00260-6. The base model behind the theta estimator.
2. S. Dereich, C. Mailler & P. Moerters, "Nonextensive condensation in reinforced branching processes", Ann. Appl. Probab. 27(4) (2017). The contrasting result, where the tail of the fitness distribution matters (arXiv id not checked).
3. C. Borgs, J. Chayes, C. Daskalakis & S. Roch, "First to market is not everything: an analysis of preferential attachment with fitness", STOC 2007. Separates the first-mover advantage from quality.
4. J. Haslegrave, J. Jordan & M. Yarrow, "Condensation in preferential attachment models with location-based choice", arXiv:1806.10959 (2018). A sister model with choice.
5. D. Wang, C. Song & A.-L. Barabasi, "Quantifying long-term scientific impact", Science 342 (2013), DOI 10.1126/science.1237825. Not cited in this paper. It estimates fitness from the timing of citations and could be applied directly to cover years.
