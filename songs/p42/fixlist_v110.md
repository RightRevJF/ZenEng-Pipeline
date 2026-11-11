# ZenEng fix list after v110

*The v110 port tested on song 40, and song 42, Nothing Important · fixes 322–328 · with the tests of 310–321 on both songs' own runs (321)*

v110's last fix is 321 (Window 130). This list starts at 322 and covers everything since v110:

- **The port test.** Fixes 310–321 ported onto song 40's default-path search and run again.
- **Song 42, *Nothing Important*.** A new default-path song in a straight feel: a piano ballad.

Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited. Nothing blocked the port, and no two fixes conflicted.

## Songs since v110

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 40 (port test) | Nothing Else on Earth | 310–321 ported. 1,000 main and 1,000 control, each twice. Survivors 505 and 537 (v109 port 476, 398); orders 3c9c4f2da558 and 30ba2486b5e4, both reproduced. | 322–324, 327 |
| 42 | Nothing Important | v110 on the default path in a straight feel: a piano ballad, ♩ = 76, B♭ major, alto (row F3–D5), 68 bars; the range centred in the row (314); the bridge drawn. Designs, named: every line two bars (230 by design); the last chorus's head, augmented tail and falling last line (a design gate, 317); the cello's countermelody and a complete solo piano part (arrangement). 1,000 main and 1,000 control, each twice. Survivors 567 and 595; orders 5614d9557a76 and 46d4320fd85a, both reproduced. Record: 255's pick, no hand edits. | 322–326, 328 |

## The tests of 310–318 on song 40 (the port)

| Fix | Main (control in the report) | Held? |
|---|---|---|
| 310 | under floor 25.8%; parallel 0.094 (kept 0.14); paired lines 4765, partner given up 1674 | **no** |
| 311 | tonic 100.0%; registers redrawn 240; misses 0 | yes |
| 312 | verse 0.0%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | share [0.0, 0.25, 0.455]; in range 53%; given up 10 (0.2%); left out 4805 | **no** |
| 314 | range [10.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.294, 0.429, 0.588]; tonic nearest 0.971; top fifth 74%; floor 38% | **no** |
| 315 | amplitude 5.0; arch [-0.106, 0.077, 0.273]; stop none | yes |
| 316 | redraws 0/13368 = 0.0; entries {'starts_on_downbeat': 0.23, 'starts_after_downbeat': 0.647, 'starts_as_pickup': 0.123} (before {'starts_on_downbeat': 0.224, 'starts_after_downbeat': 0.647, 'starts_as_pickup': 0.129}) | yes |
| 317 | none in force | yes |
| 318 | straight eighths; sixteenth onsets [0.097, 0.131, 0.179] | printed |

## The tests of 310–318 on song 42 (its own runs)

| Fix | Main (control in the report) | Held? |
|---|---|---|
| 310 | under floor 6.4%; parallel 0.188 (kept 0.14); paired lines 4083, partner given up 1474 | yes |
| 311 | tonic 81.3%; registers redrawn 202; misses 0 | **no** |
| 312 | verse 2.5%, chorus 0.0%; leap knob 1.0 | yes |
| 313 | share [0.0, 0.286, 0.625]; in range 71%; given up 1 (0.0%); left out 3287 | **no** |
| 314 | range [12.0, 16.0, 18.0, 21.0, 21.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.429, 0.571]; tonic nearest 0.972; top fifth 69%; floor 18% | **no** |
| 315 | amplitude 7.0; arch [-0.205, 0.052, 0.308]; stop none | yes |
| 316 | redraws 0/9472 = 0.0; entries {'starts_on_downbeat': 0.216, 'starts_after_downbeat': 0.644, 'starts_as_pickup': 0.14} | yes |
| 317 | {"design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)": 0.744} | **no** |
| 318 | straight eighths, q = 76; sixteenth onsets [0.079, 0.118, 0.17] | printed |

319: every instrumental note inside its instrument (song 42). 320: no figure here comes from a rescoring. 321: these tables. The full tables, main and control, are in the song's test report and in songs/p42.

## The fixes

### 322. Fix 310 holds where paired lines are alike and fails where they are not.

**Problem:** The partner's rhythm is copied bar for bar and kept only within one onset a bar; when the two lines' syllable counts differ, most copies are given up.

**Evidence:** Song 40: under the floor 25.8% (main) and 28.5% (control), down from 32% and 42% but over one in ten; likeness of bar rhythms 0.094 and 0.105 (kept 0.14); the partner given up for 1,674 of 4,765 paired lines (35%). Song 42 (all lines two bars, units of two lines): under the floor 6.4% and 5.0%, likeness 0.188 and 0.181: 310 held.

**Fix:** Where partners differ by more than one syllable, keep the partner's stressed onsets and draw the rest freely, without the one-onset check.

**Check:** On song 40, partners given up under one in ten and likeness at or above 0.14.

### 323. Fix 313 leaves out the bars a copy most needs.

**Problem:** A source bar with more onsets than the line's cap is left out of the copy entirely.

**Evidence:** Song 40: 4,805 bars left out, verse 2 in range 53% (control 66%); song 42: 3,287 left out, 71% (84%). Test: three builds in four.

**Fix:** A source bar one onset over the cap is copied with its weakest onset dropped (303's one-onset allowance), not left out.

**Check:** Verse 2 inside 25–75% in three builds of four.

### 324. 314's tonic ending is aimed at the drawn register and read on the sung median.

**Evidence:** The tonic nearest the section's sung median in 97.1% (98.6%) of song 40's builds and 97.2% (98.1%) of song 42's.

**Fix:** Aim the ending at the median of the section's notes already placed, or read the test on the drawn register's centre; state which.

**Check:** 100% on the reading the paper names.

### 325. 311 holds the register's tonic but not a design's ending.

**Problem:** Song 42's design asks the last line to end on a tonic under the hook's end. When the hook ends on the song's lowest tonic, no such ending exists, and the build dies at the design gate.

**Evidence:** The last chorus on the tonic in 81.3% (83.9%) of complete builds; 100% of survivors.

**Fix:** 311's redraw also reads a design's ending condition; or the hook's ending (302) is drawn above the song's lowest tonic when a design needs one under it.

**Check:** The design gate at nine in ten; the last chorus on the tonic in every build.

### 326. The design gate passes three builds in four (317).

**Evidence:** 74.4% (main), 76.9% (control). Why: as 325, the aim is not drawn inside the design.

**Fix:** As 325.

**Check:** Nine in ten.

### 327. 310's unit ending crowds the breath before a copy.

**Evidence:** Song 40: deaths at "no held end and breath before the copy (212)" rose from 92 to 130 (main) and to 121 (control).

**Fix:** Read the unit-end rule and 212's join together: a unit's last line ends by beat 3, or the copy after it enters after the downbeat.

**Check:** Join deaths back to v109's level.

### 328. A slow ballad draws sixteenths at pop's rate.

**Problem:** 288's sixteenth offer is not tempo-aware.

**Evidence:** Song 42 at ♩ = 76: sixteenth onsets 11.8% at the median (kept median 1%, 75th 14.3%); the hook's "hey, it's me, noth-ing" is four sixteenths.

**Fix:** Count sixteenth shares by tempo band on the kept songs and draw from the band.

**Check:** Song 42's sixteenth share inside its tempo band's middle half.

## Order of work

1. **322 and 327** (310 where partners differ, and its join): the floor on song 40 is still a quarter of builds.
2. **325 and 326** (a design's ending inside 311 and 317): one change answers both.
3. **323** (313's copies one onset over the cap).
4. **324** (where a tonic ending is aimed and read).
5. **328** (sixteenths by tempo; a count on the kept songs).

## Regression line

After these fixes, songs 40 and 42 rerun at PYTHONHASHSEED 0, N 1000, main and control, and each must reproduce its frozen order twice (today's: song 40 3c9c4f2da558 and 30ba2486b5e4, seed 20261511; song 42 5614d9557a76 and 46d4320fd85a, seed 20261552; they will change with the code).

Song 42 must keep:

- the locked lyric, every syllable sung, no never-say word, "the third morning" once;
- the chorus said with "hey, it's me" twice; chorus 2 = chorus 1;
- the last chorus's head, augmented tail and falling last line;
- every line two bars, and the range centred in the row;
- all 39 consistency checks.

After 322–328: song 40 under the floor below one in ten with likeness of bar rhythms at 0.14 or more; verse 2's copies in range in three builds of four on both songs; the tonic test at 100%; song 42's design gate at nine in ten and its last chorus on the tonic in every build; join deaths back to the v109 port's level; song 42's sixteenths inside its tempo band.

## Readings the paper does not give

**The port:** 310's pairs (line k of four-bar units 2m and 2m+1 with the same slots; no units where a slot boundary misses a four-bar line); the partner's bars copied as a prior and kept within one onset a bar, given up after fourteen tries; "ends by beat 3" read on the last onset. 311's redraw up to 50 times. 312's leap knob on the walk's larger moves. 313: a source bar over the cap left out. 314's quantiles interpolated with extrapolated tails; the odd spare semitone above; the verse's floor and cap at its median −7 and +5. 315's largest step defined for the knobs with a step clip only. 316's fits computed per slot and cached.

**Song 42:** the paper's six-line verse and bridge plans cut to four lines; the augmented tail (onsets doubled from the hook's entry, 1.5 or 1 if needed, counted); the last line drawn fresh, its floor the song's floor; the piano patterns and the cello's range (no table for a solo piano accompaniment); "blinker" pronounced B L IH1 NG K ER0; seed 20261552.

## Blind-pick tally

Song 42: the writer picked the middle slot ("the kid at the counter said, 'Nothing to save,'", top quartile under both). Songs 40 and 41 are not yet offered. Tally, 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1.
