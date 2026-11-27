# Tree-shaped form (average four-point hyperbolicity, H4m): the pass's mathematics. Result

Run 07, 26 November 2026. The rule is `PREDICTION.md` in this folder, frozen and pushed in commit 9227e71 before any outcome was joined. The shared code is `../common.py`, the script is `test.py`, the log is `run.log` and the numbers are in `result.json`. This is priority 2 of 8 tests tonight, so each test needs p < .05/8 = .00625, two-sided.

**Verdict: KILLED.** The rule written first says the prediction dies if the estimate is zero or above. It came out at **+1.41 percentage points per SD** (SE 0.92, p = .125), against the −0.5 predicted. Both artist halves also came out above zero. The estimate is not significant, so this is a kill by sign. It does not show that tree-like songs are covered *less*.

## In plain words

**The idea.** Picture a song as a family tree of phrases: sections, then variants of each section, then single phrases. Three of tonight's imaginers argued that such a song is easy for another musician to rebuild, because they can keep the branches and redo the leaves. So, among one artist's own songs, the more tree-shaped ones should more often be recorded by someone else. "More tree-shaped" means a *lower* H4m.

**What came out.** It went the other way. Within an artist, songs that were *less* tree-shaped were slightly more often covered: about 1.4 points per standard step of H4m, where about 40 songs in 100 are covered by another artist. That figure is not far enough from zero to count as a real effect (it is 1.5 standard errors from zero). But the predicted −0.5 now looks unlikely: the estimate sits about 2.1 standard errors above it. Every reading that decides nothing also came out above zero.

## The four-point condition, plainly

Take any four points and measure the distance between each pair. There are three ways to split four points into two pairs: {ab | cd}, {ac | bd} and {ad | bc}. For each split, add the two within-pair distances, which gives three **pair sums**. Then:

**fp = ½ × (largest pair sum − middle pair sum)**

- On a **tree** (distances measured along branches), the two largest pair sums are always *equal*, so fp = 0. This is the four-point condition (Buneman's theorem). A tree is the shape where every four points split cleanly into two families.
- In any other shape, the largest pair sum can stick out above the middle one, and fp > 0 measures by how much. The larger fp is, the less the four points look like two neat families.

**Example 1: four points on a tree.** Leaves a and b hang 1 unit from a branch point u. Leaves c and d hang 1 unit from a branch point v, and u and v are 2 units apart. Then a–b = 2, c–d = 2, and every cross distance (a–c, a–d, b–c, b–d) = 1 + 2 + 1 = 4.
- ab + cd = 2 + 2 = **4**
- ac + bd = 4 + 4 = **8**
- ad + bc = 4 + 4 = **8**

The largest two are equal (8 and 8), so **fp = ½(8 − 8) = 0**. The four points are perfectly tree-like.

**Example 2: four corners of a square** (side 1, ordinary straight-line distance). Corners A, B, C, D run in order around the square. Each side is 1 and each diagonal is √2 ≈ 1.414.
- AB + CD = 1 + 1 = **2**
- AD + BC = 1 + 1 = **2**
- AC + BD = 1.414 + 1.414 = **2.828**

The largest pair sum sticks out: **fp = ½(2.828 − 2) ≈ 0.414 > 0**. A square is a loop, and no tree can draw it: none of the three splits is better than the others.

**How the song score uses it.** Each point is a run of 4 consecutive bars, read as its chords' pitch content. H4m averages fp over 4,000 random sets of four such windows, then divides by the average distance, so the score does not depend on how far apart the windows are overall. **H4m = 2 × mean fp ÷ mean distance.** On the square, that ratio would be 0.828 ÷ 1.138 ≈ 0.73. Real songs average 0.099 (SD 0.016), so all of them are fairly tree-like, and the test asked whether the *more* tree-like ones, within an artist, are covered more.

## Step 1: is the measure an existing measure renamed? (notes only, before the run)

These are the within-artist Spearman correlations on the 5,901 songs by 1,678 artists. Each is computed on ranks over all songs, demeaned within artist and pairwise complete. They agree with `../chair_gates.json` to three decimals.

| H4m with | ρ (within artist) | Songs |
|---|---|---|
| ch_rep | −0.036 | 5,901 |
| V | −0.263 | 5,901 |
| ln_chg | −0.184 | 5,901 |
| ln_bars | +0.028 | 5,901 |
| H4m | 1.000 (itself) | 5,901 |
| cv_w | −0.205 | 5,901 |
| g | +0.274 | 5,901 |
| lnP | +0.156 | 5,716 |
| F | +0.123 | 5,901 |
| B | −0.064 | 5,886 |
| CH | −0.021 | 5,899 |
| A | −0.236 | 5,899 |

**It is not an existing measure renamed.**
- No overlap comes near the 0.7 line. The largest is g (spectral gap) at +0.274. Among the four gate columns, the largest is V at −0.263.
- Fitting H4m's within-artist ranks on all eleven other measures together explains only R² = 0.285 (5,716 songs with every column; this is my own check, not a gate). So about 70% of H4m's within-artist variation is not in any of the other measures.
- The chair's gates were split-half 0.582 and residual split-half 0.504; it passed both.

## What was predicted (frozen)

- **Measure:** H4m, as above (sliding 4-bar windows of L2-normalised bar chroma ÷ 2, exact duplicates dropped, 4,000 quadruples seeded by md5 of the track id, mean over the song's files). It goes into the model as z, where 1 SD = 0.0164.
- **Outcome:** y_foreign = 100 if the song's Discogs-VI version group holds a release by a performer who shares no name with the artist, and 0 if not or if the song is unmatched.
- **Model:** a linear probability model within artist, with CR1 standard errors clustered by artist. It holds z(cv_w), z(ch_rep), z(ln_chg), z(V), z(ln_bars) and five-year year bins (unknown year is its own bin). A conditional logit by artist, with the same columns, is the sign check.
- **Prediction:** β = −0.5 pp of y_foreign per SD.
- **Pass:** β < 0 with p < .00625, β < 0 in both artist halves, a conditional-logit coefficient below 0, and that logit must have converged.
- **Kill:** β ≥ 0.

## What came out

The script ran once, 19:23:24 to 19:24:29 ET on 26 November 2026, after commit cd17b08 (19:21:25). It exited cleanly. Nothing was changed.

**Power, printed before the estimate** (`common.fake_power`, 400 draws): pass rate **0.0025** if the prediction is exactly true, false-pass rate 0.000 if the true effect is 0, mean SE 0.718 pp.

**Outcome join:** 2,387 of the songs matched a Discogs-VI version group, none was dropped for lacking an own set, and 2,343 songs have y_foreign = 100. The **base rate of y_foreign is 39.7%**.

| | β (pp per SD of H4m) | SE | p | N songs | Artists |
|---|---|---|---|---|---|
| **Primary (all songs)** | **+1.411** | 0.921 | 0.125 | 5,901 | 1,678 |
| Artist half 0 | +0.979 | 1.257 | 0.436 | 2,961 | 842 |
| Artist half 1 | +1.811 | 1.346 | 0.178 | 2,940 | 836 |

- z = +1.53, far inside the ±2.734 needed. The estimate is 2.08 SE above the predicted −0.5 (two-sided p = .038 against −0.5).
- **Conditional logit (sign check):** coefficient **NaN**, p NaN, **converged: false**. More on this below.

## The verdict by the rule written first

**KILLED (β = +1.41 ≥ 0).**
- The pass fails on every count: the sign is wrong, p = .125 is not below .00625, both halves are on the wrong side, and the logit gave no number.
- The opposite-sign clause (a positive β with p < .00625 would be reported as a new hypothesis) does not apply, since p = .125.

**How firm.**
- **As a rule outcome, it is clear-cut.** The estimate is 1.5 SE above zero, not on the line. Both halves agree, and the fame-held, first-performer and bare readings all fall on the same side.
- **As evidence, it is modest.** At the SE actually seen, the kill line would fire 29% of the time if the prediction were exactly true, and 50% of the time if the effect were zero.
- **Weighed by height rather than by sign,** the estimate of +1.41 is about 2.7 times more likely if the true effect is 0 than if it is −0.5. That is a real step against the idea, but not a decisive one. The power line says the same: this test could hardly ever have passed.

**The conditional logit, and the earlier bug.**
- The shared sign check (`common.cond_logit`) had a programming bug, found when the first test ran: it read a missing attribute (`mle_retvals`) and so always returned NaN. It was fixed at commit cd17b08 before this test ran, and no rule changed.
- Here it still returned NaN, for a different reason. I re-ran its steps outside the test, notes and the same cached outcome only, writing nothing. Both the Newton fit and the BFGS fallback raised a ValueError inside statsmodels ("need covariance of parameters"), because the information matrix of this 19-column fit could not be inverted. `cond_logit` caught both errors and returned NaN with converged = false, as written.
- `test.py` did not crash, so I fixed nothing. Editing `common.py` would also trip the guard. The same NaN appears in `../lakh_arrow/result.json`.
- **It cannot change the verdict.** The logit enters only the pass rule, and the kill rests on β alone.

**The base rate is about 40%, not the 20% the power simulation assumed.**
- The fake outcomes in `PREDICTION.md` and in the printed power drew artist baselines with mean 0.20, which was run 06's uptake. The real y_foreign is 39.7%.
- A 0/1 outcome near 40% is noisier than one near 20%: its variance is 0.397 × 0.603 ≈ 0.24 against 0.16. That alone widens the SE by about 1.22 times, from 0.72 to roughly 0.88. The real SE was 0.92.
- What this means: **the test was even blinder than the 0.0025 printed.** A −0.5 pp effect is also a smaller share of a 40% base than of a 20% one. The power figures in `PREDICTION.md` are therefore optimistic, and a null or a kill here clears even less.

## Readings that decide nothing (all in `result.json`)

| Reading | β (pp per SD) | SE | p | N | Artists |
|---|---|---|---|---|---|
| On **y** (in Discogs-VI at all) | +1.345 | 0.942 | 0.153 | 5,901 | 1,678 |
| **Fame held** (Billboard flag, hotttnesss, missing-hotttnesss flag) | +1.427 | 0.920 | 0.121 | 5,901 | 1,678 |
| **First performers only** (R02-3's rule) | +0.731 | 0.913 | 0.423 | 4,755 | 1,591 |
| **Bare H4m** (cv_w and ch_rep not held) | +0.407 | 0.808 | 0.614 | 5,901 | 1,678 |
| **cv_w's own coefficient** in the primary model (H4m and ch_rep held) | +3.115 | 1.101 | 0.0047 | 5,901 | 1,678 |

- Every H4m reading is above zero and none is near significance. Fame does not explain the sign.
- **Holding cv_w moves H4m up**, from +0.41 bare to +1.41. That fits cv_w's own large positive coefficient and its −0.205 overlap with H4m. Part of the primary's positive H4m is what is left once the spread of distances is held.
- **cv_w's p = .0047 is below .00625, but it is not a test.** Nobody predicted it, it is not counted in the eight, and it was printed as a reading so the model could be seen. Treating it as a finding would be fishing. cv_w correlates +0.55 with ch_rep (it is the repetition axis in chroma space), and ch_rep's own test came out negative tonight. If anyone wants to pursue cv_w, it needs its own frozen prediction and a batch of songs not seen tonight.

## What it cannot say

- **Power.** Even if the prediction were exactly true, a pass was a 1-in-400 event, and it was less than that at the real base rate. A kill is weak evidence.
- **MIDI is not the record.** The notes come from an arranger's MIDI file, matched to the recording by audio. The pitch content is bar chroma from that file, and the chords are half-bar triad templates. H4m reads how one arranger's bars group, not necessarily how the song's form groups.
- **y_foreign is uptake, not love.** It records that another artist released a version. No measure of lasting love is used (run 06 first principles).
- **Within artist only; no cause.** It compares an artist's songs with each other. It says nothing about why, or about artists against each other. Lakh leans to well-known artists, and Discogs-VI coverage is uneven.
- **One extrapolation, one dataset.** Buneman's theorem and the 2ε stability bound are true facts about metrics. The step from "tree-like" to "rebuildable, so covered" was an extrapolation, and its authors labelled it as such. Tonight's result goes against that step for this measure on these songs. It does not touch the mathematics.

## Files

- `PREDICTION.md`: the frozen rule (commit 9227e71).
- `test.py`: unchanged.
- `run.log`: this run's output.
- `result.json`: every figure above.
- Step 1 used a notes-only script outside the repo. Nothing was committed or pushed.

## Correction (run 08, 27 November 2026; the maintainer's check of run 07)
The conditional logit gave no reading for this test: in `result.json` it is `nan` with `converged: false`. This was not the bug fixed in cd17b08 (this test ran after that fix); the logit failed to converge for this measure. The kill stands on the main estimate (+1.41 against −0.5), but the pass bar names the logit, so a reader should know this one was silent. The test that ran before the cd17b08 fix was `lakh_repetition` (its earlier output is kept as `result_before_logit_fix.json`). No rule or figure is changed.
