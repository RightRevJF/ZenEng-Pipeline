# Same Time Tomorrow (fifteenth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v39 (main at aaa2470; 944, its shape from its own words, no kept song drawn). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage22.md).

## The run

- Key D (50 to 62); other keys offered: C, E.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 509 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 463, 840: the title's stresses off the beat 28.
- The pick: b0eb26f639a0, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 255, joint gate 255, words' gate 66 (at least 0.152; builds' fit quartiles [0.244, 0.304, 0.35]).
- Distance 2.629 (gate 3.918); directed readings, printed only: low surprise -2.797, sure endings 0.333, order across scales, pitch 0.83, order across scales, rhythm 0.54.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [49, 62] |
| sung notes on a beat that are chord tones, share | 0.893 |
| sung notes a beat long or more a semitone from a chord tone | 6 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 5.4 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [36, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.682 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.028] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.2, 0.57, 0.21] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.4, 0.21, 0.37] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.32 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [8.5, 2.62] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['0/65', '3/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 59, 59] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.425 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.324, 0.355, 0.095] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | -0.045 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [3.138, 53], 'six_note_share': [0.892, 46], 'five_note_share': [0.779, 41], 'time_on_tonic': [0.2, 35], 'different_pitches': [2.714, 65], 'different_intervals': [3.065, 40], 'leaps': [0.113, 43], 'range': [13.0, 84], 'repeated_notes': [0.351, 63], 'repeated_figures': [0.408, 13], 'plainness': [-0.045, 50]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.103 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 0 |
| the plan's lift | 1 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.221 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.42 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.904 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.298, 0.295], '5th': [0.146, 0.176], 'octave': [0.175, 0.155], 'unison': [0.117, 0.151], '4th': [0.152, 0.119], '6th': [0.111, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [7.0, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.323, 0.225], 'oblique': [0.272, 0.298], 'contrary': [0.038, 0.099], 'parallel': [0.228, 0.278], 'similar': [0.139, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.3, 8.6] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.0, 12.0] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.666, 0.866] |
| roughest bars | [112, 107, 20, 58, 110] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.682 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.3, 8.6] s, over 12 beats, share and longest in beats, [0.0, 12.0] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.904, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- Line ends as drawn: stressed line-final syllables an eighth or less 0.21, a half or more 0.37 (kept 0.182, 0.29); lines run on with under a beat of rest 0.32 (kept quartiles 0.095, 0.253, 0.426).
- 922 and 924, the page gate as sung: plainness -0.045, plainer than 50 kept tunes in 100; four-note figures already sung, first 120 notes, 0.103 (kept quartiles 0.241, 0.362, 0.455).
- Breaths: silences of a beat or more per 100 beats and their median, [8.5, 2.62] (kept 7.0, 9.1, 11.1). A four-bar turn after chorus 1.
- 944, the shape from the song: no kept song is drawn. Its words ask a range of 18.0 (the pick spans 13 as sung); bars on a figure already sung 0.462 and on a rhythm already sung 0.588 (written, not acted on; the pick 0.451, 0.647). Movement at the kept middle (steps 0.396, leaps 0.102, repeated notes 0.312); the pick 0.355, 0.119, 0.377. Fit kept round 4. Its top note 11 times. Rhythm scaling 0.540 (kept 10th 0.574).
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
| readback: him read back | pass (426 of 426) |
| readback: him read back | pass (426 of 426) |
| readback: harmony read back | pass (171 of 171) |
| readback: guitar read back | pass (2753 of 2753) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (426 of 426) |
| readback_score: harmony read back | pass (171 of 171) |
| readback_score: guitar read back | pass (2753 of 2753) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass (D major) |
| lead sheet: key signature is the record's | pass (\key d \major) |
| full score: PDF written, credit line | pass (5 pages) |
| full score: footer tempo and key | pass (D major) |
| full score: key signature is the record's | pass (\key d \major) |
| parts: PDF written, credit line | pass (8 pages) |
| parts: footer tempo and key | pass (D major) |
| parts: key signature is the record's | pass (\key d \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (D major: 1 = D, 2m = Em, 3m = F♯m, 4 = G, 5 = A, 6m = Bm) |
| number chart: one cell a bar, as the record | pass (118 cells) |
| MusicXML lead sheet: onsets and pitches | pass (426) |
| demo: voice notes | pass (426) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.7 dB) |
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

Numbered from 749.128; each has Problem, Evidence, Fix and Check in the list for v40 (`songs/p68/fixlist_v40.md` and its Doc). 749.123 to 749.127 are carried.

- See the list for v40: the words-to-shape features measured two ways, and the carried items.
- Carried open: 749.61 (6/8).
