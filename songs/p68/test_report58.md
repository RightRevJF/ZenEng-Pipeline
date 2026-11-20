# Same Time Tomorrow (tenth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v32 (main at 91db1a6). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage19.md).

## The run

- Key E (52 to 61); other keys offered: D, Eb.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 455 of 1000 builds survive; deaths 926: a run of one pitch longer than the kept song's longest, across the lines 278, 838: the chorus's lift is not the plan's 247, 840: the title's stresses off the beat 19, 731: stressed syllables on the beat too few 1.
- The pick: 43493945f523, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 228, joint gate 228, words' gate 76 (at least 0.152; builds' fit quartiles [0.211, 0.265, 0.31]).
- Distance 2.82 (gate 3.918); directed readings, printed only: low surprise -2.709, sure endings -0.246, order across scales, pitch 0.632, order across scales, rhythm 0.541.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [51, 61] |
| sung notes on a beat that are chord tones, share | 0.894 |
| sung notes a beat long or more a semitone from a chord tone | 2 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 14.9 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [38, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.677 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.011] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.4, 0.43, 0.34] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.2, 0.0, 0.18] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.29 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [8.9, 2.25] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['4/65', '5/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 61, 59] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.363 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.199, 0.35, 0.126] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 0.353 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.936, 69], 'six_note_share': [0.752, 17], 'five_note_share': [0.752, 33], 'time_on_tonic': [0.377, 87], 'different_pitches': [2.223, 90], 'different_intervals': [2.758, 71], 'leaps': [0.097, 54], 'range': [10.0, 95], 'repeated_notes': [0.363, 67], 'repeated_figures': [0.465, 25], 'plainness': [0.353, 76]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.293 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 2 |
| the plan's lift | 0 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.236 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.24 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.981 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.323, 0.295], '5th': [0.18, 0.176], 'octave': [0.159, 0.155], 'unison': [0.101, 0.151], '4th': [0.132, 0.119], '6th': [0.106, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [3.9, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.3, 0.225], 'oblique': [0.283, 0.298], 'contrary': [0.106, 0.099], 'parallel': [0.194, 0.278], 'similar': [0.117, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.5, 9.1] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.019, 12.8] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.627, 0.788] |
| roughest bars | [105, 59, 112, 66, 114] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.677 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [4.5, 9.1] s, over 12 beats, share and longest in beats, [0.019, 12.8] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.981, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.35, a half or more 0.19 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.29 (kept 0.295); rest median 15 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 1 of 14 line ends (kept 42 in 100, ties read; 6 of 14 under v31). 922 and 924, the page gate read as sung: plainness 0.353, plainer than 76 kept tunes in 100 (floor, the kept 10th, -0.64; all 76 builds read pass); four-note figures already sung 0.465 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.293 (0.241, 0.362, 0.455).
- Breaths: silences of a beat or more 8.9 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 12.75 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1.
- 920, 925 to 927, the aim: the song aims at the kept song Bird Dog. Range 10 (Bird Dog 9); longest run of one pitch 9 (9); repeated notes 0.363 (0.373); chorus over verse 2 semitones (its lift 0, the plan's gate allows two). It does not follow Bird Dog's repetition: bars on a figure already sung 0.184 (0.698), bars on a rhythm already sung 0.282 (0.774), distinct rhythms over bars 0.718 (0.226), all three beyond the kept 10th to 90th on the far side from Bird Dog (749.109).
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
| readback: him read back | pass (464 of 464) |
| readback: him read back | pass (464 of 464) |
| readback: harmony read back | pass (189 of 189) |
| readback: guitar read back | pass (2745 of 2745) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (464 of 464) |
| readback_score: harmony read back | pass (189 of 189) |
| readback_score: guitar read back | pass (2745 of 2745) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (3 pages) |
| lead sheet: footer tempo and key | pass (E major) |
| lead sheet: key signature is the record's | pass (\key e \major) |
| full score: PDF written, credit line | pass (6 pages) |
| full score: footer tempo and key | pass (E major) |
| full score: key signature is the record's | pass (\key e \major) |
| parts: PDF written, credit line | pass (10 pages) |
| parts: footer tempo and key | pass (E major) |
| parts: key signature is the record's | pass (\key e \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (E major: 1 = E, 2m = F♯m, 3m = G♯m, 4 = A, 5 = B, 6m = C♯m) |
| number chart: one cell a bar, as the record | pass (118 cells) |
| MusicXML lead sheet: onsets and pitches | pass (464) |
| demo: voice notes | pass (464) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.0 dB) |
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

Numbered from 749.105; each has Problem, Evidence, Fix and Check in the list for v33 (`songs/p68/fixlist_v33.md` and its Doc).

- 749.105 (a fault) The hymn engine cannot run: 926's run cap is set only when a 4/4 engine is made, so song 53 stops with an error. The cap is also shared by every engine in one process.
- 749.106 926 passes over two builds in three in song 54, mostly one note over the cap, and mostly where the draw does not check (a copied line's join, a melisma); the builds it passes over repeat their figures more.
- 749.107 The page floor keeps range and leaps: without them it passes over 6 of 44 in song 55 instead of 7, and the pick is the same; the builds it passes over are surprising and repeat little.
- 749.108 The steps do not follow the aim: one weight for every song, so song 58's builds step more than Bird Dog and song 54's less than its aim.
- 749.109 The repeats and the rhythm do not follow the aim: song 58 aims at a kept song that repeats its bars more than nine kept songs in ten and repeats them less than nine in ten.
- Answered: 924 to 927 hold as written (the floor reads as sung; the lift, the run, the range follow the aimed song). Carried: 749.103 (two-sided variety 1.18 against the kept 10.5), 749.104's fix, 749.101.
- Carried open: 749.61 (6/8).
