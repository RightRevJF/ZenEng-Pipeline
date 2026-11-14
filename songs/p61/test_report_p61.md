---
title: "A Wire Pulled Tight (v6): test report"
subtitle: "Words and music: Jason Bryant"
---

# Intake

| Question | Answer |
|---|---|
| Source | The writer's v5 song (songbook, number chart, lead sheet from an earlier engine); the session's read: a strong idea, a generic chorus, documents that disagree and a lead sheet missing much of the lyric, including the hook |
| What to do | Revise the lyric, then take it through Luthier v7 as song 51: "A. But Luthier that can still do different time structures" |
| Lyric | Three drafts. The writer's notes on draft 1 (pre-choruses, the chorus's abstract register, tidy lines) and draft 2 ("holds when you're holding on alone", "shook the stadium roof", the fever line's syntax, to be tested against the melody); locked at draft 3 |
| Genre | Slow-build alternative rock (A) |
| Singer | Baritone (A) |
| Tempo plan | v5's, section by section: 58, 66, 64, 70, 68, 74, 78, 82, slowing, 66, 55 (A) |
| Key | A major (A) |
| Length | Two bars a line at double tempo with a half-time feel (A); asked again after a test (18 of 20 builds died on the verse lines): verse lines four bars (A), 194 bars, 5:44 |
| Hook | Save the top note: "through" on C♯4 in choruses 1–3; E4 only in the final chorus over Asus4 to A (A) |
| Bridge | Strip then build; the second pass presses to D4; a full stop, silence, four bars of guitar (A) |
| Title | A Wire Pulled Tight, files named "(v6)" to tell them from v5 (A) |
| Chords | Revised so they are not boring (A): verse F♯m7 Dadd9 Asus2 E/G♯; pre-chorus Bm7 C♯m7 Dmaj7 E (C♯dim7 in the third); chorus from D down D, C♯, B; no full A on a downbeat until the last "through" |
| Melody | 89e71513033a (A), over the judge's pick b121d283f86f |
| Deliverables | No GarageBand MIDI; a full score instead |

# The melody search (Luthier v7)

Engine: melody_l7_p61.py, written by gen_l7_p61.py from song 50's Luthier v7 file (730 to 736 in force), with this song's key, form, chords, designs and lyric. Seed 20261113+451. The tempo plan is the playing's; the engine draws on a 4/4 beat grid written at double tempo (q = 136 its written mean). The writer's chords held as chosen (438's draw printed, not applied).

**Setup runs.** A 20-build test with two-bar verse lines: 18 died for want of a placement, at the verse lines (10 to 13 syllables). With four-bar verse lines, the deaths moved to the pre-choruses' first lines. A first full run with the flat seventh allowed in the voice put G natural over F♯m7 and E/G♯; the voice was kept to the scale and the run repeated (the first run kept in runl7/first).

| | Main | Control |
|---|---|---|
| Survivors | 376 | 368 |
| Order | a37686ce104b | 37c6e1ffbafb |
| Deaths, leading | rhythm, no placement 478; the chorus above the verse 89; limits 23; the bridge design 19 | 443; 114; 31; 25 |
| The judge's pick (730) | b121d283f86f | 38c86752b17d |

**The pick of record: 89e71513033a** (the writer's choice A). The judge's pick, b121d283f86f, opens the chorus chanting: "Every hour is a wire" and "run from the cradle to the stone" sing A3 six times each, and 16 of its 64 sung lines hold one note four or more times running (749.2). Among the 245 eligible builds, none is free of such runs. 89e71513033a is 730's rule (least charge, then nearest the kept medians within 0.02) among the 15 eligible builds with no two syllables on one onset and no run of four in chorus 1's lines: charge 0.0002 (the judge's pick 0.0002), the 86.8% place, distance 6.87 (the judge's pick 3.93); its most-repeating window at the 69.5% place. Taken as drawn, no hand edits; it passes every gate and all four designs. 3 of its lines hold a note four times.

**Each fix's own reading** (main / control):

| Fix | Reading | Target | Song 51 | Result |
|---|---|---|---|---|
| 730 | The judge's pick's most-repeating window | 55% to 93% | 88.1% / 67.3% | Pass |
| 731 | Entries, stressed first syllable | kept 20 / 42 / 38 within 10 | 13 / 51 / 36; 11 / 53 / 36 | Pass; fail by one point |
| 731 | Entries, unstressed first syllable | kept 43 / 10 / 47 within 10 | 28 / 32 / 40; 27 / 33 / 40 | Fail (749 again) |
| 732 | Bars on a kept figure; rate; 651's share | 651 in 35% to 62% | 54.3%; 0.73; 37.3% | Pass |
| 733 | Builds with every window under the kept 75th | three in four | 40.2% / 42.7% | Short |
| 734 | Easier than a neighbour; than every neighbour | 89 within 3; 73 within 5 | 86.9 / 86.7; 67.5 / 67.5 | Pass; fail by half a point |
| 735 | Drawn lines against the palette (16th; 8th; quarter) | within 10 | 21.4 v 6.4; 59.9 v 49.2; 11.8 v 27.7 (power 1.42 / 1.75) | Fail (744) |
| 735 | Bits saved a gap (median) | 13% to 36% | 0.076 / 0.079 | Fail (744) |
| 736 | Deaths for want of a placement, a thousand | under 20 | 478 / 443, all at the pre-choruses' first lines | Fail (749.3) |
| 737 | Bars sung in a kept song | 81% within 8 | 83.6% / 84.2% | Pass |

**The nineteen readings (739)** for the pick of record: inside the kept range on fifteen. Outside: the least-repeating window (7.4%, kept 25th 9.3%), distinct pitches (15, kept 75th 14), pitch-class entropy (2.84 bits, kept 75th 2.73) and gaps of a sixteenth or less (19.1%, kept 75th 18.0%): a melody with more pitches and quicker notes than most kept songs, the opposite of the judge's pick.

# Arrangement and demo

- Acoustic guitar throughout (fingerpicked, then strummed); bass from pre-chorus 1; the kit from chorus 1 (light), brushes in verse 2, full from chorus 2; clean and overdriven electric guitars; organ from chorus 1.
- Half-time throughout: the snare on beat 3 of each written bar.
- The tempo plan as tempo events, bar by bar (ramps across the pre-choruses and the approach).
- The approach: a bar of silence for every part, then the acoustic guitar alone.
- The final chorus thins to voice, acoustic and organ at the G; the band returns on the Asus4; the first full A chord on a downbeat under the release.
- Energy by section (9.12): Verse 1 0.43, Chorus 1 0.71, Verse 2 0.67, Chorus 2 0.85, Verse 3 0.70, Chorus 3 0.97, Verse 4 0.80, Bridge 0.98 (a build), Last Chorus 0.82, Tag 0.29. Each chorus above its verse; the choruses climb; the bridge the top.
- The lead stands +4.0 dB over the band (the rule asks +3).

# Documents

The lead sheet (a tempo mark at every tempo change, felt tempo shown), full score, parts (harmony high and low, acoustic, clean electric, overdriven electric, organ, bass, drums), number chart, songbook (a Doc and Word), MusicXML (lead sheet and full score) and the demo (MP3, General MIDI). Every file is named "A Wire Pulled Tight (v6)".

- Every pitched staff of the lead sheet, parts and full score reads back from LilyPond's MIDI note for note; every drum hit is written.
- MusicXML reads back with music21: onsets and pitches match the record.
- Consistency: 55/55 checks pass, including the hook's C♯4 hold over Dmaj7 in choruses 1–3, E4 only in the final chorus over Asus4 into A, no full A on a downbeat before it, the bridge's two passes and D4, the silent bar, the tag's return and A2, and every tempo of the plan in the songbook.

# The blind pick (10.20)

Three slots, offered in shuffled order (A annotated, B middle, C remembered). **The writer chose C, "a second stretched thin like a wire pulled tight": the Remembered slot,** the title line. The tally is now 33 songs: Annotated top 14, Middle 9, Remembered 9, Refrain 1.

The slots:

- **Remembered:** "a second stretched thin like a wire pulled tight"
- **Middle:** "it rings with every voice you've known" (top quartile under both)
- **Annotated:** "it hums in the dark of the house"

# Findings

The v7 findings run from 740 and the next fix is 750; 740–749 are taken, so song 51's findings are numbered 749.1 to 749.3.

## 749.1 Notes of no length: two syllables on one onset

**Problem.** Some builds place a note of no length at a bar line and the next syllable on the same onset. The evaluation passes them, and the judge can pick one.

**Evidence.** Song 51's first full run: the judge's pick 0c255388ae47 sang "stamp-ing" on two D3s at one onset (Pre 3, line 1); 71 of its 202 eligible builds had such a pair, 51 of them in verse 4. Every case found is a note of length 0 on a bar line (onset a multiple of 48) followed by a note at the same onset. The same defect is in song 50's main run (117 of 519 builds) and song 49's (171 of 939). No delivered pick has it (songs 48, 49, 50 and 51 checked).

**Fix (proposed).** Make a note of no length, or two notes on one onset in a line, a hard failure in the evaluation; then find where a kept bar's last onset at the bar's end becomes a note at the next bar line.

**Check.** No survivor with a note of length 0 or two onsets alike in a line, on songs 49 to 51.

## 749.2 The chant again: the judge's pick sings a run in the chorus's first lines

**Problem.** As 746: the readings place the judge's pick inside the kept range although its chorus opens on one note, repeated.

**Evidence.** Song 51, main: b121d283f86f sings A3 six times on "Every hour is a wire" and six times on "run from the cradle to the stone"; 16 of its 64 sung lines hold one note four or more times running; its longest run is 6, inside the kept range. Among 245 eligible builds none is free of such lines (the fewest, 3); 15 keep chorus 1's lines to runs of three or fewer. The writer chose 89e71513033a among those.

**Fix (proposed).** 746's: read runs by line and add it to 730's eligibility.

**Check.** As 746, on songs 48 to 51.

## 749.3 Placement deaths at the line after a long one

**Problem.** A line of ten syllables in two bars after a line given four dies for want of a placement in about half the builds. With the long lines in two bars, nearly every build died.

**Evidence.** Song 51 main: 478 deaths a thousand, all at the pre-choruses' first lines: "The coffee's gone cold in the paper cup" 299, "The ice is all water in the glasses" 134 and 13 in the prefit's "again", Pre 3's 22; the control's the same (242, 148, 18, 26). In the 20-build test with two-bar verse lines, 18 of 20 died, at the verse lines (10 to 13 syllables). 747 found the same on song 50 at lines of 9 to 10 syllables.

**Fix (proposed).** 230: a line's slot from its syllables before the writer's form is applied, so a line of ten or more syllables gets room (three bars, or the previous line's tail); with 747's split of held notes for lines sung again.

**Check.** Deaths for want of a placement under 20 a thousand on songs 50 and 51.
