# Art-song text setting in triple/compound metre, and open corpora with aligned lyrics

Reading notes: "local count" means a number I computed myself on 2026-11-27 from the downloaded data (method stated each time); these are not published figures. Anything I know only from memory and could not open a source for is in Gaps, labelled "unverified recall".

## 1. What does the theory and empirical literature say about stress-to-beat alignment in triple and compound metre? (numbers)

### Takeaway
The literature agrees on one hard rule (stress and metrical strength must not move in opposite directions between adjacent syllables; the stronger of two neighbouring syllables takes the stronger position) and treats triple/compound metre with the same machinery as duple by making the dotted quarter the tactus in 6/8, 9/8, 12/8. No source I could open reports alignment percentages broken down by metre; the available numbers are pooled across metres.

### Cited Findings

**Temperley & Temperley 2013 (French vs English song)** — Temperley, N., & Temperley, D. (2013). Stress-meter alignment in French vocal music. *Journal of the Acoustical Society of America* 134(1), 520–527, doi:10.1121/1.4807566.
- Corpus: 54 French songs from Jameson & Heacox, *Chants de France* (1922), 9,003 syllables, 1,193 lines; English comparison = first ten songs of Hatton & Faning, *Songs of England*. — [Temperley & Temperley 2013 PDF](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- Metrical coding used a 4-level grid: tactus (level 2) = quarter note in 2/4, 3/4, 4/4 and **dotted quarter in 6/8, 9/8, 12/8**; levels 3–4 above the tactus, level 1 below; each syllable gets the highest level present at its note onset. No separate treatment of triple vs duple beyond this. — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- English: mean metrical level of stressable syllables 3.08 vs unstressable 1.93 (difference "SMAV" 1.15). French: 2.57 vs 1.80 (SMAV 0.77). English alignment significantly stronger (t = 3.63, p < .01). — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- In English, in an unstressed–stressed pair inside a polysyllabic word, the second syllable was metrically stronger in **all 94 of 94** tokens (French: 0.64 of 1,031). I.e. in English song, lexical stress inside a word is effectively inviolable. — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- Line-final syllables: 97% of French lines end on a stressable syllable, with mean metrical level 3.14 (all other syllables 1.88): the line's last stress sits on a very strong beat. — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- Category means (French): final full syllable of polysyllable 2.69; monosyllabic content word 2.26; monosyllabic function word 1.91; schwa 2.05; other syllable of polysyllable 1.59. So the ordering is word-stress > content monosyllable > function monosyllable > unstressed syllable of a polysyllable. — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)
- Later verses align worse than first verses (SMAV 0.51 vs 0.33): strophic settings are fitted to verse 1. — [same](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)

**De Castro-Arrazola, van Kranenburg & Janssen 2015 (Dutch folk song, MTC-FS)** — "Computational textsetting analysis of Dutch folk songs", Proc. Folk Music Analysis 2015.
- 3,724 songs, 3,973 stanzas, 20,662 phrases, 185,263 notes, 176,708 syllables; melismas are only **4.46% of syllables** (folk song is overwhelmingly one note per syllable). — [De Castro-Arrazola et al. 2015](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Method: binary lexical stress looked up in e-Lex; metrical prominence = music21 beat strength (0–1, downbeat = 1); both converted to contours (−, =, +) relative to the previous syllable. — [same](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Association factors (observed/expected; <0.5 = avoided): stress falling while prominence rises **0.26**; stress rising while prominence falls **0.36**; matching directions over-represented (stress− & prom− 1.77; stress+ & prom+ 1.60; stress+ & prom= 1.24). The falling-stress/rising-prominence mismatch occurs in 0.03 of transitions against 0.12 expected. — [same](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Context: phrase-final position makes a stressed-syllable mismatch far more strongly avoided; a melisma on the first syllable licenses putting the following unstressed syllable on a stronger position; the constraint acts over a span larger than the word but smaller than the phrase. — [same](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Not broken down by metre; the only mention of 6/8 is the suggestion that positions 2 and 3 of a 6/8 half-bar may not be equal in strength. — [same](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)

**Palmer & Kelly 1992** — Palmer, C., & Kelly, M. H. (1992). Linguistic prosody and musical meter in song. *Journal of Memory and Language* 31, 525–542.
- Corpus: vocal themes of Gilbert & Sullivan's 14 operettas plus English art-song settings (Arne, Purcell, Morley, Ireland etc.). Meters are grouped as binary (2/4, 4/4) and ternary (3/4, 6/8); no results reported by metre. — [Palmer & Kelly 1992 PDF](https://www.examenapium.it/cs/biblio/Palmer1992.pdf)
- Compound nouns (stress on first element): metrical accent on the first syllable in 43/48 (about 90%) in G&S and 96/105 (about 91%) in art-song settings. — [same](https://www.examenapium.it/cs/biblio/Palmer1992.pdf)
- Two-word phrases (adjective + noun, nuclear stress on the second): accent on the second word in 79/95 (about 83%) in G&S but only 67/158 (about 42%) in art song — word-level stress is honoured about 90% of the time, phrase-level stress much less reliably. — [same](https://www.examenapium.it/cs/biblio/Palmer1992.pdf)
- In performance, both metrical accent and linguistic stress independently lengthen sung syllables (F(1,9) = 23.5 and 18.0), with no interaction. — [same](https://www.examenapium.it/cs/biblio/Palmer1992.pdf)

**Hayes (building on Halle & Lerdahl 1993)** — Hayes, B. (2009). Textsetting as constraint conflict. In Aroui & Arleo (eds.), *Towards a Typology of Poetic Forms*, Benjamins.
- Four competing goals, ranked: (a) match stress to strong grid positions; (b) avoid long lapses (stretches where no syllable begins); (c) avoid extreme syllable compression; (d) align phonological phrase boundaries with line boundaries. A setting is the best compromise, not a rule output. — [Hayes, Textsetting page](https://brucehayes.org/Textsetting)
- Open data on that page: 346 lines of English folk verse with stress transcription and the modal setting chosen by nine native speakers (tab-delimited text), plus the 640-line Hayes & Kaun 1996 set with syllable weight and phrasing. — [same](https://brucehayes.org/Textsetting)

**Krebs 2014 (Schumann)** — Krebs, H. "Treading Robert Schumann's New Path: Understanding Declamation in the Late Lieder through Analysis and Recomposition", *Music Theory Online* 20.4.
- A normative ("basic rhythm of declamation") setting has four properties: poetic stresses fall on beats and strong stresses on strong beats; couplets (or single lines) align with four-bar hypermeasures; silences come where the poem implies them, normally at line ends; feet (stress-to-stress intervals) are roughly equal in duration. — [Krebs 2014](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.krebs.php)
- Triple-metre example ("Der schwere Abend", 3/4): two normative options for iambic verse — even notes, or stressed syllables elongated so the bar alternates **half note (stressed) + quarter (unstressed)**; a pause is "obligatory at the end of each line". — [same](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.krebs.php)
- Catalogue of expressive deviations: acceleration (feet compressed into eighth-note runs), elongation of a stressed syllable, omitted line-end pause (next line enters early), pause filled by piano, displacement of a strong stress off the downbeat; acceleration can shrink a four-bar hypermeasure to three. — [same](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.krebs.php)

### Inferences
- For English, treat lexical stress inside polysyllabic words as a hard constraint (94/94; about 90% for compounds) and phrase-level/monosyllable stress as soft (42–83%).
- A contour formulation is easier to implement in 3/4 and 6/8 than "stress on strong beat": for each adjacent syllable pair, forbid (stress down, strength up) and (stress up, strength down). It needs only a strength table per metre.
- A usable strength table, following Temperley's levels: 6/8 → position 1 = level 3+, position 4 = level 2 (tactus), positions 2, 3, 5, 6 = level 1; 3/4 → beat 1 = level 3, beats 2 and 3 = level 2, off-beat eighths = level 1. Note the consequence: in 3/4 beats 2 and 3 are equal, so a stressed syllable on beat 3 followed by an unstressed one on beat 1 is the violation to forbid, while stressed on 2 → unstressed on 3 is neutral.
- Final stress of every line should be forced onto a downbeat (or the mid-bar dotted-quarter beat in 6/8 at minimum).
- Fit the melody rhythm to verse 1 and accept weaker alignment in later verses, as the tradition does.

### Gaps
- No percentages by metre (3/4 vs 6/8 vs 4/4) found in any opened source. This is computable from MTCFeatures (has `wordstress`, `beatstrength`, `timesignature` per note; see section 4) — a small analysis job, not a literature fact.
- Halle & Lerdahl 1993 ("A generative textsetting model", *Current Musicology* 55), Dell & Halle 2009 ("Comparing musical textsetting in French and in English songs", same Benjamins volume, doi:10.1075/lfab.2.03del), Proto & Dell (Italian), Kiparsky ("A modular metrics for folk verse", 2006) and Hayes & Kaun 1996 were not opened; only located. Unverified recall: Halle & Lerdahl's procedure assigns the line's stressed syllables to the strong beats of the grid right-to-left from the last stress, then distributes unstressed syllables in between; Dell & Halle argue English requires stress-beat matching throughout the line while French requires it only at line end (consistent with Temperley's weaker French figure, which I did verify).
- Deborah Stein (Stein & Spillman, *Poetry into Song*, OUP 1996) not consulted.

## 2. How do lieder composers fit lines of different syllable counts into two-bar and four-bar phrases in 6/8 and 3/4? Declamatory schemas

### Takeaway
The default is one poetic stress per tactus beat, so a line takes two bars when the bar has two beats (6/8, 2/4) and a tetrameter couplet makes a four-bar phrase; trimeter lines fill three of four beats and leave the fourth as the line-end rest or long note. Malin's schema notation records exactly this (which beat each stress lands on, bar by bar), and the upbeat-versus-downbeat start is decided by whether the verse begins unstressed (iambic/anapaestic) or stressed (trochaic/dactylic).

### Cited Findings
- Malin's notation (Yonatan Malin, *Songs in Motion: Rhythm and Meter in the German Lied*, OUP 2010): each poetic stress is indexed by the beat it falls on, "/" is a barline, "–" is a beat with only a weak syllable or nothing. A trimeter line in simple duple is **[1, 2 / 1 –]**: stresses on beats 1 and 2 of bar one and beat 1 of bar two, beat 2 of bar two empty (pp. 16–17). — [London, review of Malin, MTO 17.2](https://mtosmt.org/issues/mto.11.17.2/mto.11.17.2.london.php)
- Lines normally have three or four stresses (trimeter, tetrameter); feet have two or three syllables. Pentameter "naturally supports a trimeter subcomponent" and is typically fitted into a two-bar / eight-beat frame (Wolf). — [London review](https://mtosmt.org/issues/mto.11.17.2/mto.11.17.2.london.php)
- Tetrameter, common schemas quoted from Malin by Rodgers: **[1 2 / 1 2]** (duple, downbeat start; described as "a common declamatory schema") and **[3 – / 1 – 3 – / 1 –]** (4/4 with upbeat start: stress every half bar, beginning on beat 3; "a common ... schema" within four-bar hypermeasures, Mendelssohn's "Suleika"). — [Rodgers, MTO 17.1](https://mtosmt.org/issues/mto.11.17.1/mto.11.17.1.rodgers.html)
- Triple-metre tetrameter schemas cited from Malin on Hensel's "Maienlied": upbeat-oriented **[3 / 1 – 3 / 1]** (stresses on beat 3, beat 1, beat 3, beat 1: two bars plus pickup, alternating long–short spacing) versus downbeat-oriented **[1, 2, 3 / 1 – –]** (three stresses in bar one, the fourth on the next downbeat, then two empty beats). — [London review](https://mtosmt.org/issues/mto.11.17.2/mto.11.17.2.london.php)
- A non-standard triple schema: Hensel's "Suleika" uses [1 – 3 / 1 – – / 1 – –], which Rodgers notes "is not one of Malin's common schemas"; it compresses four bars into three. — [Rodgers, MTO 17.1](https://mtosmt.org/issues/mto.11.17.1/mto.11.17.1.rodgers.html)
- In Krebs's normative model, each trimeter line occupies two bars and each couplet four; line-end pauses are short after odd lines and longer after even lines. — [Krebs 2014](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.krebs.php)
- Long lines in compound metre (Hensel "Die Ersehnte", 12/8): lines of eleven syllables with three primary stresses put each primary stress on a downbeat; a fifteen-syllable, five-stress line is handled by stretching one word over two bars; dotted-quarter rests close the units. Pentameter conventions (Hallmark & Fehn, as cited): either compress five feet into four metrical units, or declaim in five units plus an extension. — [Rodgers, MTO 17.1](https://mtosmt.org/issues/mto.11.17.1/mto.11.17.1.rodgers.html)
- Breath: where a line would run straight into the next, composers add a bar or beat (Hensel adds a 3/4 bar in "Die Mainacht" because otherwise "the vocalist would have no time to catch a breath"). — [Rodgers, MTO 17.1](https://mtosmt.org/issues/mto.11.17.1/mto.11.17.1.rodgers.html)
- Folk-song baseline: about 95.5% of syllables are set one note per syllable (melisma 4.46%). — [De Castro-Arrazola et al. 2015](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)

### Inferences
(Derived from the schemas above; rhythms written per bar, e = eighth, q = quarter, q. = dotted quarter, h = half. These are my constructions from the cited principles, not quotations.)

**6/8 (two beats per bar; each beat = q. = up to three syllable slots)**
- One stress per dotted-quarter beat. Tetrameter = 2 bars [1 2 / 1 2]; trimeter = 2 bars [1 2 / 1 –] with the last beat a rest or tied note; a tetrameter couplet or trimeter quatrain half = 4 bars.
- Foot → beat filling: trochee (S w) = q e; iamb (w S) = pickup e then q e | ... i.e. the same q–e lilt shifted by one eighth; dactyl (S w w) = e e e; anapaest (w w S) = two-eighth pickup then e e e pattern shifted. Amphibrach falls out as e | q e.
- Syllable capacity: 2–6 per bar; a two-bar line comfortably carries 6–8 syllables in duple-foot verse (q e q e | q e q.) and 9–12 in triple-foot verse (e e e e e e | e e e q.).
- Pickup rule: verse beginning unstressed takes an anacrusis of one eighth (iambic) or two eighths (anapaestic) before the barline; verse beginning stressed starts on the downbeat. The anacrusis length is borrowed from the end of the previous line's final bar, so line-final note + rest + next pickup must sum to one beat.
- Line end: masculine ending → final stress on beat 1 (or beat 2) held as q. or q + e rest; feminine ending (S w) → q e on the last beat, or the unstressed syllable on beat 2 of the bar when the stress is on beat 1 (weaker position, acceptable because strength still falls).

**3/4 (three beats per bar)**
- Two families, matching Malin's two triple schemas: (a) "long–short" [3 / 1 – 3 / 1] or its downbeat twin [1 – 3 / 1 – ...]: stressed syllable h (or q + q rest), unstressed q — the Krebs half+quarter option, also the Ländler/waltz-song lilt; one or two stresses per bar. (b) "even" [1, 2, 3 / 1 – –]: one syllable-stress per quarter, three stresses in a bar, final stress on the next downbeat and a two-beat hole for breath.
- Dactylic/anapaestic verse fits 3/4 one foot per bar (q q q), one stress per bar: a dactylic tetrameter line = 4 bars, final bar h. + rest or h + pickup.
- Iambic tetrameter (8 syllables) in family (a): pickup q | h q | h q | h q | h (rest) → 4 bars, stresses on four successive downbeats. In family (b) with eighths: pickup e | q e... is really 6/8; if the engine finds it wants q e q e, it should relabel to 6/8.
- The specific failure to guard against in 3/4: placing stresses on beats 1 and 3 and unstressed syllables on beat 1 of the following bar. Only [3 / 1] (stress on 3 followed by a stronger stress on 1) is sanctioned.

**General**
- Budget one beat of silence or sustain at every line end; double it at couplet ends (Krebs: longer pause after even lines).
- Keep melisma to a small minority of syllables (about 5%) and reserve it for stressed syllables, preferably near line end.
- When a line has too many stresses for the frame (pentameter in a tetrameter frame), demote the weakest stress (function word) to a non-beat position rather than adding a bar; when too few, elongate the last stressed syllable.

### Gaps
- I could not open Malin's book itself; his full inventory of schemas, and which he gives specifically for 6/8, is known here only through London's and Rodgers's quotations. No frequency table of schemas was found.
- Composer- and genre-specific rhythm claims requested in the brief (siciliana dotted figure in 6/8 or 12/8 in Handel/Purcell/Mozart arias; barcarolle q–e lilt in Schubert/Fauré/Mendelssohn; Ländler/waltz declamation in Schubert/Brahms; Purcell's Scotch-snap setting of English short stressed syllables; Fauré's even syllabic eighths) — no source opened for any of these. Unverified recall: siciliana = dotted-eighth, sixteenth, eighth per beat with the stress on the dotted note; barcarolle = quarter–eighth per beat; both put one stress per dotted-quarter. Temperley & Temperley's "Music-Language Correlations and the 'Scotch Snap'" (*Music Perception* 2011) exists (title seen in search results) but was not read.
- No source found giving syllables-per-bar distributions for art song in 3/4 or 6/8. Computable from OpenScore Lieder (section 3).

## 3. Which corpora have both syllable-aligned lyrics and triple/compound-metre songs, in a parseable format? How many in 3/4 and 6/8?

### Takeaway
Two corpora are immediately usable and commercially safe: OpenScore Lieder (CC0, about 1,350 art songs, roughly 265 in 3/4 and 216 in 6/8, about 370 in English by rough estimate) and the Open Hymnal (mostly US public domain, English, ABC with aligned `w:` lines, about 44 in 3/4 but only 5 in 6/8). The Meertens collections are the only ones with ready-made per-syllable stress, but they are Dutch and non-commercial.

### Cited Findings

| Corpus | Language | Size | Format | Lyrics aligned to notes? | Licence | Where |
|---|---|---|---|---|---|---|
| OpenScore Lieder | German, English, French, others | 1,352 `.mscx` scores in the repo today (README abstract: "over 1,200" songs, "over 100" composers; repo metadata file: 143 composers, 316 sets, 1,454 scores) | MuseScore `.mscx`; script converts to `.mxl` MusicXML | Yes, syllable-level lyrics in the score; plus a plain-text `lc<id>.txt` per song | CC0 1.0 | [GitHub OpenScore/Lieder](https://github.com/OpenScore/Lieder); Zenodo doi:10.5281/zenodo.15450143 |
| Open Hymnal (2014.06 ABC edition) | English | 293 tunes (local count of `X:` headers) | ABC Plus, also MIDI, PDF | Yes: 4,188 `w:` lines, hyphenated per syllable, all verses | Per hymn; most are US public domain in melody, setting, words and translation; exceptions state terms in the ABC file | [openhymnal.org copying page](http://openhymnal.org/copying.html); [ABC file](http://openhymnal.org/OpenHymnal2014.06.abc) |
| MTC-FS-INST 2.0 | Dutch | 18,618 melodies (vocal + instrumental) | `**kern`, MIDI, LilyPond, PDF, txt; no MusicXML | Yes for vocal items (see section 4) | CC BY-NC-SA 3.0 Unported | [liederenbank.nl/mtc](https://www.liederenbank.nl/mtc/) |
| MTC-FS 1.0 | Dutch | 4,120 vocal folk songs | same | Yes | CC BY-NC-SA 3.0 | [same](https://www.liederenbank.nl/mtc/) |
| MTC-ANN 2.0.1 | Dutch | 360 melodies, 26 tune families | same | Yes | CC BY-NC-SA 3.0 | [same](https://www.liederenbank.nl/mtc/) |
| MTCFeatures (derived) | Dutch (+ Essen, mainly German) | MTC-ANN 360; MTC-FS-INST about 18k; Essen 8k+; 81.6 MB | gzip JSON Lines; Python module | MTC: yes with stress; Essen: no lyrics features | CC BY-NC-SA 3.0 | [Zenodo 3551003](https://zenodo.org/records/3551003) |
| Schubert Winterreise Dataset v2.1 | German | 24 songs | MusicXML, MIDI, Sibelius, PDF; lyrics as text files; audio | Not stated; no lyric-to-note annotation listed | CC BY 3.0 | [Zenodo](https://zenodo.org/records/3968389/latest) |
| OpenEWLD (from Wikifonia) | mostly English popular song | not stated on page | compressed MusicXML + SQLite metadata | Lyrics as separate txt "where available" | Scores/lyrics "intended to contain only Public Domain content"; code MIT | [GitHub 00sapo/OpenEWLD](https://github.com/00sapo/OpenEWLD) |
| DALI | pop, multi-language | not stated on page | audio-time-aligned notes with text at note, word, line, paragraph level | Aligned to audio time, not a score; no syllable level or bar structure stated | non-commercial research only, CC BY-NC-SA 4.0; files restricted (request) | [Zenodo 2577915](https://zenodo.org/records/2577915) |
| Hayes textsetting data | English folk verse | 346 lines (+ 640-line set) | tab-delimited text: stress transcription + grid setting | Yes (syllable → grid position), no pitches | not stated | [brucehayes.org/Textsetting](https://brucehayes.org/Textsetting) |

Counts by metre (local counts):
- OpenScore Lieder, first time signature of each of the 1,352 `.mscx` files (regex over `<TimeSig>`): 4/4 421; **3/4 265**; 2/4 237; **6/8 216**; 2/2 58; 3/8 49; **9/8 33**; **12/8 20**; 6/4 18; 3/2 11. Counting songs that use the metre anywhere: 3/4 332; 6/8 247; 9/8 50; 12/8 30; 3/8 63. Only 1 file has no lyric elements; 254,821 lyric-syllable elements in total. Source data: [OpenScore/Lieder](https://github.com/OpenScore/Lieder), shallow clone 2026-11-27.
- OpenScore Lieder language, rough stop-word guess on the `lc*.txt` lyric files (1,355 files): German about 638, **English about 369**, French about 280, other/undetermined about 68. Approximate; not official metadata. Source data: [OpenScore/Lieder](https://github.com/OpenScore/Lieder).
- Open Hymnal 2014.06 ABC, `M:` fields: 4/4 196; **3/4 44**; 6/4 10; 3/2 7; **6/8 5**; 2/4 5; 2/2 3; **9/8 1**; free/none about 18. Source data: [OpenHymnal2014.06.abc](http://openhymnal.org/OpenHymnal2014.06.abc). A 2026.11 edition exists ([PDF](http://openhymnal.org/OpenHymnal2026.11.pdf)); I counted the older ABC file, so current totals will be somewhat higher.

Other facts:
- OpenScore Lieder citation: Gotham, M. R. H., & Jonas, P. (2022). The OpenScore Lieder Corpus. *Music Encoding Conference Proceedings 2021*, 131–136, doi:10.17613/1my2-dm23. The repo also ships automatic Roman-numeral analyses (`analysis_automatic.rntxt`), which is the link to the "When in Rome" meta-corpus. — [OpenScore/Lieder](https://github.com/OpenScore/Lieder)
- Winterreise dataset citation: Weiß, Zalkow, Arifi-Müller, Müller, Koops, Volk, Grohganz, "Schubert Winterreise Dataset: A Multimodal Scenario for Music Analysis", *ACM Journal on Computing and Cultural Heritage* 14(2); the Zenodo page gives the year inconsistently (2021 in notes, 2024 in metadata). — [Zenodo](https://zenodo.org/records/3968389/latest)
- Essen: the MTCFeatures documentation states that for Essen melodies "no lyrics features are present". — [MTCFeatures melody representation](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html)

### Inferences
- Best fit for an English-target engine: (1) the English subset of OpenScore Lieder (art song; expect roughly 70 in 3/4 and 60 in 6/8 if metre is distributed as in the whole corpus — an extrapolation, not a count) and (2) Open Hymnal for 3/4. English 6/8 with aligned text is the scarce resource; OpenScore's English songs are the main open supply.
- German and French OpenScore songs are still valid for learning rhythm templates per foot type (schemas are metre-and-foot facts more than language facts), but English stress rules should be applied strictly on top (section 1: English alignment is stricter than French).
- Winterreise is small (24) and its songs are already inside OpenScore Lieder's Schubert holdings in all likelihood, so it adds little for text setting.
- DALI is not useful for this purpose: no bars, no syllables, non-commercial.
- None of the commercially usable corpora has stress marks; stress must be added with a pronouncing dictionary (CMUdict for English) after parsing syllables from the lyric hyphenation.

### Gaps
- Not checked (ran out of budget); treat as leads, with unverified recall noted:
  - Essen Folksong Collection as distributed in `**kern` (KernScores) — MTCFeatures says no lyrics features; unverified recall is that the kern files carry melody and phrase marks only, with licence restricting to non-commercial research use.
  - CPDL (cpdl.org): large, per-edition licences (CPDL licence, CC variants, public domain), files mostly PDF plus assorted MusicXML/MuseScore/Finale sources; no bulk download or uniform format known. Unverified.
  - Hymnary.org: metadata and texts database; no open bulk notes-plus-lyrics download confirmed.
  - Sacred Harp: a GitHub repo "edjw/Sacred-Harp-datasets" appeared in search results but was not opened; whether it has notes aligned to text is unknown.
  - Nottingham dataset: ABC folk tunes; unverified recall is that it is instrumental with chords and no lyrics.
  - Josquin Research Project / other Humdrum collections (humdrum-data on GitHub): Renaissance polyphony with text underlay in `**text` spines; mensural, not relevant to 3/4 and 6/8 song; licence not checked.
  - Wikifonia itself is offline; OpenEWLD is the public-domain remnant. Its size and metre distribution were not obtained.
  - "When in Rome" licence details not checked.
- Exact English-song counts by metre in OpenScore Lieder: computable in minutes by joining my two local counts; not done.

## 4. Meertens MTC-FS / MTC-FS-INST: stress marks per syllable, phrase boundaries, licence

### Takeaway
Yes to both, via the MTCFeatures release: each note carries the lyric syllable, a binary `wordstress` flag, word-end, content-word, rhyme and melisma flags, phrase index/end, time signature and beat strength. Licence is CC BY-NC-SA 3.0 Unported — research use only, not commercial, and share-alike.

### Cited Findings
- Per-note lyric features in MTCFeatures (vocal melodies; set at the first note of a melisma): `lyrics` (syllable, hyphens mark word continuation), `noncontentword` (Dutch function word), `wordend`, `wordstress` ("whether the syllable is stressed"), `phoneme`, `rhymes`, `rhymescontentwords`, `melismastate` (start / in / end). — [MTCFeatures melody representation](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html)
- Phrase features: `phrase_ix`, `phrasepos` (0.0–1.0), `phrase_end`, `beatinphrase`, `beatinphrase_end`. — [same](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html)
- Metre features: `timesignature`, `beatstrength` (music21 metric weight, 0–1], `metriccontour`, `imaweight` (Inner Metric Analysis), `beat`, `beat_fraction_str`, `beatinsong`. — [same](https://pvankranenburg.github.io/MTCFeatures/melodyrepresentation.html)
- Stress is not in the original `**kern` transcriptions: De Castro-Arrazola et al. state they added it by looking words up in the e-Lex lexicon (binary, no secondary stress), discarding words whose syllable count did not match. — [De Castro-Arrazola et al. 2015](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)
- Corpus sizes and formats: MTC-FS-INST 2.0 (2018) 18,618 melodies; MTC-FS 1.0 (2014) 4,120 vocal songs; MTC-ANN 2.0.1 360; MTC-LC 1.0 4,830; `**kern`, MIDI, LilyPond, PDF, txt. — [liederenbank.nl/mtc](https://www.liederenbank.nl/mtc/)
- Licence wording on the site: "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License". The Zenodo feature release carries the same licence. Download is via a form at liederenbank.nl/mtc/download.php; features via Zenodo doi:10.5281/zenodo.3551003 (van Kranenburg 2019, v1.1). — [liederenbank.nl/mtc](https://www.liederenbank.nl/mtc/); [Zenodo 3551003](https://zenodo.org/records/3551003)
- Language: Dutch; mostly field recordings 1950s–1990s plus 19th/20th-century songbooks. — [De Castro-Arrazola et al. 2015](https://vdca.netlify.com/pdf/decastro-arrazola2015_fma-dutch-textsetting.pdf)

### Inferences
- MTCFeatures is the only resource found where "percent of stressed syllables on the downbeat in 6/8 vs 3/4" can be computed without any preprocessing (filter by `timesignature`, cross-tabulate `wordstress` against `beat`). The resulting numbers may be used as design evidence; the data itself must not ship in or train a commercial product under NC-SA.
- Dutch stress behaves like English and German (Germanic, lexical stress, many trochaic words), so the positional statistics should transfer better than French would.

### Gaps
- How many MTC-FS-INST vocal melodies are in 6/8 and 3/4, and how many carry the `wordstress` feature: not obtained (the documentation PDF and feature index were blocked from fetching). Unverified recall: 6/8 is the single most common metre in the Dutch collection.
- Whether the MTCFeatures `wordstress` values are the same e-Lex-derived values as in the 2015 paper is not stated on the feature page.
