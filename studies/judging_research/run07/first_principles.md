# Run 07: first principles

26 November 2026. Recommendations; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- 5,901 fresh whole songs, eight frozen tests: none passed, six killed, two unsettled. Power was 0.00 to 0.02 per test.
- 39.7% were taken up, not the 20% assumed; errors ran 1.2 to 1.3 times the simulated ones.
- y_foreign is almost "in Discogs-VI at all" (2,343 of 2,387 matched).
- **Repetition did not carry:** +1.00 (seen Hooktheory), then +1.32 (fresh), now −1.93 (SE 1.34) on MIDI. The two fresh batches average about +0.1 (SE 0.8). On main, the covers-count finding is also unsettled among first performers (−0.026).
- The arrow A has failed on three new batches.
- One uncounted reading stood out: cv_w, how unevenly a song's 4-bar stretches differ, +3.11 (p .0047).

**Why repetition did not carry.** Nothing on hand separates these; retire the +1.0 prediction.
- *Different construct (likely).* MIDI ch_rep shares a tenth of its variance with Hooktheory's (ρ 0.32). Dilution predicts about +0.3; −1.93 is 1.7 SE from that.
- *Templates on full arrangements (likely).* Half-bar triads pick up pads and passing notes; whole-song counts include returning choruses, unlike Hooktheory's single-section clips.
- *Arranger effort (speculation).* Loved songs may get busier files, which lowers both ch_rep and F; both came out negative.
- *The match.* It adds noise, not a sign.
- *No effect (simplest).* The one significant figure came from the discovery sample.

**Assumptions.** The arranger's file stands for the song; y_foreign records musicians choosing; artist effects absorb fame.

## 2. Question every requirement
- **Yardstick.** Love has been unused since run 02, and at 40%, "taken up at all" is near a ceiling.
- **Notes only.** Keep it (it is the question), but no notes measure has held up on unseen songs; the recording has (main).
- **Corpus.** Lakh leans to famous artists, and 40% of its tracks were dropped as ambiguous.
- **MIDI as notes.** Two files of one song agree only 0.62 to 0.84. Flag: require two-file agreement before a test.
- **Gates.** They check stability and renaming, not song against arranger.
- **.05/N at power near zero.** Had every prediction been true, any pass had about a 6% chance; zero-line kills fire half the time on noise. Flags:
  - **the 0.2 power floor (R06-5).** The maintainer agreed; it is still Jason's call. Under it, none of the eight counts.
  - **Kill only when the prediction falls outside the 95% range.** That kills ch_rep, H4m, A and F, and leaves g, CH, P\* and B unsettled.
  - **Simulate power at a realistic base rate.**

## 3. Delete (recommended)
- **ch_rep at +1.0:** the fresh batches disagree; keep it as a control.
- **H4m (tree-likeness):** +1.41 against −0.5; close card 1's family.
- **Spectral gap g (Jason's S):** failed on its second unit, so it stays stopped.
- **Chirality CH:** −0.30, then +0.30; noise.
- **Arrow A:** failed three times.
- **Triad fidelity F:** the reversal probably reads the arranger.
- **Loop period P\*:** its halves split ±1.3.
- **Burstiness B:** mostly vocabulary; negative among first performers.
- **Tonic resistance:** retire (runs 05 and 06).

## 4. Simplify
One idea was left, uncounted: repeat and contrast, sections that clearly differ while phrases recur. It was tested in step 5 and killed. Going forward, test one measure at a time, and only at power ≥ 0.2, which means effects of about 1.5 pp per SD at Lakh's size.

## 5. Speed the loop
**Written, not run:** `experiments/cv_w_singletons/`, labelled *after seeing results*. A pass there is a lead only. I joined no outcome.
- **Songs.** 3,436 songs by single-song artists: 3,648, less 212 that share a file with a seen song. None has been joined to an outcome. The comparison is across songs, holding the `tree_h4m` columns.
- **Prediction.** +1.5 pp per SD. Kill if β ≤ 0. Pass at p < .05/9, with both halves and the logit agreeing.
- **Power.** 0.07 (0.23 at .05). The kill fires 11% of the time if the prediction is true and 50% if the effect is zero, the strongest kill on hand. It runs in minutes.
- **Costs.** Style is not held across artists, and the test spends the last unseen Lakh outcomes.
- **Run afterwards (the orchestrator, after its rule was committed at 6165846): KILLED.** β −0.13 (SE 0.81, p .87), halves −0.02 and +0.005, logit −0.014; base rate 18%. The cv_w lead was a winner's curse (`experiments/cv_w_singletons/RESULT.md`). Nothing uncounted is left standing.
- **Rejected.** The seen 5,901 across artists (spent outcomes); the 8,607 ambiguous-file tracks (need a rule for which song each file is, and match data not on disk).

## 6. The obstacle and the way through
**Obstacle.** Effects of 1 to 2 pp per SD; each fresh batch gives an SE near 1; MIDI blurs the measures. Seven runs, dozens of counted tests: no pass from the notes alone.

**Way through (speculation).**
- No new measures until the floor and the range-kill are decided.
- Chords rather than arrangements: a large chord corpus with artist and title (Chordonomicon, unverified).
- Version counts among matched songs carry more per song than 0/1; pay for any look at the seen songs' counts first.
- Interim answer to Jason: from these notes, at these sizes, not yet.
