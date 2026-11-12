---
title: "ZenEng v116: song 45, Before It's Done — test report"
author: "Words and music: Jason Bryant"
---

*Song 45 written on the v116 port (songs/p47), from the writer's book "You Will Wake" (read, used, not stored). Findings numbered from 375 (song 44 took 372–374).*

## What was run

**Intake.** Q0–Q15, logged in intake.py:

- Q0, the brief (the writer's words): a tearjerker all the way with a hopeful ending, capturing the book's theology.
- Q1 A, the unfinished conversation carries the song. Q2 A, he sings to her.
- Q3 A, never-say: asked at intake, as the writer asked after song 43. Eighteen words (the names among them) and nine stock phrases.
- Q4 B, the sound: fingerpicked acoustic guitar at about 72, a cello under the second verse. The writer added: a guitar-only whole score, so a friend with a guitar could just play it.
- Q5 A, a man's middle voice. Q6 A, G major with the last chorus a whole step up in A. The writer added: don't dumb the music down to make it playable.
- Q7 A, the form: 56 bars, about 3:07. Q8 A, the title.
- Q9–Q12, the lyric: four drafts with the writer's notes, locked at draft 4.
- Q13 A, density (342): 275 syllables over 52 sung bars, 5.29 a bar, over the kept 3.6–4.1; kept as written.
- Q14 A, the chorus over the verse (298). Q15 A, the chorus design: "thought" held over a sus chord; "before it's done" stepping down to the 2nd (to the tonic in the last chorus); the tag ending on the 2nd.
- Q16 A, after delivery: hand-edit the two weak lines of the pick, log the edits and rebuild every document.

**The search.** melody_p45.py, built from the v116 port as song 44 was (gen_p45.py), seed 20261555. The search runs in G (row B2–D4); the last chorus and the tag are lifted two semitones in the record. 1,000 builds in the main run and 1,000 in the control, each made twice; both reproduced.

| Run | Survivors | Order | Rerun | Reproduced |
|---|---|---|---|---|
| main | 476 | d2ec0ab81d82 | d2ec0ab81d82 | yes |
| control | 546 | 37097d8bd9f3 | 37097d8bd9f3 | yes |

Deaths in the main run: the design 155, align 133, limits 80, returns related 80, the join (212) 51, bridge opening unrelated 18, the judge's floor 5, key word 2. The design gate passed 81.0% of complete builds (control 86.4%). Limit breaks counted: surprisal 159, run_max 112, cmp 13, sequence legs 5, spectral 5, memory 3, others 3. 356's stop fired in round 2 (rhythm bits 1.966, under the port's middle half), and in the same round the "fresh" knob froze after two largest steps (376).

**The designs.**

- **Q14 A, the lift.** As song 44 (372): the song placed high in the row, the verse register eight semitones at the bottom, the chorus register to the top. The design register test also needs the chorus register to hold G3–D4 (the designed notes). 176 register redraws in 1,000 builds.
- **Q15 A, the chorus.** Chorus 1, line 1 has a designed rhythm: "HOLD that THOUGHT, I'm STILL COM-ing" on 0, 12, 24, 54, 60, 72, 84 (twelfths of a beat); "thought" is pinned to G or D in the register, held 30. The last chorus, line 1 ("It's MORN-ing, and I HELD the THOUGHT") has its own designed rhythm, with "morning" held where "thought" was, and takes the chorus's pitches on every onset it shares with it (the passing syllables between pinned to a step). "Before it's done" is pinned D4 C4 B3 A3 in chorus 1 (copied in chorus 2) and C4 B3 A3 G3 in the last chorus (lifted: D4 C♯4 B3 A3). The tag's last note is pinned A3 (lifted: B3). Pinned notes take one note a syllable and are kept out of 349 and 215's moves.

**The pick (362).** The judge's first among the 371 of 476 survivors with no soft break: 10c3fce99da2, which is also the judge's first overall (combined 3.967). It ranks 50th by the composite. Evaluated again, it passes every gate and the design.

**The writer's hand edits (Q16 A).** Logged in the pick (edit_p45.py) and evaluated again: it still passes every gate and the design, with no soft break.

- Verse 2, line 1 ("I knew the room before they let us in"): eight E3s in a row, then A3 G3. Re-pitched on the drawn rhythm: E3 G3 F♯3 E3 D3 E3 G3 G3 A3 G3.
- Chorus, line 2 ("You're only in the next room"): six sixteenths and a bar and a half of rest (378). Re-set in eighths and quarters: D4 B3 A3 G3 E3, then "next" A3 on the downbeat and "room" G3 held two beats. Chorus 2 copies it.
- The last chorus's return of that line, re-set to the same rhythm and tune with a two-sixteenth pickup (D4 C4). It stays related to its source (267).

The judge reads the edited melody lower (combined 2.712, from 3.967); the composite rises (0.830, from 0.805). Every other line is the pick as drawn.

## The record, the demo, the documents

- **The record.** 56 bars at 72, 3:07; 278 sung notes. Voice D3–E4: verse D3–A3, chorus E3–D4, a lift of 5.0 at the median; the last chorus and the tag a whole step up, reaching E4. Guitar and cello.
- **The guitar.** Steel-string, standard tuning, no capo; every note carries its string and fret (516 notes, frets 0–5). Open-string voicings (G, D/F♯, Em7, Cadd9, Am7, Dsus4–D; in A: Asus4–A, E/G♯, F♯m7, Dadd9). The chorus bass walks G–F♯–E–C (in A, A–G♯–F♯–D). Gsus4 resolves to G under "thought." The intro's last bar plays the chorus ending (D C B A) and the tag's last bar E D C♯ B, arriving on the singer's last note. The guitar reads the sung note over D (in A, over E): the sus4 where the voice holds the fourth, the plain chord where it sings the third (379). Each note rings until its string is played again or the hand leaves its fret.
- **The cello.** Written for this tune: a falling line under verse 2, a high line over chorus 2, low held notes in the bridge with a swell into the key change, half notes in the last chorus (taking the suspension over "morning"; C♯5 at the top), and A F♯ E D in the tag.
- **Demo.** MP3, General MIDI and GarageBand MIDI. The voice is +7.2 dB over the band. The energy arc: verses 0.27 and 0.46, choruses 0.42 and 0.63, the bridge building from 0.22 to 0.50, the last chorus 0.76 (the top), the tag 0.31.
- **Voice and guitar.** The guitar-only whole score the writer asked for: voice and words over the guitar in notation (two voices, the thumb stems down) and TAB with string numbers, chord shapes above. Three pages.
- **Lead sheet and parts.** Lead sheet (voice, words, chords); parts for guitar (notation and TAB) and cello (tenor clef for its high lines). Every staff reads back from LilyPond's MIDI (voice 278, guitar treble 414, guitar thumb 102, cello 51); the TAB's strings and frets agree with the pitches. Pages checked by eye.
- **Nashville chart.** Numbered in G through the bridge and in A from the last chorus, from the guitar's shapes; a bar split where a sus resolves at the half bar.
- **Songbook and production notes.** A Doc and a Word copy, with no engine terms. The references were checked by search: Eric Clapton, "Tears in Heaven"; Jason Isbell and the 400 Unit, "If We Were Vampires"; Sufjan Stevens, "Fourth of July."
- **Consistency.** 48 of 48 checks pass.

## Findings

### 375. The bridge's secondary dominant is not read as a clash against an in-scale note.

**Problem:** The bridge ends on E major (V of A, leading into the lift). 200's clash test reads only notes outside the scale, so a sung G natural against the E chord's G♯ passes as consonant. And 349 had only one outside pitch class (G♯) to place, so its drawn share went mostly wanting.

**Evidence:** The song's post-process raised a sung G to G♯ over the E chord 782 times in the main run's 1,000 builds. 349 placed 3,073 notes and wanted 53,814 places; 358 placed 2,962 passing G♯s, over any chord.

**Fix:** Read a chord's own tones outside the scale (a secondary dominant's raised third) as chord tones for that bar, so a sung note a semitone from one clashes; and read 349's target on the song's extra pitch classes that its chords allow.

**Check:** No sung natural a semitone from a secondary dominant's raised third. 349's places wanting under a tenth of its target.

### 376. Calibration crashes when a knob freezes: the round number read a shadowed variable.

**Problem:** When a line knob takes the largest step two rounds running, calibration freezes it and prints a message. The message read `rd`, which by then is the round's reading (a dict), so the run crashed. Songs 40–44 never reached that path.

**Evidence:** Song 45's first smoke run crashed with a TypeError in calibrate. The "fresh" knob froze in round 2 (5.12). The song's generator reads the round from CAL_ROUNDS (as 356's message does). The committed v116 files for songs 40–44 are unchanged, and none of their runs reached the path.

**Fix:** The frozen-knob message reads the round counter, not the reading.

**Check:** A run in which a knob freezes completes and prints the round.

### 377. The writer's lift still kills a sixth of the builds when the chorus's designed notes sit low.

**Problem:** Q14 A asks for the chorus median three semitones over the verse's, read on what is sung. The registers are built for it (372). But the chorus's designed notes sit in its lower half: "thought" on G3 or D4, the ending D4 C4 B3 A3, and the tag on A3 in the same register. They pull the sung chorus median down toward the verse's.

**Evidence:** A diagnostic run with the design gate's parts counted (same order, d2ec0ab81d82) failed only the lift: 310 of 1,632 readings, 155 deaths. "Thought" and the ending never failed. The pick's lift is 5.0.

**Fix:** When designed notes are pinned in a section, place the section's register so its undrawn notes carry the lift; or read the lift on the drawn notes and print the designed notes' median beside it.

**Check:** The lift gate's deaths under a twentieth on a song with pinned notes; both medians printed.

### 378. Line rhythm is tempo-blind: at 72 a short line rushes in sixteenths and leaves a long gap.

**Problem:** The rhythm tables and the 341–346 knobs count note lengths in beats, whatever the tempo. At ♩ = 72 a sixteenth is 0.21 seconds. A seven-syllable line in a two-bar slot can be drawn as a beat and a half of sixteenths followed by a bar and a half of rest.

**Evidence:** "You're only in the next room" (chorus, bar 15) is sung C4 B3 F♯3 G3 E3 F♯3 on six sixteenths, "room" on beat 3, then rest until bar 17. Sixteenths are 28% of the pick's notes, against 17% in song 44's pick at 112. The main run's survivors have a median of 21%. The writer had the line re-set by hand (Q16 A).

**Fix:** Read the note-length tables in seconds, or in tempo bands, so a ballad's line spreads across its slot. A short line in a long slot should prefer longer notes to a long rest.

**Check:** At ♩ ≤ 80, the share of sixteenth notes within the kept ballad share; no line whose notes fill under half its slot when its syllables would fill it in eighths.

### 379. The arrangement does not read the sung note over a held chord.

**Problem:** The design holds "thought" across the bar line into the D chord (bar 14), and the engine sang the fourth (G) over D in other places. A D/F♯ under a held G is a minor ninth. Where the voice sang F♯ over a planned Dsus4, the reverse clash appeared. The spec has no rule for the accompaniment to follow the voice.

**Evidence:** A semitone check of sung notes (a beat or longer, or on a beat) against everything sounding found 33 of 278 notes in the first arrangement. With the guitar reading the voice (the sus4 where the fourth is held an eighth or more and longer than the third, the plain chord where the third is sung) and notes damped when the hand leaves their fret, 13 remain, all passing sixteenths and eighths (10 after the hand edits). Four half bars took the sus4; four took the plain D.

**Fix:** A rule for arrangements: over each half bar, the chord's sus or plain form follows the sung note held there; a sustained instrument note a semitone from a held sung note is moved. Add the semitone check to the consistency checks.

**Check:** No held sung note (a beat or longer) a semitone or minor ninth from a sustained accompaniment note.
