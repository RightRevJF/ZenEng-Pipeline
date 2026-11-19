# Same Time Tomorrow (second edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v24 (main at cc03065). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage8.md).

## The run

- Key C (48 to 60); other keys offered: A, D.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 638 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 273, 840: the title's stresses off the beat 89.
- The pick: 5a718dae4282, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 319, joint gate 319, words' gate 319 (at least 0.092; builds' fit quartiles [0.282, 0.322, 0.358]).
- Distance 3.503 (gate 4.104); directed readings, printed only: low surprise -2.751, sure endings -0.319, order across scales, pitch 0.905, order across scales, rhythm 0.443.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); 888: no turn: with one the song would run past the kept 75th of lengths; the song runs 326 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 14 fewer two-bar lines, or about 113 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [47, 60] |
| sung notes on a beat that are chord tones, share | 0.882 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 456 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [29, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 16.1 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [32, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.471 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.019] |
| a song with blue notes | False |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.092, quartiles 0.202, 0.291, 0.384) | 0.281 |
| the fit by length, by place in the bar, by height (kept medians 0.132, 0.311, 0.104) | [-0.035, 0.409, 0.141] |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 3.0 |
| the plan's lift | 3 |
| rest share inside sung sections, median (kept quartiles 0.21, 0.30, 0.39) | 0.236 |
| the title's stressed syllables on a beat (kept 0.73) | 0.75 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 326 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.33 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 0.917 |
| sung notes with accompaniment above them, share | 0.917 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.258, 0.295], '5th': [0.157, 0.176], 'octave': [0.172, 0.155], 'unison': [0.182, 0.151], '4th': [0.116, 0.119], '6th': [0.116, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [11.0, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.126, 0.225], 'oblique': [0.304, 0.298], 'contrary': [0.178, 0.099], 'parallel': [0.288, 0.278], 'similar': [0.105, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 5.7] |
| sung phrases over eight seconds | 0 |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.675, 0.912] |
| roughest bars | [27, 56, 30, 106, 28] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.471 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.75 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.55, Chorus 1 0.70, Verse 2 0.55, Chorus 2 0.72, Bridge 0.63, Verse 3 0.57, Last Chorus 0.73, Outro 0.55. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.9, 5.7] s, none over eight; the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. Accompaniment above a sung note 0.917: the guitar now plays in its own register (892), and the 2-in-100 rule was measured on piano (749.79).
- Two channels and chromatic harmony: chords from outside the key, share 0.013157894736842105 (the outro's B♭ and the last chorus's A); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 887: rests between lines of a section, median 24 twelfths, 11 of 50 exactly a quarter (749.58 closed in 4/4). But stressed line-final notes an eighth or less 0.44 (kept 0.22), a half or more 0.11 (kept 0.31); weak line-final syllables an eighth or less 0.85 (kept 0.40) (749.76).
- 890: no line-final word holds its weak syllable longer (0 of 14; “completely” mended).
- 891: stressed syllables a sixteenth long in lines sung again 6 of 72, against 9 of 111 in the other lines.
- 892: the guitar sounds under 0.917 of the sung notes; none a second away.
- 893: the harmony voice 40 to 57 (E2 is 40).
- Breaths: 7.6 real breaths a minute by onsets (human median 7); by durations 13.0 silences of a beat or more per 100 beats (CoCoPops quartiles 7.0, 9.1, 11.1), median silence 2 beats (CoCoPops 2.0) (749.80).
- Length: 326 s, the flag and the check agreeing (894); 2 bars in, 4 out, no turn (888).
- The pick's fit by length -0.035 (kept median 0.132) (749.81).

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
| readback: harmony read back | pass (198 of 198) |
| readback: guitar read back | pass (2601 of 2601) |
| readback: bass read back | pass (456 of 456) |
| readback: drums counted | pass (1344 of 1344) |
| readback_score: him read back | pass (469 of 469) |
| readback_score: harmony read back | pass (198 of 198) |
| readback_score: guitar read back | pass (2601 of 2601) |
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
| demo: voice at least 3 dB over the band | pass (+7.6 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.73, top Last Chorus 0.73 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

Numbered from 749.76; each has Problem, Evidence, Fix and Check in the fix list for v25 (`songs/p68/fixlist_v25.md` and its Doc).

- 749.76 887 gives the rest its kept length by cutting the line's last note below the kept lengths.
- 749.77 891 is not enough in song 54: stressed syllables a sixteenth long in lines sung again 14 of 131, against 5 of 82 in its other lines.
- 749.78 871 is a weight, not a rule: song 55's “summers” holds its weak syllable twice as long as the stressed one.
- 749.79 892 leaves a third of song 54's sung notes with no guitar; the old above-the-tune check still prints against guitars.
- 749.80 The voice now breathes after nearly every line: silences of a beat or more above the kept 75th in all three 4/4 songs.
- 749.81 Song 58's pick: fit by length -0.035; song 55's flags print one line twice.
- 749.75 answered with kept evidence (last choruses are longer, a little louder, sometimes higher; rarely denser or in a new key); song 58 meets 9.12 under v24.
- Carried open: 749.61 (6/8).
