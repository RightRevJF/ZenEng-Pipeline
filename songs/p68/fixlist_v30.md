# Luthier list for v30 (since v29)

19 November 2026. Luthier v29 (fixes 916–917) is reviewed (`lib/luthier/REVIEW_stage16.md`) and merged into main at c365a48. Every record reproduces, and `soundness.py` reproduces its report: sound by the adopted rule, with rhythm scaling (low) and pitch scaling (high) as the two allowed leans. Song 58 is rebuilt from its v29 record (seventh edition, C, a two-bar turn after chorus 1; 44 of 44 document checks pass). Four items, 749.94 to 749.97; one carried (749.61). Next finding 749.98; next fix 918.

## The margin: does a pass by 0.003 hold?

No, and I would not fix it with a margin on the reading. The pick is in effect one draw from each song's gated pool.

- Read on the pools (`studies/soundness/margin.py`, which reproduces the three picks), rhythm scaling sits under the kept 10th in 80, 59 and 94 of 100 pool builds (songs 55, 54, 58). A fresh draw of the three leans past the bound 44 times in 100; three kept songs lean that way on a given check once in 1,000.
- The bound itself is only known to about ±0.014 (bootstrap 0.560 to 0.588).

What I want instead is the same rule read on the pools (749.96): a pick drawn at random from each song's pool passes at least 90 times in 100 (three kept songs: 93). By that reading v29 is not yet sound. Four-bar turns (749.95) take rhythm scaling's lean to 1 in 1,000, and the pools to 87 passes in 100; the rest is repetition (749.97). So 749.95 to 749.97 bear on soundness. 749.94 is an improvement, first as asked.

## Items

### 749.94 The builds sit near the kept middle; choosing differently does not widen them
**Problem.** The three songs are more alike the median kept song than kept songs are to one another. The cause is in the builds themselves, not in how the pick is chosen from them.
**Evidence.** `studies/soundness/neighbour.py`, with four-bar turns, on the 21 kept-read checks. Song-checks outside the kept middle half across the three songs, for a pick drawn at random:

| Drawn from | Median (5th to 95th) |
|---|---|
| every build that lived | 20 (15 to 25) |
| the engine's pool | 17 (12 to 22) |
| the pool build nearest a randomly drawn kept song | 16 (9 to 21) |
| three kept songs drawn at random | about 30 (5th percentile about 21) |

The gates take off about three. The rest of the narrowness is in what the builds aim at: the plan aims every song at the kept medians (registers, notes a bar, the windows' scores).
**Fix.** Aim each song at a kept song, not at the kept middle. Draw one kept song at random from the title's seed, as 838 draws the lift. Take its readings (notes a bar, range, step and leap shares, repeated notes, repetition of bars) as the song's targets, in place of the kept medians the builds now steer toward. Keep every gate as it is.
**Check.** A pick drawn at random from each song's pool has at least 21 song-checks outside the middle half across the three songs, at the median, and still passes the rule at least 90 times in 100.

### 749.95 Turns of four bars, as kept songs leave them
**Problem.** 916 keeps the turns but makes them two bars whenever a song runs long. A two-bar silence rarely empties a whole four-bar stretch, and empty four-bar stretches are what rhythm scaling follows in kept songs. So rhythm scaling stays on the kept 10th.
**Evidence.** With every turn four bars, the pools' median rhythm scaling goes from 0.560 / 0.570 / 0.539 to 0.607 / 0.593 / 0.581, and the share under the kept 10th from 0.80 / 0.59 / 0.94 to 0.02 / 0.19 / 0.35 (`margin_turns_of_four.json`). The chance of a lean falls from 0.44 to 0.001. Kept turns are four bars 38 times in 100 (877's own draw).
**Fix.** Draw each turn at the kept split (two bars 62 in 100, four bars 38 in 100) whatever the length, with at least one four-bar turn in a song that has a turn. Let the bars in and out give way first, as 916 does. Each four-bar turn adds about 6 seconds at ♩ = 84.
**Check.** In each song's pool, the share of rhythm scaling under the kept 10th is at or under 0.37, so three fresh draws lean under 5 times in 100.

### 749.96 Read the soundness rule on the pools
**Problem.** The rule judges one draw, and the draw is the first build in order. A pass or a fail by a few thousandths says little about the engine.
**Evidence.** Above: a 0.003 pass on rhythm scaling that a fresh draw undoes 44 times in 100.
**Fix.** `soundness.py` keeps its single-pick report, and adds the pool reading from `neighbour.py`. **Sound** when the single picks pass, and a pick drawn at random from each song's gated pool passes at least 90 times in 100. The amendment is set out at the end of `studies/soundness/SOUNDNESS.md`.
**Check.** `soundness.py` prints both readings, and both are met.

### 749.97 The songs repeat their bar figures less than kept songs do
**Problem.** With four-bar turns, the most common lean left in the pools is repetition. Too few bars repeat a figure already sung (the rhythm with its intervals), and to a lesser degree a rhythm already sung. This is the side 912 opened by drawing from every kept rhythm.
**Evidence.** Random picks from the pools lean past the middle half on:
- bars on a figure already sung, low: 0.27;
- distinct rhythms over bars, high: 0.14;
- bars on a rhythm already sung, low: 0.14;
- pitch scaling, high: 0.15 (with rhythm scaling at 0.39 before 749.95's draw).

The first picks lean on all three repetition checks. Song 58 is past the kept bounds on two (bars on a rhythm already sung 0.299 against the 10th 0.304; distinct rhythms 0.701 against the 90th 0.696). Rhythm borrowing alone (818 at 0.2) cuts the rhythm leans to 0.07 but raises the figure lean to 0.45, because a borrowed rhythm with new pitches is a repeated rhythm and a fresh figure.
**Fix.** Raise 818's figure borrow, which repeats an earlier line's notes, not only its rhythm, until the builds' bars on a figure already sung meet the kept median (0.474). Check that 839's varied returns do not undo it.
**Check.** In the pools, no repetition check leans past the middle half more than 10 times in 100, and the pools pass the rule at least 90 times in 100.

## Carried
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known, not items
- Song 58 lifts 9 semitones into its chorus (kept 90th 5.3); its title takes the top of any room.
- Songs 54 and 58 run past the kept lengths (the lyrics); four-bar turns add to that.

## Order of work
1. 749.94 (as asked). 2. 749.95. 3. 749.97. 4. 749.96, so the next report reads the pools. 5. 749.61.

## Songs

| Song | Folder | Under v29 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 331 s; key C; a two-bar turn after chorus 1; seventh edition rebuilt from this record |
| 55, Your Yard Man | p65 | 240 s; two-bar turns after choruses 1 and 3 |
| 54, The Man Mama Prayed I'd Be | p64 | 302 s; a two-bar turn after chorus 2 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, the six kept tables, and `studies/soundness/soundness.json`: byte for byte, or the fix says so and commits the new ones.
