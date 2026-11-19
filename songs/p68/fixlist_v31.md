# Luthier list for v31 (since v30)

19 November 2026. Luthier v30 (fixes 918–921) is reviewed (`lib/luthier/REVIEW_stage17.md`) and merged into main at 7b33e96. Every record reproduces; `soundness.py` and `neighbour.py` reproduce their reports. The engine is sound by the amended rule: the pools pass 93 times in 100, and the first picks pass. Song 58 is rebuilt from its v30 record (eighth edition, D major, a four-bar turn; 44 of 44 document checks pass). Everything below is an improvement. Four items, 749.98 to 749.101; 749.94 carried with a sharper diagnosis; 749.61 carried. Next finding 749.102; next fix 922.

## The v30 list against the v30 records

| Item | Fix | Met? |
|---|---|---|
| 749.95 four-bar turns | 918 | yes: rhythm scaling past the kept 10th in 2 pool draws in 100 |
| 749.96 the rule on the pools | 921 | yes: adopted; the pools pass 93 in 100 |
| 749.97 repetition | 919 | in part: copies keep their melismas (all 32 copies match their sources); the builds' figures move toward the kept median. Repetition still leans low in the pools (749.101) |
| 749.94 variety | 920 | no: 19 against 21. Carried, with where it sits (below) |
| 749.61 6/8 | none | carried |

## Where the pools lean

`neighbour.py` now writes, for each check, the share of all pool builds outside the kept middle half, low and high (a kept song: 25 and 25 in 100). The rule catches a lean only when all three songs share it. These are the engine's tendencies underneath:

| Check | Low | High |
|---|---|---|
| rhythm scaling | 0.90 | 0 |
| pitch scaling | 0.02 | 0.78 |
| moves by step | 0.01 | 0.50 |
| moves by leap | 0.49 | 0.06 |
| range | 0.42 | 0 |
| bars on a figure already sung | 0.49 | 0 |
| bars on a rhythm already sung | 0.47 | 0 |
| distinct rhythms over bars | 0 | 0.47 |
| notes a bar (too central) | 0 | 0.01 |
| longest phrase (too central) | 0 | 0.02 |
| stressed line ends held a half note (too central) | 0.06 | 0 |
| onsets on the beat (too central) | 0.06 | 0.03 |

## Items

### 749.98 Draw the lift from the song the aim is drawn from
**Problem.** 920 aims each song at one kept song's moves and range, but the chorus's lift (838, 907) is drawn from all the kept lifts on another seed. The two can contradict each other. Song 58 aims at "Bird Dog" (range 9, no lift), and lifts its chorus 9. Its tops are narrowed toward a range of 9 while its verse and chorus are pushed 9 apart. Each section gets about six semitones, and the two sections don't overlap (verse 60 to 66, chorus 68 to 75, on the written tonic).
**Evidence.** Song 58: steps 0.566 (kept 90th 0.558), leaps 0.033 (10th 0.044), pitch scaling 1.311 (90th 1.107), the chorus 10 semitones over the verse (kept quartiles 0, 1, 4). The aimed songs' own lifts are −2, −4 and 0. The plans' lifts are 4, 6 and 9. In the pools, pitch scaling sits over the kept 75th in 78 builds in 100; across kept songs, pitch scaling rises with the lift (Spearman 0.31; `pitch_scaling_lift.py`).
**Fix.** Take the lift from the aimed kept song: its chorus's median over its verse's, as `pitch_scaling_lift.py` reads it, clamped to the voice's room. Draw from the kept lifts only where that song has no labelled verse and chorus.
**Check.** In the pools, pitch scaling over the kept 75th in no more than 40 builds in 100. Song 58's steps, leaps and pitch scaling inside the kept 10th to 90th.

### 749.99 Let a pitch repeat as kept songs repeat it
**Problem.** The pitch draw never takes a pitch three times running inside a line, and `runs_ok` refuses four. Kept songs often sing a run of five, six, eight on one note. So the longest run is 4 in all three songs, under the kept 25th. A repeat-heavy kept song cannot be reached by the aim.
**Evidence.** Longest run of one pitch: 4 / 4 / 4 (kept 10th, 25th, median, 75th, 90th: 3, 4.75, 6, 8, 10). Repeated notes never fall over the kept 75th in any pool build (high 0.000; low 0.134). Song 58 aimed at 0.373 repeated notes and sang 0.272. The cap dates from the early anti-chant gate; the kept songs set the bound now.
**Fix.** Replace the two fixed caps with the kept distribution. Let a run go on with the kept chance of a run of that length continuing, or cap it at the aimed song's own longest run. Keep the chant check on the pick (a run past the kept 90th, 10) as a gate.
**Check.** In the pools, longest run of one pitch inside the kept middle half in at least half the builds, and repeated notes over the kept 75th in at least 10 builds in 100.

### 749.100 The melody steps more, leaps less and spans less than kept songs
**Problem.** Over the pools, steps are over the kept 75th in half the builds, leaps under the 25th in half, and range under the 25th in four in ten. The aim moves this little: it tilts the moves by at most a factor of 2.5 and recentres the charge's bounds. Choosing the pool build nearest the aim brings some targets closer but narrows the songs overall: a random pick among the ten nearest has a median of 16 song-checks outside the middle half, against 19.
**Evidence.** The pool table above. Aim against pick, song 54: steps 0.595 aimed, 0.463 sung; leaps 0.12 aimed, 0.067 sung. Song 55: range 19 aimed, 14 sung. Each section's register is about a sixth (838's kept medians), and every note is drawn toward its section's centre (`exp(-(p - mu)^2 / 50)`). So a line seldom has room to leap.
**Fix.** Widen the pull toward the section's centre so the builds' range and leap shares meet the kept medians. Fit the width against the pools, as 913 refitted the place weight. Draw each section's register width from the aimed song's range rather than the kept median.
**Check.** In the pools, steps over the kept 75th, leaps under the 25th and range under the 25th each in no more than 35 builds in 100. The rule still holds on the pools.

### 749.101 Repetition still leans low
**Problem.** After 919, bars on a figure already sung and bars on a rhythm already sung are still under the kept 25th in nearly half the pool builds, and distinct rhythms over the 75th in nearly half. Returning lines that are not copies are drawn fresh, and 839 lifts a held note in returns, so each varied return is a new figure.
**Evidence.** Pool shares: figures low 0.49, rhythms low 0.47, distinct rhythms high 0.47. With the aim's repetition switched on (`AIM_REPEATS`), rhythm scaling fell until the first picks leaned (920's own trial). So the repetition has to come back without taking the empty stretches away.
**Fix.** Let 839's varied return apply at the kept share: in kept songs a later chorus is note for note 15 times in 100, and bars the same at a median of 0.57. Other returns come back unvaried. Leave the turns and the four-bar silences as they are.
**Check.** In the pools, each of the three repetition checks outside the kept middle half on its leaning side in no more than 35 builds in 100. Rhythm scaling past the kept 10th in no more than 5 pool draws in 100.

## Carried
- **749.94** The songs sit nearer the kept middle than kept songs (19 song-checks outside the middle half against 21 asked). The pool table shows where: notes a bar, the longest phrase, line-end lengths, onsets on the beat and run-ons almost never leave the kept middle. They are drawn at the kept medians, or fitted to them. Once 749.98 to 749.101 are in, let these be drawn from the aimed song's own readings, as 920 does for the moves.
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known
- The melisma share now falls a little under the share drawn (copies take their sources' melismas), still inside the kept quartiles.
- Songs 54 and 58 run past the kept lengths (the lyrics, and now four-bar turns).

## Order of work
1. 749.98. 2. 749.100. 3. 749.99. 4. 749.101. 5. 749.94. 6. 749.61. Rerun `neighbour.py` after each; the rule must hold throughout.

## Songs

| Song | Folder | Under v30 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 337 s; key D; a four-bar turn after chorus 1; aimed at "Bird Dog"; eighth edition rebuilt from this record |
| 55, Your Yard Man | p65 | aimed at "Don't Ask Me Why" (Billy Joel) |
| 54, The Man Mama Prayed I'd Be | p64 | aimed at "Could I Have This Dance" (Anne Murray) |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, the six kept tables, `studies/soundness/soundness.json`, and the shared fields of `studies/soundness/neighbour.json`: byte for byte, or the fix says so and commits the new ones.
