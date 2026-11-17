A chord writer for the engine is feasible from measured sequences: on verses and choruses in major keys, a simple model drawn from 592 training songs already passes as kept on every measure tried. Minor keys, bridges and pre-choruses need more data, genres need data this session cannot reach, and real progressions loop in a way the simple model does not.

## The data

Two collections were read in full; the two largest genre-labelled collections could not be reached from this session.

|Collection|What it is|Used for|Licence|
|---|---|---|---|
|McGill Billboard|890 chart slots, 739 unique songs charting 1958 to 1991; chords bar by bar with section labels and the tonic; raw files from ChoCo v1.0.0 (Zenodo 7706751)|Every measure here, and the prototype|CC0|
|Rolling Stone 200|de Clercq and Temperley's Roman-numeral analyses of 200 songs, written as section rules|The replication|Research corpus|
|Chordonomicon|Over 666,000 user-made chord charts with section, genre and date labels|Not reached: its download host is refused by this session's network, and its dataset card says CC BY-NC 4.0 (non-commercial), against the paper's CC BY 4.0|CC BY-NC 4.0 (card)|
|de Clercq's country corpus|200 famed country songs in Nashville numbers|Not reached (its site is refused)|Unknown|

The Billboard songs carry no genre labels, so nothing below is by genre. Mode was read per song: minor when the tonic chord is minor more often than major (128 minor, 611 major).

## What the published research says

Pop harmony has its own grammar, not common practice's: IV and ♭VII matter as much as V, progressions loop, and genre labels are a weak guide.

- **Rock harmony (de Clercq and Temperley 2011).** A hand analysis of 100 songs from Rolling Stone's 500 Greatest Songs, 20 a decade from the 1950s to the 1990s, with over 90% agreement between the two analysts. IV is the most common chord after I and most often precedes it; the five commonest chords are I, IV, V, ♭VII and VI; II, VI and III form one group of chords that go together, and ♭VII, ♭III and ♭VI another, which the authors read as a modal organisation. [paper;](https://rockcorpus.midside.com/2011_paper/declercq_temperley_2011.pdf) [slides](https://www.midside.com/presentations/declercq_2010_nemcog_slides.pdf)

- **Root motion.** The asymmetries of common-practice music (fourths up preferred to fourths down) are mostly absent in rock, so a chord's place before or after the tonic is the useful distinction. [summary](https://digitallibrary.vassar.edu/sites/default/files/2022-01/Harmony_and_Syntax_in_Contemporary_Pop_Music_0.pdf)

- **The McGill Billboard set (Burgoyne, Wild and Fujinaga 2011).** 890 slots sampled at random from the Billboard charts, annotated by experts with sections and chords; released under CC0. [paper](https://ismir2011.ismir.net/papers/OS8-1.pdf); [licence](https://mirdata.readthedocs.io/en/0.3.8/_modules/mirdata/datasets/billboard.html)

- **Loops since 2000.** A corpus of 2002 to 2021 songs is more repetitive than McGill's; most chord loops appear in only one song, and the most schematic loops were shared more widely in the McGill era (Chander and Quinn 2023). [preprint](https://easychair.org/publications/preprint/vRwsT) Loops of IV, V and vi hovering above the tonic (the "plateau loop") became widespread in recent pop (Duinker 2019). [article](https://mtosmt.org/ojs/index.php/mto/article/view/464) In post-2000 EDM-pop the loop is mostly one diatonic collection, with the melody moving independently above it (Park 2025). [dissertation](https://mtosmt.org/docs/diss-index.php?id=635)

- **Genre.** User tags put as much as 60% of recent songs under "pop/rock", and song-by-song uniqueness makes corpus averages a weak stand-in for any one song. [article](https://www.osu.tests.sfulib4.publicknowledgeproject.org/index.php/EMR/article/view/5576/5604) Country was studied by corpus only recently: de Clercq built a 200-song country corpus to test the "three chords" caricature, which Jocelyn Neal calls a misconception. [talk](https://www.midside.com/presentations/declercq_2021_smt_miig_text.pdf)

- **Writing chords by model.** MySong (Simon, Morris and Basu 2008) chose chords for a sung melody with a hidden Markov model trained on a song database, and listeners rated the results positively. [paper](https://microsoft.com/en-us/research/uploads/prod/2016/02/mysongchi2008.pdf) A semi-Markov version adds each chord's duration, so it finds where the harmony changes as well as what it changes to (Groves 2013). [paper](https://ojs.aaai.org/index.php/AIIDE/article/download/12654/12502/16171) Comparative studies judge generated chords by listening tests on fit and interest against the human progression. [study](https://arxiv.org/pdf/2001.02360)

- **Chords first or melody first.** Songwriters do both; some start from a progression and let its mood draw out melody and lyric, others hand a melody to a co-writer to harmonise. No study found settles which works better, so the engine should choose by its own test. [example](https://secretsofsongwriting.com/tag/first)

## What the Billboard songs show

Each section kind has its own job, and the jobs are sharp enough to write by: verses open on I three times in four, bridges end on V nearly half the time, and pre-choruses hardly touch the tonic.

**Major keys** (medians; first and last chord: share of sections; bigrams: share of a kind's chord changes).

|Section|Sections|Bars|Changes a bar|Distinct chords|Tonic's share|Commonest first|Commonest last|Commonest moves|
|---|---|---|---|---|---|---|---|---|
|Verse|1,690|12|0.88|4|41%|I 78%|I 39%, V 29%|IV→I 11%, I→IV 10%, V→I 8%|
|Pre-chorus|219|6|1.00|4|13%|IV 24%, I 23%, vi 16%|V 39%, IV 15%|IV→V 9%, I→IV 8%|
|Chorus|1,646|8|1.00|4|33%|I 57%, IV 15%|I 35%, V 28%|IV→I 10%, I→IV 9%, V→I 8%|
|Bridge|317|8|0.88|4|14%|IV 34%, I 15%|V 46%|IV→I 8%, IV→V 7%|
|Intro|557|5|1.00|3|50%|I 63%|I 38%, V 22%|IV→I 10%, I→IV 10%|
|Outro|339|10|1.00|3|50%|I 66%|I 50%|IV→I 12%, I→IV 12%|

**Minor keys** (128 songs).

|Section|Sections|Changes a|Distinct|Tonic's|Commonest|Commonest|Commonest|
|---|---|---|---|---|---|---|---|
|||bar||share|first|last|moves|
|Verse|361|0.69|3|48%|i 76%|i 41%, V 16%, ♭VII 11%|i→IV 5%,♭VII→i 5%, i→♭VII 5%|
|Pre-|66|1.13|5|17%|♭VI 32%, i|♭VII 21%, V|♭VI→♭VII 10%|
|chorus|||||29%|20%||
|Chorus|367|1.00|3|31%|i 54%|i 23%,♭VII 17%, V 14%|♭VII→i 6%, ♭VI→♭VII 6%, i→♭VI 5%|
|Bridge|53|0.88|4|24%|♭VI 26%|i 23%, V 21%|♭VI→♭VII 8%|

What else the songs show:

- **Chords from outside the key.** In major, ♭VII is in 18% of verses and choruses and 22% of bridges; II (V of V) in 12% to 22%. In minor, a major IV, Dorian's raised sixth, is in 23% of verses and 24% of choruses, the commonest chord from outside the key.

- **The joins.** A pre-chorus or bridge hands to the chorus on V→I most often (24% and 36% of joins); a chorus hands to a bridge on I→IV (18%).

- **Returns.** A later verse keeps the first verse's chords bar for bar 60% of the time, a chorus 55%, a pre-chorus 81%.

- **Loops.** Under a strict reading (90% of bars repeat at the period), 29% of major choruses and 31% of verses loop in 1, 2, 4 or 8 bars, more in minor (47% of choruses); most sections vary their cell.

- **Over time.** Harmony moved faster: the median verse changed chord every two bars in the 1950s and once a bar by the 1980s and 1990s.

## A prototype chord writer, tested

Where the data is plentiful, chords drawn from kept sequences pass as kept; where it is thin, the model does no better than drawing chords at random by frequency.

The prototype is a variable-order Markov model (up to three chords of context) over each section kind's chord changes, by mode, trained on 592 songs and read against the heldout 147. Each change's length is drawn from the kind's kept lengths. The baseline draws chords by their frequency alone. A first-chord or last-chord distance of 0 means the same distribution as the held-out songs, 1 means none in common.

|Section|Held out|First chord: model / baseline|Last chord: model / baseline|Distinct chords: kept / model|Tonic's share: kept / model|Bits a change: model / baseline|
|---|---|---|---|---|---|---|
|Verse, major|339|**0.10**/ 0.47|** 0.14**/ 0.32|4 / 4|34% / 33%|** 3.81**/ 4.52|
|Chorus, major|329|** 0.11**/ 0.32|** 0.14**/ 0.31|4 / 4|29% / 29%|** 3.45**/ 4.44|
|Bridge, major|68|0.30 / 0.23|0.38 / 0.42|4 / 4|17% / 13%|3.98 / 4.79|
|Pre-chorus, major|38|0.28 / 0.35|0.46 / 0.74|4 / 4|0% / 10%|4.26 / 4.77|
|Verse, minor|68|0.15 / 0.50|0.26 / 0.33|3 / 4|49% / 32%|4.62 / 4.33|
|Chorus, minor|80|0.24 / 0.36|0.29 / 0.33|3 / 4|30% / 25%|4.40 / 4.38|

Three things it shows:

1. ** Verses and choruses in major pass.** First and last chords, distinct chords, the tonic's share and changes a bar all sit with the held-out songs, and the model predicts the next chord about one bit better than frequency alone.

2. **Minor keys, bridges and pre-choruses do not.** With 51 to 293 training sections, the model learns little beyond frequency (minor verses and choruses: no better in bits) and minor verses hold the tonic too little (32% against 49%). These need more songs, or rules from Table CP as gates.

3. **It rambles where real songs loop.** Drawn sections run on ("I ii iii V vi iii IV I iii ii IV I") where kept ones repeat a two-or four-bar cell. The writer needs a structural step: draw a cell, then repeat or vary it at the kept rates.

## The same measures on a second collection

The section jobs hold on the Rolling Stone 200, a different collection analysed by different people: endings agree almost exactly, openings closely.

|Section|RS200 sections|Last chord: RS200 / Billboard|First chord: RS200 / Billboard|Top moves, RS200|
|---|---|---|---|---|
|Verse|219|I 38%, V 29% / I 39%, V 29%|I 69% / I 78%|IV→I 13%, I→IV 12%, V→I 8%|
|Chorus|162|I 33%, V 27% / I 35%, V 28%|I 43%, IV 15% / I 57%, IV 15%|I→IV 13%, IV→I 11%, V→I 8%|
|Bridge|69|V 59% / V 46%|I 29%, IV 23% / IV 34%, I 15%|IV→I 10%, I→IV 8%|
|Intro|127|I 38%, V 22% / I 38%, V 22%|I 64% / I 63%|I→IV 11%, IV→I 11%|

The RS200 figures mix major and minor songs (minor openings, i, take 12% to 15% of them), which accounts for most of the gap in first chords. Both collections change chord about once a bar and use three or four distinct chords a section.

## What this means for v8's harmony writer

Build it in three layers, chords first, and test it the way the melody is tested.

1. **The cell.** For each section, draw a loop cell of one, two or four bars from the kept cells of its kind and mode, or decide not to loop, at the kept rates (about seven sections in ten in major do not repeat strictly).

2. **The sequence.** Fill the cell, or the whole section when it does not loop, from the variable-order model of what follows what, by section kind and mode. Draw each chord's length from the kind's kept lengths, at the decade's harmonic rhythm.

3. **The jobs as gates.** Keep a section only if its first and last chords, distinct chords, tonic share and out-of-key share fall inside the kept quartiles (Tables CN and CP and these new tables). A verse opens on I; a pre-chorus or bridge ends off the tonic, usually on V; joins follow the kept moves.

Then the existing chart redraw (438) and the bass's inversions (440) run unchanged, and the melody is drawn over the written chords, as it is now. Chords first suits the engine, whose melody search already aims at chord tones; the published systems that go melody first (MySong and its successors) remain a fallback if the fit test fails.

**Mode and colour.** Minor sections draw ♭VI, ♭VII, ♭III and Dorian's IV at their kept rates; in major, ♭VII and II are the common outside chords. This replaces the hand-picked chord vocabularies by song type, which become a light preference on top.

**What still needs data.** Genre (country, soul, gospel, worship): the Billboard songs carry no labels, and the two labelled collections are unreachable here. Two routes: allow this session's network to reach the Chordonomicon host (and settle its non-commercial licence for an engine that writes songs for release), or obtain de Clercq's country corpus. Minor keys, bridges and pre-choruses: more songs, or the section-job gates carrying them until then.

**The tests.** (a) Every drawn section passes the gates; (b) on held-out songs the model beats frequency alone in bits a change for every kind it writes; (c) a listening check, drawn against kept progressions in the same section, as the published studies do; (d) the no-hand-input test from the audit: no chord in a song may come from a hand-typed list.

## Files and sources

The scripts and tables are in the repo under `studies/harmony` (commit d8055b9): `parse_billboard.py`, `measure_billboard.py` (writes `billboard_tables.json`), `prototype_writer.py` (writes `prototype_results.json`) and `rs200.py` (writes `rs200_tables.json`). The raw data is ChoCo v1.0.0 from [Zenodo record 7706751](https://zenodo.org/records/7706751), not kept in the repo. This study follows [the harmony and arrangement audit](https://claude.ai/artifact/4VpCZjhV64ua7EjPykjS1K).

Sources:

- de Clercq and Temperley, [A corpus analysis of rock harmony](https://rockcorpus.midside.com/2011_paper/declercq_temperley_2011.pdf) (Popular Music, 2011), and [conference slides](https://www.midside.com/presentations/declercq_2010_nemcog_slides.pdf)

- [Harmony and Syntax in Contemporary Pop Music](https://digitallibrary.vassar.edu/sites/default/files/2022-01/Harmony_and_Syntax_in_Contemporary_Pop_Music_0.pdf) (Vassar thesis)

- Burgoyne, Wild and Fujinaga, [An expert ground-truth set for audio chord recognition and music analysis](https://ismir2011.ismir.net/papers/OS8-1.pdf) (ISMIR 2011); [the CC0 licence, via mirdata](https://mirdata.readthedocs.io/en/0.3.8/_modules/mirdata/datasets/billboard.html)

- Chander and Quinn, [The Decline of Harmonic Schemata in Popular Music Chord Loops](https://easychair.org/publications/preprint/vRwsT) (2023)

- Duinker, [Plateau Loops and Hybrid Tonics in Recent Pop Music](https://mtosmt.org/ojs/index.php/mto/article/view/464) (Music Theory Online, 2019)

- Park, [Diatonic Chord Loops in Post-Millennial Pop Harmony](https://mtosmt.org/docs/diss-index.php?id=635) (dissertation, 2025) [On genre labels and corpus averages](https://www.osu.tests.sfulib4.publicknowledgeproject.org/index.php/EMR/article/view/5576/5604) (Empirical Musicology Review) de Clercq, [A Corpus Analysis of Harmony in Country Music](https://www.midside.com/presentations/declercq_2021_smt_miig_text.pdf) (talk, 2021)

- Simon, Morris and Basu, [MySong](https://microsoft.com/en-us/research/uploads/prod/2016/02/mysongchi2008.pdf) (CHI 2008)

- Groves, [Automatic Harmonization Using a Hidden Semi-Markov Model](https://ojs.aaai.org/index.php/AIIDE/article/download/12654/12502/16171) (2013)

- [Automatic Melody Harmonization with Triad Chords: A Comparative Study](https://arxiv.org/pdf/2001.02360) (2020)

- [Chordonomicon](https://arxiv.org/abs/2410.22046) (2024) and [its dataset card](https://huggingface.co/datasets/ailsntua/Chordonomicon)

- [Chords or melody first](https://secretsofsongwriting.com/tag/first) (Secrets of Songwriting)
