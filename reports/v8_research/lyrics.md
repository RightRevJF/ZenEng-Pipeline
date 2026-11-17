## Summary

The songs artists and critics call greatest repeat fewer of their lines than ordinary hits (0.42 against 0.57 of lines), use plainer words and range wider in feeling. The chart rewards repetition; peers reward lines that keep moving.

- **v7** already holds the deepest lyric research in the spec, but almost all of it asks whether a lyric charted. After v7's own language correction, what stands is chorus repetition, predictability, constraints per line, "you" as object and familiar words.

- **New research:** story can now be measured (agents, events, a world), and Grammynominated country songs tell more of it than their album-mates. Songs with sad endings and fall-then-rise or rise-then-fall shapes did better in a national contest. Lyrics draw an interest of their own, apart from plays.

- **Measured on 64 greatest-list songs against 209 Hot 100 songs (1958 to 1991):** fewer repeated lines (the one result that survives a strict correction), fewer rare words, a wider range of feeling, more absolutes. A crude story proxy did not separate them.

- **Songs 52 to 56:** unusually concrete and varied words, a strength. Songs 54 and 55 repeat too few lines even by the peers' standard, and songs 53, 55 and 56 hold a narrow range of feeling.

- **For v8:** seven rules (section 5): repetition between the two channels' medians, carried by the chorus; a range of feeling with the arc printed; low endings offered; a story dial for story styles; plain words; absolutes allowed; concreteness kept as style.

## 1. What Luthier v7 does now

v7's lyric research is the deepest in the spec: more than a dozen windows on 15,941 lyrics, tested against the chart, against songs that lasted and against the hymnal. Two gaps remain. Almost every test asked whether a lyric charted, never whether people who judge songs think it is good, and nothing measures story.

|Area in v7|What it found|Standing after v7's own correction (Windows 64 and 65)|
|---|---|---|
|Repetition (Window 27)|Chorus type-token ratio 0.23 against the verse's 0.575; hits repeat more even in verses|Stands|
|Predictability (Window 58)|Hits are more predictable word by word; inside the chart, bigger hits more so|Stands, weaker|
|Constraints per line (Window 59)|A line held by rhyme, metre, repetition and a concrete act lasts; about 1.5 constraints a line in every lasting form|Stands on persistence and the hymnal|
|Address (Windows 31, 34)|"You" as the object of a line, from Packard and Berger|Rests on their experiments|
|Common words (Window 34)|Familiar words are sung more intelligibly|Rests on Johnson, Huron and Collister; the chart signal fell to chance|
|Concreteness and the senses (Windows 32, 91)|Plain concreteness null; hits lean on body words, songs that last on visual words|Stands, as a dial|
|Meaning (Window 60)|Hits range in meaning; the title's company changes by the last chorus|Chart support gone; kept as craft rules|
|Blending (Window 61)|Remote word pairs and two-world titles|Chart support gone or reversed|
|The quotable line (Module 10.20)|Lines ranked against each other; the writer's blind picks as the label|Stands|
|The writing room (Modules 10.10 to 10.16, 28)|Story questions, twelve candidates by named moves, coaching, never-say lists, the mouth test|Process, not tested against an outcome|

### What the recent songs needed

Songs 52 to 56 were written from Jason's own poems and stories, so the writing room's coaching and the mouth test did most of the work. What no rule told them is how much story a song should tell, where its feeling should end, and how its words compare with songs that musicians and critics call great.

## 2. The academic record

Since v7's lyric windows, the research has moved to three things v7 never measured: story, the emotional arc, and judgements by peers rather than sales. All three point the same way: what peers reward in words is not simply what charts reward.

### Story

**Narrativity, measured.** Bamman and colleagues scored lyrics on three axes (particular agents, events in sequence, an inhabitable world) and trained a model that matches human ratings closely (Spearman 0.84; frontier language models managed 0.53 to 0.59). In 5,745 Billboard year-end hits, mean narrativity rose from 2.58 to 3.72 between 1960 and 2024, led by hip hop (4.01) and country (3.43); disco and soul were lowest [(Bamman et al. 2025)](https://anthology.ach.org/volumes/vol0003/measuring-stories-in-contemporary-songs/10.63744@w9C0wDxmZTVt.pdf).

- **Peers reward it in country.** Grammy-nominated Best Country songs scored 3.61 against 3.40 for non-nominated songs from the same album (n = 259, p = 0.002). Song of the Year nominees scored 4.2% higher, at the edge of significance; rock, R&B and rap showed no gap.

- **What carries it.** Past-tense verbs, time words, places and concrete objects; firstperson pronouns alone predicted nothing.

- **The arc.** In 12,280 lyrics and 2,823 greatest hits, songs set the stage early, move the plot steadily and peak in internal tension in the middle. Country and rap set the scene in more detail; pop moves faster and holds more conflict ([Alberhasky and Durkee 2024](https://doaj.org/article/b8e7f4e79e52458589979532040b2095)).

### The emotional arc

In a German national song contest (176 songs, 2005 to 2015), songs with sad endings drew more points than happy endings (4.06 against 3.35 on a 0 to 12 scale), and higher emotional peaks drew fewer. Of the classic story shapes, "man in a hole" (fall, then rise) and "Icarus" (rise, then fall) did best [(Rösch and Rauch 2025](https://link.springer.com/article/10.1007/s10824-025-09532-6)). Correlational, one contest, but the only outcome study of lyric arcs.

### What changed in the words

Across 353,320 English lyrics from 1970 to 2020, lyrics became simpler, more repetitive, more negative and more personal. People's views of the lyrics on Genius behave differently from their listening counts, so lyrics hold an interest of their own ([Parada- Cabaleiro et al. 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10978890).

### Already in v7 and still standing

Chorus repetition and the chart (Nunes, Ordanini and Valsesia 2015), "you" as the object of the line (Packard and Berger 2020), moderate topic atypicality (Berger and Packard 2018), constraints per line (Rubin), familiar words for sung intelligibility (Johnson, Huron and Collister 2014), and concrete object words as the mark of professional poems (Kao and Jurafsky). This study does not repeat them.

## 3. New vectors from bibliographies and arXiv

|Vector|Where it came from|What it adds|Here|
|---|---|---|---|
|Peers against the chart|Rolling Stone's 500 Greatest Songs (a poll of more than 250 artists, musicians, producers and critics), with 80 of its songs transcribed with lyrics in CoCoPops|An outcome for "great" rather than "hit"|Used (section 4)|
|A narrativity model|Bamman et al. 2025 (a fine-tuned RoBERTa beats frontier language models on this task)|Story as a measured dial for the writing room|Its features used as a proxy|
|Paired by album|Bamman et al. 2025, Grammy nominees against their album-mates|Holds artist, era and production constant|A design for a later study|
|Emotional arcs|Rösch and Rauch 2025, after Reagan et al. 2016's six story shapes|The shape of feeling through a song, and its ending|Used (range and ending)|
|Lyric views|Parada-Cabaleiro et al. 2024|Interest in the words themselves, separate from plays|Not reachable here|
|Annotated lines|arXiv [1708.03492](https://arxiv.org/pdf/1708.03492) (803,720 Genius lyric-annotation pairs); [2006.08108](https://arxiv.org/pdf/2006.08108v1)|Which lines listeners stop to explain: a line-level outcome|A later study|
|Expert ratings of whole songs|arXiv [SongEval (2505.10793)](https://arxiv.org/pdf/2505.10793), 2,399 songs rated by 16 professionals on coherence, memorability, phrasing, structure and musicality; [SongBench (2604.25937)](https://arxiv.org/pdf/2604.25937)|A human-rated outcome for whole songs, mostly AI-generated|For testing v8's demos later|
|Long notes on stressed syllables|arXiv [LOAF-M2L (2307.02146)](https://arxiv.org/html/2307.02146v1)|73% to 82% in human lyrics (Part 31)|Carried over|

## 4. Measured: greatest-list songs against ordinary hits

The songs artists and critics call greatest repeat fewer of their lines than ordinary hits, use fewer rare words, and swing wider in feeling from line to line. Story features did not separate them.

CoCoPops transcribes, as sung, 64 songs from Rolling Stone's 500 Greatest Songs and 209 songs from a random sample of the Hot 100, both from 1958 to 1991 and by the same project (studies/lyrics). Lines were cut by one rule for both: a gap of half a beat, a word held two beats, or a new section. Each comparison is shuffled within decades to control for era.

|Measure|Greatest (median)|Hot 100 (median)|AUC (greatest higher above 0.5)|p within decade|
|---|---|---|---|---|
|Repeated lines (share of lines sung more than once)|0.42|0.57|0.37|0.001|
|Rare content words (Zipf under 3)|3.2%|4.8%|0.41|0.03|
|Feeling's range across lines (spread of line valence)|0.26|0.22|0.60|0.02|
|Absolutes per line (always, never, forever)|0.054|0.034|0.60|0.01|
|Words per line|4.4|3.8|0.62|0.003|
|Proper nouns per 100 words|0.6|1.2|0.42|0.06|
|"You" per word|0.031|0.047|0.43|0.10|
|Concreteness of content words|2.90|3.01|0.44|0.11|
|Narrativity index (past tense, time, place, names, he/she/they)|−0.15|−0.08|0.45|0.25|
|Lexical variety, rhyme density, ending, mean valence|||0.47 to 0.51|over 0.5|

Twenty-four measures were compared, so only the repeated-lines result clearly survives a strict correction. The words-per-line gap may partly reflect how the two sets were encoded. The story proxy is cruder than Bamman's model, so its null says little about story itself.

This is the music's two-channel pattern again (Parts 7 and 12). The chart rewards repetition; the people who judge songs reward lines that keep moving. Part 30's hook rules and this result fit together: the chorus repeats its cell and its hook phrase, and the rest of the song keeps changing.

### Songs 52 to 56

Percentiles against the greatest-list songs (song 53 is read from its lyric as written, so its repetition is not comparable):

|Song|Repeated lines|Rare words|Feeling's range|Concreteness|Lexical variety|"You"|
|---|---|---|---|---|---|---|
|52|53 (0.43)|6|69|91|73|53|
|53|not comparable|52|6|83|67|6|
|54|19 (0.28)|48|41|100|97|20|
|55|19 (0.27)|55|14|98|95|41|
|56|61 (0.50)|25|14|83|53|78|

Jason's lyrics are unusually concrete and varied: four of five songs sit in the top fifth for concreteness. Songs 54 and 55 repeat fewer lines than four in five greatest-list songs, so their choruses carry too little return even by the peers' standard. Songs 53, 55 and 56 hold a narrow range of feeling across their lines.

## 5. What v8 should do

v8's writing room should aim for both channels: a chorus that returns, a song whose lines move, a wide range of feeling, and story where the style calls for it. Each rule has a check that runs on every lyric. If added to the fix list, they would follow Part 30's numbers.

|Rule|What v8 does|Check|
|---|---|---|
|L1. Repetition by channel|The share of lines sung more than once sits between 0.42 (the greatest-list median) and 0.57 (the Hot 100 median). The chorus and hook phrase carry the repeats (Part 30, H2 and H3); verses do not repeat lines|lyrics_our_songs.py; songs 54 and 55 (0.28, 0.27) would be raised|
|L2. A range of feeling|Line-by-line feeling spreads at least as wide as the Hot 100 median (valence spread 0.22, aim 0.26). The arc is printed with the lyric: where it falls, where it turns, where it ends|Songs 53, 55 and 56 (6th to 14th percentile) flagged|
|L3. Endings may land low|A sad or bittersweet ending, and a fall-then-rise or rise-then-fall shape, are offered as options at the story questions; the arc is reported, not scored|Report only (one contest study)|
|L4. A story dial|For story styles (country, folk, narrative, hymn testimony), the writing room asks for agents, events in order and a place, and reports past-tense verbs, time words, places and concrete objects per 100 words|Report; a narrativity model can replace the proxy later|
|L5. Plain words|Rare content words at most about 4% (greatest-list median 3.2%), which also serves sung intelligibility (v7's familiarity rule)|Already near for all five songs|
|L6. Absolutes allowed|Remove the verse penalty v7 keeps on always, never and forever (Window 34); greatest-list songs use more of them|Module 28's imagery term|
|L7. Keep the concreteness|Jason's concreteness is a strength, not a lever; leave it as a style dial (v7, Window 91)|None|

### Tests for v8

1. Songs 52 to 56 rerun on lyrics_our_songs.py: repeated lines within L1's band (song 53 read as sung), feeling's range at or above 0.22.

2. Every lyric prints its arc, its story readings and its repetition against both medians.

3. A blind pick by Jason between a v7 lyric revision and an L1 to L4 revision of one song, his choice logged.

## 6. Files and sources

### In the repo (studies/lyrics)

- lyrics_features.py: the measures, for CoCoPops Rolling Stone and Billboard transcriptions (one line rule for both); lyrics_rows.json, lyrics_rows_scored.json (derived numbers only, no lyrics)

- lyrics_analyse.py: greatest-list against Hot 100, shuffled within decades; lyrics_results.json

lyrics_our_songs.py: songs 52 to 56; lyrics_our_songs.json

### Data

- CoCoPops Rolling Stone (80 songs with syllables) and Billboard (214) transcriptions; Brysbaert concreteness norms; wordfreq; the CMU pronouncing dictionary; VADER; spaCy

### Sources

- [Bamman, Baur, Cramer, Ho and McEnaney 2025, Measuring the stories in contemporary songs](https://anthology.ach.org/volumes/vol0003/measuring-stories-in-contemporary-songs/10.63744@w9C0wDxmZTVt.pdf)

- [Alberhasky and Durkee 2024, Songs tell a story: the arc of narrative for music](https://doaj.org/article/b8e7f4e79e52458589979532040b2095)

- [Rösch and Rauch 2025, Do songs tell stories? Emotional arcs and success in a national song contest](https://link.springer.com/article/10.1007/s10824-025-09532-6)

- [Parada-Cabaleiro et al. 2024, Song lyrics have become simpler and more repetitive over the last five decades](https://pmc.ncbi.nlm.nih.gov/articles/PMC10978890)

- [Rolling Stone, The 500 Greatest Songs of All Time (how the list was made)](https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/green-day-basket-case-1225188)

- arXiv: [1708.03492](https://arxiv.org/pdf/1708.03492), [2006.08108,](https://arxiv.org/pdf/2006.08108v1) [2505.10793,](https://arxiv.org/pdf/2505.10793) [2604.25937](https://arxiv.org/pdf/2604.25937), [2307.02146](https://arxiv.org/html/2307.02146v1)

- Luthier v7, Windows 27, 31, 34, 58, 60, 61, 64, 65 and 91 (the spec)
