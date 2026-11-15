# Obtainable symbolic corpora of modern songs with accompaniment/arrangement (as of Nov 2026)

Method note: Counts marked **(counted)** were computed by me on 2026-11-15 from fresh `git clone --depth 1` checkouts of the GitHub repos named, using mido (MIDI time_signature meta events), regex over MusicXML `<beats>/<beat-type>` and MuseScore `.mscx` `<TimeSig><sigN>/<sigD>`, and the first `M:` field in ABC. "first TS" = first time signature in the file; "any TS" = number of files containing that signature anywhere. Zenodo (zenodo.org) was blocked to shell downloads in this session and the Columbia Lakh host (hog.ee.columbia.edu) did not resolve, so PDMX, Lakh, Slakh, EMOPIA, Pop1K7 and PiJAMA could not be counted; their metadata comes from their Zenodo/landing pages via web fetch.

## Q1. Which corpora contain melody AND accompaniment (piano / multi-track) for modern song styles, and what metres do they hold?

### Takeaway
Only a handful of downloadable corpora pair a melody with a separated accompaniment track: POP909 (MIT, Chinese pop, melody/bridge/piano tracks), OpenScore Lieder (CC0, 19th-c. voice + piano), the Open Hymnal Project (public domain, SATB hymns in ABC), PDMX (CC BY 4.0 umbrella, MuseScore multi-part scores of every genre) and the multi-track MIDI pools (Lakh CC BY 4.0, Slakh, GigaMIDI/MetaMIDI with restrictions). The popular-music corpora with clean track separation are overwhelmingly 4/4; triple and compound metre (3/4, 6/8, 9/8, 12/8) is plentiful only in OpenScore Lieder, the hymn and folk corpora, and probably PDMX.

### Cited Findings

**Recommended ranking for a "kept accompaniment tables by metre and style" engine (my ranking; reasons inline)**

**1. POP909** — best pop melody/accompaniment separation, permissive licence, but metre-poor
- Contents: 909 songs; each `index.mid` has a MELODY track (main melody), a BRIDGE track (sub-melody) and a PIANO track (accompaniment); also beat (audio and MIDI), chord (audio and MIDI) and key annotation txt files, plus alternate `versions` folders, and `index.xlsx` metadata (name, beats per measure, quavers per beat) — [POP909 GitHub README](https://www.github.com/music-x-lab/POP909-Dataset)
- Licence: MIT License, Copyright (c) 2020 Music X Lab — [POP909 repo LICENSE](https://www.github.com/music-x-lab/POP909-Dataset). Format: MIDI + txt + xlsx. Download: `git clone https://github.com/music-x-lab/POP909-Dataset` (also `POP909.zip` in repo). Paper: [arXiv 2008.07142 (ISMIR 2020)](https://arxiv.org/abs/2008.07142)
- **(counted)** All 909 files have the identical track layout `['', 'MELODY', 'BRIDGE', 'PIANO']` — [POP909 repo](https://www.github.com/music-x-lab/POP909-Dataset)
- **(counted)** MIDI time_signature meta events are unreliable: first TS event is 1/4 in 617 files, 4/4 in 264, 2/4 in 21, 6/8 in 5, 3/4 in 2; 84 files contain multiple TS events. Do not trust the MIDI meta events for metre — [POP909 repo](https://www.github.com/music-x-lab/POP909-Dataset)
- **(counted)** From `beat_midi.txt` downbeat markers, the modal bar length is 4 beats in 880 songs and 6 beats in 29 songs — [POP909 repo](https://www.github.com/music-x-lab/POP909-Dataset). This matches a 2026 paper that reports "880 songs in 4/4, and 29 in 3/4 or 6/8" and 77,638 measures, 503 major / 406 minor songs — [arXiv 2602.15074, Structure-Aware Piano Accompaniment via Style Planning and Dataset-Aligned Pattern Retrieval](https://arxiv.org/pdf/2602.15074)
- **(counted)** `index.xlsx` (num_beats_per_measure, num_quavers_per_beat): (2,2) 857 songs; (3,2) 28; (2,3) 23; (3,3) 1. Read as simple-duple / simple-triple (3/4) / compound-duple (6/8) / compound-triple (9/8), this gives ~52 non-duple songs, which disagrees with the 29 from the beat file — [POP909 repo](https://www.github.com/music-x-lab/POP909-Dataset)
- Derived works: AccoMontage, Polyffusion and the whole-song generation model all train on POP909. Polyffusion distributes POP909 extracted features via a SharePoint link — [Polyffusion README](https://github.com/aik2mlj/polyffusion); whole-song-gen (MIT) distributes its processed data via a Google Drive link in `data/download_link.txt` — [whole-song-gen repo](https://github.com/ZZWaang/whole-song-gen). Phrase/section annotations for POP909: [hierarchical-structure-analysis](https://www.github.com/Dsqvival/hierarchical-structure-analysis)
- Style labels (dynamics/articulation/rhythm/tension/texture/register per measure) were derived on POP909 in the 2026 paper, but release of the labels is not stated — [arXiv 2602.15074](https://arxiv.org/pdf/2602.15074)

**2. OpenScore Lieder** — best open source of voice + piano accompaniment across many metres (art song, not modern pop)
- Mirror of the MuseScore OpenScore Lieder corpus: "Collection of songs by 19th century composers in MuseScore format with associated data"; batch convertible to MusicXML/MIDI/PDF via MuseScore CLI — [OpenScore Lieder GitHub](https://github.com/OpenScore/Lieder)
- Licence: CC0 1.0 Universal (LICENSE.txt) — [OpenScore Lieder repo](https://github.com/OpenScore/Lieder)
- **(counted)** Files: 1,352 `.mscx`, 1,462 `.mscz`, 1,462 `.mxl`, 1,156 `.rntxt` (Roman-numeral harmonic analyses), 1,355 `.txt` (lyrics) — [OpenScore Lieder repo](https://github.com/OpenScore/Lieder)
- **(counted, 1,352 mscx)** First TS: 4/4 421; 3/4 265; 2/4 237; 6/8 216; 2/2 58; 3/8 49; 9/8 33; 12/8 20; 6/4 18; 3/2 11; 4/8 6; 4/2 3; 8/8 2; 6/16 2; 7/8 2; 5/4 2; 4/16, 7/4, 9/16, 15/8 1 each; none 3. Files containing TS anywhere: 4/4 478, 3/4 332, 2/4 317, 6/8 247, 2/2 67, 3/8 63, 9/8 50, 12/8 30, 6/4 28, 3/2 25, 9/4 6, 5/4 4, 7/8 3. 248 files change metre — [OpenScore Lieder repo](https://github.com/OpenScore/Lieder)

**3. Open Hymnal Project** — the only open hymn-accompaniment corpus found with full parts
- GitHub clone of all Open Hymnal data; aim: "a freely distributable, downloadable database of Christian hymns ... distributed as complete scores (words and music), using all accompaniment parts" in "ABC Plus" format, also rendered to pdf/MIDI/mp3 — [mzealey/openhymnal](https://github.com/mzealey/openhymnal)
- Licence: no formal licence file found; file headers state hymns must be "in the public domain or freely distributable" and can be "freely modified by anyone" — [openhymnal repo file headers](https://github.com/mzealey/openhymnal)
- **(counted)** 305 ABC files (one tune each); distinct `V:` voices per file: 4 voices in 286 files, 2 in 6, 3 in 3, 5 in 5, 6 in 3, 8 in 2 (i.e. mostly SATB). First `M:` field: 4/4 203; 3/4 48; 6/4 10; 3/2 7; 6/8 6; 2/4 5; 2/2 3; 8/4 2; 9/4 1; 9/8 1; none 19 — [openhymnal repo](https://github.com/mzealey/openhymnal)
- A Hugging Face derivative exists: [noahtye/openhymnal](https://huggingface.co/datasets/noahtye/openhymnal) (not inspected)

**4. PDMX** — largest openly licensed multi-part score corpus, genre-tagged, metre content not yet measured
- PDMX v9 (June 1, 2025), DOI 10.5281/zenodo.15571083: >250K public-domain MusicXML scores from MuseScore; files: MXL (1.9 GB), MIDI (214 MB), PDF (9.6 GB), MusicRender JSON, metadata JSON, `PDMX.csv` with per-song columns incl. `n_tracks`, `tracks`, genres, `n_lyrics`, `has_lyrics`; subsets "no license conflict" (222,856 songs; 31,221 songs = 12.29% had conflicting internal licences), rated, deduplicated, all-valid; licence CC BY 4.0; open access — [Zenodo PDMX v9](https://zenodo.org/records/15571083)
- Code/README: [PDMX GitHub (speechprojects fork of pnlong/PDMX)](https://github.com/speechprojects/PDMX); paper [arXiv 2409.10831](https://arxiv.org/abs/2409.10831v2)

**5. Lakh MIDI Dataset (LMD)** — huge multi-track pop/rock MIDI pool, CC BY 4.0, quality uneven
- LMD-full 176,581 unique MIDI files; LMD-matched 45,129 (matched to Million Song Dataset); LMD-aligned the same 45,129 aligned to 7digital previews; "distributed with a CC-BY 4.0 license"; Copyright meta-event "not used consistently"; some files include key signatures and lyrics — [LMD project page](https://colinraffel.com/projects/lmd/)
- Download URLs listed: `http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz`, `lmd_matched.tar.gz`, `lmd_aligned.tar.gz` — [LMD project page](https://colinraffel.com/projects/lmd/)
- AccoMontage-3 (MIT) uses processed LMD (Google Drive) for its prior and Slakh2100 for its autoencoder (processed Slakh in the Query-and-reArrange repo) — [AccoMontage-3 README](https://github.com/zhaojw1998/AccoMontage-3)

**6. Slakh2100** — 2,100 LMD-derived multi-track songs rendered to audio with per-instrument MIDI. Zenodo record exists — [Zenodo 4599666 (slakh2100-redux)](https://zenodo.org/record/4599666); licence could not be verified (fetch blocked; see Gaps).

**7. Large MIDI pools with restrictive terms**
- GigaMIDI v2.0.0: 2,136,218 MIDI files (the annotation section cites >1.4M, from an earlier version), 6,891,738 tracks, curated style labels (Musicmap); **CC BY-NC 4.0**, gated on Hugging Face (accept conditions + login), "non-commercial research or education" only — [HF Metacreation/GigaMIDI](https://huggingface.co/datasets/Metacreation/GigaMIDI)
- MetaMIDI (MMD) v1.0.1: 436,631 MIDI files; artist/title for 221,504; genre for 143,868; 168,032 MusicBrainz matches; **restricted access, research purposes only, must agree not to share/distribute**; no licence stated — [Zenodo 5142664](https://zenodo.org/records/5142664)

### Inferences
- For 3/4, 6/8 and 12/8 accompaniment tables, POP909 alone is inadequate (~29–52 non-duple songs of 909). OpenScore Lieder (≈265 3/4-first, 216 6/8-first, 33 9/8, 20 12/8 songs, all with piano) and the Open Hymnal (≈48 3/4, plus 6/4 and 3/2) supply the triple/compound textures, though in 19th-c. art-song and hymn idioms rather than pop.
- PDMX is likely the best place to harvest modern-style piano/band arrangements in non-4/4 metres (MuseScore users transcribe pop, film, worship and theatre songs), but the per-file licence conflicts (12.29%) and the fact that user-uploaded "public domain" claims for modern songs may be false make it a licence-risk corpus despite the CC BY 4.0 umbrella. Use the no-conflict subset.
- MIDI time_signature meta events should be cross-checked against beat annotations (POP909 shows 617/909 files with a spurious 1/4).

### Gaps
- PDMX, Lakh (full/matched) and Slakh time-signature distributions: not counted (Zenodo blocked to shell, Columbia host unreachable). The Lakh tutorial notebook reports no TS statistics — [LMD Tutorial notebook](https://nbviewer.jupyter.org/github/craffel/midi-dataset/blob/master/Tutorial.ipynb). No published LMD TS distribution was found.
- Slakh2100 licence not verified (Zenodo page fetch refused).
- PDMX genre list and how many scores are piano+voice or have lyrics: columns exist but counts not obtained.

## Q2. Piano-only corpora (pop covers, jazz, classical) useful as texture sources

### Takeaway
Pop piano texture is available as CC BY 4.0 (Pop1K7, all 4/4) and CC BY-NC-SA (EMOPIA); large transcribed piano corpora (Aria-MIDI, GiantMIDI-Piano, PiJAMA, MAESTRO) are mostly classical or solo jazz, and all but GiantMIDI forbid commercial use. None separate melody from accompaniment.

### Cited Findings
- **Pop1K7** (AILabs.tw) v2 (Aug 2, 2024), DOI 10.5281/zenodo.13167761: 1,747 transcribed piano performances of Western, Japanese and Korean pop, ~108 h; **all pieces in 4/4**; MIDI at each processing step + REMI/CP tokens; Pop1K7-emo adds key signatures; **CC BY 4.0**, open — [Zenodo 13167761](https://zenodo.org/records/13167761). HF mirror: [ChilleD/pop1k7](https://huggingface.co/datasets/ChilleD/pop1k7/tree/main)
- **EMOPIA**: **CC BY-NC-SA 4.0**, "prohibited to be used for commercial purposes"; data at Zenodo record 5090631 — [EMOPIA README](https://github.com/annahung31/EMOPIA)
- **GiantMIDI-Piano**: 10,855 MIDI files of 2,786 composers (curated subset 7,236 files / 1,787 composers), classical, transcribed from recordings; **CC BY 4.0** — [GiantMIDI-Piano README](https://github.com/bytedance/GiantMIDI-Piano)
- **Aria-MIDI**: 1,186,253 MIDI files (~100,629 h), 800,973 after dedup; YouTube piano transcriptions, classical-dominated but with LLM-extracted genre labels (jazz, pop, rock, soundtrack, etc.) on 86.5% of files; **CC BY-NC-SA 4.0**; download https://github.com/loubbrad/aria-midi — [arXiv 2504.15071](https://arxiv.org/html/2504.15071v1)
- **PiJAMA**: 2,777 solo jazz piano performances, 120 pianists, 244 albums, >200 h, automatic transcription, MIDI (60 MB); **CC BY-NC 4.0**; DOI 10.5281/zenodo.8354955 — [Zenodo 8354955](https://zenodo.org/records/8354955)
- **MAESTRO** v3.0.0: 1,276 performances, ~198.7 h; **CC BY-NC-SA 4.0**; MIDI-only zip at storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip — [Magenta MAESTRO page](https://magenta.tensorflow.org/datasets/maestro)
- **ASAP**: **CC BY-NC-SA 4.0** — [ASAP README](https://github.com/CPJKU/asap-dataset). **(counted, 242 MusicXML scores)** first TS: 4/4 80, 2/4 45, 3/4 43, 6/8 26, 2/2 14, 3/8 9, 12/8 8, 9/8 6, 12/16 3, 3/2 2, 6/4 2, others 1 each — [ASAP repo](https://github.com/CPJKU/asap-dataset)

### Inferences
- Pop1K7 is the cleanest commercial-safe pop piano texture source but cannot fill non-4/4 tables. Its accompaniment must be separated from melody algorithmically (it is a single piano part).

### Gaps
- EMOPIA song count and metre content were not verified (Zenodo fetch not attempted after block).

## Q3. Melody + chord (lead-sheet) corpora: jazz standards, pop, theatre-era songs

### Takeaway
Hooktheory (26,175 annotated sections, CC BY-NC-SA 3.0) is the largest downloadable pop melody+chord set and has measurable non-4/4 content; OpenEWLD (502 public-domain lead sheets, MusicXML with chords) covers standards/theatre-era songs; the Jazz Harmony Treebank (1,170 iReal-derived chord sequences, CC BY-NC-SA 4.0) and JAAH (113) cover jazz harmony. None contain accompaniment.

### Cited Findings
- **Hooktheory (Sheet Sage release)**: "50 hours of aligned melody and harmony annotations" from Hooktheory TheoryTab, **CC BY-NC-SA 3.0**, JSON (20 MB), no audio; files `Hooktheory.json.gz`, raw format, train/valid/test MIDI — [Sheet Sage README](https://github.com/chrisdonahue/sheetsage); data repo [chrisdonahue/sheetsage-data](https://github.com/chrisdonahue/sheetsage-data)
  - **(counted)** 26,175 annotations; 23,833 with melody, 25,856 with harmony; 279 with metre changes. First metre: 4/4 23,722; 6/4 1,266; 3/4 969; 2/4 53; 6/8 47; 5/4 45; 12/8 36; 9/4 14; 12/4 10; 3/8 7; 9/8 5; 8/4 1 — [sheetsage-data repo](https://github.com/chrisdonahue/sheetsage-data)
- **OpenEWLD**: public-domain subset of EWLD, "You can redistribuite this worl as you want"; repo MIT licence; DOI 10.5281/zenodo.4332855 — [OpenEWLD GitHub](https://github.com/00sapo/OpenEWLD)
  - **(counted)** 502 MXL lead sheets, all single-part, all with `<harmony>` chord symbols; first TS: 4/4 287, 2/2 94, 3/4 80, 2/4 17, 6/8 13, 3/2 1, 6/4 1, 12/8 1, none 8 — [OpenEWLD repo](https://github.com/00sapo/OpenEWLD)
- **EWLD** (full): >5,000 lead sheets; **restricted access**; requesters must agree "The data will never be used for commercial and/or profit purposes" — [Zenodo 1476555](https://zenodo.org/record/1476555)
- **Jazz Harmony Treebank**: licence CC BY-NC-SA 4.0 (LICENSE.md) — [DCMLab/JazzHarmonyTreebank](https://github.com/DCMLab/JazzHarmonyTreebank). **(counted)** 1,170 entries (fields: title, measures, beats, chords, composers, year, meter, key); meter 4/4 1,089, 3/4 78, 6/4 3 — [JHT repo](https://github.com/DCMLab/JazzHarmonyTreebank)
- **JAAH**: JSON annotations + lab chord files — [MTG/JAAH](https://github.com/MTG/JAAH). **(counted)** 113 annotation files; metre 4/4 108, 2/4 3, 3/4 1, 6/4 1 — [JAAH repo](https://github.com/MTG/JAAH)
- **Weimar Jazz Database** v2.1: 456 solo transcriptions; SQLite + unquantized MIDI of solos; **ODbL** — [Jazzomat download page](https://jazzomat.hfm-weimar.de/download/download.html)
- **Nottingham** (jukedeck clean): ABC sourced from the Nottingham Music Database, cleaned chord notation; **GPL-3.0** — [jukedeck/nottingham-dataset](https://github.com/jukedeck/nottingham-dataset). **(counted)** 3,089 MIDI files (first TS 4/4 1,607, 6/8 1,107, 3/4 178, 2/4 121, 9/8 41, 2/2 20, 3/2 9, 6/4 6); ABC_cleaned first `M:` per X: header (1,034 headers parsed): 4/4 548, 6/8 360, 3/4 60, 2/4 41, 9/8 13, 2/2 7, 3/2 3, 6/4 2 — [nottingham-dataset repo](https://github.com/jukedeck/nottingham-dataset)
- **Chordonomicon**: >666,000 songs' chord progressions with section structure, genre, sub-genre, release date, Spotify IDs; **CC BY-NC 4.0** — [HF ailsntua/Chordonomicon README](https://huggingface.co/datasets/ailsntua/Chordonomicon/raw/main/README.md)
- **symbolic-jazz-standards** (HF): 709 examples from ~200 public-domain jazz standards, Demucs stems transcribed to tokens (REMI/MIDI-like/TSD), Parquet; metadata says apache-2.0 but disclaimer cites "fair use" — [HF jspr/symbolic-jazz-standards](https://huggingface.co/datasets/jspr/symbolic-jazz-standards/blob/main/README.md)

### Inferences
- Hooktheory's 6/4 count (1,266) probably absorbs many songs heard as 6/8 or 12/8 because TheoryTab counts in quarter-note beat units; treat 6/4 + 6/8 + 12/8 as one compound bucket (~1,350).
- For a commercial songwriting engine, only OpenEWLD, Nottingham (GPL copyleft), Weimar (ODbL share-alike) and PD corpora are clearly usable beyond research; Hooktheory, JHT, Chordonomicon, EWLD are non-commercial.

### Gaps
- McGill Billboard, RWC, Isophonics, iRb (Broze & Shanahan), the Real Book chord datasets, and iReal Pro collections: not verified this session. iRb has a JS package [sharp11-irb](https://github.com/jsrmath/sharp11-irb) and an R corpus package [hcorp](https://github.com/pmcharrison/hcorp) (not inspected).
- Hooktheory licence on the [HF m-a-p/HookTheory](https://huggingface.co/datasets/m-a-p/HookTheory) mirror: page not fetchable.

## Q4. Contemporary worship, musical theatre and film symbolic data

### Takeaway
I found no open, downloadable symbolic corpus of contemporary worship (CCM), musical theatre or film songs with accompaniment. Hymnody exists only as public-domain material (Open Hymnal, 305 SATB hymns). Modern worship/theatre/film content appears only inside mixed user-upload pools (PDMX, Lakh, GigaMIDI, Aria-MIDI "soundtrack" label) with uncertain rights.

### Cited Findings
- Open Hymnal: see Q1 (305 SATB ABC hymns, PD/freely distributable) — [mzealey/openhymnal](https://github.com/mzealey/openhymnal)
- The musow catalogue lists hymn resources such as "New Hymns for Worship" and "Hymns and Carols of Christmas" (catalogue entries, not inspected for format/licence) — [musow New Hymns for Worship](https://projects.dharc.unibo.it/musow/view-1635268063-599884); [musow Hymns and Carols of Christmas](https://projects.dharc.unibo.it/musow/view-1635268063-599964)
- Aria-MIDI genre labels include "soundtrack" — [arXiv 2504.15071](https://arxiv.org/html/2504.15071v1)
- MusiCorpus (2026, an OMR dataset with MusicXML, sacred and secular, CC BY-NC-SA 4.0) is historical manuscripts, not modern song — [arXiv 2605.18436](https://arxiv.org/html/2605.18436)

### Inferences
- Worship/theatre accompaniment tables will need to be built by the user (from owned arrangements) or mined from PDMX genre tags with manual licence vetting. CCLI/PraiseCharts material is commercial and not an open corpus.

### Gaps
- No dataset found for CCM/worship-band arrangements, Broadway piano-vocal scores or film-score reductions in open symbolic form. Hymnary.org MusicXML availability not verified.
