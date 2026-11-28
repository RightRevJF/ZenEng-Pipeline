# Why a line marked "again" is drawn fresh: a count (27 Nov 2026). The copy has more syllables than its source, and the note split off for them lands just past the line's limit.

20:29 ET. A count; nothing predicted, nothing built (why_again_fresh.py wraps the routine and reads it). Figures printed from why_again_fresh_pop55.json and why_again_fresh_61.json by the command that wrote this file. Both records are the last trial's (749.240, the refit, shared bars).

## Pop 3/4, song 55's words (300 builds, 300 made)
- Tries to sing a marked line again: 7800. Drawn fresh (712): 1707.
- Turned away for ending past its own slot (749.240): **1319**. By the join to the line ahead: 377. No fit at all: 0.
- Of those past the slot: already past before the join in 1319, only after the join in 0. Past by (twelfths of a quarter: builds): {"3": 695, "6": 621, "9": 3}.
- Source's notes against the copy's syllables, [source, copy, tries]: [[5, 7, 479], [7, 8, 426], [6, 7, 205], [5, 6, 187], [7, 7, 21], [6, 6, 1]].

## Song 61's words, 6/8 (300 builds, 300 made)
- Tries to sing a marked line again: 4500. Drawn fresh (712): 761.
- Turned away for ending past its own slot (749.240): **479**. By the join to the line ahead: 279. No fit at all: 0.
- Of those past the slot: already past before the join in 479, only after the join in 0. Past by (twelfths of a quarter: builds): {"6": 343, "9": 136}.
- Source's notes against the copy's syllables, [source, copy, tries]: [[8, 11, 234], [9, 10, 230], [9, 9, 8], [10, 9, 7]].

## What it says
- Most of what is still drawn fresh is turned away by 749.240's limit, and **in nearly every such case the copy has more syllables than its source has notes** (five notes for seven syllables, seven for eight, eight for eleven).
- The routine makes the missing notes by splitting the widest gap, and it counts the gap after the last note as running to an eighth before the slot's end. A fresh line's last syllable must begin a breath before the end, which is earlier. So the split-off note lands **3 to 9 twelfths past the limit**: a sixteenth to a dotted eighth.
- The refit of the last trial left out the source's late notes and then this split put one back.
- The join to the line ahead turns away fewer (377 and 279 tries), and is a separate matter.

## The form that follows (its own rule file before any code)
When a line sung again needs more notes than its source has, the gap after its last note is counted only as far as the line's own limit (the slot's end less the line end's room), so no note is split off past it. Nothing else changes.
