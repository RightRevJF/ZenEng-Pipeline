## Summary

- **v7 has more than an on/off switch** (my earlier claim was wrong): second-singer rows, ensemble kinds, a duet harmony rule (a third or sixth below, chord tones, no crossing, no parallel fifths or octaves), the never-together duet, the backing echo and a unison anchor. But only the duet harmony has a writer, and every second voice in songs 53 to 56 was written by hand.

- **Three of those four songs broke v7's default:** a harmony above the lead (54, 55), a two-note answer (56), a descant and choir (53).

- **Traditions agree the harmony is a chord tone, not a fixed interval,** and put it above the lead as often as below: the bluegrass and country tenor, the barbershop tenor, the brother-duet third above.

- **10,529 PDMX scores measured.** v7's allowed set (3, 4, 8 or 9 semitones below) covers only about a fifth of real harmony pairs. The second voice is above the lead 28% of the time, in unison or octaves about a quarter of the time, and holds still (static or oblique) in about half of all motions. Parallel fifths are rare (about 1 per 100 motions; 3 in pop). Second voices sound under more of the lead as the song goes on, in every group.

- **What v8 should build (section 5):** six kinds of second voice with their own writers (double, harmony line, pad, answer, descant, parts); a harmony line by chord tone on the side the style calls for, with motion bands; parallel octaves only in a marked doubling passage; entries that grow with the song's intensity curve; and the measurement run on every output.

- **DALI:** the GitHub repo has no annotations; they are in restricted Zenodo record 3576083 and need an access request.

## 1. What Luthier v7 does now

A correction first. When I proposed this topic I said v7 has only an on/off backing-vocal row. That was wrong. A reread of v7 finds seven rules that touch a second voice:

|Rule in v7|What it does|What it leaves out|
|---|---|---|
|11.2 amended (v58): second- singer rows|Each singer gets a voice row and a register, so a duet can be written for two real voices|Nothing about how the two lines relate|
|v59: ensemble kinds|Names solo, duet, band with backing vocals, choir|The kinds are labels; only the duet has a writer|
|v70 fix 2 (Window 88, song 22): the duet harmony|A harmony derived from the melody: a third below by default, else a sixth (3, 4, 8 or 9 semitones); every note a chord tone; never crossing; inside the singer's row; one top note under the lead's peak in the final chorus; no parallel fifths or octaves|Harmony above the lead; motion other than parallel; where harmonies enter and leave; more than two voices|
|Fix 61: the never-together duet|A duet can be marked so the voices only alternate|Overlap, echoes, a call answered|
|Fix 84: the backing echo|Backing voices repeat the lead's last words, a third under or in unison|Chords of two or three voices; pads on a vowel|
|The unison anchor|Two voices meet in unison or the octave at an anchor|When, and how often|
|Production table: backing vocals OPTIONAL/ON|Whether backing vocals exist in the mix|Their notes|

Two more places bear on it. Window 57 measured the Open Hymnal's four-part hymns, and Module 9.14 sets voice-leading and low-interval limits that apply to any added voice. A complaint about descants is on file (line 3181 of the spec) with no rule behind it.

### What the recent songs needed

- **Song 53, Sung to Sleep (carol, organ and choir).** Four-part choir in hymn mode and a soprano descant over the last verse and refrain. All of it was written by hand on the sketch path; v7 has no descant writer.

- **Songs 54 and 55 (country, the yard-man and lake songs).** A harmony voice a third above the lead on the hook, "the crowd singing back", and on chorus 3's middle lines. v7's rule says a third below. The above-harmony was written by my hand, as were the duet tag's lines (him a third below in his octave, her above him).

- **Song 56, Terpsichore.** Backing voices answer the lead with a two-note chord over his held note in chorus 3 and the outro. That is call and response, which v7 can't write; fix 84's echo repeats the lead's words in his rhythm.

So every second voice in the last four songs was hand-made, and three of the four broke v7's default (above, not below; a chord, not a line). Jason's ruling on song 56 stands behind this report: the engine should be writing everything.

## 2. The academic record

The record on backing vocals is thin. A 2023 Trondheim master's thesis on backing vocals in pop says the topic has had little research attention, and Susan Fast and Jacqueline Warwick (cited in a 2024 Goldsmiths thesis) note there is no definitive history of the backing singer. Rock theory has mostly studied chords, not lines: Everett's survey of rock's tonal systems finds harmony matters more than counterpoint in most rock. Lacasse's work on vocal staging covers how recorded voices are placed (doubling, panning, reverb), not their notes. So the best guidance comes from the traditions that teach harmony singing by name, and from perception research.

### What each tradition does

|Tradition|Where the melody sits|The harmony voice|Source|
|---|---|---|---|
|Plain backing vocal (pop, rock)|Lead on top or in the middle|One line above or below, mostly thirds or sixths that fit the chords; some bands hold long, slow notes under the chorus|Encyclopedic summaries of vocal harmony|
|Brother duet|Lower voice|A tenor in parallel|Scaruffi; Country|
|(Delmore, Louvin,||thirds above, the|Music Hall of Fame|
|Everly)||two moving as one|summaries|
|Bluegrass trio|Middle (the "standard stack")|Tenor: the next chord tone above, following the melody's shape. Baritone: the next chord tone below. Variants: the high lead (both parts under the melody) and the high baritone (both above)|No Depression on the Osborne Brothers; bluegrass references|
|Barbershop|Second from the top, the lead|Tenor above, bass lowest, baritone fills the chord, often below the lead; four parts on every melody note|Barbershop Harmony Society definition|
|Gospel choir|Usually soprano; the tenor often takes it in some arrangers' work|Starts in unison or call and response and builds to full parts as the song goes on|Fiveable summary; ACDA on Hogan|
|Hymn (SATB)|Soprano|Alto, tenor, bass in chordal rhythm with the tune|Window 57 of the spec already|

Three points follow. First, the harmony above the lead is as normal as the one below: country and bluegrass put the tenor above by default, which is what songs 54 and 55 needed. Second, the harmony is defined by the chord, not by a fixed interval: the next chord tone above or below. A third is what that usually gives, but on some melody notes it gives a fourth or a sixth. Third, harmonies are placed: gospel builds from unison to parts, and pop holds them for the chorus.

### What perception research says about lines

Huron's derivation of voice-leading rules from perception (Music Perception, 2001; the MIT Press book, 2016) gives the reasons behind v7's rule. Unisons, octaves and fifths fuse most readily, so parallel motion in them makes two voices sound like one. That is why classical rules ban parallel fifths and octaves, and it is also why close-harmony styles use parallel motion on purpose: Huron treats close harmony as a texture that seeks fusion, where counterpoint seeks independence. He also documents that the highest voice dominates attention, and that listeners can track only a few lines at once. For a backing vocal, then, the question is not "is it independent?" but "is it meant to blend into the lead or to answer it?" v7 has one rule for both.

## 3. Perception and practice: tuning, blend, balance

These bear on how the demo renders voices and what the songbook tells singers. They don't change the notes.

|Finding|Numbers|Source|
|---|---|---|
|Unison voices should match pitch closely|Listeners preferred 0 to 5 cents of scatter; 14 cents was tolerable|Ternström 1993, J Voice|
|Real choirs scatter more than that|Typically 20 to 30 cents between singers in unison|Ternström 2003 review; Jers and Ternström|
|Choirs bend thirds|Major thirds sung wide (about 416 cents), minor thirds narrow (about 276)|Ternström 2003 review|
|Small ensembles stay near equal temperament|A student quintet tuned close to equal temperament, major thirds slightly toward just|D'Amario, Daffern, Howard and Pennill|
|Barbershop tunes chords just|The dominant seventh's seventh sung about 31 cents flat of the piano; dominant sevenths are 35 to 60% of traditional barbershop chords|Hagerman and Sundberg 1980; harmonic-seventh references; Choralnet|
|Singers need to hear themselves|Preferred self-to-other ratio about +6 dB (0 to +15)|Ternström 1999, JASA|
|The top voice takes the ear|The highest voice is perceptually dominant|Huron 2016|

### What this means for Luthier

- **A harmony above the lead competes with it.** Because the top voice takes attention, an above-harmony must sit lower in the mix and be sung lighter. Songs 54 and 55's songbooks already say "never louder"; v8 should make that a production rule tied to the harmony's side, not a note in prose.

- **Unison doubling needs a tight match.** A doubled lead (the most common backing part in modern pop) should be described as a double, tuned within a few cents, not as a harmony.

- **The demo renders equal temperament.** That is right for band songs. For a cappella or choir passages the songbook can tell singers to tune thirds and sevenths by ear; the score stays as written.

- **Practice warns against nonstop parallel thirds.** Worship-band teaching material says singers who find the third and never leave it make a part that wears out; it recommends oblique motion, holding a note while the lead moves. Section 4 measures how often real scores do that.

## 4. Measured: lead against harmony in 10,529 scores

**Data.** PDMX (Zenodo 15571083, CC BY 4.0): scores with words, deduplicated, no licence conflict, two or more parts. 12,852 qualified; 10,529 had two or more vocal parts and parsed. The lead is the part with the most syllables. At each lead note, the other part's sounding note gives the interval; consecutive pairs give the motion. The clean duet group is "2 voices, both with words" (799 scores, 100,865 note pairs).

**Caveats.** PDMX is user-made MuseScore scores, so popular songs are arrangements, not studio parts. The popular duet sample is small (48 scores, 9,170 pairs). Chords aren't in the files, so chord-tone membership isn't tested here.

### The tables

**Intervals** (share of sounding pairs, %)

|Group|Scores|Below|3rds|6ths|5ths|Unison, 8ve|Dissonant|v7's set|Crossed|
|---|---|---|---|---|---|---|---|---|---|
|Popular duets|48|67|25|9|14|26|16|18|6|
|Folk duets|22|65|28|13|9|28|17|18|4|
|Sacred duets|28|53|23|19|11|30|10|13|6|
|Classical duets|701|73|31|14|12|25|11|21|5|
|All duets|799|72|30|13|12|26|11|21|6|
|All, 3 voices|1,335|66|33|14|14|20|10|20|5|
|All, 4+ voices|8,059|61|29|15|15|20|10|18|4|
|Popular, 4+ voices|273|60|22|13|14|23|17|13|6|

"Below" is the share of pairs where the second voice is the lower part. "Dissonant" is seconds, sevenths and tritones.

**Motion and placement** (%, except the per-100 columns)

|Group|Same onset|Static or oblique|Contrary|Parallel|Parallel 5ths per 100|Parallel 8ves, unisons per 100|Present, first → last fifth|
|---|---|---|---|---|---|---|---|
|Popular duets|77|52|10|28|3.3|10.8|63 → 78|
|Folk duets|81|53|12|26|0.5|10.6|66 → 76|
|Sacred duets|78|47|14|31|0.6|16.4|72 → 90|
|Classical duets|77|45|18|28|0.9|10.2|69 → 81|
|All duets|77|46|17|28|1.1|10.5|68 → 81|
|All, 3 voices|75|48|21|20|0.7|4.7|74 → 85|
|All, 4+ voices|72|54|21|14|0.5|2.9|68 → 78|
|Popular, 4+ voices|61|67|9|16|1.4|6.9|70 → 79|

Intervals are by class, so a tenth counts as a third. "In v7's set" means exactly 3, 4, 8 or 9 semitones below the lead, which is v7's whole allowed vocabulary.

### What the numbers say

1. **v7's set covers about a fifth of real harmony.** Thirds and sixths together are 34% to 45% of sounding pairs. Restricted to below the lead and inside the octave, as v7 requires, they are 13% to 21%.

2. **The harmony is above the lead a third of the time** (28% in duets, 33% in popular duets). v7 forbids it.

3. **About a quarter of all pairs are unison or octave.** These are doubling stretches, where the two voices sing the same tune. Parallel unisons and octaves run 10 to 16 per 100 motions in duets. v7's ban on parallel octaves rules out the commonest duet texture.

4. **Parallel fifths really are rare:** under 1 per 100 motions except in popular duets (3.3). v7's ban fits everything but pop.

5. **Real harmony holds still.** About half of all motions are static or oblique; parallel motion is 28% in duets and 14% in four parts; contrary motion 10% to 21%. A rule that adds a fixed interval to the melody is parallel by construction, so v7's writer would invert this profile.

6. **Dissonance is normal on the way through:** 10% to 17% of pairs are seconds, sevenths or tritones, nearly all short passing notes.

7. **The voices mostly move together:** 77% of lead notes start with the harmony note (61% in popular four-part, where pads and held notes are common).

8. **Harmony grows through the song.** In every group the second voice sounds under more of the lead in the last fifth than in the first: popular duets go from 63% to 78%, sacred duets from 72% to 90%.

Song 53's choir could not be measured here: its scores live in the song's output folder, which is not in the repo. The measurement can be rerun on it when the folder is rebuilt (the parser reads the engine's own MusicXML).

## 5. What v8 should do

Keep what v7's rule gets right: chord tones on strong notes, inside the singer's row, no crossing, the harmony's peak under the lead's. Replace the rest with a writer for each kind of second voice, and bands from section 4.

### V1. Six kinds of second voice, each with its own writer

v59's ensemble kinds become writers. Each passage of a second voice is one of:

|Kind|What it is|Used in|
|---|---|---|
|Double|The lead's tune in unison or an octave away|Pop choruses, duets' shared lines, hymns|
|Harmony line|A line above or below that follows the lead's rhythm|Songs 54 and 55's hook, duets|
|Pad|Held vowels ("ooh", "ah") on chord tones under the lead|Pop and gospel backing|
|Answer|Its own words between or over the lead's phrases|Song 56; gospel call and response|
|Descant|An independent line above a choir or congregation|Song 53's last verse|
|Parts|Three or four voices on every melody note (trio stack, barbershop, SATB)|Song 53; bluegrass; hymns|

The intake asks which kinds the song uses and where. Fix 84's echo becomes a case of Answer, fix 61's never-together duet a constraint on Double and Answer.

### V2. The harmony line by chord tone, on either side

- **Side by style.** Above (the tenor) for country, bluegrass, brother duets and anthems; below for pop, folk and singer-songwriter by default; the intake can override. v7's "a third below" becomes the pop default, not the rule.

- **The note.** The next chord tone above (or below) the lead's note, as bluegrass and barbershop teach. That gives a third most of the time and a fourth or sixth where the chord requires. On short weak notes a passing note may stand (10% to 17% of pairs are dissonant in real scores).

- **Bands for a harmony line,** from the duet scores: thirds and sixths at least 35% of pairs; static or oblique 45% to 55%; parallel 25% to 35%; contrary at least 10%; crossing at most 6%.

- **Parallel fifths** at most 1 per 100 motions, 3.5 in pop. **Parallel unisons and octaves** only inside a passage marked Double.

### V3. Where second voices go

- Presence grows: the share of the lead covered by a second voice in the song's last fifth exceeds the first fifth's by at least 10 points (every group measured did so).

- The first entry is on a hook or chorus; the last chorus adds lines (songs 54 and 55 already did this by hand). Gospel and worship songs may build from unison through Answer to Parts.

- Tie the entries to the song-wide intensity curve (749.17), so a new voice is one of the steps that lift each return.

### V4. Production and the songbook

- A second voice above the lead is mixed and sung lighter than one below (the top voice takes the ear). The production table states the side, not only ON.

- Doubles are described as doubles, tuned tight; a cappella passages tell singers to tune thirds and sevenths by ear.

### V5. Tests

- `voices_pdmx.py` 's measures, run on every engine output through `parse_parts.py`

- (it reads the engine's MusicXML), reported against the V2 and V3 bands in the test report.

- A control run with v7's rule: the profile should show the near-total parallel motion section 4 predicts, so the change is visible.

- Rerun on song 53's choir once its output folder is rebuilt, and on songs 54 to 56's hand-written parts as the first targets the engine must match.

## 6. Files and sources

### In the repo (studies/voices)

- `parse_parts.py` : every part of a MusicXML score, aligned in time (reads PDMX and

- the engine's own scores).

- `voices_pdmx.py` : the section 4 measurement; `voices_pdmx_results.json` : its

- results; `README.md` .

### Data

PDMX, Long et al., Zenodo record 15571083, CC BY 4.0.

- DALI (Meseguer-Brocal et al.): the annotations are in restricted Zenodo record 3576083; GitHub holds only code and metadata. Not used yet; access must be requested.

### Sources

- Huron, D. (2001). Tone and voice: a derivation of the rules of voice-leading from perceptual principles. Music Perception 19(1), 1–64.

- Huron, D. (2016). Voice Leading: The Science behind a Musical Art. MIT Press.

- Ternström, S. (1993). Perceptual evaluations of voice scatter in unison choir sounds. Journal of Voice 7(2), 129–135.

- Ternström, S. (1999). Preferred self-to-other ratios in choir singing. JASA 105(6), 3563– 3574.

- Ternström, S. (2003). Choir acoustics: an overview of scientific research published to date. International Journal of Research in Choral Singing 1(1), 3–11.

- Hagerman, B. and Sundberg, J. (1980). Fundamental frequency adjustment in barbershop singing. KTH STL-QPSR 21(1).

- Devaney, J., Mandel, M. and Fujinaga, I. (2012). A study of intonation in three-part singing using AMPACT. ISMIR 2012, 511–516.

- D'Amario, S., Daffern, H., Howard, D. and Pennill, N. Tuning in a newly formed singing quintet (White Rose eprint 157113).

- Everett, W. (2004). Making sense of rock's tonal systems. Music Theory Online 10(4).

- Lacasse, S. (2000). Listen to my voice: the evocative power of vocal staging in recorded rock music. PhD thesis, Liverpool.

- The Art of Backing Vocals (2023), master's thesis, NTNU (hdl.handle.net/11250/3097093).

- Finney, R. (2024), PhD thesis on the background vocal, Goldsmiths (citing Fast and Warwick).

- Barbershop Harmony Society, definition of the barbershop style (via Sunshine District and Wikipedia).

- No Depression, "Osborne Brothers: a high lead, a long run"; Wikipedia, Bluegrass music (stacks); California Bluegrass Association, "The Perfect Stack".

- Scaruffi, P., The Everly Brothers (the Delmore tradition of harmonic thirds).

- ACDA Choral Journal, December 2020 (Battiste on Moses Hogan's arrangements).

- The Church Collective, "Structuring Vocals, Part One: Oblique Harmony" (2016).

- Wikipedia, Vocal harmony; Barbershop music; Harmonic seventh.

Not reached: Hagerman and Sundberg's full paper and Ternström's 2003 review were read only through abstracts and citing papers.
