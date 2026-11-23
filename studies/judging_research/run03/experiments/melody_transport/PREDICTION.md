# Does the tune move less than the chords under it? Melody transport, frozen before any outcome is joined

Run 03, 23 November 2026, by the chair. **After seeing results:** frozen after the bridge and curvature outcomes were read (Jason's rule: what can be tested tonight is tested tonight). A pass is a lead needing confirmation on unused songs, never a finding. No cover count, version, release, `first_year` or versions file was opened. "Chair" = a notes-only check on the 2,672 songs with ≥ 3 chords.

## Claim (I1, revised difference form, after Ollivier's κ = 1 − W1/d)
At each chord change, compare how far the tune's pitch classes move with how far the chord tones move. A tune that moves less than its harmony keeps fitting when the chords are swapped. **Extrapolation (the Inventor):** such songs are easier to re-harmonise, so within an artist they are covered more.

## Rows, chord sequence and model
Exactly as `experiments/bridge/PREDICTION.md`: the same rows, chord token, merging, wrap rule, data-pack measures weighted by `n_mel`, the `within()` model, CR1 clustered SE, md5 artist halves. Songs with no usable change are dropped (chair: 3) before the rule of two or more songs per artist.

## Measure
Per clip:
- **Chord events** are the `harmony` entries sorted by onset, each with its own [onset, offset) in beats. Consecutive events with equal token merge into one **run**; a run keeps the list of its events' intervals.
- **Chord tones of a run:** the absolute pitch-class set of its first event, {root} ∪ {(root + cumulative sums of `root_position_intervals`) mod 12}; uniform weights over the set.
- **Melody over a run:** for every `melody` note [onset, offset) and every event interval of the run, add the overlap length (if > 0) to that note's `pitch_class` mod 12. Melody pitch classes are absolute, like chord roots (chair: 70.5% of melody duration lands on chord tones read so, 31% if read tonic-relative).
- **Changes:** run i → run i+1 for consecutive runs, plus the wrap last → first when their tokens differ (the same moves as M). **Skip a change if either run has zero melody duration** (chair: 81% of changes kept).
- **W1 on the 12-pitch-class circle** with ground distance min(|i−j|, 12−|i−j|) semitones, computed exactly as Σ_k |F_k − median(F)|, F = cumulative sum over k = 0…11 of (a − b) (check: one note C to F♯ = 6; C major to G major = 1).
- **Per change:** δ = W1(melody over x, normalised; melody over y, normalised) − W1(chord tones x; chord tones y).
- **Song value MT** = the plain mean of δ over every kept change in all the song's clips (each occurrence counts once). Semitones. More negative = the tune moves less than the harmony.
- *Chair:* median +0.88 (10th to 90th 0.18 to 1.55).

## Gate (before any outcome; failing either records "stopped", no outcome joined)
MT is size-free by construction (R² 0.02 on the size block; chair), so the gate reads MT itself.
1. **Clip-to-clip:** for songs with 2+ clips, MT of clip 1 alone against clip 2 alone (surprise-file order, both defined); Spearman **≥ 0.20**. *Chair: 0.195 (1,277 pairs).*
2. **Overlap:** |Spearman ρ| with each of the 17 data-pack measures, distinct chords, links and clips **≤ 0.7**. *Chair: largest 0.175 (`length_variety`); `mel_ic_mean` +0.17, `mel_rep` −0.17.*

Chair's verdict on the gate: **fails clip-to-clip, narrowly (0.195 < 0.20); the chair expects this test to be recorded "stopped"**, with no outcome joined. No rounding. The definitions were written before the gate was computed and are not to be adjusted to pass it.

## Model columns
MT, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, the nine distinct-chord dummies.

## Prediction
**β = −0.03 SD of log(1 + covers) per SD of MT**, within artist (the Inventor's +0.03 for κ_mel; the difference form reverses the sign): more negative MT, more covers.

## Power
Printed before β: power = Φ(0.03/SE − 2.638) + Φ(−0.03/SE − 2.638). Chair: SE ≈ 0.0155, **power ≈ 0.24**, ignoring attenuation from 0.19 clip agreement.

## Rules
Tonight counts six tests, so each needs **p < .05/6 = .0083, two-sided**.
- **Pass:** β < 0, p < .0083, and β < 0 in both artist halves.
- **Kill:** β > −0.01.
- **Unsettled:** anything else, including a split between halves.
- **Opposite sign** (β > 0, p < .0083): a new hypothesis, not a pass.

## Reported, deciding nothing
Covers within 5 years and more than 10 years after `first_year`, as in the bridge experiment; β without `ch_ic_mean`; the two parts (mean melody W1, mean chord W1) entered separately in place of MT; share of changes skipped.

## What it cannot say
- **Weak measure:** two clips of one song agree at about 0.19; tune measures have failed five runs.
- **After seeing results:** a pass is a lead for unused songs only.
- **Pitch class only:** octave, contour and rhythm of the tune are ignored; a long note held across a change counts on both sides.
- **No cause; hits only; McGill untouched.**
