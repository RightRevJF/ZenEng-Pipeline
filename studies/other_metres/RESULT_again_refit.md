# A line sung again refitted inside its slot; shared bars in the 6/8 package: result (27 Nov 2026). Song 52 meets every 6/8 mark. Song 61's words are close and still miss. The added mark (712) is missed on all three, and the refit does nothing in pop. Not built.

20:25 ET. Rule: PREDICTION_again_refit.md (commit 5c8c242, before any code or run). Switches `LUTHIER_AGAIN_REFIT=1` with `LUTHIER_AGAIN_INSIDE=1`; `LUTHIER_SHARED_BARS=1` in the 6/8 package. Figures printed from again_refit.json by the command that wrote this file. Byte for byte with every switch unset: 54, 55, 52, song 53's Essen arm.

## 6/8 (pick; living median)
| | Song 52 | | Song 61's words | | The mark |
|---|---|---|---|---|---|
| Living builds; pool | 840; 352 | met | 723; 362 | met | 30; 10 |
| Builds never made, of 600 | 0 | met | 0 | met | reported |
| Notes a bar (pick; living median) | 3.954; 3.898 | met | 3.709; 3.744 | met | 3.60 to 4.33 |
| Onsets on the beat | 0.419; 0.419 | met | 0.392; 0.393 | met | 0.389 or more |
| Onsets on the first beat | 0.222; 0.218 | met | 0.21; 0.185 | **missed** | 0.211 or more |
| 731, median build made | 0.608 | met | 0.524 | met | 0.40 or more |
| Deaths on 780; on 840, in ten | 0.0; 0.0 | met | 0.0; 1.85 | **missed** | under one |
| In the voice; a leap | yes; none | met | yes; none | met |  |
| Title lines on time, in 100 (lowest) | 99.7 | met | 100.0 | met | 75 or more |

- **Song 52 meets every mark of S1 to S7 and U1 to U4, on the pick and on the living median.**
- **Song 61's words:** notes a bar and onsets on the beat are now met (shared bars put the copies in their sources' bars: {"Verse 2:0": [3, 2], "Verse 1:1": [3, 2], "Verse 2:2": [3, 2], "Verse 3:3": [3, 2], "Verse 1:4": [3, 2], "Chorus 1:4": [3, 2]} as [before, after]). First-beat onsets miss (the pick by 0.001, the median by more) and 840 takes 1.85 builds in ten.
- Shared bars on song 52 changed: {"Verse 3:0": [4, 3], "Last Chorus:2": [3, 4]}.
- The silence before a title line, median in eighths: song 52 {"Chorus 1:2": 5.0, "Chorus 2:2": 5.0, "Bridge:2": 4.0}; song 61's words {"Chorus 1:7": 5.0, "Last Chorus:7": 5.0}.

## The added mark: the lyric's "again" drawn fresh (712), over 1,000 builds
| | Before 749.240 | 749.240 | With the refit | The mark (1.5 times) | |
|---|---|---|---|---|---|
| song 52 | 1046 | 1720 | **1695** | 1569 | **missed** |
| song 61's words | 1220 | 6121 | **2584** | 1830 | **missed** |
| pop 3/4 | 564 | 5523 | **5731** | 846 | **missed** |

- Song 61's words: down from 6,121 to 2584; over the mark of 1,830.
- Song 52: hardly moved, and over its mark by a little.
- **Pop: not moved at all.** So in pop the lyric's "again" is not failing for running over. Why it fails is not known and is to be counted next.

## Pop 3/4 (song 55's words)
Living 666, pool 333; builds never made in 300: 0; deaths on 840 in ten 0.72.

| Pick; living median | 749.240 | With the refit | |
|---|---|---|---|
| Notes a bar | 2.655; 2.641 | 2.599; 2.634 | met |
| Onsets on a beat | 0.565; 0.583 | 0.523; 0.582 | met |
| K3: stressed on the first beat | 0.257; 0.321 | 0.332; 0.31 | **missed** |
| K3: stressed off the beat | 0.428; 0.353 | 0.396; 0.337 | **missed** |
| Range | 17; 16.0 | 17; 16.0 | met |
| Pitches | 13; 12.0 | 13; 12.0 | met |
| Commonest pitch | 0.22; 0.27 | 0.36; 0.268 | **missed** |
| K6: rhythm again within sections | 0.3; 0.334 | 0.318; 0.333 | **missed** |
| K6: figure again within sections | 0.136; 0.174 | 0.143; 0.174 | met |

## My expectation
The 712 mark met in pop, two chances in three: **wrong**, it did not move. On song 61's words, near the line either side: it is over. Builds never made stay at none: held. I said I could not call what shared bars would do to notes a bar; it brought song 61's words inside the mark.

## What follows
1. **Count, in pop and on song 61's words, why a line the lyric marks "again" is drawn fresh** (which of the checks turns it away: its start, its end, the join, the span limit). No form before the count.
2. **Count 840 and first-beat onsets on song 61's words** (step 4 as agreed).
3. Step 3 (the density rule may choose one bar) may not be needed: notes a bar on song 61's words is 3.709 with shared bars. I would drop it unless the next lyric shows the lack.
