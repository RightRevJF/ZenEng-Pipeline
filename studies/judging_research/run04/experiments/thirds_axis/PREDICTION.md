# The thirds axis |a₃|/a₀ of the chord profile: one two-sided test, counted once. Frozen before any outcome is joined

Run 04, 24 November 2026, by the chair. **One hypothesis, counted once (R04-G3 against R04-I1).** No cover count, version, release, `first_year`, versions file or `covers.json` has been opened. "Chair" = notes-only checks on the 2,672 songs of `hooktheory_clips.json.gz` with 3 or more distinct chords. **Run 04 does not touch the McGill hold-out.**

## Claims (Amiot, Lemma 2 and Theorem 1)
Transposing by t multiplies a₃ by e^{−iπt/2}. Chords a major third apart add on the thirds circle. Chords a whole step apart (IV–V, ♭VII–I), which share no tone, cancel. Theorem 1 makes |a₃|/a₀ invariant under transposition and inversion, so a cover's re-keying leaves it unchanged.
- **G3 (Geometer):** a high D3 means shared tones between chords. **Extrapolation:** the tune fits either chord, so coverers can reharmonise. Higher D3 goes with **more** covers.
- **I1 (Inventor, withdrawn as a reading but kept as the other side):** a low D3 means tonic, subdominant and dominant regions balanced. Lower D3 goes with **more** covers. The Skeptic showed that IV–V alone scores 0 with no tonic.

The two sides are the same number with opposite signs, so the test is one two-sided test, counted once.

## Rows and model
As `../plr_share/PREDICTION.md`, which follows run 03's fifths_path and bridge:
- songs from the `video` values of `hooktheory_clips.json.gz`, with clips also present in the surprise and rhythm files;
- 3 or more distinct tokens;
- after the gate, a truthy `first_year`, then artists with 2+ songs;
- run 03's `within()` with CR1, and md5 halves.

Songs with an undefined D3 are dropped before the artist rule (chair: none).

## Measure (frozen)
- **Per clip:** v[x] = Σ (`offset` − `onset`) over every harmony event with a positive duration, for each pitch class x in the event's set {root} ∪ {(root + cumulative sums of `root_position_intervals`) mod 12}. Each pitch class is counted once per event. Absolute pitch classes are used, since the magnitude does not depend on the key.
- **D3_clip** = |Σ_x v[x]·e^{−2πi·3x/12}| / Σ_x v[x]. It is undefined if Σ v = 0.
- **Song D3** = the plain mean of D3_clip over the song's clips where it is defined. *Chair: 10th / 50th / 90th percentile 0.153 / 0.302 / 0.469.*
- **Unit values (equal durations; must reproduce):**

| Chords | D3 |
|---|---|
| One major triad | 0.745 |
| I–vi | 0.667 |
| I–V–vi–IV | 0.333 |
| I–IV–V | 0.248 |
| ii–V–I | 0.111 |
| IV–V | 0 |

- **Invariance check:** D3 must be unchanged (to 1e-9) when 3 random clips are transposed by 5 and inverted (x → −x).

## Gate (before any outcome-side field; failing either records "stopped" and no outcome is joined)
1. **Clip-to-clip:** D3 of clip 1 vs clip 2, Spearman **≥ 0.20**. *Chair: 0.318 (1,281 pairs).*
2. **Overlap:** |Spearman| **≤ 0.7** with each of the 17 data-pack measures, distinct chords, links and clips. *Chair: largest −0.25 (`ch_ic_mean`); distinct chords −0.23.* Printed, deciding nothing: TS −0.34, PLR +0.26, FP about 0.

## Model columns
D3, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, and dummies for distinct chords 4…11 and 12+.

## Prediction
**β = +0.02 SD of log(1 + covers) per SD of D3** (G3's figure). I1 predicted −0.025.

## Power (notes-side; printed again by the script from its SE before β)
- **Residual share** after the artist fixed effect and the columns above (first year unavailable notes-side): D3 0.643, FP 0.679.
- **SE** ≈ 0.018 · √(0.679/0.643) = **0.0185**.
- **Power at +0.02, p < .01 two-sided: 0.068** (0.19 at p < .05).
- **Power floor:** far below the proposed 0.5 floor (R03-4, undecided). Printed, not blocking.

## Rules (exact; p < .05/5 = .01, two-sided, because tonight counts five hypotheses)
- **G3 passes, I1 killed:** β > 0, p < .01, and β > 0 in both artist halves.
- **I1 passes, G3 killed:** β < 0, p < .01, and β < 0 in both artist halves.
- **Both killed:** −0.01 < β < +0.01.
- **G3 unsettled, I1 killed:** β ≥ +0.01 and G3 does not pass (p ≥ .01 or split halves).
- **I1 unsettled, G3 killed:** β ≤ −0.01 and I1 does not pass.
- The threshold does not move if any other test is stopped.

## Reported, deciding nothing
- Covers within 5 years and more than 10 years after `first_year`.
- β without `ch_ic_mean`.
- β with PLR added.
- The share of songs with D3 below 0.05 (near whole-step cancellation).

## What it cannot say
- **Not fresh:** these are run 03's songs, so a pass is a lead for unused songs.
- **What D3 counts:** it sums chord time with no order. IV–V cancels whether or not a tonic follows, so neither reading is measured directly; only the sign is.
- **Low power; no cause; hits only.**
- **McGill:** the hold-out is untouched.
