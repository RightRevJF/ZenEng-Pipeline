# ZenEng v109 port (fixes 298–309), tested on song 40 (port report)

*Words and music of the test song: Jason Bryant · findings numbered from 310*

The fixes of Module 27.53 (Window 129) were ported onto song 40's default-path search (melody_v109_p40.py), and song 40 was run again before song 41: 1,000 builds main and 1,000 control (243 off), each made twice. Seed 20261511, calibration 20261512, PYTHONHASHSEED 0, code dd36a23da4a3. Rerun line: `PYTHONHASHSEED=0 python3 melody_v109_p40.py 1000 main|ctl`. Nothing blocked the port and no two fixes conflicted.

| Run | Survivors (v108) | Frozen order | Second run |
|---|---|---|---|
| Main | 476 (468) | 6ad97e7695d1 | reproduced |
| Control | 398 (570) | 4974bb2f8af1 | reproduced |

Deaths, main: the judge's floor (254; 279) 218, join: no held end and breath before the copy (212) 92, limits: a hard limit or three soft breaks (276/277, with 286's seven) 80, key word on a chord tone (134; 279) 66, bridge opening unrelated (208; 279) 54, chorus opening another tune (227; 279) 11, align: the words do not fit the returning tune 2, walk: no note 1.

## The tests of 298–309

| Fix | Test | Main (control) | Held? |
|---|---|---|---|
| 298 | intake prints the default's draws; the report prints the title line against the verse | title line's median above the verse's in 58% of builds, level 12%, below 31% (kept 56 · 18 · 26%); the pick +3 | printed |
| 299 | deaths at the floor under one in ten with 308 in; the five heaviest give-aways printed | under the floor 33.6% (41.6%); v108 26.5% (21.3%); give-aways: distinct pitches -0.508, chord tones on long notes -0.394, on offbeat eighth -0.391, past fifth -0.346, chord tones -0.252 | **no** (310) |
| 300 | realness out of 277's count; printed beside the kept chart figures | out of the count; builds 0.008 · 0.083 · 0.212 · 0.421 · 0.699 (kept chart 0.004 · 0.029 · 0.088 · 0.303 · 0.636); pick 0.649 | yes |
| 301 | each family's joint pass printed, nine in ten or more | the eight of 276: 92.0% of kept songs; the six of 286: 94.2% of the 515 pairs (no refit) | yes |
| 302 | under one build in ten moved; the last chorus on the tonic in every build | moved 0 of 1,000 (v108 207); last chorus on the tonic 96.6% (96.7%) | moves yes; tonic **no** (311) |
| 303 | verse 2 shares 25–75% in three builds of four | 0 · 0.25 · 0.5; in range 50.3% (61.4%); copy given up for 477 lines | **no** (313) |
| 304 | listed as dropped in the chorus; its reading printed | dropped; chorus target and reading r = 0.015; reading 0.5 · 0.676 · 0.882 | yes |
| 305 | arch over the span inside 0.0–0.55 at the median; no amplitude at a cap | -0.354 · -0.053 · 0.155 · 0.362 · 0.672 (median 0.155); amplitude 13.2, no cap | yes, at a cost (312) |
| 306 | last note over the mean inside 1.18–1.71 | 1.4 · 1.538 · 1.691 (v108 2 · 2.286 · 2.857) | yes |
| 307 | the top note read beside the kept | soundings 2 · 11 · 97 (kept median 4), once only 3.3% (kept 22%), longest over the median note 1 · 2 · 8 (kept 2), never on a beat 11.7% (kept 21%); the pick 3 soundings, 1.5×, on a beat | printed |
| 308 | fullest bar ≤ 57% at the median; four fifths in one bar under one line in ten; chorus spread under 2.91 in nine of ten | 0.455 · 0.533 · 0.778; four fifths 3.7%; spread 0.829 · 1.495 · 2.107, under 2.91 in 100% | yes |
| 309 | a clone with the tables reproduces the frozen order with no file made by hand | every file the search reads is committed (the 14 tables, song 36's v88 table, limits286.json, limits_v109.json); a copy of the repo with its paths pointed at itself built the same order as the workspace (30 builds, e0f15dc333e7); setup.sh links each songs/pNN to /home/claude/pNN | yes |

The order judge's four measures, median of 300 builds (Verse 1 and Chorus 1 windows) against v108 and the kept mean: parallel 0.069 (v108 0.098, kept 0.074, weight 1.525); pitch parallel -0.004 (v108 -0.012, kept 0.105, weight 0.614); smooth barline -1.241 (v108 -0.807, kept -1.378, weight 0.595); thin 48 0.333 (v108 0.667, kept 0.604, weight 0.628). Judges, main: content -3.262 · -0.716 · 2.443 (v108 -4.352 · -1.295 · 1.744); order -1.139 · -0.016 · 1.205 (v108 -0.382 · 1.002 · 2.4).

## Readings the paper does not give

- **302.** The last note is drawn among the permitted degrees inside the line's drawn register, weighted by its distance from the contour's end (a Gaussian, sd 1.5 semitones); where the register holds no permitted degree the old move is tried and, failing, the line keeps its ending (counted per build, not in the move count).
- **303.** 'Within one onset' is the symmetric difference of the bar's onsets and its source bar's; an onset outside a copied bar's set is weighted 0.04 in the rhythm draw, not barred.
- **305.** The arch term over the span is a line's arch term divided by its pitch span (0 for a one-pitch line), the median over its lines; the calibration multiplies the amplitude by the kept 0.23 over the reading (clipped 0.6–1.6 a round) with no upper cap.
- **306.** The ratio is drawn from the kept quantiles of Table DJ (5th 0.867 to 95th 2.298, linear between); the length is the palette length nearest the wanted one that fits before the next line; a title note keeps 232's two beats.
- **308.** 'No more than 57%' caps the syllables in any one bar at the whole part of 0.57 × the line's syllables, for lines of nine syllables or more, inside the rhythm draw; melisma notes are not counted.
- **300/301.** The six's family is read with the spectral limits of the v108 file and the other five on the pairs; 'refitted' would have widened the hard limits by the pairs' percentiles (not needed: 94.2%).

## Findings

**310. 308 lays the line across its bars, and the floor kills more builds, not fewer.** *Problem:* Window 129 predicted deaths at the floor falling to 8% (main) and 5% (control) once a long line is laid across its bars. *Evidence:* under the floor 33.6% and 41.6% (v108 26.5%, 21.3%); deaths 218 and 287 (v108 164, 141). The content judge rose as predicted (median -0.716 from -1.295), but the order judge fell (median -0.016 from 1.002): bars 4 and 8 are no longer thin (thin_48 0.333 from 0.667, kept 0.604) and the barline is less smooth (-1.241 from -0.807). The packed lines had left the even bars nearly empty, which the order judge read as phrasing; the rescoring changed one content measure and held the order measures. *Fix:* a line that ends a four-bar unit ends by beat 3 of bar 4 or 8, so the unit keeps its breath while the line is laid across its bars; or the judges are refitted on builds made with 308. *Check:* deaths at the floor under one build in ten; thin_48 inside the kept middle half.

**311. 302 ends the moving, but the last chorus misses the tonic in one build in thirty, silently.** *Problem:* where the drawn chorus register holds no tonic, no permitted ending can be drawn and the fallback finds none. *Evidence:* no last note moved (0 of 1,000; v108 207), yet the last chorus ends on the tonic in 96.6% of main's builds and 96.7% of the control's; every miss is a hook (whose tail the tag copies) drawn in a register without a D. *Fix:* the ending line may take a permitted degree one step outside its register, or the register draw keeps one; misses are counted. *Check:* the last chorus on the tonic in every build.

**312. 305 meets its test by widening leaps.** *Problem:* with the cap gone the amplitude rose to 13.2 and the calibration still read 0.117 against 0.23 at its last round. *Evidence:* the builds' arch over the span is 0.155 at the median (inside the kept 0.00–0.55); leaps past a fifth in the verse window rose from 0.024 to 0.05 at the median (the judge's kept mean 0.021) and became a content give-away; distinct pitches are now the heaviest. *Fix:* the arch is drawn through the walk's direction (steps toward the contour) rather than a larger contour, or leaps past a fifth are held to the kept rate. *Check:* past_fifth at the kept median with the arch over the span at 0.23.

**313. Verse 2 still copies too few bars, and 308 gives up more copies.** *Evidence:* verse 2 shares 25% of verse 1's bar rhythms at the median with one onset's difference allowed; in range 50% (control 61%); the copy was given up for 477 lines against 31 under v108, the cap of 308 and the copied bars both drawing on the same rhythm. *Fix:* copied bars are chosen among those the line's cap allows before the draw. *Check:* verse 2's share inside 25–75% in three builds of four.
