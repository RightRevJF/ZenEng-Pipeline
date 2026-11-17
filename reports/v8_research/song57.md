
*Words and music: Jason Bryant. 17 November 2026.*

# Summary

Song 57 is the first song in which nothing was written by hand after the lyric. The melody is Luthier v7's search, picked by the research gates of Parts 30 and 31 and then luthier_judge5. The chords, the band and the lead guitar come from three new writers built from the v8 research tables (writers/chords.py, writers/band.py, writers/solo.py), and the bass from the engine's own routine. The lyric was written with the writer, scored on the hook and lyric rules (Parts 30 and 32), and passed the mouth test before any music.

- **Melody search:** 1,000 main, 298 survivors (29.8%), order 82afd3ac7e99; control 322 survivors, order 29669d99b962. Both reproduced on the second pass.
- **Research gates:** of 175 clean survivors that re-evaluate clean, none passes all five; the long-note gate (R5) fails every one (best 0.74 against 0.75). The pick, be9dba1f3d5c, fails only R5 (0.588).
- **Checks:** 56/56 consistency checks pass; every staff of every engraving reads back from MIDI.

# Intake

| Question | Answer |
|---|---|
| Source | the writer's 'Acid Soaked Ramblings of Poetry', the pilgrimage seam (A) |
| Lane | Grateful Dead-style jam (A) |
| Never-say | trip-song cliches; the trip never named (A: 'like White Rabbit') |
| Title | Jehovah's Band (A) |
| Lyric | four drafts on the writer's notes; draft 4 locked (B) |
| Key | E major with the bVII (A) |
| How the music is made | build the missing writers as code first (A) |
| Tempo and feel | 112 bpm, loping 4/4, light swing (A) |
| Form | 128 bars, about 4:34, a 32-bar jam from silence (B) |

# The lyric on the new rules

| Reading | Draft 4 | Rule |
|---|---|---|
| Repeated lines | 0.42 | L1: 0.42 to 0.57 |
| Range of feeling (line valence spread) | 0.25 (47th pct of greatest-list songs) | L2: at least 0.22 |
| Rare content words | 1.6% | L5: about 4% at most |
| Concreteness | 100th pct | L7: a style dial |
| Past tense / places | 97th / 92nd pct | L4: report |
| Title per chorus / in line 1 / in the song | 2 / yes / 8 | H3: about 2 / first line / about 8 |
| Mouth test | 34 lines, 8 minor flags, no tongue-twister, density at most 4.4 syllables a second | Principle 4 |

VADER reads image lines as neutral and 'laughed' as positive, so the bridge (the extinction) reads near neutral; the low is carried by meaning the measure cannot see.

# The writers (v8 prototypes)

## Chords (writers/chords.py)

A variable-order Markov model per section kind and mode over 739 McGill Billboard songs, 1965-1979 weighted three times; candidates kept by the kept quartiles of distinct chords, tonic share, changes a bar and out-of-key share, the kept first and last chords and loop periods, and 749.22's moving harmony; the bVII (the key question) required song-wide.

| Section | Chords (one cell a bar) | Score | Flags |
|---|---|---|---|
| Intro | E A / A E / E / E A | 0.202 | none |
| Verse | E / A / E A / E / A / E / E / B A | 0.215 | none |
| Chorus | E D / A E / E D / A E / E D / A E / E D / A E ... | 0.169 | none |
| Bridge | C#m / D C#m / C#m Bm / Bm D / D C#m / D / C#m / Bm D ... | 0.212 | none |
| Jam | E / E / D / A E / E / E / D / A E ... | 0.106 | none |
| Outro | E A / E / A / E A / E / E A | 0.133 | none |

The chorus drew E-D-A-E unforced; the bridge never touches I (50% out of key, inside the kept quartiles for bridges). 438's chart then added its holds and inversions as for every v7 song.

## Band (writers/band.py)

The genre's kept tables (LPD-5, rock: patterns, onsets a bar, notes together, register), POP909's texture by role for the level curve (749.17), Module 9.14's limits, and 749.27's reading for a low lead (no chord tone within a second of a sung note). The bass is bass_v134.py's routine on every section.

| Section | Level | Organ | Rhythm guitar | Kick |
|---|---|---|---|---|
| Intro | 0.25 | x...x...x...x... | x...x...x...x... | x.....x.x....... |
| Verse 1 | 0.46 | x...x...x...x... | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Chorus 1 | 0.75 | x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Verse 2 | 0.52 | x...x...x...x... | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Chorus 2 | 0.84 | x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x. | x...x...x...x... |
| Bridge | 0.68 | x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Jam | 0.00 to 0.57 | x...x...x...x... | x...x...x...x... | x.....x.x....... |
| Verse 3 | 0.57 | x...x...x...x... | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Chorus 3 | 1.00 | x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x. | x...x...x...x... |
| Tag | 0.75 | x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x. | x.....x.x....... |
| Ending | 0.42 | x...x...x...x... | x.x.x.x.x.x.x.x. | x.....x.x....... |

The jam's entries (bar of the jam): organ 1, bass 5, drums 9, rhythm 13, lead 17.

## Lead guitar (writers/solo.py)

Trained on 398 Hooktheory solo and instrumental sections in major and Mixolydian keys: scale degree with the bucketed interval (orders 0-3), kept one-bar onset patterns by level, chord tones on beats 1 and 3 at the kept rate (0.76), the centre climbing with the level; each eight bars drawn 60 times and the draw kept whose cell recurrence sits nearest the kept median (0.445) with surprise at or under the kept median.

| Window | Recurrence | Surprise (bits) |
|---|---|---|
| Jam 17-24 | 0.422 (kept 0.445) | 2.057 (kept 1.942) |
| Jam 25-32 | 0.377 (kept 0.445) | 1.864 (kept 1.942) |

Fills in the voice's rests at bars 16, 20, 26, 36, 40, 54, 58, 110, 118, 122, 126; the intro plays the chorus's title line twice (v7's instrumental hook; H5).

# The melody search

| | Main | Control |
|---|---|---|
| Built | 1,000 | 1,000 |
| Survivors | 298 (29.8%) | 322 (32.2%) |
| Order (pass 1 = pass 2) | 82afd3ac7e99 | 29669d99b962 |
| Rhythm: no placement | 581 | 545 |
| Join: no held end and breath before the copy | 48 | 56 |
| Align: the words do not fit the returning tune | 38 | 46 |
| Key word on a chord tone | 22 | 10 |

# The pick

Of 277 clean survivors, 102 fail evaluate when it runs again on the same notes (all 'returns related (267)', the bridge's line 5 returning its line 1); the pick is taken only from the 175 that pass again, as songs 54 to 56's picks were asserted to.

| Gate | Rule | Failing (of 175) | Median, best | Pick |
|---|---|---|---|---|
| R1 | chorus above verse (mean pitch) | 43 | 1.08, 5.77 | 0.34 |
| R2 | chorus recurrence at or above the 50th length-matched pct and above the verse's | 168 | 31.2, 62.8 | 51.3 |
| R3 | typical cells at or above the 60th pct | 111 | 54.3, 94.3 | 79.6 |
| R4 | variety and surprise at or under the 50th pct | 128 | 62.2, 90.0 | 30.1 |
| R5 | long notes on stressed syllables at least 75% | 175 | 0.555, 0.74 | 0.588 |

Reported, not gated: the title's stressed syllables on a beat 0.375 (H3: about 73%), held 1.0 times the median note (H3: 1.3); the uniqueness point 6 notes with rhythm (H4: 8 or under). The pick's longest run of one pitch is 9 (kept median 6, 90th percentile 9.5). Taken as drawn: no hand edits.

# Research checks (749.4 to 749.27)

| Check | Reading | Rule | Held? |
|---|---|---|---|
| Melody surprise (749.18) | 2.48 bits | at or under 2.89 | yes |
| Chord surprise | 1.61 | at or under 3.79 | yes |
| Rhythm surprise (749.20) | 3.13 | at or under 2.49 | no |
| Rest share | 0.48 | median 0.125 | high |
| Stressed syllables on a beat | 0.45 | report | |
| The top (749.17) | Chorus 3 at 0.828 to 0.938 | 0.65 to 0.85 | yes |
| Each chorus above the one before | True | 9.12 | yes |
| Verses | Verse 1 0.58, Verse 2 0.72, Verse 3 0.64 | each return above | verse 3 below verse 2 |
| The breath (749.19) | silence at 0.453, re-entry at 0.703 | 0.55 to 0.60 | later (the form's jam) |
| Low intervals (749.21) | 0 | none | yes |
| Band above the tune | 1.00 | 749.27: a low lead | read by 749.27 |
| Within a second of the tune | 0.13 | report | |
| Phrases | 1.9 to 7.6 s, none over 8 | 2 to 6 (8 at most) | yes |
| Chords outside the key (749.23) | Bm, D | pop budget | the bVII and v the writer asked for |
| Stems | voice +5.0 dB | at least +3 | yes |

# Findings (from 749.32)

**749.32. No build reaches Part 31's long-note band.** *Problem:* 0 of 175 clean survivors put 75% of their long notes on stressed syllables (median 0.555, best 0.74). *Evidence:* the gate table above. *Fix:* weight long durations toward stressed syllables in the placement draw, not after it. *Check:* songs 54 to 57 rerun; at least half the clean survivors reach 0.75.

**749.33. The engine's title line has no hook gates.** *Problem:* without song 56's designs the title line is low and narrow: E, F#, F#, F#, E, F#, E, F#, E, C#; its stressed syllables are on a beat 38% of the time and held no longer than the median note. *Fix:* port H3 (on a beat, held 1.3 times the median) and H1's one fresh note as search gates. *Check:* the title readings pass on songs 54 to 57.

**749.34. The chorus barely lifts.** *Problem:* the pick's chorus sits 0.34 semitones over its verse and 43 of 175 sit under it. *Fix:* port H5's lift (Part 30: higher in 67% of songs, +1.5) as a register draw, not a design. *Check:* R1 on every clean survivor.

**749.35. Evaluate disagrees with the run.** *Problem:* 102 of 277 clean survivors fail evaluate on the same notes ('returns related (267)', the bridge's line 5 returning line 1). *Fix:* find the state 267 reads that the run and evaluate set differently. *Check:* every survivor re-evaluates clean.

**749.36. 749.21's limit empties the band under a low lead.** *Problem:* with the tune kept on top, the band writer could voice almost nothing under a baritone singing C#3 to A3 (verse 1's organ fell to 6 chords). *Fix:* 749.27's reading, used here: no chord tone within a second of a sung note, the voice +3 dB over the band. *Check:* low-interval breaks 0, within a second under a quarter of notes (0.13 here).

**749.37. The level curve does not read the lyric.** *Problem:* the band writer's curve comes from section roles, so the bridge, the song's extinction, sits at 0.68, louder than both verses, and verse 3 reads below verse 2. *Fix:* let the lyric's arc (L2's section valence, or the writer's turn) move the curve. *Check:* the bridge under its neighbours where the lyric falls.

**749.38. Two-bar slots leave long rests.** *Problem:* rest share 0.48 against the corpus 0.125, rhythm surprise 3.13 against 2.49: lines of 7 to 18 syllables all take two bars. *Fix:* Part 21's slots in seconds (749.25, 749.30, 749.31). *Check:* rest share under 0.3.

**749.39. The three writers are ready to port.** writers/chords.py, writers/band.py and writers/solo.py are deterministic per seed, read only kept tables, and report every choice. *Fix:* port them into v8 as the harmony, arrangement and solo writers (Parts 18, 19, 29). *Check:* songs 52 to 57 written with no hand-written chords, band or solos.

# Documents

Lead sheet, full score, parts (voice, organ, rhythm guitar, lead guitar, bass, drums), number chart, MusicXML (lead sheet and full score), demo MP3 and General MIDI, songbook and production notes. The players' notes are written from the writers' reports. The blind pick of the quotable line (10.20) was not drawn for this song.

