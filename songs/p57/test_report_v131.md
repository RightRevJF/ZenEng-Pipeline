# ZenEng v131: song 47, The Singer Doesn't Stop — test report

*Words and music: Jason Bryant. The spec is ZenEng v131 (Module 27.75). 540, 541 and 542 were ported as proposed. 525 reads the kept endings by the slot's bars from zeneng_v131_kept_slots.json. 527 set each line's slot at intake against the kept slots for its syllables. 526 reads the new song first by a judge that has not seen it. At the other AI's suggestion, song 47 has dense, wordy verse lines: the case 534 still needed. Songs 40–46 were rerun only as a regression. The paper was not edited. New findings are numbered from 550.*

## What was run

- **The song:** song 47, *The Singer Doesn't Stop*, on the default path, written from the writer's intake and his locked lyric. The source was his paper "Analytic Continuation Through Death"; the genre, at his wish, contemporary Christian. It is built with dense, wordy verse lines, as the other AI suggested, the case 534 still needed.
  - **The engine:** v129's code of record for song 43 with the song's frame, form, lyric and designs written in by gen_v131.py. It carries v130's 531 and 524 (the per-slot count) and v131's 525 and 540 (classes from zeneng_v131_kept_slots.json, by the slot's bars and the line's notes), 541 and 542.
  - **Drawn on a 438 chart:** 440's step tested on the finished chart (513).
  - **The runs:** 1,000 builds main and control, each made twice at PYTHONHASHSEED 0 (seed 20261560).
  - **The pick of record:** the engine's default (362, with 472), taken as drawn with no hand edits.
- **527 at intake:** each line's slot was set against the kept slots for its syllable count (the file's table by syllables) and shown to the writer. No line was flagged: no slot was one that under a tenth of kept lines of that count take.
- **The record:** built from both the chart and the pick (build_p57.py). The second bridge's first fourteen bars are lifted a whole step in the record (the design). The bass is by the routine (bass_v131.py: v130's routine with the scale read by the bar).
- **Readings,** each on main and control:
  - every test (readings_v131.py);
  - 526, the judge that has not seen the song (judge526.py, as the other AI specified): the 37 measures, C = 0.3, both kept collections split by piece in eight splits, fitted on songs 40–46 and tested on 47, and each of 40–46 held out in turn;
  - the standing judge's scores (519);
  - separation on the agreed 30 within the song, beside songs 40, 42 and 43;
  - Window 147's measures (reread_v131.py), the five songs 40, 42, 43, 46 and 47 together and song 47 alone; empty bars and the stream beside the kept figures (527).
- **Regression (523):** songs 40–45 (v129) and 46 (v130), main and control, rerun once and compared with their orders of record.

## Survivors and orders

| Run | Survivors | Order | Made twice, the same |
|---|---|---|---|
| Song 47, main | 711 | f363d4e78346 | yes |
| Song 47, control | 760 | 7fba0ac398c0 | yes |

Deaths, main: join: no held end and breath before the line (212) 113; design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held 84; limits: a hard limit or three soft breaks (276/277, with 286's seven) 50; rhythm: no placement 23; align: the words do not fit the returning tune 16; bridge opening unrelated (208; 279) 2; walk: no note 1.

**Regression (523).** Each closed song rerun once from its file of record, against its order of record:

| Song | Run | Order of record | Rerun | Reproduced |
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
| 46 | main | 120253ea25cb (773) | 120253ea25cb (773) | yes |
| 46 | ctl | 635084318e00 (860) | 635084318e00 (860) | yes |

Every closed song reproduces its order of record, main and control.

## 527 at intake: each line's slot beside the kept slots for its syllables

Every line has a two-bar slot (the writer's choice A). The share is that of kept lines with the same syllable count that take a two-bar slot (the file's table by syllables). A line is flagged only under a tenth.

| Line | Syllables | Slot | Kept share of that slot | Flagged |
|---|---|---|---|---|
| Verse 1, line 1 | 14 | 2 bars | 37% | no |
| Verse 1, line 2 | 18 | 2 bars | 10% | no |
| Verse 1, line 3 | 14 | 2 bars | 37% | no |
| Verse 1, line 4 | 15 | 2 bars | 27% | no |
| Chorus 1, line 1 | 4 | 2 bars | 54% | no |
| Chorus 1, line 2 | 7 | 2 bars | 53% | no |
| Chorus 1, line 3 | 11 | 2 bars | 53% | no |
| Chorus 1, line 4 | 7 | 2 bars | 53% | no |
| Chorus 1, line 5 | 6 | 2 bars | 58% | no |
| Chorus 1, line 6 | 7 | 2 bars | 53% | no |
| Verse 2, line 1 | 16 | 2 bars | 10% | no |
| Verse 2, line 2 | 15 | 2 bars | 27% | no |
| Verse 2, line 3 | 16 | 2 bars | 10% | no |
| Verse 2, line 4 | 15 | 2 bars | 27% | no |
| Chorus 2, line 1 | 4 | 2 bars | 54% | no |
| Chorus 2, line 2 | 7 | 2 bars | 53% | no |
| Chorus 2, line 3 | 11 | 2 bars | 53% | no |
| Chorus 2, line 4 | 7 | 2 bars | 53% | no |
| Chorus 2, line 5 | 6 | 2 bars | 58% | no |
| Chorus 2, line 6 | 7 | 2 bars | 53% | no |
| Bridge, line 1 | 8 | 2 bars | 56% | no |
| Bridge, line 2 | 7 | 2 bars | 53% | no |
| Bridge, line 3 | 8 | 2 bars | 56% | no |
| Bridge, line 4 | 7 | 2 bars | 53% | no |
| Bridge, line 5 | 10 | 2 bars | 32% | no |
| Bridge, line 6 | 6 | 2 bars | 58% | no |
| Bridge 2, line 1 | 8 | 2 bars | 56% | no |
| Bridge 2, line 2 | 7 | 2 bars | 53% | no |
| Bridge 2, line 3 | 8 | 2 bars | 56% | no |
| Bridge 2, line 4 | 7 | 2 bars | 53% | no |
| Bridge 2, line 5 | 10 | 2 bars | 32% | no |
| Bridge 2, line 6 | 3 | 2 bars | 36% | no |
| Bridge 2, line 7 | 3 | 2 bars | 36% | no |
| Bridge 2, line 8 | 7 | 2 bars | 53% | no |
| Last Chorus, line 1 | 4 | 2 bars | 54% | no |
| Last Chorus, line 2 | 7 | 2 bars | 53% | no |
| Last Chorus, line 3 | 11 | 2 bars | 53% | no |
| Last Chorus, line 4 | 8 | 2 bars | 56% | no |
| Last Chorus, line 5 | 6 | 2 bars | 58% | no |
| Last Chorus, line 6 | 6 | 2 bars | 58% | no |
| Tag, line 1 | 4 | 2 bars | 54% | no |
| Tag, line 2 | 7 | 2 bars | 53% | no |

## 526: the song read first by a judge that has not seen it

The judge of record's 37 measures; median fill (the fitting set's), z-scored, L2 logistic with C = 0.3, the kept and build sides weighted alike. Windows: the first verse's and first chorus's first eight bars, the engine's own reading. Kept side: CoCoPops and BiMMuDa 1958–1991 (zeneng_v131_kept_windows.json, 545 windows of 285 pieces), split in half by piece, fitted on one half and tested on the other, eight splits. Song 47 is scored by a judge fitted on songs 40–46; each earlier song by a judge refitted on the other five. AUC (0.5 is none), mean ± spread, main / control.

| Song | Separation by a judge that has not seen it | The standing judge: content mean | Under −0.72 |
|---|---|---|---|
| 47 (fitted on 40–46) | 0.729 ± 0.027 / 0.709 ± 0.04 | -0.391 / -0.522 | 36% / 42% |
| 40 (fitted on the other five) | 0.785 ± 0.021 / 0.797 ± 0.02 | -0.834 / -0.855 | 57% / 56% |
| 42 (fitted on the other five) | 0.787 ± 0.017 / 0.825 ± 0.02 | -0.965 / -0.936 | 60% / 60% |
| 43 (fitted on the other five) | 0.719 ± 0.017 / 0.77 ± 0.012 | -0.537 / -0.639 | 43% / 47% |
| 44 (fitted on the other five) | 0.868 ± 0.021 / 0.925 ± 0.01 | -1.528 / -1.669 | 86% / 90% |
| 45 (fitted on the other five) | 0.867 ± 0.02 / 0.91 ± 0.021 | -1.793 / -2.097 | 88% / 96% |
| 46 (fitted on the other five) | 0.739 ± 0.01 / 0.79 ± 0.01 | -0.37 / -0.466 | 38% / 39% |

No refit was made before these were printed. Beside them, separation within the song on the agreed 30 (a judge fitted on the song's own builds), song 47 beside 40, 42 and 43, main / control:

| Family | Within: 47 | Within: 40 / 42 / 43 | Across, 47's pairs | Across, 40/42/43 among themselves |
|---|---|---|---|---|
| agreed 30 | 0.942 / 0.948 | 0.87 / 0.886 / 0.845; 0.867 / 0.884 / 0.862 | 0.741 / 0.742 | 0.756 / 0.722 |
| pitch (agreed) | 0.853 / 0.856 | 0.817 / 0.791 / 0.793; 0.828 / 0.783 / 0.813 | 0.68 / 0.677 | 0.707 / 0.682 |
| rhythm (agreed) | 0.836 / 0.842 | 0.732 / 0.706 / 0.713; 0.721 / 0.732 / 0.703 | 0.69 / 0.709 | 0.677 / 0.638 |
| form | 0.513 / 0.507 | 0.605 / 0.734 / 0.55; 0.551 / 0.716 / 0.549 | 0.504 / 0.457 | 0.497 / 0.483 |
| harmony (CoCoPops alone, apart) | 0.742 / 0.732 | 0.541 / 0.531 / 0.626; 0.529 / 0.536 / 0.585 | 0.537 / 0.512 | 0.541 / 0.537 |

## Empty bars and the stream beside the kept figures (527)

Window 147's measures on song 47's first verse and chorus (the engine's window), main / control, beside the kept songs and song 46.

| Measure | Billboard | Rolling Stone | Song 47 | Song 46 (main) |
|---|---|---|---|---|
| empty_bars | 0.515 | 0.736 | 0.0325 / 0.03 | 0.5175 |
| gap_same_as_before | 0.387 | 0.364 | 0.4664 / 0.4596 | 0.4061 |
| equal_gap_run_max | 4.867 | 4.378 | 7.0575 / 6.8087 | 4.985 |
| gap_entropy | 1.836 | 1.9 | 1.7044 / 1.7381 | 1.8033 |
| gap_eighth | 0.465 | 0.449 | 0.4805 / 0.5096 | 0.5318 |
| notes_per_bar | 3.937 | 4.143 | 5.6481 / 5.6181 | 3.6323 |
| most_onsets_in_a_beat | 2.634 | 2.801 | 3.3838 / 3.4575 | 2.695 |
| range | 10.67 | 10.587 | 10.4 / 10.2812 | 9.8737 |
| turns_per_move | 0.584 | 0.594 | 0.561 / 0.5642 | 0.5981 |
| last_note_tonic | 0.282 | 0.328 | 0.0338 / 0.05 | 0.1837 |
| zigzag_of_three | 0.315 | 0.333 | 0.288 / 0.2967 | 0.3163 |

At the windows' own density (song 47 alone; kept, main, control):

| Band | Measure | Kept | Main | Control | Windows |
|---|---|---|---|---|---|
| 3.5 to 4.5 notes a bar | equal_gap_run_max | 4.582 | 5.635 | 5.418 | 400 / 400 |
| 3.5 to 4.5 notes a bar | gap_same_as_before | 0.389 | 0.415 | 0.412 | 400 / 400 |
| 3.5 to 4.5 notes a bar | zigzag_of_three | 0.315 | 0.215 | 0.213 | 400 / 400 |
| 3.5 to 4.5 notes a bar | gap_eighth | 0.489 | 0.526 | 0.538 | 400 / 400 |
| 3.5 to 4.5 notes a bar | turns_per_move | 0.579 | 0.481 | 0.474 | 400 / 400 |
| 3.5 to 4.5 notes a bar | range | 11.146 | 10.405 | 10.123 | 400 / 400 |
| 5.5 to 9 notes a bar | equal_gap_run_max | 6.172 | 8.48 | 8.2 | 400 / 400 |
| 5.5 to 9 notes a bar | gap_same_as_before | 0.435 | 0.518 | 0.507 | 400 / 400 |
| 5.5 to 9 notes a bar | zigzag_of_three | 0.328 | 0.361 | 0.38 | 400 / 400 |
| 5.5 to 9 notes a bar | gap_eighth | 0.463 | 0.435 | 0.481 | 400 / 400 |
| 5.5 to 9 notes a bar | turns_per_move | 0.591 | 0.641 | 0.654 | 400 / 400 |
| 5.5 to 9 notes a bar | range | 12.234 | 10.395 | 10.44 | 400 / 400 |

505's drawable runs (kept, (onsets, share)): main {'3.5 to 4.5': [0.291, [4456, 0.362]], '5.5 and over': [0.361, [8243, 0.508]], 'under 3.5': [0.271, [656, 0.293]]}; control {'3.5 to 4.5': [0.291, [2942, 0.369]], '5.5 and over': [0.361, [7864, 0.471]], 'under 3.5': [0.271, [355, 0.451]]}. Run weights by band: main {'under 3.5': 0.3407, '3.5 to 4.5': 0.1395, '4.5 to 5.5': 1.0, '5.5 and over': 0.0566}.

## 525 and 540: the ending classes by the slot's bars and the line's notes

Drawn against zeneng_v131_kept_slots.json (by notes, two-bar slots). The readings table's own 'kept' column still shows v129's combined shares; the file's shares are the ones of record here.

| Notes, slot | Lines, main / control | Classes 0 / 1 / 2 / 3+, main | Control | Kept (525) |
|---|---|---|---|---|
| 3 to 5 notes, 2-bar slot | 2400 / 2400 | [0.0, 0.694, 0.306, 0.0] | [0.0, 0.69, 0.31, 0.0] | [0.11, 0.7, 0.189, 0.0] |
| 6 to 8 notes, 2-bar slot | 6348 / 6629 | [0.055, 0.886, 0.059, 0.0] | [0.048, 0.899, 0.054, 0.0] | [0.17, 0.766, 0.064, 0.0] |
| 9 to 12 notes, 2-bar slot | 2446 / 2171 | [0.056, 0.941, 0.002, 0.0] | [0.057, 0.943, 0.0, 0.0] | [0.419, 0.571, 0.01, 0.0] |
| 13 and over notes, 2-bar slot | 2406 / 2400 | [0.31, 0.69, 0.0, 0.0] | [0.328, 0.672, 0.0, 0.0] | [0.517, 0.483, 0.0, 0.0] |

The kept endings each slot could not reach, counted over the builds (main / control):

| Slot | Main | Control |
|---|---|---|
| Bridge:2 (2 bars, 8 syllables) class 0 out of reach | 446 | 431 |
| Bridge:3 (2 bars, 7 syllables) class 0 out of reach | 89 | 102 |
| Bridge:3 (2 bars, 7 syllables) class 2 out of reach | 36 | 37 |
| Bridge:4 (2 bars, 10 syllables) class 2 out of reach | 516 | 524 |
| Chorus 1:2 (2 bars, 11 syllables) class 2 out of reach | 863 | 881 |
| Verse 1:0 (2 bars, 14 syllables) class 1 out of reach | 282 | 311 |
| Verse 1:1 (2 bars, 18 syllables) class 0 out of reach | 282 | 311 |
| Verse 1:1 (2 bars, 18 syllables) class 1 out of reach | 282 | 311 |
| Verse 1:2 (2 bars, 14 syllables) class 0 out of reach | 282 | 311 |
| Verse 1:2 (2 bars, 14 syllables) class 1 out of reach | 282 | 311 |

## 541: the second verse, main / control

| Draw | Verse 1 / verse 2, chord tones on the beat (engine's window) | 503's knob | Paired test, song 47 (of 27) |
|---|---|---|---|
| Main | 0.683 / 0.71 | 0.2789 | 17 |
| Control | 0.76 / 0.754 | 0.2789 | 19 |

The calibration's rounds (main): round 1 (0.481, 0.492, 1.0); round 2 (0.575, 0.58, 1.0); round 3 (0.686, 0.705, 1.0); round 4 (0.722, 0.772, 0.775); round 5 (0.719, 0.771, 0.465); round 6 (0.733, 0.765, 0.279).

## 542: 501's give-ups counted apart from 465's

| Count | Main | Control |
|---|---|---|
| 465: class given up for a line | 795 | 748 |
| 501: line inside the kept onsets a beat | 7442 | 7553 |
| 501: onsets a beat given up for a line | 795 | 749 |
| 501: outside the kept onsets a beat, redrawn | 21668 | 20684 |
| 542: given up at half the tries: 465's class missed (501 not) | 75 | 59 |
| 542: given up at half the tries: 501's bound and 465's class both missed | 1 | 0 |
| 542: given up at half the tries: 501's bound missed (465 not) | 719 | 689 |
| 542: given up at half the tries: neither (another bound) | 0 | 1 |

| Notes | Lines, main | Onsets a beat (25, 50, 75), main / control | Kept |
|---|---|---|---|
| 3 to 5 | 2400 | [0.857, 0.857, 1.0] / [0.857, 0.857, 1.0] | [1.143, 1.6, 2.0] |
| 6 to 8 | 6348 | [1.333, 1.714, 2.0] / [1.333, 1.714, 1.75] | [1.25, 1.636, 2.0] |
| 9 to 12 | 2446 | [1.8, 1.905, 2.0] / [1.818, 1.905, 2.0] | [1.286, 1.571, 1.882] |
| 13 and over | 2406 | [2.364, 2.545, 2.727] / [2.364, 2.545, 2.727] | [1.333, 1.586, 2.0] |

## The designs and the pick

- **The pick of record:** ff83ac7a0247, the refit judge's first among the survivors with no soft break (362/472); judge 3.15, rank 204 of 711 by the composite. No hand edits. Lift: {'median': -0.5, 'top': 2, 'lowest': 5, 'bridge': -1.0}.
- **The design gates (317):** the hook, 100.0% / 100.0%; the bridge's build, 90.1% / 88.9% (main / control).
- **The chart (438):** two or more 0.0 -> 0.0 (target 0.0), held bars 0.08 -> 0.102 (target 0.093); edits 1. 440: root at 100.0% of 79 changes; inversions [] (a step beside each: []).
- **The lift:** bars 57–70 a whole step up in the record (voice and chords). The engine drew them in G under its search row's top, G4, so the held 'do' sounds A4.

## The range (520: not aimed)

Verse window 10.36 / 10.33; chorus window 10.38 / 10.04 (kept 10.9).

## The table of tests: Song 47, The Singer Doesn't Stop

Held in both the main run and the control: 39 of 63 with a test that a kept song can pass. Not held: 311, 317, 326, 338, 347, 351, 354, 357, 360, 363, 365, 370, 372, 389, 400, 424, 465, 458, 490, 500, 501, 505, 405, 417. Many tests name songs 40–46 in their wording; they are read here on song 47's runs. 311 reads the last chorus's last line (a return, 90.7% / 96.4% on the tonic); the song's last line, the tag's, is on the tonic in every complete build. 500's 'kept' column is v129's; 525's file is above.

| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |
|---|---|---|---|---|---|---|
| 310 | likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336) | kept 0.04-0.23 | under floor 0.0%; parallel 0.194 (kept 0.14); paired lines 5500, partner given up 0 | under floor 0.0%; parallel 0.182 (kept 0.14); paired lines 5619, partner given up 0 | yes | 56% of 170 kept songs |
| 311 | the last chorus on the tonic in every build; misses none | the rule's own statement (a check) | tonic 90.7%; registers redrawn 0; misses 0 | tonic 96.4%; registers redrawn 0; misses 0 | **no** | no kept rate |
| 312 | leaps past a fifth at or under the kept 75th at the median, verse and chorus | kept 75th 3.6% | verse 1.7%, chorus 0.0%; leap knob 1.0 | verse 1.7%, chorus 0.0%; leap knob 1.0 | yes | 62% of 170 kept songs |
| 313 | verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335) | kept 25-70% (median 50%) | share [0.0, 0.333, 1.0]; in range 62%; given up 41 (1.0%); left out 578 | share [0.0, 0.5, 1.0]; in range 61%; given up 47 (1.2%); left out 486 | yes | no kept rate |
| 314 | unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324) | kept verse share 40-57%; the rule (a check) | range [10.0, 15.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.353, 0.5, 0.647]; tonic nearest the sung median 0.98, the drawn centre 1.0; top fifth 100%; floor 4% | range [9.0, 14.0, 17.0, 17.0, 17.0] (kept [10, 14.5, 17, 22, 28]); unused split max 1; verse share [0.353, 0.5, 0.625]; tonic nearest the sung median 0.985, the drawn centre 1.0; top fifth 100%; floor 5% | yes | no kept rate |
| 315 | amplitude at or under 7; arch over the span inside the kept middle half at the median | kept 0.00-0.55; the cap (a check) | amplitude 5.0; arch [0.131, 0.201, 0.443]; stop none | amplitude 5.0; arch [0.131, 0.241, 0.464]; stop none | yes | no kept rate |
| 316 | redraws per long line and entry shares | a reading (335: tries and redraws) | redraws 7240/8974 = 0.807; entries {'starts_on_downbeat': 0.228, 'starts_after_downbeat': 0.586, 'starts_as_pickup': 0.185} | redraws 8275/9091 = 0.91; entries {'starts_on_downbeat': 0.219, 'starts_after_downbeat': 0.597, 'starts_as_pickup': 0.184} | reading | no kept rate |
| 317 | each design gate's pass rate | the paper's 317: nine in ten | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.901} (spread {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 0.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.0103}) | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.889} (spread {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 0.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.0106}) | **no** | no kept rate |
| 318 | the feel named; sixteenths printed | a reading | acoustic-driven modern CCM, q = 84, sixteenth-note strum (Q4 B, Q6 A); sixteenth onsets [0.097, 0.121, 0.158] | acoustic-driven modern CCM, q = 84, sixteenth-note strum (Q4 B, Q6 A); sixteenth onsets [0.104, 0.116, 0.13] | printed | no kept rate |
| 319 | no instrumental note outside its instrument | n/a here | read on the arrangement; these runs make no instrumental lines | read on the arrangement; these runs make no instrumental lines | n/a | no kept rate |
| 320 | rescorings stated as bounds | a check | the report states no predicted counts from rescoring; figures here are from runs | the report states no predicted counts from rescoring; figures here are from runs | yes | no kept rate |
| 321 | this table | a check | this table, on this song's own runs | this table, on this song's own runs | yes | no kept rate |
| 322 | as 310 (335) | kept 0.04-0.23 | paired 5500 (1091 of another length); given up 0 (0.0%); parallel 0.194; under floor 0.0% | paired 5619 (1423 of another length); given up 0 (0.0%); parallel 0.182; under floor 0.0% | yes | 56% of 170 kept songs |
| 323 | as 313 (335) | kept 25-70% | one-over bars copied without the weakest onset 2126; left out 578; verse 2 in range 62% | one-over bars copied without the weakest onset 1932; left out 486; verse 2 in range 61% | yes | no kept rate |
| 324 | every tonic ending on the tonic nearest the centre of its section's drawn register | the rule's own statement (a check) | 847 tonic endings, on the nearest to the centre 1.0 | 872 tonic endings, on the nearest to the centre 1.0 | yes | no kept rate |
| 325 | no design death for want of a note the registers hold; the last chorus on the tonic in every complete build | the rule's own statement (a check) | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | design failures for the registers 0; last chorus on the tonic 100.0%; redrawn 0 | yes | no kept rate |
| 326 | nine builds in ten pass each design gate | the paper's 317 | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.901} | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.889} | **no** | no kept rate |
| 327 | deaths at the breath before a copy | a reading (335: a count kept songs do not have) | join deaths 0 (v109 92); refits {} | join deaths 0 (v109 92); refits {} | reading | no kept rate |
| 328 | the sixteenth share beside its band | a reading | q = 84, band 80-100: kept (0.11, 0.21, 0.36); song [0.097, 0.121, 0.158] | q = 84, band 80-100: kept (0.11, 0.21, 0.36); song [0.104, 0.116, 0.13] | printed | no kept rate |
| 329 | sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways | kept 8-13; the rule (a check) | sung [17.0, 17.0, 17.0] vs drawn [15.0, 17.0, 17.0] (gap [-2.0, 0.0, 0.0]); chorus window [9.0, 10.0, 12.0]; heaviest give-aways ['on_sixteenth', 'outside_scale', 'pushed', 'empty_bars', 'first_onset']; extremes sung low 99%, high 99% | sung [17.0, 17.0, 17.0] vs drawn [14.0, 17.0, 17.0] (gap [-3.0, -1.0, 0.0]); chorus window [9.0, 10.0, 11.0]; heaviest give-aways ['on_sixteenth', 'outside_scale', 'pushed', 'empty_bars', 'chord_tones_on_long_notes']; extremes sung low 99%, high 99% | yes | 65% of 170 kept songs |
| 330 | likeness inside the kept middle half at the median; partners given up printed | kept 0.04-0.23 | likeness 0.194; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | likeness 0.182; copies failed and the stresses kept 0; given up after the stresses 0; partners given up 0 (0.0%) | yes | 56% of 170 kept songs |
| 331 | verse 2's share inside 25-70% at the median, main and control | kept 25-70% (median 50%) | rate 0.417; verse 2 share [0.0, 0.333, 1.0] (5th, median, 95th) | rate 0.65; verse 2 share [0.0, 0.5, 1.0] (5th, median, 95th) | yes | no kept rate |
| 332 | song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held | v110's counts (the paper's test) | key-word deaths 0 (v110 89); frozen none | key-word deaths 0 (v110 42); frozen none | reading | no kept rate |
| 333 | 329's tests held; no drawn range wider than the row less two | the rule's own statement (a check) | row 19; widest drawn range 17 (row less two 17) | row 19; widest drawn range 17 (row less two 17) | yes | no kept rate |
| 334 | the sixteenth share beside its band's three quartiles | a reading | q = 84, band 80-100: kept (0.11, 0.21, 0.36); song [0.097, 0.121, 0.158] | q = 84, band 80-100: kept (0.11, 0.21, 0.36); song [0.104, 0.116, 0.13] | printed | no kept rate |
| 335 | every test names its kept figure or is marked a reading | a check | every row names its kept figure, or is marked a reading or a check of the rule's own statement | every row names its kept figure, or is marked a reading or a check of the rule's own statement | yes | no kept rate |
| 336 | the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half | a reading | under floor 0.0%; content median 1.33, at kept 25th 49.6%, at kept median 1.2%; order median 2.44, at kept 25th 99.9%, at kept median 87.0%; measures outside the kept middle half 5 of 46; heaviest give-away ('on_sixteenth', -0.7) | under floor 0.0%; content median 1.06, at kept 25th 40.9%, at kept median 0.6%; order median 2.15, at kept 25th 100.0%, at kept median 79.8%; measures outside the kept middle half 5 of 46; heaviest give-away ('on_sixteenth', -0.617) | reading | no kept rate |
| 337 | a count beside another is read with its spread; a difference under two spreads is no difference | a reading (main against control) | join: no held end and breath before the line (212) 113/97 (spread 13.7, no difference); design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held 84/97 (spread 12.8, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 50/14 (spread 7.8, a difference); rhythm: no placement 23/22 (spread 6.6, no difference); align: the words do not fit the returning tune 16/9 (spread 5.0, no difference); bridge opening unrelated (208; 279) 2/1 (spread 1.7, no difference) | join: no held end and breath before the line (212) 113/97 (spread 13.7, no difference); design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held 84/97 (spread 12.8, no difference); limits: a hard limit or three soft breaks (276/277, with 286's seven) 50/14 (spread 7.8, a difference); rhythm: no placement 23/22 (spread 6.6, no difference); align: the words do not fit the returning tune 16/9 (spread 5.0, no difference); bridge opening unrelated (208; 279) 2/1 (spread 1.7, no difference) | printed | no kept rate |
| 338 | verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed | kept 25-70% (median 50%) | verse 2 share [0.0, 0.333, 1.0]; rate 0.417; copies given up 41 | verse 2 share [0.0, 0.5, 1.0]; rate 0.65; copies given up 47 | **no** | no kept rate |
| 340 | the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures | a reading (Window 134: 11.0 and 10.4) | gap 6.67 on the 30 agreed measures, both collections pooled; costliest [('gap_sixteenth', 2.5), ('empty_bars', 1.15), ('first_note_tonic_triad', 0.61), ('last_note_tonic', 0.5), ('pitch_bits', 0.39), ('range', 0.34), ('turns_per_move', 0.22), ('mean_interval', 0.21)] | gap 7.06 on the 30 agreed measures, both collections pooled; costliest [('gap_sixteenth', 2.37), ('empty_bars', 1.28), ('first_note_tonic_triad', 0.66), ('pitch_bits', 0.58), ('range', 0.5), ('gap_eighth', 0.46), ('last_note_tonic', 0.46), ('on_beats_2_4', 0.35)] | printed | no kept rate |
| 341 | of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | sixteenth onsets 15360: pushed 19%, in runs 62%; sixteenth gaps cost 4.42; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0433}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1652}} | sixteenth onsets 14978: pushed 19%, in runs 59%; sixteenth gaps cost 3.76; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0394}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1558}} | reading (420) | no kept rate |
| 342 | the lyric's density printed at intake; the builds' notes a bar | kept 3.6-4.1 (a reading) | builds' notes a bar [3.625, 5.75, 7.625] (kept 3.6-4.1) | builds' notes a bar [3.625, 5.75, 7.625] (kept 3.6-4.1) | printed | no kept rate |
| 343 | distinct note lengths cost under half a point; four at the median | kept 4.04 | distinct lengths 5.0 at the median; cost 0.82; palette dropped for 2171 lines; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.7485}} | distinct lengths 5.0 at the median; cost 1.63; palette dropped for 2327 lines; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.8331}} | reading (420) | 49% of 170 kept songs |
| 344 | notes outside the scale within two points of the kept mean; cost under half a point | kept 7.1% | outside the scale 0.9% (kept 7.1%); cost 0.87; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0092}} | outside the scale 1.0% (kept 7.1%); cost 1.13; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0098}} | reading (420) | 13% of 170 kept songs |
| 345 | chord tones on long notes cost under half a point in the verse and the chorus | kept 72% | cost verse -0.11, chorus 0.61; chord tones on long notes 60% | cost verse -0.27, chorus 0.81; chord tones on long notes 63% | printed apart (422: harmony, CoCoPops alone) | no kept rate |
| 346 | the off-beat eighth, distinct pitches and unit returns each cost under half a point | kept 0.37, 6.4, 0.17/0.19 | costs {'on_offbeat_eighth': -0.13, 'distinct_pitches': 0.24, 'unit2_returns': 0.01, 'unit3_returns': -0.0, 'unit4_to_unit2': -0.0}; both collections {'on_offbeat_eighth': {'cocopops': 0.371, 'bimmuda': 0.411, 'builds': 0.3467}} | costs {'on_offbeat_eighth': -0.16, 'distinct_pitches': 0.24, 'unit2_returns': -0.0, 'unit3_returns': -0.02, 'unit4_to_unit2': -0.0}; both collections {'on_offbeat_eighth': {'cocopops': 0.371, 'bimmuda': 0.411, 'builds': 0.3473}} | reading (420) | no kept rate |
| 347 | no measure costs more than half a point; the gap printed | the kept mean (340's judge) | over half a point: [('gap_sixteenth', 2.5), ('empty_bars', 1.15), ('first_note_tonic_triad', 0.61)]; gap 6.67 | over half a point: [('gap_sixteenth', 2.37), ('empty_bars', 1.28), ('first_note_tonic_triad', 0.66), ('pitch_bits', 0.58)]; gap 7.06 | **no** | no kept rate |
| 348 | of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point | kept 54% pushed, 31% in runs | pushed 19%, in runs 62%; sixteenth gaps cost 4.42; lines with no room (runs allowed) 4649; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0433}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1652}} | pushed 19%, in runs 59%; sixteenth gaps cost 3.76; lines with no room (runs allowed) 4720; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0394}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1558}} | reading (420) | no kept rate |
| 349 | the outside-scale share within two points of the kept mean; cost under half a point | kept 7.1% (4.5% minor) | outside the scale 0.9% (kept 7.1%); cost 0.87; placed 1923, places wanting 82260; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0092}} | outside the scale 1.0% (kept 7.1%); cost 1.13; placed 1961, places wanting 58834; both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0098}} | reading (420) | 13% of 170 kept songs |
| 350 | no unit return costs over half a point | kept unit 3 returns 31.5% | costs {'unit2_returns': 0.01, 'unit3_returns': -0.0, 'unit4_to_unit2': -0.0}; means {'unit2_returns': 0.205, 'unit3_returns': 0.308, 'unit4_to_unit2': 0.2} | costs {'unit2_returns': -0.0, 'unit3_returns': -0.02, 'unit4_to_unit2': -0.0}; means {'unit2_returns': 0.159, 'unit3_returns': 0.263, 'unit4_to_unit2': 0.155} | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 351 | verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median | kept 50% (25-70%) | bars left out 6458; lines given up 41 (1.0%); verse 2 share [0.0, 0.333, 1.0] | bars left out 6213; lines given up 47 (1.2%); verse 2 share [0.0, 0.5, 1.0] | **no** | no kept rate |
| 352 | the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats | a check; kept repeats' middle half printed | pick {'fp': 'ff83ac7a0247', 'judge': 3.15, 'rank_by_composite': 204, 'rank_by_judge': 50, 'repeats': [0.183, 0.179]}; composite first {'fp': '98cb9685bfc2', 'judge': 2.04, 'rank_by_composite': 1, 'rank_by_judge': 321, 'repeats': [0.55, 0.286]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | pick {'fp': '1b37e8117447', 'judge': 2.76, 'rank_by_composite': 266, 'rank_by_judge': 47, 'repeats': [0.267, 0.241]}; composite first {'fp': '96d8cc7ca623', 'judge': 2.88, 'rank_by_composite': 1, 'rank_by_judge': 27, 'repeats': [0.361, 0.25]}; kept repeats {'verse': [0.143, 0.394], 'chorus': [0.13, 0.4]} | amended by 362 | no kept rate |
| 353 | a minor song's degree measures read on its tonic with the natural minor scale | the rule's own statement (a check) | a major song: n/a | a major song: n/a | n/a | no kept rate |
| 354 | each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point | the kept table (372) | 5.75 notes a bar, band ['5.5 and over', '']: kept [0.189, 0.528, 0.132, 0.119], builds [0.263, 0.484, 0.1, 0.121]; eighth gaps cost 0.23; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.263, 0.189), 'gap_eighth': (0.484, 0.528)} | 5.75 notes a bar, band ['5.5 and over', '']: kept [0.189, 0.528, 0.132, 0.119], builds [0.244, 0.509, 0.106, 0.122]; eighth gaps cost 0.82; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.244, 0.189), 'gap_eighth': (0.509, 0.528)} | **no** | 1% of 170 kept songs |
| 355 | pushed within ten points of 54% and runs within ten of 31%; onsets on a sixteenth within two points of 9.4%; rhythm-placement deaths under 1 in 20 | kept 54% / 31%; 9.4% | pushed 19%, in runs 62%; on a sixteenth 16.5%; rhythm-placement deaths 2.3%; knobs run 1, on16 0.05; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0433}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1652}} | pushed 19%, in runs 59%; on a sixteenth 15.6%; rhythm-placement deaths 2.2%; knobs run 1, on16 0.065; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0394}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1558}} | reading (420) | 6% of 170 kept songs |
| 356 | rhythm-band and memory breaks within two spreads of the version before v115; four distinct lengths at the median; song 43's survivors within two spreads of 811; the diagnostic runs printed | v112 (40, 42), v114 (43) | breaks (now, before, spread) {'rhythm band': (2, 0, 1.4), 'memory': (56, 0, 7.3)}; distinct lengths 5.0; survivors (711, None, None); rounds 6; 354 stopped: no; diagnostics {}; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.7485}} | breaks (now, before, spread) {'rhythm band': (0, 0, 0.0), 'memory': (10, 0, 3.1)}; distinct lengths 5.0; survivors (760, None, None); rounds 6; 354 stopped: no; both collections {'distinct_durations': {'cocopops': 4.035, 'bimmuda': 4.74, 'builds': 4.8331}} | reading (420) | no kept rate |
| 357 | each gap share within five points of the kept table's, main and control; the rounds printed | the kept table (372) | builds [0.263, 0.484, 0.1, 0.121] against [0.189, 0.528, 0.132, 0.119]; rounds 6; knobs {'s16': 0.886, 'g8': 1.632, 'g4': 0.195, 'glong': 0.103}; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.263, 0.189), 'gap_eighth': (0.484, 0.528)} | builds [0.244, 0.509, 0.106, 0.122] against [0.189, 0.528, 0.132, 0.119]; rounds 6; knobs {'s16': 1.0, 'g8': 0.736, 'g4': 0.184, 'glong': 0.108}; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.244, 0.189), 'gap_eighth': (0.509, 0.528)} | **no** | 1% of 170 kept songs |
| 358 | outside the scale within two points of 7.1% (4.5% minor); tritone-from-root breaks within two spreads of v115 | kept 7.1% (4.5% minor) | outside the scale 0.9% (kept 7.1%); passing notes 1294 of 1923 placed, places wanting 82260; tritone-from-root breaks (now, v115, spread) (0, 0, 0.0); both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0092}} | outside the scale 1.0% (kept 7.1%); passing notes 1454 of 1961 placed, places wanting 58834; tritone-from-root breaks (now, v115, spread) (0, 0, 0.0); both collections {'outside_scale': {'cocopops': 0.071, 'bimmuda': 0.038, 'builds': 0.0098}} | reading (420) | 13% of 170 kept songs |
| 359 | a minor song's readings and costs read against the 70 kept minor windows | kept minor means (369) | a major song: n/a | a major song: n/a | n/a | no kept rate |
| 360 | verse 2's share inside 25-70% at the median and within ten points of 50% in the main run; bars left out printed | kept 50% (25-70%) | verse 2 share [0.0, 0.333, 1.0]; bars fitted again and kept 834, not 6333; left out 6458 | verse 2 share [0.0, 0.5, 1.0]; bars fitted again and kept 1335, not 6061; left out 6213 | **no** | no kept rate |
| 361 | unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate | kept 31.5%, 18.8% | means {'unit2_returns': 0.205, 'unit3_returns': 0.308, 'unit4_to_unit2': 0.2} (kept [0.172, 0.315, 0.188]); drawn {'361: unit 2 returns unit 1 (bar grid), drawn': 3460, '361: unit 3 returns unit 1 (bar grid), drawn': 4000, '361: unit 4 returns unit 2 (bar grid), drawn': 2515, '361: unit bars copied': 4013, '361: lines drawn on a returning unit': 5507, '361: unit return given up for a line': 244} | means {'unit2_returns': 0.159, 'unit3_returns': 0.263, 'unit4_to_unit2': 0.155} (kept [0.172, 0.315, 0.188]); drawn {'361: unit 3 returns unit 1 (bar grid), drawn': 3276, '361: unit 4 returns unit 2 (bar grid), drawn': 1652, '361: unit 2 returns unit 1 (bar grid), drawn': 2426, '361: unit bars copied': 3148, '361: lines drawn on a returning unit': 4245, '361: unit return given up for a line': 164} | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 362 | the pick breaks no soft limit, or none qualified and the run says so; the number that qualified printed | a check | no soft break 452 of 711; pick ff83ac7a0247 (soft none, judge rank 50); judge's first 603a13667a52 | no soft break 590 of 760; pick 1b37e8117447 (soft none, judge rank 47); judge's first 2d8afdb6d049 | yes | no kept rate |
| 363 | a design gate fails only when its rate is more than one spread under nine in ten | the paper's 317 with 337's spread | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.901} (spread {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 0.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.0103}) | {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.889} (spread {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 0.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.0106}) | **no** | no kept rate |
| 365 | 249's gap knobs do not move; each gap share within five points of the kept table's for the section's notes a bar | the kept table (372) | 249's gap knobs {'V': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}, 'C': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}}; builds [0.263, 0.484, 0.1, 0.121] against [0.189, 0.528, 0.132, 0.119]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.263, 0.189), 'gap_eighth': (0.484, 0.528)} | 249's gap knobs {'V': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}, 'C': {'gap8': 1.0, 'gap4': 1.0, 'gap16': 1.0}}; builds [0.244, 0.509, 0.106, 0.122] against [0.189, 0.528, 0.132, 0.119]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.244, 0.189), 'gap_eighth': (0.509, 0.528)} | **no** | 1% of 170 kept songs |
| 366 | runs within ten points of 31% and pushes within ten of 54%, main and control; fallback lines printed | kept 31% / 54% | pushed 19%, in runs 62%; rate 1.0; lines may run 16053, may not 0, fallback 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0433}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1652}} | pushed 19%, in runs 59%; rate 1.0; lines may run 16358, may not 0, fallback 0; both collections {'pushed': {'cocopops': 0.123, 'bimmuda': 0.164, 'builds': 0.0394}, 'on_sixteenth': {'cocopops': 0.094, 'bimmuda': 0.134, 'builds': 0.1558}} | reading (420) | no kept rate |
| 367 | 356's band printed with its source | kept quartiles (a check) | band [1.934, 2.735] (the pooled kept table on 105 kept chart songs (373); the v88 table on 103: 2.20-2.94 (367)); stop did not fire | band [1.934, 2.735] (the pooled kept table on 105 kept chart songs (373); the v88 table on 103: 2.20-2.94 (367)); stop did not fire | yes | no kept rate |
| 368 | song 43: memory breaks (373's limit) within two spreads of v114's read the same way, or the fix responsible named | v114, read with 373's limit |  |  | — | no kept rate |
| 369 | 364's figures for v115 reproduce 0.966, 0.954, 0.942 and 0.909 within 0.01; song 43's costs read against the 70 minor windows | Window 136 (sep_v118) |  |  | — | no kept rate |
| 370 | verse 2's share within ten points of 50% at the median in the main run | kept 50% | verse 2 share [0.0, 0.333, 1.0]; kept by variant {'370: kept by variant one added': 230, '370: kept by variant copy': 596, '370: kept by variant one dropped': 8}; fitted again kept 834, not 6333 | verse 2 share [0.0, 0.5, 1.0]; kept by variant {'370: kept by variant one added': 418, '370: kept by variant copy': 897, '370: kept by variant one dropped': 20}; fitted again kept 1335, not 6061 | **no** | no kept rate |
| 371 | unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate | kept 31.5%, 18.8% | means {'unit2_returns': 0.205, 'unit3_returns': 0.308, 'unit4_to_unit2': 0.2} (kept [0.172, 0.315, 0.188]); rates {'unit2_returns': 0.8671, 'unit3_returns': 1.0, 'unit4_to_unit2': 0.6324}; returns over pairs 3921 | means {'unit2_returns': 0.159, 'unit3_returns': 0.263, 'unit4_to_unit2': 0.155} (kept [0.172, 0.315, 0.188]); rates {'unit2_returns': 0.6194, 'unit3_returns': 0.8217, 'unit4_to_unit2': 0.4216}; returns over pairs 3092 | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 372 | with every gap knob starting at one, the four gap shares within five points of the kept table's; each knob's final value printed | the kept table | knobs {'s16': 0.8857, 'g8': 1.6317, 'g4': 0.195, 'glong': 0.1033, 'run': 1.0, 'on16': 0.05}; past a factor of two ['g4', 'glong', 'on16']; builds [0.263, 0.484, 0.1, 0.121] against [0.189, 0.528, 0.132, 0.119]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.263, 0.189), 'gap_eighth': (0.484, 0.528)} | knobs {'s16': 1.0, 'g8': 0.7364, 'g4': 0.1841, 'glong': 0.1081, 'run': 1.0, 'on16': 0.065}; past a factor of two ['g4', 'glong', 'on16']; builds [0.244, 0.509, 0.106, 0.122] against [0.189, 0.528, 0.132, 0.119]; on the agreed two (sixteenth, eighth): {'gap_sixteenth': (0.244, 0.189), 'gap_eighth': (0.509, 0.528)} | **no** | 1% of 170 kept songs |
| 373 | each limit printed with its corpus; soft breaks of the rhythm band and of memory near one build in ten or fewer | kept chart songs | soft breaks: rhythm band 2, memory 56 of 847 complete | soft breaks: rhythm band 0, memory 10 of 872 complete | yes | no kept rate |
| 374 | the builds' separation beside 0.57 and 0.63 | the yardstick (sep_v118) |  |  | — | no kept rate |
| 375 | no sung note a semitone from a chord's raised tone on a beat or held a beat; 349's places wanting under a tenth of its target | the rule (a check) | a secondary dominant's raised third: 0 of 0 notes a semitone from it; any chord tone outside the scale: 0 of 0 (where {}); 349 placed 1923, wanting 82260 | a secondary dominant's raised third: 0 of 0 notes a semitone from it; any chord tone outside the scale: 0 of 0 (where {}); 349 placed 1961, wanting 58834 | yes | no kept rate |
| 376 | a run in which a knob freezes completes and prints the round | a check | stop no knob froze | stop no knob froze | yes | no kept rate |
| 377 | song 45: the lift's failures under one complete build in twenty; drawn and pinned medians printed | the rule | no pinned notes in this song | no pinned notes in this song | n/a | no kept rate |
| 378 | the median share of the slot sung, by notes, inside the kept middle half; under one line in twenty under half its slot when its syllables in eighths would fill half | kept 43-75, 53-80, 66-88, 78-94%; 4.6% | median share {'3-5': 0.727, '6-8': 0.611, '9-12': 0.714, '13+': 0.812} (all 0.727, kept 0.71); under half of full lines 1.2% (kept 4.6%); drawn to a span 8202, given up 276 | median share {'3-5': 0.727, '6-8': 0.611, '9-12': 0.735, '13+': 0.812} (all 0.727, kept 0.71); under half of full lines 1.0% (kept 4.6%); drawn to a span 8252, given up 256 | yes | no kept rate |
| 379 | no held sung note a semitone or minor ninth from a sustained accompaniment note | n/a here (song 45's build) | an arrangement rule: in song 45's build and its consistency checks (songs/p49); these runs build no arrangement | an arrangement rule: in song 45's build and its consistency checks (songs/p49); these runs build no arrangement | n/a | no kept rate |
| 380 | a chosen lift met in nine builds in ten (with its spread), with no more redraws than 311's endings take | the paper's 317 with 337's spread | lift [-1.0, 0.0, 3.0]; design {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.901}; redraws design 0, ending 0 | lift [-1.0, 0.0, 2.625]; design {"design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line": 1.0, "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held": 0.889}; redraws design 0, ending 0 | n/a | no kept rate |
| 381 | no note outside the song's sung pitch classes (a chord's own tones aside) | the rule (a check) | notes outside the sung pitch classes 0; passing placed 1294 | notes outside the sung pitch classes 0; passing placed 1454 | yes | no kept rate |
| 382 | the seven limits printed with their corpus; builds lost to limits under one in five; surprisal and memory breaks beside a design | kept chart songs | lost to limits 5.0%; surprisal breaks 3, memory 56; beside the design gate | lost to limits 1.4%; surprisal breaks 1, memory 10; beside the design gate | yes | no kept rate |
| 383 | each hand-edited line before and after, with both scores | n/a (no hand edits) | no hand edits in these runs (song 45 as drawn) | no hand edits in these runs (song 45 as drawn) | n/a | no kept rate |
| 384 | generators patched by whole statements; each patched path run once before a run of record | a check (the smoke run) | every patch matched exactly once in each file (gen_v119.py); smoke paths no smoke run on file | every patch matched exactly once in each file (gen_v119.py); smoke paths no smoke run on file | reading | no kept rate |
| 385 | notes outside the scale within two points of 7.1% (4.5% minor) | kept 7.1% (4.5% minor) | outside the scale 0.9% (kept 7.1%); cost 0.87; placed 1923, wanting 82260; passing 1294 | outside the scale 1.0% (kept 7.1%); cost 1.13; placed 1961, wanting 58834; passing 1454 | reading (420) | 13% of 170 kept songs |
| 386 | no sung note on a beat or a beat long a semitone from a chord's own outside tone, in drawn, returning or copied lines | the rule (a check) | clashes 0 of 0 notes read; moved {} | clashes 0 of 0 notes read; moved {} | yes | no kept rate |
| 387 | 356's stop a reading: it moves and freezes no knob | a check | stop did not fire; knobs {'s16': 0.886, 'g8': 1.632, 'g4': 0.195, 'glong': 0.103} | stop did not fire; knobs {'s16': 1.0, 'g8': 0.736, 'g4': 0.184, 'glong': 0.108} | yes | no kept rate |
| 388 | the two side runs made and read; nothing changed | printed (step 2) | the two side runs on song 40 (step 2): see the report | the two side runs on song 40 (step 2): see the report | printed | no kept rate |
| 389 | runs within ten points of the band's kept share; deaths for want of a rhythm within two spreads of v116's (song 45: none) | the kept table's bands; v116 | bands {'3.5 to 4.5': {'onsets': 9807, 'in_runs': 0.341, 'kept': 0.291, 'rate': 1.0}, '5.5 and over': {'onsets': 28950, 'in_runs': 0.593, 'kept': 0.361, 'rate': 1.0}, 'under 3.5': {'onsets': 3419, 'in_runs': 0.345, 'kept': 0.271, 'rate': 1.0}}; rhythm deaths 23 (before None, v116 None); join deaths 113; fallbacks {} | bands {'3.5 to 4.5': {'onsets': 7024, 'in_runs': 0.336, 'kept': 0.291, 'rate': 1.0}, '5.5 and over': {'onsets': 28505, 'in_runs': 0.569, 'kept': 0.361, 'rate': 1.0}, 'under 3.5': {'onsets': 1881, 'in_runs': 0.457, 'kept': 0.271, 'rate': 1.0}}; rhythm deaths 22 (before None, v116 None); join deaths 97; fallbacks {} | **no** | no kept rate |
| 390 | unit returns within ten points of the kept rates on the units free to draw; the free share printed | kept 17.2%, 31.5%, 18.8% | free units {'unit2_returns': {'free_mean': 0.205, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.308, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.2, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; rates {'unit2_returns': 0.8671, 'unit3_returns': 1.0, 'unit4_to_unit2': 0.6324}; plan none | free units {'unit2_returns': {'free_mean': 0.159, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.263, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.155, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; rates {'unit2_returns': 0.6194, 'unit3_returns': 0.8217, 'unit4_to_unit2': 0.4216}; plan none | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 391 | 378 read on drawn lines: the median share by notes inside the kept middle half; spans given up under one in twenty | kept 43-75, 53-80, 66-88, 78-94% | drawn lines 8552: median share {'6-8': 0.6, '9-12': 0.704, '13+': 0.828}; under half of full 0.5%; widened 795; given up 276 of 8478 (3.3%) | drawn lines 8818: median share {'6-8': 0.6, '9-12': 0.714, '13+': 0.828}; under half of full 0.5%; widened 749; given up 256 of 8508 (3.0%) | yes | no kept rate |
| 392 | song 45: the lift's failures under one complete build in twenty, read on drawn notes | the rule | no pinned notes in this song | no pinned notes in this song | n/a | no kept rate |
| 393 | verse 2's share on the lines of verse 1's syllable count within ten points of 50% (main run); the rest printed | kept 50% | equal lines [3]: share [0.0, 0.333, 1.0]; the rest [0.0, 0.167, 0.5]; all lines [0.0, 0.25, 0.5] | equal lines [3]: share [0.0, 0.5, 1.0]; the rest [0.0, 0.167, 0.667]; all lines [0.0, 0.375, 0.625] | yes | no kept rate |
| 394 | song 43's memory breaks within two spreads of v114's; the others printed | v114, read with 373's limit | memory breaks 56 (before None, v114 None); {'394: passing note placed in every occurrence': 953, '394: occurrences given the passing note': 21, '394: passing note withdrawn (an occurrence could not take it)': 177} | memory breaks 10 (before None, v114 None); {'394: passing note placed in every occurrence': 1105, '394: occurrences given the passing note': 54, '394: passing note withdrawn (an occurrence could not take it)': 190} | reading | no kept rate |
| 395 | 311 and 324 read in the section's own key where the record lifts it | the rule (a check) | lifted none; Last Chorus on the tonic 90.7%; tonic endings 847 | lifted none; Last Chorus on the tonic 96.4%; tonic endings 872 | n/a (no lift) | no kept rate |
| 396 | separability by family printed beside Window 139 | Table DY (sep_v119) | separability by family: sep_v119.py, across the five songs | separability by family: sep_v119.py, across the five songs | below | no kept rate |
| 398 | chord tones 54-76% at the median, on a beat 56-80%; non-chord notes resolved by step within ten points of 50% | kept 64%, 67%, 72%; 50% | chord tones 58.3%, on a beat 58.3%, on a downbeat 0.5; resolved by step 43.9%; knobs {'ct398': 3.457, 'ctb398': 4.049, 'ctd398': 1.0, 'res398': 6.3655, 'turn400': 0.9941} | chord tones 63.3%, on a beat 61.5%, on a downbeat 0.6; resolved by step 48.1%; knobs {'ct398': 3.0239, 'ctb398': 3.8208, 'ctd398': 1.0, 'res398': 4.2396, 'turn400': 1.2798} | printed apart (422: harmony, CoCoPops alone) | 46% of 170 kept songs |
| 399 | a sung note on the downbeat of Verse 1's and Chorus 1's first bar in 59-79% of builds, unless a design places the entry | kept 69% | withdrawn by v120 (421); printed: {'Verse 1': 0.532, 'Chorus 1': 0.0} beside both collections (first onset: CoCoPops 0.37 beats, BiMMuDa 1.36) | withdrawn by v120 (421); printed: {'Verse 1': 0.557, 'Chorus 1': 0.0} beside both collections (first onset: CoCoPops 0.37 beats, BiMMuDa 1.36) | withdrawn (421) | no kept rate |
| 400 | turns per move within 0.04 of 0.58 at the mean, verse and chorus | kept 0.58 | verse 0.647, chorus 0.483 (kept 0.584); knob 0.9941 | verse 0.657, chorus 0.476 (kept 0.584); knob 1.2798 | **no** | 30% of 170 kept songs |
| 401 | four distinct note lengths in the judge's window at the median | kept 4 | withdrawn by v120 (421); 343 a reading: distinct lengths 5.0 at the median (CoCoPops 4.0, BiMMuDa 4.7) | withdrawn by v120 (421); 343 a reading: distinct lengths 5.0 at the median (CoCoPops 4.0, BiMMuDa 4.7) | withdrawn (421) | 49% of 170 kept songs |
| 424 | leaps of a fourth or fifth, the window's last note on the tonic and empty bars each between the two collections' means or within a fifth of a sd of the nearer; outside the scale printed (420) | CoCoPops and BiMMuDa 1958-1991 | aims {'fourth_fifth': {'builds': 0.1015, 'cocopops': 0.08, 'bimmuda': 0.087, 'fifth_sd': 0.0156, 'held': True, 'agreed': True}, 'last_note_tonic': {'builds': 0.0425, 'cocopops': 0.277, 'bimmuda': 0.329, 'fifth_sd': 0.0945, 'held': False, 'agreed': True}, 'empty_bars': {'builds': 0.0342, 'cocopops': 0.468, 'bimmuda': 0.506, 'fifth_sd': 0.152, 'held': False, 'agreed': False, 'note': 'printed (428)'}, 'outside_scale': {'builds': 0.0092, 'cocopops': 0.071, 'bimmuda': 0.038, 'fifth_sd': 0.0254, 'held': False, 'agreed': False}}; knobs {'ff424': 0.3193, 'lt424': 10.0, 'eb424': 0.25}; {} | aims {'fourth_fifth': {'builds': 0.0802, 'cocopops': 0.08, 'bimmuda': 0.087, 'fifth_sd': 0.0156, 'held': True, 'agreed': True}, 'last_note_tonic': {'builds': 0.0453, 'cocopops': 0.277, 'bimmuda': 0.329, 'fifth_sd': 0.0945, 'held': False, 'agreed': True}, 'empty_bars': {'builds': 0.0315, 'cocopops': 0.468, 'bimmuda': 0.506, 'fifth_sd': 0.152, 'held': False, 'agreed': False, 'note': 'printed (428)'}, 'outside_scale': {'builds': 0.0098, 'cocopops': 0.071, 'bimmuda': 0.038, 'fifth_sd': 0.0254, 'held': False, 'agreed': False}}; knobs {'ff424': 0.2431, 'lt424': 10.0, 'eb424': 0.25}; {} | **no** | 28% of 170 kept songs |
| 459 | verse 2 read on bars whose syllable counts differ by one or less: half its bars or more read, the median share within ten points of 50% (main run) | kept 50% | share [0.0, 0.4, 0.8]; bars read [0.5, 0.625, 0.75]; builds with no such bar 0; rate 0.4166666666666667 | share [0.0, 0.6, 1.0]; bars read [0.625, 0.625, 0.75]; builds with no such bar 0; rate 0.6499999999999999 | yes | no kept rate |
| 465 | a drawn line's last onset in the bar the kept share for its notes draws; class given up and span given up each under one line in twenty | kept shares by notes (zeneng_v128_kept_lines.json) | drawn 8237, held 7442, given up 795, no class 846, landing fixed 0, entry given up 792; spans given up 276 of 8478; widest class gap 0.3999999999999999; 3 to 5: [0.0, 0.694, 0.306, 0.0] (kept [0.316, 0.531, 0.114, 0.039]), 4+ beats 0.333 (kept 0.423); 6 to 8: [0.055, 0.886, 0.059, 0.0] (kept [0.263, 0.61, 0.111, 0.017]), 4+ beats 0.626 (kept 0.483); 9 to 12: [0.056, 0.941, 0.002, 0.0] (kept [0.326, 0.541, 0.127, 0.006]), 4+ beats 0.15 (kept 0.364); 13 and over: [0.31, 0.69, 0.0, 0.0] (kept [0.385, 0.554, 0.053, 0.008]), 4+ beats 0.0 (kept 0.295) | drawn 8301, held 7553, given up 748, no class 933, landing fixed 0, entry given up 745; spans given up 256 of 8508; widest class gap 0.4019999999999999; 3 to 5: [0.0, 0.69, 0.31, 0.0] (kept [0.316, 0.531, 0.114, 0.039]), 4+ beats 0.333 (kept 0.423); 6 to 8: [0.048, 0.899, 0.054, 0.0] (kept [0.263, 0.61, 0.111, 0.017]), 4+ beats 0.644 (kept 0.483); 9 to 12: [0.057, 0.943, 0.0, 0.0] (kept [0.326, 0.541, 0.127, 0.006]), 4+ beats 0.085 (kept 0.364); 13 and over: [0.328, 0.672, 0.0, 0.0] (kept [0.385, 0.554, 0.053, 0.008]), 4+ beats 0.0 (kept 0.295) | **no** | no kept rate |
| 458 | the span's bounds from kept lines' notes a second; drawn lines' median rate inside the kept 25th-75th by notes (bands of 200 lines or more) | kept 2.2-3.8 notes a second | 3 to 5: [0.6, 1.4, 1.4] (kept [2.247, 2.993, 3.775], 2400 lines); 6 to 8: [1.68, 2.1, 2.45] (kept [2.358, 3.04, 3.835], 6348 lines); 9 to 12: [2.369, 2.567, 2.8] (kept [2.525, 3.091, 3.572], 2446 lines); 13 and over: [3.136, 3.446, 3.733] (kept [2.675, 3.164, 3.82], 2406 lines); tempo 84 | 3 to 5: [0.6, 1.4, 1.4] (kept [2.247, 2.993, 3.775], 2400 lines); 6 to 8: [1.68, 2.1, 2.4] (kept [2.358, 3.04, 3.835], 6629 lines); 9 to 12: [2.4, 2.567, 2.8] (kept [2.525, 3.091, 3.572], 2171 lines); 13 and over: [3.136, 3.446, 3.733] (kept [2.675, 3.164, 3.82], 2400 lines); tempo 84 | **no** | no kept rate |
| 478 | verse 2's repeats and steps within five points of verse 1's (first eight bars, build by build) | the first verse's own rates | repeats verse 1 / verse 2 (0.306, 0.309), steps (0.395, 0.435); knobs (0.7333, 0.8172) | repeats verse 1 / verse 2 (0.305, 0.307), steps (0.389, 0.425); knobs (0.6639, 0.6798) | yes | no kept rate |
| 484 | the pitch verse 2 keeps of verse 1 (Window 142's pair) inside 72-79% | kept 72-79% | pitch kept 0.725; rate 0.5146 | pitch kept 0.788; rate 0.6401 | yes | no kept rate |
| 476 | the content judge of record is zeneng_v128_judge.json; builds under its kept 25th percentile printed | kept mean 1.53, sd 2.0, 25th 0.23 | content mean -0.391; under the kept 25th 0.783; under 1.53 - 1.645 sd 0.034 | content mean -0.522; under the kept 25th 0.849; under 1.53 - 1.645 sd 0.037 | printed | no kept rate |
| 477 | the pick's score the mean of content and order, window by window | the rule (a check) | pick ff83ac7a0247, score 2.735; check True | pick 1b37e8117447, score 2.5; check True | printed | no kept rate |
| 486 | 389's run rates read on Verse 1 and Chorus 1 for their bands | printed | judged bands ['3.5 to 4.5', '5.5 and over']; last round {'under 3.5': (0.271, 0.312, 1.0), '3.5 to 4.5': (0.291, 0.42, 1.0), '5.5 and over': (0.361, 0.538, 1.0)} | judged bands ['3.5 to 4.5', '5.5 and over']; last round {'under 3.5': (0.271, 0.243, 1.0), '3.5 to 4.5': (0.291, 0.32, 1.0), '5.5 and over': (0.361, 0.522, 1.0)} | printed | no kept rate |
| 489 | 452's knobs by band of density | read in the reread by density band | knobs {'under 3.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '3.5 to 4.5': {'gs': 0.2087, 'er': 0.0467, 'zz': 12.7073}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 0.0634, 'er': 0.0467, 'zz': 0.0778}} | knobs {'under 3.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '3.5 to 4.5': {'gs': 0.1547, 'er': 0.0574, 'zz': 16.7772}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 0.0488, 'er': 0.0467, 'zz': 0.1902}} | read in the reread, by density band | no kept rate |
| 490 | a weight on an onset in a run, by band; drawable runs within ten points on bands of 200 onsets or more | kept by band (389) | run weights {'under 3.5': 0.3407, '3.5 to 4.5': 0.1395, '4.5 to 5.5': 1.0, '5.5 and over': 0.0566}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (4456, 0.362)), '5.5 and over': (0.361, (8243, 0.508)), 'under 3.5': (0.271, (656, 0.293))} | run weights {'under 3.5': 3.3176, '3.5 to 4.5': 0.4903, '4.5 to 5.5': 1.0, '5.5 and over': 0.0822}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (2942, 0.369)), '5.5 and over': (0.361, (7864, 0.471)), 'under 3.5': (0.271, (355, 0.451))} | **no** | no kept rate |
| 491 | 467's and 408's knobs withdrawn; song 45's chorus floor no lower than its lift allows: design deaths under one in twenty | the design (a check) | 467's and 408's knobs withdrawn (all songs); the floor is song 45's | 467's and 408's knobs withdrawn (all songs); the floor is song 45's | n/a | no kept rate |
| 494 | 457 falls back at once when no entry and landing fit the strict copy | printed | at once 3234, at half 707; rhythm deaths 23; joins {'join: no held end and breath before the line (212)': 113} | at once 2444, at half 515; rhythm deaths 22; joins {'join: no held end and breath before the line (212)': 97} | printed | no kept rate |
| 500 | 465's class drawn by the slot's length and the notes: classes within ten points of the kept for each notes band and slot (200 lines or more); given up under one line in twenty | kept shares by notes and by slot, combined | drawn 8237, given up 795; out of reach 3360; widest gap 0.29699999999999993; 3 to 5 notes, 2-bar slot: [0.0, 0.694, 0.306, 0.0] (kept [0.264, 0.651, 0.085, 0.0]); 6 to 8 notes, 2-bar slot: [0.055, 0.886, 0.059, 0.0] (kept [0.209, 0.712, 0.079, 0.0]); 9 to 12 notes, 2-bar slot: [0.056, 0.941, 0.002, 0.0] (kept [0.265, 0.644, 0.092, 0.0]); 13 and over notes, 2-bar slot: [0.31, 0.69, 0.0, 0.0] (kept [0.309, 0.653, 0.038, 0.0]) | drawn 8301, given up 748; out of reach 3530; widest gap 0.29899999999999993; 3 to 5 notes, 2-bar slot: [0.0, 0.69, 0.31, 0.0] (kept [0.264, 0.651, 0.085, 0.0]); 6 to 8 notes, 2-bar slot: [0.048, 0.899, 0.054, 0.0] (kept [0.209, 0.712, 0.079, 0.0]); 9 to 12 notes, 2-bar slot: [0.057, 0.943, 0.0, 0.0] (kept [0.265, 0.644, 0.092, 0.0]); 13 and over notes, 2-bar slot: [0.328, 0.672, 0.0, 0.0] (kept [0.309, 0.653, 0.038, 0.0]) | **no** | no kept rate |
| 501 | 458 read in onsets a beat: drawn lines' median inside the kept 25th-75th by notes (200 lines or more) | kept 1.1-2.0 onsets a beat | 3 to 5: [0.857, 0.857, 1.0] (kept [1.143, 1.6, 2.0], 2400 lines); 6 to 8: [1.333, 1.714, 2.0] (kept [1.25, 1.636, 2.0], 6348 lines); 9 to 12: [1.8, 1.905, 2.0] (kept [1.286, 1.571, 1.882], 2446 lines); 13 and over: [2.364, 2.545, 2.727] (kept [1.333, 1.586, 2.0], 2406 lines); inside 7442, redrawn 21668, given up 795 | 3 to 5: [0.857, 0.857, 1.0] (kept [1.143, 1.6, 2.0], 2400 lines); 6 to 8: [1.333, 1.714, 1.75] (kept [1.25, 1.636, 2.0], 6629 lines); 9 to 12: [1.818, 1.905, 2.0] (kept [1.286, 1.571, 1.882], 2171 lines); 13 and over: [2.364, 2.545, 2.727] (kept [1.333, 1.586, 2.0], 2400 lines); inside 7553, redrawn 20684, given up 749 | **no** | no kept rate |
| 502 | song 45: the floor at the verse's median and three; design deaths under one in twenty | the design (a check) | song 45 only | song 45 only | n/a | no kept rate |
| 503 | verse 2's chord tones on the beat within five points of verse 1's (the engine's windows) | the first verse's own rate | verse 1 / verse 2 0.683 / 0.71; knob 0.2789 | verse 1 / verse 2 0.76 / 0.754; knob 0.2789 | yes | no kept rate |
| 504 | 452's band knobs keyed by the line's own notes a bar | read in the reread by density band | notes to syllables 1.0082; knobs {'under 3.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '3.5 to 4.5': {'gs': 0.2087, 'er': 0.0467, 'zz': 12.7073}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 0.0634, 'er': 0.0467, 'zz': 0.0778}} | notes to syllables 1.002; knobs {'under 3.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '3.5 to 4.5': {'gs': 0.1547, 'er': 0.0574, 'zz': 16.7772}, '4.5 to 5.5': {'gs': 1.0, 'er': 1.0, 'zz': 1.0}, '5.5 and over': {'gs': 0.0488, 'er': 0.0467, 'zz': 0.1902}} | read in the reread, by density band | no kept rate |
| 505 | the run weight aimed alone (389's rate at one): drawable runs within ten points on bands of 200 onsets or more | kept by band (389) | 389's rates {'under 3.5': 1.0, '3.5 to 4.5': 1.0, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; run weights {'under 3.5': 0.3407, '3.5 to 4.5': 0.1395, '4.5 to 5.5': 1.0, '5.5 and over': 0.0566}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (4456, 0.362)), '5.5 and over': (0.361, (8243, 0.508)), 'under 3.5': (0.271, (656, 0.293))} | 389's rates {'under 3.5': 1.0, '3.5 to 4.5': 1.0, '4.5 to 5.5': 1.0, '5.5 and over': 1.0}; run weights {'under 3.5': 3.3176, '3.5 to 4.5': 0.4903, '4.5 to 5.5': 1.0, '5.5 and over': 0.0822}; drawable runs (kept, (onsets, share)) {'3.5 to 4.5': (0.291, (2942, 0.369)), '5.5 and over': (0.361, (7864, 0.471)), 'under 3.5': (0.271, (355, 0.451))} | **no** | no kept rate |
| 508 | a return after a designed line fitted to its breath: joins before a copy printed | printed | joins before a copy 0, before a line 113; fitted 0; align 16 | joins before a copy 0, before a line 97; fitted 0; align 9 | printed | no kept rate |
| 513 | 440's step tested on the finished chart; an inversion that has lost it taken back | the rule (a check) | inversions []; taken back [] | inversions []; taken back [] | yes | no kept rate |
| 519 | the content judge of record is zeneng_v129_judge.json; complete builds under the kept songs' 5th percentile (-0.72) printed; the floor stays on v108 | kept songs: 5th -0.72, median 1.42 | content mean -0.391; under the kept songs' 5th 36%; stays on the v108 judge (under -0.72 on every song is not under a third) | content mean -0.522; under the kept songs' 5th 42%; stays on the v108 judge (under -0.72 on every song is not under a third) | printed | no kept rate |
| 520 | no knob named for 408 or 455 in the run; the window's range printed beside the song's design (not aimed) | the rule (a check); kept range 10.9 | 408 knob in the run False; 455 knob in the run False; range verse 10.36, chorus 10.38 (kept 10.9):  | 408 knob in the run False; 455 knob in the run False; range verse 10.33, chorus 10.04 (kept 10.9):  | yes | no kept rate |
| 438 | the chart's share of bars with two or more changes inside the kept middle half (or none, drawn at the kept rate), and of bars holding the last bar's chord inside its middle half | kept 0-0.33; 0.08-0.44; none in 25% and 37% of songs | two or more 0.0 -> 0.0 (target 0.0), held bars 0.08 -> 0.102 (target 0.093); edits 1 | two or more 0.0 -> 0.0 (target 0.0), held bars 0.08 -> 0.102 (target 0.093); edits 1 | yes | no kept rate |
| 440 | the bass on the root at nine changes in ten or more; a third or fifth with a step on one side; at most one chord in twelve | the rule (a check) | root at 100.0% of 79 changes; inversions [] (a step beside each: []) | root at 100.0% of 79 changes; inversions [] (a step beside each: []) | yes | no kept rate |
| 464 | song 45: deaths at 267 at or under v118's (267 reads the bridge G before its raise) | v118 (songs/p50) | song 45 only | song 45 only | n/a | no kept rate |
| 470 | the content judge of record is the refit: its mean on complete builds, beside the v108 content | kept median 1.97 | refit content: complete builds -0.391, survivors -0.391 (v108 content 1.427; rank correlation 0.333) | refit content: complete builds -0.522, survivors -0.522 (v108 content 1.067; rank correlation 0.393) | printed | no kept rate |
| 471 | the floor on the v108 judge; the share of complete builds under the refit's kept 5th percentile (-0.51) printed | under a third on every song moves it | under the refit's kept 5th percentile 46% of complete builds; floor deaths (v108) 0; floor stays on the v108 judge | under the refit's kept 5th percentile 52% of complete builds; floor deaths (v108) 0; floor stays on the v108 judge | floor stays on the v108 judge | no kept rate |
| 472 | the pick: the refit's first among survivors with no soft break; each pick's rank under the other judge | printed | pick ff83ac7a0247; v108's pick 603a13667a52 (rank under the refit 4); the refit's pick's rank under v108 35; clean 452 | pick 1b37e8117447; v108's pick 2d8afdb6d049 (rank under the refit 2); the refit's pick's rank under v108 36; clean 590 | printed | no kept rate |
| 473 | the judge does not read a second verse | the rule | the judge reads the first eight bars of Verse 1 and Chorus 1 only; verse 2 answers to 434's test | the judge reads the first eight bars of Verse 1 and Chorus 1 only; verse 2 answers to 434's test | n/a | no kept rate |
| 456 | the last-note test read on windows whose last note the walk chose (100 or more): between the collections' means or within a fifth of a sd of the nearer | CoCoPops and BiMMuDa 1958-1991 | walked windows 718, on the tonic 10.0% (collections (0.277, 0.329)) | walked windows 767, on the tonic 10.3% (collections (0.277, 0.329)) | a reading of the mean of builds (512; outside the band) | 0% of 170 kept songs |
| 405 | 389 read on drawable lines: runs within ten points of the band's kept share where 200 onsets or more; song 45's rhythm deaths within two spreads of v116's (none) | the kept table's bands; v116 | bands (kept, rate, drawable n/runs, no room or fell back, not drawn) {'3.5 to 4.5': {'kept': 0.291, 'rate': 1.0, 'drawable': (4456, 0.362), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (5351, 0.324)}, '5.5 and over': {'kept': 0.361, 'rate': 1.0, 'drawable': (8243, 0.508), 'no room or fell back': (20006, 0.63), 'not drawn by the rhythm (copy, return, design)': (701, 0.515)}, 'under 3.5': {'kept': 0.271, 'rate': 1.0, 'drawable': (656, 0.293), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (2763, 0.358)}}; lines {'405: line drawable without runs': 11404, '405: line with no room on the eighth grid': 4626}; rhythm deaths 23 (before None) | bands (kept, rate, drawable n/runs, no room or fell back, not drawn) {'3.5 to 4.5': {'kept': 0.291, 'rate': 1.0, 'drawable': (2942, 0.369), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (4082, 0.312)}, '5.5 and over': {'kept': 0.361, 'rate': 1.0, 'drawable': (7864, 0.471), 'no room or fell back': (19885, 0.611), 'not drawn by the rhythm (copy, return, design)': (756, 0.47)}, 'under 3.5': {'kept': 0.271, 'rate': 1.0, 'drawable': (355, 0.451), 'no room or fell back': (0, 0.0), 'not drawn by the rhythm (copy, return, design)': (1526, 0.458)}}; lines {'405: line drawable without runs': 11638, '405: line with no room on the eighth grid': 4698}; rhythm deaths 22 (before None) | **no** | no kept rate |
| 409 | the window's last note on the tonic between the collections' means (27.7%, 32.9%) or within a fifth of a sd of the nearer, where the endings are not designed; its sources printed | CoCoPops and BiMMuDa 1958-1991 | on the tonic 4.2% (collections (0.277, 0.329)); walked 42%; by source (n, tonic) {'Chorus 1: a carried extreme (329)': (129, 0.0), 'Chorus 1: the walk': (718, 0.1), 'Verse 1: a copy or return': (180, 0.0), 'Verse 1: an ending rule': (667, 0.0)}; knob 10.0 | on the tonic 4.5% (collections (0.277, 0.329)); walked 44%; by source (n, tonic) {'Chorus 1: a carried extreme (329)': (105, 0.0), 'Chorus 1: the walk': (767, 0.103), 'Verse 1: a copy or return': (198, 0.0), 'Verse 1: an ending rule': (674, 0.0)}; knob 10.0 | n/a: endings designed (walked 42% of windows); on the tonic 4.3% | 0% of 170 kept songs |
| 412 | song 45: deaths at 267 within two spreads of v118's, the lift's failures under one in twenty | v118 (songs/p50) | deaths at 267 0 (v119 None, v118 None); with 267 read before the raise (450): None; lift failures None | deaths at 267 0 (v119 None, v118 None); with 267 read before the raise (450): None; lift failures None | reading (song 45's test) | no kept rate |
| 413 | unit returns within ten points of the pooled kept rates on the free units; losses counted | pooled kept | free units {'unit2_returns': {'free_mean': 0.205, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.308, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.2, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; losses {'361: unit bars copied': 4013, '413: unit-return bars left out (more than one onset off)': 5064, '361: unit return given up for a line': 244, '413: unit-return pitch not kept (range, slur or chord), a try': 873, '413: build lost on a unit-return line (no rhythm)': 21} | free units {'unit2_returns': {'free_mean': 0.159, 'kept': 0.172, 'free_share': 1.0, 'kept_pooled': 0.1635}, 'unit3_returns': {'free_mean': 0.263, 'kept': 0.315, 'free_share': 1.0, 'kept_pooled': 0.3006}, 'unit4_to_unit2': {'free_mean': 0.155, 'kept': 0.188, 'free_share': 1.0, 'kept_pooled': 0.1944}}; losses {'361: unit bars copied': 3148, '413: unit-return bars left out (more than one onset off)': 3855, '413: unit-return pitch not kept (range, slur or chord), a try': 547, '361: unit return given up for a line': 164, '413: build lost on a unit-return line (no rhythm)': 11} | a reading of the mean of builds (512; inside the band) | 0% of 170 kept songs |
| 414 | spans given up under one line in twenty | the rule | given up 276 of 8478 (3.3%); median share {'6-8': 0.6, '9-12': 0.704, '13+': 0.828}; {} | given up 256 of 8508 (3.0%); median share {'6-8': 0.6, '9-12': 0.714, '13+': 0.828}; {} | yes | no kept rate |
| 415 | verse 2 read on bars of equal syllables: half its bars or more read, the median share within ten points of 50% (main run) | kept 50% | share [0.0, 0.4, 0.8]; bars read [0.5, 0.625, 0.75]; builds with no such bar 0; rate 0.4166666666666667 | share [0.0, 0.6, 1.0]; bars read [0.625, 0.625, 0.75]; builds with no such bar 0; rate 0.6499999999999999 | yes | no kept rate |
| 417 | 311 reads the last chorus; a designed tag printed apart | the rule (a check) | Last Chorus on the tonic 90.7%; tag ('Tag', {0: 847}) | Last Chorus on the tonic 96.4%; tag ('Tag', {0: 872}) | **no** | no kept rate |
| 419 | no clash read on the chord at the note | the rule (a check) | clashes 0 of 0 (bar chord: 0); by kind {}; [] | clashes 0 of 0 (bar chord: 0); by kind {}; [] | yes | no kept rate |
| 428 | empty bars printed, not aimed, beside 378's slot share | printed | empty bars 0.034 (CoCoPops 0.468, BiMMuDa 0.506); 378's slot share {'6-8': 0.6, '9-12': 0.704, '13+': 0.828}; knob 0.25 | empty bars 0.032 (CoCoPops 0.468, BiMMuDa 0.506); 378's slot share {'6-8': 0.6, '9-12': 0.714, '13+': 0.828}; knob 0.25 | printed | no kept rate |

## Findings (550–)

### 550. Dense lines in two-bar slots pass 527 line by line, and the song still reads far from the kept songs.

**Problem:** Every line's slot is one that kept lines of its syllable count take (14 syllables in two bars: 37%; 15: 27%; 16 and over: 10%), so 527 flagged nothing. But four such lines in a row leave the verse with no rests and a stream far more even than kept songs. 527 reads a line, never its section.

**Evidence** (Window 147, song 47's first verse and chorus; main / control; kept: Billboard, Rolling Stone):

| Measure | Kept | Song 47 |
|---|---|---|
| Empty bars | 0.515, 0.736 | 0.033 / 0.030 |
| Gaps equal to the gap before | 0.387, 0.364 | 0.466 / 0.460 |
| Longest run of equal gaps | 4.87, 4.38 | 7.06 / 6.81 |
| Notes a bar | 3.94, 4.14 | 5.65 / 5.62 |
| Most onsets in a beat | 2.63, 2.80 | 3.38 / 3.46 |
| The window's last note on the tonic | 0.28, 0.33 | 0.03 / 0.05 |

- Song 46 (three-bar slots on its long lines): empty bars 0.52, the longest equal-gap run 4.99.

**Fix:** Read 527 by the section as well as the line: the share of a section's lines in slots under the kept median slot for their syllables, against the kept songs' share. Show the writer the section, not only the line.

**Check:** On the next song, every section with three or more lines inside the kept middle half for that share; empty bars in the kept middle half.

### 551. The stream in dense lines (534) is now read, and it is too even and too full of runs.

**Problem:** Song 47 gives 534 its dense windows: 400 first-verse windows at 5.5–9 notes a bar. The stream stays even and the runs stay frequent, with 505's run weight for that band driven to 0.06.

**Evidence** (5.5–9 notes a bar, song 47 alone; kept, main, control):

| Measure | Kept | Main | Control |
|---|---|---|---|
| equal_gap_run_max | 6.17 | 8.48 | 8.20 |
| gap_same_as_before | 0.435 | 0.518 | 0.507 |
| zigzag_of_three | 0.328 | 0.361 | 0.380 |
| Drawable runs (505) | 0.361 | 0.508 | 0.471 |

- 505's run weight at 5.5 and over: 0.057 / 0.082; the run rate still 15 points over the kept.
- At 3.5–4.5 notes a bar the same song reads 5.6 / 5.4 against 4.6.

**Fix:** In a line of more than two syllables a beat, draw the gaps from the kept dense table directly (the table for the band), not by weights on the general table, and cap a run of equal gaps at the kept 95th for the band.

**Check:** At 5.5–9 notes a bar, equal_gap_run_max and gap_same_as_before within the kept middle half; drawable runs within five points of 0.361.

### 552. 542 names the bound: 501 is given up, not 465, and only on dense lines.

**Problem:** Counted apart, the give-ups at half the tries are 501's in nine cases of ten. 501 redraws dense lines tens of thousands of times: a line of 13 or more notes in a two-bar slot sings 2.36–2.73 onsets a beat against the kept 5th–95th of 1.04–2.67.

**Evidence** (main / control):

- Given up at half the tries: 501 alone 719 / 689; 465 alone 75 / 59; both 1 / 0; neither 0 / 1.
- 501 redrawn 21,668 / 20,684 (song 46: 1,357 / 1,664). Inside 7,442 / 7,553.
- Onsets a beat (25th, 50th, 75th), 13 and over notes: 2.36, 2.55, 2.73 (kept 1.33, 1.59, 2.00).

**Fix:** Read 501 on the line's span as drawn (378) and the slot together: a line whose syllables cannot fit the kept rate in its slot is read against the rate its slot allows, and counted as such, not redrawn.

**Check:** 501 given up under one line in twenty on a song with dense lines, its redraws within twice song 46's.

### 553. 541 steps the right way but ends short: three rounds of steps, then the calibration stops.

**Problem:** The gap kept its sign for three rounds and the knob fell from 1.0 to 0.28 (×0.775, ×0.6, ×0.6). The calibration ends at six rounds, and the first three were inside two points on the few builds read, so they took no step.

**Evidence:**

| Draw | Verse 1 / verse 2, chord tones on the beat (engine's window) | Paired test, song 47 (of 27) |
|---|---|---|
| Main | 0.683 / 0.710 | 17 |
| Control | 0.760 / 0.754 | 19 |

- The rounds (main): 0.481 / 0.492, 0.575 / 0.580, 0.686 / 0.705 (no step); 0.722 / 0.772 (×0.775); 0.719 / 0.771 (×0.6); 0.733 / 0.765 (×0.6).
- Window 147's reading of the pair (40, 42, 43, 46, 47 pooled): verse 1 / verse 2 0.681 / 0.699 (main), and 22 of 27 under 0.15.

**Fix:** Let the calibration run past six rounds while 503's gap is over two points and its knob is still stepping, up to ten.

**Check:** Verse 2 within two points of verse 1 on both draws; the paired test at 20 of 27 on both.

### 554. 526: the judge that has not seen the song reads it as it reads the others; a judge fitted on its builds tells it apart almost perfectly.

**Problem:** None; a reading, and a caution about it. Fitted on songs 40–46 and tested on song 47's builds, the judge separates them about as well as it separates song 43 or song 46 from the kept songs. Fitted on song 47's own builds, the agreed-30 judge separates them better than any earlier song's: the unseen judge measures the earlier songs' faults, and song 47's are new ones.

**Evidence** (AUC against the held-out kept half; eight splits, mean and spread; main / control):

| Song | Judge that has not seen it (37 measures, C = 0.3) | Within the song (agreed 30, its own builds) |
|---|---|---|
| 47 | 0.729 ± 0.027 / 0.709 ± 0.040 | 0.942 / 0.948 |
| 40 | 0.785 / 0.797 | 0.870 / 0.867 |
| 42 | 0.787 / 0.825 | 0.886 / 0.884 |
| 43 | 0.719 / 0.770 | 0.845 / 0.862 |
| 44 | 0.868 / 0.925 | — |
| 45 | 0.867 / 0.910 | — |
| 46 | 0.739 / 0.790 | 0.824 / 0.847 |

- The standing judge (v129): content mean −0.39 / −0.52; under −0.72, 36% / 42% (song 46: 38% / 39%).
- Within song 47, pitch separates at 0.853 / 0.856 and rhythm at 0.836 / 0.842 (song 46: 0.759, 0.560).
- Table EN's figures for songs 40–46 (the other AI's reading): 0.75, 0.79, 0.71, 0.86, 0.88, 0.73. This session's are within 0.04.

**Fix:** None. Print both readings for each new song: the unseen judge's, and the within-song separation, with the families.

**Check:** Printed.

### 555. A designed line on a slot's downbeat after a copied line dies when the copy's source ended late.

**Problem:** The second bridge's sixth line ("But You do") is designed to begin on its slot's downbeat. The line before it is a copy of the first bridge's fifth line, which was drawn to end before a fresh line, not before a fixed one. Where the source ran late, there is no breath, and the build dies.

**Evidence:**

- Join deaths before a line: 113 / 97 (song 46: 0 / 0).
- The bridge's design gate: 90.1% pass (317's nine in ten held, by 0.1 point); its deaths 84 / 97.
- The hook's design gate: 100% / 100%.

**Fix:** When a designed line follows a copy, give the copy's source the designed line's entry as its own next line's (247's prefit) when the source is drawn.

**Check:** No join deaths before a designed line; the design gate's pass rate over nine in ten by more than a spread.

### 556. 525 makes the classes reachable, and the short and middle lines still miss class 0.

**Problem:** With the kept shares for two-bar slots (zeneng_v131_kept_slots.json), no class the kept lines never take is drawn, but class 0 is drawn far under its kept share at every length: 0–6% for 3–12 notes against the kept 11–42%, and 31% for 13 and over against 52%. Class 0 needs the next line to begin in the bar where this one ends, which here means a pickup into it, and the next line is often a copy or a design that cannot take one.

**Evidence** (classes 0 / 1 / 2 / 3, main; kept, 525, by notes and two-bar slot):

| Notes | Lines | Drawn | Kept |
|---|---|---|---|
| 3–5 | 2,400 | 0.000 / 0.694 / 0.306 / 0 | 0.110 / 0.700 / 0.189 / 0 |
| 6–8 | 6,348 | 0.055 / 0.886 / 0.059 / 0 | 0.170 / 0.766 / 0.064 / 0 |
| 9–12 | 2,446 | 0.056 / 0.941 / 0.002 / 0 | 0.419 / 0.571 / 0.010 / 0 |
| 13 and over | 2,406 | 0.310 / 0.690 / 0 / 0 | 0.517 / 0.483 / 0 / 0 |

- Out of reach, by slot (main): Chorus line 3, class 2, 863; Bridge line 5, class 2, 516; Bridge line 3, class 0, 446; verse 1's first three lines, classes 0–1, 282 each.

**Fix:** Count, for each line, whether the line after it can take a pickup (a fresh line can; a copy or design whose entry is on or after its downbeat cannot), and draw class 0 only where it can, from the kept share renormalized over what is reachable.

**Check:** Each class within ten points of the kept share among the lines whose next line can take a pickup.


## For the song after this one

- What song 47 leaves open: 527 read by the section (550), the stream drawn from the dense table (551), 501 read against the slot's rate (552), 541's calibration given room to finish (553), the join after a copy before a designed line (555), and class 0 drawn only where a pickup can be taken (556). 554 is a reading: print both separations for every new song.

## Regression line

Songs 40–46 are closed (523). Their orders of record, main / control, each reproduced by the rerun in this session (above):

| Song | Main / control |
|---|---|
| 40 | d508b254a8f4 / 04342d35cd1d |
| 42 | 9fd23492dad3 / 529bf7a1c186 |
| 43 | af58ce3be702 / a095303f51b7 |
| 44 | 2f43a0bc93d6 / 7d4dd7b83e26 |
| 45 | 6dc6710923f0 / 9a1c46f67b24 |
| 46 | 120253ea25cb / 635084318e00 |
| 47 (new) | f363d4e78346 / 7fba0ac398c0 |

- Song 47's runs were each made twice and reproduce.

## Blind-pick tally

The tally stands at 28 songs: Annotated top 11, Remembered top 8, Middle 8, Refrain 1. Songs 40, 41, 43, 44, 45, 46 and 47 have not yet been offered. Song 47's three slots: Remembered, "'Cause the singer doesn't stop"; middle (top quartile under both), "Every scar and every stumble"; Annotated, "Not a copy, not a cover".
