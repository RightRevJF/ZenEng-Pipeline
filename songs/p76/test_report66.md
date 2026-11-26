# They Did the Right Thing (first edition): test report

Words and music: Jason Bryant

Song 66 (songs/p76). The engine is Luthier v52 (main at 5dd5ba8), every trial switch off. This report is the engine's record; the songbook is for musicians.

## Intake

The writer's older lyric, revised with him and locked; the mouth tests read before any music (`mouth_readings.txt`). Settings: 4/4, ♩ = 72, tenor, guitar lead, minor, genre rock (dark indie folk-rock). His production notes are kept in `intake.py` (DESIGN_NOTES_FROM_THE_WRITER). Song 66 was first spent as the sealed test of the pair (749.217, `studies/borrow_kept`); those test records are not this song. The writer chose A minor for it (intake LOG).

## The runs

- **The engine as it is** (`lyric66.song.json`, `run/engine.log`): key Dm (52 to 69), 276 of 1000 builds living. The tune sat 2 to 19 semitones over its written tonic, so in A minor it could only be B2 to E4 or B3 to E5 for a tenor.
- **The design run** (`design66.py`, `run_d/lyric66_d.song.json`): one design gate, the whole tune inside a tenor (C3 to A4) over an A3 tonic, and the key set to A minor. 4,000 builds: 86 living; deaths 838: the chorus's lift is not the plan's 1759, design: the tune inside a tenor over an A3 tonic (the writer's A minor) 962, rhythm: the syllables cannot fit the window 849, 959: a leap past an octave inside a line 287, 840: the title's stresses off the beat 37, 751: two notes on one onset, or a note of no length 8, 731: stressed syllables on the beat too few 7, 926: a run of one pitch longer than the kept song's longest, across the lines 5. Chord draft 4 of 12. The pick 2cce3187fc59, the first past both gates; 9 builds passed the joint gate (the standard asks 10). Melody 57 to 69 (G3 to A4).
- Flags: no break: with one the song would run past the kept 75th of lengths; 888: the song runs long: 2 bars in and 4 out (the kept lower quartiles); the song runs 387 seconds, past the kept 75th (243.2): the lyric is long for its tempo; at this tempo it would need about 22 fewer two-bar lines, or about 115 beats a minute.

## The writer's design notes, laid by hand (`hand66.py`)

- 4: the final chorus's 'gone' on E4, held three bars, over the bass E, D#, D (then C#, C): “gone” bar 106.75, 0.5 beats on MIDI 65 to 12 beats on 64.
- 4: five bars added after the final chorus (bars 107 to 111), the descent's chords: bar 107 (added) to E, bar 108 (added) to E/D#, bar 109 (added) to E7/D, bar 110 (added) to A/C#, bar 111 (added) to C.
- 1: the turn after chorus 1, the descent begun: bar 41 Am to E, bar 42 Am to E/D#, bar 43 Am to E7/D, bar 44 Am to Am/C.
- 1: chorus 1's 'gone' on E4, held two bars: “gone” bar 40.75, 4 beats on MIDI 65 to 8 beats on 64.
- 1: the turn after chorus 2, the descent begun: bar 83 Am to E, bar 84 Am to E/D#.
- 1: chorus 2's 'gone' on E4, held two bars: “gone” bar 82.75, 2.5 beats on MIDI 69 to 8 beats on 64.
- 5: the tag's last word on E4, held to the outro's first bar, then the guitar alone: “thing” bar 116.75, 3 beats on MIDI 67 to 9 beats on 64.
- Parts taken out: drums 102 (2: the bridge has no drums); drums 130 (5: the tag and outro: voice and guitar); bass 40 (5: the tag and outro: voice and guitar); harmony 3 (1, 4: the held E4 sung alone); chords 4 (3: all stop, the bridge's last two beats); bass 2 (3: all stop, the bridge's last two beats).
- The stop: bar 92, beats 3 and 4. Levels: the bridge 0.55, the tag 0.62, the outro 0.5; the final chorus's band 1.12 times as loud, with a crash on its downbeat.
- Two harmony notes over the lead (“Still”, bars 36 and 102: G4 over B3) set an octave down.
- Words' fit: the pick 0.279, after the notes 0.274.

## The record's checks (the design run)

| Check | Reading |
|---|---|
| no two sung notes on one onset | True |
| no sung note of no length | True |
| the melody inside the voice | [55, 69] |
| sung notes on a beat that are chord tones, share | 0.9 |
| sung notes a beat long or more a semitone from a chord tone | 0 |
| bass notes | 464 |
| the bass on the root where a chord begins | True |
| the bass under the voice everywhere | True |
| bass register | [28, 43] |
| syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2) | 6.1 |
| of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, 30); on a word's end (kept 94) | [26, 100] |
| long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65) | 0.716 |
| flat third; flat seventh; leading tone, share of notes (kept, this family) | [0.107, 0.122, 0.0] |
| a song with blue notes | None |
| line-final syllables an eighth or less: function word, weak syllable, stressed (kept [0.358, 0.481, 0.182]) | [0.12, 0.54, 0.28] |
| line-final syllables a half note or more: function word, weak syllable, stressed (kept [0.18, 0.115, 0.29]) | [0.38, 0.15, 0.22] |
| lines that run on with under a beat of rest (kept songs [0.095, 0.253, 0.426] by quartile) | 0.32 |
| silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0) | [8.7, 2.25] |
| stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12) | ['8/51', '17/139'] |
| 9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26) | [20, 14, 69, 67] |
| the words' fit: weightier syllables on more salient notes (kept 10th 0.152, quartiles 0.248, 0.318, 0.402) | 0.279 |
| the fit by length, by place in the bar, by height (kept medians 0.209, 0.242, 0.106) | [0.27, 0.177, 0.116] |
| the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456) | -0.488 |
| the page gate: each part, and the share of kept tunes the song is plainer than | {'surprise': [4.145, 8], 'six_note_share': [0.692, 7], 'five_note_share': [0.692, 17], 'time_on_tonic': [0.282, 63], 'different_pitches': [2.735, 63], 'different_intervals': [3.148, 28], 'leaps': [0.139, 25], 'range': [14.0, 81], 'repeated_notes': [0.3, 48], 'repeated_figures': [0.481, 28], 'plainness': [-0.488, 20]} |
| four-note figures already sung, first 120 notes (kept quartiles [0.2414, 0.3621, 0.4547]) | 0.198 |
| the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4) | -4.0 |
| the plan's lift | 1 |
| rest share inside sung sections, median (kept quartiles 0.15, 0.22, 0.32) | 0.175 |
| the title's stressed syllables on a beat (kept 0.73) | 1.0 |
| title lines | 4 |
| length in seconds (kept quartiles 165, 206, 243) | 387 |
| later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100) | 0.64 |

## The band's checks

| Check | Reading |
|---|---|
| chord voicings inside the low-interval limits | True |
| sung notes with the chordal part sounding under them, share (892) | 1.0 |
| sung notes with the guitar above them, share (no kept figure; not a fault) | 0.265 |
| sung notes with accompaniment a second away, share | 0.0 |
| harmony voice: interval classes, written / kept below the lead | {'3rd': [0.308, 0.295], '5th': [0.179, 0.176], 'octave': [0.141, 0.155], 'unison': [0.141, 0.151], '4th': [0.107, 0.119], '6th': [0.124, 0.104]} |
| harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept | [6.1, 14.09] |
| harmony voice: motion, written / kept | {'static': [0.208, 0.225], 'oblique': [0.25, 0.298], 'contrary': [0.142, 0.099], 'parallel': [0.226, 0.278], 'similar': [0.175, 0.1]} |
| harmony voice: lowest note; notes under E2 (893) | [45, 0] |
| harmony voice crosses the lead | 2 |
| harmony voice a second from the lead | 0 |
| sung phrases, seconds (median, longest) | [4.6, 8.3] |
| sung phrases over 12 beats, share; the longest in beats (kept 0.042; each kept song's longest [8.0, 12.0, 15.5] by quartile) | [0.0, 10.0] |
| kicks with a bass note on them, share | 0.664 |
| roughness at sung onsets (median, 90th percentile) | [0.662, 0.811] |
| roughest bars | [103, 37, 67, 19, 60] |

## Research checks (the offline rules)

- Chant: the longest run of one pitch is 5 notes (kept median 6, 90th percentile 9.5). Each section's first eight bars, the commonest pitch: Verse 1 E4 12/45; Pre-chorus 1 D4 20/38; Chorus 1 B3 8/32; Verse 2 E4 14/45; Pre-chorus 2 D4 20/38; Chorus 2 B3 8/32; Bridge E4 21/39; Chorus 3 B3 7/34; Tag E4 5/18. Over the 0.44 that 956 holds verses to: Pre-chorus 1 D4 20 of 38; Pre-chorus 2 D4 20 of 38; Bridge E4 21 of 39. The verses are under it; the pre-choruses (D4) and the bridge (E4) sit on one note like speech.
- One song-wide intensity curve, read from the demo (band only): Intro 0.65, Verse 1 0.77, Pre-chorus 1 0.80, Chorus 1 0.82, Turn 2 0.78, Verse 2 0.78, Pre-chorus 2 0.80, Chorus 2 0.82, Turn 3 0.78, Bridge 0.40, Chorus 3 0.87, Tag 0.22, Outro 0.05. Each chorus above its verse; the top is the final chorus (0.87), bars 93 to 111, 0.76 to 0.92 of the song (749.17 asks the high point at 0.65 to 0.85); the bridge the lowest sung section before it, and the tag the release.
- A breath, then a fresh re-entry: the stop in bar 92 is two beats of silence before the final chorus enters together, at 0.76 of the song.
- Perception: sung phrases [4.6, 8.3] seconds (median, longest; the longest are the designed holds); chord voicings inside the low-interval limits; no accompaniment a second from a sung note.
- Surprise: the page gate's plainness -0.488.
- Chromatic harmony: the descent's chords (E/D♯, E7/D, A/C♯) are the writer's, under held notes; the engine's own plan uses E (V) as the minor key's dominant.

## Findings (for the next list, from 749.219)

- **749.219 A writer's key cannot be asked for.** The engine draws the tune against a written tonic and chooses the key afterwards by range. Its own run put the tonic at the bottom of the tune (D minor for a tenor). To honour the writer's A minor, a design gate kept only tunes inside a tenor over an A3 tonic: 962 of 4,000 builds died at it, and the joint gate passed 9 (the standard asks 10). Fix: a lyric `key` setting that places the draw's register against that tonic before drawing, so the asked key costs no builds.
- **749.220 The pitch ceiling reads verses only.** Here the verses are under 0.44, but the pre-choruses put D4 on 20 of 38 notes and the bridge E4 on 21 of 39 (0.54). It suits a quiet bridge and a pre-chorus that builds on one note, but 956 never read them. Check: read 956 on every sung section and report it; decide by kind whether it holds.
- **749.221 Arrangement the writer designs has no lever.** Every design note here (a held note of set length at a section's end, a bass line under it, an instrument's entry and exit by section, a stop, an added stretch of bars) was laid by hand. Fix: a design file the engine reads, naming these by section, so the record carries them and the checks read them.
- **749.222 The harmony voice sits over the lead.** Twice (“Still”, bars 36 and 102) the engine's harmony note was G4 over the lead's B3, and it reaches A2. Fix: the harmony a third to a sixth under the lead, never over it, inside a stated range.
- Length: 403 seconds, past the kept 75th (243): the lyric is long for its tempo (the engine's flag).

## The documents

Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:

| Check | Result |
|---|---|
| the document record is the song record: sung notes | pass |
| harmony notes are the engine's (two set an octave down, where the engine's sat over the lead) | pass (231; 2 recast) |
| harmony: never above the lead | pass |
| guitar: the engine's part (with the design notes), note for note | pass (964) |
| bass: the engine's part (with the design notes), note for note | pass (442) |
| drums: the engine's part (with the design notes), note for note | pass (1323) |
| guitar: every strummed note a tone of its beat's chord | pass |
| bars and chords | pass |
| design 1: each chorus ends on E4 held at least two bars | pass (Chorus 1 bar 40, 2 bars, Chorus 2 bar 82, 2 bars, Chorus 3 bar 106, 3 bars, Tag bar 116, 2 bars) |
| design 1: under the first two holds the bass begins a chromatic descent from E | pass ([[10, 4, 3], [10, 4, 3]]) |
| design 2: the bridge is voice, guitar and bass only | pass |
| design 2: the bridge the lowest level of the song's sung sections | pass (bridge 0.40) |
| design 3: all stop on the bridge's last two beats, every instrument | pass (bar 92) |
| design 4: the final chorus all in on its downbeat, nothing in the bar before | pass |
| design 4: the final chorus's hold three bars over the bass E, D♯, D, C♯, C | pass ([10, 4, 3, 2, 1, 0]) |
| design 5: the tag and outro voice and guitar only | pass |
| design 5: the tag's last word held on E4; the song ends on A minor | pass (“thing”, last chord Am) |
| design 5: the tag fades | pass |
| the key: A minor, the writer's | pass |
| the voice inside a tenor (C3 to A4) | pass (55–69) |
| every sung line spells its locked line | pass (57 lines) |
| readback: him read back | pass (468 of 468) |
| readback: him read back | pass (468 of 468) |
| readback: harmony read back | pass (231 of 231) |
| readback: guitar read back | pass (964 of 964) |
| readback: bass read back | pass (442 of 442) |
| readback: drum hits written | pass (1317 of 1317) |
| readback_score: him read back | pass (468 of 468) |
| readback_score: harmony read back | pass (231 of 231) |
| readback_score: guitar read back | pass (964 of 964) |
| readback_score: bass read back | pass (442 of 442) |
| readback_score: drum hits written | pass (1317 of 1317) |
| lead sheet: PDF written, credit line | pass (3 pages) |
| lead sheet: footer tempo and key | pass (A minor) |
| lead sheet: key signature is the record's | pass (\key a \minor) |
| full score: PDF written, credit line | pass (5 pages) |
| full score: footer tempo and key | pass (A minor) |
| full score: key signature is the record's | pass (\key a \minor) |
| parts: PDF written, credit line | pass (10 pages) |
| parts: footer tempo and key | pass (A minor) |
| parts: key signature is the record's | pass (\key a \minor) |
| Nashville chart: PDF written, credit line | pass (1 pages) |
| Nashville chart: the record's key, 1 = its tonic | pass (A minor: 1m = Am, ♭3 = C, 4m = Dm, 5 = E, ♭6 = F, ♭7 = G) |
| number chart: one cell a bar, as the record | pass (121 cells) |
| MusicXML lead sheet: onsets and pitches | pass (468) |
| demo: voice notes | pass (468) |
| demo: harmony notes | pass |
| demo: guitar notes | pass |
| demo: bass notes | pass |
| demo: drum hits | pass |
| demo: track names ASCII | pass |
| demo: voice at least 3 dB over the band | pass (+7.7 dB) |
| demo: MP3 written | pass |
| energy arc: each chorus above its verse | pass |
| energy arc: the final chorus the top | pass (final chorus 0.87) |
| songbook: no engine terms | pass |
| songbook: credit line | pass |
| songbook: every line on the lyric sheet | pass |
| songbook: producer one-sheet and its page breaks | pass |
| songbook: the held E4s and the stop named at their bars | pass |
| songbook: Word copy written | pass |
| songbook (Word): the one-sheet on one page | pass (page 9) |
