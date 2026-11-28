# Card 2: Gaeta, Garetto, Ruffo & Flammini (2022), quality vs popularity in cultural markets

## Citation and copy read

Rossano Gaeta, Michele Garetto, Giancarlo Ruffo (Univ. of Turin) and Alessandro Flammini (Indiana Univ.). "Reconciling the Quality vs Popularity Dichotomy in Online Cultural Markets." *ACM Transactions on Information Systems*, 2022, DOI 10.1145/3530790. arXiv:2204.13536, v1 only, posted 28 Apr 2022. I did not check the journal volume or issue.

Copy read: the arXiv HTML (v1), via WebFetch in two passes, plus the abs page. That covered the whole body, Sections 1 to 8, Appendices A to E (proofs) and the bibliography (refs 1 to 54). The text of reference 53 was cut off in the HTML. From the in-text arXiv id it is Iñiguez et al., arXiv:2104.13439. The end of Appendix C was garbled in the source.

## Claim and data

This is a pure theory paper with no empirical data. The model works like this:

- **Items.** There are N items with a hidden quality ranking. Each item has a popularity weight that starts at 1 and goes up by 1 every time the item is chosen. In other words, the model is a Pólya urn, a rich-get-richer process.
- **Users.** Each user is shown K items and always picks the best of them. K is the user's "quality discrimination power."
- **Popularity bias.** The platform picks which K items to show with probability proportional to rank^(−α), where rank is the item's current popularity rank. α = 0 means a uniform random menu. Large α means only the current top sellers are shown.
- **Variants.** One adds a fraction of "naïve" users who always take the number-one item. Another adds several user classes that disagree about quality.

Main results, in plain words:

1. **No popularity bias (α = 0).** If users compare just two items (K ≥ 2), popularity order converges to quality order almost surely (Prop. 3.1).
2. **Moderate popularity bias (0 < α ≤ 1).** The urn can lock into a wrong ranking, usually with the top items swapped. The number of items each user must compare to rule this out (K_min) grows without limit as the catalogue grows (Prop. 4.2).
   - Example: a 100-item catalogue at α ≈ 0.5 needs K ≥ 9.
   - With α = 1, K = 3 is enough for up to 19 items, and K = 4 is needed for 50.
   - The paper states that wrong lock-ins are not rare events (Remark 4.1). Random starting weights make early mistakes crystallize more often.
3. **Strong bias (α > 1).** K_min levels off at a constant.
4. **Naïve users.** K_min rises as the share of users who simply follow the leader rises. Once half the users do this, no amount of discernment by the others is enough.
5. **Diverse tastes.** When user classes disagree about quality, popularity concentrates less and the average quality of what gets chosen drops.
6. **Average quality.** In the correct equilibrium, the average quality of chosen items rises with both α and K (Prop. 5.1). So popularity bias is not purely harmful: it concentrates attention on the best items, at the cost of diversity and of the risk of locking in a wrong ranking.

## Is the measure from the notes?

No. "Quality" is an abstract, unobserved rank that is assumed to exist. It is defined as the order that independent users would produce if they compared items without social signals. Popularity is a count of choices. Nothing in the paper measures any property of the items themselves.

## Effect size and how it was checked

The evidence is theorems with proofs (Appendices A to E), exact enumeration of stable rankings for small N, a randomized search for larger N, and Monte Carlo runs of the urn (N = 10, K = 5, 10^6 runs per setting).

The paper does not re-analyse MusicLab. MusicLab and its follow-ups (Salganik and Watts 2008/2009; Krumme et al. 2012; van de Rijt et al. 2014; Muchnik et al. 2013) appear only as motivation. The paper gives no estimate of how much real-world success is quality and how much is luck.

The sizes it does report are counts and settling times:
- the number of stable rankings (for example, 4 for N = 10, K = 2, α = 1);
- the share of starting points that lead to each stable ranking (for example, 1/2, 1/3 and 1/6 for N = 4);
- settling times on the order of 10^6 choices, which are longer at higher α.

## What it says about lasting love and covers

What helps the project:
- The paper treats quality as real and as able to win over time. Under fair exposure, popularity order eventually matches quality order, and only light comparison by choosers is needed.
- Covering a song is a deliberate choice by a musician who knows many songs, so cover artists plausibly have a high K. That favours quality winning in the long run.

What cuts against the project:
- Quality wins only under specific conditions: exposure that is uniform or extremely popularity-driven, choosers who compare enough items, and fewer than half the choosers following the crowd.
- Radio, charts and "standards" repertoires sit in the harmful middle range of popularity bias. Huge catalogues make it worse, because the comparison needed keeps growing with catalogue size. Under those conditions, an early lucky lead can freeze into a permanent wrong ranking, and that outcome is common, not rare.
- Even the correct equilibrium needs about 10^6 choices to settle. A song with roughly 10 to 200 covers is far from settled, so its raw cover count still carries much of its early luck.
- When tastes really differ (several user classes), there is no single quality order to recover.
- Raw counts mix together three things: quality, the starting boost, and exposure bias. A measure computed from the notes should therefore track a luck-corrected fitness better than raw counts.
- If the notes measure predicts raw counts better than it predicts fitness, it is probably picking up hit-making or exposure features, not quality. That is a falsifiable check the Skeptic should insist on.
- The Discogs-VI sample is about 2,900 mostly-hit songs. That is a sample of songs that already won the early lottery, which shrinks the range of fitness and builds in selection bias.

## Methods or measures it suggests for this pass

1. **Fit a fitness model to cover timing.** For each song, take the release years of its covers as a sequence of events. Model the cover rate in year t as rate = η × (prior covers + m) × A(t − t0).
   - η is the song's fitness.
   - m is a small baseline so the first cover can happen at all.
   - A is an aging curve shared by all songs. A lognormal works, as in Wang, Song and Barabási (2013).

   Fit η by maximum likelihood on annual counts using a Poisson or negative-binomial model, with one shared aging curve plus a log-η for each song. The η estimate is the luck-corrected quality.
2. **Separate the lucky start from later growth.**
   - Define the "start" as the number of covers in the first 5 years after the original release, or the time until the 3rd cover.
   - Define "per-capita growth" as later covers divided by prior covers, with the aging curve removed.

   Under pure preferential attachment with equal fitness, per-capita growth should not depend on the song once the head start is accounted for. Real differences in η show up as songs whose per-capita rate stays high after conditioning on their head start.
3. **Test the notes measure.**
   - Regress η-hat and raw count separately on the notes measure, with release decade and genre as controls. Compare out-of-sample rank correlations, using a bootstrap over songs.
   - Also test whether the notes measure predicts later per-capita growth after controlling for the first-5-year count. This is the cleanest "quality, not luck" test.
   - As a null check, simulate fitness-free urns with the fitted aging curve and starting conditions, and see how much η spread pure luck produces. Report how much the real spread exceeds it.
4. **Diagnose lock-in.** The paper's model predicts wrong swaps among the very top songs. Check whether the notes measure disagrees with raw counts most at the top.

## Leads

1. Wang, Song & Barabási (2013), "Quantifying long-term scientific impact," *Science*, DOI 10.1126/science.1237825. This is the template for estimating fitness from the timing of citations, with aging, preferential attachment and fitness combined.
2. Bianconi & Barabási (2001), "Competition and multiscaling in evolving networks," *Europhys. Lett.*, arXiv:cond-mat/0011029. The original fitness model.
3. Ciampaglia, Nematzadeh, Menczer & Flammini (2018), "How algorithmic popularity bias hinders or promotes quality," *Sci. Rep.*, DOI 10.1038/s41598-018-34203-2 (arXiv:1707.00574). Simulations from the same group that put numbers on the trade-off between quality and popularity bias.
4. Krumme, Cebrian, Pickard & Pentland (2012), "Quantifying social influence in an online cultural market," *PLoS ONE*, DOI 10.1371/journal.pone.0033785. Fits a model to MusicLab data that separates appeal from the effect of being listed and seen.
5. Iñiguez, Pineda, Gershenson & Barabási (2022), "Universal dynamics of ranking," *Nat. Commun.*, arXiv:2104.13439. Covers ranking turnover in open systems, where new items keep arriving, which is the case for cover catalogues.

(Venue details for leads 1 to 5 come from my memory and still need checking. Only the arXiv id for lead 5 is cited in the paper itself.)
