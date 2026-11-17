A band writer for the engine can be drawn from measured parts the same way the melody is: real songs thin the intro to about 70% of their fullest band, thicken the chorus by about a quarter, play bass about once a beat at any tempo, and keep one drum bar for about half the song. Genre changes the details more than the plan.

## The data

Two collections were measured; three more that would answer the open questions could not be reached from this session.

|Collection|What it is|Used for|Licence|
|---|---|---|---|
|POP909 with phrase labels|909 Chinese pop songs, each a lead melody, a secondary melody and a professional piano accompaniment; human phrase labels (intro, sung phrases A, B and others, instrumental phrases, outro) from Dai, Zhang and Dannenberg|Texture by section role|CC BY 4.0|
|Lakh Pianoroll Dataset (LPD-5 cleansed)|21,425 songs in five parts (drums, piano, guitar, bass, strings), 4/4; 9,329 read, up to 1,500 per genre|The band by genre|CC BY 4.0|
|Million Song Dataset artist terms (via Gold-Caps)|Genre words per artist|The genre of each Lakh song: the family of the artist's top term|CC BY 4.0|
|Groove MIDI Dataset|Human drumming with fills labelled, many styles|Not reached (its host is refused)|CC BY 4.0|
|Timbre in Popular Song (TiPS)|Texture and timbre by section in 400 songs, 100 each of country, pop, metal and hip hop|Not reached; only the pop part is published so far|Open, in progress|
|Lakh MIDI (raw)|The original files with every instrument|Not reached (its host is refused); the piano-roll version above stands in|CC BY 4.0|

Two limits run through the Lakh readings: piano rolls merge repeated strikes of one held pitch, so chordal onsets are undercounted; and genre comes from the artist, not the song.

## The academic record

Scholars describe a pop band as a few functional layers whose entrances and exits mark the form; the most successful accompaniment systems retrieve real phrases and fit them to new chords rather than inventing parts note by note.

- **Functional layers (Moore 2012; Lavengood 2020).** Allan Moore's four layers: the explicit beat, the functional bass, the harmonic filler and the melody. [Open Music Theory](https://viva.pressbooks.pub/openmusictheory/chapter/texture-in-pop-music/) The harmonic filler fills the registral space between the bass and the melody. [Lavengood, MTO](https://mtosmt.org/ojs/index.php/mto/article/view/515/79) Lavengood adds a fifth, the novelty layer: intermittent, cutting in and out, often in call and response with the melody, the least common of the layers. [slides](https://presentations.meganlavengood.com/2025-tops.html)

- **The bass as its own line (de Clercq 2019).** Bass and harmony often move independently, a "harmonic-bass divorce" like the melody's. [article](https://www.midside.com/publications/declercq_2019_spectrum.pdf)

- **Form by texture.** Most work on pop form has centred on melody and harmony, with drums studied less (Geary 2024). [MTO](https://www.mtosmt.org/issues/mto.24.30.2/mto.24.30.2.geary.pdf) Texture change cues listeners that a section is changing; the verse-to-chorus step intensifies by layering new instruments and changing register, and a late surge of new events often comes about two-thirds of the way through (Schwitzgebel 2025, after White 2020). [MTO](https://mtosmt.org/issues/mto.25.31.1/mto.25.31.1.schwitzgebel.pdf) A 665-song [McGill](https://www.mcgill.ca/timbre-orchestration/research/projects/strategic-projects/interactions-timbre) subset annotated for texture and timbre found these changes are formal markers, though only general trends were identified. McGill

- **Accumulation (Spicer 2004).** "Accumulative" and "cumulative" forms build by layering, tied to multitrack recording. [chapter](https://www.taylorfrancis.com/books/9781315088631/chapters/10.4324/9781315088631-15)

- **Genre norms are still being measured.** TiPS encodes texture by section in 400 songs from the 1990s across country, pop, metal and hip hop on Moore's and Lavengood's layers. [project](https://timbreandorchestration.org/writings/project-reports/timbre-in-popular-song) Its genre norms have not been published yet.

- **Accompaniment systems.** POP909 offers several professional piano arrangements of 909 popular songs for arrangement research. [paper](https://arxiv.org/abs/2008.07142v1) AccoMontage arranges whole pieces by retrieving phrase montages from a database, recombining them by dynamic programming, then fitting their chords to the lead sheet, and beat learning-only baselines. [paper](https://arxiv.org/abs/2108.11213) PopMAG generates multi-track accompaniment for pop. [summary](https://arxiv.deeppaper.ai/papers/2008.07703v1)

## Texture by section role (POP909)

The accompaniment lifts the chorus by playing more notes, not by moving register or holding longer: in 88% of songs the B phrases (usually the chorus) are busier than the A phrases (usually the verse).

Medians over 11,431 labelled phrases in 909 songs (piano accompaniment).

|Phrase|Phrases|Piano notes a beat|Notes struck together|Share of time sounding|Secondary melody, notes a beat|
|---|---|---|---|---|---|
|Intro|872|2.31|1.42|86%|1.24|
|A (usually the verse)|2,936|2.93|1.51|92%|0.50|
|B (usually the chorus)|3,074|3.78|1.65|92%|0.63|
|Other sung phrases|2,199|3.56|1.67|91%|0.69|
|Instrumental phrases|1,799|3.25|1.65|92%|1.36|
|Outro|551|2.82|1.41|91%|1.06|

Paired within each song (865 songs with both): B over A by a median 0.73 notes a beat; B strikes more notes together in 61% of songs; register and sustain barely move (each about half up, half down). The secondary melody plays hardest where the voice rests: in intros and instrumental phrases at about twice its rate under sung phrases. The last chorus is no busier than the first (a median change of 0; busier in 49% of songs), unlike the build Window 38 reads in Western records; POP909's piano-only Chinese pop may simply not build by the piano.

## The band by genre (Lakh)

The plan is shared across genres and the details are not: every genre's commonest snare bar is 2 and 4 and in every genre shown the intro starts at about 70% of the fullest band, while kick patterns, bass syncopation and piano voicing tell country from soul.

Medians unless noted; kick bars on sixteenths, x an onset, the bar starting left.

|Genre|Songs|Snare on 2 and 4 (commonest bar)|Commonest kick bars|Hats in eighths / sixteenths|Bass notes a beat|Bass off the eighths|Piano notes struck together|Intro's band, share of the fullest|
|---|---|---|---|---|---|---|---|---|
|Country|805|69%|`x.......x.......` 28%, `x.....x.x.......` 23%|63% / 11%|0.91|1%|1.90|72%|
|Soul and R&B|598|67%|`x...x...x...x...` 15%, `x.......x.......` 13%|61% / 17%|1.12|11%|2.16|70%|
|Gospel|274|62%|`x.......x.......` 18%, `x.....x.x.......` 18%|59% / 12%|0.92|3%|1.83|69%|
|Pop|1,495|62%|`x...x...x...x...` 20%, `x.....x.x.......` 16%|54% / 16%|1.05|5%|1.89|68%|
|Rock|1,498|64%|`x.....x.x.......` 14%, `x.......x.......` 13%|57% / 13%|1.10|2%|1.92|67%|
|Folk|620|59%|`x.......x.......` 14%, `x.....x.x.......` 14%|56% / 12%|0.98|3%|1.84|70%|

What else the songs show:

**One drum bar for half the song.** The commonest kick-and-snare bar fills about half a song's bars (country 61%, the steadiest; rock 48%), around ten other bars filling the rest.

- **The bass plays about once a beat at any tempo.** Across all genres, a median 1.0 bass notes a beat below 85 beats a minute and 1.15 above 130. Slow songs syncopate more: 16% of bass notes fall off the eighths below 85, against 0.3% above 130. The engine's routine, run at song 56's doubled tempo, would have played about three a beat.

- **Chordal parts.** Guitar's commonest bar is straight eighths (15% to 23% of songs by genre). Country piano most often holds one chord a bar (20%), soul's plays eighths (15%) with thicker chords. Strings hold whole notes. About half of chordal strikes land with a bass note (country guitar 44%, soul piano 57%). Registers, 10th to 90th percentile medians: piano about D3 to B4, guitar D3 to G4, strings A3 to F5.

- **Parts playing.** The first tenth of a song carries about 70% of its fullest band, the second to the ninth tenths at the fullest, the last tenth about 93%. Drums enter by bar 1 or 2 in most songs.

- **What could not be read.** Where fills fall: Lakh songs do not start on a phrase boundary, so fills by place in an 8-bar group come out flat. That needs phrase-aligned drums (the Groove MIDI Dataset labels its fills) or section labels.

## What this means for v8's arrangement writer

Build it the way AccoMontage and the melody search both work: draw real parts from kept tables, fit them to the engine's chords, and gate them by the section plan.

1. **The section plan first.** For each section, draw the number of parts and each part's density from kept rates: the intro about 70% of the fullest band and its accompaniment about 0.6 times the chorus's notes a beat; the chorus about a quarter busier than its verse; the middle of the song at the fullest; the last tenth about 93%. This writes Module 9.12's arc and fix 238's parts playing instead of hand-arranging to pass them.

2. **The four layers, one writer each** (Moore's layers, as in the spec's Window 118 and 119 rules):

   - _Explicit beat:_ the genre's kick-and-snare bar drawn from the kept bars, held for about half the song with about ten variants; hats or ride in eighths unless the genre's sixteenth rate is drawn; a fill and crash at section ends (fix 236).

   - _Functional bass:_ the routine, made tempo-aware: about one note a beat at any tempo, syncopating off the eighths at the slow-song rate (16% below 85 beats a minute) and the genre's rate (soul 11%, country 1%).

   - _Harmonic filler:_ one bar rhythm per section from the instrument's and genre's kept rhythms (fix 237), voiced on the engine's chords inside Module 9.14's limits and the kept registers, about half of its strikes with the bass.

   - _Novelty:_ short answers only in the voice's gaps (the kept fill table, fix 235), intermittent, call and response, never under a sung word (fix 379).

3. **Tests.** Every drawn arrangement passes 9.12, 9.13, 9.14, 236 to 238 and 379; its readings fall inside the genre's kept quartiles above; and the no-hand-input test: no band note from a hand-typed list.

**What still needs data.** Fill placement and fill shapes by style (the Groove MIDI Dataset, refused here); texture by section in Western multitrack records (POP909 is Chinese pop and piano only; TiPS's country, metal and hip-hop parts are unpublished); song-level genre labels (Lakh's are the artist's). Allowing this session's network to reach those hosts, or attaching the files, would close most of it.

## Files and sources

The scripts and tables are in the repo under `studies/arrangement` (commit 36a16ef): `pop909_texture.py`, `lpd_genres.py`, `lpd_band.py` and `lpd_band_tables.py`, with their JSON outputs. The raw data is not kept in the repo. This study follows [the audit](https://claude.ai/artifact/4VpCZjhV64ua7EjPykjS1K) and [the harmony study](https://claude.ai/artifact/9vgkWHkjy3PyVMB9iKDkBJ).

Sources:

- Moore's layers and Lavengood's novelty layer: [Open Music Theory, Texture in Pop Music](https://viva.pressbooks.pub/openmusictheory/chapter/texture-in-pop-music/); Lavengood, [The Cultural Significance of Timbre Analysis](https://mtosmt.org/ojs/index.php/mto/article/view/515/79) (MTO 2020); [Instrumental Timbre slides](https://presentations.meganlavengood.com/2025-tops.html)

- de Clercq, [The Harmonic-Bass Divorce in Rock](https://www.midside.com/publications/declercq_2019_spectrum.pdf) (2019)

- Geary, [drums and form](https://www.mtosmt.org/issues/mto.24.30.2/mto.24.30.2.geary.pdf) (MTO 2024)

- Schwitzgebel, [texture, cues and expectation in post-millennial pop](https://mtosmt.org/issues/mto.25.31.1/mto.25.31.1.schwitzgebel.pdf) (MTO 2025)

- [Interactions of timbre and form, McGill](https://www.mcgill.ca/timbre-orchestration/research/projects/strategic-projects/interactions-timbre)

- Spicer, [(Ac)cumulative form in pop-rock music](https://www.taylorfrancis.com/books/9781315088631/chapters/10.4324/9781315088631-15) (2004)

- [The Timbre in Popular Song (TiPS) corpus](https://timbreandorchestration.org/writings/project-reports/timbre-in-popular-song) (2023)

- Wang et al., [POP909](https://arxiv.org/abs/2008.07142v1) (ISMIR 2020); Dai, Zhang and Dannenberg, [phrase labels](https://www.github.com/Dsqvival/hierarchical-structure-analysis) and [paper](https://arxiv.org/pdf/2010.07518) (2020)

- Zhao and Xia, [AccoMontage](https://arxiv.org/abs/2108.11213) (ISMIR 2021); Ren et al., [PopMAG](https://arxiv.deeppaper.ai/papers/2008.07703v1) (2020)

- [Lakh Pianoroll Dataset](https://zenodo.org/records/5646574) (Zenodo); [Gold-Caps LMD-Matched](https://zenodo.org/records/10178563) (Zenodo); [Groove MIDI Dataset](https://magenta.tensorflow.org/datasets/groove)
