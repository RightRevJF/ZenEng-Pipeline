# Beat strength in threes, from the physics of entrainment: a short read

28 November 2026. Asked by the writer (10:58 ET) as one narrow line: do models and measurements of how the body locks onto a beat say how strong each beat is in 3/4 and 6/8? Read by the maintainer between runs: six pages opened, most through a summary tool, so every figure below should be checked against the original before anything is built. Ideas to test, not results. No TheSession data.

## What was found

**1. Measured in the brain, beats 2 and 3 of a three-beat bar are not equal: beat 3 is the stronger.** Fujioka, Ross and Trainor (2015, Journal of Neuroscience 35(45)) played and had listeners imagine a march and a waltz on beats 390 ms apart, and read the beta-band response after each beat by MEG. In the waltz the downbeat's response was larger than the middle beat's (p < 0.01), the last beat's was larger than the middle beat's (p < 0.05), and the downbeat and the last beat did not differ significantly. Every theory of metre gives beats 2 and 3 the same weight; this measurement does not. The size of the difference is in figures I could not read; 14 listeners. https://pmc.ncbi.nlm.nih.gov/articles/PMC6605356

**2. A three-beat grouping is held as firmly as a two-beat one.** Nozaradan, Peretz, Missal and Mouraux (2011, Journal of Neuroscience 31(28)) played a 2.4 Hz beat and had listeners imagine it in twos or in threes. The brain's response at the bar's own rate appeared only for the metre imagined: 0.12 µV at 1.2 Hz for twos, 0.18 µV at 0.8 Hz for threes (medians, 8 listeners; the two were not tested against each other). Imagining threes also raised a response at 1.6 Hz, twice the bar's rate, which the authors read as a possible two-fold level arising unasked inside the three. https://pmc.ncbi.nlm.nih.gov/articles/PMC6623069

**3. Which level is "the beat" depends on clock time, not on the notation.** Parncutt (commentary in Music Theory Online, 1993, on his pulse-salience work) holds that a pulse is felt only between about 50 and 200 beats a minute and most strongly near 100 (a beat of about 0.6 s); slow tempi favour grouping in twos, fast tempi in threes. I did not reach his 1994 formula itself. https://mtosmt.org/issues/mto.93.0.3/mto.93.0.3.parncutt.html

**4. The oscillator models explain where levels come from but give no table of strengths.** Large, Herrera and Velasco (2015, Frontiers in Systems Neuroscience) model beat perception as banks of oscillators that lock to a rhythm at whole-number ratios and so produce metrical levels that are not in the sound. In what I could read, the paper ranks no ratio above another and gives no figure for three against two; its one test is a tapping study of 14 people near a 2 Hz beat. https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2015.00159/full

Not found: Palmer and Krumhansl's (1990) measured profiles for 3/4 and 6/8 as numbers (they are in a figure), and any ranking of 3:1 against 2:1 locking strength.

## What it would mean for the engine (my inference, each testable on songs we hold)

| Idea | The deduction | A count that tests it |
|---|---|---|
| Beat 3 of 3/4 is stronger than beat 2 | In worded 3/4 songs, stressed syllables fall on beat 3 more often than on beat 2 (and a note on beat 3 leads into the next bar's first beat) | On the 3/4 lead sheets: stressed syllables on beat 1, beat 2, beat 3, and off the beat. Today the engine's stress file has one figure for "another beat"; if beats 2 and 3 differ, it wants two. This is also row 5 of the mathematics report. |
| The beat is the level nearest 0.6 s | At our trial tempos a 3/4 quarter lasts 0.45 s and the bar 1.35 s, so the quarter is the beat and the bar line is a slow, weak pulse: a first-beat stress target may be less binding than a beat-level one. In 6/8 at 54 dotted quarters a minute the dotted quarter lasts 1.11 s and the eighth 0.37 s: the eighth is as near the felt beat as the dotted quarter. | In worded 6/8 and 3/4 songs sorted by tempo: does the share of stresses on the bar's first beat rise as the bar shortens toward 0.6 to 1 s? (Needs tempo marks; the lead sheets carry some.) |
| Threes hold as firmly as twos | Nothing in entrainment says a rule that works by level in 4/4 should be weaker in 3/4 | The hold-out test of the mathematics report (fit on 4/4, predict 3/4 and 6/8) |

## Plainly
The physics does not hand us a table of beat strengths for 3/4 and 6/8. It gives one measured fact the theories lack (the last beat of three is stronger than the middle one), one caution (strength follows clock time, so tempo belongs in the rule), and no reason to treat threes as a weaker kind of metre. The first is cheap to test on the lead sheets and would change one number in the engine's stress file into two.
