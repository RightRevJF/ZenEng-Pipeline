# Run 05: first principles

25 November 2026. Recommendations; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- New measures ran on all 9,588 within-artist songs: first tests of new measures on seen songs (run 04 used these songs and y_foreign for chord repetition).
- Nothing passed. Killed: the certified loop margin M (−0.20 pp per SD against +0.8), harmonic freedom (−0.23), the fifths path (+0.01). Unsettled: the arrow of time A (+0.84, p .035; halves and conditional logit agree), melody range (−0.42, p .11), tonic resistance (−0.23).
- The persistent homology was computed exactly. The theorems held; the object carried nothing.
- No y_foreign rested on a karaoke or tribute set alone.
- The corpus is not hits only: the most-transcribed "artists" are game studios and library composers.

**Assumptions.** That y_foreign records musicians choosing a song; that a clip stands for the song; that clustering by artist captures how artists differ (the loop margin's halves differ at z 3.4; one artist carries 30% of melody range's variance).

**The fame test says little about fame.** Its proxy was broken (game and library sources top the artist song counts; fame's AUC was 0.48), and about 97% of the notes' gain was artist-level style, sung pop against instrumental themes. Card 2's superstar effect is untouched.

## 2. Question every requirement
- **Yardstick.** y_foreign is neither love nor a cover count. Melody range leans one way on being taken up (−0.42) and the other on how many take it up (+0.063). Flag: keep reporting both margins.
- **Notes only.** Keep; but across artists the notes read source and style.
- **Hits only.** False as stated. Flag: leave game and library sources out of across-artist tests.
- **Within artist.** Keep. It leaves out 3,610 songs by single-song artists, the only songs whose y_foreign has never been computed.
- **Power habit.** The notes-side bound overstated SE by a third or more (melody range: real power 0.49, not 0.10). Flag: take power from a fake-outcome run. The 0.5 floor stays Jason's.
- **Rules.** The fame rule's "D ≤ 0" clause has no interval and fires half the time on noise.
- **749.159 and the v47 loop_less patch.** Their support is covers among versioned songs (−0.042, narrow; fresh McGill −0.028, unsettled). On being taken up at all, repetition leans the other way (+1.00, run 04, unsettled; tonight repeats it on the same songs). Flag: before the trial, read A on the writer's sections with and without loop_less, notes only. Cutting repetition might cut direction too.

## 3. Delete (recommended)
- **Loop margin M:** −0.20; +0.8 lies outside its 95% range. With it, the chord-chroma persistence family (thickness, second bar, melody margin), already stopped on the notes.
- **Harmonic freedom:** −0.23, negative in every reading.
- **Fifths path (R03-F1), with diatonicity:** +0.01; closes R03-F1.
- **Hooktheory song count as fame:** it ranks game studios above the Beatles.
- **Contour surprise:** withdrawn; it measured transcription habits.
- Not failed, but worth retiring: tonic resistance (gate 0.203, power 0.09).

## 4. Simplify
The best idea left is direction: chords that go round (I–V–vi–IV), not back and forth (I–IV–I–IV). Its plainest form is one count, the share of changes that step straight back (G2; ρ −0.96 with A). The topology chased this contrast and failed. Direction is unrelated to repetition (ρ +0.01), and both lean towards being taken up.

## 5. Speed the loop: an eighth test, after seeing results
`experiments/arrow_singletons/PREDICTION.md`: A on the 3,223 single-song-artist songs with A and all 17 measures, across songs, holding the 17 data-pack measures, log chord changes and run 04's block; robust errors.
- **Prediction:** +0.6 pp per SD. **Kill:** below +0.2.
- **Pass:** p < .05/8 = .00625, both halves and a logit agreeing. The seven earlier tests keep their frozen .00714.
- **Power from the notes:** 0.03; the kill line fires 30% of the time if true, 60% if zero.

Nearly blind, but cheap, and the only unused outcomes on disk. A pass is a lead needing fresh songs, never a finding. Not run; commit it first.

## 6. The obstacle and the way through
**Obstacle.** Every song with an outcome has been seen, and the effects (about 1 pp per SD on a 22% outcome) sit at the edge of what one seen-song test at .05/7 can show.

**Way through (speculation).** Fresh within-artist songs: re-match the 4,177 clips outside the data pack to Discogs-VI, then run a small frozen battery (A, chord repetition, melody range) at one threshold, committed before the join. For Jason's geometry, the useful mathematics may be dynamics, not shape. Detailed balance is the first step towards entropy production on the chord chain; a graded version, Σ (n_ij − n_ji) ln(n_ij / n_ji) with pseudocounts, is the natural next measure, checked on the notes first.

**Postscript (added after the eighth test ran; nothing above is changed).** `arrow_singletons` was **killed**: β(A) on y_foreign = −1.75 pp per SD (HC1 SE 0.67, p .009), the opposite of the predicted +0.6; halves −0.24 and −3.29; logit −0.128 (p .013). It missed the opposite-sign bar (.00625), so it is not a new finding either. Across single-song artists, songs whose chords go round were *less* often taken up, and the back-and-forth share G2 leaned the other way (+1.94, p .005, reported only). So direction's within-artist lean (+0.84) did not carry to new songs. Across artists, A may read style (vamp-based genres get covered) rather than anything a writer controls. Direction stays a seen-song lean, unconfirmed and now contradicted out of sample; the "Simplify" section's best idea is weaker than it looked.
