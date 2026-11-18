# Breath: does a hit's sung line last one slow breath?

Prediction, taken from physiology before looking at songs: the body keeps a 10-second rhythm (Mayer waves, 0.1 Hz). Bernardi found the rosary and yoga mantras slow breathing to 6 a minute and lock onto it (BMJ 2001), and Verdi phrases of about 10 s entrain heart rate and blood pressure (Circulation 2009). If music moves people through the body, great songs should breathe near that period.

Measure: the clock length of the four-bar unit (one sung line in most pop songs; the Billboard lyric line median is 7.6 s, its four-bar median 7.7 s). CoCoPops from the McGill audio timestamps; BiMMuDa from its tempo metadata. 14 songs are in both and agree to within 1% (Venus 9%).

| Set | n | median four-bar (s) | share 8 to 12 s |
|---|---|---|---|
| BiMMuDa year-end top 5, 1950-2024 | 319 | 9.23 | 0.59 |
| Rolling Stone greatest | 168 | 8.32 | 0.49 |
| Billboard top 10 | 112 | 7.84 | |
| Billboard peaked below 20 | 50 | 7.10 | |
| Billboard all | 184 | 7.69 | 0.33 |
| Luthier song 58 (84 bpm) | 1 | 11.4 | in band |

Tests (AUC, nearness to 10 s): year-end hits over Billboard below 20, 0.71 (p < 0.001), same era 1958-91 0.705; Billboard top 10 over below 20, 0.606 (p 0.03); Rolling Stone over Billboard 0.574 (p 0.017). Within Billboard, nearness against peak rank is flat (0.056).

The honest limit: 10 s is not shown to be special. Scanning the centre from 5 to 16 s, separation rises and then plateaus from about 10 s up, and raw length separates as well (0.743). What is shown: lesser songs rush the line (median 7.1 s); hits let it last about a slow breath, and that median has held between 8.0 and 10.7 s in every decade since the 1950s while styles changed around it.

Phrase level (rests of 1.5 beats or more): cycles of 2 to 3 s in hits and in song 58 alike; no separation.

Scripts: breath_lib.py, arc.py (arc.json).
