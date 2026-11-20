# Same Time Tomorrow (thirteenth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v36 (main at a006166). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage22.md).

## The run

- Key E (52 to 61); other keys offered: D, Eb.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 633 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 333, 840: the title's stresses off the beat 33, 731: stressed syllables on the beat too few 1.
- The pick: c25a55d3037f, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 317, joint gate 316, words' gate 88 (at least 0.152; builds' fit quartiles [0.265, 0.319, 0.372]).
- Distance 2.386 (gate 3.918); directed readings, printed only: low surprise -2.733, sure endings 0.127, order across scales, pitch 0.788, order across scales, rhythm 0.541.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [52, 61] |
| sung notes on a beat that are chord tones, share | 0.908 |
| sung notes a beat long or more a semitone from a chord tone | 3 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 1.0 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [25, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.697 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.0] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.4, 0.43, 0.34] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.2, 0.0, 0.18] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.29 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [8.9, 2.25] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['4/65', '5/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 61, 59] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.43 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.314, 0.35, 0.161] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 0.31 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.941, 69], 'six_note_share': [0.868, 36], 'five_note_share': [0.794, 43], 'time_on_tonic': [0.27, 57], 'different_pitches': [2.394, 87], 'different_intervals': [2.807, 67], 'leaps': [0.12, 36], 'range': [9.0, 98], 'repeated_notes': [0.364, 67], 'repeated_figures': [0.468, 25], 'plainness': [0.31, 74]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.233 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 2.0 |
| the plan's lift | 0 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.236 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.46 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.939 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.303, 0.295], '5th': [0.182, 0.176], 'octave': [0.158, 0.155], 'unison': [0.139, 0.151], '4th': [0.115, 0.119], '6th': [0.103, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [5.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.288, 0.225], 'oblique': [0.346, 0.298], 'contrary': [0.118, 0.099], 'parallel': [0.163, 0.278], 'similar': [0.085, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [42, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.5, 9.1] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.019, 12.8] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.593, 0.764] |
| roughest bars | [105, 59, 25, 28, 108] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.697 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.5, 9.1] s, over 12 beats, share and longest in beats, [0.019, 12.8] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.939, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.35, a half or more 0.19 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.29 (kept 0.295); rest median 15 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 1 of 14 line ends (kept 42 in 100, ties read). 922 and 924, the page gate read as sung: plainness 0.31, plainer than 74 kept tunes in 100 (floor, the kept 10th, -0.64; all 88 builds read pass); four-note figures already sung 0.468 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.233 (0.241, 0.362, 0.455).
- Breaths: silences of a beat or more 8.9 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 12.75 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1.
- 920, 925 to 939, the aim: the song aims at the kept song Bird Dog. Moves fitted: step 1.317, leap 2.585, repeat 0.707. Steps 0.408 (Bird Dog 0.398); leaps 0.12 (0.057); repeated notes 0.364 (0.373); chorus over verse 2 semitones (0). Range 9 (9): the tune sits on its top note 25 times (Bird Dog twice). Bars on a figure already sung 0.382 (0.698), on a rhythm already sung 0.549 (0.774), distinct rhythms 0.451 (0.226). Rhythm scaling 0.541 and range 9 are under the kept 10th (0.574, 12).
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
| readback: him read back | pass (408 of 408) |
| readback: him read back | pass (408 of 408) |
| readback: harmony read back | pass (165 of 165) |
| readback: guitar read back | pass (2718 of 2718) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (408 of 408) |
| readback_score: harmony read back | pass (165 of 165) |
| readback_score: guitar read back | pass (2718 of 2718) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (3 pages) |
| lead sheet: footer tempo and key | pass (E major) |
| lead sheet: key signature is the record's | pass (\key e \major) |
| full score: PDF written, credit line | pass (5 pages) |
| full score: footer tempo and key | pass (E major) |
| full score: key signature is the record's | pass (\key e \major) |
| parts: PDF written, credit line | pass (9 pages) |
| parts: footer tempo and key | pass (E major) |
| parts: key signature is the record's | pass (\key e \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (E major: 1 = E, 2m = F♯m, 3m = G♯m, 4 = A, 5 = B, 6m = C♯m) |
| number chart: one cell a bar, as the record | pass (118 cells) |
| MusicXML lead sheet: onsets and pitches | pass (408) |
| demo: voice notes | pass (408) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.1 dB) |
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

Numbered from 749.120; each has Problem, Evidence, Fix and Check in the list for v37 (`songs/p68/fixlist_v37.md` and its Doc).

- See the list for v37 (`songs/p68/fixlist_v37.md`): the random pool pick's rate and its spread, the fit's joint band test, the returning lines' repeats, and the answer on 749.104 and 749.103.
- Carried open: 749.61 (6/8).
