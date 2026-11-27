# Run 08 brainstorm (27 November 2026, the 02:17 ET pass)

Round 1: the three imaginers. Round 2: the Skeptic. Round 3: the replies. No agent opened an outcome. Scripts for the notes-side checks were kept outside the repo in /home/claude/scripts/; the code the tests use is copied into experiments/measures.py.

---

## Run 08, round 1: the Geometer

Notes side only. No outcome was opened. Scripts are in `/home/claude/scripts/geometer/` (`g_measures.py`, `g_checks.py`, `g_examples.py`). They ran on 40,665 charts with at least 8 chords and took about 40 s.

Every measure is computed on the change sequence: each chart's pitch-class sets, with consecutive repeats merged. W1 is card 1's Eq. 12, Σ|D − median D|. It reproduces card 1's whole table (C1).

## R08-G1: Transport economy (card 1, chromatic circle)
- **Mechanism.** A tune whose chord order is a cheap transport tour of its own chords is cheap to re-voice, transpose or re-harmonise, and a cover is such a re-voicing.
- **Recipe.** econ = 1 − w̄/b.
  - w̄ is the mean chromatic W1 between successive changes.
  - b is the mean W1 over all position pairs holding different chords: the exact expected step if the same changes came in random order. No settings.
- **Data.** ChoCo chords only.
- **Prediction.** +0.04 SD, holding ch_rep, V, ln length and first year; a second reading also holds w̄. Rough SE 0.02, so power is near the 0.2 floor.
- **Kill.** +0.04 lies outside the 95% range.
- **What the mathematics predicts (extrapolation).** W1 is rotation-invariant, so an economical progression stays cheap under every transposition and re-voicing. It should survive re-arrangement and keep being covered.

## R08-G2: Transposed repetition (the rotation group acting on the circle)
- **Mechanism.** A chord shape that returns at another pitch level is stored once, as a pattern plus a shift, while the chords keep moving. The one idea that passed (W01-J1) says literal repetition costs covers, so recurrence should pay only when transposed.
- **Recipe.**
  - Reduce each root+quality 3-gram of changes to its transposition class (q1, Δ1, q2, Δ2, q3).
  - O = share whose class was heard earlier; L = share heard earlier at the same pitch level; T = O − L. No settings.
  - T reads exact sequences only: "Autumn Leaves" scores 0, Giant Steps 0.38, Cherokee 0.20, All the Things 0.17.
- **Prediction.** T +0.05 SD, holding L, ch_rep, V, ln length and first year (L negative, not counted). Rough SE 0.03, power about 0.2.
- **Kill.** +0.05 lies outside the 95% range.

## R08-G3: Fitness beyond the urn (card 2's null, with the measures above)
- **Mechanism.** In a linear-attachment urn each song's share of new covers is a martingale, so a notes measure predicts late covers only if it carries fitness.
- **Recipe.**
  - Fit a negative binomial: new distinct artists at ages 11–30 on log(K10 + 1) + cohort + composer, plus T and econ.
  - K10 = distinct artists through age 10. Nothing new to compute.
- **Prediction.**
  - Neutral null: β ≈ 1, γ = 0. My bet (extrapolation): γ_T = +0.03, β > 1.
  - Probably under the floor, so an estimate, not a pass.
- **Kill.** γ_T has a 95% range that excludes +0.03, with power ≥ 0.2.

## Checks
| # | Check | Result |
|---|---|---|
| C1 | Card 1 table (C to F, Am, Db, F#, G7) | exact |
| C2 | Same title and artists, non-identical charts, one pair per tune (3,095) | econ r 0.71, T 0.83 (Spearman 0.72); after controls, 0.70 and 0.79 |
| C3 | iReal against Wikifonia, title only (2,002) | econ 0.41, T 0.43, ch_rep 0.33 |
| C4 | Overlap (Spearman) | econ: ch_rep −0.06, V 0.08, A 0.08, w̄ −0.53. T: L −0.21, ch_rep −0.22, V 0.39. R² on controls: econ 0.03, T 0.21 |
| C5 | Share of variance within composer (1,371 composers) | econ 0.84; T 0.43, 54% zeros, Medium Swing 0.10 against Pop 0.02 |
| C6 | **Stopped by me: two circles,** mean (fifths W1 − chromatic W1) | ρ 0.82 with the fifths step, so R03-F1 renamed |
| C7 | **Stopped by me: local straightness** in W1 space | ρ 0.76 with A, so the arrow (killed) renamed |

---

## Run 08 brainstorm, round 1: the Listener

Notes-only checks (no outcome opened): `/home/claude/scripts/listener/checks_r1.py`, `checks_r1b.py`, `examples_r1.py`. 39,915 of 42,002 charts are computable. Stability is measured on 2,394 non-identical same-title, same-artists pairs. The other 2,299 of the 4,693 pairs are exact copies. Flag for the match: some artists strings name the arranger ("be2sharp ARR:").

## R08-L1 Key travel (card 1, mathematics)
- **Mechanism:** players learn tunes that tour key areas and come home. Card 1's trade-off: W1 sees mass shifting round the circle, L1 only reweighting, so W1 with L1 held is key travel.
- **Measure:** TRAV5 is the mean circular W1 on the fifths circle (Eq. 12, Σ|D − median D|) between consecutive 4-bar windows, chord tones weighted by duration. The model holds TRAVL1 (same windows under L1), ch_rep, V, ln_bars and ln_chg. The one setting is 4 bars.
- **Check C1:**
  - Two-chart ρ is 0.80; with TRAVL1 and size held, 0.68.
  - TRAVL1 plus size explain 72% of TRAV5.
  - Within composer, the remainder has |ρ| ≤ 0.07 with every control.
  - Its ρ with R03-F1's chord-step is 0.15.
- **Prediction (extrapolation):** +0.07 SD per SD; TRAVL1 near 0.
- **Kill:** +0.07 lies outside the 95% range.

## R08-L2 Momentum or fitness (card 2, outcome side)
- **Mechanism:** lasting love is a hidden fitness. Under neutral copying, a song's share of cover activity is a martingale.
- **Computation (version timelines):**
  - Keep t0 ≤ 1994.
  - K10 counts distinct artist sets by t0+9, the original included.
  - L counts new ones from t0+10 to t0+29.
  - Fit a Poisson QMLE: log E[L] = composer FE + 5-year t0 bins + β·log(K10+1), clustered by composer.
  - Report card 2's urn ceiling (c), with c0 = 1.
- **Prediction:** β = 1.10, ceiling ≥ 0.10.
- **Kill:** 1.10 lies outside β's 95% range.
  - β ≈ 1 with a ceiling under 0.05 means the notes cannot be powered.
  - Dating error biases β down.

## R08-L3 The ii-V chunk (music cognition)
- **Mechanism:** players memorise changes as known chunks (Chase and Simon); a ii-V chart takes fewer units to learn.
- **Measure:** IIV is the share of chord changes from a minor seventh (no major 3rd) to a dominant seventh a fourth up. It has no settings.
- **Check C3:**
  - Two-chart ρ is 0.86; with size held, 0.79.
  - 48% of its variance lies within composer.
  - Within composer, its ρ is +0.18 with V and −0.31 with chord-step W1.
  - 44% of charts have a ii-V.
- **Prediction:** +0.06 SD per SD, holding ch_rep, V, ln_bars and ln_chg. Late covers with log(K10+1) held should show the same sign; that is the second model for L1 and L3.
- **Kill:** +0.06 lies outside the 95% range.

L1 and L3 sit at the floor; simulate their power before they are counted.

---

## Run 08, round 1: the Inventor

Notes only; no outcome opened. Checks C1-C10: `/home/claude/scripts/inventor/`. Data for all three: the ChoCo cache plus the planned clique match (covers, first year). "Controls" = composer FE, first-year bins, ch_rep, ln distinct chords, ln chords, ln bars.

## R08-I1 Key excursion E (card 1, Eq. 12)
- **Mechanism (extrapolation):** circular W1 shifts at most ε·h(1/2) when ε mass moves, so re-voicing barely changes it; the tonal itinerary is what a cover inherits, and phrases that leave home and return give performers more to carry.
- **Recipe:** duration-weighted chord-tone bar profiles on the fifths circle (i→7i mod 12); E = mean CEMD (Σ|D−median D|) of each 4-bar window from the whole chart (one setting); song = mean over charts.
- **Checks:** computable 41,006/42,002 (C1); two-chart stability r 0.82, against L1 0.80 and chromatic W1 0.73, as the robustness predicts (C2); ρ ch_rep −0.26, distinct 0.49, bars 0.28, global spread 0.56; residual stability 0.74 (C3); 58% within composer (C4).
- **Prediction:** +0.08 SD per SD, holding controls and spread.
- **Kill:** +0.08 outside the 95% range, or the sign flips in a composer half.

## R08-I2 Harmonic heritability (card 2; outcome-side)
- **Mechanism:** under neutral Wright-Fisher or Moran copying, songs with the same changes by different composers have unrelated cover residuals; fitness carried by the changes makes chord-space neighbours alike, with no measure to guess.
- **Recipe:** each matched song's 10 nearest matched songs by tf-idf cosine on interval-coded chord trigrams (different title, no shared composer token, not the same clique); r = residual log(1+covers) on composer FE, 5-year bins, genre; ρ_nb = corr(r_i, mean neighbour r); null permutes r within genre × decade.
- **Checks:** 31,282 tunes, top-10 cosine mean 0.39, p90 0.85 (C5); 15% of neighbours share genre vs 9% by chance (C6); two charts of one tune share 35% of neighbours vs 0.03% (C7).
- **Prediction:** ρ_nb +0.10; the neutral null predicts 0.
- **Kill:** +0.10 outside the 95% range. A ρ_nb near 0 is a ceiling: stop chord measures.

## R08-I3 Inherited template (Yule-Simon)
- **Mechanism:** a new title is an innovation; if content matters, a tune on a shared template (blues, rhythm changes) inherits the family's playability, while neutral copying predicts 0.
- **Recipe:** F = ln(1 + other-composer, other-title charts with interval-trigram Jaccard ≥ 0.4).
- **Checks:** F > 0 for 6.1%, with blues and rhythm changes on top (C8); stability r 0.45, with 95% agreement on any family (C9); ρ distinct −0.10, E −0.02; 68% within composer (C10).
- **Prediction:** +0.06 SD, at the floor; report it as an estimate unless fake-outcome power reaches 0.2.
- **Kill:** +0.06 outside the 95% range.

**Dropped:** copying fidelity (divergence between charts of one tune). Its stability is 0.13.

---

## Run 08, round 2: the Skeptic

Notes only, no outcome opened (`/home/claude/scripts/skeptic/sk_checks.py`): 25,715 iReal tunes; 15,334 by 2,526 composers with two or more.

## Confounds every test shares
- **Genre within composer.** 1,640 composers span genres; Medium Swing sits +0.56 to +0.73 SD above Pop on T, IIV and TRAV5. Every model needs genre inside composer.
- **Chart writer.** Half the same-title iReal pairs are exact copies; the real gate is iReal against Wikifonia: E .64, IIV .62, TRAV5 .54, T .45, econ .39, ch_rep .34, F .23.
- **Matching.** Match on a writer token, not a performer token. Average charts unweighted; chart count is a popularity proxy, never a control.
- **Power.** SE ≈ 1/√(0.5·N·r), r = measure variance left after composer, genre, controls.

## The notes-side proposals
"Tunes needed" = matched tunes for power 0.2 at .05/6. All can run this pass.

| Idea | Problem | Tunes needed | Sharpened test |
|---|---|---|---|
| G1 econ | Not repetition (ρ with ch_rep −.01), but ρ −.68 with the step size w̄, a relative of the killed R03-F1 | ~5,900 | Hold w̄ and genre in the primary model; +0.04 |
| G2 T | Only 27% of its variance is within composer; mostly a jazz detector | ~11,800 | Estimate only; hold L and genre |
| L1 / I1 | ρ .75 within composer: one idea. TRAV5 keeps more variance after controls (.44 against E's .33) | ~3,000 | Count TRAV5, holding TRAVL1 and genre; E as second model |
| L3 IIV | Spelling risk, yet cross-source agreement is .62; still the jazz idiom | ~4,300 | Hold genre and w̄ (ρ −.30); count it |
| I3 F | 94% zeros; cross-source agreement .23 | far above 3,200 | Estimate only: F > 0 within genre |

**Merges.** G1 is not L1/I1: econ correlates only .07 to .08 with TRAV5 and E. The template trio (T, IIV, F) correlates .04 to .12 within composer: one story, three different measures.

## Outcome side
- **G3 and L2 are one design.** L2 plus card 2's urn ceiling best answers card 2: it measures the room left for any content before a notes measure is spent.
- **Where to run it.** On the Hooktheory versions table it re-spends nothing on the notes side, but those are seen outcomes. Use them only to set power. G3's γ becomes the second model on ChoCo, frozen before it runs.
- **Dates.** Pre-1950 Discogs years are often reissues, biasing β down; report t0 ≥ 1950 and all years.
- **I2.** A genre × decade permutation does not hold the scene: bebop heads are recorded by jazz players. Permute within composer-genre × decade, and drop contrafacts of one parent.

---

## Run 08, round 3: the Geometer replies

**R08-G1 econ: revised.**
- Primary model: within composer, with genre fixed effects inside composer.
- Controls: w̄, ch_rep, V, ln length, first year.
- Prediction: +0.03 SD per SD. I lowered it from +0.04 because, once w̄ is held, econ varies only through the vocabulary baseline b.
- Second model: the same without w̄.
- Kill: +0.03 lies outside the 95% range.
- Counted only if simulated power is at least 0.2 at the matched N; otherwise it is reported as an estimate.

**R08-G2 T: revised to estimate only, withdrawn from the count.**
- Only 27% of its variance is within composer, so it would read jazz.
- Controls: L, genre, ch_rep, V, ln length, first year.
- Prediction: +0.05.

**R08-G3: merged into L2 as its second model, withdrawn as a separate test.**
- γ for econ and T, frozen before the run.
- Reported for t0 ≥ 1950 and for all years.
- Hooktheory versions are used only to set power.

---

## Run 08, round 3: the Listener answers the Skeptic

No outcome opened. I accept all of the Skeptic's sharpened tests.

**R08-L1, revised (merged with I1).**
- **Counted measure:** TRAV5.
- **Model:** composer fixed effects plus genre dummies (iReal style; Wikifonia charts with no genre form their own bin).
- **Columns held:** TRAVL1, ch_rep, V, ln_bars, ln_chg.
- **Second model:** E.
- **Charts:** averaged unweighted; the number of charts is never a control.
- **Prediction:** +0.05 SD per SD, down from +0.07 because genre takes part of the effect.
- **Kill:** +0.05 lies outside the 95% range.
- **Gate:** iReal against Wikifonia agreement is .54, so it passes.

**R08-L2, revised (merged with G3).**
- **Primary sample:** t0 ≥ 1950; all years are reported alongside.
- **Prediction:** β = 1.10, unchanged.
- **Kill:** 1.10 lies outside the 95% range.
- **Also reported:** the urn ceiling.
- **Hooktheory versions:** used only to set power.
- **Second model:** G3's γ, frozen before it runs.

**R08-L3, revised.**
- **Counted measure:** IIV.
- **Columns held:** genre, w̄, ch_rep, V, ln_bars, ln_chg.
- **Prediction:** +0.04 SD per SD, down from +0.06.
- **Kill:** +0.04 lies outside the 95% range.
- **Second model:** late covers, holding log(K10+1).
- **Caveat:** spelling risk (iReal against Wikifonia .62).

---

## Run 08, round 3: the Inventor replies

I accept matching on a writer token, unweighted chart means, and genre inside composer.

- **R08-I1: merged into L1.**
  - TRAV5 is counted.
  - E becomes TRAV5's second model, with prediction +0.08 SD per SD.
  - Controls: composer FE, genre FE, first-year bins, ch_rep, ln distinct chords, ln chords, ln bars, global spread, TRAVL1.
  - Kill: +0.08 lies outside the 95% range.
- **R08-I2: revised.**
  - Drop neighbour pairs with interval-trigram Jaccard ≥ 0.4, since these are contrafacts of one parent.
  - r is the residual of log(1+covers) on composer FE, genre FE and 5-year first-year bins.
  - The null permutes r within composer-genre × decade cells.
  - Prediction: ρ_nb +0.06, lowered from +0.10 because siblings are removed.
  - Kill: +0.06 lies outside the 95% range.
  - It is counted only if power is 0.2 or more on fake outcomes; otherwise it is an estimate.
  - Report t0 ≥ 1950 and all years.
- **R08-I3: withdrawn as a test.**
  - Cross-source agreement is .23, and 94% of charts score zero.
  - If the chair wants it, F > 0 within genre can be reported as an estimate only, at +0.06.
