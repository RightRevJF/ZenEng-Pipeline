# Run 09: first principles

27 November 2026, 10:17 ET. Recommendations only; Jason decides.

## 1. Bedrock
**Facts.**
- The one counted test (K = 1, power 0.367), the ii-V share on 1,271 unseen songs: −0.0005 (SE 0.028), range −0.055 to +0.054 against +0.05. **Unsettled.**
- The frozen non-jazz reading (−0.049) excludes +0.04: by run 08's rule the lead is "jazz repertoire". Its unframed jazz side gave +0.104 (SE 0.048), near run 08's +0.087.
- Five geometric estimates (power 0.04 to 0.19) found nothing. TR, which an added ii cannot move, gave −0.041, below its +0.035. IRR went against its prediction (−0.060, p .043).
- Seen leads: holding resolutions, the ii-V stays at +0.056; resolutions flip sign (−0.046 across composers, +0.034 within). The ii-V read from Real Book or BiaB (+0.064) beats the iReal reading (+0.020); holding log iReal chart count turns the first negative (−0.041).
- Every matched ChoCo song is now seen.

**Assumptions.** A chart stands for the song (writers agree 0.28 to 0.72); a title finds the right song; an artist set means the same in jazz as in pop; the Real Book is independent of covering (it is not: it came from canonical recordings).

## 2. Question every requirement
- **Yardstick.** Love unused since run 02. In jazz, recording standards is the convention, and the lead lives only there: the outcome may measure "is a standard". Flag: standardise within genre; add love.
- **Notes only.** Keep, but the notes are players' charts (JSIR's lead sheets were built from its recordings).
- **Hits-only corpus.** Tonight's songs were the tail run 08 left (median 4 artist sets).
- **Title-only match.** 985 of 1,283. Name-matched songs gave +0.063 (SE 0.063): dilution fits, unproven. Flag: require title plus writer.
- **Across composers.** Resolutions change sign between designs on the same songs. Flag: an across-composer null cannot refute a within-composer finding.
- **Power floor, K, run 08's 0.5.** K = 1 was consistent, but at 0.367 the likeliest result was the one we got. Flag: restore 0.5 for confirmations; pool unseen batches until they reach it.
- **8-test cap, "test everything".** Five estimates under 0.2 yielded one nominal p, against prediction (compare run 07's cv_w: +3.11, then −0.13). Flag: under 0.1 power, an idea waits.
- **Measure gates.** Stability was read mostly on BiaB against Real Book near copies. Flag: make cross-writer agreement of 0.5 binding.
- **Holding log iReal charts.** It is downstream of being played. Flag: do not hold it.

## 3. Delete (recommended)
- **TR and DRES:** prediction above the range; seen DRES negative across composers.
- **TQ:** −0.007 at power 0.037; dominant density renamed.
- **TYP:** +0.0004 against −0.02; least stable.
- **IRR as stated:** wrong sign. Do not promote the reversal: power 0.067, clustered p .064, one of about twenty readings.
- **GAP:** carries nothing; its sign follows the control.
- **The general ii-V claim:** non-jazz excludes +0.04.
- **CARC and TE (waiting):** cross-writer 0.35 and 0.28.
- **The signature family, for this outcome:** five measures, nothing.
- Kept: VR4c (+0.026 against +0.02) failed nothing; it waits for power.

## 4. Simplify
One number, one repertoire: in jazz tunes, the share of changes from a minor seventh to a dominant seventh a fourth up, against log artist sets. It marks the songbook idiom jazz players record, fitting "good to play on" and "a standard because players say so" alike. Holding early covers, it said nothing about late ones (run 08: +0.006, SE 0.032).

## 5. Speed the loop
**Prediction, written first.** Among seen jazz-partition songs, the ii-V share predicts the artist sets new to a song that recorded it after Discogs-VI's cutoff (1 July 2024), holding log prior artist sets, genre and decade: **+0.03 SD per SD**. Kill if +0.03 lies outside the 95% range. Count only at fake-outcome power 0.5.

**Why.** ChoCo was frozen in 2023, so these covers cannot have shaped the charts: time breaks the arrow from covers to chart, and no new charts are needed. I expect it to die.

**This pass?** No. It needs a Discogs monthly release dump (CC0) from after July 2024; a matching rule (title plus writer credit to seen cliques, new artist sets, first release after the cutoff) frozen before counting; and Jason's ruling that an outcome window never joined counts as unseen.

**Other route.** About 1,100 unseen jazz tunes with title and composer give power 0.5 at +0.06 (2,200 for 0.8; scaled from tonight's jazz SE), from a chord source outside ChoCo.

## 6. The obstacle and the way through
**Obstacle.** The lead lives only in jazz repertoire, where chart writers, performers and the cover count are one community, and every charted song here is spent.

**Way through (speculation).** Use time, not new songs: ask whether the ii-V predicts covers recorded after the charts were frozen, holding covers before. If yes, it judges something; if no, it reads the canon back. Interim answer: one jazz-idiom marker, not yet a judge of greatness.

**Addendum by the orchestrator (after this review, same pass).** Section 5's idea was run at once in the form the data on hand allow, under the after-seeing-results rule: not artists after July 2024 (that needs a newer dump), but artists whose first release of the song is dated 2023 or 2024, after ChoCo's charts were collected (ChoCo v1.0.0 was published 7 March 2023). Rule committed and pushed first (4055742; `experiments/late_window08/PREDICTION.md`), on run 08's 8,565 seen songs, holding log prior artist sets, genre and decade, predicted +0.03. **Result: +0.051 (SE 0.012), both halves and the Poisson model positive: a lead, supported** (`experiments/late_window08/RESULT.md`). Within composer +0.058; outside jazz +0.018, unsettled. So the review's expectation ("I expect it to die") did not hold on seen songs: the ii-V share predicts artists who took a tune up after its charts existed, which weakens the pure chart-copies-covers story but not the "working jazz repertoire" (momentum) story. The way through stands, sharpened: the same test on artists after July 2024 (a newer Discogs dump) and on unseen songs, with momentum held more tightly (prior artist sets in the last five years, not only all prior sets).
