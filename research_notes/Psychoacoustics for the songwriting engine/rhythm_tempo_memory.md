# Perception of Rhythm, Tempo, Metre and Musical Memory: Rules for a Songwriting Engine

Scope note: compiled 2026-11-15 from web sources (primary papers where reachable, otherwise reviews, book reviews and university press releases). Almost all findings come from Western (mostly US/UK/European) participants and Western popular or art-music stimuli. Where a figure is secondhand (cited inside another paper) that is flagged. Figures I could not verify against a source are confined to the Gaps subsections.

---

## 1. Tempo and pulse: range of beat perception, preferred tempo, compound vs simple metre

### Takeaway
A beat can be felt only between roughly 100 ms (fastest events that stay separate) and roughly 1.8-2 s (slowest intervals that still link up), and a beat is strongest at about 450-750 ms per beat (80-133 bpm). Popular-music tempos and natural human movement both cluster tightly around 2 Hz (about 115-130 bpm, 480-520 ms). Within the usable range, what decides whether 6/8 sounds like "two" or "six" is how far apart the beats are.

### Cited Findings
- **Sensorimotor rate limits (Repp 2006, review abstract):** the auditory upper rate limit for synchronization is about 8-10 Hz, i.e. inter-onset intervals (IOIs) of **100-125 ms**, when biomechanical constraints are avoided; this limit varies with task difficulty and musical experience. The lower limit is about **0.56 Hz (1800 ms)** "regardless of modality". For visual flashes the upper limit is below 2.5 Hz (IOIs above 400 ms). — [Repp, "Rate limits of sensorimotor synchronization", Advances in Cognitive Psychology 2006 (DOAJ record)](https://doaj.org/article/dc3f29b3977e4adf8dfe9aa998eb40de)
- **Fusion and isolation limits (secondhand, citing Clarke 1999 and Repp 2006):** events closer than about **100 ms** are heard as fused, and events more than **2 s** apart are heard as isolated. — [Dahl, Huron, Brod & Altenmüller 2014, "Preferred dance tempo" (JNMR accepted manuscript)](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)
- **Preferred tempo (Fraisse 1982, as cited by Dahl et al.):** typically **100-133 bpm**, about 451-600 ms per beat. — [Dahl et al. 2014](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)
- **Corpus tempo distribution (Moelants 2002, as cited by Dahl et al.):** across DJ bpm lists and tapping data for Western music, most tempi fall between **115 and 127 bpm (about 472-522 ms)**, with a pronounced peak at **125 bpm (480 ms)**. Moelants fitted this distribution with a resonance model derived from van Noorden & Moelants (1999). — [Dahl et al. 2014](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)
- **Body resonance (MacDougall & Moore 2005, as cited):** day-long head-acceleration recordings show a marked vertical peak at about **2 Hz (120 bpm, 500 ms)**, even in activities without much locomotion. **Styns et al. 2007:** walking synchronizes best to music at **106-130 bpm**, and 80.7% of participants tapped at the rate they walked. — [Dahl et al. 2014](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)
- **Individual differences in preferred dance tempo (Dahl et al. 2014, own data):** Exp. 1 (Ohio, N=30): chosen beat periods had a mean of **429 ms (SD 129)**, range 251-674 ms (about 89-239 bpm). Stature (height and leg length) predicted beat period, r = .69, R² = .47, so taller people preferred slower beats. Exp. 2 (Hanover, N=40): mean **415 ms (about 132 bpm)**, range 256-803 ms. Height correlated r ≈ .40 (13% of variance) and age r = −.46 (older participants chose shorter beat periods, i.e. faster tempos). Heart rate had no effect. — [Dahl et al. 2014](https://vbn.aau.dk/ws/files/201902553/Dancetempo_JNMR_accepted_source_Jan2014.pdf)
- **London (2004), Hearing in Time, pp. 27-47 (secondhand, via a student summary):** periodicity can be detected from about **100 ms to 5-6 s**. A sense of beat or tempo exists from about **200-250 ms to 2 s** (p. 46). "Maximal pulse salience" is at about **500-750 ms (80-120 bpm)**. The floor and ceiling of the beat range come from the need for a hierarchy that allows at least one level of subdivision or grouping inside the perceptual limits. London's Figs 2.5-2.6 show that "comfortable" ternary (triple-grouped) options are relatively scarce. — [Summary of London 2004 (Eastman course PDF)](https://www.midside.com/pdf/eastman/fall06/th581/london_longuet_temperley.pdf)
- **London (2011), "Tactus ≠ Tempo":** the tactus is defined as a regular level with IOI of "approximately **500-1500 ms**". Subdivisions must have IOI "**greater than 100 ms**" to keep their rhythmic identity. A **300 ms IOI** is "too fast to be heard as the beat" (citing Fraisse 1982 and Clarke 1999). Pulse-finding models (Parncutt 1994, Eck 2001) predict a **600 ms** period to be maximally salient. Listeners may "tap slowly to quick music, and vice-versa". In London's 100-120 bpm 4/4 stimuli, 14 of 19 tappers stayed on one level: 9 tapped the beat (500/600 ms) and 5 tapped slower levels (1000-2400 ms). Metronome markings index the quarter note in simple metres and the **dotted quarter in compound metres**. — [London 2011 (Carleton PDF)](https://cdn.carleton.edu/uploads/sites/721/2021/12/London-2011-Tactus-vs-Tempo.pdf)
- **Background on van Noorden & Moelants 1999:** the paper "Resonance in the perception of musical pulse" (J. New Music Research) is the source of the resonance model. I could not retrieve its exact peak and width parameters (see Gaps). — [Bibliographic record](https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/63566145)

### Inferences
- **Engine tempo rule:** put the felt beat (tactus) at **450-750 ms (80-133 bpm)**. The default "sweet spot" for a song meant to make people move is **115-128 bpm** (480-520 ms). Ballads can go down to about 60-70 bpm only if a felt subdivision (eighths at 430-500 ms) carries the motion, because 1-1.8 s beats are near the lower limit.
- **Fastest-note rule:** no articulated note value should fall below **about 100-125 ms IOI**. Prefer a floor of about 125-150 ms for sung melody, since singers and lyric syllables need more time than taps (this margin is my inference, not a measured threshold). At 120 bpm, sixteenth notes are 125 ms, right at the limit. At 140 bpm and above, avoid continuous sixteenth-note melodies.
- **Slowest-level rule:** any level the listener has to track as a beat must stay under **about 1.8-2 s**. Whole bars or hypermetric cycles longer than about 5-6 s are not felt as periodic. They have to be understood through grouping and memory instead (see section 4).
- **Compound vs simple metre (inferred from the limits above):** in 6/8 the dotted quarter is the beat, so it should land in the 450-750 ms band. That makes eighth notes 150-250 ms, comfortably above the 100 ms floor. Dotted quarter = 80-130 bpm is the natural compound-duple range. If the dotted quarter goes slower than about 1 s (below about 60 bpm), the eighths (about 330+ ms) start to become the beat, and 6/8 drifts toward a slow "six" feel. If 3/4 runs fast (quarter below about 300 ms, i.e. above about 200 bpm), the bar becomes the beat and it is felt as one-in-a-bar (a waltz "in one"). The engine should choose 3/4 or 6/8 by which level it wants felt as the 450-750 ms beat: in 6/8 that is the dotted quarter (two beats per bar, each split in three), in 3/4 the quarter (three beats per bar, each split in two).
- **Other metres:** in 2/2 and cut time the half note is the beat, so half = 80-130. For 12/8 use dotted quarter = 60-100 (slow blues and gospel, with four beats per bar). In 5/8 and 7/8 at moderate tempo the beats are uneven (2+3, 2+2+3), and the listener needs a 100 ms+ eighth with beats lasting 2-3 eighths. Grouping of uneven metres is a Western-listener constraint (see section 2).

### Gaps
- Exact parameters of the van Noorden & Moelants (1999) resonance curve (often quoted as peaking near 500-550 ms with a broad, damped shape). Not verified here because the primary text was not retrieved.
- Fraisse's "spontaneous motor tempo" of about 600 ms (often quoted with a range of about 380-880 ms) was not verified from a primary source. Only the 100-133 bpm "preferred tempo" figure is sourced.
- No retrieved experimental study directly compared perceived beat level in 6/8 vs 3/4 at matched tempos. The compound/simple guidance above is inferred from the general limits and London's dotted-quarter convention.

---

## 2. Metre perception, metrical weight, and metre induction from melody

### Takeaway
Metre is a mental, nested set of periodicities that the listener infers. Every level must fit inside the 100 ms to about 2 s beat window and the 5-6 s cycle window. Ternary (three-way) groupings fit into those windows less easily than binary ones.

### Cited Findings
- London's account: metre requires a rhythmic hierarchy with at least one subdivision or grouping inside perceptual limits. That constraint sets the beat floor (200-250 ms) and ceiling (about 2 s), and "comfortable" ternary options are relatively scarce (Figs 2.5-2.6). Secondhand summary. — [Summary of London 2004](https://www.midside.com/pdf/eastman/fall06/th581/london_longuet_temperley.pdf)
- London (2011) refers to "metric malleability" (London 2004, pp. 48-50): one rhythm can be heard under different metrical organizations. He also shows that tempo judgments depend on the tapping level as well as the stimulus. In Exp. 3, mean bias was .0097 for tactus tappers and −.0805 for double-tactus tappers (one-tailed p = .026), so how a listener moves changes how fast the music seems. — [London 2011](https://cdn.carleton.edu/uploads/sites/721/2021/12/London-2011-Tactus-vs-Tempo.pdf)
- Syncopation is defined against a metrical-weight hierarchy. Witek et al. adapted the Longuet-Higgins & Lee model, which weights onsets by metrical level (downbeat strongest, then half-bar, beat, offbeat, sixteenth), and added instrument weights. — [Witek et al. 2014 (PMC PDF)](https://www.scienceopen.com/document_file/d9d000f1-421f-4984-8e28-d5dc02f2762e/PubMedCentral/d9d000f1-421f-4984-8e28-d5dc02f2762e.pdf)
- Matthews et al. 2019 quantified rhythmic complexity with Fitch & Rosenfeld's syncopation index and Povel & Essens' C-score (a measure of how strongly a rhythm induces a clock). The two correlated at r = 0.99 across their stimuli. — [Matthews et al. 2019 (CORE PDF)](https://core.ac.uk/download/185514684.pdf)

### Inferences
- **Metrical-weight rule:** to establish a metre, put long notes, phrase starts, harmonic changes and stressed syllables on strong positions (downbeat > mid-bar beat > other beats > offbeats) during the first 1-2 bars of a section. This induces the metre before any syncopation starts. The Povel-Essens logic says that accent-on-beat rhythms induce a strong clock.
- **Lerdahl & Jackendoff preference rules (from general knowledge, not retrieved):** strong beats go on longer notes, on harmonic changes and on group onsets, and adjacent strong beats should alternate. These are a reasonable scoring rubric for the engine but are not verified in this session.
- **Ternary caution:** because ternary hierarchies fit the windows less comfortably, triple and compound metres should state the metre more explicitly (bass on beat 1, clear "oom-pah-pah" or a dotted-quarter pulse), and use less syncopation, than 4/4.

### Gaps
- London's "tempo-metrical types" (TMTs) and his formal well-formedness constraints could not be retrieved in detail. The book chapter was not accessible, and the summary did not cover them. The commonly cited idea, unverified here, is that the same notated metre becomes a different perceptual metre at different tempos, which matches the inferences in section 1.
- I found no empirical sources on metre induction from melody alone (accent rules from contour peaks and duration), e.g. Povel & Essens 1985, Temperley, or Hannon et al. 2004. Not retrieved.
- Cross-cultural caveat: Western listeners favour isochronous, binary metres. Listeners from Balkan traditions handle non-isochronous metres better (Hannon & Trehub 2005, not retrieved). That source is unverified here.

---

## 3. Groove: syncopation, pleasure, harmony, microtiming, event density

### Takeaway
The urge to move and the pleasure taken both follow an **inverted U** against syncopation, so **medium** syncopation wins. Harmony of moderate complexity strengthens this, and very dissonant harmony weakens it. Dance experience increases groove responses more than musical training does.

### Cited Findings
- **Witek et al. 2014 (PLOS ONE 9(4): e94446):** 66 participants (57 analysed for background effects) rated 50 synthesized drum breaks (kick, snare, hi-hat). Each was a two-bar loop repeated 4 times (16 s) at **120 bpm in 4/4**. The syncopation index ranged from **0 to 81**. Wanting-to-move and pleasure ratings followed an **inverted U**. Quadratic models fit better than linear ones, and better than audio entropy, which was a weak predictor. **Medium syncopation** produced the highest ratings. Dancers gave higher ratings (F(1,49) = 13.53, p = .001). Musical training was only marginal (p = .062), and familiarity with groove music had no effect. The authors interpret this as a Berlyne-style optimal-stimulation effect: "some structural resistance" to the pulse invites the body to fill in the metre. — [Witek et al. 2014 (PMC PDF)](https://www.scienceopen.com/document_file/d9d000f1-421f-4984-8e28-d5dc02f2762e/PubMedCentral/d9d000f1-421f-4984-8e28-d5dc02f2762e.pdf); [U. Birmingham record](https://research.birmingham.ac.uk/en/publications/syncopation-body-movement-and-pleasure-in-groove-music/)
- **Matthews, Witek, Heggli, Penhune & Vuust 2019 (PLOS ONE 14(1): e0204539):** N=201 online (58 musicians vs 51 non-musicians compared). Stimuli were 54 one-bar piano patterns at **96 bpm**, 4/4, with an eighth-note hi-hat, each looped 4 times (10 s). Every rhythm had **five onsets in a 3+2 pattern**: low (all onsets on strong beats), **medium (son clave, rumba clave, one custom rhythm)**, and high (only the first onset on a strong beat). Both wanting to move and pleasure showed an inverted U for rhythm, with medium rated highest. Harmony: low (triads) ≈ medium (four-note extended chords) > high (chords with a flat-ninth). **Medium-complexity chords strengthened** the rhythmic inverted U for pleasure, and high-complexity chords weakened it. Harmony's effect on wanting to move was fully mediated by pleasure. Rhythm also had a direct effect on wanting to move. Musicians showed a stronger rhythmic inverted U. — [Matthews et al. 2019 (CORE PDF)](https://core.ac.uk/download/185514684.pdf); [press coverage](https://sciencedaily.com/releases/2019/03/190306143027.htm)

### Inferences
- **Syncopation target:** aim for **moderate** syncopation. As a working operationalization (my inference from the stimuli): in a one-bar, eighth-note grid with about 5 onsets, a clave-like 3+2 pattern with 2-3 off-beat onsets is near the optimum. Avoid patterns where only the downbeat is on a strong position. On Witek's 0-81 scale, the peak sits in the middle of the range, but the exact peak value is not in the text (see Gaps).
- **Syncopation must have a metrical frame:** keep at least one layer on the beat (hi-hat eighths, kick on 1, or bass on downbeats) whenever the melody or comping syncopates. Both studies kept an isochronous reference (the hi-hat), and the "resistance to the pulse" explanation needs a pulse to resist.
- **Harmony-rhythm budget:** pair syncopated rhythms with harmony of low-to-medium complexity (triads, 7ths and 9ths). Avoid stacking heavy dissonance (b9 colours, clusters) on top of high syncopation. High complexity in both dimensions lowers pleasure.
- **Metre generalization (caution):** both groove studies used 4/4 at 96-120 bpm. Applying "medium syncopation" to 3/4 or 6/8 is extrapolation. Given the ternary caution in section 2, use a lower syncopation density in triple and compound metres.
- **Tempo for groove:** the stimuli at 96-120 bpm sit inside the 2 Hz preferred band (section 1). Groove writing should default to 95-125 bpm.

### Gaps
- **Janata, Tomic & Haberman 2012 (J Exp Psych: General):** the primary text could not be retrieved (fetch blocked). Commonly reported findings, unverified here: groove is defined as "wanting to move", groove ratings correlate strongly with enjoyment, high-groove music produces easier and more spontaneous sensorimotor coupling, and soul/R&B excerpts were rated highest. Treat these as unverified.
- **Microtiming:** no sources retrieved. The general literature (e.g. Davies et al. 2013; Senn et al.) suggests microtiming deviations do not increase groove and may reduce it, but this is unverified here.
- **Event density:** no sources retrieved on the relation between event density and groove (e.g. Madison et al. 2011 on "beat salience" and event density).
- **Matthews 2020** (groove and the motor network, NeuroImage) was not retrieved.
- The exact numeric syncopation values at the inverted-U peak in Witek 2014 appear only in figures and were not extracted.

---

## 4. Memory and chunking: sensory memory, perceptual present, phrase length

### Takeaway
Phrase-level material lives in short-term or working memory, which Snyder puts at an upper bound of about **8 s**. The phrase is the largest unit grasped as a whole, and anything longer is understood by remembering and comparing parts. The popular "3-second now" is contested.

### Cited Findings
- **Snyder, Music and Memory (2000), via Chaffin's 2002 review:** echoic memory lasts "approximately **250 msec**" (as worded in the review) and working memory about **8 seconds**. Pulses at **20 per second and higher fuse** together (about 50 ms). Phrases have "an upper limit of around **8 seconds**" and contain "**7±2**" melodic or rhythmic groupings. Sections and larger units span "from 8 seconds up to an hour or more" and rely on comparisons between events "more than 8 seconds" apart. Primitive grouping operates within the echoic window. The reviewer notes that grouping size is "only loosely related" to these memory parameters. — [Chaffin 2002, review of Snyder (UConn PDF)](https://musiclab.uconn.edu/wp-content/uploads/sites/290/2019/03/Chaffin-2002-Review-of-B.-Snyder.pdf)
- **Short-term memory for pitch (Snyder via Chaffin):** echoic memory distinguishes "upward of 1400" pitches, while short-term memory with Western tuning holds "about 90". — [Chaffin 2002](https://musiclab.uconn.edu/wp-content/uploads/sites/290/2019/03/Chaffin-2002-Review-of-B.-Snyder.pdf)
- **The 3-second "subjective present" (Pöppel) is disputed:** Pöppel argues durations up to about 3 s are judged accurately and longer ones underestimated, which he takes to mean two processing modes, with behaviours (e.g. a line of poetry) having roughly 3 s structure. White (2017, Psychological Bulletin) found no clear boundary at 3 s: performance degrades gradually, and natural behavioural segments usually last well over 3 s. White concludes that integration is an "envelope" with "no fixed time limit" that "extends well beyond the three-second mark". — [BPS Research Digest on White 2017](https://bps.org.uk/research-digest/new-review-punctures-myth-now-three-seconds-long); [White 2017 manuscript (Cardiff ORCA)](https://orca.cardiff.ac.uk/98445/1/Peter%20White%20three-second%20moment%20paper%203.pdf)
- **Periodicity window:** periodicity can be detected up to about **5-6 s** (London 2004, secondhand). This matches the idea that a bar or two-bar unit is felt as a cycle while a 4-bar phrase at slow tempo is not. — [Summary of London 2004](https://www.midside.com/pdf/eastman/fall06/th581/london_longuet_temperley.pdf)

### Inferences
- **Phrase-length rule (seconds, not bars):** a melodic phrase (the span between breaths or cadential points) should last **at most about 8 s**, ideally **2-6 s**. It should contain **about 3-9 sub-groups** (motives or rhythmic cells), with about 5-7 as the centre. Convert to bars by tempo:
  - 4/4 at 120 bpm: 1 bar = 2 s, so a 2-bar sub-phrase is 4 s and a 4-bar phrase is 8 s (at the limit). Write 4-bar phrases as 2+2 with an audible breath or cadence at the midpoint.
  - 4/4 at 80 bpm: 1 bar = 3 s, so a 4-bar phrase is 12 s, which exceeds the limit. Split into 2-bar units (6 s), each with its own closure.
  - 3/4 at 120 bpm: 1 bar = 1.5 s, so 4 bars = 6 s (fine) and 8 bars = 12 s (split 4+4).
  - 6/8 at dotted quarter = 80: 1 bar = 1.5 s, so 4 bars = 6 s (fine).
- **Motive-size rule:** a motive (primitive group) should fit inside about 1-3 s and be marked by a rest, a long note or a leap at its end, so that grouping boundaries are clear.
- **Form-level rule:** anything above about 8 s (verse, chorus, section) is understood through recognition and comparison, not as a single perceptual unit. Make its identity depend on a strongly memorable hook motive that recurs, rather than on the whole section's shape. This connects to section 5.
- **Do not hard-code "3 s"** as a perceptual constant. Use the 2-8 s range with soft penalties.

### Gaps
- Snyder's own text was not retrieved. Some commonly quoted Snyder figures, such as event fusion at about 1/16 s (63 ms) and STM of "3-5 s, up to about 8 s", could not be confirmed. The review's "250 ms" echoic figure is lower than other estimates (echoic memory is often given as about 2-4 s for some measures), so this conflict is unresolved.
- No retrieved study measured working-memory span for melodies directly (e.g. how many notes can be held for same/different judgments).

---

## 5. Repetition and exposure: liking, speech-to-song, earworms

### Takeaway
Repetition is central to music: over 90% of listening time is spent on material heard before. Inserting repetition makes even atonal art music better liked and more "musical". Exact repetition increases singing and tapping along. Earworms are slightly faster than other songs and have common overall contours with some unusual intervals. Chart popularity and recency also predict them.

### Cited Findings
- **Huron estimate:** over **90%** of the time people spend listening to music involves passages they have heard before. — [Margulis, "Why repetition can turn almost anything into music", Aeon](https://aeon.co/essays/why-repetition-can-turn-almost-anything-into-music)
- **Margulis lab experiments (summarized by Margulis, without sample sizes):**
  - Excerpts by Berio and Carter with segments re-inserted to create repetition were rated by untrained undergraduates as **more enjoyable, more interesting, and more likely human-composed**.
  - Random note sequences looped **6 times** were later rated **more musical** even when the loops were not explicitly remembered.
  - In a rondo study, **exact repetition** of the refrain led to **more tapping and singing along** than varied refrains.
  - Source: [Margulis, Aeon](https://aeon.co/essays/why-repetition-can-turn-almost-anything-into-music); [University of Arkansas press release](https://news.uark.edu/articles/40396/repetition-can-make-sounds-into-music)
- **Speech-to-song illusion (Deutsch):** a spoken phrase looped "several times" comes to sound sung. — [Margulis, Aeon](https://aeon.co/essays/why-repetition-can-turn-almost-anything-into-music)
- **Mere exposure (Zajonc):** liking increases with repeated exposure even without awareness of it. **Familiar music** activates emotional brain regions more, whether or not it is liked (Pereira et al.). — [Margulis, Aeon](https://aeon.co/essays/why-repetition-can-turn-almost-anything-into-music)
- **Jakubowski, Finkel, Stewart & Müllensiefen (2017, Psychology of Aesthetics, Creativity, and the Arts; online Nov 2016):** about 3,000 people named their frequent earworms (data 2010-2013, pop/rock/rap/R&B). The analysis compared **100 earworm tunes with 100 controls** matched on chart success and recency.
  - The only significant melodic predictor was **common global contour** (estimate 7.08, p = .03). A marginal predictor was **less common gradients between contour turning points** (p = .07), i.e. unusual intervals or leaps.
  - **Tempo:** earworms were faster, **M = 124.1 bpm (SD 28.7)** vs **115.8 bpm (SD 25.4)**, but this was not significant (p = .10).
  - A 3-predictor random forest classified earworms with **62.5%** accuracy.
  - Popularity (p < .001) and recency (p = .011) predicted how often a tune was named.
  - The earlier finding (Williamson & Müllensiefen 2012; Finkel et al. 2010; 58 songs, N = 1,014) that earworms have **longer note durations and smaller intervals** was **not replicated**.
  - The most-named earworms were "Bad Romance", "Can't Get You Out of My Head" and "Don't Stop Believin'".
  - Sources: [Jakubowski et al. full text (Durham repository)](https://durham-repository.worktribe.com/OutputFile/1371487); [press release](https://www.eurekalert.org/news-releases/555535)

### Inferences
- **Repetition is a liking lever, not a flaw:** the engine should repeat. Plan for exact repetition of the hook or chorus (3-4+ times per song) to invite singing along, since exact refrains beat varied ones in the rondo study. Use variation in verses and accompaniment to manage boredom rather than altering the hook itself.
- **Within-hook repetition:** a short motive (1-2 bars, under 4 s) repeated 2-4 times within a phrase (AAB or AABA at motive level) produces fast familiarity. Speech-to-song and the looping effect show that a handful of repetitions (around 6 in Margulis's study) suffices to make material sound "musical".
- **Earworm recipe (weak effects, about 62% classification):** use a familiar global contour (arch, or rise-then-fall as in "Twinkle Twinkle"), add one distinctive interval event (an unexpected leap, or a run of repeated notes), and use a tempo around 120-125 bpm. Do not treat "small intervals and long notes" as a rule, because it did not replicate.
- **Balance with groove:** repeated hooks pair naturally with medium syncopation (section 3). Repetition gives predictability, and syncopation gives "resistance".

### Gaps
- No source retrieved quantified an *optimal* number of chorus repetitions, or an inverted U between within-song repetition and liking (the overexposure/satiation point). The Berlyne-style "wear-out" across listening sessions was not covered.
- Primary Margulis studies (sample sizes, effect sizes; e.g. Margulis 2013 "Aesthetic responses to repetition in unfamiliar music", Empirical Studies of the Arts) were not retrieved. Only her own summaries are cited.
- Margulis's *On Repeat* (2014) book was not accessed directly.
- Speech-to-song illusion parameters (Deutsch et al. 2011: about 10 repetitions; Tierney et al. 2013) were not verified here.
- Huron's *Sweet Anticipation* (ITPRA model, predictability and pleasure) was not retrieved.
