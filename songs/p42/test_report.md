---
title: "Song 42 test report: Nothing Important"
subtitle: "ZenEng v110 (fixes 310–321): the port tested on song 40, then a new song on the default path in a straight feel"
author: "Words and music: Jason Bryant"
---

# The port test (song 40 again)

Fixes 310–321 were ported onto song 40's default-path search (`melody_v110_p40.py`, built from the tested v109 port by `gen_v110_p40.py`). Nothing blocked the port, and no two fixes conflicted. 1,000 builds main and 1,000 control (243 off), each made twice: seed 20261511, calibration 20261512, PYTHONHASHSEED 0, code d6103b203607.

| Run | Survivors (v109 port) | Frozen order | Second run |
|---|---|---|---|
| Main | 505 (476) | 3c9c4f2da558 | reproduced |
| Control | 537 (398) | 30ba2486b5e4 | reproduced |

Deaths, main: the judge's floor (254; 279) 168, join: no held end and breath before the copy (212) 130, key word on a chord tone (134; 279) 89, limits: a hard limit or three soft breaks (276/277, with 286's seven) 75, bridge opening unrelated (208; 279) 30, join: no held end and breath before the line (212) 1, chorus opening another tune (227; 279) 1, align: the words do not fit the returning tune 1.

## The tests of 310–321 on the port (321)

| Fix | Test | Main | Control | Held? |
|---|---|---|---|---|
| 310 | under the floor < 10%; likeness of bar rhythms (parallel) >= kept 0.14 at the median; no judge refitted | under floor 25.8%; parallel 0.094 (kept 0.14); paired lines 4765, partner given up 1674 | under floor 28.5%; parallel 0.105 (kept 0.14); paired lines 4847, partner given up 1706 | **no** |
| 311 | the last chorus on the tonic in every build; misses none | tonic 100.0%; registers redrawn 240; misses 0 | tonic 100.0%; registers redrawn 239; misses 0 | yes |
| 312 | leaps past a fifth <= 3.6% of moves at the median, verse and chorus | verse 0.0%, chorus 0.0%; leap knob 1.0 | verse 0.0%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | verse 2 shares 25-75% in 3 builds of 4; copies given up < 1 line in 20 | share [0.0, 0.25, 0.455]; in range 53%; given up 10 (0.2%); left out 4805 | share [0.083, 0.273, 0.5]; in range 66%; given up 18 (0.3%); left out 4069 | **no** |
| 314 | range printed; unused above/below differ by 1 at most; verse median 40-57% of the range; tonic endings nearest the median | range [10.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.294, 0.429, 0.588]; tonic nearest 0.971; top fifth 74%; floor 38% | range [11.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.312, 0.471, 0.571]; tonic nearest 0.986; top fifth 77%; floor 41% | **no** |
| 315 | amplitude <= 7; calibration stops on two largest steps running; arch over the span 0.0-0.55 at the median | amplitude 5.0; arch [-0.106, 0.077, 0.273]; stop none | amplitude 5.0; arch [-0.086, 0.09, 0.298]; stop none | yes |
| 316 | redraws per long line < 1.5; entry shares unchanged | redraws 0/13368 = 0.0; entries {'starts_on_downbeat': 0.23, 'starts_after_downbeat': 0.647, 'starts_as_pickup': 0.123} (before {'starts_on_downbeat': 0.224, 'starts_after_downbeat': 0.647, 'starts_as_pickup': 0.129}) | redraws 0/13399 = 0.0; entries {'starts_on_downbeat': 0.244, 'starts_after_downbeat': 0.628, 'starts_as_pickup': 0.129} (before {'starts_on_downbeat': 0.228, 'starts_after_downbeat': 0.639, 'starts_as_pickup': 0.133}) | yes |
| 317 | each design gate's pass rate printed; nine in ten or more | none in force | none in force | yes |
| 318 | the feel named; sixteenths printed | straight eighths; sixteenth onsets [0.097, 0.131, 0.179] | straight eighths; sixteenth onsets [0.075, 0.092, 0.114] | printed |
| 319 | no instrumental note outside its instrument | read on the arrangement (riff script); the port test has no instrumental lines | read on the arrangement (riff script); the port test has no instrumental lines | n/a |
| 320 | rescorings stated as bounds | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | this table, on this song's own runs | this table, on this song's own runs | yes |

# Song 42: Nothing Important

| | |
|---|---|
| Song | Nothing Important. A piano ballad, straight eighths at ♩ = 76, B♭ major, for a warm alto (row F3–D5); 68 bars, 3:35. |
| Source | *Resurrection-Shaped Architecture* (Jason Bryant), used abstractly: the part holds the whole; an identity outlives what carried it; known again by its marks; the promise of return from his side. Nothing is named (Q9 B: one faint echo, "the third morning"). |
| Path | Default: no era, character, summit or lift; the song's range centred in the row (314, Q8 A); the bridge drawn as kept songs do (Q15 A). |
| Designs in force | Every line two bars (Q13 A; 230 failed by a named design choice). The last chorus (Q11 note 4): "Hey, it's me" is the hook's head; "Nothing important" is the hook's tail with its rhythm augmented; "I'll call you back" falls to the tonic under the hook's end: a design gate, outside 275 (317). The cello's countermelody in the bridge and the last chorus (Q14 A; arrangement). The piano part complete on its own (Q7; arrangement). |
| Seeds | 20261552, calibration 20261553, PYTHONHASHSEED 0, code 7f9c4b29eacc. |
| Rerun | `PYTHONHASHSEED=0 python3 melody_p42.py 1000 main|ctl` |

**Intake.** Fifteen questions, one per turn, logged in `intake.py`: the idea (from the attached paper), the voicemail's turn, how to make the situation clear, the message and title, sound, form, voice and key, the song's place in the row (314), never-say, said twice, two drafts and the lock, the slots (230), the cello, the bridge.

| Run | Survivors | Frozen order | Second run |
|---|---|---|---|
| Main | 567 | 5614d9557a76 | reproduced |
| Control | 595 | 46d4320fd85a | reproduced |

Deaths, main: design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4) 247, limits: a hard limit or three soft breaks (276/277, with 286's seven) 49, the judge's floor (254; 279) 37, join: no held end and breath before the line (212) 37, bridge opening unrelated (208; 279) 35, key word on a chord tone (134; 279) 17, chorus opening another tune (227; 279) 11.

**The pick of record (255).** 389da0041c48: fifth by the composite (0.836), inside the judge's top half (judge 2.639), no soft limit broken; taken as drawn, no hand edits. The voice spans F3–A4. The verse sits highest (median F4); the chorus, his message, sits lower (median D4; lift −3 median, −2 top); the bridge lowest (median C4, touching F3). The hook moves quickly through "hey, it's me, noth-ing" (sixteenths) and holds "im-POR-tant" on E♭4. In the last chorus "Nothing important" is the hook's tail at half speed, E♭4 held over three beats; "I'll call you back" falls to B♭3.

## The tests of 310–321 on song 42's own runs (321)

| Fix | Test | Main | Control | Held? |
|---|---|---|---|---|
| 310 | under the floor < 10%; likeness of bar rhythms (parallel) >= kept 0.14 at the median; no judge refitted | under floor 6.4%; parallel 0.188 (kept 0.14); paired lines 4083, partner given up 1474 | under floor 5.0%; parallel 0.181 (kept 0.14); paired lines 4101, partner given up 1431 | yes |
| 311 | the last chorus on the tonic in every build; misses none | tonic 81.3%; registers redrawn 202; misses 0 | tonic 83.9%; registers redrawn 202; misses 0 | **no** |
| 312 | leaps past a fifth <= 3.6% of moves at the median, verse and chorus | verse 2.5%, chorus 0.0%; leap knob 1.0 | verse 2.6%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | verse 2 shares 25-75% in 3 builds of 4; copies given up < 1 line in 20 | share [0.0, 0.286, 0.625]; in range 71%; given up 1 (0.0%); left out 3287 | share [0.125, 0.375, 0.667]; in range 84%; given up 0 (0.0%); left out 2629 | **no** |
| 314 | range printed; unused above/below differ by 1 at most; verse median 40-57% of the range; tonic endings nearest the median | range [12.0, 16.0, 18.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.429, 0.571]; tonic nearest 0.972; top fifth 69%; floor 18% | range [12.0, 15.0, 18.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.438, 0.571]; tonic nearest 0.981; top fifth 75%; floor 13% | **no** |
| 315 | amplitude <= 7; calibration stops on two largest steps running; arch over the span 0.0-0.55 at the median | amplitude 7.0; arch [-0.205, 0.052, 0.308]; stop none | amplitude 7.0; arch [-0.199, 0.047, 0.315]; stop none | yes |
| 316 | redraws per long line < 1.5; entry shares unchanged | redraws 0/9472 = 0.0; entries {'starts_on_downbeat': 0.216, 'starts_after_downbeat': 0.644, 'starts_as_pickup': 0.14} | redraws 0/9495 = 0.0; entries {'starts_on_downbeat': 0.212, 'starts_after_downbeat': 0.634, 'starts_as_pickup': 0.154} | yes |
| 317 | each design gate's pass rate printed; nine in ten or more | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.744} | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.769} | **no** |
| 318 | the feel named; sixteenths printed | straight eighths, q = 76; sixteenth onsets [0.079, 0.118, 0.17] | straight eighths, q = 76; sixteenth onsets [0.056, 0.072, 0.094] | printed |
| 319 | no instrumental note outside its instrument | read on the arrangement (riff script); the port test has no instrumental lines | read on the arrangement (riff script); the port test has no instrumental lines | n/a |
| 320 | rescorings stated as bounds | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes |
| 321 | this table | this table, on this song's own runs | this table, on this song's own runs | yes |

311 on survivors: the last chorus ends on the tonic in 100% of the 567 main survivors; the misses are all builds the design gate killed (finding 325).

**Arrangement and documents.** The piano's intro figure: 1,120 drawn, 163 passed; the pick on the "and" of 1, beat 2, the "and" of 2 and the "and" of 3 (B♭4 D5 G5 F5), unrelated to every sung opening. The cello's countermelody (bridge and last chorus) C3–C4, always under the voice, no semitone, no tritone, 1 unison of 16 shared onsets. 319: every instrumental note inside its instrument's range. The demo: voice +9.9 dB over the band; the energy arc meets 9.12. Readback: the voice (259 of 259), both piano hands (537 and 236), three parts; 104 of 104 drum hits written. Consistency: every check passes.

# Readings the paper does not give

**The port:**

- **310.** A pair is line k of four-bar units 2m and 2m+1 when both units have the same slots; a section whose slot boundaries do not fall on four-bar lines has no units. The partner's every bar is copied as the prior (off-source onsets weighted 0.04) and the result kept only within one onset a bar (303); after fourteen tries the partner is given up (counted). "Ends by beat 3" is read as the last onset at or before beat 3 of the unit's last bar.
- **311.** Registers redrawn up to 50 times until the chorus's holds a tonic; a 51st miss is counted.
- **312.** A leap knob on the walk's "larger" category, cut when the calibration builds' median past_fifth exceeds 3.6%.
- **313.** A source bar with more onsets than the line's cap is left out of the copy.
- **314.** The kept range and verse-share quantiles linearly interpolated, with tails extrapolated past the 5th and 95th; the odd spare semitone above; the verse's floor and cap at its median −7 and +5 inside the song's range.
- **315.** The largest step is defined for the knobs with a step clip (amplitude, the first note's freshness, the leap knob: a multiplier at its clip); the kept-window knobs have bounds, not steps.
- **316.** What fits is computed per slot (section, line, earliest start, end) and cached.

**Song 42:**

- **Plans.** The paper's verse and bridge plans are written for six lines; each is cut to its first four.
- **Q11 note 4.** "Nothing important" is the hook's tail with its onsets doubled from the hook's own entry (1.5 or 1 if double will not fit, counted); "I'll call you back" is drawn fresh, its ending the tonic under the hook's last note, its register's floor the song's floor.
- **Q7.** The piano patterns (broken chords, quarters, block chords, held chords) are the session's; the paper has no table for a solo piano accompaniment.
- **Pronunciation.** "blinker" (not in the pronouncing dictionary): B L IH1 NG K ER0.
- **Seed.** 20261552 (20261110 + 442).

# Findings (from 322)

**322. Fix 310 holds where paired lines are alike and fails where they are not.**

- *Problem.* The partner's rhythm is copied bar for bar and kept only within one onset a bar; when the two lines' syllable counts differ, most copies are given up.
- *Evidence.* Song 40: under the floor 25.8% (main) and 28.5% (control), down from 32% and 42% but over one in ten; likeness of bar rhythms 0.094 and 0.105 (kept 0.14); the partner given up for 1,674 of 4,765 paired lines (35%). Song 42 (all lines two bars, units of two lines): under the floor 6.4% and 5.0%, likeness 0.188 and 0.181: 310 held.
- *Fix.* Where partners differ by more than one syllable, keep the partner's stressed onsets and draw the rest freely, without the one-onset check.
- *Check.* On song 40, partners given up under one in ten and likeness at or above 0.14.

**323. Fix 313 leaves out the bars a copy most needs.**

- *Problem.* A source bar with more onsets than the line's cap is left out of the copy entirely.
- *Evidence.* Song 40: 4,805 bars left out, verse 2 in range 53% (control 66%); song 42: 3,287 left out, 71% (84%). Test: three builds in four.
- *Fix.* A source bar one onset over the cap is copied with its weakest onset dropped (303's one-onset allowance), not left out.
- *Check.* Verse 2 inside 25–75% in three builds of four.

**324. 314's tonic ending is aimed at the drawn register and read on the sung median.**

- *Evidence.* The tonic nearest the section's sung median in 97.1% (98.6%) of song 40's builds and 97.2% (98.1%) of song 42's.
- *Fix.* Aim the ending at the median of the section's notes already placed, or read the test on the drawn register's centre; state which.
- *Check.* 100% on the reading the paper names.

**325. 311 holds the register's tonic but not a design's ending.**

- *Problem.* Song 42's design asks the last line to end on a tonic under the hook's end. When the hook ends on the song's lowest tonic, no such ending exists, and the build dies at the design gate.
- *Evidence.* The last chorus on the tonic in 81.3% (83.9%) of complete builds; 100% of survivors.
- *Fix.* 311's redraw also reads a design's ending condition; or the hook's ending (302) is drawn above the song's lowest tonic when a design needs one under it.
- *Check.* The design gate at nine in ten; the last chorus on the tonic in every build.

**326. The design gate passes three builds in four (317).**

- *Evidence.* 74.4% (main), 76.9% (control). Why: as 325, the aim is not drawn inside the design.
- *Fix.* As 325.
- *Check.* Nine in ten.

**327. 310's unit ending crowds the breath before a copy.**

- *Evidence.* Song 40: deaths at "no held end and breath before the copy (212)" rose from 92 to 130 (main) and to 121 (control).
- *Fix.* Read the unit-end rule and 212's join together: a unit's last line ends by beat 3, or the copy after it enters after the downbeat.
- *Check.* Join deaths back to v109's level.

**328. A slow ballad draws sixteenths at pop's rate.**

- *Problem.* 288's sixteenth offer is not tempo-aware.
- *Evidence.* Song 42 at ♩ = 76: sixteenth onsets 11.8% at the median (kept median 1%, 75th 14.3%); the hook's "hey, it's me, noth-ing" is four sixteenths.
- *Fix.* Count sixteenth shares by tempo band on the kept songs and draw from the band.
- *Check.* Song 42's sixteenth share inside its tempo band's middle half.

# Blind pick

Not yet run: offered after delivery.
