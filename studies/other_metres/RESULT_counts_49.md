# Two counts after the second held-out lyric (28 Nov 2026): the title's room is no longer needed, and the lyric's "again" read as a share. Counts; nothing predicted, nothing run under a changed form.

00:07 ET. count_title_room.py and why_again_fresh.py on the last trial's records. Figures printed from count_title_room_49/50/52/61.json, why_again_fresh_*.json and share_712.json by the command that wrote this file.

## 1. The thin chorus: what the title's room costs, and whether it is still needed
The title's room (749.229) gives a title line more bars until 0.9 of its kept windows put half its stresses on a beat. It was made before 749.244, which now offers a title line only the windows that pass that same test. So the question is whether a passing window exists at the bars the density rule gave the line in the first place.

| | Title line | Syllables | Bars, density rule to title's room | Kept windows offered, and passing 840's test, at the density rule's bars | A passing window exists |
|---|---|---|---|---|---|
| Song 49's words | Chorus 1:0 | 6 (2 stressed) | 2 to 3 | [70, 55] | yes |
| Song 49's words | Chorus 1:6 | 5 (2 stressed) | 2 to 3 | [41, 37] | yes |
| Song 49's words | Chorus 2:0 | 6 (2 stressed) | 2 to 3 | [70, 55] | yes |
| Song 49's words | Chorus 2:6 | 5 (2 stressed) | 2 to 3 | [41, 37] | yes |
| Song 49's words | Last Chorus:0 | 6 (2 stressed) | 2 to 3 | [70, 55] | yes |
| Song 50's words | Chorus 1:6 | 7 (5 stressed) | 2 to 4 | [65, 27] | yes |
| Song 50's words | Chorus 2:6 | 7 (5 stressed) | 2 to 4 | [65, 27] | yes |
| Song 50's words | Last Chorus:6 | 7 (5 stressed) | 2 to 4 | [65, 27] | yes |
| Song 52 | Chorus 1:2 | 7 (5 stressed) | 2 to 4 | [35, 10] | yes |
| Song 52 | Chorus 2:2 | 7 (5 stressed) | 2 to 4 | [35, 10] | yes |
| Song 52 | Bridge:2 | 10 (6 stressed) | 3 to 4 | [[65, 27], [9, 3]] | yes |
| Song 61's words | Chorus 1:7 | 7 (3 stressed) | 2 to 4 | [35, 19] | yes |
| Song 61's words | Last Chorus:7 | 6 (2 stressed) | 2 to 4 | [70, 48] | yes |

(A line of three or four bars is read in its two parts, as the draw makes it: [offered, passing] for each part.)

**On all four lyrics, every title line has passing windows at the bars the density rule gave it.** With 749.244 in place the title's room is buying nothing that the draw does not already do, and it costs bars:

| | Syllables a sung bar now | Bars the title's room added | Bars that could come back | Syllables a bar if they did |
|---|---|---|---|---|
| Song 49's words | 3.316 | 5 | 5 | 3.495 |
| Song 50's words | 3.505 | 6 | 6 | 3.736 |
| Song 52 | 3.565 | 5 | 5 | 3.738 |
| Song 61's words | 3.563 | 4 | 4 | 3.735 |

Essen's middle half of notes a bar is 3.60 to 4.33; notes run a little over syllables (melismas). Song 49's words would be at 3.495 syllables a bar: its notes a bar, 3.49 now on 98 bars, would be about 3.68 on 93 if the same notes were sung. That is arithmetic, not a run.

## 2. The lyric's "again" drawn fresh, as a share of the tries (300 builds)
| | Tries to sing a marked line again | Drawn fresh | Share | What happened |
|---|---|---|---|---|
| Song 52 | 4500 | 331 | 0.0736 | {"taken, or turned away by the span limit": 4169, "the join to the line ahead": 331} |
| Song 61's words | 4500 | 342 | 0.076 | {"taken, or turned away by the span limit": 4212, "the join to the line ahead": 288} |
| Song 50's words | 2400 | 125 | 0.0521 | {"taken, or turned away by the span limit": 2275, "the join to the line ahead": 125} |
| Song 49's words | 3300 | 90 | 0.0273 | {"taken, or turned away by the span limit": 3214, "the join to the line ahead": 86} |

Before 749.240 and 749.241, on the same package otherwise: song 50's words {"tries": 2400, "drawn_fresh": 111, "share": 0.0462}; song 49's words {"tries": 1210, "drawn_fresh": 29, "share": 0.024}.

- On song 49's words 86 of the 90 lines drawn fresh were turned away by the join to the line ahead; none by 749.240's limit. Its share is 0.0273.
- **The mark as the songwriting session wrote it for song 58 and after** (the higher of 1.5 times the lyric's own share before 749.240, and the highest share among the three seen lyrics now): the highest of the three seen lyrics now is **0.076**.
- Read by that mark, song 49's words' share of 0.0273 would be under it. It stays recorded as missed on the count mark it was run under.

## What follows (its own rule, before any code)
**The title's room is retired where 749.244 is on:** a title line keeps the bars the density rule gives it, and is drawn among the windows that pass 840's test. Where no passing window exists at those bars, the title's room applies as before. To be run on the four seen lyrics, every mark, before song 58's words are held out.
