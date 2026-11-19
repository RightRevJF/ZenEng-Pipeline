# Same Time Tomorrow (seventh edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v29 (main at c365a48). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage16.md).

## The run

- Key C (48 to 64); other keys offered: A, G.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 660 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 304, 840: the title's stresses off the beat 35, 731: stressed syllables on the beat too few 1.
- The pick: 12ccd22d8bf8, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 330, joint gate 330, words' gate 93 (at least 0.152; builds' fit quartiles [0.228, 0.275, 0.324]).
- Distance 3.021 (gate 3.918); directed readings, printed only: low surprise -3.015, sure endings 0.602, order across scales, pitch 0.905, order across scales, rhythm 0.501.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); 916: the song runs long: its turns are two bars; the song runs 331 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 15 fewer two-bar lines, or about 115 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [47, 64] |
| sung notes on a beat that are chord tones, share | 0.842 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 464 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 16.1 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [32, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.655 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.139] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.2, 0.64, 0.16] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.4, 0.07, 0.18] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.29 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [9.1, 2.88] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['8/65', '3/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 64, 64] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.261 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.199, 0.199, 0.115] |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 9 |
| the plan's lift | 9 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.264 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 331 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.22 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.904 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.251, 0.295], '5th': [0.215, 0.176], 'octave': [0.149, 0.155], 'unison': [0.097, 0.151], '4th': [0.128, 0.119], '6th': [0.159, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [4.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.147, 0.225], 'oblique': [0.342, 0.298], 'contrary': [0.141, 0.099], 'parallel': [0.19, 0.278], 'similar': [0.179, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [41, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.3, 9.8] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.039, 13.8] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.661, 0.79] |
| roughest bars | [112, 26, 58, 23, 62] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.655 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.72, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.56. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.3, 9.8] s, over 12 beats, share and longest in beats, [0.039, 13.8] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.904, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.16, a half or more 0.16 (kept, ties read, pooled 0.18, 0.29; by song a half or more runs 0.075 to 0.52 across the middle half); lines run on with under a beat of rest 0.29 (kept 0.295); rest median 22.5 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 4 of 14 line ends (kept 42 in 100, ties read).
- Breaths: 7.3 real breaths a minute by onsets (human median 7); silences of a beat or more 9.1 per 100 beats (kept 7.1, 8.6, 10.4), median silence 2.9 beats. Phrases split at half a beat: over 12 beats 0.039 (kept 0.042), longest 13.8 beats (kept songs' longest, quartiles 8, 12, 15.5). A two-bar turn after chorus 1 (916).
- 900: the guitar under 1.0 of the sung notes.
- Length: 331 s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).
- 749.77 (closed): with ties read, kept stressed syllables a sixteenth long inside lines, first verse and chorus 0.109, later ones 0.108.

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
| readback: harmony read back | pass (195 of 195) |
| readback: guitar read back | pass (2665 of 2665) |
| readback: bass read back | pass (464 of 464) |
| readback: drums counted | pass (1368 of 1368) |
| readback_score: him read back | pass (469 of 469) |
| readback_score: harmony read back | pass (195 of 195) |
| readback_score: guitar read back | pass (2665 of 2665) |
| readback_score: bass read back | pass (464 of 464) |
| readback_score: drums counted | pass (1368 of 1368) |
| lead sheet: PDF written, credit line | pass (3 pages) |
| lead sheet: footer tempo and key | pass (C major) |
| lead sheet: key signature is the record's | pass (\key c \major) |
| full score: PDF written, credit line | pass (6 pages) |
| full score: footer tempo and key | pass (C major) |
| full score: key signature is the record's | pass (\key c \major) |
| parts: PDF written, credit line | pass (8 pages) |
| parts: footer tempo and key | pass (C major) |
| parts: key signature is the record's | pass (\key c \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (C major: 1 = C, 2m = Dm, 3m = Em, 4 = F, 5 = G, 6m = Am) |
| number chart: one cell a bar, as the record | pass (116 cells) |
| MusicXML lead sheet: onsets and pitches | pass (469) |
| demo: voice notes | pass (469) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+7.8 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.74, top Last Chorus 0.74 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

Numbered from 749.94 (improvements from here; 749.95 bears on the margin); each has Problem, Evidence, Fix and Check in the list for v30 (`songs/p68/fixlist_v30.md` and its Doc). The soundness checks: `studies/soundness/soundness.py` reports sound on the v29 records; `margin.py` reads the same rule on the pools.

- 749.94 The builds themselves sit near the kept middle: a pick drawn at random from every build that lived has about 20 song-checks outside the middle half across the three songs, against about 30 for three kept songs; choosing toward a kept song does not widen it.
- 749.95 The pass on rhythm scaling is a coin flip: a fresh draw of the three picks leans past the kept 10th 44 times in 100. Turns of four bars, as kept songs leave 38 in 100 of them, take that to 1 in 1,000.
- 749.96 Read the rule on the pools, not one draw: sound when a pick drawn at random from each song's pool passes it at least 90 times in 100 (three kept songs: 93).
- 749.97 The songs repeat their bar figures less than kept songs do; with four-bar turns it is the most common lean left.
- Answered: 916 and 917 hold; 749.93 closed by the adopted rule.
- Carried open: 749.61 (6/8).
