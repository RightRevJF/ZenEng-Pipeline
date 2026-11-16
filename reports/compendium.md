---
title: "Luthier research compendium"
subtitle: "Every report and study written for the engine since the research began, 15 November 2026"
author: "Words and music: Jason Bryant"
---

This file gathers, in the order they were written, the research reports, studies, atlas and test report prepared for Luthier while the engine was offline. Each part is reproduced whole. The fix list ("Luthier fix list since v7") and the avenues document are separate. Scripts and data tables are in the repository RightRevJF/ZenEng-Pipeline under reports/, research_notes/, studies/, tables/metre_atlas and songs/p63.

# Part 1. Time signature research and song data (research report)

## SymbTr and Lieder fill Luthier's metre gaps

Two open corpora cover most of what Luthier is missing, and no single source covers all of it. **OpenScore Lieder** (CC0, per-note lyrics on 1,351 of 1,352 scores) supplies the sung compound metres: 50 scores containing 9/8 and 30 containing 12/8, plus 297 English-language songs that take English text-setting well beyond hymns ([OpenScore/Lieder](https://github.com/OpenScore/Lieder)). **SymbTr v2.4.3**, the Turkish makam corpus, supplies the sung additive metres with one lyric syllable per note: about 318 lyric-bearing pieces in 9/8 (mostly aksak), 47 in 5/8, 26 in 7/8 plus 18 in 7/4, and 187 in 10/8. Its licence, though, is CC BY-NC-SA 4.0 ([github.com/MTG/SymbTr](https://github.com/MTG/SymbTr)). The Finnish folk-tune archive is the only large pool of **5/4** (499 tunes), but it has no aligned lyrics and is licensed for non-commercial research only ([Catafolk index](https://github.com/bacor/catafolk)). **11/8 and 13/8 have no usable sung corpus anywhere**: SymbTr holds 1 and 4 pieces. Those metres have to be built from grouping rules rather than learned from counts. On the literature side, three findings matter most for generation. First, additive metres are sequences of 2- and 3-pulse beats with stable, tradition-specific positions for the long beat. Second, compound metres differ from their simple twins (6/8 vs 3/4, 12/8 vs 6/8) more in phrase-level grouping than in within-beat rhythm. Third, text-setting rules depend on language more than on metre: English aligns stress to beat strictly, French mainly at line ends, Bulgarian folk song hardly at all, and Finnish runosong by syllable length. The team's own hymn measurements in 3/4 and 6/8 are among the few triple/compound English stress figures that exist, because the published corpora restricted themselves to 4/4.

### Corpus weights confirm the textbook hierarchy, but only 4/4 has been measured

The one fully recovered numeric onset profile is the Huron and Ommen tally of **75,242 onsets in Essen 4/4 songs**, printed by Murphy ([Murphy 2020, *Journal MusMat*](https://musmat.org/wp-content/uploads/2020/06/05-Scott.pdf)). The downbeat takes **25.5%** of onsets. Beat 3 takes 19.0%, beat 4 17.9% and beat 2 13.6%. Eighth off-beats take 2.8 to 7.9%, and sixteenth positions under 1%. Two details are useful for checking Luthier's own Essen-derived 4/4 table. Off-beat eighths after beats 2 and 4 are about 2.5 times as common as those after beats 1 and 3. The sixteenth just before a beat is 15 to 30 times as common as the sixteenth just after it, which is the dotted-eighth-plus-sixteenth signature; the reverse "Scotch snap" figure is nearly absent from this German-dominated sample. Haydn string quartets rank the 16 positions almost identically: only 2 of 120 pairwise orderings differ ([Murphy 2020](https://musmat.org/wp-content/uploads/2020/06/05-Scott.pdf)). That gives a concrete benchmark for "how close is close enough" when the engine compares generated onset histograms with corpus ones. Palmer and Krumhansl (1990) plotted equivalent profiles for 2/4, 3/4, 4/4 and 6/8 from classical keyboard music, but this is known only through a secondary summary and no numbers were recovered ([London, Polak & Jacoby 2016](https://core.ac.uk/download/83231804.pdf)). **No published numeric profile for 3/4, 6/8, 3/8, 9/8, 12/8, 6/4 or 3/2 was found.** The team's measured Essen weights for those metres are therefore ahead of the accessible literature, not behind it.

The hierarchy does not hold everywhere. In 913 notated Turkish makam pieces, onset histograms did not match the usul accent patterns. In Malian jembe music, a four-beat ternary cycle "analogous to 12/8" (about 42,297 onsets from 15 performances), on-beat positions other than the downbeat are articulated *less* often than the upbeats just before them ([London, Polak & Jacoby 2016](https://core.ac.uk/download/83231804.pdf)). For Luthier this means a 12/8 blues or gospel profile cannot be inherited from 6/8 European folk song and assumed correct. No corpus statistics for sung 12/8 blues, gospel or doo-wop were found at all.

Two findings separate compound metres from their simple twins. In Dutch folk tunes, melodies of the same tune family notated in 6/8 and in 3/4 fell to very low similarity ranks (100 to 128). The authors attribute this to "a very different rhythmic structure expressed by a different meter notation" ([Volk et al., ISMIR 2007](https://archives.ismir.net/ismir2007/paper/000293.pdf)). In other words, transcribers' choice between 3+3 and 2+2+2 reflects real rhythm, and the engine is right to keep separate tables for 6/8 and 3/4. The other side of this is that jigs (6/8) and slides (12/8) are confused with each other in Irish audio classification, while compound tunes show autocorrelation peaks at multiples of three subdivisions ([Beauguitte, Duggan & Kelleher](https://core.ac.uk/download/301311609.pdf)). The inference is that 12/8 vs 6/8 is mostly a matter of bar and cadence placement over four dotted-quarter beats rather than a different within-beat vocabulary. Temperley and Temperley's level scheme gives a ready way to assign strength: the tactus (level 2) is the quarter in 2/4, 3/4 and 4/4 and the dotted quarter in 6/8, 9/8 and 12/8. Level 3 is the bar in 2/4, 3/4, 6/8 and 9/8 but the half-bar in 4/4 and 12/8, and level 4 is the bar in 4/4 and 12/8 ([Temperley & Temperley 2013](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)).

London's theory adds one design rule. A time signature is not a fixed felt metre: the same notated structure is heard differently at different tempi, hence his "tempo-metrical types" and "many meters hypothesis" ([London, *Hearing in Time*, introduction](https://musikwissenschaft.univie.ac.at/fileadmin/user_upload/i_musikwissenschaft/Forschung/Vortragsreihen/J_London_Hearing_in_Time_Intro.pdf)). Luthier should key each table on time signature plus tempo band. Fast 3/8 is felt as one beat per bar. 6/4 (2×3) and 3/2 (3×2) share a bar length but not a grouping. This is theory-derived; no study comparing listener perception or corpus rhythm for 3/8 vs 3/4 or 6/4 vs 3/2 was retrieved. For a realistic performance ceiling, metre-inference models trained on Essen recover the notated metre about **67 to 71%** of the time at Markov orders 1 to 4 ([van der Weij, Pearce & Honing 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5439009)). That figure is a sensible target if the engine tests whether its generated melodies "sound like" the metre they claim.

### Additive metres are chains of 2s and 3s whose long beat lands

The Balkan and Turkish additive metres all sit on a fast, roughly equal pulse grouped into short (2-pulse) and long (3-pulse) beats. The standard forms are 5 = 2+3 or 3+2, 7 = 2+2+3 or 3+2+2, 9 = 2+2+2+3, 11 = 2+2+3+2+2 or 2+2+2+2+3, and 13 = 2+2+2+3+2+2 and variants ([Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)). The placement of the long beat is fixed by dance type, not free. Hristov's 1913 Bulgarian theory, now translated, says paidushka (5 = 2+3) puts the elongated part last with a "comparatively stronger" accent, and that the reverse order "is not observed in songs". Rŭchenitsa (7 = 2+2+3) is long-last, while makedonsko horo puts the long beat first (3+2+2) ([Hristov, trans. Goldberg, MTO 30.4](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)). Singer's Macedonian work and Rice's Bulgarian work document 3+2+2 and 2+2+3. Fracile's survey of about 6,000 transcriptions lists those two **but not 2+3+2**, so a Balkan-style generator should essentially never emit 2+3+2 in 7/8. This rests on Clayton's summary, not the original ([Clayton, MTO 26.1](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)). London's well-formedness constraints, also known here only through Clayton, give the encodable model: an isochronous pulse level, beats drawn from {2, 3}, maximal evenness (spread the 3s out among the 2s), beat rates of 400 to 1200 ms, and cycles no longer than about 2 s ([Clayton, MTO 26.1](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)).

The timing of short and long beats matters only at render time, but the measurements disagree enough to state ranges rather than a single ratio. Theory gives 2:3, a long/short ratio of 1.5. Goldberg timed 18 tŭpan recordings by 9 players and found rŭchenitsa and elenino horo within about 10 ms of 2:3, with a worst case of 23 ms. Group-initial beats ran slightly long and mid-group beats slightly short, and in Pirin rŭchenitsa the first bar of each two-bar pair was 19 ms longer than the second ([Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)). Bernacki's two Pirin-Macedonian 3+2+2 songs gave beat proportions of 38:29:33 and 44:26:30 against a theoretical 42:29:29. That works out to long/short ratios of about 1.24 and 1.59, with the first short beat the shortest in over 80% of cycles; he concludes these "cannot be described by a 2:3 beat ratio" ([Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)). **Bernacki's result rests on two YouTube recordings**, so it shows that variation exists rather than how often. A defensible humanisation band is long/short 1.2 to 1.7, centred on 1.5, with symbolic durations kept as exact 2- and 3-pulse values. Tempo is bound to the type: rŭchenitsa's first short beat runs about 245 bpm (a two-bar unit near 35 bpm), and elenino horo's first beat about 138 bpm ([Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)). Rŭchenitsa short beats therefore fall below London's 400 ms beat floor. For phrasing the felt beat is the 2/3 group, but at that speed listeners track the whole bar or two-bar unit.

The melodic evidence is thin. Heavy right-hand (düm) strokes mark group onsets in both Bulgarian and Turkish accompaniment ([CompMusic usul examples](https://compmusic.upf.edu/examples-usul-mmt)). In the related North Indian 3+2+2 cycle rūpak, beats 3, 5 and 7 are subdivided more than 95% of the time, but the long first beat only 28% (42 recordings), so the long group often carries one held note ([Clayton, MTO 26.1](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)). **No corpus study of melodic onset density by pulse position in Balkan or Turkish aksak was found.** SymbTr's validated bar lines would allow the team to measure this directly, and that would be a genuinely new result.

Perception argues for redundancy. North American adults failed to detect disruptions in 2+2+3 Balkan tunes that Bulgarian and Macedonian adults, and 6- to 7-month-old North American infants, detected ([EurekAlert summary of Hannon & Trehub 2005](https://www.eurekalert.org/news-releases/602135)). Western-only adults also missed metre violations in complex Turkish metres while catching them in simple ones ([Kalender, Trehub & Schellenberg 2013](https://link.springer.com/doi/10.1007/s00426-012-0427-y)). The immigrant-adult group numbered only 17 and the Hannon and Trehub figures come from a press release, so treat this as directional. For a Western audience, Luthier should keep one grouping throughout a song, put melodic onsets on group starts and avoid mid-song regrouping unless it is a deliberate effect.

### Lyric stress follows language rules more than metre rules

English sets stress to strong beats strictly, everywhere in the line. Palmer and Kelly found compound nouns took the stronger metrical accent on their first syllable in 43 of 48 Gilbert and Sullivan cases and 96 of 105 art-song cases, about 90%. Adjective-noun phrases were set far less reliably (83% in one corpus, 42% in the other), so lexical stress is near-hard and phrasal stress soft ([Palmer & Kelly 1992](https://www.examenapium.it/cs/biblio/Palmer1992.pdf)). Hayes and Kaun's English folk-song data show matching tightening toward boundaries ("beginnings free, endings strict"). Only about 1.1% of intonational-phrase endings mismatched, against 3.9% at phonological-phrase ends. Some 10.9% of settings were "headless", leaving opening positions empty as an anacrusis or rest ([Hayes & Kaun 1996](https://www.brucehayes.org/papers/HayesAndKaunMetrics1996.pdf)). Hayes's constraint grammar ranks avoiding lapses (three empty grid positions in a row) above keeping stressless syllables off strong positions. It reproduced the consultants' favourite setting on **70.6%** of lines against 23.1% for Halle and Lerdahl's algorithm ([Hayes 2009](https://brucehayes.org/Textsetting/HayesTextsettingAsConstraintConflict.pdf)). The paper reports 364 lines and Hayes's web page 346; the source has a typo somewhere. The size of the language effect is measurable. English stress-meter alignment (SMAV) is 1.15 against 0.77 for French. Yet 97% of French line-final syllables are stressable, and without them French alignment drops to 0.49 ([Temperley & Temperley 2013](https://davidtemperley.com/wp-content/uploads/2015/11/temperley-temperley-jasa.pdf)). **The English comparison set is only ten songs.**

Style shifts English rules sharply. In 80 rock songs, 33.3% of stressed syllables are syncopated. Most of them (77% at eighth level) anticipate beats 1 and 3 by an eighth, and the rate rises with tempo and year. The 19th-century English song comparison set had none (0 of 602) ([Tan, Lustig & Temperley 2019](https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf)). In 679 pop lead sheets, downbeats and half-beats strongly favour stressed syllables, and 55% of primary-stress notes are longer than the song's mean note ([Nichols et al. 2009](https://archives.ismir.net/ismir2009/paper/000084.pdf)). Both studies analysed **only 4/4 (and 2/4)**. Hayes and Kaun forced binary chanting, and Temperley and Temperley reported no compound-metre breakdown. That leaves no published quantitative study of English text-setting in 3/4, 6/8, 9/8 or 12/8. The team's hymn figures (81% of stressed syllables on the 3/4 downbeat, 84% on the two main beats of 6/8) are therefore a primary measurement, not a replication. The triple and compound rules Luthier uses (one syllable per eighth for anapests and dactyls in 6/8; stressed-quarter plus unstressed-eighth for iambs and trochees in 6/8) are extrapolations from binary grid models that the Lieder English subset can now test.

Outside English the governing variable changes. Bulgarian folk verse counts syllables and ignores stress, even though Bulgarian stress is contrastive. Of 89 coded songs, 50 use 8-syllable lines with a fixed 5+3 caesura in 34 of them, and the same text can be sung in several aksak metres: lesno 7/8, rŭchenitsa 7/8, pajdushko 5/8, dajchovo 9/8 or kopanitsa 11/8 ([Hayes & Schuh, Bulgarian metrics handout](https://www.brucehayes.org/251HayesSchuhMetrics/handouts/12_bulgarian_metrics.pdf)). This is a small, teaching-handout sample. Luthier should map Bulgarian-style lines to whole bars (for example two bars of 7/8 per 8-syllable line, with the caesura on a bar or beat boundary) rather than forcing stress onto the long beat. Finnish Kalevala metre is governed by syllable length. Stressed syllables must be long on the downbeat and short on the upbeat, with strictness rising through the line until foot 4 has no violations ([Kiparsky 1968](https://www.brucehayes.org/251metrics/papers/Kiparsky1968Kalevala.pdf)). Sung runosong is most often in 5/4 or 4/4 ([Finnish Music Quarterly](https://fmq.fi/articles/rune-singing-the-musical-vernacular)), and Archangel Karelian solo singing mostly used a "five-beat, two-line melody" ([Kallio 2017](https://journal.oraltradition.org/wp-content/uploads/files/articles/31ii/07_31.2.pdf)). The exact 8-syllables-into-5-beats template (lengthening the final syllables) comes from a non-peer-reviewed university page and remains unverified against Launis's transcriptions ([UAF](https://www.uaf.edu/music/cms/finnish-four-beat-line.php)). In Ottoman song, Bektaş's study of 466 beste found that usul correlates with classes of quantitative aruz metre rather than individual metres ([Bektaş 2005](https://repository.bilkent.edu.tr/items/744814c8-160c-4047-a98f-16a605d31675/full)). For SymbTr lyric tables, that means syllable weight (long vs short) is the property to track against beat position, not stress.

### Ranked datasets for the missing metres and English lyrics

The table ranks sources by how much they fill the stated gaps: sung 9/8, 12/8, 5/8, 5/4, 7/8 and 11/8, and English lyric-aligned songs beyond hymns. Most counts were **computed by the research team from cloned repositories on 2026-11-15** and are not published figures. "Any" means the score contains that signature anywhere.

| Rank | Dataset | Gap metres (counts) | Lyrics aligned? | Size, format | Licence | How to get |
|---|---|---|---|---|---|---|
| 1 | OpenScore Lieder | any: 9/8 50, 12/8 30, 6/8 247, 3/8 63, 3/2 25, 6/4 28, 5/4 4, 7/8 3, 5/8 1. English subset (297): 6/8 49, 9/8 12, 12/8 5, 3/8 13, 3/2 10, 7/8 3, 5/4 2 | Yes, per note (1,351/1,352). EN 335, DE 776, FR 319 by metadata | 1,352 .mscx / 1,462 .mxl, voice + piano | **CC0 1.0** | `git clone github.com/OpenScore/Lieder` ([repo](https://github.com/OpenScore/Lieder)) |
| 2 | SymbTr v2.4.3 | with lyrics, by written metre: 9/8 318, 9/4 116 (aksak usul alone: 284 vocal, a few written 9/4), 5/8 47, 7/8 26, 7/4 18, 10/8 187, 14/8 28, 13/8 4, 15/8 3, 11/8 1 | Yes, one syllable per note row (about 1,550 vocal pieces) | 2,200 pieces; tab-separated txt, MusicXML, MIDI | **CC BY-NC-SA 4.0** (Zenodo says "Other (Open)"; conflict) | `git clone github.com/MTG/SymbTr` or Zenodo DOI 10.5281/zenodo.160552 ([repo](https://github.com/MTG/SymbTr), [Zenodo](https://zenodo.org/records/160552)) |
| 3 | Digital Archive of Finnish Folk Tunes | any: 5/4 499 (409 pure), 5/8 63, 5/2 61, 9/8 24, 15/8 24, 7/8 14, 12/8 6, 11/8 2, plus labelled 2+2+3/8, 3+2+2/8, 2+3+2/8 | No (lyrics only in online previews) | 8,613 tunes; MIDI / Matlab | **Non-commercial research**, attribution | esavelmat.jyu.fi download page; direct file link not confirmed ([download page](https://esavelmat.jyu.fi/collection_download.html), [Catafolk metadata](https://github.com/bacor/catafolk)) |
| 4 | PDMX | Not counted; must be filtered by time signature | `has_lyrics` / `n_lyrics` flags; lyrics in MusicXML | 254,077 MusicXML (222,856 "no_license_conflict") | CC BY 4.0 record; **per-song licences vary**; paper inconsistent | Zenodo DOI 10.5281/zenodo.15571083 (mxl 1.9 GB, CSV 225 MB) ([Zenodo](https://zenodo.org/records/15571083)) |
| 5 | OpenEWLD | 6/8 13, 12/8 1, 3/2 1, 6/4 1 (mostly 4/4, 2/2, 3/4) | Yes, 464/502 English lead sheets | 502 .mxl | **MIT** | `git clone github.com/00sapo/OpenEWLD`; ignore its metadata time signatures, which default to 4/4 ([repo](https://github.com/00sapo/OpenEWLD)) |
| 6 | Creighton, *Songs and Ballads from Nova Scotia* | 6/8 51, 5/4 1, 7/4 1 | No | 152 English ballads, **kern | Not stated | `git clone github.com/craigsapp/creighton-nova-scotia` ([repo](https://github.com/craigsapp/creighton-nova-scotia)) |
| 7 | Greek Folk Music Dataset (Aegean syrtos/balos) | Metres not stated | Yes, per the record | about 26 MB; MIDI, MuseScore, lyrics files | **CC BY 4.0** | Zenodo DOI 10.5281/zenodo.15470305 ([Zenodo](https://zenodo.org/records/15470305)) |
| 8 | Meertens Tune Collections + MTCFeatures | Not counted | Lyric features per note incl. `wordstress` (Dutch) | about 18,000 melodies; **kern, MIDI, feature JSON | Features **CC BY-NC-SA 3.0**; raw-file licence unverified | liederenbank.nl/mtc; `github.com/pvankranenburg/MTCFeatures` ([repo](https://github.com/pvankranenburg/MTCFeatures)) |
| 9 | Full Essen (CCARH GitHub) | Europe any: 6/8 814, 3/8 321, 3/2 137, 6/4 132, 9/8 6, 5/4 4, 7/8 1, 5/8 1; no 12/8 | No (0 files with text spines) | 8,473 **kern | **CCARH: single-user, academic research, no commercial derivatives** | `git clone github.com/ccarh/essen-folksong-collection` ([repo](https://github.com/ccarh/essen-folksong-collection)) |
| 10 | Hayes text-setting data | English folk lines on a 16-position grid (binary only) | Stress and grid position per syllable, no pitches | 640 lines + consensus-setting file | Not stated | [FolkLine.txt](https://brucehayes.org/papers/FolkLine.txt), [Hayes 2009 data](https://brucehayes.org/Textsetting/DataForHayesTextsettingAsCC.txt) |
| 11 | Small kern sets: Child Ballads (38), Erk *Liederschatz* (232) | Child: 6/8 4, 5/4 2, 9/8 1. Erk: 6/8 28, 3/8 18, 9/8 1, 5/4 1 | No (Erk: 2 files) | **kern | Unknown / not stated | [child-ballads](https://github.com/humdrum-tools/child-ballads), [erk-liederschatz](https://github.com/craigsapp/erk-liederschatz) |
| 12 | Dick Atlee Balkan page | about 35 tunes in 5, 7, 9, 11, 15, 18, 22 counts with explicit q/s groupings | Not stated; mostly dance tunes | ABC, MIDI | **None stated**; many links broken | [dickatlee.com/music/balkan](https://dickatlee.com/music/balkan) |

Mapped onto the gaps, the picture is uneven. **Sung compound 9/8 and 12/8 with lyrics** come almost entirely from Lieder (50 and 30 scores, English 12 and 5). That is enough for onset tables in German plus English, but thin for English-only stress tables in 12/8. The Lieder 9/8 scores are presumably compound triple (3+3+3), but the grouping was not checked. **Sung 9/8 aksak** is SymbTr's strongest suit, at about 284 vocal aksak pieces plus smaller usuls written in 9/8 (evfer, çifte sofyan, raks aksağı, oynak, aydın). The usul row gives only the cycle length, not the 2+2+2+3 grouping, so the grouping must come from an external usul table or be inferred from onset density ([github.com/MTG/SymbTr](https://github.com/MTG/SymbTr)). These smaller usuls' groupings were not verified and should not be assumed to be 2+2+2+3. **5/8** has about 50 lyric-bearing türk aksağı pieces in SymbTr and 63 unlyricised Finnish tunes. **5/4** is Finnish (499) with negligible lyric-aligned support (Lieder 4, SymbTr 3). **7/8** has about 44 SymbTr vocal pieces (devr-i hindî and devr-i turan, both 7/8 and 7/4), 14 Finnish tunes plus a few with explicit additive signatures, and 3 Lieder scores. **11/8 and 13/8** are effectively empty (SymbTr 1 and 4, Finnish 2 in 11/8). **English lyric-aligned songs beyond hymns** come to roughly 760 aligned scores from Lieder EN (297) and OpenEWLD (464), with PDMX as the route to thousands more once filtered.

Several promising-sounding sources should be rejected. **The Session's data dump now forbids processing "with Large Language Models"**, including "utilizing LLM tools", and it is instrumental anyway ([TheSession-data LICENSE](https://github.com/adactio/TheSession-data)). Yu et al.'s 265,020 syllable-note pairs from Lakh MIDI carry no bar or time-signature field, so they cannot feed per-metre tables ([yy1lab repo](https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation)). DALI (CC BY-NC-SA 4.0) and the HookTheory release (CC BY-NC-SA 3.0) are audio-aligned and lack score-level metre ([DALI](https://github.com/gabolsgabs/DALI); [Donahue et al.](https://ar5iv.labs.arxiv.org/html/2212.01884)). The Sacred Harp datasets are metadata only, although their time-signature column shows 6/4 plus 3/2 at about 11% of the 2025 edition (45 + 23 of 590), a useful prior for hymn-style triple metres ([edjw/Sacred-Harp-datasets](https://github.com/edjw/Sacred-Harp-datasets)). Lanphier's Bulgarian songbook is PDF and MP3 only. The Persian Radif corpus deliberately excludes metric pieces ([arXiv 2507.10456](https://arxiv.org/html/2507.10456v1)). No open, lyric-aligned symbolic corpus of Bulgarian, Macedonian, Greek (beyond the Aegean set), Romanian, Serbian or Irish sung song was found.

### Licence terms decide which tables Luthier can keep

Only three of the useful sources are clean for any use: **OpenScore Lieder (CC0), OpenEWLD (MIT) and the Greek Aegean set (CC BY 4.0)**. PDMX is CC BY 4.0 at the record level, but 12.29% of its songs have conflicting licence metadata, and the paper itself labels the corpus both "CC-0 / Public Domain" and CC-BY ([Zenodo 15571083](https://zenodo.org/records/15571083); [arXiv 2409.10831](https://arxiv.org/html/2409.10831v2)). Any PDMX subset should be restricted to the "no_license_conflict" rows and filtered on the per-song licence column.

The additive-metre sources are all encumbered. SymbTr's README specifies CC BY-NC-SA 4.0, while Zenodo lists "Other (Open)" and the CompMusic site footer says CC BY-NC-ND 3.0 ([SymbTr README](https://raw.githubusercontent.com/MTG/SymbTr/master/README.md); [CompMusic corpora](https://compmusic.upf.edu/index.php/corpora)). The safest reading is the most specific one, non-commercial and share-alike. The Finnish archive is "available for research purposes (that is, noncommercial)" ([esavelmat download page](https://esavelmat.jyu.fi/collection_download.html)). The MTC features are CC BY-NC-SA 3.0. Whether derived statistical tables (onset weights, syllable-to-beat probabilities) count as adaptations under NC-SA is a legal grey area the research did not resolve. If the ZenEng web app is or becomes commercial, tables derived from SymbTr, the Finnish archive or MTC need either permission from the rights-holders or a clean-room rebuild from CC0 and public-domain material.

Two licence issues also touch work the team has already done. The full Essen release carries the CCARH licence: "for personal use (single-user) only", "only for the purpose of academic research", and no "derivative editions intended for commercial distribution" ([license.txt](https://github.com/ccarh/essen-folksong-collection)). The research did not check music21's own redistribution terms for its bundled Essen subset, so the team should confirm whether its existing Essen-derived tables inherit this restriction. The Open Hymnal GitHub mirror carries no licence file ([mzealey/openhymnal](https://github.com/mzealey/openhymnal)). The hymns themselves are largely public domain, but the encodings' terms were not verified because openhymnal.org was unreachable. Creighton, Child Ballads, Erk, the Hayes data files and the Atlee ABC page state no licence at all.

### What Luthier should encode, with evidence grades

The table condenses the findings into encodable defaults. "Measured" means a corpus or performance figure from a cited source. "Team" means the team's own existing measurements. "Inferred" means a design extrapolation from theory or neighbouring data, which needs testing against the datasets above.

| Metre | Beat template | Weight and timing defaults | Text-setting default | Evidence |
|---|---|---|---|---|
| 3/4 | 3 quarter beats | Downbeat strongest; table already measured from Essen | Stress on downbeat (team 81%); two-syllable feet either fill beats 1–2 and hold, or stress-as-half-note with beat 3 as pickup | Team; settings inferred |
| 3/8 | 1 felt beat per bar at fast tempo | Bind to a tempo band; treat 2- and 4-bar units as hypermetre | One stress per bar | Inferred (London theory) |
| 3/2 vs 6/4 | 3×2 vs 2×3 | Keep separate grouping templates; 6/4 + 3/2 about 11% of Sacred Harp | Hymn-style, as 3/4 and 6/8 respectively | Measured prior; templates inferred |
| 6/8 | 2 dotted-quarter beats, each 3 eighths | Distinct from 3/4 (Dutch IMA result); tactus = dotted quarter | Stress on the two main beats (team 84%); anapests and dactyls one syllable per eighth; iambs and trochees long-short | Team + measured; syllable patterns inferred |
| 9/8 compound | 3 dotted-quarter beats | Build from 6/8 beat-level patterns; learn from Lieder | As 6/8, three stresses per bar | Inferred; data in Lieder (50) |
| 12/8 | 4 dotted-quarter beats; level 3 = half-bar | Mark through cadence and bar placement, not new within-beat rhythms; blues/gospel profile genre-specific and unmeasured | As 6/8, strongest stresses on beats 1 and 3 | Inferred; data in Lieder (30) |
| 5/8, 7/8, 9/8 aksak, 11/8, 13/8 | 5 = 2+3; 7 = 2+2+3 or 3+2+2 (never 2+3+2 in Balkan style); 9 = 2+2+2+3; 11 = 2+2+3+2+2; 13 = 2+2+2+3+2+2 | Downbeat > long-beat onset > other group onsets > inner pulses; phrase-final long note on the long beat; plan in two-bar units; playback long/short 1.2–1.7 | English: stress on group onsets, phrase stress on downbeat or long beat. Bulgarian style: syllable count to whole bars, stress free. Turkish style: long aruz syllables to longer notes | Groupings measured/secondary; weights and text rules inferred |
| 5/4 (Kalevala) | 5 quarter beats over an 8-syllable trochaic line | Final syllables lengthened to fill beats 4–5 | Long stressed syllables on strong beats; strict in feet 3–4, free in foot 1 | Rule A measured; rhythmic template inferred |
| All, English style shift | — | Rock: allow about one-third of stresses to anticipate beats 1 and 3 by an eighth; hymn and 19th-century style: none | No lapses of three empty positions; lexical stress near-hard (about 90%), phrasal stress soft | Measured (4/4 only) |

Several of the cited figures rest on small or secondary foundations and should be weighted accordingly. Small samples: Bernacki's 2 recordings; Goldberg's 18; Temperley and Temperley's 10-song English set; the 80-song rock corpus; Palmer and Kelly's 10- and 12-singer performance studies; Hayes and Schuh's 89 Bulgarian songs; Hannon and Trehub's 17 immigrant adults. Secondary sources: London's NI-metre constraints and Fracile's 7/8 frequencies (both via Clayton), the aksak grouping table (Wikipedia), Palmer and Krumhansl's profiles (via London et al.), Hannon and Trehub (via a press release), and the Finnish 5/4 template (a university web page). Internal count conflicts: Hayes and Kaun's corpus is 670 lines in the paper but 640 in the data file, and the two Essen counting passes disagree slightly on additive files (for example 6 vs 8 files in 5/8). Both passes agree that Essen holds fewer than a dozen files in any additive metre.

### Conclusion

The gap list splits into three tiers, each needing a different method. **Compound 9/8 and 12/8 can be learned** from Lieder under CC0, and the English subset there finally lets the team test its extrapolated 6/8 and 12/8 syllable rules against real settings rather than hymns alone. **5/8, 7/8 and 9/8 aksak can be learned only from Turkish data under a non-commercial licence**, which makes SymbTr ideal for research tables and risky for a shipped product. **11/8, 13/8 and English-language additive songs cannot be learned at all** from existing corpora. For those, the right design is generative: a London-style grouping grammar (pulses, {2,3} beats, maximal evenness, tempo bands), with weights and text-setting transferred from the measured 5, 7 and 9 tables.

The most valuable next measurements are ones nobody has published. These are per-pulse onset density in SymbTr's vocal aksak and türk aksağı pieces, which would show whether the long beat really carries the held note, and stressed-syllable placement by beat in Lieder's English 6/8, 9/8 and 12/8 songs, which would extend the team's hymn figures to secular song. Both are feasible with data already identified here. Either would put Luthier's tables ahead of the literature, which has measured English stress alignment only in 4/4 and has never counted melodic onsets in aksak song.

\newpage

# Part 2. Metre atlas: a head start for Luthier beyond 4/4

## Metre atlas: a head start for Luthier beyond 4/4

Words and music for the songs: Jason Bryant. Prepared 15 November 2026 while the engine was offline, for 749.4, 749.5, 749.9 and 749.11.

### What this is

Kept tables for every time signature the public corpora can support, a test of which tables carry across metres, English stress-to-beat tables from 301 hymns, four-part motion tables from the same hymns, research notes on the metres the corpora barely hold (5/8, 5/4, 7/8, aksak 9/8), and a proposed port. Everything is in the repository under tables/metre_atlas (JSON per metre and source; hymns.json; comparison.json) with the scripts that made it.

### The six findings

1. **Pitch carries across metres; rhythm does not.** Across nine sung metres the medians of repeated notes, steps, leaps, turns, range and longest run barely move; every rhythm reading moves a great deal, even in beat units. One pitch table can serve every metre; rhythm tables must be per metre (749.4, now on nine metres, not two).
2. **The felt metre matters, not the notation.** 6/4 and 6/8 read almost the same in beat units (1.88 against 2.00 notes a beat): they can share a table with a scale factor. 2/2 and 2/4 are close in density (1.81 against 1.64 notes a beat) but divide the beat differently, on a small 2/2 sample (62 tunes). 3/2 and 4/2 are not slow 3/4 and 4/4: they are a plainer, older style (0.74 notes a half-note beat; 44% of 3/2 bars are a whole note and a half). 3/8 is felt in one (2.6 notes a dotted-quarter beat), not as a fast 3/4.
3. **9/8 and 12/8 can be built from 6/8, beat by beat.** In the dance tunes, 9/8 and 6/8 behave alike per dotted-quarter beat (2.55 against 2.68 notes a beat; 82% against 86% of moves a third of a beat). There are almost no sung 9/8 or 12/8 tunes (6 and 0), so sung 6/8's per-beat tables, extended to three or four beats, are the best available.
4. **Vocal tables must come from sung tunes.** The dance tunes are 1.1 to 2 times denser per beat, range 17 to 19 semitones (sung: 12 to 13) and repeat notes far less (6% to 12%; sung: 17% to 22%).
5. **English stress lands on strong beats, by metre (749.5).** In 301 hymns' stanzas (about 40,000 words scored with the CMU Pronouncing Dictionary): in 3/4, 81% of stressed syllables fall on the downbeat; in 4/4, 51% on beat 1 and 38% on beat 3; in 6/8, 84% on the two main beats. Unstressed syllables go the other way.
6. **Real four-part hymn settings move with the tune more than song 52's lines did (749.9).** Altos move with the soprano 35% to 39% of the time, against it 13% to 19%, and hold 44% to 47%; basses move against it most (34% to 40%). Parallel fifths and octaves occur about once in a hundred moves. About 7% to 10% of inner-voice notes are shorter than the beat: passing notes the carol sketch never had.

### Sources

- **Sung tunes:** the Essen folk-song collection in music21's corpus (9 metres with 60 or more tunes; 5/8, 5/4, 7/8 and 9/8 with 7 or fewer).
- **Instrumental tunes:** music21's Irish and Scottish dance collections (Ryan's Mammoth, O'Neill's 1850, Aird's Airs, miscFolk), kept apart.
- **Hymns:** the Open Hymnal Project (public domain; 301 hymns, four voices, English stanzas under the soprano), read with a parser written for its interleaved ABC (hymn_parse.py).
- **Research** (below) for odd metres and text-setting.

### Every metre at a glance

Grid in twelfths of a quarter (an eighth = 6). Felt beats: simple metres on the denominator's note (half notes in 2/2, 3/2, 4/2); compound metres (3/8, 6/8, 9/8, 12/8, 6/4) on the dotted note.

| Time signature | Source | Tunes | Bar (twelfths of a quarter) | Beats | Notes a beat (median) | Onsets on a beat | Top bar rhythms (onsets; share of bars) |
|---|---|---|---|---|---|---|---|
| 2/4 | sung | 1157 | 24 | 0, 12 | 1.64 | 53% | (0, 6, 12, 18) 24%; (0,) 9%; (0, 12) 9% |
| 2/4 | instrumental | 486 | 24 | 0, 12 | 3.21 | 29% | (0, 3, 6, 9, 12, 15, 18, 21) 30%; (0, 6, 12, 18) 14%; (0, 3, 6, 9, 12, 18, 21) 7% |
| 3/4 | sung | 1190 | 36 | 0, 12, 24 | 1.15 | 67% | (0, 12, 24) 15%; (0, 24) 11%; (0,) 8% |
| 3/4 | instrumental | 207 | 36 | 0, 12, 24 | 1.30 | 66% | (0, 12, 24) 21%; (0, 24, 30) 6%; (0, 12, 24, 30) 6% |
| 4/4 | sung | 1199 | 48 | 0, 12, 24, 36 | 0.96 | 78% | (0, 12, 24, 36) 18%; (0, 18, 24, 36) 7%; (0,) 6% |
| 4/4 | instrumental | 563 | 48 | 0, 12, 24, 36 | 1.67 | 54% | (0, 6, 12, 18, 24, 30, 36, 42) 11%; (0, 6, 12, 18, 24, 36, 42) 4%; (0, 9, 12, 21, 24, 33, 36, 45) 3% |
| 2/2 | sung | 62 | 48 | 0, 24 | 1.81 | 47% | (0, 12, 24, 36) 13%; (0, 24) 10%; (0, 36) 5% |
| 2/2 | instrumental | 310 | 48 | 0, 24 | 3.59 | 27% | (0, 6, 12, 18, 24, 30, 36, 42) 43%; (0, 6, 12, 18, 24, 36, 42) 10%; (0, 12, 18, 24, 30, 36, 42) 9% |
| 3/2 | sung | 126 | 72 | 0, 24, 48 | 0.74 | 92% | (0, 48) 44%; (0, 24, 48) 14%; (0,) 10% |
| 4/2 | sung | 285 | 96 | 0, 24, 48, 72 | 0.75 | 94% | (0, 24, 48, 72) 20%; (0, 48) 14%; (0, 72) 10% |
| 3/8 | sung | 361 | 18 | 0 | 2.63 | 36% | (0, 6, 12) 33%; (0, 12) 19%; (0,) 12% |
| 3/8 | instrumental | 12 | 18 | 0 | 3.23 | 29% | (0, 6, 12) 34%; (0, 6, 9, 12, 15) 9%; (0, 12) 8% |
| 6/8 | sung | 907 | 36 | 0, 18 | 2.00 | 42% | (0, 12, 18, 30) 20%; (0, 6, 12, 18, 24, 30) 11%; (0, 12, 18, 24, 30) 9% |
| 6/8 | instrumental | 743 | 36 | 0, 18 | 2.68 | 36% | (0, 6, 12, 18, 24, 30) 43%; (0, 6, 12, 18, 30) 13%; (0, 12, 18, 24, 30) 6% |
| 9/8 | sung | 6 | 54 | 0, 18, 36 | 2.33 | 39% | (0, 12, 18, 48) 8%; (0, 9, 12, 18, 24, 30, 36, 42, 48) 6%; (0, 12, 18, 24, 30, 36, 48) 6% |
| 9/8 | instrumental | 169 | 54 | 0, 18, 36 | 2.55 | 37% | (0, 6, 12, 18, 24, 30, 36, 42, 48) 23%; (0, 6, 12, 18, 24, 30, 36, 48) 12%; (0, 12, 18, 24, 30, 36, 42, 48) 7% |
| 12/8 | instrumental | 6 | 72 | 0, 18, 36, 54 | 2.23 | 40% | (0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66) 14%; (0, 12, 18, 30, 36, 42, 48, 54) 9%; (0, 6, 12, 18, 30, 36, 48, 54, 66) 9% |
| 6/4 | sung | 131 | 72 | 0, 36 | 1.88 | 44% | (0, 24, 36, 60) 32%; (60,) 6%; (0, 36, 60) 6% |
| 5/8 | sung | 7 | 30 | 0, 12 | n/a | 36% | (0, 6, 9, 12, 18) 18%; (0, 6, 12, 24) 13%; (0, 6, 12, 18, 24) 7% |
| 5/4 | sung | 4 | 60 | 0, 12, 24, 36, 48 | 1.23 | 71% | (0, 6, 12, 24, 36, 42, 48, 54) 35%; (0, 6, 12, 24, 36, 42, 48) 12%; (0, 24, 30, 36, 48) 8% |
| 7/8 | sung | 2 | 42 | 0, 12, 24 | n/a | 51% | (0,) 21%; (0, 6, 12, 18, 30, 36) 21%; (0, 12, 18, 24) 14% |

### Finding 1 in numbers: what carries across metres

Medians per sung metre (2/4, 3/4, 4/4, 2/2, 3/2, 4/2, 3/8, 6/8, 6/4); spread = (highest − lowest) / mean.

| Reading | Lowest median | Highest median | Spread across metres |
|---|---|---|---|
| repeated notes | 17% | 22% | 0.28 |
| moves by step | 44% | 60% | 0.32 |
| moves by leap | 7% | 12% | 0.49 |
| turns of direction | 38% | 41% | 0.08 |
| range | 12.00 | 13.00 | 0.08 |
| distinct pitches | 7.00 | 9.00 | 0.25 |
| longest run of one pitch | 3.00 | 3.00 | 0.00 |
| notes a beat | 0.74 | 2.63 | 1.26 |
| gaps of half a beat | 0% | 64% | 2.82 |
| gaps of a third of a beat | 0% | 63% | 3.22 |
| gaps of a beat or more | 2% | 92% | 2.55 |
| onsets on the beat | 36% | 94% | 0.95 |
| onsets on the bar's first beat | 23% | 42% | 0.65 |
| distinct rhythms over bars | 31% | 64% | 0.66 |

### Finding 2 in numbers: notation pairs (medians)

| Pair | Notes a beat | Gaps of half a beat | Gaps of a beat or more | Onsets on a beat | Notes a bar |
|---|---|---|---|---|---|
| 3/8 vs 3/4 | 2.63 vs 1.15 | 2% vs 46% | 2% vs 39% | 36% vs 67% | 2.63 vs 3.44 |
| 6/4 vs 6/8 | 1.89 vs 2.00 | 0% vs 0% | 5% vs 6% | 44% vs 42% | 3.77 vs 4.00 |
| 3/2 vs 3/4 | 0.74 vs 1.15 | 10% vs 46% | 88% vs 39% | 92% vs 67% | 2.21 vs 3.44 |
| 2/2 vs 2/4 | 1.81 vs 1.64 | 41% vs 64% | 7% vs 14% | 47% vs 53% | 3.62 vs 3.27 |
| 4/2 vs 4/4 | 0.75 vs 0.96 | 8% vs 33% | 92% vs 63% | 94% vs 78% | 3.00 vs 3.82 |

### Finding 4 in numbers: sung against instrumental (medians)

| Metre | Notes a beat | Steps | Leaps | Repeated notes | Range |
|---|---|---|---|---|---|
| 6/8 | 2.00 vs 2.68 | 47% vs 52% | 11% vs 11% | 22% vs 12% | 13 vs 17 |
| 2/4 | 1.64 vs 3.21 | 44% vs 52% | 12% vs 14% | 20% vs 7% | 13 vs 19 |
| 3/4 | 1.15 vs 1.30 | 49% vs 60% | 11% vs 9% | 18% vs 10% | 13 vs 17 |
| 4/4 | 0.96 vs 1.67 | 51% vs 53% | 11% vs 13% | 20% vs 10% | 12 vs 17 |
| 2/2 | 1.81 vs 3.59 | 56% vs 48% | 12% vs 13% | 17% vs 6% | 13 vs 19 |

### Finding 5: stress against the bar (hymns)

Primary-stressed syllables against unstressed ones; "strong beat" is beat 3 in 4/4 and the second dotted beat in 6/8 and 6/4.

| Time signature | Hymns | Stressed syllables on the downbeat | on another strong beat | on a weaker beat | off the beat | Unstressed syllables on the downbeat | on a strong beat | on a weaker beat | off the beat |
|---|---|---|---|---|---|---|---|---|---|
| 4/4 | 197 | 51% | 38% | 9% | 1% | 15% | 16% | 60% | 9% |
| 3/4 | 46 | 81% | 0% | 16% | 3% | 17% | 0% | 72% | 10% |
| 6/8 | 6 | 52% | 33% | 0% | 16% | 13% | 8% | 0% | 79% |
| 6/4 | 10 | 48% | 18% | 0% | 34% | 9% | 9% | 0% | 82% |
| 3/2 | 6 | 42% | 0% | 41% | 16% | 11% | 0% | 47% | 43% |
| 2/4 | 5 | 90% | 0% | 7% | 3% | 18% | 0% | 62% | 20% |
| 2/2 | 3 | 68% | 0% | 26% | 6% | 13% | 0% | 36% | 51% |

**For the engine (749.5):** a kept stress-to-position table per metre, from these counts. The 6/8, 6/4, 3/2, 2/4 and 2/2 rows rest on 3 to 10 hymns each and should be read as provisional. Song 52's sketch required 55% of stressed syllables on a beat in its freshly drawn lines; the hymn 6/8 figure is 84%.

### Finding 6: four-part motion in real hymn settings

| Time signature | Voice | Moves with the tune | Against it | Holds while it moves (or the reverse) | Parallel 5ths/8ves per 100 moves | Notes shorter than the beat | Notes a bar |
|---|---|---|---|---|---|---|---|
| 4/4 | alto | 35% | 19% | 44% | 1.2 | 9% | 3.5 |
| 4/4 | tenor | 38% | 26% | 36% | 1.9 | 10% | 3.4 |
| 4/4 | bass | 27% | 40% | 28% | 1.6 | 7% | 3.4 |
| 4/4 | soprano (the tune) | | | | | 10% | 3.4 |
| 3/4 | alto | 39% | 13% | 47% | 0.8 | 8% | 2.3 |
| 3/4 | tenor | 35% | 24% | 40% | 0.9 | 7% | 2.3 |
| 3/4 | bass | 26% | 34% | 38% | 0.7 | 5% | 2.3 |
| 3/4 | soprano (the tune) | | | | | 8% | 2.3 |

**For the engine (749.9):** replace "under half the time with the tune" with kept quartiles from these hymns per voice, and add passing notes in the inner voices (7% to 10% of notes shorter than the beat).

### Hymn tunes against folk tunes (749.11)

Hymn tunes in 3/4 (46 hymns), quartiles: notes a bar 2.12 / 2.34 / 2.66; distinct bar rhythms 16% / 22% / 32% (sung folk 3/4: 35% / 47% / 67%); gaps of half a beat 0% / 7% / 24%; steps 49% / 57% / 62%. Song 53's carol sketch read 1.97 notes a bar (under the hymn range), 16% distinct bar rhythms (the hymn 25th percentile) and no half-beat gaps: plainer than a typical hymn, as the writer judged. A hymn mode should be charged against these hymn quartiles, not the folk ones. Commonest 3/4 hymn bars: half and quarter (36%), three quarters (26%), dotted half (13%), dotted quarter, eighth and quarter (6%).

### The metres the corpora barely hold: research

- **5/4:** five quarter-note beats, usually grouped 3+2 or 2+3; Brubeck's "Take Five" is 3+2, and the original Mission: Impossible theme keeps the 3+2 subgrouping. Essen has 4 sung tunes in 5/4.
- **5/8, 7/8 and aksak:** additive metres built from short (2) and long (3) pulses. 7/8 is most often 2+2+3 (the Bulgarian rachenitsa), also 3+2+2 and 2+3+2; Balkan 9/8 is usually 2+2+2+3, unlike the Western compound 3+3+3; 11/16 (kopanitsa) is 2+2+3+2+2. Essen has 7 tunes in 5/8 and 2 in 7/8.
- **Text-setting:** composers align stressed syllables with strong beats (Palmer and Kelly 1992, on English song); Halle and Lerdahl (1993) gave the first explicit model; Hayes treats a good setting as the best resolution of conflicting goals (stress on strong positions, avoiding long gaps between syllables, avoiding too many syllables crowded together, phrase ends at line ends), and published 640 lines of English set to rhythm by native speakers (Hayes and Kaun 1996), a ready test set for the engine's stress rule. Alignment also holds in French (Temperley and Temperley 2013).

### Proposed port (749.4)

1. **A metre object:** name; bar length in twelfths; beat groups as a list of lengths (3/4: [12, 12, 12]; 6/8: [18, 18]; 7/8 as 2+2+3: [12, 12, 18]; 5/4 as 3+2: [36, 24]); levels (downbeat, group starts, beats, subdivisions); the felt beat.
2. **Tables by felt metre:** shared pitch tables; rhythm tables per felt metre from sung tunes (this atlas); 6/4 from 6/8 by scale (2/2 from 2/4 only with care); 9/8 and 12/8 from 6/8 per beat; 3/2 and 4/2 as their own (plainer) style; additive metres from their groups, each group read as a short (2) or long (3) beat, until a corpus is found.
3. **Readings in beat units** (notes a beat, gaps of half, a third, a beat or more), so the judge's charge means the same in every metre.
4. **The stress rule per metre** from the hymn table (finding 5), tested on Hayes and Kaun's lines.
5. **Harmony and accompaniment per metre:** four-part motion from finding 6; bass and accompaniment figures by beat groups (749.6, 749.14).
6. **A hymn mode** charged against the hymn quartiles (749.11).

### Data still missing

- Sung English tunes beyond hymns, with words under the notes: DALI (pop songs, notes and lyrics aligned to audio) and the lyrics-melody MIDI set of Yu and others (2021) exist; neither was fetched here.
- Sung 9/8, 12/8, 5/8, 5/4 and 7/8 tunes in numbers: none in the corpora used.

### Files

tables/metre_atlas/: one JSON per metre and source (readings and quartiles, bar rhythms, two-bar windows, intervals, onset weights, durations); hymns.json (hymn readings by metre, stress tables, four-part motion and texture); comparison.json; atlas_build.py, hymn_parse.py, hymn_atlas.py, compare.py.

### Sources (links)

- Open Hymnal Project, github.com/mzealey/openhymnal (public domain)
- music21 corpus: Essen folk songs; Ryan's Mammoth; O'Neill's 1850; Aird's Airs; miscFolk
- CMU Pronouncing Dictionary via the Python package pronouncing
- Palmer, C. and Kelly, M. H. (1992), Linguistic prosody and musical meter in song, Journal of Memory and Language 31: https://www.examenapium.it/cs/biblio/Palmer1992.pdf
- Hayes, B., Textsetting as constraint conflict, with Hayes and Kaun (1996) data: https://brucehayes.org/Textsetting
- Halle, J. and Lerdahl, F., A generative textsetting model, Current Musicology 55: https://www.fredlerdahl.com/writings
- Aksak groupings: https://en.wikipedia.org/wiki/Aksak ; 7/8: https://tunable.pages.dev/time-signature/7-8/ ; 5/4 and "Take Five": https://london-calling-iaspm2020.com/?p=48 ; Mission: Impossible 3+2: https://cellofun.eu/?p=20421
- DALI dataset: https://refworks.reference-global.com/article/10.5334/tismir.30

\newpage

# Part 3. Metre atlas, round 2: SymbTr, Lieder and lead sheets

Round 2 extended the atlas with three more sources and was added to the atlas Doc (https://claude.ai/artifact/58vnmJPuJ8U9hyDLq47SVR). The tables are in tables/metre_atlas: lieder_mxl.json, ewld_mxl.json, symbtr_usul.json, with each table tagged by its licence.

### Sources added

- **OpenScore Lieder (CC0):** sung art songs with per-note lyrics in MusicXML, read for metre tables and English stress-to-beat alignment.
- **OpenEWLD (MIT):** public-domain lead sheets with chords, for popular-song tables in 4/4, 2/2, 3/4 and 6/8.
- **SymbTr (CC BY-NC-SA 4.0):** Turkish makam pieces with usul (rhythmic cycle) annotations and lyric syllables, for additive metres.

### Findings

- **Stress-to-beat in English holds across compound metres.** In hymns, art songs and lead sheets, stressed syllables fall on strong beats at 84 to 86% in 6/8, 82% in 9/8 and 84% in 12/8. English text-setting rules can carry into compound metres unchanged.
- **Additive groupings can be learned from the notes.** Scoring every arrangement of 2- and 3-pulse groups against where onsets fall recovered the traditional groupings from the music alone: aksak 2+2+2+3, türk aksağı 2+3, devr-i hindi 3+2+2, devr-i turan 2+2+3, curcuna 3+2+2+3. The engine can take additive metres as groupings and learn each grouping's onset weights.
- **Pitch readings carry across metres; rhythm readings do not.** The felt metre matters more than the notated one, and vocal tables must come from sung tunes.

### Licences

Lieder is CC0 and EWLD is MIT; both are usable without restriction. SymbTr is non-commercial (CC BY-NC-SA). The Essen tables through music21 are non-commercial too.

\newpage

# Part 4. Accompaniment corpora and music theory (research report)

## Plan the verses, not just the notes

Luthier's organ and keyboard parts sound too simple mainly because every stanza gets the same treatment, not because any one bar has too few notes. Fixing the density matters too. Two kinds of evidence point the same way. Organ pedagogy from PCUSA, *Reformed Worship* and RSCM Australia agrees on a plan: keep inner stanzas close to hymnal harmony but vary the texture and registration, and save rich harmony for introductions, interludes and a unison final stanza with free accompaniment, often after a modulation and sometimes with a descant ([PCUSA Quicksheet](https://pcusa.org/sites/default/files/2026-07/Improvising%20%26%20Reharmonizing%20in%20Worship%20Quicksheet.pdf); [Reformed Worship, Brink](https://reformedworship.org/resource/i-sing-bass-organists-use-alternative-hymn-arrangements)). On the computational side, the systems that work best treat accompaniment texture as a chord-independent pattern. They retrieve or generate it phrase by phrase, keep it consistent across sections with the same label, and vary it between section types ([Wang et al. 2020](https://arxiv.org/pdf/2008.07122v1); [Whole-song generation](https://arxiv.org/pdf/2405.09901)). On density, the engine's own measurements show the current carol organ part runs at about 40% of the onset rate of 19th-century Lieder piano parts in 3/4, with a quarter of their rhythmic complementarity to the voice. For triple and compound metres, the only open accompaniment data with melody and accompaniment kept apart are **OpenScore Lieder (CC0; 265 songs that open in 3/4 and 216 in 6/8)** and the **Open Hymnal (305 SATB hymns, 48 in 3/4)**. Every major learned accompaniment system filters its training data to 2/4 and 4/4. **No open symbolic corpus of contemporary worship, musical theatre or film accompaniment exists.** Of the music-as-language theories, only expectation models (IDyOM and its relatives) have direct evidence linking their scores to listener pleasure. Grammars, schemata and GTTM work well as generators and structural checks, but nothing yet shows that they work as quality judges.

### The carol organ plays at about 40% of the Lieder piano's rate

The engine's own Lieder accompaniment tables give a baseline for 3/4 piano writing. The median right hand makes **1.53 onsets a beat** (IQR 1.13–1.95). The median left hand makes 1.17 (0.88–1.51). **65%** of accompaniment activity complements the voice rhythmically (50–73%). Textures are split among mixed (29%), broken (27%) and block (26%), with melodic (7%), sustained (7%) and waltz (4%) figures well behind. In 6/8, broken chords lead at 35% and the right hand rises to 2.4 onsets a beat. Against this baseline, the engine's measurements of the current carol organ part in verses 1–3 are **RH 0.63, LH 0.45 and complementarity 15%**. That is about 1.9 right-hand attacks and 1.35 bass notes per 3/4 bar: a held chord with an occasional change. The right hand sits 44% below the bottom of the Lieder interquartile range, and complementarity is less than a third of the Lieder lower quartile.

There is a strong counter-argument. Lieder piano writing is the wrong benchmark for congregational stanzas. Every organ source reviewed wants the inner stanzas of a hymn left close to the hymnal harmony, so that basses can sing their part and "the primary sound must come from the congregation" ([Reformed Worship, Brink](https://reformedworship.org/resource/i-sing-bass-organists-use-alternative-hymn-arrangements)). Hymnal harmony moves with the voices, so low complementarity in those stanzas is idiomatic, not a fault. The numbers still show a real problem. If the carol tune moves mostly in quarter notes, as most 3/4 carols do, plain hymnal doubling would put the right hand at about one onset a beat. At 0.63 the organ is sustaining across tune notes, which makes it thinner than the hymnal itself. (This is an inference from the engine's figures, not a measured comparison against the tune.) The bigger problem is what the measurement implies about the other stanzas. If verses 1–3 all score alike, the part has no plan across the verses, and the final verse is where organists put the free, fuller writing. The fix therefore has two layers. Bring congregational stanzas up to at least hymnal-doubling density and vary their texture. Then write designated "free" stanzas, interludes and piano-accompanied songs to Lieder-like density and complementarity bands.

Two cross-checks support the engine's Lieder texture mix. In the only rigorous texture-annotated keyboard corpus, oscillating figures (Alberti and rocking patterns) appear in only about **5.1%** of bar labels even in early Mozart ([Couturier, Bigo & Levé, ISMIR 2022](https://archives.ismir.net/ismir2022/paper/000061.pdf)). That matches the engine's 4% waltz share. Stereotyped figures are seasoning in real repertoire, and an engine that defaults to oom-pah-pah in every 3/4 song, or Alberti bass in every ballad, over-represents them relative to the styles it imitates. The same corpus also shows that accompaniment layers are present in **84.4% of bars in slow movements but only 58.2% in faster ones**. Reflective, slow songs should almost always carry an explicit harmonic layer rather than leaving the melody exposed.

### Only Lieder and the hymnals supply open triple-metre accompaniment

The research team cloned the main repositories on 2026-11-15 and counted time signatures directly, so most counts below are team measurements, not published figures. **OpenScore Lieder** is the strongest single source. It holds 1,352 MuseScore scores of 19th-century voice and piano under **CC0**. By first time signature there are 265 in 3/4, 216 in 6/8, 33 in 9/8 and 20 in 12/8. Counting a signature anywhere in the score gives 332 with 3/4, 247 with 6/8, 50 with 9/8 and 30 with 12/8, and 248 scores change metre. The corpus also ships **1,156 Roman-numeral analyses (.rntxt)**, so the accompaniment can be read against labelled harmony without running a chord detector ([OpenScore Lieder](https://github.com/OpenScore/Lieder)). The **Open Hymnal Project** is the only open hymn corpus with full parts: 305 ABC files, 286 of them in four voices. By first metre, 203 are in 4/4, 48 in 3/4, 10 in 6/4, 7 in 3/2 and 6 in 6/8. It has no licence file; headers say the hymns must be "public domain or freely distributable" ([mzealey/openhymnal](https://github.com/mzealey/openhymnal)). It supplies the "hymnal harmony" baseline but none of the free accompaniment the engine is missing. Hymnary.org offers standard public-domain harmonisations as PDF and MusicXML, with no terms stated for those downloads ([Hymnary.org, OLD 100TH](https://hymnary.org/tune/old_100th)).

Modern pop accompaniment is cleanly available but is almost all 4/4. **POP909** (MIT licence) gives each of 909 Chinese pop songs an identical three-track layout of MELODY, BRIDGE (secondary melody) and PIANO accompaniment ([POP909 repo](https://www.github.com/music-x-lab/POP909-Dataset)). Downbeat files give 880 songs in 4/4 and 29 with six-beat bars, which matches a 2026 paper's count of "29 in 3/4 or 6/8" ([arXiv 2602.15074](https://arxiv.org/pdf/2602.15074)). The metadata spreadsheet implies about 52 non-duple songs instead, a conflict the team could not resolve. MIDI time-signature events are unusable: 617 of the 909 files claim 1/4. **PDMX** is the largest openly licensed multi-part score pool. It holds more than 250,000 MuseScore scores under a CC BY 4.0 umbrella, with track, genre and lyric columns. However, **12.29% of songs carry conflicting internal licences**, and user claims that modern songs are public domain cannot be trusted, so only the 222,856-song "no licence conflict" subset is defensible ([Zenodo PDMX v9](https://zenodo.org/records/15571083)). PDMX is the only realistic route to modern worship, theatre and film piano arrangements in 3/4 and 6/8. Its metre distribution was not counted because Zenodo blocked shell downloads. Lakh MIDI (176,581 files, CC BY 4.0) is a large multi-track pool of uneven quality ([LMD](https://colinraffel.com/projects/lmd/)). Pop1K7 (1,747 pop piano covers, CC BY 4.0) is **entirely 4/4** and keeps melody and accompaniment in one part ([Zenodo 13167761](https://zenodo.org/records/13167761)).

The gaps matter as much as the holdings. The team found **no open symbolic corpus of contemporary worship (CCM), Broadway piano-vocal scores or film reductions**, and no annotated corpus of pop, gospel or worship piano textures such as worship pads over octave left hands. Classic free-accompaniment collections exist only as scans, and most are in copyright in the US. Bairstow's *Organ Accompaniments to 24 Unison Hymn-Tune Verses* (1941) is public domain except in the US. Coleman's *Varied Hymn Accompaniments* (1953, sixteen tunes with three settings each) is public domain only in life+50 countries. Thiman's 1937 set is not public domain anywhere ([IMSLP Bairstow](https://cn.imslp.org/wiki/Organ_Accompaniments_to_24_Unison_Hymn-Tune_Verses_(Bairstow,_Edward_Cuthbert)); [IMSLP Coleman](https://imslp.org/wiki/Varied_Hymn_Accompaniments_(Coleman,_Henry)); [IMSLP Thiman](https://imslp.org/wiki/Varied_Accompaniments_to_34_Well-known_Hymn_Tunes_(Thiman,_Eric))). These collections share tunes with the hymnals (OLD HUNDREDTH, ST ANNE, HYFRYDOL, RICHMOND), so optical music recognition of the permissible scans would produce paired "hymnal versus free" settings of the same melody. No such paired corpus exists anywhere.

### Good accompaniment builds by section, fills the voice's gaps and saves its surprises

#### Texture is layered, and the two-hand split is not enough

The Algomus texture syntax is the best available vocabulary for describing what an accompaniment does. Each bar is labelled as stacked layers: M (melodic), H (harmonic) and S (static, for pedals and ostinati). Each layer has a voice count and figure flags for homorhythm, parallel motion, octaves, sustained notes, repeated notes, oscillation and scales ([ISMIR 2022](https://archives.ismir.net/ismir2022/paper/000061.pdf)). A label such as `M1/HS1b` means one melodic voice over a single persistent oscillating accompaniment voice. The most common full label in early Mozart is melody over one accompaniment voice (7.3%), and two-layer, two-voice bars make up 29.2% of configurations. The authors conclude that a plain left-hand/right-hand split "is not representative" of real texture. The reliability of the scheme is unproven: no inter-annotator agreement statistic exists, and reviewers flagged 31% of the labels, of which 22% were changed. Classical string quartets show the same melody-over-accompaniment dominance, at about 74% of 691 segments ([Giraud et al., ISMIR 2014](https://archives.ismir.net/ismir2014/paper/000143.pdf)). Pedagogy adds the pop catalogue: arpeggios over an octave bass, block-chord rhythms such as the "1 (2) &" pattern in "Thinking Out Loud", and repeated eighth- or quarter-note chords that run from Schubert's "Gute Nacht" to Sara Bareilles. It also notes that bass and top voice a tenth apart is a characteristically sonorous spacing ([Puget Sound, Arpeggiated Accompaniments](https://musictheory.pugetsound.edu/mt21c/ArpeggiatedAccompaniments.html); [Block Chord Accompaniments](https://musictheory.pugetsound.edu/mt21c/BlockChordAccompaniments.html)).

#### Density rises through the song and repeats by section label

Professional pop arrangements build. In the POP909 example analysed by the whole-song generation team, verses use mostly eighth notes and choruses sixteenths. Fill figures appear at phrase boundaries, and activity and pitch height rise in the second half toward a climax ([Wang, Min & Xia, ICLR 2024](https://arxiv.org/pdf/2405.09901)). This evidence is qualitative; nobody has published density curves by section. Repetition by section label is measured. The ratio of accompaniment similarity within the same phrase type to similarity across types (ILS) is **1.68 ± 0.09 in human arrangements**, against 1.19 for the best generator. Every chorus sounds like every other chorus, and choruses sound unlike verses. Listener research on pop choruses agrees: choruses are higher, brighter and more compressed in dynamics, while harmonic variance does not separate them from verses ([Van Balen et al., ISMIR 2013](https://archives.ismir.net/ismir2013/paper/000180.pdf)).

#### Complementarity is real but uncalibrated outside the engine's own tables

The evidence that accompaniment should move where the voice does not is directional, not numeric. In Bach's two-part Inventions, the fusing perfect consonances arrive asynchronously more often than synchronously (1,059 against 599 occurrences), while imperfect consonances tend to arrive together (1,901 against 832). Avoiding simultaneous onsets on fused intervals keeps the parts perceptually separate ([Huron 2008](https://core.ac.uk/download/159579115.pdf)). Learned arrangers trained on POP909 insert a secondary melody when the lead rests, which reproduces the professional BRIDGE track ([Wang et al. 2020](https://arxiv.org/pdf/2008.07122v1)). **No published study gives a target complementarity value, melody-to-accompaniment density ratio or register gap for song accompaniment.** The engine's own Lieder figure of 65% (50–73%) is therefore ahead of the literature. It is the best calibration target available for piano-accompanied song.

#### Hymn and organ practice puts its richness at the edges

The organ sources agree with each other more than any other body of evidence in this report, though it is practitioner consensus rather than measurement. Every source says the text sets the treatment. RSCM Australia's Steven Nisbet writes that "the meaning of the text dictates the mood of the hymn's accompaniment and level of harmonic complexity" ([RSCM Australia, Nisbet](https://rscmaustralia.org.au/wp-content/uploads/2021/04/Reharmonisation-of-last-verses-of-hymns-video-script-by-SN.pdf)). PCUSA's guidance says to "reserve richer harmonies for introductions, interludes, or final verses" and adds that "simplicity is often more effective than complexity" ([PCUSA Quicksheet](https://pcusa.org/sites/default/files/2026-07/Improvising%20%26%20Reharmonizing%20in%20Worship%20Quicksheet.pdf)). Emily Brink warns against playing every stanza the same way, and against the over-loud organ that most often turns congregations against alternative arrangements ([Reformed Worship, Brink](https://reformedworship.org/resource/i-sing-bass-organists-use-alternative-hymn-arrangements)). For inner stanzas, a single organ-training course (one author's view) gives a concrete texture menu: the melody soloed on one manual with alto and tenor on another and bass in the pedals, the tenor soloed, the alto raised an octave as a near-descant, soprano and tenor swapped, manuals only for a reflective verse, and pedal points before cadences or in interludes ([Organ Training Course, Lesson 10](https://sites.google.com/view/organtrainingcourse/lessons/lesson-10-creative-hymn-playing)).

The final stanza follows a well-documented recipe. Everyone sings the melody in unison, and the organ part is fuller, with lower pedal notes, "more secondary dominants (especially over chromatic bass lines)" and often **five or more notes per chord** ([Wikipedia, Last verse harmonisation](https://en.wikipedia.org/wiki/Last_verse_harmonisation)). Nisbet's working method is the clearest algorithm in the sources. Fix the melody, write the bass next, then fill the inner parts, and aim for a continuous progression rather than isolated "spiky" chords. He offers five bass archetypes with tune examples: tonic pedal (SONG 34), dominant pedal (SLANE, NICAEA, LASST UNS ERFREUEN), descending line (NUN DANKET, CRIMOND), ascending line (ANTIOCH, ELLACOMBE) and walking bass (BATTLE HYMN). His governing rule is: "when you go off into new harmonic territory you have to come back safely" ([RSCM Australia, Nisbet](https://rscmaustralia.org.au/wp-content/uploads/2021/04/Reharmonisation-of-last-verses-of-hymns-video-script-by-SN.pdf)). PCUSA's vocabulary list adds passing diminished chords, suspensions, modal interchange, gospel harmony and ii–V, with tritone substitution used "sparingly". A descant needs harmony written to fit it, or "the descant melody may clash" ([Wikipedia](https://en.wikipedia.org/wiki/Last_verse_harmonisation)). The King's College recordings show descants arriving in stages over 1954–1963 and drawing complaints of a "perfect rainstorm of descants", so a descant is optional, not a default ([Williams, York thesis](https://etheses.whiterose.ac.uk/id/eprint/24691/2/What%20sweeter%20music%20revised%20final.pdf)). Willcocks's last verse of "O come, all ye faithful" opens with the melody in three octaves, the lowest in the pedals, before the harmony departs from the standard setting ([Wikipedia](https://en.wikipedia.org/wiki/Last_verse_harmonisation)).

Modulation before the last verse has clear harmonic rules but no fixed length. Thomas Read says to weaken the old key before establishing the new one, and to precede the new dominant with its own applied dominant or diminished seventh so it does not sound like a half cadence in some other key. For a half-step lift in major, where the two keys share no chords, a **German augmented sixth** is "one of the quickest and simplest" routes ([The Diapason, Read 2022](https://www.thediapason.com/content/modulating-organist)). The AGO's examined method for a modulating bridge is to think in the target hymn's metre, take a motif from its opening, restate it a fourth or fifth away, arrive, and make a clean break before the singers enter ([AGO, Gehring 2013](https://wp.agohq.org/wp-content/uploads/2015/11/Modulating-Bridge.pdf)). Jan Overduin's only limit is that the interlude be "no longer than the hymn itself". He prefers the half step as "more liberating" than the whole tone, but that is one author's taste against the common modern whole-step lift ([Reformed Worship, Overduin](https://reformedworship.org/resource/giving-hymn-lift-when-should-organist-change-keys)). **No study measures whether any of these practices improves congregational singing.** The engine is encoding expert craft, not tested effects.

### Working systems separate texture from chords and choose by phrase

The productive line of accompaniment research comes from NYU Shanghai's Music X Lab, and its central move transfers directly to a rule-based engine. Wang et al. split piano music into two latent factors. Chords are a beat-wise 36-dimensional vector (root, bass, chroma). Texture is a piano-roll "shape" that deliberately carries minimal chord information. A texture can then be re-voiced onto new chords while keeping its left-hand pattern and contour ([Wang et al. 2020](https://arxiv.org/pdf/2008.07122v1)). AccoMontage retrieves whole phrases of real accompaniment from POP909 and selects a path through them by Viterbi dynamic programming. Node scores measure rhythm and chord fit to the query melody. Edge scores combine learned texture similarity between adjacent phrases with a "form" term that rewards matching phrase labels. The chosen texture is then re-harmonised to the new chords. Users can pre-filter by rhythm density and voice count (low, medium, high). In a 72-person listening test it beat template-only and sequence-to-sequence baselines on coherence and structure (p < 0.05) ([AccoMontage](https://ar5iv.labs.arxiv.org/html/2108.11213)). AccoMontage2 adds harmonisation by dynamic programming over **5,762 curated chord-progression templates**, scored at three levels: note-level melody–root dissonance, phrase-template matching and whole-piece coherence ([AccoMontage2](https://ar5iv.labs.arxiv.org/html/2209.00353)). Whole-song generation cascades four levels: form (keys and phrase labels), reduced lead sheet, lead sheet, then accompaniment. That ordering is the one an engine should follow ([Whole-song generation](https://arxiv.org/pdf/2405.09901)).

Evaluation in this field is weak but usable. Systems report overlap of pitch and duration distributions with real data (Polyffusion: 0.89 and 0.96), chord accuracy, degree of arrangement, and the ILS structure ratio. The ground-truth targets are DOA 0.333 and structure score 1.980, against 0.300 and 1.520 for the best multi-track system ([Polyffusion](https://arxiv.org/pdf/2307.10304); [Structured arrangement v4](https://arxiv.org/html/2310.16334v4)). Listener panels are small, from 23 to 72 people. **Every one of these systems is trained on data filtered to 2/4 and 4/4.** The whole-song model allows three beats per bar but calls 3/4 "underrepresented" in POP909, and no system was trained or tested on hymn, gospel, worship or organ textures. For Luthier the lesson is to copy the architecture, not the data. Store texture templates as an onset grid plus chord-tone indices plus register. Author or harvest the 3/4 and 6/8 templates from Lieder, because no learned model will supply them. Choose templates phrase by phrase with a fit-plus-transition-plus-form score. Map each template onto every chord as it arrives.

### Expectation models can judge; grammars and schemata can only generate and check

The expectation family is both implemented and validated. IDyOM, written in Common Lisp, gives per-note information content (surprise) and entropy (uncertainty) from symbolic sequences. Its short-term model learns only from the current piece and its long-term model from a training corpus ([IDyOM wiki](https://code.soundsoftware.ac.uk/projects/idyom-project/wiki/Idyom/58)). It runs from Python through the peer-reviewed py2lispIDyOM wrapper ([py2lispIDyOM](https://xinyiguan.github.io/py2lispIDyOM)), and Harrison's `ppm` R package implements the same core method without Lisp ([pmcharrison/ppm](https://rdrr.io/github/pmcharrison/ppm)). The key validation used **about 80,000 chords from 745 Billboard songs** stripped of melody and lyrics. Pleasure depended on the *interaction* of uncertainty and surprise: listeners enjoyed surprising chords when the context was predictable, and predictable chords when the context was uncertain. The interaction also showed in the amygdala, hippocampus and auditory cortex ([Cambridge summary of Cheung et al. 2019](https://cms.mus.cam.ac.uk/publications/cheung-uncertainty-surprise/); [MPI CBS](https://www.cbs.mpg.de/music-pleasure-in-pop-songs)). A 2025 study reports an inverted-U relation between predictability and preference, but it was read only through a secondary summary ([MindBlog](https://mindblog.dericbownds.net/2025/08/predictability-and-pleasure-of-music.html)). This finding lines up closely with hymn practice. By the final stanza the tune is fully predictable, because the congregation has just sung it several times. A reharmonised last verse therefore puts surprising chords exactly where the uncertainty-surprise interaction says they please most, and the "come back safely" rule restores predictability at the cadences. IDyOM's short-term/long-term split could measure this directly: train the short-term model on stanzas 1–3, then score the free stanza's chords against it. That is the report's inference, not a published test.

Effect sizes argue for using these measures as filters, not oracles. In the Hooked! study (1,715 song segments, 973 participants), recognisability tracked conventionality and melodic repetition. But the features explained a marginal R² of only **0.10 at best**, against 0.47 once song identity was included ([Van Balen et al., ISMIR 2015](https://eprints-gro.gold.ac.uk/17202/1/Vanbalenetal_ISMIR_2015.pdf)). On the Billboard Hot 100, each extra chorus repetition raised the odds of reaching No. 1 by 14.5%, a finding read through a secondary source ([Pacific Standard summary of Nunes et al.](https://psmag.com/?p=30843)).

The grammar and schema theories are formal and implemented but have no evidence on liking. Rohrmeier's jazz-harmony grammar models prolongation and preparation as nested dependencies ([EPFL DCML](https://www.epfl.ch/labs/dcml/a-grammar-theory-of-jazz-harmony/)). Harasim's probabilistic abstract grammar, trained on 357 iRealPro standards, recovers expert trees **45.95%** of the time against 15.35% for random trees ([ISMIR 2018](https://ismir2018.ismir.net/doc/pdfs/258_Paper.pdf)). That shows it can find structure; it says nothing about quality, and the model is jazz-specific. The deep-learning GTTM analyser deepGTTM-IV produced correct time-span trees for 29 of 30 pieces, but no current public download was confirmed ([Zenodo 10114163](https://zenodo.org/records/10114163)). Voice-leading schema detection in Mozart reaches F = 0.894 on balanced data but **precision near 0.01 on real, unbalanced data**. A naive detector would find galant schemata everywhere, so schema checks must be tied to known positions such as phrase openings and cadences ([Finkensiep et al., ISMIR 2020](https://archives.ismir.net/ismir2020/paper/000124.pdf)). Style priors matter. In the Rock Corpus, IV→I (1,162) outnumbers V→I (788), and ♭VII is common ([de Clercq & Temperley 2011](https://rockcorpus.midside.com/2011_paper/declercq_temperley_2011.pdf)). A common-practice "dominant must resolve" grammar would therefore wrongly penalise idiomatic worship and pop accompaniment, though it suits hymn harmony. Nobile's telos principle (verse as initiation, prechorus as build-up, chorus onset as arrival) gives a form check for where the accompaniment should lift. It rests on close analysis rather than a corpus ([Nobile, MTO](https://www.mtosmt.org/ojs/index.php/mto/article/view/864/206)). Patel's shared-syntax hypothesis is contested: language regions respond weakly to music, and people with severe aphasia judged melodic well-formedness normally ([Fedorenko lab preprint](https://www.biorxiv.org/content/10.1101/2021.06.01.446439.full)). "Music as language" is a productive engineering metaphor, not a licence to equate parse probability with beauty.

### Ranked rules for Luthier to encode

The ranking weighs how much each rule addresses "too simple", how strong its evidence is, and how cheaply a rule-based engine can implement it. "Consensus" means practitioner agreement across two or more independent bodies. "Engine" means the engine's own measurements. "Inferred" means a design step derived from cited material but not tested.

| Rank | Rule | Concrete encoding | Evidence |
|---|---|---|---|
| 1 | **Stanza-role plan for hymns and carols** | Intro (first and last phrase, or refrain) → st. 1 hymnal harmony → inner stanzas each with a different texture from a menu (melody solo, tenor solo, alto up an octave, manuals only, pedal point), chosen by text mood → optional lighter penultimate → optional 2–4-bar interlude → final stanza unison melody with free accompaniment → ending over a pedal point | Consensus (PCUSA, Brink, Nisbet, Wikipedia); texture menu single-author |
| 2 | **Density bands by role, not one setting** | Congregational stanzas: RH at least the tune's own onset rate, 4 voices. Free stanzas, interludes and piano songs: 3/4 RH 1.13–1.95, LH 0.88–1.51, complementarity 50–73%; 6/8 RH about 2.4 a beat, broken texture leading. Rise in activity and register into the last verse or chorus | Engine (Lieder tables); build curve qualitative (POP909) |
| 3 | **Texture templates separate from chords** | Store each template as onset grid × chord-tone index × register, labelled in Algomus syntax (`M1/H3h`, `M1/HS1b`); write native 3/4 and 6/8 templates harvested from Lieder; cap stereotyped figures (waltz, Alberti, rocking) at about 5% of bars | Systems (Wang, AccoMontage); Mozart 5.1%; engine 4% waltz |
| 4 | **Last-verse reharmonisation generator** | Melody fixed; one bass archetype per phrase (tonic pedal, dominant pedal, stepwise descent or ascent, walking); expanded vocabulary (V/x over chromatic bass, vii°7/x, 9ths, 4–3 and 7–6 suspensions, iv or ♭VI borrowed, relative minor at a phrase start); hymnal cadences kept; 5–6 voices plus pedal; continuous, mostly stepwise motion | Consensus (Nisbet, PCUSA, Read, Wikipedia) |
| 5 | **Complementarity in the voice's gaps** | Put fills and secondary-melody fragments where the melody holds or rests, especially at phrase ends; in countermelody layers avoid same-onset arrivals on octaves and fifths with the tune | Directional (Huron 2008; Wang 2020; POP909) |
| 6 | **Phrase-level selection with transition cost** | Choose a template per phrase by Viterbi: fit to melody rhythm and chords + similarity to the neighbouring phrase + matching section label; keep ILS-style ratio near 1.7 (same-label similar, different labels contrasting); in strophic hymns, deliberately break same-label repetition across stanzas | Systems (AccoMontage; whole-song ILS 1.68) |
| 7 | **Modulation interlude module** | Interrupt or extend final tonic; quote the opening motif in the hymn's metre; weaken the old key; whole step via V/V or ii–V of the new key; half step via German sixth respelled as the new V7; applied dominant or vii°7 before the new V with 4–3; rest or held V7 before entry; never longer than one stanza | Consensus (Read, Gehring/AGO, Overduin); chord spellings inferred |
| 8 | **Expectation judge for reharmonised stanzas** | Score chord information content with IDyOM or `ppm`, short-term model trained on earlier stanzas; reward surprise mid-phrase where entropy is low, require low surprise at cadences; reject globally extreme means | Strong for the interaction (Cheung et al. 2019); inverted U secondary; stanza application inferred |
| 9 | **Descant as an option tied to rewritten harmony** | Offer only on the final stanza; regenerate the harmony against the descant; never on by default | Wikipedia; King's history (Williams thesis) |
| 10 | **Style-specific harmony priors and form lift** | Hymn and carol: common-practice voice leading and V→I cadences. Worship and pop piano: Rock-Corpus priors (IV→I, ♭VII); accompaniment lift at the chorus onset (telos) | Rock Corpus counts; Nobile (analytic) |
| 11 | **Voice-leading constraints switched by texture** | Block pads may move homorhythmically; independent layers avoid parallel perfects with the tune; accompaniment top voice below the melody; wide spacing low, close high; bass–top tenths favoured in arpeggios | Weak (Huron 2001 abstract only; pedagogy) |
| 12 | **Do not use as quality judges** | GTTM trees, grammar parse probability and note-level schema detectors: use only as generators or position-tied checks | No liking evidence; schema precision about 0.01 |

### Ranked datasets for accompaniment tables

Datasets are ranked by usefulness for building separated-accompaniment tables in 3/4, 6/8 and modern styles, weighted by licence safety. Metre counts were **computed by the research team from cloned repositories on 2026-11-15** unless marked otherwise. "First" means the first time signature in the file and "any" means the signature appears anywhere.

| Rank | Dataset | Melody and accompaniment kept apart? | Metre counts | Size, format | Licence | How to get |
|---|---|---|---|---|---|---|
| 1 | OpenScore Lieder | Yes: voice + piano staves; 1,156 Roman-numeral analyses | first: 4/4 421, 3/4 265, 2/4 237, 6/8 216, 9/8 33, 12/8 20; any: 3/4 332, 6/8 247, 9/8 50, 12/8 30 | 1,352 .mscx / 1,462 .mxl | **CC0 1.0** | `git clone https://github.com/OpenScore/Lieder` ([repo](https://github.com/OpenScore/Lieder)) |
| 2 | Open Hymnal Project | Yes: SATB voices (286 of 305 in four parts); hymnal harmony only | first: 4/4 203, 3/4 48, 6/4 10, 3/2 7, 6/8 6, 2/4 5, 9/8 1 | 305 ABC | No licence file; headers say PD or freely distributable | `git clone https://github.com/mzealey/openhymnal` ([repo](https://github.com/mzealey/openhymnal)) |
| 3 | POP909 | Yes: MELODY, BRIDGE, PIANO tracks in every file | 880 in 4/4, 29 in 3/4 or 6/8 by downbeats (about 52 by metadata); ignore MIDI TS events | 909 MIDI + beat, chord, key files | **MIT** | `git clone https://github.com/music-x-lab/POP909-Dataset` ([repo](https://www.github.com/music-x-lab/POP909-Dataset)) |
| 4 | PDMX (no-conflict subset) | Multi-part scores; `n_tracks`, `tracks`, genre and lyric columns allow filtering | Not counted | 222,856 of >250K MusicXML; MXL 1.9 GB | CC BY 4.0 umbrella; **12.29% conflicting per-song licences** | Zenodo DOI 10.5281/zenodo.15571083 ([record](https://zenodo.org/records/15571083)) |
| 5 | Hymnary.org PD tunes | Standard four-part harmonisations | Per tune | PDF, MusicXML, MIDI | PD tunes; download terms not stated | Per-tune pages, e.g. [OLD 100TH](https://hymnary.org/tune/old_100th) |
| 6 | IMSLP free-accompaniment scans (Bairstow 1941; Coleman 1953) | Organ parts for unison stanzas; pair with hymnal settings of the same tunes | Not counted | 44 pp. and 32 pp. PDF; needs OMR | Bairstow PD outside US; Coleman PD in life+50 countries; both non-PD in US | [Bairstow](https://cn.imslp.org/wiki/Organ_Accompaniments_to_24_Unison_Hymn-Tune_Verses_(Bairstow,_Edward_Cuthbert)), [Coleman](https://imslp.org/wiki/Varied_Hymn_Accompaniments_(Coleman,_Henry)) |
| 7 | Lakh MIDI | Multi-track; melody track must be identified | Not counted (host unreachable) | 176,581 MIDI (45,129 matched) | **CC BY 4.0** | lmd_full.tar.gz from the [LMD page](https://colinraffel.com/projects/lmd/) |
| 8 | Mozart texture annotations (Algomus) | Bar-level M/H/S texture labels on piano scores | Not broken down by metre | 1,164 bar labels, 9 movements | Not stated in notes | algomus.fr/data; notes at DCMLab ([ISMIR 2022](https://archives.ismir.net/ismir2022/paper/000061.pdf)) |
| 9 | Pop1K7 | No: single piano part | **All 4/4** (published) | 1,747 MIDI, about 108 h | **CC BY 4.0** | Zenodo DOI 10.5281/zenodo.13167761 ([record](https://zenodo.org/records/13167761)) |
| 10 | Rock Corpus (RS 200) | Melody + harmony + timing, no accompaniment | Not counted | 200 songs, text encodings | **CC BY 4.0** | [rockcorpus.midside.com](https://rockcorpus.midside.com/) |
| 11 | OpenEWLD | Lead sheets: melody + chord symbols only | first: 4/4 287, 2/2 94, 3/4 80, 6/8 13, 12/8 1 | 502 MXL | **MIT** (PD content) | `git clone https://github.com/00sapo/OpenEWLD` ([repo](https://github.com/00sapo/OpenEWLD)) |
| 12 | Nottingham (jukedeck) | Melody + chords only | MIDI first: 4/4 1,607, 6/8 1,107, 3/4 178, 9/8 41 | 3,089 MIDI / ABC | **GPL-3.0** | [jukedeck/nottingham-dataset](https://github.com/jukedeck/nottingham-dataset) |
| 13 | Hooktheory (Sheet Sage) | Melody + chords only | first: 4/4 23,722, 6/4 1,266, 3/4 969, 6/8 47, 12/8 36 | 26,175 annotations, JSON | CC BY-NC-SA 3.0 | [sheetsage-data](https://github.com/chrisdonahue/sheetsage-data) |
| 14 | ASAP | Classical piano scores, no voice | first: 4/4 80, 3/4 43, 6/8 26, 12/8 8, 9/8 6 | 242 MusicXML | CC BY-NC-SA 4.0 | [asap-dataset](https://github.com/CPJKU/asap-dataset) |
| 15 | Restricted pools: GigaMIDI, MetaMIDI, Aria-MIDI, EMOPIA, MAESTRO | Mixed; mostly piano-only or unlabelled tracks | Not counted | 0.4M–2.1M MIDI (pools) | Non-commercial or research-only, some gated | [GigaMIDI](https://huggingface.co/datasets/Metacreation/GigaMIDI), [MetaMIDI](https://zenodo.org/records/5142664), [Aria-MIDI](https://arxiv.org/html/2504.15071v1) |

The table points to an uncomfortable split. Licence-clean triple and compound accompaniment exists only in 19th-century art song and public-domain hymnody. Licence-clean modern accompaniment exists only in 4/4 Chinese pop. Modern worship, theatre and film in 3/4 and 6/8 can come only from PDMX, after licence vetting by genre, or from arrangements the user owns. Slakh2100's licence could not be verified, and Lakh, Slakh and PDMX metre distributions remain uncounted.

### Conclusion

This research changes the diagnosis. "Too simple" in a hymn or carol accompaniment is first a failure of arrangement across verses and only second a failure of note density. The engine's 15% complementarity in verses 1–3 is close to idiomatic for congregational stanzas. What is missing is the free final stanza, the varied inner stanzas and the interlude that real organists use. The expectation research explains why that plan works. A tune made predictable by repetition is the context in which harmonic surprise gives the most pleasure, so the engine already has a principled judge (IDyOM's short-term model trained on the earlier stanzas) for the one stanza where it should take risks.

The biggest opportunity is in the data. No published corpus statistics exist for 3/4 or 6/8 accompaniment figures, for complementarity targets, or for how far free organ accompaniments depart from hymnal harmony. The engine's Lieder tables already fill the first two gaps. A small paired corpus fills the third: Open Hymnal or Hymnary settings matched against OMR'd Bairstow and Coleman free settings of the same tunes, which would measure the share of re-harmonised beats and the cadences preserved. That would give Luthier its last-verse rules from measurement rather than from the practitioners alone, and it would be a result the field does not yet have.

\newpage

# Part 5. Shapes of music like story arcs (research report)

## Songs climb late, but shapes remain unproven

No one has published a musical counterpart to Vonnegut's story shapes: a small set of whole-song tension, energy or melodic-height curves found in data and linked to quality or success. Two things exist instead. The first is a set of continuous tendencies. Melodic phrases lean arched and descending, pop songs cycle between low verses and high choruses while rising overall, arousal peaks about three-quarters of the way through, and listeners' remembered intensity follows the average moment more than the peak ([Cornelissen et al., ISMIR 2021](https://archives.ismir.net/ismir2021/paper/000016.pdf); [Lyu 2026](https://arxiv.org/abs/2609.15675); [Schäfer et al. 2014](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00911/full)). The second is a warning. A 2026 study found that melodic contours in nine corpora **do not form clusters at all**, and that k-means returns the familiar ascending, descending, convex and concave "types" even from synthetic contours with no cluster structure, "for primarily mathematical, not musical reasons" ([Cornelissen et al. 2026](https://arxiv.org/html/2604.13119v1)). The story-arc result is itself softer than its reputation. Reagan et al.'s "six" depends on the method chosen, their download differences were never tested for significance, and the best-controlled successor finds shape effects of about 0.05 rating points per standard deviation ([Reagan et al. 2016](https://arxiv.org/pdf/1606.07772); [Toubia et al. 2021](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/How-Quantifying-the-Shapes-of-Stories-Predicts-their-Success.pdf)). For Luthier, the practical result is a handful of graded shape rules that can be adopted now (plan an intensity curve from the parameters listeners actually track, keep the average up, peak in the last third, escalate repeats), and a study the field has not yet done. That study can start today from a Hymnary.org export already on disk, provided it treats "are there shapes at all?" as a null-model question rather than an assumption.

### Six story arcs rest on soft method and weak success links

Vonnegut's idea was a single "fortune" line drawn from beginning to end, with named shapes such as "Man in Hole": "somebody gets into trouble, gets out of it again," with the line ending "higher than where it began" ([The Marginalian](https://www.themarginalian.org/2012/11/26/kurt-vonnegut-on-the-shapes-of-stories/)). He also gave the template's own limit. Hamlet will not fit it, and the rise-and-fall pattern "pretends that we know more about life than we really do" ([Big Think](https://bigthink.com/high-culture/vonnegut-shapes/)). That caveat matters for music. It says conformity to a shape and greatness may have nothing to do with each other.

Reagan and colleagues turned the idea into a pipeline. They scored **1,327 Project Gutenberg books** with the labMT hedonometer in a 10,000-word sliding window, mean-centred the arcs, and decomposed them by SVD, Ward clustering and an 8×8 self-organising map ([Reagan et al. 2016](https://arxiv.org/pdf/1606.07772)). The "six arcs" (Rags to riches, Tragedy, Man in a hole, Icarus, Cinderella, Oedipus) come from pairing the first three SVD modes with their sign-flips. Ward clustering gave **four** dominant groups and the SOM gave **five**, so the number six is partly a counting convention. The authors' null models (shuffled "word salad" and Markov "nonsense" text) produced a flatter SVD spectrum and much lower Ward linkage cost (about 1,400 against 7,000), which they took as proof the arcs are not a method artefact. On success, the evidence is slight. Median downloads by mode ran from about **80 to 105.5**, against variances in the millions. The authors called downloads "only a rough proxy for success" and reported no significance test.

The critiques fall on three points, and each transfers to music. Lexicon sentiment is unvalidated: a 2023 review found most tools "still lack a validation," and an ensemble of 34 sentiment models found that even Transformer models "exhibited consistent disagreement between each other" ([Rebora 2023](https://iris.univr.it/bitstream/11562/1115884/2/Rebora%20-%202023%20-%20Sentiment%20Analysis%20in%20Literary%20Studies.%20A%20Critical.pdf); [Chun 2021](https://www.arxiv.org/pdf/2110.09454)). Smoothing can manufacture shapes. Fourier low-pass filters assume periodicity, so they drag the end of an arc back toward its start and ring with phantom humps; Ben Schmidt showed a plain rise from −5 to +5 turning wavy under the default filter but not under loess ([Schmidt 2015](https://benschmidt.org/2015/04/03/commodius-vici-of-recirculation-the-real-problem-with-syuzhet/)). The package's author conceded that "there really *can* be ringing artifacts" ([Jockers 2015](https://www.matthewjockers.net/?p=1408)). Finally, valence is not plot, and different success measures disagree.

The successors show how much the success claim shrinks under controls. In **6,174 films**, Del Vecchio et al. chose k = 6 themselves from k = 4 to 12, which makes the study a re-application, not an independent rediscovery. Man-in-a-hole films earned $6.56M more domestically with no controls (p < 0.001). With budget added, the effect fell to p = 0.055, and those films were rated slightly *lower* (6.45 against 6.52), leading the authors to call them "talked about" rather than "liked" ([Del Vecchio et al. 2018](https://arxiv.org/pdf/1807.02221)). Boyd, Blackburn and Pennebaker found one consistent narrative arc across about 40,000 traditional narratives, with **modest effects** (partial η² from 0.018 to 0.085) "unlikely to be visible to the human eye," and "no meaningful main effect or interaction" with IMDb rating group across 18,074 films ([Boyd et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7413736)). The best-controlled study, Toubia, Berger and Eliashberg, used year and genre fixed effects, length and 100 topic controls. One standard deviation of semantic "speed" was worth **+0.048 IMDb rating points** for films and +0.072 for TV, on scales with an SD of about 1 ([Toubia et al. 2021](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/How-Quantifying-the-Shapes-of-Stories-Predicts-their-Success.pdf)). The Bestseller Code's 80% accuracy came from class-balanced cross-validation that mixed theme, style and plot ([UNL Research](https://research.unl.edu/blog/supercomputer-helps-crack-the-code-for-bestselling-books/)), while under 0.5% of new fiction reaches the NYT list ([New Republic](https://www.newrepublic.com/article/137280/whats-purpose-bestseller)). Its plot-only contribution was never published.

The story-arc field therefore leaves three lessons for music. Arcs exist as average tendencies. Their number is a modelling decision. Their link to success is small and depends on which success you measure. One further problem emerges below. Reagan's null models answer the question "is there temporal structure?", not "are there discrete types?", and the 2026 contour paper shows those are different questions.

### Music has tendencies, not types, and contour may not cluster at all

#### The only song-arc typologies measure the lyrics

The two published attempts to cluster song arcs Reagan-style both work on words. Rösch and Rauch scored line-level lyric sentiment with `syuzhet`, smoothed with a discrete cosine transform, normalised to 0–100% of the song and ran k-means into six clusters matched to Reagan's archetypes. They used about 6,587 US chart lyrics (1977–2022) as reference and **176 Bundesvision Song Contest songs** as the outcome set. Man-in-a-hole and Icarus songs scored better, and sad endings averaged 4.055 points against 3.348 for happy ones, a correlational result ([Rösch & Rauch 2025](https://link.springer.com/article/10.1007/s10824-025-09532-6)). A UK drill study of 550 songs used the same DCT-to-100-points method and found only **k = 2** mirror-image clusters. The positive cluster had about 1.89 times the YouTube views, and the authors asked for corroboration ([Kleinberg & McFarlane](https://arxiv.org/abs/1911.01324)). That is a difference in overall level ("happier lyrics get more views"), not in shape. A 2024 study of 12,280 lyrics found one average arc, with staging early and cognitive tension peaking mid-song, and reported no popularity link in its abstract ([Alberhasky & Durkee 2024](https://doaj.org/article/b8e7f4e79e52458589979532040b2095)). For a songwriting engine, these studies describe the lyric layer. They say nothing about the melody, harmony or accompaniment.

#### Melodic contour forms a continuum, and clustering invents the four classic shapes

The strongest musical evidence on shape is a negative result, and it bears directly on any Luthier study. Cornelissen, Zuidema, Burgoyne and Honing tested phrase contours from nine datasets (Essen German folksongs, Nova Scotia songs, three Chinese subsets and Gregorian chant). They resampled each contour to 50 points and tried eight representations and several distance measures. Their "dist-dip" test applies Hartigan's dip test to the distribution of pairwise distances, which becomes multimodal when real clusters exist. **No representation, metric or dataset showed clustering**, although the test did find planted clusters in a synthetic control (via a 10-dimensional UMAP projection). Most important, k-means run on *synthetic, unclustered* contours placed its four centroids near the first two principal axes, "resulting in ascending, descending, convex and concave shapes—for primarily mathematical, not musical reasons," because "the principal components of such data approximate cosines of increasing frequency." The authors attribute an earlier four-shape finding to this artefact, show that Huron's nine-type contour typology shifts its type frequencies with an arbitrary tolerance parameter, and recommend treating contour as a continuous character and testing clusterability before adopting any typology ([Cornelissen et al. 2026](https://arxiv.org/html/2604.13119v1)). Their code is public at github.com/bacor/shapes-of-music.

The same mathematics applies to Reagan's SVD modes. A smooth random curve, decomposed by SVD, yields a monotone first mode, a single-hump second mode and a two-hump third. Those are Rags to riches, Icarus or Man in a hole, and Cinderella or Oedipus. The story arcs beat shuffled-word nulls, but shuffled words produce nearly flat curves, so any autocorrelated signal would beat them. No one has tested story or song arcs against a null that is smooth and autocorrelated but unclustered. That is the test this report recommends below.

What contour *does* show is a continuous lean. In the cosine-contour representation (DCT of a resampled pitch line, with the first coefficient read as "descendingness" and the negated second as "archedness"), German and Chinese folksong phrases were significantly more descending and arched than random segments of the same melodies (p < 0.001). The paper also reports a scale result that matters for whole-song work: capturing 95% of contour variance takes **one dimension for motifs, nine for phrases and 61 for whole songs** ([Cornelissen et al., ISMIR 2021](https://archives.ismir.net/ismir2021/paper/000016.pdf)). A raw pitch line across a whole song is not low-dimensional, so a whole-song "melodic height" shape has to be a smoothed envelope of something, not the contour itself.

#### Pop songs show local cycles that accumulate toward a late peak

The best whole-song description comes from audio, not notation. Lyu annotated 1,046 sections in **100 Chinese pop songs** and estimated valence and arousal every 0.5 s with frozen audio models trained on PMEmo. The values are model estimates, not listener ratings. Arousal rose from verse (−0.088) to pre-chorus (0.107) to chorus (0.215) to bridge (0.270). Chorus exceeded verse in 99% of songs. Repeated sections escalated: from first to last occurrence, chorus arousal rose by 0.225. Average arousal peaked at normalised position **0.78**, and the highest-arousal section sat at a mean of 0.733, in the final third in 79 of 100 songs. It was a chorus in 53 songs but the *final* chorus in only 31. Paths were far from monotonic (directness 0.242), which the author summarises as "local cycles–global accumulation." **No trajectory clustering was attempted, and no popularity link was tested** ([Lyu 2026](https://arxiv.org/abs/2609.15675)). At the album level, musicians sequencing five-track sets produced a U-shape in loudness, valence and arousal, with openers and closers highest. The authors liken it to Man in a hole, but the quadratic fit barely beat the linear one (RSS 2534.2 against 2558.2), and liking was not measured ([Neto et al. 2025](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0316963)).

#### Narrative theory offers archetypes that nobody has measured

Music theory has its own archetypes, but they are not curves. Almén's theory of musical narrative crosses order and transgression with victory and defeat to give Frye's four types: Romance, Tragedy, Comedy and Irony. It tracks the fate of marked, unexpected material against unmarked, expected material ([Wu 2018, summarising Almén](https://openscholar.uga.edu/record/6775/files/wu_crystal_w_201805_dma.pdf)). That is a different axis from tension or energy, and no one has quantified it. It could in principle be operationalised (marked material as high-surprisal, minor or chromatic; "victory" as its absorption by the end), but that is untested. Empirically, listeners' imagined story events cluster at moments of salient change in continuous tension ratings ([Margulis et al. 2022](https://collaborate.princeton.edu/en/publications/when-did-that-happen-the-dynamic-unfolding-of-perceived-musical-n/)). Narrative engagement is driven more by culturally learned "topicality" than by contrast ([McAuley et al. 2021](https://collaborate.princeton.edu/en/publications/what-drives-narrative-engagement-with-music/)). The golden-section claim for Mozart sonatas fits some movements (38 + 62 bars) but not others, and it is post hoc ([Science Frontiers](https://science-frontiers.com/sf107/sf107p14.htm)).

### Listeners track loudness and register, and remember the average

#### Score-based tension models miss what listeners weight most

Any "tension arc" for a symbolic engine has to start from what listeners report. Every listener-validated model finds that dynamics and pitch height dominate, and that harmony adds little once those are included. Farbood's parametric model gave dynamics and melodic pitch height weight 3, tempo and onset frequency 2, and harmony and lower-voice height 1. It fitted mean continuous ratings at r = .67 to .99. Inter-subject agreement was only r = .47, and a melodic-expectation component was dropped because it "did not correlate in a clear directional way with tension" ([Farbood 2012](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/Farbood_2012_Musical_Tension.pdf)). TenseMusic, an open audio pipeline, reached cross-validated r = .61 on 38 classical excerpts. Loudness carried the largest weight, roughness predicted well, and "the predictive power of tonal tension was small" ([Barchet et al. 2024](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0296385)). Granot and Eitan's 132 listeners found that loudness change, pitch direction and register drove tension, that parameters interacted rather than adding, and that a *lower* register sounded more tense overall ([Granot & Eitan 2011](https://cris.huji.ac.il/en/publications/musical-tension-and-the-interaction-of-dynamic-auditory-parameter/)). Their lower-is-tenser result and Farbood's rising-pitch effect likely reflect level versus change. In a 15.5-minute orchestral work, 90 listeners agreed on arousal and intensity across musical backgrounds but diverged on valence, and no valence curve correlated with any acoustic feature ([Heng et al. 2025](https://www.mcgill.ca/mpcl/files/mpcl/heng_2026_muspercept.pdf)). For shape work, that makes **arousal or intensity a measurable axis and valence an unreliable one**, the reverse of the story-arc literature's choice. A 2026 neural study adds that long-term IDyOM surprisal tracked continuous tension for most pieces, while within-piece surprisal did not ([bioRxiv 2026](https://www.biorxiv.org/content/10.64898/2026.01.15.699693v1.full)).

The harmonic-tension tools that can be computed from notes are real but less validated. Lerdahl and Krumhansl's model, automated as AuToTen, fits listener judgements at an average adjusted R² of .72, but it needs GTTM prolongational trees as input ([Ruiz-Marcos et al. 2020](https://core.ac.uk/download/337616552.pdf)). Herremans and Chew's spiral-array "tension ribbons" (cloud diameter, cloud momentum, tensile strain) are one call in `partitura` (`estimate_tonaltension`) and are also implemented in midi-miner ([partitura](https://partitura.readthedocs.io/en/latest/_modules/partitura/musicanalysis/tonal_tension.html); [Guo et al.](https://ar5iv.labs.arxiv.org/html/1910.02049)). Their behavioural validation is listed as future work in the system that uses them ([MorpheuS](https://ar5iv.labs.arxiv.org/html/1812.04832)). Generating music to a target curve is demonstrated. MorpheuS matched template tension profiles at r = 0.97 to 0.999, and a 2025 Transformer beam search raised curve adherence from 0.16 to 0.50 ([Ebrahimzadeh et al. 2025](https://arxiv.org/abs/2511.19342)). Neither showed that following a curve makes music better liked.

#### Memory follows the average, with a bonus for peaks, ends and steep rises

How listeners summarise a whole song decides which shape features matter. Schäfer, Zimmermann and Sedlmeier had 54 listeners rate felt intensity continuously through 11 complete, unfamiliar songs. Average intensity was the best predictor of remembered intensity (r = .805, β ≈ .58). The peak-end average added a smaller, significant amount (β ≈ .25). Variation and number of peaks did not. Remembered intensity correlated with liking at **r = .63** ([Schäfer et al. 2014](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00911/full)). In Rozin et al.'s earlier work, summarised there, peak-end was the best predictor for only 3 of 20 listeners, but large moment-to-moment *increases* raised remembered intensity (a "slope effect"). Krumhansl's Mozart study found that section endings coincided with tension peaks and new ideas with low tension ([Krumhansl 1996](https://scilit.com/publications/8d3965b5bfb58299a82af9527b9bf04c)).

#### Builds, drops and boundaries have behavioural and physiological signatures

The clearest evidence that shape changes experience comes from build-and-arrival structures and from section boundaries. Dancers' motion fell in a house-music breakdown and peaked at the drop. **78%** rated the track with a full break routine (layered build, rising pitch, snare roll, then bass and kick returning) quite or very pleasurable, against 46–53% for tracks with little structural change ([Solberg & Jensenius 2016](https://core.ac.uk/download/225893003.pdf)). Drops produced significantly higher skin-conductance responses than other sections ([Solberg & Dibben 2019](https://eprints.whiterose.ac.uk/145911/)). In EDM build-ups, a plain **linear ramp predicted listener tension better on average** than a feature model ([Bilious & Dahl 2026](https://zenodo.org/records/24023747)), which suggests listeners report a learned schema ("it rises until the drop") rather than tracking features. Chills cluster at sudden dynamic or textural changes, unprepared harmonies and the entry of a new voice or instrument (Sloboda 1991 and Grewe et al. 2007, as summarised by [Bannister & Eerola 2021](https://durham-repository.worktribe.com/OutputFile/1234646)). At streaming scale, Spotify skip curves are song-specific and stable across cohorts. Skips surge about **3.5 s after section boundaries**, so strongly that a network predicted boundaries from skip profiles alone (F = 0.630), and silent or long-fade endings attract skips ([Montecchio et al. 2020](https://ar5iv.labs.arxiv.org/html/1903.06008)). About 24% of plays are skipped within 5 s ([Lamere 2014](https://musicmachinery.com/2014/05/02/the-skip/)). The largest gap in this literature is plain: **no controlled experiment was found that manipulates a piece's global shape** (early against late climax, arch against ramp, flat against escalating choruses) and measures liking.

### Shape's share of musical success has never been measured

Hit-song science predicts success modestly from static features and almost never uses time-course features. A dance-hit classifier built on whole-track timbre statistics reached AUC 0.65 in cross-validation and 0.81 on an out-of-time test ([Herremans et al. 2014](https://ar5iv.labs.arxiv.org/html/1905.08076)). A wide-and-deep network reached 75% accuracy on a balanced Million Song Dataset sample, and **release year was the most important high-level feature** ([Zangerle et al. 2019](https://archives.ismir.net/ismir2019/paper/000037.pdf)). Typicality bends the odds of reaching No. 1 in an inverted U across 26,846 Hot 100 songs, but one SD below mean typicality is worth about half a week on the chart, and the OLS R² for peak position was .047. Label, prior hits and era carried much of the explained variance ([Askin & Mauskapf 2017](https://Www.Gwern.net/doc/culture/2017-askin.pdf)). In the Hooked! study, musical features explained a marginal R² of 0.10 at best for recognisability, against 0.47 once song identity was included ([Van Balen et al. 2015](https://eprints-gro.gold.ac.uk/17202/1/Vanbalenetal_ISMIR_2015.pdf)).

The few time-course tests are mixed. Top-10 intros shrank from over 20 s in the mid-1980s to about 5 s by 2015. But comparing an artist's most- and least-streamed songs on Spotify, Léveillé Gauvin found no support for the idea that grabbing attention sooner earns more streams ([phys.org on Léveillé Gauvin](https://phys.org/news/2017-04-music-streaming-instrumental-intro.pdf)). Earworms, matched to non-earworms on chart history, share a **common global melodic contour with unusual intervals**, and adding melodic features improved model fit significantly (χ² = 55.52), with 62.5% leave-one-out accuracy ([Jakubowski et al. 2017](https://www.apa.org/pubs/journals/releases/aca-aca0000090.pdf)). The expectation result from Billboard harmony is the strongest link between a time-varying property and pleasure. Listeners enjoyed surprising chords in predictable contexts and predictable chords in uncertain ones, a pattern measured across 745 songs ([Cheung et al. 2019](https://cms.mus.cam.ac.uk/publications/cheung-uncertainty-surprise/)). That is a local, moment-by-moment property, not a whole-song shape.

The likely order of influence on success, from everything read, is exposure, fame and era first, static sound features and typicality next, and whole-song shape a distant and unmeasured last. Del Vecchio's films and Lyu's pop data add a reason to separate outcomes. Reach (views, gross, chart weeks) and liking (ratings, remembered intensity) can move in opposite directions for the same shape. Spotify also removed the `popularity` field from Development Mode apps in February–March 2026, which closes the cheapest route to a fresh streaming outcome ([Spotify migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)).

### Three tiers of evidence sort the claims

The table separates what a reader can rely on from what is suggestive and what is untested. "Established" means replicated listener or behavioural data. "Suggestive" means a single study, descriptive corpus regularity or a weak or confounded association. "Untested" means nobody has looked, or the only evidence is theoretical.

| Tier | Claim | Basis |
|---|---|---|
| Established | Felt tension and arousal track loudness, register and density more than harmony | Farbood 2012; TenseMusic 2024; Granot & Eitan 2011; Heng et al. 2025 |
| Established | Listeners agree on arousal/intensity curves far better than on valence curves | Heng et al. 2025; Farbood inter-subject r = .47 |
| Established | Remembered intensity follows the mean moment, with a smaller peak-end bonus; it correlates with liking (r = .63) | Schäfer et al. 2014; Rozin et al. 2004 |
| Established | Section boundaries are behavioural events (skip surges ~3.5 s later) | Montecchio et al. 2020 |
| Established | Story arcs exist as average tendencies, but shape-success links shrink to small effects under controls | Reagan; Del Vecchio; Boyd; Toubia |
| Established | Phrase contours lean arched/descending relative to random segments but do not cluster into types | Cornelissen et al. 2021, 2026 |
| Suggestive | Pop arousal peaks around 0.73–0.78 of duration, with verse < pre-chorus < chorus and escalating repeats | One 100-song study with model-estimated arousal (Lyu 2026) |
| Suggestive | Build-up then drop raises pleasure and arousal; a linear ramp is the schema listeners report | Solberg & Jensenius 2016; Solberg & Dibben 2019; Bilious & Dahl 2026 |
| Suggestive | Chills follow texture thickening, new voices and unprepared harmony | Secondary summaries of Sloboda, Grewe (Bannister & Eerola 2021) |
| Suggestive | Lyric arc shapes relate to contest points (Man in a hole, Icarus better; sad endings better) | One contest, 176 songs (Rösch & Rauch 2025) |
| Suggestive | Conventional global contour with unusual intervals marks earworms | Jakubowski et al. 2017 |
| Untested | A small set of discrete whole-song musical shapes exists | No study with a clusterability test |
| Untested | Any whole-song musical shape predicts charts, streams, hymnal adoption or ratings | No study |
| Untested | Manipulating global shape (peak placement, escalation) changes liking | No controlled experiment |
| Untested | Golden-section peak placement matters | Post hoc Mozart fits only |
| Untested | Almén's narrative archetypes can be measured or affect response | Theory only |

### The field can be built from corpora already in hand

#### Outcome labels exist for hymns today and for songs one download away

Nothing on disk before this round carried a usable success label. The workspace holds OpenScore Lieder, Hooktheory clips, POP909, SymbTr, the music21 corpus (including 408 Bach chorales) and the Open Hymnal, all without outcomes (team inventory, 2026-11-15). The new Hymnary.org export changes that. Its **Total Instances** column counts published text-tune pairings per tune, and it can be exported as CSV from any tune listing ([Hymnary.org](https://hymnary.org/tunes?prefix=aa)). The team's `tunes_top5000.csv` holds 5,000 tunes from OLD HUNDRED (2,430 instances), WEBB (2,078) and DUKE STREET (1,866) down to 15. The median is 33 and the quartiles 20 / 33 / 72 (team count). A further check for this report found that the `incipit` field is a **scale-degree code of the opening 15 or 20 notes** (1,951 rows with 15 digits, 1,715 with 20). OLD HUNDRED reads 1 1 7 6 5 1 2 3 3 3 2 1 4 3 2 and DUKE STREET 1 3 4 5 6 7 1 7 6 5, both correct against the tunes. That makes a 5,000-tune study of opening-line contour against adoption possible without parsing a single score, at the cost of having no rhythm, no octave and no material past the opening. The composer field carries a year in only 665 rows, so a tune-date control will need per-tune lookups (team check).

For full-stanza shapes, the Open Hymnal supplies SATB scores: 305 ABC files with 272 distinct tune names ([mzealey/openhymnal](https://github.com/mzealey/openhymnal)). **134 of those names matched a Hymnary top-5000 title** after normalisation (team count). That join has a selection problem the study must fix. The matched tunes' instances run from 15 to 1,866 with a median of 301, nine times the Hymnary median of 33. The Open Hymnal collects well-known tunes, and unmatched names are either misspelled or below the top-5000 cut-off, so the sample is range-restricted on the outcome. The fix is to export Hymnary's full tune list (not just the top 5,000) and resolve spelling variants by hand, so that low-instance tunes enter the sample instead of dropping out of it.

For songs, three corpora define the scope:

| Corpus | Size | Outcome | What its arc can measure | Status |
|---|---|---|---|---|
| McGill Billboard 2.0 | 890 randomly sampled Hot 100 chart slots, CC0 | `peak_rank`, `weeks_on_chart`, `chart_date` | Harmony and section labels with timing; no melody | Files on Dropbox and Zenodo, both blocked from this session; user upload or an allowed mirror needed ([mirdata](https://mirdata.readthedocs.io/en/latest/_modules/mirdata/datasets/billboard.html)) |
| Rock Corpus (RS 200) | 200 songs, CC BY 4.0 | Rolling Stone 500 rank (range-restricted) | Melody, harmony and timing | Host not yet tested ([rockcorpus.midside.com](https://rockcorpus.midside.com/)) |
| Lakh MIDI matched × MSD | 45,129 MIDI files, CC BY 4.0 | `song_hotttnesss`, with `artist_familiarity`, `artist_hotttnesss` and `year` as controls | Full multi-track MIDI; MSD also stores audio `segments_loudness` and `sections_start` | Not on disk ([LMD](https://colinraffel.com/projects/lmd/); [MSD paper](https://www.ee.columbia.edu/~dpwe/pubs/BertEWL11-msd.pdf)) |

McGill is the cleanest song test because the chart slots were sampled at random. It contains minor hits as well as number ones, and the era and the outcome arrive with the annotations. Its limit is serious. It carries chords and sections but no melody, and the listener evidence says harmony is the *weakest* driver of felt tension. Its most informative arc is therefore the **section sequence**: where the first chorus falls, how often choruses recur, where the bridge sits and how harmonic rhythm changes by section. Root-distance curves are secondary. Its outcome measures how big a hit was among charting songs, not hit against non-hit. The Rock Corpus is the melody check: it validates whether chord-only arcs track melodic arcs. Lakh × MSD is the scale replication. It has one feature no other corpus offers. MSD's audio loudness curves for the same songs allow the symbolic intensity composite to be validated against real loudness. Its outcome, though, is a single opaque 2010–11 Echo Nest snapshot, and the fan-made MIDI varies in fidelity. Further options are PDMX's 14,182 user-rated scores ([PDMX paper](https://arxiv.org/html/2409.10831v2)) and Meertens tune-family size as a folk "transmission success" measure ([MTC](https://www.liederenbank.nl/mtc/)). The Session must be excluded, because its licence forbids processing with LLMs ([TheSession-data](https://www.github.com/adactio/TheSession-data)).

#### Per-bar measures should favour intensity over harmony

The measure set follows the listener evidence. Weight dynamics, register and density first, with harmony as a separate, secondary channel. Installed music21 (BSD-3) and mido already parse a Lieder score of 80 bars in 0.47 s and an Open Hymnal ABC in 0.12 s (team test). `partitura` (Apache-2.0) adds spiral-array tension ([PyPI](https://pypi.org/project/partitura/)). IDyOM surprisal needs a Lisp toolchain and has no stated licence ([IDyOM wiki](https://code.soundsoftware.ac.uk/projects/idyom-project/wiki/Idyom)), so it belongs in a second phase.

| Channel | Per-bar measure | Hymns | McGill | Rock Corpus | Lakh |
|---|---|---|---|---|---|
| Register | Mean and maximum melody pitch; whole-texture span | Soprano | none | Yes | Melody track needed |
| Density | Onsets per beat, all parts; harmonic rhythm | Yes | Harmonic rhythm only | Yes | Yes |
| Loudness proxy | Sounding voices; notated dynamics; MIDI velocity | Voice count | none | none | Velocity (weak); MSD audio loudness |
| Harmony | Root distance from tonic on the line of fifths; tensile strain; pitch-class entropy | Yes | Yes | Yes | After chord estimation |
| Contour | DCT coefficients per phrase (descendingness, archedness); position of the highest note | Yes | none | Yes | Yes |
| Structure | Section or phrase label sequence; repetition pattern (AABA etc.) | Phrase form | Native | Native | Inferred |
| Expectation (phase 2) | IDyOM long-term information content and entropy | Yes | Chords | Yes | Yes |

Each channel should be analysed separately, and a z-scored composite of register, density and voice count should serve as the "intensity" analogue of the hedonometer. The composite is a modelling choice, not an established measure. It needs one validation step: against MSD audio loudness for Lakh songs, or against a small continuous-rating panel on rendered hymns.

#### The method copies Reagan's pipeline and fixes its known faults

The time axis depends on the repertoire. Hymn tunes are strophic, so the unit is one stanza of the tune (usually four phrases), binned to 32 points or by half-phrase. Songs map each bar's midpoint to relative time, bin to 100 points, and run a sensitivity check that warps time piecewise between section boundaries so that choruses align. Smoothing must not be a Fourier low-pass. A DCT-II keeping the first 8–12 coefficients, a Savitzky–Golay filter or loess are the safe choices. Before any real data is used, each smoother is tested on synthetic ramps and steps to confirm it invents no humps (Schmidt's test). Each curve is mean-centred and unit-normalised, with the raw level kept as a separate variable, since level and shape are confounded. The songs-by-bins matrix is decomposed by SVD, and clustering (Ward and k-means, with DTW k-means only as a robustness check because warping erases position) runs only if the null-model test below allows it. Outcome models use the leading **SVD or DCT coefficients as continuous predictors**. That follows Toubia rather than Reagan, and it is the better choice at pilot sample sizes. Cluster dummies become a secondary analysis.

#### The null-model test separates "shapes exist" from "shapes are types"

The central test asks two different questions, and conflating them is the story-arc field's main error. The first question is whether songs have *non-random temporal structure*. That is almost certainly yes; a late peak or an arched phrase is enough. The second is whether songs fall into a *small number of discrete shape types*. That is what "six basic arcs" claims, and what Cornelissen et al. found false for contour. Each question needs its own null.

The surrogate families should be generated for every song or tune. Bar shuffles within a song (the analogue of word salad) destroy all order and test question one only. Section or phrase shuffles keep local material and destroy global order, so they test whether the *arrangement* of sections carries shape. Phase-randomised or per-song AR(1) surrogates keep each curve's smoothness and spectrum but carry no shared shape. These are the critical null for question two, because smooth unclustered curves are exactly what makes k-means and SVD return ascending, descending, arch and U "types." Markov melodies or chord sequences trained per corpus test whether shape arises from local grammar alone. Real data and each surrogate set then go through the identical pipeline and are compared on four statistics: variance captured by the first three SVD modes; the dist-dip test on raw pairwise distances and on a 10-dimensional UMAP projection; silhouette and gap statistics; and bootstrap cluster stability (adjusted Rand index across resamples). The method itself must also pass a positive control: synthetic data with five planted shape clusters, which the dist-dip test with UMAP detected in the 2026 study ([Cornelissen et al. 2026](https://arxiv.org/html/2604.13119v1)).

The decision rule should be fixed before outcomes are examined. Discrete shape types are declared only if the real data beat the 95th percentile of *every* surrogate family on clusterability, and the clusters are stable under bootstrap (ARI above about 0.6, a design threshold). Otherwise, shape is reported as continuous coordinates (mean curve plus SVD or DCT coefficients). That outcome is still useful. Luthier can steer by coordinates as easily as by types, and "no types" would be a publishable replication of the contour result at song scale.

#### Controls and power decide what a pilot can detect

Hymnary instances measure editorial adoption over generations. That is arguably closer to judged quality than a chart, but it carries heavy confounds. Older tunes have had longer to accumulate pairings. Common-metre and long-metre tunes can carry far more texts than irregular ones. Denominational canons and cumulative advantage reward tunes that are already popular. The hymn model should be a negative binomial on instances, controlling for poetic metre class, tune date (first publication), tradition (German chorale, English, Welsh, American), composer as a random effect, number of bars and mode. It should report incremental pseudo-R² over the controls in cross-validation, not just p-values. The McGill model should be a negative binomial on weeks on chart plus an ordinal model on peak rank, controlling for chart year (spline), song length, mode and an artist random intercept. Lakh adds `artist_familiarity` as the fame control that the other corpora lack.

Power sets expectations plainly (a standard Fisher-z approximation, two-sided α = .05, 80% power). **134 tunes detect a correlation of about 0.24**, 250 tunes about 0.18, and 5,000 incipits about 0.04. Toubia-sized effects (about 0.05 SD) would need roughly 3,000 cases. The full-stanza hymn pilot can therefore detect only a large shape effect, and a null there is uninformative about small ones. The 5,000-tune incipit study is the only design on disk with power for realistic effect sizes. Metre and age will almost certainly dominate hymn adoption. The scientific question is whether shape adds anything beyond them.

### Ranked recommendations for Luthier

#### (a) Shape rules to adopt now

Grades: **A**, behavioural or listener data at scale, replicated. **B**, controlled listener or lab studies with at least one solid primary source. **C**, descriptive corpus regularity with no outcome test. **D**, practitioner consensus, theory or the report's inference. Thresholds marked "design" are engineering choices, not findings. The rules describe *intensity planning*; they complement the stanza-role and density plans already proposed for Luthier's accompaniment, in which inner stanzas vary texture and the final stanza carries the free, fuller accompaniment ([PCUSA Quicksheet](https://pcusa.org/sites/default/files/2026-07/Improvising%20%26%20Reharmonizing%20in%20Worship%20Quicksheet.pdf)).

| Rank | Rule | Encoding in Luthier's tables | Grade |
|---|---|---|---|
| 1 | **Plan and check an explicit intensity curve built from what listeners track** | Per bar: intensity = mean of z(melody pitch), z(onsets per beat across all parts), z(sounding voices or organ registration level), plus a half-weighted z(harmonic tension). Write the target curve at the form stage; after rendering, compare actual to target and flag bars off by more than 1 SD (design) | B (Farbood; TenseMusic; Granot & Eitan; Heng) |
| 2 | **Keep the average up; contrast by steps, not by long troughs** | No stretch longer than one phrase at the curve's floor (design); quiet sections drop texture or registration but keep rhythmic motion | B (Schäfer et al.: mean β ≈ .58 against peak-end β ≈ .25); threshold D |
| 3 | **One global peak between 0.65 and 0.9 of duration, then a short release** | Pop and worship: peak at the last chorus, bridge-to-chorus arrival or key lift. Hymns: the final stanza's third phrase, with the closing cadence releasing. Do not target 0.618 | C (Lyu 2026: peak at 0.73–0.78, final third in 79%); Krumhansl 1996 section-end peaks |
| 4 | **Local cycles, global accumulation** | Verse < pre-chorus < chorus within each cycle. Each recurrence of a section type one step higher than the last (an added voice, wider spacing, a register step or a density band). Hymns: escalating stanza textures, with an optional quieter penultimate stanza before the final lift | C (Lyu: chorus +0.225 across repeats); D for the hymn mapping |
| 5 | **Ramp into arrivals and mark them with a step** | 2–4-bar near-linear build (rising bass or melody, thickening texture) before a chorus or final stanza; arrival is a sudden change in voices or register rather than a further gradual rise | B (Rozin slope effect; Solberg & Jensenius; Bilious & Dahl linear ramp) |
| 6 | **Climax toolkit at the planned peak** | Combine texture thickening, a new voice (descant, pedal entry, octave doubling), upward registral expansion of the melody, and one less-predictable chord placed where the context is most predictable, resolved safely at the cadence | C (chills via Bannister & Eerola); B for the surprise-in-predictable-context logic (Cheung et al. 2019) |
| 7 | **Give every section boundary a fresh event** | New layer, voice entry, register shift or fill at each section start | A for recorded-pop listener behaviour (Montecchio et al.); D for congregational use |
| 8 | **Score melodic contour continuously, never by type** | Compute DCT descendingness and archedness per candidate phrase; give a mild preference for arched or descending phrases over random-like ones; keep the global contour conventional and allow a few distinctive leaps | B descriptive (Cornelissen et al. 2021); C for quality (Jakubowski et al. 2017) |
| 9 | **Recorded pop and worship: early hook, no dead ends** | Vocal or hook within about 5–10 s; avoid long fades and trailing silence | A behaviour (Lamere; Montecchio), but null for within-artist streams (Léveillé Gauvin) |
| 10 | **Lyric arc as an optional, unscored layer** | Allow a Man-in-a-hole or Icarus lyric plan to be set on request; never score quality by it | C (one contest study) |
| 11 | **Anti-rules** | Do not choose among a fixed menu of N whole-song shapes; do not use golden-section placement; do not claim any shape predicts success; do not use valence as the main arc axis | Contour non-clustering (2026); valence unreliability (Heng) |

Rules 1 to 5 are cheap for a table-driven engine. They need one new table (a target intensity value per bar or phrase, set by form), one new scorer (the per-bar composite) and a comparison step. Rule 1 also produces the logging that stage 4 below needs.

#### (b) A staged plan for a "shapes of songs" study

| Stage | Question | Data | Method and outcome | Go/no-go | Effort |
|---|---|---|---|---|---|
| 0. Instrument | Do the measures and smoothers behave? | Synthetic ramps, steps and planted-cluster sets; 20 hand-checked hymns | Build the per-bar library (music21 + `partitura`); confirm smoothers invent no humps; confirm the dist-dip/UMAP test finds planted clusters; write the pre-registration (measures, N bins, smoothing k, primary hypotheses) | Smoother passes synthetic tests; positive control detected | Days |
| 1a. Hymn incipits (highest power, data on disk) | Does opening-line contour relate to adoption? | 4,996 Hymnary incipits with Total Instances; extend the export below 15 instances | Scale degrees to pitch by nearest-step rule (an assumption; test on Open Hymnal tunes whose scores exist); features: DCT coefficients, peak position, range, leap count. Negative binomial with metre, mode and tune date | Report incremental pseudo-R² and effect per SD; any effect above r ≈ 0.04 is detectable | About a week, including date lookups |
| 1b. Hymn full-stanza pilot | Do stanza-level intensity shapes exist as types, and do they add to adoption? | Open Hymnal (272 tunes) joined to the **full** Hymnary list, with spelling fixes; Bach chorale melodies added by tune name | One stanza, 32 bins; all channels separately plus composite; SVD; full null-model battery; then negative binomial on instances with metre, date, tradition, composer random effect | Types only if they beat every surrogate and are stable; outcome effect interpretable only if r > ~0.2 | One to two weeks |
| 2a. McGill Billboard | Do section and harmonic arcs relate to chart size? | McGill index plus SALAMI chord and section files (needs upload or an allowed host) | Section-sequence features (first-chorus time, chorus count and spacing, bridge position, harmonic-rhythm curve); root-distance arcs secondary; nulls including section shuffles; negative binomial on weeks, ordinal on peak, artist random effect, year spline | Same decision rule; report reach-only interpretation | One to two weeks after data arrive |
| 2b. Rock Corpus check | Do chord-only arcs track melodic arcs? | 200 songs, v2.1 | Correlate harmonic and melodic intensity curves per song; RS rank only as a descriptive outcome | If correlation is low, McGill results speak only to harmony | Days |
| 2c. Lakh × MSD replication | Do findings hold at scale with a fame control? | 45,129 matched MIDI with hotttnesss, familiarity and audio loudness | Validate the symbolic composite against MSD `segments_loudness`; rerun the pre-registered pipeline; `artist_familiarity` and year as controls | Replicate direction and size of stage 1–2 effects | Weeks (melody-track detection) |
| 3. Engine experiment (causal) | Does global shape change liking? | Luthier-generated matched versions of the same songs | Vary one factor at a time: peak at 0.4 against 0.75; flat against escalating choruses; arch against ramp. Within-subject listener ratings of liking and remembered intensity, with continuous intensity tracking on a subset | Fills the field's largest gap; tells the engine which rules earn their place | Weeks, depending on panel size |

Stages 1a and 1b can begin today. Stage 2 waits on the McGill files. Stage 3 is the one only Luthier can run. A rule-based engine can produce versions of the same song that differ only in planned shape, which no corpus can. That is exactly the controlled manipulation the literature lacks.

### Conclusion

The music question looks different after the story-arc evidence is read closely. The famous result is best understood as "narratives have average arcs, and the leading modes of any smooth signal look like named shapes." The six-type reading is weaker. Its link to success shrinks to about a twentieth of a standard deviation once topic, genre and era are controlled. Music already has the first half of that result: arched phrases, sawtooth sections and a late peak. It has good reason to doubt the second, because contour forms a continuum and clustering returns the classic shapes even from structureless data. A "shapes of songs" project should therefore aim to *map the continuum* and test whether types exist, not assume them. It should measure intensity rather than valence, because intensity is what listeners agree on and remember.

For Luthier, the asymmetry is useful. The rules worth adopting now do not depend on discrete shapes or on success prediction. They rest on how listeners track and summarise intensity, so the engine gains from them whether or not the corpus study ever finds types. The study itself has an unusual advantage. Hymnary's adoption counts measure editorial choice over generations rather than marketing, the incipit export gives 5,000 tunes of statistical power immediately, and the engine can run the controlled shape experiment that no one in the field has run. A null result on hymn shapes, properly tested against autocorrelated surrogates, would still be new knowledge.

\newpage

# Part 6. Shapes of songs: the first study

## The answer

Songs share one shape, but they do not come in types. In all three collections, songs build toward a high point late in the piece. Pop songs and MuseScore scores peak around two-thirds to four-fifths of the way through, and hymn opening lines climb to their high point about a quarter of the way in. Around that shared build, though, songs vary smoothly. They do not fall into a handful of shapes the way Reagan found six for stories. Each collection was tested against a featureless continuum with the same spread, and none clustered better than it.

Shape barely predicts success. Across 4,986 hymn tunes, 214 Billboard hits (plus 739 for song structure) and 11,266 MuseScore scores, shape added between 0.2% and 3% of the explained variation in success, after controls. Only the large samples reach statistical significance, and only because they are large.

So music has a story-arc equivalent, but it is one arc, not a menu of six, and it is a craft norm rather than a success formula.

## The data

| Collection | Pieces | The curve | Success measure | Licence |
|---|---|---|---|---|
| Hymnary.org tune export | 4,986 tunes (the top 5,000 by printings) | the opening line's melodic contour, from scale degrees | Total Instances: published text-tune pairings (median 33) | Hymnary's terms; only derived counts are kept |
| CoCoPops Billboard (McGill Billboard plus melodies) | 214 songs with melody; 739 with harmony and sections | intensity per bar: melodic height and whether the voice is singing, weighted by what listeners felt (below) | chart peak and weeks on the Hot 100, 1958 to 1991 | CC BY-NC 4.0 |
| PDMX (public-domain MuseScore scores) | 11,266 scores (a random 12,000 of 50,121 deduplicated, licence-clean scores of 24 to 400 bars) | intensity per bar: the top line's height, note onsets, notes struck together and loudness (velocity), averaged | views, favourites, star rating (2,047 with three or more ratings) | CC0 / public domain |

The Free Music Archive's play counts were downloaded too. The archive gives only whole-track summaries, though, not curves over time, and its full audio runs to hundreds of gigabytes, so it can't be used for shape. The Sacred Harp use ranks (554 songs, 1995 to 2025) were also downloaded, but no score files could be reached. sacredharpbremen.org is blocked from here.

## The method, and its self-test

Each piece's curve is resampled to relative time, smoothed with a cosine transform (which avoids the false humps a Fourier filter makes), and standardised so that only its shape counts. Two questions are then tested separately. The first is whether the pieces share a shape: the real pieces are compared with the same pieces with their bars shuffled. The second is whether the shapes fall into types: k-means clustering on the real curves is compared with curves drawn from a Gaussian with exactly the real covariance, which gives a continuum with the same modes and no types, and the clusters must also hold up when the data are resampled.

Before any real data was used, the method was checked on synthetic sets (Stage 0):

- A set built from three types was found to have types.
- A continuum was found to have none. A first version of the test wrongly found types here, because standardising curves bends the data. The null models are now drawn before standardising and standardised the same way.
- A set with a common shape had its shared shape detected: the mean curve's strength was 0.60, against 0.08 at the 95th percentile of the null.
- Pure noise showed no shared shape (0.02 against 0.08).

## Results

| | Hymn openings | Billboard | PDMX |
|---|---|---|---|
| Shared shape (mean curve strength, real against null 95th percentile) | 0.107 against 0.020 | 0.412 against 0.090 | 0.192 against 0.025 |
| First mode's share of variation (null 95th) | 43% (22%) | 21% (16%) | 18% (12%) |
| Types beyond a continuum? | no at 2 to 5 groups (less clustered than the continuum); a weak sign at 6 | no | no |
| Where the high point falls in each piece | mean 0.44 of the line (the mean curve peaks at about 0.27) | median 0.74 of the song; 58% in the last third | median 0.64; 47% in the last third |
| Variation explained by controls | 7.3% of log printings | year and length | 45% of log views |
| Added by shape | 0.27% (p = .04) | 3.3% of chart peak (p = .31), 2.5% of weeks (p = .47) | 0.16% of views, 0.21% of favourites (both p < .001); 0.5% of rating (p = .08) |

![The mean shapes](/home/claude/zeneng-pipeline/studies/shapes/mean_shapes.png)

What the shared shape looks like:

- **Billboard:** a quiet start (the intro, before the voice), then waves of verse and chorus, with the highest point at about 0.84 of the song and a fall at the end.
- **PDMX:** a steady rise, highest at about 0.86.
- **Hymn openings:** a climb to the line's high point about a quarter of the way in, then a level line.

The largest single shape term anywhere is small:

- **Hymns:** tunes whose opening lines change direction less often are printed slightly more (β = −0.035, p = .01).
- **PDMX:** the arch-like mode goes with slightly more views (β = −0.023 on a mode that runs against an arch, p = .001).

A second random sample of 12,000 PDMX scores gave the same picture: a shared shape (0.205 against 0.024), no types, a median high point at 0.64, and shape adding 0.19% of views and 0.23% of favourites, with the same arch-like mode the most consistent term (β = −0.026). Rating again showed nothing (p = .51).

Song structure, tested on 739 Billboard songs (610 with a labelled chorus, a median of 44 seconds to the first chorus), showed no single effect. The time to the first chorus, its share of the song and the number of choruses together add 1.4% to weeks on the chart (p = .03) and 0.7% to chart peak (p = .24).

## What listeners felt

A hundred of the Billboard songs carry listeners' moment-by-moment ratings of arousal, along with the audio's loudness. Across 10,195 bars:

- **Time:** the strongest single predictor of felt arousal was how far into the song the bar falls (R² = 0.047). Arousal climbs through a song even where the notes do not.
- **Loudness:** the audio's level came next (R² = 0.033).
- **Notes:** the note measures together reached R² = 0.014. Whether the voice is singing mattered most (β = 0.22), then melodic height (β = 0.10). Busier melody counted slightly against (β = −0.04), and chord changes not at all.
- **All together:** R² = 0.088.

So a curve built from the notes catches only part of what listeners feel. The part it misses (loudness, and the build over time itself) is the part an arranger controls.

## What this means for the engine

1. **Plan one intensity curve for the whole song, and build it.** The high point goes between about 0.65 and 0.85 of the length, followed by a short release. Evidence: this study's three collections and the Chinese pop study (peak at 0.73 to 0.78).
2. **Raise each return above the last.** Felt arousal climbs with time in the song, so a repeated chorus at the same level will feel flatter than the first. This supports the lift rule (749.8) and the energy arc in the songbook protocol.
3. **Put the intensity in what listeners hear.** The voice entering, a higher melody, and loudness and texture all count; harmony changes on their own do not.
4. **Don't offer a menu of shapes.** Songs vary continuously around the shared build, so the engine should score how far a song departs from the build, not which "type" it is.
5. **Weight shape lightly when judging a song.** It explains well under 1% of success in the large samples. It is a craft check, not a hit predictor.
6. **Hymn openings:** let the first line climb to its high point early, and prefer fewer direction changes. Both effects are small.

## Limits

- The Hymnary sample is the top 5,000 tunes, so very rarely printed tunes are missing, which narrows the range of the outcome. Tune age isn't controlled for: only 665 rows give a year.
- The Billboard melody sample is small (214), so it can detect only effects of about r = 0.2 or larger.
- PDMX views mostly reflect the song being arranged, not the arrangement. Song fame was controlled with the number of scores sharing the song's name, but that is a rough measure.
- All the curves come from the notes alone. The listener data show that note-based curves catch only part of felt intensity.
- The hymn result at six groups is a weak sign, not a finding. It needs confirming on a second hymn sample.

## Next

1. Run the same tests on the Sacred Harp use ranks once scores can be reached: allow sacredharpbremen.org, or attach the files. Leaders choose freely what to lead there, so it is the cleanest success measure available.
2. Run Stage 3: have the engine write the same song with different shapes (an early peak, a late peak, a flat arc) and ask listeners which they prefer. That is the field's biggest gap.
3. Port the intensity curve and the late-peak check into the engine (finding 749.17).

All scripts and results are in studies/shapes. Raw data is not included, by licence.

\newpage

# Part 7. Surprise against expectation and YouTube views

## The answer

How predictable a song's melody and chords are relates to its YouTube views about ten times more strongly than its shape does. Songs whose melody and chords follow the common patterns of popular music more closely get more views. The effect holds even when songs are compared only with other songs by the same artist.

Across songs, the note measures add 3.3% to the explained variation in log views. That is on top of the 45.6% already explained by channel size, video age, duration, category and how often the song was transcribed (p < 10⁻¹³⁹). Within artists, the strictest test, they add 0.3% (p < .001). For comparison, shape added 0.16% to 0.21% of PDMX views.

## The data and the measures

- **Songs:** 21,998 Hooktheory clips (melody and chords, transcribed by users, via Sheet Sage) from 13,198 YouTube videos. The YouTube Data API returned views for 10,855 of them and channel sizes for 6,130 channels. After dropping videos without a public subscriber count, 10,847 songs remain.
- **Surprise model:** an IDyOM-style model written for this project. It uses variable-order chains of up to three earlier events, trained on the other songs in five folds by video, so a song never predicts itself. For each note and chord it gives:
  - **surprise:** information content in bits, how unexpected the event was;
  - **uncertainty:** entropy, how open the moment was before the event.

  The melody averages 3.1 bits of surprise and 2.7 of uncertainty; the chords average 4.1 and 3.3.
- **The Cheung term:** high when surprises come in predictable moments and plain events in open ones. Cheung et al. found listeners took most pleasure from exactly that combination, in 80,000 Billboard chords.

## Results

| Measure (standardised) | Across songs: β | p | Within artist: β | p |
|---|---|---|---|---|
| Melody surprise | −0.137 | < .001 | −0.054 | .010 |
| Melody uncertainty | −0.063 | < .001 | +0.001 | .94 |
| Melody Cheung term | +0.023 | .005 | +0.025 | .06 |
| Chord surprise | −0.072 | < .001 | −0.059 | .001 |
| Chord uncertainty | +0.016 | .27 | +0.002 | .93 |
| Chord Cheung term | +0.007 | .44 | +0.024 | .08 |
| Melody repetition within the clip | −0.027 | .02 | −0.007 | .67 |
| Chord repetition within the clip | +0.047 | < .001 | +0.005 | .75 |
| Melody surprise squared (inverted U) | +0.015 | .002 | +0.004 | .56 |

Across songs, n = 10,847 (standard errors clustered by artist). Within artist, n = 7,687 songs by 1,469 artists with at least two songs.

Two things hold up in both models:

1. **Less surprising melodies and chords go with more views.** Of all the measures, chord surprise is the most stable within artists.
2. **Surprise placed in predictable moments helps a little.** The Cheung term points the same way in both models, though within artists it falls just short of the usual threshold (p = .06 and .08). The inverted-U term for melody surprise is positive across songs. So the penalty for surprise eases at the low end, but there is no sign of a "too predictable" penalty.

## Cautions

- **Views measure exposure.** The controls (channel size, age, transcription count) and the within-artist comparison remove much of fame's effect, but not all of it.
- **The model learned from the same songs it judges.** Its expectations are those of these popular songs, so a very popular idiom can read as "expected" partly because it is common in the corpus. The folds stop a song predicting itself, but not its imitators.
- **Clips are sections, not whole songs.** The transcriptions are user-made, and the counts can't be redistributed under YouTube's terms. Only scripts and results are kept.

## What this means for the engine

1. **Keep the melody and chords near the common patterns of popular music.** In the judge, reward low average surprise against a large corpus of popular songs. This is the strongest note-level effect found anywhere in our research.
2. **Spend surprise only in predictable moments.** A fresh chord or an unexpected note works after a clear, settled pattern, not inside an open, uncertain passage. This agrees with Cheung et al., though our own evidence for it is modest.
3. **Don't chase novelty for its own sake.** Nothing here rewards a high-surprise melody.
4. **Keep effects in proportion.** Even the strongest measure explains a few percent of views. The notes matter, but fame and exposure matter far more.


## Our songs against the corpus

The same model, trained on all 21,998 clips, scored six songs whose records are on disk. The percentile is each song's place among the Hooktheory clips: a lower percentile means less surprising, which is the direction that went with more views.

| Song | Melody surprise | Percentile | Chord surprise | Percentile | Chords reduced to triads: percentile |
|---|---|---|---|---|---|
| Nothing Important | 3.11 bits | 62nd | 2.53 bits | 21st | 28th |
| Blue Movie | 3.21 bits | 67th | 1.76 bits | 5th | 7th |
| Keeping Time | 2.94 bits | 53rd | 2.15 bits | 13th | 16th |
| Before It's Done | 2.88 bits | 50th | 2.73 bits | 27th | 38th |
| The Room Next Door (song 52, third edition) | 2.98 bits | 55th | 6.48 bits | 90th | 62nd |
| Sung to Sleep (song 53) | 2.74 bits | 41st | 2.47 bits | 20th | 20th |

The Hooktheory medians are 2.89 bits for melody and 3.79 bits for chords. Reduced to triads, the chord median on held-out clips is 3.06 bits.

- **Chords:** the engine's chords sit well inside the conventional, more-viewed side. Song 52 looked unusual mainly because it writes out colour chords (add9, maj7, ninths) that Hooktheory transcribers usually simplify. Reduced to plain triads, it falls from the 90th to the 62nd percentile.
- **Melodies:** every song sits near the middle of the corpus (41st to 67th percentile). The melodies are where the engine has room to move toward the more-viewed side.
- **Sung to Sleep:** its tune and chords are already more predictable than most popular songs. That fits a carol, though the reference here is pop, not hymns. By this measure, the plainness Jason noticed is not a weakness in the notes. What still looks simple is the texture and arrangement.

## Next

- Score these songs with the UMCS scorer and see whether it ranks the more-watched songs higher.
- Run the model on the engine's own songs to see where they sit against the popular corpus.

Scripts: studies/surprise in the repository.

\newpage

# Part 8. Moments people love

## The answer

When listeners single out a moment, the music is most often doing one thing: the voice comes back in after a breath, on a less expected note. Two beats before the timestamped moment the melody thins out. On the moment itself, a melody note begins after a gap and is more surprising than the song's other notes. A high note, by itself, is not what people mark. The emotional comments, the ones that mention crying, chills or the voice, fall in the second half of the song.

## The data

- **Comments:** the 100 most relevant comments on each of 4,000 videos, a random draw of the Hooktheory videos with 200,000 views or more. From them, 17,642 timestamps were kept, each reduced at once to the video, the time and keyword flags (chills, cry, best part, this part, voice, key change, bridge, drop, chorus). No names and no comment text were stored.
- **Moments:** after merging timestamps within two seconds of each other and dropping lists of times, 8,960 moments remain in 2,840 videos.
- **Matched to the music:** 1,546 of the moments fall inside a Hooktheory clip, which is timed beat by beat to its video. Each was compared with every other four-beat window in the same clip, so each song acts as its own control. The scores are in standard deviations of that clip.

## Where in the song

- **Spread:** moments spread across the song. Their median is at 0.48 of the video's length, and they thin after 0.8, when many listeners have stopped watching.
- **Emotional comments come later:**
  - cry: median at 0.60
  - voice: 0.60
  - chills: 0.55
  - best part: 0.51
- **"Chorus" comes earliest,** at 0.36, presumably the first chorus.

## What the music does

At the moment itself (the four beats from the timestamp), against the rest of the same clip, with 95% intervals:

| Measure | At the moment | Two beats before |
|---|---|---|
| Voice entering after a gap of two beats or more | +0.16 (0.10 to 0.23) | +0.06 (0.01 to 0.13) |
| Melody surprise (the most surprising note) | +0.17 (0.09 to 0.25) | +0.12 (0.05 to 0.20) |
| Uncertainty when that note arrives | +0.21 (0.14 to 0.29) | +0.12 (0.04 to 0.19) |
| Melody notes (how busy) | −0.02 (−0.09 to 0.06) | −0.20 (−0.27 to −0.13) |
| Chord surprise | +0.08 (−0.01 to 0.17) | +0.03 |
| A chord change | +0.06 (−0.02 to 0.13) | −0.06 |
| Height of the highest note | +0.04 (−0.04 to 0.12) | +0.02 |

The pattern is a thinning just before (fewer notes two beats earlier), then the voice returning on a fresh note.

One result goes against expectation. The surprising note arrives when the moment is more open, not less (uncertainty +0.21). The Cheung pattern of surprise in a predictable moment does not appear at this scale. A phrase that starts after a breath is naturally an open moment, and that is where people mark.

## How this fits the other studies

| Study | What wins |
|---|---|
| Surprise and views | More predictable melodies and chords, across a whole song |
| Moments people love | A single fresh note at the point the voice returns |
| Shapes of songs | The build to a late high point; listeners' arousal climbing through the song |

Together: a familiar song, with a few chosen moments of freshness placed where a phrase begins after a breath, and the most emotional of them in the second half.

## What this means for the engine

1. **Give the best moments a breath first.** Thin the melody for a beat or two (a rest, a held note, fewer notes), then bring the voice back in.
2. **Spend surprise on the re-entry.** Choose a less expected note at that point (a leap, an unexpected scale degree), and keep the surrounding notes conventional.
3. **Put the most emotional moments in the second half.** Around 0.55 to 0.6 of the song for the felt moments; the build's peak comes later (finding 749.17).
4. **Don't rely on a high note alone.** Height by itself did not mark the moments people chose.

## Cautions

- **Who comments, and where:** people who comment with timestamps are not all listeners. Timestamps can also point a little before or after the moment, which the lag check covers only in part.
- **Coverage:** the clips are user transcriptions of sections. Only moments inside them, 1,546 of 8,960, could be matched to the notes.
- **Size of the effects:** a sixth of a standard deviation is modest. These are tendencies, not rules.
- **Terms:** comment text and raw statistics are not kept, under YouTube's terms. Only the derived results are.

Scripts: studies/moments in the repository.

\newpage

# Part 9. The rhythm layer

## The answer

Rhythm matters as much as pitch, and it follows the same rule: familiar rhythms overall, a fresh one at the moment that counts.

- **Views:** adding rhythm to the model brings the note measures to 4.8% of the explained variation in log views across 10,828 songs, beyond the controls. Rhythm's own share is 1.5%. Among songs by the same artist, the strictest test, the rhythm block adds 0.38% (p < .001), more than melody and chords together added on their own (0.30%).
- **Familiar rhythms:** less surprising rhythms go with more views, both across songs and within artists.
- **Note density and pickups:** busier melodies (more notes a beat) do better, and so do phrases that start before the downbeat, with a pickup.
- **Syncopation:** a moderate amount is best across songs. Within artists, more syncopation goes with fewer views.
- **Loved moments:** at the moments listeners timestamp, the rhythm is at its most surprising (+0.21 SD), right where the voice re-enters after a breath.

## The rhythm layer

Each melody note becomes a rhythm token: its position in the bar on a sixteenth grid, its length class, and whether a rest of half a beat or more came before it. The surprise model (orders 0 to 3, trained by folds so a song never predicts itself) gives each note's rhythm surprise and uncertainty. Across 22,800 clips the means are 2.7 and 2.2 bits.

Descriptors, with their Hooktheory medians:

- **Syncopation per note** (a note held across a stronger beat): median 0.29.
- **Share of beats with no melody:** median 0.12.
- **Rests of a beat or more:** per bar.
- **Phrase length:** spans between rests of a beat or more, median 15.5 beats.
- **Phrases starting on the downbeat:** median 0.5.
- **Notes a beat:** median 1.08.
- **Variety of note lengths:** median 1.52 bits.

## Against views

All standardised, with the pitch and chord measures and the controls in the same model:

| Measure | Across songs: β | p | Within artist: β | p |
|---|---|---|---|---|
| Rhythm surprise | −0.085 | .002 | −0.055 | .03 |
| Rhythm uncertainty | +0.011 | .49 | +0.066 | .003 |
| Syncopation per note | −0.021 (squared −0.013, p = .02) | .27 | −0.049 | .009 |
| Share of beats with no melody | +0.049 | < .001 | +0.031 | .14 |
| Phrase length | −0.049 | < .001 | +0.048 | .02 |
| Phrases starting on the downbeat | −0.041 | < .001 | −0.026 | .06 |
| Notes a beat | +0.053 | .003 | +0.049 | .03 |
| Variety of note lengths | +0.071 | < .001 | +0.008 | .73 |
| Melody surprise | −0.107 | < .001 | −0.048 | .02 |
| Chord surprise | −0.065 | < .001 | −0.057 | .002 |

Across songs n = 10,828; within artist n = 7,671 songs by 1,466 artists.

Holding in both models: familiar rhythms, denser melodies, pickups into phrases, and not too much syncopation. Phrase length flips sign between the two models, so it supports no conclusion. Rests help across songs but not clearly within artists.

## At the moments people love

Against the rest of the same clip, rhythm surprise rises two beats before the timestamp (+0.16, 95% CI 0.07 to 0.24) and peaks at it (+0.21, 0.13 to 0.30), falling away after. This fits the earlier finding of a breath and then the voice's re-entry. Part of it is built in, though: a note after a rest is itself a less common rhythm token.

## Our songs

| Song | Rhythm surprise | Syncopation | Rests | Phrase (beats) | Notes a beat |
|---|---|---|---|---|---|
| Nothing Important | 85th percentile | 39th | 92nd | 4.9 (8th) | 48th |
| Blue Movie | 64th | 35th | 84th | 6.1 (14th) | 44th |
| Keeping Time | 57th | 27th | 88th | 6.0 (14th) | 41st |
| Before It's Done | 51st | 28th | 80th | 6.9 (19th) | 68th |
| The Room Next Door (song 52) | 76th | 28th | 50th | no breaks of a beat | 84th |
| Sung to Sleep, verse (song 53) | 26th | 0 | 26th | no breaks of a beat | 12th |
| Sung to Sleep, refrain | 44th | 0 | 0 | no breaks of a beat | 15th |

- **The engine's pop songs:** their rhythms are more surprising than most popular songs, and their phrases are short and broken by many rests. Both run against the more-viewed direction. Their syncopation is moderate.
- **Song 52:** busy (84th percentile density), with fairly surprising rhythms.
- **Sung to Sleep:** plain, sparse and unsyncopated, as a hymn tune is, with no breath of a beat or more anywhere. That last point matters for the "breath, then re-entry" rule.

## What this means for the engine

1. **Keep rhythms familiar.** Score rhythm surprise against the corpus and aim at or below the median. Luthier's pop songs run above it.
2. **Use pickups.** Start most phrases before the downbeat.
3. **Keep syncopation moderate.** Some is good; a lot works against a song.
4. **Don't starve the melody.** Very sparse lines do worse; aim near or above about one note a beat in pop styles.
5. **Spend rhythmic surprise at the best moments,** with the breath before them (749.19). In hymns that means a real breath at chosen line ends, which Sung to Sleep never has.

## Cautions

As before: views measure exposure as well as music, and the clips are user transcriptions of sections. Note offsets in Hooktheory may be drawn legato, which would make rests shorter than sung. Song 52's 6/8 was read on a grid of three quarters. The effects are small.

Scripts: studies/rhythm in the repository.

\newpage

# Part 10. Psychoacoustics for the songwriting engine (research report)

## Build the ear in, learn the surprise

Psychoacoustics can give Luthier most of what makes music sound clear, gripping and easy to follow, and it can do so from the notes alone, without a corpus. Five things can be computed directly from pitches, durations and tempo. The first is roughness and "mud" in every voicing, because critical-band physics makes the same interval rougher the lower it sits. The second is whether the sung melody is masked or upstaged: high-voice superiority appears even in 7-month-old infants and follows from cochlear mechanics. The third is whether lines hold together or split into separate streams (van Noorden's tempo-dependent boundaries and Huron's ten voice-leading principles). The fourth is the window in which a beat can be felt, roughly 100 ms to 2 s with a sweet spot of 450–750 ms. The fifth is the memory ceiling of about 8 s on a phrase. The same science identifies the physical levers behind chills: crescendo, the entry of a new or returning voice, register expansion, added roughness, and a long build of anticipation. What psychoacoustics cannot supply is the pleasure of surprise, or the pleasantness of consonance itself. Listeners with little exposure to Western music dislike roughness but show no preference for consonant intervals ([MIT News on McDermott et al. 2016](https://news.mit.edu/2016/music-tastes-cultural-not-hardwired-brain-0713)). Expectancy is a learned statistic, and the project's own strongest note-level predictors of views (melody, chord and rhythm surprise) are all measured against a corpus. The practical result is a division of labour. Hard constraints and the arousal plan move onto psychoacoustic computation. Corpus use shrinks to one job: an expectancy model that keeps the surface familiar and decides where a few surprises go. Corpora matter less than they might seem, because roughness alone explains **20–50% of how often composers use each chord type** across classical, jazz and pop corpora ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). Two gaps remain open. No study measures how song accompaniment masks a sung melody, and no study shows that deliberately engineered chill cues produce more chills. Every numeric threshold below that is marked "design" is an engineering choice, not a finding.

### Roughness is computable, register-dependent and nearly universal

#### Every roughness model shares one recipe, and register comes free

Every interference model works the same way. Each note is expanded into an assumed harmonic spectrum. For every pair of partials belonging to different notes, the model takes a weight from their amplitudes and a dissonance value from a curve that peaks at a fixed fraction of the critical band, then sums the results. Plomp and Levelt placed the roughest beating "close to one quarter of the critical bandwidth" ([Moore](https://www.mooremusic.org.uk/schenk/aco3.htm)), and Greenwood's later estimate is 30–40% ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)). Critical bandwidth is "almost constant below about 200 Hz" and becomes a roughly constant fraction of frequency above about 500 Hz. In musical terms, **the most dissonant interval is about 1.5 semitones at middle C, "roughly doubling for each octave downwards"** ([Moore](https://www.mooremusic.org.uk/schenk/aco3.htm)). Harrison and Pearce put it in modelling language: "a given frequency ratio occupies less critical-band distance as absolute frequency decreases," so one interval can be consonant high and dissonant low ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). An engine that converts MIDI numbers to hertz before scoring therefore gets register-sensitivity automatically.

The Sethares (1993) parameterisation is small enough to port in a few lines, and its constants are verified in a widely copied implementation. Set Dstar = 0.24, S1 = 0.0207, S2 = 18.96, C1 = 5, C2 = −5, A1 = −3.51 and A2 = −5.75. For each pair of partials with lower frequency Fmin and difference Fdif, compute s = Dstar/(S1·Fmin + S2). The pair's roughness is a·(C1·e^(A1·s·Fdif) + C2·e^(A2·s·Fdif)), and the current version takes the amplitude weight a as the smaller of the two amplitudes ([endolith gist](https://gist.github.com/endolith/3066664)). The research team ran this model, and the C4 result (1.4 semitones at peak roughness) matches Moore's 1.5, which cross-checks the code. The same runs show how fast the danger zone widens downward. With pure tones, roughness falls below 10% of its peak at about 6.3 semitones above C4, 9.9 above C3 and 15.5 above C2. With six-harmonic complex tones, **a major third on G2 scores rougher (4.04) than a minor second on C5 (3.20)**. A close C-major triad scores 14.2 at C2, 7.9 at C3 and 4.3 at C4, while the open voicing C2–G2–E3 scores 8.8, about as smooth as the close triad an octave higher. These are model outputs from the team's computation, not listener data, but they reproduce what arrangers already know.

#### Low-interval limits are physics, but the published tables are folklore

The arranger's "low interval limit" (no close thirds below about C3, fifths allowed lower, octaves lowest) follows directly from the critical-band mechanism. Practitioners themselves call such limits "NOT definitive rules but a good guide to avoid muddyness," and note that mud depends on dynamics and on how many upper harmonics the instrument has: "soft low voicings on for instance strings are more forgiving than loud ones on brass" ([Robin Hoffmann](https://www.robin-hoffmann.com/dfsb/low-interval-limits)). No peer-reviewed study was found that fits per-interval low-register thresholds to listener ratings. The team derived limits from the six-harmonic model instead, asking for each interval how low its lower note can go before the dyad becomes rougher than a minor third on C4. The answers were roughly B♭2 for the fifth, A1 for the octave, B♭3 for the major third, C4 for the minor third and C♯3 for the major sixth, and the minor second never qualified anywhere on the piano. These limits are about an octave more conservative for thirds than the commonly quoted jazz-arranging tables, which were not verified this session. The reference chord is arbitrary, and the model overweights minor sixths and major sevenths. **The ranking is trustworthy; the absolute thresholds are not.** This argues for computing roughness per voicing rather than hard-coding a table, and for calibrating the warning level against voicings the engine already trusts (see the first check below).

Two practical corrections follow from the mechanism, although neither has been tested on listeners. Organ registration changes the spectrum. Mixtures, mutations and reeds add strong upper partials, which raises roughness, and a 16′ pedal sounds an octave below the written note, which pushes a written third below the comfort limit. Limits must therefore be applied at sounding pitch and tightened for bright registrations. Duration matters too. The validation datasets used short piano chords, and no study models duration ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). Sustained organ and choir chords plausibly expose roughness more than decaying piano chords, so a duration-and-sustain weight is a sensible design choice, but it is untested.

#### Harmonicity and familiarity are mostly learned, which is why they are not voicing checks

The rival account says consonance comes from harmonicity: how closely the chord's pooled spectrum resembles a single harmonic series. McDermott, Lehr and Oxenham found that individual consonance ratings tracked harmonicity preference strongly, while beating measures were "weak and inconsistent." Harmonicity preference, but not aversion to beating, rose with years of musical training ([McDermott et al. 2010](https://mcdermottlab.mit.edu/papers/McDermott_Lehr_Oxenham_2010_consonance_individual_differences.pdf)). The cross-cultural evidence splits the two cleanly. More than 100 Tsimane listeners in the Bolivian Amazon showed an "undetectable" preference for consonance yet "the same dislike for… acoustic roughness" as other groups, and US listeners, especially musicians, showed the largest consonance preference ([MIT News](https://news.mit.edu/2016/music-tastes-cultural-not-hardwired-brain-0713)). Amusic listeners likewise show normal roughness aversion but no harmonicity preference, and a binary rule that asks only whether a chord fits a major scale "functions like a harmonicity model" ([Lahdelma, Eerola & Armitage 2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.802385/pdf)). The reasonable synthesis is that **roughness aversion is built into hearing, while the pleasure of consonant intervals is learned**.

Harrison and Pearce reanalysed four behavioural datasets (more than 500 participants) and three corpora (more than 100,000 compositions). They conclude that consonance is a composite of interference, harmonicity and cultural familiarity ([Cambridge summary](https://cms.mus.cam.ac.uk/publications/harrison-pearce-simultaneous-consonance/)). On the largest chord-rating dataset, Hutchinson and Knopoff roughness alone reached partial **r = .77**, harmonicity and corpus familiarity .72 each, and the composite **r = .88**. Popular audio "roughness" implementations did far worse (r ≈ .17–.57). In the corpora, interference was "consistently the most important predictor" of chord-type frequency ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). The published composite weights are interference −1.620, harmonicity +1.780 and culture −0.089, with the number-of-notes term set to zero for new data. They must be ported with incon's own feature scaling, not applied to raw outputs. Lahdelma and Eerola add a useful split between two kinds of rating. Perceived tension tracked consonance stably across familiarity levels (−.72 to −.95), but pleasantness moved with familiarity. Roughness predicted tension (+.527), while harmonicity became negligible once roughness and familiarity were controlled ([Lahdelma & Eerola 2020](https://durham-repository.worktribe.com/OutputFile/1265040)).

For the engine, the consequence is architectural. Harmonicity and culture models are largely pitch-class based, so they rank chord *types* and do not change when a chord is revoiced. Roughness is the term that changes with voicing and register. **The voicing judge should be roughness; the harmony chooser can add harmonicity and familiarity.** Roughness is also a tension dial, not only a fault. "Increased roughness" is one of the reported chill elicitors ([de Fleurian & Pearce 2021](https://rcastoragev2.blob.core.windows.net/0695c63ed1e5b482bf323b2bf1d15ab4/PMC8323431.pdf)), and tension tracks roughness. The rule should therefore be to keep the low register clear always, and to treat roughness higher up (suspensions, added-tone clusters, appoggiaturas) as a budgeted tension resource that resolves.

The tooling is ready. The R package incon takes MIDI pitches such as `c(60, 64, 67)` and uses Hutchinson and Knopoff as its default model among 16 or more ([incon README](https://rdrr.io/github/pmcharrison/incon/f/README.md)). The Python package `dissonant` (MIT licence, alpha, last released in 2018) implements the Sethares and Vassilakis models from partial frequencies and amplitudes ([PyPI](https://pypi.org/project/dissonant/)). The benchmark spectrum is 11 harmonics with 1/n amplitude ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). The caveat is validation range. The chord datasets are almost all piano or synthetic tones around F3–F4, so **the register effect is predicted by every model but not directly validated by listener data**, and choir vowels and organ registrations have not been tested at all.

### The sung line survives on top, alone in its band, moving by step

#### Streaming depends on pitch distance against rate

Two successive tones stay in one stream when the pitch distance between them is small relative to their rate. Below the fission boundary, about 1–2 semitones and almost independent of tempo, a line always coheres. Above the temporal coherence boundary it always splits, and that boundary rises from **about 4 semitones at 50 ms per tone to about 13 semitones at 150 ms** ([Deutsch, ch. 6](https://deutsch.ucsd.edu/pdf/PsyMus_3_Ch6_Grouping_Mechanisms.pdf)). Between the two boundaries, attention and build-up decide, and streaming keeps building for 10 to 60 seconds. Timing can override pitch: pauses as short as 30 ms often outweighed pitch jumps as large as 11 semitones. In about 4,600 folk songs, the mean melodic interval was 2.0 semitones within phrases and 2.9 across phrase boundaries (same source). Huron adds that a line's continuity degrades when gaps exceed about 800 ms. In a 13,178-note sample, 85% of notes were shorter than 500 ms, the median vocal note lasted 0.38 s, and vocal rests typically ran 1–2 s ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)).

Simultaneous notes fuse when their onsets are synchronous, when they move in parallel, and when their timbre and location match. Delaying the lower of two tones improves its detectability by about **10 dB per 10 ms of delay**, and real ensembles spread their onsets by 30–50 ms ([Deutsch, ch. 6](https://deutsch.ucsd.edu/pdf/PsyMus_3_Ch6_Grouping_Mechanisms.pdf)). Huron's onset-synchrony principle asks for 100 ms or more between the onsets of parts meant to be distinct. His co-modulation principle says parallel motion fuses most when it is exact in log frequency, so chromatic parallels fuse more than diatonic ones ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)).

#### Huron derives the voice-leading rules from ten perceptual principles

Huron's "Tone and Voice" (read in full this session) derives the traditional rules from six core principles and four auxiliary, style-optional ones. Each maps onto something an engine can compute.

| Principle | What it says | Rules it generates |
|---|---|---|
| P1 Toneness | Clearest pitch for harmonic complex tones between **F2 and G5** (about 80–800 Hz), best near 300 Hz | Keep melodic streams inside F2–G5 |
| P2 Temporal continuity | Gaps no longer than about 800 ms | Sustained tones; avoid mid-phrase holes in lines meant to be continuous |
| P3 Minimum masking | Roughly equal spectral energy in each critical band | Wider spacing as register descends; tessitura-sensitive spacing |
| P4 Tonal fusion | Fusion strongest for unisons, then octaves, then fifths | Avoid these intervals in proportion to the independence wanted |
| P5 Pitch proximity | Fission boundary about 2 semitones or less for tones under 700 ms | Conjunct motion, common tones, no crossing, no overlap |
| P6 Pitch co-modulation | Correlated motion fuses, most when exactly parallel | No parallel or exposed perfect intervals between independent parts |
| P7 Onset synchrony (aux.) | Distinct parts separated by 100 ms or more | Asynchronous approach to perfect intervals in polyphony |
| P8 Limited density (aux.) | **Three or fewer** concurrent parts if they are to be told apart | At most about three independent lines; extra parts fuse as pads |
| P9 Timbral differentiation (aux.) | Distinct timbres aid independence | Optional; choirs and keyboards forgo it for blend |
| P10 Source location (aux.) | Spatial separation aids streaming | A mixing note, not a score rule |

Source: [Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf).

The corpus evidence behind these principles is unusually strong for music theory. More than 10,000 four-note sonorities from Haydn quartets and Bach keyboard works show adjacent-voice intervals widening as register descends. Bach's use of harmonic intervals in the Sinfonias correlates with sensory dissonance at −0.85 and with tonal fusion at −0.82 (R² = 0.88 together): **Bach avoids fused intervals, not only rough ones**. Expert listeners' accuracy at tracking voices drops sharply between three and four voices. Across 143 works, onset synchrony was the strongest of six factors separating homophony from polyphony ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)). In Bach's Inventions, perfect consonances arrive asynchronously more often than synchronously (1,059 against 599), while imperfect consonances tend to arrive together ([Huron 2008](https://core.ac.uk/download/159579115.pdf)).

The paper's most useful lesson for a song engine is that **styles are subsets of the principles**. Homophony obeys most rules but ignores onset asynchrony, probably for text intelligibility (shared syllable onsets) and rhythmic uniformity. Barbershop deliberately keeps co-modulation and synchrony because it wants fusion. Luthier should therefore switch rule sets by intended texture: blended backing voices and hymn SATB on one setting, an independent countermelody or organ descant on another. Applying chorale rules everywhere would be wrong. This matches the texture-switching rule proposed in the earlier accompaniment research, which Huron's full text now confirms.

#### The top voice wins for reasons that start in the cochlea

In two-voice textures the higher voice is encoded more robustly, in musicians and non-musicians, with loudness matched at about 85 phons, and in **7-month-old infants**, whose mismatch responses were larger and earlier for the upper voice. An auditory-nerve model attributes the effect to middle-ear filtering and two-tone suppression. The bias is stronger in lower registers and peaks at about **24–30 semitones (2–2.5 octaves)** of separation, which matches typical soprano–bass spacing in Bach chorales. The authors call that link to compositional practice "speculative" ([Trainor et al. 2014](https://trainorlab.mcmaster.ca/publications/pdfs/High%20voice%20superiority%20effect%20Hearing%20Research%202014.pdf)). Experience reduces the effect without reversing it: bass-range players show a smaller one. The low voice has the opposite advantage for timing. Hove and colleagues reported lower-voice superiority for rhythm encoding, but only the paper's existence was verified this session, not its numbers ([PMC4104866](https://pmc.ncbi.nlm.nih.gov/articles/PMC4104866)). The design consequences are direct. Keep the sung melody as the highest sounding pitched line during vocal passages. Treat any accompaniment note sustained above it as a salience conflict, and treat a harmony voice or descant above the lead as a deliberate transfer of salience, not an accident. Put countermelodies below the melody or in its rests, and give the groove-defining onsets to the bass.

#### Masking is about bandwidth, and the score can only approximate it

Auditory filter width is ERB = 24.7·(4.37f + 1) Hz, with f in kHz ([Glasberg & Moore via ERB reference](https://static.hlt.bme.hu/semantics/external/pages/mel/en.wikipedia.org/wiki/Equivalent_rectangular_bandwidth.html)). Converted to musical distance, one ERB above a sung note spans about **4.5 semitones at C3, 3.5 at A3, 3.2 at C4, 2.6 at A4 and 2.3 at G5** (team computation from the formula). An accompaniment note within that distance of the voice's fundamental competes for the same filter, and the zone is widest exactly where male voices and keyboard left hands overlap. Classical singers escape orchestral masking through the singer's formant near 3 kHz, where orchestral energy, which peaks near 500 Hz, is low ([Timbre and Orchestration](https://timbreandorchestration.org/tor/timbre-lingo/2019/12/10/the-singers-formant)). Pop singers lack that formant but show a peak near 3.5 kHz. Loud pop accompaniment has a spectral slope between 0.5 and 2.5 kHz like that of a Wagner orchestra ([Borch & Sundberg 2002](https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_pubmed_primary_12375627)).

The notes alone cannot see formants, brightness, level or EQ, so a score-level masking check is a proxy. It is still worth building, because the three things the score does control are the ones the principles above name: register proximity to the voice, sustained density in the voice's octave, and onset coincidence with the voice's syllables. **No peer-reviewed study was found that measures lyric intelligibility or melodic salience against accompaniment register and density in songs.** That is the biggest evidence gap in this report, so the masking check's thresholds are all design values. The engine should pass what it cannot see into the songbook as mixing notes, for example "keep 2–4 kHz clear on guitars in the verses."

Voice-separation software offers a validator but not a judge. Separation is a mature task in music information retrieval: earlier perceptual and statistical models report F-measures of about 81–94 on Bach inventions and fugues, and a 2024 graph neural network reaches voice F1 96.6 on J-pop piano scores with public code ([arXiv 2011.03028](https://arxiv.org/html/2011.03028v1); [Karystinaios et al. 2024](https://arxiv.org/html/2407.21030v1)). Luthier already labels its voices, so it does not need separation. If an off-the-shelf separator merges the countermelody into the lead, or splits the lead into two, that is a useful streaming warning. No symbolic-input masking or salience estimator exists anywhere, and the repository licences could not be verified.

### Pulse lives between 100 ms and 2 s, and phrases live under 8 s

#### Every metre must put one level in the 450–750 ms window

The auditory limit for synchronising to a beat is about 8–10 Hz, which is an inter-onset interval of **100–125 ms**. The lower limit is about **1.8 s** "regardless of modality" ([Repp 2006](https://doaj.org/article/dc3f29b3977e4adf8dfe9aa998eb40de)). Preferred tempo is about 100–133 bpm. DJ and tapping corpora peak at 125 bpm, and head motion over a whole day peaks near 2 Hz ([Dahl et al. 2014](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)). London places maximal pulse salience at 500–750 ms and defines the tactus as a level near 500–1500 ms. Subdivisions must exceed 100 ms to keep their identity, and a 300 ms interval is "too fast to be heard as the beat." Metronome marks index the dotted quarter in compound metres ([London 2011](https://cdn.carleton.edu/uploads/sites/721/2021/12/London-2011-Tactus-vs-Tempo.pdf)). London's account of metre also explains why triple and compound metres are harder to get right. A metre needs at least one level of subdivision or grouping inside the perceptual limits, and "comfortable" ternary options are relatively scarce ([summary of London 2004](https://www.midside.com/pdf/eastman/fall06/th581/london_longuet_temperley.pdf)).

These limits translate into a metre table the engine can enforce at the form stage. Beat lengths and subdivisions below are computed from the tempo; the choice of beat level for each metre is an inference from the limits, because no study directly compared felt beat levels in 6/8 and 3/4 at matched tempi.

| Metre | Felt beat | Tempo for a 450–750 ms beat | Subdivision lengths | Failure modes |
|---|---|---|---|---|
| 4/4 | quarter | 80–133 | eighths 375–226 ms; sixteenths 188–113 ms | Continuous sixteenths above about 130 bpm hit the 100–125 ms floor |
| 3/4 | quarter | 80–133 | eighths 375–226 ms | Above about 200 bpm the bar becomes the beat (a waltz "in one") |
| 6/8 | dotted quarter | 80–133 | eighths 250–150 ms; sixteenths 125–75 ms | Sixteenths are unsafe above about dotted quarter 100; below about 60 the eighths become the beat and it turns into a slow "six" |
| 12/8 | dotted quarter | 60–100 (slow gospel and blues) | eighths 333–200 ms | Beat at 1 s is near the slow edge, so the eighths must carry motion |
| 5/8, 7/8 | uneven 2+3 or 2+2+3 groups | eighth at least 100 ms | — | Western listeners need very clear grouping (cross-cultural evidence not verified) |

For sung melody the floor should sit a little above the tapping limit, at about 125–150 ms per syllable (design), because syllables need more time than taps. That makes 6/8 sixteenth-note runs a specific hazard for the engine's current 6/8 work.

#### Groove follows an inverted U, and the project's data agree only partly

The urge to move and the pleasure taken both follow an inverted U against syncopation. In 66 listeners rating 50 drum breaks at 120 bpm, **medium syncopation** scored highest, dancers rated higher than non-dancers, and musical training mattered only marginally ([Witek et al. 2014](https://www.scienceopen.com/document_file/d9d000f1-421f-4984-8e28-d5dc02f2762e/PubMedCentral/d9d000f1-421f-4984-8e28-d5dc02f2762e.pdf)). With 201 online participants and piano patterns at 96 bpm, medium rhythms (son and rumba clave) again won. **Medium-complexity chords (four-note extended chords) strengthened the rhythmic inverted U for pleasure, and flat-ninth chords weakened it** ([Matthews et al. 2019](https://core.ac.uk/download/185514684.pdf)). Both studies kept an isochronous hi-hat. The usual explanation, that "structural resistance" to the pulse invites the body to fill in the metre, requires a pulse to resist, so syncopated melody needs at least one layer on the beat. Both studies also used 4/4. Their extension to 3/4 and 6/8 is extrapolation, and the ternary caution above argues for less syncopation in triple and compound metres.

The project's rhythm study partly agrees. Across 10,828 Hooktheory songs, a moderate amount of syncopation went with the most views (squared term β = −0.013, p = .02), but **within artists more syncopation went with fewer views** (β = −0.049, p = .009). Less surprising rhythms went with more views in both models, as did denser melodies and phrases that start with a pickup ([rhythm study](../studies/rhythm/rhythm_study_report.md)). Read together, the lab and corpus evidence say syncopation is a seasoning with a low optimum for sung pop melody. The groove studies measured drum and piano patterns, not vocal lines, which helps explain why their peak sits higher. Luthier's pop songs already sit at the 27th–39th percentile for syncopation, so they need no change there. Their rhythm surprise is a different matter. They sit at the 51st–85th percentile, above the corpus median, and only a corpus model can measure or fix that.

#### Phrases are bounded by working memory, and repetition is a lever

Snyder's account, known here only through a review, puts working memory at about **8 s**. A phrase, the largest unit grasped as a whole, has "an upper limit of around 8 seconds" and holds about 7±2 groupings. Anything larger is understood by comparing parts more than 8 s apart. The reviewer adds that grouping size is "only loosely related" to these memory limits ([Chaffin 2002 review of Snyder](https://musiclab.uconn.edu/wp-content/uploads/sites/290/2019/03/Chaffin-2002-Review-of-B.-Snyder.pdf)). The popular "3-second present" should not be hard-coded. A 2017 review found no boundary at 3 s and described integration as an envelope that "extends well beyond the three-second mark" ([White 2017](https://orca.cardiff.ac.uk/98445/1/Peter%20White%20three-second%20moment%20paper%203.pdf)). Phrase limits must be stated in seconds, not bars. At 120 bpm a four-bar 4/4 phrase lasts 8 s and sits at the limit. At 80 bpm it lasts 12 s and should be heard as 2 + 2, with closure in the middle. A four-bar 6/8 phrase at dotted quarter 80 lasts 6 s and is fine.

The project's corpus suggests real songs fill this window rather than staying far under it. The median Hooktheory phrase, measured between rests of a beat or more, is 15.5 beats, about 7.75 s at a typical 120 bpm. Luthier's pop phrases run 4.9–6.9 beats (8th–19th percentile), broken by many rests ([rhythm study](../studies/rhythm/rhythm_study_report.md)). The memory limit is a ceiling the engine is nowhere near, and the project data cannot yet say whether longer phrases would help, because the phrase-length coefficient flips sign between the across-song and within-artist models.

Repetition is the strongest pro-liking lever the memory literature offers, and it works without a corpus. Huron estimates that more than **90%** of listening time is spent on material heard before. In Margulis's lab, Berio and Carter excerpts with repetition re-inserted were rated more enjoyable and more likely to be human-composed, random sequences looped six times were later judged more musical, and **exact** refrains drew more tapping and singing along than varied ones ([Margulis, Aeon](https://aeon.co/essays/why-repetition-can-turn-almost-anything-into-music)). Only her summaries were available, without sample sizes. On the Billboard Hot 100, each extra chorus repetition raised the odds of reaching No. 1 by 14.5% (read through a secondary source; [Pacific Standard on Nunes et al.](https://psmag.com/?p=30843)). Earworms share a common global contour with a few unusual intervals, and a three-predictor model classified them at only 62.5%. The older finding that earworms have longer notes and smaller intervals did not replicate ([Jakubowski et al. 2017](https://durham-repository.worktribe.com/OutputFile/1371487)). In the project's own data, chord repetition within a clip went with more views across songs (β = +0.047, p < .001) but not within artists, and melodic repetition showed nothing consistent ([surprise study](../studies/surprise/surprise_study_report.md)). Repetition is the one source of familiarity the engine can generate from inside the song, and the short-term half of any expectancy model is built from exactly that.

### Chills need arousal the ear supplies and surprise the culture supplies

#### Four of Juslin's eight mechanisms live in the score

Juslin's BRECVEMA framework lists eight routes from sound to felt emotion: brainstem reflex, rhythmic entrainment, evaluative conditioning, emotional contagion, visual imagery, episodic memory, musical expectancy and aesthetic judgement ([Juslin 2013 record](https://ui.adsabs.harvard.edu/abs/2013PhLRv..10..235J)). Four can be written directly into notes and arrangement: brainstem reflex (sudden loudness, accents, roughness, very low or high sounds, silences), entrainment (tempo, pulse clarity, groove), contagion (voice-like expressive cues) and expectancy. Aesthetic judgement is partly designable through craft. Conditioning and episodic memory belong to the listener's history. The empirical basis for contagion is a meta-analysis of **104 speech studies and 41 music studies** that found "similar changes in acoustic features" convey the same emotions in both domains ([Quinto et al. 2013](https://www.frontiersin.org/articles/10.3389/fpsyg.2013.00184/full)). Three of the designable mechanisms (brainstem reflex, entrainment and contagion) run on psychoacoustic cues. Only expectancy depends on learned statistics.

#### Chills cluster at increases and arrivals after a long build

The classic studies agree on chill triggers more than on anything else. They report "new or unprepared harmony, and changes in texture and dynamics" (Sloboda), crescendos (Panksepp), "the entrance of new voices or instruments" with rising loudness and sharpness (Grewe et al.), and solo–accompaniment interplay with expanded frequency range (Guhn et al.) ([Bannister & Eerola 2018](https://www.frontiersin.org/article/10.3389/fpsyg.2018.02046/full)). A systematic corpus study summarised the elicitors as "sudden dynamic changes, increased roughness, crescendi, and the entry of new instruments." It also noted that the behavioural studies used only 3 to 23 stimuli each. Across 722 chill tracks matched to controls by artist, duration and popularity, the chill tracks were slightly sadder, slower, quieter and more acoustic, but the effects were tiny (valence difference 0.033 on a 0–1 scale), because chills are local events that whole-track averages smooth away ([de Fleurian & Pearce 2021](https://rcastoragev2.blob.core.windows.net/0695c63ed1e5b482bf323b2bf1d15ab4/PMC8323431.pdf)).

The physiology shows why the build matters as much as the peak. In PET and fMRI, pleasurable music released dopamine in the striatum. **The caudate was active during the 15 s of anticipation before a chill, and the nucleus accumbens peaked at the chill itself**. Pleasure during the anticipation window averaged 2.51, against 2.11 for the whole excerpt ([Salimpoor et al. 2011](https://www.zlab.mcgill.ca/publications/docs/salimpoor_2011_nn.pdf)). The only manipulation test cut the chill section from three pieces. Chill reports fell from 30 to 21, only marginally significant (p = .049, φ = 0.23), and skin conductance did not change. Listeners found chills elsewhere once the "trigger" was gone ([Bannister & Eerola 2018](https://www.frontiersin.org/article/10.3389/fpsyg.2018.02046/full)). Chills are probabilistic, depend on context and vary between people. Design can raise their likelihood but cannot guarantee them.

Tears appear to follow a different recipe. The widely cited Sloboda result links tears and a lump in the throat to **melodic appoggiaturas and melodic sequences** ([Sloboda 1991](https://doi.org/10.1177/0305735691192002)), but his tables were not re-read this session. The idea that tears carry a calmer, "release" physiology than chills rests on a paper that could not be fetched, so this report treats the tear recipe as plausible but unverified: slow tempo, soft dynamics, falling sequences, and appoggiaturas on stressed words over an exposed voice.

#### What is built in and what still needs a corpus

The cleanest way to answer the brief's central question is to sort each lever by whether hearing supplies it or culture does.

| Lever | Built in or learned | Key evidence | Needs a corpus? |
|---|---|---|---|
| Roughness and mud | Built in | Tsimane and amusic listeners keep roughness aversion | No |
| Pleasantness of consonant intervals | Mostly learned | Tsimane show none; grows with training | Only for the familiarity term |
| Top-voice salience | Built in | Present in 7-month-olds; cochlear model | No |
| Critical-band masking | Built in (physics) | ERB; Huron P3 | No |
| Streaming by proximity and rate | Built in (tested on Western listeners) | van Noorden; Huron | No |
| Beat window and about 2 Hz preference | Built in (motor) | Repp; body resonance | No |
| Comfort with uneven metres | Partly learned | Cross-cultural work not verified | Style knowledge |
| Groove inverted U | General mechanism; the optimum depends on style and dance experience | Witek; Matthews | Partly |
| Tempo, loudness, pitch height as arousal and emotion cues | Largely shared across cultures | Mafa listeners decoded happy, sad and scared above chance using the same cues as Westerners ([BPS on Fritz et al. 2009](https://www.bps.org.uk/research-digest/emotions-music-are-universally-recognised)) | No |
| Major/minor as happy/sad | Learned | Enculturated | Rules suffice for a Western audience |
| Melodic, harmonic and rhythmic surprise | Learned statistics | IDyOM; Cheung; the project's studies | **Yes** |
| Liking from repetition | General (mere exposure, speech-to-song) | Margulis | No; the song supplies it |
| Voice entry as an event | Built in (contagion) | Grewe; Guhn | No |
| Build-then-arrival schema | Partly learned | Listeners report a linear-ramp schema in EDM ([Bilious & Dahl 2026](https://zenodo.org/records/24023747)) | Partly |

The split matches what generative systems find. An emotion-conditioned symbolic generator controlled **arousal** significantly better than its baselines, but showed "no statistical significance" on **valence**, and the low-valence, low-arousal target was hit only 25% of the time ([Ferreira et al. 2022](https://arxiv.org/pdf/2208.05162)). Arousal runs on built-in cues and is easy to steer. Valence runs on learned cues such as mode, harmony and lyric meaning, so explicit rules may beat learned conditioning there.

#### The project's own studies refine the textbook recipe in three places

The moments study supports the arrival account in its broad lines but corrects it in detail. Two beats before a timestamped moment, the melody thins (note count −0.20 SD). At the moment, the voice enters after a gap of two beats or more (+0.16) on its most surprising note (+0.17), the rhythm is also at its most surprising (+0.21), and a high note on its own did nothing (+0.04, interval spanning zero) ([moments study](../studies/moments/moments_study_report.md); [rhythm study](../studies/rhythm/rhythm_study_report.md)). In psychoacoustic terms, three built-in mechanisms meet in one gesture. A textural contrast feeds the brainstem reflex, a returning human voice drives contagion, and a fresh note drives expectancy. The breath also does perceptual work. At typical tempi two beats last about one second, longer than Huron's roughly 800 ms continuity limit, so the voice's return is heard as a new onset that re-captures attention rather than as a continuation. That reading is an inference. It implies that accompaniment fills in the gap should stay out of the vocal register just before the re-entry, so the voice is re-identified against a clear band.

The first correction concerns the Cheung pattern. Cheung et al. found that surprising chords pleased most in predictable contexts ([Cambridge summary](https://cms.mus.cam.ac.uk/publications/cheung-uncertainty-surprise/)), and the project's surprise study found a weak positive Cheung term across whole songs (melody β = +0.023, p = .005; within artists p = .06) ([surprise study](../studies/surprise/surprise_study_report.md)). At loved moments, however, uncertainty was *higher* than elsewhere (+0.21). The two findings work on different time-scales. A phrase onset after a breath is inherently open at the next-note level, while the listener's section-level expectation (the voice will return) is highly predictable. The design rule that fits both is to make the bars before the re-entry predictable through repetition and stable harmony, then spend the surprise on the re-entry note itself. This is where the corpus is indispensable: "surprising" means low probability under a style model.

The second correction concerns timing. Emotional comments sit earlier than the intensity peak. "Chills" comments had a median position of 0.55, "cry" and "voice" 0.60, and "bridge" and "key change" about 0.56–0.59, although those last two had few cases ([moments study](../studies/moments/moments_study_report.md)). The shared build in the shapes study peaks later, with a median high point at 0.74 of a Billboard song and the mean curve highest near 0.84 ([shapes study](../studies/shapes/shapes_study_report.md)). Chinese pop arousal peaks at 0.78 ([Lyu 2026](https://arxiv.org/abs/2609.15675)). Salimpoor's two stages suggest a reading: the poignant turn (bridge, breakdown re-entry or key lift) is a distinct event from the loudest arrival, and the anticipation between them is itself rewarding. The engine should plan both, with the felt re-entry near 0.50–0.65 and the intensity peak near 0.70–0.85.

The third correction concerns what the notes can carry. In the shapes study's listener data, time in the song was the strongest predictor of felt arousal (R² = 0.047), audio loudness came next (0.033), and all note measures together reached only 0.014. Within those note measures, **whether the voice was singing mattered most (β = 0.22)**, ahead of melodic height (0.10), while chord changes did not matter at all ([shapes study](../studies/shapes/shapes_study_report.md)). Listener-validated tension models agree that dynamics and pitch height dominate and that harmony adds little ([Farbood 2012](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/f/11865/files/2020/08/Farbood_2012_Musical_Tension.pdf); [Barchet et al. 2024](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0296385)). These are precisely the built-in cues. Because remembered intensity follows the average moment more than the peak, and correlates with liking at r = .63 ([Schäfer et al. 2014](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00911/full)), the arousal plan should keep the average up and should not rely on one climactic chord.

### Three checks to build first

All three checks run on what the engine already produces: labelled voices with MIDI pitch, onset, duration and instrument, plus tempo and metre. None needs a corpus, except the optional calibration step in the first check, which uses voicings already on disk only to set a warning level, not to learn a style.

#### Check 1: roughness and harmonicity of every voicing, with register-aware low-interval limits

The unit is a vertical slice: every new onset, and every change in the set of sounding pitches. Pitches should be converted to sounding pitch before scoring. For organ, add the octave below for 16′ stops, the octave above for 4′, and extra partials for mixtures and reeds. Each note expands to 11 harmonics with 1/n amplitudes, the incon benchmark ([Harrison & Pearce 2020](https://core.ac.uk/download/228298307.pdf)). Bright organ registrations and loud brass get a slower roll-off (design). Roughness sums over all cross-note partial pairs. The first build can use the Sethares formula, whose constants are verified; Hutchinson and Knopoff, the better-validated model (r = .77), can follow once a port is checked against incon output on a reference set of chords.

The check raises three flags. A **hard mud flag** fires when any adjacent pair of voices sits below its register limit for a note lasting a beat or more. The limit is the lowest lower note at which that interval's dyad roughness stays under a reference level. A **slice warning** fires when total roughness exceeds the 95th percentile of the roughness of Open Hymnal and Bach chorale voicings whose bass is in the same register and that have the same number of notes (design calibration, since both corpora are on disk). An **alternative-voicing search** keeps the chord and the voice-leading constraints fixed, tries the available inversions and spacings, and prefers the least rough. The roughness penalty is weighted by duration, at min(1, duration in beats), and by sustain: organ and choir 1.0, decaying piano about 0.6 (design). Harmonicity, using the Harrison and Pearce 2018 model, is a separate score attached to the chord *type* and passed to the harmony chooser rather than the voicer. One exception is budgeted. Upper-register roughness above about C4 at the planned peak, or on an appoggiatura that resolves, is logged as intended tension rather than flagged, because roughness is one of the chill elicitors. Low-register roughness is never exempt.

#### Check 2: masking of the sung melody by the accompaniment

For each melody note, with fundamental f, onset and duration, the check gathers every accompaniment note that overlaps it in time and scores five conditions.

| Condition | Computation | Flag level |
|---|---|---|
| Top-voice conflict | Any accompaniment pitch above f while the voice sings; severity rises with overlap and with closeness (same or adjacent octave) | Hard if sustained for at least the melody note's duration; logged, not flagged, for a designated harmony voice or descant |
| Critical-band proximity | Accompaniment fundamentals within 1 ERB(f) of f (about 3.5 semitones at A3, 2.6 at A4), or within 1 ERB of 2f or 3f | Penalty weighted by overlap time and by onset coincidence |
| Vocal-octave crowding | Number of sustained accompaniment pitches inside the phrase's sung range, or within ±6 semitones of the melody, per beat | Warning above 2 (design); aim for a pocket about an octave wide around the voice |
| Onset coincidence | Busy accompaniment onsets in the vocal register that fall on syllable onsets | Penalty for independent layers; allowed for blended backing voices and hymn homophony |
| Outer-voice frame | Melody-to-bass distance | Mild reward for 24–30 semitones; mild penalty under 12 |

The first two rows rest on high-voice superiority and the ERB formula ([Trainor et al. 2014](https://trainorlab.mcmaster.ca/publications/pdfs/High%20voice%20superiority%20effect%20Hearing%20Research%202014.pdf); [ERB reference](https://static.hlt.bme.hu/semantics/external/pages/mel/en.wikipedia.org/wiki/Equivalent_rectangular_bandwidth.html)). The fourth rests on Rasch's onset-unmasking result ([Deutsch, ch. 6](https://deutsch.ucsd.edu/pdf/PsyMus_3_Ch6_Grouping_Mechanisms.pdf)), and the last on the "speculative" chorale link. Two further rules connect this check to the moments finding. In the one or two beats before a planned vocal re-entry, accompaniment fills should move out of the vocal octave. Fills in vocal rests are rewarded elsewhere, which matches the earlier accompaniment research's complementarity target of 50–73% for piano-accompanied song. The check's output also includes mixing notes for what the score cannot see: the 2–4 kHz band, brightness and level.

#### Check 3: voice separation and streaming

Within each line, every pair of consecutive notes is tested against a coherence boundary interpolated from about 4 semitones at 50 ms per tone to about 13 semitones at 150 ms ([Deutsch, ch. 6](https://deutsch.ucsd.edu/pdf/PsyMus_3_Ch6_Grouping_Mechanisms.pdf)). A leap above the boundary is a split risk. That is welcome only in deliberate compound melody. For inter-onset intervals above 150 ms, where the boundary was not measured, a soft leap penalty grows with interval size and shrinks as the leap's notes lengthen, following Huron's leap-lengthening rule. Rests longer than about 800 ms inside a line meant to be continuous are flagged; phrase-end breaths are exempt and are in fact wanted before the planned moments. Melodic streams must stay within F2–G5 ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)).

Between lines, the check enforces Huron's rules according to a texture tag on each layer. Layers tagged **independent** (countermelody, descant, organ solo line) get no crossing, no overlap, no parallel or exposed unisons, octaves or fifths with the melody, fused intervals approached asynchronously, and onsets offset from the melody by at least one notated subdivision (100 ms or more). Layers tagged **blend** (backing voices, hymn SATB, pads) may share onsets and move in similar motion, but they keep the no-crossing rule against the melody so that the top voice keeps its salience. Across the whole texture, the engine counts the independently moving lines and warns above three ([Huron 2001](https://www.musanim.com/articles/Huron.ToneAndVoice.2001.pdf)). Lead plus countermelody plus bass is the canonical ceiling. Optional validation runs an off-the-shelf voice separator on the rendered score and flags any case where it fails to recover the engine's intended lines.

### Ranked rules and checks the engine can compute from notes

Grades follow the earlier reports. **A**: replicated across labs or populations, including cross-cultural, infant or physiological evidence. **B**: a controlled study or validated model with a solid primary source. **C**: a corpus regularity, a secondary summary, or the project's own correlational studies. **D**: practitioner consensus, theory or a design inference. "Design" marks a threshold the engine chooses, not a finding. "Corpus" marks rules that still need a style model.

| Rank | Rule or check | What the engine computes from notes | Grade | Corpus? |
|---|---|---|---|---|
| 1 | **Check 1: roughness of every voicing, register-aware** | Sethares or Hutchinson–Knopoff roughness per slice at sounding pitch, 11 harmonics at 1/n; hard mud flag below each interval's model-derived limit; warning above the 95th percentile of hymnal voicings with the same bass register; least-rough voicing preferred | A for the mechanism (critical band; universal roughness aversion); B for the model (r = .77); D for thresholds | Calibration only |
| 2 | **Check 2: melody masking and top-voice salience** | Accompaniment above the melody; partials within 1 ERB of f, 2f or 3f; at most 2 sustained pitches in the vocal octave per beat; onset coincidence for independent layers; melody-to-bass frame of 24–30 semitones | A for top-voice superiority; B for ERB; D for every threshold (no song-masking study exists) | No |
| 3 | **Check 3: streaming and voice separation** | Interval against IOI coherence boundary (4 semitones at 50 ms to 13 at 150 ms); gaps over 800 ms; range F2–G5; texture-tagged Huron rules; at most 3 independent lines | B (van Noorden; Huron's corpus and experiments) | No |
| 4 | **Tactus window by metre** | Felt beat at 450–750 ms: 4/4 and 3/4 quarter 80–133; 6/8 dotted quarter 80–133; 12/8 dotted quarter 60–100; warn when 3/4 exceeds about 200 bpm or 6/8 falls below dotted quarter 60 | B (Repp; London; Moelants via Dahl) for limits; D for metre mapping | No |
| 5 | **Fastest-note floor** | No articulated value under 100–125 ms; sung syllables at least 125–150 ms (design); bans 6/8 sixteenth runs above about dotted quarter 100 | B for the floor; D for the vocal margin | No |
| 6 | **Intensity plan from built-in cues** | Per-bar composite of voice present, melody height, onsets per beat, sounding voices or registration; keep the average high; peak at 0.70–0.85; each repeated section a step higher | B (Farbood; TenseMusic; Schäfer); C for peak position (project shapes study; Lyu) | No |
| 7 | **Breath, then re-entry, for planned moments** | Melody thins 1–2 beats (at least about 800 ms); accompaniment leaves the vocal octave; voice re-enters on a lower-probability note and rhythm; preceding bars repetitive | C (project moments and rhythm studies; Grewe and Guhn via secondary summary) | Yes, to define "lower-probability" |
| 8 | **Stacked arrival at the peak** | At the planned peak, at least three of: crescendo or texture step, new or returning voice, upward register expansion, upper-register roughness, one unprepared but style-licensed chord; at least 15 s of build before it | B for anticipation (Salimpoor); C for triggers (systematic corpus, classic studies) | Partly (the chord) |
| 9 | **Separate the poignant turn from the loudest arrival** | Emotional re-entry or turn near 0.50–0.65; intensity peak near 0.70–0.85 | C (project moments and shapes studies) | No |
| 10 | **Familiar surface, surprise spent sparingly** | Mean melody, chord and rhythm information content at or below the corpus median; surprise allowed mainly at planned moments after repetitive context | B (Cheung); C (project: β of −0.107, −0.065 and −0.085 across songs, all holding within artists) | **Yes** |
| 11 | **Moderate syncopation with an on-beat frame** | Syncopation per note near the corpus median or a little under; at least one layer on the beat whenever melody syncopates; lower targets in 3/4 and 6/8 | B (Witek; Matthews); C (project: within-artist penalty); D for triple metres | Norms by style |
| 12 | **Harmony–rhythm complexity budget** | High syncopation is not combined with flat-ninth or cluster colour; four-note extended chords paired with medium syncopation | B (Matthews 2019) | No |
| 13 | **Phrase ceiling in seconds** | Phrase between breaths at most about 8 s, motives about 1–3 s; at slow tempi split four-bar phrases 2 + 2; never hard-code 3 s | C (Snyder through a review; White 2017) | No |
| 14 | **Exact hook repetition** | Hook or refrain repeated exactly 3–4 or more times; variety moved into verses and accompaniment; motive restated 2–4 times within a phrase | C (Margulis summaries; Nunes secondary; project chord repetition) | No |
| 15 | **Roughness as a budgeted tension dial** | Upper-register roughness allowed on suspensions and appoggiaturas that resolve and at the planned peak; low register always clear | B (tension tracks roughness: Lahdelma & Eerola); C (chill elicitor) | No |
| 16 | **Bass carries the groove** | Syncopated and groove-defining onsets placed in the bass; the melody's syncopation kept moderate | C (Hove et al., existence only) | No |
| 17 | **Harmonicity and familiarity choose chord types, not voicings** | Harrison–Pearce harmonicity plus a familiarity term in the harmony chooser, with composite weights ported using incon's scaling | B (composite r = .88) | Familiarity term |
| 18 | **Sounding-pitch and registration corrections for organ** | 16′ and 4′ octave shifts and mixture partials applied before Check 1; limits tightened for reeds and mixtures | D (model mechanics; Hoffmann) | No |
| 19 | **Tear template** | Slow tempo, soft dynamics, descending sequence, appoggiaturas on stressed words resolving onto the weak syllable, exposed voice and sparse accompaniment | D (Sloboda not re-read; physiology unverified) | No |
| 20 | **Valence by explicit rule** | Mode, harmonic colour and lyric meaning chosen by rule for the target emotion; arousal set by tempo, loudness, register and density | B for the arousal-versus-valence asymmetry (Ferreira 2022); C for universality of arousal cues (Fritz via summary) | Mode is learned, but rules suffice |
| 21 | **Anti-rules** | No register-blind consonance tables for voicing; no "high note equals climax" (project: +0.04, interval spanning zero); no universal claim for consonance preference; no 3-second constant; no countermelody above the sung line unless the transfer of salience is intended | A to C as cited above | No |

Rules 1 to 5 are hard constraints that keep the music from sounding muddy, masked or garbled to any listener. Rules 6 to 9 form the arousal plan, which runs on built-in cues. Rule 10 is where the corpus still earns its place, and the project's evidence says it is the single largest note-level effect on views.

### Conclusion

The brief asked how Luthier can move people with less reliance on corpora. The answer is not "replace the corpus with psychoacoustics" but **rearrange the work so the corpus does only the one job hearing cannot do**. Every check above that keeps music clear, physically engaging and well formed is computable from first principles and holds across listeners. That covers roughness, masking, streaming, tempo windows, memory ceilings and the arousal plan. What remains learned is narrow but decisive: which notes, chords and rhythms count as expected, and therefore where a surprise can land. The project's own studies sharpen this split. The note-level effects on views are all expectancy effects. The loved moments combine a built-in event (a voice returning after a breath) with a learned one (a less probable note). A high note on its own does nothing. For Luthier, this means a small style model for expectancy, fed by its own repetitions as the short-term half, while everything else moves into deterministic checks that need no data to stay correct.

The second implication concerns where research effort should go next. Psychoacoustics is mature on chords and lines in isolation but silent on the sung melody inside a song texture. No study measures masking of a vocal line by keyboard or organ accompaniment, none validates register effects on rated roughness, and none tests whether engineered chill cues raise chill rates. Luthier is unusually well placed to start closing that gap without a listener panel, in two ways. Once the three checks exist, they can be run on scores that already carry outcomes: PDMX's multi-part scores have views and ratings, and its melody and accompaniment parts can be separated. That would test whether masking and roughness scores relate to anything listeners do, at the same scale as the shapes study. The engine can also generate matched versions of one song that differ only in vocal-octave crowding, roughness budget or the timing of the re-entry. That is the controlled manipulation the literature lacks, ready for whenever any listener data becomes available. The three checks are worth building first because they prevent faults, and also because they turn both the corpus and the engine's own output into tests of the questions the field has left open.

\newpage

# Part 11. What musicians re-record (covers study)

## The answer

Musicians and audiences reward different things in a song's notes. How often a song is covered goes with its YouTube views only weakly (r = 0.15). Beyond views and the other controls, the notes explain 4.0% of how often a song is covered (p = .008), more than they explain of views in the same songs (1.7%).

Three measures predict being covered. None of them predicts views, and syncopation points the opposite way for audiences:

1. **Chords that move.** Songs whose chord progressions repeat less within a section are covered more (β = −0.124, p = .003). Musicians re-record songs that have harmony to work with, not a loop.
2. **Chord surprises in settled moments.** The Cheung term for chords, high when the unexpected chord arrives after a predictable stretch, predicts covers (β = +0.076, p = .03). Across 10,847 songs it never predicted views.
3. **Some syncopation.** More syncopation goes with more covers (β = +0.087, p = .02). Among songs by the same artist it went with fewer views.

All three hold, a little stronger, among the 705 songs performed by their original artist: the notes add 4.7% (p = .004); chord repetition β = −0.126, Cheung term +0.076, syncopation +0.112.


## Replication on Discogs-VI (three times the songs)

The larger SecondHandSongs release (LargeSHS) is not yet downloadable: the GitHub address its paper gives does not exist. A second, independent source is. Discogs-VI (Araz, Serra & Bogdanov, ISMIR 2024; CC BY-SA 4.0, on Zenodo) found 348,796 groups of versions in Discogs' editorial metadata from shared writers and titles. Covers here are the distinct performing artists in a song's group, minus one. The data give each song's earliest release year, so song age can be controlled.

3,080 Hooktheory songs matched, 2,360 with note measures, views and a first year (median 6 covers; 2% have none). With the release year in the controls, covers and views are unrelated (r = 0.00), so they are two separate channels.

| Measure | Covers (SHS100K, 780) | Covers (Discogs-VI, 2,360) | Views (same 2,360) |
|---|---|---|---|
| Chord repetition within a section | −0.124 (p = .003) | −0.071 (p < .001) | −0.003 (p = .88) |
| Chord surprise in settled moments (Cheung) | +0.076 (p = .03) | +0.009 (p = .54) | +0.020 (p = .21) |
| Syncopation | +0.087 (p = .02) | +0.022 (p = .16) | −0.006 (p = .72) |
| Share of beats without melody (rests) | −0.073 (p = .14) | +0.041 (p = .045) | +0.017 (p = .51) |
| Variety of note lengths | +0.008 (p = .89) | +0.039 (p = .048) | −0.009 (p = .72) |
| Notes a beat | −0.028 (p = .63) | −0.036 (p = .08) | +0.087 (p < .001) |
| Chord surprise | −0.065 (p = .16) | −0.030 (p = .06) | −0.043 (p = .02) |
| Notes add, beyond controls | 4.0% (p = .008) | 1.5% (p < 10⁻⁹) | 1.4% (p < 10⁻⁷) |

What replicates:

- **Chords that move:** songs whose chords repeat less within a section are covered more. This is the one finding that holds in both sources, and it is unrelated to views.
- **Density splits the channels:** denser melodies win views but not covers. Musicians lean the other way, toward rests and varied note lengths.
- **Conventional chord choices:** they help a little on every channel.

What does not replicate: the chord Cheung term and syncopation. They pointed the same way in Discogs-VI but were too weak to count, so they are treated as unconfirmed.

The engine's musician profile is therefore revised to:

- harmony that moves within sections;
- room in the melody (rests, varied note lengths);
- conventional chord choices.

## Why it matters

Luthier's own spec names cover counts twice as the missing yardstick for telling songs that last from songs that merely charted. A cover is a musician choosing a song, so it measures songwriting more than fame, marketing or production. With views now in hand too, the engine can be judged on two separate channels:

| Channel | What it rewards in the notes |
|---|---|
| Audiences (views, 10,847 songs) | predictable melody, chords and rhythm; denser lines; pickups; moderate syncopation |
| Musicians (covers; 780 songs on SHS100K, 2,360 on Discogs-VI) | chords that move rather than loop (both sources); room in the melody, with rests and varied note lengths (Discogs-VI); settled-moment surprises and syncopation unconfirmed |

A song that does well on both is accessible enough to be heard and rich enough to be played. The two channels pull apart on syncopation and on repetition. That points to the engine's balance: keep the melody easy to follow, and give the harmony and rhythm the play that interests players.

## Data and method

- **Covers:** SHS100K (github.com/NovaFrost/SHS100K) is the research release of SecondHandSongs: 9,359 works with the versions sampled for each (median 8; Summertime 387). A Hooktheory song matched a work when its title and an artist among the work's performers agreed. That gave 1,039 matches, 780 with note measures and views.
- **Note measures and controls:** the same as the views and rhythm studies (cross-fitted surprise models). The controls are log views, channel subscribers, video age, duration, category, the number of Hooktheory clips, and whether the Hooktheory artist is the work's first performer. Standard errors are clustered by artist.
- **Limits:**
  - SHS100K lists only sampled works that were covered, so this compares songs covered more with songs covered less, not covered with never covered.
  - Song age is not controlled beyond the video's age, and older songs have had longer to gather covers.
  - Seventeen measures were tested; at the .05 level about one would pass by chance, and three did. The block test (p = .008) and the replication on originals carry more weight than any single term.
  - LargeSHS (218,407 works; arXiv 2511.15270) is not yet published at the address its paper gives, so the replication used Discogs-VI instead (section above).

## What this means for the engine

1. **Judge on two channels.** Score a candidate against both profiles: the audience profile (predictability, denser lines; findings 749.18 and 749.20) and the musician profile (harmonic motion within sections, room in the melody, conventional chord choices). Prefer candidates that do well on both, rather than maximising either.
2. **Don't loop the harmony in every section.** Keep chord repetition within a section below the corpus median, at least in the verse or the bridge.
3. **Give the melody room.** Leave rests and vary note lengths, especially in sections the band will carry, while the hook stays dense enough for the audience profile.
4. **Treat settled-moment chord surprises and syncopation as unconfirmed for players.** They passed on SHS100K but not on Discogs-VI.

Scripts: studies/covers in the repository. The SHS100K metadata is not redistributed.

\newpage

# Part 12. Sung to Sleep (song 53): test report, first to fourth edition

## Intake

| Question | Answer |
|---|---|
| What next | The next song in 3/4, building the chorus, harmony and whole-song changes in from the start (A) |
| The request | "I really want to do another Christmas Carol, this one, with a full score for the organist and a hymn sheet for the choir perfectly aligned. Would this time signature work for that?" (yes: 3/4 suits a carol) |
| The idea | A brainstorm from the theology of the first carol ("the Word that had to learn words"); five sparks offered; the writer chose the Song sung to sleep (Job 38:7): "A. But I don't want it sung as Mary. A narrator like most Carols is fine" |
| Shape | Four verses, a refrain after each, the descant over the last verse and refrain (A) |
| Lyric | Draft 1; "I hate lullay as a word, makes no sense" (the refrain opens "Hush now"); verse 2 rewritten for distinctiveness ("the voice that called the light to be / now cried for Mary there"); the refrain's melody to lift gently and stay warm under repetition; locked at draft 3: "A. And remember, we are learning. I want you to make the adjustments musically we talked about where possible" |
| Key | E♭ major, the last verse up a step to F (A); "Just a full score for the organist and a hymn page for the choir" (no Nashville chart) |
| Tempo | Gently rocking, quarter = 88 (A) |
| Title | Sung to Sleep (A) |
| Refrain melody | "Hush now" low and still; line 3 climbs to the tune's top on "world"; the second "sleeping" a step above the first, home on "here" (A) |
| Last verse | An organ link to F; verse 4 in unison over the organ's own harmony; the final refrain in four parts with the sopranos' descant, the last "here" held (A) |

## Method

The engine draws in 4/4 only (749.4), so the tune was drawn by a 3/4 sketch of its method (gen34.py) with kept tables from the Essen folk-song collection: 1,601 tunes in 3/4 (tables_34.py, with song 52's builder: bar 36 twelfths, beats at 0, 12 and 24). The hymn form sets the rhythm's frame: Common Meter, every stressed syllable on a downbeat, every line opening on a pickup except the refrain's "Hush now" lines; inside it each bar is drawn from the kept 3/4 bars (half and quarter, quarter and half, or a slurred pair, at most one slur a line). Pitches from the kept interval shares, chord tones weighted on downbeats. Written in D and transposed: verses 1-3 and refrains to E♭, verse 4 and the final refrain to F.

The four parts: the carol pipeline's beam search (harmonize53.py; two chords added for the verse-4 organ setting, F♯7 and C in D, sounding A7 and E♭ in F). The descant: song 52's harmony-as-lines search (harm68.high) above the sopranos in their rhythm and words, chord tones of the four-part chord, "world" pinned a third above (A5) inside the search.

Both documents come from one record on one timeline and share one line of time, keys, bar lines, marks and a break every fourth bar, so bars 1-80 fall on the same systems in both (engrave53.py).

## The melody search

3,000 builds, seed 20261115+453; 2739 survivors. Deaths: refrain 2: 184, refrain 3: 77 (the refrain's line 3 climb with D5 once on "world"; line 4's step and its home). The pick: **01be9dada5fb**, charge 0.61, distance 8.9, taken as drawn.

| Reading | The pick | Median survivor | Kept 3/4 (25th, 50th, 75th) |
|---|---|---|---|
| repeated notes | 23% | 32% | 11%, 18%, 26% |
| moves by step | 50% | 43% | 38%, 48%, 60% |
| moves by leap | 8% | 10% | 7%, 11%, 17% |
| turns of direction | 40% | 41% | 33%, 40%, 47% |
| range | 13 | 12.00 | 12.00, 13.00, 14.00 |
| distinct pitches | 8 | 7.00 | 7.00, 8.00, 9.00 |
| longest run of one pitch | 3 | 4.00 | 2.00, 3.00, 4.00 |
| distinct rhythms over bars | 16% | 16% | 35%, 47%, 67% |
| notes a bar | 1.97 | 1.90 | 2.84, 3.48, 4.00 (set by the hymn form; not charged) |
| onsets on the beat | 100% | 100% | 57%, 67%, 82% (set by the hymn form; not charged) |
| onsets on the bar's first beat | 46% | 47% | 23%, 26%, 33% (set by the hymn form; not charged) |
| gaps of a sixteenth | 0% | 0% | 0%, 0%, 9% (set by the hymn form; not charged) |
| gaps of an eighth | 0% | 0% | 25%, 48%, 64% (set by the hymn form; not charged) |
| gaps of a quarter or more | 100% | 100% | 24%, 39%, 70% (set by the hymn form; not charged) |

Distinct rhythms over bars sits under the kept range (16% against 35%): every survivor's does, since the hymn frame allows only three bar rhythms (finding 749.11).

## The harmony (749.9)

Each part against the tune, at each pair of the tune's onsets, by section:

| Part | Moves with the tune | Against it | Holds while it moves (or the reverse) | Parallel fifths or octaves | Distinct distances |
|---|---|---|---|---|---|
| verse A | 17% | 22% | 61% | 0 | 8 |
| verse T | 9% | 41% | 50% | 0 | 10 |
| verse B | 21% | 33% | 46% | 0 | 12 |
| refrain A | 21% | 33% | 46% | 0 | 9 |
| refrain T | 18% | 50% | 32% | 0 | 9 |
| refrain B | 8% | 58% | 33% | 0 | 14 |
| refrain_final A | 26% | 26% | 48% | 0 | 7 |
| refrain_final T | 17% | 43% | 39% | 0 | 10 |
| refrain_final B | 21% | 42% | 38% | 0 | 10 |
| refrain_final Desc | 26% | 35% | 39% | 0 | 6 |
| verse4 organ alto (org_rh_a) | 26% | 22% | 52% | 0 | 9 |
| verse4 organ tenor (org_lh) | 22% | 43% | 35% | 0 | 12 |
| verse4 pedal | 21% | 33% | 46% | 0 | 14 |

Song 52's shadow harmony moved with the lead 74% to 85% of the time and never against it; here no part moves with the tune more than 26% of the time, and the tenor and bass move against it 33% to 58% of the time.

## Variety and shape (749.8, 749.10)

- Verses 1-3 and their refrains share one setting (a hymn's form). Verse 4 changes three things: the key (F), the texture (the choir in unison, the men an octave lower) and the harmony (the organ's own chords: F♯ minor, E minor 7, B minor 7, A7, G, E minor 7, C, A7 ... in D, a different chord on 25 of its 31 notes).
- The final refrain: four parts again, a fresh setting in F, and the descant above.
- The shape: average sounding pitch of the tune, verses 1-3 A♭4, refrains 1-3 G4, verse 4 C5, final refrain B4 (each a step above its first); the tune's top, F5, in bar 71 of 80 (88% of the way in), with the descant's A5 on the same beat. The tune's E♭5 sounds once in the first section, on the refrains' "world".

## The organ part, rewritten after delivery

The writer: "The organ music looks incredibly easy. Are you sure that's right?" It was right note for note and too plain for the request: outside a 4-bar introduction, a 2-bar link and verse 4's own chords, the organ played the choir's four parts (soprano and alto in the right hand, the tenor alone in the left, the bass in the pedal), the way an organist plays from a hymnal, and verse 4 and the introduction were in the same four-part texture. He chose A: build through the carol.

| | First version | Now |
|---|---|---|
| Introduction | 4 bars: the refrain's last line in four parts | 8 bars: the refrain's first line, then its last, the tune with one voice under it in the right hand, the left hand rocking in eighths (root, fifth, third inside a fifth), a held pedal |
| Verses 1-3 and refrains | the four choir parts doubled | a fuller form of them: a third note in the right hand on 41 of 57 chords, a filled chord in the left hand, common tones held |
| Link | 2 bars, G minor 7 to C7 | 4 bars, E♭, G minor 7, C7sus4, C7, the rocking figure going on |
| Verse 4 | the organ's own chords, in four plain parts with the tune on top | its own accompaniment: chords held below the tune (never doubling it), a suspension at a chord change, the rocking left hand, the pedal on the new bass line |
| Final refrain | the choir's four parts doubled | held chords with the tune on top, the rocking left hand in every bar, a tonic pedal under "Hush now" (bars 61-64) and a dominant pedal under "is sleeping, sleeping" (bars 73-74) |
| Coda | none | 4 bars: the refrain's last phrase once more over a tonic pedal, IV to I, the last chord held |
| Left hand in eighths | 0 | 263 notes |
| Length | 70 bars | 80 bars |

Against the tune, verse 4's organ right hand moves with it 43% of the time and holds 48%; the final refrain's pedal moves with the tune 9% of the time and holds 65%; no parallels.

## Documents

- Full score for the organist (PDF, 7 pages, 80 bars): descant (final refrain only), the choir on two staves with every verse between them, the organ's manuals and pedal (see the organ part below).
- Hymn page for the choir (PDF, 4 pages): the same bars, systems and notes without the organ staves.
- Every voice read back from LilyPond's MIDI note for note (sopranos, altos, tenors, basses, descant, organ right hand, left hand, pedal).
- Consistency: 46/46 checks pass, among them: one shared global line in both documents (80 bars); the same choir notes in both; the keys; the tune's tops and the descant's top on "world"; the descant above the sopranos; the refrain's designs; verse 4 in unison over a different harmony; the organ's introduction and coda alone, its fuller chords in verses 1-3, its right hand below the tune in verse 4, a suspension, the rocking left hand in every bar of the final refrain, the two pedal points; no parallel fifths or octaves in any part; the voices in their ranges; no Nashville chart.

## Second edition: built from the metre atlas

The writer, after the atlas was built: "Any chance once you build the tables, we can return to the recent hymn and finish it using the engine with the table you created?" The engine still draws in 4/4 only (749.4 is not ported), so the second edition is the sketch rebuilt on the atlas's tables; the rerun on the engine stays in the order of work. He chose A: a second edition now, measured before and after.

**What changed.** The tune (gen34h.py, pick 9025fdbc9b1e, seed 20261115+4532, 2740 survivors of 3,000) draws its bars from the Open Hymnal Project's 3/4 hymn bars, with a slurred second note where a hymn bar has more onsets than the frame has syllables (dotted quarter and eighth; two quarters; two eighths on the weak syllable; up to two slurs a line), and is charged against the 3/4 hymn quartiles (46 hymns) on every reading. The quarter-and-half bar was left out: in a strophic hymn it lengthens an unstressed syllable in every verse. The designs stand (Hush now low and still; the climb to D5 on world; the second sleeping a step above the first; here home on D4). The four parts: the beam search weighted toward hymn motion (the alto rewarded for parallel thirds and sixths with the tune; contrary motion rewarded mainly in the bass); the lower voices hold under the tune's slurred notes; passing notes added where a voice moves by a third (eighth pairs in the alto and tenor near the hymn rate; the bass only on longer notes). The organ doubles the passing notes in verses 1 to 3 and the refrains; verse 4, the final refrain and the coda keep their own accompaniment.

**The tune against 3/4 hymn tunes** (quartiles from 46 hymns):

| Reading | First edition | Second edition | Hymns (25th, 50th, 75th) |
|---|---|---|---|
| repeated notes | 23% (outside) | 21% (outside) | 14%, 17%, 21% |
| moves by step | 50% | 54% | 49%, 57%, 62% |
| moves by leap | 8% | 8% | 7%, 9%, 11% |
| range | 13.00 | 13.00 | 12.00, 12.00, 14.00 |
| longest run of one pitch | 3.00 | 3.00 | 2.00, 3.00, 3.00 |
| distinct rhythms over bars | 14% (outside) | 18% | 16%, 22%, 32% |
| notes a bar | 2.18 | 2.21 | 2.12, 2.34, 2.66 |
| onsets on the beat | 100% | 95% | 84%, 94%, 100% |
| gaps of half a beat | 0% | 7% | 0%, 7%, 24% |
| gaps of a beat or more | 100% | 93% | 74%, 92%, 100% |

All 19 readings: first edition 17 inside the hymn quartiles, second 18 (repeated notes 21.3%, a hair over the hymn 75th of 21.26%). Notes a bar rose from 1.97 to 2.21; half-beat gaps from 0% to 7%.

**The four parts against 3/4 hymn settings** (with the tune / against it / holding; notes shorter than the beat):

| Voice | First edition | Second edition | Hymns (medians) | Short notes, first | Short notes, second | Short notes, hymns |
|---|---|---|---|---|---|---|
| Alto | 21% / 27% / 52% | 36% / 12% / 52% | 39% / 13% / 47% | 0% | 9% | 8% |
| Tenor | 15% / 45% / 40% | 23% / 28% / 49% | 35% / 24% / 40% | 0% | 5% | 7% |
| Bass | 17% / 44% / 39% | 16% / 43% / 41% | 26% / 34% / 38% | 0% | 0% | 5% |

The alto now moves almost as hymn altos do; the tenor and bass are closer than before but still move against the tune more, and with it less, than hymn tenors and basses. No parallel fifths or octaves in either edition. A first pass split the unchanged voices around each passing note into repeated eighths (21% short notes in every voice); fixed.

**Documents.** Organ full score and hymn page, second edition (80 bars, the same layout); every voice read back from MIDI; consistency 46/46.


## Third edition: the organ part by section role

The second edition's organ was measured against a new table, the piano parts of the 326 art songs in 3/4 in OpenScore Lieder (CC0, tables/metre_atlas/accompaniment_lieder.json), and the research round "Accompaniment corpora and music theory" was run first, at the writer's request. Its first rule, from organ practice, is that each section gets a role: the inner verses stay in the hymnal harmony and change colour, while the introduction, the passages between verses and the last verse carry the free, fuller writing. The third edition's organ follows that plan. The choir's parts and the descant are unchanged (a check).

| Section | Role in the third edition |
|---|---|
| Introduction, bars 1-8 | the tune in the right hand over an inner line that moves when the tune holds; the rocking left hand; the last bar over B-flat |
| Verses 1-3, bars 9-24 | hymnal harmony in the right hand; the left hand a broken chord in quarters, the tenor's note on every downbeat; colour changed by registration verse by verse |
| Refrain, bars 25-40 | the tune on top, an inner line moving in quarters under its held notes, the rocking left hand |
| Link, bars 41-44 | broken eighths in the right hand, held chords in the left, the pedal stepping down E-flat, D, C |
| Verse 4, bars 45-60 | free harmony around the unison tune: four-note chords that change on every beat, suspensions at changes, the pedal written first and stepping into each new bass, quarters in the left hand |
| Final refrain, bars 61-76 | the tune on top, the inner line in eighths under held notes, the rocking left hand, the tonic and dominant pedals |

Before and after, against the Lieder 3/4 middle half (right hand 1.13-1.95 onsets a beat; left hand 0.88-1.51; complementarity, the share of accompaniment onsets where the tune has none, 0.50-0.73). The organ's left hand is read with its pedal, since a pianist's left hand carries the bass.

| Section | Right hand a beat | Left hand and pedal a beat | Complementarity | Commonest texture |
|---|---|---|---|---|
| introduction | 0.62 → 0.96 | 1.96 → 1.96 | 0.98 → 0.98 | mixed → mixed |
| verses 1-3 | 0.67 → 0.67 | 0.48 → 0.83 | 0.18 → 0.39 | sustained → block |
| refrain | 0.56 → 0.79 | 0.48 → 1.96 | 0.13 → 0.67 | sustained → broken |
| link | 0.42 → 1.92 | 1.92 → 0.42 | 0.96 → 0.96 | mixed → broken |
| verse 4 | 0.44 → 0.79 | 1.96 → 1.0 | 0.68 → 0.42 | broken → block |
| final refrain | 0.38 → 1.1 | 1.98 → 1.98 | 0.68 → 0.68 | broken → broken |
| coda | 0.5 → 0.5 | 1.0 → 1.0 | 1.0 → 1.0 | sustained → sustained |
| whole | 0.52 → 0.89 | 1.32 → 1.42 | 0.65 → 0.67 | broken → broken |

What changed: the refrain's complementarity rose from 0.13 to 0.67 and the verses' from 0.18 to 0.39; held, sustained bars fell from 19% of the song to 5%; verse 4 and the final refrain now move in both hands. Semitone clashes between organ and choir fell from 28 eighths to 18, and the parallel octaves between the organ's top and its pedal (four in the second edition, at bars 8, 41, 52 and 75) are gone.

What did not: the right hand over the whole song is 0.89 onsets a beat, still under the Lieder floor of 1.13. That is mostly the plan. The verses keep the hymnal right hand (0.67) because organists keep inner verses close to the hymnal harmony, and there is no table of organ hymn accompaniment to say what an organ's right hand should do; a piano part is a loose stand-in. The verses can't change from one to the next in notes, because verses 1-3 share the printed bars, so their variety is in the registration printed over bar 9.

New tools: organ_readings53.py (the readings above, by the tables' own texture rules) and clash53.py (semitone clashes, organ outer parallels). Consistency: 55 of 55 checks pass, among them the new ones for the inner line, the pedal parallels, the clash count, the Lieder ranges, the unchanged choir parts and the registrations.


## Fourth edition: the new findings applied

The choir's notes and the descant keep their pitches and onsets (a check). The changes:

- **Breaths (749.19, 749.20):** every part takes a beat's breath before the third line of each verse and refrain, after the half-stanza: bars 16 and 32, and in F bars 52 and 68. The tune had no breath of a beat or more anywhere. The organ's hands lift where their notes end there; held pedal points carry on.
- **Verses 1-3 (749.16):** the organ's right hand now carries the tune over an inner line, as the refrains do. The line is the altos (with their passing notes) plus a filling chord tone, moving to a neighbouring chord tone on held beats, so the harmony stays the hymnal one. Where there is no room above the alto, the filling note goes under it, and the lower note moves when the upper can't.
- **Each return higher (749.17):** the registration now builds through the three refrains (1st time Swell flutes; 2nd, add the Great open diapason; 3rd, add the Great principal 4′) and through the verses (v. 3 on the Great diapasons).
- **The intensity curve as sung (749.17):** intensity53.py reads the record in performed order (144 bars: three times verse and refrain). Per bar it takes the singers' top note, whether the choir sings, how many parts sound, the organ's onsets, and the dynamic with its registration step. Each verse and each refrain is above the one before. The high point falls at 0.87 of the song, at the final refrain's arrival, with the release over its last line ("hush now", p) and the coda. That is 0.02 past the 0.85 the finding proposes. It is kept because a carol's last refrain is its arrival.

Organ against the Lieder 3/4 table, third edition to fourth:

| Section | Right hand a beat | Complementarity |
|---|---|---|
| Verses 1-3 | 0.67 → 0.96 | 0.39 → 0.41 |
| Refrain | 0.79 → 0.90 | 0.67 → 0.67 |
| Final refrain | 1.10 → 1.23 | 0.68 → 0.68 |
| Whole song | 0.89 → 0.99 | 0.67 → 0.67 |

Semitone clashes stay at 18 eighths, with no outer parallels.

Against the popular corpus:

- **Melody:** the tune is at the 41st percentile for melody surprise, the 26th (verse) and 44th (refrain) for rhythm surprise, and the 20th for chords.
- **Verse re-entry:** after the new breath, the verse's re-entry note is a little more surprising than the verse's average (3.15 against 3.12 bits).
- **Refrain re-entry:** the refrain's re-entry is plain (1.56 against 2.45 bits). Its fresh moment comes four beats later, at the leap to the summit on "world". Making the re-entry itself fresher would mean changing a pitch of the locked tune, so it is left to the writer.

Consistency: 59 of 59 checks pass, including new ones for the breaths, the verse inner line, the rising returns and the late high point.


## Perception checks (psychoacoustics round)

Three checks from the research round "Psychoacoustics for the songwriting engine" were built in studies/psychoacoustics/perception.py and run on all four editions. Each was confirmed or corrected in the fourth edition:

| Check | 1st | 2nd | 3rd | 4th, before the fix | 4th, final |
|---|---|---|---|---|---|
| Organ pairs below the low-interval limits (mud) | 11 | 7 | 7 | 7 | 0 |
| Sung onsets with the organ above the tune (top voice lost) | 0% | 0% | 22% | 22% | 0.8% |
| Sung onsets with the organ a second or less from the tune | n/a | n/a | 17% | 12% | 11% |
| Choir crossings | 0 | 0 | 0 | 0 | 0 |

The fixes:

- **Mud:** a left-hand note that makes a close interval below its limit with the pedal or another left-hand note moves up an octave. The limits are an arranger's rule of thumb; the roughness model only ranks the intervals.
- **The tune on top:** verse 4's chords stay strictly under the unison tune. That restores the second edition's rule (749.8), which the third edition had relaxed for fuller voicings, and both checks now agree.

Roughness (Sethares, six harmonics) is unchanged across the editions: a mean of 0.57 a slice. Semitone clashes are 20 eighths, against 18 in the third edition and 28 in the second.

Each sung line lasted about 8.2 seconds at ♩ = 88 (median of 19 lines), just over the 8-second limit of short-term memory for a phrase. At the writer's choice, the tempo is now ♩ = 92 ("gently rocking" still), and a line lasts 7.8 seconds.

Consistency: 62 of 62 checks pass, with new ones for the low intervals, the tune on top and no choir crossings.


**Brought to Luthier's own limits (Module 9.14).** Luthier v7 already holds these voice-leading rules (Huron 2001), with stricter low-interval limits than the first sketch here: no third below F3 and no second below C4. Measured by them, the organ broke the limits at 117 places, mostly the pedal doubling the choir's basses at pitch, with the left hand a third above it. The fixes:

- **The pedal in its own octave:** the pedal is now written there (C2 to D3), sounding an octave lower again on the 16′ stops.
- **The link's left hand:** now open fifths.
- **Voicings:** verse 4's voicings are chosen clear of the limits.
- **The rest:** any remaining close pair is settled by moving the left-hand note an octave, or by thinning an inner chord. The pedal never moves.

Violations: 0. The tune is on top at 99.2% of sung onsets. 99% of the sopranos' and altos' notes still sound in the organ, and every bass note sounds in the pedal at the octave. Clashes are 20 eighths, with no outer parallels. All 62 checks pass.

## Findings

### 749.11 A hymn needs a hymn mode and hymn tables

**Problem.** The engine has no strophic mode: one tune for every stanza, the rhythm's frame set by the stanza's meter (here Common Meter, iambic), stressed syllables on downbeats. And the Essen folk tables do not describe hymn tunes: in a hymn frame every bar is one of three rhythms.

**Evidence.** Song 53's sketch built the frame by hand and drew inside it. Every survivor's distinct rhythms over bars sat under the kept 3/4 range (the pick 16%, kept 35% to 67%); onsets on the beat 100% (kept 57% to 82%); notes a bar 1.9 (kept 2.8 to 4.0): all set by the form, so printed, not charged.

**Fix (proposed).** A hymn mode: the stanza's meter (CM, LM, SM, 87.87 and so on) gives each line's pickup, stressed downbeats and held ending; the tune is drawn once and checked against every stanza's stresses. Kept tables from a hymnal corpus (tunes with their meters) for the readings the frame leaves free.

**Check.** A Common Meter tune whose rhythm readings sit inside kept hymn-tune quartiles, sung to every stanza with every stressed syllable on a downbeat.

### 749.12 A descant module

**Problem.** The engine has no descant. Song 53's descant was written with song 52's harmony-as-lines search (above the sopranos, their rhythm and words, chord tones, the summit pinned).

**Evidence.** The descant's readings: moves with the tune 26%, against it 35%, holds 39%; no parallels; its top, A5, once on "world". A first pass pinned the summit after the search and left a parallel fifth beside it (G4 to F4 under D5 to C5, in the refrain's first line); the pin moved inside the search, and the floor was lowered to let the line step down; the parallel went.

**Fix (proposed).** A descant module: a line above the tune for the last stanza or refrain, its own rhythm allowed (longer notes), the summit placed late and pinned inside the search, kept tables from published descants.

**Check.** No parallels with the tune or the bass, the summit in the last quarter, the line above the tune throughout.

### 749.13 Choral documents from one timeline

**Problem.** A choir and an organist need their pages to agree bar for bar. Engraving each document separately leaves bar numbers, breaks and notes free to drift.

**Evidence.** Song 53's two documents come from one record and share one line (time, keys, bar lines, marks, a break every fourth bar); bars 1-80 fall on the same systems in both; every voice read back from MIDI; the choir notes compared between the two sources.

**Fix (proposed).** The engine's standard for choral output: one timeline record, one shared global line with forced breaks, every document written from it, and the readback per voice.

**Check.** On any choral song: the same bars at the start of every system in every document, and every voice matching the record.

### 749.14 The engine has no accompaniment

**Problem.** Nothing in the engine writes an accompaniment. Song 53's first organ part doubled the choir's four parts for most of the carol, and its introduction and verse 4 were in the same texture: correct, and too plain for an organist's score.

**Evidence.** First version: outside the introduction and link, the organ's notes were the choir's (right hand two notes, left hand one, pedal the bass); no eighth notes; a 4-bar introduction; no coda. Rewritten: the introduction 8 bars; three notes in the right hand on 41 of 57 chords in verses 1-3; the left hand rocking in eighths (263 notes); verse 4's right hand below the tune throughout, with a suspension; the final refrain over a tonic and a dominant pedal; a 4-bar coda; every note read back from MIDI.

**Fix (proposed).** An accompaniment module for keyboard-led songs: a texture plan by section that builds through the song (doubling and support early, independence late), figures by metre (the rocking eighths in 3/4), pedal points at phrase openings and before cadences, suspensions at chord changes, an introduction from the refrain's tune and a coda from its last phrase.

**Check.** On any keyboard-led song: the accompaniment's texture grows by section, the late sections do not double the tune, and every note fits its chord or resolves by step.

### 749.16 An accompaniment plan by section role

**Problem.** The engine gives every section of an accompaniment the same treatment, so a song with repeated verses sounds static and an organ part looks thin even when each bar is correct (song 53, first and second editions: the organ's right hand 0.52 onsets a beat, 19% of bars held chords).

**Evidence.** Organ practice gives each verse a role: hymnal harmony with changes of colour for the inner verses, free harmony for the introduction, the interludes and the last verse (the research report "Accompaniment corpora and music theory"). Human arrangements repeat an accompaniment within a section type and change it between types; same-type sections are about 1.68 times more alike (POP909 studies). Song 53's third edition, written to such a plan, raised the organ's right hand to 0.89 onsets a beat and the refrain's complementarity from 0.13 to 0.67, with fewer clashes and no outer parallels.

**Fix.** Before arranging, assign each section a role (introduction, support, lift, interlude, climax, close) and a texture for each hand from the accompaniment tables (by metre: textures, onsets a beat, complementarity). Write the bass first in free sections. Repeat a section's texture when the section repeats and change it when the role changes. Where repeats share printed bars, vary by registration or orchestration. Patterns are stored apart from chords and fitted to each chord, as the published systems do.

**Check.** Per section, each hand's onsets a beat and complementarity sit inside the table's middle half for its role, or the plan says why not. Sustained bars are no more than the table's share. There are no parallel fifths or octaves between the outer voices, and no more clashes than the plain hymnal version.

\newpage
