# Counts (A) and (B): the result

28 November 2026. Rule file first: PREDICTION_counts_AB.md (ca0eabc). Every figure is printed from RESULT_counts_AB.json by the command that wrote this page. Pop 3/4, song 55's words, RESULT_251's record; 231 living builds of 400. No engine change.

## Count (A): what the draw's limits remove
| Drawn lines, expected on the first beat | Every drawn line | Title lines | After 870's wait |
|---|---|---|---|
| no limit | 0.591 | 0.656 | 0.577 |
| the earliest start alone | 0.548 | 0.656 | 0.43 |
| the room at the slot's end alone | 0.586 | 0.667 | 0.561 |
| the cap alone | 0.585 | 0.656 | 0.577 |
| the cut to the twelve best alone | 0.61 | 0.667 | 0.6 |
| the early entries alone (834) | 0.519 | 0.531 | 0.519 |
| all together | 0.49 | 0.538 | 0.388 |
| what was built | 0.472 | 0.53 | 0.378 |

## Count (B): one rhythm, many words (first beat over every set carried)
| Source line | Sets carried | Best any rhythm reaches | The rhythm of the best summed score | Best for its own words alone |
|---|---|---|---|---|
| Verse 1:0 | 24 | 0.496 | 0.363 | 0.474 |
| Chorus 1:0 | 32 | 0.592 | 0.582 | 0.535 |
| The two together | | 0.538 | 0.459 | 0.501 |
| All source lines (they overlap) | | 0.534 | 0.478 | 0.497 |

## Plainly
- **(A) Of the gap between the unlimited draw (0.591) and what is built (0.472), the early entries take most.** Each limit alone takes: the early entries (834) 0.072; the earliest start 0.043; the room 0.005; the cap 0.006; the cut to the twelve best -0.019 (it adds, not takes). All together the draw expects 0.49, and 0.472 is built; the rest is the one-bar path (876, at 0.09), which I did not replicate.
- **What 834 is:** a line that opens on a stress sings its whole rhythm an eighth or a quarter early, with chance 0.2. That chance is the 4/4 default: the pop 3/4 table carries no entry shares (it has no words), so the engine falls back to the 4/4 figure. And the early rhythm is scored as if it had not moved, so a rhythm chosen for its stresses on the first beat is then slid off it. Title lines show it plainest: 0.656 without it, 0.531 with it alone, 0.53 built.
- **749.245's rests:** lines set after 870's wait are few (164 stresses of 4288) but poor: the later start alone takes them from 0.577 to 0.43, and 21 of 67 fall to the weighted rule (built at 0.267). 749.250's edge room does not act on this lyric at all (the record has no pickup room set).
- **(B) One rhythm can serve its words:** for the two lines drawn in every build, the best any single rhythm reaches over all the sets it carries is 0.538, over 0.45. So 818 tying many sets to one rhythm is **not** a wall under K3, and the count of how far real repeated lines vary is not needed for that reason.
- **But the summed score does not find that rhythm:** the rhythm of the best summed score reaches 0.459 (Verse 1:0 alone: 0.363 against a best of 0.496). The score also weighs where unstressed syllables fall, and summed over two dozen sets that outweighs the first-beat stresses. Source lines whose best is itself under 0.45: Verse 1:1, Verse 1:2, Verse 1:3, Verse 1:6, Chorus 1:4.

## My expectation, against the result
- (A) "the earliest start takes most": **wrong.** The early entries take most (0.072 against 0.043). "The cut to twelve takes under 0.02": it takes nothing, it adds 0.019. "The room and the cap take little": right.
- (B) "Verse 1:0 under 0.45": **wrong**, 0.496. "Chorus 1:0 over 0.50": right, 0.592. "Pooled 0.42 to 0.50": **wrong**, 0.538.
