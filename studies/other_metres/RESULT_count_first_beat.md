# Where first-beat onsets are lost in 6/8: a count (27 Nov 2026). Our lines begin after their bar line four to five times as often as Essen's do. A count; nothing predicted, nothing run under a changed form.

23:15 ET. count_first_beat.py and a count of late starts, on 400 builds from each record's fitted spec (the last trial's records: song 50's words held out and now seen; song 52; song 61's words). Figures printed from count_first_beat_50/52/61.json and count_late_starts.json by the command that wrote this file. These counts are on the builds' notes before melismas are added, so the whole-song ratios run a little higher than the marks' figures; the comparisons between groups are what is read.

## The arithmetic
Onsets on the first beat, over all onsets, is the share of sung bars whose first beat carries a note, divided by notes a bar. At 3.85 notes a bar the mark of 0.211 needs a note on the first beat of 81 bars in 100.

## What a line's opening does to it
| | Lines beginning after their bar line | Bars with a note on the first beat, lines beginning ON the bar line (light opening; stressed) | Lines beginning AFTER it (light; stressed) |
|---|---|---|---|
| Song 50's words | 0.378 | 0.995; 0.991 | 0.501; 0.459 |
| Song 52 | 0.385 | 0.991; 0.998 | 0.575; 0.643 |
| Song 61's words | 0.222 | 0.967; 0.961 | 0.518; 0.484 |

A line that begins on its bar line puts a note on the first beat of nearly every bar. A line that begins after it does so in about half its bars.

## How often that happens, against the table
- **Essen 6/8's kept two-bar windows (8983):** the first onset is after the bar line in 731, a share of **0.081**. And 691 of those are one shape: the first bar holds a single note on its last eighth. That is a pickup into the next bar, caught by a window that happens to start a bar early; it is not a phrase beginning late.
- **Our builds:** 0.378 of lines on song 50's words, 0.385 on song 52, 0.222 on song 61's words.

## Which lines begin late
- Song 50's words, late lines by how made: {"870 wait": 935, "818 again": 979, "818 rhythm": 123, "again": 531, "copy": 2602, "fresh": 19}; first onsets (twelfths after the bar line: lines): {"3": 90, "6": 1729, "9": 44, "12": 1608, "15": 100, "18": 230, "24": 858, "27": 160, "30": 252, "36": 118}.
- Song 52: {"818 again": 769, "870 wait": 1096, "again": 1321, "copy": 1207, "fresh": 78, "818 rhythm": 47}; first onsets: {"3": 8, "6": 525, "9": 12, "12": 199, "18": 209, "24": 211, "30": 2497, "36": 855, "39": 1, "42": 1}.
- Song 61's words: {"870 wait": 811, "818 rhythm": 113, "818 again": 883, "copy": 114, "again": 702, "fresh": 83}; first onsets: {"3": 50, "6": 508, "9": 21, "12": 975, "15": 75, "18": 103, "24": 418, "27": 31, "30": 433, "36": 92}.
- **A line drawn fresh hardly ever begins late.** The late lines are those that wait a kept rest (870), and those sung again, copied or made by 818 from a line that did.
- Bars with a note on the first beat, by how the line was made, song 50's words: 818 again 0.807 (notes 0.245); 818 rhythm 0.799 (notes 0.026); 870 wait 0.562 (notes 0.079); again 0.86 (notes 0.165); copy 0.689 (notes 0.335); fresh 0.915 (notes 0.088); title line 1.0 (notes 0.062).

## What it says
1. **870's wait.** It has a fresh line wait a rest drawn from a fixed list (a quarter to a whole 4/4 bar: 12 to 48 twelfths), and those figures are 4/4's kept rests. In 6/8 they push a line's start a third of a bar to more than a bar past its bar line. Essen's own rests are one to three eighths and rare (1.6 a tune).
2. **Copies carry it on.** A line sung again keeps its source's onsets, the late start with them; a chorus copied twice sings the late start three times. On song 50's words copies are a third of the notes.
3. **The pickup-shaped windows.** On song 52 most late lines begin at 30 or 36 twelfths: the window whose first bar holds only a pickup, sung as if the line began there. The engine already sings pickups before the bar line by its own rule; this shape is the same thing a bar late.
4. First-beat onsets have sat just over the mark on every seen lyric and just under on the held-out one because of this: the draw is not failing to favour the first beat; two rules are moving lines off it.

## Forms that follow (each its own rule, before any code)
- **A:** outside 4/4, 870's wait is not drawn from 4/4's rests. Either it is off, or it draws from the table's own rests (Essen 6/8: one to three eighths, at the table's own rate).
- **B:** a kept window whose first bar holds only a pickup is not offered as a line's rhythm; the line's pickup is the engine's own.
- The next held-out lyric (49 or 58, by the rule) after them.
