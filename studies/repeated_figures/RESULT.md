# Where kept tunes sing a figure again (the study for 749.104)

Asked by the songwriting session before any fix: where do kept tunes' repeated four-interval figures sit?

`where.py` reads, for every figure a tune has already sung, how far back its last singing was. `pool.py` reads the same on a hundred tries at each song's builds.

| | Kept 4/4 tunes (25th, middle, 75th) | Song 55 builds | Song 54 builds | Song 58 builds |
|---|---|---|---|---|
| Repeats from within two bars | 0.06, 0.13, 0.23 | 0.02 | 0.03 | 0.15 |
| From two to eight bars back | 0.16, 0.27, 0.36 | 0.19 | 0.14 | 0.27 |
| From eight to sixteen | 0.07, 0.12, 0.19 | 0.04 | 0.04 | 0.09 |
| From over sixteen bars back | 0.29, 0.39, 0.53 | 0.74 | 0.77 | 0.45 |
| Middle distance back, bars | 8, 12, 18 | 33 | 28 | 13 |

**Finding.** Songs 55 and 54 repeat figures about as often as kept tunes do, but from far back: their repeats are whole sections come round again. The near answer, a figure sung again within a bar or two and again inside its section, is what is missing. Song 58, which aims at a kept song that repeats much, stands with the kept tunes.

**A caution.** One pick can mislead: the three picks' repeats sit exactly 1, 2, 4 or 8 bars back at 0.14, 0.21 and 0.16, inside the kept middle half (0.12 to 0.33), while their pools do not.

**Not built.** The fix this points to (fit a section's later lines to its earlier ones at near distances, splitting and merging notes for the new words) has not been tried outside the engine.
