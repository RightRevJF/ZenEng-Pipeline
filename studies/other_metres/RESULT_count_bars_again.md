# Which bars are on a rhythm already sung: the result

28 November 2026. Rule file first: PREDICTION_count_bars_again.md (ce26017). Every figure is printed from RESULT_count_bars_again.json by the command that wrote this page. Song 49's words (seed 7, 244 living builds) and song 55's (seed 4, 192); the pop 3/4 clips (459). No engine or planner change.

| In a section's first 16 sung bars (median; 25th to 75th) | Song 49's words | Song 55's words | Pop 3/4 clips (205 of 16 bars or more) |
|---|---|---|---|
| Different bar rhythms | 10.0 (8.0 to 12.0) | 10.0 (9.0 to 11.0) | 6.0 (4.0 to 8.0) |
| Bars on a rhythm already sung | 0.375 (0.25 to 0.5) | 0.375 (0.312 to 0.438) | 0.625 (0.5 to 0.75) |
| Whole section: sung bars (median) | 17.0 | 20.0 | 15.0 |

| Song 49's words: a bar, by the line it belongs to | Share of bars | On a rhythm already sung in its section |
|---|---|---|
| all bars | 1.0 | 0.459 |
| made: fresh | 0.155 | 0.262 |
| made: title line | 0.038 | 0.173 |
| made: copy | 0.214 | 0.371 |
| made: again, the source's count | 0.239 | 0.547 |
| made: again, one apart | 0.047 | 0.484 |
| made: 818 again, the source's count | 0.18 | 0.632 |
| made: 818 again, one apart | 0.105 | 0.558 |
| two lines in the bar | 0.122 | 0.292 |
| slot of 2 bars | 0.467 | 0.343 |
| slot of 4 bars | 0.533 | 0.56 |

## Plainly
- **The cause, counted: a section of ours uses about 10 different bar rhythms in its first 16 bars; a pop section uses 6.** Like for like in length, bars on a rhythm already sung are 0.375 and 0.375 in ours and 0.625 in the clips. The lyric makes no difference to that (song 49's words and song 55's give the same 10).
- **Why matching line lengths did not help:** K6 is read within a section. A verse-2 line that sings its verse-1 line again, note for note, brings that line's rhythm into verse 2 for the first time there; it is "new" to its own section. Lines sung again with their source's count sit on a rhythm already sung in their section only 0.547 of the time; copies 0.371. Singing again across sections cannot raise a within-section figure. Only what a section does inside itself can.
- **Inside a section, every source of bars makes new ones more often than not:** bars of lines drawn fresh are on a rhythm already sung 0.262 of the time, title lines 0.173; 818's lines (the line two above sung again) are the best at 0.632, and they are 0.285 of the bars. A kept two-bar window is two different bars more often than not, and each line drawn takes its own window from a table of hundreds.
- So the engine draws each line's rhythm as if the section had no memory of its bars. For pitch it has one (923: a note that completes a figure already sung is favoured, fitted in 4/4 so that figures sung again met the kept median). For rhythm it has none.

## My expectation, against the result
- "About twice as many different bar rhythms in 16 bars": 10 against 6; a little under twice. Right in substance.
- "Bars holding two lines' notes are a small share and nearly always new": 0.122 of bars, on a rhythm already sung 0.292. Right.
- "Lines sung again with their source's count sit on rhythms already sung nearly always": **wrong** (0.547), and the reason is the finding: again across sections is new within the section.
