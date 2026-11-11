# Nothing Else on Earth: song 40 under ZenEng v108 (test report)

*A debugging song on the default path · Words and music: Jason Bryant*

Riff-led rock, 4/4, straight eighths, ♩ = 116, D major, mezzo (A3–D5); 110 bars, 3:48. The lyric is Lark's song from 'The Garden That Grew by Itself' (Wild Fruit), locked at draft 3. The paper was not edited. Findings are numbered from 298.

Read first: Module 27.52 (fixes 286–297) and the tables: zeneng_v108_judges.json (cb84379c…; its weights and floor replace the v103 file's), zeneng_v108_spectral_and_registers.json (8d33013c…), zeneng_v106_gate_limits.json (ca3e6a8b…), zeneng_v105_kept_windows.json (3633a24e…), zeneng_v104_line_in_time.json (43325ed4…) and the earlier files.

**The default path.** Era none (Q8), character none (Q9), no designed summit (Q15), bridge register not chosen (Q16), chorus lift not chosen (Q17), no countermelody (Q18); the said-twice section asked as usual and answered as a plain repeat in the chorus (Q11). **No design gate is in force.** Two design choices sit off the default path and are named: the drums (Q19 B, kept at Q20: half-time verses, the full beat from the pre-chorus; an arrangement design under 236, not a melody gate), and the two-bar lines of nine or more syllables (Q21 A: the form and the lyric are the design that 230 allows; 27 lines across the song).

**Ported on song 38's rerun Run B:** 286, 287, 288, 289, 290, 291, 293 (its first half did not apply: no character), 294 (did not apply: no era), 295, 296, 297. Nothing blocked the port; no two fixes conflicted.

**Runs.** 1,000 builds main and 1,000 control (243 off), each made twice; seed 20261511, calibration seed 20261512, PYTHONHASHSEED 0; code 8275c26ef512; Python 3.13.18, numpy 2.5.3. Rerun line: `PYTHONHASHSEED=0 python3 melody_p40.py 1000 main|ctl` (a third argument names the copy: `_r`). Every build is on file, dead or alive (`every` in melody_main.pkl, melody_ctl.pkl and their `_r` copies).

## 1. Survivors and frozen orders

| Run | Survivors | Frozen order | Second run | Reproduced |
|---|---|---|---|---|
| Main (243 on) | 468 of 1,000 (46.8%) | 8922c963f670 | 8922c963f670 | yes |
| Control (243 off) | 570 of 1,000 (57.0%) | 52ad6487743f | 52ad6487743f | yes |

249's pass set the line strengths to contour amplitude 7 (the cap), widening 0.244, fresh-start spread 3.008. Its last round read arch term 0.084, widening 0.398, first note's extra surprise 1.418 bits, against the kept 1.452, 0.326, 1.338: the arch term stays far under the kept figure at the cap (finding 305).

## 2. Deaths per gate

| Gate | Main | Control | Main, would fail | Control, would fail |
|---|---|---|---|---|
| the judge's floor (254; 279) | 164 | 141 | 249 | 198 |
| limits: a hard limit or three soft breaks (276/277, with 286's seven) | 153 | 56 | 153 | 56 |
| bridge opening unrelated (208; 279) | 62 | 72 | 80 | 93 |
| key word on a chord tone (134; 279) | 61 | 34 | 89 | 39 |
| join: no held end and breath before the copy (212) | 58 | 66 | — | — |
| chorus opening another tune (227; 279) | 30 | 57 | 33 | 59 |
| align: the words do not fit the returning tune | 2 | 3 | — | — |
| join: no held end and breath before the line (212) | 1 | 1 | — | — |
| walk: no note | 1 | 0 | — | — |
| survivors | 468 | 570 | | |

Limits broken, every complete build (soft or hard): main realness 219, run_max 160, surprisal 103, chorus_top_minus_verse 64, memory 33, chorus_median_minus_verse 33, cmp 20, spectral 19, max_lengths_8_bars 2, tritone_leap_share 2; control surprisal 79, chorus_top_minus_verse 56, spectral 23, run_max 23, realness 21, cmp 10, chorus_median_minus_verse 6, tritone_leap_share 1, memory 1.

## 3. Fixes 277 and 286: soft breaks and hard limits

Fifteen limits, one count: 276's eight and 286's seven. A build dies on a hard limit or its third soft break.

| Run | Complete builds | 0 soft | 1 | 2 | 3+ | Hard limit broken | Deaths on a third soft break | Pick |
|---|---|---|---|---|---|---|---|---|
| Main (243 on) | 938 | 58.3% | 31.3% | 8.6% | 1.7% | 144 | 9 | soft none, hard none |
| Control (243 off) | 930 | 84.0% | 14.4% | 1.6% | 0.0% | 56 | 0 | soft none, hard none |
| main, the eight only | | 77.5% | 19.0% | 3.0% | 0.5% | | | |
| kept songs, the eight (Table DL) | — | 70.7% | 22.9% | 5.7% | 0.7% | — | — | — |
| calibration pairs, the seven | 515 | 76.7% | 21.4% | 1.9% | 0.0% | 35 | — | — |

Soft breaks by limit: main run_max 150, realness 140, chorus_top_minus_verse 64, surprisal 49, memory 33, chorus_median_minus_verse 31, cmp 20, spectral 14, max_lengths_8_bars 2, tritone_leap_share 2; hard: realness 79, surprisal 54, run_max 10, spectral 5, chorus_median_minus_verse 2. Control soft: chorus_top_minus_verse 56, surprisal 46, run_max 23, spectral 14, cmp 10, realness 7, chorus_median_minus_verse 6, tritone_leap_share 1, memory 1; hard: surprisal 33, realness 14, spectral 9.

Each limit: the builds' median and the pick, beside the soft and hard limits.

| Limit | Direction | Soft | Hard | Main median | Main pick | Control median | Control pick |
|---|---|---|---|---|---|---|---|
| tritone_leap_share | at most | 0.0171 | 0.0383 | 0 | 0.0068 | 0 | 0 |
| past_octave_share | at most | 0.0177 | 0.0417 | 0 | 0 | 0 | 0 |
| run_max | at most (soft: under 10; hard: under 15) | under 10 | under 15 | 7 | 6 | 6 | 5 |
| tritone_from_root_share | at most | 0.0348 | 0.1282 | 0 | 0 | 0 | 0 |
| max_lengths_8_bars | at most | 8 | 9 | 6 | 6 | 6 | 6 |
| chorus_top_minus_verse | at least | -6.05 | -10.83 | 0 | -2 | 0 | 0 |
| chorus_median_minus_verse | at least | -5 | -8.22 | 2 | -1 | 2 | 3 |
| chorus_floor_minus_verse | at least | -5 | -7 | 2 | 0 | 2 | 2 |
| spectral | between | 0.086 · 1.628 | -0.098 · 1.766 | 0.9323 | 0.9554 | 0.9284 | 0.8014 |
| cmp | at least | 0.338 | 0.0915 | 0.5296 | 0.4876 | 0.5286 | 0.5821 |
| memory | at least | 0.2266 | 0.0762 | 0.5319 | 0.4436 | 0.5882 | 0.6618 |
| surprisal | at least | 0.3333 | 0.245 | 0.6127 | 0.9167 | 0.6387 | 0.75 |
| realness | at least | 0.0518 | 0.0119 | 0.1592 | 0.466 | 0.4184 | 0.5689 |
| rhythm band | between | 1.5809 · 2.9273 | 1.3686 · 3.6124 | 2.1586 | 2.2149 | 2.0514 | 2.2761 |
| sequence legs | at most | 1 | 2 | 1 | 1 | 1 | 1 |

**The most note lengths in any eight bars (288).** Main 5th · 25th · 50th · 75th · 95th: 5 · 6 · 6 · 7 · 8 (counts {5: 102, 6: 467, 7: 314, 8: 53, 9: 2}); control 5 · 5 · 6 · 6 · 6; the pick 6; kept: six at the median, four to eight. Under v107 every build of song 38 read 5.

## The lift the registers drew (288), beside the kept figures

Chorus 1 over Verse 1, in semitones (bridge: the bridge's median over the verse's). Kept: Table DL. Builds and survivors: 5th · 25th · 50th · 75th · 95th.

| Reading | Kept 5 · 25 · 50 · 75 · 95 | Main, drawn | Main, builds | Main, survivors | Main pick (drawn → read) | Control, builds | Control pick |
|---|---|---|---|---|---|---|---|
| median | -5 · 0 · 1 · 3.125 · 10.05 | -4.997 · 0.061 · 1.04 · 3.173 · 9.93 | -5 · -1 · 2 · 4 · 9 | -5 · -1 · 1 · 4 · 8.825 | 0.12 → -1 | -4 · 0 · 2 · 4 · 9 | 3 |
| top | -6.05 · -1 · 0 · 3 · 9 | -6.051 · -0.939 · 0.057 · 3.041 · 8.896 | -7 · -2 · 0 · 3 · 5 | -5 · -2 · 0 · 3 · 5 | -0.88 → -2 | -7 · -2 · 0 · 2 · 5 | 0 |
| lowest | -5 · 0 · 2 · 4 · 9.05 | -4.993 · 0.122 · 2.038 · 4.035 · 8.962 | -2 · 0 · 2 · 4.75 · 9 | -2 · 0 · 2 · 4 · 9 | 0.23 → 0 | 0 · 0 · 2 · 5 · 9 | 2 |
| bridge | -2.9 · 0 · 2 · 5 · 7 | -3.51 · -0.079 · 2.047 · 4.97 · 6.893 | -3 · 0 · 2 · 5 · 7 | -3 · 0 · 2 · 4 · 7 | 5.36 → 1 | -2 · 0 · 2 · 4 · 7 | 7 |

The pick, in notes: Chorus 1 top G4 against Verse 1's A4; lowest A3 against A3; median E4 against F4; the bridge reaches C♯5, the song's top. Its registers were drawn at the kept 28th percentile for the chorus (one quantile for its median, top and lowest) and the 79th for the bridge. The read lift follows the drawn lift across builds (r = 0.842 median, 0.937 top). Builds inside the kept middle half: median 40.9%, top 41.2%, lowest 66.8%, bridge 68.3% (288's check asks half or more of the chorus medians).

**The spectral reading beside the lift (286).** The engine's beta_pitch on Verse 1 then Chorus 1's first eight bars, by the build's median lift:

| Median lift | Kept songs | Main (builds, median) | Control |
|---|---|---|---|
| within 2 | 0.83 | 0.795 (467) | 0.809 (540) |
| 3 to 5 | 1.08 | 0.959 (303) | 0.998 (250) |
| 6 or more | 1.23 | 1.239 (168) | 1.311 (140) |

The reading over builds, 1st · 5th · 50th · 95th · 99th: main 0.133 · 0.386 · 0.932 · 1.483 · 1.658, control 0.186 · 0.414 · 0.928 · 1.496 · 1.74 (limits: soft 0.086–1.628, hard −0.098 to 1.766); the pick 0.955. It rises with the lift as the paper says (r = 0.271 main, 0.378 control). **Deaths at the spectral reading:** main 14 soft breaks and 5 hard; it decided 5 deaths (it took part in 10); control 14 soft, 9 hard, deciding 9. Under v107 it was song 38's largest killer.

## 4. Fixes 275, 280 and 286: the kept pass rate of every gate in the search

| Gate | Kept pass rate | Source |
|---|---|---|
| limits: a hard limit or three soft breaks, the eight of 276 (276/277) | 92.0% | Table DL (v106 file) |
| the seven of 286 as limits, alone (a hard limit or three soft breaks among them) | 93.2% | the 515 POP909 calibration pairs (the spectral limits the v108 file's) |
| returns related (267) | — | not printed by the paper |
| chorus opening unrelated (227) | 94.9% | Table DL |
| bridge opening unrelated (208) | 95.2% | Table DL |
| pushed notes at most 42% (159) | 99.4% | Table DL |
| density 1.1 to 4.9 notes a second (159) | 95.3% | Table DL |
| key word on a chord tone (134) | 90.0% | Window 94 ('about nine in ten') |
| the judge's floor (254, 291) | 95.0% | kept held-out 5th percentile (v108 judges file) |
| joins: a held end and a breath (212) | — | unread by the paper (a lyric-placement rule) |
| the voice's range (intake) | — | the writer's voice row |

The seven of 286, each alone on the calibration pairs (soft limit · hard limit): spectral 95.7% · 99.2%; cmp 95.0% · 98.8%; memory 95.0% · 98.8%; surprisal 97.9% · 98.8%; realness 95.0% · 98.8%; rhythm band 89.9% · 97.7%; sequence legs 98.6% · 100.0%. Corpus: POP909 (Wang et al. 2020), the 515 major-key songs with a labelled verse and chorus (Dai et al. 2020 labels): the engine's calibration pairs for Table B, read on the whole first verse and chorus runs as the calibration was. With 286's limits the seven pass 93.2% of the pairs (no hard break and fewer than three soft); 35 of 515 pairs break a hard limit (finding 301). The spectral reading on the pairs, 1st · 5th · 50th · 95th · 99th: 0.1378 · 0.4777 · 1.0583 · 1.5671 · 1.7205.

## 5. The line readings of Table DJ

Builds' 5th · median · 95th; the pick; the kept middle half (25th · median · 75th).

| Reading | Kept | Main | Main pick | Main outside kept middle half | Control |
|---|---|---|---|---|---|
| arch or falling | 0.5 · 0.667 · 0.783 | 0.383 · 0.617 · 0.809 | 0.894 | 30.0% | 0.393 · 0.617 · 0.83 |
| valley | 0.033 · 0.087 · 0.167 | 0.021 · 0.128 · 0.319 | 0.043 | 45.1% | 0.021 · 0.128 · 0.319 |
| arch positive | 0.5 · 0.636 · 0.767 | 0.298 · 0.511 · 0.723 | 0.426 | 48.2% | 0.319 · 0.532 · 0.745 |
| arch term | 0 · 1.452 · 3.341 | -2.761 · 0.161 · 3.616 | -0.704 | 49.1% | -2.684 · 0.345 · 3.412 |
| falling term | 0.191 · 2.848 · 5.404 | -1.363 · 3.481 · 8.951 | 9.12 | 40.0% | -1.72 · 4.239 · 8.83 |
| peak first third | 0.421 · 0.6 · 0.737 | 0.404 · 0.638 · 0.851 | 0.66 | 29.4% | 0.383 · 0.617 · 0.83 |
| end minus mean | -2.267 · -1.2 · -0.315 | -2.778 · -1 · 0.667 | -3 | 36.6% | -2.782 · -1.222 · 0.913 |
| last over mean | 1.182 · 1.478 · 1.714 | 2 · 2.286 · 2.857 | 2.545 | 99.9% | 1.929 · 2.222 · 2.571 |
| widening | -0.105 · 0.326 · 1.083 | -0.824 · 0.188 · 1.138 | 0.376 | 36.7% | -0.784 · 0.184 · 1.048 |
| first note extra bits | 0.829 · 1.338 · 1.899 | 0.337 · 1.162 · 2.36 | 2.005 | 42.0% | 0.475 · 1.278 · 2.34 |
| starts on downbeat | 0.074 · 0.179 · 0.368 | 0.085 · 0.213 · 0.404 | 0.404 | 14.0% | 0.064 · 0.213 · 0.404 |
| starts after downbeat | 0.333 · 0.525 · 0.783 | 0.426 · 0.638 · 0.83 | 0.574 | 15.5% | 0.426 · 0.638 · 0.83 |
| starts as pickup | 0.034 · 0.143 · 0.357 | 0.021 · 0.128 · 0.298 | 0.021 | 11.9% | 0.021 · 0.128 · 0.298 |
| ends on downbeat | 0.111 · 0.273 · 0.429 | 0.085 · 0.298 · 0.468 | 0.447 | 16.6% | 0.085 · 0.298 · 0.468 |

Contour kinds (share of lines): kept falling 23.8%, arch 21.5%, valley 11.5%, level then falling 11.1%, rising 9.3%; main falling 26.7%, arch 15.1%, valley 14.1%, rising 11.7%, falling then level 9.8%; the pick falling 68.1%, falling then level 10.6%, arch 8.5%, level then rising 4.3%.

The move between lines a fourth or more: main 0.196 · 0.391 · 0.63 (pick 0.565); kept 34% of joins.

**The landing (289): each line's last note.**

| Run | On beat 1 | On beat 3 | On beats 2 and 4 | Off the beat | Last stress on 1 or 3 |
|---|---|---|---|---|---|
| Main (243 on) | 0.064 · 0.255 · 0.447 | 0.021 · 0.085 · 0.298 | 0.043 · 0.149 · 0.298 | 0.255 · 0.447 · 0.66 | 0.298 · 0.426 · 0.596 |
| Control (243 off) | 0.085 · 0.298 · 0.468 | 0.021 · 0.106 · 0.298 | 0.043 · 0.149 · 0.298 | 0.255 · 0.426 · 0.617 | 0.298 · 0.426 · 0.596 |
| main pick | 0.447 | 0.043 | 0.17 | 0.34 | 0.511 |
| 289's shares | 26% | 10% | 16% | 49% | 35–55% asked |

Section endings, the pick (scale degree of the last sung note): Verse 1 4, Pre 1 6, Chorus 1 5, Verse 2 4, Pre 2 6, Chorus 2 5, Bridge 2, Last Chorus 1. Across main's builds: Verse 1 5 222, 2 186, 3 152, 6 149; Chorus 1 1 342, 5 299, 3 297; Bridge 2 177, 3 149, 5 146, 1 128; Last Chorus 1 839, 5 48, 3 25, 6 15.

## 6. Fix 255: the three builds, and the pick under the old fit term (296)

| Run | Build | Composite | Composite, old fit | Content | Order | Combined | Lift (median, top) | Spectral |
|---|---|---|---|---|---|---|---|---|
| Main (243 on) | composite first: 2fe2be999be7 | 0.866 | 0.828 | 0.676 | 2.181 | 1.429 | -1, -2 | 0.955 |
| Main (243 on) | shortlist pick: 2fe2be999be7 | 0.866 | 0.828 | 0.676 | 2.181 | 1.429 | -1, -2 | 0.955 |
| Main (243 on) | judge first: d1f8d0b0beec | 0.618 | 0.593 | 4.167 | 2.394 | 3.281 | -2, -5 | 1.013 |
| Main (243 on) | pick under the old fit term (296): 353742341ffc | 0.842 | 0.854 | -0.206 | 1.472 | 0.633 | 4.5, 2 | 1.253 |
| Control (243 off) | composite first: d6fa18f1d555 | 0.896 | 0.878 | 0.053 | 0.757 | 0.405 | 3, 0 | 0.801 |
| Control (243 off) | shortlist pick: d6fa18f1d555 | 0.896 | 0.878 | 0.053 | 0.757 | 0.405 | 3, 0 | 0.801 |
| Control (243 off) | judge first: 9c0a74aa44a6 | 0.624 | 0.617 | 3.946 | 2.312 | 3.129 | 2, -2 | 0.912 |
| Control (243 off) | pick under the old fit term (296): d6fa18f1d555 | 0.896 | 0.878 | 0.053 | 0.757 | 0.405 | 3, 0 | 0.801 |
- Main (243 on): the composite's first is 36th of 468 by the judge, inside the upper half (234), so the shortlist did not change the pick. Under the old fit term the composite's first is 353742341ffc, the pick ranks 8th, and the pick **differs**. Builds: content -4.352 · -1.295 · 1.744, order -0.382 · 1.002 · 2.4, combined -1.735 · -0.13 · 1.422; 0.1% at or above the kept held-out median, 4.4% above the kept 25th, 26.5% under the floor.
- Control (243 off): the composite's first is 230th of 570 by the judge, inside the upper half (285), so the shortlist did not change the pick. Under the old fit term the composite's first is f90dbc2aba38, the pick ranks 2th, and the pick is the same. Builds: content -3.891 · -1.227 · 1.584, order -0.284 · 1.115 · 2.501, combined -1.507 · -0.046 · 1.442; 0.2% at or above the kept held-out median, 4.0% above the kept 25th, 21.3% under the floor.

**291: the refitted judges.** Kept held-out percentiles (5 · 25 · 50 · 75 · 95): content -2.015 · 1.332 · 4.16 · 7.083 · 11.791, order -1.528 · 0.049 · 1.579 · 2.814 · 5.024, combined -0.739 · 1.525 · 2.95 · 4.47 · 6.703; floor -0.739. The file carries the kept percentiles and not the held-out rows, so an AUC is not read here; the separation printed is the builds against the kept percentiles above. The content judge's heaviest give-aways (weight × z, mean over 400 builds): main notes per bar sd (-1.255), on sixteenth (-0.513), chord tones on long notes (-0.482), range (-0.269); control notes per bar sd (-1.217), on offbeat eighth (-0.478), distinct pitches (-0.446), chord tones on long notes (-0.333) (finding 299).

## 7. Distance, the outside count, reciting, the era

| Run | Distance from the centre | Outside both kept middle halves (of 56) | Verse on reciting (sd) |
|---|---|---|---|
| Main (243 on) | 0.114 · 0.19 · 0.301 (pick 0.235) | 11 · 15 · 20 (pick 17.0) | -0.973 · 0.4 · 1.88 (pick -1.003) |
| Control (243 off) | 0.062 · 0.106 · 0.18 (pick 0.145) | 6.5 · 10 · 14.275 (pick 13.0) | -0.343 · 0.46 · 1.34 (pick 0.921) |

No era was chosen (Q8), so 264 did not run; the five era readings are printed for the record: notes_per_bar 5.125, range 11.0, repeat 0.1, distinct_durations 5.0, pitch_bits 2.742. 243 drew the pick's target windows from 1959 (verse pool) and 1967 (chorus pool); the pools run 1958–1991 and 1958–1991 (medians 1974, 1976). No character was chosen (Q9), so 281 and 293's first half did not apply.

## 8. The tests of fixes 257–297

| Fix | The test | The reading (main; control where it says) | Held? |
|---|---|---|---|
| 257 | median 50–78% arched or falling; arch term positive in half or more; no survivor outside 31–94% or with valleys over 33% | 61.7%, positive 51.1%; 4 of 468 survivors outside, 18 with valleys over 33% | median yes; positive yes (51%); survivors no |
| 258 | median widening −0.1 to +1.1; no survivor outside −1.4 to +1.9 | 0.188; 2 survivors outside | median yes; survivors no (2) |
| 259 | median extra surprise 0.8–1.9 bits; joins a fourth or more in 25–40%; no survivor under −0.1 | 1.162 bits; joins 39.1%; 1 survivor under −0.1 | median yes; joins yes; survivors no (1) |
| 260 | median 33–78% after the downbeat; no survivor under 10% | 63.8%; 0 survivors under 10% | yes |
| 261 | a reading: last note over mean (kept 1.2–1.7), last note the longest | 2 · 2.286 · 2.857; longest 0.809 · 0.915 · 0.979 | printed (long; finding 306) |
| 262 | last chorus on the tonic; an earlier chorus on the tonic triad; the verse off the tonic | last chorus 89.4%, chorus 1 100.0%, verse 1 off 100.0%; the pick all three | no: the last chorus in 89% (finding 302) |
| 263 | intake count of windows both reciting and in the era | no era and no character | did not apply |
| 264 | the era gate | no era (Q8) | did not apply |
| 265 | the drawn window's year recorded and in the era | recorded: verse 1959, chorus 1967; no era | recorded; the era half did not apply |
| 266 | no aimed measure from a class median | none | yes |
| 267 | no build dies at the return gate where 239 built the return | deaths 0 main, 0 control; readings: kept 4864 | yes (287) |
| 268 | verse 2 shares 25–75% of verse 1's bar rhythms at the median | 0 · 0.182 · 0.417; in range 34.4% (control 0 · 0.222 · 0.455) | no (finding 303) |
| 269 | 260's test; last stresses on 1 or 3 in 35–55% | after 63.8%; on 1 or 3 0.298 · 0.426 · 0.596 | yes |
| 270 | dies only at ten or more (276 governs); a fifth of lines (±half) with a run of four; reciting median 1.4–2.1 where a character is chosen | runs: soft 150, hard 10; lines with a run of four 27.0%; longest run 4 · 5 · 7 · 9 · 12; reciting 0.4 (no character) | runs yes; lines with a run of four yes; reciting did not apply |
| 271/285/290 | every aim kept followed at r ≥ 0.3; beat 3 dropped; turns per move kept | turns per move: verse 0.34, chorus 0.185; beat 3 (not aimed) verse 0.077, chorus -0.043; others ≥ 0.44 | no: turns per move in the chorus (finding 304) |
| 272 | fills against gaps of 2.75 beats or more; seven in ten filled | 16 of 20 filled; 9 short gaps filled with a beat and a half | yes |
| 273 | chord strikes with a bass note; 16% or more | see the consistency check (electric piano against the bass) | yes |
| 274 | the extension named; every other section a multiple of four | the last chorus's 18 bars (the tag); all others multiples of four | yes |
| 275 | every gate printed with its kept pass rate; under 90% flagged | section 4 | printed |
| 276 | the limits on every build; pick and median beside the table | section 3 (fifteen limits) | yes |
| 277 | deaths on a hard limit or a third soft break under one in five; the pick's soft breaks printed | main 153 deaths of 1,000; control 56; pick none | yes (main 15.3%) |
| 278 | no death for a comparison, a return's first or top note, or a tritone unless chosen; design gates listed; kept rates beside | no design gate; aims below | yes |
| 279, 284, 292 | records | 292: the composite's first ranks 36 of 468 by the judge (main), 230 of 570 (control) | — |
| 280 | the seven's pass rates | amended by 286; section 4 | printed |
| 281 | a chosen character's axis | no character (Q9) | did not apply |
| 282 | a line said twice keeps its source | the chorus's line 5 = line 1, pitches and onsets (213, Q11's plain repeat) | yes |
| 283 | the feel of each section stated | straight throughout; verses half time (Q19) | stated |
| 286 | deaths at the spectral reading under one in five; the seven's joint pass rate printed | spectral decided 5 deaths main, 9 control; the seven pass 93.2% of the pairs | yes |
| 287 | no build dies at 267 where 239 built the return | 0 and 0 | yes |
| 288 | lengths in eight bars spread 4–8; chorus-over-verse medians inside the kept middle half in half the builds or more | lengths 5 · 6 · 6 · 7 · 8 (control 5 · 5 · 6 · 6 · 6); medians inside 40.9% (control 48.2%) | lengths yes (main), narrow in the control; medians no (finding 298) |
| 289 | last stresses on 1 or 3 in 35–55%; last notes on a downbeat inside the kept 11–43% | 0.298 · 0.426 · 0.596; downbeat ends 0.085 · 0.298 · 0.468 | yes |
| 290 | each aim's last two readings and the drop | beat 3: dropped (verse 0.077); turns per move: chorus 0.185 (song 38's rerun 0.172) | printed; turns per move fails a second song running |
| 291 | after the refit, the content judge's median at or above the first run's; held-out AUC printed | content median -1.295 (kept held-out median 4.16); no held-out rows on file | no (finding 299); the AUC not printable |
| 293 | verse 2's share inside 25–75% in three builds of four (the axis half: no character) | in range 34.4%; bars copied 1579 across 1,000 builds; copy given up for 31 lines | no (finding 303); first half did not apply |
| 294 | each pool's years and the ruling | no era, no character | did not apply |
| 295 | fewer than one build in ten needs the move | 207 of 1,000 (20.7%); control 143 | no (finding 302) |
| 296 | the pick under the old fit term printed | main: 353742341ffc (differs); control: the same | printed: the pick differs in main |
| 297 | the session's readings adopted | run of ten a limit; verse 2 takes its source's entry; near-level 2; the first three-quarters by time; entry 62/21/17% | yes |

Fixes that did not apply: 263, 264, 281 and 294 (no era, no character), the first half of 293 (no chosen axis), 265's era half. Fixes 279, 284 and 292 are records; 261 a reading. Failed by a named design choice: none of the tests above; 230's two-bar rule is met by Q21's design (below), and 236's drum defaults are replaced by Q19's design.

**278's aims: the builds' rate beside the kept rate (main).**

| Aim | Kept | Main | Control |
|---|---|---|---|
| chorus median over the verse's inside the kept middle half (0 to 3) | 50.0% | 40.9% | 48.2% |
| chorus top over the verse's inside the kept middle half (-1 to 3) | 50.0% | 41.2% | 41.1% |
| chorus lowest over the verse's inside the kept middle half (0 to 4) | 50.0% | 66.8% | 70.0% |
| bridge median over the verse's inside the kept middle half (0 to 5) | 50.0% | 68.3% | 71.5% |
| chorus top at or above the verse's | 72.9% | 65.6% | 63.4% |
| chorus median not below | 77.1% | 71.9% | 76.9% |
| chorus lowest note above | 55.7% | 61.6% | 65.7% |
| bridge median above the verse's | 67.4% | 68.6% | 68.0% |
| bridge top under the song's | 55.8% | 33.4% | 31.2% |
| returns keep their first note | 80.2% | 67.4% | 66.8% |
| returns keep their top note or higher | 92.4% | 99.9% | 100.0% |
| no tritone leap | 65.9% | 68.3% | 69.6% |
| no note a tritone from the root | 54.1% | 65.8% | 67.3% |

**Aims followed (correlation of target and reading across main's builds):** v:turns_per_move 0.34, c:turns_per_move 0.185, v:on_beat3 0.077, c:on_beat3 -0.043, v:on_tonic 0.853, c:on_tonic 0.733, v:on_third 0.786, c:on_third 0.559, v:on_fifth 0.854, c:on_fifth 0.623, v:repeat 0.893, c:repeat 0.892, v:step 0.872, c:step 0.874, v:chord_tones_on_beat 0.544, c:chord_tones_on_beat 0.679, v:gap_eighth 0.759, c:gap_eighth 0.558, v:gap_sixteenth 0.698, c:gap_sixteenth 0.437. The control aims every build at its pool's medians, so it has no spread to correlate.

**The other design rules, on the pick.** 230: every section's sung rate inside 3.2–6.2 syllables a bar, and every line of nine or more syllables in two bars is one of the 27 Q21 names. 232: 'earth' on beat 1 and held three beats in the hook, a whole bar in the tag. 236: the drum design (Q19) is checked against the record.

## The record

Built from the main run's shortlist pick 2fe2be999be7 with no hand edits; the riff, fills and riff break drawn by riff_p40.py (seed 20261512: the riff from 3759 distinct figures, 874 passing; the break's draw passed with chord tones on the beats 0.62, no tritone). The demo's stems: the voice +4.9 dB over the band. Energy (band only, read where a build arrives): Intro 0.27, Verse 1 0.50, Pre 1 0.74, Chorus 1 0.74, Verse 2 0.44, Pre 2 0.75, Chorus 2 0.75, Bridge 0.58, Riff break 0.73, Last Chorus 0.83, Outro 0.58. Every document passes the consistency checks against the record.

## Readings the paper does not give

- **230 (Q21).** The form and the locked lyric are the design 230 allows for lines of nine or more syllables in two bars; the 27 lines are named in the code (DESIGNED_TWO_BAR).
- **232 over 289.** A title line (the hook and the tag) lands on beat 1 or 3; 289's shares are drawn for the other lines only.
- **236 (Q19).** The half-time verse is an arrangement design and gates nothing in the melody search.
- **243.** With no era and no character, the pools are by section kind: verse and pre-chorus from the kept verse windows, chorus and bridge from the kept chorus windows.
- **249.** The chorus calibration window is Chorus 1 (no designed notes); every knob is held to a third to three times its start (the sixteenth knob down to 0.02); the contour amplitude is capped at 7.
- **267/297.** Near-level is a span of two semitones or less (297 adopted it); returns read by time.
- **286.** The six limits are read on the 515 POP909 calibration pairs at the 5th/95th (soft) and 1st/99th (hard); the sequence-legs limit is soft at one leg over (any two-leg sequence) and hard at two; the seven are counted with 276's eight in one count of three soft breaks; a reading that cannot be taken counts as hard.
- **287.** A built return is also exempt from the post-pass that steps a flat-3, flat-7 or tritone note to a chord tone, not only from the join and leap repairs.
- **288.** The kept rates of the note lengths are the v88 pop IOI shares (the 'longer' share split between 36 and 48); the palette of eight is 3, 6, 9, 12, 18, 24, 36, 48 twelfths; a title note is held two beats or more and the song's last note a bar; the chorus's median, top and lowest are drawn from one quantile together, the bridge from its own; the verse's centre E4, cap A4, floor A3 (the voice row).
- **289.** The shares are applied to each line's last note; within 'off the beat' the onset is the line's own.
- **291.** Separation is printed as the builds against the kept held-out percentiles; the file has no held-out rows for an AUC.
- **293.** A copied bar keeps every onset of its source bar; after fourteen tries the copy is given up for that line; a line that no rhythm places is placed with a free entry and landing (counted).
- **295.** The hook must end on the tonic, since the last chorus's tag copies its tail; a last note that the drawn contour misses is moved one to three semitones (counted).
- **296.** The old fit term, for the report, is the term with the lift mark restored at full marks for four semitones and half for two.
- **Form.** The last chorus's line 8 is a return of the hook (its words differ: 'and it tastes like…'); the tag is the hook's last five syllables.
- **Never-say.** 'stone' is a common noun here, not a name.
- **Seed.** 20261511, the session's convention (20261110 + 401).
- **The riff.** Placed from D3, D mixolydian over C; it plays the intro's eight bars and the outro's first three (Q5's riff-led reading).

## Findings

**298. On the default path the chorus can sit under its verse, and since 296 nothing in the pick prefers otherwise.** *Problem:* the writer asked for a world-class hook and took the default lift (Q17 A). 288 draws the chorus's median, top and lowest from the kept distribution, where the chorus top is at or under the verse's in half of kept songs, and 296 took the lift mark out of the composite's fit term, the only term that preferred a lift. *Evidence:* the pick's registers were drawn at the kept 28th percentile (chorus median +0.12, top -0.88) and read -1 and -2: the chorus tops at G4 under the verse's A4, and the hook runs C♯4–G4 and lands on D4. Under the old fit term the pick is 353742341ffc (lift +4.5 median, +2 top). Only 41% of main's builds have the chorus median inside the kept middle half (288's check asks half). *Fix:* the intake's lift question prints what the default draws (a chorus top at or under the verse's in about half the builds) before the writer answers; the paper reads, on kept songs, where the title line sits against the verse, and if it sits above in most, the title line's register becomes an aim. *Check:* the next default-path intake shows the figure; the report prints the title line's median against the verse's beside the kept figure.

**299. The judge's floor is the search's largest killer; the builds sit far under the kept held-out percentiles, and the chorus's design is what it reads.** *Problem:* the refitted judges (291) put a floor at the kept 5th percentile, and a quarter of this song's builds fall under it. *Evidence:* deaths at the floor: main 164, control 141; under the floor 26.5% (main) and 21.3% (control) of complete builds, against 5% of kept windows by its making; combined median -0.13 against the kept 2.95; 0.1% of builds reach the kept median. The heaviest give-away is the spread of notes per bar (-1.255): the chorus window reads 3.53 at the median against kept windows' 1.60 (95th 2.91). The chorus's two-bar lines put nine to eleven syllables in one bar and the held title in the next, the writer's design (Q21) and 232's hold. *Fix:* where 230's two-bar lines are a named design, the floor reads the window outside the designed section, or the design is printed with the judge's reading of it and exempt from the floor. *Check:* deaths at the floor under one build in ten when a section is a 230 design.

**300. Aiming each build at one kept window (243) costs realness.** *Problem:* the main run loses three times the control's builds at the limits, and realness is most of it. *Evidence:* realness broken in 219 main builds (79 hard) against 21 in the control (14 hard); builds' median realness 0.1592 against 0.4184; limits deaths 153 against 56. The realness limit is read on POP909's 515 pairs; the windows 243 aims at are 1958–1991 chart songs. *Fix:* read the realness limit's pass rate on the kept chart windows themselves; if aimed kept windows fail it, read the limit on that corpus. *Check:* the report prints the share of kept chart windows above the realness hard limit, and main's realness deaths come within twice the control's.

**301. 286's hard limits fail 7% of the pairs they were read on.** *Problem:* six limits each hard at their own 1st/99th compound. *Evidence:* 35 of 515 calibration pairs break a hard limit; the seven pass 93.2% of the pairs as 286 applies them (276's eight pass 92% of kept songs). *Fix:* set the hard limits so the seven together keep 99% of the pairs (or read the fifteen's joint rate and print it as one family under 275). *Check:* the seven's joint pass on the pairs at 95% or more; the fifteen's joint kept rate printed.

**302. Endings: the move 295 meant to retire still fires in one build in five, and the last chorus misses the tonic in one in ten.** *Problem:* the drawn contour misses its permitted ending and the fallback moves the note; where no move is allowed the line keeps its wrong ending. *Evidence:* last note moved in 207 of 1,000 (main) and 143 (control), against the check's one in ten; the last chorus ends on the tonic in 89.4% of main's builds (control 94.2%). In this song the hook carries the rule, since the tag copies its tail. *Fix:* draw the ending line's last note first, among the permitted degrees, and walk the line back to it. *Check:* moves under one in ten; the last chorus on the tonic in every build.

**303. Verse 2 copies too few of verse 1's bars.** *Problem:* 293 draws verse 2's bar rhythms from verse 1's at 40%, then fits the syllables, and most copies are lost in the fit. *Evidence:* verse 2 shares 18% of verse 1's bar rhythms at the median (in range in 34% of builds; control 22%); 1579 bars copied across 1,000 builds of a 12-bar verse; the copy given up for 31 lines. The session's reading kept every source onset in a copied bar (listed). *Fix:* a copied bar may add or drop one onset for the syllable count. *Check:* verse 2's share inside 25–75% in three builds of four.

**304. Turns per move fails in the chorus a second song running.** *Problem:* 290 kept the aim because it had failed once since it last held; it has now failed twice. *Evidence:* the chorus's target and reading correlate at 0.185 (song 38's rerun 0.172); the verse 0.34. *Fix:* by 285's rule, drop the aim in the chorus. *Check:* the report lists it as dropped.

**305. The contour amplitude sits at its cap and the arch term stays far under the kept figure.** *Problem:* 249's line-strength pass cannot reach the kept arch term on this song's lines. *Evidence:* 249's last round read arch term 0.084 against the kept 1.452 with the amplitude at the cap of 7; the builds' arch term 0.161 at the median, arch positive 51%. Lines here are short in pitch (a mezzo row and 288's narrow chorus), and 289's landings end most lines low. *Fix:* the arch term is calibrated on lines of the song's own span, or the paper states the arch term's kept figure per line span. *Check:* the calibration reads the arch term within the kept middle half without reaching the cap.

**306. 288's holds make every line's last note too long.** *Problem:* the end-length draw favours the long holds, and every line ends on one. *Evidence:* last note over the line's mean note 2.286 at the median (5th–95th 2.0–2.857) against the kept 1.18–1.71; 99.9% of builds outside the kept middle half (song 38's rerun 1.778). The end lengths are weighted by the long holds' kept rates and title notes take two beats or more. *Fix:* draw a line's last length from the kept last-note ratio (Table DJ) rather than the palette's rates. *Check:* the builds' median inside 1.2–1.7.

**307. Nothing reads where the song's top note falls in the words.** *Problem:* with no designed summit, the song's top note can land on a passing sixteenth or a weak word. *Evidence:* the pick's C♯5 is sung three times, each a sixteenth, first on 'the' ('takes the shadow and the shine'); in main's builds the top note falls only on unstressed syllables in 7.2% and only as sixteenths in 10.7%. *Fix:* a reading for the report: the top note's syllable stress and length beside the kept figure. *Check:* printed for every pick.

