# A line sung again ends inside its own slot: result (27 Nov 2026). Builds are made in both metres. The marks are still missed on song 61's words and in pop 3/4, and song 52's pick now misses one by 0.003. Not built.

19:57 ET. Rule: PREDICTION_again_inside.md (commit b9e3eed, before any code or run). Switch `LUTHIER_AGAIN_INSIDE=1`. Figures printed from again_inside.json by the command that wrote this file. Byte for byte with every switch unset: 54, 55, 52, song 53's Essen arm.

## 6/8
| | Song 52 | | Song 61's words | | The mark |
|---|---|---|---|---|---|
| Living builds; pool | 871; 406 | met | 706; 353 | met | 30; 10 |
| Builds never made, of 600 | 0 | met | 0 | met | reported |
| Notes a bar (pick; living median) | 3.88; 3.898 | met | 3.5; 3.489 | **missed** | 3.60 to 4.33 |
| Onsets on the beat | 0.418; 0.418 | met | 0.373; 0.427 | **missed** | 0.389 or more |
| Onsets on the first beat | 0.208; 0.215 | **missed** | 0.193; 0.206 | **missed** | 0.211 or more |
| 731, median build made | 0.614 | met | 0.573 | met | 0.40 or more |
| Deaths on 780; on 840, in ten | 0.0; 0.0 | met | 0.0; 1.8 | **missed** | under one |
| In the voice; a leap | yes; none | met | yes; none | met |  |
| Title lines on time, in 100 (lowest) | 99.7 | met | 100.0 | met | 75 or more |

- **Builds never made: none of 600 on either lyric** (song 61's words had 572 of 600).
- Song 61's words now give 706 living builds and a pool of 353 (37 and 19 before). Its marks can at last be read on a full set, and four miss: notes a bar, onsets on the beat (pick), onsets on the first beat, and 840.
- Song 52: the pick's first-beat onsets are 0.208 against 0.211; the living median meets it. By the rule (median and pick) that is a miss.
- The silence before a title line, median in eighths: song 52 {"Chorus 1:2": 5.0, "Chorus 2:2": 5.0, "Bridge:2": 4.0}; song 61's words {"Chorus 1:7": 5.0, "Last Chorus:7": 8.0}.

## Pop 3/4 (song 55's words, deduced table)
Living 629 (316 before), pool 315; builds never made in 300: 0 (127 before). Deaths on 840 in ten: 0.79.

| Pick; living median | Before | With the switch | |
|---|---|---|---|
| Notes a bar | 2.606; 2.62 | 2.655; 2.641 | met |
| Onsets on a beat | 0.565; 0.553 | 0.565; 0.583 | met |
| K3: stressed on the first beat (0.45 or more) | 0.246; 0.241 | 0.257; 0.321 | **missed** |
| K3: stressed off the beat (0.26 or under) | 0.348; 0.385 | 0.428; 0.353 | **missed** |
| Range | 17; 16.0 | 17; 16.0 | met |
| Pitches | 13; 11.0 | 13; 12.0 | met |
| Commonest pitch | 0.197; 0.257 | 0.22; 0.27 | met |
| K6: rhythm again within sections | 0.4; 0.36 | 0.3; 0.334 | **missed** |
| K6: figure again within sections | 0.25; 0.19 | 0.136; 0.174 | met |

- K3 moves toward its mark (stressed on the first beat, living median 0.241 to 0.321) and is still missed.
- **K6 is now missed where it was met:** rhythm again within sections fell. That is the cost the rule said to report.

## The cost: lines sung again (counts over 1,000 builds)
| | Living builds | The lyric's "again" drawn fresh (712) | Sung again by 818 |
|---|---|---|---|
| song 52 | 828 to 871 | 1046 to 1720 | 4275 to 3313 |
| song 61's words | 37 to 706 | 1220 to 6121 | 7599 to 7274 |
| pop 3/4 | 316 to 629 | 564 to 5523 | 8136 to 7677 |

On song 61's words and in pop, lines the lyric marks as the same tune are drawn fresh five times as often (song 61's words) and ten times as often (pop), by the counts above. The builds are made, but they repeat less. The proper answer is upstream: a copy that does not fit its slot means the plan gave it different bars from its source, or the source's rhythm does not suit the copy's syllables.

## My expectation
Builds made: held (none never made). I said perhaps a third of "again" lines drawn fresh and the count is higher. Pop K3 stays missed: held. Song 61's words meeting every mark, one chance in three: missed.

## What follows
1. **Keep the limit** (a line sung again may not run over): it is what a fresh line already obeys, and without it nothing is made. Its number is the songwriting session's.
2. **Notes a bar on song 61's words (3.5 against 3.60)** is the plan, not the draw: its notes over its sung bars. The density rule chooses among two, three and four bars; lines of four to seven syllables in two bars are two to three and a half a bar. A candidate: the rule may choose one bar.
3. **The sameness lost** (K6; 712's rise): shared bars (749.234) for the 6/8 package, and a line sung again refitted to its own syllables inside its slot and not dropped.
4. **840 on song 61's words (1.8 in ten)** and first-beat onsets: to be counted, not guessed.
