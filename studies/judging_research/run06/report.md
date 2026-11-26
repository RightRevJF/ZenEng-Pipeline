# Judging research, run 06

26 November 2026. Research only: nothing here goes into the Luthier engine or main. Song 59 and its folders were not read. The McGill hold-out was not touched.

## Tonight in three sentences

Tonight found 1,946 Hooktheory songs whose outcome had never been looked at, built their outcome with the maintainer's own Discogs match (it reproduced the data pack exactly), and tested six frozen ideas, one of them new mathematics: which way a song's chords turn round the circle of fifths. Nothing passed: two ideas were killed (melody range and "how in-key the chords are"), four were unsettled, and chord repetition, the project's most persistent lead, leaned the predicted way on the new songs for the first time (+1.32 points, both halves agreeing) but far short of the bar. The mathematics taught one firm thing: for a single song, the "downhill to home" part of the chord flow is decided by where the excerpt starts and ends, so the only honest geometry left is the loops, and the songs on hand are now too few to settle effects this small.

## The experiments

Six tests were frozen before any outcome was joined (commit 08b5167), so each needed p < .05/6 = .0083, the predicted sign in both halves of the artists, and a second model (conditional logit) agreeing. Results are in commit 3f39f56.

The outcome is the same as run 05's: was the song ever released by performers who share no name with the original artist ("taken up by another artist")? Effects are in percentage points per standard deviation of the measure, comparing each artist's songs only with that artist's other songs.

| Test | Prediction written first | Result | Verdict | Power |
|---|---|---|---|---|
| 1. Chirality: chords that turn "down" the circle of fifths (seen songs) | −0.6 | **−0.30** (SE 0.38, p .42); halves −0.62 and +0.03 | Unsettled | 0.15 |
| 2. Chord repetition on fresh songs | +1.0 | **+1.32** (SE 1.04, p .20); halves +0.46 and +1.97; logit + | Unsettled | 0.05 |
| 3. Arrow of time on fresh songs | +0.6 | **+0.09** (SE 1.17, p .94); halves split | Unsettled | 0.02 |
| 4. Tonic resistance on fresh songs | −0.6 | **−0.25** (SE 0.75, p .74); halves split | Unsettled | 0.03 |
| 5. Melody range on fresh songs | −0.7 | **+0.69** (SE 1.58, p .66) | Killed (wrong side of zero) | 0.015 |
| 6. Diatonicity on fresh songs | +0.5 | **−0.29** (SE 1.19, p .80) | Killed (wrong side of zero) | 0.014 |

Power is the chance of passing if the prediction were exactly true, from each test's own standard error.

**The fresh songs.** These are 1,946 songs in the full Hooktheory file that the data pack never measured, mostly because their transcriptions have chords but no melody. Their outcomes had never been joined to anything. Tonight the Discogs-VI dump (1.4 GB, from Zenodo) was reduced with the maintainer's own script and matched with the maintainer's own rule. Before any fresh outcome was used, the rebuild had to reproduce the data pack: it matched all 3,080 songs, the same groups, the same version lists and the same "taken up" answer for all 13,198 seen songs (100% on every check). Of the fresh songs, 1,295 have another song by the same artist and could enter the comparison; 17% of them were taken up, against 24% of seen songs.

**1. Chirality.** This was the night's new mathematics (explained below). Songs whose chords fall round the circle of fifths, as ii–V–I does, were predicted to be taken up more. The estimate leaned that way at half the predicted size, but one half of the artists showed it and the other did not. Unsettled. A side reading matters: the unsigned amount of turning gave the same lean (−0.31), so if anything is there, it may be how much a song turns, not which way.

**2. Chord repetition on fresh songs.** The test the project has wanted since run 04: a lead seen on old songs, checked on songs nobody had tested. It came out slightly larger than predicted (+1.32), with both halves and the second model positive, but its uncertainty (1.04) is so wide that p was .20. This is the third time repetition has leaned towards being taken up, and the first on outcomes never seen before. It is still not a finding.

**3. The arrow of time.** Last night's best lean (+0.84 within artist) reversed on single-song artists (−1.75). On fresh songs it is +0.09: neither story repeats. It is fading.

**4. Tonic resistance.** Run 03's measure of how central the home chord is. Unsettled for the third time, never close.

**5 and 6. Melody range and diatonicity.** Both came out on the wrong side of zero and are killed by their rules. These kills are weak: with power this low, the kill line fires about half the time even when there is no effect. Both close long-running ideas (melody range from run 05, diatonicity from run 04).

**A mistake caught.** Three experimenters reported that most fresh "taken up" songs share a Discogs group with a seen song, which would have made them not fresh. That came from a faulty flag in the shared code. Rebuilt correctly, only 10 of 312 matched fresh songs share a group with a seen song. The fresh outcomes are close to independent; the note is appended to those RESULT files.

## The mathematics, plainly

**A song as a flow.** Draw each chord a song uses as a dot, and an arrow for each move from one chord to the next. Count the arrows each way between every pair of dots. Where a song goes C→G as often as G→C, the two cancel; what is left is the *net flow*. Tonight's two papers are about how any flow on such a map splits into two kinds: a *downhill* part, as if the chords sat on a hillside and the music ran down it (tension to rest, like V to I), and a *circulating* part, which goes round loops and comes back (like I–V–vi–IV).

**What all three imaginers proved.** In a single walk through the chords, every chord you enter you also leave, except the first and the last. So the downhill part has nowhere to come from but the starting chord and nowhere to go but the ending chord. It is exactly the electric current you would get by connecting a battery between the first and last chord, with every move a one-ohm wire. In plain words: "how much a song runs downhill to home" depends only on where the excerpt was cut. The measure was stopped before any outcome was joined (it was not stable between two excerpts of the same song), and the lesson is general: for one song, the honest geometry is in the loops.

**Chirality: which way the loops turn.** Place the 12 chord roots round a clock in fifths: C at 12 o'clock, G at 1, D at 2, A at 3, and so on round to F at 11. A progression is now a path round the clock. Green's theorem says the signed area the path sweeps is a property of its loops alone; moves that go and come back add nothing. Each step adds half the sine of the angle it turns through.

**Worked example (C major, roots on the clock).**

| Progression | Clock path | Sweep per pass | CH (about 15 moves) |
|---|---|---|---|
| I–V–vi–IV (C, G, Am, F) | 12 → 1 → 3 → 11 → 12 | +0.50 | **+0.117** |
| The same backwards (C, F, Am, G) | 12 → 11 → 3 → 1 → 12 | −0.50 | **−0.117** |
| I–vi–ii–V (C, Am, Dm, G) | 12 → 3 → 2 → 1 → 12 | −0.25 | **−0.050** |
| ii–V–I (Dm, G, C) | 2 → 1 → 12 | falls each step | **−0.055** |
| I–IV back and forth | 12 → 11 → 12 … | about 0 | **−0.017** |

So the pop loop I–V–vi–IV turns one way and the jazz cadence ii–V–I the other, and no earlier measure could tell a song from itself played backwards. The bet, labelled as extrapolation, was that songs built on falling fifths, the language of the standards, are taken up more. Tonight's estimate leaned that way by half the bet, with one half of the artists disagreeing. The mathematics held; the songs did not answer clearly.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| Downhill share of the chord flow (card 1's recipe) | all three | Stopped: it is the first-to-last current |
| Holes in the chord map (loops of four or more with no shortcut) | Geometer | Withdrawn: unstable once size is held |
| How many loops; one loop's share (λ, orbit purity, dominant cycle) | Geometer, Listener, Inventor | Merged, then withdrawn: mostly the number of distinct chords |
| Arrow beyond chance (A*) | Geometer | Withdrawn: the arrow renamed |
| Downhill to the tonic (H) | Listener | Withdrawn: the excerpt boundary |
| Entropy production | Inventor | Stopped: the arrow renamed, or unstable |
| Song as heat engine | Inventor | Stopped: unstable (0.06) |
| Chirality on the circle of fifths | Inventor | Tested: unsettled |
| Fresh-song battery (repetition, arrow, range, tonic resistance, diatonicity) | Listener with the Skeptic; backlog | Tested: four unsettled, two killed |

**Agreed:** all three imaginers found the battery theorem independently, and accepted the Skeptic's point that every "loop" measure mostly counts distinct chords. Chirality was the only new axis everyone accepted. **Split:** the Listener and the Skeptic wanted the fresh repetition test at the looser one-test bar of .05; the chair kept Jason's shared threshold. Under the looser bar it would still not have passed (p .20).

## First principles

**The obstacle.** Effects of about 1 point per standard deviation on a 22% outcome, against the best standard error the Hooktheory songs can give (0.4 to 0.5 on seen songs; 1.0 or more on fresh ones). The measures have outrun the outcomes. Every within-artist song with chords has now been spent.

**The way through (partly speculation).** Pause new measures. The next fresh confirmation of chord repetition, its prediction written tonight (+1.0, one test at .05, killed if at or below zero), should run only with power of 0.5 or more: about 5,400 new within-artist songs. A large chords-only corpus matched to Discogs-VI could supply them; Chordonomicon (666,000 songs) was checked tonight, but its download is blocked from here and it carries Spotify ids rather than artist and title names. If the mathematics continues, the honest family left is a loop measure in a fixed space (as chirality is on the circle of fifths), tested only when outcomes exist to spend.

**Deleted (recommended; Jason decides):** melody range and diatonicity (killed); tonic resistance (retire: unsettled three times); everything stopped on the notes tonight (the downhill share, downhill to the tonic, the loop counts, holes, A*, entropy production, the heat engine, melodic holonomy).

**Simplified:** the best idea left is chord repetition alone, one measure and one outcome, within artist, reported on both margins: repetitive songs lean towards being taken up at all (+1.0 to +1.3 on three readings) and towards fewer coverers once taken up (−0.042, the maintainer's within-artist test).

**Flagged for Jason:**
- Five nearly blind fresh tests cut chirality's bar from .05 to .0083 (its power from 0.35 to 0.15). Proposal: count only tests with power of 0.2 or more, and report the rest as estimates.
- No test since run 02 has used love, only being taken up.
- The engine's loop-less trial (749.185) waits for "which way covers lean"; at this size the fresh songs cannot settle it. Proposal: judge it on matching the kept songs' rate alone.

## The papers

1. **March (2024), "Helmholtz-Hodge Decomposition on Graphs"** [1], arXiv 2412.09434 (probably math.CO; the abstract page was blocked, so not confirmed); read in full from the arXiv HTML. It splits any flow on a network into a gradient part, a part that circulates round circuits, and a remainder, without filling any triangles. The reader checked its dimension counts numerically and found they fail beyond networks with a single loop (for a square with a diagonal, and for four fully linked dots), though the split itself holds. Its gradient recipe is what tonight showed reads only an excerpt's ends.
2. **Homs-Dones, MacKay, Sansom & Zhou (2025), "Circular Directional Flow Decomposition of Networks"** [2], arXiv 2506.12546; read in full from the arXiv HTML. It splits a flow network into a looping part and a one-way part, shows the split is not unique (the possible splits form a polytope), gives the maximal-loop split and a unique split from the random walk's stationary distribution. For one song's chords it reduces to "one start-to-end path plus loops", the same lesson from another direction. It replaced Cruz-de-la-Rosa & Guerrero-Poblete (2026), arXiv 2603.03634, which is PDF-only and could not be read tonight.

## Ideas for coming nights (not testable tonight)

- **A powered confirmation of chord repetition:** needs about 5,400 new within-artist songs with chords and artist and title names (DATA.md).
- **Chordonomicon as that corpus:** needs a reachable copy of `chordonomicon_v2.csv` and a way to name its songs (Spotify ids only).
- **The ceiling (MusicLab), cover breadth across genres, a real fame measure:** data not on hand (DATA.md).
- **Love as an outcome:** no measure of lasting love is on hand beyond covers; worth a data search on a coming night.

## Papers you could drop in the "Judging research inbox" Drive folder

None is paywalled; all are free on arXiv but only as PDFs, which an unattended run cannot read.
- Cruz-de-la-Rosa & Guerrero-Poblete (2026). An approach to non-equilibrium Markov chains through cycle matrices. arXiv 2603.03634 (math.PR).
- Perea, J. A. & Harer, J. (2015). Sliding Windows and Persistence. Foundations of Computational Mathematics 15, 799–838. doi:10.1007/s10208-014-9206-z (carried from run 05).
- Gakhar, H. & Perea, J. A. (2023). Sliding window persistence of quasiperiodic functions. Journal of Applied and Computational Topology. arXiv 2103.04540 (carried from run 05).

## Housekeeping

Consensus reports that its free allowance for this billing period is used up, so tonight's scouting used arXiv alone and later nights will too unless the allowance is renewed.

## The proposed fix list

See the separate Doc "Proposed fix list: judging research, run 06"; the same text is in `run06/proposed_fixlist.md`.

## References

1. March, P. (2024). Helmholtz-Hodge Decomposition on Graphs. arXiv 2412.09434. https://arxiv.org/abs/2412.09434
2. Homs-Dones, MacKay, Sansom & Zhou (2025). Circular Directional Flow Decomposition of Networks. arXiv 2506.12546. https://arxiv.org/abs/2506.12546
3. Cruz-de-la-Rosa & Guerrero-Poblete (2026). An approach to non-equilibrium Markov chains through cycle matrices. arXiv 2603.03634 (not read). https://arxiv.org/abs/2603.03634
4. Kantarelis, S. et al. (2024). Chordonomicon: A Dataset of 666,000 Songs and their Chord Progressions. arXiv 2410.22046. https://arxiv.org/abs/2410.22046
5. Run 06 commits on judging-research: 08b5167 (predictions), 3f39f56 (results).
6. Data: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0, zenodo.org/records/13983028.
