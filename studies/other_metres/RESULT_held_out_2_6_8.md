# 749.245 and 749.246, then a second held-out lyric: result (27 Nov 2026). Step A: all three seen lyrics meet every mark. STEP B: THE HELD-OUT LYRIC MISSES: notes a bar, 712. Not built.

23:48 ET. Rule: PREDICTION_245_246.md (commit 2011369, before any code or run). Switches `LUTHIER_REST_TABLE=1`, `LUTHIER_PICKUP_WINDOWS=0`, unset by default. Figures, and what is met and missed, printed from held_out_2_6_8.json by the command that wrote this file (read_package.py). Every record read carries the switches meant and a judge that ran. Byte for byte with every switch unset: 54, 55, 52, song 53's Essen arm.

## Step A: the three seen lyrics, both switches on (pick; living median)
| | Song 52 | Song 61's words | Song 50's words | The mark |
|---|---|---|---|---|
| Living; pool | 827; 200 | 798; 399 | 782; 223 | 30; 10 |
| Notes a bar (pick; median) | 3.861; 3.87 | 3.655; 3.667 | 3.856; 3.845 | 3.60 to 4.33 |
| Onsets on the beat | 0.465; 0.466 | 0.475; 0.458 | 0.436; 0.462 | 0.389 |
| Onsets on the first beat | 0.247; 0.251 | 0.267; 0.26 | 0.235; 0.251 | 0.211 |
| 731 | 0.653 | 0.524 | 0.569 | 0.40 |
| Deaths on 780; 840, in ten | 0.0; 0.0 | 0.0; 0.0 | 0.0; 0.0 | under one |
| In the voice; a leap | yes; none | yes; none | yes; none |  |
| Title lines on time (lowest) | 100.0 | 94.9 | 100.0 | 75 |
| Silence before a title line (longest), eighths | 2.0 | 2.0 | 2.0 | 3 |
| 712 | 1063 | 1060 | 416 | 1,569; 1,830; 546 |
| Never made, of 600 | 0 | 0 | 0 |  |
| Lines beginning after their bar line | 0.057 | 0.03 | 0.043 | Essen 0.081 |
|  | **every mark met** | **every mark met** | **every mark met** |  |

Each switch off in turn (pick; living median):

| | |
|---|---|
| song 52, 749.245 off | living 822; pool 264 | notes a bar 3.898; 3.889 | on the beat 0.456; 0.43 | first beat 0.219; 0.22 | 731 0.585 | 840 0.0 | title 100.0 | silence 2.0 | 712 992 (limit 1569.0) | never made 0 | late lines 0.374 | MISSED: nothing |
| song 52, 749.246 off | living 829; pool 179 | notes a bar 3.87; 3.87 | on the beat 0.474; 0.459 | first beat 0.251; 0.245 | 731 0.653 | 840 0.0 | title 99.8 | silence 2.0 | 712 1029 (limit 1569.0) | never made 0 | late lines 0.124 | MISSED: nothing |
| song 61's words, 749.245 off | living 803; pool 402 | notes a bar 3.701; 3.667 | on the beat 0.394; 0.431 | first beat 0.208; 0.234 | 731 0.51 | 840 0.0 | title 96.9 | silence 2.0 | 712 1028 (limit 1830.0) | never made 0 | late lines 0.233 | MISSED: ['onsets on the first beat'] |
| song 61's words, 749.246 off | living 775; pool 388 | notes a bar 3.667; 3.667 | on the beat 0.423; 0.457 | first beat 0.248; 0.259 | 731 0.524 | 840 0.0 | title 95.6 | silence 2.0 | 712 1136 (limit 1830.0) | never made 0 | late lines 0.034 | MISSED: nothing |
| song 50's words, 749.245 off | living 765; pool 199 | notes a bar 3.866; 3.845 | on the beat 0.405; 0.409 | first beat 0.216; 0.209 | 731 0.519 | 840 0.0 | title 100.0 | silence 2.0 | 712 414 (limit 546.0) | never made 0 | late lines 0.365 | MISSED: ['onsets on the first beat'] |
| song 50's words, 749.246 off | living 795; pool 214 | notes a bar 3.856; 3.845 | on the beat 0.436; 0.464 | first beat 0.235; 0.25 | 731 0.575 | 840 0.0 | title 100.0 | silence 2.0 | 712 418 (limit 546.0) | never made 0 | late lines 0.047 | MISSED: nothing |

## Step B: song 49's words, "The World Is Asking", set in 6/8. Held out; read once.
| | Song 49's words | The mark |
|---|---|---|
| Living; pool | 816; 76 | 30; 10 |
| Notes a bar (pick; median) | 3.49; 3.51 | 3.60 to 4.33 |
| Onsets on the beat | 0.421; 0.483 | 0.389 |
| Onsets on the first beat | 0.266; 0.271 | 0.211 |
| 731 | 0.6 | 0.40 |
| Deaths on 780; 840, in ten | 0.0; 0.0 | under one |
| In the voice; a leap | yes; none |  |
| Title lines on time (lowest) | 100.0 | 75 |
| Silence before a title line (longest), eighths | 2.0 | 3 |
| 712 | 327 | 177 |
| Never made, of 600 | 0 |  |
| Lines beginning after their bar line | 0.026 | Essen 0.081 |
|  | **missed:** notes a bar, 712 |  |

- The 712 mark: its own run without 749.240 and 749.241 gave {"record": "made", "living": 307, "again_drawn_fresh_712": 118}.
- Its plan: title room {"Chorus 1:0": [2, 3, 0.989], "Chorus 1:6": [2, 3, 0.991], "Chorus 2:0": [2, 3, 0.989], "Chorus 2:6": [2, 3, 0.991], "Last Chorus:0": [2, 3, 0.989]}; pickup room {"Chorus 1:5": 1, "Chorus 2:5": 1}; 749.243 moved null; shared bars changed {"Last Chorus:6": [2, 3]}.
- Title lines on time, in 100: {"Chorus 1:0": 100.0, "Chorus 1:6": 100.0, "Chorus 2:0": 100.0, "Chorus 2:6": 100.0, "Last Chorus:0": 100.0}; silence before, eighths: {"Chorus 1:0": 2.0, "Chorus 1:6": 2.0, "Chorus 2:0": 2.0, "Chorus 2:6": 2.0, "Last Chorus:0": 2.0}.

## Step A, plainly
- **All three seen lyrics meet every mark** with both switches on, and with room: first-beat onsets 0.235 to 0.267 on the picks and 0.251 to 0.26 on the medians, against 0.211. Lines beginning after their bar line fall from 0.385, 0.222 and 0.378 to 0.057, 0.03 and 0.043; Essen's kept windows are at 0.081.
- **Which switch does it:** with 749.245 off the late lines come back (0.374, 0.233, 0.365) and first-beat onsets miss on song 61's words and song 50's words. With 749.246 off little changes (late lines 0.124, 0.034, 0.047; nothing missed). **870's 4/4 rests were the cause; the pickup-shaped windows a small part of it on song 52.**
- Song 50's words, which missed first-beat onsets as a held-out lyric, now meet every mark. That is on seen ground.

## Step B, plainly: the second held-out lyric misses two marks
- **Met on unseen words:** living builds and pool; onsets on the beat; **onsets on the first beat, 0.266 and 0.271**, the mark that the first held-out lyric missed; 731; no death on 840; the title lines on time in every build; silence 2 eighths; nothing never made; in the voice.
- **Missed: notes a bar, 3.49 on the pick and 3.51 on the living median, against 3.60.** The plan, [syllables, sung bars, syllables a bar] by section: {"Verse 1": [65, 16, 4.062], "Chorus 1": [53, 18, 2.944], "Verse 2": [64, 16, 4.0], "Chorus 2": [53, 18, 2.944], "Bridge": [38, 12, 3.167], "Last Chorus": [52, 18, 2.889]}; the whole song [325, 98, 3.316]. Lines by syllables and bars: {"3 syllables in 2 bars": 1, "5 syllables in 2 bars": 2, "5 syllables in 3 bars": 2, "6 syllables in 3 bars": 4, "7 syllables in 2 bars": 19, "8 syllables in 2 bars": 17, "9 syllables in 2 bars": 1}. The title's room added 5 bars; without them the song would be 3.495 syllables a bar.
- **Missed: the lyric's "again" drawn fresh, 327 against a mark of 177.** Its own count before 749.240 was 118 (and only 307 living builds then, against 816 now), so the mark is 1.5 times a small number.
- By the rule these are misses, and 6/8 folk is not passed on a held-out lyric. Song 49's words are now seen and are not run again tonight under a changed form.

## My expectation
All three seen lyrics passing, one chance in two: met. Late lines under 0.15 and first-beat onsets up 0.02 to 0.04: met. The held-out lyric passing, one in two: missed, on marks I did not name.

## What the misses name (to be counted, not guessed)
1. **Thin choruses.** The verses are at 4.06 and 4.0 syllables a bar, inside the table's middle half. The choruses are at 2.9: their lines are five to eight syllables, and the title's room gives six of them three bars (five and six syllables in three bars is under two a bar). The whole song is 3.32 syllables a bar; without the title room's five bars it would be 3.5, still under 3.60. The plan can make a dense section thinner (749.243) and has no way to make a thin one denser: its fewest bars for a line is two. Candidates, none counted yet: the title's room weighed against the section's density; the density rule allowed one bar for a short line (dropped earlier tonight as not needed); two short lines sharing two bars.
2. **712 on a lyric that repeated well before.** Whether 327 fresh draws in 1,000 builds is a fault or a small number over a smaller one is to be counted: which lines, and what turns them away.
