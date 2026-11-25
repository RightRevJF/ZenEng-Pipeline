# Run 05: the chair's picks

25 November 2026. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Jason's rule applies: every idea that can be tested tonight on the data at hand is tested.

No outcome was opened before the rules were frozen: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, and nothing was split by match status. My checks used the notes only (scratch scripts in /tmp/chair, outside the repo). **Run 05 does not touch the McGill hold-out.** Song 59 and its folders were not read.

## What changed tonight
The full Hooktheory notes are on hand (`searches.md`: Sheet Sage's `Hooktheory.json.gz` from raw.githubusercontent.com, kept outside the repo). So any measure computed from the notes can now be tested on all 9,588 within-artist songs, not only the 2,224 in Discogs-VI. The outcome is run 04's **y_foreign**: did a performer set sharing no name with the original artist release the song.

## Tonight's tests: seven folders

**Each test needs p < .05/7 = .00714 (two-sided, z 2.690)**, plus the same sign in both artist halves (md5 of the artist slug) and a converged conditional logit of the same sign. The threshold does not move if a test is stopped. Each script reruns its gate before reading any outcome.

| Folder | Idea | Songs | Prediction on y_foreign | Kill | Power at p < .00714 |
|---|---|---|---|---|---|
| `loop_margin/` | M, the certified loop margin (G1 = L1 = I1; card 1) | 9,576 | **+0.8 pp per SD** | below +0.3 | 0.08 |
| `arrow_of_time/` | A, detailed-balance asymmetry of chord changes (I3, absorbing G2) | 8,774 | **+0.6** | below +0.2 | 0.06 |
| `harmonic_freedom/` | I2, neutral neighbours (revised) | 9,049 | **+0.6** | below +0.2 | 0.05 |
| `melody_range/` | L2, folded melody range | 9,588 | **−0.7** | above −0.2 | 0.10 |
| `fifths_path/` | R03-F1 on the extensive margin (R04-G1 merged in) | 9,588 | **−0.6** | above −0.2 | 0.06 |
| `tonic_resistance/` | R03-I2 on the extensive margin | 9,009 | **−0.6** | above −0.2 | 0.06 |
| `fame_vs_notes/` | The Skeptic's fame-versus-notes test (card 2) | 9,588 | fame beats notes across artists; notes add < 0.01 AUC | notes add ≥ 0.01 AUC (interval above 0), or notes ≥ fame | see below |

Two of the seven are mathematical in the strict sense: `loop_margin` (persistent homology of a sliding-window embedding, with card 1's subsampling confidence bound) and `arrow_of_time` (reversibility of a Markov chain). `tonic_resistance` (effective resistance on a graph) and `fifths_path` (a Fourier phase) carry over from run 03.

### The shared model
- **Rows:** run 04's 9,588 songs by 1,741 artists with two or more songs (`common.load_rows()`). Songs where a measure is undefined drop from that test; artists are not re-filtered.
- **Outcome:** y_foreign as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Reported, deciding nothing: y, the intensive margin (log(1 + covers) among versioned songs, with `first_year` as a control), and y_foreign with karaoke and tribute sets removed.
- **Columns:** z(measure), z(`ch_rep`), z(`ch_ic_mean`), run 04's control block, artist fixed effect, plus each test's own extras: ch_rep² and ln anchors for M; ln(changes) for A; melody pcs per span for I2; `mel_ic_mean` for L2; distinct-chord dummies and links for H.
- **Model:** LPM with artist demeaning and CR1 by artist (`common.lpm`); the same in each half; conditional logit as a sign check.

## Merges and rulings
- **G1 + L1 + I1 → `loop_margin`.** One measure, card 1's TopPT margin on chord chroma. The brainstorm's freeze is kept exactly: P ∈ {2, 4} bars, B = 200, ¼-beat anchors capped at 300, b = ⌈0.99n⌉, m = 8, τ = P/9, Z/11, seed 0. **Compute:** I timed it on every clip before freezing. All 16,563 clips took 17.6 minutes on the machine's 2 cores, inside the 45-minute budget, so nothing was cut.
- **The ln-anchors control: counted before deduplication**, at P = 2 bars. The radius shrinks as the cloud grows, so the count is held. Counting after deduplication would partly hold M itself, since an exact loop loses its repeated windows (ρ with M: +0.25 before, +0.12 after). The after-deduplication count is reported.
- **G2 + I3 → `arrow_of_time`.** ρ(A, G2) = −0.96 on 8,774 songs. A decides; G2 is reported. Clips need 6 or more chord changes, and song values are weighted by changes. I added ln(total changes) as a column, because A leans towards 1 when changes are few.
- **R04-G1 (diatonicity) merged into `fifths_path`.** ρ(FP, D5) = −0.73 on the 9,588 songs, over the 0.7 renaming line; run 04 found −0.65 on the matched songs. Its author withdrew it in run 04 because its sign was set after FP leaned. FP decides and D5 is reported.
- **The fame test, cleaned up.** The Skeptic's three parts and five pass/kill clauses became one rule on two cross-validated AUC differences, grouped by artist: D = AUC(fame) − AUC(notes) and Δ = AUC(fame + notes) − AUC(fame). It **passes** if D's (1 − .00714) artist-bootstrap interval sits above 0 and Δ < 0.01. It is **killed** if Δ ≥ 0.01 with its interval above 0, or if D ≤ 0. The fame proxies are on hand: ln(the artist's number of Hooktheory songs among the 13,198) and ln(clips per song). The within-artist partial R², the ch_rep × fame interaction and the shuffle placebo are reported. This test partly tests the yardstick and the project's premise, so it compares across artists on purpose.

## Left out, and why
- **Withdrawn by their authors:** L3, contour surprise (it measures how repeated notes were transcribed).
- **Stopped on the measure side by their authors tonight (no outcome joined):**
  - loop thickness (residual clip-to-clip 0.05; ρ −0.68 with M);
  - uncertified p1 (0.06);
  - the second H1 bar (0.16);
  - the melody margin (0.11);
  - melody plus chords (0.19);
  - "the tune changes when the chords return" (0.155 to 0.18);
  - phrase-end tonic closure (0.14).
- **R03-G1, shuffle-relative curvature: left out.** It is repetition renamed: ρ −0.62 with `ch_rep` (−0.52 in run 03's curvature test). It makes no claim beyond `ch_rep`, which every test already holds. Its family, geometry built from pooled clip maps, was recommended for deletion in run 03 and again in run 04's first principles. Jason decides; I did not revive it.
- **Stopped at a measure gate in earlier runs (kept stopped):**
  - R02-gap (clip-to-clip 0.17);
  - R03-G3, the obtuse statue (0.154);
  - R03-I1, melody transport (0.195).
  
  Tonight's songs are a superset of the songs they failed on. Rerunning a failed gate on more pairs until it clears would turn the gate into a fishing step, so I did not.
- **R04-FV (the two-part story for ch_rep on y_foreign): no fresh songs.** Every within-artist song with notes was used for ch_rep on y_foreign in run 04. Fresh songs need a re-match (`DATA.md`). `ch_rep` is a column in every model tonight, but its coefficient decides nothing.
- **Data not on hand (`DATA.md` names the files):**
  - W01-J6a, early covers for new songs;
  - W01-J6c, MusicLab;
  - R02-breadth, cover breadth across genres;
  - fresh songs for R04-FV.
- **Retired earlier:** W01-J4. **Waiting on a pass:** W01-J6b, the McGill hold-out.

## Gates, checked on the notes alone

| Measure | Two clips agree (≥ 0.20) | Largest overlap (≤ 0.7) | Verdict |
|---|---|---|---|
| M | 0.369 (4,247 pairs) | n_ch −0.254 | passes |
| A | 0.302 (3,294) | ch_ic_mean +0.152 (G2, merged, −0.96, not in the model) | passes |
| I2 | 0.267 (3,796) | pcs per span −0.343 | passes |
| L2 | 0.290 (4,271) | mel_ic_mean +0.555 | passes |
| FP | 0.407 (4,268) | ch_ic_mean +0.286 (D5, merged, −0.73) | passes |
| H (run 03's residualised gate) | **0.203** (3,512) | beats −0.081 (H_res); R² on size 0.16 | passes, narrowly |

Cross-overlaps among tonight's measures are small: the largest are A with H (+0.28) and M with A (+0.19).

## Power, plainly
- **How it was computed** (as in run 04): the binary-outcome bound, SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²). Here x̃ is the measure's residual within artist after every other column. Each script prints power again from its own clustered SE before any estimate.
- **The table:**

| Test | Residual share | SE (pp) | Power at p < .00714 | at p < .05 | Kill fires if the prediction is true | Kill fires if the effect is 0 |
|---|---|---|---|---|---|---|
| loop_margin | 0.459 | 0.63 | 0.08 | 0.25 | 21% | 68% |
| arrow_of_time | 0.667 | 0.54 | 0.06 | 0.20 | 23% | 64% |
| harmonic_freedom | 0.601 | 0.56 | 0.05 | 0.19 | 24% | 64% |
| melody_range | 0.748 | 0.49 | 0.10 | 0.30 | 15% | 66% |
| fifths_path | 0.670 | 0.52 | 0.06 | 0.21 | 22% | 65% |
| tonic_resistance | 0.652 | 0.54 | 0.06 | 0.20 | 23% | 64% |

- **The fame test:** simulated on synthetic outcomes using the real predictors. It passed 6 of 6 in a fame-only world, was killed 6 of 6 when the notes add about 0.045 AUC, and was mixed at the boundary (notes add about 0.01: pass 4, kill 1, unsettled 3 of 8).
- **Against the floor:** every slope test is far below run 03's proposed 0.5 floor. That floor is Jason's undecided proposal, so power is printed and does not block. Run 04's first principles also flagged not counting tests under power 0.2 on seen songs, also Jason's call. I counted all seven, which keeps the threshold conservative.
- **What to expect:** a pass is unlikely even if a prediction is true. The kill lines decide most results, so a kill is the likeliest informative outcome and a null clears nothing.

## Practical notes for the experimenters
- **statsmodels is not installed** on this machine (the import fails), and `common.cond_logit` needs it. Install it before running, or maximise the exact conditional likelihood with scipy (BFGS, then Newton), as run 04 allowed. Without convergence a test cannot pass.
- **The songs are not unseen.** Run 04 used the same 9,588 songs for `ch_rep` and `ch_ic_mean` on y and y_foreign, and run 03 used the matched songs' FP and H on covers. Tonight's measures and the extensive contrasts for FP and H are new.
- **Each PREDICTION.md gives unit values** the script must reproduce before reading anything else.
- **The H gate is the narrowest of the night** (0.203 against 0.20). It must be coded exactly as written, and it stops if it falls below the line.

## Ranking
Seven qualified, fewer than eight, so all run tonight. If an order is wanted, by power and novelty:
1. `loop_margin`
2. `melody_range`
3. `fame_vs_notes`
4. `arrow_of_time`
5. `fifths_path`
6. `tonic_resistance`
7. `harmonic_freedom`
