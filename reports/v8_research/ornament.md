## Summary

- **v7 counts melisma and renders vibrato, and nothing else of delivery.** It adds twonote turns at corpus rates, bans melisma on cadence notes, and sets a delayed MIDI vibrato. No score or songbook for songs 52 to 56 named a scoop, fall, cry, run or vibrato style.

- **6,716 songs measured.** Chart pop sets 8% to 11% of syllables on more than one note (rising from the 1960s), arrangements of pop half that, hymns and folk about 5% to 8%, standards almost none. Melismas gather at phrase ends (2.5 to 3 times their share), are two notes three times in four, and increase through the song in every corpus. v7's cadence-note ban runs against this.

- **Delivery research:** scoops are the commonest pop inflection (short, under half a second); many pop singers barely use vibrato while gospel voices use it wide and fast; the country breaking voice falls on grief words; runs are mostly pentatonic, 4 to 7 notes, at the ends of long notes near the song's peak.

- **What v8 should build (section 5):** a written tier (melisma by style bands and placement, runs as designed moments) and a performed tier (inflections and vibrato by style, named in the songbook and rendered in the demo), with an ornament card in the test report.

## 1. What Luthier v7 does now

v7 measures melisma carefully and treats the rest of vocal delivery as MIDI rendering.

|Rule in v7|What it says|What it leaves out|
|---|---|---|
|Window 30, finding 3 (karaoke corpus)|A second note on one syllable on 11.5% of sung syllables, 15.4% at line ends; two notes in 44% of melismas; the commonest shapes a step down or a step up. The hook designer adds a two-note turn on held syllables at these rates (75% a step down)|Longer runs; how rates differ by genre and era|
|Window 95, step 4 (theory corpus)|Syllables with a melisma: 16% in the median charting song, 9% in the Lied, 0% in the standard. A third of pop's melismas fall on the phrase's last syllable; pop's summit is a melisma in 39% of songs|Hymns, gospel, R&B, country|
|Module 27|A melisma never lands on a cadence note|Why; whether singers agree|
|10.19, intelligibility|Melisma lowers word understanding a little (84% to 77%, and only on one-syllable words; Johnson, Huron and Collister 2014)||
|Module 9.5 (MIDI performance)|Vibrato by CC1, delayed and ramped in over the first quarter of a held note; phrase "breathing" by CC11|Vibrato rate and depth by style; straight tone; scoops, falls, bends in the voice|
|Window 30 and the role table (2.8)|Commas are breaths: an eighth's rest after a comma; a phrase over 13 syllables dies in the search|Where breaths go in long lines; breath as expression|
|The blues window|Blue notes come from just intonation (Kubik); the blues voice uses a cry and crosses the passaggio|A notation for the bent third or seventh in the voice|
|11.11 (genre sounds)|The pedal steel's slide-in bends and swells in General MIDI|The same for the voice|

### What the recent songs did

- **Songs 52 to 56:** every melisma in the sung lines came from the engine's two-note turn or the sketch tables. No score carried a grace note, a slide, a fall, an ad-lib or a vibrato marking for the voice.

- **Song 54:** the fiddle answered the voice with a bend from the note above into a chord tone, the only written inflection, and it was for an instrument.

- **The songbooks** describe the singer's range, blend and where to stay below the lead, but say nothing about runs, scoops or tone.

So v7 can tell how often a syllable carries more than one note, but not what a singer does with a note: the inflections a gospel, country, R&B or soul singer adds, or the plain delivery a hymn or folk tune wants.

## 2. The academic record

### Melisma and runs

- **Where it came from.** Writers on gospel and soul trace pop's runs to Black church singing: Anthony Heilbut (The Gospel Sound; his NPR guide, 2007) names Sam Cooke, Ray Charles and Aretha Franklin as the singers who carried melisma into the mainstream, and voice-science and music-press histories name Whitney Houston's "I Will Always Love You" (1992) and Mariah Carey's "Vision of Love" (1990) as the records that made heavy runs a pop norm. Country has its own older line of melisma from Appalachian and Celtic singing.

- **What a run is made of.** Teaching material and analysis agree that runs are mostly pentatonic or blues-scale, in small steps and even fast notes. Tilo Hähnel's portrait of Mahalia Jackson (Weimar and Jena DFG project "Voices and Singing in Popular Music in the USA", 2012) finds nearly every tone she sings in the pentatonic scale, melismas of 4 to 7 notes at the ends of long tones, single grace notes or glides at their starts, and ornaments growing toward the song's emotional centre, where she also sings her highest note.

- **Ornament grows with the song.** Hähnel's Jackson portrait describes ornament concentrated where the song peaks, much as gospel choirs build from unison to full parts (Part 24).

- **Riff and run.** Pedagogy distinguishes a run (a fast scalar passage) from a riff (a short repeated figure, any intervals). The CCM pedagogy literature (Bartlett and Naismith 2020, via Voice Science) describes R&B as light delivery with heavy embellishment and fast vibrato.

### Inflections beyond melisma

- **A vocabulary by style.** Edrie Means's NATS teaching list of vocal stylisms gives, for country: add-on notes, bent notes, cry, fall-offs and fall-ups, slides, tails, waves, yodel; for pop and rock: flip onsets (the "pop appoggiatura"), cry, fall-offs, fry, growl, slides, tails; for R&B and gospel the same plus riffs, shouts and shadow vowels.

- **The breaking voice carries grief.** Paul and Huron (Empirical Musicology Review, 2010) found 31 breaking-voice moments in country recordings and showed the word under the break was more grief-related than the matched word in control songs, at the level of the single word, not the line or the stanza.

- **Yodel types.** Timothy Wise (Radical Musicology, 2007) classifies falsetto effects in popular singing, from the hillbilly yodel onward, by the moment the voice breaks register.

- **Portamento.** Schubert and Wolfe argue the voice is built for pitch glides and that their near absence from emotion research reflects how hard they are to measure, not their rarity.

### Folk and hymn

v7's own theory corpus already shows the plain end: the median standard has no melismas, folk song about 4.5% (Dutch folk songs), the Lied 9%. Hymn tunes are set syllabically, with occasional two-note slurs. Section 4 measures them.

## 3. The singing voice measured

|Finding|Numbers|Source|
|---|---|---|
|Classical vibrato is narrow in rate|5.5 Hz (Pavarotti) to 6.7 Hz (Marian Anderson) on long notes, extent about ±60 cents; the rate rises in the last cycles of a long note|Prame, JASA 1994 (ten singers, Schubert's Ave Maria)|
|Ranges by style|Classical voices about 4.5 to 6.3 Hz in one review; faster in other styles; women's tend toward 7 Hz|Larrouy-Maestri et al., J Voice 2014 (review); Titze and others|
|A gospel voice|Vibrato about 6 to 7 Hz, extent over 200 cents|Hähnel on Mahalia Jackson (2012)|
|Many pop singers barely use vibrato|In 168 J-pop hits by 42 singers, several singers rarely used it|"Analysis and detection of singing techniques in repertoires of J-POP solo singers" (arXiv 2210.17367, 2022)|
|The scoop is the commonest pop inflection|Scooping was the most frequent technique, then vibrato, bend and drop; every singer scooped more than 29 times in four songs' openings; techniques last 0.1 to 1 s (mean 0.4 s) and cover 23% of singing time|The same J-pop study|
|Listeners hear through a scoop, and hear it|Pitch is judged as an average across the note and the scoop is also heard against its context|Larrouy-Maestri and Pfordresher, "Pitch perception in music: do scoops matter?" (2018)|
|Melisma costs a little intelligibility|Word understanding 84% to 77% on melismas, only on one-syllable words|Johnson, Huron and Collister 2014 (already in v7)|
|Phrases fit a breath|A phrase is held in memory up to about 8 seconds; v7's Window 3 sets phrases of 5 to 8 seconds|Part 11 (psychoacoustics) and fix-list finding 749.21; v7 Window 3|

### What this means for Luthier

- **Vibrato is a style choice, not a constant.** v7's delayed-onset CC1 is a classical habit. Pop and folk singers often sing straight tone with vibrato only on long held notes; gospel and R&B use wide, fast vibrato. The demo should set rate and depth by style and leave short notes plain.

- **Scoops and falls are the everyday ornaments of popular singing,** short (under half a second) and nearly constant. They are performance, not notes: the score shouldn't write them, but the songbook can name where the style wants them (a scoop into a stressed long note, a fall off a line's last note), and the demo can render them with pitch bend.

- **Runs are notes** and belong in the score when they're part of the song (a written turn or run), and in the songbook as optional when they're the singer's to add.

## 4. Measured: melisma in 6,716 songs

**Data.** CoCoPops transcriptions of 214 Billboard songs (1958–1991) and 80 Rolling Stone 200 songs, sung syllables with their notes; 5,981 English songs with words in PDMX (Zenodo 15571083), by PDMX's genre and tag categories (the word-setting study, Part 23, used 4,176 of the same scores: those in 4/4 or 3/4 that its stress measures read); 441 OpenEWLD standards. A melisma is a syllable sung on two or more different notes (ties merged). Phrase end: the syllable before a rest, the end, or line-ending punctuation (MusicXML), or the last syllable of a transcribed line (Billboard).

### Rates, lengths and placement

|Corpus|Songs|Melismatic syllables|Song median (middle half)|Songs with none|2 notes / 3 / 4 / 5+|At phrase ends (base)|First, middle, last third of song|
|---|---|---|---|---|---|---|---|
|Billboard, 1958–69|71|8.0%|6.7% (2.2–12.9)|1%|72 / 18 / 4 / 6|24% (8%)|7.4, 7.8, 8.9|
|Billboard, 1970–79|68|11.0%|8.3% (3.8–16.4)|6%|70 / 20 / 5 / 5|18% (7%)|10.0, 10.6, 12.6|
|Billboard, 1980–91|75|10.4%|9.1% (4.2–18.2)|5%|75 / 16 / 5 / 4|19% (8%)|9.3, 10.2, 11.8|
|Rolling Stone 200|80|8.8%|8.2% (4.8–12.0)|1%|70 / 19 / 6 / 5||7.8, 8.9, 9.7|
|PDMX popular|590|4.7%|3.5% (1.1–7.7)|12%|63 / 16 / 6 / 14|48% (15%)|3.9, 4.4, 5.8|
|PDMX hymns and sacred|407|7.3%|5.6% (1.5–13.2)|19%|73 / 13 / 5 / 9|25% (16%)|6.1, 7.6, 8.3|
|PDMX folk|330|7.9%|4.8% (0–12.5)|26%|77 / 11 / 4 / 8|23% (14%)|7.1, 7.8, 8.8|
|PDMX other classical|4,654|7.5%|5.4% (1.9–12.6)|15%|74 / 12 / 4 / 9|21% (17%)|6.9, 7.2, 8.3|
|OpenEWLD standards|441|1.9%|0% (0–2.2)|55%|81 / 6 / 3 / 9|38% (12%)|1.5, 1.7, 2.3|

**Shape (MusicXML corpora):** 45% to 64% of moves inside a melisma are steps of one or two semitones; the first move goes down in 52% to 59%; a melisma ends lower than it began in 52% to 60%. **Grace notes** are almost never written: 0 to 0.18 per 100 sung notes.

### What the numbers say

1. **Chart pop is melismatic at about 8% to 11% of syllables,** rising from the 1960s to the 1970s and holding after. Arrangements of pop songs in PDMX carry half that (4.7%): the same flattening v7 found in its karaoke corpus. Standards are almost syllabic (median 0%).

2. **Melismas gather at phrase ends:** 2.5 times their share of syllables in Billboard lines, about 3 times in PDMX popular and standards. v7's rule that a melisma never lands on a cadence note works against this: the line's last syllable is where singers ornament most.

3. **Two notes is the norm** (63% to 81% of melismas); three notes in 6% to 20%; runs of five or more in 4% to 14%, the most in popular arrangements.

4. **Melisma grows through the song in every corpus:** the last third carries more than the first (Billboard 9.0% to 11.3%; PDMX popular 3.9% to 5.8%; standards 1.5% to 2.3%). This matches Hähnel's observation that ornament concentrates toward a song's peak.

5. **v7's figures differ by method.** Window 95's "16% in the median charting song" is about twice the CoCoPops median here (8.6%); the karaoke corpus's 11.5% sits between. The likeliest cause is counting tied or repeated notes as melisma. v8 should fix one definition (different pitches, ties merged) and recompute its bands.

No open corpus of gospel, R&B or soul with notes and words was found, so their higher rates and longer runs rest on the literature (section 2), not on counts.

## 5. What v8 should do

Split ornament into two tiers: what is written (notes in the tune) and what is performed (described in the songbook, rendered in the demo, never engraved as notes).

### O1. The written tier: melisma by style, placed where singers put it

- **One definition:** a syllable on two or more different pitches, ties merged. Recompute v7's bands with it.

- **Bands by style** (share of syllables): standards and art-song-like ballads 0% to 2%; hymns and folk about 2% to 13%, median about 5%; chart pop 4% to 18%, median about 8% to 9% (post-1970 sound), 7% (1960s sound).

- **Placement:** melismas at phrase ends at 2.5 to 3 times their syllable share; on wordfinal syllables; more in the last third than the first.

- **Length:** two notes in about three quarters, three notes in about a sixth; five or more only as a designed run.

- **Shape:** mostly steps, first move down a little more often than up.

- **Retire the cadence-note ban.** Replace "a melisma never lands on a cadence note" with: the cadence note may carry a short melisma (two or three notes) that ends on the cadence pitch.

### O2. Runs (gospel, R&B, soul, worship)

- A run is 4 to 7 notes, pentatonic or blues-scale, on a long note at a phrase end, concentrated near the song's peak and in its last sections, rarely in verse 1.

Because no counted corpus exists, a run is a designed moment (11.9's vocabulary), chosen at intake for the styles that use them, and written in the score as an optional small-note line or described in the songbook as the singer's to add.

### O3. The performed tier: a vocabulary by style

|Style|Inflections to name in the songbook|Vibrato|
|---|---|---|
|Country|Scoops into stressed long notes, falls at line ends, the cry or break on a grief word (Paul and Huron), slides, the yodel flip|Light, on long notes|
|Pop and rock|Scoops, flip onsets, falls, fry at phrase starts, growl for intensity|Straight on short notes, late on long ones|
|R&B, soul, gospel|Runs, scoops, falls, cry, shouts, wide vibrato on held peaks|Fast and wide (about 6 to 7 Hz)|
|Hymn, folk, choir|Plain; tune by ear; no scoops on the beat|Little or none in unison; light in solo|
|Art song, classical|Legato, written ornaments only|About 5.5 to 6.5 Hz, about ±60 cents|

The intake's style picks the column; the songbook's "for the singer" paragraph names the two or three inflections that matter, and where (computed from the record: the stressed long notes, the line ends, the peak, the grief words).

### O4. The demo

- Render scoops (a short bend up into the note, under half a second) on stressed long notes and falls on line-final notes, by style.

- Set vibrato rate and depth by style; none on notes under about half a second.

- Breath: keep v7's comma rule, Window 3's 5 to 8 seconds and 749.21's 8-second ceiling; render a short gap before each new line.

### O5. Tests

- The test report gets an ornament card: melisma share, length distribution, phrase-end ratio, third-by-third trend, against the style's band.

- The songbook check: the singer's paragraph names the style's inflections and every bar it cites comes from the record.

- First targets: songs 54 and 55 (country inflections and the cry), song 56 (soul runs at its peak), song 53 (plain, choir).

## 6. Files and sources

### In the repo (studies/ornament)

- `ornament_corpora.py` : melisma rates, lengths, placement, shape, thirds of the song,

- and grace notes, from PDMX, OpenEWLD and CoCoPops; `ornament_results.json` .

### Data

- CoCoPops Billboard and Rolling Stone 200 (Computational Cognitive Musicology Lab, GitHub), via ../words/sung_syllables.json.

- PDMX, Long et al., Zenodo 15571083, CC BY 4.0.

- OpenEWLD (public-domain lead sheets, GitHub).

### Sources

- Heilbut, A. The Gospel Sound; NPR, "How American Idol uses and abuses melisma" (2007).

- Hähnel, T. (2012). A brief portrait of Mahalia Jackson; and Analysis of vocal recordings: twang. DFG project "Voices and Singing in Popular Music in the USA", HfM Weimar.

- Paul, B. and Huron, D. (2010). An association between breaking voice and grief-related lyrics in country music. Empirical Musicology Review 5(2), 27–35.

- Wise, T. (2007). Yodel species: a typology of falsetto effects in popular music vocal styles. Radical Musicology 2.

- Means, E. Vocal stylisms broken down (NATS 2018 handout).

- Schubert, E. and Wolfe, J. A note for emotion in music research about portamento (UNSW).

- Prame, E. (1994). Measurements of the vibrato rate of ten singers. JASA 96, 1979–1984. Larrouy-Maestri, P. and colleagues (2014). Operatic voices, J Voice (vibrato review).

- "Analysis and detection of singing techniques in repertoires of J-POP solo singers" (2022), arXiv 2210.17367.

- Larrouy-Maestri, P. and Pfordresher, P. (2018). Pitch perception in music: do scoops matter?

- Johnson, R., Huron, D. and Collister, L. (2014), on sung intelligibility (in v7). Bartlett, I. and Naismith, M. (2020), CCM pedagogy of R&B, via the Voice Science lexicon.

Not reached: no open corpus of gospel, R&B or soul transcriptions with words; DALI (restricted Zenodo 3576083) would give melisma counts from aligned recordings.
