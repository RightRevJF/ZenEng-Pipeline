# ZenEng fix list after v103

*Songs 38 and 39 · fixes 257–273 · with the runs, the deaths per gate, which fixes ran, and the paper's tests*

v103's version row (v137, Window 123) ends at fix 256, checked before numbering. This list starts at 257 and covers every song since v103: two, song 38, *Stay Tuned*, and song 39, *Fixed by Fall*. It replaces the list for song 38 alone (257–268); those fixes are carried here unchanged, and song 39 adds 269–273 and new evidence for five of them. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

The brief: two songs under v103, each idea worked out with the writer before the engine. Song 38 set out to skewer the partisan political class and became a song about cable news (the narrator was a cameraman); song 39 went back to the political class itself, both sides, with an all-seeing narrator. No list of report items came with either, so the reports follow the paper's own tests for 225–256 and the band's 233–238. The tables were read, not refitted; the judges were checked against song 37's pick before use.

## Songs since v103

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 38 | Stay Tuned | Rock (Who-style) under v103: the judges, the floor and the shortlist for the first time, with 225–251 in a song for the first time. A cable-news cameraman; the chorus the network's voice; the band stops for 'Turn it off.' Male high baritone C♯3–A4; ♩ = 132, A major; era CLASSIC (242); reciting in the verses (225, after Q14). 114 bars, 3:27. 3000 builds. | 257–268 |
| 39 | Fixed by Fall | Rock with a swagger under v103, no era: a shuffle in the verses, a straight rally march in the choruses (236's feel change by design). An all-seeing narrator cuts between rooms where both sides take the same money; the chorus is their campaign jingle sung back; the last chorus is one singer on two tracks, ending in unison. One gritty baritone A2–E4; ♩ = 108, E major; off-beat verses and chord-bound choruses (225, split by section); summit E4 on 'Vote' (244). 90 bars, 3:20. 500 builds. | 269–273 |

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

### 269. A chosen character in a section full of designed notes is not reached

**Problem:** the writer chose chord-bound for the chorus (225), but the chorus's designed notes (the summit on 'Vote', the line said twice a step down, and the copies of both) leave the walk only half the section to aim.

**Evidence:** the builds' chorus median on chord-bound −0.19 (5th–95th −1.06 to 0.88) against the chosen 1.4–2.1; the control −0.09; the chord-tones-on-the-beat aim in the chorus followed at r = 0.20. The verse's off-beat choice, in a section with nothing designed, read 1.60 (in range).

**Fix:** when a section's character is chosen, the walk aims the section's whole window, designed notes included (it compensates on the free notes), and the report says how many notes were free.

**Check:** the builds' median on a chosen axis inside 1.4–2.1 whatever the design.

### 270. 'Said twice' made the runs

**Problem:** the second chorus line was built as the first a whole step down, with each note re-chosen to a chord tone where it fell on a beat or was held; several notes landed on the same chord tone.

**Evidence:** in a 500-build run before a repair step was added, the twice line held 108 of the runs of four in builds the run clause killed, and the chorus's copies in chorus 2 and the last chorus 225 more; with the repair, run deaths fell to 12.2% (246's test: under 10%).

**Fix:** say it twice by moving the line bodily (27.44's commonest move) and correct only notes that clash (215), not every strong note to a chord tone.

**Check:** run deaths under one build in ten with a twice line in the plan.

### 271. A shuffle has no place on the grid or in the tables

**Problem:** the writer chose a shuffle (eighths swung) for the verses and a straight march for the choruses. The engine writes and reads straight eighths; the rhythm tables, the 231 landings and the judges' measures do not know a shuffle; the swing was added only in the demo.

**Evidence:** every reading in this song is on the written straight grid; no kept corpus file marks which songs swing.

**Fix:** the intake records swing per section; the class tables are split or flagged by swing; readings on swung sections are taken on the written grid and said so.

**Check:** the report states the feel of each section beside its readings.

### 272. Evidence for 258 from a song with no era

**Problem:** none new; a record.

**Evidence:** with no era set, 500 builds left 58 survivors (11.6%; control 113, 22.6%), where song 38 with CLASSIC needed 3000 builds for 43. The largest killers were the return gate, the run clause and the bridge register, not a band.

**Fix:** as 258.

**Check:** as 258.

### 273. Song 39 against 261–265

**Problem:** none new; the earlier findings read in a second song.

**Evidence:** 261: 86 of 500 died at 181 where the return was built (control 104), again. 262: verse 2 shared a median 23.5% of verse 1's bar rhythms (47% of builds in range): nearer, still short. 263: pickups 54%, landings on 1 or 3 40.5%, off the beat 35%, all inside 231's ranges, so song 38's excess came from that song (its fixed chant pickups), not from the walk in general; 263's fix stands as a calibration, not a rule. 265: onsets on beat 3 again not followed in the verse (r = 0.03; chorus 0.37); turns followed this time (0.56, 0.33).

**Fix:** 261 and 262 as written; 263 narrowed to calibration; 265 keeps beat 3 with 231.

**Check:** as each.

## Order of work

1. 258 and 259 (the era as targets, gated at the 10th–90th; target windows from the era's own kept windows): they decide whether an era song can be searched at 500 builds. Song 39, with no era, left 58 survivors at 500 (272).
2. 261 and 270 (the return gate and the run clause): one change to 181 on shared events and one to how a line is said twice; between them they killed 25% of song 39's builds and 19% of song 38's.
3. 264 and 269 (a chosen character reached): a reciting section allows runs of four; a section's whole window aimed, designed notes included.
4. 257 and 271 (the intake): warn when a character and an era leave no kept window; record swing per section and flag the tables.
5. 262 and 263 (the rhythm walk): verse 2's rhythm with verse 1's onsets as a prior; 263 narrowed to calibration (273).
6. 265, 260, 266, 267, 268 (wording, two measures added to the rows).

## Regression line

After these fixes, both songs rerun at PYTHONHASHSEED 0 must reproduce their frozen orders twice: song 38 at seed 20261491 (calibration 20261492), N 3000, song 39 at seed 20261501 (calibration 20261502), N 500. Song 38 must keep the six A4s on 'tuned' over A, the chorus opening unrelated and its floor above the verse, the pick inside CLASSIC's five bands, and lose under one build in five at the era gate (258) and none at 181 where the return was built (261); its verse median on reciting inside 1.4–2.1 (264) and verse 2's shared bar rhythms inside 25–75% (262); 59 of 59 consistency checks. Song 39 must keep the four E4s on 'Vote' over E, the twice line on D over D and the tag G♯3–F♯3–E3; lose under one build in ten at the run clause (270) and none at 181 where built (261); put the chorus median on chord-bound inside 1.4–2.1 (269); state each section's feel in the report (271); 56 of 56 consistency checks. The controls (243 off) stay as the comparison. The judges' claim stays what 27.47 says: like a kept song in content and order, not good.

## Reports

### Song 38, report 1: the runs and the pick

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

### Song 38, report 2: deaths per gate, with the control

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

### Song 38, report 3: which fixes ran, and the paper's tests

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

### Song 39, report 1: the runs and the pick

**The search.** N 500, seed 20261501, calibration seed 20261502, PYTHONHASHSEED 0, code 8397ca3ba76b, Python 3.13.18, numpy 2.5.3; the same tables as song 38. 58 survivors (11.6%), frozen order 07c5a8ad998f.

**The control.** Same seed and N, 243 off: 113 survivors (22.6%), order 05fbf6379223; its shortlist pick 042df5d35c25 (composite 0.828, combined 3.41).

| Build | Composite | Content | Order | Combined |
|---|---|---|---|---|
| composite first: 03b97e94f12c | 0.795 | -0.593 | 2.503 | 0.955 |
| shortlist pick: f69bed50793e | 0.787 | 1.981 | 2.986 | 2.484 |
| judge first: e68750259d59 | 0.586 | 3.367 | 4.854 | 4.110 |

The shortlist is 29 of 58. The composite's first build is 54th of 58 by the judge (its content score −0.59), so 255 changed the pick again. The record is built from f69bed50793e with no hand edits.

| Reading | Pick | Builds 5th · median · 95th | Kept |
|---|---|---|---|
| Content judge (log-odds) | 1.98 | -1.421 · 1.32 · 4.829 | −1.084 · 4.565 · 15.59 |
| Order judge (log-odds) | 2.99 | 1.697 · 3.155 · 4.659 | −1.53 · 1.58 · 5.02 |
| Combined | 2.48 | 0.777 · 2.204 · 4.052 | −0.06 · 3.11 · 9.70 |
| Builds called shuffled by the order judge | — | 0.2% | — |
| Measures outside both kept middle halves (of 56) | 10 | 10.85 · 14.5 · 18.5 | 16 (8–26) |
| Distance from the centre | 0.124 | 0.118 · 0.184 · 0.296 | — |
| Off-beat, verse window (sd) | 1.38 | 0.978 · 1.599 · 2.05 | chosen 1.4–2.1 |
| Chord-bound, chorus window (sd) | 0.49 | -1.062 · -0.189 · 0.876 | chosen 1.4–2.1 |

The measures that most give the builds away: distinct pitches (-1.777), on offbeat eighth (-1.316), gap eighth (-0.734), gap quarter (-0.727), gap sixteenth (-0.483) (song 38's five, the same five in a different order). The pick's order measures: verse parallel 0.345, pitch parallel 0.74, smooth barline -0.387, thin 48 0.667; chorus parallel 0.164, pitch parallel -0.161, smooth barline -0.472, thin 48 1.167.

### Song 39, report 2: deaths per gate, with the control

| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |
|---|---|---|---|---|
| returns related, on shared events (181/219/248) | 86 | 113 | 104 | 135 |
| monotony run (166/196) | 61 | 68 | 39 | 40 |
| bridge above the verse, under the summit (208) | 55 | 118 | 57 | 114 |
| leaps: tritone or past an octave | 42 | 42 | 23 | 23 |
| join: no held end and breath before the copy (212) | 41 | — | 30 | — |
| surprisal (Table B) | 27 | — | 13 | — |
| chorus at or above the verse, floor lifted (227) | 25 | 45 | 7 | 14 |
| return: first or top note not kept (239) | 21 | — | 18 | — |
| bridge opening unrelated (208) | 16 | 36 | 11 | 27 |
| spectral (Table B) | 15 | — | 6 | — |
| cmp (Table B) | 13 | — | 21 | — |
| chorus opening another tune (227) | 12 | 19 | 19 | 29 |
| realness (Table B) | 12 | — | 13 | — |
| summit placed (the writer's A; 216, 244) | 8 | 13 | 16 | 17 |
| memory (Table B) | 3 | — | 4 | — |
| key word on a chord tone (134) | 2 | 5 | 2 | 6 |
| align: the words do not fit the returning tune | 2 | — | 0 | — |
| walk: no note | 1 | — | 4 | — |
| Survivors | 58 of 500 | | 113 of 500 | |

**The instrumental figure (235).** The intro tune (6, 12, 18, 30) / steps (0, 2, -2, 2) (E4 G♯4 C♯4 G♯4 over E), unrelated to every sung line; it plays the intro and the outro. Fills: 9 gaps of two beats or more, 2 filled, 2 left open, 5 with no room (266). The solo: 8 bars, chord tones on the beat 60%, no tritone against a root, largest leap 12. No countermelody (Q11).

**The band.** Bass: the root on beat 1 of every bar it plays; root share 49% (kept 43–73%); kicks with a bass note 97%. Drums: snare on 2 and 4 in 90% of bars; kick on 1 in every bar; 2.71 kicks a bar; three kick-and-snare bars cover 96%; 8 fills in 90 bars; the feel changes at each chorus by design. Chordal part (piano): 3.65 strikes a bar, MIDI 56–66, every strike with a bass note (267). Parts by section: Intro 3, Verse 1 5, Chorus 1 5, Verse 2 6, Chorus 2 6, Bridge 5, Solo 4, Last Chorus 6, Outro 5.

### Song 39, report 3: which fixes ran, and the paper's tests

| Fix | Song 39 against the test | Held? |
|---|---|---|
| 225 | verse off-beat median 1.599 (control 1.767); chorus chord-bound median -0.189 (control -0.086) | verse yes; chorus no (269) |
| 227 | gates held; chorus bar rhythms heard in the verse: pick 25%, builds median 12% | yes |
| 228 | verse 2 shares 24% of verse 1's bar rhythms at the median, in range in 47%; last chorus +2 bars (the tag) | no (273, 262) |
| 229 | bridge 3.144 bits vs chorus 2.769; off-beat bridge +0.35 vs verse +1.38 | printed |
| 230 | every line 4–8 syllables in 2 bars; the last chorus 18 (268) | yes, with 268 |
| 231 | off the beat 35%, on 1 or 3 40%, pickups 54% | yes (273) |
| 232 | 'fixed' on beats [1, 3], held a beat against a half-beat median; 4 soundings, first bar 27 | yes |
| 239–240 | tonic endings, returns 23% vs sources 24% | yes |
| 242 | not set (Q5) | — |
| 243 | in range on 4 of 16 aimed measures; three pools (10, 22, 314 windows) | partly |
| 244 | the summit in the chorus window's first quarter (the writer's A) | yes |
| 246 | added notes too few to read (one leap, one repeat); run deaths 12.2% | no (270) |
| 247 | join deaths 8.2% | yes |
| 248 | 86 of 500 died at 181 where built | no (273, 261) |
| 250 | pick 10; builds 10.85–14.5–18.5 | yes |
| 251 | followed: tonic, third, fifth, beats 2 and 4, turns, repeat, step, eighth gaps; not followed: verse beat 3 (0.03), chorus chord tones (0.20) | mostly (269, 273) |
| 252–255 | pick combined 2.48; 0 deaths at the floor; the composite's first was 54th of 58 by the judge | yes |

What the tables did not carry: notes a bar and onsets on the downbeat in the training rows (260); a year for each kept window (259); which kept songs swing (271).

## Blind-pick tally

| Slot | Picks |
|---|---|
| Annotated top | 11 |
| Remembered top | 8 |
| Middle | 7 |
| Refrain | 1 |
| Songs picked | 27 |

Song 38: the Annotated top, "they toast the ratings, glass to glass" (over "Stay tuned, stay mad", the Remembered top, and "stay tuned, stay scared", the Middle).

Song 39: the Annotated top, "Vote for us, we'll fix it all" (over "we've got it fixed by fall", the Remembered top, and "same shrimp, same band, same donor's hand", the Middle: top quartile under both regimes). The writer picked the line where the two candidates first become 'us'. The Annotated top has now been picked in three songs running.
