# Rhythm scaling in the engine (749.138): result

**Not built. The last form passes four checks of five and misses the fifth, the words' fit, in one song by 0.008.** The lever is real and larger than I expected. (`trial_*.json`, 40 quick tunes a song; `studies/soundness/neighbour_v44_trial_verse_closer.json` and `..._apart.json`, a thousand builds a song; the engine as built is `neighbour_v44.json`.)

**The lever.** How busy a stretch is, is the lyric's syllables over the bars the engine gives them. Luthier gave nearly every line of 6 to 8 syllables two bars, in verse and chorus alike, about 3.7 notes a bar. Kept verses run 4.6 notes a bar at the middle and are 1.15 times as busy as their choruses. *Aim, apart* gives some verse lines of 6 to 8 syllables one bar: the shortest first, an even count, no two side by side, as many as bring the verse nearest the kept middle (two to four lines of a verse's eight). The chorus is untouched. The song gets shorter, and in song 55 the planner's own rule then lets the eight-bar break in.

| A thousand builds a song | Song 55 | Song 54 | Song 58 |
|---|---|---|---|
| Rhythm scaling, the builds' middle: as built; aim, apart (kept quartiles 0.605, 0.656, 0.721) | 0.592; **0.678** | 0.576; **0.620** | 0.555; 0.592 |
| Builds that live: as built; aim, apart | 342; 281 | 309; 304 | 419; 405 |
| Words' fit, the builds' middle: as built; aim, apart | 0.265; 0.253 | 0.221; **0.193** | 0.306; 0.320 |
| Verse over chorus, notes a bar (kept 10th to 90th 0.83 to 1.48) | 1.17 | 1.11 | 1.06 |
| Seconds: as built; aim, apart | 244; 240 | 307; 293 | 337; 314 |
| Pool (as `neighbour.py` counts): as built; aim, apart | 39; 22 | 25; 18 | 39; 40 |

The pools: a random pick fails the soundness rule 2.2 times in 100 as built and 0.0 under aim, apart; the neighbour choice 2.0 and 0.0; the three first builds lean on no check (as built: rhythm scaling, low). Pool builds under the kept 25th of rhythm scaling: 88 in 100 as built, 42 under aim, apart (0.883 and 0.425). The pools' spread of rhythm scaling over the kept spread: 0.37 to 0.56.

**The checks, written first.**

1. Rhythm scaling inside the kept quartiles in two of the three songs: **met** (55 and 54; song 58 moves from 0.555 to 0.592 and stays under).
2. At least 7 in 10 as many builds live, in each: **met** (82, 98, 97 in 100).
3. The words' fit down by no more than 0.02, in each: **not met in song 54** (0.221 to 0.193, down 0.028). Songs 55 and 58: down 0.012 and up 0.014.
4. The soundness rule and the pool standard: **met**.
5. The guard, verse over chorus inside the kept 10th to 90th: **met**.

**How it got here, and what I expected.** I expected the kept-share form to move rhythm scaling by 0.01 or 0.02 and fail: it did. I expected the limit (every such line in one bar) to reach the kept 25th in song 55 only: it reached 0.73, 0.67, 0.67, but songs 55 and 54 all but stopped building and the verse ran at twice the chorus, outside anything kept. I expected *aim* to fail on scaling: it passed on scaling (0.676, 0.618, 0.609) and failed on builds (song 58 kept 47 in 100, dying where three one-bar lines stood side by side). *Aim, apart* mends that. I expected it still to fail on builds; it fails on the words' fit of song 54 instead.

**Why song 54's fit falls.** Its verse lines run 7 to 9 syllables. Eight syllables in one bar are eighth notes end to end, with no long note and little choice of beat for the weighty syllables, and those are what the fit rewards. Its builds' fit, 0.193, is under the kept 25th (0.248) and over the kept 10th (0.152).

**What stands.** The switch is in the engine and off (`LUTHIER_VERSE_CLOSER`, for trials only). Song 59, the hold-out, has no verse line of 6 to 8 syllables and is unchanged by every form. Nothing here was fitted to it.

**What is to be decided.** The words' fit check was mine; Review 28's check did not ask it, and by Review 28's check this form passes. I have held to the rule as I wrote it. Two honest ways on: (a) the session rules that a fall of 0.028 in one song's builds, still over the kept 10th and gated again when the tune is chosen, is a fair price for the one lean the engine has left; or (b) a line is given one bar only if it has 7 syllables or fewer, tried next, which will move song 54 less and may not reach the quartiles in two songs.
