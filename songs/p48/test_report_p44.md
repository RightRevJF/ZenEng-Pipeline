---
title: "ZenEng v116: song 44, Keeping Time — test report"
author: "Words and music: Jason Bryant"
---

*Song 44 written on the v116 port (songs/p47), from the writer's essay "The Problem of the Other Mind." Findings numbered from 372 (v116's run took 365–371).*

## What was run

**Intake.** Q0–Q17, logged in intake.py:

- Q1 C, pop: one voice; the band does the phasing. Everything abstract; nothing obvious named.
- Q2 B, never-say: no theology words, no philosophy or science words and no stock love-song phrases, with one faint echo allowed. The echo used is "hear."
- Q3 B, the scene: two strangers on a dance floor.
- Q4 A, the chorus re-asks the question.
- Q5 A, the groove: mid-tempo dance-pop at 112, the pulse drifting and then locking.
- Q6 A, a mezzo.
- Q7 A, the form: 80 bars, 2:51. Q8, paring to 2:45, was withdrawn.
- Q9 A, the key: C minor verses opening to E-flat major.
- Q10 A, the title: Keeping Time.
- Q11 A, the failed answers: a face, then speech.
- Q12–Q15, the lyric: three rounds of notes, then locked at draft 4.
- Q16 A, the hook design.
- Q17 C, the lift: a narrow verse, then the chorus opens.

The never-say question was skipped for song 43 (its list was set by the session). It is asked again here (Q2), as the writer asked.

**The lyric.** 267 syllables over 68 sung bars, 3.93 a bar. That is inside the kept 3.6–4.1, so no density question was needed (342).

**The search.** melody_p44.py, built from the v116 port as song 43 was built (gen_p44.py), seed 20261554. 1,000 builds in the main run and 1,000 in the control, each made twice; both reproduced.

| Run | Survivors | Order | Rerun | Reproduced |
|---|---|---|---|---|
| main | 614 | 1a842f54b719 | 1a842f54b719 | yes |
| control | 675 | 41eff94b050a | 41eff94b050a | yes |

Deaths in the main run: limits 201, the judge's floor 81, bridge opening unrelated 52, the design 36, chorus opening another tune 11, other 5. The design gate passed 96.4% of complete builds (control 96.1%). Limit breaks counted: surprisal 215, memory 102, spectral 82, cmp 22, longest lengths in eight bars 14, others 8. 356's stop fired in round 1 (rhythm bits 2.548 against the port's middle half of 1.98–2.53), so the 354 knobs stayed at 1.0, as on song 43 under v116 (367).

**The designs.**

- **Q16 A, the hook.** 'Two clocks on the same wall' and 'It was always the same wall' rock between the clocks' two pitches, T and the scale step under it. 'Can't help keeping time, keeping time' is a pickup and then one cell (B♭4 B♭4 C5) sung twice, the second a step higher. In the post-chorus, 'fall on the one' twice lands on downbeats on T and then the step under it. 'Nobody's counting/leaving anymore' falls to a downbeat, the last on E-flat.
- **Q17 C, the lift.** The song is placed high in the mezzo's row. The verse register is seven semitones at the bottom of the drawn range. The chorus register runs to the top, ten semitones or more. The bridge carries the song's low note (329).

**The first run, before Q17.** 732 and 763 survivors, both reproduced. Its pick (6a61299cc70a) had the chorus 3.5 semitones under the verse at the median, so the hook sat at B♭3–D4. That run led to Q17.

**The pick (362).** The judge's first among the 481 of 614 survivors with no soft break: e8dc84c25324. It is the judge's second overall; the judge's first (ce86411c8473) breaks surprisal. It ranks 270th by the composite. Evaluated again, it passes every gate and the design. No hand edits.

## The record, the demo, the documents

- **The record.** 80 bars at 112, 2:51; 271 sung notes. Voice C4–D5: verse C4–G4, chorus F4–D5, a lift of 5.0 at the median. Drums, synth bass, pad and the pulse. The pulse drifts in dotted eighths in the intro, the verses and the outro, and locks to eighths from each pre-chorus's last bar. It plays alone in each chorus's fifth bar, ticking the clocks' notes an octave up. There is no kick in the bridge's first six bars.
- **Demo.** MP3, General MIDI and GarageBand MIDI. The voice is +6.2 dB over the band. The energy arc: verses 0.63 and 0.62, choruses 0.86 and 0.86, the last chorus 0.93 (the top), the bridge building from 0.25 to 0.83.
- **Lead sheet and parts.** Lead sheet, plus parts for synth bass, pulse, pad and drums. Every pitched staff reads back from LilyPond's MIDI (voice 271, bass 419, pulse 543, pad 249), and all 960 drum hits are written. Pages were checked by eye; the lead sheet and parts are limited to eight and nine systems a page so no page is compressed.
- **Nashville chart.** Each section is numbered in its own key: C minor for the intro, verses, pre-choruses and outro; E-flat for the chorus, post-chorus and bridge.
- **Songbook and production notes.** A Doc and a Word copy, with no engine terms. The references were checked by search: Robyn, "Dancing On My Own"; Caribou, "Can't Do Without You"; U2, "Where the Streets Have No Name."
- **Consistency.** 41 of 41 checks pass.

## Findings

### 372. The writer's lift (298) cannot be drawn by redrawing registers.

**Problem:** Q17 C (a narrow verse with the chorus over it and wider) was first set as a condition on the drawn registers, with redraws as 325 does. 288's kept differences between the chorus and the verse almost never give a chorus three semitones over a seven-semitone verse and three wider. And the chorus register the draw gives was too low for the hook's pitches.

**Evidence:** In a 100-build test, the registers were still missing the design after 50 draws in 99 builds, and 77 builds died at "rhythm: no placement" (the designed lines found no pitches). The lift had to be built instead. The song was placed high in the row (314's "high" placement), the verse register set at seven semitones at the bottom, and the chorus to the top. After that, 187 redraws in 1,000 builds and 96% design passes.

**Fix:** Give 298's choice a constructive form: the writer's lift sets the section registers' placement and widths directly, inside the drawn song range, and 288's kept differences are read as a reading for that song.

**Check:** A writer's lift is met in every build with no more redraws than 311's endings take; the lift is printed.

### 373. Fix 358's passing note is read on every pitch class outside the scale.

**Problem:** v116's 358 allows a note outside the scale that moves by step to both neighbours, whatever the chord, but it does not say which outside notes. The port took any.

**Evidence:** The first smoke pick sang E natural against C minor in four of its verse lines ("cuts you into stills" as E♭ E E♭ E E♭). With the passing notes read on the song's own sung extras (344: B natural and G-flat), the main run placed 2,130 passing notes. The outside-scale share is near its target.

**Fix:** 358 reads its passing notes on the song's sung extra pitch classes (344's), as 349 does.

**Check:** No passing note outside the song's sung pitch classes; the share outside the scale within two points of its target.

### 374. The surprisal limit kills a fifth of a designed, narrow-verse song.

**Problem:** 286's surprisal limit is read on the verse and the chorus's first eight bars. A verse held to seven semitones, with a chorus hook repeated by design, reads as less surprising than kept songs, so the limit breaks.

**Evidence:** Surprisal broke in 215 of the main run's builds (control 180). Limits were the main run's largest cause of death (201 of 386). Memory broke 102 times.

**Fix:** When a writer's design narrows a section or repeats a figure, read the limits that measure surprise and memory against kept songs with a like design, or print the breaks that the design itself causes.

**Check:** Surprisal breaks on a designed song printed beside the design. The share of builds lost to limits under a fifth.
