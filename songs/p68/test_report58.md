# Same Time Tomorrow (eleventh edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v33 (main at a1e6d2f). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage20.md).

## The run

- Key E (52 to 59); other keys offered: D, Eb.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 606 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 366, 840: the title's stresses off the beat 27, 731: stressed syllables on the beat too few 1.
- The pick: 4f5787b0b11c, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 303, joint gate 298, words' gate 81 (at least 0.152; builds' fit quartiles [0.192, 0.253, 0.301]).
- Distance 3.174 (gate 3.918); directed readings, printed only: low surprise -2.709, sure endings 0.469, order across scales, pitch 0.856, order across scales, rhythm 0.547.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [51, 59] |
| sung notes on a beat that are chord tones, share | 0.879 |
| sung notes a beat long or more a semitone from a chord tone | 2 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 15.6 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [33, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.554 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.006] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.0, 0.64, 0.13] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.4, 0.0, 0.26] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.14 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [10.7, 3.0] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['4/65', '1/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 57, 57] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.34 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.248, 0.28, 0.065] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 0.515 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.649, 83], 'six_note_share': [0.679, 5], 'five_note_share': [0.679, 13], 'time_on_tonic': [0.368, 86], 'different_pitches': [2.104, 94], 'different_intervals': [2.712, 75], 'leaps': [0.028, 96], 'range': [8.0, 99], 'repeated_notes': [0.371, 70], 'repeated_figures': [0.516, 36], 'plainness': [0.515, 81]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.362 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 2 |
| the plan's lift | 0 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.327 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.25 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.983 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.295, 0.295], '5th': [0.187, 0.176], 'octave': [0.166, 0.155], 'unison': [0.124, 0.151], '4th': [0.124, 0.119], '6th': [0.104, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [6.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.2, 0.225], 'oblique': [0.229, 0.298], 'contrary': [0.149, 0.099], 'parallel': [0.263, 0.278], 'similar': [0.16, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 8.9] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.019, 12.5] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.634, 0.788] |
| roughest bars | [62, 115, 104, 31, 28] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.554 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.9, 8.9] s, over 12 beats, share and longest in beats, [0.019, 12.5] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.983, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.14, a half or more 0.24 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.14 (kept 0.295); rest median 31.5 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 3 of 14 line ends (kept 42 in 100, ties read). 922 and 924, the page gate read as sung: plainness 0.515, plainer than 81 kept tunes in 100 (floor, the kept 10th, -0.64; all 81 builds read pass); four-note figures already sung 0.516 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.362 (0.241, 0.362, 0.455).
- Breaths: silences of a beat or more 10.7 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 12.5 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1.
- 920, 925 to 930, the aim: the song aims at the kept song Bird Dog. Steps 0.464 (Bird Dog 0.398; the step weight fitted to its limit, 0.3); leaps 0.028 (0.057); repeated notes 0.371 (0.373); longest run of one pitch 8 (9; no build removed by the run gate); chorus over verse 2 semitones (0). Range 8 (9): the tune spans D sharp to B and sits on its top note 32 times, 8 notes in 100 (Bird Dog twice; kept 90th 8.7 in 100); the title is sung on one pitch. Bars on a figure already sung 0.253 (0.698), on a rhythm already sung 0.411 (0.774), distinct rhythms 0.589 (0.226): the repeats still do not follow the aim (749.109, waiting on 749.104). Melismas drawn at 16.2 syllables in 100; Bird Dog has none (749.110).
- 900: the guitar under 1.0 of the sung notes.
- Length: 337 s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).
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
| readback: him read back | pass (467 of 467) |
| readback: him read back | pass (467 of 467) |
| readback: harmony read back | pass (193 of 193) |
| readback: guitar read back | pass (2740 of 2740) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (467 of 467) |
| readback_score: harmony read back | pass (193 of 193) |
| readback_score: guitar read back | pass (2740 of 2740) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (3 pages) |
| lead sheet: footer tempo and key | pass (E major) |
| lead sheet: key signature is the record's | pass (\key e \major) |
| full score: PDF written, credit line | pass (6 pages) |
| full score: footer tempo and key | pass (E major) |
| full score: key signature is the record's | pass (\key e \major) |
| parts: PDF written, credit line | pass (9 pages) |
| parts: footer tempo and key | pass (E major) |
| parts: key signature is the record's | pass (\key e \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (E major: 1 = E, 2m = F♯m, 3m = G♯m, 4 = A, 5 = B, 6m = C♯m) |
| number chart: one cell a bar, as the record | pass (118 cells) |
| MusicXML lead sheet: onsets and pitches | pass (467) |
| demo: voice notes | pass (467) |
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

Numbered from 749.110; each has Problem, Evidence, Fix and Check in the list for v34 (`songs/p68/fixlist_v34.md` and its Doc).

- 749.110 The step weight acts on the lines drawn fresh, about 13 notes in 100; at its limits it pushes them past any kept song (song 58's fresh lines step 11 times in 100, song 54's 79) to move the song a little. Song 58's melismas, drawn at the kept upper quartile where Bird Dog has none, add 13 points of steps on their own.
- 749.111 The range is a wall, not a peak: song 55's builds reach a register top 15 times in 100 and span 15 against 19; song 58's pick spans 8 against 9 and sits on its top note 32 times. Kept tunes reach their top a median 4 times.
- 749.112 The record's stats count the 930 trial builds with the run's (160, 480, 480 more builds), so per-build rates read from it, and the paper's counts of first notes moved, run high.
- Answered: 928 to 930 hold as written. Carried: 749.104's fix (749.109 and 749.101 wait on it), 749.103 (1.46 against the kept 10.5), the two readings of repeated figures.
- Carried open: 749.61 (6/8).
