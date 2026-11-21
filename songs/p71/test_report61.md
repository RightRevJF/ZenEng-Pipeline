# This Side of the Door (first edition): test report

Words and music: Jason Bryant

Song 61 (songs/p71), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v44 (main at 3b83673). This report is the engine's record; the songbook is for musicians. The arrangement (fingerpicked guitar, cello, strings, bass, the harmony voice in the last chorus) is the writer's, written from the engine's chords, bass line and harmony voice; no sung note is changed.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 80, voice alto, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The verse sung closer (Review 29's ruling, `LUTHIER_VERSE_CLOSER=apart`) was run too and gives the same record byte for byte: no verse line of 6 to 8 syllables stands apart from another (the verses run 8.6 syllables a line).

## The run

- Key E (55 to 71); other keys offered: G, F.
- Chords: draft 1 of 12, charge 0.0.
- Melody: 326 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 523, 840: the title's stresses off the beat 147, 731: stressed syllables on the beat too few 4.
- The pick: 2573b5e71acf; the first build past the gates spans 15, under the floor (15.52, the words ask 18.9), so the pick is the first at or over it, spanning 16 (954). Commonest pitch {'Verse': 0.387, 'Chorus': 0.388} (956 ceiling {'Verse': 0.44, 'Chorus': 0.479}). Gates: old charge's least half 163, joint gate 163, words' gate 44 (at least 0.152; builds' fit quartiles [0.196, 0.238, 0.29]).
- Distance 2.567 (gate 3.918); directed readings, printed only: low surprise -2.778, sure endings -0.144, order across scales, pitch 0.905, order across scales, rhythm 0.591.
- Flags: 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 264 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 3 fewer two-bar lines, or about 87 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [54, 71] |
| sung notes on a beat that are chord tones, share | 0.906 |
| sung notes a beat long or more a semitone from a chord tone | 1 |
| bass notes | 352 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [30, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 6.5 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 29); on a word's end (kept 94) | [35, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.652 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.021, 0.018, 0.13] |
| a song with blue notes | True |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.38, 0.33, 0.16] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.25, 0.17, 0.36] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.21 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [9.3, 2.88] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['12/44', '15/74'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 16, 71, 71] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.363 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.266, 0.242, 0.075] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | -0.224 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [3.377, 35], 'six_note_share': [0.83, 25], 'five_note_share': [0.806, 44], 'time_on_tonic': [0.145, 17], 'different_pitches': [2.82, 56], 'different_intervals': [2.974, 50], 'leaps': [0.052, 84], 'range': [17.0, 60], 'repeated_notes': [0.258, 40], 'repeated_figures': [0.38, 10], 'plainness': [-0.224, 37]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.241 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 2 |
| the plan's lift | 1 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.264 |
| the title's stressed syllables on a beat (kept 0.73) | 0.6 |
| title lines | 2 |
| length in seconds (kept quartiles 165, 206, 243) | 264 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.43 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.264 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.339, 0.295], '5th': [0.182, 0.176], 'octave': [0.14, 0.155], 'unison': [0.132, 0.151], '4th': [0.107, 0.119], '6th': [0.099, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [3.5, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.254, 0.225], 'oblique': [0.289, 0.298], 'contrary': [0.105, 0.099], 'parallel': [0.246, 0.278], 'similar': [0.105, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [51, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.7, 9.4] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.027, 12.5] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.549, 0.75] |
| roughest bars | [81, 24, 73, 70, 64] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.652 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.6 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 1 0.86, Verse 2 0.78, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.52, Verse 1 0.53, Chorus 1 0.56, Turn 1 0.55, Verse 2 0.66, Bridge 0.97, Verse 3 0.61, Last Chorus 0.93, Outro 0.46. Each chorus is above its verse: met; the top is the bridge (0.97), the arrangement's peak, and the last chorus falls away at its last two lines by design.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.7, 9.4] s, over 12 beats, share and longest in beats, [0.027, 12.5] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.264, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- Line ends as drawn: stressed line-final syllables an eighth or less 0.16, a half or more 0.36 (kept 0.182, 0.29); lines run on with under a beat of rest 0.21 (kept quartiles 0.095, 0.253, 0.426).
- 922 and 924, the page gate as sung: plainness -0.224, plainer than 37 kept tunes in 100; four-note figures already sung, first 120 notes, 0.241 (kept quartiles 0.241, 0.362, 0.455).
- Breaths: silences of a beat or more per 100 beats and their median, [9.3, 2.88] (kept 7.0, 9.1, 11.1). A four-bar turn after chorus 1.
- 944, the shape from the song: no kept song is drawn. Its words ask a range of 18.9 (the pick spans 17 as sung); bars on a figure already sung 0.330 and on a rhythm already sung 0.451 (written, not acted on; the pick 0.378, 0.473). Movement at the kept middle (steps 0.396, leaps 0.102, repeated notes 0.319); the pick 0.372, 0.049, 0.291. Fit kept round 3. Its top note 2 times. Rhythm scaling 0.591 (kept 10th 0.574).
- 900: the guitar under 1.0 of the sung notes.
- Length: 264 s, past the kept 75th (243), after the writer cut the lyric from 56 lines to 39 to reach about four minutes.
- 749.77 (closed): with ties read, kept stressed syllables a sixteenth long inside lines, first verse and chorus 0.109, later ones 0.108.

## The documents

Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:

| Check | Result |
|---|---|
| the document record is the song record: sung notes | pass |
| harmony notes are the engine's, in the last chorus only, until its seventh line | pass (48 of the engine's 121) |
| bass notes are the engine's | pass (96 of 352) |
| guitar: every picked note a tone of its half-bar's chord | pass |
| cello: every note its chord's root | pass |
| strings: every note a tone of its chord | pass |
| the arrangement: strings, bass and harmony stop at “Three, and then two” | pass (bar 81) |
| the arrangement: the outro the guitar alone | pass |
| the arrangement: the cello from verse 2, the strings and bass from the bridge | pass |
| the arrangement: no drums | pass |
| bars and chords | pass |
| every sung line spells its locked line | pass (39 lines) |
| readback: him read back | pass (330 of 330) |
| readback: him read back | pass (330 of 330) |
| readback: harmony read back | pass (48 of 48) |
| readback: guitar read back | pass (699 of 699) |
| readback: cello read back | pass (73 of 73) |
| readback: strings read back | pass (65 of 65) |
| readback: bass read back | pass (96 of 96) |
| readback_score: him read back | pass (330 of 330) |
| readback_score: harmony read back | pass (48 of 48) |
| readback_score: guitar read back | pass (699 of 699) |
| readback_score: strings read back | pass (65 of 65) |
| readback_score: cello read back | pass (73 of 73) |
| readback_score: bass read back | pass (96 of 96) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass (E major) |
| lead sheet: key signature is the record's | pass (\key e \major) |
| full score: PDF written, credit line | pass (4 pages) |
| full score: footer tempo and key | pass (E major) |
| full score: key signature is the record's | pass (\key e \major) |
| parts: PDF written, credit line | pass (8 pages) |
| parts: footer tempo and key | pass (E major) |
| parts: key signature is the record's | pass (\key e \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (E major: 1 = E, 2m = F♯m, 3m = G♯m, 4 = A, 5 = B, 6m = C♯m) |
| number chart: one cell a bar, as the record | pass (88 cells) |
| MusicXML lead sheet: onsets and pitches | pass (330) |
| demo: voice notes | pass (330) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: cello notes | pass |
| demo: string notes | pass |
| demo: no drum track | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+9.7 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| energy arc: the bridge or the last chorus the top, the music opening up | pass (bridge 0.97, last chorus 0.93) |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.93, top Bridge 0.97 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 7) |

## Findings

For the next list (after 749.145):

- 749.146: the verse lever (749.142's form) reaches no line here. Song 61's verse lines run 8 to 11 syllables, so none is a candidate; song 59's run under 6. Two songs of the last three are outside the lever's 6 to 8. The engine gives a 9-syllable line two bars as it gives a 6-syllable one.
- 749.147: a four-syllable line in a two-bar slot puts its length on its weak words. “Three, and then two” (verse 3 and the last chorus) sings “three” for a quarter of a beat and holds “and” two and a quarter beats and “then” three and a quarter. The words' fit passes the tune (0.363), so the fit does not read where a short line's length falls.
- 749.144 again: the lyric's room reads 0.06 bars unsung (kept 0.12 to 0.28) even after the cut; the four-bar turn after the first chorus is the song's only rest.
- Carried open: 749.61 (6/8).
