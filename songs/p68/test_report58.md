# Same Time Tomorrow (third edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v25 (main at 9b149f6). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage8.md).

## The run

- Key C (48 to 59); other keys offered: D, A.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 681 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 268, 840: the title's stresses off the beat 51.
- The pick: f8464f9dee35, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 341, joint gate 341, words' gate 341 (at least 0.092; builds' fit quartiles [0.298, 0.339, 0.383]).
- Distance 2.568 (gate 4.104); directed readings, printed only: low surprise -2.838, sure endings -0.097, order across scales, pitch 0.727, order across scales, rhythm 0.55.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); 888: no turn: with one the song would run past the kept 75th of lengths; the song runs 326 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 14 fewer two-bar lines, or about 113 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [47, 59] |
| sung notes on a beat that are chord tones, share | 0.812 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 456 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [29, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 16.1 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [32, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.504 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.011] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.259, 0.424, 0.236]) | [0.2, 0.21, 0.18] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.353, 0.196, 0.273]) | [0.6, 0.43, 0.29] |
| lines that run on with under a beat of rest (kept songs [0.064, 0.2, 0.387] by quartile) | 0.2 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [10.4, 2.5] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['1/65', '2/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 57, 57] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.092, quartiles 0.202, 0.291, 0.384) | 0.265 |
| the fit by length, by place in the bar, by height (kept medians 0.132, 0.311, 0.104) | [0.11, 0.528, -0.128] |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 2.0 |
| the plan's lift | 3 |
| rest share inside sung sections, median (kept quartiles 0.21, 0.30, 0.39) | 0.301 |
| the title's stressed syllables on a beat (kept 0.73) | 0.75 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 326 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.0 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 1.0 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.297, 0.295], '5th': [0.146, 0.176], 'octave': [0.156, 0.155], 'unison': [0.151, 0.151], '4th': [0.109, 0.119], '6th': [0.141, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [7.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.135, 0.225], 'oblique': [0.219, 0.298], 'contrary': [0.157, 0.099], 'parallel': [0.326, 0.278], 'similar': [0.163, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.1, 10.0] |
| sung phrases over eight seconds | 5 |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.698, 0.903] |
| roughest bars | [102, 56, 103, 27, 57] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.504 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.75 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.36, Verse 1 0.58, Chorus 1 0.73, Verse 2 0.58, Chorus 2 0.74, Bridge 0.68, Verse 3 0.60, Last Chorus 0.76, Outro 0.56. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.1, 10.0] s, 5 over eight by the check's one-beat rule (749.83); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 1.0, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.013 (the outro's B♭ and the last chorus's A); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest. Stressed line-final syllables an eighth or less 0.19, a half or more 0.27 (kept 0.24, 0.27); lines run on with under a beat of rest 0.20 (kept 0.27); rest median 27 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 8 of 14 line ends (kept 47 to 49 in 100; 42 with tied notes read, 749.82).
- Breaths: 6.6 real breaths a minute by onsets (human median 7); silences of a beat or more 10.4 per 100 beats (CoCoPops quartiles 7.0, 9.1, 11.1), median silence 2.5 beats (CoCoPops 2.0). Phrases split at half a beat: over 12 beats 0.019 (kept 0.046), longest 13.2 beats (kept songs' longest, median 12).
- 900: the guitar under 1.0 of the sung notes.
- Length: 326 s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).
- 749.77 (not raised): stressed syllables a sixteenth long, of syllables, lines sung again 1 of 65, other lines 2 of 98.

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
| readback: guitar read back | pass (2707 of 2707) |
| readback: bass read back | pass (456 of 456) |
| readback: drums counted | pass (1344 of 1344) |
| readback_score: him read back | pass (469 of 469) |
| readback_score: harmony read back | pass (192 of 192) |
| readback_score: guitar read back | pass (2707 of 2707) |
| readback_score: bass read back | pass (456 of 456) |
| readback_score: drums counted | pass (1344 of 1344) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass |
| full score: PDF written, credit line | pass (4 pages) |
| full score: footer tempo and key | pass |
| parts: PDF written, credit line | pass (8 pages) |
| parts: footer tempo and key | pass |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| number chart: one cell a bar, as the record | pass (114 cells) |
| MusicXML lead sheet: onsets and pitches | pass (469) |
| demo: voice notes | pass (469) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+7.4 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.76, top Last Chorus 0.76 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

Numbered from 749.82; each has Problem, Evidence, Fix and Check in the fix list for v26 (`songs/p68/fixlist_v26.md` and its Doc).

- 749.82 The CoCoPops parser drops every note that begins a tie, with its syllable; the kept tables built since 895 shift when the ties are read.
- 749.83 The phrase check counts a breath only at a beat of silence; kept singers breathe in half a beat, and on that rule the songs match the kept.
- Answered: 901 recounted (the retirement of 871 and 890 stands); 749.77 closed with a kept figure for returning lines.
- Carried open: 749.61 (6/8).
