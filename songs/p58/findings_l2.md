## Findings (638–)

*Numbered from 638, after the paper's 630–637.*

### 638. 631's breath, drawn past the kept 75th percentile, left 14-syllable lines no rhythm; capped there, the port runs.

**Problem:** The first port drew the breath with a tail one interquartile range past the 75th percentile, up to 36 twelfths for the verse's cell. A 14-syllable line that must finish by tick 60 has too little of its second bar left, so its first bar would need more than 308's 57% of the line. In trials, half the builds died, all of them "rhythm: no placement" in the verses and the bridge. The breath is now drawn up to the kept 75th percentile and no further.

**Evidence:** 40-build trial, main: 20 survivors of 40 with the tail, 24 of 40 with the cap. Lines that failed had breaths of 27 to 36. Switching off each of 631's other parts in turn (the next line's entry, the end, the copies, 465) left the failures in place.

**Fix:** None further (the cap is in the port). For the paper: the kept breath table might be given by the line's entry too (on the downbeat or not), since a line that opens on its downbeat cannot take a long breath and its syllables both.

**Check:** As 631's.

### 639. 631 moves the dense spans a little and pulls the sparse ones short; spans, sixteenths and joins all miss.

**Problem:** A line drawn under 600 may now run to the next line's first onset less its breath. The dense cells came up by a few hundredths. The sparse cells fell short, because their kept breaths are long (42 to 57 twelfths at the median) and the lines end earlier still. The breaths as sung run longer than those drawn: a breath bounds where a line may end, and other bounds end it sooner. The verse's lines open on their downbeat less often than kept dense lines do.

**Evidence** (main; the control within 0.02 on spans; drawn lines in two-bar slots):

| Cell | Span to the next line's first onset, 25th / 50th / 75th | Kept | Breath as sung, 25th / 50th / 75th | Kept | On the downbeat | Kept |
|---|---|---|---|---|---|---|
| Under 3.5 | 0.25 / 0.29 / 0.36 | 0.31 / 0.40 / 0.53 | 57 / 66 / 72 | 45 / 57 / 66 | 28.6% | 28.9% |
| 3.5 to 4.5 | 0.34 / 0.41 / 0.50 | 0.44 / 0.53 / 0.64 | 48 / 57 / 66 | 36 / 42 / 54 | 17.2% | 17.7% |
| 6.5 to 7.5 | 0.70 / 0.74 / 0.78 | 0.77 / 0.79 / 0.86 | 21 / 24 / 30 | 12 / 18 / 24 | 15.4% / 14.6% | 21.6% |
| 7.5 and over | 0.72 / 0.77 / 0.80 | 0.81 / 0.88 / 0.90 | 18 / 21 / 27 | 9 / 12 / 18 | 20.2% / 20.5% | 31.1% |

- **Verse 1:** sixteenths 47.3% / 48.8% against 37.9% / 35.7% for its cells.
- **Join deaths:** 3 / 2, all at the copy into Chorus 2. The main run is over the test's two in a thousand.

**Fix:** Draw the line's end and its breath together from the kept pairs of span and breath for its cell, rather than the breath as a bound alone. Let a dense line take its room at the front, before or after its bar line, at the kept shares, where its first syllable allows.

**Check:** As 631's.

### 640. 633 and 631 together undo the template: recurrence at four and eight bars falls back, and so does the coupling gain.

**Problem:** 631 holds a line on copied bars to 600's span when its source missed its own. The template's lines, the section's first, now meet their span less often, so the lines that follow them are held to two things at once, the template's onsets and a drawn span. Mostly they keep neither exactly. 633's split of syllables was taken in few lines (about 75 in a 40-build trial).

**Evidence** (within sections; exactly the same, then Jaccard 0.6 or more; main / control):

| Bars apart | Luthier v1 | Luthier v2 | Kept |
|---|---|---|---|
| 4 | 11.3% / 11.5%; 33.4% / 32.9% | 7.1% / 7.1%; 24.6% / 22.3% | 20.1%; 38.5% |
| 8 | 17.9% / 19.1% | 5.4% / 5.7% | 24.9% |
| 16 | 12.5% / 11.9% | 6.4% / 6.8% | 24.2% |
| Coupling gain, bits a bar | 0.118 / 0.123 | 0.055 / 0.052 | median 0.14 |

**Fix:** Let a line that follows the template keep the template's span whatever the template line's span did, so that 631's condition on copies applies to copies of whole lines and not to the template. Then read 633 again.

**Check:** As 633's.

### 641. 634 brings the bits saved a gap to the kept figure; intervals do not move, and the chorus's drawn lines now sing too many sixteenths.

**Problem:** With the palette's gap classes drawn as shares, a build's first half foretells its second as a kept song's does: within 0.05 of the kept 0.29 bits a gap. The classes of move at the palette's shares leave the bits saved an interval where they were. The chorus's drawn lines took the palette's sixteenths: 578's and 600's test on drawn lines now misses there, by 14 and 16 points.

**Evidence** (bits saved on the second half, at the best share of 0.3, 0.5, 0.7, 0.85; main / control; the corpus is the kept mean palette, which stands in for the pooled counts the tables file names and does not give):

- **A gap:** 0.241 / 0.242 at 0.7 (Luthier v1 0.159 / 0.165; kept 0.29). Passes.
- **An interval:** 0.038 / 0.049 at 0.5 (Luthier v1 0.036 / 0.044; kept 0.18). Misses.
- **Chorus 1, drawn lines:** sixteenths 23.8% / 24.8% (kept for their cells 9.6% / 9.1%); eighths 56.3% / 52.9% (59.4% / 59.5%); quarters 10.6% / 12.3% (17.0% / 17.1%).
- **Dense lines' longest equal-gap run:** median 4 / 4.
- **Limits:** the rhythm-band limit kills 158 / 196 builds (Luthier v1 33 / 34): the rhythm bits leave the kept band.

**Fix:** For intervals: a song's own moves come mostly from its contour and its chords, not from the classes of move, so the palette might be drawn into the contour's size (257) rather than the move classes. For the chorus: let the palette's share of a class be at most the cell's kept 95th for it. For the rhythm band: read whether the palette drawn lies outside the band for song 48's density.

**Check:** As 634's.

### 642. 635 brings the template lines' endings within ten points at eight to ten notes a bar; elsewhere class 0 still runs high.

**Problem:** The template's long lines are drawn at 601's share, and at 8 to 10 notes a bar, the rate of most of the verse's lines, they pass. At 10 and over, and on lines that follow no template, class 0 is high. Under 8 it runs low.

**Evidence** (reachable lines of 13 notes and over in two-bar slots, by the rate as sung; class 0; main / control):

| Lines | Under 8 (kept 0.65) | 8 to 10 (kept 0.51) | 10 and over (kept 0.34) |
|---|---|---|---|
| Template lines | 0.464 / 0.477 | 0.593 / 0.582 (passes) | 0.563 / 0.566 |
| Lines that follow no template | 0.495 / 0.440 | 0.658 / 0.663 | 0.600 / 0.570 |
| Lines on copied bars (not tested) | — | 0.811 / 0.788 | 0.608 / 0.665 |

**Fix:** As 612 (from the v137 list): the class from the rate of the rhythm as placed where the span drawn is not met.

**Check:** As 635's.

### 643. 557 by section: the chorus comes six tenths nearer, through the form's measures, not the engine's; the verse holds.

**Problem:** None; a reading. The chorus's long kept breaths leave its windows bars like a kept chorus's, and the form's two measures turn from a cost (−0.35) to a gain (+0.33). The engine's own part of the chorus is a little farther than under Luthier v1.

**Evidence** (main / control):

| Window | Luthier v1 | Luthier v2 |
|---|---|---|
| Verse 1 | −0.76 / −0.81 | −0.78 / −0.92 |
| Chorus 1 | −2.12 / −2.27 | −1.48 / −1.64 |
| Both | −1.44 / −1.54 (25% / 24% under the 5th) | −1.13 / −1.28 (16% / 17%) |
| Chorus split: designed / form / rest | +0.68 / −0.35 / −2.45 (main) | +0.92 / +0.33 / −2.73 (main); +0.93 / +0.34 / −2.90 (control) |

**Fix:** None.

**Check:** Printed.

### 644. 630, 632 and 603: the pick clears the median; the verse window still ends on the tonic at the kept share; leaps hold.

**Problem:** None.

**Evidence** (main / control):

- **630:** the pick's gain is 0.166 / 0.188. The pick changed on the main run (bfb7c746a67c, third under the refit, for 16defe5afb3f), and on the control it was already first (544852aa421f). Survivors at or over 0.14: 16.3% / 13.8%.
- **630 on Luthier v1's runs:** the picks are unchanged (1856be9a40e9, 0.146; b4bf8b84c2b8, 0.336).
- **632:** the verse window ends on the tonic 20.2% / 18.8% (kept 19%); 262 is lifted for that note, as under v137.
- **603:** leaps past a fifth 1.7% / 1.6%; mean interval 1.80 / 1.91 (kept 1.94).

**Fix:** None.

**Check:** As each.

### 645. The run: survivors fall by a quarter.

**Problem:** 631's breaths and 634's shares cost about 240 survivors on each run. The rhythm-band limit leads (641), then "rhythm: no placement", where lines still find no room between a long breath and their syllables (639).

**Evidence** (main / control):

- **Survivors:** 627 / 629 (Luthier v1 850 / 891). Orders e6f259b64c38 / a6023c8db5cb. Seed and designs as v134.
- **Limit deaths:** 197 / 223 (97 / 62). Rhythm band 158 / 196; run_max 56 / 43; spectral 49 / 43; the longest notes in eight bars 28 / 37.
- **Rhythm, no placement:** 112 / 118 (0 / 0).
- **The chorus above the verse:** 44 / 21.
- **Joins:** 3 / 2 at the copy into Chorus 2.
- **Kept against kept (637):** 0.513 (printed under Luthier v1; the judge was not refitted).

**Fix:** As 639 and 641.

**Check:** Survivors within a tenth of Luthier v1's.
