# Same Time Tomorrow (sixteenth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v41 (main at d498055; its shape from its own words, read one way, 946). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage22.md).

## The run

- Key A (45 to 57); other keys offered: C, B.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 508 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 455, 840: the title's stresses off the beat 36, 731: stressed syllables on the beat too few 1.
- The pick: aa7488e5c24d, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 254, joint gate 254, words' gate 71 (at least 0.152; builds' fit quartiles [0.247, 0.304, 0.356]).
- Distance 3.095 (gate 3.918); directed readings, printed only: low surprise -2.709, sure endings 0.686, order across scales, pitch 0.756, order across scales, rhythm 0.558.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [45, 57] |
| sung notes on a beat that are chord tones, share | 0.926 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 5.2 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [29, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.695 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.026] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.8, 0.21, 0.29] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.2, 0.29, 0.21] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.18 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [10.3, 2.75] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['3/65', '1/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 57, 54] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.385 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.321, 0.369, 0.061] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 0.781 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.681, 80], 'six_note_share': [0.821, 24], 'five_note_share': [0.788, 42], 'time_on_tonic': [0.52, 100], 'different_pitches': [2.127, 94], 'different_intervals': [2.593, 83], 'leaps': [0.068, 76], 'range': [12.0, 90], 'repeated_notes': [0.344, 61], 'repeated_figures': [0.563, 50], 'plainness': [0.781, 88]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.397 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 0.0 |
| the plan's lift | 1 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.247 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.43 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 1.0 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.31, 0.295], '5th': [0.185, 0.176], 'octave': [0.137, 0.155], 'unison': [0.155, 0.151], '4th': [0.137, 0.119], '6th': [0.077, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [3.3, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.267, 0.225], 'oblique': [0.273, 0.298], 'contrary': [0.187, 0.099], 'parallel': [0.193, 0.278], 'similar': [0.08, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 1 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 7.9] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.0, 11.0] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.719, 0.907] |
| roughest bars | [57, 112, 66, 113, 109] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.695 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.9, 7.9] s, over 12 beats, share and longest in beats, [0.0, 11.0] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 1.0, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- Line ends as drawn: stressed line-final syllables an eighth or less 0.29, a half or more 0.21 (kept 0.182, 0.29); lines run on with under a beat of rest 0.18 (kept quartiles 0.095, 0.253, 0.426).
- 922 and 924, the page gate as sung: plainness 0.781, plainer than 88 kept tunes in 100; four-note figures already sung, first 120 notes, 0.397 (kept quartiles 0.241, 0.362, 0.455).
- Breaths: silences of a beat or more per 100 beats and their median, [10.3, 2.75] (kept 7.0, 9.1, 11.1). A four-bar turn after chorus 1.
- 944, the shape from the song: no kept song is drawn. Its words ask a range of 19.9 (the pick spans 12 as sung); bars on a figure already sung 0.412 and on a rhythm already sung 0.545 (written, not acted on; the pick 0.464, 0.608). Movement at the kept middle (steps 0.396, leaps 0.102, repeated notes 0.319); the pick 0.444, 0.069, 0.382. Fit kept round 4. Its top note 8 times. Rhythm scaling 0.558 (kept 10th 0.574).
- 900: the guitar under 1.0 of the sung notes.
- Length: 337 s, past the kept 75th (243); 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).
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
| readback: him read back | pass (425 of 425) |
| readback: him read back | pass (425 of 425) |
| readback: harmony read back | pass (168 of 168) |
| readback: guitar read back | pass (2822 of 2822) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (425 of 425) |
| readback_score: harmony read back | pass (168 of 168) |
| readback_score: guitar read back | pass (2822 of 2822) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass (A major) |
| lead sheet: key signature is the record's | pass (\key a \major) |
| full score: PDF written, credit line | pass (4 pages) |
| full score: footer tempo and key | pass (A major) |
| full score: key signature is the record's | pass (\key a \major) |
| parts: PDF written, credit line | pass (9 pages) |
| parts: footer tempo and key | pass (A major) |
| parts: key signature is the record's | pass (\key a \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (A major: 1 = A, 2m = Bm, 3m = C♯m, 4 = D, 5 = E, 6m = F♯m) |
| number chart: one cell a bar, as the record | pass (118 cells) |
| MusicXML lead sheet: onsets and pitches | pass (425) |
| demo: voice notes | pass (425) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.3 dB) |
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

Numbered from 749.131; each has Problem, Evidence, Fix and Check in the list for v42 (`songs/p68/fixlist_v42.md` and its Doc).

- See the list for v42.
- Carried open: 749.61 (6/8).
