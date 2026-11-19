# Same Time Tomorrow: test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v22 (main at 8dea87c). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage8.md).

## The run

- Key C (48 to 60); other keys offered: A, D.
- Chords: draft 9 of 12, charge 0.0.
- Melody: 615 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 326, 840: the title's stresses off the beat 59.
- The pick: 225b8c372faa, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 308, joint gate 308, words' gate 308 (at least 0.092; builds' fit quartiles [0.305, 0.347, 0.381]).
- Distance 2.987 (gate 4.104); directed readings, printed only: low surprise -2.804, sure endings 0.223, order across scales, pitch 0.873, order across scales, rhythm 0.471.
- Flags: no break: with one the song would run past the kept 75th of lengths; the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [47, 60] |
| sung notes on a beat that are chord tones, share | 0.858 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 480 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 16.1 |
| of those, at a line's end (kept 20 in 100); on a word's end (kept 94) | [65, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.486 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.011] |
| a song with blue notes | False |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.092, quartiles 0.202, 0.291, 0.384) | 0.29 |
| the fit by length, by place in the bar, by height (kept medians 0.132, 0.311, 0.104) | [0.019, 0.541, 0.027] |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 3.0 |
| the plan's lift | 3 |
| rest share inside sung sections, median (kept quartiles 0.21, 0.30, 0.39) | 0.19 |
| the title's stressed syllables on a beat (kept 0.73) | 0.75 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 343 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.46 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with accompaniment above them, share | 0.0 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.422, 0.295], '5th': [0.161, 0.176], 'octave': [0.099, 0.155], 'unison': [0.062, 0.151], '4th': [0.156, 0.119], '6th': [0.099, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [5.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.112, 0.225], 'oblique': [0.294, 0.298], 'contrary': [0.075, 0.099], 'parallel': [0.374, 0.278], 'similar': [0.144, 0.1]} |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.6, 6.4] |
| sung phrases over eight seconds | 0 |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.675, 0.918] |
| roughest bars | [53, 66, 113, 108, 114] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.486 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.75 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.38, Verse 1 0.38, Chorus 1 0.54, Turn 2 0.64, Verse 2 0.39, Chorus 2 0.54, Bridge 0.49, Verse 3 0.39, Last Chorus 0.54, Outro 0.55. Each chorus is above its verse; the last chorus is not above the first, and the turn reads highest (749.75).
- A breath, then a fresh re-entry: real breaths (an onset gap of three beats or more) 6.1 a minute, inside the human range (median 7). The 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65).
- Perception: accompaniment above a sung note 0.0; sung phrases [4.6, 6.4] s, none over eight; the chord voicings inside the low-interval limits. But the guitar sounds under only 6 of 469 sung notes (749.73).
- Two channels and chromatic harmony: no chord from outside the key (share 0.0); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 869: sixteenths 5.3 in 100 of the sung notes (kept 15); no build died for want of a fit.
- 870: the median rest between lines of a section 15 twelfths; 24 of 50 exactly a quarter (749.58 stays open).
- 871: no two-syllable line-final word holds its weak syllable longer (0 of 13); one three-syllable word does, “completely” (749.71).
- 875: no melisma on a function word (0 of 65).
- 882: of the pick's 34 calls to refit a line, 23 are lines sung again and 11 are fresh lines that borrow an earlier line; 5 lines sung again keep their source note for note. Stressed syllables a sixteenth long in lines sung again: 3 of 75 (song 54: 19 of 134, 749.66).
- The harmony voice: 192 notes, lowest D2; 3 below E2 (749.74).
- Length: 343 s in the checks, 337 s in the flag (749.69); 229 s under v20.

## The documents

Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:

| Check | Result |
|---|---|
| the document record is the song record: sung notes | pass |
| harmony notes | pass |
| band parts | pass |
| bars and chords | pass |
| every sung line spells its locked line | pass (57 lines) |
| readback: him read back | pass (469 of 469) |
| readback: him read back | pass (469 of 469) |
| readback: harmony read back | pass (192 of 192) |
| readback: guitar read back | pass (828 of 828) |
| readback: bass read back | pass (480 of 480) |
| readback: drums counted | pass (1416 of 1416) |
| readback_score: him read back | pass (469 of 469) |
| readback_score: harmony read back | pass (192 of 192) |
| readback_score: guitar read back | pass (828 of 828) |
| readback_score: bass read back | pass (480 of 480) |
| readback_score: drums counted | pass (1416 of 1416) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass |
| full score: PDF written, credit line | pass (4 pages) |
| full score: footer tempo and key | pass |
| parts: PDF written, credit line | pass (8 pages) |
| parts: footer tempo and key | pass |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| number chart: one cell a bar, as the record | pass (120 cells) |
| MusicXML lead sheet: onsets and pitches | pass (469) |
| demo: voice notes | pass (469) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+10.4 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | not met (last chorus 0.54, top Turn 2 0.64 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

Numbered from 749.66; each has Problem, Evidence, Fix and Check in the fix list for v23 (`songs/p68/fixlist_v23.md` and its Doc).

- 749.66 A split in a line sung again (882) halves the note it splits, chosen by place alone: a stressed syllable can be left a sixteenth long.
- 749.67 Lines sung again keep less of their source, and no kept figure says how much they should.
- 749.68 In 4/4 the joint gate and the words' gate pass nearly every build.
- 749.69 One song, two lengths (343 s and 337 s), both past the kept 75th.
- 749.70 The new kept tables and the stage 8 and 9 results have no maker that runs in the repo.
- 749.71 871 reads only words stressed on their first syllable.
- 749.72 Two fits printed for one pick; two sets of kept figures for the fit.
- 749.73 Under a low voice the guitar drops out: 6 of 469 sung notes have it sounding.
- 749.74 The harmony voice has no range of its own (D2).
- 749.75 Every chorus is at level 1.0: the last chorus is not the song's top (9.12).
- Carried open: 749.58 (rests), 749.61 (6/8).
