# Classical and baroque harmonic / voice-leading patterns taken over by pop (with Queen and ABBA) — design input for a rule-based songwriting engine

Reading notes on reliability, used throughout:
- **[A]** = peer-reviewed article, scholarly book, thesis, or open textbook written by music theorists.
- **[P]** = primary statement by the musician (interview quote, as relayed by the cited page).
- **[T]** = teaching material from an exam board or theorist's blog (analytical, not peer-reviewed).
- **[W]** = Wikipedia or journalism summarising other sources (secondary; check before relying on it).
- Scale degrees are written 1-7; "b7" = lowered seventh; "#4" = raised fourth. Bass and melody lines are aligned stage by stage.
- No lyrics are reproduced.

---

## Key question 1 — Which galant/baroque schemata appear in pop, per published analysis, and how are they defined in scale degrees for bass and melody?

### Takeaway
The galant schemata are precisely defined as paired bass and melody scale-degree lines (table below), so they can be coded directly; but the published literature I could verify documents only a handful of the *baroque bass patterns* in pop (lament bass, circle-of-fifths sequence, Pachelbel/Romanesca-type bass, stepwise descending bass, cadential 6/4), not the Gjerdingen galant set by name. I found no published count of Prinner, Meyer, Fonte or Monte occurrences in pop songs.

### Cited Findings

**A. Scale-degree definitions of the galant schemata (codeable)**

Source for the table: Open Music Theory, "Galant schemas – summary" [A, open textbook following Gjerdingen 2007] — [Open Music Theory, Galant Schemas Summary](https://viva.pressbooks.pub/openmusictheory/chapter/galant-schemas-summary/). Cross-checked against [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata) [W]; disagreements are listed after the table.

| Schema | Usual place in phrase | Melody degrees | Bass degrees | Figured bass (intervals above bass) |
|---|---|---|---|---|
| Romanesca | Opening | 1-5-1-1 | 1-7-6-3 | 5, 6, 5, 6 |
| Do-Re-Mi | Opening | 1-2-3 | 1-7-1 (variant 1-5-1) | 5, 6, 5 |
| Sol-Fa-Mi | Opening | 5-4-4-3 | 1-2-7-1 | 5, 5, 6/5, 5 |
| Meyer | Opening | 1-7-4-3 | 1-2-7-1 | 5, 6/4/3, 6/5, 5 |
| Aprile | Opening | 1-7-2-1 | 1-2-7-1 | 5, 6/4/3, 6/5, 5 |
| Jupiter | Opening | 1-2-4-3 | 1-7-5-1 | 5, 6, 5, 5 |
| Pastorella | Opening | 3-2-4-3 | 1-5-5-1 | 5, 5, 7, 5 |
| Prinner | Answer to an opening | 6-5-4-3 | 4-3-2-1 (optional 5 inserted before 1) | 5, 6, 7-6, 5 |
| Modulating Prinner | Transition to dominant key | 3-2-1-7 | 8-7-6-5 | 5, 6, 7-#6, 5 |
| Fonte | Sequence, step DOWN (minor then major) | 5-4-4-3 (i.e. 4-3 in ii, then 4-3 in I) | #1-2-7-1 (i.e. 7-1 in ii, then 7-1 in I) | 6/5, 5, 6/5, 5 |
| Monte | Sequence, step UP | see conflict note below | 3-4-#4-5 (i.e. 7-1 in IV, then 7-1 in V) | 6, 5, 6, 5 (or 6/5, 5) |
| Ponte | Dominant pedal, "bridge" | 5-7-2 | 5-5-5 (pedal) | 5, 7, 7 |
| Fenaroli | Pre-cadential | 4-3-7-1 | 7-1-2-3 | 6/5, 5, 6/5, 6 |
| Indugio | Pre-cadential (prepares half cadence) | 2-4-6-1-7 | 4-4-4-#4-5 | 6/5 ×4, then 5 |
| Passo indietro | Pre-cadential | 7-1 | 4-3 | 6/4/2, 6 |
| Comma | Pre-cadential | 4-3 | 7-1 | 6/5, 5 |
| Converging cadence | Half cadence | 3-2-1-7 | 3-4-#4-5 | 6, 6/5, 6/5, 5 |
| Deceptive cadence | Cadence avoided | 1-2-2-1 | 3-4-5-6 | 6, 6/5, 5, 5 |
| Evaded cadence | Cadence avoided | 1-2-2-1 | 3-4-5-3 (detailed table) | 6, 6/5, 5, 6 |
| Cadenza semplice | Full cadence | 1-2-2-1 | 3-4-5-1 | 6, 6/5, 5, 5 |
| Cadenza composta | Full cadence with 6/4 | 1-2-3-2-1 | 3-4-5-5-1 | 6, 6/5, 6/4, 7, 5 |
| Cadenza doppia | Full cadence, long dominant | 4-3-2-2-1 | 5-5-5-5-1 | 5, 6/4, 4, 3, 5 |
| Quiescenza | After the cadence, tonic pedal | b7-6-7-1 | 1-1-1-1 | b7, 6/4, 7/4/2, 5 |

- The Open Music Theory source sorts schemata into five positions in the phrase: Opening, Answer/Process/Transition, Pre-cadential, Cadence, Post-cadential. — [Open Music Theory, Galant Schemas Summary](https://viva.pressbooks.pub/openmusictheory/chapter/galant-schemas-summary/)
- Conflict on the Monte melody: Open Music Theory's summary gives a compound line "1-b7-6-2-1-7"; Wikipedia gives "5-4-3, then 5-4-3 one step higher" over bass "7-1, then 7-1 one step higher". Both describe the same thing (a two-chord unit, dominant-to-local-tonic, repeated a step up: first in IV, then in V). — [Open Music Theory](https://viva.pressbooks.pub/openmusictheory/chapter/galant-schemas-summary/); [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata)
- Conflict on the Fonte: Wikipedia gives melody "4-3, then 4-3 one step lower" over bass "7-1, then 7-1 one step lower", first unit in the minor supertonic, second in the major tonic; Open Music Theory writes the same thing as global degrees (bass #1-2-7-1, melody 5-4-4-3). — [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata)
- Prinner detail: an optional bass 5 may be inserted in the third event (4-3-2-5-1) for a stronger close, with melody 6-5-4-(2)-3. — [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata)
- The Meyer family shares one bass (1-2 … 7-1) and differs only in melody: Meyer 1-7 … 4-3; Jupiter 1-2 … 4-3; Pastorella 3-2 … 4-3; Aprile 1-7 … 2-1; Sol-Fa-Mi 5-4 … 4-3. — [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata)
- Romanesca has leaping, stepwise and "galant" (hybrid) variants; the source gives 1-7-6-3 as the galant bass. — [Wikipedia, Galant Schemata](https://en.wikipedia.org/wiki/Galant_Schemata)
- Recent research on how schemata are ordered and melodically organised exists (Rabinovitch & Carter-Enyi, Music Theory Online 30.1, 2024), and Gjerdingen & Bourne have a Music Theory Online article on schema theory (21.2, 2015); I did not read their content in this session. — [MTO 30.1 Rabinovitch](https://mtosmt.org/issues/mto.24.30.1/mto.24.30.1.rabinovitch_carter-enyi.html); [MTO 21.2 Gjerdingen & Bourne](https://mtosmt.org/issues/mto.15.21.2/gjerdingen_bourne_usage.php)

**B. Baroque bass patterns documented in pop, with definitions and named examples**

*Lament bass (descending minor tetrachord)*
- Definition: bass 1-b7-b6-5 ("do-te-le-sol"), "most typically harmonized by I-bVII-bVI-V"; the chord over b7 can vary (e.g. a III chord in second inversion). Pop examples given: Dire Straits "Sultans of Swing" (1978); Muse "Thoughts of a Dying Atheist" (2004). [A] — [Open Music Theory, Classical Schemas (in a Pop Context), Hughes & Shaffer](https://viva.pressbooks.pub/openmusictheory/chapter/classical-schemas/)
- The lament bass is a ground bass descending a perfect fourth from tonic to dominant with each step harmonised; the diatonic form is the "Phrygian tetrachord"; the chromatic form fills in all semitones ("chromatic fourth"); associated with 17th-century Venetian opera and Purcell. [W] — [Lament bass explained](https://everything.explained.today/Lament_bass)
- Further pop examples from a theorist's teaching blog: Ray Charles "Hit the Road Jack" (i-bVII-bVI-V), The Turtles "Happy Together", The Beach Boys "Good Vibrations" (verse). Classical model named: Purcell, "Dido's Lament" (1689). [T] — [Ethan Hein, Identifying harmonized basslines](https://ethanhein.substack.com/p/identifying-harmonized-basslines)
- Chromatic versions: bass 1-b7-6-b6-5, harmonised either as changing chords or as one minor chord over a moving bass ("line cliché": Cm, Cm/Bb, Cm/A, Cm/Ab, Cm/G); Beatles examples listed: "Eleanor Rigby", "While My Guitar Gently Weeps", "Dear Prudence", "Magical Mystery Tour", "Lucy in the Sky with Diamonds". Fully chromatic 1-7-b7-6-b6-5: Beatles "Michelle", "Something", "Cry Baby Cry", "I Me Mine", "Fixing a Hole", "And Your Bird Can Sing"; David Bowie "Life on Mars?" [T] — [Ethan Hein, Identifying harmonized basslines](https://ethanhein.substack.com/p/identifying-harmonized-basslines)

*Circle-of-fifths (descending-fifth) sequence*
- Definition: at least four chords whose roots descend by perfect fifth; often starts on i and ends on the relative major (VII-III heard as V-I of the relative major); need not start on tonic; a chromatic variant makes each pair an applied ii-V of the next. Pop examples: Aqua "Barbie Girl" (1997); Muse "Thoughts of a Dying Atheist" (verse: lament followed by circle of fifths leading to a chorus in the relative major); Radiohead "You and Whose Army?" [A] — [Open Music Theory, Classical Schemas (in a Pop Context)](https://viva.pressbooks.pub/openmusictheory/chapter/classical-schemas/)
- Queen's "Killer Queen" contains a circle-of-fifths passage at bars 20-21 (chorus), reused as the descending chord pattern of the guitar solo at bars 44-47. [T] — [Pearson Edexcel GCSE set-work guide, Killer Queen](https://qualifications.pearson.com/content/dam/pdf/GCSE/Music/2016/teaching-and-learning-materials/Killer_Queen_set_work_suport_guide.pdf)

*Stepwise descending major-scale bass (rule-of-the-octave-like descent)*
- Bass 1-7-6-5-4-3-2-1 with chords in inversion: Procol Harum "A Whiter Shade of Pale" (1967), David Bowie "Changes" (chorus), Billy Joel "Piano Man" (verse), Jackson 5 "I'll Be There" (verse); inversion-based partial descents in Simon & Garfunkel "The 59th Street Bridge Song" and Elton John "Rocket Man". [T] — [Ethan Hein, Identifying harmonized basslines](https://ethanhein.substack.com/p/identifying-harmonized-basslines)
- Cadential 6/4 (the "cadenza composta" bass 5-5-1 with 6/4 then 5/3) is "occasionally" found in pop; example Coldplay "Til Kingdom Come" (2005). [T] — [Ethan Hein, Identifying harmonized basslines](https://ethanhein.substack.com/p/identifying-harmonized-basslines)

*Pachelbel / Romanesca-type bass*
- Wikipedia's list of Pachelbel-derived pop describes the Canon's harmony as a repeated bass and chord sequence, "similar to the romanesca" and to I-V-vi-IV. Songs listed with a reference each: Bee Gees "Spicks and Specks" (1966; bass and chords "nearly identical"), Aphrodite's Child "Rain and Tears" (1968), Pop-Tops "Oh Lord, Why Lord" (1968), Ralph McTell "Streets of London" (1969), Original Caste "One Tin Soldier" (1969), Moody Blues "Isn't Life Strange" (1972), Bob Marley "No Woman, No Cry" (1974), Village People / Pet Shop Boys "Go West" (1979/1993), Ozzy Osbourne "Goodbye to Romance" (1980), "I Dreamed a Dream" (Les Misérables, 1980), Kylie Minogue "I Should Be So Lucky" (1987), The Farm "All Together Now" (1990), Aerosmith "Cryin'" (1993), Green Day "Basket Case" (1994; one chord altered), Blues Traveler "Hook" (1994), Coolio "C U When U Get There" (1997), Vitamin C "Graduation (Friends Forever)" (2000), My Chemical Romance "Welcome to the Black Parade" (2006), Vampire Weekend "Step" (2013), Maroon 5 "Memories" (2019), among about 30 entries. [W] — [Wikipedia, List of variations on Pachelbel's Canon](https://en.wikipedia.org/wiki/List_of_variations_on_Pachelbel%27s_Canon)
- Producer Pete Waterman called the Canon "almost the godfather of pop music" (BBC News, 7 October 2002), and said "I Should Be So Lucky" was inspired by it. [P via W] — [Wikipedia, List of variations on Pachelbel's Canon](https://en.wikipedia.org/wiki/List_of_variations_on_Pachelbel%27s_Canon)

**C. Other documented classical-to-pop borrowings (direct quotation rather than schema)**
- Billy Joel "This Night" (1984): chorus is based on the second movement of Beethoven's "Pathétique" sonata; Beethoven is credited as co-writer ("L. v. Beethoven") on the sleeve. [W] — [Wikipedia, This Night](https://en.wikipedia.org/wiki/This_Night_(Billy_Joel_song))
- Eric Carmen "All by Myself" (1975): verse melody adapted from the second movement of Rachmaninoff's Piano Concerto No. 2; "Never Gonna Fall in Love Again" draws on the third movement of Rachmaninoff's Symphony No. 2; the Rachmaninoff estate receives 12 percent of royalties on both songs, because the music was still in copyright outside the US. [W, citing Carmen interviews] — [Wikipedia, All by Myself](https://en.wikipedia.org/wiki/All_by_Myself)
- George Martin studied composition, conducting and orchestration at the Guildhall School and played oboe; he wrote the string quartet for "Yesterday" (1965); for "Eleanor Rigby" McCartney asked for something like Vivaldi and Martin modelled the staccato strings on Bernard Herrmann's "Psycho" score; the "Penny Lane" piccolo trumpet solo was inspired by Bach's Brandenburg Concerto No. 2; "All You Need Is Love" quotes Bach's Invention No. 8 in F in its fade-out. [W, BBC Music Magazine] — [classical-music.com, George Martin](https://www.classical-music.com/features/artists/george-martin)

### Inferences
- For coding, each galant schema reduces to a small record: `{name, position_in_phrase, bass_degrees[], melody_degrees[], figures[]}` with 2-5 stages. The melody and bass lines move mostly in parallel tenths/sixths or in contrary motion; every stage pair above is consonant (third, fifth, sixth, octave) or a prepared seventh. This two-voice frame is exactly "counterpoint between voice and bass", which is the feature the engine wants.
- The Meyer family is the most reusable for a song engine: one bass (1-2 … 7-1, i.e. I – V4/3 … V6/5 – I) accepts five different melodies. It is a ready-made "open half / closed half" (question/answer) phrase pair.
- Fonte (down a step, minor then major) and Monte (up a step, IV then V) are the galant forms of the pop "sequence": a two-chord cell (local dominant to local tonic) transposed by step. They are natural material for a pre-chorus or bridge; Monte raises tension, Fonte relaxes it.
- The pop "Pachelbel" loop I-V-vi-iii-IV-I-IV-V is, in its first four chords, the leaping Romanesca (bass 1-5-6-3); the galant Romanesca bass 1-7-6-3 is the same harmony with the second chord in first inversion (V6). The pop "descending major bass" 1-7-6-5-4-3 (A Whiter Shade of Pale, Piano Man) is the stepwise Romanesca. So the three pop habits are variants of one schema and can share one rule with a "bass shape" switch (leaping / stepwise / hybrid).
- The Prinner (bass 4-3-2-1 under melody 6-5-4-3 in parallel tenths) corresponds to the pop progression IV – I6 – ii(7)/V – I, a common "answer" after a tonic opening. I found no published source naming it in pop, so this mapping is my own reading.
- The published pop-pedagogy sources document the *bass-line* patterns far better than the *melody* half of the schemata. The melody degrees in the galant table are the part the engine would be adding beyond what pop analyses usually record.

### Gaps
- I found **no published count** of galant schemata (Prinner, Meyer, Fonte, Monte, etc.) in a pop corpus. The only counts found are for chord progressions in general (Key question 3).
- I could not open Gjerdingen's book ("Music in the Galant Style", Oxford University Press, 2007) or its companion site; the degree table comes from Open Music Theory and Wikipedia, both of which follow Gjerdingen. The report writer should treat the table as "Gjerdingen as transmitted by a textbook".
- Rule of the octave and partimento practice: no source fetched in this session gave the standard harmonisation in figures. From general knowledge only (unverified here): ascending bass 1-2-3-4-5-6-7-8 takes 5/3, 6/4/3, 6, 6/5, 5/3, 6, 6/5, 5/3; descending 8-7-6-5-4-3-2-1 takes 5/3, 6, #6/4/3, 5/3, 6/4/2, 6, 6/4/3, 5/3. Verify against a partimento source (e.g. Sanguinetti, "The Art of Partimento", or Gjerdingen's "Monuments of Partimenti" site) before coding.
- Books known to treat pop schemata but **not verified in this session**: Christopher Doll, "Hearing Harmony" (2017); David Temperley, "The Musical Language of Rock" (2018); Drew Nobile, "Form as Harmony in Rock Music" (2020); Walter Everett, "The Foundations of Rock" (2009) and "Making Sense of Rock's Tonal Systems" (Music Theory Online, 2004); Philip Tagg, "Everyday Tonality". These probably contain the named-example evidence that is missing here.
- Wikipedia pages for "A Whiter Shade of Pale" (Bach: usually said to echo the Air from Orchestral Suite No. 3 and the cantata "Wachet auf"), Barry Manilow's "Could It Be Magic" (Chopin, Prelude in C minor Op. 28 No. 20) and Elvis Presley's "Can't Help Falling in Love" (melody from Martini's "Plaisir d'amour", 1784) could not be fetched; those three attributions are widely repeated but are **unsourced in these notes**.
- Beatles "In My Life" (baroque-style piano solo recorded at half speed) and "Because" (Lennon: Moonlight Sonata chords reversed) were not verified from a fetched source.

---

## Key question 2 — What specific classical devices are documented in Queen and ABBA songs, and what have the musicians and musicologists said?

### Takeaway
For Queen there is solid scholarly work (Braae 2015 and 2016; McLeod 2001) and bar-level teaching analysis of "Killer Queen", documenting frequent modulation by fourth/fifth, circle-of-fifths passages, chromatic descending lines, and multi-voice counterpoint; Mercury himself called "Bohemian Rhapsody" a "mock opera" and "The Millionaire Waltz" "a Strauss waltz". For ABBA, what I could verify is biographical and self-reported (folk accordion and schlager upbringing, nightly Bach listening, Nordic "melancholy" from folk, Sibelius and Grieg), and I found no accessible peer-reviewed bar-level harmonic analysis of the named ABBA songs.

### Cited Findings

**Queen — scholarship**
- Nick Braae, "Sonic Patterns and Compositional Strategies in Queen's 'Bohemian Rhapsody'", Twentieth-Century Music 12/2 (2015): 173-196. Argues the song's form and harmony reflect the band's recurring "compositional strategies" and its textures reflect their "sonic patterns"; it is the first Queen song to present all major elements of the band's idiolect. Its reference list includes Jack Boss's paper on hidden repetition and classical form in the song. [A; abstract only read] — [Cambridge, Braae 2015](https://www.cambridge.org/core/journals/twentieth-century-music/article/sonic-patterns-and-compositional-strategies-in-queens-bohemian-rhapsody/489FEB6E684A86A6634183D71853F93E)
- Nick Braae, "A Kind of Magic: Identifying and Analysing Queen's Idiolect, 1973-1980", PhD thesis, University of Waikato, 2016: analyses 90 songs on eight studio albums across nine musical elements; separates "compositional strategies" (structural traits realised differently per song) from "sonic patterns" (arrangement and production traits realised the same way); names the stylistic sources as hard rock, progressive rock, glam rock, cabaret, 1960s pop and 1930s American popular song (the abstract does **not** name classical music). Chapter 4 holds the harmonic and formal findings. [A; abstract only read] — [Waikato Research Commons, Braae 2016](https://researchcommons.waikato.ac.nz/entities/publication/f5fdeeca-fcfe-43a2-89c2-5ed903cefc31); full PDF (47 MB): [thesis.pdf](https://researchcommons.waikato.ac.nz/bitstreams/b3f9efd0-dea7-4d1b-a35f-72d03f0a121a/download)
- Ken McLeod, "Bohemian Rhapsodies: Operatic Influences on Rock Music", Popular Music 20/2 (2001): 189-203. Examines operatic vocality and borrowing in Queen, Nina Hagen, Klaus Nomi and Malcolm McLaren; argues opera-rock fusions transgress musical conventions and mirror the crossing of cultural boundaries of sexuality, gender and class. [A; abstract only read] — [Cambridge, McLeod 2001](https://www.cambridge.org/core/journals/popular-music/article/abs/bohemian-rhapsodies-operatic-influences-on-rock-music/4AC69CE9CA8052AEF542E531709489C4)

**Queen — "Bohemian Rhapsody" (1975)** [W unless marked]
- Key plan: a cappella introduction in B-flat major (V-I cadence F7-B-flat establishes key; one 5/4 bar); ballad starts in B-flat and tonicises E-flat via B-flat7-E-flat; a descending chromatic run mid-verse leads to E-flat (up a fourth); guitar solo in E-flat; a descending bass line sets up the move to A major for the opera section; opera section ends on a block B-flat chord; hard-rock section; coda uses ascending B-flat Mixolydian octaves back to E-flat, touches C minor, ends in E-flat with a shift to F just before the final note. — [Wikipedia, Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody)
- Devices named: "chromatic side-slipping" in the first verse; descending chromatic bass as modulation device; Mixolydian mode in the coda; about 180 vocal overdubs in places. — [Wikipedia, Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody)
- Mercury called it a "mock opera": "It was basically three songs that I wanted to put out, and I just put the three together"; he said he did not know much about opera, only certain pieces. [P via W] — [Wikipedia, Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody)
- Brian May on the guitar solo: he wanted "a little tune that would be a counterpart to the main melody; I didn't just want to play the melody", and "the fingers tend to be predictable unless being led by the brain" (i.e. he composes solos by singing them, not by hand habit). [P via W] — [Wikipedia, Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody)
- Musicologist Judith Peraino: the song follows an "operatic logic", multi-tracked choruses alternating with aria-like solos. Tom Service compared its unity across diverse styles to classical symphonic works; critics compare it with 19th-century rhapsodic works. Earlier embryos of the style: "My Fairy King" (1973), "The March of the Black Queen" (1974). — [Wikipedia, Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody)

**Queen — "Killer Queen" (1974)** [T: Pearson Edexcel GCSE set-work guide]
- Home key E-flat major, but opens on C minor and shifts quickly, so "tonality is often ambiguous"; passing modulations are confirmed by perfect cadences and then followed by parallel shifts to a new key.
- Chorus (bars 14-22): cadences into B-flat major, moves to D minor, then C major, then travels along a circle of fifths (bars 20-21) before sliding back to B-flat.
- Chromatic/descending devices: descending sequence in guitar (bar 7); inner chromatic descending pattern (bars 31-33); pedal (bars 27-30); extended chord F11 (bar 47); mostly root position with some first and second inversions.
- Melody: mainly syllabic; starts conjunct with small leaps of a third or fourth, then mixes stepwise motion with "wide angular leaps", often a rising major sixth (bars 6-7); an octave leap at bar 62; the climax (bar 67) has the voices very high in four parts.
- Phrase lengths are irregular: verse phrase 4 bars then 5 (extended by a 6/8 bar); chorus 8 bars as 5 + 3.
- Texture: homophonic with imitation and layering; guitars in thirds; imitation between guitar parts in the solo; three-part guitar texture; antiphonal exchange between voices and band.
- All from — [Pearson, Killer Queen set work support guide](https://qualifications.pearson.com/content/dam/pdf/GCSE/Music/2016/teaching-and-learning-materials/Killer_Queen_set_work_suport_guide.pdf)
- Wikipedia adds "elaborate four-part harmonies", a multitracked "bell effect" guitar solo in which, per May, "each part has its own voice", and two bass lines at one point, one a descending run; AllMusic says it "recalls the cabaret songs of yesteryear". May called it the song that "best summed up our kind of music". [W] — [Wikipedia, Killer Queen](https://en.wikipedia.org/wiki/Killer_Queen)

**Queen — "Somebody to Love" (1976)** [W]
- In A-flat major; written by Mercury at the piano; modelled on gospel (Aretha Franklin) rather than the "English choir" style of "Bohemian Rhapsody"; Mercury, May and Taylor multitracked to imitate a 100-voice choir; harmony parts span about F2 to A-flat5; Roger Taylor: "We tried to keep the track in a loose, gospel-type feel". — [Wikipedia, Somebody to Love](https://en.wikipedia.org/wiki/Somebody_to_Love_(Queen_song))
- Melodic-peak note: the high note at the top of the building line on the studio recording was not Mercury's original melody; live he held sustained A-flat4s. — [Wikipedia, Somebody to Love](https://en.wikipedia.org/wiki/Somebody_to_Love_(Queen_song))

**Queen — "The Millionaire Waltz" (1976)** [P, quotes collected by a fan archive with dated sources]
- Mercury (Circus, 31 January 1977): "this track is something that Queen has never done before — a Strauss waltz!"; "Brian has orchestrated it fully with guitars… He goes from tubas to piccolos to cellos."
- Mercury (1977): "We set it out as though we'd hired an orchestra to come into the studio."
- May (Guitar Player, January 1983): "there must be about 18 or 20 guitar tracks"; (Capital Radio, May 1977) "a complete sort of orchestra, with all its sections and choirs"; (Mojo, August 1999) "Sometimes there are ten different things going on at once."
- Taylor (Circus, 1977): "comparable to Bohemian Rhapsody, in the sense that it's an arranged, intricate number."
- All from — [queensongs.info, quotes on The Millionaire Waltz](https://www.queensongs.info/quotes/queen/a-day-at-the-races/the-millionaire-waltz)

**ABBA — the musicians' own account**
- Benny Andersson's father and grandfather played accordion; at six he was given one and introduced to Swedish folk music, traditional music and schlager; he taught himself piano from age ten; his first records were by schlager singer Caterina Valente and by Elvis Presley; honorary doctorate in 2008 for contribution to the Swedish folk tradition; 1987 solo album with the Orsa Spelmän fiddlers. [W] — [Wikipedia, Benny Andersson](https://en.wikipedia.org/wiki/Benny_Andersson)
- In his 2010 Rock and Roll Hall of Fame speech Andersson attributed the melancholy in Swedish pop to Russian folk songs, Sibelius, Grieg and the long winters. [W] — [Wikipedia, Benny Andersson](https://en.wikipedia.org/wiki/Benny_Andersson)
- Andersson, NPR interview (May 2015, as relayed): a "melancholy belt" above the 59th latitude, linked to Swedish folk, Russian folk, Sibelius, Grieg, and "some of the harmonies" of the two female voices. [P via secondary] — [Inroads Journal, "Thank You for the Music", H. Milner 2022](https://inroadsjournal.ca/thank-you-for-the-music/)
- Andersson to Classic FM (3 September 2021): "I only listen to classical music now. I listen to Bach every night"; on Bach: "He has a connection to something that no one else has had"; on Rossini overtures: "It has a pulse, rhythm, it has good melodies." [P] — [Classic FM, Benny Andersson](https://classicfm.com/music-news/videos/benny-andersson-abba)

**ABBA — song-level facts** [W]
- "The Winner Takes It All" (1980): ballad in G-flat major; first tried as an up-tempo song with constant beat, judged "much too stiff and metrical"; Andersson then proposed a French chanson-style arrangement "with a descending piano line and a looser structure"; Andersson said the idea came "from old ideas, from old small musical pieces"; string arrangement by Rutger Gunnarsson. — [Wikipedia, The Winner Takes It All](https://en.wikipedia.org/wiki/The_Winner_Takes_It_All)
- "Chiquitita" (1979): genre tags pop / soft rock / schlager; the revised arrangement was influenced by Simon & Garfunkel's "El Condor Pasa"; Pitchfork lists it among the ABBA songs with the strongest schlager influence; solo voice for about the first minute before the second voice joins in harmony. — [Wikipedia, Chiquitita](https://en.wikipedia.org/wiki/Chiquitita)
- "Thank You for the Music" (1977): first recorded with a "jazzy cabaret feel" in the style of Doris Day; later re-arranged on the same melody. — [Wikipedia, Thank You for the Music](https://en.wikipedia.org/wiki/Thank_You_for_the_Music)
- A non-specialist essay claims ABBA's arrangements are "highly complex" and that the bitter-sweet harmony comes from the soprano/mezzo pairing; this is opinion, not analysis. — [Inroads Journal, Milner 2022](https://inroadsjournal.ca/thank-you-for-the-music/)

### Inferences
- Devices documented for Queen that translate directly into rules: (1) section-to-section key change by a fourth or fifth, prepared by turning the old tonic into a dominant seventh (B-flat7 → E-flat); (2) a chromatic descending bass used as the *connector* into a new key; (3) a short circle-of-fifths run inside the chorus that leaves and returns to the key; (4) each "visited" key confirmed by its own V-I; (5) irregular phrase lengths (4+5, 5+3) made by inserting a half-bar; (6) a counter-melody that answers rather than doubles the tune (May's stated method); (7) melody that mixes stepwise motion with a signature wide leap (rising sixth, octave) and saves the highest notes for the final verse/climax.
- The "Killer Queen" chorus tonal path (B-flat → D minor → C → fifths → B-flat) behaves like a Fonte/Monte-style sequence of short tonicisations. That is my reading; the exam-board guide does not use schema terms.
- Mercury's own labels ("mock opera", "a Strauss waltz") show the classical element in Queen is partly deliberate pastiche of *genres and textures* (opera chorus, waltz orchestration), layered over harmonic habits that Braae traces mostly to cabaret, 1930s popular song and 1960s pop rather than to the classical canon. A report should not overstate "Queen = classical harmony"; the scholarly abstract available does not say that.
- For ABBA, the verifiable through-line is folk and schlager (accordion repertoire: waltzes, polkas, stepwise sequential melodies over I-IV-V with secondary dominants) plus Andersson's later-declared love of Bach. The claim that specific ABBA songs use baroque sequence or counterpoint is common in commentary but I could not tie it to a peer-reviewed analysis in this session; treat it as plausible but undocumented here.
- The one arranging fact that is documented for "The Winner Takes It All" — a descending piano line over a loosened metre — fits the "descending bass/inner line under a repeated melodic cell" family from Key question 1.

### Gaps
- Braae's and McLeod's detailed findings (which chords, which modulations, counts across 90 songs) are behind paywalls or in a 47 MB PDF that I did not read; only abstracts were available. The thesis PDF is open access and is the single best next source for Queen rules.
- No verified source in this session for: Mercury's piano training (commonly reported as reaching Grade IV piano), "Bohemian Rhapsody" opera-section chord-by-chord analysis, or Brian May's statements about harmony stacking in thirds/sixths.
- ABBA scholarship I know exists but could **not verify or open**: Per F. Broman, "'When All Is Said and Done': Swedes, ABBA, and the Politics of Kitsch" (Journal of Popular Music Studies, 2005); Philip Tagg, "Fernando the Flute" (book-length analysis of ABBA's "Fernando"); Carl Magnus Palm, "ABBA: The Complete Recording Sessions" and "Bright Lights Dark Shadows" (session facts and composer quotes). None of the named songs' keys, chord progressions, sequences, counter-melodies or key changes ("Dancing Queen", "I Have a Dream", "Chiquitita", "Thank You for the Music") were found in a citable analytical source.
- The widely repeated claims that "Dancing Queen" has a baroque-style descending piano figure, that "Chiquitita" ends with a classical-style piano coda, and that "I Have a Dream" modulates up for the final chorus are **not sourced** in these notes.
- No Rick Beato-type secondary analyses were consulted.

---

## Key question 3 — Corpus studies comparing classical and pop harmony: what is shared and what differs?

### Takeaway
Corpus counts agree that classical and rock share the same top three chords (I, IV, V) and a tonic share near one third, but differ sharply in *direction*: classical harmony is strongly asymmetric (descending-fifth root motion about three to four times as common as ascending-fifth; V→I about five times IV→I), while rock is nearly symmetric (ascending and descending fourths about equal; IV→I more common than V→I). Rock also uses far more root-position chords and bVII.

### Cited Findings

**Rock: de Clercq & Temperley, "A corpus analysis of rock harmony", Popular Music 30/1 (2011)** — [PDF](https://rockcorpus.midside.com/2011_paper/declercq_temperley_2011.pdf)
- Corpus: 100 songs from Rolling Stone's "500 Greatest Songs" (20 per decade, 1950s-1990s), 99 analysed; about 9,300 chords per analyst; two analysts agreed on 92.4% of chromatic relative roots.
- Chord-root share: I 32.8%, IV 22.6%, V 16.3%, bVII 8.1%, VI 7.2%, bVI 4.0%, II 3.6%, bIII 2.6%, III 1.9%. Top five roots = 87%.
- Chord quality: 75.8% major, 23.4% minor, 0.7% diminished. Inversion: 94.1% root position (versus about 60% in common-practice music, per the paper).
- Into the tonic: IV→I 1,162; V→I 788; bVII→I 386; bVI→I 208; VI→I 144; II→I 120.
- Out of the tonic: I→IV 1,052; I→V 710; I→bVII 470; I→VI 302; I→II 132.
- Root motion (counts): up a fourth 2,266 vs down a fourth 2,220; up a major second 1,384 vs down 1,386; up a minor third 410 vs down 454; up a major third 326 vs down 412; tritone 20. The paper's point: common-practice harmony favours ascending fourths (= descending fifths), descending thirds and ascending seconds; the rock corpus shows no such asymmetry.
- Three-chord cadences ending on I: IV-V-I 352; V-IV-I 292; bVII-IV-I 146; VI-IV-I 126; bVII-bVI-I 103; bIII-bVI-I 66; II-V-I 63.
- By decade: 1950s I/IV/V together over 95% of chords (42.3 / 32.1 / 22.1%); from the 1960s bVII enters (about 8-11%); flat-side chords (bIII, bVI) rise after the 1960s; 1990s VI reaches 10.0%.

**Common practice: Temperley, "A Statistical Analysis of Tonal Harmony" (Kostka-Payne corpus)** — [davidtemperley.com/kp-stats](https://davidtemperley.com/kp-stats/)
- Corpus: 46 excerpts from the Kostka-Payne harmony textbook, 919 chords (18th-19th century).
- Chord-root share: I 34.6%, V 23.3%, II 11.3%, IV 7.6%, VI 5.4%, VII 3.8%, bVI 3.7%, III 2.3%, bVII 0.7%.
- Transitions: V→I 167 (84.8% of moves from V); I→V 116; II→V 45; IV→I 32; IV→V 11. After recoding cadential 6/4 as V: II→V 62 (about 63% of moves from II), IV→I 27, IV→V 16.
- Root motion: up a fourth (descending fifth) 308 vs down a fourth (ascending fifth) 167; seconds ascending 127 vs descending 65; thirds descending 64 vs ascending 32.

**Bach and Palestrina: Tymoczko, "Root Motion, Function, Scale-Degree"** — [PDF](https://dmitri.mycpanel.princeton.edu/files/publications/tonaltheories.pdf)
- Bach chorales (5,240 progressions, crude MIDI survey): fifth down 35% vs up 10%; second up 26% vs down 6%; third down 13% vs up 10%. 74% of progressions are of the "dominant" type (fifth down, third down, second up).
- Palestrina (1,159 progressions): fifth down 28% vs up 14%; third down 22% vs up 13%; second up 15% vs down 8%; 65% "dominant" type — so the asymmetry predates functional tonality.
- The asymmetry belongs to particular chords, not to all: share of "dominant-type" departures by chord — V 94%, vii° 91%, ii 81%, iii 68%, IV 66%, vi 58%, I 56%.
- A simple generating table that approximates Bach's major-mode practice (probability of next chord): I → V 41%, IV 30%, ii 14%, vi 11%, vii° 3%, iii 1%; ii → V 61%, vii° 31%, vi 8%; iii → IV 86%, vi 14%; IV → V 35%, I 29%, vii° 22%, ii 14%; V → I 86%, vi 14%; vi → ii 31%, V 29%, IV 25%, vii° 15%; vii° → I 100%.
- Of the "backward" (subdominant-type) progressions in 30 Bach chorales, three account for 87%: I-V (63%), IV-I (16%), V-IV6 (8%).

**Function models: White & Quinn, "Chord Context and Harmonic Function in Tonal Music", Music Theory Spectrum 40/2 (2018): 314-35** — [PDF](https://static1.squarespace.com/static/545183b3e4b0f4d5bea12a07/t/5c9d08d2e79c70d789ae3e9a/1553795368989/mty021+(1).pdf)
- Method: hidden Markov models learned from chord order alone on three corpora: Kostka-Payne, Bach chorales, and the McGill Billboard corpus (649 songs, 64,591 chords after de-duplication).
- Common practice: V is the most common non-tonic chord and serves both as the tonic's opposite pole and as the chord that leads to the tonic. Bach chorales with three states reproduce tonic → pre-dominant → dominant → tonic.
- Billboard pop: I about 23.5%, IV about 21.7%, V about 15.5% of chords; IV (not V) is the tonic's opposite pole; about 22.3% of all transitions run between the tonic and subdominant states; an eight-state model fits best.
- Conclusion: the three-function (tonic / pre-dominant / dominant) model is not universal; each repertoire has its own syntax.

**The Billboard corpus itself: Burgoyne, Wild & Fujinaga, ISMIR 2011** — [PDF](https://ismir2011.ismir.net/papers/OS8-1.pdf)
- Random sample of Billboard Hot 100 chart slots, 4 August 1958 to 30 November 1991, stratified by era and chart-rank quintile; over 1,000 songs, 1,100 unique singles by 533 artists, 414,059 labelled beats.
- Songs average 11.8 unique chords (range 1-84); late-1970s songs show the greatest harmonic variety; major chords are more than half of all chord tokens.

**Listener evidence**
- Vuvan & Hughes, "Musical Style Affects the Strength of Harmonic Expectancy" (Music & Science, 2019) exists and addresses whether listeners' chord expectations differ between classical and rock contexts; not read in this session. — [DOI](https://doi.org/10.1177/2059204318816066)

### Inferences
- My arithmetic from the tables above (not stated in the sources): V→I outnumbers IV→I by about 5.2 to 1 in the Kostka-Payne corpus (167 vs 32) but IV→I outnumbers V→I by about 1.5 to 1 in the rock corpus (1,162 vs 788). Descending-fifth root motion is about 39% of all root motions in Kostka-Payne (308 of 788) and about 25% in rock (2,266 of 9,153), where ascending-fifth motion is essentially equal (24%).
- A practical "classical-ness" dial for the engine can therefore be built from four measurable quantities: (a) ratio of descending-fifth to ascending-fifth root moves (classical about 2-3.5 : 1; rock about 1 : 1); (b) ratio of V→I to IV→I; (c) share of inverted chords (classical about 40%; rock about 6%); (d) share of ii and vii° versus bVII and bVI.
- Tymoczko's transition table is directly usable as a first-order chord generator for a "classical" mode, and the de Clercq-Temperley counts as a "rock" mode; Queen and ABBA would be expected to sit between, nearer the classical end on (a)-(c). That expectation is untested: I found no corpus measurement of Queen or ABBA specifically.
- The late-1970s peak in harmonic variety in the Billboard corpus coincides with the Queen/ABBA period; this is a coincidence of dates noted from the source, not a finding about those bands.
- Schemata are not visible in root-only corpora: inversions carry the bass line (1-7-6-3, 4-3-2-1), and rock-corpus encodings drop or under-use inversion. A schema-aware engine needs bass-degree and melody-degree data, which these corpora do not supply.

### Gaps
- No study found that counts *schemata* (as bass+melody pairs) in a pop corpus, or that compares Queen/ABBA with the rock corpus.
- I did not retrieve Temperley & de Clercq's later 200-song extension (2013), which adds melodic transcriptions, or the minor-mode breakdown.
- The Bach percentages come from what Tymoczko himself calls a crude MIDI survey that includes spurious progressions; treat them as approximate.
- The Kostka-Payne corpus is small (919 chords) and made of textbook examples chosen to illustrate rules, so it likely overstates regularity.

---

## Key question 4 — Is there evidence that songs using these classical patterns last longer or are liked more?

### Takeaway
I found no empirical study testing whether classical schemata, sequences or voice-leading patterns make songs more liked or longer-lived. The nearest evidence is one correlational chart study showing that more successful songs use slightly *less common* chords in the verse and then relax into a more predictable chorus — a contrast effect, small in size.

### Cited Findings
- Miles, Rosen & Grzywacz, "A Statistical Analysis of the Relationship between Harmonic Surprise and Preference in Popular Music", Frontiers in Human Neuroscience (2017). Corpus: McGill Billboard (732 songs, 1958-1991), reduced to 545 major-key non-modulating songs; top chart quartile (151 songs) compared with bottom quartile (150). — [Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2017.00263/full)
- Result 1: top-quartile songs averaged 5.31 bits of chord surprise versus 4.84 for the bottom quartile (p < 0.01; Cohen's d = 0.289, a small effect). The difference was spread across 247 of 302 chord types, not driven by a few rare chords. — [Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2017.00263/full)
- Result 2: the difference lies in the verses (5.26 vs 4.60 bits, p < 0.001); choruses and bridges did not differ between quartiles. — same source
- Result 3: top-quartile songs showed a larger *drop* in surprise from verse into the following chorus (2.15 vs 0.95 bits, p < 0.001); section-to-section variability of surprise was higher in top-quartile songs (standard deviation 1.07 vs 0.89 bits). — same source
- Authors' limits: correlational only; chart rank is a proxy shaped by sales and airplay; "surprise" is zero-order (how rare a chord is in the corpus), ignoring chord order — informal tests with chord-sequence measures showed no quartile difference; all songs were already hits, so an inverted-U cannot be tested; modulating songs were excluded. — same source
- A later study on novelty and cultural evolution in popular music exists (EPJ Data Science, 2023) but was not read in this session. — [Springer](https://link.springer.com/article/10.1140/epjds/s13688-023-00377-7)
- Anecdotal only: the same Pachelbel-type progression underlies charting songs from 1966 to 2019 (list in Key question 1), and Pete Waterman called the Canon "almost the godfather of pop music". This shows persistence of the pattern, not that it causes success. — [Wikipedia, List of variations on Pachelbel's Canon](https://en.wikipedia.org/wiki/List_of_variations_on_Pachelbel%27s_Canon)

### Inferences
- The one measured effect points at *contrast between sections*, not at any particular classical device: harmonically richer verse, plainer chorus. Queen's and ABBA's practice of modulating or sequencing in verses and bridges and landing on diatonic, strongly cadential choruses is consistent with it, but the study did not test those bands or those devices, and it excluded songs that change key.
- Because the surprise measure ignores chord order, it cannot credit sequences, bass lines or schemata at all. The honest position for the engine's design document is: classical patterns are a well-defined, time-tested way to generate coherent harmony and voice-bass counterpoint; evidence that they raise liking or longevity is absent, not negative.
- Survivorship caution: the canon of "classical-sounding" pop hits (Queen, ABBA, Beatles, Procol Harum) is selected after the fact; no source here compares them with equally classical-sounding songs that failed.

### Gaps
- No study found on longevity (decades-later streaming, cover counts, catalogue sales) as a function of harmonic schemata, sequence use, bass-line motion or modulation.
- No listener experiment found that compares liking for galant-schema-based versus loop-based pop progressions.
- Related work probably relevant but not located or read: Askin & Mauskapf (2017, American Sociological Review) on "optimal differentiation" of hit songs; Cheung et al. (2019, Current Biology) on uncertainty and surprise in chord pleasure; Vuvan & Hughes (2019) on style-dependent harmonic expectancy.
