# ZenEng v130: song 46, Dry Ground (the next song, 522) — test report

*Words and music: Jason Bryant. The spec is ZenEng v130 (Module 27.74). Song 46 was written on the default path: drawn on a 438 chart with 440's step tested on the finished chart, its bass written by the routine, its record built from both. It is read by every reading of Windows 141–149 beside songs 40, 42 and 43, on both draws (479). 530, 531 and 538 were adopted as proposed and 524 is the form's rule. Songs 40–45 are closed (523) and were rerun only as a regression. The paper was not edited. New findings are numbered from 540.*

## What was run

- **The song (522):** song 46, *Dry Ground*, on the default path, written from the writer's intake (Q1–Q13) and his locked lyric.
  - The engine: v129's code of record for song 43 (q = 118, four on the floor, A minor, the tenor row C3–A4), with the song's form, lyric and design written in by gen_v130.py, plus 530 and 531 (adopted as proposed) and 524 (the form's rule).
  - Drawn on a 438 chart, with 440's step tested on the finished chart (513).
  - 1,000 builds main and control, each made twice at PYTHONHASHSEED 0 (seed 20261559).
  - The pick of record: the engine's default (362, with 472), taken as drawn with no hand edits.
- **The record:** built from both the chart and the pick (build_p56.py). The bass was written by the routine (bass_v130.py: 439, 445–448, 516, 517 and 538).
- **Side runs:** song 46, main and control, with 501 off (531's check).
- **Readings,** each on main and control:
  - every test (readings_v130.py);
  - separation on the agreed 30, song 46 beside songs 40, 42 and 43 (their v129 runs of record);
  - Window 147's measures with the engine's window (reread_v130.py), the four songs together and song 46 alone;
  - the judge of record (519);
  - the bass (538), beside v129's routine on the same record;
  - the kept pass rates (kept_pass_v129.json).
- **Regression (523):** songs 40–45, main and control, rerun once from their v129 files and compared with their orders of record.

## Survivors and orders

| Run | Survivors | Order | Made twice, the same |
|---|---|---|---|
| Song 46, main | 773 | 120253ea25cb | yes |
| Song 46, control | 860 | 635084318e00 | yes |
| Song 46, main, 501 off | 756 | 541dc7fed54f | (a side run) |
| Song 46, control, 501 off | 811 | 0371d720feec | (a side run) |

**Regression (523).** Each closed song rerun once from its v129 file, against its order of record:

| Song | Run | Order of record (v129) | Rerun | Reproduced |
|---|---|---|---|---|
| 40 | main | d508b254a8f4 (796) | d508b254a8f4 (796) | yes |
| 40 | ctl | 04342d35cd1d (885) | 04342d35cd1d (885) | yes |
| 42 | main | 9fd23492dad3 (801) | 9fd23492dad3 (801) | yes |
| 42 | ctl | 529bf7a1c186 (820) | 529bf7a1c186 (820) | yes |
| 43 | main | af58ce3be702 (882) | af58ce3be702 (882) | yes |
| 43 | ctl | a095303f51b7 (904) | a095303f51b7 (904) | yes |
| 44 | main | 2f43a0bc93d6 (776) | 2f43a0bc93d6 (776) | yes |
| 44 | ctl | 7d4dd7b83e26 (755) | 7d4dd7b83e26 (755) | yes |
| 45 | main | 6dc6710923f0 (824) | 6dc6710923f0 (824) | yes |
| 45 | ctl | 9a1c46f67b24 (814) | 9a1c46f67b24 (814) | yes |

Every closed song reproduces its order of record, main and control.

## How the v130 rules went in

- **524 (the form gives a line room).** Q11 A laid out the form: every line of nine syllables or more has a slot of three bars or more (12 lines; none flagged, since the lyric allowed it everywhere). Verse and pre-chorus 2-2-3-3 (10 bars), chorus 2-2-3-3-2-4 (16), bridge 3-3-3-3 (12), sung outro 3-3-2-4 (12): 120 bars. The run counts, for each slot, the kept endings (465's classes, 500's shares) it cannot reach, and prints them below.
- **530.** 503's knob takes the full step (×0.6 or ×1.6) each round while verse 2's chord tones on the beat are more than two points from verse 1's; within two points it stays.
- **531.** 501's bound is the kept 5th–95th percentile of onsets a beat (OB501's outer pair) in place of the middle half.
- **538.** In bass_v130.py: in a section with four kicks a bar, each cell of the plan (A B A C A B D E) keeps its own figure of intervals and its own articulation (legato; short off-beats; staccato; accented off-beats), with B's and D's figures and articulations drawn apart from A's.
- **The song.** gen_v130.py writes melody_v130_p56.py from song 43's v129 file, patching whole statements (each asserted to match once): the form, plan, slots, lyric, the sung outro (in the verse's register, ending on the tonic), and the design (Q12 A). The design: "water" on the chorus's high note through 329's carrier, "flood" ending on the tonic and landing by the slot's third downbeat so it can hold two bars, and the last chorus's copy taking the falsetto B4 (outside the row, exempt from the range death, pinned). The four-line pre-chorus takes the verse's line plans. A smoke run (20 builds) passed before the runs of record.

## The song's design and the pick

- **The pick of record:** 3f5704fc0291, the refit judge's first among the survivors with no soft break (362/472); judge 3.02, rank 599 of 773 by the composite. No hand edits.
- **The lift:** median 0.0, top 0, lowest 0, bridge 0.0 (546).
- **The design gate (317, Q12 A):** complete builds passing, main 94.3% (spread 0.7%), control 96.8% (spread 0.6%); nine in ten held. Design deaths 57 / 32.
- **The chart (438):** two or more 0.0 -> 0.192 (target 0.182), held bars 0.117 -> 0.1 (target 0.101); edits 18. 440: root at 100.0% of 131 changes; inversions [] (a step beside each: []).

## 524: the slots and the endings they cannot reach (main / control)

| Line | Syllables | Slot (bars) |
|---|---|---|
| Verse 1, line 3 | 9 | 3 |
| Verse 1, line 4 | 11 | 3 |
| Chorus 1, line 3 | 10 | 3 |
| Verse 2, line 3 | 9 | 3 |
| Pre 2, line 3 | 9 | 3 |
| Chorus 2, line 3 | 10 | 3 |
| Bridge, line 1 | 9 | 3 |
| Bridge, line 2 | 9 | 3 |
| Bridge, line 3 | 10 | 3 |
| Bridge, line 4 | 9 | 3 |
| Last Chorus, line 3 | 10 | 3 |
| Outro, line 1 | 9 | 3 |

The kept endings each slot cannot reach, counted over the builds (a line counted once each time it is drawn):

| Slot | Main | Control |
|---|---|---|
| Bridge:0 (3 bars, 9 syllables) class 3 out of reach | 999 | 997 |
| Bridge:1 (3 bars, 9 syllables) class 3 out of reach | 999 | 997 |
| Bridge:2 (3 bars, 10 syllables) class 0 out of reach | 390 | 393 |
| Bridge:2 (3 bars, 10 syllables) class 2 out of reach | 108 | 109 |
| Bridge:2 (3 bars, 10 syllables) class 3 out of reach | 999 | 997 |
| Chorus 1:2 (3 bars, 10 syllables) class 3 out of reach | 999 | 997 |
| Outro:0 (3 bars, 9 syllables) class 3 out of reach | 999 | 997 |
| Verse 1:2 (3 bars, 9 syllables) class 3 out of reach | 1000 | 1000 |

500's classes by notes and slot against the kept shares (532's check: each within ten points):

| Notes, slot | Lines, main / control | Classes 0 / 1 / 2 / 3+, main | Control | Kept |
|---|---|---|---|---|
| 6 to 8 notes, 2-bar slot | 6302 / 6855 | [0.072, 0.842, 0.079, 0.008] | [0.078, 0.828, 0.087, 0.007] | [0.209, 0.712, 0.079, 0.0] |
| 6 to 8 notes, 3-bar slot | 1263 / 1586 | [0.067, 0.439, 0.485, 0.01] | [0.055, 0.453, 0.471, 0.021] | [0.129, 0.522, 0.282, 0.066] |
| 9 to 12 notes, 2-bar slot | 898 / 345 | [0.081, 0.886, 0.031, 0.001] | [0.09, 0.893, 0.017, 0.0] | [0.265, 0.644, 0.092, 0.0] |
| 9 to 12 notes, 3-bar slot | 4628 / 4414 | [0.081, 0.517, 0.399, 0.003] | [0.084, 0.534, 0.38, 0.003] | [0.165, 0.478, 0.333, 0.024] |
| 13 and over notes, 3-bar slot | 109 / — | [0.092, 0.789, 0.119, 0.0] | — | [0.228, 0.572, 0.162, 0.038] |

## 530: the second verse, main / control

| Draw | Verse 1 / verse 2, chord tones on the beat | 503's knob | Paired test, song 46 (under 0.15 kept sd, of 27) | Pair: same rhythm, onsets shared, pitch kept |
|---|---|---|---|---|
| Main | 0.701 / 0.694 | 0.96 | 19 | [0.159, 0.667, 0.762] |
| Control | 0.699 / 0.733 | 1.6 | 17 | [0.154, 0.643, 0.778] |

Beside songs 40, 42 and 43 (v129, read the same way; verse 1 / verse 2, by song): main 40 [0.721, 0.729]; 42 [0.632, 0.669]; 43 [0.669, 0.694]; 46 [0.701, 0.694]; control 40 [0.697, 0.715]; 42 [0.643, 0.687]; 43 [0.66, 0.676]; 46 [0.699, 0.733].

The calibration's rounds (main): round 1 (0.422, 0.413, 1.0); round 2 (0.71, 0.712, 1.0); round 3 (0.651, 0.661, 1.0); round 4 (0.56, 0.581, 0.6); round 5 (0.755, 0.709, 0.96); round 6 (0.614, 0.616, 0.96).

## 531: the line's rate (501), and the side runs

| Run | 501 inside | Redrawn | Given up (with 465) | Joins before a line | Joins before a copy | Survivors |
|---|---|---|---|---|---|---|
| Main | 15229 | 1357 | 1757 | 0 | 0 | 773 |
| Control | 15134 | 1664 | 1827 | 0 | 0 | 860 |
| Main, 501 off | — | — | 2820 | 2 | 3 | 756 |
| Control, 501 off | — | — | 2807 | 1 | 2 | 811 |

| Notes | Lines, main | Onsets a beat (25, 50, 75), main / control | Kept |
|---|---|---|---|
| 6 to 8 | 7565 | [1.273, 1.556, 2.0] / [1.333, 1.647, 2.0] | [1.25, 1.636, 2.0] |
| 9 to 12 | 5526 | [1.2, 1.375, 1.6] / [1.143, 1.286, 1.455] | [1.286, 1.571, 1.882] |
| 13 and over | 109 | [1.412, 1.529, 1.655] / — | [1.333, 1.586, 2.0] |

## 534: the stream at the windows' own density (song 46 alone)

| Band | Measure | Kept | Main | Control | Windows, main / control |
|---|---|---|---|---|---|
| 3.5 to 4.5 notes a bar | equal_gap_run_max | 4.582 | 4.982 | 4.662 | 796 / 800 |
| 3.5 to 4.5 notes a bar | gap_same_as_before | 0.389 | 0.406 | 0.384 | 796 / 800 |
| 3.5 to 4.5 notes a bar | zigzag_of_three | 0.315 | 0.316 | 0.327 | 796 / 800 |
| 3.5 to 4.5 notes a bar | gap_eighth | 0.489 | 0.531 | 0.54 | 796 / 800 |
| 3.5 to 4.5 notes a bar | turns_per_move | 0.579 | 0.598 | 0.596 | 796 / 800 |
| 3.5 to 4.5 notes a bar | range | 11.146 | 9.873 | 9.909 | 796 / 800 |
| 4.5 to 5.5 notes a bar | equal_gap_run_max | 5.5 | 5.5 | — | 4 / 0 |
| 4.5 to 5.5 notes a bar | gap_same_as_before | 0.42 | 0.468 | — | 4 / 0 |
| 4.5 to 5.5 notes a bar | zigzag_of_three | 0.349 | 0.378 | — | 4 / 0 |
| 4.5 to 5.5 notes a bar | gap_eighth | 0.518 | 0.609 | — | 4 / 0 |
| 4.5 to 5.5 notes a bar | turns_per_move | 0.608 | 0.631 | — | 4 / 0 |
| 4.5 to 5.5 notes a bar | range | 11.108 | 10.0 | — | 4 / 0 |

505's drawable runs (kept, (onsets, share)): main {'3.5 to 4.5': [0.291, [2801, 0.283]], 'under 3.5': [0.271, [15402, 0.239]]}; control {'3.5 to 4.5': [0.291, [3430, 0.159]], 'under 3.5': [0.271, [16270, 0.163]]}. 504's notes to syllables: 1.0396 / 1.0185.

## Separation on both draws (479), song 46 beside songs 40, 42 and 43

The agreed 30 measures, both collections pooled, the first 400 complete builds of each run. Songs 40, 42 and 43 are their v129 runs of record. Main / control.

| Family | Within: 46 | Within: 40 / 42 / 43 | Across, 46's pairs | Across, 40/42/43 among themselves | Across, all four |
|---|---|---|---|---|---|
| agreed 30 | 0.824 / 0.847 | 0.87 / 0.886 / 0.845; 0.867 / 0.884 / 0.862 | 0.689 / 0.67 | 0.756 / 0.722 | 0.723 / 0.696 |
| pitch (agreed) | 0.759 / 0.77 | 0.817 / 0.791 / 0.793; 0.828 / 0.783 / 0.813 | 0.717 / 0.701 | 0.707 / 0.682 | 0.712 / 0.691 |
| rhythm (agreed) | 0.56 / 0.594 | 0.732 / 0.706 / 0.713; 0.721 / 0.732 / 0.703 | 0.572 / 0.567 | 0.677 / 0.638 | 0.625 / 0.603 |
| form | 0.644 / 0.641 | 0.605 / 0.734 / 0.55; 0.551 / 0.716 / 0.549 | 0.492 / 0.449 | 0.497 / 0.483 | 0.494 / 0.466 |
| harmony (CoCoPops alone, apart) | 0.567 / 0.552 | 0.541 / 0.531 / 0.626; 0.529 / 0.536 / 0.585 | 0.541 / 0.486 | 0.541 / 0.537 | 0.541 / 0.512 |

Costs on the 30, pooled over the four songs (points; kept mean, builds' mean):

- **main** (gap 1.89): gap_eighth 0.42 (0.475, 0.572); distinct_pitches 0.31 (6.439, 6.799); range 0.23 (10.895, 10.273); pitch_sd 0.16 (2.967, 2.778); past_fifth 0.15 (0.024, 0.034); empty_bars 0.12 (0.484, 0.27)
- **control** (gap 1.77): gap_eighth 0.33 (0.475, 0.551); range 0.24 (10.895, 10.085); pitch_sd 0.22 (2.967, 2.737); empty_bars 0.13 (0.484, 0.259); past_fifth 0.12 (0.024, 0.032); distinct_pitches 0.11 (6.439, 6.582)

## The first verse and chorus beside the kept songs (both draws)

Window 147's measures, with the window taken the engine's way (519: every note sung in the eight bars, the chord at the note; songs 43 and 46 on A minor). Each song's mean, main / control.

| Measure | Billboard | Rolling Stone | Song 46 | Song 40 | Song 42 | Song 43 |
|---|---|---|---|---|---|---|
| notes_per_bar | 3.937 | 4.143 | 3.6323 / 3.5189 | 4.9473 / 4.8431 | 4.5384 / 4.4458 | 4.2741 / 4.1727 |
| range | 10.67 | 10.587 | 9.8737 / 9.9087 | 9.9887 / 9.5437 | 10.695 / 10.3963 | 10.535 / 10.4925 |
| distinct_pitches | 6.362 | 6.453 | 6.5925 / 6.365 | 6.925 / 6.6238 | 6.8075 / 6.515 | 6.8712 / 6.8238 |
| repeat | 0.273 | 0.291 | 0.2553 / 0.2772 | 0.2829 / 0.2789 | 0.2531 / 0.2714 | 0.2604 / 0.2606 |
| step | 0.436 | 0.417 | 0.4557 / 0.4064 | 0.441 / 0.4387 | 0.4148 / 0.3961 | 0.4523 / 0.442 |
| third | 0.191 | 0.191 | 0.1659 / 0.1977 | 0.1755 / 0.1771 | 0.1975 / 0.1956 | 0.1663 / 0.1803 |
| fourth_fifth | 0.079 | 0.079 | 0.0907 / 0.0824 | 0.0735 / 0.084 | 0.092 / 0.0972 | 0.0865 / 0.0864 |
| mean_interval | 2.071 | 2.03 | 2.1514 / 2.1704 | 2.0198 / 2.0355 | 2.3181 / 2.2578 | 2.1497 / 2.1395 |
| turns_per_move | 0.584 | 0.594 | 0.5981 / 0.5959 | 0.6175 / 0.6194 | 0.6046 / 0.6054 | 0.6123 / 0.6183 |
| last_note_tonic | 0.282 | 0.328 | 0.1837 / 0.2087 | 0.24 / 0.2925 | 0.1775 / 0.1975 | 0.0675 / 0.045 |
| peak_position | 0.315 | 0.293 | 0.2789 / 0.2335 | 0.3348 / 0.2925 | 0.2575 / 0.2483 | 0.333 / 0.3035 |
| on_beats_2_4 | 0.21 | 0.201 | 0.2111 / 0.2241 | 0.2201 / 0.2258 | 0.2149 / 0.2314 | 0.2175 / 0.2236 |
| gap_eighth | 0.465 | 0.449 | 0.5318 / 0.54 | 0.5976 / 0.505 | 0.5906 / 0.6074 | 0.5679 / 0.5503 |
| gap_quarter | 0.186 | 0.175 | 0.1851 / 0.1884 | 0.124 / 0.1545 | 0.1344 / 0.1746 | 0.1624 / 0.1838 |
| gap_longer | 0.2 | 0.177 | 0.159 / 0.1625 | 0.1139 / 0.1196 | 0.1196 / 0.1221 | 0.1564 / 0.1596 |
| first_onset | 0.574 | 0.869 | 0.5272 / 0.5813 | 0.4291 / 0.4494 | 0.4419 / 0.4509 | 0.4106 / 0.4416 |
| bar_rhythm_repeats | 0.229 | 0.192 | 0.1384 / 0.1389 | 0.1583 / 0.131 | 0.1729 / 0.1647 | 0.223 / 0.2263 |
| equal_gap_run_max | 4.867 | 4.378 | 4.985 / 4.6625 | 6.175 / 4.8587 | 5.2375 / 4.835 | 5.175 / 4.6525 |
| gap_same_as_before | 0.387 | 0.364 | 0.4061 / 0.3837 | 0.4898 / 0.3923 | 0.4492 / 0.4274 | 0.4131 / 0.3789 |
| gap_entropy | 1.836 | 1.9 | 1.8033 / 1.9341 | 1.5533 / 1.9345 | 1.6567 / 1.6873 | 1.7479 / 1.8767 |
| most_onsets_in_a_beat | 2.634 | 2.801 | 2.695 / 2.8237 | 2.7975 / 3.05 | 2.9175 / 2.8487 | 2.7412 / 2.8262 |
| phrase_starts_same_place | 0.551 | 0.521 | 0.4409 / 0.4036 | 0.5152 / 0.4673 | 0.5071 / 0.4972 | 0.4675 / 0.4495 |
| zigzag_of_three | 0.315 | 0.333 | 0.3163 / 0.3269 | 0.3483 / 0.3523 | 0.3398 / 0.3454 | 0.3254 / 0.3384 |
| chord_tones | 0.644 | 0.622 | 0.6328 / 0.6714 | 0.6378 / 0.6239 | 0.6198 / 0.6249 | 0.6152 / 0.6241 |
| chord_tones_on_beat | 0.674 | 0.643 | 0.6976 / 0.7161 | 0.6877 / 0.6626 | 0.658 / 0.6615 | 0.6695 / 0.6696 |
| chord_tones_off_beat | 0.612 | 0.603 | 0.5645 / 0.6212 | 0.589 / 0.5847 | 0.585 / 0.5867 | 0.5587 / 0.5748 |
| chord_tones_on_downbeat | 0.729 | 0.705 | 0.7612 / 0.7652 | 0.7576 / 0.728 | 0.6911 / 0.7252 | 0.7066 / 0.6982 |
| empty_bars | 0.515 | 0.736 | 0.5175 / 0.5275 | 0.15 / 0.1313 | 0.3175 / 0.3013 | 0.0938 / 0.0775 |
| downbeat_chord_tone | 0.737 | 0.691 | 0.7612 / 0.7652 | 0.7576 / 0.728 | 0.6911 / 0.7252 | 0.7066 / 0.6982 |
| downbeat_on_root | 0.261 | 0.227 | 0.2373 / 0.2685 | 0.1732 / 0.1564 | 0.2375 / 0.2502 | 0.24 / 0.2287 |
| downbeat_on_third | 0.242 | 0.27 | 0.2721 / 0.2471 | 0.3202 / 0.2807 | 0.2436 / 0.2463 | 0.239 / 0.2501 |
| downbeat_on_fifth | 0.225 | 0.217 | 0.2518 / 0.2497 | 0.2642 / 0.2909 | 0.21 / 0.2288 | 0.2276 / 0.2194 |
| melody_on_root | 0.234 | 0.217 | 0.2217 / 0.233 | 0.1973 / 0.1776 | 0.2049 / 0.2061 | 0.1948 / 0.1917 |
| melody_on_third | 0.201 | 0.199 | 0.2171 / 0.2272 | 0.2057 / 0.1981 | 0.2091 / 0.2105 | 0.2021 / 0.2129 |
| melody_on_fifth | 0.204 | 0.215 | 0.1985 / 0.2151 | 0.2388 / 0.252 | 0.2068 / 0.209 | 0.2207 / 0.2225 |
| melody_a_step_above_a_chord_tone | 0.233 | 0.251 | 0.2454 / 0.2271 | 0.2594 / 0.269 | 0.2283 / 0.2318 | 0.2929 / 0.2931 |
| over_bass_second_or_seventh | 0.18 | 0.19 | 0.1899 / 0.1587 | 0.1754 / 0.1844 | 0.2114 / 0.2049 | 0.2024 / 0.1894 |
| parallel_perfect | 0.147 | 0.102 | 0.0978 / 0.1171 | 0.0868 / 0.0818 | 0.0738 / 0.0844 | 0.0943 / 0.093 |
| contrary_of_moving | 0.435 | 0.394 | 0.4938 / 0.4897 | 0.5303 / 0.571 | 0.538 / 0.5177 | 0.3846 / 0.3755 |

## The judge of record (519)

| Song | Content mean, main / control | Under −0.72, main / control |
|---|---|---|
| 46 | -0.37 / -0.466 | 38% / 39% |
| 40 (v129) | -0.834 / -0.855 | 57% / 56% |
| 42 (v129) | -0.965 / -0.936 | 60% / 60% |
| 43 (v129) | -0.537 / -0.639 | 43% / 47% |

## The range beside the design (520: not aimed)

| Song | Verse window, main / control | Chorus window, main / control | Kept | The design |
|---|---|---|---|---|
| 46 | 10.4 / 10.64 | 9.38 / 9.31 | 10.9 | Q12 A: the falsetto B4 once, in the last chorus (outside these windows) |
| 40 (v129) | 9.65 / 9.22 | 10.19 / 9.94 | 10.9 | no designed range (the song's register and 329's carriers) |
| 42 (v129) | 11.06 / 10.72 | 10.45 / 10.14 | 10.9 | no designed range |
| 43 (v129) | 10.33 / 10.26 | 10.7 / 10.53 | 10.9 | no designed range ('blue movie' falls from the chorus's top) |

## The bass (538): song 46's record, v129's routine beside v130's

Each section's eight bars read with Window 144's measures() against the pop-and-rock quartiles. Window medians, v129's routine → v130's (the record):

| Measure | Pop and rock (25, 50, 75) | Song 46 |
|---|---|---|
| notes_per_bar | [5.125, 7.0, 8.0] | 7.25 → 7.375 |
| pitch_classes_per_bar | [2.125, 2.837, 3.75] | 3.125 → 3.25 |
| on_the_bars_first_note | [0.375, 0.524, 0.725] | 0.5 → 0.5 |
| iv_repeat | [0.2, 0.362, 0.606] | 0.34 → 0.273 |
| iv_step | [0.092, 0.2, 0.324] | 0.167 → 0.172 |
| iv_octave | [0.0, 0.0, 0.048] | 0.018 → 0.033 |
| bar_rhythm_same_as_last | [0.0, 0.143, 0.571] | 0.286 → 0.143 |
| distinct_bar_rhythms | [2.0, 3.0, 5.0] | 3.0 → 3.0 |
| kick_with_bass | [0.696, 0.915, 1.0] | 1.0 → 1.0 |
| bass_with_kick_kicked_bars | — | 0.552 → 0.533 |
| into_the_bar_by_step_of_changes | — | 0.5 → 0.429 |

| Window | Four kicks a bar | Onset rhythms | Onsets and lengths | Rhythm and figure | Every test passed |
|---|---|---|---|---|---|
| Intro, bar 1 | yes | 7 → 6 | 7 → 7 | 8 → 8 | yes → yes |
| Verse 1, bar 9 | yes | 3 → 2 | 3 → 3 | 7 → 7 | yes → yes |
| Pre 1, bar 19 | yes | 2 → 3 | 2 → 5 | 7 → 7 | yes → yes |
| Chorus 1, bar 29 | yes | 2 → 3 | 2 → 3 | 8 → 6 | yes → yes |
| Chorus 1, bar 37 | yes | 2 → 3 | 2 → 3 | 7 → 7 | yes → yes |
| Verse 2, bar 45 | yes | 2 → 2 | 2 → 3 | 7 → 8 | yes → yes |
| Pre 2, bar 55 | yes | 2 → 2 | 2 → 2 | 7 → 8 | yes → yes |
| Chorus 2, bar 65 | yes | 3 → 3 | 3 → 4 | 8 → 6 | no → yes |
| Chorus 2, bar 73 | yes | 3 → 3 | 3 → 4 | 7 → 8 | yes → yes |
| Bridge, bar 81 | no | 4 → 7 | 4 → 7 | 8 → 7 | yes → yes |
| Bridge, bar 89 | yes | 3 → 4 | 3 → 4 | 4 → 4 | yes → yes |
| Last Chorus, bar 93 | yes | 3 → 3 | 3 → 5 | 8 → 8 | yes → yes |
| Last Chorus, bar 101 | yes | 3 → 2 | 3 → 5 | 8 → 6 | yes → yes |
| Outro, bar 109 | yes | 3 → 3 | 3 → 3 | 8 → 8 | no → no |
| Outro, bar 117 | no | 2 → 3 | 2 → 3 | 4 → 4 | yes → yes |

| Test | v129's routine | v130's (the record) |
|---|---|---|
| 445 two or more bar rhythms | 15/15 | 15/15 |
| 445 the bar before repeated in under half | 15/15 | 15/15 |
| 446 2-4 pitch classes a bar | 15/15 | 15/15 |
| 446 38-73% on the bar's first note | 15/15 | 15/15 |
| 447 repeats 20-61% | 15/15 | 15/15 |
| 447 steps 9-32% | 15/15 | 14/15 |
| 447 octaves under 29% | 15/15 | 15/15 |
| 447 no alternating octaves | 15/15 | 15/15 |
| 448 a note on 70% of kicks | 15/15 | 15/15 |
| 448 35-59% of notes on a kick (bars with a kick, 516) | 13/13 | 13/13 |
| 448 a step into the next bar in 25-50% of changes | 11/13 | 13/13 |
| 440 the root at every change | 100% of 131 | 100% of 131 |

## The table of tests: Song 46, Dry Ground

Held in both the main run and the control: 48 of 64 with a test that a kept song can pass. Not held: 325, 338, 347, 351, 360, 370, 375, 378, 389, 391, 465, 458, 490, 500, 505, 405. Many tests name songs 40–45 in their wording; they are read here on song 46's runs. A test no kept song passes read as a build is read is a reading of the mean of builds only (512); the last column is the share of kept songs that pass (496).

| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |
|---|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 6.0%; parallel 0.081 (kept 0.14); paired lines 0, partner given up 0 | under floor 4.7%; parallel 0.08 (kept 0.14); paired lines 0, partner given up 0 | yes | 56% of 170 kept songs |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 100.0%; registers redrawn 0; misses 0 | tonic 100.0%; registers redrawn 0; misses 0 | yes | no kept rate |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 3.0%, chorus 0.0%; leap knob 1.0 | verse 3.5%, chorus 0.0%; leap knob 1.0 | yes | 62% of 170 kept songs |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.0, 0.333, 0.714]; in range 66%; given up 110 (2.8%); left out 1833 | share [0.0, 0.286, 0.6]; in range 67%; given up 124 (3.1%); left out 1619 | yes | no kept rate |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [10.0, 15.0, 17.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.333, 0.421, 0.579]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 100%; floor 4% | range [10.0, 14.0, 17.0, 19.0, 19.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.364, 0.438, 0.588]; tonic nearest the sung median 1.0, the drawn centre 1.0; top fifth 100%; floor 4% | yes | no kept rate |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [-0.12, 0.021, 0.207]; stop none | amplitude 7.0; arch [-0.148, 0.048, 0.232]; stop none | yes | no kept rate |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 29/9214 = 0.003; entries {'starts_on_downbeat': 0.207, 'starts_after_downbeat': 0.695, 'starts_as_pickup': 0.098} | redraws 25/9157 = 0.003; entries {'starts_on_downbeat': 0.202, 'starts_after_downbeat': 0.693, 'starts_as_pickup': 0.105} | reading | no kept rate |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.943} (spread {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.0073}) | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.968} (spread {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.0056}) | yes | no kept rate |
| 318 | the feel named; sixteenths printed | a reading | atmospheric pop, q = 118, four on the floor, straight (Q4 C, Q6 A); sixteenth onsets [0.03, 0.057, 0.108] | atmospheric pop, q = 118, four on the floor, straight (Q4 C, Q6 A); sixteenth onsets [0.068, 0.083, 0.101] | printed | no kept rate |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a | no kept rate |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes | no kept rate |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes | no kept rate |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 0 (0 of another length); given up 0 (0.0%); parallel 0.081; under floor 6.0% | paired 0 (0 of another length); given up 0 (0.0%); parallel 0.08; under floor 4.7% | yes | 56% of 170 kept songs |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 2365; left out 1833; verse 2 in range 66% | one-over bars copied without the weakest onset 2069; left out 1619; verse 2 in range 67% | yes | no kept rate |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 1998 tonic endings, on the nearest to the centre 1.0 | 1994 tonic endings, on the nearest to the centre 1.0 | yes | no kept rate |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 25; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers 20; last chorus on the tonic 100.0%; redrawn 0 | **no** | no kept rate |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.943} | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.968} | yes | no kept rate |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 0 (v109 92); refits {} | join deaths 0 (v109 92); refits {'327: return fitted again without a pickup': 1, '327: copy fitted again after its downbeat': 1} | reading | no kept rate |
| 328 | the sixteenth share beside its band | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.03, 0.057, 0.108] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.068, 0.083, 0.101] | printed | no kept rate |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [19.0, 21.0, 21.0] vs drawn [15.0, 17.0, 19.0] (gap [-5.0, -4.0, -2.0]); chorus window [7.0, 10.0, 12.0]; heaviest give-aways ['outside_scale', 'gap_sixteenth', 'empty_bars', 'chord_tones_on_beat', 'peak_position']; extremes sung low 100%, high 100% | sung [19.0, 21.0, 21.0] vs drawn [14.0, 17.0, 19.0] (gap [-5.0, -4.0, -2.0]); chorus window [7.0, 9.0, 11.0]; heaviest give-aways ['outside_scale', 'gap_quarter', 'empty_bars', 'chord_tones_on_beat', 'gap_sixteenth']; extremes sung low 100%, high 100% | yes | 65% of 170 kept songs |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.081; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | likeness 0.08; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | yes | 56% of 170 kept songs |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.222; verse 2 share [0.0, 0.333, 0.714] (5th, median, 95th) | rate 0.252; verse 2 share [0.0, 0.286, 0.6] (5th, median, 95th) | yes | no kept rate |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 11 (v110 89); frozen none | key-word deaths 2 (v110 42); frozen none | reading | no kept rate |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 21; widest drawn range 19 (row less two 19) | row 21; widest drawn range 19 (row less two 19) | yes | no kept rate |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.03, 0.057, 0.108] | q = 118, band 100-120: kept (0.04, 0.12, 0.27); song [0.068, 0.083, 0.101] | printed | no kept rate |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes | no kept rate |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 6.0%; content median -0.19, at kept 25th 21.0%, at kept median 1.2%; order median 1.37, at kept 25th 95.1%, at kept median 41.6%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | under floor 4.7%; content median 0.05, at kept 25th 19.8%, at kept median 0.2%; order median 1.38, at kept 25th 94.5%, at kept median 40.0%; measures outside the kept middle half 1 of 46; heaviest give-away ('outside_scale', -0.572) | reading | no kept rate |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | limits: a hard limit or three soft breaks (276/277, with 286's seven) 79/31 (spread 10.1, a difference); the judge's floor (254; 279) 49/41 (spread 9.3, no difference); design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A) 57/32 (spread 9.2, a difference); chorus opening another tune (227; 279) 29/29 (spread 7.5, no difference); key word on a chord tone (134; 279) 11/2 (spread 3.6, a difference); walk: no note 1/3 (spread 2.0, no difference) | limits: a hard limit or three soft breaks (276/277, with 286's seven) 79/31 (spread 10.1, a difference); the judge's floor (254; 279) 49/41 (spread 9.3, no difference); design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A) 57/32 (spread 9.2, a difference); chorus opening another tune (227; 279) 29/29 (spread 7.5, no difference); key word on a chord tone (134; 279) 11/2 (spread 3.6, a difference); walk: no note 1/3 (spread 2.0, no difference) | printed | no kept rate |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.0, 0.333, 0.714]; rate 0.222; copies given up 110 | verse 2 share [0.0, 0.286, 0.6]; rate 0.252; copies given up 124 | **no** | no kept rate |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 2.67 on the 30 agreed measures, both collections pooled; costliest [('unit4_to_unit2', 1.01), ('range', 0.42), ('unit3_returns', 0.3), ('gap_eighth', 0.2), ('past_fifth', 0.16), ('ascending', 0.14), ('pitch_sd', 0.13), ('last_note_tonic', 0.09)] | gap 3.16 on the 30 agreed measures, both collections pooled; costliest [('unit4_to_unit2', 1.06), ('unit3_returns', 0.35), ('range', 0.34), ('gap_eighth', 0.27), ('past_fifth', 0.25), ('pitch_sd', 0.2), ('peak_position', 0.17), ('on_fifth', 0.08)] | printed | no kept rate |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 5046: pushed 38%, in runs 26%; sixteenth gaps cost 0.04; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1249}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.0864}} | sixteenth onsets 6069: pushed 46%, in runs 16%; sixteenth gaps cost 0.07; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1136}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1074}} | reading (420) | no kept rate |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [3.375, 3.625, 3.875] (kept 3.6-4.1) | builds' notes a bar [3.375, 3.5, 3.75] (kept 3.6-4.1) | printed | no kept rate |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 5.0 at the median; cost 1.55; palette dropped for 677 lines; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.96}} | distinct lengths 5.0 at the median; cost 2.44; palette dropped for 712 lines; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 5.2497}} | reading (420) | 49% of 170 kept songs |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 2.3% (kept 7.1%); cost 1.15; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0227}} | outside the scale 2.2% (kept 7.1%); cost 0.96; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0217}} | reading (420) | 13% of 170 kept songs |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse 0.05, chorus 0.03; chord tones on long notes 69% | cost verse -0.0, chorus -0.01; chord tones on long notes 73% | printed apart (422: harmony, CoCoPops alone) | no kept rate |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': 0.53, 'distinct_pitches': 0.08, 'unit2_returns': 0.01, 'unit3_returns': 0.32, 'unit4_to_unit2': 0.69}; both collections {'on_offbeat_eighth': {'cocopops': 0.371, 'bimmuda': 0.411, 'builds': 0.4015}} | costs {'on_offbeat_eighth': -0.02, 'distinct_pitches': 0.05, 'unit2_returns': 0.02, 'unit3_returns': 0.35, 'unit4_to_unit2': 0.63}; both collections {'on_offbeat_eighth': {'cocopops': 0.371, 'bimmuda': 0.411, 'builds': 0.3686}} | reading (420) | no kept rate |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('unit4_to_unit2', 1.01)]; gap 2.67 | over half a point: [('unit4_to_unit2', 1.06)]; gap 3.16 | **no** | no kept rate |
| 348 | of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | pushed 38%, in runs 26%; sixteenth gaps cost 0.04; lines with no room (runs allowed) 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1249}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.0864}} | pushed 46%, in runs 16%; sixteenth gaps cost 0.07; lines with no room (runs allowed) 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1136}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1074}} | reading (420) | no kept rate |
| 349 | the outside-scale share within two points of the kept mean; cost under half a point | kept 7.1% (4.5% minor) | outside the scale 2.3% (kept 4.5%); cost 1.15; placed 4764, places wanting 51109; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0227}} | outside the scale 2.2% (kept 4.5%); cost 0.96; placed 4372, places wanting 50513; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0217}} | reading (420) | 13% of 170 kept songs |
| 350 | no unit return costs over half a point | kept unit 3 returns 31.5% | costs {'unit2_returns': 0.01, 'unit3_returns': 0.32, 'unit4_to_unit2': 0.69}; means {'unit2_returns': 0.158, 'unit3_returns': 0.079, 'unit4_to_unit2': 0.001} | costs {'unit2_returns': 0.02, 'unit3_returns': 0.35, 'unit4_to_unit2': 0.63}; means {'unit2_returns': 0.141, 'unit3_returns': 0.076, 'unit4_to_unit2': 0.001} | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 351 | verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median | kept 50% (25-70%) | bars left out 15789; lines given up 110 (2.8%); verse 2 share [0.0, 0.333, 0.714] | bars left out 15847; lines given up 124 (3.1%); verse 2 share [0.0, 0.286, 0.6] | **no** | no kept rate |
| 352 | the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats | a check; kept repeats' middle half printed | pick {'fp': '3f5704fc0291', 'judge': 3.02, 'rank_by_composite': 599, 'rank_by_judge': 7, 'repeats': [0.194, 0.708]}; composite first {'fp': '606af72aaaec', 'judge': -0.48, 'rank_by_composite': 1, 'rank_by_judge': 734, 'repeats': [0.29, 0.13]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | pick {'fp': '125edf2da033', 'judge': 1.78, 'rank_by_composite': 196, 'rank_by_judge': 91, 'repeats': [0.429, 0.375]}; composite first {'fp': '51866da24f66', 'judge': -0.41, 'rank_by_composite': 1, 'rank_by_judge': 819, 'repeats': [0.138, 0.276]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | amended by 362 | no kept rate |
| 353 | a minor song's degree measures read on its tonic with the natural minor scale | the rule's own statement (a check) | a minor song: the window measures on its tonic with the natural minor scale | a minor song: the window measures on its tonic with the natural minor scale | yes | no kept rate |
| 354 | each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point | the kept table (372) | 3.62 notes a bar, band ['3.5 to 4.5', '']: kept [0.067, 0.516, 0.204, 0.197], builds [0.091, 0.544, 0.183, 0.157]; eighth gaps cost 0.51; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.067), 'gap_eighth': (0.544, 0.516)} | 3.5 notes a bar, band ['3.5 to 4.5', '']: kept [0.062, 0.499, 0.209, 0.214], builds [0.091, 0.541, 0.189, 0.161]; eighth gaps cost 1.23; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.062), 'gap_eighth': (0.541, 0.499)} | yes | 1% of 170 kept songs |
| 355 | pushed within ten points of 54% and runs within ten of 31%; onsets on a sixteenth within two points of 9.4%; rhythm-placement deaths under 1 in 20 | kept 54% / 31%; 9.4% | pushed 38%, in runs 26%; on a sixteenth 8.6%; rhythm-placement deaths 0.0%; knobs run 1, on16 0.792; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1249}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.0864}} | pushed 46%, in runs 16%; on a sixteenth 10.7%; rhythm-placement deaths 0.0%; knobs run 1, on16 1.917; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1136}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1074}} | reading (420) | 6% of 170 kept songs |
| 356 | rhythm-band and memory breaks within two spreads of the version before v115; four distinct lengths at the median; song 43's survivors within two spreads of 811; the diagnostic runs printed | v112 (40, 42), v114 (43) | breaks (now, before, spread) {'rhythm band': (54, 0, 7.1), 'memory': (85, 0, 8.8)}; distinct lengths 5.0; survivors (773, None, None); rounds 6; 354 stopped: ["round 1: ['rhythm_bits'] outside the kept middle half (distinct lengths 5.0, rhythm bits 3.009); a reading (387): no knob stops"]; diagnostics {}; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.96}} | breaks (now, before, spread) {'rhythm band': (17, 0, 4.1), 'memory': (49, 0, 6.8)}; distinct lengths 5.0; survivors (860, None, None); rounds 5; 354 stopped: ["round 2: ['distinct_durations', 'rhythm_bits'] outside the kept middle half (distinct lengths 6.0, rhythm bits 3.06); a reading (387): no knob stops"]; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 5.2497}} | reading (420) | no kept rate |
| 357 | each gap share within five points of the kept table's, main and control; the rounds printed | the kept table (372) | builds [0.091, 0.544, 0.183, 0.157] against [0.067, 0.516, 0.204, 0.197]; rounds 6; knobs {'s16': 0.247, 'g8': 1.425, 'g4': 2.707, 'glong': 0.748}; stopped by 356; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.067), 'gap_eighth': (0.544, 0.516)} | builds [0.091, 0.541, 0.189, 0.161] against [0.062, 0.499, 0.209, 0.214]; rounds 5; knobs {'s16': 0.623, 'g8': 0.983, 'g4': 2.049, 'glong': 0.667}; stopped by 356; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.062), 'gap_eighth': (0.541, 0.499)} | yes | 1% of 170 kept songs |
| 358 | outside the scale within two points of 7.1% (4.5% minor); tritone-from-root breaks within two spreads of v115 | kept 7.1% (4.5% minor) | outside the scale 2.3% (kept 4.5%); passing notes 3995 of 4764 placed, places wanting 51109; tritone-from-root breaks (now, v115, spread) (0, 0, 0.0); both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0227}} | outside the scale 2.2% (kept 4.5%); passing notes 3634 of 4372 placed, places wanting 50513; tritone-from-root breaks (now, v115, spread) (0, 0, 0.0); both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0217}} | reading (420) | 13% of 170 kept songs |
| 359 | a minor song's readings and costs read against the 70 kept minor windows | kept minor means (369) | 70 minor windows; gap 7.45 (all 7.43); outside the scale {'builds': 0.023, 'minor_mean': 0.045, 'cost_minor': 0.53, 'cost_all': 1.15}; costliest [('distinct_durations', 1.93), ('notes_per_bar_sd', 1.55), ('unit4_to_unit2', 0.68), ('outside_scale', 0.53)] | 70 minor windows; gap 9.07 (all 8.78); outside the scale {'builds': 0.022, 'minor_mean': 0.045, 'cost_minor': 0.46, 'cost_all': 0.96}; costliest [('distinct_durations', 2.88), ('notes_per_bar_sd', 1.58), ('gap_eighth', 0.94), ('unit4_to_unit2', 0.62)] | printed | no kept rate |
| 360 | verse 2's share inside 25-70% at the median and within ten points of 50% in the main run; bars left out printed | kept 50% (25-70%) | verse 2 share [0.0, 0.333, 0.714]; bars fitted again and kept 826, not 15543; left out 15789 | verse 2 share [0.0, 0.286, 0.6]; bars fitted again and kept 861, not 15642; left out 15847 | **no** | no kept rate |
| 361 | unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate | kept 31.5%, 18.8% | means {'unit2_returns': 0.158, 'unit3_returns': 0.079, 'unit4_to_unit2': 0.001} (kept [0.172, 0.315, 0.188]); drawn {'361: unit 3 returns unit 1 (bar grid), drawn': 5000, '361: unit 4 returns unit 2 (bar grid), drawn': 5000, '361: unit 2 returns unit 1 (bar grid), drawn': 1213, '361: unit bars copied': 3467, '361: lines drawn on a returning unit': 9926, '361: unit return inside one line, not drawn': 501, '361: unit return given up for a line': 64} | means {'unit2_returns': 0.141, 'unit3_returns': 0.076, 'unit4_to_unit2': 0.001} (kept [0.172, 0.315, 0.188]); drawn {'361: unit 3 returns unit 1 (bar grid), drawn': 5000, '361: unit 4 returns unit 2 (bar grid), drawn': 5000, '361: unit 2 returns unit 1 (bar grid), drawn': 761, '361: unit bars copied': 2871, '361: lines drawn on a returning unit': 9629, '361: unit return inside one line, not drawn': 293, '361: unit return given up for a line': 73} | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 362 | the pick breaks no soft limit, or none qualified and the run says so; the number that qualified printed | a check | no soft break 553 of 773; pick 3f5704fc0291 (soft none, judge rank 7); judge's first ee6908aa3e7b | no soft break 661 of 860; pick 125edf2da033 (soft none, judge rank 91); judge's first 33653b3593e6 | yes | no kept rate |
| 363 | a design gate fails only when its rate is more than one spread under nine in ten | the paper's 317 with 337's spread | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.943} (spread {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.0073}) | {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.968} (spread {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.0056}) | yes | no kept rate |
| 365 | 249's gap knobs do not move; each gap share within five points of the kept table's for the section's notes a bar | the kept table (372) | 249's gap knobs {'V': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}, 'C': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}}; builds [0.091, 0.544, 0.183, 0.157] against [0.067, 0.516, 0.204, 0.197]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.067), 'gap_eighth': (0.544, 0.516)} | 249's gap knobs {'V': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}, 'C': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}}; builds [0.091, 0.541, 0.189, 0.161] against [0.062, 0.499, 0.209, 0.214]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.062), 'gap_eighth': (0.541, 0.499)} | yes | 1% of 170 kept songs |
| 366 | runs within ten points of 31% and pushes within ten of 54%, main and control; fallback lines printed | kept 31% / 54% | pushed 38%, in runs 26%; rate 1.0; lines may run 28947, may not 0, fallback 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1249}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.0864}} | pushed 46%, in runs 16%; rate 1.0; lines may run 28842, may not 0, fallback 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.1136}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1074}} | reading (420) | no kept rate |
| 367 | 356's band printed with its source | kept quartiles (a check) | band [1.934, 2.735] (the pooled kept table on 105 kept chart songs (373); the v88 table on 103: 2.20-2.94 (367)); stop ["round 1: ['rhythm_bits'] outside the kept middle half (distinct lengths 5.0, rhythm bits 3.009); a reading (387): no knob stops"] | band [1.934, 2.735] (the pooled kept table on 105 kept chart songs (373); the v88 table on 103: 2.20-2.94 (367)); stop ["round 2: ['distinct_durations', 'rhythm_bits'] outside the kept middle half (distinct lengths 6.0, rhythm bits 3.06); a reading (387): no knob stops"] | yes | no kept rate |
| 368 | song 43: memory breaks (373's limit) within two spreads of v114's read the same way, or the fix responsible named | v114, read with 373's limit |  |  | — | no kept rate |
| 369 | 364's figures for v115 reproduce 0.966, 0.954, 0.942 and 0.909 within 0.01; song 43's costs read against the 70 minor windows | Window 136 (sep_v118) |  |  | — | no kept rate |
| 370 | verse 2's share within ten points of 50% at the median in the main run | kept 50% | verse 2 share [0.0, 0.333, 0.714]; kept by variant {'370: kept by variant copy': 599, '370: kept by variant one added': 189, '370: kept by variant one dropped': 38}; fitted again kept 826, not 15543 | verse 2 share [0.0, 0.286, 0.6]; kept by variant {'370: kept by variant copy': 583, '370: kept by variant one added': 210, '370: kept by variant one dropped': 68}; fitted again kept 861, not 15642 | **no** | no kept rate |
| 371 | unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate | kept 31.5%, 18.8% | means {'unit2_returns': 0.158, 'unit3_returns': 0.079, 'unit4_to_unit2': 0.001} (kept [0.172, 0.315, 0.188]); rates {'unit2_returns': 0.2461, 'unit3_returns': 1.0, 'unit4_to_unit2': 1.0}; returns over pairs 0 | means {'unit2_returns': 0.141, 'unit3_returns': 0.076, 'unit4_to_unit2': 0.001} (kept [0.172, 0.315, 0.188]); rates {'unit2_returns': 0.1505, 'unit3_returns': 1.0, 'unit4_to_unit2': 1.0}; returns over pairs 0 | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 372 | with every gap knob starting at one, the four gap shares within five points of the kept table's; each knob's final value printed | the kept table | knobs {'s16': 0.2474, 'g8': 1.4251, 'g4': 2.7066, 'glong': 0.7478, 'run': 1.0, 'on16': 0.7924}; past a factor of two ['s16', 'g4']; builds [0.091, 0.544, 0.183, 0.157] against [0.067, 0.516, 0.204, 0.197]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.067), 'gap_eighth': (0.544, 0.516)} | knobs {'s16': 0.6233, 'g8': 0.9834, 'g4': 2.0491, 'glong': 0.6668, 'run': 1.0, 'on16': 1.9172}; past a factor of two ['g4']; builds [0.091, 0.541, 0.189, 0.161] against [0.062, 0.499, 0.209, 0.214]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.091, 0.062), 'gap_eighth': (0.541, 0.499)} | yes | 1% of 170 kept songs |
| 373 | each limit printed with its corpus; soft breaks of the rhythm band and of memory near one build in ten or fewer | kept chart songs | soft breaks: rhythm band 54, memory 85 of 999 complete | soft breaks: rhythm band 17, memory 49 of 997 complete | yes | no kept rate |
| 374 | the builds' separation beside 0.57 and 0.63 | the yardstick (sep_v118) |  |  | — | no kept rate |
| 375 | no sung note a semitone from a chord's raised tone on a beat or held a beat; 349's places wanting under a tenth of its target | the rule (a check) | a secondary dominant's raised third: 0 of 4128 notes a semitone from it; any chord tone outside the scale: 0 of 4128 (where {}); 349 placed 4764, wanting 51109 | a secondary dominant's raised third: 4 of 4089 notes a semitone from it; any chord tone outside the scale: 4 of 4089 (where {'inside': 4, 'line: exact': 4}); 349 placed 4372, wanting 50513 | **no** | no kept rate |
| 376 | a run in which a knob freezes completes and prints the round | a check | stop no knob froze | stop no knob froze | yes | no kept rate |
| 377 | song 45: the lift's failures under one complete build in twenty; drawn and pinned medians printed | the rule | no pinned notes in this song | no pinned notes in this song | n/a | no kept rate |
| 378 | the median share of the slot sung, by notes, inside the kept middle half; under one line in twenty under half its slot when its syllables in eighths would fill half | kept 43-75, 53-80, 66-88, 78-94%; 4.6% | median share {'6-8': 0.588, '9-12': 0.659, '13+': 0.704} (all 0.625, kept 0.71); under half of full lines 4.7% (kept 4.6%); drawn to a span 16923, given up 56 | median share {'6-8': 0.586, '9-12': 0.667, '13+': 0.667} (all 0.615, kept 0.71); under half of full lines 5.5% (kept 4.6%); drawn to a span 16890, given up 66 | **no** | no kept rate |
| 379 | no held sung note a semitone or minor ninth from a sustained accompaniment note | n/a here (song 45's build) | an arrangement rule: in song 45's build and its consistency checks (songs/p49); these runs build no arrangement | an arrangement rule: in song 45's build and its consistency checks (songs/p49); these runs build no arrangement | n/a | no kept rate |
| 380 | a chosen lift met in nine builds in ten (with its spread), with no more redraws than 311's endings take | the paper's 317 with 337's spread | lift [0.0, 2.0, 3.0]; design {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.943}; redraws design 0, ending 0 | lift [0.0, 1.0, 3.0]; design {"design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)": 0.968}; redraws design 0, ending 0 | n/a | no kept rate |
| 381 | no note outside the song's sung pitch classes (a chord's own tones aside) | the rule (a check) | notes outside the sung pitch classes 0; passing placed 3995 | notes outside the sung pitch classes 0; passing placed 3634 | yes | no kept rate |
| 382 | the seven limits printed with their corpus; builds lost to limits under one in five; surprisal and memory breaks beside a design | kept chart songs | lost to limits 7.9%; surprisal breaks 37, memory 85; beside the design gate | lost to limits 3.1%; surprisal breaks 37, memory 49; beside the design gate | yes | no kept rate |
| 383 | each hand-edited line before and after, with both scores | n/a (no hand edits) | no hand edits in these runs (song 45 as drawn) | no hand edits in these runs (song 45 as drawn) | n/a | no kept rate |
| 384 | generators patched by whole statements; each patched path run once before a run of record | a check (the smoke run) | every patch matched exactly once in each file (gen_v119.py); smoke paths no smoke run on file | every patch matched exactly once in each file (gen_v119.py); smoke paths no smoke run on file | reading | no kept rate |
| 385 | notes outside the scale within two points of 7.1% (4.5% minor) | kept 7.1% (4.5% minor) | outside the scale 2.3% (kept 4.5%); cost 1.15; placed 4764, wanting 51109; passing 3995 | outside the scale 2.2% (kept 4.5%); cost 0.96; placed 4372, wanting 50513; passing 3634 | reading (420) | 13% of 170 kept songs |
| 386 | no sung note on a beat or a beat long a semitone from a chord's own outside tone, in drawn, returning or copied lines | the rule (a check) | clashes 0 of 4128 notes read; moved {"386: notes moved off a semitone from a chord's outside tone": 1008, '386: moved in a rhythm line': 478, '386: moved in a both line': 204, '386: moved in a exact line': 210, '386: moved in a pitch line': 79, '386: moved in a fresh line': 37} | clashes 4 of 4089 notes read; moved {"386: notes moved off a semitone from a chord's outside tone": 1017, '386: moved in a both line': 206, '386: moved in a rhythm line': 578, '386: moved in a exact line': 171, '386: moved in a pitch line': 44, '386: moved in a fresh line': 18} | yes | no kept rate |
| 387 | 356's stop a reading: it moves and freezes no knob | a check | stop ["round 1: ['rhythm_bits'] outside the kept middle half (distinct lengths 5.0, rhythm bits 3.009); a reading (387): no knob stops"]; knobs {'s16': 0.247, 'g8': 1.425, 'g4': 2.707, 'glong': 0.748} | stop ["round 2: ['distinct_durations', 'rhythm_bits'] outside the kept middle half (distinct lengths 6.0, rhythm bits 3.06); a reading (387): no knob stops"]; knobs {'s16': 0.623, 'g8': 0.983, 'g4': 2.049, 'glong': 0.667} | yes | no kept rate |
| 388 | the two side runs made and read; nothing changed | printed (step 2) | the two side runs on song 40 (step 2): see the report | the two side runs on song 40 (step 2): see the report | printed | no kept rate |
| 389 | runs within ten points of the band's kept share; deaths for want of a rhythm within two spreads of v116's (song 45: none) | the kept table's bands; v116 | bands {'3.5 to 4.5': {'onsets': 3014, 'in_runs': 0.273, 'kept': 0.291, 'rate': 1.0}, 'under 3.5': {'onsets': 22955, 'in_runs': 0.233, 'kept': 0.271, 'rate': 1.0}}; rhythm deaths 0 (before None, v116 None); join deaths 0; fallbacks {} | bands {'3.5 to 4.5': {'onsets': 3641, 'in_runs': 0.151, 'kept': 0.291, 'rate': 1.0}, 'under 3.5': {'onsets': 24877, 'in_runs': 0.156, 'kept': 0.271, 'rate': 1.0}}; rhythm deaths 0 (before None, v116 None); join deaths 0; fallbacks {} | **no** | no kept rate |
| 390 | unit returns within ten points of the kept rates on the units free to draw; the free share printed | kept 17.2%, 31.5%, 18.8% | free units {'unit2_returns': {'free_mean': 0.158, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.079, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.001, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; rates {'unit2_returns': 0.2461, 'unit3_returns': 1.0, 'unit4_to_unit2': 1.0}; plan none | free units {'unit2_returns': {'free_mean': 0.141, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.076, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.001, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; rates {'unit2_returns': 0.1505, 'unit3_returns': 1.0, 'unit4_to_unit2': 1.0}; plan none | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 391 | 378 read on drawn lines: the median share by notes inside the kept middle half; spans given up under one in twenty | kept 43-75, 53-80, 66-88, 78-94% | drawn lines 16983: median share {'6-8': 0.581, '9-12': 0.674, '13+': 0.717}; under half of full 2.3%; widened 1757; given up 56 of 16979 (0.3%) | drawn lines 16949: median share {'6-8': 0.583, '9-12': 0.68}; under half of full 2.8%; widened 1827; given up 66 of 16956 (0.4%) | **no** | no kept rate |
| 392 | song 45: the lift's failures under one complete build in twenty, read on drawn notes | the rule | no pinned notes in this song | no pinned notes in this song | n/a | no kept rate |
| 393 | verse 2's share on the lines of verse 1's syllable count within ten points of 50% (main run); the rest printed | kept 50% | equal lines [0, 1, 2]: share [0.0, 0.333, 0.714]; the rest [0.0, 0.333, 0.667]; all lines [0.1, 0.333, 0.625] | equal lines [0, 1, 2]: share [0.0, 0.286, 0.6]; the rest [0.0, 0.333, 0.667]; all lines [0.111, 0.3, 0.571] | yes | no kept rate |
| 394 | song 43's memory breaks within two spreads of v114's; the others printed | v114, read with 373's limit | memory breaks 85 (before None, v114 None); {'394: passing note withdrawn (an occurrence could not take it)': 906, '394: passing note placed in every occurrence': 1651, '394: occurrences given the passing note': 217} | memory breaks 49 (before None, v114 None); {'394: passing note placed in every occurrence': 1410, '394: occurrences given the passing note': 136, '394: passing note withdrawn (an occurrence could not take it)': 896} | reading | no kept rate |
| 395 | 311 and 324 read in the section's own key where the record lifts it | the rule (a check) | lifted none; Outro on the tonic 100.0%; tonic endings 1998 | lifted none; Outro on the tonic 100.0%; tonic endings 1994 | n/a (no lift) | no kept rate |
| 396 | separability by family printed beside Window 139 | Table DY (sep_v119) | separability by family: sep_v119.py, across the five songs | separability by family: sep_v119.py, across the five songs | below | no kept rate |
| 398 | chord tones 54-76% at the median, on a beat 56-80%; non-chord notes resolved by step within ten points of 50% | kept 64%, 67%, 72%; 50% | chord tones 63.6%, on a beat 72.2%, on a downbeat 0.8; resolved by step 50.6%; knobs {'ct398': 2.0744, 'ctb398': 1.4539, 'ctd398': 1.0, 'res398': 3.3969, 'turn400': 0.5} | chord tones 66.7%, on a beat 73.3%, on a downbeat 0.8; resolved by step 50.6%; knobs {'ct398': 1.7443, 'ctb398': 1.0853, 'ctd398': 1.0, 'res398': 1.9558, 'turn400': 0.7688} | printed apart (422: harmony, CoCoPops alone) | 46% of 170 kept songs |
| 399 | a sung note on the downbeat of Verse 1's and Chorus 1's first bar in 59-79% of builds, unless a design places the entry | kept 69% | withdrawn by v120 (421); printed: {'Verse 1': 0.286, 'Chorus 1': 0.394} beside both collections (first onset: CoCoPops 0.37 beats, BiMMuDa 1.36) | withdrawn by v120 (421); printed: {'Verse 1': 0.287, 'Chorus 1': 0.395} beside both collections (first onset: CoCoPops 0.37 beats, BiMMuDa 1.36) | withdrawn (421) | no kept rate |
| 400 | turns per move within 0.04 of 0.58 at the mean, verse and chorus | kept 0.58 | verse 0.595, chorus 0.615 (kept 0.584); knob 0.5 | verse 0.59, chorus 0.6 (kept 0.584); knob 0.7688 | yes | 30% of 170 kept songs |
| 401 | four distinct note lengths in the judge's window at the median | kept 4 | withdrawn by v120 (421); 343 a reading: distinct lengths 5.0 at the median (CoCoPops 4.0, BiMMuDa 4.7) | withdrawn by v120 (421); 343 a reading: distinct lengths 5.0 at the median (CoCoPops 4.0, BiMMuDa 4.7) | withdrawn (421) | 49% of 170 kept songs |
| 424 | leaps of a fourth or fifth, the window's last note on the tonic and empty bars each between the two collections' means or within a fifth of a sd of the nearer; outside the scale printed (420) | CoCoPops and BiMMuDa 1958-1991 | aims {'fourth_fifth': {'builds': 0.0883, 'cocopops': 0.08, 'bimmuda': 0.087, 'fifth_sd': 0.0156, 'held': True, 'agreed': True}, 'last_note_tonic': {'builds': 0.1947, 'cocopops': 0.277, 'bimmuda': 0.329, 'fifth_sd': 0.0945, 'held': True, 'agreed': True}, 'empty_bars': {'builds': 0.5105, 'cocopops': 0.468, 'bimmuda': 0.506, 'fifth_sd': 0.152, 'held': True, 'agreed': False, 'note': 'printed (428)'}, 'outside_scale': {'builds': 0.0227, 'cocopops': 0.071, 'bimmuda': 0.038, 'fifth_sd': 0.0254, 'held': True, 'agreed': False}}; knobs {'ff424': 0.1861, 'lt424': 10.0, 'eb424': 0.25}; {} | aims {'fourth_fifth': {'builds': 0.0818, 'cocopops': 0.08, 'bimmuda': 0.087, 'fifth_sd': 0.0156, 'held': True, 'agreed': True}, 'last_note_tonic': {'builds': 0.2091, 'cocopops': 0.277, 'bimmuda': 0.329, 'fifth_sd': 0.0945, 'held': True, 'agreed': True}, 'empty_bars': {'builds': 0.51, 'cocopops': 0.468, 'bimmuda': 0.506, 'fifth_sd': 0.152, 'held': True, 'agreed': False, 'note': 'printed (428)'}, 'outside_scale': {'builds': 0.0217, 'cocopops': 0.071, 'bimmuda': 0.038, 'fifth_sd': 0.0254, 'held': True, 'agreed': False}}; knobs {'ff424': 0.169, 'lt424': 9.3744, 'eb424': 0.25}; {} | yes | 28% of 170 kept songs |
| 459 | verse 2 read on bars whose syllable counts differ by one or less: half its bars or more read, the median share within ten points of 50% (main run) | kept 50% | share [0.143, 0.429, 0.8]; bars read [0.375, 0.7, 1.0]; builds with no such bar 0; rate 0.22222222222222232 | share [0.167, 0.429, 0.75]; bars read [0.4, 0.667, 1.0]; builds with no such bar 0; rate 0.25238095238095243 | yes | no kept rate |
| 465 | a drawn line's last onset in the bar the kept share for its notes draws; class given up and span given up each under one line in twenty | kept shares by notes (zeneng_v128_kept_lines.json) | drawn 16986, held 15229, given up 1757, no class 0, landing fixed 0, entry given up 2034; spans given up 56 of 16979; widest class gap 0.245; 6 to 8: [0.071, 0.778, 0.147, 0.005] (kept [0.263, 0.61, 0.111, 0.017]), 4+ beats 0.772 (kept 0.483); 9 to 12: [0.081, 0.578, 0.34, 0.001] (kept [0.326, 0.541, 0.127, 0.006]), 4+ beats 0.814 (kept 0.364); 13 and over: [0.092, 0.789, 0.119, 0.0] (kept [0.385, 0.554, 0.053, 0.008]), 4+ beats 0.844 (kept 0.295) | drawn 16961, held 15134, given up 1827, no class 0, landing fixed 0, entry given up 2047; spans given up 66 of 16956; widest class gap 0.242; 6 to 8: [0.074, 0.76, 0.16, 0.006] (kept [0.263, 0.61, 0.111, 0.017]), 4+ beats 0.802 (kept 0.483); 9 to 12: [0.084, 0.561, 0.354, 0.001] (kept [0.326, 0.541, 0.127, 0.006]), 4+ beats 0.854 (kept 0.364) | **no** | no kept rate |
| 458 | the span's bounds from kept lines' notes a second; drawn lines' median rate inside the kept 25th-75th by notes (bands of 200 lines or more) | kept 2.2-3.8 notes a second | 6 to 8: [2.421, 2.861, 3.312] (kept [2.358, 3.04, 3.835], 7539 lines); 9 to 12: [2.212, 2.484, 2.95] (kept [2.525, 3.091, 3.572], 5515 lines); 13 and over: [2.691, 2.898, 3.059] (kept [2.675, 3.164, 3.82], 109 lines); tempo 118 | 6 to 8: [2.421, 2.898, 3.312] (kept [2.358, 3.04, 3.835], 8411 lines); 9 to 12: [2.145, 2.36, 2.622] (kept [2.525, 3.091, 3.572], 4749 lines); tempo 118 | **no** | no kept rate |
| 478 | verse 2's repeats and steps within five points of verse 1's (first eight bars, build by build) | the first verse's own rates | repeats verse 1 / verse 2 (0.281, 0.29), steps (0.448, 0.42); knobs (0.8179, 1.3776) | repeats verse 1 / verse 2 (0.27, 0.262), steps (0.41, 0.389); knobs (0.9346, 1.5241) | yes | no kept rate |
| 484 | the pitch verse 2 keeps of verse 1 (Window 142's pair) inside 72-79% | kept 72-79% | pitch kept 0.762; rate 0.6051 | pitch kept 0.778; rate 0.6618 | yes | no kept rate |
| 476 | the content judge of record is zeneng_v128_judge.json; builds under its kept 25th percentile printed | kept mean 1.53, sd 2.0, 25th 0.23 | content mean -0.37; under the kept 25th 0.725; under 1.53 - 1.645 sd 0.104 | content mean -0.466; under the kept 25th 0.743; under 1.53 - 1.645 sd 0.11 | printed | no kept rate |
| 477 | the pick's score the mean of content and order, window by window | the rule (a check) | pick 3f5704fc0291, score 2.583; check True | pick 125edf2da033, score 3.079; check True | printed | no kept rate |
| 486 | 389's run rates read on Verse 1 and Chorus 1 for their bands | printed | judged bands ['3.5 to 4.5', 'under 3.5']; last round {'under 3.5': (0.271, 0.176, 1.0), '3.5 to 4.5': (0.291, 0.265, 1.0)} | judged bands ['3.5 to 4.5', 'under 3.5']; last round {'under 3.5': (0.271, 0.215, 1.0), '3.5 to 4.5': (0.291, 0.274, 1.0)} | printed | no kept rate |
| 489 | 452's knobs by band of density | read in the reread by density band | knobs {'under 3.5': {'gs': 0.3993, 'er': 0.5022, 'zz': 0.2101}, '3.5 to 4.5': {'gs': 0.3289, 'er': 0.1787, 'zz': 0.4676}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}} | knobs {'under 3.5': {'gs': 1.1184, 'er': 0.8784, 'zz': 1.0116}, '3.5 to 4.5': {'gs': 0.444, 'er': 0.2429, 'zz': 0.6626}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}} | read in the reread, by density band | no kept rate |
| 490 | a weight on an onset in a run, by band; drawable runs within ten points on bands of 200 onsets or more | kept by band (389) | run weights {'under 3.5': 1.6113, '3.5 to 4.5': 0.9008, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (2801, 0.283)), 'under 3.5': (0.271, (15402, 0.239))} | run weights {'under 3.5': 4.392, '3.5 to 4.5': 0.9247, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (3430, 0.159)), 'under 3.5': (0.271, (16270, 0.163))} | **no** | no kept rate |
| 491 | 467's and 408's knobs withdrawn; song 45's chorus floor no lower than its lift allows: design deaths under one in twenty | the design (a check) | 467's and 408's knobs withdrawn (all songs); the floor is song 45's | 467's and 408's knobs withdrawn (all songs); the floor is song 45's | n/a | no kept rate |
| 494 | 457 falls back at once when no entry and landing fit the strict copy | printed | at once 6957, at half 1686; rhythm deaths 0; joins {} | at once 6827, at half 1726; rhythm deaths 0; joins {} | printed | no kept rate |
| 500 | 465's class drawn by the slot's length and the notes: classes within ten points of the kept for each notes band and slot (200 lines or more); given up under one line in twenty | kept shares by notes and by slot, combined | drawn 16986, given up 1757; out of reach 6493; widest gap 0.242; 6 to 8 notes, 2-bar slot: [0.072, 0.842, 0.079, 0.008] (kept [0.209, 0.712, 0.079, 0.0]); 6 to 8 notes, 3-bar slot: [0.067, 0.439, 0.485, 0.01] (kept [0.129, 0.522, 0.282, 0.066]); 9 to 12 notes, 2-bar slot: [0.081, 0.886, 0.031, 0.001] (kept [0.265, 0.644, 0.092, 0.0]); 9 to 12 notes, 3-bar slot: [0.081, 0.517, 0.399, 0.003] (kept [0.165, 0.478, 0.333, 0.024]); 13 and over notes, 3-bar slot: [0.092, 0.789, 0.119, 0.0] (kept [0.228, 0.572, 0.162, 0.038]) | drawn 16961, given up 1827; out of reach 6487; widest gap 0.249; 6 to 8 notes, 2-bar slot: [0.078, 0.828, 0.087, 0.007] (kept [0.209, 0.712, 0.079, 0.0]); 6 to 8 notes, 3-bar slot: [0.055, 0.453, 0.471, 0.021] (kept [0.129, 0.522, 0.282, 0.066]); 9 to 12 notes, 2-bar slot: [0.09, 0.893, 0.017, 0.0] (kept [0.265, 0.644, 0.092, 0.0]); 9 to 12 notes, 3-bar slot: [0.084, 0.534, 0.38, 0.003] (kept [0.165, 0.478, 0.333, 0.024]) | **no** | no kept rate |
| 501 | 458 read in onsets a beat: drawn lines' median inside the kept 25th-75th by notes (200 lines or more) | kept 1.1-2.0 onsets a beat | 6 to 8: [1.273, 1.556, 2.0] (kept [1.25, 1.636, 2.0], 7565 lines); 9 to 12: [1.2, 1.375, 1.6] (kept [1.286, 1.571, 1.882], 5526 lines); 13 and over: [1.412, 1.529, 1.655] (kept [1.333, 1.586, 2.0], 109 lines); inside 15229, redrawn 1357, given up 1757 | 6 to 8: [1.333, 1.647, 2.0] (kept [1.25, 1.636, 2.0], 8441 lines); 9 to 12: [1.143, 1.286, 1.455] (kept [1.286, 1.571, 1.882], 4759 lines); inside 15134, redrawn 1664, given up 1827 | yes | no kept rate |
| 502 | song 45: the floor at the verse's median and three; design deaths under one in twenty | the design (a check) | song 45 only | song 45 only | n/a | no kept rate |
| 503 | verse 2's chord tones on the beat within five points of verse 1's (the engine's windows) | the first verse's own rate | verse 1 / verse 2 0.701 / 0.694; knob 0.96 | verse 1 / verse 2 0.699 / 0.733; knob 1.6 | yes | no kept rate |
| 504 | 452's band knobs keyed by the line's own notes a bar | read in the reread by density band | notes to syllables 1.0396; knobs {'under 3.5': {'gs': 0.3993, 'er': 0.5022, 'zz': 0.2101}, '3.5 to 4.5': {'gs': 0.3289, 'er': 0.1787, 'zz': 0.4676}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}} | notes to syllables 1.0185; knobs {'under 3.5': {'gs': 1.1184, 'er': 0.8784, 'zz': 1.0116}, '3.5 to 4.5': {'gs': 0.444, 'er': 0.2429, 'zz': 0.6626}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}} | read in the reread, by density band | no kept rate |
| 505 | the run weight aimed alone (389's rate at one): drawable runs within ten points on bands of 200 onsets or more | kept by band (389) | 389's rates {'under 3.5': 1.0, '3.5 to 4.5': 1.0, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; run weights {'under 3.5': 1.6113, '3.5 to 4.5': 0.9008, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (2801, 0.283)), 'under 3.5': (0.271, (15402, 0.239))} | 389's rates {'under 3.5': 1.0, '3.5 to 4.5': 1.0, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; run weights {'under 3.5': 4.392, '3.5 to 4.5': 0.9247, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (3430, 0.159)), 'under 3.5': (0.271, (16270, 0.163))} | **no** | no kept rate |
| 508 | a return after a designed line fitted to its breath: joins before a copy printed | printed | joins before a copy 0, before a line 0; fitted 0; align 0 | joins before a copy 0, before a line 0; fitted 0; align 0 | printed | no kept rate |
| 513 | 440's step tested on the finished chart; an inversion that has lost it taken back | the rule (a check) | inversions []; taken back [] | inversions []; taken back [] | yes | no kept rate |
| 519 | the content judge of record is zeneng_v129_judge.json; complete builds under the kept songs' 5th percentile (-0.72) printed; the floor stays on v108 | kept songs: 5th -0.72, median 1.42 | content mean -0.37; under the kept songs' 5th 38%; stays on the v108 judge (under -0.72 on every song is not under a third) | content mean -0.466; under the kept songs' 5th 39%; stays on the v108 judge (under -0.72 on every song is not under a third) | printed | no kept rate |
| 520 | no knob named for 408 or 455 in the run; the window's range printed beside the song's design (not aimed) | the rule (a check); kept range 10.9 | 408 knob in the run False; 455 knob in the run False; range verse 10.4, chorus 9.38 (kept 10.9):  | 408 knob in the run False; 455 knob in the run False; range verse 10.64, chorus 9.31 (kept 10.9):  | yes | no kept rate |
| 438 | the chart's share of bars with two or more changes inside the kept middle half (or none, drawn at the kept rate), and of bars holding the last bar's chord inside its middle half | kept 0-0.33; 0.08-0.44; none in 25% and 37% of songs | two or more 0.0 -> 0.192 (target 0.182), held bars 0.117 -> 0.1 (target 0.101); edits 18 | two or more 0.0 -> 0.192 (target 0.182), held bars 0.117 -> 0.1 (target 0.101); edits 18 | yes | no kept rate |
| 440 | the bass on the root at nine changes in ten or more; a third or fifth with a step on one side; at most one chord in twelve | the rule (a check) | root at 100.0% of 131 changes; inversions [] (a step beside each: []) | root at 100.0% of 131 changes; inversions [] (a step beside each: []) | yes | no kept rate |
| 464 | song 45: deaths at 267 at or under v118's (267 reads the bridge G before its raise) | v118 (songs/p50) | song 45 only | song 45 only | n/a | no kept rate |
| 470 | the content judge of record is the refit: its mean on complete builds, beside the v108 content | kept median 1.97 | refit content: complete builds -0.37, survivors -0.37 (v108 content -0.047; rank correlation 0.359) | refit content: complete builds -0.466, survivors -0.466 (v108 content 0.023; rank correlation 0.429) | printed | no kept rate |
| 471 | the floor on the v108 judge; the share of complete builds under the refit's kept 5th percentile (-0.51) printed | under a third on every song moves it | under the refit's kept 5th percentile 45% of complete builds; floor deaths (v108) 49; floor stays on the v108 judge | under the refit's kept 5th percentile 48% of complete builds; floor deaths (v108) 41; floor stays on the v108 judge | floor stays on the v108 judge | no kept rate |
| 472 | the pick: the refit's first among survivors with no soft break; each pick's rank under the other judge | printed | pick 3f5704fc0291; v108's pick ee6908aa3e7b (rank under the refit 3); the refit's pick's rank under v108 4; clean 553 | pick 125edf2da033; v108's pick e0e296157792 (rank under the refit 196); the refit's pick's rank under v108 68; clean 661 | printed | no kept rate |
| 473 | the judge does not read a second verse | the rule | the judge reads the first eight bars of Verse 1 and Chorus 1 only; verse 2 answers to 434's test | the judge reads the first eight bars of Verse 1 and Chorus 1 only; verse 2 answers to 434's test | n/a | no kept rate |
| 456 | the last-note test read on windows whose last note the walk chose (100 or more): between the collections' means or within a fifth of a sd of the nearer | CoCoPops and BiMMuDa 1958-1991 | walked windows 1697, on the tonic 17.8% (collections (0.277, 0.329)) | walked windows 1670, on the tonic 20.1% (collections (0.277, 0.329)) | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 405 | 389 read on drawable lines: runs within ten points of the band's kept share where 200 onsets or more; song 45's rhythm deaths within two spreads of v116's (none) | the kept table's bands; v116 | bands (kept, rate, drawable n/runs, no room or fell back, not drawn) {'3.5 to 4.5': {'kept': 0.291, 'rate': 1.0, 'drawable': (2801, 0.283), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (213, 0.136)}, 'under 3.5': {'kept': 0.271, 'rate': 1.0, 'drawable': (15402, 0.239), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (7553, 0.221)}}; lines {'405: line drawable without runs': 28947}; rhythm deaths 0 (before None) | bands (kept, rate, drawable n/runs, no room or fell back, not drawn) {'3.5 to 4.5': {'kept': 0.291, 'rate': 1.0, 'drawable': (3430, 0.159), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (211, 0.014)}, 'under 3.5': {'kept': 0.271, 'rate': 1.0, 'drawable': (16270, 0.163), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (8607, 0.142)}}; lines {'405: line drawable without runs': 28842}; rhythm deaths 0 (before None) | **no** | no kept rate |
| 409 | the window's last note on the tonic between the collections' means (27.7%, 32.9%) or within a fifth of a sd of the nearer, where the endings are not designed; its sources printed | CoCoPops and BiMMuDa 1958-1991 | on the tonic 19.5% (collections (0.277, 0.329)); walked 85%; by source (n, tonic) {'Chorus 1: the walk': (999, 0.238), 'Verse 1: a carried extreme (329)': (13, 0.0), 'Verse 1: a copy or return': (288, 0.302), 'Verse 1: the walk': (698, 0.092)}; knob 10.0 | on the tonic 20.9% (collections (0.277, 0.329)); walked 84%; by source (n, tonic) {'Chorus 1: the walk': (997, 0.276), 'Verse 1: a carried extreme (329)': (5, 0.0), 'Verse 1: a copy or return': (319, 0.254), 'Verse 1: the walk': (673, 0.091)}; knob 9.3744 | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 412 | song 45: deaths at 267 within two spreads of v118's, the lift's failures under one in twenty | v118 (songs/p50) | deaths at 267 0 (v119 None, v118 None); with 267 read before the raise (450): None; lift failures None | deaths at 267 0 (v119 None, v118 None); with 267 read before the raise (450): None; lift failures None | reading (song 45's test) | no kept rate |
| 413 | unit returns within ten points of the pooled kept rates on the free units; losses counted | pooled kept | free units {'unit2_returns': {'free_mean': 0.158, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.079, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.001, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; losses {'361: unit bars copied': 3467, '413: unit-return bars left out (more than one onset off)': 14714, '413: unit-return pitch not kept (range, slur or chord), a try': 1717, '361: unit return given up for a line': 64} | free units {'unit2_returns': {'free_mean': 0.141, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.076, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.001, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; losses {'361: unit bars copied': 2871, '413: unit-return bars left out (more than one onset off)': 14663, '413: unit-return pitch not kept (range, slur or chord), a try': 1193, '361: unit return given up for a line': 73} | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 414 | spans given up under one line in twenty | the rule | given up 56 of 16979 (0.3%); median share {'6-8': 0.581, '9-12': 0.674, '13+': 0.717}; {} | given up 66 of 16956 (0.4%); median share {'6-8': 0.583, '9-12': 0.68}; {} | yes | no kept rate |
| 415 | verse 2 read on bars of equal syllables: half its bars or more read, the median share within ten points of 50% (main run) | kept 50% | share [0.143, 0.429, 0.8]; bars read [0.375, 0.7, 1.0]; builds with no such bar 0; rate 0.22222222222222232 | share [0.167, 0.429, 0.75]; bars read [0.4, 0.667, 1.0]; builds with no such bar 0; rate 0.25238095238095243 | yes | no kept rate |
| 417 | 311 reads the last chorus; a designed tag printed apart | the rule (a check) | Outro on the tonic 100.0%; tag no tag | Outro on the tonic 100.0%; tag no tag | yes | no kept rate |
| 419 | no clash read on the chord at the note | the rule (a check) | clashes 0 of 4128 (bar chord: 0); by kind {}; [] | clashes 0 of 4087 (bar chord: 4); by kind {}; [] | yes | no kept rate |
| 428 | empty bars printed, not aimed, beside 378's slot share | printed | empty bars 0.511 (CoCoPops 0.468, BiMMuDa 0.506); 378's slot share {'6-8': 0.581, '9-12': 0.674, '13+': 0.717}; knob 0.25 | empty bars 0.51 (CoCoPops 0.468, BiMMuDa 0.506); 378's slot share {'6-8': 0.583, '9-12': 0.68}; knob 0.25 | printed | no kept rate |

## The kept pass rates (496, 512)

v128 Run 3 (496): each test's kept pass rate, printed beside it. A kept song (CoCoPops, 314 windows of 170 songs, zeneng_v105_kept_windows.json
with zeneng_v117_kept_songs_and_modes.json's song ids) is read the way the test reads a song: the mean of its own windows (its verse and its
chorus), against the test's band. A test whose band is the engine's own rule, a count of deaths, or a reading has no kept rate and says so.

| Test | Kept pass rate | How it is read |
|---|---|---|
| 310 | 56% of 170 kept songs | likeness of bar rhythms inside 0.04-0.23 (song mean of parallel) |
| 311 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 312 | 62% of 170 kept songs | past_fifth at or under 3.6% in both windows |
| 313 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 314 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 315 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 316 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 317 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 318 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 319 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 320 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 321 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 322 | 56% of 170 kept songs | likeness of bar rhythms inside 0.04-0.23 (song mean of parallel) |
| 323 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 324 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 325 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 326 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 327 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 328 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 329 | 65% of 170 kept songs | range inside the kept middle half, 8-13 (song mean) |
| 330 | 56% of 170 kept songs | likeness of bar rhythms inside 0.04-0.23 (song mean of parallel) |
| 331 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 332 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 333 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 334 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 335 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 336 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 337 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 338 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 340 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 341 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 342 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 343 | 49% of 170 kept songs | four distinct note lengths (song median) |
| 344 | 13% of 170 kept songs | outside_scale within two points of 7.1% (song mean) |
| 345 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 346 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 347 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 348 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 349 | 13% of 170 kept songs | outside_scale within two points of 7.1% (song mean) |
| 350 | 0% of 170 kept songs | unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1) |
| 351 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 352 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 353 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 354 | 1% of 170 kept songs | each of the four gap shares within five points of the kept mean (song mean) |
| 355 | 6% of 170 kept songs | on_sixteenth within two points of 9.4% (song mean; runs and pushes are not in the kept windows) |
| 356 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 357 | 1% of 170 kept songs | each of the four gap shares within five points of the kept mean (song mean) |
| 358 | 13% of 170 kept songs | outside_scale within two points of 7.1% (song mean) |
| 359 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 360 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 361 | 0% of 170 kept songs | unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1) |
| 362 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 363 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 365 | 1% of 170 kept songs | each of the four gap shares within five points of the kept mean (song mean) |
| 366 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 367 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 368 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 369 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 370 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 371 | 0% of 170 kept songs | unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1) |
| 372 | 1% of 170 kept songs | each of the four gap shares within five points of the kept mean (song mean) |
| 373 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 374 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 375 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 376 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 377 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 378 | no kept rate | a line's median share of its slot inside the kept middle half by notes: half of kept lines by definition (Window 138's lines are not on this machine) |
| 379 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 380 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 381 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 382 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 383 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 384 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 385 | 13% of 170 kept songs | outside_scale within two points of 7.1% (song mean) |
| 386 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 387 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 388 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 389 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 390 | 0% of 170 kept songs | unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1) |
| 391 | no kept rate | a line's median share of its slot inside the kept middle half by notes: half of kept lines by definition (Window 138's lines are not on this machine) |
| 392 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 393 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 394 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 395 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 396 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 398 | 46% of 170 kept songs | chord tones 54-76% and on a beat 56-80% (song mean) |
| 399 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 400 | 30% of 170 kept songs | turns per move within 0.04 of 0.584 (song mean) |
| 401 | 49% of 170 kept songs | four distinct note lengths (song median) |
| 405 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 408 | 30% of 170 kept songs | turns per move within 0.04 of 0.584 (song mean) |
| 409 | 0% of 170 kept songs | the window's last note on the tonic 27.7-32.9% or within 0.09 (a song's two windows read 0, 0.5 or 1) |
| 412 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 413 | 0% of 170 kept songs | unit returns within ten points of the kept rate (a song's windows read 0, 0.5 or 1) |
| 414 | no kept rate | a line's median share of its slot inside the kept middle half by notes: half of kept lines by definition (Window 138's lines are not on this machine) |
| 415 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 417 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 419 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 424 | 28% of 170 kept songs | fourths and fifths between the collections' means or within a fifth of a sd (song mean) |
| 428 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 438 | no kept rate | both shares inside their kept middle halves: half of kept songs on each by definition; the joint share is not in the table (no song rows) |
| 440 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 441 | no kept rate | first-beat root within six points of 24%, third within six of 26% (no song-level kept table here) |
| 453 | 65% of 170 kept songs | range inside the kept middle half, 8-13 (song mean) |
| 456 | 0% of 170 kept songs | the window's last note on the tonic 27.7-32.9% or within 0.09 (a song's two windows read 0, 0.5 or 1) |
| 458 | no kept rate | drawn lines' median rate inside the kept 25th-75th: half of kept lines by definition |
| 459 | no kept rate | verse 2's share within ten points of 50%: Billboard's median song passes, Rolling Stone's (0.375) does not; not computable song by song here (Window 142) |
| 464 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 465 | no kept rate | a drawn line's class: the kept shares are the kept lines' own (a reading of the share, not a song test) |
| 470 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 471 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 472 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 473 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 476 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 477 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 478 | no kept rate | verse 2's repeats and steps within five points of verse 1's: not computable song by song (no paired kept verses here) |
| 484 | no kept rate | pitch kept 72-79%: the kept collections' figure (no song-by-song figure here) |
| 486 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 489 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 490 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 491 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 494 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 500 | no kept rate | the class shares are the kept lines' own (a reading of shares, not a song test) |
| 501 | no kept rate | drawn lines' median rate inside the kept 25th-75th: half of kept lines by definition |
| 502 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 503 | no kept rate | verse 2's chord tones on the beat within five points of verse 1's: not computable song by song (no paired kept verses here) |
| 504 | no kept rate | a reading, a cost, or a share read on builds (no song-level kept test) |
| 505 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 508 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 513 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 519 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |
| 520 | no kept rate | a check of the engine's own rule, a count of deaths or breaks, or a design: no kept rate |

## Findings (540–)

### 540. 524 gives the long lines their room; a three-bar slot still cannot reach class 3, and short lines in it overshoot class 2.

**Problem:** With every line of nine syllables or more in a slot of three bars (Q11 A), the 9–12-note lines in three-bar slots come within ten points of the kept classes. Two things are still out of line. Class 3 cannot be reached in any three-bar slot: its last onset would have to fall before the slot's first bar. Short lines that share a three-bar slot with a long partner (the pre-chorus's lines 3 and 4) draw class 2 far over the kept share.

**Evidence** (classes 0 / 1 / 2 / 3, main; kept for the notes and slot):

| Notes, slot | Lines | Drawn | Kept |
|---|---|---|---|
| 9–12, three bars | 4,628 | 0.081 / 0.517 / 0.399 / 0.003 | 0.165 / 0.478 / 0.333 / 0.024 |
| 6–8, three bars | 1,263 | 0.067 / 0.439 / 0.485 / 0.010 | 0.129 / 0.522 / 0.282 / 0.066 |
| 6–8, two bars | 6,302 | 0.072 / 0.842 / 0.079 / 0.008 | 0.209 / 0.712 / 0.079 / 0.000 |

- Out of reach (main): class 3 in a three-bar slot of 9 syllables, 3,997; of 10 syllables, 1,998; class 0 of 10 syllables, 390. Control the same within ten.
- By slot, every build: Verse 1 line 3, Chorus line 3, Bridge lines 1–3 and the Outro's first line each lose class 3 in every build.
- 500's kept shares by slot lump every slot over ten beats together (SL465's last band), so a three-bar slot is given four-bar shares.

**Fix:** Split 500's last band into three-bar and four-bar slots (kept shares for each), and draw the class only among those the slot can reach.

**Check:** On the next song, each class within ten points of the kept share for its notes and slot, three-bar slots included.

### 541. 530 meets its figure on the main draw and misses it on the control; the full step swings.

**Problem:** Taking the full step every round until verse 2 is within two points makes 503's knob swing on the few unaimed builds a calibration round reads. The knob ends where its last round left it, and the two draws end on opposite sides.

**Evidence:**

| Draw | Verse 1 / verse 2, chord tones on the beat | Knob | Paired test, song 46 (of 27) |
|---|---|---|---|
| Main | 0.701 / 0.694 | 0.96 | 19 |
| Control | 0.699 / 0.733 | 1.60 | 17 |

- The knob after each round (main): 1.0, 1.0, 1.0, 0.6, 0.96, 0.96; the gap between the verses moved between 0.2 and 4.6 points from round to round.
- Songs 40, 42 and 43 (v129, the same reading): verse 2 over verse 1 by 0.8 to 3.7 points.

**Fix:** Take the full step only while the gap keeps its sign two rounds running; otherwise half. Read the knob on all the round's unaimed builds pooled with the round before.

**Check:** Verse 2 within two points of verse 1 on both draws, and the paired test at 20 of 27 or more on both.

### 542. 531 cuts 501's redraws to a few percent; lines given up stay at one in ten, counted with 465's.

**Problem:** On the kept 5th–95th, 501 redraws few lines, and the joins hold. But a line is given up at half its tries 1,757 times (main), one line in ten against the check's one in twenty. The count is the same as 465's "class given up" because both are released on the same try, so the report cannot tell which bound failed.

**Evidence:**

- 501, main / control: inside 15,229 / 15,134; redrawn 1,357 / 1,664; given up 1,757 / 1,827 (10.3% / 10.8%). v129: song 40 redrew 22,488, song 45 49,166.
- Joins before a line: 0 / 0 with 501; 2 / 1 with 501 off (side runs). Joins before a copy: 0 / 0 against 3 / 2. Within two spreads.
- With 501 off, 465 gives up more lines: 2,820 / 2,807 against 1,757 / 1,827.

**Fix:** Count 501's give-ups apart from 465's, and print which bound the line was missing at half its tries.

**Check:** 501 alone given up under one line in twenty on the next song.

### 543. 534 cannot be read on song 46: it has no dense windows.

**Problem:** None; a reading. The long slots keep song 46 at 3.5–4.5 notes a bar in every first verse and chorus: 796 windows in that band, 4 at 4.5–5.5, none denser. The stream in dense lines (504, 505) is not exercised.

**Evidence** (song 46, its own density, 3.5–4.5 notes a bar; kept, main, control):

| Measure | Kept | Main | Control |
|---|---|---|---|
| equal_gap_run_max | 4.582 | 4.982 | 4.662 |
| gap_same_as_before | 0.389 | 0.406 | 0.384 |
| zigzag_of_three | 0.315 | 0.316 | 0.327 |

- 505's drawable runs at 3.5–4.5: 0.283 / 0.159 against the kept 0.291.

**Fix:** None. 534 stays open for a song with dense lines.

**Check:** Printed.

### 544. 538 varies the bass by articulation where the four kicks fix the rhythm.

**Problem:** None; a reading. On song 46 the v129 routine already gave each bar its own pitch figure (6–8 of 8 bars). 538 adds articulation to the cells, so bars that share an onset rhythm now differ in length and accent.

**Evidence** (eight-bar windows with four kicks a bar; v129's routine on the same record → v130's):

- Onset rhythms a window: 2–3 → 2–3 (the check, two or more, holds on every window).
- Onsets and lengths a window: 2–3 → 3–5 (the intro 7 → 7; the second pre-chorus 2 → 2).
- Windows passing every test of 445–448: 13 → 14 of 15. The root at every change: 100%.

**Fix:** None.

**Check:** Printed.

### 545. Song 46 is the hardest of the four to tell from the kept songs.

**Problem:** None; a reading.

**Evidence** (the agreed 30, both collections pooled, the first 400 complete builds; main / control):

| Song | Within the song | Across, the song's pairs |
|---|---|---|
| 46 | 0.824 / 0.847 | 0.689 / 0.670 |
| 40 | 0.870 / 0.867 | — |
| 42 | 0.886 / 0.884 | — |
| 43 | 0.845 / 0.862 | — |
| 40, 42, 43 among themselves | — | 0.756 / 0.722 |

- Most of the difference is rhythm: within song 46 the rhythm family separates at 0.560 / 0.594, against 0.703–0.732 on songs 40, 42 and 43; pitch 0.759 / 0.770 against 0.783–0.828.
- With song 46, the across mean of all four is 0.723 / 0.696; whether that is a real change is not read (song 46 has no run before it).
- Window 147, first verse and chorus (main): song 46's empty bars 0.518 (Billboard 0.515, Rolling Stone 0.736; songs 40, 42, 43: 0.150–0.318); gap entropy 1.803 (kept 1.836–1.900; others 1.553–1.748); equal-gap runs 4.99 (kept 4.38–4.87; others 5.18–6.18). Its notes a bar, 3.63, is the lowest of the four.
- The judge (519): content mean −0.37 / −0.47; under −0.72, 38% / 39% (songs 40, 42, 43: 57%, 60%, 43% in v129).

**Fix:** None. The three-bar slots, not an aim, move the rests and the rhythm's spread toward the kept songs.

**Check:** Printed.

### 546. The default path picked a chorus at the verse's height; the design carries the lift.

**Problem:** None; a reading. The pick (3f5704fc0291, the refit judge's first with no soft break, rank 7 by the judge) has its chorus median, top and lowest note equal to the verse's (0, 0, 0). Each is inside the kept middle half (0 to 3, −1 to 3, 0 to 4). The chorus's top, E4 on "water," is the verse's top. The only height is the designed falsetto B4.

**Evidence:**

- The builds' lift (main): median 0 / 2 / 3 (5th, median, 95th).
- The design gate: 94.3% / 96.8% of complete builds pass (317's nine in ten held). 57 / 32 design deaths.
- The last "flood" leaps a minor tenth (G♯3 to B4), outside 312's reading, which takes the first verse and chorus.

**Fix:** None.

**Check:** Printed.

## For the song after this one

- What song 46 leaves open: 500's last band for three-bar slots (540), 503's knob on both draws (541), 501's give-ups counted apart (542), and the stream in dense lines (534, unread here: 543).

## Regression line

Songs 40–45 are closed (523). Their orders of record at v129 (ZE_PART=1), main / control, each reproduced by the rerun in this session (above):

| Song | Main / control |
|---|---|
| 40 | d508b254a8f4 / 04342d35cd1d |
| 42 | 9fd23492dad3 / 529bf7a1c186 |
| 43 | af58ce3be702 / a095303f51b7 |
| 44 | 2f43a0bc93d6 / 7d4dd7b83e26 |
| 45 | 6dc6710923f0 / 9a1c46f67b24 |
| 46 (new) | 120253ea25cb / 635084318e00 |

- Song 46's runs were each made twice and reproduce.

## Blind-pick tally

The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40, 41, 43, 44, 45 and 46 have not yet been offered. Song 46's three slots: Remembered, "Now I'm living on dry ground"; middle (top quartile under both), "The sprinkler hangs a rainbow on the lawn"; Annotated, "The windows running thick with breath".
