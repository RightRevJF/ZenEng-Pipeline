# Card 1: Cheung et al. 2019, uncertainty x surprise in chord progressions

## Citation and link
Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019). Uncertainty and
surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*
29(23), 4084-4092.e4. doi:10.1016/j.cub.2019.09.067 (Elsevier open archive).

- Author copy (article + STAR Methods + references): stefan-koelsch.de/papers/cheung_harrison_meyer_pearce_haynes_koelsch_2019_...current_biology_29.pdf
- Publisher HTML: sciencedirect.com/science/article/pii/S0960982219312588 (used to confirm the signs in Table 1 and the
  fMRI estimates, which the PDF text extraction dropped).
- Supplement (Document S1: Tables S1-S4, Figs S1-S3): ars.els-cdn.com/content/image/1-s2.0-S0960982219312588-mmc1.pdf

What I read: the whole main article (summary, introduction, results, Table 1, figure captions, discussion, limitations),
the full STAR Methods (participants, stimuli, IDyOM, behavioral and fMRI analysis, data availability) and the full
85-item reference list. I read them through a text-extraction tool in several targeted passes, not as a verbatim page
view. **I did not read the supplement**: both supplement links were blocked (permission request unanswered). So the list
of 30 source songs (Table S1), the acoustic-feature correlations (Table S3), the full fMRI table (Table S4) and Figs
S1-S3 are known to me only from how the main text describes them. cell.com and doi.org also failed to load.

## The claim, and the data it rests on
Claim: how pleasant a chord feels depends on surprise and uncertainty *together*, not on surprise alone. A chord pleases
most when it is surprising after a predictable stretch, or unsurprising after an uncertain one; this joint effect also
shows up in the amygdala/anterior hippocampus and auditory cortex, while the striatum (nucleus accumbens, caudate)
tracks uncertainty only.

- **Corpus for the expectation model:** McGill Billboard corpus (Burgoyne et al. 2011), 745 US Hot 100 songs from
  1958-1991, 80,943 chords.
- **Stimuli:** 30 chord progressions from 30 different corpus songs, 30-38 chords each (mean 34.6), 1,039 chords total.
  Picked by an algorithm: start on the tonic in root position, end on a perfect or plagal cadence, contain chords from
  all four high/low surprise x high/low uncertainty corners (top and bottom 40%), enough spread, no over-repetitive
  stretches. All transposed to C major. Rendered from MIDI with a mixed guitar/marimba timbre, one chord every 2.4 s.
  A generic drum loop in 4, unrelated to the song's own metre, was added for momentum. No melody, no chord rhythm, no
  lyrics. The example song shown is ABBA's "Knowing Me, Knowing You"; no listener recognised the songs.
- **Experiment 1 (behavior):** 39 adults (21 female, mean age 24) rated each chord's pleasantness live on a slider.
- **Experiment 2 (fMRI):** 40 different adults (20 female, mean age 25), 3T multiband scanning, listening to the same 30
  progressions and rating each whole progression afterwards.
- **Success:** in a linear mixed model, the uncertainty x surprise term predicts chord-by-chord pleasantness beyond
  acoustic controls; in fMRI, the same term modulates activity in pre-chosen regions after Bonferroni correction.

## The measure: from the notes or not?
Yes, the predictors are from the notes. Surprise = information content of each chord (minus log probability) and
uncertainty = entropy of the model's prediction just before the chord, both from IDyOM on chord symbols (scale degree +
chord type + inversion; one viewpoint). IDyOM blended a long-term model trained on the Billboard corpus (10-fold
cross-validation so a song is not scored by a model that saw it) with a short-term model trained on the progression
itself. The paper does not say whether the 30 stimulus songs were in the training folds of their own predictions; the
cross-validation implies not.

What is *not* from the notes: the outcome (felt pleasure, BOLD signal) and the control covariates (sensory dissonance,
spectral centroid, spectral complexity from Essentia on the rendered audio). The stimuli remove melody, rhythm and words,
so this is a pure harmony test, which suits Jason's notes-only aim, but it says nothing about tune or rhythm.

## How big the effect is and how it was checked
Experiment 1 (standardized coefficients, chord-level ratings averaged over the 39 listeners, AR(1) errors, random slopes by
progression, likelihood-ratio tests):
- uncertainty -0.14, surprise -0.33, uncertainty x surprise -0.12 (p about 2e-4); sensory dissonance -0.25, spectral
  complexity +0.22, spectral centroid +0.07. Full model vs null chi2(8) = 225. Marginal R2 0.48, conditional 0.65 (these
  include the acoustic covariates, so the share due to the expectation terms alone is smaller and not reported).
- Uncertainty and surprise were nearly uncorrelated in the stimuli (r = 0.02), by design.
- Reading Table 1 at face value (my arithmetic, not the authors'): the slope of surprise is -0.33 - 0.12 x uncertainty,
  which only turns positive about 2.6 SD below mean uncertainty. So across most of the space, surprise *lowers* pleasure;
  the well-known surprise-after-predictability corner is a small region. The paper calls the fitted surface a saddle.

Experiment 2 (n = 40, seven regions from an independent meta-analysis, Bonferroni within analysis):
- interaction: left amygdala/hippocampus -0.12 (sign test, corrected p = .045, borderline), right -0.14 (p = .002), left
  auditory cortex -0.18 (p = .0001), right -0.13 (p = .002).
- uncertainty main effect (positive): right nucleus accumbens +0.24, left caudate +0.28, pre-SMA +0.36; no surprise or
  interaction effect in accumbens or caudate.

Checks and weak spots:
- No held-out test of the behavioral model and no preregistration. Subject-level random effects were dropped (residuals
  went heteroscedastic) and the model was fitted to ratings averaged over listeners, which smooths noise and helps R2.
  Effective sample for generalising to *music* is 30 progressions, all from one corpus.
- The fMRI sample is a new group of people, so the joint pattern was seen twice in two measures, but with the same 30
  stimuli: no new music, no other style. Regions were chosen in advance (good); only ROI tests, no whole-brain map.
- Acoustic confounds were controlled with three covariates; how strongly they correlate with surprise/uncertainty is in
  Table S3, which I could not read.
- Authors' own limits: synthetic isochronous chords, values relative to a 1958-1991 US pop corpus, culture/style and
  expertise effects untested. Data available only on request.

## What it says about Jason's yardstick
- It measures momentary pleasure in strangers hearing unfamiliar chord loops for the first time. It is silent on lasting
  love (years of re-listening, when the long-term model already knows the song) and on covers. Ironically the stimuli come
  from chart hits, but chart success is never used as an outcome.
- On re-hearing, the short-term model would make a known song ever less surprising, so the chord-by-chord effect may not
  carry over to songs people love for decades. A song-level average is a different object from the chord-level effect.
- The repo's covers study already tried a Cheung-style chord term (-mean(zIC x zH), a song average that rewards both
  corners of the saddle): +0.076 on SHS100K, +0.009 (p .54) on Discogs-VI. This paper gives no reason to expect a
  song-level average to predict covers, so the failed replication is not a strike against Cheung, nor is the SHS100K
  pass support for it.
- Two gaps between the repo term and Cheung's measure worth noting: the repo model is long-term only (no short-term,
  within-song model), uses root + quality without inversion, collapses repeated chords, and is trained on Hooktheory clips
  rather than whole Billboard songs. And Cheung's strongest single term is the *negative* main effect of surprise, which
  the repo term ignores; that main effect points the opposite way from the one note finding that did replicate (less
  chord repetition, chords that move, goes with more covers).

## One test Luthier could run
**Frozen Cheung pleasure index vs covers, on the McGill Billboard corpus** (public, DDMAL; the paper's own training
corpus, so the measure is applied in its home domain).
1. Measure: rebuild IDyOM-style chord IC and entropy with Cheung's alphabet (scale degree, type, inversion) and both
   long- and short-term models, 10-fold by song. For every chord compute the frozen Table 1 prediction
   P = -0.143 zH - 0.327 zIC - 0.124 zH x zIC (no refitting). Song score = mean P; secondary score = share of chords in the
   two pleasure corners (low H/high IC, high H/low IC).
2. Data: join the ~740 Billboard songs to SecondHandSongs cover counts (SHS100K and Discogs-VI separately). Controls:
   release year, Billboard peak position and weeks on chart (in the corpus metadata), song length in chords, artist
   clustering. Also add the repo's chord-repetition measure.
3. Prediction: mean P predicts *more* covers within era (positive beta), in both cover sources, and adds to chord
   repetition. Because P is dominated by the negative surprise term, a pass would mean predictable-feeling progressions
   get covered more, in tension with chords that move; whichever wins is informative.
4. Failure: beta < +0.05 or p > .05 in either cover source, or opposite signs across sources, or the effect vanishes once
   chart weeks are held (meaning it only tracks popularity). With about 700 songs, a true beta of 0.10 is detectable.

## Leads
1. Gold, B. P., Mas-Herrero, E., Zeighami, Y., Benovoy, M., Dagher, A., & Zatorre, R. J. (2019). Musical reward
   prediction errors engage the nucleus accumbens and motivate learning. *PNAS* 116(8), 3310-3315.
   doi:10.1073/pnas.1809855116. The striatal reward-prediction-error account Cheung argues against; links expectation to
   motivation to learn a song, nearer to lasting love than momentary pleasure. (The same group's J Neurosci 2019 paper on
   predictability and uncertainty, not in this bibliography, is also worth a look.)
2. Burgoyne, J. A., Wild, J., & Fujinaga, I. (2011). An expert ground truth set for audio chord recognition and music
   analysis. *Proc. 12th ISMIR*, 633-638. The McGill Billboard corpus itself, with chart metadata: the data for the test
   above.
3. Hansen, N. C., & Pearce, M. T. (2014). Predictive uncertainty in auditory sequence processing. *Frontiers in
   Psychology* 5, 1052. doi:10.3389/fpsyg.2014.01052. Shows listeners feel IDyOM entropy directly; the basis for treating
   uncertainty as its own dimension.
4. Berlyne, D. E. (1971). *Aesthetics and Psychobiology*. Appleton-Century-Crofts. The inverted-U and habituation theory;
   the classic account of why liking changes with repeated exposure, which bears on lasting love.
5. Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
   doi:10.7551/mitpress/6575.001.0001. Covers how expectation, repetition and familiarity interact over many hearings,
   the gap between first-hearing pleasure and long-run love.
