# Before the Bread Goes Cold (first edition): test report

Words and music: Jason Bryant

Song 59 (songs/p69), the hold-out test of Luthier v34 as merged (main at b6bf0e9): written end to end from a new lyric with `lib/luthier/song_from_lyric.py`, with no change to the engine during the song and the pick taken as drawn. This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 120, voice baritone, lead guitar, mode major, genre rock, seed 1. Nothing else was typed or chosen by hand. The record was written once, on main at b6bf0e9, and not changed.

## The run

- Key A (45 to 64); other keys offered: G, Ab.
- Chords: draft 9 of 12, charge 0.0.
- Melody: 138 of 1000 builds survive; deaths rhythm: the syllables cannot fit the window 500, 838: the chorus's lift is not the plan's 329, 840: the title's stresses off the beat 28, join before a copy (780) 2, 751: two notes on one onset, or a note of no length 2, 926: a run of one pitch longer than the kept song's longest, across the lines 1.
- The pick: 6290c71743e3, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 69, joint gate 69, words' gate 20 (at least 0.152; builds' fit quartiles [0.228, 0.272, 0.329]).
- Distance 1.751 (gate 3.918); directed readings, printed only: low surprise -2.907, sure endings 0.251, order across scales, pitch 0.905, order across scales, rhythm 0.656.
- Flags: Verse 1 line 1: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 2: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 3: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 4: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 5: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 6: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 7: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 1 line 8: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 1: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 2: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 3: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 4: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 5: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 6: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 7: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Verse 2 line 8: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760); Bridge line 3: a slot of 3 bars, past the kept two-bar windows: set by weighted placement (760).

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [44, 64] |
| sung notes on a beat that are chord tones, share | 0.935 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 480 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 7.2 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 28); on a word's end (kept 94) | [16, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.672 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.049] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.43, 0.0, 0.2] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.0, 0.4, 0.13] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.37 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [6.2, 2.5] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['1/40', '4/109'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [14, 10, 54, 54] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.349 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.222, 0.369, 0.09] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | -0.084 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [3.568, 25], 'six_note_share': [0.943, 69], 'five_note_share': [0.8, 44], 'time_on_tonic': [0.373, 87], 'different_pitches': [2.802, 58], 'different_intervals': [3.101, 34], 'leaps': [0.136, 26], 'range': [20.0, 32], 'repeated_notes': [0.32, 55], 'repeated_figures': [0.434, 16], 'plainness': [-0.084, 46]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.172 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 3.0 |
| the plan's lift | 3 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.202 |
| the title's stressed syllables on a beat (kept 0.73) | 0.5 |
| title lines | 4 |
| length in seconds (kept quartiles 165, 206, 243) | 240 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.78 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.965 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.302, 0.295], '5th': [0.112, 0.176], 'octave': [0.164, 0.155], 'unison': [0.19, 0.151], '4th': [0.147, 0.119], '6th': [0.086, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [8.0, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.239, 0.225], 'oblique': [0.31, 0.298], 'contrary': [0.133, 0.099], 'parallel': [0.204, 0.278], 'similar': [0.115, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 1 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.2, 7.0] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.049, 14.0] |
| kicks with a bass note on them, share | 0.664 |
| roughness at sung onsets (median, 90th percentile) | [0.736, 0.968] |
| roughest bars | [76, 101, 71, 106, 103] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.672 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.5 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 1 0.86, Verse 2 0.78, Chorus 2 1.0, Break 0.86, Bridge 0.94, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.13, Verse 1 0.29, Chorus 1 0.46, Turn 1 0.33, Verse 2 0.29, Chorus 2 0.46, Break 0.64, Bridge 0.42, Last Chorus 0.47, Outro 0.28. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.2, 7.0] s, over 12 beats, share and longest in beats, [0.049, 14.0] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.965, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.21, a half or more 0.10 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.37 (kept 0.295); rest median 12 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 5 of 5 line ends (kept 42 in 100, ties read). 922 and 924, the page gate read as sung: plainness -0.084, plainer than 46 kept tunes in 100 (floor -0.64; 19 of 20 builds read pass); four-note figures already sung 0.434 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.172 (0.241, 0.362, 0.455).
- Breaths: silences of a beat or more 6.2 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 14 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1; an eight-bar break after chorus 2, the lead guitar on verse 1's tune.
- 920, 925 to 933, the aim: the song aims at the kept song Two Hearts (Phil Collins, 1989). Melismas drawn at its share, 7.1 syllables in 100 (932). The step fit kept round 2 of 6 (step 1.208, leap 0.717); its rounds read 9 to 17 builds of 80, for half the trial builds died in the rhythm draw. Range: the aim is 24, past the baritone's span; the tops were set for 22; the builds span 17 at the median, the pick 20.
- 900: the guitar under 1.0 of the sung notes.
- Length: 240 s. Deaths: half the thousand builds died before a pitch was drawn, the syllables not fitting the window (the verse lines run 11 to 14 syllables at 120 beats a minute, set in three-bar slots).

## The hold-out readings

Read after the song was built (`studies/holdout59/`). soundness.py on the record alone: no check past the kept 10th to 90th; three of the 21 checks read on kept songs outside the kept middle half (fit by place high, moves by step low, silences low). A single kept song stands outside the middle half on a median of 10 (quartiles 9, 12); 1 kept song in 147 stands outside on 3 or fewer. Songs 55, 54 and 58 stand outside on 6, 6 and 5. The three-song rule passes on every three of songs 55, 54, 58 and 59; with song 59 in, no check leans past the kept quartiles.
Against its aimed song (every living build's median, aimpool readings): it sits within a fifth of the kept middle half's width of Two Hearts on most checks, nearer than songs 55, 54 and 58 sit to theirs, because Two Hearts sits near the kept middle. Where Two Hearts leaves the middle, the builds do not follow: range 17 against 24, repeated notes 0.336 against 0.21, rhythm scaling 0.676 against 0.593.

## The documents

Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:

| Check | Result |
|---|---|
| the document record is the song record: sung notes | pass |
| harmony notes | pass |
| band parts | pass |
| bars and chords | pass |
| every sung line spells its locked line | pass (42 lines) |
| readback: him read back | pass (370 of 370) |
| readback: him read back | pass (370 of 370) |
| readback: harmony read back | pass (116 of 116) |
| readback: guitar read back | pass (2860 of 2860) |
| readback: lead read back | pass (39 of 39) |
| readback: bass read back | pass (480 of 480) |
| readback: drums counted | pass (1532 of 1532) |
| readback_score: him read back | pass (370 of 370) |
| readback_score: harmony read back | pass (116 of 116) |
| readback_score: guitar read back | pass (2860 of 2860) |
| readback_score: lead read back | pass (39 of 39) |
| readback_score: bass read back | pass (480 of 480) |
| readback_score: drums counted | pass (1532 of 1532) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass (A major) |
| lead sheet: key signature is the record's | pass (\key a \major) |
| full score: PDF written, credit line | pass (5 pages) |
| full score: footer tempo and key | pass (A major) |
| full score: key signature is the record's | pass (\key a \major) |
| parts: PDF written, credit line | pass (9 pages) |
| parts: footer tempo and key | pass (A major) |
| parts: key signature is the record's | pass (\key a \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (A major: 1 = A, 2m = Bm, 3m = C♯m, 4 = D, 5 = E, 6m = F♯m) |
| number chart: one cell a bar, as the record | pass (120 cells) |
| MusicXML lead sheet: onsets and pitches | pass (370) |
| demo: voice notes | pass (370) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: lead guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.4 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | not met (last chorus 0.47, top Break 0.64 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

For the next list (from 749.113).

- Out of sample, the songs sit nearer the kept middle than almost any kept song (749.103 holds on a new lyric).
- Where the aim leaves the middle, the builds stay in it: range, repeated notes and rhythm scaling did not follow Two Hearts (749.111 and 749.109 hold on a new lyric).
- Long lines at a quick tempo kill half the builds in the rhythm draw, and the step fit then reads too few builds a round to be trusted.
- The break's lead guitar makes the break read as the demo's loudest section, above the last chorus (9.12 not met as a reading).
