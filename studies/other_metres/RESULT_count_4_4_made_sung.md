# Does 4/4 lose its repeats to melismas too? The result

28 November 2026. Rule file first: PREDICTION_count_4_4_made_sung.md (a91c7bd). Figures printed from RESULT_count_4_4_made_sung.json by the command that wrote this page. The 4/4 engine as it is, every switch unset; each run by the planner's own routine, its pick equal to the record's. Four of the five songs: song 59's run was cut off by the machine's time limit and is not reported.

| 4/4 song (engine as it is, every switch unset) | Pool: bars on a rhythm already sung, as made; as sung | Living: as made; as sung | Syllables on two notes |
|---|---|---|---|
| 54 | 0.656; 0.566 | 0.692; 0.605 | 0.076 |
| 55 | 0.574; 0.482 | 0.582; 0.5 | 0.083 |
| 61 | 0.484; 0.406 | 0.5; 0.418 | 0.058 |
| 66 | 0.622; 0.535 | 0.618; 0.53 | 0.056 |

## Plainly
- **Yes, the same gap is in 4/4.** On the living builds, bars on a rhythm already sung fall by 0.082 to 0.088 once the second notes are placed, on every song read. The pool shows the same.
- 4/4's bars-on-a-rhythm figure is read on the whole song, where copies of whole sections (which 919 already covers) carry most of the repeats; the loss comes from 818's lines and from lines sung again with a different count, as in 3/4.
- So 749.261 is a 4/4 question too, and part of the judging research's run 13 gap (rhythm figures heard before: 0.36 in the engine against 0.54 in real songs) is this. A trial of 749.261 in 4/4 would be a form in the built engine's own metre, so it is for the songwriting session to order, on seen 4/4 songs, with the byte check for once expected to fail where the switch is set.

## My expectation, against the result
- "The same gap, smaller: 0.05 to 0.10": 0.082 to 0.088. Right.
