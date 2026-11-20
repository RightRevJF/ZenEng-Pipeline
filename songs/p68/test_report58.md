# Same Time Tomorrow (twelfth edition): test report

Words and music: Jason Bryant

Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v35 (main at 78f8ee4). This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: metre 4/4, bpm 84, voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage21.md).

## The run

- Key A (45 to 54); other keys offered: C, B.
- Chords: draft 5 of 12, charge 0.0.
- Melody: 649 of 1000 builds survive; deaths 838: the chorus's lift is not the plan's 319, 840: the title's stresses off the beat 31, 731: stressed syllables on the beat too few 1.
- The pick: 95b4993a0ca6, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half 325, joint gate 325, words' gate 87 (at least 0.152; builds' fit quartiles [0.259, 0.315, 0.363]).
- Distance 3.101 (gate 3.918); directed readings, printed only: low surprise -2.709, sure endings 0.643, order across scales, pitch 0.689, order across scales, rhythm 0.507.
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 337 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 16 fewer two-bar lines, or about 117 beats a minute.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [44, 54] |
| sung notes on a beat that are chord tones, share | 0.892 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 472 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 1.2 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 32); on a word's end (kept 94) | [40, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.656 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.002] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.2, 0.29, 0.24] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.2, 0.07, 0.24] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.2 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [10.1, 1.75] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['16/65', '10/98'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [16, 14, 54, 54] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.301 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.299, 0.218, 0.109] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 0.749 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.823, 74], 'six_note_share': [0.817, 23], 'five_note_share': [0.792, 43], 'time_on_tonic': [0.496, 100], 'different_pitches': [2.056, 96], 'different_intervals': [2.838, 65], 'leaps': [0.044, 88], 'range': [10.0, 95], 'repeated_notes': [0.331, 57], 'repeated_figures': [0.565, 51], 'plainness': [0.749, 88]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.319 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 0.0 |
| the plan's lift | 0 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.179 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 337 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.54 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 1.0 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.242, 0.295], '5th': [0.2, 0.176], 'octave': [0.145, 0.155], 'unison': [0.182, 0.151], '4th': [0.127, 0.119], '6th': [0.103, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [10.7, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.239, 0.225], 'oblique': [0.314, 0.298], 'contrary': [0.075, 0.099], 'parallel': [0.258, 0.278], 'similar': [0.113, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 0 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 8.8] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.018, 12.2] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.75, 0.927] |
| roughest bars | [105, 101, 21, 106, 55] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.656 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 1.0 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 2 0.86, Verse 2 0.78, Chorus 2 1.0, Bridge 0.94, Verse 3 0.78, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.35, Verse 1 0.56, Chorus 1 0.71, Turn 2 0.61, Verse 2 0.56, Chorus 2 0.72, Bridge 0.67, Verse 3 0.58, Last Chorus 0.74, Outro 0.54. Each chorus is above its verse and the last chorus reads highest: 9.12 met.
- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.
- Perception: sung phrases [3.9, 8.8] s, over 12 beats, share and longest in beats, [0.018, 12.2] by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note 1.0, printed without a kept figure (900).
- Two channels and chromatic harmony: chords from outside the key, share 0.0 (); the bass's chromatic notes are passing notes.

## Readings the paper does not give

- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.22, a half or more 0.24 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.20 (kept 0.295); rest median 21 twelfths.
- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 4 of 14 line ends (kept 42 in 100, ties read). 922 and 924, the page gate read as sung: plainness 0.749, plainer than 88 kept tunes in 100 (floor, the kept 10th, -0.64; all 87 builds read pass); four-note figures already sung 0.565 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.319 (0.241, 0.362, 0.455).
- Breaths: silences of a beat or more 10.1 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 12.25 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1.
- 920, 925 to 936, the aim: the song aims at the kept song Bird Dog. Melismas at its share (none; 1.12 syllables in 100 drawn at the kept floor). Moves fitted: step 1.506, leap 2.109, repeat 0.609. Steps 0.422 (Bird Dog 0.398); leaps 0.044 (0.057); repeated notes 0.331 (0.373); chorus over verse 0 (0). Range 10 as sung (9); A to F sharp before melismas, a span of 9: the tune sits on its top note 54 times (Bird Dog twice). Bars on a figure already sung 0.505 (0.698), on a rhythm already sung 0.619 (0.774), distinct rhythms 0.381 (0.226): closer to Bird Dog than at v33. Rhythm scaling 0.507, under the kept 10th (0.574).
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
| readback: him read back | pass (409 of 409) |
| readback: him read back | pass (409 of 409) |
| readback: harmony read back | pass (165 of 165) |
| readback: guitar read back | pass (2832 of 2832) |
| readback: bass read back | pass (472 of 472) |
| readback: drums counted | pass (1392 of 1392) |
| readback_score: him read back | pass (409 of 409) |
| readback_score: harmony read back | pass (165 of 165) |
| readback_score: guitar read back | pass (2832 of 2832) |
| readback_score: bass read back | pass (472 of 472) |
| readback_score: drums counted | pass (1392 of 1392) |
| lead sheet: PDF written, credit line | pass (3 pages) |
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
| MusicXML lead sheet: onsets and pitches | pass (409) |
| demo: voice notes | pass (409) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+8.5 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.74, top Last Chorus 0.74 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 9) |

## Findings

Numbered from 749.117; each has Problem, Evidence, Fix and Check in the list for v36 (`songs/p68/fixlist_v36.md` and its Doc).

- 749.117 The paper's 'random pool pick' figure has been the neighbour choice's since v32; the random pick from the engine's pool fails 2.6 in 100 under v35 (2.5 in v34).
- 749.118 936 meets its check in songs 58 and 59, not 55 and 54: a refitted line sets split notes and lead-ins to the same pitch at fixed shares the repeat weight never reaches, and the fit walks back to its start after a round outside the kept band.
- 749.119 935 acts in every build of songs 55 and 54, not only song 59's bridge line; the pools' failure rates rose with 934 and 935 together (936 lowers them).
- Answered: 934 holds; 935 holds for song 59 (rhythm deaths 500 to 52); 936 in two songs of four. Carried: 749.116, 749.103 (song 59 more central than every kept song), 749.111, 749.104's fix, 749.109, 749.101.
- Carried open: 749.61 (6/8).
