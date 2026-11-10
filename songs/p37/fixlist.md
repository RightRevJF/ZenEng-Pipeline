# ZenEng fix list after v96

*Song 37 · fixes 225–232 · with the readings the brief asked for, the deaths per gate, which fixes ran, and the paper's tests*

v96's version row (v130) ends at fix 224, checked before numbering. This list starts at 225 and covers every song since v96: one, song 37, *Windows Down*. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

The brief, as the writer relayed it: a new pop, rock or country song under v96; read the spec and the three tables files, don't refit; intake one question a turn with the full lyric before music, and at the lyric 220 (multiples of four; lines too long named), 213 (ask for one verse or chorus whose first two lines are within three syllables, and say why), 202 and 208 (the summit and bridge questions with the kept figures); port 224 first, then 212, 214, 215, 216, 217, 218, 219, 223; a control with 224 off; report the distance on 46 measures, the measures outside both kept middle halves, the bar-window returns, the section lengths, the eighth gaps and longest note with their spread, survivors and deaths; push the code with the seed; number findings from 225.

## Songs since v96

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 37 | Windows Down | The rock class under v96, 224 run for the first time. A man walks out of his plant's last shift after twenty-six years and drives home to his wife, windows down to air the cutting oil out of his clothes. Male baritone D3–F♯4; 4/4 at ♩ = 122, A major, heartland rock with a guitar hook and a 16-bar solo. Every section a multiple of four bars, every line two (220); the chorus opens by saying it twice (213); the summit F♯4 on chorus line 4's first word, five times (202, 216); the bridge lifted (208). 112 bars, 3:40. One control (224 off) and one probe (targets from the kept 5th–95th). | 225–232 |

## The fixes

### 225. 224 draws from the middle half, but distance counts only what lies outside it

**Problem:** 224 draws each build's targets from the kept middle half (25th–75th) and aims the build there. 210's distance is zero for any value inside the middle half, so a build that meets its targets adds nothing to its distance on those measures. Kept songs are far from the centre because each lies outside the middle half on a number of measures (half of kept songs are outside on any one measure, by definition).

**Evidence:** Builds' distance 0.052–0.089–0.135 (5th, median, 95th); 45% too central (under 0.086) and 6% inside the chart songs' middle half (0.133–0.228). The control (every build aimed at the medians): 0.079 median, 62% too central, 3% inside. A probe with targets drawn from the kept 5th–95th: 0.109 median, 20% too central, 24% inside. 224 moved the builds a third of the way; the wider draw moved them further. Song 36 version 3: 75% too central.

**Fix:** Draw each build's targets from the kept distribution itself, not its middle half: from the chart songs' values (or the 5th–95th, as the probe did), so a build is aimed outside the middle half on about as many measures as a kept song is.

**Check:** 224's test: the builds' median distance inside 0.133–0.228 and fewer than one build in ten too central.

### 226. A summit on the chorus's last line puts every chorus window's peak late

**Problem:** The writer put the summit on the first word of chorus line 4 (fixes 202, 216). The summit question showed where chart pop puts its peak in the song (31%). The discriminator reads 8-bar windows, where chart pop's peak falls early (median 23% of the window). A summit in line 4 of an 8-bar chorus sits at 75% of every chorus window.

**Evidence:** Peak position 0.75 in every chorus window; outside both kept middle halves in 100% of builds, in the run, the control and the probe. Time in the top third was low in 57% of builds, because the single F♯4 is the only note in the top third.

**Fix:** The summit question shows the window figure beside the song figure. A summit in a window's last quarter is named at intake as a choice, and the report prints the measures it fixes as design-caused rather than as drift.

**Check:** The question prints both figures; the report separates design-caused readings.

### 227. The lyric's density sets a floor under notes a bar and eighth-note gaps

**Problem:** 218 asks for about four syllables a bar and eighth-note gaps inside 27–62%. A lyric of seven-to-nine-syllable lines on two-bar lines puts 32 or more notes in each 8-bar window, so notes a bar cannot go below about 4.25. With that many notes, most gaps are eighths whatever the build is aimed at.

**Evidence:** Notes a bar 4.25–4.31–4.62 across builds (drawn targets averaged 3.80; the reading followed the target, r 0.62, but sat 0.55 above it). Eighth gaps 47–63–78% (targets averaged 0.48; followed, r 0.55, but 15 points high); the median is above both middle halves, and 56% of builds were outside both.

**Fix:** At the lyric stage, 218 counts the lyric's notes a bar (kept median 3.75) and names it when the lines are dense. 224 clips a build's drawn target to what the lyric allows and records it as clipped.

**Check:** Where the lyric allows, the builds' eighth-gap median inside 27–62%; where it does not, the report says so at the lyric stage.

### 228. The run clause is the largest killer, and copies make the runs

**Problem:** 196's run clause (four repeated notes) killed more builds than anything else. The walk bans a fourth repeat, so the runs come from notes the walk did not draw: 181's aligned returns (split events and pickups) and the copied lines.

**Evidence:** 122 of 500 builds died at the run clause in the run, and 122 in the control. Of the runs of four in 240 builds checked, 51% fell in the verse's aligned returns, 16% in chorus copies and 19% in fresh chorus lines next to the fixed summit and tonic notes.

**Fix:** 181's mapping moves a split event or an added pickup by step, not to the same pitch. A copied or aligned line that would make a run of four has its extra notes re-walked, as 215 moves a copied note.

**Check:** Run-clause deaths under one build in ten.

### 229. 212 misses copies that are aligned, not copied whole

**Problem:** 212 draws a line knowing the first onset of the copy after it. When the copy is aligned to new words (a verse 2 or pre-chorus 2 line), 181's mapping can move its first syllable into a pickup, so the copy starts earlier than its source did.

**Evidence:** Join deaths 57 of 500 (11.4%), down from 47% in song 36 version 3, but above 212's test (under one in ten). 32 of the 57 died at the join before a copy.

**Fix:** Align the copy first, then draw the line before it against the aligned copy's first onset.

**Check:** Join deaths under one build in ten.

### 230. 219's anchor is not enough when the return has more syllables

**Problem:** 219 reads the 181 gate on lines from each line's downbeat. Where a returning line has more syllables than its first statement, 181's mapping splits events, and the split notes change the contour the gate compares.

**Evidence:** 11 builds died at 181, every one on contour (correlation under 0.6), and every one a verse line returning line 1 with a different syllable count (7 against 9).

**Fix:** The gate compares the return on its source's events only, with the split notes left out, because 181 built the return from those events.

**Check:** No build dies at 181 where its construction was used (219's test).

### 231. 214's on-beat share runs high, and the rank of record picks an off-target build

**Problem:** 214's calibration from song 36 did not carry to a new key, register and lyric. After recalibration the builds still ran high on the beat, and the composite, which knows nothing of a build's own targets, picked a build far from them.

**Evidence:** Chord tones on the beat 74% at the builds' median (test: within three points of 69%); off the beat 65%. The readings followed their targets only loosely (r 0.41 on, 0.43 off). The pick read 65% on and 82% off against its own targets of 70% and 75%, and was outside both kept middle halves on chord tones off the beat.

**Fix:** A short calibration pass at the start of every run, on the run's own song (recorded with the seed), sets 214's and 224's mapping. Each build's distance from its own targets is printed beside the rank of record, with no change to the ranking (211).

**Check:** The builds' medians within three points of 69% and 62%; the target error printed for the pick.

### 232. The number of measures outside both middle halves has no yardstick

**Problem:** The brief asks for every measure outside both kept middle halves, of 56. The tables give the percentiles of each measure, but not how many measures a kept song is outside both on, so a pick's count cannot be read.

**Evidence:** The pick is outside both on 13 measures, the builds on 5–9–14, the control's pick on 9 (song 36: version 1 on 8, version 3 on 1). Several are fixed by the design: peak position, time in the top third, and notes on the downbeat and on beats 2 and 4, through the summit's place and the two-bar lines. The rest belong to the pick.

**Fix:** Print the chart songs' own count of measures outside both middle halves (median and 5th–95th) in the discriminator file.

**Check:** The report prints the pick's count beside the chart songs' range.

## Order of work

1. **225** (draw from the kept distribution): it decides whether 224 can pass its own test.
2. **231** (calibrate on each run; print the target error), then **227** (clip targets to the lyric): together they decide whether a build reads near its targets.
3. **228**, **229**, **230** (copies: runs, joins, the return gate): one change to 181's mapping and the order in which lines are drawn.
4. **226** (the summit question's window figure) and **232** (a yardstick for the outside count): wording and a table.

## Regression line

After these fixes, song 37 rerun at N 500, seed 20261481, PYTHONHASHSEED 0 must: reproduce its frozen order twice; keep every section a multiple of four bars and every chorus's last line on A; keep the five F♯4s on beats over D; keep the bar-window returns at or above 31% and the opening repeated at once in 15–30% of windows; keep the builds' interval medians within two points of their targets; lose fewer than one build in ten at joins, at the run clause and at 181; put the builds' median distance inside 0.133–0.228 with fewer than one in ten too central; and pass 47 of 47 consistency checks. The control (224 off) must still read about 62% too central, so the comparison stands. The composite scored the pick 0.884 and the control's first pick 0.838; it stays the rank of record (211) and nothing more.

## Report 1: the readings the brief asked for

**The search.** N 500, seed 20261481, PYTHONHASHSEED 0, code b1b68b67d425, Python 3.13.18, numpy 2.5.3, tables 561355b1… and 1a2af952…. 153 survivors (30.6%); reproduced exactly on a second run, frozen order 15ed5929f53d. Pick 9a3e548d293f, first by the rank of record (composite 0.884); no hand edits. Plans: verse AABC, pre-chorus AB, chorus ABAC sung twice, bridge ABAC. The pick's drawn targets: repeat 0.169, step 0.560, third 0.161, fourth or fifth 0.092, past a fifth 0.018, chord tones 0.699 on the beat and 0.751 off, eighth gaps 0.567, quarter gaps 0.162, longest over median 3.64, notes a bar 3.72.

**The control.** Same seed and N, 224 off (every build aimed at the chart medians). 109 survivors, order 4d23a255a8b9; first pick 8db8e134f3a6 (composite 0.838).

**The probe.** Same seed and N, targets drawn from the kept 5th–95th. 147 survivors, order f04360d518e5.

Builds are every song the generator finished, before the gates. Across all builds the opening unit returned third in 39% of verse and chorus windows and was repeated at once in 28% (means; kept 31–49% and 17–28%).

| Reading | Pick | Builds 5th · median · 95th | Control's pick | Control builds (median) | Probe builds (median) | Kept |
|---|---|---|---|---|---|---|
| Distance from the centre, 46 measures | 0.103 | 0.052 · 0.089 · 0.135 | 0.053 | 0.079 | 0.109 | chart songs 0.086 · 0.176 · 0.351 |
| Builds too central | — | 45% | — | 62% | 20% | chart songs 5% |
| Measures outside both kept middle halves (of 56) | 13 | 5 · 9 · 14 | 9 | 9 | 10 | — |
| Opening unit returns third (bar windows) | 75% | 0% · 25% · 100% | 25% | 25% | 25% | 31% (chart) · 49% (grid) |
| Opening unit repeated at once (bar windows) | 25% | 0% · 0% · 100% | 0% | 0% | 0% | 17% · 28% |
| Gaps of an eighth | 58% | 47% · 63% · 78% | 64% | 59% | 72% | chart 32–47–62% · grid 27–44–61% |
| Gaps of a quarter | 33% | 8% · 20% · 39% | 21% | 21% | 15% | chart 6–15–28% |
| Longest note over the median note | 4 | 1.5 · 3 · 4 | 4 | 3.5 | 4 | chart 2–3–4 · grid 2–3–5 |
| Notes a bar | 4.25 | 4.25 · 4.31 · 4.62 | 4.25 | 4.25 | 4.38 | chart 2.94–3.75–4.63 |
| Chord tones on the beat | 65% | 55% · 74% · 94% | 59% | 74% | 69% | chart 56–69–80% |
| Chord tones off the beat | 82% | 42% · 65% · 86% | 92% | 67% | 61% | chart 47–63–76% |
| Pitch surprise (bits a note) | 2.66 | 2.51 · 2.72 · 3.02 | 2.66 | 2.64 | 2.86 | chart 2.53–2.74–3.03 |
| Spread of notes bar to bar | 2.14 | 0.98 · 1.79 · 2.64 | 2.17 | 1.71 | 2.00 | chart 1.20–1.62–2.12 |
| Bridge median over the verse's (semitones) | +5 | 0 · +2 · +7 | +3 | +2 | +2 | kept +2 (68% above) |
| Bridge onsets a bar over the verse's | 0.94 | 0.89 · 0.94 · 1.00 | 0.94 | 0.94 | 0.94 | kept 0.97 (0.78–1.21) |

**Section lengths in bars:** Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 16 · Last Chorus 16 · Outro 8 = 112.

**Measures outside both kept middle halves.** The pick is outside both on 13: step 0.597 (high), turns per move 0.692 (high), longest run one way 2 (low), on the third 0.324 (high), on the fifth 0 (low), peak position 0.75 (high), time in the top third 0.057 (low), on the downbeat 0.235 (high), on beats 2 and 4 0.147 (low), quarter gaps 0.333 (high), spread of notes 2.14 (high), chord tones off the beat 0.824 (high), non-chord tones resolved by step 1 (high). The measures most often outside across the builds: peak position 100% (control 100%), time in the top third 57%, eighth gaps 56% (control 40%), on beat 3 54%, low position 51%, turns per move 38%, on the fifth 37%, spread 36%. The full table is in the test report.

## Report 2: deaths per gate, with the control

| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |
|---|---|---|---|---|
| monotony run (196) | 122 | 128 | 122 | 129 |
| bridge above the verse (208) | 50 | 92 | 52 | 91 |
| rhythm: no placement | 41 | — | 40 | — |
| join before a copy (212) | 32 | — | 23 | — |
| join before a line (212) | 25 | — | 26 | — |
| leaps: tritone or past an octave | 20 | 20 | 27 | 27 |
| spectral (Table B) | 19 | — | 41 | — |
| returns related, on lines (181/219) | 11 | 25 | 27 | 45 |
| realness (Table B) | 9 | — | 17 | — |
| bridge opening unrelated (208) | 8 | 13 | 10 | 18 |
| cmp (Table B) | 7 | — | 1 | — |
| key word on a chord tone (134) | 3 | 6 | 3 | 4 |
| surprisal (Table B) | 0 | — | 1 | — |
| align: the words do not fit | 0 | — | 1 | — |
| summit (216), register (133), tritone from the root (215), pitch and rhythm bands, pushed notes, density, sequence legs, note lengths (206) | 0 | 0–1 | 0 | 0–1 |
| **Survivors** | **153 of 500** | | **109 of 500** | |

**The instrumental hook (209).** 2,506 distinct one-bar figures drawn from the pop rhythm table; 214 passed the lead gates. The pick: A4 E5 B4 A4 over A, on the 'and' of 1, beat 2, its 'and', and the 'and' of 3; chord tones on the beat 100%; unrelated to the vocal hook (onsets 0.17, contour 0.79). It plays in 26 slots: the intro, the holds after chorus lines, the outro. **The solo:** 16 bars; chord tones on the beats 80%, no tritone against a root, rhythm 1.92 bits (inside the pop band), largest leap 11 semitones; the first draw passed. No corpus on file separates instrumental figures from the voice, so 209 has no kept figure behind it.

## Report 3: which fixes ran, and the paper's tests

| Fix | Ran? | The paper's test | Song 37 |
|---|---|---|---|
| 224 | yes | targets drawn and recorded; median distance inside 0.133–0.228; under one build in ten too central | recorded for all 500 builds; median 0.089; 45% too central: **fails** (225) |
| 212 | yes | join deaths under one in ten; survivors near the control's | 57 (11.4%); survivors 153 against the control's 109: **fails narrowly** (229) |
| 213 | yes, at intake | builds repeat the opening unit at once in 15–30% of windows; nothing gates the pick | 28%: passes |
| 214 | yes | medians within three points of 69% and 62%; 198 still passes | 74% and 65%: **5 points high** on the beat (231); intervals 28.7 / 43.5 / 1.8 against targets 27.3 / 44.2 / 1.8 |
| 215 | yes | no survivor holds a tritone from the root | none: passes |
| 216 | yes | every summit on a beat over a chord that holds it | bars 27, 35, 55, 63, 95, beat 1, over D: passes |
| 217 | yes | the hook returns on its own chords; every chorus's last line on the tonic | passes |
| 218 | yes | three held lengths; eighth gaps inside 27–62%; longest over median varies between 2 and 4 | ends 24 ×14, 18 ×17, 12 ×8; eighth gaps median 63%, **above** (227); longest varies 1.5 · 3 · 4 |
| 219 | yes | no build dies at 181 where construction was used | 11 died, all on contour: **fails** (230) |
| 220 | yes, at intake | multiples of four; bar-window returns at or above 31% | all multiples of four; returns third in 39% of windows (song 36 v3: 1%): passes |
| 221 | yes | 210 on 46 measures from the file | yes |
| 222 | yes | the spread printed; the pick inside the middle half, or the report says not | 2.14, just above 2.12: says not |
| 223 | yes | 194's four words pass | 'someday', 'somewhere', 'July', 'radio', 'microwave' one stress each away from a line's end: passes |
| 202, 208 | yes, at intake | the questions print the kept figures | yes (31% in the song; the bridge's 94%, 68%, 46%, 14%, 0.97) |
| 192 | not applicable | — | a band song |

**What the tables did not carry:** the chart songs' own count of measures outside both middle halves (232); the share of eighth-note gaps in windows as dense as this lyric's (227); a corpus of instrumental figures (209).

## Blind-pick tally

| Slot | Picks |
|---|---|
| Annotated top | 9 |
| Remembered top | 8 |
| Middle | 7 |
| Refrain | 1 |
| Songs picked | 25 |

Song 37: the Remembered top, "I'm hollering home with all I've got." The slots were "Noon, and my shadow's under my boots" (Annotated top), "Windows down till the oil smell's gone" (Middle: top quartile under both regimes) and the line picked (Remembered top), offered in shuffled order. The pick is the line that carries the summit, the F♯4 on 'HOL-lering'.
