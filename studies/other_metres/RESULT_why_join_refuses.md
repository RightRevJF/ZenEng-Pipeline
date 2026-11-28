# What the join refuses when a marked line is sung again: a count (28 Nov 2026). Every refusal is a run of one pitch that the copy itself made.

00:27 ET. A count (why_join_refuses.py, 300 builds from each of the last trial's records); nothing predicted, nothing run under a changed form. Figures printed from why_join_refuses_52/61/50/49.json by the command that wrote this file.

| | Tries that reached the join | Refused, and why | The commonest cases: [source's notes, the line's syllables, longest run of one pitch in the source, longest in the copy, tries] |
|---|---|---|---|
| Song 52 | 4500 | {"the line's own run of one pitch is over the cap": 254} | [[12, 11, 2, 4, 36], [12, 14, 2, 4, 28], [7, 11, 2, 4, 24], [12, 11, 2, 5, 20]] |
| Song 61's words | 4500 | {"the line's own run of one pitch is over the cap": 387} | [[8, 11, 2, 5, 69], [10, 9, 2, 4, 41], [9, 10, 2, 4, 33], [9, 9, 2, 4, 19]] |
| Song 50's words | 2400 | {"the line's own run of one pitch is over the cap": 89} | [[7, 10, 3, 4, 17], [8, 9, 2, 4, 16], [7, 10, 2, 4, 14], [7, 6, 2, 4, 6]] |
| Song 49's words | 3300 | {"the line's own run of one pitch is over the cap": 102} | [[5, 6, 2, 5, 25], [8, 8, 2, 4, 23], [5, 6, 2, 4, 20], [8, 8, 2, 5, 7]] |

- These songs are not aimed (False), so the join's test is one thing only: no run of one pitch longer than 3 inside the line. Nothing is carried in from the line ahead, and the join's own mend (the first note moves a step) is not offered to a song that is not aimed.
- **In every refusal the source's longest run is two or three, inside the cap, and the copy's is four to six.** The copy makes the run: a note split off for an extra syllable repeats its neighbour's pitch, and notes moved onto the new section's chord land on one another.
- Song 61's words' Verse 3, fourth line (eleven syllables on an eight-note source) is {"the line's own run of one pitch is over the cap": 130}.

## The form that follows (its own rule, before any code)
A line sung again mends its own run: where the copy has made a run of one pitch longer than the cap, the note that takes it over the cap moves a scale step toward the note after it, inside the line's register. If that does not bring every run inside the cap, the line is refused as now.
