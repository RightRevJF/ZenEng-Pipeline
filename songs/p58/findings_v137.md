## Findings (610–)

### 610. 600 does not reach the kept spans: a line must be done by beat 3 of its slot's last bar, which caps a two-bar line at 0.75 of its slot.

**Problem:** The engine's slot end (slot_end, in the engine since song 40: "the line done by beat 3 of its last bar") puts a two-bar line's last onset no later than tick 72 of 96. A line that starts on its downbeat can therefore span no more than 0.75 of its slot. Kept dense lines run past that (0.79 to 0.90). A drawn span over 0.75 can be met only from a pickup, and the verse's lines open on a stressed syllable, so they take none.

- About 79% of the spans drawn for the 6.5–7.5 cell, and 92% of those for the 7.5-and-over cell, lie past 0.75.
- Those lines found no rhythm at their span, gave it up at half their tries, and were sung at the old span.

This conflict between 600 and the slot end should have been found before the run. It was found reading the run, and the run is reported as made.

**Evidence** (drawn lines in two-bar slots, first to last onset over the slot, 25th / 50th / 75th; main; the control is within 0.03):

| Cell | Lines | v137 | v136 | Kept |
|---|---|---|---|---|
| Under 3.5 | 923 | 0.31 / 0.38 / 0.44 | 0.31 / 0.38 / 0.50 | 0.31 / 0.40 / 0.53 |
| 3.5 to 4.5 | 3,589 | 0.44 / 0.50 / 0.56 | 0.41 / 0.47 / 0.56 | 0.44 / 0.53 / 0.64 |
| 4.5 to 5.5 | 444 | 0.50 / 0.56 / 0.66 | 0.50 / 0.56 / 0.63 | 0.56 / 0.68 / 0.71 |
| 6.5 to 7.5 | 7,107 | 0.69 / 0.75 / 0.81 | 0.69 / 0.75 / 0.81 | 0.77 / 0.79 / 0.86 |
| 7.5 and over | 4,509 | 0.69 / 0.75 / 0.81 | 0.69 / 0.75 / 0.81 | 0.81 / 0.88 / 0.90 |

- **Counts (main / control):** spans drawn 17,386 / 17,486. Lines placed at their span 7,439 / 7,499. Tries with no first onset that leaves room for the span 6,692 / 6,463. Tries with no rhythm at the span 15,444 / 16,033. Spans given up 1,360 / 1,337.
- **Verse 1's one wholly drawn line** (its first, 15 syllables, the 7.5-and-over cell): 0.66 / 0.69 / 0.72 in both versions.
- **The choruses:** their 75th percentiles fall 0.05 to 0.10 short, where the slot end does not bind. That cause is not traced here. The chorus's second and third lines copy the bars of an earlier unit (361) in 92% and 100% of builds.

**Fix:** For lines drawn under 600, let the last onset run as late as the next line's first onset less the breath (212's 18 twelfths), not beat 3 of the last bar.

**Check:** Drawn lines' spans at the kept quartiles of their cell, within 0.05.

### 611. 600's gap values follow the span: the verse still sings half sixteenths; the chorus's drawn lines pass.

**Problem:** The verse is drawn from its cell's gap values but sung inside the old span, so its gaps cannot be the kept ones (610). Read on drawn lines (590), the chorus is within ten points on all three gaps. The dense lines' runs hold.

**Evidence** (main / control; kept: each line's cell, two-bar slots, weighted by gaps):

| Section | Sixteenth | Eighth | Quarter |
|---|---|---|---|
| Verse 1 | 50.1% / 51.4% (kept 37.9% / 35.8%) | 37.8% / 35.6% (48.3% / 50.2%) | 4.5% / 4.9% (3.9% / 4.1%) |
| Verse 2 | 51.4% / 52.1% (42.2% / 40.7%) | 36.7% / 35.1% (44.3% / 45.7%) | 4.5% / 5.1% (3.6% / 3.7%) |
| Bridge | 48.0% / 48.8% (32.3% / 29.9%) | 39.1% / 37.7% (53.3% / 55.5%) | 5.6% / 6.0% (4.3% / 4.5%) |
| Chorus 1, drawn lines | 15.1% / 15.9% (9.8% / 9.2%) | 56.6% / 52.6% (59.4% / 59.5%) | 15.7% / 17.3% (16.9% / 17.1%) |

Dense lines (nine notes or more at eight a bar and over): longest equal-gap run, 50th / 75th / 90th / 95th, 4 / 5 / 6 / 7 on both runs (kept median 4).

**Fix:** Follows 610.

**Check:** As 600's.

### 612. 601 moves the long lines' endings toward the kept share, but the rate drawn is not the rate sung.

**Problem:** The class is drawn at the rate the drawn span gives. Where the span is not met (610), the line is sung in less of its slot and so faster than drawn: a line drawn at 0.85 of its slot (about 8 notes a bar) is sung at 0.75 (about 9 to 10). It then carries the 8-to-10 share of class 0 into the 10-and-over cell.

**Evidence** (reachable drawn lines of 13 notes and over in two-bar slots, by the rate as sung; class 0; main / control):

| Rate as sung | Lines | v137 | v136 | Kept |
|---|---|---|---|---|
| Under 8 | 171 / 210 | 0.596 / 0.600 | 0.671 / 0.664 | 0.65 |
| 8 to 10 | 6,069 / 6,286 | 0.627 / 0.616 | 0.702 / 0.695 | 0.51 |
| 10 and over | 2,590 / 2,393 | 0.625 / 0.634 | 0.697 / 0.668 | 0.34 |
| All | 8,830 / 8,889 | 0.626 / 0.620 | 0.700 / 0.686 | 0.517 |

**Fix:** Follows 610. If the span cannot be met, draw the class again from the rate of the rhythm as placed.

**Check:** As 601's.

### 613. 602 lands: the verse's window ends on the tonic at the kept share for the chord under it.

**Problem:** None.

- The verse window's last note stands over B in every build, so the tonic is not a chord tone there, and it is the tonic 18.4% / 19.7% of the time (kept 19%).
- The window's last line returns the line before it, so the weight goes on that line's last note, read against the chord under the return.
- 262's rule that the first verse ends off the tonic is lifted for that note, by the writer's ruling (logged in intake.py). It, not 398, kept songs 42 to 48 under 3%.
- The chorus's window ends on the hook, a designed line, set aside in all 993 / 999 builds.

**Evidence** (main / control): tonic drawn 392 / 413 times, of which 39 / 28 found no move that reaches it and were drawn without the rule. Tonic not drawn 1,643 / 1,607. v136's figure was 2.3% / 2.3%.

**Fix:** None. For the paper: 262 to be read against 602, for every song.

**Check:** Printed.

### 614. 603 meets its leap test, but the mean interval stays wide: the leaps moved to fourths and fifths, and the verse repeats a note too seldom.

**Problem:** With leaps past a fifth held, the verse window's share of them fell to the kept figure. The mean interval is still 0.19 / 0.22 over the kept dense 1.94: some of the held leaps became fourths and fifths, and the verse repeats a note less often than kept dense windows do.

**Evidence** (Verse 1 window, main; kept: the 84 kept windows at 5.5 notes a bar and over):

| Move | v137 | v136 | Kept dense |
|---|---|---|---|
| Repeat | 27.8% | 27.4% | 32.5% |
| Step | 40.6% | 41.0% | 39.5% |
| Third | 19.4% | 18.4% | 18.2% |
| Fourth or fifth | 9.6% | 8.2% | 7.7% |
| Past a fifth | 2.5% (control 2.6%) | 5.0% | 2.2% |
| Mean interval | 2.13 (control 2.16) | 2.25 | 1.94 |

**Fix:** In dense lines, take the shares of the moves (repeat to past a fifth) from kept dense lines, not only the cap on the largest.

**Check:** As 603's.

### 615. 604: by the count, the hook is a net gain to the chorus, and the engine's own part of the chorus is about 2.9, not 1.6.

**Problem:** None; a reading, as 604 asks. The designed part was read by scoring each window again with its designed lines taken out, holding the form's two measures (empty bars, notes a bar) at the window's own values. The form's part is those two measures' share of the score; the rest is the engine's.

- In the chorus the hook costs in distinct pitches, interval size and its sixteenths, but it gives the window its range and spread. Net, it raises the score by 0.84 / 0.88.
- Window 157's reading, made by naming measures, put the engine's own part of the chorus near 1.6. The count puts it at 2.84 / 2.96.
- Caveat: taking the hook out also shortens the window's sung span, which moves the measures of range and peak.

**Evidence** (score less the band's kept mean, and its three parts; main / control; the measures' parts sum to the total):

| Section | Total | On designed lines | From the form | The rest |
|---|---|---|---|---|
| Verse 1, v137 | −0.76 / −0.69 | 0 / 0 | +0.11 / +0.09 | −0.87 / −0.78 |
| Chorus 1, v137 | −2.32 / −2.46 | +0.84 / +0.88 | −0.33 / −0.38 | −2.84 / −2.96 |
| Verse 1, v136 | −1.32 / −1.40 | 0 / 0 | +0.11 / +0.10 | −1.43 / −1.50 |
| Chorus 1, v136 | −2.26 / −2.32 | +0.92 / +0.97 | −0.35 / −0.39 | −2.83 / −2.90 |

The hook by measure, v137 main, in points as a cost:

- **Costs:** distinct pitches 1.70, mean interval 0.42, longest run one way 0.37, ascending 0.32, sixteenths 0.27, zigzag 0.26.
- **Gains:** range −1.82, pitch spread −0.59, turns per move −0.51, peak position −0.44, on the fifth −0.25, pitch bits −0.16.

The chorus's costliest measures as a whole (main): distinct pitches 0.82, sixteenths 0.69, last note tonic 0.39, empty bars 0.35, ascending 0.32, mean interval 0.28.

**Fix:** None.

**Check:** Printed for each section.

### 616. 557 by section: the verse comes six tenths nearer; the chorus does not move.

**Problem:** None; a reading.

**Evidence** (the judge of v132, not refitted; score less the band's kept mean; windows under the band's kept 5th; main / control):

| Window | v136 | v137 |
|---|---|---|
| Verse 1 | −1.32 / −1.40; 27.6% / 29.0% | −0.76 / −0.69; 14.5% / 10.0% |
| Chorus 1 | −2.26 / −2.32; 39.6% / 40.4% | −2.32 / −2.46; 43.1% / 45.6% |
| Both | −1.79 / −1.86; 33.6% / 34.7% | −1.54 / −1.57; 28.8% / 27.8% |

The verse's gain came from 602 and 603, not from 600:

- The last note's cost fell from 0.27 to 0.08 / 0.06.
- Leaps past a fifth left the twelve costliest measures.
- The mean interval's cost fell from 0.54 / 0.53 to 0.33 / 0.39.
- The sixteenths' cost rose a little, from 0.93 / 0.98 to 1.04 / 1.11.

**Fix:** None.

**Check:** Printed.

### 617. The run: survivors, deaths and the ports' counts.

**Problem:** One reading against a test: the main run has three join deaths at ('Verse 1', 3), over 577's two in a thousand.

**Evidence** (main / control):

- **Survivors:** 887 / 911 (v136 886 / 937). Orders 104d263b6bd6 / 25552792b7c3. Seed and designs as v134.
- **Design deaths:** the chorus above the verse 57 / 40 (v136 46 / 28); the bridge's build 3 / 2 (4 / 1).
- **Limit deaths:** 29 / 28 (44 / 20). Run_max 22 / 9; the longest notes in eight bars 15 / 3; memory 10 / 10; spectral 4 / 11; rhythm band 3 / 10.
- **Bridge opening unrelated:** 17 / 18 (14 / 11).
- **Join deaths:** 3 / 0 (1 / 0), all at ('Verse 1', 3). Walk deaths 4 / 1.
- **603:** leaps held in 10,007 moves (main).

**Fix:** None; the join deaths to be read again once 610 changes where the verse's lines end.

**Check:** As 577's.

### 618. The side run for 610 (not of record): with the slot end lifted the spans barely move; the breath before the next line is the deeper limit.

**Problem:** For lines drawn under 600, the side run let the last onset run to the slot's end less the breath, and dropped 406's landing weights while the span is held (gen_v137s_p58.py). The dense cells still fall short, for three reasons:

- **212's breath:** at least 18 twelfths from a line's last onset to the next line's first. In a two-bar slot that caps the span near 0.81, under the 7.5-and-over cell's kept median of 0.875. Kept dense lines breathe about an eighth (roughly 10 to 13 twelfths at the cell's median and 75th percentile); the verse's lines here take 18 / 21 / 27 at the quartiles.
- **465's class 0 with a pickup:** the line must be done by tick 72 for the next line to pick up into its last bar, and 601 draws that class at 51% for these lines.
- **Copied rhythms:** most verse and bridge lines take their rhythm from an earlier line, either a unit's bars (361) or verse 1 sung again, and inherit its span.

610's spans were read against the nominal two bars. Read as the kept table reads them, from a line's first onset to the next line's first onset, the shortfall is the same.

**Evidence** (main; drawn lines in two-bar slots; the span over the time to the next line's first onset; 25th / 50th / 75th):

| Cell | v136 | v137 | Side run | Kept |
|---|---|---|---|---|
| 6.5 to 7.5 | 0.70 / 0.75 / 0.79 | 0.69 / 0.73 / 0.79 | 0.72 / 0.76 / 0.79 | 0.77 / 0.79 / 0.86 |
| 7.5 and over | 0.72 / 0.77 / 0.80 | 0.71 / 0.77 / 0.79 | 0.72 / 0.77 / 0.80 | 0.81 / 0.88 / 0.90 |
| 3.5 to 4.5 | 0.44 / 0.50 / 0.56 | 0.41 / 0.49 / 0.56 | 0.42 / 0.50 / 0.60 | 0.44 / 0.53 / 0.64 |

The side run's other readings (main / control):

- **557:** verse −0.86 / −0.92; chorus −2.27 / −2.26; both windows −1.56 / −1.59. The verse sits a tenth or two under v137's run of record.
- **601, class 0 by the rate as sung:** 8 to 10 0.544 / 0.546 (kept 0.51, passes); 10 and over 0.663 / 0.661 (kept 0.34); under 8 0.368 / 0.344 (kept 0.65).
- **602:** 17.4% / 19.4% (kept 19%).
- **603:** past a fifth 2.5% / 2.3%; mean interval 2.13 / 2.23.
- **Gaps:** verse sixteenths 49.3% / 49.3% (kept for its cells 37.8% / 35.9%).
- **Survivors:** 866 / 910; orders 087dd81361f9 / 5468a5af6262. Limit deaths 50 / 33; the chorus above the verse 68 / 42.

**Fix:** For dense lines, take the breath before the next line from kept dense lines (about an eighth at the median) rather than 212's fixed 18 twelfths. Read 465's class 0 with a pickup against the span 600 draws. Let copied rhythms (361, sung again) keep their source's span only where the source met its own.

**Check:** As 600's, read from first onset to the next line's first onset.
