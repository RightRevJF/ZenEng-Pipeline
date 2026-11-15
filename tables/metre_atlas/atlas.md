# Metre atlas: a head start for Luthier beyond 4/4

Words and music for the songs: Jason Bryant. Prepared 15 November 2026 while the engine was offline, for 749.4, 749.5, 749.9 and 749.11.

## What this is

Kept tables for every time signature the public corpora can support, a test of which tables carry across metres, English stress-to-beat tables from 301 hymns, four-part motion tables from the same hymns, research notes on the metres the corpora barely hold (5/8, 5/4, 7/8, aksak 9/8), and a proposed port. Everything is in the repository under tables/metre_atlas (JSON per metre and source; hymns.json; comparison.json) with the scripts that made it.

## The six findings

1. **Pitch carries across metres; rhythm does not.** Across nine sung metres the medians of repeated notes, steps, leaps, turns, range and longest run barely move; every rhythm reading moves a great deal, even in beat units. One pitch table can serve every metre; rhythm tables must be per metre (749.4, now on nine metres, not two).
2. **The felt metre matters, not the notation.** 6/4 and 6/8 read almost the same in beat units (1.88 against 2.00 notes a beat): they can share a table with a scale factor. 2/2 and 2/4 are close in density (1.81 against 1.64 notes a beat) but divide the beat differently, on a small 2/2 sample (62 tunes). 3/2 and 4/2 are not slow 3/4 and 4/4: they are a plainer, older style (0.74 notes a half-note beat; 44% of 3/2 bars are a whole note and a half). 3/8 is felt in one (2.6 notes a dotted-quarter beat), not as a fast 3/4.
3. **9/8 and 12/8 can be built from 6/8, beat by beat.** In the dance tunes, 9/8 and 6/8 behave alike per dotted-quarter beat (2.55 against 2.68 notes a beat; 82% against 86% of moves a third of a beat). There are almost no sung 9/8 or 12/8 tunes (6 and 0), so sung 6/8's per-beat tables, extended to three or four beats, are the best available.
4. **Vocal tables must come from sung tunes.** The dance tunes are 1.1 to 2 times denser per beat, range 17 to 19 semitones (sung: 12 to 13) and repeat notes far less (6% to 12%; sung: 17% to 22%).
5. **English stress lands on strong beats, by metre (749.5).** In 301 hymns' stanzas (about 40,000 words scored with the CMU Pronouncing Dictionary): in 3/4, 81% of stressed syllables fall on the downbeat; in 4/4, 51% on beat 1 and 38% on beat 3; in 6/8, 84% on the two main beats. Unstressed syllables go the other way.
6. **Real four-part hymn settings move with the tune more than song 52's lines did (749.9).** Altos move with the soprano 35% to 39% of the time, against it 13% to 19%, and hold 44% to 47%; basses move against it most (34% to 40%). Parallel fifths and octaves occur about once in a hundred moves. About 7% to 10% of inner-voice notes are shorter than the beat: passing notes the carol sketch never had.

## Sources

- **Sung tunes:** the Essen folk-song collection in music21's corpus (9 metres with 60 or more tunes; 5/8, 5/4, 7/8 and 9/8 with 7 or fewer).
- **Instrumental tunes:** music21's Irish and Scottish dance collections (Ryan's Mammoth, O'Neill's 1850, Aird's Airs, miscFolk), kept apart.
- **Hymns:** the Open Hymnal Project (public domain; 301 hymns, four voices, English stanzas under the soprano), read with a parser written for its interleaved ABC (hymn_parse.py).
- **Research** (below) for odd metres and text-setting.

## Every metre at a glance

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

## Finding 1 in numbers: what carries across metres

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

## Finding 2 in numbers: notation pairs (medians)

| Pair | Notes a beat | Gaps of half a beat | Gaps of a beat or more | Onsets on a beat | Notes a bar |
|---|---|---|---|---|---|
| 3/8 vs 3/4 | 2.63 vs 1.15 | 2% vs 46% | 2% vs 39% | 36% vs 67% | 2.63 vs 3.44 |
| 6/4 vs 6/8 | 1.89 vs 2.00 | 0% vs 0% | 5% vs 6% | 44% vs 42% | 3.77 vs 4.00 |
| 3/2 vs 3/4 | 0.74 vs 1.15 | 10% vs 46% | 88% vs 39% | 92% vs 67% | 2.21 vs 3.44 |
| 2/2 vs 2/4 | 1.81 vs 1.64 | 41% vs 64% | 7% vs 14% | 47% vs 53% | 3.62 vs 3.27 |
| 4/2 vs 4/4 | 0.75 vs 0.96 | 8% vs 33% | 92% vs 63% | 94% vs 78% | 3.00 vs 3.82 |

## Finding 4 in numbers: sung against instrumental (medians)

| Metre | Notes a beat | Steps | Leaps | Repeated notes | Range |
|---|---|---|---|---|---|
| 6/8 | 2.00 vs 2.68 | 47% vs 52% | 11% vs 11% | 22% vs 12% | 13 vs 17 |
| 2/4 | 1.64 vs 3.21 | 44% vs 52% | 12% vs 14% | 20% vs 7% | 13 vs 19 |
| 3/4 | 1.15 vs 1.30 | 49% vs 60% | 11% vs 9% | 18% vs 10% | 13 vs 17 |
| 4/4 | 0.96 vs 1.67 | 51% vs 53% | 11% vs 13% | 20% vs 10% | 12 vs 17 |
| 2/2 | 1.81 vs 3.59 | 56% vs 48% | 12% vs 13% | 17% vs 6% | 13 vs 19 |

## Finding 5: stress against the bar (hymns)

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

## Finding 6: four-part motion in real hymn settings

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

## Hymn tunes against folk tunes (749.11)

Hymn tunes in 3/4 (46 hymns), quartiles: notes a bar 2.12 / 2.34 / 2.66; distinct bar rhythms 16% / 22% / 32% (sung folk 3/4: 35% / 47% / 67%); gaps of half a beat 0% / 7% / 24%; steps 49% / 57% / 62%. Song 53's carol sketch read 1.97 notes a bar (under the hymn range), 16% distinct bar rhythms (the hymn 25th percentile) and no half-beat gaps: plainer than a typical hymn, as the writer judged. A hymn mode should be charged against these hymn quartiles, not the folk ones. Commonest 3/4 hymn bars: half and quarter (36%), three quarters (26%), dotted half (13%), dotted quarter, eighth and quarter (6%).

## The metres the corpora barely hold: research

- **5/4:** five quarter-note beats, usually grouped 3+2 or 2+3; Brubeck's "Take Five" is 3+2, and the original Mission: Impossible theme keeps the 3+2 subgrouping. Essen has 4 sung tunes in 5/4.
- **5/8, 7/8 and aksak:** additive metres built from short (2) and long (3) pulses. 7/8 is most often 2+2+3 (the Bulgarian rachenitsa), also 3+2+2 and 2+3+2; Balkan 9/8 is usually 2+2+2+3, unlike the Western compound 3+3+3; 11/16 (kopanitsa) is 2+2+3+2+2. Essen has 7 tunes in 5/8 and 2 in 7/8.
- **Text-setting:** composers align stressed syllables with strong beats (Palmer and Kelly 1992, on English song); Halle and Lerdahl (1993) gave the first explicit model; Hayes treats a good setting as the best resolution of conflicting goals (stress on strong positions, avoiding long gaps between syllables, avoiding too many syllables crowded together, phrase ends at line ends), and published 640 lines of English set to rhythm by native speakers (Hayes and Kaun 1996), a ready test set for the engine's stress rule. Alignment also holds in French (Temperley and Temperley 2013).

## Proposed port (749.4)

1. **A metre object:** name; bar length in twelfths; beat groups as a list of lengths (3/4: [12, 12, 12]; 6/8: [18, 18]; 7/8 as 2+2+3: [12, 12, 18]; 5/4 as 3+2: [36, 24]); levels (downbeat, group starts, beats, subdivisions); the felt beat.
2. **Tables by felt metre:** shared pitch tables; rhythm tables per felt metre from sung tunes (this atlas); 6/4 from 6/8 by scale (2/2 from 2/4 only with care); 9/8 and 12/8 from 6/8 per beat; 3/2 and 4/2 as their own (plainer) style; additive metres from their groups, each group read as a short (2) or long (3) beat, until a corpus is found.
3. **Readings in beat units** (notes a beat, gaps of half, a third, a beat or more), so the judge's charge means the same in every metre.
4. **The stress rule per metre** from the hymn table (finding 5), tested on Hayes and Kaun's lines.
5. **Harmony and accompaniment per metre:** four-part motion from finding 6; bass and accompaniment figures by beat groups (749.6, 749.14).
6. **A hymn mode** charged against the hymn quartiles (749.11).

## Data still missing

- Sung English tunes beyond hymns, with words under the notes: DALI (pop songs, notes and lyrics aligned to audio) and the lyrics-melody MIDI set of Yu and others (2021) exist; neither was fetched here.
- Sung 9/8, 12/8, 5/8, 5/4 and 7/8 tunes in numbers: none in the corpora used.

## Files

tables/metre_atlas/: one JSON per metre and source (readings and quartiles, bar rhythms, two-bar windows, intervals, onset weights, durations); hymns.json (hymn readings by metre, stress tables, four-part motion and texture); comparison.json; atlas_build.py, hymn_parse.py, hymn_atlas.py, compare.py.

## Sources (links)

- Open Hymnal Project, github.com/mzealey/openhymnal (public domain)
- music21 corpus: Essen folk songs; Ryan's Mammoth; O'Neill's 1850; Aird's Airs; miscFolk
- CMU Pronouncing Dictionary via the Python package pronouncing
- Palmer, C. and Kelly, M. H. (1992), Linguistic prosody and musical meter in song, Journal of Memory and Language 31: https://www.examenapium.it/cs/biblio/Palmer1992.pdf
- Hayes, B., Textsetting as constraint conflict, with Hayes and Kaun (1996) data: https://brucehayes.org/Textsetting
- Halle, J. and Lerdahl, F., A generative textsetting model, Current Musicology 55: https://www.fredlerdahl.com/writings
- Aksak groupings: https://en.wikipedia.org/wiki/Aksak ; 7/8: https://tunable.pages.dev/time-signature/7-8/ ; 5/4 and "Take Five": https://london-calling-iaspm2020.com/?p=48 ; Mission: Impossible 3+2: https://cellofun.eu/?p=20421
- DALI dataset: https://refworks.reference-global.com/article/10.5334/tismir.30
