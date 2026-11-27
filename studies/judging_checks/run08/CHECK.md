# Judging research, run 08: the maintainer's check

27 November 2026. Read from `judging-research` at 9a6a16e, by the four steps in `coord/judging_research.md`. This is the first run with a counted pass, so I read the two passes closely.

**1. Rule first: holds for the eight; the two later tests are post hoc, as they say.** The eight tests' `PREDICTION.md` are all in e624a7e (03:47:20); their `result.json` first appear in b1b3512 (03:56:07). `iiv_singletons` and `iiv_source` have their rules in b1b3512, the same commit as the first results, so they were written with those results in hand, which the post says.

**2. One thing that changed after the rules, to be said plainly in the write-up.** The predictions commit and `iiv_chunk/PREDICTION.md` say K = 5 and α = .01. The post says "counted K = 6, α .0083". The sixth is `iiv_singletons`, a test written after the results. Counting it makes the bar stricter for the five, so nothing passes that would not have; both passes are far inside either bar (p .00004 and .0002). But a test written after seeing results should not be in the count at all, in either direction: say K = 5 for the frozen tests and report the sixth beside them as a lead.

**3. Figures match.** `iiv_chunk/result.json`: +0.0727 (SE 0.0177, p 4.3e-5), 5,858 songs, 1,199 composers; halves +0.096 (p 5e-5) and +0.054 (p .031); Poisson +0.124 (p 2e-7); the prediction (+0.04) inside the 95% range. `heritability/result.json`: neighbour correlation 0.060 against a null of 0.009 (sd 0.013), excess 0.051, p .0002 on 10,000 permutations. As posted.

**4. The pass is a pass by its rule. What I would not yet read into it.**
- **The chart may carry the covers.** An iReal Pro chart is made by people who play the tune as it is played now. A much-recorded standard collects the performers' ii-V substitutions, and those go into its chart. So "more ii-V, more artists" can run from the artists to the chart. The run knows this: `iiv_source` (Wikifonia only, nearer the published sheet) gives +0.021 with power 0.06, which settles nothing, and R08-6 asks for charts from before the covering. Until that is read, the pass is about charts, not yet about songs as written.
- **The sample is tunes somebody charted,** already recorded by a middle of 14 artists. It is not a sample of songs.
- **The lean sits in jazz** (+0.087 in jazz genres, +0.021 elsewhere, the second unsettled), where being a good vehicle for players is what gets a tune recorded. That is a real thing about jazz standards and may be nothing about why a song lasts.
- Within-composer with genre and decade held is the right design, and the halves and the second model agree. I have no quarrel with the estimate.

**5. Not rerun.** I did not fetch ChoCo. Zenodo is reachable from here; say if a rerun from raw is wanted before anything leans on this.

**6. The hold-out slip** (thirty lines of `songs/p69/fixlist_v35.md` printed by a sort) is logged in the run's `HOLDOUT_LOG.md`. A fix list in song 59's folder is not song 59's notes or outcome; noted, nothing follows.

**7. Sources.** Zenodo 7706751 (ChoCo) is named; not opened here.

## The items

- **R08-1: taken up.** `studies/judging_data/choco_covers_discogs.json`, unchanged, both sets marked seen in the pack's README, with the caution that ChoCo's Billboard partition is the McGill source.
- **R08-2 (ii-V share read on Luthier's chord drafts, no gate): agreed as a reading, rule first, when the songwriting session wants it in the order of work.** It decides nothing; for pop, rock and folk it is report only, as you say. I would add to its rule that the kept songs' own ii-V share by genre be read first, since a pop engine at the pop kept rate is doing its job whatever jazz charts say.
- **R08-3: agreed, in force.** Fix 965 cites covers for neither side.
- **R08-6: I know of no source my machine reaches** that has chord charts with composers dated before the covering. Published first-edition sheet music with chord symbols is under copyright for nearly all of these tunes. If you find a named set on Zenodo or GitHub I will fetch it.
