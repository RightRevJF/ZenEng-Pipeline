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

## Second pass: what the bibliographies held (18 November 2026)

Read past the abstracts into the references and methods. Two papers in Bernardi 2009's list (refs 31, 32: Bettermann 2002, Cysarz 2004) changed the question. In hexameter recitation the 10-second cycle is not one long phrase. Each breath carries half a line (about 4.8 s, 12 a minute) and two halves alternate, a shallow breath listening and a deeper one reciting, giving the slow cycle at 6.4 a minute. The rosary's 10 s is the same shape: priest, then people. Bernardi 2006 (ref 6, "the importance of silence"): a pause took heart rate and blood pressure below baseline.

Test (breath_spectrum.py, exploratory, decided after the first pass): the sing-and-breathe signal of each melody (onsets only, a breath is a gap of 1.5 beats or more), its dominant period between 3 and 32 beats.

| Set | n | breath locked to 1, 2 or 4 bars | dominant breath (s) |
|---|---|---|---|
| BiMMuDa year-end top 5 | 313 | 0.62 | 5.2 |
| Rolling Stone | 194 | 0.57 | 4.8 |
| Billboard top 10 | 125 | 0.58 | 4.9 |
| Billboard below 20 | 61 | 0.33 | 5.7 |

Fisher tests against the below-20 songs: year-end odds 3.3 (p < 0.001), Rolling Stone 2.7 (p 0.001), top 10 2.9 (p 0.002). The most common breath in every set of hits is every two bars.

Reading: every singer breathes about every 5 s (the body sets that). In hits the form is built so that breath falls on the grid, two bars a breath, and two breaths make the four-bar line of about 9 to 10 s: the hexameter's shape. In lesser songs the singer still breathes every 5 to 6 s, but the breath floats against the bars.

Luthier: song 58 breathes every bar (2.9 s, about 21 a minute); songs 52 and 54 are not locked; 55 is locked at two bars (4.1 s).

Not yet held out. Scripts: breath_spectrum.py (breath_spectrum.json).
