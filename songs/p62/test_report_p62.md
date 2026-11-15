---
title: "The Room Next Door: test report"
subtitle: "Words and music: Jason Bryant"
---

# Intake

| Question | Answer |
|---|---|
| Purpose | Keep writing while the engine is down, "ideally pacing the way for the other engine to know how to easily handle different time (not just 4/4)" |
| Time signature | 6/8 (A) |
| Source | The writer's parable "The Room Next Door" in *Wild Fruit* (A, among three offered) |
| Lyric | Draft 1 for his notes; one note (verse 3's "the house was still" confusing): the sleep said outright (A); locked at draft 2 |
| Sound | An intimate folk ballad: fingerpicked guitar in 6/8, soft piano, a cello at the bridge; dotted quarter about 54 (A) |
| Singer | An alto (A) |
| Key | D major (A) |
| Form | Intro 4; verse, chorus, verse, chorus; a 4-bar cello interlude; verse, bridge, verse; the final chorus with the hook twice; outro 4: 84 bars, 3:07 (A) |
| Hook | "door" on D5, the song's top, held; "wall" open on A4; the second time at the end home on D4 (A) |
| Bridge | A hush, guitar out, piano and cello; "and you were there" lifts to B4; "gone" held open (A) |
| Title | The Room Next Door (A) |
| Chords | Richer (C), then the chart as written (A): add9s, maj7s, m9s, sus4s; Cadd9 in the bridge; B♭maj7 under "and some morning it opens" |
| Melody | "I don't want to see the melody. Just finish the song": taken by the sketch's own rule, no candidates shown |

# Why a sketch, not Luthier

Luthier draws on a fixed 4/4 grid (a bar of 48 twelfths, a beat of 12), and every kept table it reads (bar rhythms, figures, windows, palettes, the judge's readings) comes from 4/4 songs. A 4/4 melody mapped onto 6/8 can only become a swung 4/4 (song 50's way): each dotted-quarter beat then holds two syllables at most, eight in two bars, and these lines carry 10 to 14. So this melody was drawn by a compound-metre sketch built on Luthier's method (gen68.py), with kept tables from the Essen folk-song collection (music21's corpus): 922 sung tunes in 6/8, and 923 in 4/4 for comparison (tables_68.py).

What carries over and what replaces it:

| Luthier | In the 6/8 sketch |
|---|---|
| 653/680: a drawn line from a kept line, whole | A kept two-bar window (72 twelfths) with the line's syllable count, drawn by its frequency and by stress fit |
| 731: entries by the first syllable's stress | Leading unstressed syllables (up to two) sung as eighths before the bar line; stressed syllables scored onto the two beats (0 and 18) |
| 288/314: registers | The verse low (A3–A4 around E4), the chorus above it (D4–C♯5 around G♯4), the bridge's first lines low (A3–F♯4) |
| 650: the per-note reading | Each next pitch drawn from the kept 6/8 interval shares, chord tones weighted on the beats |
| 'again', 'copy' | Verses 2–4 sing verse 1's tunes fitted to their syllables (a held note split, a short one merged); chorus 2 copies chorus 1; the final chorus copies its first two lines, draws the line over B♭maj7 (no F♯, C♯ or B), refits the fourth |
| 317: designs | The hooks, the bridge's last line, pinned |
| 730/715: the judge | Every survivor read on the kept 6/8 quartiles; the pick the least charge, then the nearest the medians |
| Added (746, 749.1, 749.2) | No line holds a pitch four times running; no note of no length; no two onsets alike |

# The melody search

3,000 builds, seed 20261113+452; 657 survivors.

| Deaths | Count |
|---|---|
| Stressed syllables on the beat too few (under 55% in the drawn lines, under 40% in all) | 1,217 |
| The chorus above the verse | 397 |
| A refit that would not fit (verses 2–4, the final chorus's fourth line, the bridge) | 729 |

**The pick: 8f4cc7fe75bf**, charge 1.69, distance 10.4. Plans: the verse ABCD, the bridge ABCX. Taken as drawn.

| Reading | The pick | Median survivor | Kept 6/8 (25th, 50th, 75th) |
|---|---|---|---|
| Repeated notes | 30.5% | 29.2% | 12.5, 21.6, 30.9 |
| Moves by step | 42.2% | 46.1% | 37.5, 47.6, 60.9 |
| Moves by leap | 12.5% | 9.1% | 7.0, 11.4, 16.7 |
| Turns of direction | 35.7% | 36.5% | 32.0, 39.5, 46.4 |
| Longest run of one pitch | 3 | 4 | 2, 3, 4 |
| Distinct rhythms over bars | 31.9% | 29.2% | 46.2, 56.2, 71.4 (under: the choruses and verses repeat) |
| Onsets on the beat | 35.8% | 35.8% | 38.9, 42.5, 46.2 (under) |
| Onsets on the bar's first beat | 17.7% | 17.4% | 21.1, 23.1, 25.8 (under) |
| Notes a bar | 5.35 | 5.35 | 3.6, 4.0, 4.33 (the lyric's; not charged) |
| Gaps of a sixteenth | 27.1% | 24.2% | 0, 5.7, 13.5 (the lyric's; not charged) |
| Range; distinct pitches | 15; 10 | 17; 11 | 12, 13, 14; 7, 8, 9 (the designs'; not charged) |

Stressed syllables on a beat: 47% of the pick's (151).

# Arrangement and demo

- Fingerpicked acoustic guitar in six (the bass note on 1 and 4); piano and acoustic bass from chorus 1; the cello from chorus 2; the cello sings the hook's tune in the interlude; no drums.
- The bridge: guitar and bass out; held piano and the cello.
- Harmony (above and below) on the hook in every chorus and on every line of the final chorus.
- The outro slows to its last chord (tempo events in the demo).
- The bass written by hand (root on 1, fifth or approach on 4): the bass routine reads 4/4 bars (749.6).
- Energy by section (9.12): Verse 1 0.45, Chorus 1 0.72, Verse 2 0.74, Chorus 2 0.90, Interlude 0.79, Verse 3 0.76, Bridge 0.17, Verse 4 0.82, Last Chorus 0.96. Each chorus above its verse; the bridge the hush; the last chorus the top.
- The lead stands +8.1 dB over the band (the rule asks +3).

# Documents

The lead sheet, full score, parts (harmony high and low, acoustic guitar, piano, cello, acoustic bass), number chart, songbook (a Doc and Word), MusicXML (lead sheet and full score) and the demo (MP3, General MIDI), all in 6/8 (bars of 36 twelfths; nothing written across the bar's middle beat but a whole-bar dotted half).

- Every pitched staff of the lead sheet, parts and full score reads back from LilyPond's MIDI note for note.
- MusicXML reads back with music21 (6/8, dotted quarter = 54): onsets and pitches match the record.
- Consistency: 44/44 checks pass, including the hook's D5 only on "door", the home "wall" on D4, the bridge without guitar or bass, B♭maj7 under "and some morning it opens", the voice in the scale, no runs of four, no notes of no length.

# The blind pick (10.20)

Three slots, offered shuffled (A middle, B annotated, C remembered). **The writer chose B, the annotated slot.**

- **Remembered:** "there's a door in the wall"
- **Middle:** "and I said there's a door, and it's going to open" (top quartile under both)
- **Annotated:** "and I said hello through the plaster that night"

# Findings

## 749.4 Luthier draws only in 4/4; the metre should be a parameter, with kept tables per metre

**Problem.** The bar (48), the beat (12), the strong positions and every kept table are 4/4. A 6/8 song can only be set as swung 4/4, which holds two syllables a beat.

**Evidence.** Essen, 922 tunes in 6/8 against 923 in 4/4. The readings about pitch match closely between the metres (median repeated notes 21.6% against 20.0%; steps 47.6% against 50.9%; leaps 11.4% against 11.4%; longest run 3 against 3; range 13 against 12). The readings about rhythm do not: onsets on the beat 42.5% against 77.6%; gaps of an eighth 62.5% against 34.1%; gaps of a quarter or more 25.0% against 61.3%. The commonest 6/8 bar is quarter-eighth, quarter-eighth (0, 12, 18, 30), 2,295 of 11,288 bars; the commonest 4/4 bar is four quarters (1,988 of 11,834).

**Fix (proposed).** Make the metre a parameter: the bar's length, its beats (6/8: 36 and 0, 18; 3/4: 36 and 0, 12, 24; 7/8: 42 and 0, 12, 24), and the kept tables for rhythm by metre (bars, two-bar windows, gap classes, palettes); keep the pitch tables shared. The sketch's tables (tables/essen_meter_tables.json) are a first 6/8 set.

**Check.** A 6/8 song drawn by the engine with every reading read against kept 6/8 quartiles.

## 749.5 The stress rule restated for compound metre

**Problem.** 731 reads entries before, on and after the bar line. In 6/8 the question is whether stressed syllables land on the bar's two beats, and the kept table for that needs sung songs with words; Essen has none.

**Evidence.** The sketch scored stress onto the beats and required 55% in the drawn lines; 1,217 of 3,000 builds died there; the pick puts 47% of its stressed syllables on a beat overall (the refitted verses lower).

**Fix (proposed).** A kept stress-to-position table per metre from a sung corpus with lyrics; until then, the sketch's rule.

**Check.** Stressed syllables on the beat within ten points of the kept share, on song 52.

## 749.6 The bass routine reads only 4/4 bars

**Problem.** bass_v134 writes on 48-twelfth bars; it cannot write a 6/8 bass.

**Evidence.** Song 52's bass was written by hand: the root on the first beat, the fifth or a step toward the next chord on the second.

**Fix (proposed).** The bar's length and beats as parameters of the routine, with kept bass tables per metre.

**Check.** A 6/8 bass from the routine passing its window tests.

## 749.7 A dense lyric in 6/8 sits far above the folk tables' density

**Problem.** These lines carry 10 to 14 syllables in two bars of 6/8: 5.35 notes a bar against Essen's 4.0 median (75th 4.33), and sixteenths in 27% of the gaps against 5.7%. The kept windows thin out above 12 notes (31 windows of 14 notes).

**Evidence.** As above; the sketch did not charge notes a bar, the gap classes, range or distinct pitches, since the lyric and the designs set them.

**Fix (proposed).** Kept 6/8 tables by notes-a-bar cell (as 714 and 738 do for 4/4), from a corpus with more syllables a bar (sung ballads, hymns), before the engine charges rhythm in 6/8.

**Check.** The pick's gap classes inside the kept quartiles of its own cell.
