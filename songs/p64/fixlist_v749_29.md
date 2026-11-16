# Luthier fix list for v8 (since v7)

Nov 14, 2026 · @Jason Bryant

This list is cumulative since the spec's last version (Luthier v7, Module 27.88, Window 164). Songs 48 (The Ratios Hold) and 49 (The World Is Asking) were each rerun once on Luthier v7, main and control, at the same seeds and designs. Fixes 730 to 736 were ported onto the v6 engine in one pass; 737, 738 and 739 are readings. The pick is luthier\_judge5.pick, not edited or refitted. Song 49's pick of record stays e2b80cdc3a1c. Song 50 (The Small Things), a new song, was run once on the same v7 engine with its own key (D major), plan, designs and lyric, at seed 20261113+450; its pick of record is the judge's pick, f583fd857dda, taken as drawn. Song 51 (A Wire Pulled Tight), the writer's song from an earlier engine with its lyric revised, was run on the same v7 engine in A major with a tempo plan (q = 116 rising to 164, written at double tempo with a half-time feel; the beat grid 4/4), 194 bars, at seed 20261113+451; its pick of record, 89e71513033a, is the writer's choice over the judge's pick. Song 51's findings are numbered 749.1 to 749.3, since 740 to 749 are taken and 750 is the next fix. Words and music: Jason Bryant. Findings run from 740, as the paper asked. Each has Problem, Evidence, Fix and Check.

**Since the engine went offline (14 to 15 November).** The engine was offline, so two songs were written by sketches outside it, in metres the engine cannot yet write: song 52 (The Room Next Door, 6/8, three editions) and song 53 (Sung to Sleep, a 3/4 carol for organ and choir, four editions). Nine research rounds and studies ran alongside: the metre atlas, accompaniment, song shapes, surprise against expectation (YouTube views), the moments people love (timestamped comments), the rhythm layer, psychoacoustics, and covers (SHS100K and Discogs-VI). A tenth, on chromatic harmony, followed the maintainer's review of 28 songs. Their findings are 749.4 to 749.23 below.

**Song 54 (16 November), back on the engine.** The Man Mama Prayed I'd Be, a country story song (the writer's earlier lyric, renovated), was run on the same v7 engine by gen\_l7\_p64.py from song 51's file: G major, q = 120, 126 bars, every line in two bars, no bridge, the chart drawn by 438 (the default path), seed 20261113+454. Main 63a84b18e7dc (185 survivors, 143 clean) and control c43334ae0deb (192), each made twice, reproduced. The judge's pick d48480b70b0d sang two syllables on one onset; the pick of record, d12c2728e6f1, is 730's own rule over the clean survivors without that fault (the rule song 51's re-pick used). Its findings are 749.24 to 749.29; the next is 749.30.

Two companion documents go with this list:

- **"Luthier research compendium - 15 November 2026"** (one file): every report, study, atlas and test report written in that time.
- **"For Luthier's maintainer: avenues and new rules"** (a Doc): the new rules in one table with evidence grades, and the avenues ranked.

Several findings confirm rules Luthier v7 already holds (749.19 Windows 2 and 3; 749.21 Modules 9.13 and 9.14). They are marked so they are not ported twice.

## The songs

| Song | Title | Runs, main / control (survivors) | Pick (730), main / control | 728's rule would pick | Pick of record | Blind pick |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | The Ratios Hold | db3ed0fc13ab / 44de852103a9 (775 / 752) | aab38d0971e1 / ed90305e255a | 54db4425f286 / ed90305e255a | v134 | Annotated |
| 49 | The World Is Asking | cb0a317e10d9 / 9787becabe8d (664 / 666) | 2f8263b62ee4 / 962791062353 | ef3a04a2c45c / 672e402c17eb | e2b80cdc3a1c | Annotated |
| 50 | The Small Things | 46073782f2d5 / cd7f41ab51d3 (284 / 234) | f583fd857dda / 20c6b0cba73d | f583fd857dda / 20c6b0cba73d | f583fd857dda | Middle |
| 51 | A Wire Pulled Tight | a37686ce104b / 37c6e1ffbafb (376 / 368) | b121d283f86f / 38c86752b17d | 7a1c563b0c31 / 38c86752b17d | 89e71513033a (the writer's choice) | Remembered |
| 52 | The Room Next Door (6/8) | the 6/8 sketch, 3,000 builds (657) | 8f4cc7fe75bf (the sketch's rule) | not read | 8f4cc7fe75bf | Annotated |
| 53 | Sung to Sleep (3/4 carol) | the 3/4 hymn sketch, 3,000 builds (2,739); hymn mode (gen34h) for editions 2 to 4 | 9025fdbc9b1e (hymn mode; first edition 01be9dada5fb) | not read | 9025fdbc9b1e, fourth edition (organ by section role, breaths, Module 9.14 limits, ♩ = 92) | pending |
| 54 | The Man Mama Prayed I'd Be | 63a84b18e7dc / c43334ae0deb (185 / 192) | d48480b70b0d / 501b81ba463c | not read | d12c2728e6f1 (730's rule without two syllables on one onset, 749.26) | Middle |

## The port check (730)

luthier\_judge5.py (sha256 fac5abf2…) was saved beside luthier\_judge4.py and its data and called as given. On the Luthier v6 runs' clean survivors it gives every listed pick: song 48 3bf00742c210 (263 eligible of 458) and e5bb0fda1502 (254 of 434); song 49 2a630947f684 (323 of 575) and 8a996bd122a8 (311 of 557). e2b80cdc3a1c is eligible at a window place of 0.631. The session's reader for 739 gives the kept 25th, 50th and 75th percentiles of all nineteen readings exactly as the tables file does.

## Song 48: each fix's test

Main / control.

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The pick's most-repeating window | place 0.552 to 0.934 | 0.847 / 0.695 | Pass |
| 730 | Eligible (under 715; under 730) of clean; within 0.02 of the least | printed | 440, 382 of 488 / 476, 424 of 512; 112 / 121 | Printed |
| 731 | Entries before / on / after, stressed openings | 20 / 42 / 38 within 10 | 54 / 22 / 25; 54 / 21 / 25 | Fail (742) |
| 731 | The same, unstressed openings | 43 / 10 / 47 within 10 | 25 / 38 / 36; 26 / 38 / 36 | Fail (742) |
| 732 | Bars (3+ notes) on a kept figure, rate under one | 56% within 15 | 47.3% / 48.0%, rate 1.0 | Value passes; the rate is at one (743) |
| 732 | 651's share still passes | middle half 35% to 62% | 37.0% / 37.1% | Pass, near the floor |
| 733 | Each window under the kept 75th in three builds in four | 75% | verse 1 82 / 80, chorus 95 / 94, verse 2 93 / 93, bridge 82 / 83, last chorus 97 / 97 | Pass |
| 733 | Longest run of one pitch | kept 4 to 7 | median 8 / 8 (pick 8 / 6) | Printed: over |
| 734 | Easier of a pair; easier than every neighbour | 89 within 3; 73 within 5 | 86.0 / 86.6; 65.6 / 66.7 | Pass; fail (745) |
| 734 | The power's rounds, with standard errors | printed | main back to 1.00 at round 3; control one raise counted (1.42), back to 1.42 at round 5 | Printed |
| 735 | Drawn lines (under 6.5 notes a bar) against the palette: 16th; 8th; quarter | within 10 | 14.9 v 11.3; 62.8 v 58.5; 13.6 v 17.9 (power 1.0) | Pass |
| 735 | Bits saved a gap (the judge's reader, median) | 0.13 to 0.36 | 0.102 / 0.106 | Fail (744) |
| 735 | Gaps from the kept mean palette (median) | 0.19 or more | 0.218 / 0.218 | Pass |
| 736 | Deaths for want of a placement | under 20 (song 49's test) | 4 / 5 | Pass |
| 737 | Bars sung in a kept song, every complete build | 81% within 8 | 75.1% / 74.9% | Pass |
| 738 | Lines of 6.5 notes a bar and over against the kept cell: 6.5–7.5 | within 10 | 29.7 v 28.5; 61.1 v 56.8; 5.2 v 4.6 | Pass |
| 738 | The same, 7.5 and over | within 10 | 35.6 v 50.4; 58.0 v 36.9; 2.6 v 2.9 | Fail (744) |
| 657 | Survivors |  | 775 / 752 (v6 731 / 724) |  |

## Song 49: each fix's test

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The pick's most-repeating window | 0.552 to 0.934 | 0.916 / 0.818 | Pass, but the pick chants (740) |
| 730 | Eligible (715; 730) of clean; within 0.02 | printed | 523, 462 of 558 / 533, 452 of 576; 268 / 254 | Printed |
| 731 | Stressed openings | 20 / 42 / 38 | 27 / 31 / 42; 26 / 31 / 43 | Fail on the bar line (742) |
| 731 | Unstressed openings | 43 / 10 / 47 | 29 / 27 / 44; 29 / 27 / 44 | Fail (742) |
| 732 | Kept figures, rate under one | 56% within 15 | 49.1% / 49.5%, rate 1.0 | Value passes; the rate is at one (743) |
| 732 | 651's share | 35% to 62% | 39.1% / 39.1% | Pass |
| 733 | Each window under the kept 75th, three in four | 75% | 84 / 82, 95 / 97, 96 / 94, 95 / 97, 84 / 86, 95 / 97 | Pass |
| 733 | Longest run of one pitch | kept 4 to 7 | median 8 / 8 (pick 16 / 14) | Printed: over (740) |
| 734 | Easier of a pair; than every neighbour | 89 within 3; 73 within 5 | 86.5 / 86.5; 68.0 / 68.1 | Pass; pass at the edge |
| 734 | The power's rounds | printed | both back to 1.00 at round 3 | Printed (745) |
| 735 | Drawn lines against the palette: 16th; 8th; quarter | within 10 | 19.4 v 7.5; 63.8 v 53.7; 10.3 v 24.0 (power 1.80 / 1.60) | Fail (744) |
| 735 | Bits saved a gap | 0.13 to 0.36 | 0.082 / 0.088 | Fail (744) |
| 735 | Gaps from the kept mean palette | 0.19 or more | 0.171 / 0.172 | Fail (744) |
| 736 | Deaths for want of a placement | under 20 | 39 / 27, all at Verse 1 line 4 | Fail (741) |
| 737 | Bars sung in a kept song | 81% within 8 | 82.0% / 82.4% | Pass |
| 738 | Lines of 6.5 notes a bar and over | within 10 | none in this song |  |
|  | Survivors |  | 664 / 666 (v6 660 / 662) |  |

## Song 50: each fix's test

Main / control. The engine draws straight 4/4; the swing is in the demo only.

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The pick's most-repeating window | 0.552 to 0.934 | 0.714 / 0.695 (the bridge) | Pass |
| 730 | Eligible (715; 730) of clean; within 0.02 | printed | 195, 149 of 223 / 185, 156 of 206; 105 / 103 | Printed |
| 731 | Stressed openings | 20 / 42 / 38 | 21 / 40 / 39; 21 / 43 / 36 | Pass |
| 731 | Unstressed openings | 43 / 10 / 47 | 24 / 33 / 44; 23 / 34 / 44 | Fail (742, 749) |
| 732 | Kept figures, rate under one | 56% within 15 | 55.5% / 54.0%, rate 0.83 / 0.78 | Pass; the rate under one |
| 732 | 651's share | 35% to 62% | 46.1% / 46.1% | Pass |
| 733 | Each window under the kept 75th, three in four | 75% | 84 / 81, 92 / 93, 95 / 94, 92 / 92, 95 / 92, 92 / 93 | Pass |
| 733 | Builds with every window under | printed | 70.1% / 65.0% | Printed |
| 733 | Longest run of one pitch | kept 4 to 7 | median 7 / 7 (pick 7 / 7) | Inside, but runs inside lines (746) |
| 734 | Easier of a pair; than every neighbour | 89 within 3; 73 within 5 | 88.3 / 88.1; 71.6 / 71.2 | Pass; pass |
| 734 | The power's rounds | printed | main two raises (1.02, 1.05) do not count, back to 1.00 at round 6; control the same at round 5 | Printed (745) |
| 735 | Drawn lines against the palette: 16th; 8th; quarter | within 10 | 20.5 v 9.2; 61.8 v 56.3; 11.1 v 21.4 (power 3.43 / 2.71) | Fail (744) |
| 735 | Bits saved a gap | 0.13 to 0.36 | 0.067 / 0.063 | Fail (744) |
| 735 | Gaps from the kept mean palette | 0.19 or more | 0.167 / 0.160 | Fail (744) |
| 736 | Deaths for want of a placement | under 20 | 244 / 233, at Chorus 1 line 1 and Verse 2 lines 1 and 3 | Fail (747) |
| 737 | Bars sung in a kept song | 81% within 8 | 79.5% / 78.9% | Pass |
| 738 | Lines of 6.5 notes a bar and over | within 10 | none in this song |  |
|  | Survivors (clean) |  | 284 / 234 (223 / 206) |  |

On song 50 the palette's power searched as far as 4.10 (main) and 4.10 (control); the largest gap never fell under 0.107. This is 744 on a third song: the power moves, the gaps do not.

## Song 51: each fix's test

Main / control. Verse lines four bars, every other line two; the hook's line held six bars (eight in the final chorus). The voice kept to the scale (a first run with the flat seventh allowed is kept apart).

| Fix | Test | Target | v7 | Result |
| --- | --- | --- | --- | --- |
| 730 | The judge's pick's most-repeating window | 0.552 to 0.934 | 0.881 / 0.673 | Pass, but the pick chants (749.2) |
| 730 | Eligible under 730 of clean | printed | 245 of 320 / 263 of 317 | Printed |
| 731 | Stressed openings | 20 / 42 / 38 | 13 / 51 / 36; 11 / 53 / 36 | Pass; fail by one point |
| 731 | Unstressed openings | 43 / 10 / 47 | 28 / 32 / 40; 27 / 33 / 40 | Fail (742, 749) |
| 732 | Kept figures; rate; 651's share | 56% within 15; 35% to 62% | 54.3%, rate 0.73; 37.3% | Pass |
| 733 | Builds with every window under the kept 75th | printed | 40.2% / 42.7% | Printed (thirteen windows) |
| 734 | Easier of a pair; than every neighbour | 89 within 3; 73 within 5 | 86.9 / 86.7; 67.5 / 67.5 | Pass; fail by half a point |
| 735 | Drawn lines against the palette: 16th; 8th; quarter | within 10 | 21.4 v 6.4; 59.9 v 49.2; 11.8 v 27.7 (power 1.42 / 1.75) | Fail (744) |
| 735 | Bits saved a gap | 0.13 to 0.36 | 0.076 / 0.079 | Fail (744) |
| 736 | Deaths for want of a placement | under 20 | 478 / 443, all at the pre-choruses' first lines | Fail (749.3) |
| 737 | Bars sung in a kept song | 81% within 8 | 83.6% / 84.2% | Pass |
|  | Survivors (clean) |  | 376 / 368 (320 / 317) |  |

The palette's power searched to 1.6 (main) and 2.56 (control); the largest gap never fell under 0.135: 744 on a fourth song.

## 739: the nineteen readings for the pick and the median build

Outside the kept middle half (the pick; the median clean build):

- **Song 48 main (aab38d0971e1):** least-repeating window 0.09 (under); spread between windows 0.40 (over); longest run 8 (over); range 22 (over); pitch-class entropy 2.76 (over); gaps of an eighth 62% (over); gaps of a quarter or more 19% (under); onsets on a bar's first beat 14% (under). Median build: longest run 8, range 22, sixteenths 23%, quarters 19%, first-beat onsets 12%, the two largest sections' medians 7 apart.
- **Song 48 control (ed90305e255a):** range 22, distinct pitches 15, entropy 2.76, sixteenths 25%, quarters 18%, first-beat onsets 12%, sections 9 apart. Median build as main.
- **Song 49 main (2f8263b62ee4):** least-repeating window 0.42 (over); longest run 16 (over); steps 53% (over); leaps 6% (under); entropy 2.74 (over); first-beat onsets 10% (under); sections 7 apart (over). Median build: longest run 8, first-beat onsets 12.5%.
- **Song 49 control (962791062353):** least-repeating window 0.07 (under); longest run 14 (over); first-beat onsets 14% (under). Median build: longest run 8, first-beat onsets 13%.

* **Song 50 main (f583fd857dda):** steps 33% (under); leaps 21% (over); turns 66% (at the kept 75th). Fifteen of nineteen inside. Median build: steps 46%, leaps 9%, turns 59%, all inside; bars of one pitch 5%.
* **Song 50 control (20c6b0cba73d):** entropy 2.79 (over); gaps of an eighth 62% (over); gaps of a quarter or more 24% (under); first-beat onsets 12% (under); bars of one pitch 12.3% (over). Median build as main.

- **Song 51 main, the judge's pick (b121d283f86f):** spread between windows 0.37 (over); leaps 15% (over); the two largest sections' medians 7 apart (over). Median build: all inside.
- **Song 51, the pick of record (89e71513033a):** least-repeating window 0.07 (under); distinct pitches 15 (over); entropy 2.84 (over); gaps of a sixteenth or less 19% (over). More pitches and quicker notes, the opposite of the judge's pick.
- **Song 51 control (38c86752b17d):** entropy 2.73 (over). Median build: longest run 8 (over).

What 728's rule (every window under the kept 75th, among builds eligible under 715) would have picked: song 48 54db4425f286 / ed90305e255a (278 / 296 builds); song 49 ef3a04a2c45c / 672e402c17eb (348 / 361 builds); song 50 f583fd857dda / 20c6b0cba73d (140 / 120 builds), the same as the judge's picks; song 51 7a1c563b0c31 / 38c86752b17d (111 / 138 builds).

## How the ports were made

- **730:** luthier\_judge5.pick over the clean survivors, as 715's; the record keeps each build's window places.
- **731:** 653's kept line is drawn from the table's lines whole for the line's cell whose first-syllable stress matches the line's first syllable as this engine stresses it (lines of unknown stress set aside; the whole cell where none match, which did not happen). In 680 a stressed opening's pickup runs to the next stressed syllable; in the old draw the first syllable may stand before the bar line. 714's exact first onset stays.
- **732:** 717 draws first, at its rate; a bar that takes no kept figure goes to 651, which draws from every bar the song has sung (as it did).
- **733:** the window is the section's first eight bars; its repeats so far are read from the lines placed and the line's notes so far; at or over 713's ceiling for the section's density, 717 draws among kept figures with no repeated note.
- **734:** the calibration's unaimed builds are a hundred a round. A raise counts when the reading rises by more than two standard errors of the difference from the round before. After two raises in turn that do not count, the power returns to the last value that counted (the starting 1.0 if none did) and stays.
- **735:** 711's ratio is raised to a power Q, searched in the calibration (up by 1.6 at first; reversed and narrowed to the square root of the step when the largest gap grows) while drawn lines under 6.5 notes a bar stand more than ten points from the build's capped palette in the sixteenth, eighth or quarter.
- **736:** 313 keeps a copied bar whatever its count; 680 takes a copied bar over the cap as a fixed bar; in the old draw a copied bar's own count is that bar's cap.
- **737, 738, 739:** read by read\_l7.py and read739.py; 739's readers reproduce the tables file's kept percentiles.

## Order of work

1. 749.1: notes of no length, two syllables on one onset, in a third of the survivors of songs 49 to 51; the judge can pick one.
2. 740, 746 and 749.2: the judge still admits a chant across two lines (song 49) and runs of one note inside lines (songs 50 and 51).
3. 748: the judge does not read motion; song 50's pick leaps.
4. 742: entries on the bar line where a pickup does not fit; the old draw's entry weights for stressed openings; 749, the unstressed openings again on song 50.
5. 741, 747 and 749.3: deaths for want of room, song 49's before the next line, song 50's where a returning line outgrows its source, song 51's at lines of ten syllables or more in two bars.
6. 744: the palette's power cannot move the gaps; bits saved and 738's densest lines.
7. 743: 717's rate at one.
8. 745: the power returns to its start.
9. 749.4 to 749.7: the metre as a parameter, with kept rhythm tables per metre (a first 6/8 set from Essen); the stress rule, the bass routine and density cells for compound metre.
10. 749.8, 749.9: a returning chorus lifted, not copied; harmony written as lines. Both tried on song 52, with the before and after.
11. 749.10: a song plan by section place, the top placed late; tried on song 52 (third edition).
12. 749.11 to 749.13: a hymn mode with hymn tables, a descant module, choral documents from one timeline (song 53).
13. Then rerun song 53 (Sung to Sleep) on the engine, the writer's choice (15 Nov). The sketch reached a fourth edition while the engine was offline: a hymn-mode tune (749.11), passing notes in the four parts, an organ part written by section role against the Lieder accompaniment tables (749.14, 749.16), breaths before the third line of every verse and refrain (749.19), Module 9.14's limits with the pedal in its own octave (749.21), and ♩ = 92 so that sung lines last 7.8 seconds. It stands as the target for the engine's own run, which should match or beat it on every check in songs/p63/consistency53.py (62 checks).
14. 749.15: the metre atlas is ready; start the port of 749.4, 749.5, 749.9 and 749.11 from it.
15. 749.14 and 749.16: an accompaniment module, with textures by section role measured against the Lieder accompaniment tables (tables/metre\_atlas/accompaniment\_lieder.json). Needed before song 53's rerun.
16. 749.18 and 749.20: add melody, chord and rhythm surprise against a large popular corpus to the judge (studies/surprise, studies/rhythm). The audience channel.
17. 749.22: the musician channel (harmonic motion within sections, melodic room, conventional chord choices), then a judge on both channels. Replicate on LargeSHS when it is published.
18. 749.23: the chromatic home as an intake style option (declared vocabulary per section, first entry 1 unit, then free), applied dominants first. The default budget stays as it is.
19. 749.17 and 749.19: one song-wide intensity curve, with the high point at 0.65 to 0.85 and the emotional moment at 0.55 to 0.60, each with a breath and a fresh re-entry. These are measured targets for Windows 2 and 3 and the 9.12 energy arc, not new mechanisms.
20. 749.21: port Module 9.14 to organ and choir textures (the pedal in its own octave, the sung tune on top, phrase length in seconds). Use studies/psychoacoustics/perception.py as the reference check.

Song 54's findings, in order:

- 749.26 (with 749.1): two syllables on one onset in 61% of song 54's clean survivors and in the judge's pick. Make it a death first; it decides every pick.
- 749.25 (with 741, 747, 749.3): placement deaths at nine- and ten-syllable lines whose rhythm is borrowed (712, 310, 361): split the longest note or draw the bar fresh.
- 749.24: the bridge optional in every reader.
- 749.29: g-dropped forms, "'n'" and "a.m." read by the lexicon; one question for the rest.
- 749.27 and 749.28: read 749.21's band-over-the-tune limit by texture, and 749.17 and 749.19's places by the song's turn when the type is Narrative.

## Findings

### 740. The judge reads repeats by window, and its pick still chants across two lines

**Problem:** 730 places the most-repeating window among kept windows. A window repeats in a share of its moves, so a chant that fills one window's first two lines and nothing else can stand under the upper quartile. Song 49's pick under v7 does.

**Evidence:** Song 49 main, the pick 2f8263b62ee4: Bridge lines 1 and 2, "I don't have proof, I have a door / I'm leaving open just a crack," sing sixteen G3s in a row. Its bridge window repeats in 55% of its moves, the 0.916 place, under the 0.934 limit; its other windows lie at 0.42 to 0.45. The control pick 962791062353 runs fourteen E3s from Chorus 2's last line into the bridge. Kept songs' longest run of one pitch: median 6, 90th percentile 9.5, 95th 11.25. The median clean build's longest run is 8 on both songs. The line on sixteen G3s is the writer's own blind pick for the song.

**Fix (proposed):** Add the longest run of one pitch to the pick's eligibility, inside the kept middle half (4 to 7.25) or under the kept 90th (9.5); or read a window by its longest run as well as its share.

**Check:** No pick with a run of one pitch past the kept 90th, on songs 48 and 49.

### 741. Song 49's deaths are a want of room, not the template's bar

**Problem:** 736 lets a copied bar keep its count, and it did (727 copied bars over 308's cap kept, song 49 main), but song 49's deaths remain at Verse 1 line 4. The line that dies has no copied bar over the cap.

**Evidence:** Deaths for want of a placement 39 / 27 a thousand (v6 60 / 55), all at Verse 1 line 4, "I grew up trusting what I could touch" (9 syllables). In 150 builds drawn again with the line watched, it failed four times: three times with no copied bar at all, with its last onset held to 48 or 51 twelfths by the next line's entry and breath, or with room only to the slot's end at 72; once with a single copied note. The next line, "The nail, the bread, the roof of tin," now draws pickups more often (731).

**Fix (proposed):** Where a line's syllables cannot fit before the next line's entry less its breath, let the next line's pickup shorten (or its breath give way, as 681 does before a line sung again) before the line is given up.

**Check:** Deaths for want of a placement under 20 in a thousand on song 49.

### 742. Entries by stress miss both ways: pickups that do not fit fall on the bar line, and the old draw prefers a pickup

**Problem:** The kept line is now drawn by the first syllable's stress, but the entries as sung do not follow it. Unstressed openings land on the bar line three or four times as often as kept lines do, and song 48's stressed openings come in early in over half their lines.

**Evidence:** Song 48: unstressed openings 25 / 38 / 36 against 43 / 10 / 47; stressed 54 / 22 / 25 against 20 / 42 / 38, but the stressed lines are two lines of the lyric, "Dear one, you will..." and "Something something was singing." Song 49: unstressed 29 / 27 / 44; stressed 27 / 31 / 42. Two mechanisms. (1) In 680 a pickup that does not fit after the previous line's breath is dropped, and the line then starts on the bar line: on song 48, unstressed lines that start on the bar line had 24 twelfths or less from the previous line's last onset in 71% of cases, lines that start before it in 49%. (2) When 680 falls back, the old draw weighs a first onset before the bar line 1.0, on it 0.35, after it 0.5; with 731 a stressed first syllable may now take that pickup.

**Fix (proposed):** Where the kept line's pickup does not fit, shorten it to what fits, or draw the kept line again among lines of the stress whose entry fits; and weigh the old draw's first onset by the kept shares for the line's stress.

**Check:** 731's test, each kind within ten points.

### 743. 717's rate still stands at one

**Problem:** Taking 717's turn before 651 raised the share of bars on a kept figure into the test, but the rate is still at its limit in all four runs, which 732's test asks it not to be.

**Evidence:** Song 48: 47.3% / 48.0% (v6 40.6% / 41.1%); song 49: 49.1% / 49.5% (v6 42.0% / 43.0%); rate 1.0 from the second round in every run. 651's share fell to 37% (song 48) and 39% (song 49), near its lower quartile of 35%. Of the bars eligible, 96% took a kept figure (song 48 main 14,130 of 14,762; song 49 main 11,208 of 11,706); 733 restricted the draw to figures without a repeat 3,291 and 2,379 times.

**Fix (proposed):** None from here beyond 722's: the eligible bars cap the reading. Either accept the rate at one, or let a bar of a template line or a copied bar take a kept figure too.

**Check:** 717 at 56% within fifteen points with the rate under one.

### 744. The palette's power cannot move the gaps

**Problem:** 735 raises 711's ratio to a power until the drawn lines meet their palette. On song 48 they already did, and the power stayed at one; on song 49 the power searched from 1.0 to 1.8 and the sung gaps did not move. Bits saved a gap stay under the kept middle half on both songs.

**Evidence:** Song 49, drawn lines under 6.5 notes a bar, sung against palette: sixteenths 19% against 7.5%, eighths 64% against 54%, quarters 10% against 24%, at every power the search tried (round by round the sung shares stay within two points). Bits saved a gap 0.082 / 0.088 (median; kept middle half 0.13 to 0.36); gaps 0.17 from the kept mean palette (0.19 asked). Song 48: drawn lines within ten points at power 1.0; bits saved 0.102 / 0.106; distance 0.218. Lines of 7.5 notes a bar and over (738): sixteenths 36% against the kept cell's 50%, eighths 58% against 37%. Song 49's lines carry eight or nine syllables in two bars, and a whole kept bar of four or five notes holds eighths whatever the weight: the gaps follow the counts, and the counts follow the words.

**Fix (proposed):** Draw the line's split of notes over its bars (the counts) with the palette in view, not only the bars of a given count; or let the palette choose between a pickup and a later entry, which moves a note out of the bar. Read bits saved against kept songs of the build's notes a sung bar.

**Check:** Bits saved a gap inside 0.13 to 0.36; 735's test.

### 745. The power returns to where it began

**Problem:** With a hundred builds a round, a raise counts only when the reading rises by more than about 0.007, and the reading hardly moves with the power. In three runs of four the power went back to 1.0; the share against every neighbour fails on song 48.

**Evidence:** Standard error 0.0024 to 0.0030 a round. Song 48 main: powers 1.00, 1.18, 1.41 read 0.869, 0.868, 0.871: neither raise counts; back to 1.0. Control: 1.21 does not count, 1.42 counts (0.866 to 0.878), 1.56 and 1.83 do not; back to 1.42. Song 49: both back to 1.0. Easier than every neighbour: song 48 65.6% / 66.7% (fails 73% within five), song 49 68.0% / 68.1% (passes at the edge). Across powers 1.0 to 1.8 the first share stays between 0.861 and 0.884.

**Fix (proposed):** None to the stop, which works as written. The paper may rule that 650's second share is out of reach of the power under 713's ceiling and whole kept bars, and read it as a reading.

**Check:** 650's two shares printed with the power's rounds.

### 746. The pick sings runs of one note inside lines, and no reading sees it

**Problem:** The judge's pick repeats a pitch four or more times running inside sung lines, and every reading places it inside the kept range. 740 is the same fault across two lines; this is the fault inside one.

**Evidence:** Song 50 main, f583fd857dda: chorus lines 1 and 2 open on D3 five times; "and the afternoon holds still" sings A3 five times. Its longest run is 7 (kept 4 to 7.5) and its bars of one pitch 10.5% (kept 75th 12.2%), both inside. Its windows pass 713's ceiling and 730's place (0.714). Of the 149 builds eligible under 730, 1 has no in-line run of four or more equal notes. The writer took the pick knowing this.

**Fix (proposed):** Read runs by line: the share of sung lines with a run of four or more equal notes, against the kept share for the line's density, with a ceiling at the kept 75th; add it to 730's eligibility, beside 740's longest run.

**Check:** On songs 48 to 50, the share of eligible builds with in-line runs falls to the kept share, and the pick's lines lie under the ceiling.

### 747. Placement deaths where a returning line outgrows its source

**Problem:** 736 uncaps copied bars, but a line with more syllables than its source line has notes still finds no placement. 741 is a want of room before the next line; this is a want of notes in the source.

**Evidence:** Song 50: 244 / 233 deaths a thousand (target under 20). Main: Chorus 1 line 1, 84 ("And I think somebody's watching this", 9 syllables); Verse 2 line 3 in the prefit's "again", 81, and in the draw, 58 ("just Sammie and Maggie doing their work", 10 syllables, over "Sammie takes his post again", 7 notes); Verse 2 line 1, 16. The control's spread is the same (67; 88; 58; 13).

**Fix (proposed):** When a returning line has more syllables than its source has notes, split the source's longest notes (a held note becomes two of the same pitch) before the prefit tries again, up to 308's cap; only then draw.

**Check:** Deaths for want of a placement under 20 a thousand on songs 49 and 50; the returning tune still read as the same (align).

### 748. The judge does not read motion, so its pick leaps

**Problem:** 730's eligibility reads repeats and ease, not steps and leaps. Song 50's pick lies outside the kept range on all three motion readings.

**Evidence:** The pick moves by step in 33.3% of its moves (kept 25th 34.8%), by leap of 5 semitones or more in 21.2% (kept 75th 14.2%), and turns in 66.1% (kept 75th 66.1%). The median clean build: 46.2%, 8.8%, 59.4%, all inside. The designed hook and bridge rise hold no leap of 5 semitones or more, so the leaps are the engine's. Song 49's v7 pick erred the other way (steps 53%, leaps 6%).

**Fix (proposed):** Add steps and leaps to 730's eligibility, inside the kept middle half, or charge them in the judge's distance.

**Check:** The pick's steps and leaps inside the kept range on songs 48 to 50.

### 749. Unstressed openings still land on the bar line (742 on song 50)

**Problem:** 731 draws the kept line by the first syllable's stress. On song 50 the stressed openings now land where kept songs do; the unstressed do not.

**Evidence:** Song 50, unstressed openings before / on / after: 24 / 33 / 44 (main), 23 / 34 / 44 (control); kept 43 / 10 / 47. Stressed: 21 / 40 / 39 and 21 / 43 / 36, against 20 / 42 / 38: the first pass on any song. Lines opening on a weak word ("and", "I", "the", "that") land on the downbeat a third of the time; kept songs put such words there a tenth of the time.

**Fix (proposed):** 742's, with this added: for an unstressed first syllable, draw the entry from the kept unstressed shares, and move it before the beat when the next syllable is stressed and the pickup fits.

**Check:** 731's test, each kind within ten points, on songs 48 to 50.

### 749.1. Notes of no length: two syllables on one onset

**Problem:** Some builds place a note of no length at a bar line and the next syllable on the same onset. The evaluation passes them, and the judge can pick one.

**Evidence:** Song 51's first full run: the judge's pick 0c255388ae47 sang "stamp-ing" on two D3s at one onset (Pre 3, line 1); 71 of its 202 eligible builds had such a pair, 51 of them in verse 4. Every case found is a note of length 0 on a bar line (onset a multiple of 48) followed by a note at the same onset. The same defect is in song 50's main run (117 of 519 builds) and song 49's (171 of 939). No delivered pick has it (songs 48 to 51 checked).

**Fix (proposed):** Make a note of no length, or two notes on one onset in a line, a hard failure in the evaluation; then find where a kept bar's last onset at the bar's end becomes a note at the next bar line.

**Check:** No survivor with a note of length 0 or two onsets alike in a line, on songs 49 to 51.

### 749.2. The chant again: the judge's pick sings a run in the chorus's first lines

**Problem:** As 746: the readings place the judge's pick inside the kept range although its chorus opens on one note, repeated.

**Evidence:** Song 51, main: b121d283f86f sings A3 six times on "Every hour is a wire" and six times on "run from the cradle to the stone"; 16 of its 64 sung lines hold one note four or more times running; its longest run is 6, inside the kept range. Among 245 eligible builds none is free of such lines (the fewest, 3); 15 keep chorus 1's lines to runs of three or fewer. The writer chose 89e71513033a among those (charge 0.0002, as the judge's pick).

**Fix (proposed):** 746's: read runs by line and add it to 730's eligibility.

**Check:** As 746, on songs 48 to 51.

### 749.3. Placement deaths at lines of ten syllables in two bars

**Problem:** A line of ten syllables in two bars after a line given four dies for want of a placement in about half the builds. With the long lines in two bars, nearly every build died.

**Evidence:** Song 51 main: 478 deaths a thousand, all at the pre-choruses' first lines: "The coffee's gone cold in the paper cup" 299, "The ice is all water in the glasses" 134 and 13 in the prefit's "again", Pre 3's 22; the control's the same (242, 148, 18, 26). In a 20-build test with two-bar verse lines, 18 of 20 died, at the verse lines (10 to 13 syllables); the writer gave the verse lines four bars. 747 found the same on song 50 at lines of 9 to 10 syllables.

**Fix (proposed):** 230: a line's slot from its syllables before the writer's form is applied, so a line of ten or more syllables gets room (three bars, or the previous line's tail); with 747's split of held notes for lines sung again.

**Check:** Deaths for want of a placement under 20 a thousand on songs 50 and 51.

### 749.4. Luthier draws only in 4/4; the metre should be a parameter, with kept tables per metre

**Problem:** The bar (48), the beat (12), the strong positions and every kept table are 4/4. A 6/8 song can only be set as swung 4/4, which holds two syllables a beat (eight in two bars); song 52's lines carry 10 to 14.

**Evidence:** Song 52 (The Room Next Door, 6/8) was drawn by a compound-metre sketch of Luthier's method (gen68.py) with kept tables from the Essen folk-song collection: 922 sung tunes in 6/8 against 923 in 4/4 (tables\_68.py; tables/essen\_meter\_tables.json in songs/p62). The pitch readings match closely between the metres (median repeated notes 21.6% against 20.0%; steps 47.6% against 50.9%; leaps 11.4% against 11.4%; longest run 3 against 3; range 13 against 12). The rhythm readings do not: onsets on the beat 42.5% against 77.6%; gaps of an eighth 62.5% against 34.1%; gaps of a quarter or more 25.0% against 61.3%. The commonest 6/8 bar is quarter-eighth, quarter-eighth (0, 12, 18, 30), 2,295 of 11,288 bars; the commonest 4/4 bar is four quarters (1,988 of 11,834).

**Fix (proposed):** Make the metre a parameter: the bar's length and its beats (6/8: 36, beats 0 and 18; 3/4: 36, beats 0, 12, 24; 7/8: 42, beats 0, 12, 24), and the kept rhythm tables by metre (bars, two-bar windows, gap classes, palettes); keep the pitch tables shared. The sketch's mapping of Luthier's modules (653/680 a kept two-bar window by syllable count; 731 stress onto the beats; 288/314 registers; 650 intervals from the kept shares; 'again' and 'copy'; 730's charge on the kept quartiles) is a first draft of the port.

**Check:** A 6/8 song drawn by the engine, every reading read against kept 6/8 quartiles.

### 749.5. The stress rule restated for compound metre

**Problem:** 731 reads entries before, on and after the bar line. In 6/8 the question is whether stressed syllables land on the bar's two beats, and its kept table needs sung songs with words; Essen has none.

**Evidence:** The sketch scored stress onto the beats and required 55% of the stressed syllables on a beat in the freshly drawn lines (40% overall); 1,217 of 3,000 builds died there. The pick puts 47% of its stressed syllables on a beat (the refitted verses lower).

**Fix (proposed):** A kept stress-to-position table per metre from a sung corpus with lyrics; until then, the sketch's rule.

**Check:** Stressed syllables on the beat within ten points of the kept share, on song 52.

### 749.6. The bass routine reads only 4/4 bars

**Problem:** bass\_v134 writes on bars of 48 twelfths; it cannot write a 6/8 bass.

**Evidence:** Song 52's bass was written by hand: the root on the first beat, the fifth or a step toward the next chord on the second.

**Fix (proposed):** The bar's length and beats as parameters of the routine, with kept bass tables per metre.

**Check:** A 6/8 bass from the routine passing its window tests.

### 749.7. A dense lyric in 6/8 sits far above the folk tables' density

**Problem:** Song 52's lines carry 10 to 14 syllables in two bars of 6/8: 5.35 notes a bar against Essen's 4.0 median (75th 4.33), and sixteenth-note gaps in 27% of moves against 5.7%. The kept windows thin out above 12 notes (31 windows of 14 notes).

**Evidence:** As above; the sketch did not charge notes a bar, the gap classes, range or distinct pitches, since the lyric and the designs set them.

**Fix (proposed):** Kept 6/8 tables by notes-a-bar cell (as 714 and 738 do for 4/4), from a corpus with more syllables a bar (sung ballads, hymns), before the engine charges rhythm in 6/8.

**Check:** The pick's gap classes inside the kept quartiles of its own cell.

### 749.8. A returning chorus has no rule for change

**Problem:** 'copy' sings chorus 2 exactly as chorus 1. The hook should return unchanged, but a whole chorus sung note for note again reads as a loop, and outside readers flag it often (the writer, 15 Nov).

**Evidence:** Song 52 before: chorus 2 differed from chorus 1 in 0 of 49 notes; songs 48 to 51 the same. Tried on song 52 (vary68.py): the first line and the hook exact; on each inner line the longest stressed held note (or the line's last) lifted to the nearest chord tone above, within a minor third (a fourth for a line's last note), at or under the section's cap, no run of four, no leap past a fifth; the final chorus's copied line takes the lift. Result: "sunlight" A4 to B4, "door" (line 3) E4 to A4, "all" A4 to B4: 3 of 49 notes, rhythm unchanged, every gate passing, the charge unchanged at 1.69. Pick of record now 9bf4a225b954 (drawn as 8f4cc7fe75bf).

**Fix (proposed):** 'copy' becomes 'return', as tried. Later, optionally: a rhythmic variant where a returning line's words change.

**Check:** On songs 48 to 52, each returning chorus differs from the first in 1 to 10% of its notes, never in its hook or first line, and passes every gate.

### 749.9. The harmony shadows the lead

**Problem:** The harmony parts take the nearest chord tone a third or fourth from each lead note, in the lead's rhythm: they move with the lead almost all the time, never against it, and keep to three distances from it.

**Evidence:** Song 52, read at each pair of the lead's onsets inside the harmony (the hook in every chorus, every line of the final chorus). Before: the high part moved with the lead 74% of the time, against it 0%, held 26%; the low part 85%, 0%, 15%; three distances each. After (harm68.py: a high part with the words chosen by least cost over each phrase, small moves and holds cheap, contrary and oblique motion cheaper than similar, parallel fifths, octaves and tritones ruled out; a low part singing "ooh" in long notes, at most one change a beat, chord tones only): high 22% / 12% / 66%, six distances; low 15% / 2% / 83%, nine distances, 18 notes (17 held) instead of 70. No parallel fifths or octaves in either version.

**Fix (proposed):** Harmony written as lines, as tried; the motion readings added to the checks.

**Check:** On songs 48 to 52, each harmony part moves with the lead under half the time, with no parallel fifths or octaves.

### 749.10. Nothing plans or reads the song as a whole

**Problem:** Every reading the engine charges is local (per note, per bar, per two-bar window), and every register comes from the section's kind, never its place in the song. So the verses sit at one height, the last chorus is no higher than the first, and the song's top comes early.

**Evidence:** Song 52 before: verses 1 to 4 within 0.2 semitones of each other on average (B3 to A4 each); the last chorus's lines 0.75 below chorus 1's; the top, D5, first in bar 21 of 84 (24% of the way in). Tried on song 52, third edition (shape68.py): a target mean for each section by its place (verses 1 and 2 as drawn, verse 3 about +0.75, verse 4 about +1.75, the last chorus above chorus 2), reached by moving whole lines up one step of the scale (latest line first, each once), the shape kept, with chord, cap, run and leap repairs; and the last chorus's first "door" on E5, once. After: verse means 64.5, 64.6, 65.5, 66.4; the last chorus's lines 1.0 above chorus 1's; the top, E5, in bar 77 (90%); the note-level readings and the charge unchanged (1.69; leaps 12.5%). A first try that lifted single notes again and again (134 lifts, notes moved up to a fifth) bent the tunes and pushed leaps out of the kept range; it was dropped. Pick of record now e1051a4a6d7f.

**Fix (proposed):** A song plan read before the melody is drawn: a target mean for each section by its place, and the song's top placed late; reached by moving whole lines by a step of the scale, as tried. Song-level readings added to the judge: the verses' rise, the last chorus against the first, the top's place. A key change is a later option.

**Check:** On songs 48 to 52: the later verses at or above the first, the last chorus above the first, the top in the last third, every note-level reading still in its kept range.

### 749.11. A hymn needs a hymn mode and hymn tables

**Problem:** The engine has no strophic mode: one tune for every stanza, the rhythm's frame set by the stanza's meter (Common Meter, iambic), stressed syllables on downbeats. And the Essen folk tables do not describe hymn tunes: in a hymn frame every bar is one of three rhythms.

**Evidence:** Song 53 (Sung to Sleep, a Christmas carol in 3/4, Common Meter with refrain) was drawn by a 3/4 sketch (gen34.py) with kept tables from Essen's 1,601 tunes in 3/4 (tables\_34.py, song 52's builder); the frame was built by hand and drawn inside. Every survivor's distinct rhythms over bars sat under the kept range (the pick 16%, kept 35% to 67%); onsets on the beat 100% (kept 57% to 82%); notes a bar 1.9 (kept 2.8 to 4.0), all set by the form, printed, not charged. The pitch readings sat inside the kept ranges (charge 0.61, all of it rhythm variety).

**Fix (proposed):** A hymn mode: the stanza's meter (CM, LM, SM, 87.87 and so on) gives each line's pickup, stressed downbeats and held ending; the tune drawn once and checked against every stanza's stresses. Kept tables from a hymnal corpus for the readings the frame leaves free.

**Check:** A Common Meter tune whose rhythm readings sit inside kept hymn-tune quartiles, sung to every stanza with every stressed syllable on a downbeat.

### 749.12. A descant module

**Problem:** The engine has no descant. Song 53's was written with 749.9's harmony-as-lines search (above the sopranos, in their rhythm and words, chord tones of the four-part chord, the summit pinned).

**Evidence:** The descant moves with the tune 26% of the time, against it 35%, holds 39%; no parallels; its top, A5, once, on the final refrain's "world" (bar 71 of 80), the same beat as the tune's F5. A first pass pinned the summit after the search and left a parallel fifth beside it (in the refrain's first line); with the pin inside the search and the floor lowered, it went.

**Fix (proposed):** A descant module for the last stanza or refrain: its own rhythm allowed, the summit placed late and pinned inside the search, kept tables from published descants.

**Check:** No parallels with the tune or the bass, the summit in the last quarter, the line above the tune throughout.

### 749.13. Choral documents from one timeline

**Problem:** A choir and an organist need their pages to agree bar for bar; documents engraved separately drift.

**Evidence:** Song 53's organ full score and hymn page come from one record and share one global line (time, keys, bar lines, marks, a break every fourth bar): bars 1 to 80 fall on the same systems in both; every voice (choir, descant, organ manuals, pedal) read back from MIDI note for note; 46/46 consistency checks. 749.8 to 749.10 carried into the hymn form: verse 4 in F, in unison over the organ's own harmony (a different chord on 25 of 31 notes); the final refrain in four parts with the descant; no part moving with the tune more than 26% of the time, the tenor and bass against it 33% to 58%, no parallels; the tune's top, F5, in bar 71 of 80 (88% of the way in).

**Fix (proposed):** The engine's standard for choral output: one timeline record, one shared global line with forced breaks, every document written from it, the readback per voice.

**Check:** On any choral song: the same bars at the start of every system in every document, every voice matching the record.

### 749.14. The engine has no accompaniment

**Problem:** Nothing in the engine writes an accompaniment. Song 53's first organ part doubled the choir's four parts for most of the carol, and its introduction and verse 4 were in the same plain texture: correct, and too plain for an organist's score (the writer: "The organ music looks incredibly easy. Are you sure that's right?").

**Evidence:** First version: outside a 4-bar introduction and a 2-bar link, the organ's notes were the choir's (right hand two notes, left hand one, pedal the bass); no eighth notes; no coda; 70 bars. Rewritten (the writer's A: build through the carol): an 8-bar introduction on the refrain's tune over a rocking left hand and a held pedal; verses 1-3 a fuller form of the choir's harmony (three notes in the right hand on 41 of 57 chords); a 4-bar link; verse 4's right hand held below the tune throughout (never doubling it), with a suspension; the final refrain over a tonic pedal under "Hush now" and a dominant pedal under "is sleeping, sleeping"; the left hand rocking in eighths through the introduction, link, verse 4 and final refrain; a 4-bar coda; 80 bars; every note read back from MIDI.

**Fix (proposed):** An accompaniment module for keyboard-led songs: a texture plan by section that builds through the song (doubling and support early, independence late), figures by metre (rocking eighths in 3/4), pedal points at phrase openings and before cadences, suspensions at chord changes, an introduction from the refrain's tune and a coda from its last phrase.

**Check:** On any keyboard-led song: the texture grows by section, the late sections do not double the tune, every note fits its chord or resolves by step.

### 749.15. The metre atlas: kept tables for metres beyond 4/4 are ready

**Problem:** 749.4, 749.5, 749.9 and 749.11 each need kept tables the engine does not have: rhythm by metre, stress-to-beat by metre, four-part motion from real settings, hymn tunes.

**Evidence:** Built while the engine was offline (the writer, 15 Nov): tables/metre\_atlas in the repository and the Doc "Metre atlas: a head start for Luthier beyond 4/4" (https://claude.ai/artifact/58vnmJPuJ8U9hyDLq47SVR). Sung tables for 2/4, 3/4, 4/4, 2/2, 3/2, 4/2, 3/8, 6/8, 6/4 (62 to 1,199 Essen tunes each) and instrumental tables for six metres (169 to 743 dance tunes), kept apart. Across nine sung metres the pitch readings barely move (turns, range and longest run within 8%) while every rhythm reading moves (spreads 0.65 to 3.2, even in beat units). 6/4 reads as 6/8 in beat units; 3/2 and 4/2 are a plainer style, not slow 3/4 and 4/4; 3/8 is felt in one; 9/8 behaves like 6/8 per beat. From the Open Hymnal Project's 301 hymns (about 40,000 English words scored): stressed syllables on the downbeat 81% in 3/4, on beats 1 and 3 89% in 4/4, on the two main beats 84% in 6/8; altos move with the soprano 35% to 39% of the time and hold 44% to 47%, basses move against it 34% to 40%, parallels about once a hundred moves, 7% to 10% of inner-voice notes shorter than the beat; 3/4 hymn tunes run 2.1 to 2.7 notes a bar with 16% to 32% distinct bar rhythms. 5/8, 5/4 and 7/8 have 7, 4 and 2 sung tunes, so their groupings (5/4 as 3+2 or 2+3; 7/8 as 2+2+3, 3+2+2, 2+3+2; Balkan 9/8 as 2+2+2+3) come from research.

**Fix (proposed):** The port set out in the atlas: a metre object with beat groups; rhythm tables by felt metre from sung tunes (6/4 from 6/8 by scale; 9/8 and 12/8 from 6/8 per beat; additive metres from their groups); readings in beat units; the stress table per metre (749.5); four-part motion quartiles per voice (749.9); hymn quartiles for a hymn mode (749.11).

**Check:** A song in each of 3/4, 6/8 and 9/8 drawn by the engine with every reading inside its metre's kept quartiles, and its stressed syllables within ten points of the hymn table.

**Round 2 (15 Nov):** after a deep-research round, three collections were added and every table tagged with its licence: OpenScore Lieder (1,462 art songs, 342 English; CC0), OpenEWLD (502 lead sheets, 447 English; MIT) and SymbTr (2,200 Turkish pieces, about 1,550 sung; CC BY-NC-SA, non-commercial). English stressed syllables on strong beats in 6/8: 84% (hymns), 86% (art songs), 86% (lead sheets); 9/8 82% and 12/8 84% (art songs, the 12/8 on 3 songs); popular 4/4 syncopates (11% of stresses off the beat against hymns' 1%). The additive groupings were measured from SymbTr's onset weights and match the literature wherever it gives one (aksak 9/8 2+2+2+3; türk aksağı 5/8 2+3; devr-i hindî 7/8 3+2+2; devr-i turan 7/8 2+2+3; curcuna 10/8 3+2+2+3), so the metre object's beat groups can be learned from data. Licence note for the port: the round-1 Essen tables are non-commercial (music21's permission); Lieder, EWLD and the Open Hymnal scores are cleared for commercial use; the Finnish 5/4 archive was unreachable from the workspace.

**Applied to song 53 (Sung to Sleep, second edition, 15 Nov):** the sketch rebuilt on the atlas (the engine still draws in 4/4). The tune drawn from the Open Hymnal's 3/4 bars and charged against the 3/4 hymn quartiles: 18 of 19 readings inside (first edition 17); notes a bar 1.97 to 2.21; half-beat gaps 0% to 7% (hymn median 7%). The four parts weighted toward hymn motion with passing notes: the alto with the tune / against / holding 36% / 12% / 52% (hymns 39% / 13% / 47%; first edition 21% / 27% / 52%); tenor 23% / 28% / 49% (hymns 35% / 24% / 40%); bass 16% / 43% / 41% (hymns 26% / 34% / 38%); short notes in the alto 9% and tenor 5% (hymns 8%, 7%). For the port: a motion target per voice, and passing notes by rate, are enough to bring an alto line inside the hymn ranges; the tenor and bass need more.

### 749.16. An accompaniment plan by section role

**Problem:** The engine gives every section of an accompaniment the same treatment, so a song with repeated verses sounds static and an organ part looks thin even when every bar is correct (song 53, first and second editions: the organ's right hand 0.52 onsets a beat, 19% of bars held chords).

**Evidence:** Organ practice gives each verse a role: hymnal harmony with changes of colour for the inner verses, free harmony for the introduction, the interludes and the last verse (research report "Accompaniment corpora and music theory", 15 Nov). In human pop arrangements, sections of the same type are about 1.68 times more alike than sections of different types (POP909 studies). Song 53's third edition, written to such a plan and measured against the Lieder 3/4 accompaniment table, raised the organ's right hand to 0.89 onsets a beat. It raised the refrain's complementarity from 0.13 to 0.67 and cut held bars from 19% to 5%. Clashes with the choir fell from 28 eighths to 18, and the four outer parallel octaves were removed. The choir parts are unchanged. Still short: the whole-song right hand is under the Lieder floor of 1.13, because verses 1 to 3 keep the hymnal right hand by plan and no organ table exists.

**Fix (proposed):** Before arranging, give each section a role (introduction, support, lift, interlude, climax, close) and a texture for each hand from the accompaniment tables (by metre: textures, onsets a beat, complementarity). Write the bass first in free sections. Store patterns apart from chords and fit them to each chord. Repeat a texture when its section repeats and change it when the role changes. Where repeats share printed bars, vary them by registration or orchestration.

**Check:** Per section, each hand's onsets a beat and complementarity fall inside the table's middle half for its role, or the plan says why not. Sustained bars are no more than the table's share. There are no parallel fifths or octaves between the outer voices, and no more clashes than the plain hymnal version.

### 749.17. A song-wide intensity curve with a late high point

**Problem:** The engine has no plan for a song's intensity over its whole length. Sections are written one at a time, so whether the song builds, where its high point falls, and whether each return rises above the last are left to chance.

**Evidence:** The first "shapes of songs" study (studies/shapes, 15 Nov) tested 4,986 hymn opening lines (Hymnary.org), 214 Billboard melodies plus 739 song structures (CoCoPops), and 11,266 public-domain MuseScore scores (PDMX), with a self-tested method and null models. Every collection shares one shape: a build to a late high point (median at 0.74 of the song for Billboard, 0.64 for PDMX; mean curves highest at about 0.84 to 0.86). No collection falls into types beyond a continuum. Shape adds under 0.5% of the variation in success in the large samples (PDMX views 0.16% and 0.19% in two samples) and a non-significant 2.5% to 3.3% on the Billboard chart. In 100 songs rated moment by moment by listeners, felt arousal climbed with time in the song (R² 0.047), more than any note measure could explain. Of the note measures, the voice singing (β 0.22) and melodic height (β 0.10) carried the most; chord changes carried none.

**Fix (proposed):** Plan a per-bar intensity curve before arranging. Compute it from melodic height, whether the voice is singing, texture (onsets, notes struck together) and dynamics. Place the song's high point between about 0.65 and 0.85 of its length, follow it with a short release, and make each return of a section higher than the last. Score a song by how far it departs from this build, not by which shape type it is: there are no types. Give shape a light weight in the judge.

**Check:** The intensity curve's highest smoothed point falls between 0.65 and 0.85 of the song, or the plan says why not. Each repeated chorus is at least as intense as the one before. There is no menu of fixed shapes.

### 749.18. Judge the notes against what popular music leads a listener to expect

**Problem:** The judge has no measure of how expected a melody or chord progression is against popular music. Novelty and convention are left to the generator's tables, with no calibrated target and no rule for where a surprise belongs.

**Evidence:** A surprise model in the style of IDyOM (variable-order chains up to order 3, trained by folds so a song never predicts itself) scored 21,998 Hooktheory clips. Its scores were set against YouTube views for 10,847 songs, with controls for channel size, video age, duration, category and transcription count. Lower melody and chord surprise went with more views: across songs, β −0.137 for melody and −0.072 for chords, and the note measures added 3.3% of variance beyond controls (p < 10⁻¹³⁹). The effect held among songs by the same artist (1,469 artists, β −0.054 melody and −0.059 chords, 0.3% added, p < .001). Surprise placed in predictable moments (the Cheung term) helped slightly (β +0.023 to +0.025; p = .005 across songs, .06 within artist). Nothing rewarded high surprise. Against the corpus, the engine's chords sit at the 5th to 38th percentile (conventional) and its melodies at the 41st to 67th (middling); Sung to Sleep is at the 41st (melody) and 20th (chords). Studies/surprise in the repository.

**Fix (proposed):** Add to the judge a measure of melody and chord surprise against a large corpus of popular songs. Target melody surprise at or below the corpus median, and reward surprises that come in predictable moments: a fresh chord or note after a settled pattern, not inside an open, uncertain passage. Keep the weight modest; the effects are a few percent at most.

**Check:** A pick's mean melody surprise is at or below the corpus median, or the plan names the moment it spends surprise on. High-surprise events fall where the moment before was predictable (low entropy).

### 749.19. Give the best moments a breath, then a fresh re-entry

**Problem:** The engine has no idea of a song's best moments: where they go, or what the music should do at them. Surprise and texture changes are spread evenly or left to chance.

**Evidence:** In the "moments people love" study (studies/moments, 15 Nov), the 100 most relevant comments on 4,000 Hooktheory videos gave 8,960 timestamped moments in 2,840 videos. 1,546 of them fell inside clips timed beat by beat, and each was compared with the rest of its own clip. At the moment, the voice re-enters after a gap (+0.16 SD, 95% CI 0.10 to 0.23) on a more surprising note (+0.17, 0.09 to 0.25). Two beats before, the melody thins (−0.20, −0.27 to −0.13). The height of the highest note doesn't mark the moment (+0.04, n.s.). The surprising note comes in a more open moment (uncertainty +0.21), so the Cheung pattern doesn't hold at this scale. Comments that mention crying, chills or the voice fall at a median of 0.55 to 0.60 of the song.

**Fix (proposed):** Choose a few best moments per song and place the most emotional in the second half (about 0.55 to 0.6, before the build's peak, 749.17). At each one, thin the melody for a beat or two (a rest, a held note, fewer notes), then bring the voice back on a less expected note: a leap or an unexpected scale degree. Keep the notes around it conventional (749.18). Don't count on a high note alone.

**Check:** Each marked moment has fewer melody onsets in the two beats before it than the section's average, a voice entry at the moment, and a note whose surprise is above the section's average. At least one marked moment falls between 0.5 and 0.7 of the song.

**Relation to Luthier v7:** this is evidence for rules Luthier already has, not a new rule:

- **Window 2's design spec:** the designed silence is the anticipation moment, and the re-entry is the reward moment (Salimpoor's caudate and nucleus accumbens).
- **Window 3:** phrases of 5 to 8 seconds.

The new part is the listener data: 8,960 timestamped moments, the two-beat thinning, the surprising re-entry note, and the placement at 0.55 to 0.60 of the song. Port it as a check on those windows' rules, with these numbers.

### 749.20. Familiar rhythms, pickups, moderate syncopation; rhythmic surprise at the best moments

**Problem:** The judge measures pitch and chords but not how expected a melody's rhythm is, and the generator has no targets for syncopation, density or how phrases begin. Luthier's pop songs run more rhythmically surprising than most popular songs, with short, rest-broken phrases.

**Evidence:** The rhythm layer (studies/rhythm, 15 Nov) turned each note into a token: its position in the bar on a sixteenth grid, its length class, and whether a rest came before it. A surprise model trained by folds scored 22,800 Hooktheory clips. In models with the pitch and chord measures and the same controls, against YouTube views:

- **Size:** rhythm added 1.5% across 10,828 songs and 0.38% within artist (1,466 artists, p < .001), more than melody and chords added together within artist.
- **Holding in both models:** lower rhythm surprise (β −0.085 across, −0.055 within), more notes a beat (+0.053, +0.049), and phrases starting off the downbeat (−0.041, −0.026 for downbeat starts).
- **Syncopation:** an inverted U across songs (squared term −0.013, p = .02) and −0.049 within artist (p = .009).
- **Loved moments:** at timestamped moments, rhythm surprise peaked (+0.21 SD, 95% CI 0.13 to 0.30).
- **Our songs:** the four Luthier pop songs sit at the 51st to 85th percentile for rhythm surprise and the 8th to 19th for phrase length. Sung to Sleep has no breath of a beat or more anywhere.

**Fix (proposed):** Add rhythm surprise to the judge, against a large corpus, with a target at or below the median. Prefer pickups into phrases. Keep syncopation moderate, near the corpus median. Don't let lines get too sparse in pop styles (about one note a beat or more). Spend rhythmic surprise at the best moments, after a breath (749.19). In hymns, give chosen line ends a real breath.

**Check:** A pick's mean rhythm surprise is at or below the corpus median. Most phrases start before the downbeat. Syncopation per note is within the corpus middle half. Each marked moment carries the section's highest rhythm surprise within two beats.

### 749.21. Perception checks: mud, the tune on top, separate lines, phrase length in seconds

**Problem:** The engine checks its voicings and placement against rules from theory books, not against how hearing works. A voicing can pass every rule and still be muddy low down, or bury the sung tune under the accompaniment.

**Evidence:** The research round "Psychoacoustics for the songwriting engine" (15 Nov) gives the basis:

- **Roughness:** Sethares and Plomp–Levelt roughness depends on register. The roughest interval is about 1.5 semitones at C4 and widens each octave down. Hutchinson–Knopoff roughness predicts chord ratings at r = .77, and the Harrison & Pearce composite at .88.
- **The top voice:** the highest line is heard best by listeners of every kind.
- **Separate lines:** Huron's perceptual principles account for the classic voice-leading rules.
- **Phrase length:** short-term memory caps a phrase at about 8 seconds.

Applied to song 53's four editions (studies/psychoacoustics/perception.py), the checks found two real faults. Seven organ pairs sat below the low-interval limits. In verse 4, the organ sat above the unison tune at 22% of sung onsets, after the third edition's fuller voicings. Both were fixed (to 0 and 0.8%) with no other check worse. Sung lines last 8.2 s at ♩ = 88.

**Fix (proposed):**

- **Mud:** score every voicing for roughness at sounding pitch, flag any adjacent pair below its register limit for its interval size, and revoice (an octave up, or another inversion).
- **The tune on top:** keep the sung tune on top. Flag accompaniment above it, notes a second or less from it, and crowding in the octave below it.
- **Separate lines:** apply Huron's rules for separate lines: pitch proximity, no crossings, no parallel perfect intervals between parts meant to stay separate.
- **Phrase length:** measure phrase length in seconds, not bars: 2 to 6 s is ideal, 8 s the most. At slow tempos use two-bar phrase units or add breaths.
- **Roughness above about C4:** treat it as planned tension at suspensions, appoggiaturas and the peak, never as a fault in itself.

**Check:** No adjacent pair is below its low-interval limit. The accompaniment is above the sung tune at no more than 2% of sung onsets. There are no crossings among choir parts. Sung phrases last 8 s or less, or the plan says why.

**Relation to Luthier v7 (corrected 15 Nov):** most of this restates rules Luthier already has:

- **Module 9.14:** Huron 2001, with voice-leading costs and low-interval limits of no third below F3 and no second below C4.
- **Module 9.13:** register.
- **Window 67:** precision weighting.
- **The tension composite:** roughness at 0.15.

The session's first sketch used looser limits than Module 9.14. By Luthier's own limits, song 53's organ broke them at 117 places, mostly the pedal doubling the choir's basses at pitch under a left hand a third above. The new parts to port are:

1. **Module 9.14 for organ and choir:** extend its limits from the demo keys to organ and choir textures, with the pedal written in its own octave (C2 to D3).
2. **Phrase length in seconds:** add it beside Window 3's 5 to 8 seconds.
3. **The tune on top:** count accompaniment above the sung tune.

Song 53's fourth edition now has 0 violations of Module 9.14's limits, and the tune is on top at 99.2% of sung onsets.

### 749.22. A two-channel judge: what audiences watch and what musicians re-record

**Problem:** Luthier's judges rank builds against kept songs, and its own spec twice names cover counts as the missing yardstick for songs that last. There is no outcome that measures songwriting apart from fame and production, and none that separates what audiences reward from what players reward.

**Evidence:** In the covers study (studies/covers, 15 Nov), SHS100K, the SecondHandSongs research release, was matched to 1,039 Hooktheory songs; 780 had note measures and YouTube views. Cover counts went with views only weakly (r = 0.15). Beyond views and controls, the notes explained 4.0% of covers (p = .008), and 4.7% among the 705 songs by their original artist (p = .004). In the same songs they explained 1.7% of views. Three measures predicted covers and not views:

- **Less chord repetition within a section:** β −0.124, p = .003.
- **The Cheung term for chords** (surprise after a settled stretch): β +0.076, p = .03.
- **More syncopation:** β +0.087, p = .02. Within artist it went with fewer views (749.20).

Against views across 10,847 songs (749.18, 749.20), predictability won.

**Replication (Discogs-VI, 2,360 songs, with the song's first release year controlled):** covers and views are unrelated (r = 0.00). Notes add 1.5% to covers (p < 10⁻⁹).

- **Replicated:** less chord repetition within a section (β −0.071, p < .001; not views).
- **New:** more rests (+0.041, p = .045) and more varied note lengths (+0.039, p = .048) go with covers. Density splits the channels: −0.036 for covers (p = .08) and +0.087 for views (p < .001).
- **Not replicated:** the chord Cheung term (+0.009, p = .54) and syncopation (+0.022, p = .16); both are treated as unconfirmed.

LargeSHS is not published at the address its paper gives.

**Fix (proposed):** Judge each candidate on two channels. The audience profile is 749.18 and 749.20: predictable melody, chords and rhythm, pickups, moderate syncopation. The musician profile, as replicated, is harmonic motion (chord repetition within a section below the corpus median in at least one section), room in the melody (rests and varied note lengths), and conventional chord choices; settled-moment chord surprises and syncopation stay unconfirmed. Prefer candidates that do well on both rather than maximising either. Replicate on LargeSHS (218,407 works) when it is published.

**Check:** A pick sits at or above the corpus median on both channel scores. Where the two disagree, the sung line follows the audience profile and the harmony and accompaniment follow the musician profile.

### 749.23. Chromatic harmony: a style the engine can choose, not a default

**Problem:** The maintainer's review of 28 songs found that the engine places one borrowed chord or one modulation well but never lives in chromatic harmony: secondary dominants and borrowed chords as ordinary language, modal mixture across a section. It proposed pushing in that direction. The cause is in the spec: the Departure Cost Framework (Window 19.9) charges 1 unit for every borrowed chord or secondary dominant and 2 for a resolving secondary dominant or a parallel-minor lift, against a ceiling per song, so the engine spends one and goes home.

**Evidence:** studies/chromatic (report: "Chromatic harmony: views, covers and our songs").

- **Our songs:** chord symbols from 31 songs (p21 to p63). 15 have no chromatic chord, 9 have one, 7 have two to four. The median is 2.5% of chord mentions outside the key (popular median 4.4%). The commonest is ♭VII (9 songs). Only The World Is Asking and A Wire Pulled Tight use several applied dominants. The maintainer's reading holds.
- **Audiences:** in 10,749 Hooktheory songs, a 1 SD larger chromatic share of chord time goes with −0.14 SD log views over the controls (p < .001), −0.07 with the note measures held, and −0.13 within one artist's songs. Mixture carries most of it. Applied dominants carry no penalty once the note measures are held (+0.00, p .78).
- **Musicians:** no effect on covers in Discogs-VI (2,355 songs; chromatic share +0.01, p .61). SHS100K (781) leans positive for sections that live in chromatic harmony (+0.10, p .01 with the note measures) and for applied dominants (+0.08, p .06), but the larger source does not confirm it. 749.22's musician channel is about chords that change within a section, not chords outside the key.

**Fix (proposed):** Keep the departure budget as the default; the audience data support rationing, and the musician data give no reason to spend more. Add a chromatic home as a style option chosen at intake, for songs whose style lives there (gospel, jazz, prog, art song, some worship), built like the synthetic modal homes: a section declares its chromatic vocabulary; each chord costs 1 unit when it first enters and nothing for the rest of that section. Within it, prefer applied dominants that resolve to their target, and use mixture sparingly outside the lament and groove homes. The sung line stays plain over it (melody surprise at or below the corpus median, 749.18). Grade B for the views penalty; C for applied dominants and covers.

**Style norms (hymns and art song, added the same evening):** Roman-numeral analyses (When in Rome, CC BY-SA 4.0; OpenScore Lieder) give the chromatic share of chord time in the local key: Goudimel psalms 4.2% (41), Bach chorales 6.2% (371), art songs 13.3% (179 human analyses) to 15.4% (1,083 automatic); popular songs 4.4%. The kind differs more than the amount: popular songs use mostly mixture, while psalms, chorales and art songs use applied dominants at about 2% to 4% of chord changes, and art songs add diminished sevenths, augmented sixths and the Neapolitan. About half of the chorales' and art songs' 8-bar spans hold two or more chromatic chords. English hymns (Open Hymnal, 295, measured from the notes) sit near the psalms. Our songs (2.5%, mostly ♭VII) are below plain hymns and use the popular kind even in songs 52 and 53. So the chromatic home carries a norm per style:

- **Hymn mode:** applied dominants are ordinary and cost nothing, about 2% to 4% of chord changes (one or two a verse, often at a cadence: V/V, V/vi, V/ii); mixture under 2%.
- **Chorale or art-song style:** chromatic chords in about half of 8-bar spans, a local share of 6% (chorale) to 13% to 15% (art song), with diminished sevenths, augmented sixths, the Neapolitan and free tonicisation.
- **Popular styles:** the v7 budget; mixture is the native kind there and the one audiences penalise most.

**Check:** A song with the option has at least one section with two or more distinct chromatic chords and at least a quarter of its chord time outside the key (the popular 75th percentile, 24.7%); every applied dominant resolves; the sung line's surprise stays at or below the median. Songs without the option stay within the v7 budget, and their scores on both channel profiles do not fall.

### 749.24. The engine assumes a bridge

**Problem:** Song 54 has no bridge. Six readers in the v7 file read the bridge and stopped the run: the bridge plan draw, the era reading's three windows, 278's aims, 208/279's bridge-opening gate, the lift's bridge median and the reading's bridge axes.

**Evidence:** The first smoke test failed on each in turn; songs 48 to 51 all had bridges. gen\_l7\_p64.py guards them (the era read over the two windows present).

**Fix (proposed):** Make the bridge optional: draw its plan only if it is sung; read the era over the windows present; leave the bridge's aims and gate unread when there is none.

**Check:** A song with no bridge runs with no song-specific guard; songs 48 to 51 reproduce their orders.

### 749.25. Placement deaths at nine- and ten-syllable lines with borrowed rhythms

**Problem:** Two-thirds of song 54's builds died for want of a placement (667 main, 662 control a thousand), the most of any song since v7 (741, 747, 749.3).

**Evidence:** A trace (songs/p64/diag/trace\_place.py) wrapped the rhythm draw over 80 control builds. Failed and kept calls had the same room (earliest start and latest last onset alike), so the window is not the cause. The failures fall on lines of 9 and 10 syllables in two-bar slots whose rhythm is borrowed: verse lines sung again on verse 1's onsets (712), and verse 1 and chorus 1 lines drawn on a partner's or a returning unit's bars (310, 361). Main, by line: verse 2 line 7 (10 syllables) 168; verse 3 line 6 (10) 122; chorus 1 line 5 (9) 72; verse 1 line 3 (9) 68; chorus 2 line 5 (10) 59. Of the 58 sung lines, 18 have 9 syllables or more.

**Fix (proposed):** When a borrowed rhythm cannot take a line's syllables, split its longest note (as 682 does for the template) or draw the bar fresh, rather than end the build.

**Check:** Song 54's main run keeps its pick; placement deaths under a third; songs 48 to 51 reproduce.

### 749.26. Two syllables on one onset, in most of the clean survivors

**Problem:** 749.1 again, and larger: 87 of song 54's 143 clean survivors (61%) sing two syllables on one onset, and the judge's pick d48480b70b0d was one of them ("coffee" and "can", verse 4: the second syllable of "coffee" has no length).

**Evidence:** Main run. Re-picked by 730's rule over the other 56 (42 eligible): d12c2728e6f1, charge 0.0005, place 0.862, its most-repeating window 0.843.

**Fix (proposed):** A note of no length is a death (or 715 makes the build ineligible); find where the second onset is lost.

**Check:** No survivor with two syllables on one onset, on songs 49 to 54; a pick that had none unchanged.

### 749.27. The band-over-the-tune limit does not carry over to a low lead

**Problem:** 749.21's limit (the accompaniment above the sung tune at most 2% of the time) was set on organ and choir, where the tune is the top line. With a baritone under guitars, fiddle and steel, most of his notes have something above them, as on most country records.

**Evidence:** Song 54: him 81%, her 15% (her accompaniment kept below her); within a second of the tune 13%; the voices 5.2 dB over the band; no low-interval breaks once the acoustic voicings were rewritten (586 before).

**Fix (proposed):** Keep the 2% limit where the tune is the top line (choir, organ, a high lead). For a lead below the band, read salience by level and by what lies within a second of the tune.

**Check:** Songs 52, 53 and 54 each pass under the rule that fits them.

### 749.28. A story's turn falls later than the shape targets

**Problem:** 749.17 puts the high point at 0.65 to 0.85 of the song and 749.19 the breath at 0.55 to 0.60. In a story song whose twist is in the last verse, both fall late.

**Evidence:** Song 54: the breath (the band stops on beat 3 of bar 108) at 0.853; the top at chorus 4, her entry, 0.857 to 0.952; each chorus above its verse and each return above the last. Her entry is the payoff and cannot move earlier without changing the story.

**Fix (proposed):** Read the targets against the song's turn when the type is Narrative: the breath before the turn and the high point at it, wherever the story puts them, with the release after.

**Check:** A Narrative song's breath and top fall at its turn; other types keep 0.55 to 0.60 and 0.65 to 0.85.

### 749.29. The lexicon check: dialect forms and "a.m."

**Problem:** Five of song 54's six unknown words were g-dropped forms of known words (sleepin', mornin', fixin' and so on); "Git 'n' Split" read its "n" as the letter N, stressed; "a.m." splits into "a" and "m". Protocol 0b v67 asks one word at a time; the writer's rule is one question a turn, so the six went as one question.

**Evidence:** Song 54's intake; the readings in gen\_l7\_p64.py (LEX64); "'n'" added to the function words.

**Fix (proposed):** Derive -in' forms from the -ing entry; read "'n'" as unstressed AH0 N and "a.m." as one word, EY2 EH1 M; ask only words with no derivable reading, all in one question.

**Check:** Song 54's lyric needs only "mildewed" asked.

Also read on song 54 (no finding): melody surprise 3.05 bits against the popular median 2.89, rhythm 3.42 against 2.49 (749.18, 749.20 not met; the engine does not yet charge them); chords 1.85 against 3.79; no chord outside the key (749.23); phrases 1.0 to 6.8 seconds (749.21). The pick of record's longest run of one pitch is 9 (the kept 90th percentile 9.5).

## Running total

- **Songs on Luthier v7:** 5 (48 The Ratios Hold, 49 The World Is Asking, 50 The Small Things, 51 A Wire Pulled Tight, 54 The Man Mama Prayed I'd Be). Song 52 (The Room Next Door, 6/8) was drawn by a compound-metre sketch, not the engine.
- **Findings since v7:** 39 (740 to 749, 749.1 to 749.29). One is a bug (749.1); four (749.4 to 749.7) are the plan for metres other than 4/4; three (749.8 to 749.10) are about variety and the song's shape, each tried on song 52 with the before and after and carried into song 53; four (749.11 to 749.14) are for hymns, choral output and accompaniment; one (749.15) hands over the metre atlas; one (749.16) is the accompaniment plan by section role, tried on song 53's third edition; one (749.17) is the song-wide intensity curve from the shapes study; one (749.18) is the surprise-against-expectation measure from the YouTube study; one (749.19) is the breath-then-fresh-re-entry rule from timestamped comments; one (749.20) is the rhythm layer; one (749.21) is the perception checks from the psychoacoustics round; one (749.22) is the two-channel judge from the covers study; one (749.23) is the chromatic-harmony test, a style option rather than a default; six (749.24 to 749.29) are song 54's: the assumed bridge, placement deaths with borrowed rhythms, two syllables on one onset in most survivors, a perception limit that does not carry to a low lead, the shape targets in a story song, and the lexicon's dialect forms; the rest are readings or proposals.
- **Picks of record not the judge's:** 3 of 5 (songs 49, 51 and 54): two for chanting (728, 740, 746, 749.2), song 54's for two syllables on one onset (749.1, 749.26).
- **Failing on every song:** bits saved a gap (744); the per-note share against every neighbour (745, 734); unstressed entries on the bar line (742, 749).
- **Placement deaths over target:** songs 49, 50, 51 and 54 (741, 747, 749.3, 749.25).
- **Not yet possible on the engine:** any metre but 4/4 (song 50 asked for 6/8 and was set in swung 4/4; song 51's tempo plan was written at double tempo in 4/4); song 52 is in true 6/8, by the sketch, with kept 6/8 tables from Essen (749.4 to 749.7); song 53 is in 3/4, by the hymn sketch, with hymn tables (749.11), and the metre atlas holds kept tables for every common metre (749.15).

## Regression line

Songs 40–47 are closed (523, 571). Song 48's record stands on v134 (5440fb310f58 / ce6f70d21d6a). Its reruns: v136 473ea72c00d9 / 54d5fcc4eae6; v137 104d263b6bd6 / 25552792b7c3; Luthier v1 da01fc0096fb / 1ddae17ce4bc; Luthier v2 e6f259b64c38 / a6023c8db5cb; Luthier v3 run A c6ee6ce5c6a4 / da3ddf5aaf62, run B 2276b48371d3 / 7d544b83f0f7; Luthier v4 e897f1e17e02 / 8924d5f25684; Luthier v6 21a41b55f90a / 3021b2a276db; Luthier v7 db3ed0fc13ab / 44de852103a9. Song 49: Luthier v4 a467ceb242b7 / e8691d73b008; Luthier v6 ef9d3a2a2039 / bf016d1e7243 (pick of record e2b80cdc3a1c); Luthier v7 cb0a317e10d9 / 9787becabe8d. Song 50: Luthier v7 46073782f2d5 / cd7f41ab51d3 (pick of record f583fd857dda). Song 51: Luthier v7 a37686ce104b / 37c6e1ffbafb (pick of record 89e71513033a). Song 54: Luthier v7 63a84b18e7dc / c43334ae0deb (pick of record d12c2728e6f1).

## Blind-pick tally

35 songs: Annotated top 15, Middle 10, Remembered top 9, Refrain 1 (song 52: Annotated, "and I said hello through the plaster that night") (song 50: Middle, "And I think somebody's watching this"; song 51: Remembered, "a second stretched thin like a wire pulled tight"; song 54: Middle, "The man Mama prayed I'd be"). Not yet offered: songs 40, 41, 43, 44, 45 and 46.
