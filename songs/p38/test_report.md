---
title: "Stay Tuned — Test report (ZenEng v103)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

## The brief

A new song under ZenEng v103 (version row v137, Window 123, last fix 256), worked on as an idea with the writer before the engine. The idea: a narrator who shows the partisan political class on both sides as one act, biting and sarcastic, no side favoured. Tables read, not refitted: zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json, zeneng_v96_discriminator_tables.json, zeneng_v97_axes_of_character.json, zeneng_v100_bass_and_figures.json, zeneng_v101_band_returns_eras.json, zeneng_v102_song37_checks.json, zeneng_v103_selector.json (hashes in the rerun line). Findings are numbered from 257. The paper is not edited.

## Intake

| # | Question | Answer |
|---|---|---|
| goal |  | New song. 'This one let's work on the idea a little together before we use the engine as the idea is rough and not really embodied yet.' |
| the idea (writer) |  | I'm mad. The Who's 'Won't Get Fooled Again' very much on my mind. Politicians are often (always?) deceitful and nothing ever improves; from the cost of living to rising rates of depression and suicide something isn't rig |
| idea 1: whose mouth |  | Don't know how we stay embodied but I think a narrator is best, highlighting the evils of the partisan political hacks. The song can't seem to favor one side or the other (conservative and liberal): show them both equall |
| idea 2: the narrator |  | A |
| idea 3: the turn |  | C |
| idea 4: title |  | A |
| 1 | class and sound | A |
| 2 | who sings (11.2) | A |
| 3 | tempo, feel, key | A |
| 4 | form (220/228: multiples of four; the last chorus two bars longer) | A |
| 5 (242) | era setting | B |
| 5 (242), changed |  | Change question 5 to A |
| 6 (225) | the song's character on the eight axes (16 ends offered, 'nothing in particular' a choice) | 9 |
| 7 | never say | A |
| 8 (213) | which section opens by saying it twice | A |
| lyric draft 1 |  | lyric_draft1.md |
| lyric draft 1 notes (writer) |  | 1 personal stake under-developed (pre-chorus 2): develop and connect, or cut; 2 verse 1 generic: one concrete, slightly ugly studio detail; 3 bridge stops one step short: cleaner setup, push one degree further; 4 title:  |
| lyric draft 2 |  | lyric_draft2.md |
| lyric draft 2 notes (writer) |  | 1 pre-chorus 1 still the weakest: functional but generic, lacks bite; 2 chorus second half ('the only way the show goes on / is you. So turn it off.') competes with the stronger final ending; the climax has moved to the  |
| lyric draft 3 |  | lyric_draft3.md |
| lyric draft 3 notes (writer, 'Consider these first. Worth changing?') |  | 1 the 'Stay tuned, stay mad / stay tuned, stay scared' chant does a lot of repetitive work; keep arrangement and delivery from feeling static across three appearances; 2 'one man paying for it all' (verse 2) is the softe |
| lyric draft 4 |  | lyric_draft4.md |
| pre-chorus 1 repeated word (writer) |  | Don't like the repeated shouting word in prechorus 1. Can we switch one of them to yell or is the repetition purposeful? |
| lyric draft 5 |  | lyric_draft5.md |
| lyric draft 5: lock or notes |  | A |
| 9 (244, 216) | summit placement | A |
| 10 (208) | bridge register | A |
| 11 (235) | chorus countermelody | B |
| 12 (236) | drum design | B |
| note (before build) |  | the tables artifact now holds zeneng_v103_selector.json ('ZenEng v103, Window 123, fixes 252-256', content and order judges fitted 'for song 38', floor -0.059); the attached spec is v102 (last fix 251). Asked the writer  |
| 13 | which spec governs | A |
| note (conflict found before build) |  | Q6 'reciting' (1.4-2.1 sd) against Q5 era CLASSIC (242): of 314 kept chart windows (v103 training rows), the 20 at 1.4-2.1 on reciting repeat 52% of moves (none at or under 33%) and read 2.41 bits a note; CLASSIC's bands |
| 14 | reciting against CLASSIC | A |

**The song.** *Stay Tuned*: rock (Who-style), 4/4 at ♩ = 132, A major, male high baritone C♯3–A4. A cable-news cameraman tells what he sees; the chorus is the network's own voice; in the last chorus he cuts the cameras and says turn it off. Form: Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 8 · Breakdown 8 · Last Chorus 18 · Outro 8 = 114 bars, 3:27. Every sung line two bars (3–8 syllables; 230). The title is sung 9 times, first at bar 21 of 114 (232; kept 2–10, median 5, first in the opening third in 72%).

## The ports

| Fix | In song 38 |
|---|---|
| 225/226/243 | Each build's targets are one whole kept chart window from the v103 training rows: the verse and pre-chorus from the 20 kept windows at 1.4–2.1 on reciting (Q6, Q14), the chorus and bridge from the 48 kept windows inside at least three of CLASSIC's four bands the rows carry (finding 259). The window index is recorded with the build. Seventeen measures aimed; notes a bar is not in the rows and is read from the chart median (finding 260). The control aims at each pool's medians. |
| 249 | A calibration pass (3 rounds × 30 builds, seed recorded) sets fifteen knobs per pool so a build aimed at its pool's medians reads near them. |
| 251 | Aims added: on the tonic, third and fifth (pitch weights by degree); onsets on beat 3 and on beats 2 and 4 (the rhythm's place weights); turns per move (a reversal weight). The low point's place is not aimed. |
| 227 | Gates: the chorus opening unrelated to the verse's; its median not below the verse's; its lowest note above the verse's. |
| 228 | Verse 2 and pre 2 sung again: verse 1's contour and first and last notes, the rhythm drawn afresh for the new words, a stressed note on a beat moved a step to a chord tone. The last chorus is chorus 1's tune and 18 bars (the writer's 'Turn it off.' as the two-bar extension in place of a hook repeat). |
| 230/231/232 | Two-bar slots; each line's landing drawn from 231's shares (chorus 26/20/18/36 for beat 1, beat 3, beats 2 and 4, off the beat; verse 20/20/18/42); the title's stress fixed on beat 1, held three beats (the chant design). |
| 239/240/246/247/248 | Returns at the source's level, first note kept, change in the last quarter (shared notes on the beat keep their pitch), top note kept or higher; added notes drawn (repeat .28, step .48, leap .24); no steering to the tonic; no sequencing. A copy, return or re-sung line is fitted before the line ahead of it. 181's gate reads the shared events only. |
| 242 | CLASSIC: notes a bar, range, repeats, distinct note lengths and pitch surprise gated on Table DG's middle halves, read as the median over the first 8 bars of Verse 1, Chorus 1 and the Bridge (Q14: A). It replaces the pop pitch band (153/182). |
| 244/216 | The summit A4 on 'tuned' (chorus lines 1 and 5), beat 1 of the chorus window's first bar, over A; six times; gated. |
| 208 | The bridge: opening unrelated, median above the verse, top under the summit (the writer's A). |
| 252–255 | The content and order judges with the file's weights (fitted through song 37, for song 38); checked against song 37's pick first: Verse 1 content 0.586, order 3.059; Chorus 1 −1.027, 5.221, as the file gives. The floor (−0.059) a gate; the shortlist the upper half by combined score; the pick the composite's first on it. |

## The runs

Main: 3000 built, 43 survivors (1.4%), order 6c9159e817fe. Control (243 off): 3000 built, 118 survivors (3.9%), order 2e84eb46c145. The run is 3000 builds, not 500: at 500 the main run left 10 survivors, too few for a shortlist.

| Death | Main | Control |
|---|---|---|
| era CLASSIC bands (242) | 1554 | 1211 |
| returns related, on shared events (181/219/248) | 317 | 333 |
| spectral (Table B) | 278 | 590 |
| monotony run (166/196) | 261 | 185 |
| leaps: tritone or past an octave | 153 | 135 |
| bridge opening unrelated (208) | 74 | 102 |
| return: first or top note not kept (239) | 65 | 68 |
| join: no held end and breath before the line (212) | 57 | 56 |
| join: no held end and breath before the copy (212) | 55 | 34 |
| chorus at or above the verse, floor lifted (227) | 45 | 58 |
| bridge above the verse, under the summit (208) | 44 | 30 |
| memory (Table B) | 19 | 35 |
| align: the words do not fit the returning tune | 10 | 13 |
| cmp (Table B) | 8 | 12 |
| summit placed (the writer's A; 216, 244) | 7 | 7 |
| key word on a chord tone (134) | 5 | 10 |
| realness (Table B) | 4 | 1 |
| the judge's floor (254) | 1 | 0 |
| surprisal (Table B) | 0 | 2 |

Rerun: `PYTHONHASHSEED=0 python3 melody_p38.py 3000 main`; seed 20261491, calibration seed 20261492, code 072042b9fa72, Python 3.13.18, numpy 2.5.3, PYTHONHASHSEED 0. Tables: zeneng_v100_bass_and_figures.json cfe324a5892893a5, zeneng_v101_band_returns_eras.json 0224a91747a584e5, zeneng_v102_song37_checks.json caaa40ecfc747e98, zeneng_v103_selector.json aefba3718173b03d, zeneng_v88_tables.json 561355b1110d1d8e, zeneng_v91_hymn_supplement.json e74e7c30cb04e141, zeneng_v96_discriminator_tables.json 1a2af952c43c3eb7, zeneng_v97_axes_of_character.json 00e65c5b516848aa.

## The pick (255)

| Build | Composite | Content | Order | Combined |
|---|---|---|---|---|
| composite first: fd9ca29c0cc2 | 0.813 | 2.857 | 1.290 | 2.074 |
| shortlist pick: cee0932cdefd | 0.772 | 2.061 | 3.162 | 2.611 |
| judge first: 2aff01296a68 | 0.585 | 6.556 | 4.375 | 5.466 |

The shortlist is 21 of 43 survivors. The composite's first build is 23th of 43 by the judge, outside the shortlist, so 255 changed the pick. The record is built from cee0932cdefd with no hand edits.

## The tests

| Fix | Test | Song 38 | Held? |
|---|---|---|---|
| 225 | builds' median on reciting 1.4–2.1 (verse) | builds 0.27 – 1.153 – 2.072 (5th–median–95th); control 0.495 – 1.425 – 2.325; pick verse 1.48 | no: median 1.15 (finding 264) |
| 225 | pick's place on all eight axes | verse Reach +0.24, Chord-bound +0.67, Sixteenth motion -0.01, Stepwise -0.20, Reciting +1.48, Off-beat +0.83, Uneven lengths +0.45, Late peak +0.81; chorus Reach +1.05, Chord-bound -0.13, Sixteenth motion -0.14, Stepwise -0.18, Reciting +0.34, Off-beat -0.04, Uneven lengths +0.99, Late peak -1.26 | printed |
| 226 | unchosen axes: medians within 1 sd; spread ≥ control's | 15 of 15 medians within 1 sd; spread at or above the control's on 14 of 15; distance builds 0.11 – 0.168 – 0.245, control 0.092 – 0.143 – 0.215 | yes |
| 227 | chorus opening unrelated, median not below, floor above; chorus bar rhythms heard in the verse | gates held on every survivor; pick: chorus median 62 vs verse 52, low 57 vs 49; shared bar rhythms pick 29%, builds 0 – 0.125 – 0.375 (kept median 12%) | yes |
| 228 | verse 2 shares ¼–¾ of verse 1's bar rhythms across builds; last chorus +2 bars; exact bar repetition | builds 0 – 0.125 – 0.375, in range in 30%; pick 0%; +2 bars (the writer's tag); exact bars 42% vs chart 38% | no (finding 262) |
| 229 | bridge surprise vs chorus; off-beat vs verse | bridge 2.974 bits a note vs chorus 3.009; off-beat axis bridge +0.51 vs verse +0.83 | printed |
| 230 | each line's syllables and slot; no 9+ line in 2 bars; sections multiples of 4; sung rate 3.2–6.2 a bar | every line 3–8 syllables, 2 bars; every section a multiple of 4 except the last chorus's 18 (228's extension; finding 268); sung rate pick 4.27, builds 3.733 – 4.267 – 4.667 | yes, with 268 |
| 231 | last stresses off the beat 25–50%, on 1 or 3 35–55%; pickups 40–70% | builds off 0.122 – 0.268 – 0.415, on 1/3 0.439 – 0.585 – 0.732, pickups 0.634 – 0.805 – 0.902; pick 15%, 61%, 68% | off-beat yes; 1/3 and pickups high (finding 263) |
| 232 | title stress on 1 or 3, held ≥ 2× median syllable | beat [1], held 3 beats vs median syllable 0.5 beat; 9 soundings, first bar 21 | yes |
| 239 | each return's kind | pick: fresh 12, pitch 2, twice 1, exact 16, both 2, rhythm 1, sung again 6, designed 1 | printed |
| 240 | returns end on the tonic within 10 points of sources | builds 13% vs sources 14%; pick 0 of 6 vs 0 | yes |
| 243 | window recorded; 40–60% of builds outside the chart middle half on each aimed measure; distance beside the aimed share | windows recorded (pick: verse 294, chorus 307); in 40–60% on 8 of 16 measures (repeat 58%, step 30%, third 62%, fourth_fifth 41%, past_fifth 25%, chord_tones_on_beat 48%, chord_tones_off_beat 47%, gap_eighth 48%, gap_quarter 41%, longest_over_median_note 30%, notes_per_bar 0%, on_tonic 39%, on_third 61%, on_fifth 45%, on_beat3 37%, on_beats_2_4 56%, turns_per_move 39%); builds' distance 0.11 – 0.168 – 0.245; the aimed measures carry 37% of a kept window's distance | partly |
| 245 | notes a bar the lines need | Verse 1 3.75, Pre 1 4.0, Chorus 1 2.88, Verse 2 3.75, Pre 2 4.0, Chorus 2 2.88, Bridge 3.38, Last Chorus 2.72 — none at 4.25, so 218's eighth grid stands | yes |
| 246 | added notes repeat 20–40%; run deaths under 1 in 10 | 29% repeat ({'added_repeat': 853, 'added_step': 1385, 'added_leap': 732}); run deaths 8.7% | yes |
| 247 | join deaths under 1 in 10 | 3.7% | yes |
| 248 | no build dies at 181 where its construction was used | 317 of 3000 died there | no (finding 261) |
| 249 | calibration recorded; chord-tone medians within 3 points of targets' means | seed 20261492; v:chord_tones_on_beat reading 0.571 vs target 0.718; v:chord_tones_off_beat reading 0.571 vs target 0.724; c:chord_tones_on_beat reading 0.692 vs target 0.665; c:chord_tones_off_beat reading 0.636 vs target 0.674 | chorus on the beat yes; verse no (finding 264) |
| 250 | pick's outside count beside 16 (8–26); builds' 5th, median, 95th | pick 10.5; builds 11.5 – 15.5 – 19 | yes (above 8) |
| 251 | each aim followed (r ≥ 0.3) | v:on_tonic 0.641, c:on_tonic 0.721, v:on_third 0.765, c:on_third 0.664, v:on_fifth 0.787, c:on_fifth 0.705, v:on_beat3 0.229, c:on_beat3 0.19, v:on_beats_2_4 0.407, c:on_beats_2_4 0.514, v:turns_per_move 0.169, c:turns_per_move 0.123, v:repeat 0.374, c:repeat 0.7, v:step 0.686, c:step 0.704, v:chord_tones_on_beat 0.377, c:chord_tones_on_beat 0.507, v:gap_eighth 0.368, c:gap_eighth 0.374 | tonic, third, fifth, beats 2 and 4, repeat, step, chord tones, eighth gaps yes; beat 3 and turns no (finding 265) |
| 252 | pick's score; builds 5th/median/95th beside kept; five give-away measures | pick content 2.06; builds -0.945 – 1.611 – 5.023; kept 5th -1.084, median 4.565, 95th 15.59; give-aways: distinct_pitches (-0.825), on_offbeat_eighth (-0.776), gap_eighth (-0.485), gap_sixteenth (-0.483), gap_quarter (-0.382); kept rows above this song's builds in 77% of pairs (the rows are the judge's training data, so this flatters it) | printed |
| 253 | four order measures for verse and chorus beside kept middle halves; share called shuffled | verse parallel 0.273, pitch_parallel 0.142, smooth_barline -0.962, thin_48 3.667; chorus parallel 0.241, pitch_parallel -0.1, smooth_barline 1.495, thin_48 1.167; builds called shuffled 0.3% | printed; the chorus's smooth bar line +1.50 is outside (the chant's leap to A4 sits inside the bar, by design) |
| 254 | no survivor under the floor; deaths counted; over half named | 1 death at the floor (8 builds would have failed it); builds' combined 0.797 – 2.211 – 4.073, kept median 3.114 | yes |
| 255 | three builds with all three scores; record from the shortlist pick | above | yes |
| 256 | none (a record) | nothing in 256 used to rank | — |
| 242 | the era set and its bands | CLASSIC; pick notes_per_bar 3.375, range 12.0, repeat 0.182, distinct_durations 5.0, pitch_bits 2.971; died at the gate 1554 of 3000 (52%) | yes, at a cost (finding 258) |
| 233 | root on beat 1 of every bar with a chord; root share 43–73%; a cell per section; 4 kick hits in 5 carry a bass note | beat 1 the root 100% of bass bars (the bass waits for the verse: intro bars 5–8 have no bass, 96% of chord bars); root share 65%; kicks with bass 98% | yes |
| 236 | Table DD's readings | snare on 2 and 4 in 84% of bars with drums (the breakdown's first four bars and the fill bars without); kick on 1 in 100%; 3.12 kicks a bar; the commonest kick-and-snare bar covers 52%, three cover 81%; 11 fills in 101 bars; drums enter bar 5; four on the floor named (Q12) | yes |
| 237 | one rhythm a section; 3–4 notes in MIDI 51–71; ½–9/10 of strikes with the bass | held, pad or quarter stabs by section; MIDI 57–68; 2.97 strikes a bar; with the bass 100% | no (finding 267) |
| 238 | parts by section; intro ≤ half the fullest; nothing before the last chorus fuller than it; verse not fuller than its chorus | Intro 4, Verse 1 5, Pre 1 6, Chorus 1 7, Verse 2 6, Pre 2 7, Chorus 2 7, Bridge 6, Solo 6, Breakdown 7, Last Chorus 8, Outro 4 | yes |
| 235 | intro tune unrelated to every sung line; fills 2–3 beats, 4–6 notes, start within a beat, end on a chord tone, no echo; countermelody under half unison/octave | intro tune (6, 12, 18, 30) / steps (0, -3, -4, -3), unrelated to all 41 sung lines; fills after Chorus 1:7 (gap 3 beats): 6 notes, 2 beats, from 0.75 beats after; after Verse 2:3 (gap 4 beats): 6 notes, 2 beats, from 0.5 beats after; after Bridge:2 (gap 3 beats): 4 notes, 2 beats, from 0.5 beats after; {'gap left open (30%)': 2, 'no fill fits': 13, 'filled': 3}; countermelody 3 of 16 struck-together notes at unison or octave (19%) | yes; few gaps can take a fill (finding 266) |

## The demo

Stems: the lead vocal +5.9 dB over the band (rule ≥ +3). Energy arc (band only): Intro 0.60; Verse 1 0.78; Pre 1 0.80; Chorus 1 0.87; Verse 2 0.79; Pre 2 0.87; Chorus 2 0.88; Bridge 0.64; Solo 0.89; Breakdown 0.88; Last Chorus 0.92; Outro 0.53. Each chorus reads above its verse; the last chorus is the top; the bridge and the breakdown's opening pull back by design.

## The quotable line (10.20)

Slots for the blind pick: remembered 'Stay tuned, stay mad,', middle 'stay tuned, stay scared,' (top quartile under both), annotated 'they toast the ratings, glass to glass;'. The writer's pick: pending.

## Findings

**257. An axis end the era cannot hold.** *Problem:* the writer chose reciting (225) and CLASSIC (242); no kept window does both. *Evidence:* of 314 kept chart windows, the 20 at 1.4–2.1 on reciting repeat 52% of moves (none at or under 33%) and read 2.41 bits a note; CLASSIC's bands are 16–33% and 2.67–3.19. The writer settled it at Q14 (recite in the verses only). *Fix:* when a chosen axis end and the era's bands leave no kept window between them, the intake says so at the character question and offers the split by section. *Check:* the conflict is printed at intake with the count of kept windows that meet both.
**258. The era gate kills half the run.** *Problem:* 242 sets five bands at the era's middle halves; as gates they kill most builds. *Evidence:* 1554 of 3000 main builds (52%) died there; survival fell to 1.4% (song 37: 31%); the run went to 3000 builds to leave 43 survivors. Only 1 of 314 kept windows sits inside all four of the bands the rows carry; a middle half is passed by half of kept songs by definition. *Fix:* read the era's middle halves as targets (243's draw) and gate at the era's 10th–90th. *Check:* under an era, deaths at the era gate under one build in five; the pick inside the middle halves on at least three of five.
**259. 243's draw and the era do not talk.** *Problem:* targets drawn from any kept window pull builds toward the modern surface that CLASSIC's gate then kills. *Evidence:* the chorus and bridge pool was cut here to the 48 kept windows inside at least three of the four era bands the rows carry (a choice, recorded). A 300-build trial before and after the cut went from 7 to 13 passing the gates, but the chant's pickup design changed in the same step, so the cut's own effect was not measured. *Fix:* under an era, draw the target window from that era's kept windows (the rows need a year). *Check:* the drawn windows' era is printed; deaths at the era gate fall.
**260. Two aimed measures are missing from the rows.** *Problem:* 243 draws targets from a whole kept window, but the v103 training rows lack notes a bar (aimed since 224) and the onsets on the downbeat (251). *Evidence:* the rows carry 50 measures; notes a bar was read from the chart median for every build. *Fix:* add notes_per_bar and on_downbeat to the rows. *Check:* every aimed measure drawn from the window.
**261. 248's test fails: returns die at 181 where the construction was used.** *Problem:* 239's change in the last quarter and the reciting verse make built returns read unrelated on the shared events. *Evidence:* 317 of 3000 builds died at 181/219/248 (control 333); the reading is r < 0.6 on the pitch series of the shared events, and a reciting line whose shared notes are one pitch reads r = 0 against a moving source. *Fix:* 181 on shared events: related when the first three-quarters of the shared events keep their pitches, or both series are near-constant; the late change keeps steps. *Check:* no build dies at 181 where its return was built by 239.
**262. Verse 2 sung again shares too little rhythm with verse 1.** *Problem:* 228 asks for a quarter to three-quarters of verse 1's bar rhythms; refitting each line from its own syllables gives far fewer. *Evidence:* builds 0%–12.5%–37.5% (5th–median–95th); in range in 30%; the pick 0%. *Fix:* draw verse 2's line rhythm with verse 1's onsets as a prior (the rhythm walk tilted toward the source's places, the kept 40% at the median). *Check:* across builds the median share inside 25–75%.
**263. Too many pickups, too many landings on 1 and 3.** *Problem:* 231 asks for pickups on 40–70% of lines and last stresses on 1 or 3 in 35–55%. *Evidence:* builds 80.5% pickups (63–90%) and 58.5% on 1 or 3; the off-beat share is in range (27%). The first syllable's weight before the bar (1.0 against 0.35 on it) and the two-bar lines with holds push both. *Fix:* calibrate the pickup weight on the song (249) to 55%, and read 231's landing on the drawn target, not the walk's result. *Check:* both inside their ranges across builds.
**264. A reciting verse meets the run clause.** *Problem:* the verse aimed at kept reciting windows reads less reciting than its targets. *Evidence:* builds' median 1.15 on reciting (test: 1.4–2.1); the control, aimed at the reciting pool's medians, 1.43; verse chord tones on the beat read 0.57 against targets of 0.72 (249: within 3 points). The walk forbids a fourth repeat and 166/196 gates runs over three, while kept reciting windows repeat on 52% of moves. *Fix:* when reciting is chosen, allow runs of four in that section and recalibrate the chord-tone knob on repeated notes. *Check:* builds' median on reciting inside 1.4–2.1; chord tones within 3 points.
**265. Two of 251's aims are not followed.** *Problem:* turns per move and onsets on beat 3 do not track their targets. *Evidence:* target–reading correlation: turns 0.17 (verse) and 0.12 (chorus); beat 3 0.23 and 0.19. The tonic, third and fifth (0.64–0.79), beats 2 and 4 (0.41, 0.51), repeats, steps, chord tones and eighth gaps are followed. *Fix:* drop turns as an aim (the walk's direction is already set by DESC and 197) or carry direction memory; let 231's landing draw take beat 3. *Check:* r ≥ 0.3 on every aim kept.
**266. Few gaps can take a fill.** *Problem:* 235's fill (start 0.47–0.96 beats after the voice, 1.85–2.58 beats long, ending before the voice) needs about 2.75 beats; two-bar lines with held ends leave 2. *Evidence:* 18 gaps of two beats or more; 13 had no room; 3 filled (70% intended). *Fix:* the 70% counted on gaps of 2.75 beats or more, or a one-and-a-half-beat fill allowed in a two-beat gap. *Check:* the report prints fills against the eligible gaps.
**267. The chordal part always falls with an eighth-note bass.** *Problem:* 237's test caps strikes with a bass note at nine in ten. *Evidence:* the bass cell is eighths, so every organ strike (on the beat or a held chord) falls with a bass note: 100%. *Fix:* read 237's share against bass notes on the beat, or exempt an eighth-note bass cell. *Check:* stated with the bass cell beside it.
**268. 228's extension against 230's multiple of four.** *Problem:* 230 says every section's slots sum to a multiple of four; 228 makes the last chorus two bars longer by default. *Evidence:* the last chorus is 18 bars. *Fix:* 230 names 228's extension as the exception. *Check:* the lyric check prints the extension as designed.
