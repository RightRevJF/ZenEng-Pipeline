# Judging research, run 07: the maintainer's check

26 November 2026. Read from `judging-research` at af7662b. Checked by the four steps in `coord/judging_research.md`.

**1. Rule first: holds for the eight; the ninth is post hoc, as it says.** Each of the eight tests' `PREDICTION.md` is in commit 9227e71 (19:19:57) and none was changed afterwards (the only later change under any `PREDICTION.md` is the ninth's, added at 6165846, 19:36:39). Results: `lakh_repetition/result.json` first appears in cd17b08 (19:21:25), the other seven in 0908976 (19:27:36), the ninth in 93399bb (19:39:06). So the first test's outcome was joined about a minute and a half after the rules were pushed; tight, but in order.

**2. Figures: the three I read match.** `lakh_repetition`: −1.93 (SE 1.34, p .148), N 5,901 in 1,678 artists, conditional logit −0.122 (converged). `triad_fidelity`: −2.10 (SE 1.04, p .044), logit −0.144 (p .015). `tree_h4m`: +1.41 (SE 0.92, p .125). `RESULT.md` agrees with `result.json` in each. I did not read the other five line by line.

**3. One thing to put right in the write-up.** In `tree_h4m/result.json` the conditional logit is `nan`, `converged: false`. The run's post says the nan bug was fixed before seven of the eight tests ran, so this is not that bug: the logit did not converge for this measure. The result's text reports both artist halves and does not say the logit failed. It changes nothing (the test is killed by sign on the main estimate), but the bar is "a conditional logit agreeing", so a reader should be told this one gave no reading. The songwriting session has already asked that the test which ran before the fix be named; it is `lakh_repetition` (its earlier output is kept as `result_before_logit_fix.json`).

**4. Not rerun.** I did not fetch the Lakh files, so `test.py` was not rerun from the raw data and the table's keys were not rebuilt. Zenodo is reachable from this machine; if a rerun is wanted for a result that is to be leaned on, say which and I will do it. Nothing in run 07 is leaned on by the engine, so I have not spent the time.

**5. The bar.** .05/8 = .00625 as stated; no test is under it; nothing passed. Agreed.

**6. Sources.** The two papers and the three Zenodo records named in the proposed list exist (arXiv 2412.05746, Gilbert and Yim; arXiv 1307.6188, Perea and Harer; Zenodo 5646574, 10178563, 3258042). Not read in full here.

**7. The hold-out.** The log says the McGill outcomes and song 59 were not read, and that McGill titles were read only to exclude those songs first. I have no way to verify a negative; the code path (`common._mcgill_keys`) is as described.

## The items

- **R07-1: taken up.** The table is in the pack as `studies/judging_data/lakh_covers_discogs.json`, copied unchanged, with a section in the pack's README marking both sets seen (the 5,901, and the 3,436 single-song-artist songs of the ninth test, which are not in the table) and naming the sources. No 749 number: it is a data note.
- **R07-2: agreed, already in force.** Fix 965 is judged on the kept songs' rate and cites covers for neither side. I will not cite run 06's lean as a direction.
- **R07-3:** (1) the 0.2 power floor is already ruled yes (R06-5, the writer, recorded in the pack's README). (2) Kill only when the prediction lies outside the estimate's own 95% range: I agree; a kill line at zero fires about half the time on noise when power is near nothing, and the engine's own readings today (several "nothing named" results on small counts) would be more honest under it. (3) Simulate power at the realised base rate: agreed, it is simply the right base rate. These are method, which the sessions settle; the writer can overrule.
- **R07-4:** recorded. None becomes an engine reading.
