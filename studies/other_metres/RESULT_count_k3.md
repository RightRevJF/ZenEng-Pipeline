# K3 in pop 3/4: the ceiling, the floor of the trade, and where the stress is lost (28 Nov 2026). The lines drawn fresh meet K3. The lines sung again to new words do not, and they are seven tenths of the song. A count; nothing predicted, nothing run.

03:30 ET. Asked by the songwriting session (03:24 ET): read what the mark allows before building toward it. count_k3_ceiling.py (from the table and the last pop record's plan) and count_k3_by_made.py (400 builds from that record). Figures printed from count_k3_ceiling_pop55.json and count_k3_by_made_pop55.json by the command that wrote this file.

## 1 and 2. The ceiling and the floor of the trade (song 55's words, the pop table as kept, the plan of RESULT_pop_3_4_b.md)
Every line has kept windows at its planned bars (56 lines; 0 without). Over 187 stressed syllables:

| | Stressed on the first beat | Stressed off the beat |
|---|---|---|
| Each line takes its best window (the ceiling; the floor for off the beat) | **0.674** | **0.0** |
| Windows taken by kept count alone | **0.421** | **0.165** |
| The builds (pick; living median) | 0.337; 0.326 | 0.326; 0.348 |
| K3's mark | 0.45 or more | 0.26 or under |

(The two bounds in the first row are separate: one window need not be best for both.)

- **The ceiling is well over 0.45,** so the mark can be reached on this lyric and table.
- **But the builds are under what kept count alone would give** (0.33 against 0.42 on the first beat; 0.34 against 0.17 off the beat). A draw that weighed stress too little would land between count alone and the ceiling. Landing under count alone says the stress is being lost somewhere other than in the weighing of windows.

## Where it is lost: K3 by how each line was made (244 living builds)
| How the line was made | Share of the song's stressed syllables | On the first beat | Off the beat |
|---|---|---|---|
| all | 1.0 | 0.317 | 0.347 |
| again | 0.503 | 0.272 | 0.387 |
| 818 again | 0.221 | 0.227 | 0.453 |
| copy | 0.176 | 0.477 | 0.197 |
| fresh | 0.077 | 0.467 | 0.181 |
| title line | 0.016 | 0.512 | 0.1 |
| 870 wait | 0.007 | 0.29 | 0.326 |

- **Lines drawn fresh, title lines and copies meet K3:** 0.47 to 0.51 on the first beat, 0.10 to 0.20 off the beat. The draw, with the table's stress score, is doing what the mark asks.
- **Lines sung again to new words do not:** the lyric's own "again" lines (half the song's stresses) are at 0.27 and 0.39; lines 818 sings again (a fifth) at 0.23 and 0.45.
- A copy sings the same words to the same rhythm, so it keeps its source's fit. A line sung again sings **new words** to the old rhythm, and outside 4/4 the routine fits them by splitting the widest gap and dropping the narrowest, with no regard to which syllables are stressed. In 4/4 the same routine chooses its splits and drops by the words' weights (fix 882); that choice has never been made outside 4/4.

## What this changes
- **K3 is not the ordering of count against stress in the draw.** On 27 November the reachability count showed the mark could be reached and the draw did not reach it, and the cause was taken to be the ordering; 749.236 (the weight from data) was the form. That reading did not separate fresh lines from lines sung again. Read apart, the draw reaches the mark and the refit of new words does not.
- 749.236 may still be worth fitting for its own sake, and Lieder is still the worded source for stress outside 4/4. But neither is what K3 needs, and the Lieder fetch is not on K3's road.

## The form that follows (its own rule, before any code)
**A line sung again fits its new words:** where the syllables do not match the source's notes one for one, the choice of which gaps to split and which notes to drop is the one that sets the new words' stresses best by the table's own stress score (749.231's, the same score the draw uses), as 882 does in 4/4 by the words' weights. The source's pitches and the notes kept are as now. Marks: K1 to K8, K3 read also apart for lines sung again; the 6/8 lyrics read again, since the routine is shared.
