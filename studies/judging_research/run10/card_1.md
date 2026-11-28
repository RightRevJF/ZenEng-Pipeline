# Card 1: Mijangos, Bravetti and Padilla (2022), intervallic transition graphs via persistent homology

## 1. Citation and copy read

Mijangos, M., Bravetti, A., and Padilla, P. "Musical Stylistic Analysis: A Study of Intervallic Transition Graphs via Persistent Homology." arXiv:2204.11139, v1 (the only version), submitted 23 April 2022. Categories: cs.SD, eess.AS, math.AT. The abs page gives no journal reference and no DOI. The authors are at IIMAS, UNAM, Mexico City.

Copy read: the arXiv HTML version (https://arxiv.org/html/2204.11139), dated 26 April 2022, plus the abs page for metadata. I read the whole text, from the abstract through Sections 1 to 6 and all 19 references, using WebFetch twice for the full account and the exact definitions and equations. The paper has no appendices.

Not reached: the code and full work list in the authors' GitHub repository (github.com/MartinMij/TDA-SQ). I also could not check the figures' numbers, because the results are shown only as plots (PCA scatters and dispersion bars).

## 2. Main construction and theorems

**Graph from the notes (Def. 19).** The analysis takes one instrument part at a time, such as the first violin.
- The 12 pitch classes are the nodes.
- Each step from one note to the next, i to j, adds the product of the two notes' durations (in seconds) to cell (i, j). Durations are first adjusted by Parncutt's 1994 pulse-salience and accent model.
- Dividing by the grand total gives a 12x12 matrix of transition probabilities p(i, j). Repeated pitches (self-loops) are kept.
- The matrix is the adjacency matrix of a weighted directed graph. The authors compute it with the MATLAB MIDI Toolbox.
- Despite the paper's name, the nodes are pitch classes, not intervals. An interval appears only implicitly, as an edge.

**From digraph to metric space (Defs. 17 and 18).**
- Each directed edge a to b gets a new middle vertex v_ab, joined to a and to b by two undirected edges of weight w(a,b)/2 each. A loop becomes a single edge of the same weight to its middle vertex.
- The length of a path is the sum of 1/weight over its edges. The distance between two vertices is the shortest path length, and is infinite if no path exists.
- Frequent transitions therefore make pitch classes close together.
- This step makes the directed graph symmetric. The authors list handling asymmetry directly, perhaps with Bregman divergences, as future work.

**Filtration and homology.** The pipeline is a Vietoris-Rips filtration on that finite metric space, with coefficients in Z2. Only H0 (components) and H1 (loops) are computed.

Each barcode is reduced to three numbers: the mean of the finite bar lengths, their standard deviation, and their persistent entropy. Infinite bars are given death m+1, where m is the largest finite death. That gives 4 instruments x 2 dimensions x 3 statistics, a 24-number vector per movement. The vectors go into a PCA plot.

"Dispersion" is the spread of one composer's points around that composer's centroid. As printed, the formula is missing the square on the norm.

**What is proved.** Nothing. Section 3 contains definitions only, with no lemma or theorem. No stability theorem is stated or cited. The authors offer no argument that small changes to the score give small changes to the barcode. They also give no reason for choosing 1/weight as length, or the m+1 rule.

My own observation (not in the paper): the H0 part of a Rips filtration on a shortest-path metric just records the minimum spanning tree's edge lengths. An unused pitch class becomes an extra infinite bar.

## 3. Is the measure from the notes?

Yes. It uses only symbolic pitch and duration from the score. The one outside ingredient is Parncutt's accent model, which reweights durations by metrical position. That model is still computed from the notes and the meter, not from any listener data.

## 4. Effect sizes and how checked

**Corpus.** 18 string-quartet movements, mostly minuets, scherzos or similar:
- 7 by Haydn (1771 to 1799)
- 6 by Mozart (1773 to 1790)
- 5 by Beethoven (1798 to 1825)

Section 5.2 adds four subgenres per composer (minuets, allegros, adagios and others). The text does not list those works.

**Results.** Dispersion rises from Haydn to Mozart to Beethoven. Minuets are the least dispersed subgenre and adagios the most. Two Mozart adagios were removed as outliers from one plot.

**Rest handling (Section 5.3).** Two options were tried on seven Haydn first-violin parts: dropping transitions across a rest, or down-weighting them by 1/(s/(uv)+1). Only one work changed noticeably. The authors call the method robust.

**Statistics.**
- No effect sizes are given in numbers.
- The text reports no PCA variance explained.
- There are no significance tests, confidence intervals, baselines or held-out data.
- There is no comparison with simpler features.

The composer ordering rests on reading figures for 5 to 7 points per group. It is then interpreted through Rosen's narrative of the Classical style. The evidence is weak and descriptive.

## 5. Lasting love and covers

The paper says nothing about popularity, endurance, listener preference or covers. Its target is stylistic consistency versus innovation.

The following is my extrapolation, not the paper's claim. "Low dispersion within a genre" could be read as a measure of how firmly a tune sits inside its type, for example how jig-like a jig is. Whether conformity or deviation goes with lasting love is an open question this paper cannot answer.

## 6. Methods or measures suggested for this pass

These measures are designed for TheSession.org settings. The input is the ordered list of notes (MIDI pitch, duration in beats). Grace notes and ABC ornament braces {} are removed, and ties are merged.

Defaults and invariances shared by all of them:
- **Weighting.** The parameter-free default is to weight each transition by **1** (a count), not by Parncutt-adjusted duration products. Parncutt's model has free parameters.
- **Units.** Use beats rather than seconds, so no tempo is needed.
- **Metric.** Keep the paper's 1/p metric, but do not add middle vertices. Symmetrize instead with p_sym(a,b) = p(a,b) + p(b,a). Adding middle vertices floods H0 with near-trivial bars.
- **Infinite bars.** Drop them instead of applying the m+1 rule.
- **Transposition.** Every graph measure here is transposition-invariant, because relabeling nodes does not change the graph's shape.
- **Tempo.** Count weighting is tempo-invariant. Duration weighting is too, after normalizing.
- **Length.** None of these measures is length-invariant. Longer tunes have more distinct transitions. Always compare within a tune type, or compute on a fixed window such as the first 16 bars or the A part only.

**Stability check for every measure.**
1. Take tunes with two or more settings.
2. Compute the measure on two settings chosen at random.
3. Report the Spearman rank correlation and the ICC across tunes.
4. Also compare the bottleneck distance between the two settings' barcodes with the distance between random pairs of tunes of the same type and mode.

A measure worth keeping should have ICC well above zero and smaller within-tune than between-tune distances.

My caution: 1/p is unbounded. A single variant note in one setting creates a rare transition with a huge distance. Tested on a stable feature like the MST total, that is a real source of instability.

**M1. MST spread of the pitch-transition graph (the H0 barcode).**
- How to compute:
  1. Count transitions between consecutive MIDI pitches, keeping octaves distinct. Irish tunes span about two octaves.
  2. Convert to p_sym, set the edge length to 1/p_sym, and take all-pairs shortest paths.
  3. Run Rips H0, which is the same as the minimum spanning tree.
  4. Report the mean and total of the finite bar lengths.
- Interpretation: a low value means a tightly knit pitch vocabulary that the tune keeps moving within.
- Might rename: the number of distinct pitches (it sets the bar count) and the transition entropy. Regress on both and keep only the residual.

**M2. H1 loop count and total persistence of the same metric space.**
- How to compute: Rips H1 on the shortest-path distance matrix, for example with ripser. There are no parameters. Report the number of bars and the sum of their lengths.
- Interpretation: it captures circuits of pitch movement that are not filled in by shortcuts, such as a run up and a leap back.
- Might rename: the cycle rank of the undirected graph (distinct undirected transitions minus distinct pitches plus 1). Always report the correlation with that count. If it is above 0.9, the topology adds nothing.

**M3. A truly intervallic transition graph.**
- How to compute:
  1. Turn the melody into its interval sequence (semitone differences).
  2. The nodes are the distinct intervals. The edges are consecutive interval pairs, by count.
  3. Apply the same 1/p metric, H0 and H1, and the persistent entropy of the finite H0 bars (the paper's Eq. 24 without the infinite-bar rule).
- Invariances: transposition-invariant by construction, and closer to motif shape than M1.
- Might rename: the number of distinct intervals, interval entropy, and the bigram entropy of intervals.

**M4. Persistent entropy of the H0 barcode as an evenness score.**
- How to compute: with the finite H0 bar lengths l_i from M1, set q_i = l_i / sum(l), then E = -sum(q_i log q_i). Normalize by log(number of bars) so that tunes with different pitch counts are comparable.
- Interpretation: it is high when all the pitch "links" are about equally strong, and low when a few weak links hang off a strong core. A weak link might be a rare high note.
- Might rename: the evenness of the pitch distribution. Check against the normalized pitch entropy.

**M5. Within-type dispersion, the paper's own statistic repurposed.**
- How to compute:
  1. Build a vector for each tune from M1 to M4, z-scored within the tune type.
  2. Measure the distance from the tune to its type's centroid, the median over its settings.
  3. Also measure setting-to-setting dispersion within a tune, the paper's dispersion applied to settings.
- Interpretation: the first is a "typicality" score. The second is a measure of transcription agreement that could be tested against popularity. That test is my extrapolation: tunes many people play may gather more, and more varied, settings.
- Might rename: the setting count, and note count through length. Control for both.

## 7. Leads

1. Grant, Knights, Padilla, Tidhar, "Network-theoretic analysis of Haydn's string quartets," J. Mathematics and Music 16(1):18-28, 2022 (DOI not checked). This is the network-statistics version of the same transition graphs. It is a non-topological baseline worth comparing against.
2. Padilla, Knights, Ruiz Tarrío, Tidhar, "Identification and evolution of musical style I: hierarchical transition networks and their modular structure," MCM 2017, Springer LNCS, pp. 259-278 (DOI not checked). It is the source of the transition-matrix construction.
3. Bergomi and Baratè, "Homological persistence in time series: an application to music classification," J. Mathematics and Music 14(2):204-221, 2020 (DOI not checked). It applies persistence to melodies as time series, an alternative filtration to try.
4. Rucco, Castiglione, Merelli, Pettini, "Characterisation of the idiotypic immune network through persistent entropy," ECCS 2014 proceedings, Springer, 2016 (DOI not checked). It is the source of the persistent-entropy summary used here.
5. My addition, not cited by the paper: Chazal, Cohen-Steiner, Guibas, Mémoli, Oudot, "Gromov-Hausdorff stable signatures for shapes using persistence," Computer Graphics Forum 28(5), 2009 (DOI not checked). It gives the stability theorem the paper lacks: Rips barcodes move no more than the metric does. It is the basis for a bottleneck-distance check between settings.
