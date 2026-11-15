# Obtainable symbolic datasets of sung melodies in additive / asymmetric and non-Western metres (for building 5/8, 7/8, 9/8 aksak, 10/8, 11/8, 13/8 tables)

Research date: 2026-11-15. Verification method: SymbTr was cloned from GitHub today (commit 246bbe3, dated 2025-04-18, VERSION file = 2.4.3) and its usul and metre counts were computed locally from the 2,200 txt files. The Essen collection was cloned from github.com/ccarh/essen-folksong-collection and its metres counted. All other entries were checked by fetching their landing pages. In this sandbox zenodo.org's API, kern.humdrum.org and the GitHub API were blocked or rate-limited. Where a Zenodo page was fetched through WebFetch it is marked "page verified". Plain `git clone` of public GitHub repos worked.

**Ranked inventory (most useful first for a sung additive-metre table):**

| Rank | Dataset | Tradition | Pieces | Additive content | Vocal / lyrics aligned | Format | Licence | Location |
|---|---|---|---|---|---|---|---|---|
| 1 | SymbTr v2.4.3 | Turkish makam (art + folk) | 2,200 (about 1,550 with sung lyrics) | Very rich: 9/8 aksak etc. 367, 10/8 288, 5/8 61, 7/8 41, 14/8 29, 13/8 4, 11/8 1, 15/8 3 | Yes, one syllable per note row | txt (tab-separated), MusicXML, MIDI, mu2, PDF | CC BY-NC-SA 4.0 (non-commercial) | github.com/MTG/SymbTr ; Zenodo DOI 10.5281/zenodo.160552 |
| 2 | Greek Folk Music Dataset (Aegean syrtos/balos) | Greek Aegean | not stated | Unknown (syrtos and balos are dances, metres not given) | Yes, aligned lyrics | MIDI, MuseScore, PDF, lyrics files, xlsx | CC BY 4.0 | Zenodo DOI 10.5281/zenodo.15470305 |
| 3 | Arab-Andalusian corpus | Moroccan al-Ala | 164 recordings with MusicXML transcriptions | Mizan cycles (not classic aksak) | Vocal; lyrics in a separate dataset | MusicXML + JSON metadata (mizan) | CC BY-NC 4.0 | Zenodo DOI 10.5281/zenodo.1291776 (lyrics: Zenodo 1291904) |
| 4 | PDMX | Mixed (MuseScore user uploads) | over 250,000 | Unknown; must be mined by time signature | has_lyrics flag | MusicXML (MXL), MIDI, PDF, JSON | CC BY 4.0 (per-song licences vary) | Zenodo DOI 10.5281/zenodo.15571083 |
| 5 | Digital Archive of Finnish Folk Tunes (Suomen Kansan Sävelmiä) | Finnish incl. runosongs RS1/RS2 | 8,613 | Kalevala-metre runosongs (5/4-type) in RS subcollections; counts unknown | Lyrics are in the database | MIDI-type note matrices (Matlab), exact format not confirmed | Non-commercial research, attribution; copyright SKS + Eerola/Toiviainen | esavelmat.jyu.fi |
| 6 | Dick Atlee Balkan odd-metre page | Balkan (Bulgarian, Macedonian, etc.) | about 35 | 5, 7, 9, 11, 15, 18, 22 counts | Not stated (mostly dance tunes) | ABC, MIDI, JPEG | No licence stated | dickatlee.com/music/balkan |
| 7 | Jingju Music Scores Collection | Beijing opera | 92 | None (banshi, not additive) | Vocal, lyrics per line with offsets | MusicXML + CSV | "Research purposes", contact author | Zenodo record 1285613 |
| 8 | Radif Corpus | Persian dastgah | 228 gushehs | None (metric pieces deliberately excluded) | No lyrics mentioned | CSV, MIDI, MusicXML | CC BY 4.0 | Zenodo DOI 10.5281/zenodo.15742125 |
| 9 | Essen Folksong Collection | European + Chinese folk | 8,473 kern files | Almost none (5/8: 6 files, 7/8: 1, 9/8: 6, 10/8, 11/8, 13/8: 0) | Many vocal; text in kern | **kern | Restrictive CCARH copyright notice | github.com/ccarh/essen-folksong-collection |
| Not usable | Lanphier Bulgarian/Macedonian songbook | Bulgarian/Macedonian | 21 | 7/8, 9/8, 11/16, 13/16, 15/16, 18/16 | 3 vocal pieces | PDF + MP3 only (not symbolic) | Commercial ($24.95) | lanphier.net/songbook |
| Not usable | Lyra | Greek traditional | — | — | — | Audio + metadata (not symbolic) | — | arXiv 2211.11479 |
| Not usable | ORD-CC32 (1932 Cairo Congress) | Arab | — | iqa tags | — | Audio features + metadata | CC BY-SA 4.0 | arXiv 2506.14503 |

---

## Q1. SymbTr (Turkish makam symbolic corpus): size, vocal pieces, usul list and counts, formats, licence, location

### Takeaway
SymbTr is by far the best obtainable source: 2,200 pieces, about 1,550 with syllable-aligned lyrics, and each score starts with an explicit usul row giving the cycle as a time signature. It holds 367 pieces in 9/8, 288 in 10/8, 61 in 5/8, 41 in 7/8 (plus 30 in 7/4), 29 in 14/8 and small numbers in 13/8, 15/8 and 11/8. The licence is non-commercial share-alike, which matters if ZenEng is ever commercial.

### Cited Findings
- SymbTr "consists of 2200 pieces from 155 makams, 88 usuls, 56 forms, about 865.000 musical notes and 80 hours nominal playback time", drawn from Turkish art and folk music — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md)
- Scores come in text, MusicXML, PDF, MIDI and mu2 formats. PDFs are in a separate repo (github.com/MTG/SymbTr-pdf). The MusicXML is auto-generated from the txt files and has no beaming information yet. The README says beams "should be connected according to the beat locations of the usul" — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md)
- Licence: CC BY-NC-SA 4.0 (README badge and License section) — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md). The Zenodo record for v2.4.3 lists the licence only as "Other (Open)" — [Zenodo 160552](https://zenodo.org/records/160552). The CompMusic corpora page gives no corpus-specific licence and a site footer of CC BY-NC-ND 3.0 — [CompMusic corpora](https://compmusic.upf.edu/index.php/corpora). **Conflict flagged: treat as CC BY-NC-SA 4.0, the most specific statement.**
- Zenodo archive: "SymbTr v2.4.3", DOI 10.5281/zenodo.160552, published 2016-10-13, single 24.5 MB zip (md5 ddf3b165db6a2532761b10a743d37019), linked to the GitHub v2.4.3 release — [Zenodo 160552](https://zenodo.org/records/160552)
- The CompMusic page describes the Turkish corpus as 2,200 scores with "74 usuls" and links github.com/MTG/SymbTr/releases/tag/v2.0.0. This is outdated next to the README's 88 usuls — [CompMusic corpora](https://compmusic.upf.edu/index.php/corpora)
- Changelog: v2.4 "Added the usul row to the start of each score" and "Corrected and validated the measure boundaries for the entire collection semi-automatically". v2.3 "Corrected the usul time signatures in mu2 file headers". v2.4.3 "Added the second lyrics of four music scores" — [SymbTr Changelog.md, in the cloned repo at github.com/MTG/SymbTr](https://github.com/MTG/SymbTr)
- Citation: M. K. Karaosmanoğlu, "A Turkish makam music symbolic database for music information retrieval: SymbTr", ISMIR 2012, pp. 223–228 — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md)
- Helper tools named in the README: SymbTr-extras (clean-up/conversion), symbtrdataextractor (section info, especially vocal sections, plus MusicBrainz metadata via symbTr_mbid.json), makam-symbolic-phrase-segmentation, and tomato (score conversion and analysis) — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md)

**Locally verified structure (git clone of github.com/MTG/SymbTr, 2026-11-15, HEAD 246bbe3 dated 2025-04-18, VERSION 2.4.3)** — [github.com/MTG/SymbTr](https://github.com/MTG/SymbTr)
- 2,200 files each in txt/, MusicXML/, midi/, mu2/. Sizes are txt 45 MB, MusicXML 271 MB, midi 15 MB, mu2 23 MB. Distinct usul slugs in filenames: 88. Forms: 56. Makams: 155. These match the README.
- Filename scheme: `makam--form--usul--title--composer.txt` (e.g. `acem--ilahi--duyek--aldanma_dunya--zekai_dede.txt`).
- txt columns: `Sira Kod Nota53 NotaAE Koma53 KomaAE Pay Payda Ms LNS Bas Soz1 Offset`. Row 1 is the usul row (Kod=51), where `Pay/Payda` gives the cycle length (e.g. `8/8 ... Düyek`). Note rows (Kod=9) carry one lyric syllable each in `Soz1`, which gives syllable-to-note alignment directly. Durations are given as Pay/Payda fractions and as ms. Pitch is in 53-TET koma plus Western AE names.
- Vocal count: 1,550 of 2,200 pieces have at least 10 note rows with a lowercase lyric syllable in Soz1. My heuristic excludes the uppercase section labels such as "TESLİM" and "1. HANE" that instrumental peşrevs put in that column. A looser test, any text, gives 1,795, but that count includes labels.
- Forms (total / vocal by the loose any-text test): şarkı 994/904, türkü 285/283, seyir 169/0, küpe 120/120, peşrev 93/81*, saz semaisi 86/82*, aranağme 73/70, ilahi 42/34, beste 41/25, yürük semai 36/31, ağır semai 32/26, rumeli türküsü 15/15, zeybek 14/3, köçekçe 13/10. *These are from the loose test. Instrumental forms drop sharply under the strict test.

**Usul counts relevant to additive tables (strict vocal heuristic; metre = the usul row's Pay/Payda):**

| Usul (slug) | Pieces | With lyrics | Metre(s) written in file |
|---|---|---|---|
| aksak | 319 | 284 | 9/8 ×303, 9/4 ×16 |
| ağır aksak (agiraksak) | 108 | 85 | 9/4 ×108 |
| evfer | 20 | 14 | 9/8 |
| ağır evfer | 13 | 12 | 9/4 |
| çifte sofyan | 14 | 11 | 9/8 ×13, 9/16 ×1 |
| raks aksağı | 12 (+1 _ii in 9/16) | 10 | 9/8 |
| oynak | 11 | 8 | 9/8 ×9, 9/4 ×2 |
| aydın | 9 | 8 | 9/8 |
| türk aksağı | 64 | 50 | 5/8 ×61, 5/4 ×3 |
| devr-i hindî | 58 (+2 _ii) | 34 | 7/8 ×28, 7/4 ×30 |
| devr-i turan | 10 (+1 _ii, 7/16) | 8 | 7/8 |
| devr-i aryan | 1 | 0 | 7/8 |
| curcuna | 111 | 99 | 10/8 |
| kapalı curcuna | 49 | 49 | 10/8 ×45, 10/16 ×4 |
| aksak semai | 128 | 39 (mostly instrumental saz semaisi) | 10/8 |
| ağır aksak semai | 13 | 7 | 10/4 |
| devr-i süreyya, cengi harbi, aksak semai evferi | 1, 1, 2 | 1, 1, 2 | 10/8 |
| tek vuruş | 1 | 1 | 11/8 |
| nim evsat; bektaşi devr-i revanı | 2; 2 | 2; 2 | 13/8 |
| şarkı devr-i revanı | 5 | 3 | 13/4 |
| devr-i revan; devr-i revanı hindî | 3; 25 | 3; 25 | 14/8 |
| raksan; bektaşi raksanı | 2; 1 | 2; 1 | 15/8 |
| evsat | 5 | 5 | 26/8 ×4, 26/4 ×1 |
| (symmetrical, for contrast) sofyan 293 (4/4), düyek 278 (8/8 ×247, 8/4 ×31), nim sofyan 99 (2/4), semai 100 (3/4), sengin semai 72 (6/4), yürük semai 62 (6/4 mostly) + yürük semai II 55 (6/8 mostly), müsemmen 38 (8/8) | | | |
| Long cycles: devr-i kebir 33 (28/4), muhammes 22 (32/4), hafif 19 (32), zencir 8 (120/4), darb-ı fetih 5 (88/4), çember 9 (24/4), fahte 9 (20/4) | | mostly instrumental or long-form beste | |

**Totals by written metre (all / with lyrics):** 9/8 367/318, 10/8 288/187, 9/4 141/116, 5/8 61/47, 7/8 41/26, 7/4 30/18, 14/8 29/28, 10/4 17/10, 13/4 6/4, 13/8 4/4, 15/8 3/3, 5/4 3/3, 11/8 1/1, 7/16 2/1, 9/16 2/2, 10/16 5/5. Symmetrical totals are 8/8 292, 4/4 288, 6/4 138, 2/4 100, 3/4 98 and 6/8 62. — computed from [github.com/MTG/SymbTr](https://github.com/MTG/SymbTr) txt files.

### Inferences
- **Mapping to Western time signatures:** SymbTr already writes each usul as a numerator over 8 or 4 (or 16/2). The denominator varies within one usul: devr-i hindî appears as 28× 7/8 and 30× 7/4, aksak as 9/8 and 9/4, curcuna as 10/8 and 10/16. So denominators reflect the source edition's notated tempo level, not a different cycle. A table should key on usul plus numerator and treat the denominator as a tempo or notation choice. Ağır aksak (9/4) is the slow "heavy" form of aksak (9/8).
- **Internal grouping is not in the data.** The txt usul row only gives the total length (e.g. 9/8), not the düm/tek stroke pattern or the 2+2+2+3-type grouping. ZenEng would need an external usul definition table to assign groupings. Common-practice groupings, unverified here and to be checked against a makam theory source, are: aksak 9/8 = 2+2+2+3, türk aksağı 5/8 = 2+3, devr-i hindî 7/8 = 3+2+2, curcuna 10/8 = 3+2+2+3, aksak semai 10/8 = 3+2+2+3 with different strokes. Measure boundaries are validated in v2.4, so per-measure stress statistics (e.g. note-onset density per eighth-note position) can be derived empirically from the 284 vocal aksak and 50 vocal türk aksağı pieces to learn the grouping from the data.
- Usable sizes for kept tables: 9/8 aksak family (about 320 vocal pieces) and 10/8 curcuna family (about 150 vocal) are robust. 5/8 (about 50 vocal) and 7/8 (about 45 vocal incl. 7/4 and devr-i turan) are workable. 11/8 (1), 13/8 (4) and 15/8 (3) are too thin for statistics from SymbTr alone.
- Lyrics are Ottoman/Turkish syllables per note, which supports syllable-to-beat placement tables (prosody to metre) directly.
- Licence: CC BY-NC-SA blocks commercial redistribution and requires share-alike for derived tables if they count as adaptations. Derived statistical tables are a grey area that should be flagged to the user.

### Gaps
- I did not verify the exact usul stroke definitions (düm/tek patterns) in a machine-readable file. SymbTr-extras and the makam toolbox may hold one, but those submodules were not cloned.
- No published paper with per-usul counts for v2.4.3 was located. The counts above are my own computation.

---

## Q2. Other CompMusic corpora (Carnatic, Hindustani, Arab-Andalusian, Beijing opera, Dunya): symbolic vs audio

### Takeaway
All five CompMusic corpora have some symbolic component. Only Arab-Andalusian (MusicXML, CC BY-NC 4.0, Zenodo) and Jingju (MusicXML, research-only, on request) are cleanly packaged for download. The Carnatic and Hindustani "scores" are text notations from third-party sites (shivkumar.org, Swarganga) reached through Dunya, with no stated licence. None gives tala-level additive counts in a downloadable package.

### Cited Findings
- CompMusic lists Carnatic (machine-readable notation converted from Dr. Shivkumar Kalyanaraman's archives, 15 talas, lyrics from Sahityam.net, via dunya.compmusic.upf.edu/carnatic) and Hindustani (26 talas, lyrics with scores from Swarganga Music Foundation, swarganga.org/bandishbase.php). No score counts, formats, licence or DOI are given for either — [CompMusic corpora](https://compmusic.upf.edu/index.php/corpora)
- Arab-Andalusian corpus: DOI 10.5281/zenodo.1291776, version 1.0 (2018-06-18). 164 concert recordings (>125 h audio). It includes manually made MusicXML transcriptions. Title, form, **mizan (rhythmic cycle)**, nawba and tab are in JSON files. Lyrics are distributed separately (Zenodo record 1291904). It ships as a single 8.9 GB tar.gz. Licence CC BY-NC 4.0, open access — [Zenodo 1291776](https://zenodo.org/record/1291776)
- CompMusic describes 165 scored Arab-Andalusian recordings in MuseScore, with lyrics from the *Diwan Al-Ala* songbook (TSV/JSON and Dunya API) — [CompMusic corpora](https://compmusic.upf.edu/index.php/corpora)
- Jingju Music Scores Collection: 92 scores, MuseScore 2.1.0 exported to MusicXML 1.0, jianpu converted to staff and all set in E major. `lines_data.csv` gives lyrics per sung line with start and end offsets, and banshi metadata. "Available for research purposes" by contacting Rafael Caro Repetto. Zenodo record 1285613 — [CompMusic node 348](https://compmusic.upf.edu/node/348)

### Inferences
- Arab-Andalusian mizans (basit, qa'im wa nisf, btayhi, darj, quddam) are cyclic but largely notated in simple or compound metres, so they matter for a "non-Western cycle" table but not for aksak tables. The 8.9 GB bundle is mostly audio, so expect to extract only the MusicXML and JSON.
- Jingju banshi are free or simple metres (no additive cycles). Useful only for lyric-melody alignment work.
- For Carnatic misra chapu (7) and khanda chapu (5), the only symbolic path found is Dunya plus Shivkumar's text notations, whose licence is unclear. This is not a ready-to-use dataset.

### Gaps
- I could not confirm current (2026) Dunya API access terms (the API historically required a registered token), nor any per-tala counts for Carnatic or Hindustani notations.
- I did not open the Arab-Andalusian MusicXML to tally mizan counts. The 8.9 GB archive and a blocked Zenodo API in the sandbox prevented it.

---

## Q3. Greek, Bulgarian, Macedonian, Romanian, Serbian, Albanian folk song symbolic corpora

### Takeaway
No large, openly licensed symbolic corpus of Balkan sung melodies in 7/8, 9/8 or 11/8 was found. The best open Greek item is a CC BY 4.0 Zenodo set of Aegean syrtos/balos transcriptions (MIDI and MuseScore, with lyrics), and its metres are not stated. Bulgarian digital folk song libraries exist as research systems, not downloadable datasets. Lyra (Greek) is audio plus metadata only.

### Cited Findings
- "Greek Folk Music Dataset" (Zenodo, v2, 2025-05-19), DOI 10.5281/zenodo.15470305. Covers Greek Aegean folk music focused on syrtos and balos. Contains manually transcribed MIDI scores, lyrics files, xlsx metadata, pattern-analysis txt, and MuseScore (.mscz) plus PDF scores, about 26.3 MB. CC BY 4.0. Includes aligned lyrics. Piece count and metres are not stated on the page — [Zenodo 15470305](https://zenodo.org/records/15470305)
- Lyra: "A Dataset for Greek Traditional and Folk Music" (ISMIR 2022) — [arXiv 2211.11479](https://arxiv.org/pdf/2211.11479.pdf); [ISMIR archive](https://archives.ismir.net/ismir2022/paper/000045.pdf). Audio/metadata-oriented, not symbolic. My characterisation comes from the title and venue only; the paper body was not fetched.
- "Bulgarian Folk Songs in a Digital Library" (DiPP 2011) describes a digital library system for Bulgarian folk songs — [NBU eprints](https://eprints.nbu.bg/id/eprint/896/); [DiPP article](https://dipp.math.bas.bg/dipp/article/view/459). No public bulk symbolic download was found.
- Bill Lanphier's songbook: 21 Bulgarian and Macedonian instrumentals and vocals in metres including 7/8, 7/16, 9/8, 11/16, 13/16, 15/16 and 18/16. Sold as PDF plus MP3 only, $24.95, copyright 2011, no symbolic files — [lanphier.net/songbook](https://lanphier.net/songbook)
- Essen Folksong Collection, cloned from github.com/ccarh/essen-folksong-collection: 8,473 .krn files. Files with `*M5/8`: 6 (Chinese shanxi/han/natmin, one magyar). `*M7/8`: 1. `*M9/8`: 6. `*M10/8`, `*M11/8`, `*M13/8`, `*M7/4`: 0. The "jugoslav" subset (115 songs) is Gottschee German-speaking songs (e.g. "ARE: Europa, Suedosteuropa, Jugoslavija, Gottschee") in 3/4, 4/4 and 2/4, with no additive metres. The "romania" subset exists, but I did not inspect it beyond the global metre counts. The licence file carries a CCARH "IMPORTANT LEGAL REMINDER" stating the data are copyrighted and regulated by a licence agreement — [github.com/ccarh/essen-folksong-collection](https://github.com/ccarh/essen-folksong-collection)

### Inferences
- For Greek kalamatianos 7/8 and zeibekiko 9/8, and Bulgarian or Macedonian 7/8, 11/8 and 13/8 sung melodies, there appears to be no open, downloadable, lyric-aligned symbolic corpus as of 2026. ZenEng would need to (a) mine PDMX by time signature, (b) hand-encode from public-domain printed collections, or (c) lean on Turkish SymbTr for 5/8, 7/8, 9/8 and 10/8 statistics as a regional proxy. Turkish aksak and Balkan aksak are historically related, but the cited sources do not establish that the groupings map one to one.
- Essen is effectively useless for additive metres and its licence is restrictive, so a negative result is itself useful.

### Gaps
- No Romanian, Serbian or Albanian open symbolic sung corpus was located in this pass. Searches were limited and should be repeated with local-language terms.
- The Greek Aegean dataset's piece count and metres were not obtainable (Zenodo was rate-limited).

---

## Q4. Balkan / klezmer ABC collections online, with counts by metre

### Takeaway
Only small, unlicensed ABC sets turned up. Dick Atlee's odd-metre page has about 35 Balkan tunes in ABC plus MIDI, covering 5, 7, 9, 11, 15, 18 and 22-count cycles, mostly instrumental dance tunes. It is useful as a seed list of named rhythms and groupings, not as a statistical corpus.

### Cited Findings
- Dick Atlee's Balkan page: about 35 tunes (Balkan plus a few Greek, Italian, German and Polish), each with standard ABC and often a "w/rhythm" ABC version with chords on every beat. Also MIDI (normal and slow) and JPEG sheet images. Metres include 5 (Pajduško), 7 (many Macedonian and Bulgarian tunes), 9 (De-A-Lungul, Fatiše Kolo), 11 (Gankino Horo, Kopanitsa), 15 (Bučimiš), 18 (Jove Male Mome, 7+11) and 22 (Sandansko Horo, 9+9+4), with count patterns written as q = 2 and s = 3. No licence is stated, and many links had broken by February 2025. It also links to Paul Boizot's "Irregular Rhythms" page — [dickatlee.com/music/balkan](https://dickatlee.com/music/balkan)

### Inferences
- The q/s count patterns on Atlee's page give explicit grouping data (e.g. Kopanitsa 11 = qqsqq) that SymbTr lacks. They suit a hand-curated grouping lookup table for 7, 9, 11, 13, 15, 18 and 22 cycles.
- abcnotation.com search is a further possible mining route for ABC files with `M:7/8` and similar headers, but it was not verified in this pass.

### Gaps
- No large klezmer or folk-dance ABC archive with metre counts was verified. Paul Boizot's page was not fetched.

---

## Q5. Finnish runosong (Kalevala metre, 5/4) symbolic data

### Takeaway
The Digital Archive of Finnish Folk Tunes (8,613 tunes digitised from *Suomen Kansan Sävelmiä*, with lyrics and metre recorded) includes Rune Song subcollections RS1 (Ingrian) and RS2 (Karelian). It is the most promising source for 5/4-type Kalevala-metre melodies, under non-commercial research terms. Its file format and current downloadability are not fully confirmed.

### Cited Findings
- The digitised database contains 8,613 tunes, against about 9,000 in the printed volumes. It lists Rune Song subcollections RS1 (Ingrian, 1910) and RS2 (Karelian, 1930). Lyrics and metre are among the fields entered — [esavelmat.jyu.fi collection](https://esavelmat.jyu.fi/collection.html)
- Download page terms: research use for non-commercial purposes only, with attribution. Copyright in the original collection is held by the Finnish Literary Society (SKS), and in the electronic collection by Tuomas Eerola and Petri Toiviainen. Subcollection codes include LS1 (Laulusävelmät 1) and RS1 (Runosävelmät 1). An update note mentions note velocities set to 100 and a file version updated for Matlab 7. The citation URL is http://www.jyu.fi/musica/sks/ — [esavelmat.jyu.fi download page](https://esavelmat.jyu.fi/collection_download.html)
- Finnic oral poetry research corpora (texts) exist, e.g. the Finnic corpus article in *Folklore* vol. 94 — [folklore.ee](https://folklore.ee/Folklore/vol94/finnic_corpus.pdf); [Kallio et al.](https://www.folklorefellows.fi/wp-content/uploads/Kallio-et-al.pdf). These are text/poetry corpora (SKVR), not melody encodings.

### Inferences
- The Matlab note-matrix format implies MIDI-derived data, which suits rhythm statistics but may not carry lyric-to-note alignment.
- Kalevala-metre songs are typically notated in 5/4 or 5/8 (sometimes 2/4 + 3/4), so the RS subcollections would feed a 5-cycle table distinct from türk aksağı.

### Gaps
- The exact downloadable file formats, RS subcollection sizes and 5/4 counts could not be confirmed. The download page text gave no direct file links in the fetch.
- Zenodo record 4537606 (which surfaced in a runosong search) could not be read because of rate limiting, so its content is unknown.

---

## Q6. Sephardic, Persian and Arabic iqa' symbolic datasets

### Takeaway
No open symbolic Sephardic corpus was found. Persian: the CC BY 4.0 Radif Corpus is symbolic but deliberately excludes metric pieces, so it is useless for cycle tables. Arabic: ORD-CC32 has iqa' tags but is audio-derived. The Arab-Andalusian MusicXML (Q2) is the only Arabic-sphere symbolic set with cycle (mizan) labels.

### Cited Findings
- Radif Corpus: 228 non-metric gushehs across all 13 dastgah/avaz, distributed as CSV, MIDI and MusicXML. Metric pieces "usually performed at the end of each dastgāh" are excluded. No lyrics are mentioned. CC BY 4.0, DOI 10.5281/zenodo.15742125 — [arXiv 2507.10456](https://arxiv.org/html/2507.10456v1)
- ORD-CC32 (1932 Cairo Congress of Arab Music): metadata, maqam and iqa' tags, tonic labels and acoustic features. CC BY-SA 4.0, on Zenodo. Not symbolic notation — [arXiv 2506.14503](https://www.arxiv.org/abs/2506.14503)

### Inferences
- For Arabic iqa' such as samai thaqil 10/8, aqsaq 9/8 and dawr hindi 7/8, Turkish SymbTr (aksak semai 10/8, aksak 9/8, devr-i hindî 7/8) is the closest open symbolic analogue, since the Ottoman and Arab cycle systems share names and structures.

### Gaps
- No Sephardic/Ladino symbolic song dataset was found. No Persian zarbi/reng symbolic dataset with rhythmic cycles was found.

---

## Q7. Dataset papers reporting metre/usul statistics; large general sources to mine

### Takeaway
The only usable metre statistics found are those computed here from SymbTr. PDMX (over 250k CC-licensed MusicXML files) is a large secondary source that could be filtered by time signature to find user-made scores in 5/8, 7/8, 11/8 and similar, with heterogeneous quality and provenance.

### Cited Findings
- PDMX: over 250,000 MuseScore public-domain/CC scores. A "no_license_conflict" subset holds 222,856, and about 31,221 (12.29%) have conflicting licence data. Formats are MusicRender JSON plus MXL, PDF and MIDI, with a PDMX.csv index carrying `has_lyrics` and `n_lyrics` fields. Time signatures are not listed in the index. Record licence CC BY 4.0, with per-song licences in a column. DOI 10.5281/zenodo.15571083 — [Zenodo 15571083](https://zenodo.org/records/15571083)
- SymbTr ISMIR 2012 paper reference (Karaosmanoğlu) — [SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md)
- Jingju collection paper: "A Collection of Music Scores for Corpus Based Jingju Singing Research", ISMIR 2017 — [ISMIR archive](https://archives.ismir.net/ismir2017/paper/000119.pdf)

### Inferences
- A PDMX filter (`has_lyrics == True` plus time signature in {5/8, 7/8, 9/8, 10/8, 11/8, 13/8}, with genre tags like "Balkan", "Greek" or "folk" where present) is the most practical way to gather Balkan and Greek sung examples at scale. Each file's licence column must be respected.

### Gaps
- No ISMIR, TISMIR or FMA paper with corpus-wide aksak statistics for Balkan or Greek symbolic data was found in this pass. The musow catalogue was not queried.
