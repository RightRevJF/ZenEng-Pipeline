# ZenEng fix list after v109

*The port test (song 40 again) and song 41, The Water Used to Sing · fixes 310–319 · with the runs, the tests of 298–309 and the readings the paper does not give*

v109's last fix is 309 (Window 129). This list starts at 310 and covers everything since v109:

- **The port test.** Fixes 298–309 ported onto song 40's default-path search and run again (findings 310–313).
- **Song 41, *The Water Used to Sing*.** A new default-path song in a different feel: a swung shuffle (findings 314–319).

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Nothing blocked the port, and no two fixes conflicted.

## Songs since v109

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 40 (port test) | Nothing Else on Earth | v109's 298–309 ported onto song 40's default path. 1,000 builds main and 1,000 control (243 off), each twice. Survivors 476 and 398; both orders reproduced. | 310–313 |
| 41 | The Water Used to Sing | v109 on the default path in a new feel: Americana swung shuffle, ♩ = 96, G major, male baritone (G2–E4 sounding). Verse, pre-chorus, chorus, bridge, break, a third verse. Mixed line lengths up to 12 syllables. No era, character, summit, chorus lift or drum design; said twice in the chorus. Off the default path, named: the bridge below the verse (Q16 B, a design gate), the countermelody in the last chorus only (Q18 B, arrangement), and the slots (Q20 A: 230 failed by design, the form grown to 104 bars because 308 needs two bars for every 9+ syllable line). 1,000 main and 1,000 control, each twice. Survivors 615 and 660; both orders reproduced. The record is 255's pick, with no hand edits. | 314–319 |

## The tests of 298–309 (the port, on song 40)

| Fix | Result | Held? |
|---|---|---|
| 298 | Title line above the verse in 58% of builds (kept 56%) | printed |
| 299 | Under the floor 33.6% (v108 26.5%) | **no** (310) |
| 300 | Realness out of the count, printed beside the kept chart figures | yes |
| 301 | The eight: 92.0% of kept songs; the six: 94.2% of the pairs (no refit) | yes |
| 302 | No last note moved (v108 207); last chorus on the tonic 96.6% | moves yes; tonic **no** (311) |
| 303 | Verse 2 shares 25–75% in 50.3% of builds | **no** (313) |
| 304 | Turns per move dropped in the chorus | yes |
| 305 | Arch over the span 0.155 at the median; amplitude 13.2, no cap | yes, at a cost (312) |
| 306 | Last note over the mean 1.54 (inside 1.18–1.71) | yes |
| 307 | The top note read beside the kept | printed |
| 308 | Fullest bar 0.533 at the median | yes |
| 309 | Every file a run reads committed; a clone reproduces the order | yes |

On song 41: 309 held (all 42 files the search reads are committed, listed in songs/p41/reads_melody_p41.txt). 308 held but costs tries (316). 305 again ran up to its clip (315).

## The fixes

### 310. 308 lays the line across its bars, and the floor kills more builds, not fewer.

**Problem:** Window 129 predicted deaths at the floor falling to 8% (main) and 5% (control) once a long line is laid across its bars.

**Evidence:**

- Under the floor 33.6% and 41.6% (v108 26.5%, 21.3%); deaths 218 and 287 (v108 164, 141).
- The content judge rose as predicted (median −0.716 from −1.295), but the order judge fell (median −0.016 from 1.002).
- Bars 4 and 8 are no longer thin (thin_48 0.333 from 0.667, kept 0.604), and the barline is less smooth (−1.241 from −0.807).
- The packed lines had left the even bars nearly empty, which the order judge read as phrasing.

**Fix:** a line that ends a four-bar unit ends by beat 3 of bar 4 or 8, so the unit keeps its breath. Or refit the judges on builds made with 308.

**Check:** deaths at the floor under one build in ten; thin_48 inside the kept middle half.

### 311. 302 ends the moving, but the last chorus misses the tonic in one build in thirty, silently.

**Problem:** where the drawn chorus register holds no tonic, no permitted ending can be drawn and the fallback finds none.

**Evidence:**

- No last note moved (0 of 1,000; v108 207).
- Yet the last chorus ends on the tonic in only 96.6% of main's builds and 96.7% of the control's.
- Every miss is a hook (whose tail the tag copies) drawn in a register without a D.

**Fix:** let the ending line take a permitted degree one step outside its register, or make the register draw keep one. Count the misses.

**Check:** the last chorus on the tonic in every build.

### 312. 305 meets its test by widening leaps.

**Problem:** with the cap gone the amplitude rose to 13.2, and the calibration still read 0.117 against 0.23 at its last round.

**Evidence:**

- The arch over the span is 0.155 at the median (inside the kept 0.00–0.55).
- Leaps past a fifth in the verse window rose from 0.024 to 0.05 at the median (the judge's kept mean is 0.021) and became a content give-away.

**Fix:** draw the arch through the walk's direction (steps toward the contour) rather than a larger contour, or hold leaps past a fifth to the kept rate.

**Check:** past_fifth at the kept median with the arch over the span at 0.23.

### 313. Verse 2 still copies too few bars, and 308 gives up more copies.

**Evidence:**

- Verse 2 shares 25% of verse 1's bar rhythms at the median, with one onset's difference allowed; in range 50% of builds (control 61%).
- The copy was given up for 477 lines, against 31 under v108. The cap of 308 and the copied bars both draw on the same rhythm.

**Fix:** choose the copied bars among those the line's cap allows, before the draw.

**Check:** verse 2's share inside 25–75% in three builds of four.

### 314. The verse's place in the voice row decides the song's register, and the paper doesn't give it.

**Problem:** 288 draws the chorus and bridge registers against the verse's. The verse's centre, cap and floor are the session's numbers (song 40: E4, A4, A3; song 41: E3, A3, A2). On song 41 they put the whole song in the row's low octave.

**Evidence:**

- 98.5% of main survivors (100% of the control's) touch G2, the row's floor.
- The top note is A3 at the median; 54% never go above A3, and only 14% reach the row's top, E4.
- The pick spans G2–A3 (14 of the row's 21 semitones), its chorus top 3 under the verse's (36% of survivors have a chorus top under the verse's).
- The bridge-below design (Q16 B) and the hook's tonic ending (262/302) both press toward the floor.

**Fix:** count where the verse sits in the singer's row in kept songs (its median and top as shares of the row), and draw the verse register from that per build, as 288 draws the rest.

**Check:** the survivors' highest and lowest notes against the kept shares, and the row's top fifth used in about the kept share of builds.

### 315. 305's amplitude is set by its clip, not by its reading (312, worse).

**Problem:** the calibration multiplies the arch amplitude by at most 1.6 a round. On song 41 it took the full 1.6 every round in both runs: 5 × 1.6³ = 20.48.

**Evidence:**

- The reading at the last round was 0.132 against the aimed 0.23; the survivors' arch over the span is 0.161 at the median.
- Leaps past a fifth in the verse window are 0.119 at the median (judge's kept mean 0.021; song 40's port 0.05).
- The pick has ten leaps past a fifth inside lines, one a minor seventh up onto an unstressed syllable.

**Fix:** as 312, draw the arch through the walk's direction. Or stop the calibration and report it when two rounds running hit the clip.

**Check:** the amplitude settles before its clip; past_fifth at the kept median with the arch over the span near 0.23.

### 316. 308's cap costs about four tries per long line.

**Problem:** with the entry and landing drawn first (231, 260), a 12-syllable line in two bars capped at 6 a bar has very few placements. Most draws find none.

**Evidence:** 37,711 long-line redraws in 1,000 main builds (about four per long line), and 99 lines placed with a free entry and landing. Only 7 builds died at placement.

**Fix:** for a line of 9 or more syllables, draw the entry and landing only from those that admit the cap.

**Check:** redraws per long line under 1.5, with the entry and landing shares unchanged.

### 317. A design gate read on a sung median passes under nine builds in ten (275).

**Problem:** the bridge is aimed 1.5 to 5 semitones under the verse, but the walk's median drifts, and the gate reads the sung medians.

**Evidence:** the bridge-below gate killed 14.4% of main builds and 9.8% of the control's, under 275's nine in ten. It was the largest killer in main.

**Fix:** read a register design on the drawn register (the aim) and print the sung reading. Or say that a design gate stands outside 275 and print its pass rate before the run.

**Check:** a design gate's pass rate printed before the run, and under one build in ten lost to it.

### 318. A swung shuffle draws sixteenths at straight pop's rate.

**Problem:** the class's rhythm table and 288's sixteenth offer (14.7%) come from straight-eighth pop. In a swung feel the sixteenth is rare and awkward, because the swung eighth already fills the beat.

**Evidence:**

- 16.7% of the pick's inner gaps are sixteenths; the survivors' median share of onsets on sixteenth positions is 12%.
- The page is written straight under a swing mark, so the singer meets sixteenth pairs inside a shuffle.
- The paper has no reading for swing; the playback ratio (2:1) was the session's.

**Fix:** add a feel at intake (straight or swung). Under swing, the grid is the triplet eighth, and the sixteenth share comes from kept swung songs (to be counted).

**Check:** the sixteenth share in swung builds at the kept swung rate.

### 319. The break solo's octave repair can climb out of the instrument.

**Problem:** song 38's solo method folds each note toward the one before by octaves, and a run of folds can cascade upward.

**Evidence:** song 41's first solo reached A6 (MIDI 93), past a 24-fret guitar's top E6. The solo check (chord tones, tritones, rhythm band, leap) passed it. The session folded the solo to C6 at most and added a range check (top B5).

**Fix:** the solo check (and every instrumental line's check) reads the instrument's range.

**Check:** no instrumental note outside its instrument's range.

## Order of work

1. **314** (the verse's place in the row): it decides the register of every default-path song, and on song 41 it put the whole song at the floor.
2. **312 and 315** (the arch through the walk): the same mechanism twice, and now the largest content give-away.
3. **310** (the floor after 308): the even bars' breath.
4. **317** (design gates under 275) and **316** (draw the long line's entry and landing within the cap).
5. **311** (the tonic in every build), **313** (verse 2's copies within the cap).
6. **318** (a feel at intake; count swung songs) and **319** (instrument ranges).

## Regression line

After these fixes, both songs rerun at PYTHONHASHSEED 0, N 1000, main and control, and each must reproduce its frozen order twice. The orders will change with the code. Today's:

- Song 40 (v109 port, seed 20261511): main 6ad97e7695d1, control 4974bb2f8af1.
- Song 41 (seed 20261521): main 615aa4e7f73d, control 83c59a365e29.

Song 41 must keep:

- the locked lyric, every syllable sung, and no never-say word, with 'living water' once;
- chorus 2 = chorus 1, and the hook said twice in the chorus;
- the hook ending on the tonic, and the tag 'It sings.' the hook's last two notes on the tonic;
- the bridge under the verse;
- every 9+ syllable line in two bars;
- all 44 consistency checks.

After 310–319, song 41 should also:

- use the row's top fifth at the kept share;
- read past_fifth at the kept median, with the amplitude settled before its clip;
- need under 1.5 redraws per long line;
- lose under one build in ten at the design gate;
- draw sixteenths at the swung rate once a feel is asked;
- keep every instrumental note in range.

The regression lines of songs 38 and 40 from the lists after v107 and v108 stand beside it.

## Reports

- **Song 41 runs:**
  - Main: 615 of 1,000 survived (order 615aa4e7f73d).
  - Control: 660 of 1,000 (order 83c59a365e29).
  - Both reproduced on the second making. Code 2cb5717c5b99; seed 20261521, calibration 20261522.
- **Deaths, main:**
  - Bridge-below design gate: 144.
  - Limits: 142.
  - Bridge opening unrelated: 48.
  - Judge's floor: 17.
  - Key word on a chord tone: 11.
  - Placement: 7; align: 5; join: 4; walk: 4.
  - Chorus opening another tune: 3.
- **The pick:**
  - 4767e10a1dce, fourth by the composite (0.818), judge 2.241, no soft limit broken.
  - Lift: median 0, top −3, lowest −2; bridge −3.
- **Judges:** survivors' combined median 0.921 (main), 0.822 (control).
- **Documents:** lead sheet and six parts read back from LilyPond's MIDI; 1,064 of 1,064 drum hits written. The demo's voice is +6.2 dB over the band, and the energy arc meets 9.12.

## Readings the paper does not give

**The port (on song 40):**

- **302.** The last note is drawn among the permitted degrees inside the line's register, weighted by its distance from the contour's end (sd 1.5 semitones). With none, the old move is tried and, failing, the line keeps its ending (counted).
- **303.** 'Within one onset' is the symmetric difference of the bar's onsets and its source's. An onset outside a copied bar's set is weighted 0.04, not barred.
- **305.** The arch over the span is the arch term divided by the line's pitch span (0 for one pitch), the median over lines. The amplitude is multiplied by 0.23 over the reading, clipped 0.6–1.6 a round, with no upper cap.
- **306.** The ratio is drawn from Table DJ's kept quantiles (0.867 to 2.298, linear between). A title note keeps 232's two beats.
- **308.** The cap is the whole part of 0.57 × the line's syllables, for lines of 9 or more, inside the rhythm draw. Melisma notes are not counted.
- **300/301.** The six read with the v108 spectral limits and the other five on the pairs; no refit needed (94.2%).

**Song 41:**

- **288.** The verse's centre E3, cap A3, floor A2 in a baritone row G2–E4 (see 314).
- **208 (Q16 B).** The design's aim: the bridge median 1.5 to 5 semitones under the verse's, drawn evenly. The gate is read on the sung medians.
- **230 (Q20 A).** Verses 1 and 2 share the slots 2-1-2-1-1-1; verse 3 and the bridge take two bars a line.
- **228/293.** Verse 3 is sung again from verse 1 (the paper names verse 2 only), its bars copied at 40% into longer slots.
- **213.** The last chorus's plan:
  - Lines 1–2 are copies.
  - Line 3 is a return of the hook (its second pass varied, the writer's note).
  - Line 6 is a return of line 5 or fresh, drawn.
  - Line 7 is a return of the chorus's last line or fresh, drawn.
  - The tag is the hook's last two syllables.
- **235.**
  - The lick from G3; fills from A3 to G5.
  - The solo held to C6 (319).
  - The countermelody's row G4–E5 and its rule: it moves where the voice holds and holds a chord tone where the voice moves.
- **236.** Brushes and sticks by section; sticks at verse 3's fifth bar.
- **200.** B♭ and F as the flat 3 and flat 7 in G.
- **Swing.** Played 2:1 in the demo only; the record and the page are straight (318).
- **Seed.** 20261521, the session's convention (20261110 + 411).

## Blind-pick tally

Songs 40 and 41's blind picks are offered after delivery. The tally stands at 27 songs until they are answered: Annotated top 11, Remembered top 8, Middle 7, Refrain 1.
