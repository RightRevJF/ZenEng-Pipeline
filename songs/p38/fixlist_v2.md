# ZenEng fix list after v107

*Song 38 rerun under v107 · fixes 286–295 · with the three runs, the deaths per gate, the tests of 257–285 and the readings the paper did not spell out*

v107's last fix is 285 (Window 127, version row v141). This list starts at 286 and covers every song since v107: one, a regression run of song 38, *Stay Tuned*, rerun under v107 with the locked lyric, every intake answer, the form, key, tempo, chords, seed 20261491 and calibration seed 20261492 unchanged, and the judges' weights as fitted through song 37. It is the first song to run fixes 257–280. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

## Songs since v107

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 38 (rerun) | Stay Tuned | v107 on a song already built under v103: Run A the gates only (276–278, 270, 264, 267), Run B full v107 (257–274, 281, 282, 285 added), Run C B with 243 off. 3,000 builds each, each run twice. Survivors A 219, B 610, C 702 (v1: 43). Record from Run B's shortlist pick. | 286–295 |

## The fixes

### 286. The spectral reading is now the search's largest killer

**Problem:** with the era gate and the run clause refitted, the Table B spectral band (unaudited, 280) kills half the builds, in every run.

**Evidence:** deaths 1,621 (A), 1,431 (B), 1,589 (C) of 3,000; it would fail 2,258, 1,807 and 1,890 complete builds. Every failure is above the band's 95th percentile (the pitch series too smooth), none below. It was there in v1 too: 77% of v1's 2,813 complete builds with a reading sit above the 95th, hidden because the era gate killed them first. On the 515 POP909 calibration pairs it passes 89.9% alone, and the seven unaudited gates pass 75.7% together, under 275's nine in ten.

**Fix:** the seven join 277's count as soft limits at their calibration 5th or 95th, with hard limits at the 1st or 99th read on the same pairs; the spectral band's reading on a two-section tune (verse and chorus run together) is checked against a kept rock song's before it is used.

**Check:** deaths at the spectral reading under one build in five; the seven's joint pass rate printed with the limits.

### 287. The return gate still kills returns 239 built, through two later steps

**Problem:** 267 reads what 239 builds, but two steps after 239 change a return's early shared notes.

**Evidence:** deaths at 267: 447 (A), 162 (B), 213 (C). In A, 252 of the 497 failing returns differ first on their first shared note: v1's join repair (212) re-walks a line's pickup when the join leaps past an octave or a tritone, returns included. In B, which drops that repair (259), 101 of 169 differ elsewhere before the last quarter and 45 on the note just before it: the repair step that re-walks a leap past a sixth or a tritone re-draws the note before the leap when the leap's own note is kept.

**Fix:** a return built by 239 is exempt from both: a join is mended on the line that is not a return, and a leap a late change makes is undone by drawing that late note again, never an earlier one.

**Check:** no build dies at 267 where 239 built the return.

### 288. The generator still writes the old gates

**Problem:** the gates became limits and aims, but the generator's own tables still hold the builds where the gates did.

**Evidence:** every build in all three runs has at most five note lengths in any eight bars (5th–95th 5 · 5; kept 4 · 6 · 8): the five-length palette written for fix 206 is still offered, though 206 is now a limit at eight. The chorus's top is 10 semitones over the verse's and its median 5 over at the builds' median (kept: 0 and 1 at the median; 9 and 10 at the 95th), from the section registers (the verse capped at B3, the summit A4); 278's aims read 100% because they ask only a direction. The B pick's one band outside CLASSIC's middle half is distinct durations (4.0 against 4.33–6.0), the same palette.

**Fix:** the palette offers up to eight lengths, drawn at kept rates for the class; the section registers are drawn so the chorus-over-verse differences follow the kept distribution, and 278's aims carry the kept band, not only the direction.

**Check:** the most lengths in eight bars spreads 4–8 across builds; the chorus-over-verse medians land inside the kept middle half in half the builds or more.

### 289. The landing draw puts too many last stresses on 1 or 3

**Problem:** 269's second test (last stresses on 1 or 3 in 35–55% of lines) fails with the entry now drawn at 260's rates.

**Evidence:** Run B 48.8 · 63.4 · 80.5% (5th, median, 95th); A 58.5%; lines whose last note falls on a downbeat 46% against the kept 27% (Table DJ). The draw's own shares put b1 and b3 at 46% (chorus) and 40% (verse) before the weak syllables after the last stress are placed. Entry by 260's reading is in range (after the downbeat 39%; kept 33–78%), and the pickups that remain are the designed chant lines and their copies (9 of 41 lines) with verse 2's inherited entries.

**Fix:** refit 231's landing shares on Window 124's line-end positions (last note on beat 1 26%, beat 3 9.5%, off the beat 49%).

**Check:** last stresses on 1 or 3 inside 35–55% across builds; last notes on a downbeat inside the kept 11–43%.

### 290. Turns per move and onsets on beat 3: not followed again

**Problem:** two of 251's aims still do not track their targets.

**Evidence:** correlation of target and reading across Run B's builds: turns per move 0.10 (verse), 0.17 (chorus) (song 38 under v103: 0.17, 0.12; song 39: 0.56, 0.33); onsets on beat 3, now through the landing draw (285): 0.20 and 0.08 (song 38 v103: 0.23, 0.19; song 39: 0.03, 0.37). Gaps of an eighth fell under 0.3 in the verse for the first time (0.26). The landing draw places one syllable a line, too few to move a window's share of beat-3 onsets.

**Fix:** by 285's rule turns stays (song 39 followed it, so it has not failed two songs running); beat 3 has failed in the verse in two songs running (song 39 0.03, this run 0.20) and is dropped as an aim.

**Check:** the report lists each aim's last two readings and the drop.

### 291. The judge reads v107's lines as less like a kept song

**Problem:** the line fixes move every Table DJ reading toward kept songs, while the content judge, fitted through song 37 on the old generator's builds, moves the other way.

**Evidence:** builds' content score at the median: v1 1.61, A 1.51, B 0.66, C 0.61 (kept 4.57); combined 2.21, 2.12, 1.64, 1.66 (kept 3.11). The give-aways that grew are gaps of an eighth (−0.49 in A to −0.88 in B) and distinct pitches (−0.36 to −0.75). In the same builds the arch term, widening, first-note surprise and entry moved inside or toward the kept middle half. The judge's weights were held fixed by the brief so the scores compare; its floor killed 53 in B against 10 in A.

**Fix:** the judges are refitted on builds made under v107 against the kept rows, with the line readings of Table DJ among their measures; until then the shortlist under v107 ranks on a yardstick fitted to the generator before it.

**Check:** after the refit, the content judge's median on Run B's builds is at or above v1's, and its AUC on held-out kept rows is printed.

### 292. The shortlist did not change the pick (a record)

**Problem:** none; a record against 255's first two songs.

**Evidence:** the composite's first build was inside the judge's upper half in all three runs: 60th of 219 (A), 111th of 610 (B), 300th of 702 (C). Under v103 it was 23rd of 43 (song 38) and 54th of 58 (song 39).

**Fix:** none.

**Check:** the report prints the rank each run.

### 293. A chosen character and verse 2's rhythm sit on their test's edge

**Problem:** 270/281's reciting test and 268's verse 2 test are met only at their limit, and the shortlist pick is not reciting at all.

**Evidence:** the verse median on reciting is 1.379 in B (A 1.351; C, aimed at the pool's medians, 1.541; test 1.4–2.1); the B pick's verse reads 0.65. Verse 2 shares 25% of verse 1's bar rhythms at the median in B (A 12.5%, C 16.7%), in range in 51% of builds, with the session's prior weight 8; with 4 the median was also 25%: the share moves in eighths of a section and the prior barely moves it.

**Fix:** 249 calibrates the chosen axis itself (the section's window read on the axis) rather than its measures one by one; 268 draws verse 2's bar rhythms from verse 1's bars at the kept 40%, then fits the syllables, rather than tilting a free rhythm walk.

**Check:** the reciting median inside 1.4–2.1 in B as well as C; verse 2's share inside 25–75% in three builds of four.

### 294. Fix 265 against the writer's split by section

**Problem:** 265's test (the drawn window's year in the era) cannot hold for a section whose character the writer chose against the era (263's split).

**Evidence:** the verse pool keeps its 20 reciting windows of any year by the writer's ruling (10 of them 1980–1989: ten windows to 1979 is too few to draw 3,000 builds from); the chorus pool is all to 1979.

**Fix:** 265 reads: under an era the target window is drawn from that era's windows, except in a section whose character the writer chose against the era at intake, which draws from the windows of that character.

**Check:** the report prints each pool's years and the ruling.

### 295. Fix 262 is met by moving the last note

**Problem:** the section endings hold in every build, but often by a move after the walk.

**Evidence:** in Run B the last note of a section was moved by a step to meet 262 910 times in 3,000 builds (a fresh last line redrawn up to seven times, then moved; a returning last line moved), because the verse's last chord is E (V), whose chord tones the walk favours, and Chorus 1's tail return copies a line that did not end on the tonic triad.

**Fix:** the contour of a section's last line is drawn toward an allowed ending (its end height on a permitted degree), and a returning last line's late change is drawn among the permitted degrees.

**Check:** fewer than one build in ten needs the move.

## Order of work

1. 286 (the unaudited gates as soft limits): the spectral band now kills half of every run, and the seven together pass 75.7% of the calibration pairs.
2. 287 (the return gate): two steps after 239 still change early shared notes; one rule exempts a built return from both.
3. 291 (refit the judges on v107 builds): the shortlist is ranking v107's lines with a yardstick fitted to the old generator.
4. 288 (the generator's palette and registers): the limits are loose but the builds still sit at five note lengths and a chorus ten semitones over the verse.
5. 289 and 290 (the landing draw; beat 3 dropped as an aim).
6. 293, 295 (a chosen axis calibrated whole; verse 2's bars drawn from verse 1's; section endings drawn, not moved).
7. 294 (265's wording for a section the writer split from the era); 292 (a record).

## Regression line

After these fixes, song 38 reruns at PYTHONHASHSEED 0, seed 20261491 (calibration 20261492), N 3000, Run B and Run C, and must reproduce their frozen orders twice (today's: B d648725d3587, C 3a6e5a3ea5af; they will change with the code). It must keep the six A4s on 'tuned' over A, the said-twice line moved whole on G4 over G, the tag E4–C♯4–A3, the bridge above the verse and under the summit (the two design gates); lose under one build in five at the spectral reading (286) and none at 267 where 239 built the return (287); spread the most note lengths in eight bars across 4–8 (288); put last stresses on 1 or 3 in 35–55% of lines (289); read the verse median on reciting inside 1.4–2.1 in B as well as C and verse 2's shared bar rhythms inside 25–75% in three builds of four (293); need the section-ending move in fewer than one build in ten (295); and pass every consistency check (55 of 55 today). The Table DJ readings that reached the kept middle half in Run B (arched or falling 68%, arch term +1.25, widening +0.20, entry after the downbeat 39%, the first note's extra surprise 1.74 bits) must stay there. The judges' claim stays what 27.47 says: like a kept song in content and order, not good.

## Reports

### Report 1: the runs and the pick

| Run | Survivors | Frozen order | Second run | Reproduced |
|---|---|---|---|---|
| A | 219 of 3,000 (7.3%) | 2f9ce3d36fce | 2f9ce3d36fce | yes |
| B | 610 of 3,000 (20.3%) | d648725d3587 | d648725d3587 | yes |
| C | 702 of 3,000 (23.4%) | 3a6e5a3ea5af | 3a6e5a3ea5af | yes |
| v1 (v103) | 43 of 3,000 (1.4%); control 118 | 6c9159e817fe | — | (reproduced in the first session) |

249's pass set Run B's and C's line strengths to contour amplitude 5.14, widening 1.31, fresh-start spread 1.99 semitones (round 3 read arch term 1.284, widening 0.302, first note's extra surprise 1.434 bits, against the kept 1.452, 0.326, 1.338).

| Run | Build | Composite | Content | Order | Combined |
|---|---|---|---|---|---|
| A | composite first: 400668bdcdf5 | 0.857 | 1.644 | 3.913 | 2.779 |
| A | shortlist pick: 400668bdcdf5 | 0.857 | 1.644 | 3.913 | 2.779 |
| A | judge first: 9345147b82c4 | 0.786 | 6.517 | 3.659 | 5.088 |
| B | composite first: 45a09df333f6 | 0.85 | 2.965 | 2.051 | 2.508 |
| B | shortlist pick: 45a09df333f6 | 0.85 | 2.965 | 2.051 | 2.508 |
| B | judge first: 80019b6a03c0 | 0.584 | 9.172 | 3.489 | 6.33 |
| C | composite first: 9dbd460307fe | 0.865 | 0.325 | 3.375 | 1.85 |
| C | shortlist pick: 9dbd460307fe | 0.865 | 0.325 | 3.375 | 1.85 |
| C | judge first: 5898b5e9741e | 0.63 | 6.554 | 3.288 | 4.921 |

- Run A: the composite's first is 60th of 219 by the judge, inside the upper half (109), so the shortlist did not change the pick. Builds: content -1.281 · 1.512 · 4.929, order 1.074 · 2.74 · 4.5, combined 0.689 · 2.119 · 4.029.
- Run B: the composite's first is 111th of 610 by the judge, inside the upper half (305), so the shortlist did not change the pick. Builds: content -2.046 · 0.66 · 3.856, order 0.925 · 2.632 · 4.505, combined 0.224 · 1.638 · 3.388.
- Run C: the composite's first is 300th of 702 by the judge, inside the upper half (351), so the shortlist did not change the pick. Builds: content -1.932 · 0.606 · 3.888, order 0.878 · 2.673 · 4.542, combined 0.245 · 1.659 · 3.436.
- v1: the composite's first was 23rd of 43 and the shortlist changed the pick. Kept windows: content 4.565, order 1.58, combined 3.11 (medians).

The content judge's heaviest give-aways (weight × z, mean over 400 builds): v1: distinct pitches (-0.825), on offbeat eighth (-0.776), gap eighth (-0.485), gap sixteenth (-0.483); A: on offbeat eighth (-0.74), gap eighth (-0.494), gap sixteenth (-0.483), gap quarter (-0.388); B: gap eighth (-0.877), on offbeat eighth (-0.841), distinct pitches (-0.754), gap sixteenth (-0.483).

### Report 2: deaths per gate, beside the first run

| Gate (v107) | v1 | A | B | C |
|---|---|---|---|---|
| limits: a hard limit or three soft breaks (276/277) | 459 (leaps 153; monotony run (166/196) 261; chorus at or above the verse, floor lifted (227) 45) | 0 | 1 | 1 |
| era: fewer than four of five bands inside CLASSIC's 5th-95th (264) | 1554 | 190 | 128 | 19 |
| returns related (267) | 317 | 447 | 162 | 213 |
| return: first or top note not kept (239) | 65 | 0 | 0 | 0 |
| summit placed (design gate; 216, 244) | 7 | 16 | 0 | 0 |
| bridge above the verse, under the summit (design gate; 208) | 44 | 89 | 86 | 44 |
| chorus opening another tune (227; 279) | 0 | 0 | 0 | 0 |
| bridge opening unrelated (208; 279) | 74 | 55 | 113 | 139 |
| rhythm band (163; unaudited) | 0 | 0 | 0 | 0 |
| pushed notes (159; 279) | 0 | 0 | 0 | 0 |
| density (159; 279) | 0 | 0 | 0 | 0 |
| sequence legs (148; unaudited) | 0 | 0 | 0 | 0 |
| key word on a chord tone (134; 279) | 5 | 52 | 101 | 26 |
| the judge's floor (254; 279) | 1 | 10 | 53 | 52 |
| spectral (Table B; unaudited) | 278 | 1621 | 1431 | 1589 |
| cmp (Table B; unaudited) | 8 | 56 | 47 | 49 |
| memory (Table B; unaudited) | 19 | 86 | 65 | 65 |
| surprisal (Table B; unaudited) | 0 | 8 | 39 | 23 |
| realness (Table B; unaudited) | 4 | 33 | 99 | 10 |
| join: no held end and breath before the line (212) | 57 | 65 | 35 | 36 |
| join: no held end and breath before the copy (212) | 55 | 53 | 30 | 32 |
| align: the words do not fit the returning tune | 10 | 0 | 0 | 0 |
| rhythm: no placement | 0 | 0 | 0 | 0 |
| walk: no note | 0 | 0 | 0 | 0 |
| range (the voice row) | 0 | 0 | 0 | 0 |
| Survivors | 43 | 219 | 610 | 702 |

The v1 row for the limits adds the six gates 276 turned into limits (leaps 153, the run clause 261, the chorus floor 45). The death order is v1's (a build dies at the first gate it fails), so a gate's count depends on what dies before it. The 'would fail' counts, every gate read on every complete build:

| Gate | A | B | C |
|---|---|---|---|
| limits: a hard limit or three soft breaks (276/277) | 0 | 1 | 1 |
| summit placed (design gate; 216, 244) | 16 | 0 | 0 |
| returns related (267) | 451 | 162 | 213 |
| bridge opening unrelated (208; 279) | 70 | 121 | 147 |
| bridge above the verse, under the summit (design gate; 208) | 117 | 95 | 51 |
| era: fewer than four of five bands inside CLASSIC's 5th-95th (264) | 238 | 158 | 27 |
| key word on a chord tone (134; 279) | 70 | 116 | 29 |
| the judge's floor (254; 279) | 18 | 62 | 57 |
| spectral (Table B; unaudited) | 2258 | 1807 | 1890 |
| cmp (Table B; unaudited) | 75 | 63 | 59 |
| memory (Table B; unaudited) | 134 | 75 | 83 |
| surprisal (Table B; unaudited) | 16 | 48 | 28 |
| realness (Table B; unaudited) | 64 | 148 | 10 |

### Report 3: the limits, the pass rates and the line readings

| Run | Complete builds | 0 soft | 1 | 2 | 3+ | Deaths on a hard limit | Deaths on a third soft break | Pick's soft breaks |
|---|---|---|---|---|---|---|---|---|
| A | 2882 | 99.8% | 0.2% | 0.0% | 0.0% | 0 | 0 | 0  |
| B | 2935 | 93.7% | 6.3% | 0.1% | 0.0% | 1 | 0 | 0  |
| C | 2932 | 94.7% | 5.3% | 0.0% | 0.0% | 1 | 0 | 0  |
| kept songs | — | 70.7% | 22.9% | 5.7% | 0.7% | — | — | — |

Soft breaks by limit: Run A: run_max 4, tritone_leap_share 2; Run B: tritone_leap_share 157, run_max 19, past_octave_share 12; Run C: tritone_leap_share 151, past_octave_share 4.

Each limit, the builds' median and the pick, beside Table DL (Run B; Run A and C alongside):

| Limit | Soft | Hard | B builds' median | B pick | A median | C median |
|---|---|---|---|---|---|---|
| tritone_leap_share | 0.0171 | 0.0383 | 0 | 0.011 | 0 | 0 |
| past_octave_share | 0.0177 | 0.0417 | 0 | 0.007 | 0 | 0 |
| run_max | under 10 | under 15 | 7 | 5 | 7 | 6 |
| tritone_from_root_share | 0.0348 | 0.1282 | 0 | 0 | 0 | 0 |
| max_lengths_8_bars | 8.0 | 9.0 | 5 | 5 | 5 | 5 |
| chorus_top_minus_verse | -6.05 | -10.83 | 10 | 10 | 12 | 10 |
| chorus_median_minus_verse | -5.0 | -8.22 | 10 | 5 | 10 | 9 |
| chorus_floor_minus_verse | -5.0 | -7.0 | 7 | 7 | 7 | 7 |

The builds still sit at one point on two readings: the most note lengths in any eight bars is 5 in every build of all three runs (5th to 95th: 5 · 5 · 5 · 5 · 5; kept median 6, 4 to 8), and the chorus's top is 10 semitones over the verse's at the median (kept: 0 at the median, 9 at the 95th). The longest run in a line now spreads (5 · 6 · 7 · 8 · 8 in B; kept 2 · 4 · 5 · 7 · 10). A tritone leap appears in 36.3% of B's builds and a leap past an octave in 28.8% (kept songs: 34% and 41% have one); in A, 4.4% and 0.9%.

| Gate | Kept pass rate | Source |
|---|---|---|
| limits: three soft breaks or one hard (276/277) | 92.0% | Table DL |
| summit placed (216, 244) | — | design gate (exempt from 275) |
| bridge median above the verse's, top under the summit (208) | 32.6% ⚑ | design gate (exempt); kept as coded |
| era: four of five bands inside CLASSIC's 5th-95th (264) | 90.8% | Table DK |
| returns related (267) | — | not printed by the paper; 239 as a gate: first note 80%, top 92% of kept returns |
| chorus opening unrelated (227) | 94.9% | Table DL |
| bridge opening unrelated (208) | 95.2% | Table DL |
| pushed notes at most 42% (159) | 99.4% | Table DL |
| density 1.1 to 4.9 notes a second (159) | 95.3% | Table DL |
| key word on a chord tone (134) | 90.0% | Window 94 ('about nine in ten') |
| the judge's floor (254) | 95.0% | kept 5th percentile by its making |
| joins: a held end and a breath before the line or copy (212) | — | unread by the paper and here (a lyric-placement rule) |
| the voice's range (intake) | — | the writer's voice row, not a kept-song gate |
| spectral (session, 280) | 89.9% ⚑ | POP909 calibration pairs (515) |
| cmp (session, 280) | 95.0% | POP909 calibration pairs (515) |
| memory (session, 280) | 95.0% | POP909 calibration pairs (515) |
| surprisal (session, 280) | 97.9% | POP909 calibration pairs (515) |
| realness (session, 280) | 95.0% | POP909 calibration pairs (515) |
| rhythm band (163) (session, 280) | 98.4% | POP909 calibration pairs (515) |
| sequence legs (148) (session, 280) | 100.0% | POP909 calibration pairs (515) |

The seven gates of fix 280 were run with the engine's own functions on its calibration pairs: **POP909 (Wang et al. 2020), the 515 major-key songs with a labelled verse and chorus (Dai et al. 2020 labels): the engine's calibration pairs for Table B, read on the whole first verse and chorus runs as the calibration was**. The five Table B readings pass together on 75.9% of the 515 pairs; all seven together on 75.7% (breaks per pair: 0: 390, 1: 102, 2: 22, 3: 1). The family is under 275's nine in ten and is flagged (⚑); by the writer's ruling the seven stayed as gates in all three runs. Table B's floors were set on these pairs at the 5th percentile (the spectral band at the 5th and 95th), so each passes about 95% (90%) alone by its making; the joint rate is the new reading. The sequence-legs gate was read with bars counted from the pair's own first bar (the engine's bar_cells counts the song's sung bars); the rhythm band with the engine's rhythm table on the pairs' sixteenth grid.

Builds' 5th · median · 95th; the pick; the kept middle half (25th · median · 75th). Every complete build is read; v1's are its 2,813 complete builds (the first run kept notes for these, not for the builds that died while being made).

| Reading | Kept | v1 | A | B | B pick | B outside kept middle half | C |
|---|---|---|---|---|---|---|---|
| arch or falling | 0.5 · 0.667 · 0.783 | 0.463 · 0.61 · 0.78 | 0.439 · 0.585 · 0.78 | 0.488 · 0.683 · 0.854 | 0.732 | 21.0% | 0.512 · 0.683 · 0.854 |
| valley | 0.033 · 0.087 · 0.167 | 0.024 · 0.122 · 0.293 | 0 · 0.098 · 0.268 | 0 · 0.098 · 0.244 | 0.122 | 43.1% | 0 · 0.098 · 0.244 |
| arch positive | 0.5 · 0.636 · 0.767 | 0.366 · 0.585 · 0.78 | 0.366 · 0.585 · 0.78 | 0.366 · 0.585 · 0.78 | 0.537 | 31.4% | 0.39 · 0.61 · 0.805 |
| arch term | 0 · 1.452 · 3.341 | -1.711 · 1.273 · 4.148 | -1.175 · 1.092 · 3.899 | -1.005 · 1.246 · 4.136 | 1.626 | 28.8% | -0.75 · 1.387 · 4.275 |
| falling term | 0.191 · 2.848 · 5.404 | -0.864 · 3.529 · 7.883 | -0.471 · 3.301 · 7.762 | 0.806 · 5.01 · 10.932 | 11.574 | 48.2% | 1.511 · 5.435 · 10.44 |
| peak first third | 0.421 · 0.6 · 0.737 | 0.244 · 0.415 · 0.585 | 0.268 · 0.463 · 0.634 | 0.317 · 0.512 · 0.683 | 0.585 | 26.9% | 0.293 · 0.463 · 0.659 |
| end minus mean | -2.267 · -1.2 · -0.315 | -2.429 · -0.75 · 0.444 | -2.286 · -0.571 · 0.25 | -3.25 · -0.875 · 0.25 | -3.556 | 46.3% | -3.25 · -1 · 0.25 |
| last over mean | 1.182 · 1.478 · 1.714 | 1.333 · 1.615 · 2 | 1.333 · 1.615 · 2 | 1.429 · 1.778 · 2.182 | 1.5 | 64.0% | 1.455 · 1.714 · 1.909 |
| widening | -0.105 · 0.326 · 1.083 | -1.805 · -0.366 · 1.22 | -1.878 · -0.427 · 1.146 | -1.122 · 0.195 · 1.634 | 1.537 | 55.0% | -1.122 · 0.39 · 1.854 |
| first note extra bits | 0.829 · 1.338 · 1.899 | -0.31 · 0.689 · 1.691 | -0.331 · 0.734 · 1.722 | 0.519 · 1.737 · 3.058 | 3.716 | 51.8% | 0.503 · 1.715 · 3.026 |
| starts on downbeat | 0.074 · 0.179 · 0.368 | 0.024 · 0.073 · 0.098 | 0.024 · 0.073 · 0.098 | 0.049 · 0.146 · 0.317 | 0.22 | 19.4% | 0.049 · 0.146 · 0.317 |
| starts after downbeat | 0.333 · 0.525 · 0.783 | 0.024 · 0.122 · 0.293 | 0.024 · 0.122 · 0.293 | 0.195 · 0.39 · 0.585 | 0.22 | 27.9% | 0.195 · 0.39 · 0.585 |
| starts as pickup | 0.034 · 0.143 · 0.357 | 0.634 · 0.805 · 0.902 | 0.634 · 0.805 · 0.902 | 0.317 · 0.439 · 0.61 | 0.561 | 82.7% | 0.317 · 0.439 · 0.61 |
| ends on downbeat | 0.111 · 0.273 · 0.429 | 0.341 · 0.439 · 0.61 | 0.341 · 0.439 · 0.634 | 0.317 · 0.463 · 0.634 | 0.463 | 58.9% | 0.341 · 0.488 · 0.659 |

Contour kinds (share of lines): kept falling 23.8%, arch 21.5%, valley 11.5%, level then falling 11.1%, rising 9.3%; Run B falling 33.1%, level then falling 15.5%, arch 12.2%, valley 10.0%, rising 7.9%; the B pick falling 41.5%, valley 12.2%, rising 4.9%, level then falling 19.5%, level then rising 9.8%.

The move between lines a fourth or more: A 0.075 · 0.175 · 0.35; B 0.2 · 0.375 · 0.575 (pick 0.55); kept 34% of joins.

**Line entry, two readings side by side (285).**

| Run | 231: lines with a pickup | 231: last stress on 1 or 3 | 231: last stress off the beat | 260: after the downbeat | 260: on it | 260: on beat 4 |
|---|---|---|---|---|---|---|
| A | 0.634 · 0.805 · 0.902 | 0.439 · 0.585 · 0.732 | 0.122 · 0.268 · 0.415 | 0.024 · 0.122 · 0.293 | 0.024 · 0.073 · 0.098 | 0.634 · 0.805 · 0.902 |
| B | 0.317 · 0.439 · 0.61 | 0.488 · 0.634 · 0.805 | 0.098 · 0.22 · 0.39 | 0.195 · 0.39 · 0.585 | 0.049 · 0.146 · 0.317 | 0.317 · 0.439 · 0.61 |
| C | 0.317 · 0.439 · 0.61 | 0.488 · 0.634 · 0.78 | 0.122 · 0.244 · 0.39 | 0.195 · 0.39 · 0.585 | 0.049 · 0.146 · 0.317 | 0.317 · 0.439 · 0.61 |
| kept | 40–70% asked | 35–55% asked | — | 33 · 52 · 78% | 7 · 18 · 37% | 3 · 14 · 36% |

Section endings, the B pick (scale degree of the last sung note): Verse 1 7, Pre 1 6, Chorus 1 1, Verse 2 7, Pre 2 6, Chorus 2 1, Bridge 7, Last Chorus 1. Across B's builds Chorus 1 ends 1 1113, 5 988, 3 834; Verse 1 5 627, 3 584, 7 527, 2 420. The last note over the line's mean note 1.429 · 1.778 · 2.182 (kept 1.18 · 1.48 · 1.71); the last note the line's longest in 0.561 · 0.707 · 0.878 of lines (kept 61%).

### Report 4: the tests of 257–285 and the regression line from the list after v103

| Fix | The test | The reading | Held? |
|---|---|---|---|
| 257 | median 50–78% arched or falling; arch term positive in half or more; no survivor outside 31–94% or with valleys over 33% | B 68.3%, positive 58.5%; 7 of 610 survivors outside, 5 with valleys over 33%; pick's contours: falling 41.5%, valley 12.2%, rising 4.9% | median yes; survivors no (12) |
| 258 | median widening −0.1 to +1.1; no survivor outside −1.4 to +1.9; the pick's interval by fifths printed | B 0.195; 19 survivors outside; pick by fifths 1.58 · 2.35 · 1.71 · 1.67 · 3.14 (A -0.427) | median yes; survivors no |
| 259 | first pitch from the contour; median extra surprise 0.8–1.9 bits; joins a fourth or more in 25–40%; no survivor under −0.1; a copy keeps its first note | B 1.737 bits; joins 37.5%; 2 survivors under −0.1 (A 0.734, 17.5%) | median yes; survivors no (2) |
| 260 | median 33–78% after the downbeat; no survivor under 10%; a section entering one way named a design | B 39.0%; 2 survivors under 10% (A 12.2%, 105); the chant lines are designed pickups | median yes; survivors no (2) |
| 261 | a reading: last note over mean (kept 1.2–1.7), last note the longest | B 1.429 · 1.778 · 2.182; longest 0.561 · 0.707 · 0.878 | printed (long) |
| 262 | last chorus on the tonic; an earlier chorus on the tonic triad; the verse off the tonic | B: last chorus 100.0%, chorus 1 100.0%, verse 1 off 100.0% (910 last notes moved) | yes |
| 263 | intake count of windows both reciting and CLASSIC | the first session's Q14; not asked again (no intake questions) | n/a here |
| 264 | rejected only when fewer than four of five bands inside the 5th–95th; deaths under one in five; the pick inside the middle halves on three of five | deaths A 190, B 128, C 19 of 3,000; B pick 4 of five | yes |
| 265 | the drawn window's year recorded and in the era | chorus pool all to 1979 (100.0%); B pick: verse window 161 (1966), chorus 177 (1958); the verse pool keeps any year (the writer) | chorus yes; verse by ruling (294) |
| 266 | no aimed measure from a class median | B none (all from the window); A: notes a bar from the chart median (the v1 rows) | yes (B) |
| 267 | no build dies at the return gate where 239 built the return | deaths A 447, B 162, C 213; near-level used 2 times in B | no (287) |
| 268 | verse 2 shares 25–75% of verse 1's bar rhythms at the median | B 0 · 0.25 · 0.571, in range 51.4% (A 0 · 0.125 · 0.375) | at the edge (293) |
| 269 | 260's test; last stresses on 1 or 3 in 35–55% | B after 39.0%; on 1 or 3 0.488 · 0.634 · 0.805 | entry yes; landing no (289) |
| 270 | dies only at ten or more; a fifth of lines (±half) with a run of four; reciting median 1.4–2.1 | runs ≥10: 19 soft breaks, 0 hard (276/277 govern); lines with a run of four 25.1%; reciting B 1.379, A 1.351, C 1.541 | runs yes; reciting no in B (by 0.02) |
| 271/285 | every aim kept followed at r ≥ 0.3; dropped after two songs running under it | turns per move: verse 0.102, chorus 0.172 (song 39 0.56, 0.33); beat 3 via the landing draw: verse 0.202, chorus 0.078 | no (290) |
| 272 | fills against gaps of 2.75 beats or more; seven in ten filled | 7 of 9 eligible gaps filled; short gaps 9 filled with a beat and a half | yes |
| 273 | chord strikes with a bass note printed beside the bass cell; 16% or more | 100% (eighth-note bass cell), see the record | yes |
| 274 | the extension named; every other section a multiple of four | the last chorus's 18 bars named; all others multiples of four | yes |
| 275 | every gate printed with its kept pass rate; families under 90% flagged | section 4; flagged: the seven unaudited gates together (75.7%), the spectral band alone (89.9%) | printed |
| 276 | the eight limits on every build; pick and median beside Table DL | section 3 | yes |
| 277 | deaths on a hard limit or third soft break under one in five; the pick's soft breaks printed | B 1 death of 3,000; pick 0 soft breaks | yes |
| 278 | no death for a comparison, a return's first or top note, or a tritone unless chosen; design gates listed; kept rates beside the builds' | design gates: the summit, the bridge's register; aims in the table below | yes |
| 279 | a record | the six sound gates as they stand | — |
| 280 | the seven unaudited gates' pass rates on the calibration songs and together | section 4; together 75.7% | printed; under 90% |
| 281 | with a section's character chosen, the median on that axis in 1.4–2.1 whatever is designed; free notes printed | verse reciting B 1.379; free notes in the pick: Verse 1 17, Pre 1 16, Chorus 1 33, Bridge 23 | no, narrowly (293) |
| 282 | a line said twice keeps its source's intervals except notes changed for 276's tritone reading | B: notes changed 0 · 0 · 0; the pick 0; 'tuned' on G4 over G | yes |
| 283 | the feel of each section stated | every section straight | n/a (no swing) |
| 284 | a record | song 39's | — |

Fixes that did not apply to this song: 263 (an intake count; the writer had already settled reciting against CLASSIC at Q14 and no intake question was asked), 283 (no section is swung), 279 and 284 (records), 261 (a reading only). Fixes 257–262, 265, 266, 268, 269, 271, 281 and 282 ran in Run B and C only, by the brief's design.

**278's aims: the builds' rate beside the kept rate.**

| Aim | Kept | A | B | C |
|---|---|---|---|---|
| chorus top at or above the verse's | 72.9% | 100.0% | 100.0% | 100.0% |
| chorus median not below | 77.1% | 100.0% | 100.0% | 100.0% |
| chorus lowest note above | 55.7% | 97.3% | 99.3% | 99.2% |
| bridge median above the verse's | 67.4% | 95.9% | 96.8% | 98.3% |
| bridge top under the song's | 55.8% | 100.0% | 100.0% | 100.0% |
| returns keep their first note | 80.2% | 86.0% | 83.0% | 81.5% |
| returns keep their top note or higher | 92.4% | 99.5% | 99.5% | 99.4% |
| five note lengths at most (V1, C1 windows) | 80.8% | 100.0% | 100.0% | 100.0% |
| no tritone leap | 65.9% | 95.6% | 63.7% | 65.9% |
| no note a tritone from the root | 54.1% | 100.0% | 100.0% | 100.0% |

**Aims followed (285's two readings), correlation of target and reading across Run B's builds:** v:on_tonic 0.59, c:on_tonic 0.664, v:on_third 0.68, c:on_third 0.712, v:on_fifth 0.749, c:on_fifth 0.723, v:on_beat3 0.202, c:on_beat3 0.078, v:on_beats_2_4 0.333, c:on_beats_2_4 0.332, v:turns_per_move 0.102, c:turns_per_move 0.172, v:repeat 0.491, c:repeat 0.762, v:step 0.607, c:step 0.713, v:chord_tones_on_beat 0.447, c:chord_tones_on_beat 0.457, v:gap_eighth 0.262, c:gap_eighth 0.335. Run C aims every build at the same medians, so it has no correlation to read.

| Item | Reading | Held? |
|---|---|---|
| Both orders reproduced twice at PYTHONHASHSEED 0 | A 2f9ce3d36fce, B d648725d3587, C 3a6e5a3ea5af, each the same on the second run | held |
| The six A4s on 'tuned' over A | six, bars 21, 29, 49, 57, 89, 97 | held |
| The chorus opening unrelated | yes | held |
| The chorus floor above the verse's | 54 against 47 (now an aim, 278) | held |
| The pick inside CLASSIC's five bands | 5th–95th on five; middle halves on four (notes_per_bar, range, repeat, pitch_bits) | held as 264 reads it |
| Under one build in five at the era gate (258 → 264) | A 190, B 128, C 19 of 3,000 | held |
| None at 181 where the return was built (261 → 267) | A 447, B 162, C 213 | not held (287) |
| Verse median on reciting inside 1.4–2.1 (264 → 270) | A 1.351, B 1.379, C 1.541 | B not held by 0.02; C held |
| Verse 2's shared bar rhythms inside 25–75% (262 → 268) | A 0.125, B 0.25, C 0.167 | B at the floor; A and C not held |
| Every consistency check | 55 of 55 | held |
| The controls stay as the comparison | Run C beside Run B throughout | held |
| The judges' claim stays what 27.47 says | like a kept song in content and order, not good; no claim made beyond it | held |

## Readings the paper did not spell out

Every place this rerun had to choose a number or a reading that v107 does not give, by fix, so the paper can be corrected. The writer ruled on the first five before the runs.

| Fix | The reading taken |
|---|---|
| 270, 276, 277 | The run clause is one of 276's eight limits: a run of 10–14 in a line is a soft break, 15 or more hard (the writer's ruling). 270 contributes only the lifted ban: the walk may repeat a fourth time, and the v1 repair step no longer re-walks runs of four. The repair step still re-walks leaps past a sixth and tritones. |
| 268, 269 | In verse 2 each line takes its source line's entry kind, and the rest of the rhythm walk is tilted toward verse 1's onsets (the writer's ruling). The tilt multiplies a source onset's weight by 8, the session's number, chosen by trial (4 left the median at the same 25%), not calibrated. |
| 267 | Near-level means both shared-event pitch series span 2 semitones or less: the session's number, uncounted (the writer's ruling). |
| 267 | 'The first three-quarters of the events it shares' is read by time, the shared events before 0.75 of the line's span, which is the quarter in which v1's 239 makes its late change. Read by count, a build whose change lay in the last quarter by time but not the last quarter by count died; 31 of the first 60 test builds did. |
| 280 | The seven unaudited gates stay as gates in all three runs; their pass rates are printed on the 515 POP909 major-key pairs (the writer's ruling). They did not join 277's count: the paper gives no soft or hard values for them. |
| 282 | Run B and C build the said-twice line as its source moved whole; Run A keeps v1's way (the writer's ruling). A note is changed only where it is a tritone from its chord's root on a beat or held a beat (276's reading), to the nearer semitone that is not. |
| 278 | A return's first or top note: vary_return's six tries steer toward keeping both, and if none of the six does, the last try is kept. |
| 264 | Run A keeps v1's chorus pool (windows inside three of the four CLASSIC middle-half bands the old rows carry) as the way the middle halves are aimed at. |
| 265 | Run B's chorus and bridge pool is every kept window to 1979 (200), with no band filter. The verse pool keeps its 20 reciting windows of any year (the writer's ruling: Q14 let the verses recite against CLASSIC). |
| 260, 269 | Entry rates: the kept song medians (on 0.179, after 0.525, pickup 0.143) normalised to 21%, 62%, 17%. 'After the downbeat' is the 'and' of 1 to the 'and' of 3 on the eighth grid; 'pickup' is beat 4 of the bar before or its 'and'. A stressed first syllable cannot be a pickup; the kind is then redrawn between on and after. The chant lines are designed pickups. |
| 259 | In B and C the v1 join repair (a line's pickup re-walked when the join leaps past an octave or a tritone) and the steering of a line's last note toward the next line's first are dropped. The first pitch is drawn around h0 = the section's centre + N(0, s) − the contour's mean, kept inside the section's register, with a spread of 1.5 semitones around h0; s is 249's fresh-start knob. |
| 257 | Contour kinds are drawn at Window 124's kept shares of lines. Each kind is a piecewise line through the line's time (arch: 0 → +1 at 0.3 → −0.2; falling 0 → −1; valley 0 → −1 at 0.5 → 0; and so on), scaled by 249's amplitude knob × U(0.7, 1.3); the walk is pulled toward it with a Gaussian of 2.5 semitones. Designed lines, copies, returns and re-sung lines keep their own notes. |
| 258 | Widening is a tilt on the walk's interval categories through the line: repeats and steps × exp(−W(x − ½)), thirds and larger × exp(W(x − ½)), x the time through the line, W 249's widening knob. |
| 249 | The three line strengths are calibrated in the same 3 × 30 pass toward Table DJ's kept medians (arch term 1.452, widening 0.326, first note's extra surprise 1.338): multiplicative for amplitude and spread, additive for widening, with caps. |
| 285 | The window's beat-3 share tilts the b3 share of 231's landing draw by (target ÷ pool median)^1.5; the walk's beat-3 tilt and its calibration knob are removed. |
| 262 | Verse 1's last note is kept off the tonic and Chorus 1's on A, C♯ or E. A fresh last line is redrawn up to seven times, then (and for a returning last line) its last note moves by the smallest step to an allowed scale tone (910 times in B). The pre-chorus and the bridge have no rule; verse 2 inherits verse 1's ending. |
| 281 | No compensation was computed: verse 1's only non-free notes are returns of its own free lines, so the free lines carry the whole aim. The free-note counts are printed. |
| 27.48 (Table DJ) | Lines are the engine's lyric lines, not found by rule, with three notes or more. A song's value is the median over its lines for the arch and falling terms, the last note less the mean and the last note over the mean; the mean for shares and the widening. The first note's extra surprise is the mean surprise of each line's first note (from the line before's last note) less the mean of all other notes, under the v104 file's first-order model. |
| 276 | The limits are read on the whole song's sung notes in order, moves across line joins included; the run inside a line; the tritone from the root on notes on a beat or a beat or longer; the chorus comparisons on Chorus 1 and Verse 1 as whole sections. |
| 272 | A short fill starts half a beat after the voice stops and ends as it returns, with no margin; short gaps are offered a fill at the same 70% and are not counted in the rate. |
| 264 | The five era readings are v1's: the median of the first 8-bar windows of Verse 1, Chorus 1 and the Bridge. |
| All runs | Builds that died while being made keep their partial notes and fingerprint; their judge scores are empty. |

## Blind-pick tally

No blind pick: a regression run reuses the song's locked lyric. The tally stands at 27 songs: Annotated top 11, Remembered top 8, Middle 7, Refrain 1.
