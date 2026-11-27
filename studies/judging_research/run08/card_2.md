# Card 2 (counter-evidence): Evans & Giometto, turnover in neutral copying models

## 1. Citation and copy read

T. S. Evans and A. Giometto (Imperial College London), "Turnover Rate of Popularity Charts in Neutral Models," arXiv:1105.4044 (2011). The copy shows no journal reference, DOI or version number; its appendix says it "will not appear in the published version", so a published version may exist (unconfirmed).

Copy read: both ar5iv URLs were blocked (permission request unanswered). WebFetch of arxiv.org/abs/1105.4044 returned the full text (abstract, all sections, conclusions, appendix, 14-item bibliography), read in five passes. I also skimmed Bentley, Lipo, Herzog & Hahn 2007 (hahnlab PDF) for context only.

## 2. Main construction and results

**Models.** N individuals each hold one artefact, and artefacts have no intrinsic value.
- **Wright-Fisher (WF):** each step, everyone updates at once. With probability 1-mu a person copies the artefact of someone chosen at random from the previous step. With probability mu they invent a brand-new one.
- **Moran:** one random individual updates per step, using the same copy-or-invent rule.

**Turnover.** The chart is the top y artefacts by current frequency. z is the number of artefacts that leave the chart plus the number that enter, between successive steps. Bentley et al. counted entries only, so z here is about twice theirs. In this paper's units, Bentley's formula reads z = 2·sqrt(mu)·y, with no dependence on N.

**Results (all from simulation).**
- **WF, Nmu < ~0.15·y:** the chart is not full, because fewer than y artefacts survive. z = 2Nmu, which is about Nmu fresh innovations entering and about Nmu dying each step. Fit: exponents of mu, y and N equal 1.000, 0.000 and 1.000, with prefactor 1.997.
- **WF, Nmu > ~0.15·y** (Bentley's regime): z = d·mu^a·y^b·N^c gives a = 0.550, b = 0.860, c = 0.130, d = 1.38 for N from 180 to 3,993, and a = 0.558, b = 0.879, c = 0.091, d = 1.79 for N from 1,000 to 13,000 (y < N/100). Bentley's exponents (1/2, 1, 0, 2) are statistically excluded, and z depends weakly on N, perhaps logarithmically. At N of 100,000 to 144,000 (Table I), Bentley's formula overestimates z by 7-18%; the large-N fit is within about 6%.
- **Moran:** there is a critical point near mu_c ≈ (N/y)^(-3/2). Below it, z = 2mu per update, independent of y and N (fitted d = 2.02). Above it there is no power law, and z collapses onto a function of y/N.

**Analytic vs simulated.** Only the relaxation eigenvalues of F2 are analytic (from the literature), used to set burn-in (4/mu WF, 4N/mu Moran). Every turnover law is an empirical fit to about 6,000 WF and 350 Moran parameter sets; the low-mu laws get only a heuristic explanation.

**Popularity distribution.** The paper only states that WF frequencies follow a power law with a cutoff (Ewens's results), and gives no exponent.

**Data.** None is fitted. The paper cites Bentley's baby-name, dog-breed and album-chart results, and notes that real populations (about 10^6 per year) are larger than anything simulated.

## 3. Is anything here from the notes?

No. This is a null model with no content at all: artefacts differ only by luck and age. For our outcome (distinct artists recording a song, and when), it says rich-get-richer copying alone can produce heavy-tailed cover counts and steady churn at the top. If our version counts behave like this null, the outcome carries little signal the notes could predict.

## 4. Proved, assumed, effect sizes, checks

**Assumed:** equal attractiveness; uniform copying from the previous generation only (no long memory, no network); constant mu; steady state.

**Derived:** nothing new analytically. The contribution is the empirical regime map and the finding that Bentley's sqrt(mu)·y law is approximate in WF and fails in Moran.

**Effect sizes:** the mu and y exponents are off from Bentley's by about +10% and -14%; z varies by about 50% across the simulated N range.

**Checks:** steady state via F2(t); ensembles sized for at most 10% error on z; log-linear fits on geometric grids. The authors' caveat: the practical gap from Bentley may be small, but WF vs Moran changes the scaling qualitatively.

## 5. Lasting love and covers

**Strongest honest case for content-free covers.** Unbiased copying plus a small innovation rate reproduces stable chart turnover (Bentley found a near-constant 5.6% weekly album-chart turnover over 20 years), heavy-tailed popularity, and turnover near-linear in chart size. A song that happens to collect early versions becomes a bigger target for later ones, so "standards" could partly be winners of a compounding lottery. Salganik-type experiments show social influence inflates inequality and unpredictability.

**Limits of that case:**
1. A neutral fit does not prove neutrality. Bentley concedes other models fit the same aggregates, and this paper shows even the neutral formula depends on modelling details.
2. Turnover is a weak statistic: biased copying (Acerbi & Bentley) shifts z only modestly.
3. Bentley's own data hold clear non-neutral events (Dalmatians after a Disney re-release).
4. Covers are not uniform copies of whatever is current. Long memory, publishers and original-artist fame are non-content, non-neutral forces the null cannot separate from notes.
5. Turnover measures churn, not which songs last; long survival is exactly where hidden fitness would show.

## 6. Methods and measures for this pass

**Setup.** For each song, let t0 be its first year. Let C(a) be the number of distinct new artists with an earliest release at age a (age 1 = t0), and let K10 be the cumulative count of distinct artists through age 10, including the original. Keep songs with t0 at least 30 years before Discogs coverage thins out, and fit Hooktheory (~3,000) and Lakh (~2,400) separately.

**(a) Martingale / linear-attachment test.** Let L = the number of distinct new artists at ages 11-30. Fit a negative-binomial GLM:

log E[L] = cohort(t0, 5-year bins) + beta·log(K10 + c0) + gamma·X

Here c0 is an initial-attractiveness offset (fitted, or fixed at 1) and X is anything known by age 10 (notes features, original artist's fame, genre). Under linear preferential attachment with a shared aging curve, a song's share of all cover activity is a martingale, so beta = 1 and gamma = 0. **Favours neutrality:** beta within about 0.1 of 1 and gamma ≈ 0, out of sample. **Heterogeneous fitness** (content or fame): beta > 1, since fit songs start high and keep growing. **Saturation/fatigue:** beta < 1.

**(b) Distribution shape.** *Simon/Yule:* with alpha = share of all clique recordings that are first versions, versions per song should have tail P(k) ~ k^-(1+1/(1-alpha)), about 2 for small alpha. Fit with Clauset-Shalizi-Newman MLE above k_min. *Ewens/Watterson:* for each year's n cover recordings over K distinct songs, compare F = sum of p_i^2 with its Ewens expectation given n and K. F well above implies conformity or selection; below implies anti-conformity. Caveat: our songs are pre-selected hits, so trust only the upper tail and the conditional tests.

**(c) Content ceiling.** Simulate the null: a Polya urn keeping each song's observed K10, t0 and the observed yearly total of new covers, allocating each cover with probability proportional to (K + c0) × the cohort's aging factor. Over 1,000 replicates compute the variance of log(L+1) given K10. Then content share ceiling = (observed residual variance - urn variance) / observed residual variance. That is the most any song-level attribute, notes included, could explain beyond copying momentum. A per-song fitness random effect (Wang-Song-Barabasi style) gives the same ceiling as a parameter.

**(d) What would contradict neutrality.** A pre-registered notes score (features fitted on held-out songs) that predicts L with gamma > 0 holding log K10, cohort and original-artist fame; predicts "sleeper" revivals among songs with K10 = 1; and survives a permutation test shuffling scores within K10 × cohort cells. **gamma = 0 with beta = 1** supports copying for the late phase but does not clear the notes, because content may have acted through K10 itself. To test that, check whether the notes score predicts K10 relative to the original's chart success.

**(e) Cover-chart turnover.** For each year, rank songs by new versions over a trailing 5-year window and compute z for y = 5, 10, 20, 40, 80. Estimate mu as the yearly share of versions going to songs with no earlier version. Compare with the Evans-Giometto large-N fit (a = 0.558, b = 0.879) and with 2y·sqrt(mu). Near-zero turnover at small y (evergreens holding the top longer than the null allows) favours selection; turnover near-linear in y matching the fit favours neutrality.

## 7. Leads

Citations and DOIs below are from memory and should be checked before use.

1. Bentley, Lipo, Herzog & Hahn 2007, Evol. Hum. Behav. 28:151, doi:10.1016/j.evolhumbehav.2006.10.002 (the source of the formula).
2. Acerbi & Bentley 2014, "Biases in cultural transmission shape the turnover of popular traits," Evol. Hum. Behav., doi:10.1016/j.evolhumbehav.2014.02.003.
3. Salganik, Dodds & Watts 2006, "Experimental study of inequality and unpredictability in an artificial cultural market," Science 311:854, doi:10.1126/science.1121066.
4. Wang, Song & Barabasi 2013, "Quantifying long-term scientific impact," Science 342:127, doi:10.1126/science.1237825 (fitness plus attachment plus aging, a template for (a) and (c)).
5. Kandler & Shennan 2013, "A non-equilibrium neutral model for analysing cultural change," J. R. Soc. Interface, doi:10.1098/rsif.2013.0302.
