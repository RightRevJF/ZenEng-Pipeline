# ZenEng fix list after v103

*Song 38 · fixes 257–268 · with the runs, the deaths per gate, which fixes ran, and the paper's tests*

v103's version row (v137, Window 123) ends at fix 256, checked before numbering. This list starts at 257 and covers every song since v103: one, song 38, *Stay Tuned*. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

The brief: a new song under v103, the idea worked out with the writer before the engine (it was rough and not yet embodied). No list of report items came with it this time, so the reports below follow the paper's own tests for 225–256 and the band's 233–238. The tables were read, not refitted, including the new zeneng_v103_selector.json; the judges were checked against song 37's pick before use (Verse 1 content 0.586, order 3.059; Chorus 1 −1.027, 5.221, as the file gives).

## Songs since v103

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 38 | Stay Tuned | The rock class (Who-style) under v103: the judges, the floor and the shortlist (252–255) for the first time, with 225–251 run in a song for the first time too. A cable-news cameraman shows both sides of the shouting class as one act; the chorus is the network's voice, and in the last chorus he cuts the cameras and says turn it off. Male high baritone C♯3–A4; 4/4 at ♩ = 132, A major; era CLASSIC (242); reciting chosen as the song's character (225), then confined to the verses when it proved incompatible with CLASSIC (Q14). 114 bars, 3:27, the last chorus two bars longer (228). Summit A4 on 'tuned', the chorus window's first beat, six times (244). Four on the floor in the choruses (236), countermelody in the last chorus (235). A control with 243 off. | 257–268 |

## The fixes

### 257. An axis end the era cannot hold

**Problem:** the writer chose reciting (225) and CLASSIC (242); no kept window does both.

**Evidence:** of 314 kept chart windows, the 20 at 1.4–2.1 on reciting repeat 52% of moves (none at or under 33%) and read 2.41 bits a note; CLASSIC's bands are 16–33% and 2.67–3.19. The writer settled it at Q14 (recite in the verses only).

**Fix:** when a chosen axis end and the era's bands leave no kept window between them, the intake says so at the character question and offers the split by section.

**Check:** the conflict is printed at intake with the count of kept windows that meet both.

### 258. The era gate kills half the run

**Problem:** 242 sets five bands at the era's middle halves; as gates they kill most builds.

**Evidence:** 1554 of 3000 main builds (52%) died there; survival fell to 1.4% (song 37: 31%); the run went to 3000 builds to leave 43 survivors. Only 1 of 314 kept windows sits inside all four of the bands the rows carry; a middle half is passed by half of kept songs by definition.

**Fix:** read the era's middle halves as targets (243's draw) and gate at the era's 10th–90th.

**Check:** under an era, deaths at the era gate under one build in five; the pick inside the middle halves on at least three of five.

### 259. 243's draw and the era do not talk

**Problem:** targets drawn from any kept window pull builds toward the modern surface that CLASSIC's gate then kills.

**Evidence:** the chorus and bridge pool was cut here to the 48 kept windows inside at least three of the four era bands the rows carry (a choice, recorded). A 300-build trial before and after the cut went from 7 to 13 passing the gates, but the chant's pickup design changed in the same step, so the cut's own effect was not measured.

**Fix:** under an era, draw the target window from that era's kept windows (the rows need a year).

**Check:** the drawn windows' era is printed; deaths at the era gate fall.

### 260. Two aimed measures are missing from the rows

**Problem:** 243 draws targets from a whole kept window, but the v103 training rows lack notes a bar (aimed since 224) and the onsets on the downbeat (251).

**Evidence:** the rows carry 50 measures; notes a bar was read from the chart median for every build.

**Fix:** add notes_per_bar and on_downbeat to the rows.

**Check:** every aimed measure drawn from the window.

### 261. 248's test fails: returns die at 181 where the construction was used

**Problem:** 239's change in the last quarter and the reciting verse make built returns read unrelated on the shared events.

**Evidence:** 317 of 3000 builds died at 181/219/248 (control 333); the reading is r < 0.6 on the pitch series of the shared events, and a reciting line whose shared notes are one pitch reads r = 0 against a moving source.

**Fix:** 181 on shared events: related when the first three-quarters of the shared events keep their pitches, or both series are near-constant; the late change keeps steps.

**Check:** no build dies at 181 where its return was built by 239.

### 262. Verse 2 sung again shares too little rhythm with verse 1

**Problem:** 228 asks for a quarter to three-quarters of verse 1's bar rhythms; refitting each line from its own syllables gives far fewer.

**Evidence:** builds 0%–12.5%–37.5% (5th–median–95th); in range in 30%; the pick 0%.

**Fix:** draw verse 2's line rhythm with verse 1's onsets as a prior (the rhythm walk tilted toward the source's places, the kept 40% at the median).

**Check:** across builds the median share inside 25–75%.

### 263. Too many pickups, too many landings on 1 and 3

**Problem:** 231 asks for pickups on 40–70% of lines and last stresses on 1 or 3 in 35–55%.

**Evidence:** builds 80.5% pickups (63–90%) and 58.5% on 1 or 3; the off-beat share is in range (27%). The first syllable's weight before the bar (1.0 against 0.35 on it) and the two-bar lines with holds push both.

**Fix:** calibrate the pickup weight on the song (249) to 55%, and read 231's landing on the drawn target, not the walk's result.

**Check:** both inside their ranges across builds.

### 264. A reciting verse meets the run clause

**Problem:** the verse aimed at kept reciting windows reads less reciting than its targets.

**Evidence:** builds' median 1.15 on reciting (test: 1.4–2.1); the control, aimed at the reciting pool's medians, 1.43; verse chord tones on the beat read 0.57 against targets of 0.72 (249: within 3 points). The walk forbids a fourth repeat and 166/196 gates runs over three, while kept reciting windows repeat on 52% of moves.

**Fix:** when reciting is chosen, allow runs of four in that section and recalibrate the chord-tone knob on repeated notes.

**Check:** builds' median on reciting inside 1.4–2.1; chord tones within 3 points.

### 265. Two of 251's aims are not followed

**Problem:** turns per move and onsets on beat 3 do not track their targets.

**Evidence:** target–reading correlation: turns 0.17 (verse) and 0.12 (chorus); beat 3 0.23 and 0.19. The tonic, third and fifth (0.64–0.79), beats 2 and 4 (0.41, 0.51), repeats, steps, chord tones and eighth gaps are followed.

**Fix:** drop turns as an aim (the walk's direction is already set by DESC and 197) or carry direction memory; let 231's landing draw take beat 3.

**Check:** r ≥ 0.3 on every aim kept.

### 266. Few gaps can take a fill

**Problem:** 235's fill (start 0.47–0.96 beats after the voice, 1.85–2.58 beats long, ending before the voice) needs about 2.75 beats; two-bar lines with held ends leave 2.

**Evidence:** 18 gaps of two beats or more; 13 had no room; 3 filled (70% intended).

**Fix:** the 70% counted on gaps of 2.75 beats or more, or a one-and-a-half-beat fill allowed in a two-beat gap.

**Check:** the report prints fills against the eligible gaps.

### 267. The chordal part always falls with an eighth-note bass

**Problem:** 237's test caps strikes with a bass note at nine in ten.

**Evidence:** the bass cell is eighths, so every organ strike (on the beat or a held chord) falls with a bass note: 100%.

**Fix:** read 237's share against bass notes on the beat, or exempt an eighth-note bass cell.

**Check:** stated with the bass cell beside it.

### 268. 228's extension against 230's multiple of four

**Problem:** 230 says every section's slots sum to a multiple of four; 228 makes the last chorus two bars longer by default.

**Evidence:** the last chorus is 18 bars.

**Fix:** 230 names 228's extension as the exception.

**Check:** the lyric check prints the extension as designed.

## Order of work

1. 258 and 259 (the era as targets, gated at the 10th–90th; target windows drawn from the era's own kept windows): together they decide whether an era song can be searched at 500 builds.
2. 257 (the intake warns when a chosen character and the era leave no kept window): a question's wording and a count.
3. 264 (a reciting section allows runs of four; the chord-tone knob recalibrated) and 261 (181 on shared events accepts a late change and near-constant lines): one change to the run clause and one to the return gate.
4. 262 (verse 2's rhythm with verse 1's onsets as a prior) and 263 (the pickup weight calibrated to 55%): the rhythm walk.
5. 265 (drop the turns aim; beat 3 left to 231), 260 (two measures added to the rows), 266, 267 and 268 (wording of 235, 237 and 230's tests).

## Regression line

After these fixes, song 38 rerun at N 3000, seed 20261491 (calibration seed 20261492), PYTHONHASHSEED 0 must: reproduce its frozen order twice; keep the six A4s on 'tuned', beat 1, over A; keep the chorus opening unrelated to the verse with its floor above; keep the pick inside CLASSIC's five bands; lose under one build in five at the era gate (258) and none at 181 where the return was built (261); put the builds' verse median on reciting inside 1.4–2.1 (264) and verse 2's shared bar rhythms inside 25–75% (262); bring pickups and landings on 1 and 3 inside 231's ranges (263); and pass 59 of 59 consistency checks. With 258 in place the same search should leave more than 43 survivors at 3000 builds (and enough at 500 for a shortlist). The control (243 off) stays as the comparison. The judges' claim stays what 27.47 says: like a kept song in content and order, not good.

## Report 1: the runs and the pick

**The search.** N 3000, seed 20261491, calibration seed 20261492, PYTHONHASHSEED 0, code 072042b9fa72, Python 3.13.18, numpy 2.5.3; tables v88 561355b1…, v96 1a2af952…, v97 00e65c5b…, v100 cfe324a5…, v101 0224a917…, v102 caaa40ec…, v103 aefba371…. 43 survivors (1.4%), frozen order 6c9159e817fe. The run is 3000 builds: at 500 it left 10 survivors, too few for a shortlist (258).

**The control.** Same seed and N, 243 off (each build aimed at its pool's medians): 118 survivors (3.9%), order 2e84eb46c145; its shortlist pick 3760e62261fd (composite 0.801, combined 3.69).

**The three builds of 255.**

| Build | Composite | Content | Order | Combined |
|---|---|---|---|---|
| composite first: fd9ca29c0cc2 | 0.813 | 2.857 | 1.290 | 2.074 |
| shortlist pick: cee0932cdefd | 0.772 | 2.061 | 3.162 | 2.611 |
| judge first: 2aff01296a68 | 0.585 | 6.556 | 4.375 | 5.466 |

The shortlist is 21 of 43. The composite's first build is 23rd of 43 by the judge, outside the upper half, so 255 changed the pick. The record is built from cee0932cdefd with no hand edits.

| Reading | Pick | Builds 5th · median · 95th | Kept |
|---|---|---|---|
| Content judge (log-odds) | 2.06 | -0.945 · 1.611 · 5.023 | -1.084 · 4.565 · 15.59 |
| Order judge (log-odds) | 3.16 | 1.064 · 2.782 · 4.556 | −1.53 · 1.58 · 5.02 |
| Combined | 2.61 | 0.797 · 2.211 · 4.073 | −0.06 · 3.11 · 9.70 |
| Builds called shuffled by the order judge | — | 0.3% | — |
| Measures outside both kept middle halves (of 56) | 10.5 | 11.5 · 15.5 · 19 | 16 (8–26) |
| Distance from the centre (verse and chorus windows) | 0.086 | 0.11 · 0.168 · 0.245 | — |
| Reciting, verse window (sd) | 1.48 | 0.27 · 1.153 · 2.072 | chosen 1.4–2.1 |

The measures that most give the builds away (weight × z, averaged): distinct_pitches (-0.825), on_offbeat_eighth (-0.776), gap_eighth (-0.485), gap_sixteenth (-0.483), gap_quarter (-0.382). Kept training rows sit above this song's builds in 77% of pairs (the rows are the judge's training data, so this flatters it). The pick's order measures: verse parallel 0.273, pitch_parallel 0.142, smooth_barline -0.962, thin_48 3.667; chorus parallel 0.241, pitch_parallel -0.1, smooth_barline 1.495, thin_48 1.167 (kept middle halves 0.04–0.23, 0.03–0.37, −1.65 to −0.17, −0.2 to 2.5); the chorus's smooth bar line is outside because the designed chant leaps to A4 inside the bar.

**The era (242), the pick:** notes_per_bar 3.375, range 12.0, repeat 0.182, distinct_durations 5.0, pitch_bits 2.971 (median of Verse 1, Chorus 1 and the Bridge, each inside CLASSIC's middle half). By window: Verse 1 notes_per_bar 4.25, range 10.0, repeat 0.485, distinct_durations 4.0, pitch_bits 2.501; Chorus 1 notes_per_bar 2.875, range 12.0, repeat 0.182, distinct_durations 5.0, pitch_bits 2.971; Bridge notes_per_bar 3.375, range 12.0, repeat 0.115, distinct_durations 5.0, pitch_bits 3.004.

## Report 2: deaths per gate, with the control

| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |
|---|---|---|---|---|
| era CLASSIC bands (242) | 1554 | 2281 | 1211 | 1734 |
| returns related, on shared events (181/219/248) | 317 | 382 | 333 | 379 |
| spectral (Table B) | 278 | — | 590 | — |
| monotony run (166/196) | 261 | 273 | 185 | 193 |
| leaps: tritone or past an octave | 153 | 153 | 135 | 135 |
| bridge opening unrelated (208) | 74 | 107 | 102 | 126 |
| return: first or top note not kept (239) | 65 | — | 68 | — |
| join: no held end and breath before the line (212) | 57 | — | 56 | — |
| join: no held end and breath before the copy (212) | 55 | — | 34 | — |
| chorus at or above the verse, floor lifted (227) | 45 | 56 | 58 | 79 |
| bridge above the verse, under the summit (208) | 44 | 72 | 30 | 55 |
| memory (Table B) | 19 | — | 35 | — |
| align: the words do not fit the returning tune | 10 | — | 13 | — |
| cmp (Table B) | 8 | — | 12 | — |
| summit placed (the writer's A; 216, 244) | 7 | 7 | 7 | 8 |
| key word on a chord tone (134) | 5 | 54 | 10 | 33 |
| realness (Table B) | 4 | — | 1 | — |
| the judge's floor (254) | 1 | 8 | 0 | 1 |
| surprisal (Table B) | 0 | — | 2 | — |
| register (133), chorus opening another tune (227), no tone a tritone from the root (215), rhythm band (163), pushed notes (159), density (159), sequence legs (148), note lengths <= 5 per 8 bars (206) | 0 | 0 | 0 | 0 |
| Survivors | 43 of 3000 | | 118 of 3000 | |

**The instrumental figure (235).** 3,782 distinct one-bar intro tunes drawn; 497 passed (816 died as related to a sung line). The pick: A4 E4 D4 E4 over A, on the 'and' of 1, beat 2, its 'and' and the 'and' of 3; it plays intro bars 5–8 and breakdown bars 85–88. Fills: 18 gaps of two beats or more, 3 filled, 2 left open, 13 with no room (266). The solo: 8 bars, chord tones on the beat 69%, no tritone against a root, largest leap 9. The countermelody: 3 of 16 struck-together notes at unison or octave (19%).

**The band.** Bass: the root on beat 1 of every bar it plays, root share 65% (kept 43–73%), kicks with a bass note 98%. Drums: in at bar 5; snare on 2 and 4 in 84% of drum bars (the breakdown and fill bars without); kick on 1 in every bar; 3.12 kicks a bar; three kick-and-snare bars cover 81%; 11 fills in 101 bars. Chordal part: 2.97 strikes a bar, MIDI 57–68, every strike with a bass note (267). Parts by section: Intro 4, Verse 1 5, Pre 1 6, Chorus 1 7, Verse 2 6, Pre 2 7, Chorus 2 7, Bridge 6, Solo 6, Breakdown 7, Last Chorus 8, Outro 4.

## Report 3: which fixes ran, and the paper's tests

| Fix | Ran? | Song 38 against the test | Held? |
|---|---|---|---|
| 225 | yes, at intake (reciting; Q14 confined it to the verses) | builds' verse median on reciting 1.153 (5th–95th 0.27–2.072); control 1.43; pick 1.48 | no (264) |
| 226 | yes (through 243's whole-window draw) | unchosen axes: medians within 1 sd on 15 of 15; spread at or above the control's on 14 of 15 | yes |
| 227 | yes | gates held; chorus bar rhythms heard in the verse: pick 29%, builds median 12% (kept 12%) | yes |
| 228 | yes | verse 2 shares 12% of verse 1's bar rhythms at the median, in range in 30%; last chorus +2 bars (the writer's tag); exact bars 42% vs chart 38% | no (262) |
| 229 | yes (printed) | bridge 2.974 bits vs chorus 3.009; off-beat axis bridge +0.51 vs verse +0.83 | printed |
| 230 | yes, at the lyric | every line 3–8 syllables in 2 bars; sections multiples of four but the last chorus's 18 | yes, with 268 |
| 231 | yes | builds: off the beat 27%, on 1 or 3 58%, pickups 80% | off-beat yes; the other two high (263) |
| 232 | yes (designed) | stress on beat 1, held 3 beats against a half-beat median; 9 soundings, first at bar 21 | yes |
| 233–238 | yes (the band) | Report 2's band paragraph | yes, but 237's share (267) |
| 239–240 | yes | pick's returns: pitch 2, exact 16, both 2, rhythm 1, sung again 6; tonic endings, returns 13% vs sources 14% | yes |
| 241 | — | a record | — |
| 242 | yes (CLASSIC) | the pick inside all five; 1554 of 3000 builds died at the gate (52%) | yes, at a cost (258) |
| 243 | yes | windows recorded; 40–60% outside the chart middle half on 8 of 16 aimed measures; the aimed measures carry 37% of a kept window's distance | partly (259, 260) |
| 244 | yes, at intake | both figures shown; the writer put the summit in the first quarter | yes |
| 245 | yes, at the lyric | notes a bar the lines need: verse 3.75, pre 4.0, chorus 2.88, bridge 3.38; none dense | yes |
| 246 | yes | added notes repeat 29%; run deaths 8.7% | yes |
| 247 | yes | join deaths 3.7% | yes |
| 248 | yes | 317 of 3000 died at 181 where the return was built | no (261) |
| 249 | yes | 3 rounds × 30 builds, seed 20261492; chord tones: chorus on the beat 0.692 vs 0.665, off 0.636 vs 0.674; verse 0.571 vs 0.718 and 0.571 vs 0.724 | chorus nearly; verse no (264) |
| 250 | yes | pick 10.5; builds 11.5–15.5–19.0 | yes |
| 251 | yes | followed (r ≥ 0.3): tonic, third, fifth, beats 2 and 4, repeat, step, chord tones, eighth gaps; not followed: turns 0.17/0.12, beat 3 0.23/0.19; low point not aimed | partly (265) |
| 252 | yes (file weights) | above, Report 1 | printed; no refit here |
| 253 | yes | above, Report 1 | printed |
| 254 | yes | 1 death at the floor (8 would fail) | yes |
| 255 | yes | the composite's first was 23rd of 43 by the judge; the pick changed | yes |
| 256 | — | nothing in 256 used to rank | — |

What the tables did not carry: notes a bar and onsets on the downbeat in the v103 training rows (260); a year for each kept window, so an era's own windows could be drawn (259).

## Blind-pick tally

| Slot | Picks |
|---|---|
| Annotated top | 10 |
| Remembered top | 8 |
| Middle | 7 |
| Refrain | 1 |
| Songs picked | 26 |

Song 38: the Annotated top, "they toast the ratings, glass to glass." The slots were offered in shuffled order: A that line, B "Stay tuned, stay mad" (Remembered top), C "stay tuned, stay scared" (Middle: top quartile under both regimes).
