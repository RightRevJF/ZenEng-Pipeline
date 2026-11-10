---
title: "Windows Down — Test report (ZenEng v96)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

## The brief

A new song under ZenEng v96, pop, rock or country. The spec read first (version row v130, last fix 224; the session's 212–223 under its numbers; Module 27.38 for what changed in 213, 218 and 220, and for 224); the tables read, not refitted: zeneng_v88_tables.json (sha256 561355b1…), zeneng_v91_hymn_supplement.json (e74e7c30…), zeneng_v96_discriminator_tables.json (1a2af952…; 56 measures, 46 marked for the distance). Intake one question a turn, the full lyric before any music; at the lyric stage 220 (every section a multiple of four bars; lines too long for two bars named), 213 (one verse or chorus whose first two lines are within three syllables, and why), 202 and 208 (the summit question with chart pop's peak; the bridge question with the kept figures). Ported before the search: 224 first, then 212, 214, 215, 216, 217, 218, 219, 223. A control with 224 off. Findings from 225; the paper not edited.

## Intake

| # | Question | Answer |
|---|---|---|
| 1 | which class | B |
| 2 | the one moment (10.10) | A |
| 3 | who sings, to whom | B |
| 4 | the turn | A |
| 5 | title | A |
| 6 | who sings (11.2) | A |
| 7 | tempo, feel, key | A |
| 8 | form (220: multiples of four; 139: summed and timed) | A |
| 9 | never say | A |
| 10 (213) | which section opens by saying it twice | A |
| — | lyric draft 1 | shown in full (lyric_draft1.md) |
| — | lyric draft 1 notes | 1 too many generic images (gravel crunching, sun still high, radio low, county road): one or two details only this plant, this man, this day; 2 pre-choruses functional, not charged; 3 bridge good not  |
| — | lyric draft 2 | shown in full (lyric_draft2.md) |
| — | lyric draft 2 notes | 1 pre-choruses lag: Pre 1 a little explanatory; Pre 2 line 2 strong, line 1 functional not vivid; 2 verse 2 observational while the song has become personal (the gate a good detail); 3 'Number Four we |
| — | lyric draft 3 | shown in full (lyric_draft3.md) |
| — | lyric draft 3 | A |
| — | form correction (no question) | Q8's sum was wrong: Intro 4 | V1 8 | Pre 4 | Ch 8 | V2 8 | Pre 4 | Ch 8 | Bridge 8 | Solo 8 | Last Ch 16 | Outro 4 = 80 bars, 2:37 at q = 122 (not 88, 2:53). Told the writer. |
| 11 (202, 216) | the summit; chart pop's peak at a median 31%, in chorus or bridge 67%, sounded about 4 times | A. But the song is taking too short. Rock songs are longer than pop, right? |
| 12 | length (rock runs longer) | A |
| 13 (208) | the bridge's register; kept (69 chart songs): opening related to neither 94% (a gate); median above the verse 68% (+2 st); highest of three 46%, lowest 14%; pace 0.97 of the verse (0.78-1.21) | A |

**The song.** *Windows Down*: heartland rock, 4/4 at ♩ = 122, A major, male baritone D3–F♯4. A man walks out of his plant's last shift after twenty-six years and drives home to his wife with the windows down. Form (220: every section a multiple of four bars, every line two bars, no three-bar line chosen): Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 16 · Last Chorus 16 · Outro 8 = 112 bars, 3:40. At the lyric, no line needed more than two bars at about four syllables a bar; the tightest held nine sung syllables after the pickup and were named while the lyric was open. The chorus opens with two title lines of eight syllables each (213).

## The ports

| Fix | In song 37 |
|---|---|
| 224 | Before each build, a target drawn uniformly from chart pop's kept middle half (25th–75th) on eleven calibrated measures (repeat, step, third, fourth or fifth, past a fifth, chord tones on and off the beat, eighth- and quarter-note gaps, the longest note over the median, notes a bar), recorded with the build. The walk's category weights, the chord term, the rhythm's gap tilt and landing, the line-end holds and the melismas are aimed at the build's own point. The control draws nothing: every build aimed at the chart medians. |
| 212 | A line followed by a copy (a repeated section, a returning unit, the chorus's second eight bars, and chorus 1's line 4 before verse 2's first line) is drawn with its last onset no later than the copy's first onset less a quarter's hold and an eighth's breath. |
| 214 | One draw over every candidate pitch, each interval category tilted by the chord it offers; recalibrated for this song so builds read near their own targets. |
| 215 | No sung note a tritone from its chord's root (G♯ over D here); the walk skips it, a copied note moves a step to a chord tone; gated on beats and on notes a quarter or longer. |
| 216 | The summit (the writer's A): F♯4 on 'HOL-lering', the first stress of chorus line 4, fixed on that line's downbeat; the chord plan puts D under it (D holds F♯); five times. |
| 217 | Copies keep their place counted from their line's end (two-bar lines, so no copy moves); every chorus's last line lands on A over A. |
| 218 | About four syllables a bar; onsets on eighths; quarters inside lines (the gap tilt, and lines that land on beat 3 of their second bar); line ends held a quarter, a dotted quarter or a half. |
| 219 | The 181 gate read on lines, onsets and contour counted from each line's downbeat. |
| 223 | A compound of two monosyllables ('someday') takes its primary on the first part, except as the line's last word. |
| kept | 181/195 returns; 182's walk with 197's turn; 196's run clause; 200; 205's plans (the chorus offered by the lyric, AABC drawn at 0.3); 208 (the bridge's opening a gate, its median above the verse's a gate, the writer's A: lifted); 209 (riff_p37.py); 210 on 46 measures from the v96 file; 211. No stressed syllable is placed as a pickup. |

**The search.** N 500, seed 20261481, PYTHONHASHSEED 0, code b1b68b67d425, Python 3.13.18, numpy 2.5.3. 153 survivors of 500; frozen order 15ed5929f53d, reproduced exactly on a second run. Pick 9a3e548d293f, first by the rank of record (composite 0.884); no hand edits. Plans: verse AABC, pre-chorus AB, chorus ABAC sung twice, bridge ABAC. The pick's drawn targets: repeat 0.169, step 0.5603, third 0.1607, fourth fifth 0.0918, past fifth 0.0182, chord tones on beat 0.6987, chord tones off beat 0.7509, gap eighth 0.5666, gap quarter 0.1624, longest over median note 3.6416, notes per bar 3.7152.

**The control.** Same seed and N, 224 off (every build aimed at the chart medians). 109 survivors, order 4d23a255a8b9; first pick 8db8e134f3a6 (composite 0.838).

**A probe (not asked for; evidence for finding 225).** Same seed and N, targets drawn from the kept 5th–95th instead of the middle half: 147 survivors, order f04360d518e5.

**Hand inspection of the pick.** Printed syllable by syllable before the record was built. Two faults in earlier picks of the same code were fixed in the construction and the run repeated: a stressed syllable placed as a pickup ('WIN-dows' with 'win' before the bar and '-dows' on the downbeat; 'NUM-ber' likewise), now never allowed; and the last line's first 'home', which the writer asked to be held, sung as an eighth; that line is now drawn with its first 'home' held a half note and its second 'I'm almost home' landing on A3. The frozen pick needed no hand edit.

## The readings the brief asked for

Builds are every song the generator finished, before the gates. Bar-window shares are medians in the table; across all builds the opening unit returned third in 39% of verse and chorus windows and was repeated at once in 28% (means; kept 31–49% and 17–28%).

| Reading | Pick | Builds 5th · median · 95th | Control's pick | Control builds (median) | Probe (5th–95th draws), builds median | Kept |
|---|---|---|---|---|---|---|
| Distance from the centre, 46 measures | 0.103 | 0.052 · 0.089 · 0.135 | 0.053 | 0.079 | 0.109 | chart songs 0.086 · 0.176 · 0.351 |
| Measures outside both kept middle halves (of 56) | 13 | 5 · 9 · 14 | 9 | 9 | 10 | — |
| Opening unit returns third (bar windows) | 75% | 0% · 25% · 100% | 25% | 25% | 25% | kept 31% (chart) · 49% (grid) |
| Opening unit repeated at once (bar windows) | 25% | 0% · 0% · 100% | 0% | 0% | 0% | kept 17% · 28% |
| Gaps of an eighth | 58% | 47% · 63% · 78% | 64% | 59% | 72% | chart 32–47–62% · grid 27–44–61% |
| Gaps of a quarter | 33% | 8% · 20% · 39% | 21% | 21% | 15% | chart 6–15–28% |
| Longest note over the median note | 4 | 1.5 · 3 · 4 | 4 | 3.5 | 4 | chart 2–3–4 · grid 2–3–5 |
| Notes a bar | 4.25 | 4.25 · 4.31 · 4.62 | 4.25 | 4.25 | 4.38 | chart 2.94–3.75–4.63 |
| Chord tones on the beat | 65% | 55% · 74% · 94% | 59% | 74% | 69% | chart 56–69–80% |
| Chord tones off the beat | 82% | 42% · 65% · 86% | 92% | 67% | 61% | chart 47–63–76% |
| Pitch surprise (bits a note, whole song) | 2.66 | 2.51 · 2.72 · 3.02 | 2.66 | 2.64 | 2.86 | chart 2.53–2.74–3.03 |
| Spread of notes bar to bar | 2.14 | 0.98 · 1.79 · 2.64 | 2.17 | 1.71 | 2.00 | chart 1.20–1.62–2.12 |
| Bridge median over the verse's (semitones) | 5 | 0 · 2 · 7 | 3 | 2 | 2 | kept +2 (68% above) |
| Bridge onsets a bar over the verse's | 0.94 | 0.89 · 0.94 · 1.00 | 0.94 | 0.94 | 0.94 | kept 0.97 (0.78–1.21) |

**Distance from the centre (210, on the 46 measures from the v96 file).** The pick 0.103, inside the chart range; the control's pick 0.053, TOO CENTRAL. Builds too central (under 0.086): run 45%, control 62%, probe 20% (song 36 version 3: 75%). Builds inside the chart songs' middle half (0.133–0.228): run 6%, control 3%, probe 24%.

**Every measure outside both kept middle halves (of 56).** The pick is outside both on 13: step 0.597 (high), turns per move 0.692 (high), longest run one way 2 (low), on third 0.324 (high), on fifth 0 (low), peak position 0.75 (high), time in top third 0.057 (low), on downbeat 0.235 (high), on beats 2 4 0.147 (low), gap quarter 0.333 (high), notes per bar sd 2.14 (high), chord tones off beat 0.824 (high), non chord resolved by step 1 (high). The control's pick on 9. The table lists every measure the pick is outside on and every measure at least a fifth of the builds are outside on.

| Measure | The pick | Share of builds outside (run) | Control | Probe | Chart 25–50–75 | Grid 25–50–75 |
|---|---|---|---|---|---|---|
| peak position | 0.75 (high) | 100% | 100% | 100% | 0.0391–0.2266–0.5469 | 0.0859–0.25–0.5781 |
| time in top third | 0.057 (low) | 57% | 58% | 53% | 0.2425–0.3778–0.5036 | 0.2143–0.3281–0.4771 |
| gap eighth | inside | 56% | 40% | 71% | 0.3158–0.4737–0.6154 | 0.2727–0.4444–0.6133 |
| on beat3 | inside | 54% | 62% | 37% | 0.0769–0.125–0.1667 | 0.0652–0.1154–0.1667 |
| low position | inside | 51% | 56% | 48% | 0.1367–0.3281–0.5547 | 0.0859–0.2344–0.5 |
| turns per move | 0.692 (high) | 38% | 33% | 36% | 0.4783–0.5714–0.6667 | 0.4667–0.5667–0.6765 |
| on fifth | 0 (low) | 37% | 36% | 26% | 0.0476–0.1429–0.2383 | 0.0833–0.1515–0.2353 |
| notes per bar sd | 2.14 (high) | 36% | 24% | 45% | 1.199–1.6154–2.1195 | 0.927–1.479–2.0463 |
| ascending | inside | 33% | 36% | 33% | 0.4167–0.4667–0.5 | 0.4142–0.4756–0.5357 |
| chord tones off beat | 0.824 (high) | 32% | 33% | 47% | 0.4748–0.625–0.7647 | 0.5–0.6207–0.7647 |
| on third | 0.324 (high) | 30% | 27% | 31% | 0.1127–0.1875–0.2698 | 0.1053–0.1786–0.2619 |
| non chord resolved by step | 1 (high) | 28% | 29% | 26% | 0.3153–0.5–0.6667 | 0.2857–0.4667–0.6667 |
| distinct bar rhythms | inside | 27% | 23% | 11% | 5–6–7 | 3–5–6 |
| on tonic | inside | 25% | 25% | 23% | 0.1143–0.2174–0.3333 | 0.1111–0.2–0.2857 |
| first note tonic triad | inside | 25% | 25% | 32% | 0.5–1–1 | 1–1–1 |
| chord tones on beat | inside | 23% | 19% | 42% | 0.5625–0.6923–0.8 | 0.5714–0.7222–0.8571 |
| step | 0.597 (high) | 22% | 18% | 32% | 0.3221–0.4286–0.5455 | 0.3–0.4375–0.5652 |
| longest run one way | 2 (low) | 21% | 18% | 16% | 3–3–4 | 3–3–4 |
| chord tones on long notes | inside | 21% | 13% | 34% | 0.5505–0.75–0.931 | 0.5714–0.7407–0.9183 |
| gap quarter | 0.333 (high) | 20% | 12% | 30% | 0.0597–0.15–0.2768 | 0.0476–0.16–0.3125 |
| on downbeat | 0.235 (high) | 20% | 31% | 19% | 0.1371–0.1739–0.2308 | 0.0865–0.1333–0.1905 |
| on beats 2 4 | 0.147 (low) | 12% | 12% | 11% | 0.1515–0.2174–0.2649 | 0.1571–0.2321–0.2903 |

**Section lengths in bars.** Intro 8 · Verse 1 8 · Pre 1 4 · Chorus 1 16 · Verse 2 8 · Pre 2 4 · Chorus 2 16 · Bridge 8 · Solo 16 · Last Chorus 16 · Outro 8 = 112: every section a multiple of four.

**How far the builds followed their targets (224).** Correlation between a build's drawn target and what it reads, and the means: gap eighth r 0.55 (target 0.48, read 0.63); gap quarter r 0.37 (target 0.18, read 0.21); longest over median note r 0.32 (target 2.97, read 3.26); notes per bar r 0.62 (target 3.80, read 4.35); chord tones on beat r 0.41 (target 0.68, read 0.74); chord tones off beat r 0.43 (target 0.61, read 0.64).

## Deaths per gate, with the control

| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |
|---|---|---|---|---|
| rhythm: no placement | 41 | — | 40 | — |
| monotony run (166/196) | 122 | 128 | 122 | 129 |
| join: no held end and breath before the copy (212) | 32 | — | 23 | — |
| realness (Table B) | 9 | — | 17 | — |
| bridge above the verse (208) | 50 | 92 | 52 | 91 |
| join: no held end and breath before the line (212) | 25 | — | 26 | — |
| bridge opening unrelated (208) | 8 | 13 | 10 | 18 |
| spectral (Table B) | 19 | — | 41 | — |
| leaps: tritone or past an octave | 20 | 20 | 27 | 27 |
| cmp (Table B) | 7 | — | 1 | — |
| returns related, on lines (181/219) | 11 | 25 | 27 | 45 |
| key word on a chord tone (134) | 3 | 6 | 3 | 4 |
| surprisal (Table B) | 0 | — | 1 | — |
| align: the words do not fit the tune | 0 | — | 1 | — |
| summit placed (the writer's A; 216) | 0 | — | 0 | — |
| register (133) | 0 | — | 0 | — |
| no tone a tritone from the root (215) | 0 | — | 0 | — |
| pitch band (153/182) | 0 | 1 | 0 | 1 |
| rhythm band (163) | 0 | — | 0 | — |
| pushed notes (159) | 0 | — | 0 | — |
| density (159) | 0 | — | 0 | — |
| sequence legs (148) | 0 | — | 0 | — |
| note lengths <= 5 per 8 bars (206) | 0 | — | 0 | — |
| **Survivors** | **153 of 500** | | **109 of 500** | |

## The paper's tests

| Fix | Test | Song 37 |
|---|---|---|
| 212 | with 206 on, join deaths under one build in ten; survivors near the control's share | 57 join deaths (11.4%; song 36 v3: 47%); survivors 153, the control 109: **fails narrowly** (finding 229) |
| 213 | the intake asks; builds repeat the opening unit at once in 15–30% of verse and chorus windows; nothing gates the pick | asked at question 10; 28% of windows across builds; the pick 25%: passes |
| 214 | builds' medians within three points of 69% and 62%; 198 still passes | 74% and 65%: on the beat **5 points high**; intervals 28.7% / 43.5% / 1.8% (repeat, step, past a fifth; the drawn targets average 27.3 / 44.2 / 1.8) |
| 215 | no survivor has such a note on a beat or held a quarter or longer | none in the 40 kept survivors; the gate killed none: passes |
| 216 | every summit lands on a beat over a chord that holds it | bar 27 beat 1 over D; bar 35 beat 1 over D; bar 55 beat 1 over D; bar 63 beat 1 over D; bar 95 beat 1 over D: passes |
| 217 | every return of the hook lands on its own chords; every chorus's last line on the tonic | the hook returns on A–E each time; all six chorus endings on A over A: passes |
| 218 | line ends use three held lengths; eighth-note gaps inside 27–62%; the longest note over the median varies across builds between 2 and 4 | line ends: 24 twelfths ×14, 18 twelfths ×17, 12 twelfths ×8; eighth gaps 47% · 63% · 78% (median **above** the band: finding 227); longest over median 1.5 · 3 · 4: varies |
| 219 | no build dies at 181 where its construction was used | 11 died, all on contour, verse lines 2 and 3 returning line 1 with different syllable counts: **fails** (finding 230) |
| 220 | every section a multiple of four bars; the bar-window return share at or above 31%; a designed three-bar line prints both readings | all multiples of four; returns third in 39% of windows across builds (song 36 v3: 1%), the pick 75%; no three-bar line: passes |
| 221 | 210 computed on 46 measures from the file, the chart range beside it | yes (46 measures, file 1a2af952c43c3eb7…) |
| 222 | the spread printed; the pick inside the chart's middle half, or the report says not | the pick 2.14, **just above** 2.12 (not inside) |
| 223 | 194's four words pass | 'someday' ['stressed', 'weak'], 'somewhere' ['stressed', 'weak'], 'July' ['weak', 'stressed'], 'radio' ['stressed', 'weak', 'weak'], 'microwave' ['stressed', 'weak', 'weak']: passes |
| 224 | targets drawn and recorded; the builds' median distance inside 0.133–0.228; fewer than one build in ten too central | drawn and recorded for all 500 builds; median 0.089; 45% too central (control 62%): **fails** (finding 225) |

## Which fixes ran

| Fix | Ran? | How |
|---|---|---|
| 224 | yes | targets from the chart's middle halves, recorded per build; control at the medians |
| 212, 214, 215, 216, 217, 218, 219, 223 | yes | as above |
| 213, 220, 202, 208 | yes | at intake (questions 8, 10, 11, 13) |
| 194–203, 205, 206 | yes | as amended by v96 (205's plans; 206 at most five lengths, gated) |
| 209 | yes | the instrumental hook and the solo (below) |
| 210, 211, 221 | yes | the distance on 46 measures; the composite the rank of record |
| 222 | yes | a reading |
| 181, 182 and earlier | yes | construction and gates as before |
| 192 | not applicable | a band song (triads over a root bass) |

**The instrumental hook (209).** 2506 distinct one-bar figures drawn from the pop rhythm table; 214 passed the lead gates (rhythm in the pop band; chord tones on the beats 60% or more; no semitone against a held sung note; nothing under A4; no tritone or flat ninth against a root). Deaths: below A4 (the voice's top is F#4) 1008; a tritone or flat ninth against the root 492; a semitone against a held sung note 318; rhythm band (164 via 163) 300; chord tones on the beats under 0.6 97; no contour of its own (no turn) 67; related to the vocal hook (27.31) 10. The pick: onsets (6, 12, 18, 30) in twelfths (A4 E5 B4 A4 over A); chord tones on the beat 100%; unrelated to the vocal hook (onsets 0.17, contour 0.79). It plays in 26 slots: the intro, the holds after chorus lines, the outro. **The solo:** 16 bars, the hook, its answer a third higher, a walked line, the hook landing on A; chord tones on the beats 79%, no tritone against a root, rhythm 1.92 bits (inside the pop band), largest leap 11 semitones; the first draw passed. No corpus on file separates instrumental figures from the voice, so 209 has no kept figure behind it.

**The demo.** Voice +6.1 dB over the band. Energy (9.12): Intro 0.65, Verse 1 0.58, Pre 1 0.79, Chorus 1 0.80, Verse 2 0.50, Pre 2 0.77, Chorus 2 0.80, Bridge 0.81, Solo 0.82, Last Chorus 0.86, Outro 0.81. Each chorus above its verse; the last chorus the top (the solo's first eight bars were thinned, hats for the ride and the organ out, so the solo builds into it).

**Documents.** The demo (MP3, General MIDI, GarageBand MIDI), the lead sheet, the parts, the number chart and the songbook were written from the record; every staff reads back against it, and 47 of 47 consistency checks pass (consistency_p37.py).

**Findings.** 225–232, on the new fix list (after v96).
