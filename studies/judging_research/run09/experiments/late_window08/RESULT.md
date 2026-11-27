# late_window08: result (a lead on seen songs, written after seeing results)

**What was asked.** Run 08's lead was that tunes with more "ii-V" moves (a minor-seventh chord stepping to a dominant seventh a fourth higher) are recorded by more artists. The worry is that the arrow runs backwards: iReal Pro charts are written by players of a tune as it is played now, so a much-recorded tune's chart may carry the ii-Vs its performers added. Artists who first recorded a song AFTER the charts were collected cannot have shaped them. ChoCo v1.0.0 was published on 7 March 2023 (Zenodo 7706751), so its charts were collected before then; Discogs-VI 20240701 holds releases up to mid-2024.

**The rule, written first** (commit 4055742, pushed before the outcome was read; this folder's PREDICTION.md). On run 08's 8,565 songs (seen: their total cover counts were opened in run 08), count the artist sets whose earliest dated release of the song is in 2023 or 2024 (n_new) and those from 2022 or earlier (n_prior). Regress the standardised log(1 + n_new) on the ii-V share, holding log(1 + n_prior), the five run 08 shape columns, genre and decade. Predicted **+0.03 SD per SD**, positive in both halves of the composers and in a Poisson model. Labelled after seeing results and on seen songs: a lead, never in the pass's count (K stays 1).

**What came out** (`result.json`).
- 1,483 new artist sets in all; 11.9% of the songs gained at least one in 2023 to 2024. The middle song had 12 earlier artist sets.
- **Main estimate: +0.051 SD per SD (SE 0.012, p .00003), 95% range +0.027 to +0.075.** Halves +0.052 and +0.046. Poisson +0.068 (p .034).
- Power printed beforehand (fake outcomes, without the n_prior column, which cannot be built before the outcome): 0.68. The true power is lower, because most songs gained no new artist.

**Verdict by the rule: lead supported** (p < .05, positive, both halves positive, Poisson positive). +0.03 lies inside the range.

**Readings (deciding nothing).**
- Without holding earlier artist sets: +0.079 (SE 0.013).
- Within composer (run 08's model, 5,858 songs, 1,199 composers): +0.058 (SE 0.021, p .006).
- Genres other than jazz (4,017 songs): +0.018 (SE 0.018, p .30), halves +0.041 and −0.010. Unsettled, as in every non-jazz reading so far.

**How firm.** Firm as a lead on these songs: the estimate is four SEs from zero, both halves and both models agree, and it holds within composer. It says that among tunes equally taken up before the charts were collected, those whose charts have more ii-Vs gained more new artists afterwards. Those artists could not have put the ii-Vs into the charts, so the pure "the chart copies the covers" story is weakened.

**What it cannot say.**
- **Momentum.** A tune that jazz players are recording a lot is both charted carefully and recorded again; holding earlier artist sets absorbs only part of that. The coarse genre bins do not separate "a jazz standard still in the working repertoire" from "a song with ii-Vs".
- **Jazz only.** Outside jazz genres it is small and unsettled, matching this pass's "jazz repertoire" label from iiv_confirm09.
- **Seen songs, after seeing results.** It needs songs not yet used, or artists after July 2024 (a newer Discogs dump), to become a finding.
- **Thin window.** Eighteen months of releases, and Discogs lags new releases. Artist sets first dated January to early March 2023 slightly overlap the charts' collection.
- **The year is a set's earliest dated release of the song**, as the maintainer's `cliques_versions.py` stores it; undated sets are left out of both counts.

Credit: ChoCo (CC BY 4.0); Discogs-VI 20240701 (CC BY-SA 4.0).
