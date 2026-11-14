---
title: "The Small Things: test report"
subtitle: "Words and music: Jason Bryant"
---

# Intake

| Question | Answer |
|---|---|
| Lyric | The writer's own (first called "Late afternoon"); one fix at his request ("at old Sammie in his crouch"); his sketched chords set aside; locked as shown |
| Sound | Gentle acoustic folk: fingerpicked guitar, soft piano (A) |
| Beat | A lilting 6/8 (A), asked again when the session found Luthier is 4/4 only: 4/4 with a slow swing (A) |
| Key | D major (he answered "D", taken as option A) |
| Form | Intro 4, verse 16, chorus 16, verse 16, chorus 16, bridge 8, last chorus 16, outro 4: 96 bars at ♩ = 88 swung, about 4:22 (C) |
| Singer | Baritone, A2 to D4 |
| Hook | "I think God likes the small things" climbs to D4 on "small", held; "I think He always will" lands home on D3 (A) |
| Bridge | Lines 1 to 3 low (A2 to D3), guitar alone; a beat of silence; "and the holy showed up clear" rises to A3 and holds, open (A) |
| Title | The Small Things (A) |
| Deliverables | No GarageBand MIDI; a full score instead |
| Pick | The judge's pick, f583fd857dda: "this melody works for the song: build everything from it" (A) |

# The melody search (Luthier v7)

Engine: melody_l7_p60.py, written by gen_l7_p60.py from song 49's Luthier v7 file (730 to 736 in force), with the song's own key, plan, designs and lyric. Seed 20261113+450; 1,000 builds each, main and control. Swing is in the demo only; the engine draws straight 4/4.

| | Main | Control |
|---|---|---|
| Survivors | 284 | 234 |
| Clean | 223 | 206 |
| Order | 46073782f2d5 | cd7f41ab51d3 |
| Deaths, leading | rhythm, no placement 244; the chorus above the verse 223; join 209; align 28; limits 9 | the chorus above the verse 254; rhythm, no placement 233; join 233; align 31; limits 8 |
| The judge's pick (730) | f583fd857dda | 20c6b0cba73d |

Of the join deaths, 121 (main) are at Bridge line 3, the chant into the designed silence: 212 asks a held end and a breath before the copy, and the line's first beat is the silence itself. Printed, not numbered.

**The pick of record: f583fd857dda**, the judge's pick and the engine's, taken as drawn with no hand edits (the writer's choice A). Eligible under 715: 195 of 223 clean; under 730: 149. Charge 0.0137, the 84.3% place, distance 2.33 (median build: charge 0.0084, the 84.9% place). Its most-repeating window is the bridge, at the 71.4% place for its density (kept middle half 55.2% to 93.4%). It passes every gate and all three designs: the hook's figure and top D4; the bridge low, chanted and silent at line 3; the chorus two semitones and more over the verse.

The session told the writer before he chose: the pick repeats notes inside lines (chorus lines 1 and 2 open on D3 five times; "and the afternoon holds still" sings A3 five times), and only 1 of the 149 eligible builds has no in-line run of four or more equal notes (746).

**Each fix's own reading** (main / control):

| Fix | Reading | Target | Song 50 | Result |
|---|---|---|---|---|
| 730 | The pick's most-repeating window, place | kept middle half, 55% to 93% | 71.4% / 69.5% | Pass |
| 730 | Clean builds whose most-repeating window lies over / under the middle half | | 5.4% / 20.6% | Printed |
| 731 | Entries before / on / after, stressed first syllable | kept 20 / 42 / 38 | 21 / 40 / 39 | Pass |
| 731 | The same, unstressed first syllable | kept 43 / 10 / 47 | 24 / 33 / 44 | Fail (749) |
| 732 | Bars on a kept figure (717); its rate; 651's share | 651 in 35% to 62% | 55.5%; 0.83; 46.1% | Pass |
| 733 | Builds with every window under the kept 75th | three in four | 70.1% / 65.0% | Short |
| 733 | Longest run of one pitch (25th, 50th, 75th) | kept 4 to 7 | 6, 7, 8 | At the top |
| 734 | Sung note easier than a neighbour; than every neighbour | 89% within 3; 73% within 5 | 88.3 / 88.1; 71.6 / 71.2 | Pass; pass |
| 735 | Bits saved a gap (median) | kept 13% to 36% | 0.067 / 0.063 | Fail (744 again) |
| 736 | Deaths for want of a placement, a thousand | under 20 | 244 / 233 | Fail (747) |
| 737 | Bars sung in a kept song, every complete build | 81% within 8 | 79.5% / 78.9% | Pass |

**The nineteen readings (739)**, the pick against the kept quartiles. Inside the kept range on fifteen. Outside on three, all motion:

| Reading | The pick | Median clean build | Kept 25th, 50th, 75th |
|---|---|---|---|
| Moves by step | 33.3% | 46.2% | 34.8, 41.3, 50.5 |
| Moves by leap (5 semitones or more) | 21.2% | 8.8% | 7.4, 10.4, 14.2 |
| Turns of direction | 66.1% | 59.4% | 52.6, 58.3, 66.1 |
| Longest run of one pitch | 7 | 7 | 4, 6, 7.5 |
| Bars of one pitch | 10.5% | 5.3% | 0, 3.6, 12.2 |
| Range, semitones | 17 | 17 | 14, 17, 21 |
| Median pitch, two largest sections, difference | 3 | 3 | 1, 2, 5 |

The control's pick is outside on four (entropy, eighths, quarters, first beats) and on bars of one pitch (12.3%).

# Arrangement and demo

- Fingerpicked acoustic guitar throughout (travis: thumb on root and fifth, fingers between), swung in playback (the offbeat eighth at two-thirds of the beat).
- Piano: the hook's tune in the intro; answers in verse 2; chords in the choruses; out in the bridge; "I think He always will" echoed in the outro.
- Acoustic bass from halfway through verse 1; out in the bridge.
- Brushes: rim in chorus 1, snare in chorus 2 and the last chorus.
- Harmony (above and below) on the hook lines and on every line of the last chorus.
- The bridge: guitar alone, one beat of silence for every part at bar 75.
- The last line slows by tempo events to 0.66 of ♩ = 88.
- Energy by section (9.12): Intro 0.33, Verse 1 0.69 (a build), Chorus 1 0.73, Verse 2 0.74, Chorus 2 0.81, Bridge 0.08 (the drop, by design), Last Chorus 0.86, Outro 0.32. Each chorus is above its verse; the last chorus is the top.
- The lead stands +5.7 dB over the band (the rule asks +3).

# Documents

Built from the pick of record: the lead sheet, full score, parts (harmony, guitar, piano, bass, drums), number chart, songbook (a Doc and Word), MusicXML (lead sheet and full score) and the demo (MP3, General MIDI). The songbook's bar numbers, pitches and chords are read from the record.

- Every pitched staff of the lead sheet, parts and full score reads back from LilyPond's MIDI note for note.
- MusicXML reads back with music21: onsets and pitches match the record.
- Consistency: 42/42 checks pass, including the hook's held D4 and D3 landing, the bridge's silent beat, its rise to A3, and the ritardando.

# The blind pick (10.20)

Three slots, offered after delivery in shuffled order (A annotated, B remembered, C middle). **The writer chose C, "And I think somebody's watching this": the Middle slot.** The tally is now 32 songs: Annotated top 14, Middle 9, Remembered 8, Refrain 1.

The slots:

- **Remembered:** "I think God likes the small things" (the most-repeated hook line)
- **Middle:** "And I think somebody's watching this"
- **Annotated:** "A bumblebee goes bouncing by"


# Findings

## 746 The pick sings runs of one note inside lines, and no reading sees it

**Problem.** The judge's pick repeats a pitch four or more times running inside sung lines, and the readings all place it inside the kept range.

**Evidence.** Song 50, main: f583fd857dda opens chorus lines 1 and 2 on D3 five times and sings "and the afternoon holds still" on A3 five times. Its longest run is 7 (kept 4 to 7.5) and its bars of one pitch 10.5% (kept 75th 12.2%), both inside. Its windows pass 713's ceiling and 730's place (71.4%). Of the 149 builds eligible under 730, 1 has no in-line run of four or more equal notes. The writer took the pick knowing this.

**Fix (proposed).** Read runs by line: the share of sung lines with a run of four or more equal notes, against the kept share for the line's density, with a ceiling at the kept 75th; add it to 730's eligibility.

**Check.** On songs 48 to 50, the share of eligible builds with in-line runs falls to the kept share, and the pick's lines lie under the ceiling.

## 747 Placement deaths where a line outgrows its source

**Problem.** 736 uncaps copied bars, but a line with more syllables than its source line has notes still finds no placement.

**Evidence.** 244 / 233 deaths a thousand (the target is under 20). Main: Chorus 1 line 1, 84 ("And I think somebody's watching this", 9 syllables); Verse 2 line 3 in the prefit's "again", 81, and in the draw, 58 ("just Sammie and Maggie doing their work", 10 syllables, over "Sammie takes his post again", 7 notes); Verse 2 line 1, 16. The control's spread is the same.

**Fix (proposed).** When a returning line has more syllables than its source has notes, split the source's longest notes (a held note becomes two of the same pitch) before the prefit tries again, up to 308's cap; only then draw.

**Check.** Deaths for want of a placement under 20 a thousand on song 50; the returning tune still read as the same (align).

## 748 The judge does not read motion, so its pick leaps

**Problem.** 730's eligibility reads repeats and ease, not steps and leaps. The pick lies outside the kept range on all three motion readings.

**Evidence.** The pick moves by step in 33.3% of its moves (kept 25th 34.8%), by leap in 21.2% (kept 75th 14.2%), and turns in 66.1% (kept 75th 66.1%). The median clean build: 46.2%, 8.8%, 59.4%, all inside. The designed hook and bridge rise contain no leap of 5 semitones or more, so the leaps are the engine's.

**Fix (proposed).** Add steps and leaps to 730's eligibility, inside the kept middle half, or charge them in the judge's distance.

**Check.** The pick's steps and leaps inside the kept range on songs 48 to 50.

## 749 Unstressed first syllables enter on the beat three times as often as kept songs

**Problem.** 731 draws the line's entry by its first syllable's stress. Stressed lines land where kept songs do; unstressed lines do not.

**Evidence.** Unstressed first syllables enter before / on / after the beat: 24 / 33 / 44 (main), 23 / 34 / 44 (control); kept 43 / 10 / 47. Stressed: 21 / 40 / 39 against kept 20 / 42 / 38. Lines opening on a weak word ("and", "I", "the", "that") land on the downbeat a third of the time; kept songs put such words there a tenth of the time and before the beat, as pickups, four times as often.

**Fix (proposed).** For an unstressed first syllable, draw the entry from the kept unstressed shares, and let 731's pickup rule move it before the beat when the next syllable is stressed.

**Check.** Unstressed entries within 10 points of 43 / 10 / 47 on songs 48 to 50; stressed entries held.
