# Steps around the circle of fifths: a fixed-space path, frozen before any outcome is joined

Run 03, 23 November 2026, by the chair. **After seeing results:** frozen after the bridge and curvature outcomes were read (Jason's rule: what can be tested tonight is tested tonight). A pass is a lead needing confirmation on unused songs, never a finding. No cover count, version, release, `first_year` or versions file was opened. "Chair" = a notes-only check on the 2,672 songs with ≥ 3 chords.

## Claim (new; `first_principles.md` §6)
Tonight's geometry failed because each song built its own tiny space. Here the space is fixed: each chord is a point on the fifths circle, the phase of its 5th Fourier coefficient (Amiot). A song is a path; a short song is a noisier reading, not a different geometry.

## Direction, chosen from first principles before any outcome
Two notes findings exist. **Chord surprise (−0.042):** less expected chords, fewer covers. **Chords that move (`ch_rep`, −0.042):** more 3-gram repetition, fewer covers. Step size is about *distance*, not *recurrence*: a I–V–vi–IV loop repeats fully yet steps small; non-repeating chromatic-mediant moves step large. So it speaks to plainness, the surprise side. Prediction: **smaller steps (plainer motion around the circle), more covers.** Both `ch_rep` and `ch_ic_mean` are held, so the test asks whether a fixed-space distance carries plainness beyond corpus surprise.

## Rows, chord sequence and model
Exactly as `experiments/bridge/PREDICTION.md`: the same rows, chord token, merging, wrap rule, data-pack measures weighted by `n_mel`, the `within()` model, CR1 clustered SE, md5 artist halves.

## Measure
- **Chord set:** for each merged run (consecutive equal tokens), the pitch-class set of its first event relative to the clip's tonic (`keys[0].tonic_pitch_class`, 0 if none): S = {r} ∪ {(r + cumulative sums of `root_position_intervals`) mod 12}, r = (root − tonic) mod 12.
- **Phase:** f5(S) = Σ_{k∈S} exp(−2πi·5k/12); θ = `numpy.angle(f5)`. If |f5| < 1e-6 (augmented triad, diminished seventh, tritone) the chord has no phase.
- **Moves:** run i → run i+1, plus the wrap last → first when tokens differ (exactly the moves of M). Skip a move if either chord has no phase (chair: 426 of 68,314).
- **Step** = shortest arc |θ_x − θ_y| on the circle, in radians, in [0, π].
- **FP** = the plain mean of the step over every kept move in all of the song's clips. Size-free by construction.
- **Unit values** (must reproduce): I→V, I→IV, I→vi, ii→V each π/6 = 0.524; I→iii, I→♭VII, I→i, IV→V each 1.047; I→♭VI 2.094; I→♭II 2.618; V→vi 0; I→ii 0; V7 has the same phase as I.
- *Chair:* median 0.663 (10th to 90th 0.428 to 1.047); no song undefined.

## Gate (before any outcome; failing either records "stopped", no outcome joined)
1. **Clip-to-clip:** for songs with 2+ clips, FP of clip 1 alone against clip 2 alone (surprise-file order, both defined); Spearman **≥ 0.20**. *Chair: 0.356 (1,281 pairs).*
2. **Overlap:** |Spearman ρ| with each of the 17 data-pack measures, distinct chords, links and clips **≤ 0.7**. *Chair: largest +0.22 (`ch_ic_mean`); distinct chords +0.19, `ch_rep` −0.11; R² on the size block 0.02.*

Chair's verdict on the gate: **passes**. It is the most stable of tonight's six measures.

## Model columns
FP, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, the nine distinct-chord dummies.

## Prediction
**β = −0.02 SD of log(1 + covers) per SD of FP**, within artist: smaller steps, more covers. Smaller than surprise's −0.042 because surprise is held and shares part of the same plainness (ρ +0.22).

## Power
Printed before β: power = Φ(0.02/SE − 2.638) + Φ(−0.02/SE − 2.638). Chair: SE ≈ 0.016, **power ≈ 0.08**.

## Rules
Tonight counts six tests, so each needs **p < .05/6 = .0083, two-sided**.
- **Pass:** β < 0, p < .0083, and β < 0 in both artist halves.
- **Kill:** β > −0.01.
- **Unsettled:** anything else, including a split between halves.
- **Opposite sign** (β > 0, p < .0083): a new hypothesis ("bold steps are what coverers take up"), not a pass.

## Reported, deciding nothing
Covers within 5 years and more than 10 years after `first_year`, as in the bridge experiment; β without `ch_ic_mean` (expected more negative if FP shares surprise's plainness); the share of zero steps.

## What it cannot say
- **Coarse geometry:** f5 phase is a chord's centre on the fifths circle, not its function. I, ii and V7 share a phase, as do V and vi, so V7→I and V→vi count as no step. Thirds-circle (f3) motion and voice-leading distance are not measured.
- **Low power:** a null clears nothing.
- **After seeing results:** a pass is a lead for unused songs only; this idea was written tonight, after two outcomes.
- **Key:** step size is transposition-free, but modulations inside a clip are not followed.
- **No cause; hits only; McGill untouched.**
