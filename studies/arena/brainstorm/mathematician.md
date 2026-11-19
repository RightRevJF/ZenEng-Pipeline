# Mathematician: what is the right space for a song?

## 1. Diagnosis

Every failed test measured the **page** (tune and chords). Every surviving test measured the **recording**. The page is a function of the recording: you get it by throwing away voice, timbre, arrangement, timing and production. Information can only be lost by such a map, never gained. So the day's result is a clean statement: the part of greatness we can currently detect lives in what the page throws away.

In geometric terms, think of all recordings as a space sitting over the space of pages. Above each page is a **fibre** (the set of all ways to realise that page in sound). The cover yardstick makes this concrete: a covered song is one page with many points in its fibre. We searched the base space for a day and found nothing; the three signals that held are all fibre coordinates.

Why the three Hilbert-space attempts were wrong:

- **Hand-built six coordinates.** Not quotiented by the symmetries (transposition, tempo, octave, re-voicing), so two versions of one song landed far apart, and the distances between songs were mostly nuisance.
- **k-means regions.** Cutting a space into cells destroys the geometry you wanted to see; a path through cell labels has no shape, only a sequence.
- **Autoencoder.** It learns where songs are *dense*, so distance from its manifold measures unusualness. That was already tested as "newness" and scored zero on the page.

Deeper than all three: they looked for greatness as a function of one song alone. But the yardstick (still loved, much covered) is a statement about a song's **orbit** (the set of all its versions and re-uses) and about its place **relative to the population** of other songs. A function on single points cannot see either.

### The questions asked, answered briefly

**What are the symmetries?** Transposition (shift all pitches), time-stretch (tempo), time-shift, octave displacement of individual notes, re-voicing (which instrument plays what), and re-performance (everything a cover changes). The page is roughly the recording divided by the last two. Dividing by too few makes distances noise; dividing by all of them, which is what the page does, divided out the signal.

**What kind of object is a song?** Not a point and not only a path. The most useful picture is a **section of a bundle over time**: at each moment there is a page-state (melody note, chord) and above it a fibre-state (who is playing, how loud, how dense, how bright). Ideas 2 and 3 measure the fibre and how it moves as the page repeats.

**What does "great songs lie on a manifold" mean, exactly?** It means: there is a representation X of songs in which the probability distribution of great songs differs from that of good songs. The sharp test is a **two-sample test**: train any classifier (k-nearest-neighbour in the chosen metric is the honest one) to tell great from good in X, and score it on held-out songs. If it cannot beat chance, then great and good are the same cloud in X and no shape of any kind exists there: no manifold, no curvature, no topology. This is one test per candidate space, and it replaces forty tests of individual features. Any claim of "lower dimension" must also beat a matched control: random subsets of good songs of the same size, since any small sample looks low-dimensional.

## 2. Ideas, most promising first

### Idea 1. Orbit breadth: sharpen the yardstick before sharpening the ruler

**Plain words.** Counting covers measures fame as much as music. What the page should predict, if it predicts anything, is how *far* a song travels: across genres, across decades, and into versions with no words at all. A song covered by a bluegrass band, a jazz trio and a string quartet has shown that its identity survives large changes of sound. That is the mathematical content of "great tune", and it has not been used as the target.

**Mathematics.** For each work w with cover list {(performer_i, year_i, title_i)}:
- breadth B(w) = Shannon entropy of the genre labels of its cover performers, −Σ p_g log p_g;
- span T(w) = year of last cover minus year of first;
- tail exponent a(w): fit covers-per-year after release to t^(−a); small a means the song keeps being rediscovered;
- wordless share I(w) = fraction of covers by instrumental performers (orchestras, jazz instrumentalists, titles marked instrumental).
Regress each on log(cover count) and log(chart peak) and keep the residual. Re-run the best page features against the residuals.

**Data.** Cover lists: have. Performer genres: have for charting artists; the rest would need a MusicBrainz or Discogs genre dump (check GitHub and Zenodo mirrors).

**Wrong if** page features predict residual breadth and wordless share no better than they predicted the original grade (held-out rank correlation under 0.05).

**Odds.** 25%. The wordless share is also a direct test of the owner's claim that music moves people without words.

### Idea 2. The shape of the empty space

**Plain words.** The three sound findings say the same thing three ways: few bands filled, few events per second, a spectrum left open. The owner's statue comparison fits better than he may have meant: a statue is defined by the marble removed. Measure the holes in the arrangement, not the notes: how much room there is, how the room is distributed across sizes, and whether the melody sits inside a hole the accompaniment leaves for it.

**Mathematics.** From multi-track MIDI build a piano roll R[t, p] (1 if any pitched track sounds pitch p at sixteenth-note t).
- Fill F = mean of R over the song's active pitch range.
- **Lacunarity** (a standard measure of gappiness at each scale): slide an r-by-r box over R, let m be the count of filled cells in the box, and set L(r) = mean(m²) / mean(m)². Compute for r = 1, 2, 4, 8, 16; record L(4) and the slope of log L against log r.
- **Clearance**: identify the melody track (match it to the transcribed tune we already hold). For each melody note, count accompaniment notes sounding at the same time within 4 semitones. Average over notes; low is clear.
- **Turn-taking**: per beat, correlation between melody onsets and accompaniment onsets. Negative means they alternate.

**Data.** Multi-track MIDI for about 1,400 graded songs: have. Caveat: these are fan-made sequences, not the records; they keep the arrangement's layout but not its production.

**Wrong if** none of F, L, clearance, turn-taking reaches 0.08 on held-out songs after controlling for release year and genre. Year control matters: older records are sparser and have had longer to be covered, which could fake the whole sparse-spectrum result.

**Odds.** 20%.

### Idea 3. Holonomy of the return

**Plain words.** "Varied repetition" failed on the page, but there the test was whether the tune changes when it comes back. In most songs the tune does not change; what changes is everything around it. When the chorus returns, the page-state is the same and the sound-state is somewhere else. Holonomy (a geometer's word for "you went round a loop and did not come back where you started") measures that displacement. The guess: in great songs every return moves the sound in a consistent direction, so the song goes somewhere while repeating itself.

**Mathematics.** From MIDI, per bar b compute a 12-number pitch-class vector c_b. Self-similarity S[i, j] = max over the 12 transpositions of cosine(c_i, shifted c_j). Find repeated blocks: runs of 4 or more bars along a diagonal with mean S above 0.85. For each occurrence k of a repeated block compute a fibre vector f_k = (tracks active, notes per bar, pitch span, lowest pitch, highest pitch, drum hits per bar, mean velocity), standardised within the song. Displacements d_k = f_(k+1) − f_k.
- Size H = mean length of d_k.
- Coherence C = |Σ d_k| / Σ |d_k| (1 if every return moves the same way, near 0 if it wanders).
- Parallelism P = cosine between the mean displacement of the verse and of the chorus.

**Data.** MIDI: have. The real version needs time-resolved sound. The Million Song Dataset holds per-segment timbre and pitch vectors for a million recordings, and the SecondHandSongs cover set is keyed to it; worth checking whether a mirror is reachable from GitHub or Zenodo. That one dataset would unlock ideas 2, 3, 5 and 6 on real recordings.

**Wrong if** C, H and P all score under 0.05 on held-out songs, or songs with H near zero (returns identical) grade as well as the rest.

**Odds.** 20%.

### Idea 4. Where the cloud was heading

**Plain words.** "Sounds unlike its year" held, in any direction. But there are three different ways to be unlike: ahead of where music was going, off in a direction nobody followed, or behind. Influence was tested on tunes and failed; in sound it has not been separated out. Treat each year's hits as a cloud of points and ask how the cloud moved over the next decade.

**Mathematics.** Whiten the Spotify readings (18,000 hits) or Essentia numbers (3,500). For a song x released in year t:
- unusualness u(x) = −log density of x among hits of years t−2 to t+2 (k-nearest-neighbour estimate);
- drift score r(x) = log [ density among hits of t+3 to t+10 / density among hits of t−2 to t+2 ], estimated by a logistic classifier between the two groups;
- lonely score = u(x) with r(x) removed by regression.
Test which of r and the lonely score carries the +0.09.

**Data.** Have.

**Wrong if** r adds nothing beyond u (then great songs are not forerunners), or the lonely score adds nothing (then they are not inimitable). Either outcome is informative; only "both zero" is a dead end.

**Odds.** 20% that one of the two cleanly beats the plain measure.

### Idea 5. A metric taught by covers, and the identity margin

**Plain words.** The right distance between songs is one where two versions of the same song are close and different songs are far. We can learn it rather than guess it, wherever we hold two readings of one work. Then ask how much empty room surrounds each song in that metric. A song with a wide moat can be bent a long way and still be itself, which is what a much-covered song has demonstrated.

**Mathematics.** Same-work pairs: the three transcription sources of each tune; the same title under different artists and duplicate files in the Lakh set. Start from a descriptor already free of the simple symmetries: take the bar-by-pitch-class matrix in 16-bar windows, take the magnitude of its two-dimensional Fourier transform (which discards transposition and time-shift), and take the median over windows to get a vector v. Learn a linear map A minimising the triplet loss max(0, |Av_a − Av_p|² − |Av_a − Av_n|² + 1), where a and p are the same work and n is another. Distance d(x, y) = |Av_x − Av_y|. Margin M(x) = distance from x to its 5th-nearest different work, divided by the median same-work distance in the training pairs.

**Data.** Have. This differs from the failed "newness" test because A keeps only the directions that carry identity and squashes the ones performers change freely.

**Wrong if** M scores under 0.05 held-out, or equals raw-feature newness once A is replaced by the identity.

**Odds.** 12%. It is still a page measure, and the page has a poor record.

### Idea 6. The song as an operator: does it know which way time runs?

**Plain words.** A picture depends on the axes chosen; the spectrum of an operator does not. Treat the song as a rule that carries each moment to the next and study the rule. Two properties were not on the tested list. Irreversibility: does the song sound statistically different played backwards, that is, does it go somewhere? And transient growth: can the rule build tension before it settles, which only a lopsided ("non-normal") rule can do.

**Mathematics.** States: per beat, the pair (melody scale degree, chord root relative to key), merged to at most 20 states. Transition matrix P with add-half smoothing; stationary distribution q.
- Entropy production E = Σ q_i P_ij log( q_i P_ij / (q_j P_ji) ); zero exactly when forward and backward are indistinguishable.
- Spectral gap G = 1 − |second eigenvalue of P| (how fast the song forgets).
- Non-normality N = |P Pᵀ − Pᵀ P| / |P|² (Frobenius norms).
Report each as a z-score against 200 copies of the same song with its phrases shuffled, to remove the effect of song length.

**Data.** Have, for the page. Far better on time-resolved sound (see idea 3).

**Wrong if** z-scored E, G, N all sit under 0.05 held-out.

**Odds.** 8% on the page, perhaps 15% on real sound.

### Idea 7. Shape with no coordinates at all

**Plain words.** The owner's hunch stated literally, in the one form that needs no choice of axes. A song is a set of moments with distances between them; that is already a shape. Two such shapes can be compared directly, by asking how well the moments of one can be matched to the moments of the other while preserving distances. No Hilbert space is chosen, so none can be chosen wrongly.

**Mathematics.** For each song, bars are points; D[i, j] = transposition-minimised distance between bars i and j, combining pitch-class content and rhythm, scaled so the song's diameter is 1. Compare songs X and Y by **Gromov-Wasserstein distance** (the smallest average mismatch |D_X[i, k] − D_Y[j, l]| over soft matchings of bars; the Python Optimal Transport library computes it). This yields a distance between any two songs. Then run the two-sample test of section 1: k-nearest-neighbour classification of great against good on held-out songs.

**Data.** Have.

**Wrong if** the classifier's held-out accuracy is within sampling error of chance. That result would retire "greatness is the shape of the written song" for good, which is worth knowing.

**Odds.** 7%. Related tests (loops, persistence, form) already failed. I include it because it is the decisive version.

## 3. The wild idea: great songs are eigenvectors of the telephone game

Every time a song is sung from memory, taught, or covered, a transmission operator T is applied to it: some features are kept, some are smoothed away, some are replaced by whatever is easiest to remember and sing. Apply T hundreds of times and only what T leaves nearly unchanged survives: its slowest-decaying directions, the eigenvectors with eigenvalue near one. On this view greatness is not beauty at all but **fixedness under retelling**, and the yardstick (loved for decades, covered by many) is simply a count of how many applications of T the song has survived.

We hold samples of the far end of this process: folk tunes and hymn tunes have been through T for centuries. So fit a probability model to the folk and hymn corpus, in a representation free of key and tempo, and score each hit by how probable it is under that model *relative to* a model fitted to ordinary hits: score = log p_folk(x) − log p_hits(x). The prediction is that hits which already look like the end state of the telephone game are the ones that will be carried forward. A second, stranger test: simulate T directly (drop ornaments, snap rhythms to simple ratios, pull intervals toward steps, regularise phrase lengths), apply it ten times, and measure how far each tune moves. Great tunes should barely move. "Robustness under perturbation" failed, but random perturbation is not T; T has a direction.

I would not defend it in public because it says the great song is the one that was already worn smooth, which is the opposite of what the sound findings say (great recordings are unlike their neighbours). But both could be true at once: a worn-smooth page inside an unrepeatable fibre. That combination, tested as an interaction between the folk-likeness of the tune and the unusualness of the recording, is the single experiment I would most like to see run.
