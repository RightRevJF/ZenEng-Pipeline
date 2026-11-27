# Judging research, run 07

26 November 2026, the evening pass (18:17 ET). For Jason.

## This pass in three sentences

For the first time, the research tested its ideas on whole songs: 5,901 songs that had never been looked at, taken from a large public set of MIDI files and matched by name to the covers database. Nine tests were frozen before any result was seen, including the pass's mathematics, a measure of how "tree-shaped" a song's form is. None passed: seven were killed and two are unsettled, and the chord-repetition lean that had held on Hooktheory clips for four passes turned the other way on these songs.

What it means: with these songs and these effect sizes, nothing in the notes alone has yet shown it can tell which songs other musicians take up. The next step is to settle two method questions (below) before building more measures.

## The experiments

Each test needed p below .05 ÷ 8 = .00625 (the ninth, written after seeing results, .05 ÷ 9), the predicted sign in both halves of the artists, and a matching sign in a second kind of model. Effects are in percentage points of "taken up by another artist" per standard deviation of the measure, comparing songs by the same artist. About 40% of these songs were taken up.

| Test | Idea | Predicted | Result | Verdict | Power |
|---|---|---|---|---|---|
| lakh_repetition | Chord repetition (the long-standing lean) | +1.0 | −1.93 (SE 1.34) | Killed | 0.01 |
| tree_h4m | Tree-shaped form (the mathematics) | −0.5 | +1.41 (SE 0.92) | Killed | 0.00 |
| spectral_gap | Your S = 1 + g/π on whole songs | −0.3 | +0.26 (SE 0.86) | Killed (weak) | 0.01 |
| lakh_chirality | Which way the chords turn on the circle of fifths | −0.6 | +0.30 (SE 0.76) | Killed (weak) | 0.00 |
| lakh_arrow | The arrow of time in the chords | +0.6 | −1.36 (SE 0.76) | Killed | 0.01 |
| loop_period | Length of the phrase that returns | +0.6 | +0.05 (SE 0.74) | Unsettled | 0.02 |
| burstiness | Chords returning in section-like bunches | +0.3 | +0.57 (SE 0.97) | Unsettled | 0.00 |
| triad_fidelity | How close the harmony sits to plain triads | +0.5 | −2.10 (SE 1.04) | Killed | 0.00 |
| cv_w_singletons | Contrast between sections, on other songs (after seeing results) | +1.5 | −0.13 (SE 0.81) | Killed | 0.06 |

**Power** is the chance a test would have passed if its prediction were exactly true, worked out on fake outcomes before the real ones were joined. Every one was near zero, so these kills are weak evidence; the strongest moves the odds by about four to one.

**Chord repetition.** On Hooktheory clips, songs whose chord patterns come back more often were taken up a little more (+1.0, then +1.3 on fresh clips). On these whole songs the sign reversed (−1.9), not significant. The repetition read from MIDI files is a different thing from Hooktheory's (they agree only weakly, 0.32), so the honest reading is "no effect shown", and the +1.0 prediction should be retired.

**Tree-shaped form.** Songs whose 4-bar stretches nest like a family tree were predicted to be taken up more. They were, if anything, taken up a little less (+1.4 on a measure where low means tree-like).

**Your formula S.** The spectral gap g measures how freely a song's chords mix. On clips it was too unstable to test; on whole songs it is stable, and it showed nothing (+0.26 against −0.3).

**Chirality and the arrow.** Both had looked possible on Hooktheory. On fresh whole songs chirality sits on zero, and the arrow went the wrong way for the third batch in a row.

**Loop period and burstiness.** Both unsettled: estimates near zero with wide error.

**Triad fidelity.** Songs closer to plain triads were taken up less (−2.1, p .044, not past the bar). This most likely reads how the MIDI arranger voiced the file, not the song.

**Contrast between sections.** One number printed beside the tree test looked strong (+3.1). It was tested on 3,436 other songs, by artists with one song each, and vanished (−0.13). It was a fluke of looking at many numbers.

## The mathematics: is a song shaped like a tree?

A mathematician named Gromov gave a test for how close any set of distances is to a tree. Take any four points and add up their distances in pairs, three ways. On a tree, the two largest sums are always equal.

*Worked example.* Four leaves on a tree, two on each branch, each leaf one step from its fork and the two forks two steps apart: the three pair sums are 4, 8 and 8. The two largest are equal, so the gap is zero: a perfect tree. Four corners of a unit square: the sums are 2, 2 and 2.83, so the gap is 0.41: not a tree.

For a song, each point is a 4-bar stretch of music, and the distance between two stretches is how different their notes are. Averaging the gap over thousands of random sets of four stretches gives one number per song (H4m). Low means the song's form nests like a family tree: sections, then variants, then phrases. Gilbert and Yim (card 1) proved how this average behaves and warned that it can look small just because all the distances are bunched together, so the spread of the distances was held in the test. Real songs are much more tree-like than their own bars shuffled at random (93 to 98% of songs), so the measure sees real structure. It just did not predict which songs other artists took up.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| G1 Tree-shaped statue (bar types) | Geometer | Merged into L1 |
| G2 Ring of 8-bar windows (sliding-window persistence) | Geometer | Withdrawn |
| G3 Your S on whole songs | Geometer | Killed (weak) |
| L1 Tree-shaped memory of phrases | Listener | Killed |
| L2 Loop period | Listener | Unsettled |
| L3 Little new after the first third | Listener | Withdrawn (repetition renamed) |
| I1 Phylogenetic form | Inventor | Merged into L1 |
| I2 Campfire fidelity | Inventor | Killed |
| I3 Kac burstiness | Inventor | Unsettled |

**Where they agreed:** one tree measure, not three; it must sit beside the spread of distances and chord repetition; a MIDI file belongs to a title, not to one artist (dropping shared files would have removed covers).
**Where they split:** how many tests to count. The Skeptic wanted two; your rule says every testable idea is tested and counted, so eight were.

## First principles

**The obstacle.** The effects being looked for are 1 to 2 points on a 40% outcome. Each fresh batch of songs gives an error of about 1 point, and MIDI files blur the measures. Seven passes and dozens of counted tests have found no pass from the notes alone.

**The way through (speculation).** First, two method rulings from you (in the fix list, R07-3): count only tests with a real chance of passing (power 0.2 or more), and kill a test only when its prediction falls outside its own error range. Second, chords rather than arrangements: a large chord corpus with artist and title. Third, number of versions instead of yes or no, which carries more per song.

**Deleted (recommended, nothing dropped without you):** chord repetition at +1.0, the tree measure, the spectral gap, chirality, the arrow, triad fidelity, loop period, burstiness, contrast, and tonic resistance (unsettled three times).

**Simplified:** one measure at a time, only at power 0.2 or more, which at this size means effects of about 1.5 points per SD.

## The papers

1. **Gilbert and Yim (2024), Hyperbolicity, slimness, and minsize, on average** [1]. Defines the average of five tree-likeness measures over random points and proves which averages bound which. It gave tonight's main measure and its warning about bunched distances.
2. **Perea and Harer (2015), Sliding windows and persistence** [2]. Proves that a periodic signal cut into overlapping windows traces a loop whose size, measured by topology, scores how periodic it is, and that the loop is roundest when the window matches the period. The ring test built on it was withdrawn by its author before testing (it read mostly noise); the loop-period test used its window-equals-period rule.

## The new data

The Lakh Pianoroll Dataset [3] (21,425 MIDI songs, matched to the Million Song Dataset), named through the Gold-Caps metadata [4], with Billboard chart flags from [5]. After removing songs already seen on Hooktheory, the McGill hold-out songs, files shared by different titles and karaoke or tribute acts, 5,901 songs by 1,678 artists with two or more songs remained. All are now seen. The joined table is on the research branch (`data/lakh_songs_discogs_run07.json`).

## Ideas for coming passes (could not be tested tonight)

- **The obtuse statue** (run 03, R03-G3): passes its stability check on whole songs; ranked ninth, so it waits for an unseen batch.
- **Tonic resistance:** needs a written key; MIDI has none.
- **Melody transport:** needs a separate melody line; these files mix it in.
- **The MusicLab ceiling** and **cross-genre breadth:** data not on hand.

## Paywalled papers

None this pass.

## Fix list

The proposed fix list for the maintainer is the Doc "Proposed fix list: judging research, run 07" (https://claude.ai/artifact/6VHFj6aQHoz8wUxRTwcMow). This report is the Doc "Judging research, run 07" (https://claude.ai/artifact/CMbhxVrSd5NP6gBPqRTWLR).

## References

1. Gilbert, A. C. and Yim, J.-H. (2024). Hyperbolicity, slimness, and minsize, on average. arXiv:2412.05746. https://arxiv.org/abs/2412.05746
2. Perea, J. A. and Harer, J. (2015). Sliding windows and persistence: an application of topological methods to signal analysis. Foundations of Computational Mathematics 15. arXiv:1307.6188. https://arxiv.org/abs/1307.6188
3. Dong, H.-W., Hsiao, W.-Y., Yang, L.-C. and Yang, Y.-H. (2018). Lakh Pianoroll Dataset (from Raffel's Lakh MIDI Dataset). Zenodo 5646574, CC BY 4.0. https://zenodo.org/records/5646574
4. Jonason, N., Casini, L. and Sturm, B. (2023). Gold-Caps LMD-matched (Million Song Dataset metadata). Zenodo 10178563, CC BY 4.0. https://zenodo.org/records/10178563
5. Zangerle, E. et al. (2019). Hit Song Prediction dataset. Zenodo 3258042. https://zenodo.org/records/3258042
6. Araz, R. O., Serra, X. and Bogdanov, D. (2024). Discogs-VI. Zenodo 13983028, CC BY-SA 4.0. https://zenodo.org/records/13983028
