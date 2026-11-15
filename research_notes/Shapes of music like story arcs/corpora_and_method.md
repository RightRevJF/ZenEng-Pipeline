# Shapes of songs: corpora with outcome labels, per-bar measures, and a method modelled on Reagan et al. (2016)

Method note. Workspace counts marked **(counted)** were made by this researcher on 2026-11-15 with `find`, and with Python scripts (run with `python3 -I`) kept in `/home/claude/p63/scripts/`. New downloads went only into `/home/claude/dl/shape/`. Download hosts that the agent proxy refused in this session: Dropbox (McGill Billboard files), zenodo.org (PDMX, McGill index JSON), ddmal.music.mcgill.ca, and GitHub repos not attached to the session. So the McGill Billboard index, PDMX.csv, Lakh and the MSD files could **not** be fetched or counted here. hymnary.org CSV export worked. This file does not repeat the metre counts already in `Accompaniment corpora and music theory/modern_corpora.md` or `Time signature research and song data/datasets_european_english.md`.

## Q1. Which corpus gives the best test of "shape predicts success" for songs, and which for hymns? (Includes the workspace inventory.)

### Takeaway
For songs, the cleanest test is the **McGill Billboard** set: CC0 chord and section annotations for 890 randomly sampled Hot 100 chart slots (1958–1991), with `peak_rank` and `weeks_on_chart` in its index. Its weakness is that it has harmony only and no melody. The **Rock Corpus** (200 RS-500 songs, CC BY 4.0, melody, harmony and timing, with rank) is the melody check. **Lakh-matched × Million Song Dataset** (45,129 MIDI files, CC BY 4.0, with `song_hotttnesss`) is the large but noisy option. For hymns, **Hymnary.org "Total Instances"** (the number of published text-tune pairings per tune, exportable as CSV, verified here) is a ready-made outcome. Joined by tune name to the Open Hymnal (134 of 272 tune names matched within Hymnary's top 5,000 alone), and potentially to the music21 Bach chorales, it gives a hymn study that can start today. Meertens tune-family sizes are the folk-song analogue. **Nothing already on disk carries a usable popularity label.** Hooktheory, POP909, Lieder and Sacred Harp have only joinable IDs or proxies.

### Cited Findings

**The model study (what is being imitated)**
- Reagan et al. used 1,327 Project Gutenberg fiction books and a 10,000-word sliding window scored with the labMT/hedonometer lexicon. They put mean-centred arcs as rows of a matrix A = UΣVᵀ (the modes are the rows of Vᵀ; the coefficients are W = UΣ, normalised within each book). They also ran Ward hierarchical clustering, with the number of clusters chosen by silhouette, and a Kohonen self-organising map. Six arcs resulted: Rags to riches, Tragedy, Man in a hole, Icarus, Cinderella, Oedipus — [Reagan et al. 2016, EPJ Data Science (PDF)](https://cdanfort.w3.uvm.edu/research/2016-reagan-epj.pdf); [EPJ abstract page](https://epjds.epj.org/articles/epjdata/abs/2016/01/13688_2016_Article_93/13688_2016_Article_93.html)
- Success was proxied by Gutenberg downloads ("only a rough proxy for success"). Icarus, Oedipus and two "Man in a hole" variants had the highest median downloads. Results were shown as medians and box plots with **no formal significance test**. Null models ("word salad" shuffles and n-gram "nonsense" text) gave a flatter SVD spectrum and weaker clustering — [Reagan et al. 2016](https://cdanfort.w3.uvm.edu/research/2016-reagan-epj.pdf)
- Nearest existing song study (lyrics, not notes): Rösch & Rauch (2025, *J. Cultural Economics* 49:603–637). They took line-level lyric sentiment, smoothed it with a **discrete cosine transform**, normalised it to a 0–100% timeline (following Reagan and Del Vecchio et al. 2021), and ran k-means into six archetypes derived from about 6,587 US chart songs (1977–2022). Outcome: points in the Bundesvision Song Contest (176 songs, about 2,800 state-by-song observations), modelled with state fixed effects. "Man in a hole" and "Icarus" scored significantly better, and happy endings were linked to fewer points. The authors call this correlational — [Rösch & Rauch 2025](https://link.springer.com/article/10.1007/s10824-025-09532-6)

**Candidate corpora with outcome labels (size, label, licence, download, time-series support)**

| Corpus | Size | Outcome label | Licence | Download | Per-bar/section series? |
|---|---|---|---|---|---|
| McGill Billboard 2.0 | 890 chart slots, random sample of Billboard slots | index: `chart_date, target_rank, actual_rank, title, artist, peak_rank, weeks_on_chart` | CC0 | `billboard-2.0-index.csv` and `billboard-2.0-salami_chords.tar.gz` (Dropbox), `billboard_index_2.0.json` (Zenodo 13930536) | Yes for harmony and sections (SALAMI-format chord and section files); no melody |
| Rock Corpus (RS 200) | 200 songs | Rolling Stone 500 rank (column in the song lists) | CC BY 4.0 | rockcorpus.midside.com, zips v1.0–v2.1 (v2.1 fixes octave errors) | Yes: harmonic analyses (two analysts), melodic transcriptions, timing data, lyrics and stress for a subset |
| Lakh MIDI, LMD-matched | 45,129 MIDI files matched to MSD (of 176,581 in LMD-full) | via MSD: `song_hotttnesss`, `artist_hotttnesss`, `artist_familiarity`, `year` | CC BY 4.0 (LMD) | `lmd_matched.tar.gz`, `lmd_matched_h5.tar.gz`, `match_scores.json` | Yes (full multi-track MIDI); melody track must be identified |
| PDMX v9 | >250K MusicXML (254,077 in the paper); 14,182 rated | 5-star average `rating` (rated = non-zero); paper mentions "rating and user comment information" | CC BY 4.0 umbrella; use the no-licence-conflict subset | Zenodo 15571083 (`PDMX.csv` 225 MB) | Yes (full scores) |
| Hymnary.org tunes | 5,000 tunes exported here (top by instances) | **Total Instances** = count of published text-tune combinations | Terms of reuse not verified | CSV export link on any tune listing (`...&export=csv&limit=N`) | Incipit code only; full scores not bulk-exportable (unverified) |
| Meertens MTC-FS-INST-2.0 | 18,618 pieces (vocal and instrumental) | `tunefamily` and `tunefamily_full` per melody, plus `year` → tune-family size (variant count) | CC BY-NC-SA 3.0 | liederenbank.nl/mtc/download.php (form); feature JSON on Zenodo 3551003 | Yes (**kern/MIDI; MTCFeatures gives per-note features) |
| The Session | Irish dance tunes (ABC) | `tune_popularity` CSV (tunebook counts) | LICENSE **prohibits processing with LLMs**; ODbL | adactio/TheSession-data | Yes, but excluded |
| Chordonomicon | 667,858 tracks; section labels on 403,923 | none (release date and genre only; Ultimate Guitar ratings used only to pick versions) | CC BY-NC 4.0 (per HF README in earlier notes; the paper says "limited licensing") | HF ailsntua/Chordonomicon | Chords and sections; no bars/durations verified |

Sources for the table:
- McGill: "890 slots from a random sample of Billboard chart slots", CC0, index fields and URLs — [mirdata billboard loader](https://mirdata.readthedocs.io/en/latest/_modules/mirdata/datasets/billboard.html); project page [DDMAL McGill Billboard](https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)) (not reachable from this session)
- Rock Corpus: 200 songs from RS 500 (Dec 9, 2004 issue), annotation types, CC BY 4.0, rank column in the song lists — [rockcorpus.midside.com](https://rockcorpus.midside.com/); [Melodic transcriptions page](https://rockcorpus.midside.com/melodic_transcriptions.html)
- Lakh: counts, CC-BY 4.0, `match_scores.json`, `lmd_matched_h5.tar.gz` "MSD HDF5 metadata files for every LMD-matched entry" — [LMD project page](https://colinraffel.com/projects/lmd/)
- MSD per-song fields "artist familiarity", "artist hotttnesss", "song hotttnesss", "year" (515,576 dated tracks, 1922–2011), plus "sections start" and "segments loudness" (audio-derived) — [Bertin-Mahieux et al. 2011 (PDF)](https://www.ee.columbia.edu/~dpwe/pubs/BertEWL11-msd.pdf)
- PDMX rating definition and 14,182 rated songs (ratings 2.83–4.98). Rated songs show higher pitch-class entropy and lower scale consistency, rising with rating. About 67% of songs have no genre tag — [PDMX paper, arXiv 2409.10831v2](https://arxiv.org/html/2409.10831v2); files and licence — [Zenodo 15571083](https://zenodo.org/records/15571083)
- Hymnary columns, including "Total Instances" ("published text-tune combinations") and the "Export as CSV" link — [hymnary.org tune listing](https://hymnary.org/tunes?prefix=aa) (Hymnary's glossary page, [definition of terms](https://hymnary.org/wiki/definition_of_terms), was found in search but not fetched)
- MTC: 18,618 pieces, CC BY-NC-SA 3.0, formats, download form; MTC-ANN 360 melodies in 26 tune families — [Meertens Tune Collections](https://www.liederenbank.nl/mtc/). The `tunefamily` and `tunefamily_full` metadata fields are present for MTC melodies and empty for Essen — MTCFeatures docs, `docsrc/v1.1/source/melodyrepresentation.rst` **(read on disk)**, [MTCFeatures repo](https://github.com/pvankranenburg/MTCFeatures); feature data — [Zenodo 3551003](https://zenodo.org/records/3551003)
- The Session LLM prohibition and the `tune_popularity` CSV — [adactio/TheSession-data](https://www.github.com/adactio/TheSession-data) (as recorded in `datasets_european_english.md`)
- Chordonomicon section labels (8 classes, 2,679,123 labels over 403,923 tracks), genres, release dates, Ultimate Guitar source — [Chordonomicon paper arXiv 2410.22046](https://arxiv.org/html/2410.22046v1)
- **Spotify popularity can no longer be joined cheaply.** Spotify's February 2026 Development Mode changes list `popularity` as a removed field for Track and Album (and `followers`, `popularity` for Artist), and remove batch `GET /tracks`. New apps were affected from Feb 11, 2026, and existing Dev Mode apps were migrated Mar 9, 2026. Extended Quota Mode is not affected — [Spotify Feb 2026 migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)

**Hymnary export, done here (small, saved to `/home/claude/dl/shape/hymnary/`)**
- **(counted)** `tunes_top5000.csv`: 5,000 tunes sorted by Total Instances. Columns: `totalInstances, tuneTitle, tuneAuthNumber, composers, tuneKey, incipit, meter, tuneSources`. Instances run from max 2,430 (OLD HUNDRED) through WEBB 2,078, DUKE STREET 1,866, DENNIS 1,854, AMERICA 1,810, down to 15; the median is 33. 4,996 rows have a numeric incipit. Meter is blank in 2,597 rows, then Irregular 237, 8.6.8.6 (CM) 235, 8.8.8.8 (LM) 199, 8.7.8.7 D 84, 6.6.8.6 (SM) 71 — [hymnary.org CSV export](https://hymnary.org/tunes?prefix=aa)
- **(counted)** The Open Hymnal has 272 distinct tune names (taken from the filename suffix, e.g. `...-Hursley.abc`). **134 match a Hymnary top-5000 tune title** after case and punctuation normalisation. Their instance quartiles are 15 / 78 / 301 / 700 / 1,866 (e.g. Hursley 1,354; Cwm Rhondda 428; Christus der ist mein Leben 403; St Alban 297). Unmatched examples include Cranham, Sellinge and Crucifer. Some will match against the full (not top-5000) list or under an alternate spelling — [mzealey/openhymnal](https://github.com/mzealey/openhymnal), Hymnary export as above

**Workspace inventory (what is on disk now)**

| Location | Contents **(counted)** | Outcome label? |
|---|---|---|
| `/home/claude/atlas/src/Lieder` (842 MB) | OpenScore Lieder: 1,462 .mxl, 1,462 .mscz, 1,352 .mscx, 1,156 .rntxt (Roman numerals), 1,356 .txt. `data/scores.yaml` has 1,462 entries with fields path, imslp, set_id, language (1,461), lyricist (1,397), **liedernet** text ID (1,299), number, audio (32). `composers.yaml` has gender, born/died, wikidata, imslp | **None.** Proxies only: number of settings of each text on lieder.net, composer Wikidata or IMSLP prominence (external lookups) |
| `/home/claude/atlas/src/SymbTr` (374 MB) | Turkish makam: 2,200 each of .xml, .txt, .mu2, .mid; `symbTr_mbid.json` (MusicBrainz IDs) | None |
| `/home/claude/atlas/src/openhymnal` (5.7 MB) | 305 .abc (SATB; 272 distinct tune names), 15 .mid | None on disk; **Hymnary instances joinable** (134 matched, above) |
| `/home/claude/chrisdonahue/sheetsage-data` (236 MB) | Hooktheory: `Hooktheory.json.gz` (20 MB) has 26,175 clips with keys tags, split, hooktheory{id, artist slug, song slug, annotators, urls}, youtube{id, url, duration}, alignment, annotations{num_beats, meters, keys, melody, harmony}. `Hooktheory_Raw.json.gz` (96 MB) has 26,178 clips covering **15,215 songs, 6,079 artists, 15,007 YouTube IDs**. Clips per song: 1 → 8,625; 2 → 3,748; 3 → 1,843; 4 → 663; 5 → 220; ≥6 → 116. Section names present in only 74 raw clips. Also train/valid/test MIDI tarballs and RWC MIDI | **None.** Artist/title slugs could be joined to Billboard Hot 100 history; YouTube IDs could be joined to view counts (external, API terms apply) |
| `/home/claude/dl/pop909` (153 MB) | POP909: 909 song folders (MIDI with MELODY/BRIDGE/PIANO tracks, beat, chord, key files) plus `index.xlsx` with columns `song_id, name, artist, modify_times, num_beats_per_measure, num_quavers_per_beat` | **None** (`modify_times` is annotation revisions, not popularity) |
| `/home/claude/dl/pdmx`, `/home/claude/dl/lmd`, `/home/claude/dl/emopia` | **Empty directories** | n/a (PDMX ratings and Lakh/MSD hotttnesss are not on disk) |
| `/home/claude/dl/hook/Hooktheory.json.gz` | 378-byte GitHub "access not enabled" error message, **not data** | n/a |
| `/home/claude/dl/gh/` | Repos: MTG_JAAH, OpenEWLD, polyffusion, jukedeck nottingham-dataset, DCMLab JazzHarmonyTreebank (treebank.json includes `year`), EMOPIA (code), CPJKU asap-dataset, AccoMontage-3, sheetsage (code), whole-song-gen, openhymnal, GiantMIDI-Piano (code), OpenScore_Lieder | None (JHT has composition year only) |
| `/tmp/dl/` (3.5 GB) | OpenEWLD 502 .mxl; Essen 8,473 .krn; Creighton 152 .krn; Erk 232 .krn; Child ballads **38 .krn (only "Tune No. 1" of each ballad)**; ELTE folk corpus 14,340 .xml (2,390 Hungarian song **texts**, no music); Sacred Harp CSV/JSON (1991: 554 rows; 2025: 590 rows; fields song_number, title, composer, dates, poet, meter, lyrics, time_signature); catafolk and cfreg registries (index.csv metadata; has a `tune_family_id` column, empty for Bronson); MTCFeatures code and docs only (no feature data); DALI code only (no data); yy1lab lyrics-melody 76,526 .npy (2.3 GB, no bar info); openhymnal and Lieder duplicates | **None** |
| music21 10.5.2 corpus (`/usr/local/lib/python3.13/site-packages/music21/corpus`) | bach 408 .mxl (+20 .rntxt), palestrina 1,318 .krn, ryansMammoth 1,059 .abc, oneills1850 39 .abc, essenFolksong 31 multi-tune .abc, monteverdi 49 .mxl + 48 .rntxt, trecento 101 .xml, beethoven 22 .mxl, mozart 16, haydn 9, plus singletons | None on disk; Bach chorale tune names are joinable to Hymnary |
| `/home/claude/dl/shape/hymnary/` (new) | `tunes_top.csv` (200 rows), `tunes_top5000.csv` (5,000 rows) | **Yes: Total Instances per tune** |

### Inferences
- **Best song test: McGill Billboard.** It is the only open corpus found where the outcome (peak rank, weeks on chart), the era (chart date) and a whole-song time axis (timed chord and section annotations) arrive together under CC0. Because the slots were sampled at random across chart positions, it contains low-peaking minor hits as well as number ones, which is the variance a "shape predicts success" test needs. Its limits: about 890 slots (fewer distinct songs after duplicates; not verified), harmony and sections only, and a pre-1992 window. Arcs from it would be **harmonic** arcs (root distance from the tonic, harmonic rhythm, chord-quality tension, section novelty), not melodic ones.
- **Melody check: Rock Corpus.** It has melody and harmony with timing under CC BY 4.0, but only 200 songs, all canonical (range restriction: rank 1–500 among "greatest"). It suits validating that harmonic arcs computed from chords alone track melodic arcs, rather than serving as the main outcome test.
- **Scale option: LMD-matched + MSD.** It gives 45k songs and a continuous outcome, but hotttnesss is a single 2010–11 Echo Nest snapshot of an opaque metric. MIDI files are fan-made arrangements of variable fidelity, and melody-track detection adds noise. Good for a replication once the method is fixed on McGill.
- **Hooktheory** (on disk, 15k songs) is clip-based: about 57% of songs have a single clip. It cannot give whole-song arcs. It could give a "where in the song does this clip sit" analysis via the YouTube duration and alignment times, which is useful but not the Reagan design.
- **Best hymn test: Hymnary Total Instances × hymn melodies (Open Hymnal now; Bach chorale melodies and other PD sources next).** Hymn tunes are strophic, so the "shape" is the arc within one stanza (typically 4 phrases, 8–32 bars). Instance counts are heavy-tailed (median 33, max 2,430 in the top 5,000) and confounded by **tune age** (exposure time), **poetic meter** (a CM or LM tune can carry far more texts than an irregular one), denomination and cumulative-advantage dynamics. These must be controlled.
- **Folk analogue:** MTC tune-family size (how many variants of a tune family survive in the collection) is a "transmission success" outcome comparable to Hymnary instances, but it is non-commercial (CC BY-NC-SA) and its download was not reachable from this session.
- **Exclude The Session** from any Claude-assisted pipeline (licence forbids LLM processing).

### Gaps
- McGill Billboard: number of **distinct** songs among the 890 slots, the exact year range of annotated slots, and whether all slots have SALAMI-format section labels were not verified (files blocked). The 1958–1991 range is from the assignment brief, not confirmed here.
- Lakh: tarball sizes not listed on the project page. The share of LMD-matched entries with a non-zero/non-NaN `song_hotttnesss` is unknown. **The Echo Nest Taste Profile** (user play counts) was not verified in this session, so its size and licence are unconfirmed.
- PDMX: whether `PDMX.csv` or the metadata JSON also carries views, favourites or number of ratings (the paper names only `rating`) is unverified because Zenodo was blocked.
- POP909: no popularity metadata exists in the index; external Chinese chart data was not sought.
- Hymnary.org: terms of use for bulk CSV export and any API were not found. Text-level instance counts (`/texts` export) are probably available by the same mechanism but were not tested. Matching to the full tune list (beyond the top 5,000) was not done.
- Sacred Harp: usage frequency of each song at singings (the published minutes, e.g. fasola.org) would be an excellent hymn outcome, but it was not verified this session.
- Bronson's full Child-ballad tune set (variant counts per ballad) is not on disk (only 38 tune-1 files) and was not located in open symbolic form.
- Essen folksong: no outcome label exists. Its licence was not re-verified.
- OpenScore Lieder: no outcome label. A lieder.net "number of settings per text" scrape was not attempted.

## Q2. What per-bar measures can we compute today with code we have or can install?

### Takeaway
Today, with installed music21 (BSD-3) and mido (MIT), we can compute per bar: melodic pitch height and register (mean, max, range), note density, number of sounding voices, velocity (MIDI) or notated dynamics (MusicXML), and chord-root distance from the tonic. Hooktheory and the Lieder `.rntxt` files give scale-degree or Roman-numeral roots directly. A quick test parsed a Lieder MusicXML (80 bars) in 0.47 s and an Open Hymnal ABC in 0.12 s. Harmonic tension (Herremans & Chew's spiral-array cloud diameter, cloud momentum and tensile strain) is one `pip install partitura` away (Apache-2.0, v1.9.0). IDyOM information content needs a Common Lisp install, and its licence was not verified this session. No verified open implementation of Lerdahl's tonal-tension model was found.

### Cited Findings
- **Installed now (checked with importlib.metadata):** music21 10.5.2 (BSD-3-Clause), mido 1.3.3 (MIT), numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1 (BSD-3), pandas 3.0.5, openpyxl 3.1.5. **Not installed:** partitura, pretty_midi, muspy, miditoolkit, statsmodels, tslearn **(checked locally)**
- **Installable, licences from PyPI:** partitura 1.9.0, Apache 2.0; muspy 0.5.0, MIT; tslearn 0.10.0, BSD-2-Clause — [PyPI partitura](https://pypi.org/project/partitura/), [PyPI muspy](https://pypi.org/project/muspy/), [PyPI tslearn](https://pypi.org/project/tslearn/)
- **Per-bar pitch height and density test (counted):** music21 parsed `lc29748062.mxl` (Lieder): 80 measures in 0.47 s, per-bar mean MIDI pitch and note count (e.g. bar 10: 66.0, 6 notes). It parsed Open Hymnal `Holy_God_We_Praise_Thy_Name-Te_Deum-Hursley.abc`: 96 measures in 0.12 s (the bar count suggests repeated stanzas or voices are concatenated, so one stanza must be isolated) — script `/home/claude/p63/scripts/perbar.py`
- **Tension ribbons (Herremans & Chew 2016) in partitura:** `estimate_tonaltension(note_info, ws=1.0, ss="onset", ...)` returns `cloud_diameter`, `cloud_momentum` and `tensile_strain` per score position. The window `ws` defaults to 1 beat and can be set per position. It accepts a note array or Part, and estimates spelling and key if they are missing — [partitura tonal_tension source](https://partitura.readthedocs.io/en/latest/_modules/partitura/musicanalysis/tonal_tension.html)
- **midi-miner** (Guo, Herremans et al.) computes the same three tension measures from MIDI with a default half-note window (figures per bar). Key comes from the spiral-array algorithm. GitHub: ruiguo-bio/midi-miner. **Licence not stated** in the paper (and the repo was not reachable here) — [MIDI Miner paper, arXiv 1910.02049](https://ar5iv.labs.arxiv.org/html/1910.02049)
- Original tension-ribbons description — [Herremans & Chew, Tension ribbons](https://dorienherremans.com/content/tension-ribbons-quantifying-and-visualising-tonal-tension)
- **IDyOM:** "IDyOM computes the information content (IC) for each note". `:detail 3` outputs raw IC per event, and `:output-path` writes files. Usage is from a Common Lisp REPL (`(idyom:idyom 18 '(cpitch) '(cpitch))`). The wiki page states **no licence** — [IDyOM wiki](https://code.soundsoftware.ac.uk/projects/idyom-project/wiki/Idyom). A Python-facing port or wrapper appears at [ppidyom (Georgia Tech)](https://ppidyom.ccml.gtcmt.gatech.edu/articles/Overview.html) (not inspected)
- **Chord roots relative to the tonic are native in Hooktheory:** raw chord objects carry `root` (scale degree), `type`, `inversion`, `applied`, `borrowed`, plus a `keys` list (tonic, scale). Notes are stored as scale degree `sd` plus `octave` **(read on disk)** — [chrisdonahue/sheetsage-data](https://github.com/chrisdonahue/sheetsage-data)
- **Roman numerals:** 1,156 `.rntxt` analyses in OpenScore Lieder **(counted)**, readable by music21 — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)
- **MTCFeatures** supplies per-note feature sequences plus metadata (`tunefamily`, `year`, `freemeter`). Rests and grace notes are omitted, and tied notes are merged into one value — MTCFeatures docs `melodyrepresentation.rst` **(read on disk)**, [MTCFeatures](https://github.com/pvankranenburg/MTCFeatures)
- **Harmonic content and rating:** PDMX rated songs show higher pitch-class entropy, which suggests per-bar pitch-class entropy is a cheap "harmonic richness" curve worth including — [PDMX paper](https://arxiv.org/html/2409.10831v2)

**Measure-by-corpus availability (inference from the formats above)**

| Measure (per bar or section) | Code | McGill (chords) | Rock Corpus | Lakh MIDI | Hooktheory | Hymns (ABC/MXL) | Lieder |
|---|---|---|---|---|---|---|---|
| Melodic pitch height, register, range | music21 / mido | no melody | yes | yes (melody track needed) | yes | yes (soprano) | yes (voice staff) |
| Note density, onsets per beat | music21 / mido | harmonic rhythm only | yes | yes | yes | yes | yes |
| Loudness proxy: velocity, voice count, notated dynamics | mido / music21 | no | no | velocity yes | no | voice count only | dynamics markings |
| Chord-root distance from tonic (line of fifths) | own code, music21 roman | yes | yes | after chord estimation | native | after chordify | native via .rntxt |
| Tension ribbons | partitura (Apache-2.0) | from chord pitches | yes | yes | yes | yes | yes |
| IDyOM IC and entropy | IDyOM (Lisp) | no | yes | yes | yes | yes | yes |
| Pitch-class entropy per window | numpy | from chord pitches | yes | yes | yes | yes | yes |

### Inferences
- The minimal measure set needing no new installs is: (1) mean melodic pitch per bar, (2) note density, (3) chord-root fifths-distance from the tonic, (4) pitch-class entropy over a window. Adding partitura gives (5) tensile strain as a principled "tension" curve.
- MIDI velocity is a weak loudness proxy in fan-made MIDI and absent in transcriptions such as Hooktheory or McGill. In scores, voice count and notated dynamics are better. A composite "intensity" (z-scored pitch height + density + voice count) is a reasonable analogue of the hedonometer score, but this is a modelling choice, not an established measure.
- IDyOM should be phase two: it needs a Lisp toolchain, a training corpus per style, and licence confirmation.

### Gaps
- No open, verified implementation of Lerdahl's (2001) tonal-tension model (TPS distances plus attraction) was found in this session.
- partitura's tension output was not run here (not installed). Runtime on 45k Lakh files is unknown.
- IDyOM licence and current repository (GitHub mtpearce/idyom) not verified; the GitHub API was blocked for unattached repos.
- midi-miner licence unknown.
- Whether POP909 MIDI velocities carry performance dynamics was not checked.

## Q3. What would a minimal first study look like (data, measure, method, outcome, controls), and what would it take?

### Takeaway
Run two small, parallel pilots with a common method. **Study A (songs):** McGill Billboard chords and sections → per-bar harmonic-intensity curves → relative-time resampling to 100 points → DCT low-pass smoothing → mean-centred SVD plus Ward or k-means clustering (with shuffled-bar null models) → negative-binomial or ordinal models of `weeks_on_chart` and `peak_rank` on shape, with chart-year, artist random effects and song length as controls. **Study B (hymns):** Open Hymnal soprano lines (and Bach chorale melodies) joined to Hymnary Total Instances → single-stanza pitch-height and tension curves → the same shape pipeline → negative binomial on instances, controlling for tune date, poetic meter and composer. Study B can start today with data on disk plus the 600 KB Hymnary export. Study A needs the roughly few-MB McGill files fetched by a route the proxy allows (or uploaded by the user).

### Cited Findings
- **Normalisation in the model studies:** Reagan et al. slide a fixed-length window to produce a fixed number of points per book, then mean-centre each arc before SVD. Mode coefficients are normalised within each book so high-energy books don't dominate — [Reagan et al. 2016](https://cdanfort.w3.uvm.edu/research/2016-reagan-epj.pdf). Rösch & Rauch normalise to a 0–100% timeline and smooth with a discrete cosine transform before k-means into six clusters — [Rösch & Rauch 2025](https://link.springer.com/article/10.1007/s10824-025-09532-6)
- **Cluster count and validation:** Ward minimum-variance clustering with silhouette-chosen k, a SOM as a second method, and "word salad" and Markov "nonsense" nulls, which should flatten the SVD spectrum if the structure is real — [Reagan et al. 2016](https://cdanfort.w3.uvm.edu/research/2016-reagan-epj.pdf)
- **Outcome modelling precedent:** panel models with fixed effects, Poisson and logit. Results were described as correlational, with controls for audio features (valence, tempo, etc.) to separate lyric arcs from musical effects — [Rösch & Rauch 2025](https://link.springer.com/article/10.1007/s10824-025-09532-6)
- **McGill outcome fields** (`chart_date`, `peak_rank`, `weeks_on_chart`, `target_rank`, `actual_rank`) and CC0 status — [mirdata billboard](https://mirdata.readthedocs.io/en/latest/_modules/mirdata/datasets/billboard.html)
- **Hymnary outcome** (Total Instances) and CSV export, verified by download here — [hymnary.org](https://hymnary.org/tunes?prefix=aa)
- **Spotify popularity is not a viable fresh outcome** for a Development Mode app after March 9, 2026 — [Spotify migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)

**Proposed protocol (this researcher's design, built on the cited methods)**

1. **Time axis**
   - Songs: per bar, then map each bar's midpoint to relative time t ∈ [0, 1]. Resample by bin-averaging into N = 100 bins (or 50 for short songs).
   - Sensitivity check: section-anchored time warping, using piecewise-linear warping between McGill or Chordonomicon section boundaries, so that verse and chorus land at comparable positions.
   - Hymns: one stanza only (strip repeats and extra verses), N = 32 bins or per-half-phrase bins. Strophic repetition means the stanza is the unit of shape.
2. **Measures**
   - Primary "intensity" curve: z-scored per song, the sum of melodic pitch height, note density and tensile strain (or root fifths-distance where melody is absent, as in McGill).
   - Report each component separately as well, since composites hide which dimension drives an effect.
3. **Smoothing**
   - Use a DCT-II low-pass (keep the first k ≈ 8–12 coefficients), a Savitzky–Golay filter, or LOESS on the binned series.
   - **Avoid DFT/FFT low-pass.** It treats the series as periodic, so a song that ends higher than it starts gets an artificial jump and Gibbs ringing at both ends. The DCT's even extension removes that wrap-around discontinuity.
   - Also run Reagan's plain sliding window (e.g. 10% of song length) as a check.
4. **Shape extraction**
   - Mean-centre and unit-normalise each curve, build the matrix A (songs × bins), and take its SVD. Inspect the singular-value spectrum against the nulls.
   - Cluster with Ward (silhouette-chosen k) and k-means. Optionally run DTW-based k-means (tslearn) as a robustness check, though DTW partly erases the "where in the song" information the study is about.
5. **Null models**
   - (a) Shuffle bars within a song.
   - (b) Shuffle sections within a song (for songs).
   - (c) Markov-generated surrogate melodies or chord sequences trained per song.
   - Real data must show a steeper SVD spectrum and better clustering than the nulls, otherwise any "shapes" are smoothing artefacts.
6. **Outcome tests**
   - McGill: negative binomial on `weeks_on_chart` and an ordinal or log model on `peak_rank`. Predictors: the first 4–6 SVD coefficients (continuous, more power than clusters), and cluster membership as a secondary analysis. Controls: chart year or decade spline, song length (bars), tempo if available, key mode, and an artist random intercept (mixed model) or within-artist comparison.
   - Hymns: negative binomial on Total Instances. Controls: tune composition date (exposure), poetic meter class (CM/LM/SM/87.87/other/irregular), composer random effect, public-domain flag, number of bars.
   - Use a held-out split or cross-validation and report the effect size (incremental pseudo-R² over controls), not just p-values. Pre-register the measure, smoothing k and N before looking at outcomes.
7. **Replication** on LMD-matched + MSD hotttnesss (songs) and MTC tune-family size (folk), if those downloads become available.

**What it would take**
- Study B (hymns), today: parse 289 Open Hymnal "Complete" ABC files with music21, isolate the soprano and one stanza, and compute curves. Join to Hymnary (134 matched now; extend with a full tune export and manual fixes for spelling variants). Optionally add the music21 Bach chorale melodies (408 .mxl) by chorale tune name. Install partitura, statsmodels and tslearn. N is likely about 150–300 tunes: enough for a pilot, thin for six clusters plus controls.
- Study A (songs): fetch `billboard-2.0-index.csv` and `billboard-2.0-salami_chords.tar.gz` (small; the Dropbox host must be allowed, or the user uploads them). Write a SALAMI chord-and-section parser (or use mirdata). Compute harmonic curves. N ≈ the distinct songs in 890 slots.
- Melody validation: Rock Corpus v2.1 zip (CC BY 4.0) from rockcorpus.midside.com (host not tested here).

### Inferences
- Expect weak effects. In Reagan's own study the shape-to-downloads link was descriptive (box plots, no test). Rösch & Rauch found significant but correlational arc effects for lyrics. A null result on music is plausible and still informative if the null models show that the shapes themselves are real.
- For hymns, poetic meter and age will likely dominate instance counts. The interesting question is whether shape adds anything beyond them, so report incremental fit.
- Using SVD coefficients as continuous predictors rather than six discrete clusters improves statistical power at small N (McGill, hymns).

### Gaps
- Whether McGill's 890 slots reduce to enough distinct songs, with section labels on every song, for a powered test is unverified.
- No precedent was found for SVD or clustering of **symbolic-music** intensity arcs against an outcome. The only song-arc outcome study found uses lyric sentiment (Rösch & Rauch 2025). Huron's "melodic arch" literature on phrase contour was not checked this session.
- The Hymnary terms of reuse and the size of the full tune export are unverified. Text-level instances (an alternative hymn outcome) were not exported.
- Taste Profile play counts, PDMX views and favourites, and Sacred Harp leading frequencies were not verified as available. Each would strengthen the outcome side.
