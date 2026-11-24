# Run 04: the chair's picks

24 November 2026. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Jason's rule applies: every idea that can be tested tonight on the data at hand is tested.

No outcome was opened before the rules were frozen: no covers file, no versions file, no `covers.json`. Nothing was computed split by whether a song is matched to Discogs-VI. My checks used the notes only. **Run 04 does not touch the McGill hold-out** (`experiments/HOLDOUT_LOG.md`).

## Tonight's tests: four folders, five hypotheses

**Each hypothesis needs p < .05/5 = .01 (two-sided)**, plus the same sign in both artist halves (md5 of the artist slug, as in run 03). On the new outcome, the conditional logit must also agree in sign. The threshold does not move if a test is stopped.

| Folder | Hypothesis | Songs | Outcome | Prediction | Power at p < .01 |
|---|---|---|---|---|---|
| `move_extensive/` | H1: chords that move (`ch_rep`) | 9,588 in 1,741 artists | In Discogs-VI at all (0/1) | −1.0 pp per SD | 0.15 |
| `move_extensive/` | H2: chord surprise (`ch_ic_mean`) | same model | same | −1.0 pp per SD | 0.20 |
| `info_rate/` | Distance from the habitual surprise per beat | 9,574 | same | −0.8 pp per SD | 0.15 |
| `plr_share/` | Share of P/L/R moves on Amiot's torus | ~1,924 in 420 artists | log(1 + covers) | +0.02 SD per SD | 0.08 |
| `thirds_axis/` | \|a₃\|/a₀: G3 (+) against I1 (−) | ~1,924 | log(1 + covers) | +0.02, two-sided | 0.07 |

### The new outcome
Whether a Hooktheory song is in Discogs-VI at all, meaning at least two performer sets released it under one title and writer.
- **Size:** five times run 03's within-artist rows.
- **What it is not:** lasting love. A non-match is not a true "never covered".
- **Model:**
  - Linear, with artist fixed effects.
  - Every artist with two or more songs stays in. The Skeptic showed that artists with no matched song still count in a linear model; this was fixed before the join.
  - Held: chord-count bins, clips per song (a fame proxy), length, and three title flags from the slug (word count, parentheses, a title shared with another artist).
  - No first year exists for unmatched songs, so era comes only through the artist.

**Chord surprise counts as its own hypothesis.** It was found on cover counts and never stated first, and this contrast is unseen, so tonight is its first fresh test. A kill of it kills "plainly", not chords that move.

## What merged
- **G2 + L2 → `plr_share`.** The share of P/L/R moves is the measure. The mean torus step, its near-complement (ρ −0.70), is reported only.
- **G3 + I1 → `thirds_axis`.** Same number, opposite signs, so this is one two-sided test, counted once:
  - G3 passes if β > 0, p < .01, and both halves are positive;
  - I1 passes in the mirror case;
  - both die if |β| < 0.01;
  - otherwise the side the estimate leans to is unsettled and the other dies.
- **L1's composite → run 03's two-term form.** `ch_rep` decides; chord surprise sits beside it.

## Left out, and why
- **Withdrawn by their authors:**
  - G1, diatonicity: its sign was set after the fifths path leaned.
  - L3, the one chord you remember.
  - I2, the harmonic ratchet.
- **Stopped on the measure side (no outcome joined):**
  - Torus winding and signed area: whole-step moves are exact half-turns, so the sign is arbitrary.
  - R5: the fifths path renamed.
  - R03-G3 and R03-I1: run 03 gate failures.
  - R02-gap on Hooktheory. Its McGill outcome is the hold-out.
- **Data not on hand (`DATA.md` names the files):**
  - Tonic resistance, the fifths path and shuffle-relative curvature: they need the unmatched songs' notes (Sheet Sage's `Hooktheory.json.gz` or `m-a-p/HookTheory`).
  - Early covers for new songs.
  - MusicLab.
  - Cover breadth across genres: needs the Discogs releases dump.
- **Retired earlier:** W01-J4.
- **Waiting on a pass:** W01-J6b, the hold-out.

## Gates, checked on the notes alone
Each script reruns its gate before reading any outcome. The gate needs two clips of one song to agree at Spearman ≥ 0.20, and no |ρ| above 0.7 with a data-pack measure or the size block. All five pass:

| Measure | Two clips agree | Largest overlap |
|---|---|---|
| `ch_rep` | 0.32 | −0.44 |
| `ch_ic_mean` | 0.50 | +0.48 |
| Information-rate deviation | 0.28 | +0.17 |
| PLR share | 0.35 | +0.14 |
| D3 | 0.32 | −0.25 |

Printed, deciding nothing: chord surprise correlates +0.78 with its own spread (`ch_ic_sd`), which is outside the 17 measures and outside the model.

## Power, plainly
- **How it was computed:**
  - New outcome: the binary bound (variance 0.21 × 0.79) over each measure's leftover variance within artist.
  - Cover tests: run 03's fifths-path SE (0.018, same songs), scaled by leftover variance.
- **Against the floor:** all five are far below run 03's proposed 0.5 floor. That floor is Jason's undecided proposal, so power is printed and does not block. Each script prints power again from its own SE before the estimate.
- **What to expect:**
  - The new outcome gives two to three times the power of the cover tests, yet a true −1.0 pp still passes only about one time in six.
  - The torus tests reuse run 03's songs and are nearly blind.
  - A kill is the likeliest informative result; a null clears nothing.

## Ranking
Five qualified, fewer than eight, so no ranking is needed. If an order is wanted, by power and freshness:
1. Chord surprise.
2. Chords that move.
3. The information rate.
4. The two torus tests.

My check scripts are scratch files, not in the repo.
