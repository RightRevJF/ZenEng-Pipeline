## Summary

- **v7 picks a key from the hook and the voice only** (27.14 ranks keys by where the hook's degrees land). Songs 52 to 56 got instrument-friendly keys (D, E♭, G, A, E minor) because they were chosen by hand.

- **Instruments shape keys.** In 739 Billboard songs, guitar-led songs sit in open-string keys 65% of the time and in E, A or B major twice as often as piano-led songs; piano, strings and synthesizer songs use flat keys about twice as often as guitar songs. Spotify's 30 million tracks lean the same way (G, C, D, A major first).

- **Minor rose and open-string keys fell:** BiMMuDa's hits go from 11% minor before 1970 to about half after 1990, and from about half in open-string keys to under a third. Country and rock stay in open major keys; R&B, soul and hip-hop live in flat keys and minor.

- **The singer:** a hit's sung range is about an octave, with its floor on the tonic or the dominant below and its top near the fifth above the octave, so the key follows from the voice's floor and the frame. Key colour is a myth on equal-tempered instruments (Powell and Dibben).

- **What v8 should do:** choose the frame from the voice, filter by the lead instrument (with a capo when needed), set the mode default by genre and era, and only then rank by the hook as 27.14 does now.

## 1. What Luthier v7 does now

v7 chooses a key from the voice and the hook alone.

|Rule in v7|What it says|What it leaves out|
|---|---|---|
|27.14, the key from the contract|When the writer names no key, list for each key the pitches where the hook's required degrees land inside the voice's approach window; rank keys by how many; offer two to hear|The instruments, the genre, the era, the key the band will want to play in|
|Module 11.2, the voice rows|One table of ranges, breaks and finals per voice (male 52–66, break 64; female 57–71, break 69; gospel, worship, congregational and bass rows) serves the search, 27.14 and the range check|How a real singer's key relates to their range|
|Fix 20, the capo|An intake field; capo shapes printed beside concert chords|When a capo is the right answer|
|Fix 92, editions|A second edition by transposition or octave, with an ossia|Choosing which editions a song needs|
|Fix 34, spelling|Pitches spelled from the key (sharps in sharp keys, flats in flat keys)||
|Module 9-M.4, metal|The tonic is the lowest open string of the tuning|The same logic for every guitar song|

### What the recent songs used

- **Song 52** (6/8 guitar ballad): D major. **Song 53** (carol, organ and choir): E♭ major, the last verse up to F. **Song 54** (country): G major. **Song 55** (country): A major. **Song 56** (soul ballad): E minor.

- Four of the five sit in the keys a guitar plays openly (D, G, A, E minor) and the organ carol in a flat key, which is what players of those instruments would expect. Each was chosen at intake by hand; nothing in v7 asked for an open-string key, or said that a carol for organ and choir usually sits in a flat key.

## 2. The academic record

- **Instruments shape the key.** Spotify's Kenny Ning analysed the keys of some 30 million tracks (2015): G major 10.7% and C major 10.2%, then D and A; more than a third of all songs sit in G, C, D or A major, and the commonest minors (A, E, B minor) are their relatives. His explanation: E suits guitar but not piano, C suits piano but not guitar, and G suits both. Guitar teaching sources say the same about open strings (E, A, D, G and their minors).

- **Minor has risen.** Schellenberg and von Scheve (Psychology of Aesthetics, Creativity, and the Arts, 2012; over 1,000 Billboard year-end top-40 songs, 1965–2009) found the share of minor-mode hits doubled over five decades, while tempo fell and songs got longer. Press summaries of the paper give 85% major in the 1960s against 42.5% in 2005–09.

- **Key colour is a myth on equal-tempered instruments.** Powell and Dibben (Musicae Scientiae, 2005): about three quarters of participants claimed key-mood associations, which matched 18th-century beliefs (sharps bright, flats mellow), but no one could identify mood from key or key from mood, and moving a piece to another key didn't change its perceived mood. What does change is pitch height relative to the voice, and the instrument's open strings and tone.

- **Hymnals choose keys for the congregation.** Joey Stanley's count of the Latter-day Saint hymnal (341 hymns) finds G major 22%, D 16%, C, E♭ and F about 14% each, B♭ 11%, A♭ 6%, and almost no A or D♭. Half the hymns top out at D5, and only about 2% go above E5.

- **Untrained voices are narrow.** Kuhn, Wachhaus, Moore and Pantle (Journal of Research in Music Education, 1979; 597 non-music undergraduates) found 98% could sing comfortably from B♭3 to G4, 84% from G3 to B4, 75% from G♭3 to C5. Worshipleading advice built on it: lower the key when the tune goes above C5 unless people sing parts.

## 3. Measured: keys by instrument, era and genre

**Data.** McGill Billboard (739 songs, 1958–1991): the annotated tonic, mode from the tonic chord, and the lead instrument the annotators marked most often. BiMMuDa (381 top-five singles, 1950–2022): tonic, mode and genre from its metadata. "Open-string keys" means E, A, D, G and C major and E, A and D minor; "flat keys" means F, B♭, E♭, A♭ and D♭ major.

### By lead instrument (McGill Billboard)

|Lead instrument|Songs|Minor|Open-string keys|Flat keys (of major)|E, A or B major (of major)|Commonest keys|
|---|---|---|---|---|---|---|
|Guitar|335|17%|65%|23%|31%|D, G, E, A, C|
|Piano|48|2%|56%|43%|15%|C, G, B♭, D♭|
|Synthesizer|61|34%|49%|42%|20%|G, A♭, D, E|
|Strings|30|13%|50%|50%|15%|C, E♭, F|
|Horns or sax|59|15%|64%|30%|16%|C, D, F, E♭|
|All|739|17%|62%|29%|27%|C, D, G, E, A|

### By era and genre (BiMMuDa, with McGill for comparison)

|Group|Songs|Minor|Open-string keys|Flat keys (of major)|
|---|---|---|---|---|
|1950–69|102|11%|52%|42%|
|1970–89|102|32%|46%|29%|
|1990–2009|102|49%|36%|44%|
|2010–22|75|45%|31%|46%|
|McGill, 1958–69 / 1970–79 / 1980–91|237 / 260 / 242|10% / 16% / 26%|61% / 62% / 62%|34% / 27% / 25%|
|Rock|81|30%|53%|23%|
|Country|16|0%|62%|31%|
|Pop|139|27%|43%|42%|
|Funk and soul|44|36%|36%|50%|
|R&B|42|48%|31%|50%|
|Hip-hop|31|68%|26%|60%|

I also read the notated key signatures of 16,000 PDMX and OpenEWLD scores, but usermade scores default heavily to C and lead sheets are often transposed for convenience, so those counts describe the notation, not the records, and are left out.

### What the numbers say

1. **Guitar songs sit in guitar keys.** Guitar-led Billboard songs use open-string keys 65% of the time and the sharp guitar keys (E, A, B major) twice as often as piano-led songs (31% against 15%). Piano, strings and synthesizer songs use flat keys about twice as often as guitar songs (42% to 50% against 23%).

2. **Minor rose steadily:** 10% to 26% in Billboard between the 1960s and the 1980s, 11% to about half in BiMMuDa by 1990–2009, which agrees with Schellenberg and von Scheve.

3. **Open-string keys fell as guitars gave way to keyboards and production:** from about half of BiMMuDa's hits before 1970 to under a third after 2010.

4. **Genre separates sharply:** country and rock live in open-string major keys; R&B, funk, soul and hip-hop in flat keys and minor. Hip-hop is two-thirds minor.

5. **Songs 52 to 56 match their instruments:** four guitar-led songs in D, G, A and E minor, and an organ carol in E♭.

## 4. The singer: where the tonic sits in the range

A key is a choice of where the song's frame lands in a voice. I measured where the tonic falls inside the sung range of real hits (the range taken as the 5th to 95th percentile of the melody's notes, so a stray note doesn't decide it).

|Corpus|Songs|Range (semitones), median and middle half|Lowest note above the tonic below it|Highest note above that tonic|Commonest lowest notes|Commonest highest notes|
|---|---|---|---|---|---|---|
|BiMMuDa, 1950–2022|374|12 (10–14)|median 5|median 17|the tonic (26%), the dominant (22%)|the 5th above the octave (20%), the 3rd above it (11%)|
|CoCoPops Billboard|214|12 (9–14)|median 5|median 16.5|the tonic (32%), the dominant (14%), the 6th (14%)|the 5th above the octave (17%), the 3rd above it (13%)|

**Two frames cover most songs.** The melody's floor is the tonic (an "authentic" range, 1 up to 8 and a little over) or the dominant below it (a "plagal" range, 5 to 5 an octave up). The ceiling is most often the fifth above the upper tonic.

- **The sung range of a hit is about an octave,** with the middle half 9 to 14 semitones. v7's voice rows are 14 to 17 semitones wide, so a song uses most of a row, not all of it.

- **So the key follows from the voice and the frame.** For a singer whose comfortable floor is L, the tonic is L (authentic frame) or L plus 5 (plagal frame); the top lands near the tonic plus 16 to 19. Choosing between the two frames, and among nearby keys the instruments like, is the real decision.

- **For a congregation,** a floor around B♭3 to D4 and a top at D5 (Kuhn and colleagues; the hymnal's commonest top note) give the familiar hymn keys of G, D, E♭ and F when the melody spans tonic to tonic or 5 to 5.

## 5. What v8 should do

Keep 27.14's hook check. Put it third, after the voice and the instruments.

### K1. The voice and the frame first

- From the voice row and the melody's frame, list the candidate tonics: the row's floor as the tonic (authentic frame) or the floor plus 5 (plagal frame), with the song's span (median 12, middle half 9 to 14) under the row's top. This turns 27.14's search over all twelve keys into two or three candidates.

- For congregational songs, keep the top at D5 (E♭5 at most) and the floor at about B♭3, as hymnals do.

### K2. The instruments next

|Lead instrument|Prefer|Avoid unless asked|
|---|---|---|
|Acoustic or electric guitar|E, A, D, G, C major; E, A, D, B minor; a capo for anything else, printed as shapes|E♭, A♭, D♭without a capo|
|Piano|C, G, F, B♭, D, E♭|Many-sharp keys (B, F♯)|
|Organ and choir; hymns|G, D, E♭, F, C, B♭|A and D♭(rare in hymnals)|
|Horns, strings|F, B♭, E♭, C|E, A, B major|
|Synthesizer, production-led pop, R&B, hip-hop|No instrumental constraint: choose by voice; flat keys and minor common||
|Fiddle, mandolin, banjo (country, bluegrass)|G, D, A, E, C|Flat keys|

When the voice's candidates and the instrument's preferences don't meet, offer the capo (guitar) or say which is being given up.

### K3. Mode by genre and era

- Default minor share by genre and era for the mode question at intake: country and 1960s pop about one song in ten; rock about three in ten; pop after 1990 about half; R&B about half; hip-hop about two thirds.

- Don't attach moods to particular keys (Powell and Dibben); the mood comes from mode, tempo and where the melody sits in the voice.

### K4. Then the hook

27.14 ranks the remaining candidates by where the hook's required degrees land in the voice's approach window, and offers two to hear, as now.

### K5. Tests

- The key report prints the frame (authentic or plagal), the span against the row, the instrument's preference, the capo if used, and the hook's landing.

- Songs 52 to 56 as targets: the chooser should arrive at D, E♭, G, A and E minor or name the near alternative and why.

## 6. Files and sources

### In the repo (studies/keys)

- `keys_corpora.py` : keys and modes by lead instrument and era (McGill Billboard), by

- era and genre (BiMMuDa), and the notated keys of PDMX and OpenEWLD (not used in the report); `keys_results.json` .

- `tonic_in_range.py` : where the tonic sits in the sung range (BiMMuDa, CoCoPops

- Billboard); `tonic_in_range.json` .

### Data

- McGill Billboard annotations via ChoCo (Zenodo 7706751); BiMMuDa (Hamilton and Pearce); CoCoPops Billboard; PDMX (Zenodo 15571083); OpenEWLD.

### Sources

- Ning, K. (2015). The most popular keys of all music on Spotify (Spotify Insights; reported by Hypebot, Gizmodo and Digital Trends).

- Schellenberg, E. G. and von Scheve, C. (2012). Emotional cues in American popular music: five decades of the Top 40. Psychology of Aesthetics, Creativity, and the Arts.

- Powell, J. and Dibben, N. (2005). Key-mood association: a self perpetuating myth. Musicae Scientiae 9(2).

- Stanley, J. LDS Hymn Stats: key signatures; highest soprano notes.

- Kuhn, T. L., Wachhaus, G., Moore, R. S. and Pantle, J. E. (1979). Undergraduate nonmusic major vocal ranges. Journal of Research in Music Education; as summarised by Reformed Worship, "Highs and lows of singing".

- Guitar Command, guitar keys and open strings.

Not measured: the fiddle, mandolin and banjo row of K2 comes from practice, not counts; no corpus marks those instruments with keys.
