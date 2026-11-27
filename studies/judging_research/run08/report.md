# Judging research, run 08

27 November 2026, the early pass (02:17 ET). For Jason.

## This pass in three sentences

Ten tests were run on 8,640 tunes the research had never looked at: lead-sheet chord charts from a public corpus (ChoCo: iReal Pro and Wikifonia), matched to the covers database by title and songwriter, with the outcome being how many different artists recorded each tune. For the first time in eight passes, measures from the notes passed tests whose rules were written first: tunes with more "ii-V" moves (a minor-seventh chord stepping to a dominant seventh a fourth higher, the most common chord move in jazz) were recorded by more artists, and so were tunes whose closest chord look-alikes by other songwriters were themselves much recorded. The ii-V result held again on 2,707 further unseen tunes, but it sits mostly in jazz tunes, and the old chord-repetition lean and the pass's geometry test were both killed.

What it means: there is now a real signal in the notes, but it may be the jazz player's ear (which tunes jazz musicians like to play over) rather than a measure of greatness in general. The next step is to check it on chord charts not written by jazz players.

## The experiments

Each counted test needed its power to be 0.2 or more (your 0.2 floor), p below .05 ÷ 6 (the pass counted six), the predicted sign in both halves of the songwriters, and the same sign in a second kind of model. A counted test is killed only when its prediction falls outside its own 95% range (the range kill). Effects are in standard deviations (SD) of "how many artists recorded the tune" per SD of the measure, comparing tunes by the same songwriter, with genre and decade held.

| Test | Idea | Predicted | Result | Verdict | Power |
|---|---|---|---|---|---|
| iiv_chunk | Share of ii-V moves | +0.04 | **+0.073** (SE 0.018) | **Pass** | 0.39 |
| heritability | Chord look-alikes by other writers share covers | +0.06 | **+0.051** (p .0002) | **Pass** | 0.65 |
| iiv_singletons | ii-V on 2,707 unseen tunes (after seeing results) | +0.07 | **+0.057** (SE 0.019) | **Pass, as a lead** | 0.69 |
| chrep_confirm | Chord repetition (the one earlier lean) | −0.04 | −0.003 (SE 0.014) | Killed | 0.49 |
| key_travel | Key travel on the circle of fifths (the mathematics) | +0.05 | −0.031 (SE 0.026) | Killed | 0.21 |
| cover_timeline | Do early covers alone drive late covers? | slope 1.10 | 0.91 (SE 0.030) | Killed | 0.25 |
| transport_economy | Chord order as a cheap tour | +0.03 | −0.035 (SE 0.016) | Estimate only | 0.22 |
| tonic_resistance | Pull of the home chord (written keys) | −0.03 | +0.021 (SE 0.012) | Estimate only | 0.28 |
| transposed_rep | Patterns that return at another pitch | +0.05 | +0.014 (SE 0.015) | Estimate only | 0.79 |
| iiv_source | ii-V read from Wikifonia sheets only (after seeing results) | +0.07 | +0.021 (SE 0.039) | Estimate only | 0.06 |

**Power** is the chance the test would pass if its prediction were exactly true, worked out on fake outcomes before the real ones were joined. "Estimate only" means it was frozen and reported but passes and kills nothing.

**The ii-V share.** Comparing tunes by the same songwriter, a tune one step higher in ii-V moves was recorded by about 13% more artists. Both halves of the songwriters agreed, and so did the second model. Written after seeing that, a second test on 2,707 tunes whose writer has only one tune in the set found the same (+0.057). But there the effect was +0.087 in jazz genres and only +0.021 elsewhere.

**Chord look-alikes.** For each tune, the ten tunes by other writers whose chord moves look most alike were found. A tune's covers tend to go with its look-alikes' covers, beyond what writer, genre and decade explain, and beyond a shuffled baseline. The link halves for tunes from 1950 on, so a shared jazz scene may explain part of it.

**Chord repetition.** The research's only earlier lean (from Hooktheory songs) was retested with real power on fresh tunes and came out at zero. It is retired as a predictor.

**Key travel.** The geometry test (below) predicted that tunes which tour more keys get covered more. They did not (−0.031).

**Early and late covers.** If covers spread purely by copying, a tune with twice the early covers would get twice the late ones (slope 1). The slope was 0.91: early leaders keep leading, but their lead fades. Pure copying is rejected, and copying explains about half of the spread in late covers, leaving at most half for anything about the song itself.

**The four estimates** decide nothing. Two went the wrong way (transport economy, tonic resistance).

## The mathematics: moving sand around a clock

Put the twelve notes round a clock face in the order of the circle of fifths (C, G, D, A, ...). A chord is a little pile of sand on its notes. How far apart are two chords? Card 1's paper proves an exact recipe for the cheapest way to shovel one pile into the other on a circle: add up the differences as you walk round, then subtract their middle value (the median), and sum what is left. No settings to choose.

*Worked example.* C major (C, E, G) to F major (F, A, C): the cheapest way is for each third of the sand to move one step round the circle (G to C, C to F, E to A), so the cost is 1.0. C major to Db major costs 3.0, three times as far, which is what a musician hears. A plain count of how much sand changed bins scores these two moves 1.33 and 2.0, so it barely tells near from far.

For key travel, each 4-bar stretch of a tune became one pile, and the score was the average shovelling cost from one stretch to the next. A tune sitting on C, C, F, C scores 0.67; putting Db in the middle scores 2.0. The idea was that tunes which travel further and come home give players more to carry. The test said no: within a songwriter's tunes, more travel went with slightly fewer recordings.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| G1 Transport economy | Geometer | Estimate, wrong sign |
| G2 Transposed repetition | Geometer | Estimate (author withdrew it from the count) |
| G3 Fitness beyond copying | Geometer | Merged into the timeline test |
| L1 Key travel | Listener | Killed |
| L2 Momentum or fitness (timeline) | Listener | Killed |
| L3 The ii-V chunk | Listener | **Passed** |
| I1 Key excursion | Inventor | Merged into key travel |
| I2 Harmonic heritability | Inventor | **Passed** |
| I3 Inherited template | Inventor | Withdrawn (unstable) |

**Where they agreed:** match on the songwriter, not the performer; hold genre inside each songwriter; average a tune's charts equally; one key-travel test, not two.
**Where they split:** whether the ii-V and heritability ideas read songs or the jazz idiom (the Skeptic's worry, still open), and how many tests to count. No count was consistent, so the chair counted five by a written rule and left two tests above the power floor as estimates.

## First principles

**The obstacle.** The only chord corpus large enough to have power is written and chosen by the same community whose recordings are the outcome. A jazz player writing an iReal chart may add ii-V moves to a tune because jazz players already play it.

**The way through (speculation).** Read harmony from before the covering: published first-edition sheet music or lead sheets not made by jazz players, then test the ii-V share again, and test whether it predicts late covers when early covers are held (tonight: +0.006, nothing).

**Deleted (recommended, nothing dropped without you):** chord repetition as a predictor (keep it as a control), key travel, the "momentum hides fitness" idea, transport economy, tonic resistance (against its prediction a fourth time), transposed repetition.

**Simplified:** one number per tune, the ii-V share, against how many artists recorded it, genre and decade held. Honestly: on present evidence it is about tunes as jazz players use them, not yet about great songs in general.

**A lesson:** testing everything tonight spent every matched tune. The remaining 542 unseen tunes give too little power (0.04) to confirm anything, so they were kept.

## The papers

1. **Rabin, Delon and Gousseau (2011), Transportation distances on the circle** [1]. Proves the exact recipe for optimal transport on a circle (a median of running differences) for any sensible cost. For equal three-note chords it equals the smallest voice leading divided by three. It gave tonight's key-travel and transport-economy measures.
2. **Evans and Giometto (2011), Turnover rate of popularity charts in neutral models** [2]. The counter-evidence due this pass: if everyone copies at random and no song is better than another, charts still show heavy hits and steady turnover. It gave the early-and-late-covers test (which rejected pure copying) and the shuffled baseline behind the look-alike test.

## Ideas for coming passes (could not be tested tonight)

- **A confirmation of the ii-V lead outside jazz charts:** needs chord charts with titles and composers written before covering (not found on Zenodo or GitHub tonight).
- **Melody transport (R03-I1):** the Wikifonia melodies are in the download but not parsed yet.
- **The obtuse statue, loop period, burstiness:** ranked ninth to eleventh with power under 0.05; on these tunes they would now re-spend seen outcomes.
- **The MusicLab ceiling and cross-genre breadth:** data not on hand.

## Paywalled papers

None this pass.

## Fix list

The proposed fix list for the maintainer is the Doc "Proposed fix list: judging research, run 08" (https://claude.ai/artifact/9erV8FEcZTmDGVk52j5FDj). This report is the Doc "Judging research, run 08" (https://claude.ai/artifact/L9hE7vxc7Ryj4tBqHxCYWK).

## References

1. Rabin, J., Delon, J. and Gousseau, Y. (2011). Transportation distances on the circle. Journal of Mathematical Imaging and Vision; arXiv:0906.5499. https://arxiv.org/abs/0906.5499
2. Evans, T. S. and Giometto, A. (2011). Turnover rate of popularity charts in neutral models. arXiv:1105.4044. https://arxiv.org/abs/1105.4044
3. de Berardinis, J., Meroño-Peñuela, A., Poltronieri, A. and Presutti, V. (2023). ChoCo: a chord corpus and a data transformation workflow for musical harmony knowledge graphs. Scientific Data; data at Zenodo 7706751 (CC BY 4.0). https://zenodo.org/records/7706751
4. Araz, R. O., Serra, X. and Bogdanov, D. (2024). Discogs-VI. Zenodo 13983028, CC BY-SA 4.0. https://zenodo.org/records/13983028
