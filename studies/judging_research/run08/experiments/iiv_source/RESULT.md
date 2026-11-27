# iiv_source: result (written after seeing results; an estimate on seen songs; decides nothing)

**In plain words.** `iiv_chunk` found that songs with more ii-V steps get covered more. A rival explanation is that the jazz players who write iReal Pro charts add ii-Vs to tunes they already play, so the measure would partly reflect "already popular with jazz players" rather than the song itself. To check, we read the ii-V share only from Wikifonia lead sheets, which were mostly typed in from published sheet music, on the 1,128 songs that have both kinds of chart. The Wikifonia reading came out near zero. But the iReal reading of the *same* songs also came out near zero, so this small subset shows no effect from either source and cannot tell the song apart from the chart writer. These songs were already used in `iiv_chunk`, and the test was far too small to detect an effect of the expected size.

**Predicted (frozen in b1b3512).** +0.07 SD per SD for the Wikifonia reading. Status ESTIMATE: no pass and no kill.

**Power (printed before the estimate):** 0.06 (α = .05/6, composer share 0.3, fake SE 0.048, 300 draws). PREDICTION.md says 0.05; that is the same calculation, rounded. Far below the 0.2 floor.

**What came out (result.json).** Composer fixed effects plus decade dummies (one genre bin), N 1,128, 466 composers.

| IIV read from | β | SE | p | 95% range |
|---|---|---|---|---|
| Wikifonia only | +0.021 | 0.039 | 0.59 | −0.055 to +0.097 |
| iReal only (same songs) | −0.006 | 0.048 | 0.89 | −0.100 to +0.087 |

Spearman correlation of the two IIV readings across songs: 0.619.

**Verdict.** None (an estimate). Both ranges contain the predicted +0.07 and contain zero.

**How firm.** Not firm. The point estimates would suggest the Wikifonia reading is no weaker than the iReal one, but the SEs are about two-thirds the size of the effect under test, and the iReal reading on this subset does not reproduce `iiv_chunk`'s +0.073 (SE 0.018, all 5,858 design songs). So the subset gives no baseline to compare against. Composers with only one song in the subset add nothing to a within-composer estimate, so the effective sample is smaller than 1,128.

**Renaming check (measure_gates.json, all design charts).** IIV two-chart stability 0.772; first-iReal vs first-Wikifonia chart agreement 0.584 (the same 1,128 songs); within-composer ρ with ch_rep −0.021, with V +0.217. It passes, so IIV is not a renamed ch_rep or V. The gates were not computed separately for Wikifonia-only values.

**What it cannot say.**
- *Song vs chart writer:* not settled (see above). That Wikifonia came from published sheet music is an assumption, and was not checked here.
- *Seen songs:* this re-uses the songs and the outcome that `iiv_chunk` already used.
- *Genre within composer, jazz idiom:* genre is one bin here. Songs with both chart types lean toward jazz-repertoire standards.
- *Selection:* a song that has both a Wikifonia and an iReal chart is not a typical song.
- *Name matching:* the same composer-key and title matching limits apply as in the design.
