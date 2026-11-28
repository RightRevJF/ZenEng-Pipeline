# 749.255, 956's ceiling outside 4/4 at the metre's own table: the result

28 November 2026. Rule file first: PREDICTION_255.md (41d1361), with the ceiling printed (0.396 for every part; no section labels). Every figure is printed from RESULT_255.json (before-figures from RESULT_counts_K5_pool.json) by the command that wrote this page. Pop 3/4, song 55's words, arm 2's package with `LUTHIER_CEILING_TABLE=1`, seeds 1, 2, 3, 1,000 builds each; each pool read from inside the planner's own run, each pick equal to its record's.

| (pick; living median) | Seed 1 | Seed 2 | Seed 3 | Wanted |
|---|---|---|---|---|
| K1 living; pool | 591; 236 | 788; 362 | 609; 165 | 30; 10 |
| K2 notes a bar | 2.683; 2.662 | 2.739; 2.718 | 2.585; 2.599 | 2.38 to 3.85 |
| K3 on the first beat | 0.455; 0.46 | 0.439; 0.46 (pick misses) | 0.444; 0.46 (pick misses) | 0.45 or more |
| K3 off the beat | 0.118; 0.134 | 0.139; 0.134 | 0.155; 0.134 | 0.26 or under |
| K4 range | 17; 16.0 | 17; 16.0 | 13; 15.0 | 12 or more |
| K4 pitches | 12; 11.0 | 12; 12.0 | 9; 10.0 | 7 or more |
| K5 commonest pitch | 0.173; 0.278 | 0.226; 0.211 | 0.264; 0.331 **median missed** | 0.303 or under |
| K6 rhythm again within sections | 0.45; 0.4 | 0.4; 0.381 | 0.45; 0.429 | 0.349 to 0.871 |
| K6 figure again within sections | 0.211; 0.2 | 0.25; 0.158 | 0.25; 0.2 | 0.667 or under |
| Builds the ceiling read; passed | 296; 236 | 394; 362 | 305; 165 | |
| The pool's median commonest pitch (before 749.255) | 0.263 (0.274) | 0.207 (0.21) | 0.29 (0.318) | |
| The pool meeting K5, in 100 (before) | 80.9 (72.3) | 98.6 (98.0) | 66.1 (41.0) | |
| Mark 2: the pool on the six like marks, in 100 | 86.9 | 76.2 | 89.7 | 76.2 or more |
| The pool meeting all nine, in 100 (before) | 41.5 (36.5) | 40.6 (40.1) | 38.8 (23.9) | watched |
| The pick meets all nine | yes | no | no | reported |
| Marked lines drawn fresh; source lines' first beat; lines late | 0.0001; 0.527; 0.027 | 0.0001; 0.528; 0.024 | 0.0001; 0.528; 0.025 | 0.076; 0.40; 0.15 |
| Chord mark (source's share); voice; leap | 1.0 (0.942); in; none | 1.0 (0.953); in; none | 1.0 (0.965); in; none | |
| 838's deaths in 1,000 | 409 | 212 | 391 | flag over 450 |

## Plainly
- **Mark 1 is missed at seed 3, and it could not have been met by this form.** K5 on the living median at seed 3 is 0.331, exactly as before. The living builds are read before the judge's gates; a gate changes the pool, not the living builds. I should have said so in the rule file and did not see it until the result. Seeds 1 and 2 meet every mark on the living median.
- **What the gate does do, at seed 3:** it passes over 140 of 305 builds; the pool's median commonest pitch falls from 0.318 to 0.29 (K5's line is 0.303), and the pool meeting K5 rises from 41.0 to 66.1 in 100. The pick at seed 3 now meets K5 (0.264).
- **Mark 2 met** (the pool on the six like marks: 86.9, 76.2, 89.7 against 76.2; seed 2 sits exactly on it). **K1 met** (pools of 236, 362, 165): the gate does not starve the pool.
- **The picks, reported:** seed 1 meets all nine; seeds 2 and 3 miss K3 on the first beat (0.439 and 0.444). The pool meeting all nine is 41.5, 40.6 and 38.8 in 100.
- 838 is 409, 212, 391: unchanged, as it must be (the ceiling acts after it). The five 6/8 lyrics are byte for byte the same with the switch set (all); every unset song byte for byte (all); room files this engine's. The records carry the ceiling ({'Verse': 0.396, 'Chorus': 0.396}) and the judge ran.

## My expectation, against the result
- "Seed 3's median commonest falls only a little and K5 still misses": it misses, but for a reason I had not seen: the living median cannot move at all. The pool's median did fall, further than I said (to 0.29). Right outcome, wrong reasoning.
- Mark 2 and K1 met at every seed: right.
