# Round two: the evolutionist

## 1. The two strongest ideas from the others, and what my field adds

**Sceptic, Idea 1: hymn tunes with texts and tunes crossed** (the songwriter and I proposed the same laboratory; the sceptic's crossed model is the best form of it). To a biologist this is a reciprocal-transplant experiment: the same tune grown in many texts, the same text in rival tunes. Two corrections.

- Hymnals are not independent witnesses. Editors copy earlier hymnals, and denominations hold lineages of them. Counting hymnals counts ancestry, the same error as counting species without a family tree. Fix: add a random effect for hymnal lineage (denomination x publisher line), or count only first adoptions into a lineage.
- A stronger measure is hiding in the same data. Each revision of a hymnal line is a selection event with a known denominator: tunes present in edition k either survive into edition k+1 or are dropped. That gives a life table with the dead observed, which no hit dataset has. Compute the hazard h_j = P(tune j dropped at a revision | present before it) by discrete-time survival regression on age, metre and lineage. The tune's fitness is its frailty term. Also, in rival-tune contests, control which tune held the text first; incumbency is cumulative advantage.

**Physicist, Idea 1: the stiff-sloppy spectrum of the version cloud, with the predictive step.** This is my conserved core in better geometry, and its predictive step (learn identity directions from covered works, then score any single recording) is what breaks the circularity. Two corrections.

- Low variance across covers is not conservation unless there is a neutral baseline. Everyone keeps 4/4; that tells us nothing. Geneticists divide the observed rate of change by the rate expected under no constraint. Here: for feature f and a cover by performer a of an original by performer o, the expected change is the distance between a and o on f in their OTHER, non-cover repertoire. Constraint ratio c_f(w) = mean squared change of f across covers of w / mean squared a-to-o repertoire difference on f. Below 1 means the song holds that feature against the performer's habits (stiff); near 1 means free. Build the identity space from c_f, not from raw variance. This also removes the leak the physicist worried about, that a wide cloud is only a diverse set of coverers.
- Covers are a tree, not a cloud of independent draws. Most later versions copy one earlier version, often not the original. Cluster versions into lineages first and weight lineages, not versions, or one famous cover's twenty imitators will look like a stiff core.

## 2. The weakest idea in the room

My own Idea 5, transmissible surprise, and it takes the mathematician's "eigenvectors of the telephone game" down with it as far as hits are concerned. Exact reasons:

1. There is no telephone game for recorded songs. A chain accumulates error because each singer learns from the last. A hit has a master copy; every coverer returns to the record (or to one famous cover). Transmission is star-shaped, so errors do not compound and no attractor is ever approached. The sung-chain results describe traditions without a master and do not transfer.
2. The copier is synthetic. A simulated lossy learner is "robustness under perturbation" again with a fancier noise model, and that already failed.
3. Nearness to the attractor is the universal part (the physicist's own argument): every followable tune is near it, so it cannot rank them. The components it reduces to (small intervals, simple rhythm, singability) are already on the failed list.
4. My statistic was a maximum over windows, which grows with song length for no musical reason.

The idea stays alive only where chains are real: session tunes and hymn tunes, and there real variants should replace the simulation.

## 3. A new idea that exists only because the papers are read together: which VERSION becomes the template

Sources: the producer's claim that a bare record is "legible" and so invites covers; the sceptic's within-work design that holds the page exactly fixed; the physicist's free dimensions; my point that covers form lineages.

Plain words. Within one work, some versions have children and some do not. Later coverers of "Hallelujah" copy Cale and Buckley, not Cohen. So ask, with the song held constant, what sound makes a version the one others copy. That measures the selection pressure on sound directly, with no popularity yardstick at all, and it tests legibility as a cause. It also carries a warning for every page test so far: if the template is often not the original, the transcriptions graded a specimen that is not the one being reproduced.

Mathematics. For work w, versions v with date t_v and feature vector x_v. For each later version c, assign a parent among earlier versions by similarity in the free dimensions (tempo ratio, key, duration, section order, title variant, aligned chroma): P(parent(c) = v) = softmax of -distance(c, v). Fecundity k_v = sum over c of P(parent(c) = v). Fit k_v ~ Poisson(exp(a_w + b . x_v + g * log fame_v + log years available)), with a_w a per-work intercept. The vector b is the selection gradient on sound with the page fixed. Producer's prediction: b positive on vocal exposure and sparseness. Then the Price equation splits the change in a work's average sound across cover generations into selection (which versions are copied: Cov(k, x)/mean k) and transmission bias (how copies differ from parents: E[k * change in x]/mean k). If covers everywhere drift the same way (slower, sparser, sadder), that direction is what the population is selecting for.

Data. Full version needs per-version features and dates (Da-TACOS plus SecondHandSongs dates; verify both). A miniature runs today: among works with two or more charting versions, conditional logistic regression of which version is more loved now on the difference in their Essentia and Spotify readings.

Wrong if. b is zero within works, or the original is the parent in nearly all cases (then there is no lineage structure to exploit).

## 4. Votes

- First test with data in hand: the sceptic's Idea 2, which is my breeding value. Take works that charted in more than one artist's hands and estimate what share of a recording's later love belongs to the work (intraclass correlation, original's fame controlled, checked where the later version is the bigger one). It needs no musical feature, so it cannot fail for want of the right one, and it fixes the ceiling every other result is judged against. The within-work regression of love on sound comes free from the same table.
- First test needing new data: Hymnary's tune x text x hymnal table, run as the sceptic's crossed model plus the edition-to-edition survival analysis above. If Hymnary cannot be had, The Session's dump on GitHub.

## 5. The theory the room is converging on, and whether I believe it

A great song fixes very little very firmly and leaves the rest open (room around the voice on the record, room for the next performer across records), so greatness is the amount of freedom a song permits per unit of identity it insists on, at a fixed distance from other songs.

I half believe it. As a description of standards I give it 70%. As something predictable from a single specimen before any cover exists, 30%. Three cautions. Six people reading one brief and all seizing on "sparse" is not six independent confirmations. Measured on the cover cloud it is close to the yardstick restated, so only the single-specimen prediction counts as evidence. And in biology openness to variation is almost never what selection acts on; it is a by-product. A song may be covered because it is cheap to cover, which is reproduction without love. I expect this theory to explain "covered" well and "still loved" poorly, and the sparse-recording result to shrink inside narrow year bands.
