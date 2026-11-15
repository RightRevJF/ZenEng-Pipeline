# Metric Hierarchies and Melodic Rhythm in Triple and Compound Metres vs 2/4 and 4/4: Corpus and Cognitive Literature

Scope note: this research pass used about 20 tool calls. Several canonical sources (Huron's *Sweet Anticipation* ch. 10, Palmer & Krumhansl 1990 full text, Temperley 2010 *Music Perception*, London's *Hearing in Time* full text, Sioros & Guedes 2014 syncopation PDFs) could not be retrieved in full. Where a figure was not seen in a retrieved source, it is listed under Gaps rather than reported from memory. The one hard numeric onset profile recovered (Essen 4/4, Huron & Ommen tally) is solid. No equivalent verified numeric profile for 3/4 or 6/8 was retrieved, and that is the main gap.

## Q1. What onset-position profiles have been measured for 3/4, 6/8, 2/4, 4/4 (Palmer & Krumhansl 1990; Huron/Essen; Temperley; Volk IMA)?

### Takeaway
Corpus onset counts track the textbook metric hierarchy closely. In the Essen 4/4 tally (75,242 onsets at sixteenth-note resolution), the downbeat takes about 25.5% of all onsets, the three other beats take 13.6 to 19.0%, eighth off-beats take 2.8 to 7.9%, and sixteenth positions take 0.03 to 0.8%. The ordering of positions by count almost exactly matches Haydn string quartets. Palmer & Krumhansl (1990) plotted equivalent profiles for 2/4, 3/4, 4/4 and 6/8 from classical keyboard music, but no numbers for those were retrieved here.

### Cited Findings
- **Essen 4/4 onset counts by sixteenth-note beat class (bc 0 to 15):** 19221, 24, 2116, 412, 10226, 25, 5661, 430, 14280, 24, 2380, 348, 13458, 39, 5964, 634. These come from Huron & Ommen's tally of common-time monophonic songs in the Essen Folksong Database, shared privately with Scott Murphy (2015) and printed in his footnote 5 — [Murphy 2020, *Journal MusMat* IV/1, "Common Rhythm as Discrete Derivative of Its Common-Time Meter"](https://musmat.org/wp-content/uploads/2020/06/05-Scott.pdf)
  - Normalised by me from those counts (total 75,242), as share of all onsets / relative to the downbeat:
    - bc0 (beat 1): .2555 / 1.00
    - bc1: .0003 / .001
    - bc2 (eighth off-beat): .0281 / .110
    - bc3 (sixteenth before beat 2): .0055 / .021
    - bc4 (beat 2): .1359 / .532
    - bc5: .0003 / .001
    - bc6: .0752 / .295
    - bc7: .0057 / .022
    - bc8 (beat 3): .1898 / .743
    - bc9: .0003 / .001
    - bc10: .0316 / .124
    - bc11: .0046 / .018
    - bc12 (beat 4): .1789 / .700
    - bc13: .0005 / .002
    - bc14: .0793 / .310
    - bc15 (sixteenth before the next downbeat): .0084 / .033
- **Theoretical metric-weight levels Murphy uses for 4/4:** bc0 = level 4; bc8 = level 3; bc4 and bc12 = level 2; even bcs = level 1; odd bcs = level 0 — [Murphy 2020](https://musmat.org/wp-content/uploads/2020/06/05-Scott.pdf)
- **Haydn string quartets (4/4, counted with music21):** beat classes rank 0 to 15 by onset count with no ties. Only 2 of the 120 pairwise orderings differ between the Haydn and Essen rankings. The ordering by the "backwards discrete derivative" of Murphy's metric function "perfectly corresponds to its ranking by onset count" — [Murphy 2020](https://musmat.org/wp-content/uploads/2020/06/05-Scott.pdf)
- **Palmer & Krumhansl (1990):** they used an ad hoc corpus of classical keyboard music (Bach, Mozart, Brahms, Shostakovich) and found a strong correlation between onset frequencies and Western metrical accent patterns. Their Fig. 2 shows onset frequencies for **2/4, 3/4, 4/4 and 6/8** — as summarised by [London, Polak & Jacoby 2016, *Psychonomic Bulletin & Review*](https://core.ac.uk/download/83231804.pdf)
- **Palmer & Krumhansl (1990), further:** listeners' temporal expectations also reflected the metrical hierarchy, and musicians showed finer differentiation — as summarised by [van der Weij, Pearce & Honing 2017, *Frontiers in Psychology* 8:824](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)
- **Counter-evidence outside Western music:**
  - Holzapfel (2015), 913 notated Turkish makam pieces: onset histograms for six usul do not match the usuls' metrical accent patterns — [London et al. 2016](https://core.ac.uk/download/83231804.pdf)
  - Malian jembe music (15 performances, about 42,297 onsets): apart from the downbeat, on-beat positions are articulated *less* often than the upbeat positions just before them, and the most frequent onset locations are not periodically spaced (2+3+3+4 and 2+4+3+2+1 patterns) — [London et al. 2016](https://core.ac.uk/download/83231804.pdf)
- **Inner Metric Analysis (Volk):**
  - Metric weights come from the onsets themselves, not the bar lines. A "local meter" is any set of at least 3 equally spaced onsets. Each onset's weight is the sum over all local meters through it of k(m)^p, where k(m) is the local meter's length; the paper uses ℓ = 2 and p = 3 — [Volk et al., ISMIR 2007, "Applying rhythmic similarity based on inner metric analysis to folksong research"](https://archives.ismir.net/ismir2007/paper/000293.pdf)
  - That paper shows IMA weights for 6/8 Dutch folk melodies only qualitatively (Fig. 1) and gives no quantitative check against the notated metre — [ISMIR 2007](https://archives.ismir.net/ismir2007/paper/000293.pdf)

### Inferences
- For a generator's 4/4 onset prior at sixteenth resolution, the Essen numbers give a ready-made table. Key features:
  - Beat 3 outranks beats 2 and 4.
  - Beat 4 (.179) is close to beat 3 (.190), probably because of phrase-final and anacrusis patterns.
  - Off-beat eighths after beats 2 and 4 (bc6, bc14 ≈ .075 to .079) are about 2.5× more common than those after beats 1 and 3 (bc2, bc10 ≈ .028 to .032). In Essen 4/4, motion is denser in the second half of each half-bar.
  - The sixteenth just *before* a beat (bc3, 7, 11, 15) is about 15 to 30× more common than the sixteenth just *after* a beat (bc1, 5, 9, 13). This is the dotted-eighth + sixteenth signature. Reversed "Scotch snap" figures are nearly absent.
- A defensible way to build 3/4 and 6/8 priors when no counts are available is the same hierarchical scheme (downbeat > beats > subdivisions), with the corrections the 4/4 data suggest: "before-the-beat" subdivisions outweigh "after-the-beat" ones, and the last beat of the bar is boosted. This is an inference, not a measurement.

### Gaps
- No numeric onset-by-position values for **3/4, 6/8, 2/4, 3/8, 9/8, 12/8, 6/4 or 3/2** were retrieved. Palmer & Krumhansl's Fig. 2 (2/4, 3/4, 4/4, 6/8) and Huron's *Sweet Anticipation* ch. 10 figures from Essen are the obvious sources, but neither text was accessible here (the ResearchGate copy of *Sweet Anticipation* only exposed front matter and ch. 1).
- Next step: compute these directly from the Essen corpus (kern files via music21 or humdrum), using the same beat-class method as Huron & Ommen.
- Palmer & Krumhansl's correlation coefficients and rating data were not retrieved.

## Q2. How do melodies differ between simple and compound metres (subdivision into 3, dotted rhythms, hemiola, 6/4 vs 3/2)?

### Takeaway
The retrieved computational work treats simple and compound metres as distinct categories that are nonetheless often confused. In meter-inference models trained on Essen, a 6/8-biased model still assigns many rhythms to 3/4 or 2/4. Jigs (6/8) and slides (12/8) are hard to tell apart from audio. Compound metres show autocorrelation peaks at multiples of 3 subdivision units.

### Cited Findings
- **Essen German subset:** 4,966 songs with a single time signature. The most frequent metres are 4/4, 2/4, 3/4 and 6/8, in that order of prominence (Fig. 2; no counts in the text). A balanced training set used 658 songs each of 2/4, 3/4 and 6/8 — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)
- **Same paper, enculturation training sets:** 1,136 rhythms per culture, made up of 950 in 2/4, 132 in 4/4, 35 in 3/4 and 19 in 3/8. This shows how heavily duple metres dominate this Essen sample (German vs Chinese sets) — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)
- **Inferential-bias experiment:** the 6/8-biased model classified 594 rhythms as one of the three triple-type metres (471 as 6/8, 83 as 3/4, 40 as 2/4). The 3/4-biased model classified 395 as 3/4. Both models assigned about half of the 2,048 test rhythms to 2/4 (1,059 and 1,045). The paper's count of test rhythms is internally inconsistent (211 patterns ×4 in the text vs 2,048 in Table 3) — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)
- **Irish traditional music corpus (*Foinn Seisiún*, 326 recordings):**
  - Simple-metre tunes (205): reel 139 (4/4), polka 28 (2/4), hornpipe 18 (4/4), barndance 6, waltz 5 (3/4), mazurka 4 (3/4), fling 3, song 2.
  - Compound-metre tunes (121): jig 104 (6/8), slide 14 (12/8), slip jig 3 (9/8).
  - Source: [Beauguitte/Duggan/Kelleher, "Rhythm Inference From Audio Recordings of Irish Traditional Music"](https://core.ac.uk/download/301311609.pdf)
- **Same paper, rhythm features:**
  - "The majority of the notes have the duration of a quaver."
  - Hornpipes and mazurkas are played with noticeable swing, which separates hornpipes from reels despite the shared 4/4.
  - For compound tunes, "more prominent peaks appear at multiples of 3" in the onset autocorrelation.
  - Slides were most often misclassified as jigs, since both are compound duple.
  - Source: [same](https://core.ac.uk/download/301311609.pdf)
- **IMA on Dutch folksongs (141 melodies, *Onder de groene linde*):** melodies of the same tune family notated in a *different* metre (6/8 vs 3/4 subgroups of "Frankrijk 2") fell to very low similarity ranks (100 to 128). The authors conclude that "a very different rhythmic structure expressed by a different meter notation" was the main cause of low ranks. Within metre subgroups, ranks were much better (Frankrijk 2b 3/4: mean rank 6.81; Frankrijk 2a 6/8: 24.88) — [ISMIR 2007](https://archives.ismir.net/ismir2007/paper/000293.pdf)

### Inferences
- In 6/8 vs 3/4 the same six eighth-note slots are grouped 3+3 vs 2+2+2. The IMA result suggests transcribers' choice between them follows real rhythmic structure, not arbitrary notation. So a generator should use different onset priors for 6/8 and 3/4 even though they share a bar length.
- Mutual confusion of jig and slide, and the dominance of 2/4 in model classification, suggest 12/8 vs 6/8 (and 6/8 vs 2/4) differ mainly in *phrase-level* grouping (bar length vs phrase length), not beat-level patterning. A generator should signal 12/8 through 4-beat phrase/cadence placement rather than through different within-beat rhythms.

### Gaps
- No corpus statistics were retrieved on dotted-rhythm frequency by metre, hemiola frequency in 3/4 and 6/8 repertoires, or 6/4 vs 3/2 usage.
- Not retrieved: London's *Hearing in Time* discussion of beat-subdivision floors (often cited as about 100 ms) and tactus preference (often cited as about 600 ms). Only the introduction was accessible, and it gives no numbers — [London, *Hearing in Time* intro](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf). Candidate sources not fetched: [Repp, London & Keller 2005, *Music Perception*](https://cdn.carleton.edu/uploads/sites/721/2021/12/Repp-London-Keller-2005-MP.pdf) and [London 2011 "Tactus ≠ Tempo"](https://cdn.carleton.edu/uploads/sites/721/2021/12/London-2011-Tactus-vs-Tempo.pdf).

## Q3. Are 3/8, 3/2 and 6/4 notational variants or distinct felt metres?

### Takeaway
London's position is that a notated metre is not a fixed felt metre. The same formal metric architecture is heard differently depending on tempo, which is why he proposes "tempo-metrical types" and a "many meters hypothesis". A generator should therefore define a metre as time signature + tempo, not time signature alone.

### Cited Findings
- **Metre as entrainment:** London defines meter as "a mode of attending", "a musically particular form of entrainment or attunement", applied to beats abstracted from the rhythmic surface. Rhythm is defined by inter-onset intervals, not sounded durations — [London, *Hearing in Time*, intro](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf)
- **Tempo dependence:** perceived meter changes with tempo even when "its formal architecture remains constant", hence "tempo-metrical types" — [same](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf)
- **Well-formedness:** metric hierarchies obey perceptual well-formedness constraints, including a global "maximal evenness" constraint. The book applies one set of constraints to Western and non-Western music and also treats non-isochronous meters (chs. 7 and 8) — [same](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf)
- **Many-meters hypothesis:** listeners learn context-specific, expressively timed patterns, possibly hundreds of them, rather than a few archetypal meters — [same](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf)
- **3/8 in a computational model:** van der Weij et al.'s model treats 3/8 as its own metrical category alongside 2/4, 3/4 and 4/4, with period in sixteenths and phase resolved to sixteenths. It considers 320 interpretations in total, or 48 if limited to 4/4, 2/4, 3/4 and 6/8 — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)

### Inferences
- Under London's framework, 3/8 at a fast tempo is likely felt as one beat per bar (a hypermetric "one"), while 3/4 at a moderate tempo has three felt beats. 6/4 vs 3/2 differ by grouping (2×3 vs 3×2) at the same total length. A generator should encode them as distinct grouping templates and attach a tempo range.
- Treat this as theory-derived design guidance. No corpus measurement supporting it was retrieved.

### Gaps
- No empirical study was retrieved that directly compares listener perception or corpus rhythm statistics for 3/8 vs 3/4, 3/2 vs 3/4, or 6/4 vs 3/2.
- London's specific tempo thresholds for when a 3/8 or 6/8 bar collapses to one or two beats were not retrieved.

## Q4. What computational models generate or evaluate rhythm conditioned on metre?

### Takeaway
The main lines are:
- Temperley's generative probabilistic metre/rhythm models, in which surface onsets are generated from metrical structure with level-dependent probabilities. The hierarchical-position model is judged the best trade-off.
- IDyOM-style variable-order Markov models with joint metre inference (van der Weij et al.).
- Inner Metric Analysis for onset-derived weights.
- Syncopation-transformation methods (Sioros et al.) that move onsets relative to a metrical template.

Evaluation tools include cross-entropy / information content, meter-classification accuracy, error-detection against distorted versions, and listener groove ratings.

### Cited Findings
- **Temperley (2007, 2009, 2010):** a family of probabilistic metrical models. Van der Weij et al. report that Temperley judged the **hierarchical position model** the best trade-off. Temperley (2010) is a generative model in which surface rhythms derive from an underlying metrical structure — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009); [London et al. 2016](https://core.ac.uk/download/83231804.pdf)
- **Temperley, *Music and Probability* (2007), rhythm model:**
  - Three metrical levels (tactus, upper, lower). Whether the upper level is duple or triple is a probability parameter estimated from the Essen Folk Song Collection.
  - Tested on 65 Essen melodies (Temperley's own performances).
  - In error detection with 10 distorted versions per melody, the undistorted version received higher probability in **82%** of cases.
  - Supra-tactus performance was good; tactus and sub-tactus were weaker than Temperley's earlier Melisma model.
  - Source: [Pearce, Müllensiefen, Lewis & Rhodes 2007 review, *Empirical Musicology Review* 2(4)](https://core.ac.uk/download/159560081.pdf)
- **Van der Weij, Pearce & Honing (2017), IDyOM with metrical inference:**
  - Onsets are quantised to 96th notes.
  - Metre-classification accuracy is about 38% / 67% / 71% at order bounds 0 / 1 / 4.
  - Joint metrical inference lowers average information content (IC 2.19 vs 2.29 at order 0; 1.34 vs 1.54 at order 4).
  - Cross-cultural transfer: German→German IC 1.21, score 0.84; Chinese→German IC 1.32, score 0.59.
  - Source: [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)
- **IMA implementation details:** at least 3 onsets per local meter, weight exponent p = 3, ℓ = 2. Similarity is the windowed Pearson correlation of weight profiles on a common grid, per one-bar window starting at the first full bar (upbeats ignored). The comparison baseline was SIMILE's rhytGauss — [ISMIR 2007](https://archives.ismir.net/ismir2007/paper/000293.pdf)
- **Sioros et al. (2014), "Syncopation creates the sensation of groove in synthesized music examples":**
  - Metrical template (4/4 only): quarter-note positions 1 and 3 are strong, 2 and 4 weak.
  - Transformations anticipate phrase-final notes, or notes on weak quarter positions, to earlier weaker positions at eighth or sixteenth level (8D8A, 8D16A, 16D8A, 16D16A).
  - "Density" transforms add notes without syncopation, as a control.
  - Exp. 1: n = 28, 12 melodies × 5 versions, 120 BPM. Exp. 2: n = 22.
  - Groove effect sizes vs quantised: Density 0.208 and 0.233; maximum syncopation 0.439; 8D 0.601; 8A 0.597. Moderate syncopation beat maximal syncopation, and "there is no simple relation between syncopation magnitude and groove."
  - Source: [Sioros, Miron, Davies, Gouyon & Madison 2014, *Frontiers in Psychology* 5:1036](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01036/full)
- **Syncopation measures cited there:** Longuet-Higgins & Lee (1984), where syncopation exists only against an established metre; Gómez et al. (2005, 2007), weighted metric-strength measures; Huron & Ommen (2006); Sioros & Guedes (2011); Song et al. (2013), where the position of a syncopation relative to the metre affects its perceived strength — [Sioros et al. 2014](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01036/full)

### Inferences
- **Generation:** a Temperley-style hierarchical-position model is the simplest metre-conditioned generator. For each metrical level, give a probability of an onset at that level given onsets at the level above. Swap the upper-level arity parameter (2 vs 3) and the beat-division arity (2 vs 3) to get 2/4, 3/4, 6/8, 9/8 and 12/8 from one model. Fit the parameters per metre from corpus counts (the Essen 4/4 table above is one fit target).
- **Evaluation:**
  - The cross-entropy of generated rhythms under a metre-specific model, compared with held-out human melodies in that metre.
  - Whether a meter-inference model (IDyOM/Temperley-style) recovers the intended time signature. The 67 to 71% accuracy on Essen sets a realistic human-data ceiling.
  - The correlation of the generated onset-position histogram with the corpus histogram (Palmer & Krumhansl-style). Murphy's rank-agreement test (2 of 120 pairwise inversions between Haydn and Essen) gives a sense of how closely two genuine repertoires agree.
  - IMA weight-profile correlation with the notated grid.
- **Syncopation:** syncopation should be moderate. Sioros's anticipation-by-one-eighth transforms gave the largest groove effect in 4/4. Equivalent templates for triple and compound metres would need defining, since the study was 4/4 only.

### Gaps
- Temperley 2010 (*Music Perception*, "Modeling common-practice rhythm") per-model cross-entropy values and level probabilities were not retrieved. The *EMR* review gives no parameter values.
- Not fetched: Sioros & Guedes's own syncopation measure and its handling of ternary subdivisions. Candidate PDFs: [SiorosGuedes2014](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/4/23414/files/2022/01/SiorosGuedes2014.pdf), [SiorosGuedes2014b](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/4/23414/files/2022/01/SiorosGuedes2014b.pdf), and [ISMIR 2012 "On Measuring Syncopation to Drive an Interactive Music System"](https://ir.webis.de/anthology/2012.ismir_conference-2012.48).
- No retrieved source documented metre-conditioned *neural* symbolic generators (time-signature tokens in folk-rnn, Music Transformer, etc.) or metre-specific evaluation metrics. A search returned only general generation papers, none verified as relevant.
- Toussaint's rhythm-complexity measures (WNBD, off-beatness, Keith) were not retrieved.

## Q5. What corpus statistics exist for 12/8 and 9/8 in sung repertoires (blues/gospel 12/8, slip jigs 9/8, slides 12/8)?

### Takeaway
Only instrumental Irish data was found, and 9/8 and 12/8 are rare there: 3 slip jigs (9/8) and 14 slides (12/8) among 326 tunes, against 104 jigs (6/8). No corpus statistics for 12/8 blues or gospel singing were found. The only quantified 12/8-like onset data comes from Malian drumming, which does *not* follow a Western-style hierarchy.

### Cited Findings
- ***Foinn Seisiún* corpus, 326 tunes:** slip jig 9/8 = 3; slide 12/8 = 14; jig 6/8 = 104. So 121 compound tunes vs 205 simple ones, with 9/8 + 12/8 = 17 tunes (5.2%). Slides were frequently classified as jigs — [Rhythm Inference From Audio Recordings of Irish Traditional Music](https://core.ac.uk/download/301311609.pdf)
- **Malian jembe music (Manjanin, Woloso, Maraka; 15 performances, about 42,297 onsets):** an isochronous four-beat cycle with consistently ternary subdivision, "analogous to 12/8". On-beat positions other than the downbeat are articulated less often than the preceding upbeat position. Mid-beat positions are much rarer than their neighbours. Tempo rose from about 120 to 180 bpm within performances — [London, Polak & Jacoby 2016](https://core.ac.uk/download/83231804.pdf)
- **Essen sample sizes for compound metres:** the German Essen subset's most common metres include 6/8, but the paper prints no counts for 9/8 or 12/8 — [van der Weij et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)

### Inferences
- For a 12/8 generator, the Malian data warns that a ternary-subdivided four-beat metre does not automatically yield a "downbeat > beats > subdivisions" onset profile. Stylistic idiom can invert beat and pre-beat weights.
- For blues/gospel 12/8, the engine should probably treat the onset profile as genre-specific rather than inherit it from 6/8 folk song. This is inference only; no blues/gospel counts were found.
- Since 9/8 and 12/8 are rare even in Irish dance music, a corpus-trained model will be data-starved for them. Deriving their priors compositionally from 6/8 beat-level patterns (3 or 4 dotted-quarter beats) is a pragmatic option.

### Gaps
- No corpus statistics were retrieved for 12/8 blues, gospel, doo-wop or hymn repertoires (onset profiles, shuffle ratios, or proportion of songs in 12/8).
- No onset-position data for slip jigs (9/8) or slides (12/8) was retrieved. thesession.org tune-type counts were not obtained.
- No sung-repertoire (lyric-bearing) 9/8 corpus was found.
