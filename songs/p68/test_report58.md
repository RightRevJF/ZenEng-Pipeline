# Same Time Tomorrow (fourth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v26 (main at c476c45). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage13.md).

## The run

- Key A (45 to 62); other keys offered: G, Ab.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 676 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 289, 840: the title's stresses off the beat 34, 731: stressed syllables on the beat too few 1.
- The pick: b15bdc785338, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 338, joint gate 338, words' gate 338 (at least 0.152; builds' fit quartiles [0.327, 0.381, 0.42]).
- Distance 3.308 (gate 3.918); directed readings, printed only: low surprise -3.106, sure endings 0.323, order across scales, pitch 0.905, order across scales, rhythm 0.479.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); 888: no turn: with one the song would run past the kept 75th of lengths; the song runs 326 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 14 fewer two-bar lines, or about 113 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [44, 62] |
| sung notes on a beat that are chord tones, share | 0.887 |
| sung notes a beat long or more a semitone from a chord tone | 1 |
| bass notes | 456 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 16.1 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [32, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.514 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.041] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.0, 0.43, 0.21] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.0, 0.0, 0.29] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.25 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [9.8, 3.0] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['5/65', '30/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 62, 62] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.162 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [-0.017, 0.27, 0.051] |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 10.0 |
| the plan's lift | 9 |
| rest share inside sung sections, median (kept quartiles 0.14, 0.23, 0.33) | 0.278 |
| the title's stressed syllables on a beat (kept 0.73) | 0.5 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 326 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.45 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.945 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.269, 0.295], '5th': [0.204, 0.176], 'octave': [0.156, 0.155], 'unison': [0.151, 0.151], '4th': [0.145, 0.119], '6th': [0.075, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [9.4, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.159, 0.225], 'oblique': [0.282, 0.298], 'contrary': [0.147, 0.099], 'parallel': [0.271, 0.278], 'similar': [0.141, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [42, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 10.7] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.077, 15.0] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.744, 0.877] |
| roughest bars | [62, 23, 109, 99, 110] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.514 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.5 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.36, Verse 1 0.58, Chorus 1 0.73, Verse 2 0.58, Chorus 2 0.74, Bridge 0.68, Verse 3 0.60, Last Chorus 0.76, Outro 0.56. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.9, 10.7] s, over 12 beats, share and longest in beats, [0.077, 15.0] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 0.945, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.013 (F# in the last chorus; G in the outro); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.22, a half or more 0.30 (kept, ties read, 0.18, 0.29); lines run on with under a beat of rest 0.25 (kept 0.295); rest median 25.5 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 5 of 14 line ends (kept 42 in 100, ties read).
- Breaths: 7.4 real breaths a minute by onsets (human median 7); silences of a beat or more 9.8 per 100 beats (CoCoPops, ties read, quartiles 6.7, 8.5, 10.4), median silence 3.0 beats (CoCoPops 2.0). Phrases split at half a beat: over 12 beats 0.077 (kept 0.042), longest 15.0 beats (kept songs' longest, quartiles 8, 12, 15.5): 749.88.
- 900: the guitar under 1.0 of the sung notes.
- Length: 326 s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).
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
| readback: harmony read back | pass (186 of 186) |
| readback: guitar read back | pass (2652 of 2652) |
| readback: bass read back | pass (456 of 456) |
| readback: drums counted | pass (1344 of 1344) |
| readback_score: him read back | pass (469 of 469) |
| readback_score: harmony read back | pass (186 of 186) |
| readback_score: guitar read back | pass (2652 of 2652) |
| readback_score: bass read back | pass (456 of 456) |
| readback_score: drums counted | pass (1344 of 1344) |
| lead sheet: PDF written, credit line | pass (3 pages) |
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
| number chart: one cell a bar, as the record | pass (114 cells) |
| MusicXML lead sheet: onsets and pitches | pass (469) |
| demo: voice notes | pass (469) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.1 dB) |
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

Numbered from 749.84; each has Problem, Evidence, Fix and Check in the fix list for v27 (`songs/p68/fixlist_v27.md` and its Doc).

- 749.84 The chorus lift is one draw from the kept lifts, clamped to the voice; songs 54 and 58 drew 11 and 12, and 58's key went to A with the verse at the bottom of a baritone.
- 749.85 All three picks sit below their builds' median on the words' fit; 58's pick is 0.162 against a gate of 0.152, with a negative fit by length.
- 749.86 register_plan.json cannot be remade from the repo, and it now sets the key.
- 749.87 make_kept_4_4_tables on the old parse does not quite give back surprise_quartiles.
- 749.88 Phrases over 12 beats run at about twice the kept share in all three 4/4 picks; 906 prints it and nothing acts on it.
- 749.89 Two constants recounted on the mended corpus: 877 stands, 876 falls by about a tenth.
- Answered: 904 to 906 hold; 749.82 and 749.83 closed.
- Carried open: 749.61 (6/8).
