# Predictions, written before any of the 410 songs was measured (18 November 2026, 18:00)

Data: CoCoPops (Condit-Schultz and colleagues): 200 songs from Rolling Stone's 500 Greatest Songs (de Clercq and Temperley's corpus, re-encoded) and
210 sung songs from a random sample of the Billboard Hot 100, 1958-1991, each with melody and chords by bar. Plus Luthier's songs 54, 55, 58.

Readings from each song's bar-against-bar picture (ssm_lib.py):
- architecture: share of bars inside a long repeat (a diagonal run of 4 or more bars, likeness 0.8 or more, at a distance of 8 bars or more)
- nesting: how many of the distances 2, 4, 8, 16 and 32 bars stand out as a peak of repetition (blocks inside blocks: the same order at every scale)
- weave: likeness at distances of 1 to 3 bars over likeness at 8 to 32 bars (small things repeat, large things do not)
- centre: how unlike the rest of the song its most distinctive 4-to-8-bar stretch is, if that stretch lies between 0.35 and 0.85 of the song
- frame: likeness of the song's first 8 bars to its last 8 (best alignment)
- sameness: mean likeness of all bar pairs

P1. Rolling Stone songs show more architecture than the Billboard sample (AUC over 0.55).
P2. Rolling Stone songs more often have a centre (AUC over 0.55).
P3. Rolling Stone songs more often have a frame (AUC over 0.55).
P4. Rolling Stone songs show more nesting (AUC over 0.55).
P5. Luthier's songs sit under the human 10th percentile on architecture and over the human 90th on weave.
P6. Inside the Billboard sample no reading relates to peak or weeks past |rho| 0.15.
What I expect, given today's other nulls: at most one of P1-P4 holds; P5 holds; P6 holds.
Check against encoding: songs in both sets are read in both encodings; a reading that differs between the two encodings of the same song is not trusted.
