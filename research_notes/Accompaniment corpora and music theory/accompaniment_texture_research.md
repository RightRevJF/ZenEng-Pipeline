# Accompaniment and Musical Texture: Computational Representation, Generation and Evaluation (for idiomatic keyboard accompaniment in a songwriting engine)

Scope note: these notes cover (1) texture taxonomies and annotated corpora, (2) accompaniment-generation systems and their representations, corpora and evaluation, (3) measurable properties of good accompaniment, (4) metre-specific (3/4, 6/8) statistics, and (5) voice-leading rules relevant to accompaniment voicings. Sample sizes are given wherever the source reports them. Where a source was only partly readable (abstract only), that is said explicitly.

---

## Q1. What texture categories have been defined and annotated, and with what inter-annotator agreement?

### Takeaway
The only rigorous, openly released symbolic texture-annotation scheme for keyboard music is the Algomus (Lille) group's syntax (Couturier, Bigo, Levé, ISMIR 2022). It labels each bar as stacked layers with functions M (melodic), H (harmonic, i.e. accompaniment) and S (static: pedals and ostinati), plus voice counts and figure flags (homorhythm, parallel, octave, sustained, repeated notes, oscillation, scale). It was applied to 1,164 bars of three early Mozart sonatas. Neither this dataset nor its string-quartet predecessor (Giraud et al. 2014) reports a kappa-style inter-annotator agreement figure. The only reliability numbers are review and revision rates: 31% of labels were flagged and 22% changed. Pop piano corpora (POP909) separate melody, secondary melody and accompaniment tracks but carry no texture-type labels.

### Cited Findings

**Couturier, Bigo & Levé (2022), "A Dataset of Symbolic Texture Annotations in Mozart Piano Sonatas", ISMIR 2022**
- The syntax is one text label per bar. Independent layers are separated by "/" and ordered by descending register (e.g. `M1/H2`). — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Layer functions are M (melodic), H (harmonic, which covers accompaniment) and S (static, such as pedals and ostinati). They can combine, e.g. `HS1` for a persistent arpeggio. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Density is the number of voices in a layer, written as an integer after the function. Global density (total voices) is optional and goes in brackets before the label. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Internal-organization flags: h = homorhythmy, p = parallel motion, o = octave, t = sustained notes, r = repeated notes, b = oscillations (e.g. Alberti-like or rocking figures), s = scale motives. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Further notation: sublayers in parentheses, e.g. `M1/HS1(S1/M1)` for alternating repeated-pitch and melodic lines. "_" marks sparse layers and empty bars, and "," splits a bar where the texture changes. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Corpus: 9 movements from 3 early Mozart sonatas (K. 279, K. 280, K. 283), all in sonata form. This gives 1,164 bar-level annotations, 1,357 textural configurations once bars with two labels are split (16.6% of bars), and 2,317 non-empty layers. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Annotation procedure: one expert annotated every bar on the Dezrann platform, and a Python script checked the syntax. Two reviewers flagged doubts, which were resolved by the expert or by consensus. Of the 1,164 initial labels, 31% received reviewer feedback and 22% (256) were changed. The paper reports no kappa or similar agreement statistic, and notes that normalization was "not strictly formalized". — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Frequencies (share of 2,317 layers): M1 (single-voice melody) 24.9%, M1s (melody with scale motives) 7.0%, M2p (melody in parallel, usually 3rds or 6ths) 3.7%. The most common full label is `M1/HS1` (melody plus single-voice accompaniment) at 7.3% of labels. Oscillations (b) appear in about 5.1% of labels. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Function combinations: melody only (no H or S) 20.2%; all three functions (M, H, S) 23.5%; melodic and/or harmonic without static 34.1%. M is present in 94.6% of bars. H is present in 84.4% of bars in the slow movements but only 58.2% in the other six movements. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- 29.2% of non-empty configurations have diversity|density 2|2 (two layers, two voices), and diversity rarely exceeds 2. The authors conclude that a simple two-layer split matching the two hands is not representative. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Automatic prediction: logistic regression on 62 descriptors, leave-one-piece-out cross-validation. F1 scores: M 0.912, H 0.744, h/p/o 0.810, t 0.669, S 0.616, o 0.538, s 0.363, b (oscillation) 0.098. Scale motives and oscillations did worst, partly because those patterns extend beyond one bar. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf)
- Data: annotations at http://algomus.fr/data, descriptor code at http://algomus.fr/code, note files (MuseScore/TSV) at https://github.com/DCMLab/mozart_piano_sonatas/tree/main/notes, annotation platform http://dezrann.net. — [ISMIR 2022 paper](https://archives.ismir.net/ismir2022/paper/000061.pdf); dataset record also at [HAL](https://hal.archives-ouvertes.fr/hal-03860195) and [B2FIND "Mozart Piano Sonatas with Form, Harmony, and Texture Annotations"](https://b2find.eudat.eu/dataset/be297494-842f-5208-93cd-470521912e17)

**Couturier, Bigo & Levé (2023), "Comparing Texture in Piano Scores", ISMIR 2023**
- The paper compares three textural spaces. (1) Huron's space of polyphony, monophony, homophony and heterophony, defined by onset synchrony and semblant motion. (2) Couturier et al.'s density (number of threads) × diversity (number of layers). (3) 12 binary textural elements: layer roles (melodic, harmonic, static), voice relationships (homorhythmy, parallel, octave) and figures (sustained, repeated, scale, oscillation). — [ISMIR 2023 paper](https://archives.ismir.net/ismir2023/paper/000060.pdf)
- Data used: TAVERN (27 theme-and-variation sets, 10 Mozart and 17 Beethoven, 1,060 phrases), the 1,164 Mozart texture labels, Mozart's Ten Variations in G, K. 455 (338 bars), and about 1,160 bar pairs from K. 279/280/283. The 1,164 labels use only 17 distinct density-diversity combinations. — [ISMIR 2023 paper](https://archives.ismir.net/ismir2023/paper/000060.pdf)
- No inter-annotator agreement is reported. The paper notes that label production can be subjective, and that only the "texel" distance it proposes captures the roles of layers. Code is in Python (music21; **kern/MusicXML) at http://algomus.fr/code. — [ISMIR 2023 paper](https://archives.ismir.net/ismir2023/paper/000060.pdf)

**Giraud, Levé, Mercier, Rigaudière & Thorez (2014), "Towards Modeling Texture in Symbolic Data", ISMIR 2014**
- Model: notes are grouped into perceived layers, each tagged melodic (mel) or accompaniment (acc). Both kinds are described by homorhythmy (h), parallel motion (p), octave (o) and unison (u). Accompaniment layers are described mainly by rhythmic traits: sustained, sparse or repeated chords, Alberti bass, pedal notes, syncopation. Categories include mel/acc, mel/mel, mel, acc, acc/mel/acc and mel/acc/acc. — [ISMIR 2014 paper](https://archives.ismir.net/ismir2014/paper/000143.pdf)
- Corpus: ten string-quartet first movements, 1,488 measures in total: Haydn op. 33 nos. 1–6, Mozart K. 80, K. 155 and K. 157, and Schubert op. 125 no. 1. Annotation was manual, with segments at least one bar long and boundaries rounded to bar lines. The authors say agreeing on short segments and boundaries is difficult and that h/p/o/u judgements were subjective. No agreement statistics are given. — [ISMIR 2014 paper](https://archives.ismir.net/ismir2014/paper/000143.pdf)
- Frequencies (691 segments): mel/acc 512 (about 74%), other 68, mel 50, acc/mel/acc 24, acc/mel 18, acc 15, mel/mel 4. Relation labels: h 295, p 272, o 63, u 5. Within mel/acc, 254 segments put the melody in the first violin over the three lower voices (S/ATB), and 81 have a parallel melody in the two violins (SAp/TB). — [ISMIR 2014 paper](https://archives.ismir.net/ismir2014/paper/000143.pdf)
- Detection of synchronized (p/o/u) layers: 434 layers found, covering 797 measures (53.6%). 356/434 (82.0%) overlap a true layer. Sensitivity is 194/340, which is 57.1% by the table; the text states 58.0%, an internal inconsistency in the paper. Ground truth: www.algomus.fr/truth. — [ISMIR 2014 paper](https://archives.ismir.net/ismir2014/paper/000143.pdf)

**Pedagogical (non-corpus) taxonomies of keyboard accompaniment**
- Open textbook *Music Theory for the 21st-Century Classroom* (Hutchinson, Univ. of Puget Sound), ch. 14 "Accompanimental Textures". Subsections: chorale texture, arpeggiated accompaniments, block-chord accompaniments, afterbeats and offbeats, 3–2 son clave, distinctive bass lines. — [Arpeggiated Accompaniments page](https://musictheory.pugetsound.edu/mt21c/ArpeggiatedAccompaniments.html); parent: [Accompanimental Textures](https://musictheory.pugetsound.edu/mt21c/AccompanimentalTexture.html)
- Arpeggios: the chord is spread rhythmically in one part over a bass in octaves in a lower part. Variants are descending (Alicia Keys, "If I Ain't Got You"), ascending and descending ("Colour My World"), and sixteenth-note arpeggios in 4/4 ("No Scrubs"). Alberti bass is a "low–high–middle–high" arpeggio (Mozart K. 545, I). Organ block chords can be layered under arpeggios to give a sense of legato. — [Arpeggiated Accompaniments](https://musictheory.pugetsound.edu/mt21c/ArpeggiatedAccompaniments.html)
- Block-chord rhythms catalogued:
  - "1 (2) &", two chords per bar: Ed Sheeran "Thinking Out Loud", Bruno Mars "That's What I Like", James Arthur "Say You Won't Let Go"
  - "Barbara Ann": 1 2 3 (4) & (1) & (2) & 3
  - repeated eighth-note chords: Mozart K. 310, I; Schubert "Gute Nacht"; Schumann "Ich grolle nicht"; "We Are Young"
  - repeated quarter-note chords: Handel "Ombra mai fu", Billy Joel "She's Got a Way", Sara Bareilles "Love Song"

  — [Block Chord Accompaniments](https://musictheory.pugetsound.edu/mt21c/BlockChordAccompaniments.html)
- In the Beethoven ("Moonlight") and Keys arpeggio examples, bass and soprano sit a tenth apart, which the text calls harmonious. — [Arpeggiated Accompaniments](https://musictheory.pugetsound.edu/mt21c/ArpeggiatedAccompaniments.html)

**Pop piano corpora (no texture-type labels)**
- POP909 (Wang et al., ISMIR 2020) has three MIDI tracks per song. MELODY is the vocal melody. BRIDGE holds secondary melodies or lead-instrument parts. PIANO is the main accompaniment, "including broken chords, arpeggios, and other textures". BRIDGE and PIANO together form the piano accompaniment. There are no per-bar texture-category labels and no phrase or structure annotations. — [POP909 paper (arXiv)](https://arxiv.org/pdf/2008.07142); [GitHub](https://github.com/music-x-lab/POP909-Dataset)

### Inferences
- For an engine, the Couturier syntax is a ready-made target vocabulary. A bar-level texture plan such as `M1/HS1b` (melody over one-voice oscillating accompaniment, i.e. Alberti or rocking) or `M1/H3h` (melody over three-voice homorhythmic block chords) can be generated first and then realized with notes.
- In Classical piano writing, melody-over-accompaniment (mel/acc) dominates: about 74% of segments in the string quartets, and the M + single-voice accompaniment label is the most common single label in Mozart. Accompaniment is far more present in slow movements (84% vs 58% of bars), which suggests that ballad and slow-song sections should almost always carry an explicit H layer.
- Oscillation figures (Alberti, rocking) are a minority (about 5% of labels) even in early Mozart, and they are the hardest to detect automatically (F1 0.098). An engine that uses Alberti bass everywhere would over-represent it relative to the Classical style itself.
- With no published agreement statistic, annotation reliability is unknown. The 22% revision rate suggests substantial ambiguity, especially at texture boundaries.

### Gaps
- No inter-annotator agreement statistic (kappa, alpha) has been published for any symbolic texture-annotation dataset found. Only the 31% flagged / 22% revised figures exist.
- No annotated corpus found that labels pop, gospel or worship piano textures (e.g. stride, gospel "shout" piano, worship pad + octave left hand, 9th/sus "worship" voicings), and no published frequency statistics for stride, gospel or worship idioms. Pedagogical sources were not reached in this session.
- No corpus-measured frequencies found for oom-pah/waltz bass, rocking figures, countermelody or ostinato as separate categories in song accompaniment. Couturier's S (static) function and b (oscillation) flag lump some of these together.
- The Puget Sound "Afterbeats and Offbeats" page (oom-pah, waltz) could not be fetched (not on the allowlist), so its content is not reported.

---

## Q2. What representations make accompaniment generation work, and what corpora were they trained on? How are systems evaluated?

### Takeaway
The dominant successful line is NYU Shanghai's Music X Lab (Gus Xia, Ziyu Wang, Jingwei Zhao). It represents accompaniment as a piano-roll whose texture (rhythmic and voicing "shape") is disentangled from chords (beat-wise 36-D root/bass/chroma). Systems then retrieve or generate texture independently and re-voice it to new chords. Almost all of this work is trained on POP909 (909 Chinese pop songs with professional piano arrangements), filtered to 2/4 and 4/4, so triple and compound metres are essentially untested. Evaluation is mostly 5-point listener ratings (23–72 participants) plus distributional metrics: overlapped pitch/duration area, chord accuracy, degree-of-arrangement, and an "inter-phrase latent similarity" (ILS) for structure.

### Cited Findings

**Wang, Wang, Zhang & Xia (2020), "Learning Interpretable Representation for Controllable Polyphonic Music Generation" (ISMIR 2020): chord-texture disentanglement**
- A VAE learns two latent factors, chord and texture, on 8-beat piano segments. Applications are compositional style transfer, texture variation and accompaniment arrangement. — [arXiv abstract](https://arxiv.org/abs/2008.07122)
- Chord input: rule-extracted chords at 1-beat resolution form a 36×8 matrix per 8-beat segment. Each beat is a 12-D one-hot root, 12-D one-hot bass and 12-D multi-hot chroma, encoded by a bi-GRU into z_chd. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Texture input: a 128×32 piano-roll (MIDI pitch × 1/4-beat frames). Each entry holds the note's duration at its onset and is zero elsewhere. The texture encoder is a CNN (1→10 channels, 12×4 kernel, stride 1×4, ReLU, 4×1 max-pool) followed by a bi-GRU giving z_txt. The aim is a blurry "concept sketch" of the texture that carries minimal chord information. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- z_chd and z_txt are each 256-D. Data: POP909 restricted to 2/4 and 4/4, cut into 8-beat segments, giving 66K samples. The train/test split is 90/10 by song, with training data transposed to all 12 keys. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Objective tests: under small transpositions z_chd changes much more than z_txt (most sensitive to a tritone, least to an octave). Pitch perturbation moves z_chd, and rhythm perturbation (halving durations) moves z_txt. Results are shown as plots only. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Listening test: 36 listeners rated texture-swapped 2-bar pieces on a 5-point scale (creativity, naturalness, musicality). The best of five random transfers rated significantly higher than the original (p < 0.005), but on average the transferred versions rated below the originals. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Qualitative findings:
  - Posterior sampling varies mainly the right-hand melody while the left-hand accompaniment changes little. The authors read this as the model treating the left-hand pattern as the dominant texture feature.
  - Swapping z_txt every 2 bars transfers texture while keeping the chords.
  - A Transformer arranger conditioned on melody adds a secondary melody when the lead rests.

  — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1); code: https://github.com/ZZWaang/polyphonic-chord-texture-disentanglement

**POP909 (Wang, Chen, Jiang et al., ISMIR 2020)**
- 909 songs (about 60 hours) by 462 artists, arranged for piano by professional musicians split into arranger and reviewer teams. The project started with 1,000 candidate songs. Annotations: hand-labelled tempo curves aligned to the audio, plus beat/downbeat, chord and key from MIR algorithms. — [POP909 paper](https://arxiv.org/pdf/2008.07142)
- Annotation quality: MIDI and audio beats agree more than 90% within 100 ms, and downbeats 80%. Chord root agreement is above 75% for more than 800 songs, with a few below 40%. Metre distribution is not reported. — [POP909 paper](https://arxiv.org/pdf/2008.07142)
- Suggested tasks: piano accompaniment generation conditioned on melody, and re-orchestration from audio. — [POP909 paper](https://arxiv.org/pdf/2008.07142); [GitHub](https://github.com/music-x-lab/POP909-Dataset)

**AccoMontage (Zhao & Xia, ISMIR 2021): retrieval + style transfer**
- Representation: melody as 130-D one-hot (128 pitches + hold + rest), chords as 12-D chroma, accompaniment as a 128-D piano-roll. For matching, rhythm is condensed to 3-D (onset/hold/rest) and chords are mapped to a 12-D Tonal Interval Vector. — [AccoMontage (ar5iv)](https://ar5iv.labs.arxiv.org/html/2108.11213)
- Corpus: 857 POP909 songs in 2/4 and 4/4, giving 11,032 phrases per the text; Table 1 sums to 10,982, a small discrepancy in the source. Four-bar (3,591) and eight-bar (3,796) phrases are the most common. Test queries are about 1,000 Nottingham folk tunes with hand-labelled phrases. — [AccoMontage (ar5iv)](https://ar5iv.labs.arxiv.org/html/2108.11213)
- Method: phrase selection is a path through a layered graph. Node scores measure rhythm and chord fit to the query. Edge scores combine a contrastively learned texture-similarity term with a "form" term favouring matching phrase labels. The path is solved by Viterbi DP (O(nN²)), with δ = 0.3 and γ = 0.7 at inference. The selected reference's texture is then re-harmonized to the query's chords with the Wang et al. 2020 chord-texture VAE. Users can pre-filter by rhythm density and voice number (low/medium/high). — [AccoMontage (ar5iv)](https://ar5iv.labs.arxiv.org/html/2108.11213)
- Evaluation: 72 participants (67 effective ratings per metric) rated 14 Nottingham songs on coherence, structure and musicality (5-point scale). AccoMontage beat a template-only baseline and a seq2seq baseline significantly on coherence and structure (p < 0.05) and marginally on musicality (p = 0.053). — [AccoMontage (ar5iv)](https://ar5iv.labs.arxiv.org/html/2108.11213); code: https://github.com/zhaojw1998/AccoMontage

**AccoMontage2 (Yi, Zhao, Xia et al., ISMIR 2022): harmonization + arrangement**
- Harmonization is dynamic programming over 5,762 curated 4- or 8-bar chord-progression templates, drawn from a 64,524-file MIDI collection. Templates are labelled major/minor and assigned one of four styles: Pop-standard (triads only), Pop-complex (7ths, 9ths, chromatic), Dark, R&B. — [AccoMontage2 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2209.00353)
- Three loss levels: micro (note-wise melody-vs-chord-root dissonance matrix, different for major and minor), meso (phrase-template matching, with transition penalty T = 1 + log_N(1/c)) and macro (whole-piece coherence). Example weights α = 0.1, β = 0.5. — [AccoMontage2 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2209.00353)
- A GUI exposes "several levels" of piano-texture voicing density and rhythmic complexity, which are not defined in the text. Evaluation: 15 participants, 44 effective ratings per criterion (harmonicity, creativity, musicality). The system significantly beat a BLSTM baseline (p < 0.05). — [AccoMontage2 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2209.00353); [arXiv abstract](https://arxiv.org/abs/2209.00353v1); code: https://github.com/billyblu2000/accomontage2

**AccoMontage-3 / "Structured Multi-Track Accompaniment Arrangement via Style Prior Modelling" (Zhao et al., arXiv 2310.16334 v4)**
- Content is a piano reduction (all tracks downmixed) encoded to a 256-D VAE latent. Style is a per-track "orchestral function": a rhythm and groove skeleton from normalized onset counts, VQ-VAE coded at 1-beat resolution (8 codes per 2 bars, codebook 128). — [arXiv v4](https://arxiv.org/html/2310.16334v4)
- Two stages: Stage 1 is a piano texture prior that sets the whole-song phrase structure and chords; Stage 2 is an orchestral-function prior that orchestrates the piano score. Windowed sampling advances 4 bars at a time, conditioned on the previous 28 bars, with a timing condition giving each position as a fraction of the song. — [arXiv v4](https://arxiv.org/html/2310.16334v4)
- Data: Slakh2100 (about 2K pieces) for the autoencoder; Lakh MIDI (about 110K pieces kept, 2/4 and 4/4) for the prior; 50 Nottingham + 50 WikiMT pieces for testing; POP909 (88-piece test set; 857 4/4 pieces for structure). — [arXiv v4](https://arxiv.org/html/2310.16334v4)
- Lead sheet to multi-track results:

  | System | Chord accuracy | DOA | Structure | Latency (s/bar) |
  |---|---|---|---|---|
  | This system | 0.567 | 0.300 | 1.520 | 0.461 |
  | AMT | 0.446 | 0.294 | 1.094 | 6.32 |
  | PopMAG | 0.470 | 0.270 | 1.086 | not recorded here |
  | GETMusic | 0.423 | 0.225 | 1.243 | not recorded here |
  | Ground truth | n/a | 0.333 | 1.980 | n/a |

  Stage 1 (lead sheet to piano): chord accuracy 0.540 vs 0.430 for Whole-Song-Gen; structure 1.983 vs 1.153. Subjective study: 23 participants, 5 criteria, significant on all (p < 0.05). — [arXiv v4](https://arxiv.org/html/2310.16334v4); demo: https://zhaojw1998.github.io/structured-arrangement/ (earlier version: [AccoMontage-3 page](https://zhaojw1998.github.io/AccoMontage-3))

**Polyffusion (Min, Jiang, Xia & Zhao, ISMIR 2023): diffusion on piano-roll**
- Representation: a 2-channel binary piano-roll (onset, sustain), 128 steps of 1/4 beat (8 bars) × 128 pitches. Data: POP909 (2/4 and 4/4 only), 8-bar windows with a 1-bar hop, about 64K samples, 90/10 song-level split, 12-key transposition. — [Polyffusion arXiv](https://arxiv.org/pdf/2307.10304)
- Controls:
  - internal: inpainting, including accompaniment given melody by masking the accompaniment
  - external chord: beat-wise 36-D vectors compressed to a 512-D latent per 8 bars
  - external texture: 256-D per 2 bars, concatenated to 1,024-D per 8 bars

  Controls are injected by cross-attention, with classifier-free guidance. — [Polyffusion arXiv](https://arxiv.org/pdf/2307.10304)
- Accompaniment-given-melody evaluation: overlapped area of pitch/duration distributions 0.89/0.96 vs 0.88/0.89 for a Transformer baseline, averaged over 160 samples. In a 36-participant listening test it was significantly better on "fitness" (p < 0.05). — [Polyffusion arXiv](https://arxiv.org/pdf/2307.10304); code: https://github.com/aik2mlj/polyffusion

**Whole-song generation (Wang, Min & Xia, ICLR 2024): cascaded diffusion**
- Four-level hierarchy: Form (keys + phrase labels, bar resolution); Reduced lead sheet (beat resolution); Lead sheet (step resolution); Accompaniment (step resolution). Phrase labels: A verse, B chorus, X other phrase with lead melody, i intro, o outro, b bridge. — [Whole-song paper](https://arxiv.org/pdf/2405.09901)
- Accompaniment is a 2-channel (onset, sustain) piano-roll over 128 pitches at 4 steps per beat, with γ ∈ {3, 4} beats per bar. 3/4 is supported but "underrepresented" in the data. Accompaniment is extracted from POP909 BRIDGE + PIANO. — [Whole-song paper](https://arxiv.org/pdf/2405.09901)
- Structure metric ILS (same-phrase-type similarity divided by all-phrase similarity, using pretrained VAE latents): ground truth ILS_txt (accompaniment) 1.68 ± 0.09 vs cascaded diffusion 1.19; Polyffusion + phrase labels 0.61; Transformer-XL (REMI) + phrase labels 0.74. Subjective study: 57 participants, double-blind. — [Whole-song paper](https://arxiv.org/pdf/2405.09901); code: https://github.com/ZZWaang/whole-song-gen; demo: https://wholesonggen.github.io; [ICLR listing](https://iclr.cc/virtual/2024/poster/17633)

### Inferences
- The engineering lesson is consistent: treat texture as a chord-independent onset/duration pattern (piano-roll "shape") and voice it onto chords separately. The VAE rests on that separation, AccoMontage works by retrieving whole real phrases and re-voicing them, and the success of this design over end-to-end seq2seq suggests that a rule-based engine could do the same thing. It could store a library of idiomatic 1–2-bar texture templates (onset grid + relative chord-tone indices + register), choose one per section, and map it onto each chord.
- Phrase-level retrieval with a transition cost for texture similarity (AccoMontage) is a cheap way to get coherent-but-varying accompaniment across a song without learning.
- Every major system filters to 2/4 and 4/4, so none of them supplies learned 3/4 or 6/8 accompaniment idioms. A 3/4 or 6/8 accompaniment library has to come from theory or hand-built templates.
- POP909 is Chinese Mandopop with arranger-made piano covers, so its idioms (eighth-note verses, sixteenth-note choruses) may not transfer directly to Western hymnody, gospel or worship styles.

### Gaps
- No accompaniment-generation system found that is trained on, or evaluated for, hymn, gospel, worship, stride or organ textures.
- The AccoMontage2 texture "levels" (voicing density, rhythmic complexity) are not defined in the text reached.
- Mean listener scores for most systems appear only in figures and were not extractable.

---

## Q3. What measurable properties distinguish a good accompaniment (rhythmic complementarity, density curves across sections, register spacing)?

### Takeaway
Published systems measure "good accompaniment" only indirectly:
- distributional similarity to human data (pitch and duration overlap, pitch-class histograms)
- chord accuracy
- degree-of-arrangement (DOA)
- structural self-similarity between same-label phrases (ILS)
- listener ratings of coherence, fitness, naturalness and musicality

Direct corpus statistics on melody–accompaniment density ratios, register gaps or rhythmic complementarity in song accompaniment were not found. The best empirical anchors are qualitative POP909 observations (eighth-note verses, sixteenth-note choruses, fills at phrase boundaries, rising activity toward the climax), the ground-truth ILS value showing that accompaniment repeats across same-label phrases, and Huron's corpus evidence that independent polyphonic parts avoid synchronous onsets.

### Cited Findings
- Build across sections: the whole-song paper's POP909 example uses mostly eighth-note accompaniment in verses and sixteenth notes in choruses, adds "fill" figures at phrase boundaries, and raises activity and pitch height in the second half toward a climax. This is qualitative; the paper gives no density statistics. — [Whole-song paper](https://arxiv.org/pdf/2405.09901)
- Accompaniment repeats by phrase type: ground-truth ILS_txt = 1.68 ± 0.09. Accompaniment in same-label phrases (e.g. every chorus) is markedly more similar than across phrase types, and generators fall short (1.19 at best). — [Whole-song paper](https://arxiv.org/pdf/2405.09901)
- Ground truth for multi-track arrangement: DOA 0.333 and structure 1.980, against 0.300/1.520 for the best system. These are targets a generator can be benchmarked against. — [AccoMontage-3 / Structured arrangement v4](https://arxiv.org/html/2310.16334v4)
- Polyffusion measures accompaniment quality as the overlap of pitch and duration distributions with real data (0.89/0.96), plus a listener "fitness" rating to the melody. — [Polyffusion](https://arxiv.org/pdf/2307.10304)
- Complementarity with the melody, observed in learned models: Wang et al.'s arranger adds a secondary melody when the lead melody rests, mirroring the POP909 BRIDGE track. — [Wang et al. 2020](https://arxiv.org/pdf/2008.07122v1); [POP909](https://arxiv.org/pdf/2008.07142)
- AccoMontage's controllable dimensions are rhythm density and voice number, each low/medium/high. Its phrase-transition score uses a learned texture-similarity term, so adjacent phrases have smaller texture distance than random pairs: contrastive loss decreases from random pairs, to same-song pairs, to adjacent pairs. — [AccoMontage](https://ar5iv.labs.arxiv.org/html/2108.11213)
- Onset asynchrony (independence) evidence from Huron (2008), *Empirical Musicology Review*:
  - Bach 15 two-part Inventions: 5,608 harmonic intervals; 26 three-part WTC fugues: 31,913 intervals.
  - Inventions, perfect consonances: 599 synchronous vs 1,059 asynchronous.
  - Inventions, imperfect consonances: 1,901 synchronous vs 832 asynchronous.
  - Perfect (fusing) intervals are more often approached asynchronously, supporting the claim that avoiding tonal fusion and onset synchrony keeps parts perceptually independent.
  - Huron (1993) found Bach's Inventions avoid synchronous onsets relative to a metre-controlled baseline.
  - Rasch (1981) found onset asynchrony grows with the number of voices.

  — [Huron 2008, EMR (CORE PDF)](https://core.ac.uk/download/159579115.pdf)
- Huron's textural space (onset synchrony × semblant motion) defines homophony as high onset synchrony and polyphony as low synchrony with independent motion. This gives a measurable axis for "block chord vs independent countermelody". — [Couturier et al. 2023](https://archives.ismir.net/ismir2023/paper/000060.pdf)
- Register: the Puget Sound text notes bass–soprano tenths as harmonious spacing in arpeggiated accompaniments. — [Arpeggiated Accompaniments](https://musictheory.pugetsound.edu/mt21c/ArpeggiatedAccompaniments.html)

### Inferences
These are actionable heuristics for a rule-based engine, drawn from the findings above rather than validated metrics.
- Treat accompaniment density as a section-level control. The plan should be:
  1. lower subdivision in verses (e.g. eighths), higher in choruses (e.g. sixteenths)
  2. fills where the melody rests at phrase ends
  3. a rising register and activity curve into the final chorus
- Keep accompaniment templates identical, or nearly so, across same-label sections (high ILS), and vary them between section types.
- Measure rhythmic complementarity as the fraction of accompaniment onsets that fall where the melody does not attack, and reward activity in melody rests. This is supported directionally by the secondary-melody-in-rests behaviour and Huron's asynchrony findings, but no published target value exists for song accompaniment.
- Use distributional checks against a reference corpus (pitch-range and duration histograms, DOA-like measures) as automatic sanity tests, with listener ratings as the gold standard.

### Gaps
- No published corpus statistics found for:
  - melody-to-accompaniment onset-density ratios in songs
  - typical register gap between the lowest melody note and the highest accompaniment note
  - quantitative density curves by section (verse/chorus/bridge) in POP909 or other pop corpora

  POP909 itself reports no register or density statistics per track.
- No validated "rhythmic complementarity" metric for accompaniment evaluation was found. A search returned only general rhythm-embedding papers.

---

## Q4. Are there published statistics of accompaniment figures in 3/4 and 6/8 (waltz, barcarolle, lullaby figures)?

### Takeaway
None found. The main generative corpora and systems explicitly exclude triple and compound metres (2/4 and 4/4 only), and the texture-annotation papers do not break results down by metre. Waltz, barcarolle and lullaby (rocking 6/8) figures are documented only in pedagogy, not in measured corpora.

### Cited Findings
- AccoMontage keeps only POP909 songs in 2/4 and 4/4 (857 songs). — [AccoMontage](https://ar5iv.labs.arxiv.org/html/2108.11213)
- The Wang et al. 2020 chord-texture VAE keeps only 2/4 and 4/4 pieces. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Polyffusion keeps only 2/4 and 4/4 pieces. — [Polyffusion](https://arxiv.org/pdf/2307.10304)
- The AccoMontage-3 prior keeps about 110K of about 170K LMD pieces in 2/4 and 4/4. — [arXiv v4](https://arxiv.org/html/2310.16334v4)
- Whole-song generation supports 3 or 4 beats per bar, but 3/4 is "underrepresented" in POP909. — [Whole-song paper](https://arxiv.org/pdf/2405.09901)
- The POP909 paper uses beat trackers assuming simple and compound metre, but reports no metre distribution. — [POP909](https://arxiv.org/pdf/2008.07142)
- The Couturier et al. 2022 Mozart texture dataset reports no findings by metre. — [ISMIR 2022](https://archives.ismir.net/ismir2022/paper/000061.pdf)

### Inferences
- A songwriting engine targeting hymns, lullabies and waltz-time songs cannot borrow learned 3/4 or 6/8 accompaniment idioms from these systems. It needs hand-authored templates:
  - 3/4: bass on 1 with chords on 2–3, or a broken-chord eighth pattern
  - 6/8: a rocking low–high–mid figure per dotted-quarter beat, or a barcarolle bass on 1 and 4 with chords on the off-eighths
- The Couturier syntax could annotate a small in-house 3/4 and 6/8 reference set (e.g. `M1/HS1b` for rocking figures, or `M1/S1,H2` for waltz bass plus chords) if empirical frequencies are wanted.

### Gaps
- No peer-reviewed corpus statistics found on frequencies of waltz/oom-pah-pah, barcarolle or 6/8 rocking figures, by style or otherwise.
- The Puget Sound "Afterbeats and Offbeats" chapter (which likely covers oom-pah and waltz patterns) could not be fetched.
- Caplin-style formal-function theory of accompaniment (e.g. accompaniment intensification in continuations) was not reached in this session.

---

## Q5. What rules govern voice leading in accompaniment voicings?

### Takeaway
The most rigorous source is Huron's "Tone and Voice" (Music Perception 19/1, 2001). It derives most traditional voice-leading rules from six core perceptual principles and treats auxiliary principles as compositional "options" that distinguish polyphony, homophony and close harmony, which is directly relevant to choosing accompaniment textures. Only the abstract was readable here. Within generation systems, voice-leading is handled implicitly by learned decoders. AccoMontage2 explicitly claims support for ninth chords "with voice leading" in its harmonizer.

### Cited Findings
- Huron (2001) explains the traditional rules of Western voice-leading with experimentally established perceptual principles. Six core principles account for most rules in historical and contemporary theory texts and are treated like axioms from which the rules are derived. The derivation also yields non-traditional rules that predict previously unnoticed features of practice. Auxiliary principles act as compositional options that may distinguish polyphony, homophony and close harmony. Source: abstract only. — [ScienceGate record, Music Perception 2001, doi 10.1525/mp.2001.19.1.1](https://www.sciencegate.app/document/10.1525/mp.2001.19.1.1); [Scilit record](https://www.scilit.net/publications/94cabd5623d929e69eb16f5bd5ad72a0)
- Huron later expanded this into a book, *Voice Leading: The Science behind a Musical Art* (MIT Press). — [Penguin Random House listing](https://www.penguinrandomhouse.com/books/657442/voice-leading-by-david-huron/9780262537384/)
- Corpus evidence (Huron 2008): in Bach, perfect consonances such as octaves and fifths are more often prepared asynchronously (one voice moves first) than imperfect consonances. This supports avoiding simultaneous arrival on fused intervals between independent parts. — [Huron 2008, EMR](https://core.ac.uk/download/159579115.pdf)
- AccoMontage2's harmonizer "supports ninth chords with voice leading". The baselines support up to seventh chords in root position only. — [AccoMontage2 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2209.00353)
- In the Wang et al. 2020 texture swap, the left-hand accompaniment shape and melody contour are preserved when chords change. The texture's intervallic shape is re-mapped onto the new chord rather than being re-voiced from scratch. — [arXiv PDF](https://arxiv.org/pdf/2008.07122v1)
- Schema-level voice leading: Finkensiep, Déguernel, Neuwirth & Rohrmeier (ISMIR 2020) annotated two-voice voice-leading schemata in all 54 Mozart piano-sonata movements (about 7,500 bars, 103,829 notes, 244 true instances). The most frequent were Fonte.2 (49), Quiescenza.2 (46), Fenaroli.2 flipped (43) and Prinner.2 (32). Classifier F-score was 0.894 on balanced data but only 0.020 on the real imbalanced data. — [ISMIR 2020 paper](https://archives.ismir.net/ismir2020/paper/000124.pdf); data: https://github.com/DCMLab/schema_annotation_data

### Inferences
- For keyboard accompaniment voicings, a practical rule set consistent with Huron's framing (perceptual independence vs fusion) and common practice is:
  - keep common tones
  - move inner voices by the smallest interval to the next chord
  - space wider in the low register and closer above
  - avoid parallel octaves and fifths between the bass and the melody-bearing top voice when the accompaniment is meant to be independent
  - let the accompaniment's top voice stay below the melody

  The specific rules beyond what is cited above come from standard theory and were not verified against Huron's full text here.
- Because homophonic (block-chord) and polyphonic (countermelody) textures sit at opposite ends of Huron's onset-synchrony axis, an engine should switch voice-leading constraints with the texture. Block-chord pads tolerate synchronized, fused motion. A countermelody layer should avoid onset synchrony and parallel perfect intervals with the lead.
- Galant schemata (Prinner, Fonte, Quiescenza) are measured, frequent bass/treble frameworks in Mozart and could serve as phrase-level voice-leading skeletons for classical-style accompaniment.

### Gaps
- The full text of Huron (2001) was not accessible, so the six principles (commonly cited as toneness, temporal continuity, minimum masking, tonal fusion, pitch proximity and pitch co-modulation) and the derived rules, such as chord spacing and the avoidance of parallel perfect intervals, could not be verified against the source in this session. They should be checked before being cited as Huron's.
- No peer-reviewed study found that measures voice-leading practice specifically in keyboard accompaniment (as opposed to chorales or polyphony) in pop, gospel or worship piano. The Wikipedia "Voice leading" page was not on the allowlist.
