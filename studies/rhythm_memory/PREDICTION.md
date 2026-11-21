# What gives a kept song's rhythm its long memory? The rule, written before the data is read

**The fault.** Rhythm scaling is low in every Luthier song (builds about 0.55 to 0.59; kept quartiles 0.61, 0.66, 0.72). It is the one check the songs fail together, and it falls further when the engine repeats more.

**What rhythm scaling is.** The sung tune's onsets are laid on a grid of sixteenths, a one where a note begins and a zero elsewhere, through the whole song, silences included. Rhythm scaling is how far the density of onsets keeps its memory across longer and longer spans (detrended fluctuation analysis). A shuffled song reads 0.51. A high reading means stretches where the singing is busy and stretches where it is sparse, lasting many bars.

**What was looked at before this rule was written:** the definition above (lib/luthier/scaling.py); the windows' medians of rhythm scaling; the songwriting session's 749.123 (Luthier's repeats come from far back, kept songs' from near). No kept song's rhythm was read against its rhythm scaling.

**Four things that might carry it,** each read on every kept 4/4 song:

1. **Slow change in how busy the singing is:** the spread, across windows of four bars, of onsets a bar, over the mean. (Sections that differ in how many notes a bar they sing.)
2. **Silence:** the share of bars, between the first and last sung note, in which nothing is sung.
3. **Near answers:** the share of bars sung on a rhythm heard within the eight bars before.
4. **Far returns:** the share of bars sung on a rhythm last heard more than sixteen bars before.

**The rule.** A thing **carries** rhythm scaling if its rank correlation with it across the kept songs is 0.30 or more in size and beats 99 in 100 shuffles. Then Luthier's songs (the builds of songs 55, 54 and 58 under Window 196, song 59 read beside them) are set against the kept songs on each thing that carries it. **The cause of the fault** is a thing that carries rhythm scaling and on which Luthier's builds stand outside the kept middle half on the low-scaling side in at least two of the three songs.

If nothing carries it, or Luthier stands with the kept songs on everything that does, the cause is not among these four and the study says so.

**Prediction, for the record:** 1 and 2 carry it; 3 a little; Luthier's songs change too little in how busy they are, because every line is drawn from the same windows into slots of the same length.

No change to the engine comes from this study. A mechanism, if one is found, gets its own rule and trial.
