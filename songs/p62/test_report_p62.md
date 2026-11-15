---
title: "The Room Next Door: test report, third edition"
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

# After delivery: chorus 2 varied, the harmony rewritten

The writer: "One of the comments that I get frequently from other ais is that the chorus music stays identical throughout the song and that the harmony don't move far. Is that deliberate or a limitation of the engine?" The answer: the copy is deliberate, the lack of any rule for varying a returning chorus is a limitation, and the harmony rule (the nearest chord tone a third or fourth away, in the lead's rhythm) is a limitation. He chose C: revise song 52 as a test, then add the findings with the before and after.

**Chorus 2 (vary68.py).** The first line and the hook stay exact. On each inner line, the longest held note that is stressed (or the line's last) is lifted to the nearest chord tone above, within a minor third (a fourth for a line's last note), at or under C♯5, no run of four, no leap past a fifth. The final chorus's second line takes chorus 2's version.

| Line | Word | Chorus 1 | Chorus 2 |
|---|---|---|---|
| 2 | "sunlight" (bar 34) | A4 | B4 |
| 3 | "door" (bar 36) | E4 | A4 |
| 4 | "all" (bar 38) | A4 | B4 |

3 of chorus 2's 49 notes changed (none before); rhythm unchanged; every gate still passes; the readings' charge unchanged at 1.69. The melody's fingerprint is now 9bf4a225b954 (drawn as 8f4cc7fe75bf).

**The harmony (harm68.py).** The high part sings the words, chosen as one line over each phrase by least cost: small moves and held notes cheap, contrary and oblique motion cheaper than similar, parallel fifths and octaves and tritones ruled out, thirds the home interval. The low part sings "ooh" in long notes under the lead, at most one change a beat, chord tones only, no second, seventh or tritone against a lead note of an eighth or longer.

Read at each pair of the lead's onsets inside the harmony (the hook in every chorus, every line of the final chorus):

| Reading | High, before | High, after | Low, before | Low, after |
|---|---|---|---|---|
| Moves with the lead (similar) | 74% | 22% | 85% | 15% |
| Moves against it (contrary) | 0% | 12% | 0% | 2% |
| Holds while it moves, or the reverse (oblique) | 26% | 66% | 15% | 83% |
| Parallel fifths or octaves | 0 | 0 | 0 | 0 |
| Distinct distances from the lead | 3 | 6 | 3 | 9 |
| Farthest from the lead (semitones) | 5 | 9 | 5 | 12 |
| Notes | 70 | 70 | 70 | 18 |
| Held notes (a dotted quarter or more) | 9 | 9 | 9 | 17 |
| Mean move (semitones) | 2.1 | 1.0 | 2.2 | 3.1 |

Every document rebuilt from the new record; every staff reads back note for note; consistency 52/52 (eight new checks: chorus 2's first line and hook exact, one lift per inner line, lifts upward and under C♯5, the final chorus's second line as chorus 2's, no parallel fifths or octaves, neither part moving with the lead more than half the time, the high part on every syllable, the parts on their sides of the lead).

## 749.8 A returning chorus has no rule for change

**Problem.** 'copy' sings chorus 2 exactly as chorus 1. The hook should return unchanged, but a whole chorus sung note for note again reads as a loop, and readers flag it.

**Evidence.** Song 52 before: chorus 2 differed from chorus 1 in 0 of 49 notes; songs 48 to 51 the same. After the lift rule: 3 of 49, each a held note raised to a chord tone, the hook and first line exact, every gate and the charge unchanged.

**Fix (proposed).** 'copy' becomes 'return': the first line and the hook exact; on each inner line, at most one held note lifted as above; the final chorus takes the returning chorus's lifts on its copied lines. Optional later: a rhythmic variant for a line whose words change.

**Check.** On songs 48 to 52, each returning chorus differs from the first in 1 to 10% of its notes, never in its hook, and passes every gate.

## 749.9 The harmony shadows the lead

**Problem.** The harmony parts take the nearest chord tone a third or fourth from each lead note, in the lead's rhythm, so they move with the lead almost all the time, never against it, and keep to three distances from it.

**Evidence.** As in the table: before, the high part moved with the lead 74% of the time and never against it; the low part 85%. After: 22% and 15%, contrary motion 12% and 2%, holding 66% and 83%, and no parallel fifths or octaves in either version.

**Fix (proposed).** Harmony written as lines (harm68.py): a high part with the words chosen by least cost over the phrase, and a low "ooh" part in long notes; readings for motion against the lead added to the checks.

**Check.** Each part moves with the lead under half the time, no parallel fifths or octaves, on songs 48 to 52.

# Third edition: the song shaped as a whole

The writer: "The melody's long range structure still doesn't change much. Is that by design or limitation?" The answer: the strophic verse is by design; that nothing plans or reads the song as a whole is a limitation (every reading is local: per note, per bar, per two-bar window; registers come from a section's kind, never its place). He chose B: try a song-wide shape on song 52 as a third edition, measured before and after.

**The plan (shape68.py).** Verses 1 and 2 as drawn; verse 3 about three quarters of a semitone higher on average, verse 4 about one and three quarters, cap B4; choruses 1 and 2 as they are; the last chorus's lines above chorus 2's, cap C♯5; the bridge the hush; the song's top moved late: the last chorus's first "door" on E5, once. A section meets its target by whole lines moving up one step of the scale (the latest line first, each once), the shape kept; a stressed, long or on-the-beat note out of its chord moves to the nearest chord tone, a note over the cap comes down, over B♭ no F♯, C♯ or B, the voice in the scale, no run of four (the weakest note of one takes the next fit), no leap past a fifth. A first try that lifted single notes again and again (134 lifts, notes moved up to a fifth) bent the tunes and pushed leaps out of the kept range; it was dropped.

Lines moved: Verse 3 line 4 (7 notes); Verse 3 line 3 (9 notes); Verse 3 line 2 (6 notes); Verse 4 line 4 (10 notes); Verse 4 line 3 (12 notes); Verse 4 line 2 (8 notes); Verse 4 line 1 (11 notes); Last Chorus line 4 (7 notes); Last Chorus line 3 (10 notes); Last Chorus line 2 (11 notes); Last Chorus line 1 (8 notes); and "door" D5 to E5 (bar 77).

| Section | Mean pitch before | After | Change |
|---|---|---|---|
| Verse 1 | 64.5 | 64.5 | +0.0 |
| Chorus 1 | 67.9 | 67.9 | +0.0 |
| Verse 2 | 64.6 | 64.6 | +0.0 |
| Chorus 2 | 68.1 | 68.1 | +0.0 |
| Verse 3 | 64.4 | 65.5 | +1.0 |
| Bridge | 63.9 | 63.9 | +0.0 |
| Verse 4 | 64.3 | 66.4 | +2.1 |
| Last Chorus | 67.3 | 68.7 | +1.4 |

| Song-level reading | Before | After |
|---|---|---|
| Verse 4 over verse 1 | -0.19 | +1.88 |
| The verses rise in order | no | yes |
| Last chorus over chorus 1 (lines before the hook) | -0.75 | +0.99 |
| Top note; bar of its first sounding | D5; bar 21 | E5; bar 77 |
| Share of the song before the top | 24% | 90% |

The note-level readings barely move: charge unchanged at 1.69; leaps 12.5% (12.5% before; kept range 7.0 to 16.7); longest run of one pitch 4 across a line join (each line still under four). The melody's fingerprint is now e1051a4a6d7f. The voice's range is now B3 to E5. The harmony, rewritten against the new lead: high part with the lead 23%, against 15%, holding 62%; low part 17%, 2%, 81%; no parallels. Documents rebuilt, every staff reads back, consistency 55/55 (three new checks: the verses rise, the last chorus the highest chorus, the top in the song's last fifth; the hook checks moved to E5 in the last chorus).

## 749.10 Nothing plans or reads the song as a whole

**Problem.** Every reading the engine charges is local, and every register comes from the section's kind. So the verses sit at one height, the last chorus is no higher than the first, and the song's top comes early.

**Evidence.** Song 52 before: verses 1 to 4 within 0.2 semitones of each other on average (B3 to A4 each); the last chorus's lines 0.75 below chorus 1's; the top, D5, first in bar 21 of 84 (24% of the way in). After the plan above: verses 64.5, 64.6, 65.5, 66.4; the last chorus's lines 1.0 above chorus 1's; the top, E5, in bar 77 (90%); the note-level readings and charge unchanged.

**Fix (proposed).** A song plan read before the melody is drawn: a target mean for each section by its place (the strophic sections may hold, the later ones rise), and the song's top placed late; reached by moving whole lines by a step of the scale, as tried. Song-level readings added to the judge: the verses' rise, the last chorus against the first, the top's place. A key change is a later option.

**Check.** On songs 48 to 52: the later verses at or above the first, the last chorus above the first, the top in the last third, with every note-level reading still in its kept range.

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
