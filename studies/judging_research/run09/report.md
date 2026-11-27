# Judging research, run 09

27 November 2026, the mid-morning pass (10:17 ET). For Jason. Research only: nothing here goes into the Luthier engine. Song 59 and the McGill hold-out were not touched.

## This pass in three sentences

This pass found 1,283 songs nobody had tested, from chord charts written outside the iReal Pro community (Band-in-a-Box files, the Real Book, and transcriptions of single recordings), and used them to check run 08's one standing lead: songs with more "ii-V" moves get recorded by more artists. On these new songs the lead came out at zero (unsettled, not killed), it was clearly absent outside jazz, so by the rule written in run 08 it is now labelled "jazz repertoire", and the five new geometric measures from this pass's mathematics paper all said nothing. But a test written afterwards on the old songs found that ii-V tunes kept gaining new artists in 2023 and 2024, after their charts were written, so the lead looks like a real property of tunes jazz musicians want to play, not just the chart copying the covers.

## The experiments

The rules for every test were committed before any outcome was opened (commit 379e219, pushed at 11:15 ET; results in 687e735). The outcome is how many different artists recorded each song (Discogs-VI, on a log scale). Effects are in standard deviations (SD) of that outcome per SD of the measure, with genre and decade held.

Only one test had enough power to count (power 0.367), so the pass bar was p < .05 for that one test. Run 08 had asked for power 0.5 before running this confirmation; the ruled floor is 0.2, so it was counted, and that relaxation is stated here plainly. Tests under the floor are "estimates": they pass nothing and kill nothing.

| Test | Idea | Predicted first | Result | Verdict | Power |
|---|---|---|---|---|---|
| iiv_confirm09 | ii-V share on 1,271 unseen songs | +0.05 | −0.0005 (SE 0.028) | **Unsettled** (counted) | 0.37 |
| (reading) | the same, outside jazz | +0.04 | −0.049 (SE 0.033) | Label: **"jazz repertoire"** | 0.19 |
| tr_resolve | dominants that resolve (a ii cannot move it) | +0.035 | −0.041 (SE 0.027) | Estimate | 0.19 |
| tq_tension | tension's ups and downs (lead-lag area) | +0.01 | −0.007 (SE 0.030) | Estimate | 0.04 |
| irr_skeleton | the chord walk left after removing back-and-forth | +0.02 | −0.060 (SE 0.029) | Estimate, opposite sign | 0.07 |
| vr4c_momentum | runs of fifths in the bass line | +0.02 | +0.026 (SE 0.027) | Estimate | 0.12 |
| typ_typical | how typical a song's shape is for its genre | −0.02 | +0.0004 (SE 0.029) | Estimate | 0.07 |
| gap_writer08 | ii-Vs read from a non-iReal chart, on old songs | song story +0.045 | +0.064 alone; iReal reading +0.020 | Lead (old songs) | 0.21 |
| iiv_dres08 | the ii or the resolution? (old songs) | +0.035 | ii-V +0.056; resolutions −0.046 | Lead (old songs) | 0.81 |
| late_window08 | new artists in 2023 to 2024, prior artists held (written after) | +0.03 | **+0.051 (SE 0.012)** | **Lead supported** (old songs) | 0.68 |
| late_momentum08 | the same, recent momentum held (written after) | +0.03 | **+0.044 (SE 0.012)** | **Lead supported** (old songs) | 0.68 |

Power is the chance the test would pass if its prediction were exactly true, worked out on fake outcomes before the real ones were opened. "Old songs" means run 08's songs, whose outcomes had already been looked at: these give leads, never findings.

**The confirmation.** On the new songs the ii-V share predicted nothing overall (−0.0005). The prediction (+0.05) sits just inside the 95% range, so it is not killed, only unsettled. Outside jazz the estimate was negative (−0.049) and excluded +0.04, which by run 08's frozen rule labels the lead "jazz repertoire". Inside the jazz charts alone it was +0.104 (SE 0.048), but that reading was not written first and decides nothing. Most new songs were matched by title alone, which adds wrong matches and pulls estimates towards zero.

**Resolving dominants.** If chart writers simply add ii chords before each V, a measure that ignores the ii would carry the true effect. It came out slightly negative. On old songs, holding resolutions left the ii-V share as strong as before (+0.056): the ii-V move itself carries it, not the resolution.

**Upstream and iReal charts.** On 1,181 old songs that have both kinds of chart, the ii-V share read from a Real Book or Band-in-a-Box chart predicted covers (+0.064) better than the iReal reading of the same songs (+0.020). That is the opposite of what "iReal players add the ii-Vs" predicts. The frozen main model, which also held how many iReal charts a song has, gave a confusing result (both stories excluded), because that chart count is itself a sign of being much played.

**New artists after the charts.** This is the pass's most useful result, though a lead only. ChoCo's charts were collected before March 2023. Among old songs with the same number of earlier artists, those with more ii-Vs gained more new artists in 2023 and 2024 (+0.051), and still +0.044 when the last five years' momentum was held too. Those artists could not have put the ii-Vs into the charts. Outside jazz it was small and unsettled (+0.024).

**The geometry estimates.** None decided anything; their power was 0.04 to 0.19. One came out against its prediction with p .043 (the back-and-forth measure, below), which is something to watch, not a finding.

## The mathematics: a song as a path, and what it remembers

Put each chord on the circle of fifths as a point, and join the points in order: a song becomes a path. This pass's paper (Chevyrev and Kormilitzin) is about the **signature** of a path: a list of numbers that summarises it completely, whatever the tempo. Its first level is just where you end up. Its second level is the **Lévy area**: the signed area between the path and the straight line from start to finish, worked out by the surveyor's shoelace formula. Run 06's chirality was exactly this area.

The paper's deepest fact is what the signature *cannot* see. A step out and straight back (C to F and back to C) leaves no trace: the signature treats it as if it never happened. Mathematicians call such detours "tree-like".

*Worked example.* The walk C, F, C, G, C is two detours from C and back, so after cancelling them nothing is left: its "irreducible share" is 0 out of 4 steps. The pop loop C, G, Am, F, C, G, Am, F never steps straight back, so all 7 steps survive: share 1. The Inventor bet that songs whose walks survive this cancelling (more journey, less rocking) are covered more. On the new songs it went the other way (−0.060): if anything, rocking back and forth went with more recordings. It was uncounted and power was 0.07, so it may be noise; it is noted in the backlog.

The Geometer used the same theorem as a lie detector for chart writers: a ii chord slipped in just before a V, when the bass returns, is a detour, so a measure built on the "detour-free" path cannot be moved by such additions. That measure (resolving dominants) found nothing. The honest summary: the signature gave clean, stable measures from the notes, and on these songs none of them predicted recordings.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| TQ: tension's lead-lag area | Geometer | Estimate, nothing |
| TR: dominants that resolve, ii removed (merged with DRES) | Geometer and Listener | Estimate, slightly negative |
| TE: area of key position against tension | Geometer | Waits (cap of eight; unstable across chart writers) |
| Signature shape look-alikes | Geometer | Withdrawn (unstable across writers) |
| ii-V read upstream, and the iReal gap | Listener | Merged into the confirmation; old-song lead |
| Cadence arch (when resolutions arrive) | Listener | Waits (unstable across writers) |
| Fifths-plane area of roots | Listener | Withdrawn: it is chirality |
| IRR: walk left after cancelling detours | Inventor | Estimate, opposite sign |
| VR4c: runs of fifths | Inventor | Estimate, nothing |
| TYP: how typical a song's shape is | Inventor | Estimate, nothing |

**Where they agreed:** all four accepted that the pass's real question was the chart-writer worry, merged the two "resolving dominant" measures, and agreed with the Skeptic that only one or two tests could have power on 1,283 songs. **Where they split:** the Skeptic warned that the Real Book is not truly "before covering" (it was compiled from famous recordings) and that only about 110 pop transcriptions read an original recording; the Listener and Geometer still thought the upstream readings worth running as estimates.

## First principles

**The obstacle.** The lead lives only in jazz repertoire, where the chart writers, the performers and the cover counts are one community, and every song with chords and names on this machine has now been used.

**The way through (partly speculation).** Use time instead of new songs: ask whether the ii-V share predicts artists who took a tune up after its charts existed. This pass did that on old songs and the lead held (+0.044 with momentum held). To make it a finding it needs artists after July 2024 (a newer Discogs dump) or unseen jazz tunes from another chord source; about 1,100 such tunes would give power 0.5.

**Deleted (recommended; you decide):** the resolving-dominant measures (TR, DRES), TQ, TYP, the iReal "gap" idea, and the signature family as a predictor of recordings on present evidence. IRR's reversal is not promoted. VR4c failed nothing and waits for power. The ii-V share as a general judge of songs is retired; as a marker of jazz repertoire it stands.

**Simplified:** one number, the ii-V share, for jazz tunes, against artists who recorded the tune, now including artists who came after the charts.

**Flagged for you:** restoring run 08's power-0.5 condition for confirmations (at 0.37 the likeliest result was the one we got); requiring title plus writer matches; making agreement between chart writers a binding gate; and still no measure of "love" beyond recordings.

## The papers

1. **Chevyrev and Kormilitzin, "A Primer on the Signature Method in Machine Learning"** [1]. The mathematics of path signatures: iterated integrals, the Lévy area, Chen's identity, the uniqueness theorem up to tree-like detours, and the lead-lag trick that turns ups and downs into an area. It gave this pass's five geometric measures.
2. **Lee and Jeong, "JSIR: An Audio-Aligned, Multi-Task Dataset of Jazz Standard Recordings"** [2]. 44 jazz standards, each with a lead sheet and 4 to 9 recordings' chords. A quick check found recordings play as many ii-Vs as the lead sheets (about 0.15 of chord changes), but the lead sheets were built from the recordings, so it cannot settle the chart-writer worry.

## Ideas for coming passes (could not be tested this pass)

- **The late-window lead on artists after July 2024:** needs a newer Discogs data dump (not reachable from here).
- **A powered check on unseen jazz tunes:** needs about 1,100 tunes with title, composer and chords from outside ChoCo.
- **A check outside jazz:** needs pop, rock and folk chord charts with names, several thousand.
- **Cadence arch and key-against-tension areas:** frozen, waiting for unseen songs.
- **The MusicLab ceiling and cross-genre breadth:** data not on hand.

## Paywalled papers

None this pass.

## Fix list

The proposed fix list for the maintainer is the Doc "Proposed fix list: judging research, run 09" (https://claude.ai/artifact/BXZRqqxiFxoeCbm6EK9sRz); the same text is in `run09/proposed_fixlist.md`. This report is published as the Doc "Judging research, run 09" (https://claude.ai/artifact/RH7H79gxTgx5RopbDNi3XS).

## References

1. Chevyrev, I. and Kormilitzin, A. (2016; v2 2025). A Primer on the Signature Method in Machine Learning. arXiv:1603.03788. https://arxiv.org/abs/1603.03788
2. Lee, S. and Jeong, D. (2026). JSIR: An Audio-Aligned, Multi-Task Dataset of Jazz Standard Recordings. arXiv:2610.15356. https://arxiv.org/abs/2610.15356 ; data https://github.com/MALerLab/JSIR (CC BY-SA 4.0)
3. de Berardinis, J. et al. (2023). ChoCo: a chord corpus. Zenodo 7706751 (CC BY 4.0). https://zenodo.org/records/7706751
4. Araz, R. O., Serra, X. and Bogdanov, D. (2024). Discogs-VI. Zenodo 13983028 (CC BY-SA 4.0). https://zenodo.org/records/13983028
5. Run 09 commits on judging-research: 379e219 (predictions), 687e735 (results), 4055742 and 780e2c2 (the two after-seeing-results rules), 7fa66b2 (their results and every RESULT.md).
