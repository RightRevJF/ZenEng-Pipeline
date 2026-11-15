---
title: "Sung to Sleep: test report (second edition)"
subtitle: "Words and music: Jason Bryant"
---

# Intake

| Question | Answer |
|---|---|
| What next | The next song in 3/4, building the chorus, harmony and whole-song changes in from the start (A) |
| The request | "I really want to do another Christmas Carol, this one, with a full score for the organist and a hymn sheet for the choir perfectly aligned. Would this time signature work for that?" (yes: 3/4 suits a carol) |
| The idea | A brainstorm from the theology of the first carol ("the Word that had to learn words"); five sparks offered; the writer chose the Song sung to sleep (Job 38:7): "A. But I don't want it sung as Mary. A narrator like most Carols is fine" |
| Shape | Four verses, a refrain after each, the descant over the last verse and refrain (A) |
| Lyric | Draft 1; "I hate lullay as a word, makes no sense" (the refrain opens "Hush now"); verse 2 rewritten for distinctiveness ("the voice that called the light to be / now cried for Mary there"); the refrain's melody to lift gently and stay warm under repetition; locked at draft 3: "A. And remember, we are learning. I want you to make the adjustments musically we talked about where possible" |
| Key | E♭ major, the last verse up a step to F (A); "Just a full score for the organist and a hymn page for the choir" (no Nashville chart) |
| Tempo | Gently rocking, quarter = 88 (A) |
| Title | Sung to Sleep (A) |
| Refrain melody | "Hush now" low and still; line 3 climbs to the tune's top on "world"; the second "sleeping" a step above the first, home on "here" (A) |
| Last verse | An organ link to F; verse 4 in unison over the organ's own harmony; the final refrain in four parts with the sopranos' descant, the last "here" held (A) |

# Method

The engine draws in 4/4 only (749.4), so the tune was drawn by a 3/4 sketch of its method (gen34.py) with kept tables from the Essen folk-song collection: 1,601 tunes in 3/4 (tables_34.py, with song 52's builder: bar 36 twelfths, beats at 0, 12 and 24). The hymn form sets the rhythm's frame: Common Meter, every stressed syllable on a downbeat, every line opening on a pickup except the refrain's "Hush now" lines; inside it each bar is drawn from the kept 3/4 bars (half and quarter, quarter and half, or a slurred pair, at most one slur a line). Pitches from the kept interval shares, chord tones weighted on downbeats. Written in D and transposed: verses 1-3 and refrains to E♭, verse 4 and the final refrain to F.

The four parts: the carol pipeline's beam search (harmonize53.py; two chords added for the verse-4 organ setting, F♯7 and C in D, sounding A7 and E♭ in F). The descant: song 52's harmony-as-lines search (harm68.high) above the sopranos in their rhythm and words, chord tones of the four-part chord, "world" pinned a third above (A5) inside the search.

Both documents come from one record on one timeline and share one line of time, keys, bar lines, marks and a break every fourth bar, so bars 1-80 fall on the same systems in both (engrave53.py).

# The melody search

3,000 builds, seed 20261115+453; 2739 survivors. Deaths: refrain 2: 184, refrain 3: 77 (the refrain's line 3 climb with D5 once on "world"; line 4's step and its home). The pick: **01be9dada5fb**, charge 0.61, distance 8.9, taken as drawn.

| Reading | The pick | Median survivor | Kept 3/4 (25th, 50th, 75th) |
|---|---|---|---|
| repeated notes | 23% | 32% | 11%, 18%, 26% |
| moves by step | 50% | 43% | 38%, 48%, 60% |
| moves by leap | 8% | 10% | 7%, 11%, 17% |
| turns of direction | 40% | 41% | 33%, 40%, 47% |
| range | 13 | 12.00 | 12.00, 13.00, 14.00 |
| distinct pitches | 8 | 7.00 | 7.00, 8.00, 9.00 |
| longest run of one pitch | 3 | 4.00 | 2.00, 3.00, 4.00 |
| distinct rhythms over bars | 16% | 16% | 35%, 47%, 67% |
| notes a bar | 1.97 | 1.90 | 2.84, 3.48, 4.00 (set by the hymn form; not charged) |
| onsets on the beat | 100% | 100% | 57%, 67%, 82% (set by the hymn form; not charged) |
| onsets on the bar's first beat | 46% | 47% | 23%, 26%, 33% (set by the hymn form; not charged) |
| gaps of a sixteenth | 0% | 0% | 0%, 0%, 9% (set by the hymn form; not charged) |
| gaps of an eighth | 0% | 0% | 25%, 48%, 64% (set by the hymn form; not charged) |
| gaps of a quarter or more | 100% | 100% | 24%, 39%, 70% (set by the hymn form; not charged) |

Distinct rhythms over bars sits under the kept range (16% against 35%): every survivor's does, since the hymn frame allows only three bar rhythms (finding 749.11).

# The harmony (749.9)

Each part against the tune, at each pair of the tune's onsets, by section:

| Part | Moves with the tune | Against it | Holds while it moves (or the reverse) | Parallel fifths or octaves | Distinct distances |
|---|---|---|---|---|---|
| verse A | 17% | 22% | 61% | 0 | 8 |
| verse T | 9% | 41% | 50% | 0 | 10 |
| verse B | 21% | 33% | 46% | 0 | 12 |
| refrain A | 21% | 33% | 46% | 0 | 9 |
| refrain T | 18% | 50% | 32% | 0 | 9 |
| refrain B | 8% | 58% | 33% | 0 | 14 |
| refrain_final A | 26% | 26% | 48% | 0 | 7 |
| refrain_final T | 17% | 43% | 39% | 0 | 10 |
| refrain_final B | 21% | 42% | 38% | 0 | 10 |
| refrain_final Desc | 26% | 35% | 39% | 0 | 6 |
| verse4 organ alto (org_rh_a) | 26% | 22% | 52% | 0 | 9 |
| verse4 organ tenor (org_lh) | 22% | 43% | 35% | 0 | 12 |
| verse4 pedal | 21% | 33% | 46% | 0 | 14 |

Song 52's shadow harmony moved with the lead 74% to 85% of the time and never against it; here no part moves with the tune more than 26% of the time, and the tenor and bass move against it 33% to 58% of the time.

# Variety and shape (749.8, 749.10)

- Verses 1-3 and their refrains share one setting (a hymn's form). Verse 4 changes three things: the key (F), the texture (the choir in unison, the men an octave lower) and the harmony (the organ's own chords: F♯ minor, E minor 7, B minor 7, A7, G, E minor 7, C, A7 ... in D, a different chord on 25 of its 31 notes).
- The final refrain: four parts again, a fresh setting in F, and the descant above.
- The shape: average sounding pitch of the tune, verses 1-3 A♭4, refrains 1-3 G4, verse 4 C5, final refrain B4 (each a step above its first); the tune's top, F5, in bar 71 of 80 (88% of the way in), with the descant's A5 on the same beat. The tune's E♭5 sounds once in the first section, on the refrains' "world".

# The organ part, rewritten after delivery

The writer: "The organ music looks incredibly easy. Are you sure that's right?" It was right note for note and too plain for the request: outside a 4-bar introduction, a 2-bar link and verse 4's own chords, the organ played the choir's four parts (soprano and alto in the right hand, the tenor alone in the left, the bass in the pedal), the way an organist plays from a hymnal, and verse 4 and the introduction were in the same four-part texture. He chose A: build through the carol.

| | First version | Now |
|---|---|---|
| Introduction | 4 bars: the refrain's last line in four parts | 8 bars: the refrain's first line, then its last, the tune with one voice under it in the right hand, the left hand rocking in eighths (root, fifth, third inside a fifth), a held pedal |
| Verses 1-3 and refrains | the four choir parts doubled | a fuller form of them: a third note in the right hand on 41 of 57 chords, a filled chord in the left hand, common tones held |
| Link | 2 bars, G minor 7 to C7 | 4 bars, E♭, G minor 7, C7sus4, C7, the rocking figure going on |
| Verse 4 | the organ's own chords, in four plain parts with the tune on top | its own accompaniment: chords held below the tune (never doubling it), a suspension at a chord change, the rocking left hand, the pedal on the new bass line |
| Final refrain | the choir's four parts doubled | held chords with the tune on top, the rocking left hand in every bar, a tonic pedal under "Hush now" (bars 61-64) and a dominant pedal under "is sleeping, sleeping" (bars 73-74) |
| Coda | none | 4 bars: the refrain's last phrase once more over a tonic pedal, IV to I, the last chord held |
| Left hand in eighths | 0 | 263 notes |
| Length | 70 bars | 80 bars |

Against the tune, verse 4's organ right hand moves with it 43% of the time and holds 48%; the final refrain's pedal moves with the tune 9% of the time and holds 65%; no parallels.

# Documents

- Full score for the organist (PDF, 7 pages, 80 bars): descant (final refrain only), the choir on two staves with every verse between them, the organ's manuals and pedal (see the organ part below).
- Hymn page for the choir (PDF, 4 pages): the same bars, systems and notes without the organ staves.
- Every voice read back from LilyPond's MIDI note for note (sopranos, altos, tenors, basses, descant, organ right hand, left hand, pedal).
- Consistency: 46/46 checks pass, among them: one shared global line in both documents (80 bars); the same choir notes in both; the keys; the tune's tops and the descant's top on "world"; the descant above the sopranos; the refrain's designs; verse 4 in unison over a different harmony; the organ's introduction and coda alone, its fuller chords in verses 1-3, its right hand below the tune in verse 4, a suspension, the rocking left hand in every bar of the final refrain, the two pedal points; no parallel fifths or octaves in any part; the voices in their ranges; no Nashville chart.

# Second edition: built from the metre atlas

The writer, after the atlas was built: "Any chance once you build the tables, we can return to the recent hymn and finish it using the engine with the table you created?" The engine still draws in 4/4 only (749.4 is not ported), so the second edition is the sketch rebuilt on the atlas's tables; the rerun on the engine stays in the order of work. He chose A: a second edition now, measured before and after.

**What changed.** The tune (gen34h.py, pick 9025fdbc9b1e, seed 20261115+4532, 2740 survivors of 3,000) draws its bars from the Open Hymnal Project's 3/4 hymn bars, with a slurred second note where a hymn bar has more onsets than the frame has syllables (dotted quarter and eighth; two quarters; two eighths on the weak syllable; up to two slurs a line), and is charged against the 3/4 hymn quartiles (46 hymns) on every reading. The quarter-and-half bar was left out: in a strophic hymn it lengthens an unstressed syllable in every verse. The designs stand (Hush now low and still; the climb to D5 on world; the second sleeping a step above the first; here home on D4). The four parts: the beam search weighted toward hymn motion (the alto rewarded for parallel thirds and sixths with the tune; contrary motion rewarded mainly in the bass); the lower voices hold under the tune's slurred notes; passing notes added where a voice moves by a third (eighth pairs in the alto and tenor near the hymn rate; the bass only on longer notes). The organ doubles the passing notes in verses 1 to 3 and the refrains; verse 4, the final refrain and the coda keep their own accompaniment.

**The tune against 3/4 hymn tunes** (quartiles from 46 hymns):

| Reading | First edition | Second edition | Hymns (25th, 50th, 75th) |
|---|---|---|---|
| repeated notes | 23% (outside) | 21% (outside) | 14%, 17%, 21% |
| moves by step | 50% | 54% | 49%, 57%, 62% |
| moves by leap | 8% | 8% | 7%, 9%, 11% |
| range | 13.00 | 13.00 | 12.00, 12.00, 14.00 |
| longest run of one pitch | 3.00 | 3.00 | 2.00, 3.00, 3.00 |
| distinct rhythms over bars | 14% (outside) | 18% | 16%, 22%, 32% |
| notes a bar | 2.18 | 2.21 | 2.12, 2.34, 2.66 |
| onsets on the beat | 100% | 95% | 84%, 94%, 100% |
| gaps of half a beat | 0% | 7% | 0%, 7%, 24% |
| gaps of a beat or more | 100% | 93% | 74%, 92%, 100% |

All 19 readings: first edition 17 inside the hymn quartiles, second 18 (repeated notes 21.3%, a hair over the hymn 75th of 21.26%). Notes a bar rose from 1.97 to 2.21; half-beat gaps from 0% to 7%.

**The four parts against 3/4 hymn settings** (with the tune / against it / holding; notes shorter than the beat):

| Voice | First edition | Second edition | Hymns (medians) | Short notes, first | Short notes, second | Short notes, hymns |
|---|---|---|---|---|---|---|
| Alto | 21% / 27% / 52% | 36% / 12% / 52% | 39% / 13% / 47% | 0% | 9% | 8% |
| Tenor | 15% / 45% / 40% | 23% / 28% / 49% | 35% / 24% / 40% | 0% | 5% | 7% |
| Bass | 17% / 44% / 39% | 16% / 43% / 41% | 26% / 34% / 38% | 0% | 0% | 5% |

The alto now moves almost as hymn altos do; the tenor and bass are closer than before but still move against the tune more, and with it less, than hymn tenors and basses. No parallel fifths or octaves in either edition. A first pass split the unchanged voices around each passing note into repeated eighths (21% short notes in every voice); fixed.

**Documents.** Organ full score and hymn page, second edition (80 bars, the same layout); every voice read back from MIDI; consistency 46/46.


# Third edition: the organ part by section role

The second edition's organ was measured against a new table, the piano parts of the 326 art songs in 3/4 in OpenScore Lieder (CC0, tables/metre_atlas/accompaniment_lieder.json), and the research round "Accompaniment corpora and music theory" was run first, at the writer's request. Its first rule, from organ practice, is that each section gets a role: the inner verses stay in the hymnal harmony and change colour, while the introduction, the passages between verses and the last verse carry the free, fuller writing. The third edition's organ follows that plan. The choir's parts and the descant are unchanged (a check).

| Section | Role in the third edition |
|---|---|
| Introduction, bars 1-8 | the tune in the right hand over an inner line that moves when the tune holds; the rocking left hand; the last bar over B-flat |
| Verses 1-3, bars 9-24 | hymnal harmony in the right hand; the left hand a broken chord in quarters, the tenor's note on every downbeat; colour changed by registration verse by verse |
| Refrain, bars 25-40 | the tune on top, an inner line moving in quarters under its held notes, the rocking left hand |
| Link, bars 41-44 | broken eighths in the right hand, held chords in the left, the pedal stepping down E-flat, D, C |
| Verse 4, bars 45-60 | free harmony around the unison tune: four-note chords that change on every beat, suspensions at changes, the pedal written first and stepping into each new bass, quarters in the left hand |
| Final refrain, bars 61-76 | the tune on top, the inner line in eighths under held notes, the rocking left hand, the tonic and dominant pedals |

Before and after, against the Lieder 3/4 middle half (right hand 1.13-1.95 onsets a beat; left hand 0.88-1.51; complementarity, the share of accompaniment onsets where the tune has none, 0.50-0.73). The organ's left hand is read with its pedal, since a pianist's left hand carries the bass.

| Section | Right hand a beat | Left hand and pedal a beat | Complementarity | Commonest texture |
|---|---|---|---|---|
| introduction | 0.62 → 0.96 | 1.96 → 1.96 | 0.98 → 0.98 | mixed → mixed |
| verses 1-3 | 0.67 → 0.67 | 0.48 → 0.83 | 0.18 → 0.39 | sustained → block |
| refrain | 0.56 → 0.79 | 0.48 → 1.96 | 0.13 → 0.67 | sustained → broken |
| link | 0.42 → 1.92 | 1.92 → 0.42 | 0.96 → 0.96 | mixed → broken |
| verse 4 | 0.44 → 0.79 | 1.96 → 1.0 | 0.68 → 0.42 | broken → block |
| final refrain | 0.38 → 1.1 | 1.98 → 1.98 | 0.68 → 0.68 | broken → broken |
| coda | 0.5 → 0.5 | 1.0 → 1.0 | 1.0 → 1.0 | sustained → sustained |
| whole | 0.52 → 0.89 | 1.32 → 1.42 | 0.65 → 0.67 | broken → broken |

What changed: the refrain's complementarity rose from 0.13 to 0.67 and the verses' from 0.18 to 0.39; held, sustained bars fell from 19% of the song to 5%; verse 4 and the final refrain now move in both hands. Semitone clashes between organ and choir fell from 28 eighths to 18, and the parallel octaves between the organ's top and its pedal (four in the second edition, at bars 8, 41, 52 and 75) are gone.

What did not: the right hand over the whole song is 0.89 onsets a beat, still under the Lieder floor of 1.13. That is mostly the plan. The verses keep the hymnal right hand (0.67) because organists keep inner verses close to the hymnal harmony, and there is no table of organ hymn accompaniment to say what an organ's right hand should do; a piano part is a loose stand-in. The verses can't change from one to the next in notes, because verses 1-3 share the printed bars, so their variety is in the registration printed over bar 9.

New tools: organ_readings53.py (the readings above, by the tables' own texture rules) and clash53.py (semitone clashes, organ outer parallels). Consistency: 55 of 55 checks pass, among them the new ones for the inner line, the pedal parallels, the clash count, the Lieder ranges, the unchanged choir parts and the registrations.


# Fourth edition: the new findings applied

The choir's notes and the descant keep their pitches and onsets (a check). The changes:

- **Breaths (749.19, 749.20):** every part takes a beat's breath before the third line of each verse and refrain, after the half-stanza: bars 16 and 32, and in F bars 52 and 68. The tune had no breath of a beat or more anywhere. The organ's hands lift where their notes end there; held pedal points carry on.
- **Verses 1-3 (749.16):** the organ's right hand now carries the tune over an inner line, as the refrains do. The line is the altos (with their passing notes) plus a filling chord tone, moving to a neighbouring chord tone on held beats, so the harmony stays the hymnal one. Where there is no room above the alto, the filling note goes under it, and the lower note moves when the upper can't.
- **Each return higher (749.17):** the registration now builds through the three refrains (1st time Swell flutes; 2nd, add the Great open diapason; 3rd, add the Great principal 4′) and through the verses (v. 3 on the Great diapasons).
- **The intensity curve as sung (749.17):** intensity53.py reads the record in performed order (144 bars: three times verse and refrain). Per bar it takes the singers' top note, whether the choir sings, how many parts sound, the organ's onsets, and the dynamic with its registration step. Each verse and each refrain is above the one before. The high point falls at 0.87 of the song, at the final refrain's arrival, with the release over its last line ("hush now", p) and the coda. That is 0.02 past the 0.85 the finding proposes. It is kept because a carol's last refrain is its arrival.

Organ against the Lieder 3/4 table, third edition to fourth:

| Section | Right hand a beat | Complementarity |
|---|---|---|
| Verses 1-3 | 0.67 → 0.96 | 0.39 → 0.41 |
| Refrain | 0.79 → 0.90 | 0.67 → 0.67 |
| Final refrain | 1.10 → 1.23 | 0.68 → 0.68 |
| Whole song | 0.89 → 0.99 | 0.67 → 0.67 |

Semitone clashes stay at 18 eighths, with no outer parallels.

Against the popular corpus:

- **Melody:** the tune is at the 41st percentile for melody surprise, the 26th (verse) and 44th (refrain) for rhythm surprise, and the 20th for chords.
- **Verse re-entry:** after the new breath, the verse's re-entry note is a little more surprising than the verse's average (3.15 against 3.12 bits).
- **Refrain re-entry:** the refrain's re-entry is plain (1.56 against 2.45 bits). Its fresh moment comes four beats later, at the leap to the summit on "world". Making the re-entry itself fresher would mean changing a pitch of the locked tune, so it is left to the writer.

Consistency: 59 of 59 checks pass, including new ones for the breaths, the verse inner line, the rising returns and the late high point.

# Findings

## 749.11 A hymn needs a hymn mode and hymn tables

**Problem.** The engine has no strophic mode: one tune for every stanza, the rhythm's frame set by the stanza's meter (here Common Meter, iambic), stressed syllables on downbeats. And the Essen folk tables do not describe hymn tunes: in a hymn frame every bar is one of three rhythms.

**Evidence.** Song 53's sketch built the frame by hand and drew inside it. Every survivor's distinct rhythms over bars sat under the kept 3/4 range (the pick 16%, kept 35% to 67%); onsets on the beat 100% (kept 57% to 82%); notes a bar 1.9 (kept 2.8 to 4.0): all set by the form, so printed, not charged.

**Fix (proposed).** A hymn mode: the stanza's meter (CM, LM, SM, 87.87 and so on) gives each line's pickup, stressed downbeats and held ending; the tune is drawn once and checked against every stanza's stresses. Kept tables from a hymnal corpus (tunes with their meters) for the readings the frame leaves free.

**Check.** A Common Meter tune whose rhythm readings sit inside kept hymn-tune quartiles, sung to every stanza with every stressed syllable on a downbeat.

## 749.12 A descant module

**Problem.** The engine has no descant. Song 53's descant was written with song 52's harmony-as-lines search (above the sopranos, their rhythm and words, chord tones, the summit pinned).

**Evidence.** The descant's readings: moves with the tune 26%, against it 35%, holds 39%; no parallels; its top, A5, once on "world". A first pass pinned the summit after the search and left a parallel fifth beside it (G4 to F4 under D5 to C5, in the refrain's first line); the pin moved inside the search, and the floor was lowered to let the line step down; the parallel went.

**Fix (proposed).** A descant module: a line above the tune for the last stanza or refrain, its own rhythm allowed (longer notes), the summit placed late and pinned inside the search, kept tables from published descants.

**Check.** No parallels with the tune or the bass, the summit in the last quarter, the line above the tune throughout.

## 749.13 Choral documents from one timeline

**Problem.** A choir and an organist need their pages to agree bar for bar. Engraving each document separately leaves bar numbers, breaks and notes free to drift.

**Evidence.** Song 53's two documents come from one record and share one line (time, keys, bar lines, marks, a break every fourth bar); bars 1-80 fall on the same systems in both; every voice read back from MIDI; the choir notes compared between the two sources.

**Fix (proposed).** The engine's standard for choral output: one timeline record, one shared global line with forced breaks, every document written from it, and the readback per voice.

**Check.** On any choral song: the same bars at the start of every system in every document, and every voice matching the record.

## 749.14 The engine has no accompaniment

**Problem.** Nothing in the engine writes an accompaniment. Song 53's first organ part doubled the choir's four parts for most of the carol, and its introduction and verse 4 were in the same texture: correct, and too plain for an organist's score.

**Evidence.** First version: outside the introduction and link, the organ's notes were the choir's (right hand two notes, left hand one, pedal the bass); no eighth notes; a 4-bar introduction; no coda. Rewritten: the introduction 8 bars; three notes in the right hand on 41 of 57 chords in verses 1-3; the left hand rocking in eighths (263 notes); verse 4's right hand below the tune throughout, with a suspension; the final refrain over a tonic and a dominant pedal; a 4-bar coda; every note read back from MIDI.

**Fix (proposed).** An accompaniment module for keyboard-led songs: a texture plan by section that builds through the song (doubling and support early, independence late), figures by metre (the rocking eighths in 3/4), pedal points at phrase openings and before cadences, suspensions at chord changes, an introduction from the refrain's tune and a coda from its last phrase.

**Check.** On any keyboard-led song: the accompaniment's texture grows by section, the late sections do not double the tune, and every note fits its chord or resolves by step.

## 749.16 An accompaniment plan by section role

**Problem.** The engine gives every section of an accompaniment the same treatment, so a song with repeated verses sounds static and an organ part looks thin even when each bar is correct (song 53, first and second editions: the organ's right hand 0.52 onsets a beat, 19% of bars held chords).

**Evidence.** Organ practice gives each verse a role: hymnal harmony with changes of colour for the inner verses, free harmony for the introduction, the interludes and the last verse (the research report "Accompaniment corpora and music theory"). Human arrangements repeat an accompaniment within a section type and change it between types; same-type sections are about 1.68 times more alike (POP909 studies). Song 53's third edition, written to such a plan, raised the organ's right hand to 0.89 onsets a beat and the refrain's complementarity from 0.13 to 0.67, with fewer clashes and no outer parallels.

**Fix.** Before arranging, assign each section a role (introduction, support, lift, interlude, climax, close) and a texture for each hand from the accompaniment tables (by metre: textures, onsets a beat, complementarity). Write the bass first in free sections. Repeat a section's texture when the section repeats and change it when the role changes. Where repeats share printed bars, vary by registration or orchestration. Patterns are stored apart from chords and fitted to each chord, as the published systems do.

**Check.** Per section, each hand's onsets a beat and complementarity sit inside the table's middle half for its role, or the plan says why not. Sustained bars are no more than the table's share. There are no parallel fifths or octaves between the outer voices, and no more clashes than the plain hymnal version.
