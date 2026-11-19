# When is the engine sound?

A fixed set of 23 checks, read the same way on each kept 4/4 song (CoCoPops Billboard, 160 songs, tie starts read) and on each of the three 4/4 records (songs 55, 54, 58). `python3 studies/soundness/soundness.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json` writes `soundness.json`. The set does not change between versions. Once the engine passes it, later findings are improvements, not faults.

## Why the test is a lean, not every check in the middle half

A kept song sits outside its own kept middle half on about half the checks: 10 of 21 at the median (quartiles 8 to 13). Only about 2 kept songs in 100 have no more than four checks outside the middle half and none outside the 10th to 90th. A rule asking each song for every check in the middle half would fail nearly every real song.

What marks an engine fault is a lean: all three songs beyond the same kept bound on the same check. One song outside is that song; three on the same side is the engine.

**The rule.** The engine is sound when:
1. no check has all three songs beyond the kept 10th, or all three beyond the kept 90th; and
2. no more than two checks have all three songs beyond the kept 25th, or all three beyond the kept 75th.

Drawn at random 20,000 times, three kept songs fail this rule 6.8 times in 100. Rule 1 alone catches 2.5 in 100; rule 2 alone, 5.2. So it is a bar kept songs clear about 93 times in 100.

## The checks

Kept 10th / 25th / median / 75th / 90th by song. Then each song under v28, marked: **in** the middle half, *near* (between the 25th and 10th or the 75th and 90th), or **out**.

| # | Check | Kept 10 / 25 / 50 / 75 / 90 | 55 | 54 | 58 |
|---|---|---|---|---|---|
| 1 | stressed syllables on a beat | 0.35 / 0.446 / 0.542 / 0.661 / 0.76 | 0.545 in | 0.504 in | 0.597 in |
| 2 | the words' fit, whole | 0.152 / 0.248 / 0.318 / 0.402 / 0.446 | 0.352 in | 0.249 in | 0.320 in |
| 3 | fit by length | 0.041 / 0.118 / 0.209 / 0.297 / 0.369 | 0.387 **out** | 0.177 in | 0.218 in |
| 4 | fit by place | 0.008 / 0.115 / 0.242 / 0.333 / 0.412 | 0.150 in | 0.129 in | 0.291 in |
| 5 | fit by height | −0.042 / 0.045 / 0.106 / 0.178 / 0.243 | 0.081 in | 0.109 in | 0.171 in |
| 6 | onsets on the beat | 0.286 / 0.382 / 0.451 / 0.525 / 0.596 | 0.434 in | 0.431 in | 0.412 in |
| 7 | onsets on the bar's first beat | 0.069 / 0.093 / 0.124 / 0.161 / 0.199 | 0.113 in | 0.125 in | 0.124 in |
| 8 | notes a bar | 3.15 / 3.59 / 4.30 / 5.00 / 6.01 | 4.12 in | 4.45 in | 4.47 in |
| 9 | distinct rhythms over bars | 0.227 / 0.313 / 0.405 / 0.546 / 0.696 | 0.511 in | 0.487 in | 0.676 *near* |
| 10 | bars on a rhythm already sung | 0.304 / 0.454 / 0.595 / 0.687 / 0.773 | 0.489 in | 0.513 in | 0.324 *near* |
| 11 | rhythm scaling | 0.574 / 0.608 / 0.656 / 0.721 / 0.770 | 0.546 **out** | 0.547 **out** | 0.532 **out** |
| 12 | moves by step | 0.265 / 0.329 / 0.396 / 0.489 / 0.558 | 0.459 in | 0.412 in | 0.457 in |
| 13 | moves by leap | 0.044 / 0.073 / 0.102 / 0.140 / 0.182 | 0.070 *near* | 0.151 *near* | 0.105 in |
| 14 | repeated notes | 0.157 / 0.210 / 0.312 / 0.392 / 0.469 | 0.281 in | 0.289 in | 0.284 in |
| 15 | range, semitones | 12 / 14 / 17 / 21 / 26 | 13 *near* | 15 in | 18 in |
| 16 | bars on a figure already sung | 0.199 / 0.344 / 0.474 / 0.579 / 0.664 | 0.356 in | 0.407 in | 0.257 *near* |
| 17 | pitch scaling | 0.667 / 0.792 / 0.905 / 1.023 / 1.107 | 1.003 in | 1.091 *near* | 1.200 **out** |
| 18 | silences of a beat or more, per 100 beats | 5.3 / 7.1 / 8.6 / 10.4 / 13.2 | 8.6 in | 9.9 in | 9.7 in |
| 19 | longest phrase, beats (a breath at half a beat) | 6.5 / 8 / 12 / 15.5 / 20 | 17.0 *near* | 10.5 in | 10.0 in |
| 20 | lines run on (under a beat of rest), share | 0.037 / 0.095 / 0.253 / 0.426 / 0.554 | 0.382 in | 0.193 in | 0.250 in |
| 21 | stressed line ends held a half note or more, share | 0 / 0.075 / 0.231 / 0.523 / 0.724 | 0.359 in | 0.273 in | 0.105 in |
| 22 | the chorus's median over the verse's, semitones (kept lifts, `register_plan.json`) | −3 / 0 / 1 / 4 / 5.3 | 5 *near* | 8 **out** | 8 **out** |
| 23 | rest share inside sung sections (`register_plan.json`) | 0.09 / 0.15 / 0.22 / 0.32 / 0.42 | 0.23 in | 0.211 in | 0.293 in |

Checks 1 to 21 are read on every kept song, so they enter the random draws. Checks 22 and 23 are read against the kept percentiles that `register_plan.json` holds.

Every reading is taken on the notes as sung, melismas included, as the kept songs are read. That is why onsets on the beat and the scalings differ a little from the engine's own readings of the pick.

## Where v28 stands

- **Rule 1: not met, on one check.** Rhythm scaling is under the kept 10th in all three songs (749.93).
- **Rule 2: met.** Two checks lean beyond the middle half: rhythm scaling, low, and the chorus's lift, high (5, 8, 8 against a kept 75th of 4). Pitch scaling follows the lift as it does in kept songs; kept songs with a lift of 8 or more have a median pitch scaling of 1.115.

One fix from sound. When 749.93 is closed and the rule holds on a rerun of all three songs, the engine is sound by this standard. Later findings would then be improvements: variety, taste, the paper's own aims.

Song by song, the three sit nearer the kept middle than kept songs do. Across the 21 checks read on kept songs, 13 song-checks fall outside the middle half; three kept songs drawn at random have about 30 (5th percentile about 21). That is not a fault under this rule. It is the first improvement to make (749.94).

## What is left out, and why

- **Length** is the lyric's (songs 54 and 58 run past the kept 75th of 243 seconds because their lyrics are long). The engine flags it.
- **Melisma share** is drawn from the kept quartiles by construction.
- **Harmony and band** have no per-song kept rows in the repo. Their checks stay in the band report.
- **The title's stressed syllables on a beat** (kept 0.73) is pooled, not by song.
