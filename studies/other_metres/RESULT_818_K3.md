# Two counts: 818 on the 6/8 title line, and whether pop K3 can be reached. Result

27 November 2026, 17:49 ET. Rule: PREDICTION_818_K3.md (committed first, 5b0fe49). Figures printed from counts_818_K3.json by the command that wrote this file. The engine's only change is a per-line record of how a line was made; songs 54, 55, 52 and 53 written through afterwards are the same bytes as before.

## Count 1: 818 is the cause (song 52, 993 builds made of 1,000)
| How the chorus title line was made | Builds | On time, in 100 | Died on 840 |
|---|---|---|---|
| 818 again | 704 | 16.9 | 107 |
| 818 rhythm | 103 | 15.5 | 15 |
| fresh | 186 | 100.0 | 0 |

- Made by 818: 807 builds, on time 16.7 in 100. Not made by 818: 186 builds, on time 100.0 in 100.
- Difference: **83.3 points** (the rule asked 20). Every 840 death is a build where 818 made the line.
- **By the rule, the next form is: a title line is drawn fresh; 818 does not apply to it.** Marks U1 to U4 unchanged. My expectation (separates) held.

## Count 2: K3 can be reached on song 55's lines; the draw's ordering is what misses it
- Stressed syllables: 187 over 56 lines.
- (a) Upper bound, ignoring window counts: **0.743**.
- (b) Best within the kept windows the draw may offer: **0.674** (lines with no kept window: 0).
- The draw's living median: 0.241. The mark: 0.45.
- **By the rule: (a) and (b) clear 0.45 and the draw does not, so the cause is the ordering (window count before stress), and the form is the weight from data (749.236).** The lyric is not the reason; lines written for three are not needed for this mark. My expectation held.
- A caution on (b): it is the best single window per line, taken freely. A real song cannot take every line's best at once (copies, joins, the gates), so 0.674 is a ceiling of the draw's space, not a promise.

## The builds never made: 127 of 300
| Line | Syllables | Slot bars | Sung bars | How | Builds of 300 |
|---|---|---|---|---|---|
| Verse 1:7 | 9 | 4 | 3 | fresh | 102 |
| Verse 1:6 | 9 | 2 | 2 | fresh | 23 |
| Verse 3:7 | 6 | 4 | 3 | again | 1 |
| Verse 2:6 | 6 | 2 | 2 | again | 1 |

All are "the syllables cannot fit the window". One line carries most of it: Verse 1's eighth line, nine syllables planned into three sung bars. Its neighbour (nine syllables in two bars) carries most of the rest. That is a planning fault on dense lines, separate from K3, and a candidate of its own: a line whose syllables have few or no kept windows at its planned bars takes a bar more.
