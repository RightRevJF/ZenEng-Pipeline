# A line sung again mends its own run; then the third held-out lyric: result (28 Nov 2026). Step A: all four seen lyrics meet every mark. STEP B: THE HELD-OUT LYRIC MEETS EVERY MARK. Not built.

00:40 ET. Rule: PREDICTION_again_runs.md (commit 0b92d08, before any code or run). Switch `LUTHIER_AGAIN_RUNS=1`, unset by default. Figures, and what is met and missed, printed from held_out_3_6_8.json by the command that wrote this file; every record carries its switches and a judge that ran. Byte for byte with every switch unset: 54, 55, 52, song 53's Essen arm.

## Step A: the four seen lyrics (pick; living median)
| | Song 52 | Song 61's words | Song 50's words | Song 49's words | The mark |
|---|---|---|---|---|---|
| Living; pool | 906; 212 | 742; 371 | 702; 273 | 656; 226 | 30; 10 |
| Sung bars | 101 | 83 | 91 | 92 |  |
| Notes a bar (pick; median) | 4.149; 4.158 | 3.855; 3.843 | 4.077; 4.099 | 3.772; 3.75 | 3.60 to 4.33 |
| Onsets on the beat | 0.453; 0.451 | 0.456; 0.443 | 0.437; 0.448 | 0.49; 0.492 | 0.389 |
| Onsets on the first beat | 0.236; 0.235 | 0.253; 0.248 | 0.235; 0.237 | 0.256; 0.257 | 0.211 |
| 731 | 0.608 | 0.524 | 0.55 | 0.629 | 0.40 |
| Deaths on 780; 840, in ten | 0.0; 0.0 | 0.0; 0.09 | 0.0; 0.84 | 0.0; 0.63 | under one |
| In the voice; a leap | yes; none | yes; none | yes; none | yes; none |  |
| Title lines on time (lowest) | 100.0 | 100.0 | 100.0 | 92.5 | 75 |
| Silence before a title line (longest), eighths | 2.0 | 2.0 | 2.0 | 2.0 | 3 |
| "Again" drawn fresh, share (300 builds) | 0.0 (0 of 4500) | 0.0153 (69 of 4500) | 0.0 (0 of 2400) | 0.0009 (3 of 3300) | 0.076 |
| Never made, of 600 | 0 | 0 | 0 | 0 |  |
| Lines beginning after their bar line | 0.067 | 0.026 | 0.037 | 0.034 | Essen 0.081 |
|  | **every mark met** | **every mark met** | **every mark met** | **every mark met** |  |

- Watched, not a mark: 840 in ten was 0, 0.07, 0.68 and 0.67 before this form; it is 0.0, 0.09, 0.84 and 0.63 now.

## Step B: song 58's words, "Same Time Tomorrow", set in 6/8. Held out; read once.
| | Song 58's words | The mark |
|---|---|---|
| Living; pool | 759; 156 | 30; 10 |
| Sung bars | 114 |  |
| Notes a bar (pick; median) | 4.061; 4.035 | 3.60 to 4.33 |
| Onsets on the beat | 0.425; 0.487 | 0.389 |
| Onsets on the first beat | 0.218; 0.243 | 0.211 |
| 731 | 0.637 | 0.40 |
| Deaths on 780; 840, in ten | 0.0; 0.4 | under one |
| In the voice; a leap | yes; none |  |
| Title lines on time (lowest) | 94.9 | 75 |
| Silence before a title line (longest), eighths | 2.0 | 3 |
| "Again" drawn fresh, share (300 builds) | 0.0001 (1 of 6900) | 0.076 |
| Never made, of 600 | 0 |  |
| Lines beginning after their bar line | 0.028 | Essen 0.081 |
|  | **every mark met** |  |

- Its share limit: its own run without 749.240, 749.241 and the run mend gave {"record": "made", "living": 789, "tries": 6900, "drawn_fresh": 291, "share": 0.0422}; the limit is the higher of 0.076 and 1.5 times that share.
- Its plan: title room null; pickup room null; 749.243 moved null.
- Title lines on time, in 100: {"Chorus 1:0": 94.9, "Chorus 1:6": 94.9, "Chorus 2:0": 94.9, "Chorus 2:6": 94.9, "Last Chorus:0": 94.9, "Last Chorus:8": 94.9}; silence before, eighths: {"Chorus 1:0": 2.0, "Chorus 1:6": 2.0, "Chorus 2:0": 2.0, "Chorus 2:6": 2.0, "Last Chorus:0": 2.0, "Last Chorus:8": 2.0}; deaths on 840 in ten (1,000 builds from the fitted spec): 0.4.

## Plainly
- **Step A:** the share of marked lines drawn fresh fell to 0.0, 0.0153, 0.0 and 0.0009; song 61's words, which missed at 0.0969, are met. Every other mark held on all four.
- **Step B: a lyric none of this work had seen, set in 6/8 and read once, meets every mark:** living builds and pool, notes a bar, onsets on the beat and on the first beat, 731, no death on 780 and 840 under one in ten, in the voice, no leap, every title line on time, the silence before the title 2 eighths, one marked line in 6,900 tries drawn fresh, nothing never made. Switches carried: {"table": "../../studies/other_metres/trial_tables/6-8_folk_sung", "title_entry_pickup": null, "title_840": true, "again_inside": true, "again_refit": 2, "kept_rests_rate": 0.1405, "no_pickup_windows": true}; the judge ran: True.
- **The nearest it comes to a mark:** onsets on the first beat on the pick, 0.218 against 0.211 (the living median is 0.243); title lines on time at their lowest 94.9 in 100; 840 at 0.4 in ten.

## What this is and is not
- **It is** the first time the 6/8 folk package has met every mark on unseen words. Three held-out lyrics were read once each tonight: the first missed one mark, the second two others, the third none. Each miss was counted, a form written before its run, and the seen lyrics read again before the next unseen one.
- **It is not** proof that 6/8 works. All five lyrics were written for 4/4 and set in 6/8; one held-out pass is one lyric; and 840 has crept back from none toward its limit on two seen lyrics (0.84 and 0.63 in ten) since the title's room was retired. The test that counts is song 69, written for 6/8 and banked. Whether it runs is the songwriting session's to put to the writer.
- There are no more unseen spent folk lyrics. Song 58's words are seen now.
- Nothing is built. Every switch is unset by default.

## My expectation
The share under 0.03 on all four: met. All four passing, two chances in three: met. Song 58's words passing, one chance in two: met.
