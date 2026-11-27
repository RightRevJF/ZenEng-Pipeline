# Repeat-and-contrast (cv_w) on songs by single-song artists: result

Run 07, 26 November 2026. **Written after seeing results** (rule committed at 6165846, before this outcome was joined). Figures from `result.json`.

**Killed.** The lead did not carry over.

**What was predicted.** In tonight's `tree_h4m` model, an uncounted column, cv_w (how unevenly far apart a song's 4-bar stretches are: some near-repeats, some strong contrasts), came out at +3.11 points per SD (p .0047). The first-principles reviewer froze a test of it on the only Lakh songs nobody had joined to an outcome: songs by artists with one song in the set. Prediction +1.5 points per SD on y_foreign, across songs; kill if β ≤ 0; pass (a lead only) at p < .05/9 = .00556 with both halves and a converged logit positive.

**What came out.**

| | β (pp per SD) | SE | p | N |
|---|---|---|---|---|
| **Main** (H4m and ch_rep held, notes controls, year bins) | **−0.13** | 0.81 | .87 | 3,348 |
| Half 0 | −0.02 | 1.18 | .99 | 1,685 |
| Half 1 | +0.005 | 1.14 | 1.00 | 1,663 |
| Logit (sign check, converged) | −0.014 | | .85 | |

- Power printed before the estimate: 0.06 (simulated base rate 40%). The real base rate here is **18%**, lower, as the PREDICTION warned single-song artists might be.
- 3,436 songs after 212 sharing a MIDI file with a seen song; 87 more dropped because their Discogs-VI clique was already matched by a seen song; 719 matched, 691 taken up by another artist.
- **Verdict by the rule written first: KILLED** (β ≤ 0). The kill fires 11% of the time if +1.5 were true and 50% if the effect is zero (PREDICTION.md), so the evidence moves about four to one against the lead.

**Readings that decide nothing:** bare cv_w +0.47 (p .46); first performers only +0.99 (p .15); fame held, style held (F, tempo) and shared cliques kept all near zero or negative (−0.63, −0.54). None is significant.

**What it means.** The within-artist cv_w reading was most likely the largest of many printed numbers (a winner's curse), as its author expected. On songs no one had looked at, contrast between sections shows nothing.

**What it cannot say.** Across artists, not within (genre and style not held); MIDI arrangements matched to recordings by audio; y_foreign is uptake, not love. It spent the last unseen Lakh outcomes except the 8,607 tracks on ambiguous files.
