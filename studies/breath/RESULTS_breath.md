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

## Test A: the breath and the return (prediction from 749.19, fixed before the run)

breath_return.py. A real breath is an onset gap of 3 beats or more; the return is the song's re-entry with the rarest pitch class and widest leap (ranked within the song).

| Set | n | real breaths (median) | return in 0.55 to 0.65 | return in last 40% |
|---|---|---|---|---|
| BiMMuDa year-end | 252 | 17 | 0.087 | 0.57 |
| Rolling Stone | 189 | 22 | 0.085 | 0.57 |
| Billboard top 10 | 122 | 23 | 0.139 | 0.58 |
| Billboard below 20 | 59 | 20 | 0.085 | 0.53 |

Chance for the window is 0.10. The prediction fails: no set concentrates its return at 0.55 to 0.65, and hits do not differ from lesser songs (Fisher p 0.34 to 1.0). Fresh re-entries are not over-represented in 0.5 to 0.7 (observed over expected 0.94 to 1.09). What is universal: the freshest return falls late, the last 40% of the song, in every set alike. That is a property of songs, not of great ones.

Luthier: song 58 takes 6 real breaths in 3.3 minutes (hits 17 to 23 in about the same length); song 52 takes 1, song 54 18, song 55 24. Song 58's freshest return is at 0.29.

## Held out (PREDICTION_holdout.md, written and committed first): Hooktheory songs on the Hot 100

holdout.py. 1,479 Hooktheory songs joined to the Hot 100, none in CoCoPops or BiMMuDa; the longest clip of each.

| | top 10 | below 20 | test | held? |
|---|---|---|---|---|
| H1 breath locked to 1, 2 or 4 bars (clips of 64 beats or more) | 0.645 (183) | 0.576 (165) | odds 1.34, p 0.11 (needed 1.5, p under 0.05) | no |
| same, clips of 32 beats or more | 0.576 (618) | 0.553 (532) | odds 1.10, p 0.23 | no |
| H2 four-bar unit (s) | 7.52 | 7.68 | AUC 0.47 | no |
| H3 commonest breath in top-10 songs is every two bars | 8 beats | 8 beats too | | yes, but it is true of both |

The lead does not hold. Breathing on the grid, usually every two bars, is what pop melodies do (about 0.55 to 0.65 of songs in every set but one), and the
one set that fell short, the 61 CoCoPops songs that peaked below 20, was the outlier the discovery rested on. The four-bar line's length does not separate
either. Limit: Hooktheory clips are sections, often choruses, not whole songs. Nothing to build for greatness. What stays true for Luthier is about
being a normal song: real breaths about 7 a minute, mended in 4/4 by 870, 876 and 877; breath on the grid in more than half of human songs, where songs 58
and 55 (v22) are not.
