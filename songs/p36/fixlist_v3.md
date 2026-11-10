# ZenEng fix list after v95

*Song 36, version 3 · fixes 212–223 · with the readings the brief asked for, the deaths per gate, which fixes ran, and the paper's tests*

v95's version row (v129) ends at fix 211, checked before numbering. This list starts at 212 and covers every song since v95: one, song 36 rebuilt as version 3. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

The brief, as the writer relayed it: rebuild song 36's music under ZenEng v95 on the locked lyric (draft 5) and the same form plan; read the tables, don't refit; port 201, 199, 206, 205, 208, 209, 194–198, 200, 202, 203, 195 and 210–211 before the search, in that order; ask two questions (the bridge, the summit); run a control with 199, 201, 205 and 206 off; report the readings; push the code with the seed; number findings from 212.

## Songs since v95

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 36, version 3 | Dance Anyway | v95's ports on a finished lyric: the line span from syllables (201), the chord in the walk (199), a small stock of note lengths (206), say it twice (205), the bridge's job (208), the instrumental hook (209), 194–198, 200, 202, 203, 195, and 210–211 as readings. Disco-pop, E♭ major, ♩ = 118, female voice B♭3–D5; the form grew from 88 bars (2:59) to 99 (3:21). Writer's answers: the bridge lifted above the verse; the summit D5 on chorus line 6's last word in every chorus. One control (199, 201, 205, 206 off). | 212–223 |

## The fixes

### 212. 206's held end and breath kill the lines that come back

**Problem:** 206 holds a line's last note one of two lengths and 201 keeps a breath after it, so a line needs about a beat and a half between its last onset and the next line's first. A line that returns (a repeated verse, a chorus copy, a returning unit) brings its source's pickup with it, and the line before it is built without knowing that pickup is coming.

**Evidence:** Version 3 lost 234 of its 500 builds (47%) at that join, the largest single cause; the control, with 206 off, lost none there. Survivors fell to 55 (11%) from the control's 130.

**Fix:** When the next line is a copy, build the line before it knowing the copy's first onset: its last stress and held end placed so the hold and the breath end before the copy's pickup (or the copy's pickup cut by one syllable where the words allow). No new gate.

**Check:** With 206 on, join deaths under 10% of builds; survivors back near the control's share.

### 213. "Say it twice" is drawn where the reading cannot see it

**Problem:** 205 draws AABC and AAAB plans where a section's first two lines are within three syllables, and asks that one section open by repeating its first unit. In song 36 only the chorus head (6 and 9 syllables) and the pre-chorus qualify; verse and bridge lines differ by 4 and 5. The pre-chorus was made to open AA, but the reading counts verse and chorus 8-bar windows only, and AABC choruses survive the gates yet rank low on the composite.

**Evidence:** The opening unit repeated at once in 7.3% of verse and chorus windows across builds (test: 15–30%); any such window in 16% of builds; 1 of 55 survivors had an AABC chorus, at rank 27; the pick 0% (kept 17–28%; version 1 was 1%; the control 0%).

**Fix:** Three choices for the paper. (a) At intake, when the lyric is still open, 205 asks for one verse or chorus whose first two lines are within three syllables. (b) Count a pre-chorus that opens AA in the reading. (c) Make "one section opens so" a gate on the pick where the lyric allows it, so the rank of record chooses among builds that meet it.

**Check:** Builds inside 15–30%; the pick has one verse or chorus window that repeats at once whenever the lyric allows.

### 214. 199's chord term needs one draw over every candidate

**Problem:** 182's walk draws an interval category first (repeat, step, third, …) and a pitch inside it. 199's chord term can only choose within the category already drawn, so it rarely reaches the beat: from E♭ a step offers F or D, and neither is in E♭.

**Evidence:** Weights of 100 to 0.01 on the beat left on-beat chord tones at 48% of builds (with the base weight, 52%). With one draw over every candidate, each category's weight tilted by the chord it offers (its weight with the chord term over its weight without), chord tone to other at 2.5 : 0.38 on the beat and 5.0 : 1.0 off it, the builds landed at 71% on and 64% off (chart 69% and 62%), and the interval shares stayed within two points of Table CG (28.5%, 41.0%, 3.2% against 27.6%, 42.6%, 3.0%).

**Fix:** Write 199 as the joint draw, with the calibration on the finished melody (as 198 does for intervals): the weights set so the builds' medians meet the chart's on-beat and off-beat shares.

**Check:** Builds' medians within three points of 69% and 62%; 198's test still passes.

### 215. A scale tone a tritone from its chord's root

**Problem:** 200 keeps ♭3 and ♭7 off a tritone from the root, but nothing keeps a diatonic tone off it: D over A♭ (the scale's 7th over IV) and G over D♭ (over ♭VII) pass every gate.

**Evidence:** In the first version 3 picks: the summit D5 on 'twelve' held a half over A♭; a D4 slur held a half over A♭; G4 held over D♭; four such notes in a later pick, all in copied lines. All passed the gates.

**Fix:** Extend 200 to every sung pitch class: no note a tritone from its chord's root on a beat or held a quarter or longer. The walk skips them; a copied note moves a step to a chord tone.

**Check:** No survivor has such a note (version 3 after the change: none in any survivor).

### 216. A summit placed at intake sets the chord under it

**Problem:** The writer put the D5 on the last word of chorus line 6. The chord plan put that word over A♭, where D is a tritone from the root, and the line's rhythm let it fall off the beat. 202 places the summit but reads neither its chord nor its beat.

**Evidence:** 42 builds died at the summit gate before the line was given a cadence rhythm (its last stress on a beat in its last bar) and its second chord moved from A♭ to B♭ (V); the control, without the cadence rhythm, lost 115 there. After the change the D5s land on beat 2 of bars 31, 63 and 90, over B♭.

**Fix:** When the summit is placed at intake, the engine reads the chord under the chosen word and, if it does not hold the summit pitch, moves that bar to a chord that does (or asks); the summit's line takes the cadence rhythm.

**Check:** Every summit lands on a beat over a chord containing it.

### 217. A returning tune in a line of another length (201 with 181)

**Problem:** 201 gives a line its span from its own syllables, but 181 copies a tune with its source's span. Two cases in song 36: the last chorus's last line ('I'm still here, so I dance anyway') has three bars where the hook it returns has two; and chorus line 8 copies line 4's tune, so it lands where line 4 lands (beat 3 of its middle bar), over ♭VII, instead of in its last bar on I.

**Evidence:** The control lost 78 builds at "no room before the hook". In version 3 the hook was placed a bar later, keeping its place in its own bars, and the chords under that line re-laid (D♭ under 'I'm still here', E♭ under the hook). Chorus line 8 holds B♭4 over D♭ and the band lands on E♭ a bar later.

**Fix:** A copy keeps its place counted from the end of its line (its last bar), and the chords under a returning tune follow it; a section's last line keeps 201's cadence (last stress in its last bar) even when it is a copy, by moving the copy, not the chords.

**Check:** Every return of the hook lands on the chords it was written on; every chorus's last line lands on I.

### 218. 201 and 206 together leave the voice in eighth notes

**Problem:** At about five syllables a bar, with no sixteenths and two held line-end lengths, the median note is an eighth in every window; the longest/median ratio is then fixed by the held end.

**Evidence:** Longest over median 4 in every build (5th, median and 95th all 4; kept 3); 76% of the pick's notes are eighths; different lengths per 8 bars 3–4–4 (kept 4).

**Fix:** The paper chooses: hold line ends a dotted quarter only (ratio 3), or let 201 count about four syllables a bar so quarters can be the median. The chart's share of eighth-note medians is not on file and would decide it.

**Check:** Longest over median inside 2–4 with some builds at 3; lengths per 8 bars still at most five.

### 219. The line reading needs its anchor

**Problem:** 195 has the 181 gate read lines. Counted from each unit's own first onset, a sung repeat that adds or drops a pickup fails: its onsets shift by the pickup and the contour is compared out of step.

**Evidence:** With that anchor, 20 of 21 AABC choruses failed their own repeat (onset overlap 0.5). Counting onsets and contour from each line's own downbeat, 4 of 500 builds died at 181.

**Fix:** State 195's anchor: a line unit is read from its line's first downbeat; the pickup's onsets count, the contour starts at the downbeat.

**Check:** No build dies at 181 where its construction was used. (Version 3: 4 still did, where the summit or the tritone repair changed a copied note after construction; 216 and 215 should place those notes before the copy is made.)

### 220. The 8-bar stock reading under uneven spans

**Problem:** 195's test asks 27.31's bar-window 8-bar stock share to stay at or above 39%. With three-bar lines (201), 8-bar windows no longer fall on phrase boundaries, so the stock designs cannot be found.

**Evidence:** The pick 0%; builds median 0% (mean 7.6%); the control (two-bar lines) 33%.

**Fix:** Where 201 gives a section uneven spans, read 27.31's designs on phrase windows (whole lines) and print both readings; drop the 39% floor for those sections.

**Check:** The report prints the phrase-window and bar-window design readings side by side.

### 221. 210 cannot be computed from the tables on file

**Problem:** 210 reads 46 discriminator measures. The tables print 11 numeric measures with chart quartiles (Table CU) and two repetition shares. A distance on 11 measures is not the paper's distance.

**Evidence:** On the 11: the pick 0.031 (TOO CENTRAL beside 0.086–0.351), builds 0.012–0.052–0.137, the control's pick 0.441 (FAR), its builds' median 0.518. 199, 206 and 198 aim the run at Table CU's medians, so on those 11 the run is central by construction.

**Fix:** Print all 46 measures with both corpora's quartiles (Table CU in full), so 210 and 204 can be run; until then the report labels the distance partial.

**Check:** 210 computed on 46 measures, with the chart range beside it.

### 222. The bar-to-bar spread is above the kept range (207)

**Problem:** With held ends and three-bar lines, some bars hold one long note and the next is packed with eighths.

**Evidence:** Spread (standard deviation of onsets a bar) 2.23 in the pick, outside the chart's middle half (1.20–1.62–2.12) in 6 of its 8 windows; builds 1.48–1.87–2.28; the control 2.60.

**Fix:** A reading only, as 207 has it; 212's planned line ends and 218's choice should bring it in. If not, a default that spreads a three-bar line's syllables across all three bars.

**Check:** The pick's spread inside the chart's middle half.

### 223. 'somewhere' is still read with two stresses (194)

**Problem:** 194's test names 'somewhere' among the words that carry one stress; the stress reading still gives it two (a compound: some + where).

**Evidence:** The reading: July (one), radio (one), microwave (one), somewhere (two). 'anyway' at a line's end carries its first and last.

**Fix:** Compounds of two monosyllables take the primary on the first part only, except at a line's end.

**Check:** 194's test passes on its four words.

## Order of work

1. **212** (line ends before copies) and **217** (copies in lines of other spans): together they decide whether 201 and 206 can run without halving the survivors.
2. **214** (the joint draw for 199) and **215** (no tone a tritone from the root): one change to the walk.
3. **216** (the summit's chord and beat): wording at intake, plus the cadence rhythm.
4. **213** (say it twice): the paper chooses (a), (b) or (c).
5. **218** (the eighth-note median): the paper chooses.
6. **219**, **220** (the line reading's anchor; the stock reading under uneven spans).
7. **221** (Table CU in full), **222** (a reading), **223** (a stress rule).

## Regression line

After these fixes, song 36 version 3 rerun at N 500, seed 20261473, PYTHONHASHSEED 0 must: reproduce its frozen order twice; keep the builds' chord tones within three points of 69% on the beat and 62% off; keep sixteenth gaps at 0% and lengths per 8 bars at most five; keep the interval medians within two points of Table CG; keep the bridge related to neither opening and its median above the verse's; keep every D5 on a beat over B♭; lose under 10% of builds at joins; and pass 49 of 49 consistency checks. The control (199, 201, 205, 206 off) must still read 29% sixteenth gaps and 7–8 lengths per 8 bars, so the comparison stands. The composite again could not tell the pick (0.862) from the control's first pick (0.879): it stays the rank of record (211) and nothing more.

## Report 1: the readings the brief asked for

**The search.** N 500, seed 20261473, PYTHONHASHSEED 0, code 9a1169b02f02, Python 3.13.18, numpy 2.5.3, tables 561355b1110d1d8e…. 55 survivors (11.0%); reproduced exactly on a second run, frozen order 0256c9241d20. Pick 374966ffc8d9, first by the rank of record (composite 0.862); no hand edits. Plans: verse ABAB, pre-chorus AA, chorus A B C D A' B' C' D', bridge ABCD. Form 99 bars, 3:21 (third bars: verse lines 2 and 4, chorus lines 4 and 8, bridge line 2).

**The control.** Same seed and N, with 199, 201, 205 and 206 off (88 bars, two-bar lines, a sixteenth grid, free line ends, version 1's chord term and plans); everything else on. 130 survivors, order bb074ba2bb43; first pick 9459945b6685 (composite 0.879).

Builds are every song the generator finished, before the gates.

| Reading | Pick | Builds 5th · median · 95th | Control's pick | Control's builds (median) | Kept / chart | Version 1 |
|---|---|---|---|---|---|---|
| Chord tones on the beat | 79% | 62% · 71% · 81% | 62% | 63% | chart 69% (pop 72%) | — |
| Chord tones off the beat | 52% | 53% · 64% · 73% | 43% | 45% | chart 62% | — |
| All notes on chord tones | 66% | — | — | — | chart 54–65–76% | 40% |
| Sixteenth-note gaps | 0% | 0% · 0% · 0% | 29% | 29% | pop 2% | 38% |
| Longest note over the median note | 4 | 4 · 4 · 4 | 7.75 | 9.25 | kept 3 (chart 2–4) | 9 |
| Different note lengths per 8 bars | 4 | 3 · 4 · 4 | 7 | 7.5 | kept 4 (chart 3–5) | 7 |
| Opening unit repeated at once, share of windows | 0% | 0% · 0% · 38% | 0% | 0% | kept 17–28% | 1% |
| Stock designs, 8 bars | 0% | 0% · 0% · 47% | 33% | 33% | — | — |
| Stock designs, 16 bars | 0% | 0% · 0% · 0% | 100% | 100% | — | — |
| Pitch surprise (bits a note) | 2.82 | 2.65 · 2.85 · 3.03 | 2.99 | 2.84 | chart 2.53–2.74–3.03 | — |
| Repeated notes | 25% | 22% · 28% · 35% | 24% | 22% | pop 27.6% | 23.7% |
| Steps | 42% | 33% · 41% · 50% | 52% | 53% | pop 42.6% | 47.3% |
| Leaps past a fifth | 3% | 1% · 3% · 7% | 4% | 3% | pop 3.0% | 1.3% |
| Exact bar repetition | 53% | 52% · 57% · 62% | 53% | 53% | — | — |
| Spread of notes bar to bar | 2.23 | 1.48 · 1.87 · 2.28 | 2.60 | 2.37 | chart 1.20–1.62–2.12 | — |
| Bridge median over the verse's (semitones) | +2 | 0 · +3 · +7 | +5 | +2.5 | kept +2 (68% above) | — |
| Bridge onsets a bar over the verse's | 1.02 | 0.96 · 1.04 · 1.09 | 0.88 | 0.92 | kept 0.97 (0.78–1.21) | — |
| Bridge opening related to the verse's / chorus's | neither (contour −0.61 / −0.66) | either in 12% of builds | neither | 0% | neither 94% | — |
| Distance from the centre (partial, 11 of 46) | 0.031, TOO CENTRAL | 0.012 · 0.052 · 0.137 | 0.441, FAR | 0.518 | chart 0.176 (0.086–0.351) | — |

## Report 2: deaths per gate, with the control

| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |
|---|---|---|---|---|
| join: no held end and breath before the line (206) | 234 | — | 0 | — |
| align: the words do not fit the returning unit | 69 | — | 0 | — |
| monotony run (166/196) | 61 | 65 | 31 | 41 |
| summit placed (the writer's A) | 29 | 56 | 115 | 151 |
| leaps: tritone or past an octave | 24 | 24 | 104 | 104 |
| bridge opening unrelated (208) | 9 | 22 | 0 | 2 |
| rhythm: no placement | 8 | — | 0 | — |
| returns related, on lines (181/195) | 4 | 9 | 14 | 36 |
| bridge above the verse (208) | 3 | 17 | 25 | 78 |
| spectral (Table B) | 3 | — | 3 | — |
| cmp (Table B) | 1 | — | 0 | — |
| align: no room before the hook | 0 | — | 78 | — |
| key word on a chord tone (134) | 0 | 0 | 0 | 2 |
| note lengths at most 5 per 8 bars (206) | 0 | 0 | 0 (not gated) | 422 |
| register, pitch band, rhythm band, pushed notes, density, sequence legs | 0 | 0 | 0 | 0 |
| **Survivors** | **55 of 500** | | **130 of 500** | |

"Would fail" counts every build that finished, whatever killed it first. The control's 422 builds over five lengths are what 206 prevents by construction.

**The instrumental hook (209).** 2,513 distinct one-bar figures drawn from the pop rhythm table; 199 passed the lead gates (rhythm in the pop band; chord tones on the beats ≥ 60%; no semitone against a held sung note; nothing under G4; no tritone or flat ninth against a root). Deaths: tritone against a root on a beat 992; semitone against a held sung note 461; under G4 354; rhythm band 338; chord tones on the beats 115; no turn 51; related to the vocal hook 3. The pick: E♭5 C5 G5 B♭5 E♭5 over E♭, onsets on 1, 1e, 1&, 2&, 3&; chord tones on the beat 100%; 80% of its notes off the beat; unrelated to the vocal hook (onsets 0.29, contour −0.17); seed 20261474. It plays 19 times (intro, the holds after chorus lines, outro), never over a sung onset. No corpus on file separates instrumental figures from the voice, so this rule has no kept figure behind it.

## Report 3: which fixes ran, and the paper's tests

| Fix | Ran? | How | The paper's test |
|---|---|---|---|
| 201 | yes | spans from syllables; eighth grid; cadence rhythm for a section's last line and the summit's line | sixteenths 0%; final note 4× the median; third bars named: passes |
| 199 | yes | the joint draw (214), 2.5 : 0.38 on the beat, 5.0 : 1.0 off | all notes 66% on chord tones (middle half 54–76%); key-word deaths 0 (version 1: 42): passes |
| 206 | yes | eighth onsets; line ends a half or a dotted quarter, then an eighth's breath | at most 4 lengths in any 8 bars; ends 24 ×27, 18 ×13; longest 4×: passes |
| 205 | yes | AABC/AAAB at about one in five where admissible; the pre-chorus opens AA | 7.3% of windows across builds: **fails** (213) |
| 208 | yes | register above the verse; opening gate on lines; median gate; pace printed | related to neither; +2 semitones; onsets 1.02: passes |
| 209 | yes | a one-bar figure searched against the pick | unrelated; never over a sung onset; intro, choruses, outro; no corpus figure stated: passes |
| 194 | yes | the stress reading | 'somewhere' carries two: **fails** (223) |
| 195 | yes | the 181 gate on lines, anchored at the line's downbeat (219); bar windows kept for 27.31 | 4 deaths at 181; 8-bar stock 0%: **fails** (219, 220) |
| 196 | yes | the run clause only | monotony deaths from the run clause; two-pitch lines 0%: passes |
| 197 | yes | a turn back after a leap past a fifth | the pick none; 2 of the 40 inspected survivors, in copied lines |
| 198 | yes | the draw aimed (repeat ×0.95, step ×1.35, third ×0.8, larger ×1.6) | 28.5%, 41.0%, 3.2%: passes |
| 200 | yes | ♭3/♭7 rule, extended to every tone a tritone from the root (215) | none in any survivor: passes |
| 202 | yes | the summit at intake with chart pop's 31% beside the options; three D5s on beats over B♭ (216) | passes |
| 203 | yes | 192 not applicable (a band song) | passes |
| 204 | partly | Table CU's chart quartiles only; the grid corpus's are not on file | outside the chart's middle half in the pick's 8 windows: spread 6, fourths and fifths 4, chord tones on the beat 3, off the beat 3, mean interval 3, pitch surprise 2 |
| 207 | yes | a reading | 2.23 against 1.20–1.62–2.12 (222) |
| 210 | partly | 11 of 46 measures | 0.031, TOO CENTRAL (221) |
| 211 | yes | the composite as the rank of record | — |

**What the tables did not carry:** the 46 discriminator measures and their quartiles in both corpora (210, 204); the chart's share of eighth-note medians (218); a corpus of instrumental figures (209).

## Blind-pick tally

| Slot | Picks |
|---|---|
| Annotated top | 9 |
| Remembered top | 7 |
| Middle | 7 |
| Refrain | 1 |
| Songs picked | 24 |

No new pick for version 3: the lyric is unchanged, and draft 5 offers the same three lines as version 1's pick (Middle: "by the green of a clock stuck on twelve").
