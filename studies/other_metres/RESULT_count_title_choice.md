# The title line's one rhythm, against Essen: a count (28 Nov 2026). Ours is well above the table's; the doubled stress pull on a title line is what narrows it. A count; nothing predicted, nothing run.

01:49 ET. Asked by the songwriting session (01:40 ET). count_title_choice.py (600 builds from the last trial's records) and count_title_weights.py (the draw's own formula, read from the code, on the same windows). Figures printed from count_title_choice_*.json and count_title_weights_*.json by the command that wrote this file. Two-bar title lines drawn fresh only (song 52's bridge title line is three bars and is left out of the table's side).

## Ours against the table
For each title line: the kept two-bar windows offered to it (with the engine's pickups) that pass 840's test; the share of the table's own count the commonest of them takes; how many it takes to cover nine tenths; and the same for the rhythms our 600 builds took.

| | Syllables | Passing windows | Table: commonest share | Table: windows to cover 0.9 | Ours: commonest share of builds | Ours: rhythms to cover 0.9 |
|---|---|---|---|---|---|---|
| Song 52, Chorus 1:2 | 7 (5 stressed) | 10 | 0.329 | 6 | 0.548 | 3 |
| Song 61's words, Chorus 1:7 | 7 (3 stressed) | 19 | 0.229 | 11 | 0.545 | 4 |
| Song 50's words, Chorus 1:6 | 7 (5 stressed) | 27 | 0.252 | 10 | 0.863 | 2 |
| Song 49's words, Chorus 1:0 | 6 (2 stressed) | 55 | 0.285 | 19 | 0.907 | 1 |
| Song 49's words, Chorus 1:6 | 5 (2 stressed) | 37 | 0.134 | 22 | 0.677 | 3 |
| Song 58's words, Chorus 1:0 | 5 (4 stressed) | 28 | 0.585 | 11 | 0.925 | 1 |

**Ours is well above Essen's on every title line.** Among windows that pass 840's test, Essen's commonest takes 0.13 to 0.59 of the count and it takes 6 to 22 windows to cover nine tenths; our draw gives one rhythm 0.55 to 0.93 of builds and covers nine tenths with one to four.

## What narrows it: the draw's own weights
A line's kept windows are weighed by their kept count, the entry's share, and a stress score; for a title line the stress score is doubled (840's first form, fix 840: "the title's stresses pulled twice as hard to the beat": 2.8 against a line's 1.4). The commonest window's share among the passing windows under each weighting, worked from the code's formula:

| | By kept count alone | No stress pull (count, entry, the cut to twelve) | A line's ordinary pull (1.4) | As built (2.8) | As built, no cut to twelve | Seen in 600 builds |
|---|---|---|---|---|---|---|
| Song 52, Chorus 1:2 | 0.329 | 0.325 | 0.365 | 0.479 | 0.479 | 0.548 |
| Song 61's words, Chorus 1:7 | 0.229 | 0.242 | 0.555 | 0.569 | 0.569 | 0.545 |
| Song 50's words, Chorus 1:6 | 0.252 | 0.335 | 0.72 | 0.851 | 0.851 | 0.863 |
| Song 49's words, Chorus 1:0 | 0.285 | 0.238 | 0.178 | 0.279 | 0.275 | 0.907 |
| Song 49's words, Chorus 1:6 | 0.134 | 0.239 | 0.339 | 0.364 | 0.364 | 0.677 |
| Song 58's words, Chorus 1:0 | 0.585 | 0.607 | 0.803 | 0.992 | 0.992 | 0.925 |

- **The doubled pull is the cause on four of the six lines:** with it the commonest window takes 0.48 to 0.99; with no pull it takes 0.24 to 0.61, which is the table's own share. The entry's weight and the cut to the twelve best change little.
- The doubled pull was made so that a title line would pass 840. 749.244 and 749.248 now see to that directly: every window offered already passes. The pull is doing the test's work a second time, and the cost is the choice.
- In 6/8 folk the stress score is not from a table (the only stress file tried was borrowed and dropped), so the pull is also not the table's.
- **One line the weights do not explain:** song 49's words, the chorus's first line. The formula gives its commonest window 0.28; the builds give one rhythm 0.91. Something else narrows it (the limits on where it may start and end, most likely, but that is a guess and is to be counted).

## The form that follows (its own rule, before any code)
**749.249, for the songwriting session's word:** a title line drawn among the windows that pass 840's test is weighed as any window is by the table (kept count and the entry), with no stress pull on top: the test has done that work. And the count on song 49's words' first chorus line before it.
