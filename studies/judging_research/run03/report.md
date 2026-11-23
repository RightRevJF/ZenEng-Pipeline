# Judging research, run 03

23 November 2026. Research only: nothing here goes into the Luthier engine or main. Song 59 and its folders were not read. The McGill hold-out was not touched.

## Tonight in three sentences

Tonight tested two shapes from geometry on the chord maps of 1,924 hit songs, each compared only with the same artist's other songs: whether a song's chords contain a "bridge" (a move nothing else can replace), and how "curved" the walk through its chords is. Both were killed by rules written down before any cover count was looked at: songs with a bridge were covered slightly more, not less, and curvature predicted nothing once song size, chord repetition and chord surprise were held. The mathematics was computed correctly and every theorem checked out on every song, but the chord maps of these short transcriptions are too small for curvature to mean anything except how many chords a song uses, so geometry has to move to a bigger, fixed space.

## The experiments

### 1. The bridge (bold new idea)
**Idea.** Draw a song as a map: chords are places, and a road joins two chords whenever the song moves between them. A bridge is a road you cannot avoid; take it away and the map falls in two. The guess was that a cover artist cannot re-route such a move, so a song with a bridge leaves less room to re-arrange and gets covered less.

**Prediction, written first** (committed ad201ad before any outcome): within each artist's own songs, a song with a bridge is covered less, by 0.025 of a standard deviation per standard deviation of the bridge flag. Killed if the estimate came out above −0.01.

**Result.** +0.021 (standard error 0.016, p .21; 95% range −0.011 to +0.053), 1,924 songs, 420 artists. Both halves of the artists leaned the same wrong way (+0.034 and +0.008). **Killed.** Power to see the predicted effect was only 0.24, but a true −0.025 would almost never land at +0.021 (2.8 standard errors away), so the kill means something. About 31% of songs have a bridge, and the share rises with how many sections were transcribed, which is a warning about the maps themselves.

### 2. Curvature of the chord walk (builds on the spectral gap)
**Idea.** Ollivier's curvature asks: if a listener is at chord x or at the neighbouring chord y, do they expect much the same next chord? If so, x and y can stand in for each other, and a re-arranger can swap them. The guess was that songs with more of that "stand-in" curvature get covered more, beyond what size, chord repetition and chord surprise already explain.

**Prediction, written first:** +0.02 per standard deviation, within artist, with size, repetition and surprise held. Killed if zero or below, or if most of it turned out to be chord surprise.

**Result.** −0.0002 (standard error 0.029, p .995), same songs. Halves +0.001 and −0.001. **Killed.** Without chord surprise in the model it was +0.020 (p .48), so the little there was belonged to surprise. Power was only 0.06, so this says the effect is not large, not that it is exactly zero.

### What else the experiments showed (deciding nothing)
- The spectral gap, the one geometric measure that had passed its checks on the McGill whole-song charts, fails its stability check on these short Hooktheory clips: two clips of the same song agree only 0.17. It is kept out of every model on these songs. Jason's S = 1 + g/π only rescales g, so it falls with it here.
- **Not a test, labelled as such:** in the curvature model, chord repetition came out at −0.061 and chord surprise at −0.089, both stronger than the maintainer's −0.042. Songs that loop less also tend to surprise more (they correlate −0.29), and the two pull covers in opposite directions, so each may hide the other. This came from a model built for another question, so it is a lead for a rule-first test, not evidence.

## The mathematics, plainly

**Curvature without a surface.** On a ball, two people who start walking north side by side come together at the pole: positive curvature. On a saddle they drift apart: negative. Ollivier (2009) found a way to say this for any random walk, even one that hops between a handful of chords. Take two neighbouring chords. Look at where the song is likely to go next from each. If those two clouds of next chords overlap a lot, the cost of moving one cloud onto the other is small, and the curvature is positive. The theorem that makes it useful: if every move in a song has positive curvature, the walk forgets where it started at least that fast (the spectral gap is at least the smallest curvature). That theorem held on every one of the 2,672 songs.

**A worked example** (with the walk allowed to pause half the time, as the theory needs):

| Chord map | Curvature of each move |
|---|---|
| Three chords in a ring, I → IV → V → I | 0.5 |
| Four chords in a ring, I → V → vi → IV → I | 0 |
| A hub, I, joined to IV, V, vi and ii | 0.25 |
| Four chords all joined to each other | 0.67 |

The lesson is in the second row. The four-chord loop that runs through half of pop is perfectly flat. Curvature on maps this small mostly counts triangles: whether a chord's neighbours are also each other's neighbours. So on a song of 5 or 6 chords, curvature is mostly a measure of how many chords there are and how they repeat (size explained 46% of it). That is why it added nothing.

**The bridge, as electricity.** Devriendt and Lambiotte (2022) treat the chord map as an electrical circuit: each road a wire. The effective resistance between two chords is how hard it is to push current from one to the other. A road whose resistance equals that of its own wire carries all the current: no other path exists. That is exactly a bridge. Their curvature also places the chords as corners of a shape in a high-dimensional space (a literal "song in a Hilbert space"), but on these small maps its average is fixed at one over the number of chords, so only its spread could carry news.

**What it means.** The mathematics was right; the objects were too small. A geometry built from a dozen chord moves mostly measures size and repetition. A geometry that could survive is one where the space is fixed in advance and the song is a path through it: for example Tymoczko's voice-leading space, or the circle of fifths given by the Fourier phases of each chord. There a short song gives a noisier reading of the same shape, not a different shape.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| G1 Curvature beyond the vocabulary (shuffle-relative) | Geometer | Merged into L1; tracks repetition (−0.52 to −0.62); reported only |
| G2 Out-and-back links: the bridge | Geometer | Tested tonight with L2: **failed** |
| G3 The obtuse statue (circumcentre outside the shape) | Geometer | Untested; ranked later |
| L1 Substitutable chords: Ollivier curvature | Listener | Tested tonight: **failed** |
| L2 No detour: traffic on bridges | Listener | Merged into the bridge test: **failed** |
| L3 Curvature × repetition | Listener | Withdrawn (no power) |
| I1 The melody as a contraction of the harmony | Inventor | Untested; ranked later in a simpler form |
| I2 Tonic resistance: is home the hub? | Inventor | Untested; passed its surprise gate; ranked later |
| I3 The cover done on the computer | Inventor | Withdrawn (leaned on the gap) |

**Agreed:** on tiny chord maps curvature mostly measures size, so every geometric measure must be compared against size and must hold the number of transcribed clips. **Split:** the Geometer wanted to remove size by shuffling the song's own chords; the Listener by statistics. The shuffled version turned out to be chord repetition renamed, so the Listener's version was tested. The Geometer would have rescued the spectral gap with the McGill rule; the chair ran that gate without any outcome and the gap failed.

## First principles

**The obstacle.** The one real signal is small (chords that move: about 0.04 of a standard deviation within artist), every song on disk has now been looked at, and geometry built from a song's dozen chord moves mostly measures size and repetition.

**The way through (partly speculation).** Get fresh songs in bulk: about 10,400 Hooktheory songs with chord measures are not yet matched to Discogs-VI and could be matched by a rule fixed in advance, without looking at cover counts. Freeze one two-term rule (chord repetition and chord surprise together) before joining covers, and do not join until there are at least 2,000 songs. Move geometry into a fixed space (voice-leading or the circle of fifths) or onto McGill's whole-song maps, and check its stability before any outcome.

**Deleted (recommended; Jason decides):** the bridge flag and traffic on bridges (wrong sign); mean Ollivier curvature (zero; what little there was belonged to surprise); shuffle-relative curvature (repetition renamed); the spectral gap on Hooktheory songs (unstable); S = 1 + g/π as a test of its own on these songs (it only rescales g); any curvature variant on these maps (would be chosen after seeing tonight).

**Simplified:** chords that move, in its simplest honest form: covers, artist held, first year, chord count, and two terms only, repetition and surprise.

**Flagged:** every test since run 02 uses covers alone, not lasting love; the matched songs were chosen by having been versioned at all (only about 2% have no cover); tonight's tests had power of 0.24 and 0.06, and a floor of 0.5 before joining any outcome is proposed for Jason's decision.

## The papers

1. **Ollivier (2009), "Ricci curvature of Markov chains on metric spaces"**, Journal of Functional Analysis 256, 810–864 [1]. Defines curvature for any random walk on any space with distances: the cost of moving one step's cloud of destinations onto a neighbour's. Positive curvature forces fast forgetting (a spectral gap at least as large), a bounded diameter, and concentration. The walk need not be reversible, which chord walks are not. Read in full from the arXiv copy (through a summarising reader; caveat in card 1).
2. **Devriendt and Lambiotte (2022), "Discrete curvature on graphs from the effective resistance"**, Journal of Physics: Complexity 3, 025008 [2]. A curvature from electrical resistance, computed with a few lines of linear algebra and no settings. Proves that a node's curvature lies between fixed bounds, that curvatures add up to the number of pieces of the graph, that cut points have curvature at most zero, and that a link is a bridge exactly when its conductance times resistance equals 1. Read in full from the arXiv copy.

A Consensus research-agent query (Pro, one use) scouted the known pitfalls of curvature on small directed graphs [3]; it is not cited as evidence.

## Ideas ranked for coming nights

1. **Chord repetition and chord surprise together, on fresh songs**, rule first, once at least 2,000 newly matched songs are in hand (the first-principles next step; also what the maintainer's 749.157 asks of chord surprise).
2. **A fixed-space geometry:** each song's path on the circle of fifths (Fourier phase of each chord) or its voice-leading distances per move; stability checked before any outcome. This keeps Jason's geometry and drops the tiny-map problem.
3. **Tonic resistance H or the obtuse statue G3**, whichever is more stable, only after a stability check; or the spectral gap on McGill whole songs by a frozen rule, against the hold-out only once a measure has passed elsewhere.

## Paywalled papers for the inbox

None new tonight: both papers were open. Not reached (fetch blocked, not paywalled): the companion paper Devriendt, Ottolini and Steinerberger (2024), "Graph curvature via resistance distance", Discrete Applied Mathematics, arXiv 2302.06021.

## The proposed fix list

See the separate Doc "Proposed fix list: judging research, run 03" (https://claude.ai/artifact/UbBeN34uMjwi5yeboC5zbN); the same text is in `run03/proposed_fixlist.md`. This report is published as the Doc "Judging research, run 03" (https://claude.ai/artifact/3EY6MrGcAE4BVp8fJY7QQm).

## References

1. Ollivier, Y. (2009). Ricci curvature of Markov chains on metric spaces. J. Funct. Anal. 256, 810–864. https://arxiv.org/abs/math/0701886
2. Devriendt, K. & Lambiotte, R. (2022). Discrete curvature on graphs from the effective resistance. J. Phys. Complexity 3, 025008. https://arxiv.org/abs/2201.06385
3. Consensus research thread (scout only): https://consensus.app/search/methodological-question-for-a-planned-test-we-will/lX9tKl28QACoAkRrn67bUg/
4. The maintainer's within-artist test: `studies/judging_checks/within_artist/RESULT.md` on main (−0.042, p .009).
5. Data: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Discogs-VI (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.

## Addendum: four more tests the same night (Jason's new rule, 23 November)

Jason set a standing rule after the run: if an idea can be tested, test it. The four ideas that had been parked were frozen (commit 09ce7bd) after the first two results were seen, so they count as "after seeing results": six tests in all tonight, each needing p < .0083, and any pass would be a lead needing fresh songs.

| Test | Prediction written first | Result | Verdict | Power |
|---|---|---|---|---|
| Tonic resistance: is home the electrical hub? | Home more central, more covers (−0.03) | −0.019 (SE 0.014, p .19); halves −0.010, −0.027 | Unsettled (right direction, not strong enough) | 0.31 |
| Fifths path: average step around the circle of fifths per chord change | Smaller steps, more covers (−0.02) | −0.017 (SE 0.018, p .36); halves −0.011, −0.021 | Unsettled | 0.06 |
| The obtuse statue | More obtuse, more covers | No outcome joined | Stopped: too unstable between clips (0.154, needed 0.20) | n/a |
| Melody transport | Tune moves less than the chords, more covers | No outcome joined | Stopped: too unstable between clips (0.195, needed 0.20) | n/a |

Both measures that reached the outcome leaned the predicted way in both artist halves, and both grew when chord surprise was left out (−0.026 and −0.028), so part of each is plain harmony under another name. Neither is evidence yet. They are the first two geometric measures in this research that were not killed, and both are cheap to test again on fresh songs (fix list item R03-1).
