# Review 29: the verse sung closer, read at the chosen tune

Window 201's fifth check read the builds' middle words' fit. What reaches a singer is the chosen tune, which is gated on the words again. So the three songs were run in full under `LUTHIER_VERSE_CLOSER=apart` (a separate worktree, nothing committed), and form (b), one bar only for lines of 6 or 7 syllables, was read on Window 201's 40 quick tunes a song (`trial.py`, form `apart7`).

## Form (a), "apart", the chosen tunes (1,000 builds a song)

| Song | Range | Words' fit (as built) | Rhythm scaling |
|---|---|---|---|
| 55 | 15 | 0.347 (0.341) | 0.688 |
| 54 | 19 | 0.272 (0.275) | 0.646 |
| 58 | 17 | 0.357 (0.307) | 0.550 |

`soundness.py` on the three: sound, **no lean at all** (as built: rhythm scaling, low); 10 checks outside the middle half (as built 12). Song 58's tune stays under the kept 10th of rhythm scaling (0.574).

## Form (b), "apart7", 40 quick tunes a song

Songs 55 and 58 take the same one-bar lines as (a). Song 54 takes none: every candidate line is 8 or 9 syllables. Its rhythm scaling reads 0.601, under the kept 25th (0.605). By the window's first check (inside the quartiles in two songs of three), (b) would pass in song 55 only.

## Weak syllables held on the top note

`held_weak_top.py`: kept songs' longest weak syllable on the top note, in beats, 50th to 99th: 0.5, 1, 1.5, 1.5, 2. 28 kept songs in 100 hold one a beat or more; 5 hold one two beats or more. Song 58's "the" is a beat (the kept 75th). Song 60's "me" is held four beats, past the kept 99th, but it is "even you, even me", where "me" carries the contrast and is stressed when spoken; the word's tier calls it weak.
