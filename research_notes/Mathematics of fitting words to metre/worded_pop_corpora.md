# Worded pop corpora: datasets with syllables aligned to sung notes, and their 3/4, 6/8, 12/8 content (as of November 2026)

Scope note: documentation and papers only; no dataset was downloaded. Nothing from TheSession.org was used or is recommended. "Not published" means no count by metre was found in the documentation read. Items marked "(background knowledge, unverified this session)" were not confirmed against a source in this session and sit in Inferences or Gaps, not in Cited Findings.

## Ranking by usefulness for measuring stress-to-beat placement in 3/4 and 6/8 pop

### Takeaway
No dataset publishes a ready-made set of worded pop songs in 3/4 or 6/8, and every stress-annotated pop resource found (Rolling Stone 5x20, and the 4/4-only lyric-to-melody sets) deliberately excluded non-4/4 songs. The realistic route to "a few dozen to a few hundred" worded triple or compound pop songs is (1) karaoke-lyric MIDI in the Lakh MIDI Dataset, filtered on time-signature events, backed by (2) the 214 CoCoPops-Billboard melody-plus-lyric transcriptions, with DALI as a large but metre-less third option.

### Cited Findings
Ranked list (evidence for each row is in the sections below):

| Rank | Dataset | Words on notes? | Metre info? | Size | Licence | Triple/compound count |
|---|---|---|---|---|---|---|
| 1 | Lakh MIDI (lyric/karaoke-bearing files) | Syllable or word text events timed against notes | MIDI time-signature and tempo events | 176,581 files in LMD-full; about 8,000 to 8,500 with usable English lyrics in two independent studies | CC-BY 4.0 on the collection; underlying songs in copyright, authorship untraceable | Not published; count by reading time-signature events |
| 2 | CoCoPops-Billboard | **kern melody plus **silbe syllables | Humdrum barlines and metre interpretations | 214 songs with melody and lyrics (of 739 files) | CC BY 4.0 | Not published; count by reading metre records |
| 3 | DALI v1/v2 | Text per note, word, line, paragraph | None (times in seconds only) | 5,358 (v1), 7,756 (v2) | CC BY-NC-SA 4.0, research use, access by request | Not published; needs audio beat/downbeat tracking |
| 4 | Rolling Stone 5x20 stress set (Temperley; also in CoCoPops-RS) | Syllable per note with 4-level stress | Time signature column per syllable | 80 songs | No licence stated on source page; CC BY 4.0 as redistributed in CoCoPops | Zero by design (4/4 and 2/4 only) |
| 5 | MTC-FS-INST 2.0 / MTC-ANN (Dutch folk song) | Syllable per note, with wordstress | timesignature, beatstrength per note | about 18,000 / 360 melodies | CC BY-NC-SA 3.0 | Not published; trivially countable from the `timesignature` feature |
| 6 | OpenScore Lieder (art song) | Lyrics under notes in score | Notated | over 1,200 to 1,350 songs | CC0 | Not published; countable from scores |
| 7 | OpenEWLD / EWLD (already in the engine) | Lyrics in MusicXML where available | Notated, single time signature per score | not stated on repo page | MIT code; public-domain scores | DB `metric` field is buggy |
| 8 | Yu et al. lyrics-melody set; Melistas et al. set (both LMD-derived) | Syllable-note pairs | Bar position dropped (Yu); not reported (Melistas) | 7,998 / 8,505 files | none stated | Not recoverable from released triplets; go back to source MIDI |
| 9 | SongComposer data | Lyric-melody pairs | bpm only | 10K to 100K rows | Apache-2.0 | Not recoverable |
| 10 | SongGLM, TeleMelody, CSL-L2M data | yes | bar/position kept | 206,884 / 157,702 / 10,170 | none stated / not released | Zero by design (4/4 only) |
| none | Hooktheory/Sheet Sage, MulTTiPop | No lyrics | yes | — | CC BY-NC-SA 3.0 / none stated | n/a |

- Sources for the table rows: [Lakh page](https://colinraffel.com/projects/lmd/); [Yu et al.](https://arxiv.org/pdf/1908.05551); [Melistas et al.](https://preview.aclanthology.org/moar-dois/2021.nlp4musa-1.3.pdf); [CoCoPops paper](https://archives.ismir.net/ismir2023/paper/000027.pdf); [DALI repo](https://github.com/gabolsgabs/DALI); [DALI Zenodo](https://zenodo.org/records/2577915); [rock corpus stress page](https://rockcorpus.midside.com/lyrics_stress.html); [MTC](https://www.liederenbank.nl/mtc/); [MTCFeatures](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html); [OpenScore Lieder](https://github.com/OpenScore/Lieder); [OpenEWLD](https://github.com/00sapo/OpenEWLD); [SongComposer data card](https://huggingface.co/datasets/Mar2Ding/songcompose_data/blob/main/README.md); [SongGLM](https://arxiv.org/pdf/2412.18107); [TeleMelody](https://arxiv.org/pdf/2109.09617v1); [CSL-L2M](https://arxiv.org/pdf/2412.09887); [Sheet Sage repo](https://github.com/edychat/sheetsage).

### Inferences
- The ranking weighs four things: real pop repertoire, syllable-to-note alignment in symbolic time (bars and beats, not seconds), explicit metre, and enough non-4/4 material. Lakh karaoke MIDI is the only source that plausibly scores on all four at scale; CoCoPops-Billboard is cleaner and clearly licensed but small.
- Every research group that built a stress-aware or beat-aware lyric-melody corpus filtered to 4/4. The gap the engine has is therefore a gap in the field, not an oversight; a triple-metre worded pop table would be new work.
- Licence posture: for all pop sources the songs themselves are in copyright. Deriving aggregate statistics (stress-by-beat histograms) and storing only those statistics is a different act from redistributing the transcriptions; the notes below flag which datasets add a non-commercial clause on top. This is not legal advice.

### Gaps
- No source gives a count of 3/4, 6/8 or 12/8 songs for any pop dataset. All counts must be computed.

## DALI (Meseguer-Brocal et al., v1 and v2)

### Takeaway
DALI has the scale (5,358 then 7,756 songs) and note-level text, but its annotations are in seconds with no time signature, beat or downbeat, so metre must be recovered from the audio; it is non-commercial, research-only and request-gated.

### Cited Findings
- Sizes: 5,358 songs in version 1 and 7,756 in version 2. — [DALI paper page](https://alicecohenh.github.io/dali2.html)
- Origin: annotations come from open-source karaoke-game communities where non-expert users share text files, with "no further professional revision"; 13,339 annotation files were retrieved and 5,358 matched to audio for v1. — [DALI arXiv paper](https://arxiv.org/pdf/1906.10606)
- Content: each note is a triple of time (start and duration relative to a frame rate), musical note, and text; lyrics at four levels (notes, words, lines, paragraphs). In the released files each element has `text`, `time` (start and end in seconds) and `freq`; timing parameters `offset` and `fr` are stored per song. — [DALI arXiv paper](https://arxiv.org/pdf/1906.10606); [DALI GitHub](https://github.com/gabolsgabs/DALI)
- Beats, downbeats, time signature, BPM: not mentioned on the repository page, the paper, or the Zenodo record. — [DALI GitHub](https://github.com/gabolsgabs/DALI); [Zenodo](https://zenodo.org/records/2577915)
- Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0; "offered free of charge for non-commercial research use only", "for educational purposes only", not for commercial purposes without the copyright holders' permission; files are restricted and access requires a request stating affiliation and planned application. — [Zenodo](https://zenodo.org/records/2577915); [DALI GitHub](https://github.com/gabolsgabs/DALI)
- Audio is not distributed; each entry links to a YouTube URL with a working-link flag. A manually verified ground-truth subset of 105 songs exists for v1. — [DALI GitHub](https://github.com/gabolsgabs/DALI)
- Known problems: audio version may not match the annotation (live, remix); global offset and frame-rate errors (corrected by search, accuracy not reported); local errors (misaligned lyric blocks, misspellings, note mistakes) left uncorrected. — [DALI arXiv paper](https://arxiv.org/pdf/1906.10606); [DALI GitHub](https://github.com/gabolsgabs/DALI)

### Inferences
- Metre recovery options: (a) run a beat/downbeat tracker on the YouTube audio and map note onsets to beats; (b) because the source karaoke files express time in frames at a per-song rate `fr`, note onsets are quantised to a tempo grid, so beat positions (but not bar length) can be recovered without audio; bar length would then be guessed from onset-autocorrelation at 3 versus 4 beats. Both are error-prone for 6/8 versus 3/4 versus 12/8 shuffle. (Option b is my reading of the `fr` parameter, not something the DALI documents state.)
- The text unit at note level is whatever the karaoke author typed per note, usually a syllable, but it is not guaranteed to be linguistically syllabified.
- The no-AI question: no clause about machine learning or AI was found; the constraint is NC plus research-only plus gated access.

### Gaps
- No language or genre breakdown and no metre count were found. No DALI v2 additions for beats or downbeats were documented in the pages read.
- I did not find a separate "DALI v2 annotations" licence distinct from CC BY-NC-SA 4.0.

## Karaoke MIDI: the Lakh MIDI Dataset

### Takeaway
LMD is the largest reachable pool: 176,581 files, of which two independent papers extracted roughly 8,000 to 8,500 files with usable English lyrics aligned to melody notes. It carries time-signature information natively, but no one has published a count by metre, and the copyright position is unresolved by its CC-BY 4.0 label.

### Cited Findings
- Sizes: LMD-full 176,581 unique MIDI files (a few thousand probably corrupt); LMD-matched 45,129 files matched to Million Song Dataset entries; LMD-aligned is the matched set aligned to 7digital previews. — [Lakh MIDI page](https://colinraffel.com/projects/lmd/)
- Licence and copyright: "distributed with a CC-BY 4.0 license"; the compiler did not transcribe the files; MIDI Copyright meta-events are "not used consistently", so attributing files to authors is not feasible. — [Lakh MIDI page](https://colinraffel.com/projects/lmd/)
- The page notes that MIDI files in some cases include lyrics and can supply metre information such as beats and downbeats; it gives no count of lyric-bearing files and does not mention karaoke. — [Lakh MIDI page](https://colinraffel.com/projects/lmd/)
- Yu et al. found 7,998 LMD-full files with English lyrics (plus 4,199 from a Reddit MIDI collection, total 12,197 files, about 789 hours); alignment used timestamps in the MIDI tracks. — [Yu et al., Conditional LSTM-GAN](https://arxiv.org/pdf/1908.05551)
- Melistas et al. started from the 45,129 LMD-matched files and kept 8,505 valid tracks with English lyrics, assigning each lyric event to its closest note. — [Melistas et al. 2021](https://preview.aclanthology.org/moar-dois/2021.nlp4musa-1.3.pdf)
- A 2026 CMU dataset (MulTTiPop) matched LMD-matched MIDI to TheoryTab entries by title and artist: 572 segments, 374 unique songs. It has no lyric annotation, but shows LMD files can be joined to Hooktheory songs. — [MulTTiPop](https://huggingface.co/papers/2607.08756.md)

### Inferences
- How to count metre: parse each lyric-bearing file's time-signature meta events (numerator/denominator) and keep 3/4, 6/8, 9/8, 12/8, 6/4. Caveats (background knowledge, unverified this session): files with no time-signature event default to 4/4; hobbyist sequencers often left 4/4 in place for waltzes and wrote 12/8 shuffles as 4/4 with triplets, so a second test (onset distribution on a 3-fold versus 2-fold grid) is needed, and the true compound-metre count will exceed the naive event count.
- Text granularity (background knowledge): .kar files store text meta events, commonly one per syllable with "/" and "\" marking line and paragraph breaks; other files use the lyric meta event. Syllable splits follow the sequencer author, not a dictionary, so re-syllabify whole words against CMUdict before assigning stress.
- If even 2 to 5 percent of about 8,000 English lyric files are in triple or compound metre, that yields roughly 160 to 400 songs; this is an order-of-magnitude guess, not a measured figure. The Rolling Stone 5x20 exclusion rate (17 of 100 songs not in 4/4 or 2/4, see below) suggests the pop base rate is not negligible.
- Joining LMD-matched lyric files to the Hooktheory 3/4 and 6/8 TheoryTabs already in the engine (as MulTTiPop did) would put words on melodies the engine already trusts.
- Quality problems to expect (background knowledge): duplicate versions of the same song, melody track sometimes an instrumental "guide" with simplified rhythm, lyric events slightly early relative to notes, and quantisation that erases the anticipations real singers use.

### Gaps
- No published total for lyric-bearing files in LMD-full across all languages, and no published metre breakdown.
- I found no named, citable "Lakh MIDI karaoke" subset with its own licence; the two LMD-derived sets above are the nearest thing.
- The CC-BY 4.0 label covers the compiler's contribution; whether individual transcriptions infringe was not addressed by any source read.

## CoCoPops, the Rolling Stone corpus, and Temperley's stress annotations

### Takeaway
CoCoPops-Billboard gives 214 human-transcribed pop songs with melody and syllables under CC BY 4.0, the cleanest worded pop source; its metre mix is unpublished. The only stress-annotated pop set (80 Rolling Stone songs) was restricted to 4/4 and 2/4, and 17 of the 100 candidate songs were dropped for having other time signatures.

### Cited Findings
- CoCoPops-Billboard: 739 files with harmony, form, phrase and timestamps; 214 include melody (**kern) and lyric (**silbe) transcriptions and rhyme schemes; 100 of those have valence/arousal and RMS. — [CoCoPops ISMIR 2023 paper](https://archives.ismir.net/ismir2023/paper/000027.pdf)
- CoCoPops-RS200: melody and harmony for the 200-song Rolling Stone corpus, with lyrics and three-level stress for 80 songs. Whole corpus: 398 unique songs, 63,809 words (48,018 in Billboard), 145,822 note onsets (86,215 in Billboard). — [CoCoPops paper](https://archives.ismir.net/ismir2023/paper/000027.pdf)
- Format and licence: Humdrum files with spines including **kern, **silbe, **stress, **harm, **harte, **timestamp, **rhyme, **phrase; licence CC BY 4.0; hosted under the Computational-Cognitive-Musicology-Lab GitHub organisation, with YouTube links and MusicBrainz IDs for the 214-song subset. — [CoCoPops paper](https://archives.ismir.net/ismir2023/paper/000027.pdf)
- Repositories: CoCoPops-Billboard and CoCoPops-RollingStone under github.com/Computational-Cognitive-Musicology-Lab. — [CCML project page](https://ccml.gtcmt.gatech.edu/projects/CoCoPops.html)
- Metre: the paper mentions 4/4 and 12/8 only as an example of a corrected inconsistency and gives no counts by metre. — [CoCoPops paper](https://archives.ismir.net/ismir2023/paper/000027.pdf)
- Rolling Stone stress files: lyrics and stress for 80 songs, melisma transcriptions for 99 songs ("5x20": 20 top-ranked songs per decade, 1950s to 1990s). Each line is one syllable with time signature code (e.g. 404), onset in measures, pitch, scale degree, stress level (0 unstressed, 1 primary, 2 secondary, 3 non-word; function words forced to 0), and the word. The 80 were chosen because they use only 4/4 or 2/4. No licence is stated on the page. — [Rock corpus lyrics and stress page](https://rockcorpus.midside.com/lyrics_stress.html)
- Exclusions: of the 100 songs, 17 had time signatures other than 4/4 or 2/4 and 3 were rap, leaving 80. — [Tan, Lustig and Temperley 2019](https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf)
- White, Pater and Breen (2022) likewise kept only quadruple-metre songs from the RS 200 (192 of 200 kept; removals were for compound or triple metre or encoding errors, not broken down). — [White et al. 2022](https://par.nsf.gov/servlets/purl/10356498)

### Inferences
- The RS 5x20 melodic transcriptions for the 17 non-4/4 songs exist (melisma transcriptions cover 99 songs) but have no lyric or stress files. Adding lyrics to those 17 by hand, in the documented six-column format, is a small, well-defined job that would give a pilot triple/compound set matched in method to Temperley's 4/4 data.
- 17 percent non-4/4-or-2/4 among top-ranked rock songs, versus 8 of 200 removed by White et al., are inconsistent base rates; the difference is probably definitional (12/8 shuffles counted as non-4/4 in one and not the other), which is itself a warning about how 12/8 is encoded.
- To count metre in CoCoPops-Billboard: grep the Humdrum metre interpretation records (e.g. `*M3/4`, `*M6/8`, `*M12/8`) across the 214 melody files. With 214 songs sampled from Billboard charts 1958 to 1991, expect perhaps one to three dozen compound or triple songs; this is a guess to be replaced by the grep.
- Stress is not annotated in the Billboard subset; it can be added with CMUdict using Temperley's rule (function words forced to 0) for comparability.

### Gaps
- GitHub README and LICENSE pages for the two CoCoPops repositories could not be fetched in this session; current file counts after 2023 are unverified.
- Whether "The Musical Language of Rock" itself tabulates stress by beat for non-4/4 songs was not established; the review found does not say.

## Other symbolic sources (folk, art song, lead sheets, hymns, MIR sets)

### Takeaway
Outside pop, MTC is the best-instrumented resource (per-note word stress and beat strength on about 18,000 Dutch melodies) and OpenScore Lieder is the freest (CC0), but neither is pop or English. Hooktheory data carries no lyrics, and the common MIR melody sets either lack lyrics or lack metre.

### Cited Findings
- MTC collections and sizes: MTC-ANN 2.0.1, 360 melodies; MTC-FS 1.0, 4,120 vocal folk songs; MTC-FS-INST 2.0, 18,618 pieces (instrumental and vocal); MTC-LC 1.0, 4,830; MTC-INST 1.0, 2,368. Formats include **kern, MIDI, LilyPond. All under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported; download via a form at liederenbank.nl/mtc. — [Meertens Tune Collections](https://www.liederenbank.nl/mtc/)
- MTCFeatures per-note fields for vocal melodies: `lyrics` (syllable with hyphen continuation), `wordstress` (whether the syllable is stressed), `noncontentword` (Dutch function word), `wordend`, `phoneme`, `rhymes`, `melismastate`; metre fields `timesignature`, `beatstrength` (music21 metric weight), `beat`, `beat_str`, `beat_fraction_str`, `imaweight`. Lyric features sit on the first note of a melisma. Essen melodies have no lyric features. — [MTCFeatures melody representation](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html)
- Melodies marked "Mixed meters" are treated as free metre because metre changes are often not exactly indicated. — [MTCFeatures introduction](https://pvankranenburg.github.io/MTCFeatures/introduction.html)
- OpenScore Lieder: released under CC0; described as "over 1,200 nineteenth century songs" by over 100 composers in a range of languages; MuseScore source files convertible in bulk to MusicXML; `scores.tsv` metadata; Zenodo DOI 10.5281/zenodo.15450143. A MuseScore announcement gives "over 1350" scores. — [OpenScore Lieder GitHub](https://github.com/OpenScore/Lieder); [MuseScore announcement](https://musescore.org/en/node/325308)
- OpenEWLD: public-domain subset of the Enhanced Wikifonia Leadsheet Dataset; compressed MusicXML lead sheets with chord symbols and lyrics where available; at most one time signature per score; only triplets allowed; single voice. The SQLite `features.metric` field is affected by a bug where 4/4 may appear incorrectly. Code under MIT; secondhandsongs metadata CC BY-NC 3.0. Full EWLD must be rebuilt from the old Wikifonia archive. — [OpenEWLD GitHub](https://github.com/00sapo/OpenEWLD)
- Hooktheory/TheoryTab: staff state "Bands, lyrics, and polyphony (multiple voice) are not allowed inside the theorytab part of the site", and the lyrics control was removed intentionally. — [Hooktheory forum](https://forum.hooktheory.com/t/lyrics-button-is-gone/3463)
- Sheet Sage Hooktheory dump: 50 hours of aligned melody and harmony annotations, CC BY-NC-SA 3.0, no audio; lyrics are not among the described fields. — [Sheet Sage GitHub](https://github.com/edychat/sheetsage)
- MulTTiPop (2026): multitrack MIDI with beat alignment for 374 songs; no lyric annotation; authors ask that it be used for evaluation, not training. — [MulTTiPop](https://huggingface.co/papers/2607.08756.md)

### Inferences
- MTC is the one place where a stress-by-beat-strength table for 3/4 and 6/8 song can be computed in a few lines today (filter `timesignature`, cross `wordstress` with `beatstrength`). It is Dutch folk song, so it gives a method template and a Germanic-language baseline, not pop evidence. Its NC-SA licence matters if the engine is ever commercial.
- For OpenEWLD, do not trust the database metric column; read the time signature from each MusicXML file.
- OpenScore Lieder is mostly German and French; English-language share is small, so it is a weak proxy for English stress placement. It is, however, the only CC0 source.
- Background knowledge, unverified this session: POP909 (909 Chinese pop songs, MIDI with beat annotations) has no lyrics; MIR-ST500 has vocal note transcriptions without lyrics; NUS-48E is 48 sung and spoken recordings of 20 English songs with phone-level labels but no score or metre; the Weimar Jazz Database is instrumental solos; SALAMI is structural annotation only; the Nottingham set is instrumental folk tunes with chords; Song Describer and MusicNet have no aligned lyrics. None of these helps.
- Hymn sources (background knowledge, unverified): Hymnary.org indexes texts and tunes with syllabic metre strings (8.6.8.6 and so on), which describe syllable counts per line, not time signature; public-domain hymnals engraved in open formats (e.g. the Open Hymnal project) would give syllable-under-note data in 3/4 and 6/4, but they are hymns, not pop, and Hymnary's own terms would need checking before any bulk use.

### Gaps
- Counts by metre: not published for MTC, OpenScore Lieder or OpenEWLD in the pages read.
- Number of MTC vocal melodies with lyrics is not stated on the pages read (MTC-FS has 4,120 vocal songs).
- Hymnary.org licence and bulk-download terms were not found; LyricFind, Musixmatch and Songle alignment data were not researched to a citable level (background knowledge: these are commercial or audio-time alignments at line or word level, without notes or metre).

## Lyric-to-melody generation datasets, 2019 to 2026, and whether they keep bar and beat

### Takeaway
The generation literature offers large paired sets, but each one either discards bar positions (Yu et al., SongComposer) or filters to 4/4 (SongGLM, TeleMelody, CSL-L2M). None can supply triple-metre evidence as released.

### Cited Findings
- Yu et al.: 12,197 MIDI files; paired training data from the 7,998 LMD-full files; only one-syllable-to-one-note pairs; each note stored as pitch, note duration, rest duration; 13,251 sequences of 20 notes, 265,020 syllable-note pairs; released on GitHub (yy1lab/Lyrics-Conditioned-Neural-Melody-Generation); no licence given; bar or beat position not stated as preserved. — [Yu et al.](https://arxiv.org/pdf/1908.05551)
- Melistas et al.: 8,505 LMD-matched tracks with English lyrics; syllables via Phonetisaurus; multi-note syllables keep the first note plus extension symbols; time signature not reported; code and data at github.com/gulnazaki/lyrics-melody; no licence stated. — [Melistas et al.](https://preview.aclanthology.org/moar-dois/2021.nlp4musa-1.3.pdf)
- SongComposer data (Hugging Face Mar2Ding/songcompose_data): unpaired lyrics, unpaired melodies, and aligned pairs with note durations, rest durations and bpm; English and Chinese; Apache-2.0; no bar, beat or time-signature field. — [SongComposer data card](https://huggingface.co/datasets/Mar2Ding/songcompose_data/blob/main/README.md)
- SongGLM: 206,884 English MIDI songs built from about 1.6 million MelodyNet MIDI files; bar and position kept per note; CMUdict stress used; only 4/4 melodies extracted; release and licence not stated. — [SongGLM](https://arxiv.org/pdf/2412.18107)
- TeleMelody: template-melody data from LMD-matched (157,702 samples); English lyric-rhythm data 9,761 samples from forced-aligned audio; only constant-tempo 4/4; notes encoded with bar index and 1/16 position. — [TeleMelody](https://arxiv.org/pdf/2109.09617v1)
- CSL-L2M: 10,170 Chinese pop songs, 4/4 only, REMI-style representation; public release not stated. — [CSL-L2M](https://arxiv.org/pdf/2412.09887)

### Inferences
- The Yu et al. triplets could in principle be re-barred by cumulative duration, but the 20-note excerpts start at arbitrary points and have no time signature, so they are unsuitable for stress-on-beat work. Their value is as an index of which LMD files have English lyrics.
- SongGLM's pipeline (CMUdict stress, bar and position tokens, word-to-nearest-note alignment) is exactly the pipeline needed; rerunning it without the 4/4 filter on lyric-bearing MIDI is the practical recipe.
- MelodyNet's roughly 1.6 million MIDI files imply a far larger lyric-bearing pool than LMD, but it comes from the WuYun/MelodyGLM line of work and I did not verify its availability or licence.

### Gaps
- SongMASS, ROC ("Re-creation of Creations"), and WuYun data details were not fetched; background knowledge is that they follow the same 4/4 convention, unverified.
- No 2025 to 2026 dataset was found that explicitly includes or reports 3/4 or 6/8 lyric-melody pairs.

## Published stress-to-beat statistics usable directly

### Takeaway
Two usable sets of numbers exist: Tan, Lustig and Temperley's 4/4 rock figures (a third of stressed syllables syncopated, three quarters of those anticipatory), and one small score-based study that gives a 3/4 versus 4/4 split (stress matching 0.508 in 3/4 against 0.657 in 4/4). Nothing was found for 6/8 or 12/8.

### Cited Findings
- Rock, 4/4, 80 songs, 23,032 notes: stress distribution primary 43.5%, secondary 1.8%, unstressed 50.3%, non-word 4.4%; function words 31% of word tokens. — [Tan, Lustig and Temperley 2019](https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf)
- Same study: eighth-note-level syncopation quotient .228 (2,382 of 10,433 stressed syllables); sixteenth-level .105; combined .333; anticipatory share .772 at eighth level, .762 combined. Syncopation tendency by shift: beat 3 anticipated (5 to 4) .554, beat 1 anticipated (1 to 8) .504, 3 to 2 .439, 7 to 6 .351. Comparison set of 10 nineteenth-century English songs (1,397 notes) has zero syncopated stressed syllables out of 602. — [Tan, Lustig and Temperley 2019](https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf)
- Same study: syncopation at the eighth level rises with tempo and with year; data public at rockcorpus.midside.com. — [Tan, Lustig and Temperley 2019](https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf)
- "Relationships between Keywords and Strong Beats in Lyrical Music": 56 songs from piano books, 26 in 3/4 and 30 in 4/4 (1,492 syllables in 3/4, 2,024 in 4/4); 59.9% of stressed syllables on strong beats overall; syllable stress matching 0.594 overall, 0.508 in 3/4, 0.657 in 4/4; keyword stress matching 0.796 overall, 0.711 in 3/4, 0.855 in 4/4. The paper's own figures conflict in places (80.8% versus 76.8% of keywords on strong beats). — [arXiv 2412.04202](https://arxiv.org/html/2412.04202v1)
- White, Pater and Breen report onset (not stress) profiles for 4/4 only: post-2015 melodies have about 6.75 events per bar against 4.29 and more offbeat sixteenths. — [White et al. 2022](https://par.nsf.gov/servlets/purl/10356498)

### Inferences
- The 3/4 figure of about 0.51 from the keywords paper comes from piano-book songs with a coarse strong/weak beat coding, so it understates fit if beat 1 alone is "strong" and beats 2 and 3 are lumped as weak. Treat it as a floor and a methodological precedent, not a pop norm.
- Temperley's key result transfers as a hypothesis for compound metre: in pop, a stressed syllable landing one subdivision before a strong beat should be scored as fitting, not as a miss. The engine's 3/4 and 6/8 scoring should allow for anticipation before testing.
- The 80-song stress files are small enough to recompute any 4/4 table the engine needs in the exact form it uses, giving a control against which a new triple-metre table can be compared.

### Gaps
- No published stress-by-beat table for pop in 3/4, 6/8 or 12/8 was found.
- No published stress-to-beat statistics for DALI, LMD lyric files, CoCoPops-Billboard or MTC were found in the sources read (MTC work on stress and metric weight may exist in Van Kranenburg's publications; not searched).

## Well-known 3/4, 6/8 and 12/8 pop, rock and country songs for checking corpus coverage

### Takeaway
A checklist of a few dozen famous triple or compound songs is easy to assemble, and popular lists agree on a core set; the lists also show why automated counting is hard, since they mix true 3/4, 6/8, 12/8 shuffles and songs that change metre.

### Cited Findings
- Listed as 3/4: Patti Page "The Tennessee Waltz"; Doris Day "Que Sera, Sera"; Elvis Presley "Are You Lonesome Tonight?"; Jackie DeShannon "What the World Needs Now"; Bob Dylan "The Times They Are A-Changin'"; "My Favorite Things"; The Beatles "We Can Work It Out"; Jimi Hendrix "Manic Depression"; Engelbert Humperdinck "The Last Waltz"; Paul Simon "Still Crazy After All These Years"; Wings "Mull of Kintyre"; The Stranglers "Golden Brown"; Metallica "One"; Bjork "It's Oh So Quiet"; Kelly Clarkson "Breakaway". — [Beta Monkey, 3/4 examples](https://www.betamonkey.com/popular-examples-of-music-written-in-3-4/)
- Listed as 6/8: Queen "We Are the Champions"; Journey "Lights"; The Beatles "Oh! Darling", "Norwegian Wood", "You've Got to Hide Your Love Away"; Blondie "Call Me"; Tears for Fears "Everybody Wants to Rule the World"; Metallica "Nothing Else Matters". — [Beta Monkey, 6/8 examples](https://www.betamonkey.com/popular-examples-music-written-68/)

### Inferences
- Several entries on those lists are contestable (my judgement, unsourced): "We Can Work It Out" is 4/4 with waltz-time passages in the bridge; "Golden Brown" alternates bar lengths; "One" changes metre; "Call Me" and "Everybody Wants to Rule the World" are usually heard as shuffled 4/4 or 12/8. A coverage test should use unambiguous songs.
- Suggested unambiguous checklist from general knowledge (unsourced; verify each against a score before relying on it). 3/4: "Piano Man", "Take It to the Limit", "Annie's Song", "Time in a Bottle", "Mr. Bojangles", "Moon River", "Open Arms", "Could I Have This Dance", "You Light Up My Life", "Delilah", "Tennessee Waltz", "Are You Lonesome Tonight?", "The Times They Are A-Changin'", "Scarborough Fair". 6/8: "Nothing Else Matters", "House of the Rising Sun", "We Are the Champions", "Norwegian Wood", "Tennessee Whiskey", "Gravity" (John Mayer), "Iris", "Kiss from a Rose", "Breakaway", "A Thousand Years". 12/8: "Hallelujah", "Unchained Melody", "Everybody Hurts", "Can't Help Falling in Love", "When a Man Loves a Woman", "Oh! Darling", "Fallin'", "Perfect" (Ed Sheeran), "Somebody to Love" (Queen), "I Got You Babe".
- Feasibility: the pre-2000 titles above are exactly the repertoire hobbyist karaoke MIDI favoured, so LMD is likely to hold most of them, often in several versions; the post-2010 titles are unlikely to be in LMD (compiled around 2016 from older web archives) or CoCoPops-Billboard (charts to 1991). A few dozen worded triple or compound pop songs looks readily achievable; a few hundred is plausible from LMD lyric files but must be confirmed by the count.
- A cheap first experiment: search the LMD-matched metadata (artist and title via the Million Song Dataset match) for the checklist above, then check which hits have lyric events and what time signature they declare. That measures both coverage and how often 6/8 and 12/8 are mis-declared as 4/4.

### Gaps
- No scholarly list of triple or compound-metre chart songs with verified time signatures was found; the sources here are popular web lists.
- No measured share of 3/4, 6/8 or 12/8 songs in the Billboard charts was found.
