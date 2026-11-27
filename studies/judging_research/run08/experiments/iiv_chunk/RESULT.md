# iiv_chunk (R08-L3, the ii-V share): result

**In plain words.** We asked whether, among songs by the same composer, the songs whose chord charts use more ii-V moves (a minor seventh chord followed by a dominant seventh a fourth up, the stock jazz move) are recorded by more different artists. They are, somewhat more than predicted, and the test passed by the rule written first. That is an association within composers, holding genre, era, size and other chord measures. It does not show that ii-Vs cause covers, or separate the song from the jazz repertoire it belongs to.

**Predicted (frozen in PREDICTION.md before any outcome was joined).** β = +0.04 SD of y_cov (log of 1 + artist sets, standardised) per SD of IIV. Pass: p < .01, β > 0, β > 0 in both composer halves, Poisson coefficient > 0. Kill: +0.04 outside β ± 1.96 SE.

**Came out** (5,858 songs, 1,199 composers):
- Power, printed before the estimate: 0.387 (assumed composer share 0.3; 0.553 at 0.5). Over the 0.2 floor: counted.
- β = **+0.073**, SE 0.0177, p = 4.3 × 10⁻⁵; 95% range +0.038 to +0.107.
- Halves: +0.096 (SE 0.023; 2,973 songs) and +0.054 (SE 0.025, p = .031; 2,885 songs).
- Poisson on artist sets: +0.124 (SE 0.024, p = 1.8 × 10⁻⁷), about 13% more artist sets per SD.

**Verdict: PASS.** Every pass condition holds, and the verdict is the same at the final bar (.05/6 = .0083).

**How firm.** The sign is firm: p is far below the bar; both halves and the second model agree. The size is not: the estimate is 1.8 times the prediction, which sits 0.002 inside the range's lower edge. The second half alone (p = .031) would not pass. One frozen test, run once.

**Renaming check** (`../measure_gates.json`). Two-chart stability 0.772 (0.708 after size); iReal against Wikifonia 0.584. Within-composer ρ with ch_rep −0.021, with V +0.217: far from 0.8, not renamed. ρ with w_chr −0.339; w_chr is held.

**Reported, deciding nothing.** Without w_chr: +0.076 (SE 0.017). Writer-matched songs only: +0.074 (SE 0.018; 5,541 songs).

**Follow-ups written after seeing this result** (own RESULT.md each). `../iiv_singletons/`: a pass on 2,707 unseen songs, across composers (+0.057, SE 0.019), concentrated in jazz genres (+0.087 against +0.021): a lead, not a finding. `../iiv_source/` (Wikifonia against iReal charts): underpowered (power 0.06), settles nothing.

**What it cannot say.**
- Genre within composer: a composer's jazz and pop tunes are compared with each other; genre is a coarse bin.
- Jazz idiom: IIV partly marks jazz (Medium Swing charts sit 0.73 SD above Pop), and jazz standards get recorded often whatever their chords.
- Chart writers: iReal charts come from jazz players, who may add ii-Vs to tunes they already play, so the outcome could leak into the measure. Still open. Chord spelling (m7 or 6, dominant or sus) also varies by writer.
- Name matching: songs and composers are matched by title and name tokens; some may be wrong.
- Selection: only tunes someone charted are here, and charting favours tunes that get played.
