# Everything That Moves (first edition): test report

Words and music: Jason Bryant

Song 60 (songs/p70), from the writer's paper on near-1/f scaling in animal sound across two phyla (CrossPhylum v2) and the C. elegans crawling check: written end to end from a new lyric with `lib/luthier/song_from_lyric.py` on main at 14f7eeb (v36 merged), with no change to the engine during the song. The pick chanted, so the method's re-pick was offered (below); the writer kept the engine's pick. Song 59 stays the hold-out; nothing here was fitted to it. This report is the engine's record; the songbook is for musicians.

## What a person typed

The title; the words by section (the second chorus typed out); settings: metre 4/4, bpm 116, voice baritone, lead guitar, mode major, genre soul / r&b (the engine has no funk or disco tables; the writer's lane is funk-disco), seed 1. The record was written once and not changed; the documents add an arrangement read from it (below).

## The run

- Key A (47 to 59); other keys offered: C, B.
- Chords: draft 1 of 12, charge 0.0.
- Melody: 88 of 1000 builds survive; deaths join before a copy (780) 784, 838: the chorus's lift is not the plan's 106, 840: the title's stresses off the beat 22.
- The pick: 02d0629cc008, the judge's. Gates: old charge's least half 44, joint gate 44, words' gate 11 (at least 0.152).
- Distance 2.66 (gate 3.918); directed readings, printed only: low surprise -2.709, sure endings 0.34, order across scales, pitch 0.895, order across scales, rhythm 0.656.
- Flags: 'peeper' is not in the lexicon; read as P IY1 P ER0.

## The record's checks

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [45, 59] |
| sung notes on a beat that are chord tones, share | 0.958 |
| sung notes a beat long or more a semitone from a chord tone | 1 |
| bass notes | 416 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 42] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 6.0 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 26); on a word's end (kept 94) | [27, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.685 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.0, 0.0, 0.103] |
| a song with blue notes | False |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.33, None, 0.19] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.33, None, 0.19] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.51 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [5.4, 2.0] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['9/39', '12/109'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [12, 10, 57, 57] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.296 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.244, 0.155, 0.055] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | 1.009 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [2.524, 89], 'six_note_share': [0.843, 28], 'five_note_share': [0.774, 40], 'time_on_tonic': [0.491, 100], 'different_pitches': [2.18, 93], 'different_intervals': [2.386, 93], 'leaps': [0.041, 90], 'range': [14.0, 81], 'repeated_notes': [0.474, 90], 'repeated_figures': [0.631, 66], 'plainness': [1.009, 95]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.448 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | 0.0 |
| the plan's lift | 2 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.087 |
| the title's stressed syllables on a beat (kept 0.73) | 0.5 |
| title lines | 6 |
| length in seconds (kept quartiles 165, 206, 243) | 215 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.75 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 1.0 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.278, 0.295], '5th': [0.201, 0.176], 'octave': [0.16, 0.155], 'unison': [0.132, 0.151], '4th': [0.132, 0.119], '6th': [0.097, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [3.5, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.199, 0.225], 'oblique': [0.291, 0.298], 'contrary': [0.149, 0.099], 'parallel': [0.255, 0.278], 'similar': [0.106, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [40, 0] |
| harmony voice crosses the lead | 1 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [3.9, 6.7] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.057, 13.0] |
| kicks with a bass note on them, share | 1.0 |
| roughness at sung onsets (median, 90th percentile) | [0.706, 0.86] |
| roughest bars | [86, 54, 24, 58, 90] |

## Research checks (the offline rules)

- Metre and stress: long notes on stressed syllables 0.685 (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.5 (kept 0.73).
- One song-wide intensity curve: section levels Intro 0.61, Verse 1 0.78, Chorus 1 1.0, Turn 1 0.86, Verse 2 0.78, Chorus 2 1.0, Break 0.86, Bridge 0.94, Last Chorus 1.0, Outro 0.75. Read from the demo (band only): Intro 0.19, Verse 1 0.36, Chorus 1 0.67, Turn 1 0.41, Verse 2 0.37, Chorus 2 0.68, Break 0.67, Bridge 0.47, Last Chorus 0.69, Outro 0.36. Each chorus above its verse; the last chorus reads highest, the break below it (the horn stabs lift the choruses).
- Perception: sung phrases [3.9, 6.7] s; over 12 beats, share and longest in beats, [0.057, 13.0] (kept 0.042); chord voicings inside the low-interval limits; no accompaniment a second from a sung note.
- Two channels and chromatic harmony: chords from outside the key, share 0.0.

## Readings the paper does not give

- The aim: the kept song TheWeatherGirls ItsRainingMen 1983. Its readings: repeated notes 0.47119, moves by step 0.29153, moves by leap 0.07458, range 24.0, bars on a figure already sung 0.26506, bars on a rhythm already sung 0.53012, distinct rhythms over bars 0.46988, longest run of one pitch 17.0. The run cap 10 (its own longest run, 17, capped); melismas at its share, 5.23 syllables in 100 (932); the step fit kept round 1 of 6.
- The page gate, as sung: plainness 1.009, plainer than 95 kept tunes in 100; time on the tonic plainer than 100 in 100. Four-note figures already sung, first 120 notes, 0.448 (kept quartiles 0.241, 0.362, 0.455).
- The chorus's median over the verse's: 0.0 semitones, the plan's lift 2 (838 passes within two). The chorus climbs inside itself: its top, A3, on “groove” in every chorus.
- Breaths: silences of a beat or more per 100 beats and their median, [5.4, 2.0] (kept 7.0, 9.1, 11.1). Lines run on with under a beat of rest 0.51 (kept quartiles 0.095, 0.253, 0.426).
- Length: 215 s.

## The chant and the re-pick

The pick chants: the verses sit on E3 for 70 notes in 100, a run of 10 of one pitch as sung (kept 90th percentile 9.5). The aimed song's own longest run is 17, capped at 10, so the gate let it through by design. The method's re-pick (`songs/p70/repick60.py`): the judge's own rule over the same run's builds with no run over 9 (52 of the 88 set aside). It drew 7205d09f0ede in B (capo 2): verses that move (commonest note 36 in 100), but a chorus on D♯3 for 53 notes in 100 that never climbs (B2 to F♯3). Both demos went to the writer; he kept the engine's pick. The re-pick's record is kept as `lyric60.nochant.song.json`.

## The arrangement added to the record

The writer chose a funk-disco lane: a busy bass line, sixteenth-note hi-hat, rhythm guitar, horns on the chorus. The engine's soul / r&b band gives four on the floor, eighth hats, eighth guitar, quarter-note bass. `build60.py` adds, read from the engine's parts and nothing invented: the bass's quarters split into eighths, root then octave (the octave kept only where it stays two semitones under every sung note then); the hats split into sixteenths; horn stabs on 1 and the and of 2 in every chorus from the guitar's top two notes; the break's tune given to the horns. The document checks test each against the engine's parts.

## The documents

Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:

| Check | Result |
|---|---|
| the document record is the song record: sung notes | pass |
| harmony notes | pass |
| band parts: guitar as the record | pass |
| bass: the record's roots on every beat, the octave or the root on the and | pass (832 notes) |
| bass under the voice everywhere | pass |
| drums: the record's hits, the hats split into sixteenths | pass (2239 hits) |
| horns: stabs only in the choruses, the break's tune as the record | pass |
| bars and chords | pass |
| every sung line spells its locked line | pass (40 lines) |
| readback: him read back | pass (389 of 389) |
| readback: him read back | pass (389 of 389) |
| readback: harmony read back | pass (144 of 144) |
| readback: guitar read back | pass (2465 of 2465) |
| readback: horns read back | pass (173 of 173) |
| readback: bass read back | pass (832 of 832) |
| readback: drums counted | pass (2230 of 2230) |
| readback_score: him read back | pass (389 of 389) |
| readback_score: harmony read back | pass (144 of 144) |
| readback_score: guitar read back | pass (2465 of 2465) |
| readback_score: horns read back | pass (173 of 173) |
| readback_score: bass read back | pass (832 of 832) |
| readback_score: drums counted | pass (2230 of 2230) |
| lead sheet: PDF written, credit line | pass (2 pages) |
| lead sheet: footer tempo and key | pass (A major) |
| lead sheet: key signature is the record's | pass (\key a \major) |
| full score: PDF written, credit line | pass (7 pages) |
| full score: footer tempo and key | pass (A major) |
| full score: key signature is the record's | pass (\key a \major) |
| parts: PDF written, credit line | pass (12 pages) |
| parts: footer tempo and key | pass (A major) |
| parts: key signature is the record's | pass (\key a \major) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (A major: 1 = A, 2m = Bm, 3m = C♯m, 4 = D, 5 = E, 6m = F♯m) |
| number chart: one cell a bar, as the record | pass (104 cells) |
| MusicXML lead sheet: onsets and pitches | pass (389) |
| demo: voice notes | pass (389) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: horn notes | pass |
| demo: bass notes | pass |
| songbook: the chorus's top note and word, from the record | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+9.1 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| READING, the engine's, not a document check: the last chorus or the bridge the top (9.12) | pass (last chorus 0.69, top Last Chorus 0.69 (749.75)) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 8) |

## Findings

For the next list (from 749.123).

- An aim that chants lets the pick chant: the run cap is the aimed song's own longest run (capped at 10), so a pick can sit on one note for 70 in 100 verse notes. The method's chant check then offers a re-pick, and here the re-pick lost the chorus's climb. The cap and the chant check disagree on what a kept song allows.
- 784 of 1,000 builds die at the join before a copy (780).
- The chorus's median sits where the verse's does (0 against a plan of 2), yet the chorus plainly climbs to the song's chorus top: the median reading misses a climb inside the chorus.
- One harmony note crosses the lead by more than an octave (bar 95, G♯4 over G♯3).
- No funk or disco tables: the soul / r&b band is plainer than the lane, and the documents had to add the bass octaves and sixteenth hats.
