# Judging research, run 05

25 November 2026. Research only: nothing here goes into the Luthier engine or main. Song 59 and its folders were not read. The McGill hold-out was not touched.

## Tonight in three sentences

Tonight found the notes of every Hooktheory song at a public address, so eight new ideas could be tested on all 9,588 songs whose artist has two or more songs, against one question: did another artist ever release the song? The main mathematical idea, measuring how truly a song's chords go round in a circle with persistent homology, was killed, and so were three others; three more leaned the predicted way without reaching the bar. The most promising lean, chords that move in one direction rather than back and forth, reversed on 3,212 new songs, so tonight leaves no finding, only a clearer map of where the notes stop helping.

## The experiments

Seven tests were frozen before any outcome was joined (commit 1f6c36d), so each needed p < .05/7 = .0071. An eighth was frozen after seeing those seven (commit 2bfd4ca) and needed p < .05/8 = .0063. A pass also needed the same sign in both halves of the artists and in a second model (conditional logit).

The outcome, "taken up by another artist", is whether the song's Discogs-VI group holds a release by performers who share no name with the original artist. About 22% of these songs qualify. Every effect is in percentage points per standard deviation of the measure, compared only among the same artist's songs.

| Test | Prediction written first | Result | Verdict | Power |
|---|---|---|---|---|
| 1. Certified chord loop (persistent homology) | +0.8 | **−0.20** (SE 0.44, p .64); halves +1.39 and −1.62 | Killed | 0.19 |
| 2. Arrow of time: chords go round, not back and forth | +0.6 | **+0.84** (SE 0.40, p .035); halves +0.78 and +0.84 | Unsettled | 0.12 |
| 3. Harmonic freedom: how many chords fit the tune | +0.6 | **−0.23** (SE 0.41, p .58) | Killed | 0.11 |
| 4. Melody range (narrower is easier to sing) | −0.7 | **−0.42** (SE 0.26, p .11); halves −0.33 and −0.52 | Unsettled | 0.49 |
| 5. Fifths path (run 03's idea, new outcome) | −0.6 | **+0.015** (SE 0.32, p .96) | Killed | 0.21 |
| 6. Tonic resistance (run 03's idea, new outcome) | −0.6 | **−0.23** (SE 0.44, p .61) | Unsettled | 0.09 |
| 7. Fame against the notes (the Skeptic's test) | Fame predicts more than the notes | Fame AUC 0.48, notes 0.69 | Killed (proxy broken) | n/a |
| 8. Arrow of time on single-song artists (after seeing results) | +0.6 | **−1.75** (SE 0.67, p .009) | Killed (opposite sign) | 0.03 |

Power is the chance of passing if the prediction were exactly true, computed from each test's own standard error.

**1. The certified chord loop.** This was the night's mathematics (explained below). Songs whose chords make a clean, certifiable circle were predicted to be taken up more. They were not: the estimate is slightly negative, and the predicted +0.8 lies outside its 95% range. The two halves of the artists disagreed sharply (+1.39 against −1.62), which says the measure is noisy in a way no single number captures.

**2. The arrow of time.** This borrows an idea from physics. A process in "detailed balance" looks the same played backwards; one with an arrow of time does not. I–V–vi–IV goes round one way and scores 1. A I–IV vamp swings back and forth and scores near 0. Within artist, songs with more direction leaned towards being taken up (+0.84), with both halves and the second model agreeing, but p was .035, not below .0071.

**3. Harmonic freedom.** The Inventor's idea from evolution: a tune that many chords fit lets a coverer re-harmonise it. It came out slightly negative and was killed.

**4. Melody range.** The Listener's idea: a tune an ordinary voice can sing is easier for others to take up. Narrower tunes did lean that way (−0.42), in both halves, but not far enough. Among songs already covered, wider tunes had slightly more coverers (+0.063, p .042, reported only), the opposite lean. This is the same two-faced pattern run 04 saw for chord repetition.

**5 and 6. Run 03's two geometry measures, retested.** The fifths path (how far each chord change travels round the circle of fifths) did nothing (+0.015). Tonic resistance (how central the home chord is in the song's chord network, measured like electrical resistance) leaned the predicted way by a hair, 0.03 short of its kill line, with power 0.09. It is unsettled and the review recommends retiring it.

**7. Fame against the notes.** Tonight's counter-evidence paper (below) found that an artist's past chart success predicts a new hit about as well as a whole model of the sound. The Skeptic predicted the same here. It failed for a dull reason: the fame proxy on hand, the artist's number of songs on Hooktheory, is topped by game studios and library composers, so it scored worse than a coin toss (AUC 0.48). The notes' better score (0.69) was about 97% style: sung pop against instrumental themes. So this test says little about real fame, and it taught that the corpus is not hits only.

**8. The arrow of time on new songs.** After seeing test 2, the reviewer froze one more test on the 3,212 songs by artists with a single song, the only songs on disk whose outcome had never been modelled. Direction went the other way: −1.75 (p .009), killed by its rule. With one song per artist the comparison is across artists, so it may read genre (vamp-based styles get covered) more than anything a writer controls. Either way, test 2's lean did not carry to new songs.

**One more thing every model showed.** Chord repetition sat in every model as a control, and every time it leaned towards being taken up (+1.0 to +1.5 per SD). These are the same songs run 04 used, so this is the same lead seen again, not new evidence.

## The mathematics, plainly

**Turning a song into a shape.** Write down, every half beat, which of the 12 notes the current chord holds. Now take a "snapshot": nine glimpses of that strip spread across two bars, stacked into one long list of numbers. That list is a single point in a space with many directions. Slide forward a quarter beat and take the next snapshot. A section becomes a cloud of a few hundred points.

**Why a loop makes a ring.** If the chords go round and come back, the snapshots come back to where they started, so the cloud lies on a closed ring, like beads on a necklace. Persistent homology measures the ring's hole. Picture a bubble growing round every bead. When neighbouring bubbles touch, the necklace closes and a hole appears. Keep growing them, and eventually they fill the middle and the hole vanishes. The longer the hole lasts, the more real the loop.

**What tonight's paper added.** Park and colleagues prove that a truly periodic signal gives exactly one such hole, born at once and lasting at least a known amount, and that a non-periodic one gives none early. They also give a way to say how sure we are: drop 1% of the beads, many times, and see how far a dropped bead can be from the rest. Double that distance and you have an uncertainty radius. A hole counts as certified only if it outlasts twice that radius. What is left over is the margin.

**Worked example** (16 bars in C, one chord per bar):

| Progression | Hole lasts | Twice the uncertainty | Margin |
|---|---|---|---|
| I–V–vi–IV, four times round (C, G, Am, F) | 0.770 | 0.528 | **0.242** |
| I–IV back and forth, eight times (C, F, C, F) | 0.740 | 0.725 | **0.016** |
| One chord held throughout | nothing moves | | no value |

The back-and-forth makes almost as big a hole, but its beads bunch up at the two chords with few in between, so the uncertainty swallows nearly all of it. Mathematically it is closer to a line segment than a circle.

**The bet, and what happened.** The paper's stability theorem says any disturbance smaller than half the margin cannot break the circle. A cover is such a disturbance: new voicings, tempo and instruments. So the imaginers bet that songs with a big margin survive re-dressing and get taken up more. The mathematics worked exactly as proved; the songs did not care. A clean circle in chord space did not predict being recorded by someone else.

**The arrow of time, the night's other mathematics.** For each move from chord X to chord Y, count how often the song makes the reverse move. A = 1 minus the share of moves matched by a reverse. In the table above, I–V–vi–IV scores 1.00 and I–IV scores 0.07. Physicists use the same count to tell a living process from one at rest. It leaned the right way within artist and the wrong way on new songs.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| G1 = L1 = I1: certified chord loop margin | Geometer, Listener, Inventor | Tested: killed |
| G2 back-and-forth share | Geometer | Merged into I3 (ρ −0.96) |
| I3 arrow of time (detailed balance) | Inventor | Tested: unsettled; then killed on new songs |
| I2 harmonic freedom | Inventor | Tested: killed |
| L2 melody range | Listener | Tested: unsettled |
| L3 contour surprise | Listener | Withdrawn (it measured transcription habits) |
| Fame against the notes | Skeptic | Tested: killed (broken proxy) |
| Fifths path and diatonicity (run 03, run 04) | backlog | Tested: killed |
| Tonic resistance (run 03) | backlog | Tested: unsettled; retire recommended |
| Loop thickness, melody loop, second hole, and two more | Geometer, Listener | Stopped on the notes (unstable between clips) |

**Agreed:** all three imaginers independently reached for the same measure, the certified loop margin, and accepted one frozen version. Card 1's own suggested "loop thickness" turned out to be chord repetition and length in disguise. The back-and-forth share and the arrow of time are one number seen from two sides.

**Split:** the imaginers read the loop margin as robustness that invites re-recording; the Skeptic warned it might only attract karaoke and cover factories (it turned out that no song's result rested on a karaoke or tribute release alone). The Skeptic alone predicted that fame would swamp the notes.

## First principles

**The obstacle.** Every song with an outcome on disk has now been looked at, and the effects the notes can carry (about 1 point per SD on a 22% outcome) sit right at the edge of what one test on seen songs can show at tonight's bar. The single fresh check tonight (test 8) contradicted the best lean.

**The way through (partly speculation).**
- Fresh songs by the same artists: re-match the Hooktheory clips the data pack leaves out to Discogs-VI, then test a small frozen set (chord repetition, direction, melody range) once, at one threshold, rule committed first.
- For Jason's geometry, the useful mathematics may be *dynamics* rather than *shape*: not what figure the chords draw, but how they flow. Detailed balance is the first step towards "entropy production" on the chord chain, a graded measure of how far a song is from running the same backwards. It should be checked on the notes first.

**Deleted (recommended; Jason decides):**
- the certified loop margin and its whole persistent-homology family;
- harmonic freedom;
- the fifths path, with diatonicity (closes run 03's idea);
- the Hooktheory song count as a fame measure;
- contour surprise (withdrawn).
Tonic resistance is recommended for retirement.

**Simplified:** the best idea left was direction, in its plainest form: the share of chord changes that step straight back. It is unrelated to chord repetition. After test 8 it is weaker than it looked.

**Flagged:**
- The corpus is not hits only: across-artist comparisons mix pop with game and library music.
- The power estimates made before each test overstated the noise by a third or more; a dry run on a fake outcome gives a truer figure.
- The engine's loop-less trial still rests on cover counts among songs already covered; on being taken up at all, repetition leans the other way.

## The papers

1. **Park, An, Kim & Kim (2025, revised 2026), "Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings"** [1], arXiv 2512.06324 (mathematical statistics); read in full from the arXiv HTML. It proves that the snapshot cloud of a smooth periodic signal is a clean circle with one long-lived hole of guaranteed size, and that a non-periodic signal gives no early hole. A subsampling radius turns this into a test with controlled error rates. It assumes smooth signals sampled densely; chord changes are steps, which is why tonight blurred them. It says nothing about songs or two-cycle (torus) shapes. It replaced Perea and Harer's founding paper, which could not be read in full tonight.
2. **Interiano, Kazemi, Wang, Yang, Yu & Komarova (2018), "Musical trends and predictability of success in contemporary songs in and out of the top charts"** [2], Royal Society Open Science; read in full from the University of California repository copy. On UK releases from 1985 to 2015, a forest of audio descriptors (mood, timbre, genre) predicted chart entry at 0.69 to 0.75 accuracy on balanced data; adding whether the artist had charted in the past five years raised it to 0.82 to 0.86. The features are sound, not notes, and the outcome is chart entry, not lasting love or covers. It cuts against judging from the notes mainly by showing how much the artist carries, which is why this project compares songs within artist.

## Ideas for coming nights (not testable tonight)

- **Fresh within-artist songs** (the way through): needs the Discogs-VI `main.zip` re-match (Zenodo, 1.4 GB, reachable from here) of the songs the data pack leaves out; proposed as R05-2.
- **Entropy production on the chord chain:** a new measure; it should first pass a stability check on the notes, then wait for fresh songs rather than spend more seen ones.
- **Torus shapes (two cycles at once):** need Gakhar and Perea's paper, which could not be read tonight.
- **The ceiling (MusicLab) and covers across genres:** data not on hand (`run05/DATA.md`).
- **A real fame measure:** needs chart data per artist, not on hand.

## Papers you could drop in the "Judging research inbox" Drive folder

Neither is paywalled; both are free on arXiv, but only as PDFs, which this unattended run could not read. A copy in the inbox would let a coming night read them in full.
- Perea, J. A. & Harer, J. (2015). Sliding Windows and Persistence: An Application of Topological Methods to Signal Analysis. Foundations of Computational Mathematics 15, 799–838. doi:10.1007/s10208-014-9206-z (arXiv 1307.6188).
- Gakhar, H. & Perea, J. A. (2023/2024). Sliding window persistence of quasiperiodic functions. Journal of Applied and Computational Topology. arXiv 2103.04540.

## The proposed fix list

See the separate Doc "Proposed fix list: judging research, run 05" (https://claude.ai/artifact/Uihh8u39QUGNC4mFoNmYry); the same text is in `run05/proposed_fixlist.md`. This report is published as the Doc "Judging research, run 05" (https://claude.ai/artifact/FFmtD1g9RKS9xczCyUPsqQ).

## Housekeeping

During the brainstorm, one helper agent published its notes by mistake as a private artifact titled "r2_listener.md" (visible only to Jason). Nothing in it is sensitive; it can be deleted from the artifacts gallery, or left.

## References

1. Park, D., An, J., Kim, T. & Kim, J. (2025; v4 2026). Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings. arXiv 2512.06324. https://arxiv.org/abs/2512.06324
2. Interiano, M., Kazemi, K., Wang, L., Yang, J., Yu, Z. & Komarova, N. L. (2018). Musical trends and predictability of success in contemporary songs in and out of the top charts. Royal Society Open Science 5, 171274. https://doi.org/10.1098/rsos.171274
3. Perea, J. A. & Harer, J. (2015). Sliding Windows and Persistence. Foundations of Computational Mathematics 15, 799–838. https://arxiv.org/abs/1307.6188
4. The maintainer's within-artist test: `studies/judging_checks/within_artist/RESULT.md` on main (−0.042, p .009).
5. Run 05 commits on judging-research: 1f6c36d (predictions), 3df4b7f (seven results), 2bfd4ca (eighth prediction), 537f894 (eighth result and first principles).
6. Data: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0, fetched from github.com/chrisdonahue/sheetsage-data; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
