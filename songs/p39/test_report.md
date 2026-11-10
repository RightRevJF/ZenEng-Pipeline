---
title: "Fixed by Fall — Test report (ZenEng v103)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

## The brief

Song 39 under ZenEng v103 (version row v137, last fix 256), written after song 38 turned into a song about the media: the writer wanted the political class shown as reckless profiteers, both sides. The idea was worked out with the writer before the engine. Tables read, not refitted (hashes in the rerun line). Findings are numbered from 269 (song 38's ran 257–268). The paper is not edited.

## Intake

| # | Question | Answer |
|---|---|---|
| goal |  | C (after song 38): start a new song from the idea up; keep Stay Tuned as the media song it became |
| idea 1: whose eyes |  | Is there any way we can choose an omniscient narrator? I know it's harder to ground things physically but it's also easier to really bite. |
| idea 2: how the omniscient voice stays grounded |  | A |
| idea 3: what the chorus does |  | B |
| idea 4: the turn |  | B |
| idea 5: title |  | B |
| 1 | class and sound | A |
| 2 | who sings (11.2) | C |
| 3 | tempo, feel, key | A |
| 4 | form | A |
| 5 (242) | era setting | A |
| 6 (225) | character | I'll take your recommendation |
| 7 | never say | A |
| 8 (213) | which section opens by saying it twice | A |
| lyric draft 1 |  | lyric_draft1.md |
| lyric draft 1 notes (writer) |  | B. 1 some lines explain rather than show (hearing room, pound the desk, call it war); 2 the rusting bridge vs ribbon is familiar; 3 temperature: the unpaid guard is a moral note against the cold transactional details; 4  |
| lyric draft 2 |  | lyric_draft2.md |
| lyric draft 2 notes (writer) |  | 1 the chorus hasn't grown; by the second appearance it feels flat: one small internal variation or a colder delivery; 2 bridge not pushed as hard: 'one lake, two docks, one lobby firm' good, could be more specific or str |
| lyric draft 3 |  | lyric_draft3.md |
| lyric draft 3: lock or notes |  | A |
| 9 (244, 216) | summit placement | A |
| 10 (208) | bridge register | A |
| 11 (235) | chorus countermelody | A |
| 12 (236) | drum design | B |
| build |  |  |
| blind pick (10.20), offered |  | B |

**The song.** *Fixed by Fall*: rock with a swagger, 4/4 at ♩ = 108, E major; a shuffle (eighths swung) in the verses, bridge, solo, intro and outro, a straight rally march in the choruses (Q12); one gritty baritone A2–E4, double-tracked as two candidates in the last chorus (Q2). An all-seeing narrator cuts between rooms where both sides take the same money; the chorus is their campaign jingle sung back; the bridge follows them out of office; the last chorus ends in unison. Form: Intro 4 · Verse 16 · Chorus 8 · Verse 16 · Chorus 8 · Bridge 8 · Solo 8 · Last Chorus 18 · Outro 4 = 90 bars, 3:20. Every line two bars (4–8 syllables; 230). The title is sung 4 times, first at bar 27 of 90 (232). No era (Q5).

## The ports

| Fix | In song 39 |
|---|---|
| 225/226/243 | Targets are one whole kept window: the verse from the 10 kept windows at 1.4–2.1 on off-beat, the chorus from the 22 at 1.4–2.1 on chord-bound (Q6; no kept window does both, so split by section), the bridge from all 314. Seventeen measures aimed; notes a bar from the chart median (260). The control aims at each pool's medians. |
| 249 | A calibration pass (3 rounds × 30 builds) per pool: verse on Verse 1, chorus on Chorus 1, bridge on the Bridge. |
| 227/228/230–232/239/240/246–248/251 | As in song 38 (verse 2 sung again; returns at the source's level, change late, added notes drawn; copies fitted first). Verse plans for eight lines: lines 1–4 from the plan list, lines 5–8 a varied return of 1–4 or fresh. |
| 244/216 | The summit E4 on 'Vote', beat 1 of each chorus's first bar, over E; the second line said twice a whole step down (D4 over D); the last chorus's unison 'Vote for us' returns it; four summits, gated. |
| 208 | The bridge: opening unrelated, median above the verse, top under the summit. |
| 242 | Not set (Q5); the pop pitch band (153/182) applies. |
| 252–255 | The judges with the file's weights, the floor a gate, the shortlist. |
| Designed | 'Fixed by fall.' (the tag) G♯3–F♯3–E3. The last chorus's voices from the lyric's marks. The swing is the demo's (271). |

## The runs

Main: 500 built, 58 survivors (11.6%), order 07c5a8ad998f. Control (243 off): 500 built, 113 survivors (22.6%), order 05fbf6379223.

| Death | Main | Control |
|---|---|---|
| returns related, on shared events (181/219/248) | 86 | 104 |
| monotony run (166/196) | 61 | 39 |
| bridge above the verse, under the summit (208) | 55 | 57 |
| leaps: tritone or past an octave | 42 | 23 |
| join: no held end and breath before the copy (212) | 41 | 30 |
| surprisal (Table B) | 27 | 13 |
| chorus at or above the verse, floor lifted (227) | 25 | 7 |
| return: first or top note not kept (239) | 21 | 18 |
| bridge opening unrelated (208) | 16 | 11 |
| spectral (Table B) | 15 | 6 |
| cmp (Table B) | 13 | 21 |
| realness (Table B) | 12 | 13 |
| chorus opening another tune (227) | 12 | 19 |
| summit placed (the writer's A; 216, 244) | 8 | 16 |
| memory (Table B) | 3 | 4 |
| align: the words do not fit the returning tune | 2 | 0 |
| key word on a chord tone (134) | 2 | 2 |
| walk: no note | 1 | 4 |

Rerun: `PYTHONHASHSEED=0 python3 melody_p39.py 500 main`; seed 20261501, calibration seed 20261502, code 8397ca3ba76b, Python 3.13.18, numpy 2.5.3, PYTHONHASHSEED 0. Tables: zeneng_v100_bass_and_figures.json cfe324a5892893a5, zeneng_v101_band_returns_eras.json 0224a91747a584e5, zeneng_v102_song37_checks.json caaa40ecfc747e98, zeneng_v103_selector.json aefba3718173b03d, zeneng_v88_tables.json 561355b1110d1d8e, zeneng_v91_hymn_supplement.json e74e7c30cb04e141, zeneng_v96_discriminator_tables.json 1a2af952c43c3eb7, zeneng_v97_axes_of_character.json 00e65c5b516848aa.

## The pick (255)

| Build | Composite | Content | Order | Combined |
|---|---|---|---|---|
| composite first: 03b97e94f12c | 0.795 | -0.593 | 2.503 | 0.955 |
| shortlist pick: f69bed50793e | 0.787 | 1.981 | 2.986 | 2.484 |
| judge first: e68750259d59 | 0.586 | 3.367 | 4.854 | 4.110 |

The shortlist is 29 of 58 survivors. The composite's first build is 54th of 58 by the judge, outside the shortlist, so 255 changed the pick. The record is built from f69bed50793e with no hand edits.

## The tests

| Fix | Test | Song 39 | Held? |
|---|---|---|---|
| 225 | builds' median on the chosen axes 1.4–2.1 | verse off-beat: builds 0.978 – 1.599 – 2.05, control 1.203 – 1.767 – 2.177, pick 1.38; chorus chord-bound: builds -1.062 – -0.189 – 0.876, control -0.944 – -0.086 – 0.911, pick 0.49 | verse yes; chorus no (269) |
| 225 | pick's place on all eight axes | verse Reach +0.60, Chord-bound -0.01, Sixteenth motion +0.06, Stepwise +1.16, Reciting -1.20, Off-beat +1.38, Uneven lengths +0.24, Late peak -0.14; chorus Reach +0.79, Chord-bound +0.49, Sixteenth motion -0.73, Stepwise -0.30, Reciting +0.57, Off-beat -0.83, Uneven lengths +0.19, Late peak -0.34 | printed |
| 226 | unchosen axes within 1 sd; spread ≥ control's | 14 of 14 within 1 sd; spread at or above the control's on 14 of 14; distance builds 0.118 – 0.184 – 0.296, control 0.109 – 0.158 – 0.225 | printed |
| 227 | chorus opening unrelated, median not below, floor above; shared bar rhythms | pick: chorus median 57 vs verse 52, low 49 vs 45; shared bar rhythms pick 25%, builds 0 – 0.125 – 0.429 (kept 12%) | yes |
| 228 | verse 2 shares ¼–¾ of verse 1's bar rhythms; last chorus +2 bars | builds 0.041 – 0.235 – 0.5, in range 47%; pick 0%; +2 (the tag) | no (273) |
| 229 | bridge surprise vs chorus; off-beat vs verse | bridge 3.144 bits vs chorus 2.769; off-beat bridge +0.35 vs verse +1.38 | printed |
| 230 | slots; sections multiples of 4; sung rate | every line 4–8 syllables in 2 bars; the last chorus 18 (268); sung rate pick 4.57, builds 4.267 – 4.667 – 5.333 | yes, with 268 |
| 231 | off-beat 25–50%, on 1 or 3 35–55%, pickups 40–70% | builds 0.135 – 0.351 – 0.595, 0.216 – 0.405 – 0.676, 0.397 – 0.541 – 0.649 | yes (273) |
| 232 | title stress on 1 or 3, held ≥ 2× median | 'fixed' on beat [1, 3], held 1 beat vs median 0.5; 4 soundings, first bar 27 | yes |
| 239 | each return's kind | pick: fresh 8, exact 13, rhythm 2, both 2, twice 1, sung again 8, pitch 2, designed 1 | printed |
| 240 | tonic endings within 10 points | builds 23% vs sources 24%; pick 5 of 12 vs 5 | yes |
| 243 | 40–60% outside the chart middle half per aimed measure | windows recorded (pick: verse 137, chorus 105, bridge 230); in range on 4 of 16; distance 0.118 – 0.184 – 0.296; aimed share 37% | partly |
| 245 | notes a bar the lines need | Verse 1 3.94, Chorus 1 3.5, Verse 2 3.94, Chorus 2 3.5, Bridge 4.0, Last Chorus 3.22 | yes (none dense) |
| 246 | added notes repeat 20–40%; run deaths under 1 in 10 | {'added_leap': 1, 'added_repeat': 1} (too few to read); run deaths 12.2% | no (270) |
| 247 | join deaths under 1 in 10 | 8.2% | yes |
| 248 | no deaths at 181 where built | 86 of 500 | no (273, 261) |
| 249 | calibration; chord tones within 3 points | v:chord_tones_on_beat 0.643 vs 0.693; v:chord_tones_off_beat 0.429 vs 0.429; c:chord_tones_on_beat 0.706 vs 0.888; c:chord_tones_off_beat 0.636 vs 0.801 | printed |
| 250 | outside count beside 16 (8–26) | pick 10; builds 10.85 – 14.5 – 18.5 | yes |
| 251 | aims followed (r ≥ 0.3) | v:on_tonic 0.814, c:on_tonic 0.717, v:on_third 0.739, c:on_third 0.668, v:on_fifth 0.668, c:on_fifth 0.725, v:on_beat3 0.034, c:on_beat3 0.372, v:on_beats_2_4 0.616, c:on_beats_2_4 0.44, v:turns_per_move 0.559, c:turns_per_move 0.33, v:repeat 0.936, c:repeat 0.69, v:step 0.904, c:step 0.749, v:chord_tones_on_beat 0.487, c:chord_tones_on_beat 0.195, v:gap_eighth 0.567, c:gap_eighth 0.472 | mostly; verse beat 3 and chorus chord tones no (269, 273) |
| 252 | judge scores, give-aways | pick content 1.98; builds -1.421 – 1.32 – 4.829; kept median 4.565; give-aways: distinct_pitches (-1.777), on_offbeat_eighth (-1.316), gap_eighth (-0.734), gap_quarter (-0.727), gap_sixteenth (-0.483); kept rows above builds in 81% of pairs | printed |
| 253 | order measures; share called shuffled | verse parallel 0.345, pitch_parallel 0.74, smooth_barline -0.387, thin_48 0.667; chorus parallel 0.164, pitch_parallel -0.161, smooth_barline -0.472, thin_48 1.167; shuffled 0.2% | printed |
| 254 | floor | 0 deaths (0 would fail); builds 0.777 – 2.204 – 4.052 | yes |
| 255 | three builds; record from the shortlist pick | above | yes |
| 242 | era | not set (Q5) | — |
| 233 | root on beat 1; root share 43–73%; kicks with bass | beat 1 the root 100%; root share 49%; kicks with bass 97% | yes |
| 236 | Table DD readings | snare 2 and 4 90%; kick on 1 100%; 2.71 kicks a bar; top groove 56%, three 96%; 8 fills in 90 bars; the feel change at each chorus named (Q12) | yes |
| 237 | one rhythm a section; MIDI 51–71; ½–9/10 with the bass | MIDI 56–66; 3.65 strikes a bar; with the bass 100% | no (267) |
| 238 | parts by section | Intro 3, Verse 1 5, Chorus 1 5, Verse 2 6, Chorus 2 6, Bridge 5, Solo 4, Last Chorus 6, Outro 5 | yes |
| 235 | intro tune unrelated; fills | intro tune (6, 12, 18, 30) / (0, 2, -2, 2); fills after Verse 2:0 (5.5 beats): 6 notes, 3 beats, from 0.75; after Verse 2:3 (3 beats): 6 notes, 2.25 beats, from 0.5; {'no fill fits': 5, 'gap left open (30%)': 2, 'filled': 2}; no countermelody (Q11) | yes (266) |

## The demo

Stems: the lead vocal +6.0 dB over the band (rule ≥ +3). Energy arc (band only): Intro 0.28; Verse 1 0.41; Chorus 1 0.56; Verse 2 0.53; Chorus 2 0.56; Bridge 0.26; Solo 0.45; Last Chorus 0.59; Outro 0.51. Each chorus reads above its verse; the last chorus is the top; the bridge pulls back by design.

## The quotable line (10.20)

Slots for the blind pick: remembered 'we've got it fixed by fall.', middle 'same shrimp, same band, same donor's hand' (top quartile under both), annotated 'Vote for us, we'll fix it all,'. The writer's pick: A, the annotated slot ('they toast the ratings, glass to glass'). Tally after song 38: Annotated 10, Remembered 8, Middle 7, Refrain 1 (26 songs).

## Findings

**269. A chosen character in a section full of designed notes is not reached.** *Problem:* the writer chose chord-bound for the chorus (225), but the chorus's designed notes (the summit on 'Vote', the line said twice a step down, and the copies of both) leave the walk only half the section to aim. *Evidence:* the builds' chorus median on chord-bound −0.19 (5th–95th −1.06 to 0.88) against the chosen 1.4–2.1; the control −0.09; the chord-tones-on-the-beat aim in the chorus followed at r = 0.20. The verse's off-beat choice, in a section with nothing designed, read 1.60 (in range). *Fix:* when a section's character is chosen, the walk aims the section's whole window, designed notes included (it compensates on the free notes), and the report says how many notes were free. *Check:* the builds' median on a chosen axis inside 1.4–2.1 whatever the design.
**270. 'Said twice' made the runs.** *Problem:* the second chorus line was built as the first a whole step down, with each note re-chosen to a chord tone where it fell on a beat or was held; several notes landed on the same chord tone. *Evidence:* in a 500-build run before a repair step was added, the twice line held 108 of the runs of four in builds the run clause killed, and the chorus's copies in chorus 2 and the last chorus 225 more; with the repair, run deaths fell to 12.2% (246's test: under 10%). *Fix:* say it twice by moving the line bodily (27.44's commonest move) and correct only notes that clash (215), not every strong note to a chord tone. *Check:* run deaths under one build in ten with a twice line in the plan.
**271. A shuffle has no place on the grid or in the tables.** *Problem:* the writer chose a shuffle (eighths swung) for the verses and a straight march for the choruses. The engine writes and reads straight eighths; the rhythm tables, the 231 landings and the judges' measures do not know a shuffle; the swing was added only in the demo. *Evidence:* every reading in this song is on the written straight grid; no kept corpus file marks which songs swing. *Fix:* the intake records swing per section; the class tables are split or flagged by swing; readings on swung sections are taken on the written grid and said so. *Check:* the report states the feel of each section beside its readings.
**272. Evidence for 258 from a song with no era.** *Problem:* none new; a record. *Evidence:* with no era set, 500 builds left 58 survivors (11.6%; control 113, 22.6%), where song 38 with CLASSIC needed 3000 builds for 43. The largest killers were the return gate, the run clause and the bridge register, not a band. *Fix:* as 258. *Check:* as 258.
**273. Song 39 against 261–265.** *Problem:* none new; the earlier findings read in a second song. *Evidence:* 261: 86 of 500 died at 181 where the return was built (control 104), again. 262: verse 2 shared a median 23.5% of verse 1's bar rhythms (47% of builds in range): nearer, still short. 263: pickups 54%, landings on 1 or 3 40.5%, off the beat 35%, all inside 231's ranges, so song 38's excess came from that song (its fixed chant pickups), not from the walk in general; 263's fix stands as a calibration, not a rule. 265: onsets on beat 3 again not followed in the verse (r = 0.03; chorus 0.37); turns followed this time (0.56, 0.33). *Fix:* 261 and 262 as written; 263 narrowed to calibration; 265 keeps beat 3 with 231. *Check:* as each.
