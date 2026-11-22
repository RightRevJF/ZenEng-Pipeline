# Checks on the judging research, nights one and two: rules written before anything is run

The nightly judging research proposes ideas; nothing of it is in the engine. Two of its claims can be checked today on data in this repo, with no outcome (no covers, views or chart figures) read.

## A. The spectral gap g: do I get the chair's numbers, and is g stable within a song?

**Seen before writing:** the chair's table in run 02 (721 of 739 McGill songs kept; g against within-section repetition −0.26; against distinct chords +0.02; against E +0.47; median g 0.19, middle half 0.09 to 0.30; 8.7% of songs under 0.01). The chair's script was a scratch file and is not in the repo, so those figures cannot be reproduced from what is committed. The chair also named the check it did not run: whether g on a song's first half agrees with g on its second half.

**What is done.** g is built again from the chair's written rules alone (`gap.py`): tokens = Roman numeral with quality, plus a 7 where the chart flags one; no-chord marks dropped; a chord repeating the one before merged; all sections in performed order joined; moves counted, rows normalised, the last chord joined to the first; g = 1 − |λ2|. Within-section repetition = the share of a section's chord 3-grams already heard earlier in that section, first instance of each section letter, sections of at least 4 merged chords, weighted by bars.

**Prediction 1 (reproduction).** Songs kept within 10 of 721; Spearman of g with repetition within 0.05 of −0.26; with distinct chords within 0.05 of +0.02; median g within 0.03 of 0.19. If any is outside, the chair's figures do not reproduce from its own written rules, and I say so.

**Prediction 2 (stability, new).** Each song's merged sequence is cut at its midpoint; g is built on each half by the same rules (halves with fewer than 4 merged chords or 2 distinct chords dropped). Read: Spearman between the two halves' g. Beside it, the same split for two plain measures: distinct chords, and the share of chord 3-grams already heard earlier in the half.
- I expect g's halves to agree weakly: Spearman between 0.15 and 0.45. On a graph of 6 to 10 chords one unusual move shifts λ2.
- I expect the plain measures to agree better: distinct chords over 0.6, repetition over 0.4.
- **What it would mean.** Under 0.3: g is mostly noise at song length and should not go near an outcome. 0.3 to 0.5: weak; usable only with a large sample. Over 0.5: stable enough to test. A measure cannot predict covers better than it predicts itself.

## B. The reading J1 says can go ahead: do Luthier's sections loop more than kept sections?

**Seen before writing:** song 58's record, whose verse runs I V four times, then V, then I V four times, then V; so I expect its verse to read high. Nothing else of the readings.

**What is done** (`loops.py`). Within-section chord repetition, by the same rule as A, for the first verse, first chorus and bridge of songs 55, 54, 58 and 60 (song 59 read beside them and deciding nothing), from each record's Roman numerals; and for McGill sections labelled verse, chorus and bridge (first instance of each letter). The kept quartiles by part, and where each Luthier section stands.

**Prediction.** Luthier's verses stand at or over the kept middle in at least three of the four songs, and at least one stands over the kept 75th. Choruses I do not know. If Luthier's sections stand inside the kept middle half throughout, J1 has nothing to act on in these songs.

**What this cannot say.** Whether looping less would make a song more covered. That is the judging research's R02-1 (within-artist) test, which needs data not on this machine.
