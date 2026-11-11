---
title: "Song 41 test report: The Water Used to Sing"
subtitle: "ZenEng v109 (fixes 298–309 ported), the default path in a swung shuffle"
author: "Words and music: Jason Bryant"
---

# The run

| | |
|---|---|
| Spec | ZenEng v109. Fixes 298–309 ported onto song 40 first and tested there (port report, findings 310–313). Song 41 runs on the tested port unchanged except for its song constants. |
| Song | The Water Used to Sing. A swung shuffle, q = 96, G major, 104 bars (4:20). Male baritone, row G2–E4 sounding, written an octave up. |
| Source | *When the Bible Refuses to Behave* (Jason Bryant), used abstractly: mastery over a living thing drains its joy and sustenance. No church word is sung; one faint echo, "living water" (Q10 B). |
| Path | Default: no era, no character, no summit, no chorus lift, no drum design. |
| Designs in force | The bridge median under the verse's (Q16 B; a design gate). The countermelody in the last chorus only (Q18 B; arrangement). Two-bar slots for the 9–12-syllable lines and one-bar slots for 6–8 in verses 1–2 (Q20 A; fix 230 failed by a named design choice). |
| Seeds | 20261521, calibration 20261522, PYTHONHASHSEED 0, code 2cb5717c5b99. |
| Rerun | `PYTHONHASHSEED=0 python3 melody_p41.py 1000 main\|ctl` |
| Blocks | None. No fix had to be changed to port, and no two fixes conflicted. |

# Intake

Twenty questions, one per turn, every answer logged in intake.py:

- Idea, centre, image, title and hook (Q1–Q4).
- Sound (Q5: Americana shuffle) and form (Q6: 96 bars).
- Voice (Q7: baritone in G).
- Era, character and never-say (Q8–Q10).
- Said twice (Q11: the chorus).
- Three lyric drafts and the lock (Q12–Q14).
- The design questions (Q15–Q19).
- The slot question (Q20).

Q20 grew the form to 104 bars. Fix 308 caps a long line at int(0.57·n) syllables a bar, so a line of 9 or more syllables needs two bars. The bridge (11, 7, 9, 7, 12, 7) and verse 3 (12, 6, 9, 5, 8, 9) needed nine bars each and could not fit eight. Both became 12 bars.

# The melody search

| | Main | Control (243 off) |
|---|---|---|
| Built | 1,000 | 1,000 |
| Survivors | 615 (61.5%) | 660 (66.0%) |
| Order (made twice, same) | 615aa4e7f73d | 83c59a365e29 |
| Design gate (bridge under the verse) | 144 | 98 |
| Limits (276/277 with 286) | 142 | 118 |
| Bridge opening unrelated | 48 | 75 |
| Judge's floor | 17 | 19 |
| Key word on a chord tone | 11 | 3 |
| Placement, walk, join, align | 23 | 24 |
| Judge, survivors' median | 0.921 | 0.822 |

**The pick of record (255).** 4767e10a1dce: fourth by the composite (0.818), inside the judge's top half (judge 2.241). Inspected line by line and taken as drawn, with no hand edits. It passes every gate and the design gate, with no soft limit broken.

**What it sounds like.**

- The voice spans G2–A3, 14 of the row's 21 semitones.
- Verse A2–A3. Chorus G2–F♯3: the chorus top is 3 under the verse's, and the medians are level.
- Bridge G2–G3, its median 3 under the verse's (the design).
- The hook falls to the tonic G2 on "sing." "Now it only shines" lands on G2 over the ♭VII.
- The tag "It sings." takes the hook's last two notes and is held into the outro.
- Verse 1 has a chromatic climb (E3 F3 F♯3 G3 A3), and B♭2 blue notes fall on "fair," "grey," "watch" and "mule."
- Ten leaps past a fifth inside lines. One is a minor seventh up onto an unstressed "a" (bar 11).

# Arrangement and documents

**The intro lick (235).** 1,185 drawn and 152 passed. The pick is a root–fifth figure on the offbeats (onsets 6, 12, 24, 30), unrelated to every sung opening.

**The break.** The first draw passed: chord tones on the beats 0.65, no tritone, rhythm inside the band. Its top note was found at A6 in the first build: the octave repair cascaded. The solo is now folded to C6 at most and checked (top B5).

**Fills.** Four in the choruses' six gaps (one open by the 30% draw, one short gap open).

**The countermelody.** G4–E5, always above the voice, no semitone and no tritone. 3 of the 13 shared onsets are unisons or octaves.

**The demo.** The voice is +6.2 dB over the band. The energy arc meets 9.12: each chorus is above its verse, the bridge is the floor and the last chorus is the top. The swing is applied in playback only. The drum kit changes between brush and standard by program change.

**Readback.** The voice reads back from the lead sheet (326 of 326 notes). Six parts read back, and all 1,064 drum hits are written.

**Consistency.** 43 of 43 checks pass.

# Readings the paper does not give

- **288.** The verse's place in the voice row: verse centre E3, cap A3, floor A2 are the session's numbers. The chorus and bridge are drawn relative to them.
- **208 (Q16 B).** The design's aim: the bridge median 1.5 to 5 semitones under the verse's, drawn evenly, and the gate read on the sung medians.
- **230 (Q20 A).** The verse slots 2-1-2-1-1-1 shared by verses 1 and 2, and verse 3 at two bars a line.
- **228/293.** Verse 3 sung again from verse 1 (the paper names verse 2 only), its bars copied at 40% into longer slots.
- **213.** The last chorus's plan:
  - Lines 1–2 are copies.
  - Line 3 is a return of the hook (the second pass varied, the writer's note).
  - Line 6 is a return of line 5 or fresh, drawn.
  - Line 7 is a return of the chorus's last line or fresh, drawn.
  - The tag is the hook's last two syllables.
- **235.**
  - The lick from G3; the fills from A3 to G5.
  - The solo held to C6.
  - The countermelody's row G4–E5 and its rule: it moves where the voice holds and holds a chord tone where the voice moves.
- **236.** Brushes and sticks by section; sticks at verse 3's fifth bar.
- **200.** B♭ and F as the flat 3 and flat 7 in G.
- **Swing.** No reading: the playback ratio 2:1 is the session's.

# Findings (from 314)

**314. The verse's place in the row decides the song's register, and the paper doesn't give it.**

- *Problem.* Fix 288 draws the chorus and bridge registers against the verse's, but the verse's centre, cap and floor are the session's numbers. Here they put the whole song in the row's low octave.
- *Evidence.*
  - 98.5% of main survivors (and every control survivor) touch G2, the row's floor.
  - The top note is A3 at the median.
  - 54% of survivors never go above A3, 59% never above B♭3, and 14% reach E4.
  - The pick spans G2–A3 with its chorus top 3 under the verse's; 36% of survivors have the chorus top under the verse's.
  - The bridge-below design and the hook's tonic ending (262/302) both press toward the floor.
- *Fix.* Count where the verse sits in the singer's row in kept songs (its median and top as a share of the row), and draw the verse register from that per build, as 288 draws the rest.
- *Check.* The survivors' top note and lowest note against the kept shares, and the row's top fifth used in about the kept share of builds.

**315. Fix 305's amplitude is set by its clip, not by its reading (312, twice over).**

- *Problem.* The calibration multiplies the arch amplitude by at most 1.6 a round. On this song it took the most every round: 5 × 1.6³ = 20.48 in both runs.
- *Evidence.*
  - The reading at the last round was 0.132 against the aimed 0.23.
  - The survivors' arch over the span is 0.161 at the median.
  - Leaps past a fifth in the verse window are 0.119 at the median: the judge's kept mean is 0.021, and song 40's port read 0.05.
  - The pick has ten leaps past a fifth, one a minor seventh onto a weak syllable.
- *Fix.* As 312: draw the arch through the walk's direction (steps toward the contour), not a taller contour. Or stop the calibration when the amplitude's last two rounds both hit the clip, and report it.
- *Check.* The amplitude settles before its clip, and past_fifth sits at the kept median with the arch over the span near 0.23.

**316. Fix 308's cap costs about four tries per long line.**

- *Problem.* With the entry and the landing drawn first (231, 260), a 12-syllable line in two bars with a cap of 6 a bar has very few placements, and most draws find none.
- *Evidence.*
  - 37,711 long-line redraws in 1,000 builds (main), about four per long line.
  - 99 lines placed with a free entry and landing.
  - Only 7 builds died at placement.
- *Fix.* For a line of 9 or more syllables, draw the entry and landing only from those that admit the cap.
- *Check.* Redraws per long line under 1.5, and the entry and landing shares unchanged.

**317. A design gate on a sung median passes under nine builds in ten (275).**

- *Problem.* The bridge is aimed 1.5 to 5 semitones under the verse, but the walk's median drifts, and the gate reads the sung medians.
- *Evidence.* The gate killed 14.4% of main builds and 9.8% of control builds. That is under 275's nine in ten.
- *Fix.* Either read a register design on the drawn register (the aim) and print the sung reading, or let a design gate stand outside 275 and print its pass rate.
- *Check.* A design gate's pass rate printed before the run.

**318. A shuffle draws sixteenths at straight pop's rate.**

- *Problem.* The class's rhythm table and 288's sixteenth offer (14.7%) come from straight-eighth pop. In a swung feel the sixteenth is rare and awkward, because the swung eighth already fills the beat.
- *Evidence.*
  - 16.7% of the pick's inner gaps are sixteenths.
  - The survivors' median share of onsets on sixteenth positions is 12%.
  - The lead sheet is written straight, so the singer meets sixteenth pairs under a swing mark.
- *Fix.* Add a feel at intake. Under swing, the grid is the triplet eighth and the sixteenth share comes from kept swung songs (to be counted).
- *Check.* The sixteenth share in swung builds at the kept swung rate.

**319. The break solo's octave repair can climb out of the instrument.**

- *Problem.* Song 38's solo method folds each note toward the one before by octaves. A run of folds can cascade upward.
- *Evidence.* The first solo drawn reached A6 (MIDI 93), past a 24-fret guitar's top E6. The solo check (chord tones, tritones, rhythm, leap) passed it.
- *Fix.* The solo check also reads the instrument's range. Folded here to C6.
- *Check.* No solo note outside its instrument's range.

# Blind pick

Not yet run: offered after delivery.
