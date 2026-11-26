# Each line about its own centre, by kept contours: result

26 November 2026. Form and marks in `PREDICTION.md` (committed before any run). The clean reading: `clean.json`. The whole-engine runs were stopped once the clean reading had decided.

**It fails marks 1 and 3. Not built. The form does almost nothing, and that is the finding.**

Each v50 record's fitted spec, only the form changed, a thousand builds:

| | 55 | 54 | 58 | 49 | 50 | 59 |
|---|---|---|---|---|---|---|
| 1. Spread between a verse's lines, v50 → the form (kept middle half 0.86 to 2.38) | 1.30 → 1.22 | 1.01 → 1.14 | 0.82 → **0.83** | 0.72 → **0.64** | 0.69 → 0.91 | 1.10 → 1.19 |
| 2. How a line's height follows the last (kept −0.90 to +0.52) | −0.36 | −0.21 | −0.26 | −0.29 | −0.31 | −0.25 |
| 3. The middle verse's share on its commonest pitch | 0.335 → 0.347 | 0.351 → 0.336 | 0.462 → 0.450 | 0.474 → 0.478 | 0.496 → 0.436 | 0.347 → 0.339 |
| Verses over the ceiling, builds in 100 | 16 → 17 | 15 → 14 | 56 → 55 | 56 → 58 | 65 → 49 | 24 → 19 |
| Living builds | 293 → 272 | 279 → 288 | 366 → 337 | 327 → 312 | 243 → 239 | 320 → 306 |

Mark 1 fails in songs 58 and 49. Mark 3 asked the share lower in five songs of six; it is lower in four. Mark 2 holds, as it would for almost anything.

## What it teaches (749.202)

The kept contours move a line's centre by about two and a half semitones, line to line. The lines themselves move by a tenth of that. **A line's height in the engine is not set by its register's centre.** The pull to the centre is wide (it falls to a third of its strength six or seven semitones away), so a centre moved two semitones is barely felt. What sets where a line sits is where the line before left off, and the interval the draw takes from there.

That points at one place: **the join.** The draw takes a line's first note from the last note of the line before by the same interval table it uses inside a line. The kept table pools the two. But in kept songs they are not alike: I counted them for fix 964, and intervals of an octave or more are 5 in a thousand inside lines and 46 in a thousand at the joins. Kept singers finish a line, breathe, and start the next somewhere else. The engine starts the next line a step from where it stopped.

If that is so, this is the octave bin's kind of fault again (one table read as if it were two things), and it has the octave bin's kind of mend: the join drawn from the kept joins. It is the next reading, its rule written first: `studies/line_joins`.

## Against what I expected

Marks 1 and 3 to hold: both wrong. I took it that a line sits where its register puts it. The doubt I named (the chorus's lift, mark 5) never came to be tested.
