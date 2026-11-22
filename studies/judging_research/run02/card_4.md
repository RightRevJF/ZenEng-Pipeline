# Card 4: Note-transition networks across four centuries (Di Marco et al. 2026)

## Citation and link
Di Marco, N., Loru, E., Galeazzi, A., Cinelli, M., and Quattrociocchi, W. (2026). Decoding the evolution of melodic and harmonic structure of Western music through the lens of network science. *Scientific Reports* 16, 11121 (published 23 April 2026). doi:10.1038/s41598-026-42872-7. Preprint: arXiv:2501.07557, titled "Decoding Musical Evolution Through Network Science" (v1, 13 January 2025, the only arXiv version).

Copies read, both whole, through a page-reading tool that answers questions about the page. The numbers below are as that tool reported them, not copied by hand.
- **Preprint PDF**, https://arxiv.org/pdf/2501.07557: main text, methods, supplementary figures, Extended Data Tables 2 and 3, and all 52 references.
- **Published version**, the open-access (Creative Commons) PDF held in Sapienza's repository, https://iris.uniroma1.it/retrieve/8c5f0957-59a5-4e15-b043-7336d4eb0c89/DiMarco_decoding_evolution_2026.pdf: main text, methods, and all 73 references. The article is open access.

Not reached:
- arxiv.org/html/2501.07557 and the nature.com article page: the permission requests were not answered.
- The published Supplementary Information, which sits on nature.com. Because of this, the published version's Mann-Kendall table (S2), its effective-resistance figures (S4, S5) and its temporal-bias check (S6, Table S1) were seen only as text describing them.

**How the published version differs from the preprint:**
- The main text no longer analyses Spotify popularity. Popularity is still collected, but the results never use it.
- It adds a second robustness measure, effective resistance.
- It adds a temporal-bias check.
- It adds a review of earlier work on simplification: Serrà 2012, Mauch 2015, Hamilton and Pearce 2024, Clark and Arthur 2022, Deruty 2024.
- The dated count is 15,243 pieces, against 15,192 in the preprint.
- It is more cautious, calling its readings speculative and limited to a symbolic, twelve-tone view.

The popularity numbers below therefore come from the preprint only.

## The claim, and the data it rests on
- **Corpus:** MetaMIDI, more than 400,000 MIDI files. Of these, about 160,000 have a title, artist and genre. Keyword filtering to six macro-genres (Classical, Jazz, Rock, Pop, Electronic, Hip Hop), a length over 60 seconds and a clean parse leave about 40,000. After fuzzy matching to Spotify, 21,480 unique pieces remain, dated 1600 to 2021.
- **Genre and dates:** genre comes from the MetaMIDI tags. Release dates were guessed by an LLM (Gemini 1.5 Flash) for about 72% of pieces, and checked against 100 hand-dated songs. Gemini dates are used before 1980 and Spotify dates after.
- **Claims:**
  1. Classical and Jazz networks are more "complex" than those of the newer genres: higher weighted efficiency, higher mean node entropy, lower weighted reciprocity.
  2. Over time, Classical efficiency falls (Mann-Kendall tau -0.40) and Jazz efficiency rises, then falls. The genres drift together, which the authors call simplification and loosely link to streaming and algorithmic curation.
- **What counts as success:** there is no success outcome in the published paper. It describes genres and eras. Only the preprint's Extended Data Table 3 sets the measures against Spotify track popularity, which is a current-streaming score.

## The measure: from the notes or not?
Yes, from the notes. Each MIDI channel becomes a directed, weighted network. A node is a distinct note, and the paper never says whether that means an absolute pitch or a pitch class. An arrow runs from one note to the note that follows it, weighted by how often that happens. Repeated notes (self-loops) are dropped. When a chord follows a chord, every note of the first is joined to every note of the second. Drum channels are ignored.

**What is left unclear:**
- The paper never says how the networks of the separate channels become one network per piece.
- So a piece's network is a blend of all its parts (bass, pads, lead), not the tune and not the chord progression.

**Measures:**
- density
- reciprocity, and weighted reciprocity: how much traffic goes A to B and back to A
- mean node entropy: how evenly a note spreads to its possible next notes
- global efficiency, unweighted and weighted
- vertex count
- network entropy and effective resistance, as robustness checks
- a 12-number interval profile (how often each interval from 0 to 11 semitones occurs) with a UMAP map, plus graph2vec embeddings

No audio, lyrics or marketing go into the measures. Spotify supplies only dates and, in the preprint, the popularity outcome.

## How big the effect is and how it was checked
- **Genre differences:** most pairwise Mann-Whitney tests (Holm-corrected) reject sameness. Rock, Pop, Electronic and Hip Hop often cannot be told apart from one another.
- **Interval map:**
  - Component 1 tracks density (r about 0.22), reciprocity (0.18) and efficiency (0.16).
  - Component 2 tracks weighted reciprocity (-0.44), weighted efficiency (0.37) and entropy (0.30).
- **Trends over time (preprint, Mann-Kendall on decade means, Holm-adjusted):**
  - Classical efficiency: tau -0.40, p .001.
  - Jazz efficiency: tau -0.49, p .048.
  - Rock efficiency: +0.71, p .037, a rise.
  - Every other genre-and-measure pair is not significant.
  - These tests run on a handful of decade points.
- **Popularity, preprint only (Pearson r with Spotify popularity):**
  - Classical: weighted efficiency -0.19, entropy -0.17, density -0.12, weighted reciprocity +0.09.
  - Jazz: entropy -0.16, weighted reciprocity +0.16, weighted efficiency -0.13.
  - Pop and Rock, where Luthier lives: all four under 0.07 in size. Entropy -0.04, weighted reciprocity +0.05 and +0.05, weighted efficiency -0.04 and -0.06. These pass only because the samples are large.
  - Hip Hop and Electronic: mostly null.
  - The direction is that more popular pieces are simpler, with more back-and-forth and less branching.
  - At the artist level, sticking to a narrow range of intervals goes slightly with lower artist popularity (r -0.12).
- **Checks:**
  - Null models: rewired networks have higher efficiency than the real ones, while weight-shuffled networks look like the real ones.
  - Alternative measures (network entropy, effective resistance) and graph2vec give the same genre ordering.
  - Release dates were validated on 100 hand-dated songs.
- **Missing:**
  - No held-out data and no second corpus.
  - No control for the number of notes, piece length, number of channels, or how the MIDI file was made. Classical files are often sequenced from scores; pop files are often karaoke-style arrangements made by fans. These are corpus-source and transcription-quality confounds that line up with genre.
  - Genre tags are coarse. Spotify matching uses the first-listed artist and fuzzy titles. The authors admit both.
  - Popularity is not adjusted for era, even though Spotify popularity heavily favours recent tracks.

## What it says about the yardstick (lasting love plus covers), not only popularity
Very little directly. The published paper has no outcome. The preprint's outcome is Spotify popularity: a snapshot of current streams, uncorrected for age, with no covers. It is close to the "popularity alone" this project excludes.
- **One relevant reading:** within Pop and Rock, popularity leans faintly toward lower branching and more back-and-forth (|r| of 0.04 to 0.06). That is the audience profile Luthier already found in its views study: predictable, denser, more repetitive.
- **What it suggests for the yardstick:** the covers study found the musician channel pulling the other way, toward chords that move. So these network measures may also split the two channels. Popularity would lean toward simpler networks, and covers toward richer ones.
- **The paper's claim that music has simplified over time** is a claim about genre mixes and eras, not about which songs last. It says nothing about lasting love.

## One test Luthier could run on its kept tables
**Do the branching and back-and-forth of a song's chord network predict the yardstick beyond chords that move?**

- **Data:** Hooktheory songs on the yardstick, 2005 or earlier (the 944-song chord set), with the 2006-2012 set (407 songs) kept unseen for a repeat.
- **Network:** one per song, built from chords and not from all notes:
  - nodes are chords named relative to the key (Roman numerals with quality);
  - an arrow runs from each chord to the next chord that differs from it, weighted by count, with repeats dropped as in the paper;
  - built over the whole song, section boundaries ignored.
- **Measures:**
  - E, mean node entropy: how evenly each chord branches to different next chords, normalised as in the paper.
  - R, weighted reciprocity: the share of traffic that goes A to B and straight back.
- **Controls:** year, source, number of distinct chords (vertex count, which the paper never held), song length in chords, and the existing within-section chord-repetition measure.
- **Prediction, written now:**
  - E goes with higher G: partial Spearman +0.05 or more in each half (artists split by name) and pooled p < .05.
  - R goes with lower G: -0.05 or lower in each half.
  - This is the opposite of the preprint's popularity direction.
- **Fail:**
  - pooled E below +0.03, or halves of different sign;
  - R likewise;
  - or the sign flips on the 407 fresh songs.
- **Is it just "chords that move" under another name?** Partly, and the test is built to show how much.
  - Repetition counts how often a pattern recurs. Entropy ignores recurrence: a I-V-vi-IV loop played twenty times has entropy zero, exactly like the same loop played once. Entropy instead measures whether a chord ever leads somewhere new.
  - Reciprocity separates a two-chord rocking vamp, which scores high, from a four-chord cycle, which scores zero, even though both loop.
  - So, with repetition held:
    - If E adds nothing, it is the same finding renamed.
    - If E adds something, branching is a separate property of the chords.
    - If R carries the effect, rocking back and forth, not looping as such, is what musicians avoid.
- **Melody-network version:** not recommended. Five earlier shape runs found nothing in the tune on unseen songs.

## Leads
1. **Information content of note transitions in the music of J. S. Bach.** Kulkarni, S., David, S. U., Lynn, C. W., Bassett, D. S., 2024, Physical Review Research 6, 013136, doi:10.1103/PhysRevResearch.6.013136. A more careful note-transition network with an information measure tied to how listeners learn; a better-founded version of the entropy idea.
2. **Network representations reveal structured uncertainty in music.** Rosselló, L. B., Jankowski, R., Bersini, H., Boguñá, M., Serrano, M. A., 2025, arXiv:2509.14053, doi:10.48550/arXiv.2509.14053. Network-geometry group (Boguñá, Serrano); a likely route to the project's non-Euclidean and hidden-geometry interest.
3. **On the complex network structure of musical pieces: Analysis of some use cases from different music genres.** Ferretti, S., 2017, Multimedia Tools and Applications 77, 16003-16029, doi:10.1007/s11042-017-5175-y. The earlier piece-level note-network method this paper builds on; check how it handles channels and pitch identity.
4. **Trajectories and revolutions in popular melody based on US charts from 1950 to 2023.** Hamilton, M., Pearce, M., 2024, Scientific Reports 14, 14749, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11224395/. A note-based study of chart melodies with information-theoretic complexity; closest in corpus to Luthier's, and its simplification claim can be tested against the yardstick.
5. **Evolution of music by public choice.** MacCallum, R. M., Mauch, M., Burt, A., Leroi, A. M., 2012, PNAS 109, 12081-12086, doi:10.1073/pnas.1203182109. Music evolved by listener selection alone; an experimental handle on what "love" selects for in the notes.
