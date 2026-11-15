# Sensory consonance and dissonance models computable from symbolic notes (for a rule-based voicing engine)

Research date: 2026-11-15. Scope: what can be computed from pitches, voicings and durations. Sources fetched this session are linked inline. Items marked **[UNVERIFIED: background knowledge]** come from the researcher's prior knowledge. They could not be checked against a primary source in this session (PMC pages were blocked by a captcha, and Sethares's site and GitHub were not on the fetch allowlist), so they sit only in Inferences and Gaps.

Note on the session's own computations: Sections 1 and 3 include numbers the researcher computed in Python. The computation used the Sethares (1993) parameterisation, with constants verified from the endolith gist cited below. These are model outputs, not perceptual data, and are labelled as such.

## 1. Roughness (interference) models: how each is computed and how it depends on register

### Takeaway
Every roughness model follows the same recipe. Expand each note into an assumed harmonic spectrum, then for every pair of partials take a weighting from the amplitudes and a dissonance curve that peaks at a fixed fraction of the critical band, and sum. Critical bandwidth stops shrinking in Hz at low frequencies, so a fixed musical interval does more "damage" the lower it sits. The roughness peak is about 1.4 semitones at middle C and roughly doubles each octave down. Register dependence is therefore built into all of these models once notes are converted to Hz.

### Cited Findings
- **Plomp & Levelt (1965), "Tonal consonance and critical bandwidth" (JASA 38:548).** This is the foundational paper. Its catalogue entries are at [PubMed 5831012](https://pubmed.ncbi.nlm.nih.gov/5831012/) and [MPI](https://www.mpi.nl/publications/item66382/tonal-consonance-and-critical-bandwidth) (full text not retrieved). The roughest beat frequency occurs "close to one quarter of the critical bandwidth" ([Moore, "Modern psycho-acoustics and its impact on Schenkerian analysis"](https://www.mooremusic.org.uk/schenk/aco3.htm), citing Plomp & Levelt).
- **Critical band vs register.** Critical bandwidth is "almost constant below about 200 Hz" and "approximates to a constant fraction of the basic frequency above about 500 Hz." In musical terms, from "the top of the treble stave upward" the most dissonant interval is "somewhat less than a semitone"; "at middle C it is 1.5 semitones, roughly doubling for each octave downwards from there" ([Moore](https://www.mooremusic.org.uk/schenk/aco3.htm)).
- Harrison & Pearce make the register point in the language of models: "A given frequency ratio occupies less critical-band distance as absolute frequency decreases," so the same interval can be consonant high and dissonant low ([Harrison & Pearce 2020, author manuscript via CORE](https://core.ac.uk/download/228298307.pdf)).
- **Sethares (1993) parameterisation of the Plomp-Levelt curve.** These are the exact constants used in a widely copied Python implementation. Dstar = 0.24 ("point of maximum dissonance"), S1 = 0.0207 and S2 = 18.96 ("used to stretch dissonance curve for different freqs"), C1 = 5, C2 = −5, A1 = −3.51, A2 = −5.75. For each pair of partials with lower frequency Fmin and difference Fdif: s = Dstar/(S1·Fmin + S2), and roughness = a·(C1·e^(A1·s·Fdif) + C2·e^(A2·s·Fdif)). Total dissonance is the sum over all pairs. The amplitude weighting a defaults to min(a1, a2) ("current", following Sethares's time-domain appendix), with the product a1·a2 labelled the "older model" ([endolith gist, sethares.py](https://gist.github.com/endolith/3066664)). The same constants appear in the Haskell `hmt` library ([hackage hmt Sethares_1994](https://hackage.haskell.org/package/hmt-0.16/docs/src/Music-Theory-Tuning-Sethares_1994.html)).
- **Vassilakis (2001).** The `dissonant` package describes it as "a modification of the pair function that weights relative rather than absolute amplitudes," with Vassilakis 2010 extending it ([PyPI dissonant](https://pypi.org/project/dissonant/)).
- **Hutchinson & Knopoff (1978), Sethares (1993), Vassilakis (2001), Parncutt & Strasburger (1994, "pure" sonorousness) and Weisser & Lartillot (2013)** are grouped by Harrison & Pearce as "interference, pure dyads" models: they sum roughness over pairs of pure-tone partials. Huron (1994) and Bowling et al. (2018) are "complex dyads" models. Leman (2000), Skovenborg & Nielsen (2002), Wang et al. (2013) and Vencovský (2016) are "waveform" models ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- **Spectrum assumption used in the benchmark implementation (incon).** Each note gets 11 harmonics including the fundamental. The i-th harmonic has amplitude i^−1 (a 1/n roll-off), and tones are assumed incoherent for amplitude summation ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). The fetch tool rendered the amplitude as "i−1"; read in context this is 1/i.
- **Instrument dependence of "mud".** Practitioner guidance: "The amount of mud a voicing generates is highly depending on its dynamic and how many higher harmonics the sound contains… soft low voicings on for instance strings are more forgiving than loud ones on brass" ([Robin Hoffmann, Low Interval Limits](https://www.robin-hoffmann.com/dfsb/low-interval-limits)).

### Inferences
- **Researcher computation, pure tones (Sethares constants above, fundamentals only).** This gives the interval of peak roughness and the interval at which roughness falls below 50% and 10% of peak, by the lower note's register:

| Lower note | Hz | Peak roughness | < 50% of peak | < 10% of peak |
|---|---|---|---|---|
| C2 | 65.4 | 4.3 st (≈ M3) | 10.0 st | 15.5 st |
| G2 | 98.0 | 3.1 st | 7.4 st | 12.0 st |
| C3 | 130.8 | 2.5 st | 6.0 st | 9.9 st |
| G3 | 196.0 | 1.8 st | 4.5 st | 7.6 st |
| C4 | 261.6 | 1.4 st | 3.6 st | 6.3 st |
| G4 | 392.0 | 1.1 st | 2.8 st | 4.8 st |
| C5 | 523.3 | 0.9 st | 2.3 st | 4.1 st |
| C6 | 1046.5 | 0.6 st | 1.6 st | 2.9 st |

  The C4 value (1.4 st) matches Moore's "1.5 semitones at middle C," which cross-checks the implementation. A closed-form shortcut for engine code: peak Δf ≈ 0.918·(0.0207·f_low + 18.96) Hz, which is about 17 to 37 Hz across the keyboard.
- **Researcher computation, harmonic complex tones.** Six harmonics, amplitude 0.88^(k−1), min-amplitude weighting, summing only across partials of different notes. Dyad roughness by lower note:

| Lower | m2 | M2 | m3 | M3 | P4 | TT | P5 | m6 | M6 | m7 | M7 | P8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C2 | 5.78 | 6.42 | 5.86 | 5.43 | 5.03 | 5.12 | 3.79 | 4.47 | 3.97 | 4.04 | 3.41 | 1.46 |
| G2 | 4.75 | 5.03 | 4.42 | 4.04 | 3.55 | 3.81 | 2.41 | 3.34 | 2.80 | 3.00 | 2.64 | 0.61 |
| C3 | 4.34 | 4.22 | 3.58 | 3.24 | 2.68 | 3.06 | 1.66 | 2.72 | 2.15 | 2.41 | 2.31 | 0.30 |
| C4 | 3.77 | 2.65 | 2.08 | 1.91 | 1.27 | 1.87 | 0.63 | 1.75 | 1.13 | 1.37 | 1.83 | 0.05 |
| C5 | 3.20 | 1.52 | 1.24 | 1.28 | 0.67 | 1.30 | 0.34 | 1.29 | 0.69 | 0.76 | 1.46 | 0.01 |

  Under this model, a major third on G2 (4.04) is computed rougher than a minor second on C5 (3.20). The same model gives close C-major triads totals of 14.2 at C2, 7.9 at C3 and 4.3 at C4, against 8.8 for an open C2–G2–E3. The open voicing at C2 is about as smooth as a close triad an octave higher.
- **Kameoka & Kuriyagawa (1969).** **[UNVERIFIED: background knowledge]** In JASA 46, they fitted a dyad "dissonance intensity" curve that depends on SPL as well as frequency difference, and summed partial dissonances with a power-law (non-linear) rule. It is rarely implemented today and is not in incon's list.
- **Hutchinson & Knopoff (1978).** **[UNVERIFIED: background knowledge]** As implemented in incon/dycon (following Mashinter 2006): critical bandwidth CBW = 1.72·(f̄)^0.65, with f̄ the mean frequency of the two partials. y = |f_i − f_j|/CBW and g(y) = (e·(y/0.25)·exp(−y/0.25))², which peaks at y = 0.25. Roughness = Σ A_iA_j·g(y) / ΣA_i². Check the actual dycon source before porting.
- **Vassilakis (2001/2005).** **[UNVERIFIED: background knowledge]** Per pair: R = (A1·A2)^0.1 · 0.5·(2·A_min/(A_min + A_max))^3.11 · (e^(−3.5·s·Δf) − e^(−5.75·s·Δf)), with s = 0.24/(0.0207·f_min + 18.96). This is the Sethares frequency term multiplied by an amplitude-fluctuation-degree term. The search did not retrieve a primary source for the formula. Use the `dissonant` source code as the reference.
- **For an engine.** Any of these can be computed directly from MIDI pitches once a spectral template per instrument (partial count and roll-off) is chosen. The register effect then appears automatically, and no separate "low interval limit" table is needed, though a table is a cheap approximation.

### Gaps
- Full text of Plomp & Levelt (1965) was not retrieved: one PDF link redirected to a homepage and PubMed gives only the abstract. Not verified this session: the per-frequency consonance curves, and the paper's often-cited analysis of a Bach trio sonata and a Dvořák string quartet showing that composers use wider intervals when the lower tone is low **[UNVERIFIED: background knowledge]**.
- Sethares's own code page (sethares.engr.wisc.edu/comprog.html, which hosts Matlab and other implementations) could not be fetched (not on the allowlist). Language and licence not confirmed.
- No primary-source text was found for the Hutchinson & Knopoff or Vassilakis equations.

## 2. Harmonicity/periodicity models and the roughness-vs-harmonicity debate

### Takeaway
Harmonicity models score how closely the pooled spectrum of a chord resembles one harmonic series, that is, how strongly it implies a single virtual fundamental. McDermott, Lehr & Oxenham (2010) found that individual consonance preferences tracked harmonicity, not beating. Harrison & Pearce (2020) reanalysed four datasets and argue that consonance is a composite of interference, harmonicity and cultural familiarity, with interference the strongest single predictor of how composers actually use chords. Cross-cultural work (Tsimane) shows roughness aversion is widespread, while the preference for consonant intervals is largely learned.

### Cited Findings
- **Models in incon, by class.**
  - *Periodicity/harmonicity:* `gill_09_harmonicity` (Gill & Purves 2009), `har_18_harmonicity` (Harrison & Pearce 2018), `milne_13_harmonicity` (Milne 2013), `parn_88_root_ambig` (Parncutt 1988), `parn_94_complex` (Parncutt & Strasburger 1994), `stolz_15_periodicity` (Stolzenburg 2015).
  - *Interference:* `bowl_18_min_freq_dist`, `huron_94_dyadic`, `hutch_78_roughness`, `parn_94_pure`, `seth_93_roughness`, `vass_01_roughness`, `wang_13_roughness`.
  - *Culture:* `jl_12_tonal` (Johnson-Laird et al. 2012), `har_19_corpus`.
  - *Numerosity:* `parn_94_mult`.
  - *Composite:* `har_19_composite`.

  ([incon README on rdrr.io](https://rdrr.io/github/pmcharrison/incon/f/README.md))
- **Harrison & Pearce's taxonomy of harmonicity models.** *Ratio simplicity:* Stolzenburg (2015). *Spectral pattern matching:* Terhardt (1982), Parncutt (1988), Parncutt (1989) and Parncutt & Strasburger (1994), Gill & Purves (2009), and Milne (2013) with Harrison & Pearce (2018) ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- **Harrison & Pearce / Milne harmonicity parameters:** roll-off ρ = 0.75 and Gaussian smoothing σ = 6.83 cents, from Milne & Holland (2016) ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- **McDermott, Lehr & Oxenham (2010), Current Biology.**
  - Stimuli: intervals and triads in five timbres (saxophone, sung vowels, synthetic sung vowels, synthetic complex tones, pure tones).
  - Beating preference: ratings of diotic minus dichotic pure-tone pairs 0.75 or 1.5 st apart.
  - Harmonicity preference: ratings of harmonic minus inharmonic complex tones.
  - Results: both harmonicity measures "correlated strongly with both consonance measures"; beating measures were "weak and inconsistent." Beating and harmonicity preferences were uncorrelated with each other (r from −0.09 to 0.17). Harmonicity preference, but not beating aversion, rose with years of musical training.
  - Conclusion: "Our findings suggest that consonance is due to harmonic frequency relations."
  - Source: [McDermott, Lehr & Oxenham 2010 PDF](https://mcdermottlab.mit.edu/papers/McDermott_Lehr_Oxenham_2010_consonance_individual_differences.pdf)
- **McDermott et al. (2016), Nature, Tsimane.**
  - More than 100 Tsimane (Bolivian Amazon, little Western music exposure) were tested in 2011 and 2015. Their preference for consonance was "undetectable," yet they "showed the same dislike for a musical quality known as acoustic roughness" as the other groups.
  - Comparison groups: Bolivian town and La Paz residents showed a small preference; US listeners showed a much larger one, larger in musicians.
  - Conclusion: "preferences for consonance over dissonance depend on exposure to Western musical culture."
  - Source: [MIT News 2016](https://news.mit.edu/2016/music-tastes-cultural-not-hardwired-brain-0713)
- **Harrison & Pearce (2020), Psychological Review 127(2), doi:10.1037/rev0000169.** They argue against "the recent consensus" that harmonicity is the main driver. They reanalysed four behavioural datasets (more than 500 participants) and modelled three corpora (more than 100,000 compositions), concluding that consonance is a composite of interference, periodicity/harmonicity and cultural familiarity ([Cambridge CMS summary](https://cms.mus.cam.ac.uk/publications/harrison-pearce-simultaneous-consonance/)).
- **Composite model coefficients (Table 3).** Intercept 0.628; number of notes 0.422; interference (Hutchinson & Knopoff) −1.620; periodicity/harmonicity (Harrison & Pearce 2018) +1.780; culture −0.089. Coefficients can be rounded to about 3 significant figures. For data outside Bowling et al. (2018), the authors "recommend setting the number of notes coefficient to zero" ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
  - The culture coefficient is printed as negative in Table 3 even though the text describes familiarity as having a positive effect. The likely reason is that the corpus model is scored as "corpus dissonance" (higher means less familiar), so a negative sign means familiar chords score as more consonant. This is an inference; confirm in the incon source.
- **What composers do (corpus analyses).**
  - Corpora: classical (128 million chords), jazz (iRB) and popular (Billboard).
  - Interference was "consistently the most important predictor" of how often a chord type appears, explaining about 20–50% of variance across genres.
  - Harmonicity mattered for classical, was weakly positive for popular and weakly negative for jazz.
  - Number of notes explained about half as much variance as interference.
  - Fit: r = .95 classical, .55 jazz, .67 popular.
  - Source: [Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)
- **Eerola & Lahdelma (2021).** A binary "Tonal Dissonance Model" (1 if the pitch set fits a major scale, else 0) "functions like a harmonicity model" and performs no worse than partial-based harmonicity models. Amusic listeners show normal roughness aversion but no harmonicity preference (Cousineau et al. 2012) ([Lahdelma, Eerola & Armitage 2022, Frontiers opinion](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.802385/pdf)).

### Inferences
- **Stolzenburg (2015) periodicity.** **[UNVERIFIED: background knowledge]** Approximate each frequency ratio relative to the lowest note by a simple fraction within a tolerance of about 1%. The chord's "relative periodicity" is the lowest common multiple of the denominators, log-scaled and often averaged over each note taken as reference. This is computable from pitch classes plus the bass.
- **Parncutt (1988).** **[UNVERIFIED: background knowledge]** Root-support weights (unison/octave, fifth, major third, minor seventh, major ninth templates) give a root ambiguity score. Pitch-class based, so register-blind.
- **Milne (2013) spectral pitch similarity.** **[UNVERIFIED: background knowledge]** Each pitch class is expanded into a harmonic template and smoothed with a Gaussian. Chords are compared by the cosine similarity of their expectation vectors. Harrison & Pearce (2018) adapted this into a harmonicity score: the peak of the chord's similarity to a harmonic template over all candidate fundamentals.
- **Engine design.** Harmonicity models in incon are largely pitch-class based, so they do not change with voicing or register. Roughness models do. For a voicing judge, the voicing-sensitive term is roughness. Harmonicity and familiarity mainly rank chord types, which is a harmony-selection decision rather than a voicing decision.

### Gaps
- Exact correlation coefficients in McDermott et al. 2010 appear only in figures and could not be read.
- Terhardt's virtual-pitch algorithm details were not retrieved this session.
- The Tsimane finding (consonance preference learned, roughness aversion widespread) is reported via MIT News, not the Nature paper itself.

## 3. Low-interval limits and spacing norms (keyboard, organ, SATB)

### Takeaway
The "low interval limit" rule (no close thirds below about C3, fifths are fine lower, octaves lowest) follows directly from critical-band physics: roughness depends on Hz separation, and critical bandwidth stops shrinking below about 200 Hz. Published tables are practitioner heuristics, not empirically fitted thresholds. A roughness model run on the actual pitches reproduces their ordering. The engine can either hard-code a table or compute roughness per voicing.

### Cited Findings
- Low interval limits "are NOT definitive rules but a good guide to avoid muddyness." Intervals "like the perfect fifth can be put lower than for example the minor second." Mud depends on dynamic and harmonic content ([Robin Hoffmann](https://www.robin-hoffmann.com/dfsb/low-interval-limits)). The numeric table on that page is an image and could not be read.
- The physics behind the rule: the roughest interval is about 1.5 st at middle C and roughly doubles per octave downward ([Moore](https://www.mooremusic.org.uk/schenk/aco3.htm)). In model terms, a fixed ratio occupies less critical-band distance at low frequency ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- The Harrison & Pearce corpus voicing algorithm targets a mean pitch near middle C. No register or spacing finding was reported; even spacing is discussed only as a corollary of efficient voice leading (after Tymoczko 2011) ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).

### Inferences
- **Model-derived low interval limits (researcher computation).** Same six-harmonic Sethares model as in Section 1. For each interval, the lowest lower-note at which dyad roughness never exceeds a reference roughness from there upward:
  - *Reference = minor third on C4:* M2 F#4, m3 C4, M3 Bb3, P4 F3, TT Bb3, P5 Bb2, m6 G3, M6 C#3, m7 E3, M7 F3, P8 A1. The m2 never qualifies within the piano range.
  - *Reference = perfect fifth on C3:* P5 C3, P8 B1, P4 Ab3, M6 F3, M3 E4, m3 F4.
  - These are more conservative than jazz-arranging tables by about an octave for thirds. The reference choice is arbitrary, and the min-amplitude 6-partial model overweights m6 and M7. Treat them as a ranking, not literal thresholds.
- **Traditional table.** **[UNVERIFIED: background knowledge; commonly attributed to Berklee arranging pedagogy, e.g. Pease & Pullig, *Modern Jazz Voicings*]** Lowest recommended lower note, roughly: m2 E3, M2 Eb3, m3 C3, M3 Bb2, P4 Bb2, TT B2, P5 Bb1, m6 G2, M6 F2, m7 F2, M7 F2. Exact values vary by source; verify before hard-coding.
- **SATB spacing norms.** **[UNVERIFIED: background knowledge]** No more than an octave between soprano and alto or between alto and tenor, with tenor–bass allowed up to about a twelfth. Huron (2001, "Tone and Voice," Music Perception 19:1–64) derives voice-leading rules from perceptual principles. Huron & Sellmer (1992, JASA) re-examined the Plomp & Levelt corpus claim. Both reportedly support the view that wider low intervals reduce critical-band masking and roughness, while the upper-voice octave limit relates to voice fusion and streaming rather than roughness. Not verified this session.
- **Organ.** Many stops have strong upper partials, and mixtures and mutations add partials above the fundamental, so roughness rises. On a 16′ pedal a third sounds an octave lower than written, pushing it below the comfort limit. An engine should apply the limits at sounding pitch, not written pitch, and tighten them for reedy or mixture registrations. This is an inference from the model mechanics and Hoffmann's harmonic-content remark.

### Gaps
- No peer-reviewed study was found that empirically fits per-interval low-register thresholds to listener ratings. Existing tables appear to be pedagogical.
- Huron (2001) and Huron & Sellmer (1992) could not be retrieved.

## 4. Validation: how well models predict listener ratings, and the role of timbre and duration

### Takeaway
On the largest chord dataset (Bowling et al. 2018), Hutchinson & Knopoff roughness alone reaches partial r = .77. Harrison & Pearce harmonicity and corpus familiarity each reach .72, and the composite reaches r = .88. Many popular "roughness" implementations perform poorly on this dataset (r ≈ .17–.57). Familiarity strongly modulates pleasantness ratings, while perceived tension tracks roughness more stably. Timbre and duration are under-studied: most datasets use one piano timbre in the F3–F4 range.

### Cited Findings
- **Bowling, Purves & Gill (2018), PNAS.** 12 dyads, 66 triads and 220 tetrads (all chords within an octave), in just intonation, with a Bösendorfer piano sample. Mean F0 was 263 Hz, with tones spanning 174–349 Hz (about F3–F4), so register was not varied. Thirty participants (15 conservatory students in Singapore, 15 Vienna students) rated chords on a 4-point scale. Vocal-similarity metrics predicted the more consonant chord in 98% of significant pairwise differences. Roughness was not tested by the authors ([Bowling et al. PNAS PDF](https://chrysalis-foundation.org/PNAS-2017-Bowling-1713206115.pdf)).
- **Harrison & Pearce reanalysis of Bowling (partial r controlling for number of notes).**
  - Hutchinson & Knopoff: r = .77 [.72, .81]
  - Harrison & Pearce harmonicity: .72 [.66, .77]
  - Corpus familiarity: .72 [.66, .77]
  - Johnson-Laird et al. rule-based: .63
  - Parncutt & Strasburger: .56
  - Other harmonicity models: .62–.72
  - Sethares-based MIRtoolbox (audio): .57
  - MIRtoolbox periodicity: .18
  - Essentia interference: .19
  - Wang et al. 2013: .17 (.46 with phase factors disabled)
  - Composite: r = .88 [.85, .90], "All four features contributed significantly and substantially… with broadly similar regression coefficients."
  - On other datasets: Schwartz et al. 2003 dyads, composite r = .87 [.59, .96]; Lahdelma & Eerola 2016, .97 without the number-of-notes term. On Johnson-Laird Exp. 2 (48 four-note chords), the composite was only "almost on a par" with harmonicity.
  - Huron (1994), Parncutt (1988) and Stolzenburg (2015) "performed well" on validation sets.
  - Source: [Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)
- **Johnson-Laird et al. (2012).** Exp. 1 used 27 participants rating 55 three-note chords; Exp. 2 used 39 participants rating 48 four-note chords ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- **Lahdelma & Eerola (2020), Scientific Reports.** Online Western participants (Exp. 1 n = 407; Exp. 2 n = 392). Exp. 1 played 25 Bowling chords in piano and sine timbres, equal temperament, 2 s each.
  - Pleasantness correlated with consonance at .96 for musicians and .87 for non-musicians.
  - Tension stayed strongly negatively correlated with consonance across familiarity levels (−.72 to −.95), whereas pleasantness varied with familiarity (musicians: .70, .45, .96).
  - Model correlations in Exp. 2 (72 piano chords):
    - Hutchinson & Knopoff roughness: consonance −.630, pleasantness −.454, tension +.527
    - Harrison & Pearce harmonicity: consonance .478, tension −.422; negligible after controlling for roughness and familiarity
    - Familiarity: consonance .609, pleasantness .664, preference .684
  - Source: [Lahdelma & Eerola 2020, Durham repository PDF](https://durham-repository.worktribe.com/OutputFile/1265040)
- **Popescu et al. (2019), Scientific Reports,** "The pleasantness of sensory dissonance is mediated by musical style and expertise," doi:10.1038/s41598-018-35873-8 ([OUCI record](https://ouci.dntb.gov.ua/works/45gEZaE9); an [author correction](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6579756/) exists). The abstract could not be retrieved.
- **Timbre.** McDermott et al. (2010) tested five timbres including pure tones ([PDF](https://mcdermottlab.mit.edu/papers/McDermott_Lehr_Oxenham_2010_consonance_individual_differences.pdf)). Harrison & Pearce list timbre/spectra variation and voicing as a key gap: models assume idealised harmonic spectra, and Bowling used just tuning ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).
- **Duration.** Chord durations were unavailable for the classical and jazz corpora, so counts were used instead. No duration effect on perceived consonance was modelled ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)).

### Inferences
- **For a voicing engine,** Hutchinson & Knopoff roughness with 11 harmonics at 1/n amplitude is the best-validated single symbolic predictor, and it is voicing- and register-sensitive. Add Harrison & Pearce harmonicity and a familiarity term for chord-type choice using the published coefficients, with the number-of-notes coefficient set to 0.
- The validation datasets are almost all mid-register (around F3–F4) piano or synthetic tones. **Register effects on ratings are predicted by the models but not directly validated by these datasets.** Choir (vowel formants) and organ registrations have not been validated.
- **Duration as a heuristic (unvalidated).** Roughness matters more on sustained chords (organ, choir) than on short or decaying piano chords. One option is to weight roughness penalties by duration, and by sustain for organ.

### Gaps
- No dataset was found that systematically varies register or voicing of the same chord against listener ratings, apart from Lahdelma & Eerola 2016, whose transpositions were averaged.
- No source was found on duration effects on consonance ratings.
- Popescu 2019 findings could not be retrieved.

## 5. Open code: implementations, licences, inputs

### Takeaway
The most complete symbolic toolkit is the R package **incon**, with 16+ models, MIDI pitch input, and the Hutchinson & Knopoff default. Python options are thinner. `dissonant` (MIT, 2018 alpha) implements Plomp-Levelt, Sethares, Vassilakis and Cook from partial frequencies and amplitudes. The Sethares formula is small enough to port directly; the constants are verified above.

### Cited Findings
- **incon (R; github.com/pmcharrison/incon).** Example input: `chord <- c(60, 64, 67)` (MIDI note numbers). "The default model is that of Hutchinson & Knopoff (1978)." The model list is in Section 2 ([rdrr incon README](https://rdrr.io/github/pmcharrison/incon/f/README.md)). It is built from lower-level packages (har18, dycon, parn94, wang13) ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). A separate `bowl18` package implements Bowling et al.'s vocal-similarity algorithms ([rdrr bowl18](https://rdrr.io/github/pmcharrison/bowl18/f/README.md)). An online "Consonance models" app also exists ([Cambridge CMS](https://cms.mus.cam.ac.uk/publications/harrison-pearce-simultaneous-consonance/)).
- **dissonant (Python, Bohumir Zamecnik; github.com/bzamecnik/dissonant).** MIT licence; version 0.1.1 released 3 Apr 2018; "3 – Alpha."
  - Models: PlompLevelt1965 (data only), Sethares1993, Vassilakis2001 (Vassilakis2010 mentioned), Cook2002, Cook2006, Cook2009. Includes "corrections of errors found in the formulas in the papers."
  - API: `harmonic_tone(pitch_to_freq([0,4,7,12]), n_partials=10)` then `dissonance(freqs, amps, model='sethares1993')`. Pitch-to-frequency conversion uses 12-TET at A = 440 Hz.
  - Source: [PyPI dissonant](https://pypi.org/project/dissonant/)
- **Sethares function in Python** (endolith gist; min vs product amplitude option): [gist 3066664](https://gist.github.com/endolith/3066664). **Haskell:** the `hmt` package ([hackage](https://hackage.haskell.org/package/hmt-0.16/docs/src/Music-Theory-Tuning-Sethares_1994.html)).

### Inferences
- **Porting incon to Python.** Python-native work is simplest by reimplementing Hutchinson & Knopoff (about 30 lines) with the incon spectral settings: 11 harmonics, 1/n amplitude, incoherent summation. Validate against incon output for a test set, e.g. `rpy2` or a one-off R run producing a reference table.
- **music21.** **[UNVERIFIED: background knowledge]** It offers only binary/rule checks such as `Chord.isConsonant()` and interval classes. It has no psychoacoustic roughness model, but it is useful for parsing and voicing manipulation.
- **Input requirements.** All the symbolic models need MIDI pitch (absolute, for roughness) or pitch class (most harmonicity and culture models), plus a spectral template. Duration and dynamics are not inputs to any of them.

### Gaps
- incon's licence could not be confirmed: the README fetch did not show it and GitHub was not fetchable. **[UNVERIFIED: background knowledge]** It is believed to be MIT.
- The language and licence of Sethares's own website code could not be verified.
- Activity and maintenance of incon and dissonant as of November 2026 could not be checked. dissonant's last release is from 2018.
