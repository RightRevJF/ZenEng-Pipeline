# Harmonic chirality: do songs whose chords turn clockwise round the circle of fifths go with uptake by other artists? Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Idea R06-I1 (the Inventor), in the open-walk form he froze in round 2 after the Skeptic's warning about wrapped walks. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, nothing in `/home/claude/shape/`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks (`../common.py`, `../power_fake.py`; scratch in /tmp/claude-0/r6/chair).

**Tonight counts six tests** (`chirality`, `fresh_repetition`, `fresh_arrow`, `fresh_range`, `fresh_tonic`, `fresh_diatonic`). **Each needs p < .05/6 = .00833, two-sided (z = 2.638).** The threshold does not move if a test is stopped.

## Claim and the mathematics
Put each chord's root on the circle of fifths. A progression then traces a path round the circle, and its signed area says which way it turns. Falling fifths (ii–V–I, each chord a dominant falling home) turn clockwise; I–V–vi–IV turns counterclockwise.

- **Green's theorem on the Hodge cycle part** (cards 1 and 2). For a closed walk the net flow F of chord moves has zero divergence, so it is pure cycle part C, and the swept area is ⟨C, ω⟩ for the area 1-form ω. Moves that go and come back, and tree-like detours, add exactly 0.
- **The only new axis.** Last night's arrow A, and entropy production, are unchanged when a song is played backwards. Chirality changes sign. On the notes it is unrelated to A (ρ +0.07), to repetition (+0.07) and to size (V −0.12, ln K −0.03).
- **Extrapolation (the Inventor's, labelled as such):** the most re-recorded repertoire, the standards, turns clockwise. So within an artist's own songs, songs that turn clockwise (negative CH) are more often taken up by another artist.

## Measure CH (frozen; `common.CH_clip`)
Per clip, from the raw Hooktheory annotations (`run05 common.raw_clips()`):
1. Harmony events sorted by `onset` (Python's stable sort), each mapped to `run05 common.chord_pcs(h)` (absolute pitch-class set; inversions ignored; extensions kept).
2. Collapse consecutive equal sets into runs s₀ … s_K. Each run's root is the `root_pitch_class` of its first event. K = number of changes. **K < 6: no value.**
3. θ_t = 2π · ((7 · root_t) mod 12) / 12.
4. **CH = (1/K) · Σ_{t=0}^{K−1} ½ sin(θ_{t+1} − θ_t).** Open walk: no move from the last run back to the first. No settings.

**Song value:** the mean of the clip values over clips that have one, **weighted by each clip's K** (as for A). No clip value: the song drops from every model of this test.

**Unit values** (one chord per beat, tonic C; the script must reproduce them before anything else):

| Progression | K | CH (open, frozen) | CH wrapped (reported) | A |
|---|---|---|---|---|
| I–V–vi–IV ×4 | 15 | **+0.1167** | +0.1333 | 1.0000 |
| I–IV–vi–V ×4 (its reverse) | 15 | **−0.1167** | −0.1333 | 1.0000 |
| I–vi–ii–V ×4 | 15 | **−0.0500** | −0.0667 | 1.0000 |
| ii–V–I ×5 | 14 | **−0.0549** | −0.0239 | 1.0000 |
| I–IV ×8 | 15 | **−0.0167** | 0.0000 | 0.0667 |
| I–V ×8 | 15 | **+0.0167** | 0.0000 | 0.0667 |
| I–V ×2 | 3 | no value (K < 6) | | |

(The Inventor's wrapped values, I–V–vi–IV +0.133 and I–vi–ii–V −0.067, are reproduced. A back-and-forth vamp is 0 when wrapped; the open walk leaves one unpaired move, worth ½ sin(Δθ)/K, here ±1/(4K).)

*Chair:* **8,774 of the 9,588 songs have a value** (by 1,727 artists; 878 / 849 per half); 10th / 50th / 90th percentiles −0.083 / +0.005 / +0.104; mean +0.0078, **SD 0.0771**; 53% above 0, 2% exactly 0. Open and wrapped forms agree at ρ 0.918.

## Songs
Run 04's rows from `run05 common.load_rows()`: 9,588 songs by 1,741 artists with two or more songs; halves `r['half']` (md5 of the artist slug mod 2). Songs with no CH drop; artists are not re-filtered.

## Outcome
**Primary: y_foreign**, exactly as `run05 common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign NaN are dropped. Call it through `common.guard(HERE)` first, so that this file and `../common.py` must both be committed.

## Columns
- **z(CH)** over the songs with a value (population SD).
- z(A) (run 05's arrow, `common.A_clip`, K-weighted; same clips as CH), z(`ch_rep`), z(`ch_ic_mean`), all scaled over the 9,588 rows (the seen mean and SD of songs with a value).
- **V** (`common`: distinct chord pitch-class sets per clip, mean weighted by K) and **ln_chg** = ln(max(total K over the song's clips, 1)). The Skeptic's size controls.
- Run 04's control block, `run05 common.controls(rows)`.
- Artist fixed effect.

*Chair:* within artist, V, ln K, A and ch_rep explain R² 0.009 of CH (the Inventor's check).

## Model
- **LPM:** `run05 common.lpm(X, y_foreign, artist)`: demeaned, no constant, CR1 by artist.
- **Halves:** the same LPM within each half.
- **Conditional logit:** `run05 common.cond_logit` (statsmodels 0.15 is installed), same columns, not demeaned. Print drops and convergence. No convergence, no pass.

## Gate (notes only; before the outcome; failing records "stopped")
`run05 common.gate(rows, "CH", extra={"ln_chg": …, "V": …, "A": …})`:
1. Clip 1 vs clip 2 Spearman **≥ 0.20**. *Chair: 0.252 on 3,294 pairs.*
2. |Spearman| **≤ 0.7** with the 17 data-pack measures, n_ch, beats, clips per song, ln_chg, V and A. *Chair: largest ch_ic_mean −0.141.*

Chair's verdict: passes.

## Prediction
**β(CH) on y_foreign = −0.6 percentage points per SD** (clockwise, more uptake), within artist.

## Rules
- **Pass:** β < 0 and two-sided p < .00833; β < 0 in both halves; conditional logit < 0 and converged.
- **Kill:** β > −0.2 (wrong sign, or weaker than −0.2).
- **Opposite sign** (β > 0, p < .00833): killed, and reported as a new hypothesis ("counterclockwise loops such as I–V–vi–IV are what others take up"), not a pass.
- **Unsettled:** anything else.

## Power (fake outcomes on these rows and columns, `../power_fake.py`, before any outcome)

| | SE (pp) | Pass rate if −0.6 is true | Power at p < .00833 | at p < .05 | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|---|
| calibrated (run 05's real SE) | 0.38 | 0.135 | 0.15 | 0.35 | 15% | 71% |
| homogeneous (22% everywhere) | 0.51 | 0.074 | 0.07 | 0.22 | 21% | 63% |

The notes-side bound is 0.51 pp. This is the night's best-powered test, and still far below run 03's proposed 0.5 floor (Jason's undecided proposal; printed, not blocking). A kill is the likeliest informative result.

## Reported, deciding nothing
- The wrapped form (`CH_clip(a, wrap=True)`) in place of CH; |CH| in place of CH.
- The model without z(A) and V; without z(ch_ic_mean).
- β(CH) on y; the intensive margin (z(log(1 + covers)) among songs with y = 100, non-null covers and a first_year, same columns plus `first_year`); y_foreign with "karaoke" or "tribute" sets removed.
- **CH on the fresh songs**, only after `../fresh_repetition/PREDICTION.md`'s validation passes: the fresh design of that file with z(CH) (seen SD 0.0771) and extra columns z(A) and z(ch_rep). *Chair:* 888 fresh rows by 448 artists; SE about 1.06 pp, power 0.02. Its sign is frozen here as negative, but it decides nothing tonight: CH's one counted test is the seen one, and a second counted look at the same idea on the same night would only dilute the threshold.

## Order the script must follow
1. Unit values (must reproduce). 2. Rows and CH, A, V, ln_chg from the notes; percentiles. 3. Gate; stop if it fails. 4. Notes-side power. 5. `common.guard`, then `load_outcomes`. 6. Counts. 7. Clustered SE and power at −0.6, p < .00833. 8. β, halves, conditional logit, verdict. 9. Reported items (the fresh reading last, and only if validation passed). 10. `result.json`.

## What it cannot say
- Genre within artist: falling-fifth ballads against plagal rock (the Skeptic). Within artist absorbs most of it, not all.
- y_foreign is not lasting love. The 9,588 songs were used in runs 04 and 05; CH is new on them, but they are not unseen.
- The circle-of-fifths position ignores chord quality: a minor ii and a major II sit at the same point.
- Low power; a null clears nothing. Hits only; no cause. The McGill hold-out is untouched.
