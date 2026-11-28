# 749.249, the title line's stress pull: two arms on the five seen lyrics (28 Nov 2026). Arm A MISSES; arm B MISSES. By the rule written beforehand the title keeps the doubled pull, and song 69's package is b573749's. Not built.

02:19 ET. Rule: PREDICTION_249.md (commit c401371, before any code or run). Switch `LUTHIER_TITLE_PULL` (0 for arm A, 1.4 for arm B), unset by default. Figures, and what is met and missed, printed from forms_249.json by the command that wrote this file; every record carries its switches and a judge that ran. Byte for byte with every switch unset: 54, 55, 52, song 53's Essen arm.

| | Mark 1 (every mark as it stands) | 840 in ten | Mark 2: the title lines' stresses on a beat against the other fresh lines' median | Watched: the commonest rhythm's share of builds (the table's) |
|---|---|---|---|---|
| song 52, as built (2.8) | every one met | 0.0 | {"Chorus 1:2": 0.6, "Bridge:2": 0.833} against 0.75: **missed** | 0.548 (table 0.329); 0.373 (table None) |
| song 52, arm A (no pull) | every one met | 0.0 | {"Chorus 1:2": 0.6, "Bridge:2": 0.667} against 0.75: **missed** | 0.532 (table 0.329); 0.255 (table None) |
| song 52, arm B (1.4) | every one met | 0.0 | {"Chorus 1:2": 0.6, "Bridge:2": 0.833} against 0.75: **missed** | 0.542 (table 0.329); 0.23 (table None) |
| song 61's words, as built (2.8) | every one met | 0.02 | {"Chorus 1:7": 1.0} against 0.69: met | 0.545 (table 0.229) |
| song 61's words, arm A (no pull) | every one met | 0.02 | {"Chorus 1:7": 1.0} against 0.69: met | 0.342 (table 0.229) |
| song 61's words, arm B (1.4) | every one met | 0.02 | {"Chorus 1:7": 1.0} against 0.69: met | 0.53 (table 0.229) |
| song 50's words, as built (2.8) | every one met | 0.0 | {"Chorus 1:6": 0.8} against 0.6: met | 0.863 (table 0.252) |
| song 50's words, arm A (no pull) | every one met | 0.0 | {"Chorus 1:6": 0.6} against 0.6: met | 0.348 (table 0.252) |
| song 50's words, arm B (1.4) | every one met | 0.0 | {"Chorus 1:6": 0.8} against 0.6: met | 0.813 (table 0.252) |
| song 49's words, as built (2.8) | every one met | 0.0 | {"Chorus 1:0": 1.0, "Chorus 1:6": 1.0} against 0.8: met | 0.907 (table 0.285); 0.677 (table 0.134) |
| song 49's words, arm A (no pull) | every one met | 0.0 | {"Chorus 1:0": 0.5, "Chorus 1:6": 1.0} against 0.8: **missed** | 0.365 (table 0.285); 0.34 (table 0.134) |
| song 49's words, arm B (1.4) | every one met | 0.0 | {"Chorus 1:0": 1.0, "Chorus 1:6": 1.0} against 0.8: met | 0.895 (table 0.285); 0.67 (table 0.134) |
| song 58's words, as built (2.8) | every one met | 0.0 | {"Chorus 1:0": 1.0} against 0.75: met | 0.925 (table 0.585) |
| song 58's words, arm A (no pull) | **missed:** onsets on the beat | 0.0 | {"Chorus 1:0": 0.5} against 0.775: **missed** | 0.725 (table 0.585) |
| song 58's words, arm B (1.4) | every one met | 0.0 | {"Chorus 1:0": 1.0} against 0.75: met | 0.782 (table 0.585) |

## Plainly
- **Arm A (no pull) misses.** The title's choice widens to near the table's, as the formula said. But the title lines are then set worse than the lines around them on three lyrics (mark 2), and on song 58's words the pick's onsets on the beat fall under their mark.
- **Arm B (the ordinary pull) meets every mark as it stands on all five, and misses mark 2 on song 52 only:** its chorus title line puts 0.6 of its stresses on a beat against 0.75 for the other fresh lines.
- **That same line is at 0.6 as built, with the doubled pull.** Mark 2 is missed on song 52 under the package song 58's words passed on. The line has five stressed syllables in seven, in two bars of two beats each: four beats for five stresses, so 0.8 at the very most, and the windows that pass 840's test give it 0.6. So on that line mark 2 does not tell arm B from what is built now; both sit at 0.6.
- **By the rule as written, neither arm passes, so the title keeps the doubled pull and the narrowing stays on the list as a known cost. Song 69's package is b573749's.** I do not move the mark. Whether mark 2 should be read against what a line's stresses and beats allow is the songwriting session's to say, for a later run.

## Watched: is our commonest rhythm the table's commonest passing window?
(true or false, then its rank in the table among the passing windows and its share of the table's count)

| | As built | Arm A | Arm B |
|---|---|---|---|
| song 52, Chorus 1:2 | False, [3, 0.149] | False, [3, 0.149] | False, [3, 0.149] |
| song 61's words, Chorus 1:7 | True, [1, 0.229] | True, [1, 0.229] | True, [1, 0.229] |
| song 50's words, Chorus 1:6 | False, [4, 0.074] | False, [5, 0.072] | False, [4, 0.074] |
| song 49's words, Chorus 1:0 | False, [3, 0.084] | False, [3, 0.084] | False, [3, 0.084] |
| song 49's words, Chorus 1:6 | False, [2, 0.115] | False, [2, 0.115] | False, [2, 0.115] |
| song 58's words, Chorus 1:0 | False, [4, 0.034] | True, [1, 0.585] | False, [4, 0.034] |

As built, on five of the six two-bar title lines our commonest rhythm is not the table's commonest passing window: it is the table's second to fourth, with 0.03 to 0.15 of the table's count. Arm B leaves that as it is. Arm A changes it on one line (song 58's words, to the table's commonest). On song 49's words and song 52 the limits, not the pull, are choosing (see the count below), so no arm moves them. So the second fault the songwriting session asked about is there as built: the draw narrows onto a window the tunes use less often.

## The count: song 49's words, the chorus's first line (formula 0.28, builds 0.91)
- The earliest start and latest last onset the line is given (twelfths; builds): {"0, 54": 530, "-6, 54": 38, "-12, 54": 19, "-9, 54": 13}. Of its 55 passing windows, 9 lie inside the commonest limits. Among those the formula gives the commonest 0.901; the builds give 0.907; the same rhythm: True. Sung all in one bar: 0.005.
- **What the formula left out is the limits.** The line opens the chorus on a light syllable and wants a pickup, but in 530 builds of 600 the earliest it may start is its bar line exactly, because the last line of the verse ends at its last allowed place. Its pickup windows are shut out, and few are left.
- The chorus's seventh line: limits {"-12, 54": 548, "-6, 54": 52}; the formula inside them 0.74, the builds 0.677.
- **This names a gap in 749.232's third reading:** it gives room for the title's pickup to the line ahead *within a section*. A title line that opens a section has the last line of the section before it ahead of it, and that line is given no such room. Song 69's chorus opens on its title three times.

## My expectation
Arm A missing mark 2 on one or two lyrics: it misses on three. Arm B passing, three chances in four: it misses mark 2 on one line, where what is built misses it too; I did not check the mark against the present package before the run, and should have.
