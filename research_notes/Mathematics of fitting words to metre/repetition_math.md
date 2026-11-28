# Mathematics of repetition and variation in song melodies and rhythms

Reading notes for the report writer.
- Every bullet under "Cited Findings" was read from the linked page in this session (via a fetch summary; I did not see raw PDFs, so page-exact wording and table cells should be re-checked before quoting).
- Anything I know only from background knowledge and could not re-verify is placed under "Gaps" and tagged **[recalled, unverified]**. Treat those as leads, not citations.
- Engine context supplied by the coordinator (not a published figure): engine builds repeat a two-bar rhythm exactly about 1 time in 100; the project's own corpus of pop melodies in 3/4 repeats it exactly about 23 times in 100.
- No data from TheSession.org was used, downloaded or processed.

## 1. Measured rates: how often bars, two-bar units and phrases repeat exactly or with small edits in popular music

### Takeaway
No published study I could find reports the exact statistic the engine needs (share of two-bar melodic rhythm cells that exactly repeat an earlier cell in pop songs). The nearest published numbers all point the same way as the project's 23 percent: 65 to 85 percent of a pop song's duration is repeated material, over half of phrases repeat immediately, about a third of old popular-song phrases have strictly repeating bar-rhythm layouts, and the standard 16-bar SRDC/sentence layout builds in one restated 4-bar unit out of four. An exact-repeat rate of 1 percent is far outside every measured figure.

### Cited Findings

**Song-level and phrase-level repetition (Dai et al., POP909 and PDSA)**
- Datasets: POP909 = 909 Chinese pop songs (MIDI); PDSA = 348 American popular songs dated 1580 to 1924 (MusicXML). Only 4/4 songs analysed. Licence not stated in the paper. — [Dai et al., "What is missing in deep music generation? A study of repetition and structure in popular music", arXiv 2209.00182](https://arxiv.org/pdf/2209.00182)
- Phrases are defined as approximate repetitions of sequences of 4 or more measures; rhythm is described with onset patterns per half-note unit, onsets quantised to sixteenth notes. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- For 79% of POP909 songs, 15% to 35% of the duration is new material and the rest (65% to 85%) is repetition. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- In POP909 more than 50% of phrases repeat immediately, and almost all phrases have their repeat within the first quarter of the song. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- In PDSA, 7% of phrases have the same rhythm pattern in every measure, and 28% of phrases follow one of the bar-level rhythm layouts abab, aabbaabb, aba or abababa. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- Rhythm vocabulary is small in older popular song: PDSA uses 54 distinct half-note onset patterns, POP909 uses all 128 possible. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- Within-song statistics predict the next note about 1 bit better than cross-song statistics; the best mix for predicting the first eight notes of a repeat is 70% within-song model, 30% corpus model, i.e. P(x) = 0.7 P_song(x) + 0.3 P_corpus(x). — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- Cross-entropy by position (corpus model): over 3.5 bits at section starts, about 3.2 bits at other phrase starts, about 2.6 bits in phrase middles. Novelty is concentrated at phrase and section starts. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- A Music Transformer trained on POP909 produces a larger rhythm-pattern vocabulary than real songs (plot only, no table), i.e. generators under-repeat rhythm, the same fault the engine shows. — [Dai et al.](https://arxiv.org/pdf/2209.00182)

**Form-level repetition (Summach; de Clercq and Temperley)**
- Corpus: 700 songs, Billboard annual Top 20, 1955 to 1989; it contains 93 strophic and 202 AABA songs. — [Summach, "The Structure, Function, and Genesis of the Prechorus", MTO 17.3](https://www.mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.php)
- SRDC = statement, restatement (or response), departure, conclusion (Everett's term). R "usually repeats S, though it may respond with different material". The pattern is aa'ba' or aa'bc. S and R are typically four bars each; the 16-bar sentence is the common paradigm; D+C together must be longer than S or R (short-short-long). — [Summach](https://www.mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.php)
- Share of AABA and strophic songs whose strophes are sentential (SRDC): under one third in 1959, 60% by 1964, average 43% in 1965 to 1969, about 60% through 1989. More than a quarter of all 700 songs contain a sentential module; strophes are sentential almost half the time. — [Summach](https://www.mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.php)
- Prechorus: about a third of verse-chorus songs in 1965 to 1969, 60% in the late 1980s. — [Summach](https://www.mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.php)
- Textbook phrase layouts in pop/rock: a phrase is typically four bars and one lyric line; two-part sections are aa' (second half reuses the first; a prime marks new lyrics, a new ending or variation); two-part ab is "very rarely" used; three-part aa'b (12-bar blues); four-part srdc as aaba or aabc, with abcd or abca only "occasionally". Qualitative only, no counts. — [Open Music Theory, "Melody and Phrasing"](https://viva.pressbooks.pub/openmusictheory/chapter/melody-and-phrasing/)
- Rolling Stone 200 corpus: 99% (DT) or 90% (TdC) of songs have a verse, 68% or 59% a chorus, 31% or 38% a bridge, about 6% a prechorus. This paper gives no bar-level repetition rate. — [de Clercq, "Interactions between Harmony and Form in a Corpus of Rock Music", JMT 2017](https://www.midside.com/publications/declercq_2017_jmt.pdf)

**Rhythm statistics without a direct repetition rate (White, Pater and Breen)**
- Corpora: 192 melodies from the de Clercq and Temperley Rolling Stone corpus (1955 to 1997) and 24 Billboard top-five songs (2015 to 2019), 4/4 only. Licences not stated. — [White, Pater and Breen, "A comparative analysis of melodic rhythm in two corpora of American popular music", J. Math. Music 2022](https://par.nsf.gov/servlets/purl/10356498)
- Events per bar: 4.29 (older) vs 6.75 (newer); events per second 1.87 vs 2.71; normalised entropy of the 16-position onset profile H/log n = 0.81 vs 0.89. — [White, Pater and Breen](https://par.nsf.gov/servlets/purl/10356498)
- Repetition proxy: each song's top 50 rhythmic 4-grams (four consecutive metrically indexed onsets) are ranked by frequency and fitted with a logarithmic curve; slope is -4.22 (older) vs -6.93 (newer). A steeper slope means a few rhythmic cells are reused more heavily, so recent pop is rhythmically more repetitive at the cell level. Bar-level and two-bar repetition were not measured; verse-to-verse variation was not measured. — [White, Pater and Breen](https://par.nsf.gov/servlets/purl/10356498)

**Whole-repertoire and compression figures**
- Huron and Ollen (2004), as reported in a review of Margulis: about 94% of musical passages are literally repeated at some later point, in a sample covering five continents and five centuries. — [Albrecht, review of Margulis "On Repeat", MTO 20.4](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.albrecht.php)
- Margulis's working definition is literal repetition, with notated repetition "an imperfect but pragmatic proxy for acoustic repetition". — [Albrecht review](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.albrecht.php)
- Lyrics: about 15,000 Billboard Hot 100 songs, 1958 to 2017, compressed with Lempel-Ziv. The average 1960 song shrinks 45.7%; 2014 is the most repetitive year, with the average song compressing 22% more than in 1960 (relative); Top-10 songs were more repetitive than the rest in every year 1960 to 2015; extremes are "Around the World" at 98% and "Cheap Thrills" at 76%; artist averages run from 38% (Brad Paisley) to 60% (Backstreet Boys). — [Morris, "Are Pop Lyrics Getting More Repetitive?", The Pudding 2017](https://pudding.cool/2017/05/song-repetition/)
- Melody analogue: 718 MIDI encodings of Billboard year-end Top-20 songs, 1956 to 2015, melody strings compressed with Lempel-Ziv 1977. Compressibility rises over time (R = +.23); no significant difference between Top 10 and positions 11 to 20 (p = .070); much less spread after about 2001. Undergraduate poster; no mean compressibility reported. — [Kent State, "Melodies of Pop: Measuring Melodic Repetitiveness Throughout the Billboard Era"](https://oaks.kent.edu/ugresearch/2020/art/melodies-pop-measuring-melodic-repetitiveness-throughout-billboard-era)
- Audio scale: 464,411 recordings, 1955 to 2010 (Million Song Dataset). Pitch codeword rank-frequency follows a power law with exponent 2.18 ± 0.06, stable across years; year-to-year rank correlation of codewords 0.97 ± 0.02; pitch-transition networks show clustering falling from about 0.65 to 0.45 and path length rising from 2.9 to 3.2, read as more restricted transitions; loudness rises 0.13 dB per year. The article is CC BY-NC-SA 3.0. — [Serrà et al., "Measuring the Evolution of Contemporary Western Popular Music", Sci. Rep. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3405292)
- Chart success: 2,480 songs (1,029 number ones, 1,451 that never rose above position 90), 1958 to 2012. Each additional chorus repetition raised the likelihood of reaching number one rather than staying at the bottom by 14.5%; chorus repetitions ranged from 1 to 16; a ceiling effect was found for word repetition (threshold not reported in this account). Secondary press account of Nunes, Ordanini and Valsesia (2015). — [Pacific Standard, "Yeah, Yeah, Yeah: Repetitive Lyrics Boost Songs' Popularity"](https://psmag.com/?p=30843)

**Pitch-pattern repetition in art and folk melody (for comparison)**
- Pitch-class windows of 4 notes in 852 keyboard pieces: literal repetition occurs about 14 times more often than random forms within the same transformation orbit and 3.4 times more than in shuffled lines; transposition 1.56 times chance (2 times at 5 notes); inversion is avoided (0.84); retrograde is at chance. Folk phrases (MTC-ANN, 1,890 phrases; Essen, 44,765 phrases) and themes: repetition dominates over mirror forms in longer melodies. Rhythm and metre were not analysed. Licences as stated there: MTC-ANN 2.0.1 CC BY-NC-SA 3.0; Essen CC BY-SA 4.0. — ["Symmetric Structure and Motivic Transformation in Melodies, Phrases, and Themes", arXiv 2610.40303](https://arxiv.org/pdf/2610.40303)

### Inferences
- Arithmetic from Summach's SRDC description: in a 16-bar SRDC unit made of eight two-bar cells, R restates S, so 2 of 8 cells (25%) repeat an earlier cell within the unit even if D and C are entirely new. Where C returns to S material (aa'ba') the figure rises toward 4 of 8 (50%). With 43% to 60% of strophes sentential, a within-section exact-or-near repeat rate for two-bar rhythm in the range of roughly 20% to 35% is what the form literature predicts. The project's own 23% sits inside that range.
- PDSA: 7% + 28% = 35% of phrases have a strictly repeating bar-rhythm layout (all bars the same, or alternating). For a four-bar phrase laid out abab, the second two-bar cell exactly repeats the first. So about a third of phrases in that corpus contain an exact internal rhythmic repeat at the one- or two-bar level. This is a floor on "some exact repetition", not the same statistic as the 23%, but it is the same order of size.
- The engine's 1% is about 20 to 30 times below every corpus figure. The Transformer result (larger rhythm vocabulary than real songs) shows this is a known failure of generators, not a quirk.
- Because pitch is more often varied than rhythm in restatements (the prime in aa' marks "new ending or variation"), the safest design is to make rhythm the thing that is copied exactly and pitch the thing that is varied at the cadence. This direction is supported qualitatively by Open Music Theory and by the folk-song evidence in section 3; I found no table that splits "rhythm exact, pitch varied" from the reverse in a pop corpus.
- Across-verse repetition is far higher than within-section repetition: if 65% to 85% of a song is repeated material and choruses and verses recur whole, the across-section exact-repeat rate for two-bar rhythm should be well above 50%. No direct count found.

### Gaps
- No published table of "share of two-bar melodic rhythm cells exactly equal to an earlier cell" for pop/rock, split by within-section and across-verse. The CoCoPops / Rolling Stone melodic transcriptions and the Hooktheory-derived datasets would allow it to be computed, but I found no paper that reports it.
- No published split of exact versus near-exact (1 or 2 edits) repetition for rhythm versus pitch in pop melody.
- I could not reach the original Nunes, Ordanini and Valsesia paper (J. Consumer Psychology 2015) or Huron and Ollen (2004); the numbers above are second-hand.
- **[recalled, unverified]** Huron's "Sweet Anticipation" (2006) is the usual citation for the 94% figure and for the statement that most music heard is music heard before. Check the book for the exact sample (50 works is the number I recall).
- **[recalled, unverified]** Burgoyne's McGill Billboard corpus (chord and form annotations for about 740 distinct songs, 1958 to 1991) is released under CC0; POP909 is on GitHub under the MIT licence; the Rolling Stone corpus is freely downloadable for research with no formal licence text. Verify before use.
- **[recalled, unverified]** Burgoyne et al.'s "Hooked on Music" experiments found that melodic repetitiveness and conventionality predict recognition speed (catchiness). I did not fetch it.

## 2. Formal measures and models of repetition (definitions)

### Takeaway
The measures divide into four families: compression (how much shorter the piece becomes when repeats are factored out), information dynamics (how predictable each event is given the past), pattern discovery (which point sets recur under translation) and string or geometric distances between two rhythm cells. For a two-bar engine target, the practical tools are an exact-match rate on onset strings, a small edit or swap distance for "near repeats", and a compression ratio as a whole-song check.

### Cited Findings

**Point-set compression (Meredith: SIA, SIATEC, COSIATEC)**
- A piece is a set D of points (t, p): onset time in tatums and pitch (morphetic or chromatic). Two patterns are translationally equivalent if one equals the other plus a fixed vector v. — [Meredith, "COSIATEC and SIATECCompress: Pattern discovery by geometric compression"](https://core.ac.uk/download/60675404.pdf)
- Maximal translatable pattern: MTP(v, D) = { p in D : p + v in D }. — [Meredith](https://core.ac.uk/download/60675404.pdf)
- Translational equivalence class: TEC(P, D) = { Q subset of D : Q is a translate of P }, i.e. all exact occurrences of a pattern. Listing n occurrences of an m-point pattern costs 2mn integers; pattern plus translators costs 2(m + n - 1). — [Meredith](https://core.ac.uk/download/60675404.pdf)
- Covered set COV(T) = union of all occurrences in the TEC. Compression ratio of a TEC: CR(T) = |COV(T)| / (|P(T)| + |V(T)| - 1), where P is the pattern and V the translator set. Compactness = points in the pattern divided by all dataset points inside the pattern's bounding box. — [Meredith](https://core.ac.uk/download/60675404.pdf)
- SIA sorts all difference vectors p_i - p_j and reads each run of equal vectors as an MTP; SIATEC adds all occurrences of each MTP (worst case O(n^3)); COSIATEC greedily takes the best TEC (by compression ratio, then compactness), removes its covered set and repeats, giving a strict partition of the piece. — [Meredith](https://core.ac.uk/download/60675404.pdf)
- COSIATEC typically reaches compression ratios "between 2 and 4" on classical and baroque music. On the JKU Patterns Development Database the best mean three-layer F1 was 0.49. — [Meredith](https://core.ac.uk/download/60675404.pdf)

**String compression**
- Lempel-Ziv compression is used as the repetition measure for lyrics: percent size reduction = 1 - (compressed length / original length). — [Morris, The Pudding](https://pudding.cool/2017/05/song-repetition/)
- The same measure applied to melody strings extracted with Humdrum. — [Kent State poster](https://oaks.kent.edu/ugresearch/2020/art/melodies-pop-measuring-melodic-repetitiveness-throughout-billboard-era)

**Information dynamics**
- Information content (surprise) of an event: IC(x) = -log2 p(x | context). Entropy (uncertainty) before the event: H = sum over x of p(x) IC(x). In IDyOM these come from a variable-order Markov model that combines a long-term model (trained on a corpus) with a short-term model learned within the piece; it is the short-term model that rewards within-song repetition. Formulas are my standard rendering of the paper's verbal definitions. — [Gold et al., "Predictability and uncertainty in the pleasure of music", J. Neurosci. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867811)
- Abdallah and Plumbley, for a Markov chain with transition matrix a (a_ij = p(next = i | now = j)) and stationary distribution pi:
  - Surprisingness L(i | j) = -log a_ij.
  - Entropy rate h(a) = - sum_ij pi_j a_ij log a_ij.
  - Redundancy (Dubnov's "information rate") = H(pi) - h(a), where H(pi) = - sum_i pi_i log pi_i.
  - Instantaneous predictive information I(i | j) = sum_k a_ki (log a_ki - log [a^2]_kj): the KL divergence between the forecast of the following symbol after and before seeing the current one.
  - Predictive information rate PIR = I(X; Y | Z) = H(X | Z) - H(X | Y, Z); for a Markov chain PIR = h(a^2) - h(a).
  — [Abdallah and Plumbley, "Information dynamics: patterns of expectation and surprise in the perception of music"](https://core.ac.uk/download/30696123.pdf)
- PIR is zero for a fully deterministic chain and for a memoryless one, and is highest at intermediate entropy rate; for N > 3 states the maximum appears close to but possibly below (1/2) log N (unproven). Redundancy, by contrast, is maximised by a deterministic cycle. The authors offer PIR as a formal version of the inverted U. — [Abdallah and Plumbley](https://core.ac.uk/download/30696123.pdf)
- Applied to Philip Glass's "Gradus", an adaptive first-order model averaged 1.29 nats per symbol against 2.48 for a naive encoding; the first note of each bar is about 0.9 nats more surprising than average. — [Abdallah and Plumbley](https://core.ac.uk/download/30696123.pdf)
- Normalised entropy of an onset profile: H / log n, with H = - sum p(x_i) log p(x_i) over n metric positions. — [White, Pater and Breen](https://par.nsf.gov/servlets/purl/10356498)

**Group-theoretic repetition measures**
- Treat a window of m pitch classes as an element acted on by G = D12 x Dm (|G| = 48m; transposition, inversion, retrograde, cyclic shift). Orbit entropy H_orbit = - sum_o P(o) log2 P(o); number of orbits K(m) = 19, 163, 1,110, 10,962 for m = 3 to 6; deployment ratio eta = mean within-orbit entropy / mean orbit capacity, in [0, 1]; enrichment O/E of each relation type against shuffled surrogates. Only window pairs at distance >= m are compared. — [arXiv 2610.40303](https://arxiv.org/pdf/2610.40303)

**Rhythm distances between two cells (Toussaint)**
- Rhythms are binary onset strings on a tatum grid. Hamming distance = number of positions that differ, O(n). — [Toussaint, "A Comparison of Rhythmic Similarity Measures", ISMIR 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)
- Euclidean interval-vector distance = Euclidean distance between the two vectors of inter-onset intervals. Interval-ratio distance (Coyle and Shmulevich) works on x_i = t_(i+1) / t_i. — [Toussaint 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)
- Swap distance = minimum number of interchanges of an adjacent onset and rest needed to turn one rhythm into the other (equal onset counts; O(n) via onset positions). For unequal counts the directed swap distance moves every onset of the denser rhythm onto an onset of the sparser one, each sparse onset receiving at least one. — [Toussaint 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)
- Chronotonic distance: draw each rhythm as a step function whose height over each inter-onset interval equals that interval's length, then take the area between the two functions, K = integral |f1(x) - f2(x)| dx. O(n). — [Toussaint 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)
- In Toussaint's phylogenetic tests the chronotonic distance performed best overall and swap distance a close second; he warns against generalising beyond the small rhythm families tested. — [Toussaint 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)

**Structure evaluation**
- Boundary F-measure: P = hits / estimated boundaries, R = hits / annotated boundaries, F_alpha = (1 + alpha^2) P R / (alpha^2 P + R); listeners weight precision more, with alpha = 0.58 the first value giving significant agreement. — [Nieto et al., "Perceptual Analysis of the F-Measure for Evaluating Section Boundaries in Music", ISMIR 2014](https://archives.ismir.net/ismir2014/paper/000124.pdf)

**Grammars of line and stanza repetition**
- Folk-verse lines sit on a 16-position grid (2 hemistichs, 4 dipods, 8 feet). Line types by truncation: 4 (full), 3f (three beats plus feminine ending), 3 (three beats, final foot empty), G ("Green-O"). Greater truncation makes a more salient line break (cadentiality order G, 3f, 3). Of 625 logical four-line combinations only a small set is attested (4444, 4343, 4443, 3333, G3G3, 4G4G, 3343 and others); constraints are saliency, parallelism and long-last, ranked differently per song (factorial typology). — [Hayes, course handout on Hayes and MacEachern quatrain form](https://www.brucehayes.org/251HayesSchuhMetrics/handouts/12QuatrainI.pdf)

### Inferences
- Suggested engine metrics, all computable from the definitions above:
  - Exact two-bar repeat rate: encode each two-bar cell as a binary onset string on the tatum grid (18 or 24 positions in 3/4 depending on eighth or sixteenth tatum; ties count as no onset). Rate = cells equal to any earlier cell in the section / (cells - 1).
  - Near-repeat rate: same, with directed swap distance or Hamming distance <= 1 or 2 counted as a varied repeat. Chronotonic distance is better when note counts differ, which is exactly the changed-syllable case.
  - Whole-song check: COSIATEC-style compression ratio on (onset, pitch) points, or LZ compression of the onset string. A real song should land well above 2; a build that refits every line will land near 1.
  - Short-term-model information content: train a within-song n-gram on the rhythm string; mean IC should fall in later lines of a section. Dai et al.'s 0.7 / 0.3 mix is a ready prior for how much the song's own material should outweigh corpus habits.
- The Hayes and MacEachern grammar implies that the admissible unit of repetition is the line type on a fixed grid, not the note list: two lines of type 4 share the same strong positions even when syllable counts differ. That is a formal licence for "exact rhythm on the strong positions, free filling of weak positions".

### Gaps
- I could not open the MIREX "Discovery of Repeated Themes and Sections" page (blocked) or Collins's papers. **[recalled, unverified]** definitions: cardinality score s(P, Q) = max over translations of |P ∩ (Q + v)| / max(|P|, |Q|); establishment precision / recall average, over output or ground-truth patterns, the best cardinality score against any occurrence of any pattern on the other side; occurrence precision / recall do the same over occurrences but only for pattern pairs whose establishment score exceeds c (c = 0.75 and 0.5); three-layer F1 nests an F1 over notes inside an F1 over occurrences inside an F1 over patterns. Ground truth is the JKU Patterns Development Database (five classical pieces). Verify against Collins's task description.
- **[recalled, unverified]** Levenshtein edit distance on rhythm strings: minimum number of insertions, deletions and substitutions, computed by dynamic programming in O(nm); Post and Toussaint ("The edit distance as a measure of perceived rhythmic similarity") report that it tracks human similarity judgements better than swap or chronotonic distance. A search result for this paper appeared but I did not read it.
- **[recalled, unverified]** Lempel-Ziv complexity (1976): number of distinct phrases in the left-to-right parsing of the string; normalised as c(n) log_k(n) / n for alphabet size k.
- **[recalled, unverified]** GTTM (Lerdahl and Jackendoff 1983): Grouping Preference Rule 6 and Metrical Preference Rule 1 say parallel passages should receive parallel grouping and metrical structure; the theory gives no numeric definition of parallelism. Bod's data-oriented parsing of the Essen collection combined likelihood and simplicity and reached about 81% phrase-boundary F-score. Conklin's distinctive patterns rank a pattern by the ratio of its frequency in a target corpus to its frequency in an anticorpus. Dubnov's information rate IR = I(past; present). Foote's self-similarity matrix S(i, j) = similarity of feature frames i and j, with repeats appearing as off-diagonal stripes and a checkerboard kernel along the diagonal giving a novelty curve. None of these were fetched this session.
- No probabilistic grammar of pop-song phrase repetition with published rule probabilities was found.

## 3. Variation under changing text: how strophic songs fit one tune to verses with different syllable counts

### Takeaway
The linguistics literature models a tune as a fixed grid of strong and weak positions, with the text free to fill or leave empty the weak positions. Strong beats and their stress matches are what stay constant across verses; added or missing syllables are absorbed in weak positions, at the line start (pickup) and at the line end (truncation), almost never by melisma. Published work gives rules and a few counts, but no corpus table of "how many notes a later verse changes".

### Cited Findings

**The grid model and its constraints (Hayes; Hayes and Kaun; Hayes and MacEachern)**
- Textsetting is defined as the problem of aligning the syllables of a new stanza to the rhythm of a song the singer already knows; speakers do this consistently ("productive textsetting ability"). Four ranked, violable goals: (a) match stress to strong positions, (b) avoid long lapses with no syllable onset, (c) avoid extreme syllable compression, (d) align phonological phrase boundaries with line boundaries. Formalised in Optimality Theory: a good setting often violates a lower goal to satisfy a higher one. Data: 346 lines set by nine speakers (longer version 670 lines); free tab-delimited download, no licence stated. — [Hayes, "Textsetting as Constraint Conflict"](https://brucehayes.org/Textsetting)
- Experiment: 670 English folk-song lines (Sharp's collection), ten speakers chanting each line. Speakers produced on average 3.41 different settings per line; the most popular setting averaged 6.7 of 11 votes. Transcription reliability 99.6% per position. — [Hayes and Kaun, "The role of phonological phrasing in sung and chanted verse" (1996)](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- A four-beat line has 16 terminal positions; syllables go on the four strong and eight medium positions and use the weakest positions sparingly. No line in the corpus fills more than 14 of 16 positions. A syllable is taken to last until the next begins. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- Headless settings (nothing in the first two positions) are 10.9% of settings (760 of 6,998). Truncation takes two forms: Green-O lines and three-beat lines with a silent fourth beat. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- Stress Matching is the main constraint: rises and falls in stress should match rises and falls in grid strength; an empty position counts as weaker than any stressless syllable. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- Duration rule: a syllable's natural length should set its number of grid slots. Long syllables, and syllables at word end and especially phrase end, get the long slot; stress plus phrasing explain about half the variance in syllable duration (r^2 = .532 on 100 lines). Even rhythm is the most common outcome; dotted rhythm goes to long stressed syllables, Scotch snap to short stressed ones. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- Mismatches (stressed syllable on a weak position) are rare at line start and cluster in the final dipod, as a last resort after sliding syllables, truncating, or stealing a position from the neighbouring line. Of 17 line-final inversions in the original settings, 12 are in unrhymed lines. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)
- Corpus of 1,028 Appalachian folk songs: a 16-position grid usually suffices per line. In one grid family lines usually start with one or two stressless syllables before the first strong beat (pickup); in the other they start on the stress. Line-final syllables rarely fill the last grid position. — [Hayes and MacEachern, "Are there lines in folk poetry?" (1996)](https://www.brucehayes.org/papers/HayesAndMacEachern1996AreThereLinesInFolkPoetry.pdf)
- "Theft": about 10.4% of the 1,028 songs (107) borrow grid positions from a neighbouring line to hold extra syllables. Leftward theft takes at most the last strong beat of the preceding line and is stable through the song; rightward theft takes only weak or medium positions, is sporadic, and rarely reaches the next line's first strong beat. — [Hayes and MacEachern](https://www.brucehayes.org/papers/HayesAndMacEachern1996AreThereLinesInFolkPoetry.pdf)

**Corpus statistics on syllable-note alignment (Dutch folk song)**
- Corpus: 3,724 songs from MTC-FS; 3,973 stanzas, 20,662 phrases, 185,263 notes, 176,708 syllables. — [De Castro-Arrazola, van Kranenburg and Janssen, "Computational textsetting analysis of Dutch folk songs" (FMA 2015)](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Only 4.46% of syllables are melismas (more than one note). Syllable to note is otherwise one to one. — [De Castro-Arrazola et al.](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Method: for each pair of consecutive syllables, code the change in stress (-, =, +) and in metric prominence (-, =, +); association factor = observed / expected frequency. Stress rising while prominence falls = 0.36; stress falling while prominence rises = 0.26; matched movement 1.60 to 1.77. Values under 0.5 are treated as avoided. The ban on stress-up, prominence-down is stricter at phrase end; the reverse mismatch is relaxed phrase-finally and next to melismas. — [De Castro-Arrazola et al.](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- This paper does not compare stanzas of the same song with one another. — [De Castro-Arrazola et al.](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)

**Restatement variation in pop**
- In pop/rock phrase layouts the restatement is written a' when it carries new lyrics, a new ending or other variation; no counts given. — [Open Music Theory](https://viva.pressbooks.pub/openmusictheory/chapter/melody-and-phrasing/)

### Inferences
- With melisma at under 5% of syllables, a verse line with one more syllable almost always has one more note, and a line with one fewer has one fewer note (or a tie). So in strophic song, note-count changes between verses track syllable-count changes close to one for one.
- Rules for an engine, read off the constraints above (order of preference):
  1. Keep every strong-position onset of the model line (the four strong positions of the 16-slot grid, or beat 1 of each bar in 3/4). These are the rhythm's identity.
  2. Extra unstressed syllable at the line start: add a pickup in the weak positions before the first strong beat (borrowing from the end of the previous line is the commonest stable form of "theft").
  3. Extra unstressed syllable inside the line: split a medium or long note into two shorter ones on a weak position. Do not create extreme compression (goal c) and do not fill more than 14 of 16 slots.
  4. Missing syllable: tie two notes (hold the earlier syllable to the next onset), preferably lengthening a stressed, long or phrase-final syllable (duration rule). A lapse is worse than a long note (goal b), so tie rather than rest.
  5. Line end: allow masculine or feminine ending to differ (types 4 vs 3f vs 3) only if the quatrain pattern stays among the attested types; leave the last grid slot empty.
  6. Melisma only as a last resort and mainly phrase-finally.
- The Hayes and Kaun result that ten speakers gave 3.41 settings per line, with the modal setting taking about 61% of votes (6.7 of 11), means there is no single correct refit. It also means that the engine's habit of refitting almost every line is not itself wrong; the fault is that refits change strong-position onsets too. A measure of "exact repetition" that looks only at strong and medium positions would be the linguistically motivated one.
- Suggested dual target: (i) exact onset-string identity on the full tatum grid for cells whose syllable counts match; (ii) identity on the strong and medium positions only ("skeleton identity") for cells whose syllable counts differ.

### Gaps
- No corpus count was found of how often verse 2 changes the rhythm of verse 1 in pop, rock, hymn or folk song, or by how many notes. This could be computed from MTC-FS (multiple stanzas underlaid) or from CoCoPops transcriptions; nobody appears to have published it.
- No published statistics on variation between repeated choruses (ad libs, final-chorus lifts). Qualitative discussion only.
- Kiparsky's "A modular metrics for folk verse" (which rebuilds the Hayes and MacEachern typology from independent metre, rhythm and text modules) and Halle and Lerdahl's 1993 generative textsetting model appeared in search results but were not read. Dell and Halle's French and English comparison likewise.
- Hymnody: I found no quantitative source on how metrical-psalm or hymn tunes absorb irregular syllable counts. **[recalled, unverified]** the hymn-book convention is to print slurs for two notes on one syllable and small or dotted-tie notes where a stanza has an extra syllable, and common-metre tunes are interchangeable by syllable count (8.6.8.6), which avoids the problem by design.
- Contrafacta: no computational study with numbers found.
- **[recalled, unverified]** Janssen, Burgoyne and Honing (2017, Frontiers in Psychology, "Predicting variation of folk songs") found that phrases which repeat within their melody, are short, and contain highly expected intervals are the most stable across variants in the Dutch MTC-ANN corpus. The page was blocked this session.
- **[recalled, unverified]** MTC-FS and MTC-ANN are distributed by the Meertens Institute under CC BY-NC-SA 3.0 (confirmed above only for MTC-ANN 2.0.1, via a third paper).

## 4. Is there an optimal amount of repetition? Inverted-U evidence and a target band

### Takeaway
The evidence for an inverted U between predictability and liking is strong and replicated, and repetition is the main thing that lowers information content, so there is a preferred middle. But no study expresses the optimum as a percentage of repeated bars. The defensible engineering target is the corpus rate itself, with a band wide enough to cover form differences.

### Cited Findings
- Review of 57 studies over about 115 years: 50 (87.7%) are compatible with an inverted-U relation between liking and familiarity or complexity, 5 (8.8%) mixed, 2 (3.5%) incompatible. — [Chmiel and Schubert, "Back to the inverted-U for music preference: A review of the literature", Psychology of Music 2017](https://researchers.westernsydney.edu.au/en/publications/back-to-the-inverted-u-for-music-preference-a-review-of-the-liter/)
- Gold et al., Study 1: 43 listeners, 55 real monophonic excerpts of about 30 s; IDyOM (trained on 903 melodies) supplies duration-weighted mean information content (IC) and entropy. Liking has significant quadratic effects of both that beat linear fits: IC linear beta = -0.21, quadratic beta = -0.09 (26.3% of variance); entropy linear -0.09, quadratic -0.06 (19.1%). — [Gold et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867811)
- Study 2: 27 listeners, 12 excerpts each heard 7 times: IC quadratic beta = -0.18 (41.6% of variance); entropy linear -0.31, quadratic -0.25 (34.9%). Liking declined over the seven hearings, and the inverted-U shape held across repetitions (interaction p = .38). — [Gold et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867811)
- Interaction pattern: when uncertainty is low, high surprise is disliked and low or medium surprise are liked equally; when uncertainty is high, low surprise is preferred. Individual fits vary widely (per-listener R^2 from 0.005 to 0.42 in Study 1; 31 of 43 listeners show the negative quadratic). — [Gold et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867811)
- Cheung et al.: about 80,000 chords from US Billboard pop songs modelled by machine learning; chords were most pleasurable either when uncertainty was low and surprise high, or when uncertainty was high and surprise low. — [Cheung et al., "Uncertainty and Surprise Jointly Predict Musical Pleasure...", Current Biology 2019, summary page](https://cms.mus.cam.ac.uk/publications/cheung-uncertainty-surprise/)
- Margulis: inserting verbatim repeats of short passages into Berio and Carter excerpts raised expert listeners' ratings of enjoyment, interest and likelihood of human authorship (no numbers in the review). — [Albrecht review of "On Repeat"](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.albrecht.php)
- Chart data: each added chorus repetition raised the odds of number one by 14.5%, with a ceiling effect for too much word repetition. — [Pacific Standard on Nunes et al.](https://psmag.com/?p=30843)
- Top-10 songs have more repetitive lyrics than other charting songs in every year 1960 to 2015; for melody the Top-10 versus 11 to 20 difference was not significant (p = .070). — [Morris, The Pudding](https://pudding.cool/2017/05/song-repetition/); [Kent State poster](https://oaks.kent.edu/ugresearch/2020/art/melodies-pop-measuring-melodic-repetitiveness-throughout-billboard-era)
- Formal counterpart: predictive information rate is zero at both extremes (fully repetitive, fully random) and peaks at intermediate entropy rate. — [Abdallah and Plumbley](https://core.ac.uk/download/30696123.pdf)

### Inferences
- The Cheung and Gold interaction gives a placement rule rather than a rate: put exact repetition where the listener is uncertain (new section, new verse text, start of a phrase after a contrast) and put the departure where the listener is confident (after two statements, at D of SRDC, at the cadence of a restatement). This matches Dai et al.'s finding that novelty is concentrated at section and phrase starts and matches the short-short-long SRDC design.
- A target band for exact two-bar rhythm repetition within a section, built only from numbers in these notes:
  - centre: 23% (project corpus, 3/4);
  - lower edge about 15%: below the SRDC floor of 25% only because not every section is SRDC (43% to 60% are);
  - upper edge about 35% to 40%: PDSA's 35% of phrases with strict repeating layouts, and aa'ba' layouts reaching 50% of cells.
  - A working band of roughly 15% to 35% exact, with a further share of near repeats (skeleton identity, one split or tie), is defensible. This band is my inference; no source states it.
- Nothing in the preference literature suggests harm from moving 1% to about 20%: on every chart and rating measure found, more repetition than a generator typically produces is neutral or positive until a high ceiling.
- Liking drops with repeated hearings of the same excerpt (Gold Study 2) but the shape of the curve does not change, so the target need not be adjusted for expected replay count.

### Gaps
- No study maps "percent of bars repeated" to liking. The inverted-U work uses information content, not repetition counts; converting between them needs a model run on the engine's own output.
- I could not read Cheung et al.'s full text (PubMed blocked); participant numbers and effect sizes are missing. **[recalled, unverified]** 39 listeners rated 30 chord progressions drawn from 745 Billboard songs (McGill Billboard corpus).
- The Nunes ceiling for word repetition has no threshold in the accounts I could reach.
- Berlyne's and Wundt's original curves are qualitative; I did not fetch a primary source.

## 5. Differences between triple and duple metre, and between genres

### Takeaway
I found no published comparison of melodic or rhythmic repetition rates between triple-metre and duple-metre songs. Every pop corpus study located excludes non-4/4 songs. Genre and era differences are documented for lyrics and for rhythmic cell reuse, but only in 4/4.

### Cited Findings
- Dai et al. analyse only 4/4 songs in POP909 and PDSA. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- White, Pater and Breen keep only quadruple-metre songs (one of 25 recent hits was dropped for metre). — [White, Pater and Breen](https://par.nsf.gov/servlets/purl/10356498)
- Era: rhythmic 4-gram rank slope steepens from -4.22 (1955 to 1997) to -6.93 (2015 to 2019), and onset-profile entropy rises 0.81 to 0.89: newer songs have denser, more varied onset positions yet reuse their top cells more. Within the recent set, 4-gram slopes did not differ between pop and non-pop (rap, hip-hop, trap); non-pop had more notes per second (3.58 vs 2.48). — [White, Pater and Breen](https://par.nsf.gov/servlets/purl/10356498)
- Era and corpus: PDSA (pre-1925 American popular song) uses 54 of 128 possible half-note onset patterns; POP909 uses all 128. — [Dai et al.](https://arxiv.org/pdf/2209.00182)
- Lyrics by genre: country and hip-hop cluster apart from pop and rock in the 2000s; artist averages run from 38% to 60% compressibility. — [Morris, The Pudding](https://pudding.cool/2017/05/song-repetition/)
- Form by era: sentential (SRDC) strophes rise from under a third (1959) to about 60% (1964 onward); verse-chorus form approaches a monopoly by the late 1980s. — [Summach](https://www.mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.php)
- Folk versus instrumental themes: symmetric folk phrases are mostly mirror forms (59% to 69%), symmetric instrumental themes mostly repetition; dance forms reuse the narrowest range of transformed variants (deployment ratio 0.23 vs 0.28 to 0.34). Pitch only; metre not analysed. — [arXiv 2610.40303](https://arxiv.org/pdf/2610.40303)
- Toussaint's distance tests treat binary (4/4) and ternary (12/8) rhythm families separately; chronotonic distance gave the best trees for the ternary family. — [Toussaint 2004](https://archives.ismir.net/ismir2004/paper/000134.pdf)
- Hayes and Kaun's speakers were steered to binary settings; ternary settings were corrected away, so their counts say nothing about triple metre. — [Hayes and Kaun](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)

### Inferences
- A bar of 3/4 has fewer tatum positions (6 eighths, 12 sixteenths) than a bar of 4/4 (8, 16), so the space of possible two-bar onset patterns is far smaller (2^12 against 2^16 at eighth-note resolution). By chance alone, and more so under a small working vocabulary like PDSA's, exact repetition should be more frequent in 3/4 than in 4/4. The project's 23% for 3/4 may therefore be somewhat higher than the matching 4/4 figure; the engine should hold separate targets per metre, measured from its own corpus.
- Since the literature offers no triple-metre benchmark, the project's own 3/4 corpus count is the best available number, and is worth reporting with its exact definition (tatum resolution, treatment of ties and pickups, within-section versus whole-song comparison).

### Gaps
- No published triple versus duple comparison of repetition found, in pop or in folk corpora.
- No genre table of bar-level melodic or rhythmic repetition found (only lyrics compression and 4-gram slopes).
- The MPB Corpus (Brazilian popular music; melody, rhythm and harmony; arXiv 2608.13842) appeared in search results and may contain rhythm-repetition statistics; not read.
