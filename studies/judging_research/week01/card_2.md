# Card 2: Janssen, Burgoyne and Honing (2017), which folk-song phrases survive oral transmission

## Citation and link
Janssen, B., Burgoyne, J. A., and Honing, H. (2017). Predicting variation of folk songs: a corpus analysis study on the memorability of melodies. *Frontiers in Psychology* 8:621. doi:10.3389/fpsyg.2017.00621 (open access; PMC5403935).

What I read: the full article PDF (University of Amsterdam repository copy, the same as the Frontiers PDF), covering the introduction, methods, results, Tables 1 and 2, Figures 1 to 3 as described in the text, the discussion, footnotes and the 46-item reference list. I could not read the Supplementary Material (the Frontiers supplement page), the code repository (github.com/BeritJanssen/Stability) or the PMC page, because those fetches were blocked when a permission request went unanswered. The supplement holds the details of the combined similarity measure, the pitch-reversal scoring and a worked motif example. Its main points are summarised in the article body.

## The claim, and the data behind it
Claim: in oral transmission, melodic phrases that are easier to remember change less. A phrase is more stable when it is short, early in the song, low in surprise (made of expected material) and built from small intervals. Repetition helps too, but only a little. The authors present memorability as one force alongside random drift, not as a replacement for drift.

Data: the folk song part of the Meertens Tune Collections (MTC-FS). It holds 4,125 monophonic Dutch songs, mostly from fieldwork recordings made between 1950 and 1980, plus 1,245 transcriptions from 19th and 20th century songbooks. Experts grouped them into tune families (sets of variants of one tune). The corpus was split three ways:
- training: 360 melodies with hand-annotated phrase occurrences, used to tune the matcher;
- test: 1,695 melodies from families with at least five variants, giving 9,639 phrases in 147 tune families;
- background: 1,000 melodies from small families, used only to train the expectancy model, with any related melodies removed.

Stable means a phrase turns up in many of the other variants in its own tune family. The authors take this definition from Bronson (1951), and the outcome is binary for each pair of phrase and variant (present or absent). There were 170,803 such judgments, about 18 per phrase.

## The measure: from the notes or not?
Yes, the measure comes entirely from the notes (pitch and onset), with no words and no audio. Occurrence was found by an automatic matcher that combines city-block distance, Smith-Waterman local alignment and point-set structure induction. Thresholds were tuned on the training set. Against human annotators, the matcher misses about 30% of true occurrences and adds about 8% false ones.

Predictors, all computed on the query phrase inside its own melody and z-scored:
- Phrase length: number of notes (mean 9.1).
- Phrase repetition: exact repeats of the phrase within its own melody (range 1 to 4, mean 1.17).
- Phrase position: index in the song, where 1 is first.
- Pitch proximity: the negated mean interval size in semitones, a simplified Schellenberg implication-realization measure.
- Pitch reversal: Schellenberg's reversal score averaged over the phrase.
- Surprisal: mean IDyOM information content. The settings were a pitch-interval viewpoint, a long-term model only, trained on the background set, with order capped at 9.
- Motif repetivity: the negated mean normalised entropy of motifs of 2 to 6 notes (FANTASTIC style).

## How big the effect is and how it was checked
- Model: a logistic GLMM in lme4, with a random intercept for each tune family and fixed slopes. All 128 predictor subsets were compared by AICc in MuMIn. The full seven-predictor model won, beating the next best by about 70 AICc.
- Standardised log-odds per SD, all with tight 95% CIs that exclude zero. Phrase length had the largest effect at -0.30, followed by surprisal at -0.24. Position (-0.10), proximity (+0.10), repetition (+0.09), motif repetivity (+0.08) and reversal (+0.05) were smaller. As odds ratios, one SD more surprisal lowers the odds that a phrase survives by about 21%, and one SD more length lowers them by about 26%.
- Fit: marginal R² was 0.05 (fixed effects only) and conditional R² was 0.22 (adding tune family). The tune family SD was 0.84 on the logit scale, which dwarfs any single predictor. The authors call R² = 0.05 a mid-sized effect, but 95% of the variance is left unexplained.
- Checks: correlations among the parameter estimates stayed at or below 0.6. The background corpus was kept apart from the test corpus for IDyOM training. Beyond that, there was no held-out prediction, no cross-validation, no replication on a second tradition, no interactions and no robustness runs. Significance rests on CIs from about 170k non-independent pairs. Phrases from the same melody are not given their own random effect, so the CIs are probably too narrow.
- Confounds the authors name: matcher errors (shorter phrases may simply be easier to match, which could inflate the length effect), annotator disagreement, regional and demographic bias, thin IDyOM context for opening phrases, and long gaps between when singers learned songs and when they were recorded. They could not test drift directly.
- One mild surprise: more expected material was more stable. That goes against the view that distinctive or surprising melodies are better remembered (Müllensiefen and Halpern 2014).

## What it says about Jason's yardstick (lasting love plus covers)
The link is real but narrow. Surviving oral transmission is literally re-performance by others over time, so it is the closest folk analogue to covers. The finding is that features of the notes do predict which material others reproduce faithfully, but weakly. Fixed note features explain about 5%. That is close to the covers study's result that notes explain about 4% of covers beyond views. The family a phrase belongs to explains far more, and the same is true of our finding that the artist accounts for about 0.15 of G.

Gaps to be honest about:
1. The unit is the phrase inside a song, compared with sibling phrases, not whole songs compared with each other. It says which parts of a tune survive, not which tunes get loved.
2. Stability here means fidelity of copying, while covers mean choosing to perform a song at all. Faithful copying favours plain, predictable, short material, which is the opposite of what makes a pop song stand out. In our covers data, it was less chord repetition ("chords that move") that held up, not more.
3. Pop covers are learned from fixed recordings, not from memory passed between people, so the pressure on memory is much weaker.
4. Love is not measured at all.

The useful message for Luthier: low surprise makes a phrase easy to carry. That may be a floor for a song to be singable by others, not a sign of greatness. That fits the Cheung-style idea that surprise only pays after a predictable stretch.

## One test Luthier could run
Song-level carryover to covers on public stores (no per-song corpora are committed, and song 59 is excluded).
- Data: Hooktheory melodies with SHS100K cover counts (780 songs), then replication on the Discogs-VI-matched set (2,360 songs).
- Measure: the song's mean phrase-level IDyOM information content, using a pitch-interval viewpoint, a long-term model only, trained on a separate background set of Hooktheory songs not in the test set. Phrases are Hooktheory section melodies split at rests of at least one beat. Two secondary measures are mean phrase length in notes and mean absolute interval.
- Predicted direction: lower mean surprisal goes with more covers, holding views, release year and era as in the covers study. The pre-stated threshold is a standardised beta of -0.05 or stronger.
- Failure: the 95% CI includes zero on either store, or the sign is positive on either store. As a within-song check, the opening phrase should have the lowest surprisal more often than chance in high-cover songs than in low-cover songs. If it does not, the folk "early and expected" pattern does not carry over.

## Leads
1. Müllensiefen, D., and Halpern, A. R. (2014). The role of features and context in recognition of novel melodies. *Music Perception* 31, 418-435. doi:10.1525/mp.2014.31.5.418. It is the main counter-claim, that distinctive features aid memory, and it uses FANTASTIC note features that we could compute.
2. Van Balen, J., Burgoyne, J. A., Bountouridis, D., Müllensiefen, D., and Veltkamp, R. (2015). Corpus analysis tools for computational hook discovery. Proc. ISMIR 2015, 227-233 (no DOI). It applies note features to pop catchiness, which is closer to our songs than folk.
3. Burgoyne, J. A., Bountouridis, D., Van Balen, J., and Honing, H. (2013). Hooked: a game for discovering what makes music catchy. Proc. ISMIR 2013, 245-250 (no DOI). It is a large crowd measure of pop recall that could serve as a memorability yardstick for the same songs.
4. Rubin, D. C. (1995). Memory in Oral Traditions: The Cognitive Psychology of Epic, Ballads, and Counting-out Rhymes. Oxford University Press (no DOI). It is the theory of how constraints like rhythm and repetition make material last through re-performance.
5. Janssen, B., van Kranenburg, P., and Volk, A. (2017). Finding occurrences of melodic segments in folk songs: a comparison of symbolic similarity measures. *Journal of New Music Research* 46. doi:10.1080/09298215.2017.1316292. It describes the matcher behind the stability measure, which is needed to judge how far its 30% miss rate biases the length effect.
