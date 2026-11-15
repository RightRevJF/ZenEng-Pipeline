# Additive / Asymmetric (Non-Isochronous) Metres: Literature Notes for Melody Generation

Scope: 5/8, 5/4, 7/8, 9/8 aksak (2+2+2+3), 11/8, 13/8 and related forms (Bulgarian/Macedonian, Turkish usul, Greek, Finnish runosong). Notation used throughout: "2" = short beat of two pulses, "3" = long beat of three pulses; "322" = long-short-short (3+2+2), etc.

Research note on coverage: about 30 search/fetch calls were made. Several key primary sources could not be read in full (paywalls, CAPTCHA, allowlist blocks): Hannon & Trehub 2005 full text, Polak's EMR commentary on Goldberg, Goldberg's EMR 2015 numeric tables, Snyder et al. 2006, Hannon/Soley/Ullal 2012, Brăiloiu 1951 and Fracile 2003 originals, and London's *Hearing in Time* itself (London's NI-meter rules are reported here via Clayton's 2020 MTO summary). These are flagged in the Gaps sections.

---

## Q1. What groupings are standard for each metre, and in which traditions?

### Takeaway
Additive metres are built from 2- and 3-pulse beats over a fast, roughly equal pulse; the standard Balkan/Turkish forms are 5 = 2+3/3+2, 7 = 2+2+3 or 3+2+2 (2+3+2 is rare in Balkan folk corpora), 9 = 2+2+2+3, 11 = 2+2+3+2+2 (or 2+2+2+2+3), 13 = 2+2+2+3+2+2 (and variants). In Bulgaria the position of the long beat is dance-specific and stable (paidushko long-last 2+3; rŭchenitsa long-last 2+2+3; makedonsko horo long-first 3+2+2).

### Cited Findings
**General aksak table (pulse groupings and named examples):**
- 5 pulses: 2+3, 3+2 (Turkish Türk aksağı; Bulgarian paidushko) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)
- 7 pulses: 2+2+3, 2+3+2, 3+2+2 (Turkish devr-i turan, devr-i hindi; Bulgarian račenica, lesnoto/četvorno) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak) (the table names these dances against the 7-groupings but the fetch did not resolve which name pairs with which rotation)
- 9 pulses: 2+2+2+3 "and variants" (Turkish aksak usul; Bulgarian daychovo, grancharsko) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)
- 11 pulses: 2+2+2+2+3 and 2+2+3+2+2 (Bulgarian gankino) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)
- 13 pulses: 2+2+2+2+2+3, 2+2+2+3+2+2, 3+4+4+2 (Bulgarian elenino horo, krivo sadovsko horo; Turkish şarkı devr-i revâni) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)
- Longer compound aksak cycles of 15, 18, 22, 25 pulses exist (Bulgarian bučimiš, jove malaj mome, sandansko horo, sedi donka) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)
- Wikipedia's aksak article cites Brăiloiu 1951 "Le rythme aksak" (*Revue de Musicologie*), Fracile 2003, Arom 2004, Cler 1994 as its basis; it describes aksak as "uninterrupted reiteration of a matrix" of binary and ternary quantities; "aksak" means limping/stumbling — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)

**Bulgarian (Hristov 1913/1925, translated by Goldberg, MTO 30.4, 2024):**
- Paidushka (5 = 2+3): the elongated part is at the end and receives a "comparatively stronger" accent; the reverse order (3+2) is "not observed in songs" — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Rŭchenitsa (7 = 2+2+3): elongated beat at the end; makedonsko horo and mŭzhka rŭchenitsa put it at the beginning (3+2+2) — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Short part = 2 indivisible elements, elongated part = 3 elements; a "two-triple-group" metre (3+3) has two beats — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)

**Corpus frequency of 7-pulse rotations:**
- Singer (Macedonia) and Rice (Bulgaria) document 322 and 223; Fracile's study of ~6,000 transcriptions lists 322 and 223 but not 232 — [Clayton, MTO 26.1 (2020), summarising](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)
- London (2012) under maximal evenness allows nine 7-cycle varieties: 34, 322, 2221 and their rotations — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)

**Elenino horo (a contested case):**
- Published as 7/8, 13/16, 12/16 and others; Goldberg's timing of 8 tŭpan players (25 measures each) fits 7/8 best, 13/16 and 12/16 poorly — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- Dancers' steps fall on sixteenth positions 1, 5, 9, 11 of 14 (i.e., eighth-note durations 2+2+1+2), and both drumsticks strike together on those positions in >50% of measures; this creates a layer with a 1:2 short:long ratio, violating the usual theoretical rule that unequal beats must be less than 2:1 — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- Musicians count it variously as 1-2-3, 1-2-1-2, or 1-2-1-2-1-2-3, and many tŭpan players think in rhythmic templates rather than time signatures — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- Hristov suggested fast tempos lead musicians to hear 13/16 songs as 7/8 — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)

**Turkish usul:**
- Usul names by beat count: 5 = zafer, türk aksağı; 7 = devr-i hindî, devr-i turan, devr-i aryân; 8 = düyek; 9 = aksak, ağır aksak, oynak, evfer, bulgar darbı, çiftesofyan (raksaksağı); 10 = aksaksemaî; 13 = nimevsat; 14 = devrirevan; usuls range up to 88 (Darbıfetih) in the list (and to 128 per the text) — [Wikipedia, "Rhythm in Turkish music"](https://en.wikipedia.org/wiki/Rhythm_in_Turkish_music)
- Stroke vocables: "düm" = strong low stroke (single or double duration); "tek/teke/tekkyaa/te-ek" = light strokes — [Wikipedia, "Rhythm in Turkish music"](https://en.wikipedia.org/wiki/Rhythm_in_Turkish_music)
- CompMusic presents aksak as 9/8 and düyek as 8/8, notated as strong right-hand "düm" strokes vs weaker left-hand strokes, with an eighth-note pulsation from the cycle start — [CompMusic, Usul examples](https://compmusic.upf.edu/examples-usul-mmt)
- Aksak metres in Turkey occur mainly in vocal and instrumental dance music — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)

**Finnish runosong:**
- Rune singing's most common musical metres are 5/4 and 4/4; a special 9/8 wedding rhythm occurs in the northern rune-singing area — [Finnish Music Quarterly, "Rune singing: the musical vernacular"](https://fmq.fi/articles/rune-singing-the-musical-vernacular)
- The trochaic-tetrameter line that "looks like 4/4 on the page" is "often sung in 5/4, with the last two syllables having equal emphasis" — [University of Alaska Fairbanks music page (non-peer-reviewed)](https://www.uaf.edu/music/cms/finnish-four-beat-line.php)

### Inferences
- Engine default table (derived from the above): 5/8 → {2+3 (Bulgarian default, long-last), 3+2 (Turkish permits)}; 7/8 → {2+2+3 rŭchenitsa, 3+2+2 makedonsko/lesnoto/kalamatianos-type}, weight 2+3+2 low; 9/8 aksak → 2+2+2+3; 11/8 → 2+2+3+2+2 (long in middle) or 2+2+2+2+3; 13/8 → 2+2+2+3+2+2 or 2+2+2+2+2+3. Treat 9/8 = 3+3+3 (compound triple) as a separate, isochronous category and never mix it with aksak 2+2+2+3 within a tune unless deliberately modulating.
- Because Fracile's ~6,000-tune corpus lacks 232, a generator imitating Balkan folk style should essentially never emit 2+3+2 in 7/8.
- Hristov's long-last rule for paidushka suggests 5/8 Bulgarian melodies should put the long beat (and its accent) at the end of the bar.
- A Finnish runosong 5/4 setting likely corresponds to an 8-syllable line where the final two syllables each get a full beat (inference from "last two syllables having equal emphasis"; the exact durational template was not confirmed in a scholarly source).

### Gaps
- Specific Turkish usul-to-grouping mappings (e.g., which of devr-i hindi / devr-i turan is 3+2+2 vs 2+2+3; türk aksağı 2+3 vs 3+2; aksak semai 10/8 = 3+2+2+3?) and the düm/tek stroke pattern for each could not be confirmed from a readable source. Recollection (unverified): aksak 9/8 = 2+2+2+3, devr-i hindi = 3+2+2, curcuna 10/8 = 3+2+2+3. Verify with Holzapfel & Bozkurt (ISMIR 2012) or the CompMusic SymbTr corpus.
- Greek groupings (kalamatianos 7/8 = 3+2+2, tsamikos 3/4 with uneven beats, zeibekiko 9/4, karsilamas 9/8 = 2+2+2+3) were not confirmed by any source fetched here.
- Bulgarian kopanitsa/gankino 11/8 grouping and dance-specific 13/8 groupings rely only on Wikipedia's table.
- The scholarly basis for Finnish 5/4 runosong (Launis, Asplund, Leisiö, Saarinen music analyses) was not reached; the "5/4" claim rests on FMQ and a university web page.

---

## Q2. How are short and long beats actually timed in performance?

### Takeaway
Theory (Hristov, Cler, London) says short:long = 2:3 (long/short = 1.5). Measurements split: Goldberg's 18-recording Bulgarian tŭpan study finds rŭchenitsa and elenino horo within about 10 ms of 2:3 (max 23 ms), while Bernacki's two Pirin 3+2+2 songs show measured proportions that do not fit 2:3 at all (long/short ≈ 1.24 and 1.59, with the first short beat shortest). Systematic microtiming: group-initial beats lengthened, mid-group beats shortened, final IOI of the bar sometimes shortened.

### Cited Findings
**Theoretical ratio:**
- Standard Bulgarian theory uses a 2:3 short-to-long ratio — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- Hristov: primary element pulse ~400–432 per minute; short part = 2 elements, elongated = 3 (implies 1.5, but nominal, not measured); whole-measure tempos ~80 (paidushka) and 60–66 M.M. (rŭchenitsa) — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Cler (1994), southwestern Turkish aksak: "the ratio between short and long units is 2:3" (no sample size given; slowest chart tempo 35 bpm) — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)

**Goldberg, "Timing of Unequal Beats in Bulgarian Drumming" (GMTH Proceedings 2015, pub. 2020):**
- Sample: 18 recordings by 9 tŭpan players (one rŭchenitsa + one elenino horo each), three regions; random 28-measure samples (42 measures per mean in the table) — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Largest deviation from theoretical 2:3 timing ≈ 23 ms (long beat, bar 1, northern Bulgarian rŭchenitsa); most deviations < 10 ms; differences of ~7 ms reach significance by dance, region and position in the two-bar group; SDs ≈ 10–15 ms after tempo normalisation — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Tempo: rŭchenitsa first short beat ≈ 245 bpm; elenino horo first beat ≈ 138 bpm (non-overlapping); elenino measure level ≈ 39 bpm; rŭchenitsa two-bar level ≈ 35 bpm — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Pirin rŭchenitsa: first beat 15–20 ms longer than each of the other three short beats in the two-bar group; first measure averages 19 ms longer than the second (rŭchenitsa) and 12 ms longer (elenino); other regions ≤ ~6 ms — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Across groups, beats at group beginnings tend to be longer and mid-group beats shorter, most pronounced at the start of two-bar groups; rŭchenitsa deviates from theory more than elenino horo — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)

**Goldberg, elenino horo (AAWM 2019):**
- In Mustakov's performance the final IOI of each measure was shorter than the other six; actual vs expected measure end differed by ~44 ms (less than half a sixteenth); a commercial recording (Ivan Shibilev, 25 measures, melody/chord onsets) showed the same short-final-IOI pattern; three players had three IOI boundaries > 1 SD from theoretical 7/8 — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)

**Goldberg, rŭchenitsa (via Clayton):**
- Rŭchenitsa (223) averaged 1615 ms per two-cycle unit, fastest IOI 115 ms — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)

**Goldberg, EMR 2015/16 (abstract only):**
- Two percussion performances in long-short-short aksak (Macedonian Romani singer Muzafer Bizlim tapping an ostinato; Bulgarian tŭpan player Mitko Popov in ensemble): timing varies with melodic grouping and ensemble interaction; Bizlim's tap timing "seems to mark some local and large-scale group boundaries" — [Goldberg, EMR 10(4)](https://www.osu.tests.sfulib4.publicknowledgeproject.org/index.php/EMR/article/view/4884)

**Bernacki 2023, two Pirin-Macedonian dance-songs in 3+2+2 (tambura stroke IOIs):**
- "Malka moma vada kopa": 54 cycles; beat means 321 / 246 / 272 ms (SD 29/24/24); cycle 839 ms; proportions 38:29:33 — [Bernacki, Konservatoryum 10(1) 2023, full text](https://dergipark.org.tr/en/download/article-file/2930763)
- "Oi le Kale": 48 cycles; beat means 399 / 229 / 272 ms (SD 35/28/29); cycle 900 ms; proportions 44:26:30 — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)
- Theoretical 3+2+2 reference = 42:29:29; Beat 3 longer than Beat 2 in 82% and 81% of cycles (Beat2:Beat3 = 0.91 and 0.86); proportion SDs ~2.6–3.3% of cycle — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)
- Conclusion: proportions "do not align with and cannot be described by a 2:3 beat ratio"; author proposes describing these as "three-beat long-short-short" rather than 7/8; a local musician called the songs 7/8 played "neritmichno" — [Bernacki 2023, abstract](https://dergipark.org.tr/en/pub/konservatoryum/article/1245746); [full text](https://dergipark.org.tr/en/download/article-file/2930763)
- Limitations: only two YouTube recordings of unknown date/context — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)

**Tempo ranges:**
- Bartók: "Bulgarian rhythm" pulse 200–400 bpm, up to 600 bpm for "hyperbulgarian"; Moelants (2006): cycle lengths ~1–2 s — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)

**Lab production/synchronisation (Western musicians):**
- Repp, London & Keller 2008: 10 musicians tapping with 2+3, 3+2, 2+2+3, 3+2+2 etc. at 400 ms ("2") and 600 ms ("3"); distortions were "small" but tones after short intervals came early, i.e., an *enhancement* of short/long contrast; some 3-interval patterns showed first short shortened and second lengthened — [Repp, London & Keller, Music Perception 26(2) 2008](https://cdn.carleton.edu/uploads/sites/721/2021/12/Repp-London-Keller-2008-MP.pdf)

### Inferences
- Derived long/short ratios (my arithmetic): Bernacki song 1 = 1.30 (vs Beat 2), 1.18 (vs Beat 3), 1.24 (vs mean short); song 2 = 1.74, 1.47, 1.59. Goldberg's ±23 ms maximum around a ~245 ms short beat implies long/short roughly in 1.41–1.59 for rŭchenitsa. So a plausible humanisation range is long/short ≈ 1.2–1.7, centred near 1.5 for Bulgarian drumming with regional/song variation.
- Practical microtiming template for playback (not for symbolic scoring): keep symbolic durations as exact 2/3 pulses; at render time lengthen each group-initial beat (esp. bar 1 of a two-bar group) by ~2–6% of a beat, shorten mid-group short beats; in long-short-short, make the first short beat the shortest (~0.9× the second).
- Implied tempo windows: rŭchenitsa ~70–75 bars/min (808–900 ms bar), pulse ~115–130 ms; elenino horo much slower beat (~435 ms first beat). A generator should bind metre type to tempo band (London's "tempo-metrical types").

### Gaps
- Polak's EMR commentary on Goldberg ("Pattern and Variation in the Timing of Aksak Meter") and Goldberg's EMR numeric tables could not be fetched.
- No measured ratios found for Turkish usul performance (Holzapfel/Bozkurt), Greek, or 9/8, 11/8, 13/8 aksak; no measured data for Finnish 5/4 runosong timing.
- No study separating melodic (vocal/instrumental) note timing from drum timing in aksak was found.

---

## Q3. Which theoretical models describe these metres?

### Takeaway
Three lineages: (1) Hristov's 1913 Bulgarian theory of indivisible elements grouped into 2- and 3-element parts (Bartók's "Bulgarian rhythm"); (2) Brăiloiu's 1951 "aksak" generalisation (with Fracile and Arom continuing), defined by reiteration of a binary/ternary matrix; (3) London's NI-meter theory: an isochronous subdivision level under non-isochronous beats, constrained by maximal evenness and tempo limits.

### Cited Findings
- Hristov: Bulgarian irregular metres are built from indivisible elements (chronos protos) combined into 2- or 3-element parts, unlike European irregular metres that subdivide equal parts; some relations are "chronos alogoi"; Bartók named the type "Bulgarian rhythm" after Hristov and Stoin — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Goldberg reads Brăiloiu's renaming ("aksak") as a challenge to Bulgarian claims of national ownership — [Hristov trans. Goldberg, MTO 30.4 (2024), translator's note](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Aksak: rhythm system based on "the uninterrupted reiteration of a matrix" of binary and ternary quantities (Brăiloiu 1951) — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak); see also Arom, "Pour une théorie de l'aksak" — [HAL Collège de France](https://hal-college-de-france.archives-ouvertes.fr/halshs-03940899v1)
- London (1995): complex metres rely on an isochronous subdivision level, with beats long (3) or short (2); they "require explicit specification of their invariant features through the patterns of duration"; all levels "must come into being together and be maintained together" — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)
- London (2012): beat rates 400–1200 ms; NI-meters more tightly tempo-constrained than isochronous; longest metrically significant intervals ~2000 ms; 7-cycles must use one long + two short beats (322/223/232) at the beat level; maximal evenness yields nine 7-cycle varieties (34, 322, 2221 + rotations) — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)
- London's interpretation is "compatible with the great majority of examples in the literature from Turkey and the Balkans" (Clayton) — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)
- Current metric theory requires unequal durations in a layer to be less than 2:1; elenino horo's step layer (2+2+1+2 eighths) is a counterexample — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- London's "many meters" hypothesis: small, consistent timing differences can be learned as distinct metres defining a style; Goldberg links his data to London's tempo-metrical types — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Bernacki argues his data challenge the isochronous-subdivision assumption and calls for revising Balkan NI-meter theory — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)

### Inferences
- For a symbolic engine, London's model is the most encodable: a pulse grid; a beat sequence over {2,3}; constraint of maximal evenness (no two 3s adjacent when 2s are available to separate them, e.g., 2+3+2+3 rather than 3+3+2+2); bar duration ≤ ~2 s.
- Note a tension to handle: rŭchenitsa short beats (~245 ms) fall below London's 400 ms beat floor, so the felt beat is probably the bar (3 beats) or two-bar unit; the generator's "beat" for phrasing purposes should be the 2/3 group, but its "felt pulse" may be the whole bar at fast tempos.

### Gaps
- Brăiloiu 1951, Fracile 2003 and Arom 2004 originals not read; their specific claims (e.g., Brăiloiu's ratio rules, permissible matrices, "aksak irregular" vs "regular" types) are not verified here.
- London's *Hearing in Time* 2nd ed. not consulted directly; numbers come from Clayton's summary.

---

## Q4. Accent hierarchy and melodic behaviour (metric weight, note density, phrase endings)

### Takeaway
Evidence is thin but consistent: the long beat carries extra weight (Hristov: "comparatively stronger" accent on paidushka's final long beat); downbeat and group-initial beats are marked by heavy (right-hand / düm) drum strokes; group-initial beats are timed long; dance steps land on group starts. No quantitative corpus study of melodic note density per short vs long group was found.

### Cited Findings
- Paidushka 2+3: the long final part receives "comparatively stronger" accent — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Rŭchenitsa accompaniment: heavy right-hand and light left-hand strokes on tŭpan/daire; in the "second group" metres each element is a separate beat with independent accent — [Hristov trans. Goldberg, MTO 30.4 (2024)](https://www.mtosmt.org/issues/mto.24.30.4/mto.24.30.4.goldberg.pdf)
- Turkish usul: strong "düm" (right hand, low) vs light "tek" (left hand) strokes define the cycle — [CompMusic](https://compmusic.upf.edu/examples-usul-mmt); [Wikipedia, "Rhythm in Turkish music"](https://en.wikipedia.org/wiki/Rhythm_in_Turkish_music)
- Elenino horo: both sticks together on positions 1, 5, 9, 11 (>50% of measures); final dance step gives a sense of "landing"; regional (Pirin zurna) drumming styles differ — [Goldberg, AAWM 7.2 (2019)](https://oldaawmjournal.iftawm.org/articles/2019b/Goldberg_AAWM_Vol_7_2.pdf)
- Timing varies with melodic grouping; a singer's taps mark local and large-scale group boundaries — [Goldberg, EMR 10(4)](https://www.osu.tests.sfulib4.publicknowledgeproject.org/index.php/EMR/article/view/4884); [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Two-bar grouping is perceptually/temporally real in rŭchenitsa (first bar of pair longer in Pirin) — [Goldberg, GMTH 2015](https://storage.gmth.de/proceedings/articles/198/pdf/gmth-proceedings-artikel-198.pdf)
- Rūpak tāl (a North Indian 3+2+2 cycle, a related NI case): beats 3, 5, 7 subdivided >95% of the time while beat 1 subdivided only 28% (42 recordings) — i.e., the long first group is often a single held note — [Clayton, MTO 26.1 (2020)](https://www.mtosmt.org/ojs/index.php/mto/article/view/462/60)
- Bernacki speculates syllables-per-measure (2 vs 3 alternating vs mostly 2) may shape microtiming — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)

### Inferences
- Suggested weight hierarchy for encoding: bar downbeat (group 1) > long-group onset (if not group 1) > other group onsets > within-group pulses. In long-last metres (2+3, 2+2+3, 2+2+2+3) the long group is both an accent and a cadential "landing" slot; place phrase-final long notes on the long group's onset and let them fill it.
- Note-density heuristic (weakly supported, by analogy to the rūpak data and Hristov's elements): short groups more often carry 1–2 notes on pulse onsets; long groups often carry one longer note or a 2+1 / 1+2 figure. Avoid placing onsets on the 2nd pulse of a short group when emphasising metre clarity; syncopation in this idiom is mostly expressed by tying across group boundaries, not by off-pulse onsets (inference, unverified).
- Phrase structure: plan in two-bar units (supported by rŭchenitsa two-bar timing), with 4- and 8-bar phrases.

### Gaps
- No corpus-statistics study of note onsets per pulse position in Bulgarian/Turkish/Greek aksak melodies was located (a natural target: Essen folksong collection's Balkan subsets, CompMusic SymbTr for Turkish usul).
- No study quantifying where phrase-final long notes fall in 9/8, 11/8, 13/8.

---

## Q5. What perception and learning evidence exists?

### Takeaway
Enculturation shapes NI-metre perception: North American adults detect disruptions to simple (isochronous) metres but not to Balkan 2+2+3 metres, while Bulgarian/Macedonian adults and 6–7-month-old North American infants detect both. Adults with some non-Western exposure detect complex-metre violations in unfamiliar Turkish music but still do better on simple metre.

### Cited Findings
- Hannon & Trehub (2005, *Psychological Science*, "Metrical Categories in Infancy and Adulthood"): 50 North American college students, 17 first/second-generation Bulgarian and Macedonian immigrant adults, 64 North American infants aged 6–7 months; four Serbian/Bulgarian folk-dance tunes, two simple metre and two complex (2+2+3); altered versions inserted beats to change structure — [EurekAlert release, 7 Feb 2005](https://www.eurekalert.org/news-releases/602135)
- Results: North American adults detected changes to simple-metre tunes but not complex; Bulgarian/Macedonian adults detected changes in both; infants detected changes in both (like the immigrant adults); authors concluded no rhythms are inherently easier for the brain and flexibility is lost with narrow exposure — [EurekAlert release](https://www.eurekalert.org/news-releases/602135)
- Kalender, Trehub & Schellenberg (2013, *Psychological Research* 77:196–203): with unfamiliar Turkish music, Western-only adults detected meter violations in simple but not complex (non-isochronous tactus) metres; adults with some non-Western exposure detected both, better on simple — [Springer](https://link.springer.com/doi/10.1007/s00426-012-0427-y)
- Western musicians can synchronise with 2:3 NI patterns at 400/600 ms with small, contrast-enhancing distortions — [Repp, London & Keller 2008](https://cdn.carleton.edu/uploads/sites/721/2021/12/Repp-London-Keller-2008-MP.pdf)

### Inferences
- For Western-enculturated listeners (likely ZenEng's audience), NI metres need strong, redundant cueing: consistent grouping across the piece, drum/bass marking every group onset, melodic onsets aligned with group starts, and avoiding mid-piece changes of grouping. Bulgarian/Macedonian-enculturated listeners tolerate and track more variation.
- Sample sizes are modest (17 immigrant adults; 64 infants), so treat these as directional.

### Gaps
- Exact effect sizes for Hannon & Trehub 2005 (PMC full text blocked by CAPTCHA).
- Hannon, Soley & Ullal (2012, JEP:HPP, "Familiarity overrides complexity...") and Hannon & Trehub (2005, PNAS, infants losing sensitivity by 12 months, recovered with 2 weeks of exposure) not read; Snyder, Hannon, Large & Christiansen (2006, Music Perception 24(2), synchronisation and continuation tapping to complex meters) located but not fetched — [listing](https://www.sciencegate.app/document/10.1525/mp.2006.24.2.135).

---

## Q6. How are melodies set to text in these metres?

### Takeaway
Only partial evidence was found. In Finnish Kalevala-metre singing, long stressed syllables go on stressed beats and short stressed syllables on unstressed beats, word stress is always word-initial, melodies typically span a pentachord, and the 8-position trochaic line is often stretched to 5/4 by giving the last two syllables equal weight. For Balkan aksak, syllable counts per bar (2 vs 3) appear to interact with timing, but no systematic stress-to-group study was found.

### Cited Findings
- Finnish stress falls on the first syllable of the word; long stressed syllables are placed on stressed beats and short stressed syllables on unstressed beats — [FMQ](https://fmq.fi/articles/rune-singing-the-musical-vernacular)
- Melodic range usually a pentachord (sometimes 3–4 notes, or 1–2 more); basically pentatonic; first and fifth degrees relatively fixed, third variable; large leaps rare; tonic–dominant tension central; lines and melodies chosen in performance; solo, alternating and heterophonic group singing — [FMQ](https://fmq.fi/articles/rune-singing-the-musical-vernacular)
- 4/4-looking trochaic tetrameter is "often sung in 5/4, with the last two syllables having equal emphasis" — [UAF](https://www.uaf.edu/music/cms/finnish-four-beat-line.php)
- Runosong performance often has a dual structure (lead singer + choir/assistant repeating lines); textual and musical structures "seem independent of each other" (Saarinen; corpus 5,874 lines of Arhippa Perttunen) — [Saarinen, Oral Tradition 31/2 (2017)](https://journal.oraltradition.org/wp-content/uploads/files/articles/31ii/10_31.2.pdf)
- Bulgarian/Macedonian 3+2+2 songs: "Malka moma vada kopa" alternates 2 and 3 syllables per measure, "Oi le Kale" mostly 2 per measure — [Bernacki 2023](https://dergipark.org.tr/en/download/article-file/2930763)
- Turkish prosodic vs musical metre in the beste form (Bektaş 2005) is cited as a relevant study — [Wikipedia, "Aksak"](https://en.wikipedia.org/wiki/Aksak)

### Inferences
- Finnish 5/4 template for an 8-syllable trochaic line: syllables 1–6 on eighth-note pairs (3 beats of 2 syllables, stressed syllables on beat onsets) and syllables 7 and 8 each a full quarter (beats 4 and 5) gives 5/4; this matches "last two syllables equal emphasis" but should be verified against Launis's transcriptions.
- General lyric-setting rule for aksak: place stressed syllables on group onsets, with the most prominent (phrase-stress) syllable on the downbeat or the long group; a 3-pulse group can host a stressed long syllable or a stressed+unstressed pair (2+1 pulses); a 2-pulse group hosts one syllable or an unstressed pair.

### Gaps
- No peer-reviewed study of Bulgarian, Macedonian, or Greek lyric stress placement relative to 2/3 groups was obtained.
- Bektaş 2005 (Turkish prosody vs usul) not read.
- No measured syllable durations in sung runosong.
