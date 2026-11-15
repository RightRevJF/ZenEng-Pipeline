# Symbolic datasets of sung melodies (European, Anglo-American, English-language) for per-time-signature kept tables

Method note: Most dataset hosts outside GitHub were blocked from this session (kern.ccarh.org, liederenbank.nl, esavelmat.jyu.fi, jyu.fi, vwml.org, abc.sourceforge.net, musow, openhymnal.org all returned proxy 403 or not-allowlisted). GitHub repos could be shallow-cloned, so wherever a repo was cloned on 2026-11-15 the counts below were **computed directly from the files by this researcher** (time signatures from `*M` in **kern, `<sigN>/<sigD>` in MuseScore, `<beats>/<beat-type>` in MusicXML, `M:` in ABC; lyrics from `**text`/`**silbe` spines, `<Lyrics>`, `<lyric>`, `w:` lines). "First meter" = opening time signature; "any meter" = tunes containing that signature anywhere (mixed-meter tunes counted once per signature). Counts of this kind are marked "(counted)".

## 1. Ranked inventory (for a songwriting engine needing compound/odd metres and English syllable-aligned lyrics)

### Takeaway
No single open dataset gives large numbers of sung, lyric-aligned melodies in 9/8, 12/8, 5/4, 5/8 or 7/8. The best combination is: OpenScore Lieder (CC0, per-note lyrics, 297 English songs, real 6/8, 9/8 and 12/8 counts), Essen (largest 6/8 and 3/8 folk pool, no lyrics, restrictive CCARH licence), the Finnish Folk Tunes (the only big source of 5/4, plus some 5/8, 7/8, 9/8, 15/8; non-commercial, no lyrics), and PDMX (CC BY 4.0, 250k MusicXML with a lyrics flag) for scale. The Session's data now carries an explicit ban on LLM use.

### Cited Findings
Ranked table (verified status as of 2026-11-15):

| Rank | Dataset | Sung? | Tunes | Key non-4/4 counts | Lyrics aligned to notes? | Format | Licence | Location (verified?) |
|---|---|---|---|---|---|---|---|---|
| 1 | OpenScore Lieder | Sung (art song, voice+piano) | 1,352 .mscx / 1,462 .mxl (corpus.yaml says 1,454 scores) | any: 6/8 247, 3/8 63, 9/8 50, 12/8 30, 6/4 28, 3/2 25, 5/4 4, 7/8 3, 5/8 1, 15/8 1 | Yes, 1,351 of 1,352 scores have per-note `<Lyrics>`; 335 EN, 776 DE, 319 FR | MuseScore (.mscx/.mscz), MusicXML (.mxl), lyrics .txt, harmony .rntxt | CC0 1.0 | github.com/OpenScore/Lieder (cloned) |
| 2 | Essen Folksong Collection (full **kern) | Sung folk songs (melody only) | 8,473 (6,213 in `europa/`) | Europe any: 6/8 814, 3/8 321, 6/4 132, 3/2 137, 9/8 6, 5/4 4, 7/8 1, 5/8 1 | No (0 files with **text) | **kern | CCARH licence: academic research, single-user, no derivative commercial editions | github.com/ccarh/essen-folksong-collection (cloned) |
| 3 | Digital Archive of Finnish Folk Tunes | Mostly sung (Krohn's Suomen Kansan Sävelmiä) | 8,613 | any: 5/4 499 (409 pure 5/4), 6/8 304, 3/8 238, 5/8 63, 5/2 61, 9/8 24, 15/8 24, 7/8 14, 12/8 6, plus additive signatures such as 2+2+3/8 | No (lyrics only in online previews) | MIDI (and Matlab) | Non-commercial research, attribution | esavelmat.jyu.fi (could not reach; download page found via search) |
| 4 | Meertens Tune Collections (MTC-FS-INST 2.0, MTC-ANN 2.0.1) | Mostly sung Dutch songs (FS) plus instrumental (INST) | c. 18,000 (FS-INST); 360 (ANN) | not counted | MTCFeatures has lyric-derived per-note features (lyrics, wordstress, phoneme, wordend, noncontentword) | **kern and MIDI; feature JSON | Features CC BY-NC-SA 3.0 | liederenbank.nl/mtc (blocked here); github.com/pvankranenburg/MTCFeatures (cloned) |
| 5 | PDMX | Mixed (MuseScore user scores) | 254,077; 222,856 "no_license_conflict" | not reported | `has_lyrics` / `n_lyrics` flag; lyrics in MusicXML | MusicXML, MIDI, MusicRender JSON, PDF | CC BY 4.0 (Zenodo v9) | zenodo.org/records/15571083 (verified) |
| 6 | OpenEWLD | Sung lead sheets (popular/jazz standards, public domain) | 502 | 6/8 13, 12/8 1, 6/4 1, 3/2 1 | Yes, 464 of 502 have `<lyric>` | MusicXML (.mxl) + lyrics .txt | MIT (repo) | github.com/00sapo/OpenEWLD, DOI 10.5281/zenodo.4332855 (cloned) |
| 7 | Creighton, Songs and Ballads from Nova Scotia | Sung (English-language ballads) | 152 | 6/8 51, 6/4 1, 3/8 1, 5/4 1, 7/4 1 | No | **kern | Not stated | github.com/craigsapp/creighton-nova-scotia (cloned) |
| 8 | Open Hymnal | Sung hymns (SATB) | c. 305 .abc files (Choir + Complete folders, overlapping) | 6/4 9, 3/2 5, 6/8 4, 8/4 2, 9/4 1 | Yes, 212 files have `w:` lines | ABC (+ some MIDI) | Not stated in repo | github.com/mzealey/openhymnal (cloned); HF noahtye/openhymnal |
| 9 | Child Ballads (Bronson selection) | Sung | 38 | 6/8 4, 6/4 3, 5/4 2, 9/8 1 | No | **kern | Unknown | github.com/humdrum-tools/child-ballads (cloned) |
| 10 | Erk, Deutscher Liederschatz | Sung, with piano | 232 | 6/8 28, 3/8 18, 9/8 1, 5/4 1 | Only 2 files have **text | **kern | Not stated | github.com/craigsapp/erk-liederschatz (cloned) |
| 11 | Yu et al. lyrics-melody (LMD-derived) | Sung English pop melodies | c. 7,500 (LMD-full) and c. 11,600 (LMD+Reddit) .npy | none (no bar or time signature info) | Yes, syllable-aligned | NumPy arrays | Not stated; lyrics copyrighted | github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation (cloned) |
| 12 | Sacred Harp datasets | Metadata only (no notes) | 554 (1991 ed.), 590 (2025 ed.) | 2025: 6/4 45, 6/8 23, 3/2 23 | Lyrics text + poetic meter, not aligned | CSV/JSON/XLSX | Not stated | github.com/edjw/Sacred-Harp-datasets (cloned) |
| 13 | DALI | Audio-aligned vocal notes (not scores) | (see repo) | none | Yes (audio-time-aligned) | gz annotations | CC BY-NC-SA 4.0 | github.com/gabolsgabs/DALI (cloned) |
| 14 | HookTheory (Sheet Sage release) | Pop melody + chords | c. 22k segments / 13k recordings | not stated | Lyrics not stated | JSON | CC BY-NC-SA 3.0 | via github.com/chrisdonahue/sheetsage |
| — | The Session data | Instrumental dance tunes | (not counted, see §8) | — | No | ABC in CSV/JSON/SQLite | ODbL plus a clause banning LLM use | github.com/adactio/TheSession-data |

Supporting citations for each row are in the sections below.

### Inferences
- For 9/8 and 12/8 *with lyrics*, OpenScore Lieder is the only verified open source with dozens of examples (50 and 30 scores). For 5/4, 5/8 and 7/8 the Finnish archive is by far the biggest pool, but it has no lyrics and a non-commercial licence.
- 3/8 and 6/8 are well covered (Essen Europe has about 1,100 songs in those metres; Creighton has 51 English-language 6/8 ballads).
- For English syllable-aligned tables, the realistic stack is OpenScore Lieder EN (297 matched scores), OpenEWLD (464 with lyrics), Open Hymnal (212 with `w:` lines), and a filtered PDMX subset (`has_lyrics` true, CC0/PD, rated or deduplicated). Yu et al. is aligned, but it has no metre, so it cannot feed per-time-signature tables.

### Gaps
- Licence status of Creighton, Child Ballads (Bronson) and Erk repos is not stated in the READMEs read.
- PDMX time-signature distribution was not computed (14.4 GB archive not downloaded).

## 2. KernScores: full Essen, Densmore, other folk collections

### Takeaway
The full Essen collection (8,473 kern files) is now on GitHub as `ccarh/essen-folksong-collection`, updated November 2026. It has no lyrics and a restrictive CCARH licence. KernScores' current host is kernscores.stanford.edu, which lists 10,356 monophonic songs, including Densmore (373), Creighton (152), Friuli (80), British children's songs (53), Stephen Foster (38) and Schubert songs (35).

### Cited Findings
- GitHub repo "ccarh/essen-folksong-collection: The Essen Folksong Collection in the Humdrum format", last updated 2026-11-04 — [GitHub search result](https://github.com/ccarh/essen-folksong-collection)
- (counted) 8,473 .krn files. Region folders: Germany sub-collections (erk 1,700, boehme 704, ballad 687, zuccal 616, fink 566, altdeu1/2 309/316, kinder 213, allerkbd 110, dva 106), China (han 1,223, shanxi 802, natmin 206), plus europa/jugoslav 115, oesterrh 104, schweiz 93, elsass 91, nederlan 85, lothring 71, magyar 45, czech 43, rossiya 37, romania 28, polska 25, france 14, ukraina 13, sverige 11, danmark 9, italia 8, luxembrg 8, england 4 — [ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)
- (counted) All 8,473 files, first meter: 2/4 3,016; 4/4 1,838; 3/4 1,508; 6/8 805; 3/8 336; 4/2 239; free/X 202; 6/4 123; 3/2 115; 5/4 11; 5/8 8; 9/8 4; 7/8 3. 732 files are mixed-meter. — [ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)
- (counted) Europe only (6,213 files), any meter: 4/4 1,697; 2/4 1,392; 3/4 1,356; 6/8 814; 3/8 321; 4/2 308; X 150; 3/2 137; 6/2 135; 6/4 132; 9/8 6; 5/4 4; 7/8 1; 5/8 1; no 12/8. Most 5/4, 5/8 and 7/8 Essen items are in the Chinese subsets. — [ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)
- (counted) 0 of 8,473 files contain a **text or **silbe spine, so no lyrics in this kern release — [ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)
- README: "a database of some 6,255 folksong transcriptions… primarily of folksongs from Germany (5,370)…". This is the older European figure; the repo also holds the Chinese sets. — [README.txt in repo](https://github.com/ccarh/essen-folksong-collection)
- license.txt is the CCARH MuseData licence: "for personal use (single-user) only", "only for the purpose of academic research", no "derivative editions intended for commercial distribution", CCARH must be acknowledged — [license.txt in repo](https://github.com/ccarh/essen-folksong-collection)
- KernScores data page: Essen 8,473 (Germany 5,365; China 2,246; other Europe 848); Densmore 373 (Sioux 245, Pawnee 86, Chippewa 42); Creighton 152; Friuli 80; pentatonic songs 67; British children's songs 53; Stephen Foster 38; Schubert 35; Gershwin 29; total 10,356 monophonic songs. Lyrics and licence are not stated there. — [KernScores data highlights](https://kernscores.stanford.edu/help/data)
- Densmore Teton Sioux is also on GitHub as craigsapp/densmore-teton-sioux — [GitHub search, user craigsapp](https://github.com/craigsapp/densmore-teton-sioux)
- CCARH Ojibway (Densmore) page — [CCARH publications](https://www.ccarh.org/publications/data/humdrum/ojibway)
- The Catafolk catalogue indexes kern corpora including bronson-child-ballads, creighton-nova-scotia, densmore-* (10 tribes), erk-deutscher-liederhort, boehme-*, haydn-scottish-songs (51, kern), sagrillo-ireland (62, kern, "no lyrics"), sagrillo-luxembourg, pinck-verklingende-weisen, and the Essen China sets — [bacor/catafolk-registry](https://github.com/bacor/catafolk-registry); [Catafolk site](https://bacor.github.io/catafolk/datasets/finnish-folk-tunes/0.0.0)

### Inferences
- The GitHub Essen is the complete KernScores set (8,473 files). That is almost certainly larger than music21's bundled Essen subset, but music21's count was not verified.
- Because the CCARH licence is personal/academic only, kept tables derived from Essen should be treated as internal statistics. Do not redistribute the melodies, and get CCARH clearance before any commercial use.
- Densmore songs are Native American, outside the European/Anglo-American brief. They are useful only for irregular-metre statistics.

### Gaps
- Whether the original EsAC Essen files (the Schaffrath database) carry song texts for the German songs could not be checked, because the EsAC sources were not reachable.
- KernScores' Stephen Foster, British children's songs and Schubert sets may encode lyrics, but kern.ccarh.org and kernscores.stanford.edu bulk download could not be tested from this session.

## 3. Meertens Tune Collections (Dutch)

### Takeaway
MTC-FS-INST 2.0 (c. 18,000 Dutch melodies) and MTC-ANN 2.0.1 (360 annotated) are distributed as **kern and MIDI from liederenbank.nl/mtc. The MTCFeatures Python package (CC BY-NC-SA 3.0) exposes per-note lyric features. The primary site could not be reached to confirm counts by metre.

### Cited Findings
- "The melodies are provided in Humdrum **kern encoding and as MIDI sequences"; datasets: "MTC-ANN-2.0.1 - A small set of 360 richly annotated melodies from Dutch sources. MTC-FS-INST-2.0 - A large set of c. 18 thousand melodies from Dutch sources. ESSEN Folksong Collection - …over 8 thousand" — [MTCFeatures README](https://github.com/pvankranenburg/MTCFeatures); [MTCFeatures docs](https://pvankranenburg.github.io/MTCFeatures/introduction.html)
- LICENCE_Data: feature sets for MTC-ANN-2.0.1 and MTC-FSINST-2.0 are "licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License… Based on a work at http://www.liederenbank.nl/mtc" — [MTCFeatures LICENCE_Data](https://github.com/pvankranenburg/MTCFeatures)
- (counted, documentation grep) The MTCFeatures docs reference the features `lyrics`, `wordstress`, `phoneme`, `wordend`, `noncontentword` and `timesignature` — [MTCFeatures docsrc](https://github.com/pvankranenburg/MTCFeatures)
- Zenodo record "Melodic Features for Meertens Tune Collections and ESSEN Folksong Collection", v1.1, 22 Nov 2019 — [Zenodo 3551003](https://zenodo.org/records/3551003)
- MTC-ANN paper record — [Utrecht DSpace](https://dspace.library.uu.nl/handle/1874/346322)
- Official site — [liederenbank.nl/mtc](https://www.liederenbank.nl/mtc/) (not reachable from this session; listed in search results)

### Inferences
- The lyric features make MTC the only large European folk-song set found here with note-level text information (Dutch, not English). That suits syllable-stress modelling, but not English tables.

### Gaps
- Exact split of vocal vs instrumental in MTC-FS-INST, time-signature counts, and the licence on the raw **kern/MIDI files (as opposed to the features) were not verified, because liederenbank.nl was blocked.

## 4. Finnish Folk Tunes (Suomen Kansan Sävelmät)

### Takeaway
The Digital Archive of Finnish Folk Tunes (Eerola & Toiviainen 2004) has 8,613 tunes in MIDI. Per Catafolk's index, 499 contain 5/4 (409 entirely in 5/4, the Kalevala-type metre), with 63 in 5/8, 14 in 7/8, 24 in 9/8 and 24 in 15/8. It is research-only and non-commercial, with no lyrics in the dataset.

### Cited Findings
- 8,613 tunes, "mostly collected in the 19th century and published in Ilmari Krohn's Suomen Kansan Sävelmiä"; format MIDI (Matlab); non-commercial; copyright of the original collection is held by the Finnish Literary Society and of the digital collection by Eerola & Toiviainen; lyrics appear in online previews but not in the dataset — [Catafolk: finnish-folk-tunes](https://bacor.github.io/catafolk/datasets/finnish-folk-tunes/0.0.0)
- Download page: database "available for research purposes (that is, noncommercial)", attribution required; no direct file links visible to the fetcher — [esavelmat collection download](https://esavelmat.jyu.fi/collection_download.html)
- Other entry points: [Digital archive of Finnish Folk Tunes (English)](https://esavelmat.jyu.fi/index_en.html); [JYU materials for computational music research](https://www.jyu.fi/hytk/fi/laitokset/mutku/en/research/materials); a LINDAT catalogue entry also lists it — [LINDAT LRT-823](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-823?show=full)
- (counted from Catafolk index.csv, 8,613 rows, "meters" column) Any meter: 2/4 4,038; 4/4 2,351; 3/4 1,371; 5/4 499; 6/8 304; 3/8 238; 3/2 164; 2/8 92; 6/4 89; 5/8 63; 5/2 61; 9/8 24; 15/8 24; 7/8 14; 12/8 6; additive signatures 2+2+3/8 (6), 3+2+2/8 (5), 3+4/8 (5), 3+3+2/8 (4), 2+3+2/8 (2), 11/8 (2). Pure 5/4 tunes: 409. — [bacor/catafolk (old/datasets/finnish-folk-tunes/index.csv)](https://github.com/bacor/catafolk)

### Inferences
- This is the single best source for 5/4 and a useful source for 5/8 and 7/8 asymmetric groupings. The additive signatures even give explicit beat-grouping labels. MIDI lacks bar lines, so the Catafolk/index metadata is needed to assign metre.

### Gaps
- Direct MIDI archive URL was not confirmed (jyu.fi blocked; the fetched download page showed no file links). Whether the MIDI Toolbox distribution still bundles the collection is unverified.

## 5. Hymns and shape-note (Sacred Harp, Open Hymnal, Hymnary)

### Takeaway
No open symbolic (note-level) Sacred Harp corpus was found. The open Sacred Harp datasets are metadata plus lyrics with time signatures. Open Hymnal gives about 300 ABC hymns, 212 with `w:` lyric lines, mostly 4/4 and 3/4.

### Cited Findings
- edjw/Sacred-Harp-datasets: CSV/JSON (+ XLSX for 2025) with song number, title, composer, dates, poet, "poetic meter", "lyrics", "time signature". No note data. — [edjw/Sacred-Harp-datasets README](https://github.com/edjw/Sacred-Harp-datasets)
- (counted) 1991 edition 554 rows: 4/4 314, 2/4 76, 6/4 48, 3/4 41, 6/8 27, 3/2 21, 2/2 10, "Multiple" 8. 2025 edition 590 rows: 4/4 353, 2/4 82, 6/4 45, 3/4 41, 6/8 23, 3/2 23, 2/2 9, "Multiple" 7 — [edjw/Sacred-Harp-datasets](https://github.com/edjw/Sacred-Harp-datasets)
- Sacred-Harp-Publishing-Company/2025-edition: "Texts and Metadata for the 2025 Edition of the Sacred Harp" (updated 2026-11-09) — [GitHub](https://github.com/Sacred-Harp-Publishing-Company/2025-edition)
- Open Hymnal mirror: "clone of all the data that is found on the Open Hymnal project (http://openhymnal.org/)"; the project's aim is "a freely distributable, downloadable database of Christian hymns" — [mzealey/openhymnal](https://github.com/mzealey/openhymnal)
- (counted) 305 .abc files across Choir/ and Complete/ folders (likely duplicates across folders); M: values 4/4 ~139, 3/4 ~34, 6/4 9, 3/2 5, 2/4 5, 6/8 4, 2/2 3, 8/4 2, 9/4 1, none ~9; 212 files contain `w:` (note-aligned lyric) lines; no LICENSE file in repo — [mzealey/openhymnal](https://github.com/mzealey/openhymnal)
- Hugging Face copy: [noahtye/openhymnal](https://huggingface.co/datasets/noahtye/openhymnal)
- Distributed Proofreaders "English Hymnal – Wiki Music Experiment" has ABC transcriptions — [pgdp.net](https://www.pgdp.net/wiki/The_English_Hymnal_-_Wiki_Music_Experiment/ABC)
- hymnary.org responded HTTP 200 from this session — [hymnary.org](https://hymnary.org/)

### Inferences
- Sacred Harp CSVs can serve as priors (metre vs poetic meter vs text) but not as melodic tables. Their 6/4 and 3/2 share (~11% combined) is distinctive and worth noting for the engine.
- Open Hymnal plus English Hymnal ABC is the most practical open source of English hymn melodies with aligned `w:` lyrics. Hymn texts and tunes are mostly public domain, but the Open Hymnal repo carries no explicit licence.

### Gaps
- Hymnary.org bulk MusicXML/ABC export terms were not investigated. CCEL hymnal symbolic data not found.
- No note-level Sacred Harp corpus (kern/MusicXML) was found on GitHub search ("sacred harp" returned only minutes, apps and metadata repos).

## 6. German/European art song with lyrics: OpenScore Lieder

### Takeaway
OpenScore Lieder is CC0, with 1,352 MuseScore files (1,462 MXL). Nearly all have per-note lyrics: 776 German, 335 English and 319 French by metadata. Of the matched English scores (297), 49 contain 6/8, 12 contain 9/8, 5 contain 12/8, 13 contain 3/8, 3 contain 7/8 and 2 contain 5/4.

### Cited Findings
- "Collection of songs by 19th century composers in MuseScore format with associated data", mirror of musescore.com/openscore-lieder-corpus; can be batch-converted to MusicXML/MIDI with `mscore -j corpus_conversion.json` — [OpenScore/Lieder README](https://github.com/OpenScore/Lieder)
- LICENSE.txt is "CC0 1.0 Universal" — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)
- data/corpus.yaml: 143 composers (82 male, 61 female), 316 sets, 1,454 scores — [OpenScore/Lieder data](https://github.com/OpenScore/Lieder)
- (counted) Files: 1,352 .mscx, 1,462 .mscz, 1,462 .mxl, 1,355 .txt (lyrics), 1,156 .rntxt (Roman-numeral analyses); 1,351 of 1,352 .mscx contain `<Lyrics>` — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)
- (counted) scores.yaml language tags: DE 776, EN 335, FR 319, PT 12, IT 10, SV 3, PL 2, ES 2 — [OpenScore/Lieder scores.yaml](https://github.com/OpenScore/Lieder)
- (counted) All scores, first meter: 4/4 421, 3/4 265, 2/4 237, 6/8 216, 2/2 58, 3/8 49, 9/8 33, 12/8 20, 6/4 18, 3/2 11, 7/8 2, 5/4 2. Any meter: 6/8 247, 3/8 63, 9/8 50, 12/8 30, 6/4 28, 3/2 25, 9/4 6, 5/4 4, 7/8 3, 5/8 1, 15/8 1, 9/16 1 — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)
- (counted, language-matched subset 1,304 of 1,461 entries) EN 297: 4/4 127, 3/4 75, 2/4 54, 6/8 49, 2/2 17, 3/8 13, 9/8 12, 3/2 10, 6/4 5, 12/8 5, 7/8 3, 5/4 2, 15/8 1. DE 707: 6/8 134, 3/8 35, 9/8 22, 12/8 13, 5/4 1. FR 280: 6/8 44, 9/8 11, 12/8 10, 3/8 12, 5/4 1 — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)

### Inferences
- These are art songs with piano accompaniment, so the vocal staff must be extracted (the staff carrying lyrics). Melodies are more chromatic and wider-ranged than folk song, so tables built from them should probably be weighted or kept separate from folk tables.
- The English subset (around 300) is Victorian/Edwardian parlour and art song, a good match for "English songs with syllable-aligned lyrics" in compound metres.

### Gaps
- Some 157 scores.yaml entries did not match a directory path with this researcher's crude parser, so the language breakdown is approximate.
- DCML's Schubert Winterreise and other Lieder datasets could not be checked (repo API blocked; not cloned).

## 7. English songs with aligned lyrics: lead sheets, pop, PDMX

### Takeaway
OpenEWLD (502 public-domain lead sheets, 464 with lyrics, MIT) and PDMX (CC BY 4.0, 254k MusicXML, 222,856 recommended "no_license_conflict" subset, with a lyrics flag) are the usable score-based sources. Yu et al.'s set is syllable-aligned but has no metre. DALI and HookTheory are audio-derived and non-commercial (CC BY-NC-SA).

### Cited Findings
- OpenEWLD: "a dataset extracted from EWLD containing only public domain scores. You can redistribuite this work as you want"; DOI 10.5281/zenodo.4332855; MIT License; README warns of a bug where its metadata "getTimeSignatures() returns '4/4' by default" — [00sapo/OpenEWLD](https://github.com/00sapo/OpenEWLD)
- (counted directly from MusicXML, not their metadata) 502 .mxl; 464 contain `<lyric>`; time signatures: 4/4 287, 2/2 94, 3/4 80, 2/4 17, 6/8 13, 3/2 1, 6/4 1, 12/8 1 — [00sapo/OpenEWLD](https://github.com/00sapo/OpenEWLD)
- PDMX v9 (1 June 2025) on Zenodo: CC BY 4.0; files data.tar.gz 2.2 GB, mxl.tar.gz 1.9 GB, mid.tar.gz 214 MB, PDMX.csv 225 MB, pdf 9.6 GB; 31,221 songs (12.29%) had a licence conflict between public and internal metadata, so the authors "recommend using the no_license_conflict subset" (222,856 songs); CSV has `has_lyrics`, `n_lyrics`, `genres` columns — [Zenodo 15571083](https://zenodo.org/records/15571083)
- PDMX paper: 254,077 MusicXML files; "over 10M lyric tokens"; deduplicated subset 102,635; rated subset 14,182; paper text is inconsistent (Table I says "CC-0 / Public Domain", introduction says CC-BY) — [arXiv 2409.10831v2](https://arxiv.org/html/2409.10831v2)
- Yu et al. repo: lyrics-melody dataset for "Conditional LSTM-GAN for Melody Generation from Lyrics" (ACM TOMCCAP 2021); paper at arXiv 1908.05551 — [yy1lab/Lyrics-Conditioned-Neural-Melody-Generation](https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation)
- (counted) lmd-full_MIDI_dataset: Syllable_Parsing 7,597 .npy, Word_Parsing 7,497, Sentence_Parsing 7,574; lmd-full_and_reddit_MIDI_dataset: syllable_level 11,678, word_level 11,528. Each note is stored as numeric values with pitch as frequency in Hz (e.g. 466.16 = B♭4). No bar or time-signature field. — [yy1lab repo](https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation)
- DALI: "a large Dataset of synchronised Audio, LyrIcs and vocal notes", ISMIR 2018; data as gz files with versions in the repo; licence CC BY-NC-SA 4.0 — [gabolsgabs/DALI](https://github.com/gabolsgabs/DALI)
- HookTheory dataset (Sheet Sage): about 22k segments from about 13k recordings, 50 h; melody onsets and pitches, chords, refined beat/downbeat alignment; JSON; CC BY-NC-SA 3.0; time signature and lyrics not described — [Donahue et al., arXiv 2212.01884](https://ar5iv.labs.arxiv.org/html/2212.01884)

### Inferences
- For English per-time-signature tables, OpenEWLD is clean but almost entirely duple/triple simple metre. PDMX is the only route to hundreds or thousands of English sung items in 6/8, 9/8 and 12/8, but it would need filtering (`has_lyrics`, `no_license_conflict`, rating, a language check on lyric text) and parsing of the MusicXML time signatures.
- DALI and HookTheory are non-commercial and lack score-level metre, so they are low value for kept metre tables.

### Gaps
- PDMX time-signature counts and the share of English-language lyrics were not computed.
- The full EWLD (non-open, about 5,000 lead sheets) access terms were not checked.

## 8. The Session (thesession.org) data dump

### Takeaway
The dump is instrumental Irish dance music (jigs 6/8, slip jigs 9/8, slides 12/8). Its LICENSE now forbids processing the material with large language models, apart from an accessibility exception. Because of that clause, this researcher deleted the clone without counting tune types.

### Cited Findings
- Repo contents: csv/ (aliases, events, recordings, sessions, sets, tune_popularity, tunes), json/, thesession.db; tunes.csv columns: tune_id, setting_id, name, type, meter, mode, abc, date, username, composer — [adactio/TheSession-data](https://github.com/adactio/TheSession-data)
- LICENSE.md: "Prohibition on LLM Use: You may not use, adapt, modify, or process the material in any way with Large Language Models. This includes but is not limited to training Large Language Models, utilizing LLM tools, or incorporating the material into any LLM-related applications or systems", with an accessibility exception. Database also references ODC ODbL. — [TheSession-data LICENSE.md](https://github.com/adactio/TheSession-data)

### Inferences
- An engine built or run with LLM tooling (ZenEng is built with Claude) should not ingest The Session data. The material is instrumental anyway. Nottingham Music Database (ABC, instrumental, many 6/8 jigs) would be an alternative, but it is also instrumental.

### Gaps
- Counts of slip jigs and slides were not computed, by choice (licence). Nottingham DB availability was not verified (abc.sourceforge.net blocked).

## 9. Other national and English sung collections (Bronson, VWML, Polish, Czech, Hungarian, Balkan, Irish sung)

### Takeaway
Beyond Essen's small national subsets, no open symbolic sung-melody corpora were found for Polish, Czech/Slovak, Greek, Bulgarian, Macedonian, Romanian or Irish sung song. The only digital Bronson material located is a 38-tune kern selection. VWML/EFDSS material is available piecemeal as ABC through Folkopedia's transcription programme, with no stated licence.

### Cited Findings
- humdrum-tools/child-ballads: "Selection from the Child Ballads", 38 kern files (counted); first meter 4/4 21, 3/4 7, 6/8 4, 6/4 3, 2/4 2, 3/2 1; any 5/4 2, 9/8 1; no lyrics — [humdrum-tools/child-ballads](https://github.com/humdrum-tools/child-ballads)
- Catafolk lists "Child Ballads" sourced from KernScores `/osu/monophony/british`, kern, licence "Unknown", 38 rows (counted) — [catafolk-registry bronson-child-ballads](https://github.com/bacor/catafolk-registry)
- Creighton Nova Scotia: "Digital edition of Songs and Ballads from Nova Scotia, collected by Helen Creighton (1932)"; 152 kern (counted), first meter 6/8 51, 3/4 44, 4/4 44, 2/4 11; no **text spines — [craigsapp/creighton-nova-scotia](https://github.com/craigsapp/creighton-nova-scotia)
- Erk Deutscher Liederschatz (1859–72, 3 vols × 200 songs with piano): 232 kern files (counted), 6/8 28, 3/8 18, 9/8 1, 5/4 1; only 2 files with **text; also in humdrum-tools/humdrum-data — [craigsapp/erk-liederschatz](https://github.com/craigsapp/erk-liederschatz)
- Essen national subsets (counted): jugoslav 115, magyar 45, czech 43, rossiya 37, romania 28, polska 25, ukraina 13, england 4 — [ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)
- ELTE Folk Song Corpus: 2,390 Hungarian folk songs as TEI XML texts with metre annotation (qualitative/quantitative) but no melodies — [ELTE-DH/folk-song-corpus](https://github.com/ELTE-DH/folk-song-corpus)
- SimFolk (Slovak folk song similarity thesis app, 2020), dataset status unclear — [MichalMizak/SimFolk](https://github.com/MichalMizak/SimFolk)
- Folkopedia Full English Transcription Programme (formerly Take 6): e.g. Vaughan Williams MS RVW2/2 with about 190 items, each with .abc, .mid, .pdf at `https://folkopedia.info/wiki/File:RVW2-2-[n].abc`; licence not stated; whether lyrics are included not stated — [Folkopedia RVW2/2](https://folkopedia.info/wiki/Full_English_Transcription_Programme:_The_Vaughan_Williams_Archive_at_the_British_Library,_MS_RVW2/2); related: [Take 6 Transcription Programme](https://folkopedia.info/wiki/Take_6_Transcription_Programme); [VWML Full English project](https://update.vwml.org/thefullenglishproject)
- Village Music Project (English social dance tune manuscripts in ABC, instrumental) — [VMP ABC protocol](https://www.village-music-project.org.uk/?p=17)

### Inferences
- English traditional *sung* 6/8 material is best sourced from Creighton (51) plus the Essen/Child kern selections, and potentially Folkopedia's VWML ABC files if their licence and lyric content are confirmed.
- Balkan asymmetric metres (7/8, 9/8 aksak) have no verified open symbolic sung corpus here. Finnish 5/8 and 7/8 and the small counts in Lieder and Essen are the only verified sources.

### Gaps
- No digital symbolic edition of Bronson's complete *Traditional Tunes of the Child Ballads* was found.
- Comhaltas, the Irish Traditional Music Archive and Greek/Bulgarian/Romanian sung transcription corpora were not found via GitHub search or this session's queries. The musow catalogue (projects.dharc.unibo.it/musow) was not reachable, though search results show it indexes hymnals (e.g. "Hymns and Carols of Christmas") — [musow entry](https://projects.dharc.unibo.it/musow/view-1635268063-599964).
- VWML main site (vwml.org) was blocked, so its own downloadable ABC/data offerings were not verified.
