# Card 2: Which Irish tunes musicians keep learning

## Citation and link
McBride, John M., and Armand M. Leroi (2026). "Population Ecology of Tunes." arXiv:2609.09501 [q-bio.PE; cs.SD; physics.soc-ph], v1, submitted 8 September 2026. DOI 10.48550/arXiv.2609.09501. Licence CC BY-NC-SA 4.0. Preprint only; no journal reference yet.

- The ID in the brief, arXiv:2607.12673, is a different McBride paper (McBride and Fitch, on aligning Irish tune variants like protein sequences). The right ID was found with a search of arxiv.org.
- Copy read: the arXiv HTML, https://arxiv.org/html/2609.09501v1. I read all of it: abstract, introduction, results, discussion, methods and the 43 references. I checked the PDF, https://arxiv.org/pdf/2609.09501v1, for the figure labels and for any supplement.
- Not reached: the Supplementary Material (Figs S1 to S14, results on all 22,216 tunes, the Skellam birth-death model, curves showing each melodic feature's effect, the robustness check S5). It is cited throughout but is not in the HTML or the PDF, and no separate link is given. The paper also has no statement on whether its data or code are available.

## The claim, and the data it rests on
- **Corpus:** TheSession.org, the main online home of Irish traditional dance music. Tunes are posted in ABC notation, often in several "settings" (versions). Users add tunes to a personal "tunebook".
- **Data:** 820,752 tunebook adds for 22,216 tunes, logged weekly from December 2012 to March 2026 (695 weeks). The site owner supplied the data. A second weekly-totals set from GitHub (2019 to 2026) is used to rebuild the frequencies. Six tunes with bot-like bursts were removed (63 bursts).
- **What counts as success:** a per-tune fitness, β. It measures how much more often a tune is added than its current share of all tunebooks would predict. It is fitted in a birth-process model with a ridge prior. β ranges from −0.84 to +1.60 over the 11,791 tunes that reached at least 10 tunebooks. The authors treat a tunebook add as a stand-in for having learned the tune or meaning to learn it, while admitting it might only be a bookmark.
- **Claims:**
  1. Popularity is not neutral copying. Tunes really differ in fitness, with some tunes "systematically more likely to be learned than others". The per-tune model beats the neutral model by ΔAIC −57,700.
  2. Conformity (popular because popular) is weak: global exponent 0.024, or 0.048 with saturation. It is worth only about 3% of the gain from per-tune fitness.
  3. Prestige from recordings matters most. Melody matters a little, and simpler melodies do better.
  4. Tunes played together in sets are carried along with each other, like genetic hitchhiking.
  5. A single video can revive a dormant tune.
  6. Repertoire diversity still rises (entropy +0.37 bits; active tunes go from about 9,000 to over 22,000) because new tunes keep arriving. Among the 8,808 tunes present at the start, diversity slowly falls.

## The measure: from the notes or not?
Mixed. The outcome (tunebook adds) is musician behaviour, not notes. Nine predictors are fed to an XGBoost model:

- **Not notes (four):**
  - number of recordings on TheSession;
  - Discogs "have" counts for those recordings;
  - top Spotify popularity of matched tracks;
  - the tune's average tunebook count.
- **From the notes (five):** computed from the ABC text of each setting and taken as the median across settings:
  - pitch-class entropy;
  - note density (onsets per quarter note, repeated notes not counted);
  - LZ76 compression complexity of the pitch-class sequence;
  - mean absolute interval;
  - contour complexity (how often the melody changes direction).

All five are melody only. Harmony is not measured (session tunes carry no chords). Rhythm enters only through note density. Several other note measures were dropped early for collinearity, including range, number of distinct pitches and bar count.

## How big the effect is and how it was checked
- **Fit:**
  - The whole model predicts β with an out-of-fold r of 0.56. The cross-validated R² is 0.29 (in-sample 0.42). It uses 8,051 tunes with complete covariates, 5-fold cross-validation and inverse-variance weights.
  - The Fig. 2a legend shows a total of 0.24, which the text does not reconcile with 0.29.
- **Unique share of each group** (the R² lost when the group is removed):
  - social and recording prestige: 16 points;
  - average popularity: 1 point;
  - **melody: 3 points.**
  The marginal R² of melody on its own is not reported in the main text.
- **Direction:** In a GAM of partial effects, fitness falls as pitch(-class) entropy and note density rise. Simpler tunes do better on average. No slope or effect size is given in the main text; the curves are in the supplement I could not reach. The authors note that this goes against an earlier inverted-U (middling complexity best) reported for this site (Street et al. 2022).
- **Checks:**
  - AIC comparisons of neutral, frequency-dependent and per-tune models;
  - FDR-corrected per-tune Wald tests;
  - sliding 2-year windows to track fitness over time;
  - a popularity-only null model for sets: observed set pairs repeat up to 134 times, against at most 8 under the null.
- **Not done:**
  - no second platform or held-out time period;
  - no control for how long a tune has been on the site or how old it is;
  - recordings are both cause and effect, since a fit tune gets recorded and a recording raises fitness. The authors flag this.
- **Case studies:**
  - Maids of Selma: β rose to at least 0.7 after an October 2020 video with over 80,000 views, about one tunebook add per 500 views. Its set partner Lisnagun rose too.
  - The Bag of Potatoes is well recorded, including by the Chieftains, yet its fitness is negative (−0.32).

## What it says about the yardstick (lasting love plus covers), not only popularity
- **Closest match: the covers half.** A tunebook add is a musician choosing to learn and play a tune. That is close to the covers half of G, closer than streams or views. And β is growth beyond current popularity, so the design already strips out "popular because popular". That is the separation the project wants.
- **What melody adds is small.** In the purest tradition of musicians choosing tunes, melody adds about 3% of explained variance beyond prestige, and the larger signal is who recorded it. This matches the project's results so far: the note signal for covers is real but small (the covers study found 1.5 to 4%), and same-artist tests found nothing.
- **Direction:**
  - In this tradition, simpler, lower-entropy, less dense melodies spread better among players. That fits the covers study's Discogs-VI result: denser melodies did not win covers (notes a beat −0.036, p = .08).
  - It does not speak to the one replicated finding (moving chords), because harmony is absent here.
- **Fitness is not lasting love.** β is a rate of spread over 13 years, not lasting love. A newly fashionable tune can have high β. Decades-old tunes that hold steady sit near zero.
- **Different setting.** The material is instrumental dance tunes inside one tradition. The project's songs are sung popular hits, and the tunes here are not hits at all. Transfer is not guaranteed.
- **Cross-style breadth cannot be tested.** All the tunes here live within one style.

## One test Luthier could run on its kept tables
**Do simpler melodies get more covers among hits?** Use the 2,360 Hooktheory songs matched to Discogs-VI (median 6 covers), split into two halves by artist.

- **Measures:** compute the paper's five melody measures from the Hooktheory melody, using scale degrees taken as pitch classes relative to the key and the median across a song's sections:
  - pitch-class entropy;
  - note density with repeats not counted;
  - normalised LZ76 complexity of the pitch-class sequence;
  - mean absolute interval;
  - contour-change rate.
- **Outcome and controls:** log(1 + covers), with the covers study's controls: log views, first year, duration, number of Hooktheory clips, original artist or not, and chord repetition within a section. Holding chord repetition shows whether melodic simplicity adds anything beyond the moving-chords finding.
- **Prediction, written in advance:**
  - the partial β of pitch-class entropy is negative in both halves and pooled (p < .05);
  - LZ76 complexity is negative pooled;
  - note density is negative or zero, not positive.
- **Fails if:**
  - pitch-class entropy is positive pooled;
  - or it is negative in one half and positive in the other;
  - or |β| < 0.03 pooled.
- **Second reading** (same rule, a separate prediction): if Discogs genre tags allow it, use the number of distinct genres among a song's covers (cross-style breadth) as the outcome. Prediction: lower pitch-class entropy goes with more genres, on the idea that a plainer tune moves across styles more easily.

## Leads
1. **The role of population size in folk tune complexity.** Street, S. E., Eerola, T., Kendal, J. R. (2022). Humanities and Social Sciences Communications 9:152. https://doi.org/10.1057/s41599-022-01139-y. Reason: same site; reports the inverted-U for complexity against popularity that this paper contradicts. Needed to judge which holds.
2. **Predicting variation of folk songs: a corpus analysis study on the memorability of melodies.** Janssen, B., Burgoyne, J. A., Honing, H. (2017). Frontiers in Psychology 8:621. https://doi.org/10.3389/fpsyg.2017.00621. Reason: note features that predict which melody phrases survive oral passing-on, a direct "what lasts in the notes" study.
3. **Large-scale iterated singing experiments reveal oral transmission mechanisms underlying music evolution.** Anglada-Tort, M., Harrison, P. M. C., Lee, H., Jacoby, N. (2023). Current Biology 33(8):1472-1486. https://doi.org/10.1016/j.cub.2023.02.070. Reason: controlled experiment on which melodic shapes survive being passed on; separates memory bias from prestige.
4. **Neutral syndrome.** Leroi, A. M., Lambert, B., Rosindell, J., Zhang, X., Kokkoris, G. D. (2020). Nature Human Behaviour. https://doi.org/10.1038/s41562-020-0844-7. Reason: when popularity data look like chance copying, and how to tell real selection from drift. A guard for G.
5. **Detecting evolutionary forces in language change.** Newberry, M. G., Ahern, C. A., Clark, R., Plotkin, J. B. (2017). Nature 551:223-226. https://doi.org/10.1038/nature24455. Reason: a method for estimating selection versus drift from frequency time series. It could be applied to songs' yearly cover counts.
