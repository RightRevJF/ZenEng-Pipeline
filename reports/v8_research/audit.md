## Summary

The engine writes one thing: the sung melody. On harmony and arrangement, the record (Luthier v7, 15,350 lines, plus its tables) holds a great deal of research but almost no code that writes anything.

- **Harmony.** 24 items, among them six measured tables. In code: the chord chart's redraw (438), the bass's inversions (440), and the melody's fit to the chords (375, 386, 431, 432, 441, 442). Missing: anything that writes a section's chord progression. Every song's chord plan has been typed by an AI, including song 36's "chords by the section jobs (177)", which were a hand-written list.

- **Arrangement.** Module 9 (9.1 to 9.14), the rock and metal modules (9-R, 9-M), Windows 118, 119, 143 and 144, and the offline findings 749.14, 749.16 and 749.21. In code: the bass routine (Windows 143 and 144) and the readers (9.12 energy arc, 9.13, 9.14). Missing: drums, the chordal part, instrumental figures, the texture plan and parts playing. Every band part but the bass has been written by an AI, per song, in that song's build script.

So a v8 that writes everything needs two new generators, harmony and arrangement, built the way the melody is: drawn from tables measured on real songs, and tested. Much of the measuring is done already; the main gaps are sequence data (what follows what) and data by genre and section role.

## How to read the status

|Status|Meaning|
|---|---|
|**Writes**|The engine's own code makes these notes or chords, the same way every run, with no AI choosing.|
|** Reads**|The engine's code measures or checks it (a reading, a gate, a consistency check) but writes nothing.|
|** Table**|The numbers were measured from real music and saved; no code writes from them yet.|
|** Rule**|Written in the spec as what a song should do; applied only by an AI writing each song by hand, if at all.|
|** Missing**|Not in the record.|

Evidence is the fix or Window number in the spec, and the file where the code lives (the engine of record is `songs/p66/melody_l7_p66.py` ; the bass routine `bass_v134.py`).

## Harmony: what the record holds

Of 24 harmony items, the engine writes from four and reads four; the other sixteen are tables, rules or missing, and nothing writes from them. No code writes a chord progression.

|Item|Where|What it says|Status|
|---|---|---|---|
|The chart's changes|Window 143, fix 438|A section's bars with two changes, and bars holding the last chord, inside the kept quartiles (Table ED)|** Writes**: adds or holds changes within a plan it is given|
|The bass under the chord|440|The root at nine changes in ten; a third or fifth in the bass with a step beside it|** Writes**(inversions, `BASS8`)|
|The melody against the chord|375, 386, 431, 432, 441, 442|Chord tones on the first beat near 72%; no note a semitone from a chord's outside tone|** Writes**the melody's fit; the chords themselves are given|
|Modal chord tones in minor|349, 353|A minor song's measures read on its own tonic; its outside notes at the kept minor rate|** Writes**(melody only)|
|Melody against bass, by class|Window 95, 135 to 137|Interval and motion shares at bass moves; hymn gates; the bass as a line in hymns|** Reads**(printed); the hymn gate only in the sketch path|
|Cadences by strength|138|A full close ends on 1 over I; an open half on 2, 7 or 5 over V|** Reads**; nothing writes the V or the I|
|No contrary-motion rule|443|Direction against the bass is printed, never gated|** Reads**|
|Harmony by class|Window 105, 173 to 175; Table CN|Vocabulary, root motion, chords a bar, tonic time, sevenths, inversions in seven bodies of music (24,137 Hooktheory pieces to 54 Mozart sonatas)|** Table** (`zeneng_v88_tables.json`)|
|Pull and distance|175, Table CO|Each chord's pull toward the tonic and each move's distance, by class|**Table**|
|Section jobs|Window 106, 176, 177; Table CP|Verse opens on I and holds most tonic; chorus opens on I or IV and adds a chord; bridge and pre-chorus end on V; first and last chords and joins in 739 McGill songs|** Table**; song 36's "chords by the section jobs" were a hand-typed list|
|The chorus changes the loop|Window 28|Chorus harmony differs from the verse's; the chorus sits above|** Rule**|
|Hits are not harmonically special|Windows 28, 56|No harmony feature separates top-ten records|** Rule**(a caution)|
|Harmony beyond the loop|Window 56, Table AJ|A second chord model for songs with sevenths (the standards)|** Table**; the ledger (11.14) is not in the v7 pipeline|
|Expectation of chords|Window 46; 749.18|Chord surprise against a popular-music model; the sung line at or below the median|** Reads**(research check, outside the engine)|
|Modulation|Window 55|9% of McGill songs modulate, once, mostly up a semitone or tone, near the middle|** Table**; the v7 engine's lift is switched off (`LIFT2 = 0`)|
|Harmonic rhythm|Part VII update; type tables (0.05 to 0.40 departure)|Rate of change by type; one deceleration before the bridge or last chorus|** Rule**|
|Mode as colour palette|Part IV-D; type tables|A mode for each song type (Dorian for Paradox, Ionian or Dorian for Longing)|** Rule**; chosen at intake from options an AI wrote|
|Chord vocabulary by type|Module 0.4, type tables|Allowed and forbidden chords by type (min7, sus4 for Paradox)|** Rule**|
|The deceptive cadence|Window 8; item 111|V to vi at a seam in a Longing song|** Rule**|
|Blues and gospel harmony|Windows 15, 16; Modules 21, 22|The twelve-bar system; the vamp in a new key|** Rule**|
|Hymn setting|Window 57; 749.11 to 749.13|Four parts against hymn quartiles; passing notes in inner voices|** Rule**; songs 52 and 53 by AI sketch scripts|
|Chromatic harmony as a style|749.23|Applied dominants and mixture rates by style|** Table**(studies/chromatic) and ** Rule**|
|Harmony voices as lines|749.9|A harmony part written as a line, not a shadow of the lead|** Rule**|
|A section's chord|none|What follows what, by section|** Missing**|
|progression||and genre||

## Arrangement: what the record holds

Of 27 arrangement items, the engine writes two (the bass, and the demo's audio from the record) and reads seven. Drums, the chordal part, fills, the intro figure, the texture plan and parts playing are measured or ruled but never written by code: each song's build script, written by an AI, has done them by hand.

|Item|Where|What it says|Status|
|---|---|---|---|
|The bass as a line|Window 118, 233; Windows 143, 144, 439, 444 to 448|Root on 1 and at each change; a one-or two-bar cell; a note on most kicks; bands from 434 transcribed patterns|** Writes**(`bass_v134.py`), on the engine's grid only (it ran sixteenths at song 56's 72)|
|Outer voices, twice|234|The outer-voice reading on the written bass and on the roots|** Reads**|
|The drum part|Window 119, 236; Table DD|Snare on 2 and 4, kick on 1 in nine bars of ten; one kick-and-snare bar a section; a fill in a section's last bar; patterns from 2,667 band arrangements|** Table** (`zeneng_v101_band_returns_eras.json`) and**Rule**; drums typed per song|
|The chordal part|237; Table DE|One bar rhythm a section from the kept vocabulary; three or four notes between MIDI 51 and 71, under the voice's top|** Table**and** Rule**; typed per song|
|Parts playing|238|The intro half the fullest or fewer; the last chorus the fullest; each verse no fuller than its chorus|** Table**and** Rule**|
|The instrumental figure|235; Table (instrumental figures)|Intro figure unrelated to the voice; fills of two to three beats and four to six notes, in the voice's gaps, ending on a chord tone|** Table** (`zeneng_v100_bass_and_figures.json`) and**Rule**|
|The instrumental hook|Window 112, 209|An instrumental line that returns as a hook|** Rule**|
|The accompaniment follows the voice|379|No held sung note a semitone or minor ninth from a held accompaniment note|** Reads**(consistency)|
|Performance: microtiming, velocity, articulation, controllers, rubato|9.1 to 9.5, 9.7|Offsets by instrument; velocity and articulation by section; a rubato budget|** Rule**; the demo applies only pink-noise velocity and timing (v43)|
|Instrument selection|9.6|Lead, double and prohibited instruments by context|** Rule**; instruments chosen at intake from AI-written options|
|Section entry and exit map|9.8|Which layer plays in which section (a twelve-layer Americana stack)|** Rule**|
|MIDI drift patterns|9.9|Symptoms and corrections for mechanical demos|** Rule**|
|Timbral arc|9.11|Brightness, richness and intimacy by section|** Rule**|
|The energy arc|9.12; Window 38 (14,286 records)|Each chorus above its verse; the last chorus or bridge the top; read by where a build arrives|** Reads**(the demo's report); arranged by hand to pass|
|Register collision|9.13|Who sits in the singer's octave, bar by bar|** Reads**|
|Low-interval limits|9.14; 749.21|No second below C4, no third below F3|** Reads**(`perception.py`); voicings kept inside by a hand function in each build|
|Rock production|9-R; Window 14|Palm-muted verses, open choruses; the feel column|** Rule**(rock songs arranged by hand)|
|Metal|9-M|Presets, voicings, the riff, the feel ladder|** Rule**(the metal song arranged by hand)|
|Audio by decade|Window 40|Loudness and onset rate by era|** Table**(era defaults in the production notes)|
|The demo|11.11|Render and stems; the voice 3 dB over the band|** Writes**the audio from the record (a fixed script)|
|No accompaniment|749.14|Nothing in the engine writes an accompaniment|** Missing**(the finding itself)|
|Accompaniment by section role|749.16; Lieder tables|A texture plan by section, measured against 1,403 Lieder (OpenScore, CC0)|** Table**(`accompaniment_lieder.json`) and ** Rule**; song 53 by hand|
|One intensity curve|749.17|The high point at 0.65 to 0.85, a release after|** Reads**(research check)|
|A breath, then a fresh re-entry|749.19|Thin the band a beat or two before the best moment|** Rule**; placed by hand|
|A low lead under the band|749.27|The 2% band-over-tune limit does not fit a baritone under guitars|** Reads**(an open finding)|
|Harmony and backing voices|749.9; 9-M.7|Lines, not shadows; when a crowd voice joins|** Rule**; typed per song|
|Genre patterns|none|Grooves, comping|** Missing**|
|(country, soul, gospel)||and fills by genre and section||

## Who has written what, songs 48 to 56

In every song since v7 the engine wrote the sung melody and an AI wrote the chord plan and every band part but the bass. Read from each song's generator and build script.

|Song|Melody|Chord plan|Hook's notes|Band|Bass|
|---|---|---|---|---|---|
|48 The Ratios Hold|Engine|AI|Engine (no design)|AI|Engine routine|
|49 The World Is Asking|Engine|AI|Engine (no design)|AI|Engine routine|
|50 The Small Things|Engine|AI|Engine (no design)|AI|Engine routine|
|51 A Wire Pulled Tight|Engine|AI|AI design, the writer's choice|AI|Engine routine|
|52 The Room Next Door|AI sketch script|AI|AI|AI|AI|
|53 Sung to Sleep|AI sketch script|AI|AI|AI|AI|
|54 The Man Mama Prayed I'd Be|Engine|AI|AI design, the writer's choice|AI|Engine routine|
|55 Your Yard Man|Engine|AI|AI design, the writer's choice|AI|Engine routine|
|56 Terpsichore|Engine (running)|AI|AI design, the writer's choice|AI draft, withdrawn|AI draft, withdrawn|

The lyrics were the writer's words, drafted or revised in session with an AI and locked by him; the engine's line scorer (Module 28) and the mouth tests did not run on songs 54 and 55. The intake questions and their three options were written by an AI each time; the spec's question tree (Q0 to Q8) is not a program.

## The gaps, and the research that would fill them

The record already describes what real harmony and bands do on average; what it lacks is what follows what, and how it differs by genre and by section. Those are the two things a generator needs.

|Rank|Gap|What to research|Data|What the engine gets|
|---|---|---|---|---|
|H1|A section's chord progression|Sequences of chords by section kind and genre: loops, lengths, harmonic rhythm, how a section ends and joins the next|McGill Billboard (the raw annotations, not only Table CP); Hooktheory; a large genre-labelled chord collection|A progression drawn per section from kept sequences, gated by Tables CN and CP|
|H2|The order of chords and melody|Whether real songwriting and the data favour chords first, melody first, or both together; how well a drawn progression fits a melody already drawn|Hooktheory (melody and chords aligned)|A decided order of work, and a fit test|
|H3|Mode and borrowed chords by genre|Rates of minor, Dorian, Mixolydian, ♭VII,♭VI and applied dominants in country, soul, rock, worship and pop|The same collections, by genre|Per-genre vocabularies replacing the hand-picked type tables|
|H4|Harmony and backing voices|When a second voice joins, and at what interval; answers and crowd voices|Arranging literature; multitrack vocals where they exist|A harmony-voice writer with its own test|
|A1|Drums by genre and section|Grooves, fills and crashes for country, soul, rock and pop, and how they change from verse to chorus|Lakh MIDI with genre tags (the existing Table DD, split by genre); style-labelled drum performances|A drum writer drawing a section's pattern and fills from kept bars|
|A2|Texture by section role|Which parts enter, leave, thicken or thin, section by section, in pop records (749.16 has this only for Lieder)|Multitrack MIDI with section labels (POP909's structure; Lakh with sections found by repetition)|A texture plan by section role, replacing the hand plans and the 9.8 stack|
|A3|The chordal part by instrument|Comping rhythms, voicings and registers for piano, organ and guitar against the voice, by genre (Table DE pools all instruments)|Lakh MIDI, split by instrument and genre|A chordal-part writer with Table DE's vocabulary per instrument|
|A4|Fills and answers in the voice's gaps|Their length, register and notes by genre (the existing figure table pools them)|Lakh MIDI lead tracks|A fill writer for the gaps, never under a sung word (379)|
|A5|The bass at any tempo|Bass cells by tempo and subdivision, so a|The 434 transcribed patterns, read by tempo|The routine made tempo-aware|
|||ballad at 72 does not run sixteenths|||

Two cautions from the record itself: harmony and arrangement features have never separated hits from other songs (Windows 28, 38, 56), so these tables should describe what real songs typically do, not promise success; and every new table needs a kept-song test, as the melody's do.

## Proposed order of work for v8, and the test

Harmony first, then the band, then a test that makes "the engine writes everything" checkable.

1. ** Research H1 to H3**, then build the harmony writer. The engine's order becomes form, harmony, melody, arrangement; the chart redraw (438) and the bass's inversions (440) stay as they are.

2. **A5** : make the bass routine read the tempo. A small job, and it removes the one place the routine failed.

3. **Research A1 to A4**, then build the drum, texture, chordal-part and fill writers, each with its own kept-song test.

4. **H4** : the harmony-voice writer.

5. **The no-hand-input test.** A run may take only the writer's intake answers (from a fixed questionnaire written from the spec's Q0 to Q8) and his locked lyric. The song's generator may set only those. The test report lists every input that did not come from the engine, and a song fails if any chord or band note came from a hand-typed list.

6. **Rerun songs 54 to 56** under the test, and compare them by ear with the versions already delivered.

Until then, a delivered song should say plainly what wrote it: the engine's melody, an AI's chords and band.

## Data on hand and data to fetch

The measured summaries are in the repo; the raw collections they came from are not, and the research needs them again.

|Data|What it gives|Where it stands|
|---|---|---|
|`zeneng_v88_tables.json`|Harmony by class and by section; outer voices; cadences|In the repo (song folders' tables)|
|`zeneng_v101_band_returns_eras.json`|Drums, the chordal part and parts playing in 2,667 band arrangements|In the repo|
|`zeneng_v100_bass_and_figures.json`|Bass lines in 2,165 songs; instrumental figures in 879|In the repo|
|`zeneng_v123`, `zeneng_v124`|The chart and the bass at and between the chords|In the repo; used by the engine|
|`accompaniment_lieder.json`|Accompaniment textures in 1,403 Lieder|In the repo (metre atlas)|
|McGill Billboard annotations|Chords in time with section labels, 890 songs|To fetch again (raw)|
|Hooktheory|Melody and chords aligned, about 24,000 pieces|To fetch again (raw)|
|Lakh MIDI (clean subset) with genre tags|Multitrack band parts by genre|To fetch again (raw)|
|POP909|Pop songs with melody, accompaniment and structure|To fetch|
|Chordonomicon|Over 666,000 chord progressions labelled with verse, chorus and bridge, genre and release date (the paper says CC BY 4.0; its dataset card says CC BY-NC 4.0, non-commercial; its download host is refused by this session)|New; to fetch|
|Groove MIDI Dataset|13.6 hours, 1,150 files of human drumming in many styles, by 10 drummers (CC BY 4.0)|New; to fetch|

This session's shell can reach only package sites and GitHub, so the large collections may need to be attached or fetched where the earlier studies fetched them; each study script's docstring says how.

Sources: [Chordonomicon (arXiv 2410.22046);](https://arxiv.org/abs/2410.22046) [Groove MIDI Dataset (Magenta)](https://magenta.tensorflow.org/datasets/groove); Luthier v7 (Windows 28, 38, 56, 95, 105, 106, 118, 119, 143, 144; Module 9; 9-R; 9-M); the fix list for v8 (749.9, 749.14, 749.16, 749.17, 749.19, 749.21, 749.23, 749.27).
