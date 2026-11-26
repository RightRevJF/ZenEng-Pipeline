# Fresh songs, test 3: melody range on songs whose outcome has never been seen. Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Idea R05-L2 (status testing: run 05 −0.42 pp per SD, p .11, unsettled). No outcome has been opened by the chair or by any brainstorm agent (see `../fresh_repetition/PREDICTION.md`). Figures marked *chair* come from notes-only checks.

**Shared rules:** `../fresh_repetition/PREDICTION.md` and `../common.py`, unless this file says otherwise.

**Tonight counts six tests. Each needs p < .05/6 = .00833, two-sided (z = 2.638).**

## Claim (run 05, unchanged)
The original artist's voice is fixed; other singers take up songs an ordinary voice fits. Within an artist's own songs, a narrower melody range goes with more uptake by another artist. Only fresh songs with a melody can enter (most fresh clips are chords only).

## Measure L2 (frozen in run05/experiments/melody_range/PREDICTION.md; `common.L2_clip`)
`melody_midi` notes sorted; fewer than 4 notes: no value; fold every written interval larger than an octave back inside it (an interval of exactly 12 is kept); weights = note durations; clip value = the duration-weighted 95th minus 5th percentile of the folded pitches (`searchsorted`, left). Song value: n_mel-weighted mean (`run05 common.song_measure`).

**Unit values** (must reproduce): 0, 4, 7, 12 → 12; 0, 4, 19, 12 → 7; C-major scale 0 … 16 → 16.

## One change from run 05, made on the notes before any outcome: songs above three octaves are dropped
*Chair:* L2 has transcription artefacts. On the 9,588 seen rows the maximum is 1,030 semitones and the SD is 17.5, against a median of 11; one fresh song reaches 1,053. A fake-outcome run on the uncapped measure showed what this does to a sample of about 400 fresh songs: with no true effect, the clustered test came out significant in 14% of draws at p < .00833. The few extreme rows carry the slope, and the sandwich SE does not see it.

So **rows with L2 > 36 semitones are dropped, seen and fresh alike (`common.L2_CAP`, column `L2c`).** A 5th–95th percentile range beyond three octaves is not a range one voice sings. This drops 285 of the 9,588 seen rows (3.0%) and 9 of the 413 fresh battery rows with a melody. With the cap, the fake null comes out significant in 0.5% to 1.5% of draws, close to the nominal 0.8%.

The z scale is the mean and SD of L2 over the seen rows at or under the cap: **mean 11.87, SD 5.45 semitones**. Run 05's per-SD unit was 17.5 semitones, inflated by the artefacts, so tonight's unit is about a third of run 05's. If run 05's −0.42 were a straight-line effect, it would be about −0.13 per tonight's SD. Tonight's prediction keeps the claim's own size, −0.7 per SD, not that conversion.

## Rows
The shared battery rows with L2c: **4,746 rows = 4,342 seen + 404 fresh** (*chair*), fresh rows by 260 artists, 563 artists in all. Fresh clip 1 vs clip 2 agreement 0.396 on 52 pairs (seen 0.290).

## Columns
z_fresh(L2c), z_seen(L2c), z(ch_rep), shared controls. **mel_ic_mean, run 05's extra column, is left out**: it is a corpus-model score and cannot be computed identically for fresh songs (shared rule). has_mel is 1 on every row here, so it drops out.

## Prediction
**β(z_fresh) on y_foreign = −0.7 pp per SD** (narrower, more uptake).

## Rules
- **Pass:** β < 0, two-sided p < .00833, β < 0 in both halves, conditional logit < 0 and converged.
- **Kill:** β ≥ 0.
- **Opposite sign** (β > 0, p < .00833): killed; reported as a new hypothesis ("wide-range showpieces are what others take up").
- **Unsettled:** anything else.

## Power (fake outcomes, `../power_fake.py`)
| | SE (pp) | Pass rate if −0.7 is true | Kill fires if true | Kill fires if 0 | Power at p < .05 |
|---|---|---|---|---|---|
| calibrated | 1.78 | 0.021 | 35% | 52% | 0.07 |
| homogeneous | 2.45 | 0.023 | 40% | 50% | 0.06 |

The weakest test tonight: only 404 fresh songs have a melody.

## Reported, deciding nothing
- **Run 05's exact form, uncapped, on run 05's z scale (SD 17.5)**, with the warning above about its SE.
- The unfolded range in place of L2c; z_seen; β on y; W01-J6a early and late uptake; karaoke/tribute removed; clique-collision drop; the fresh-only within-artist model.

## Order
1. Unit values. 2. Seen reproduction (9,588 with a value; percentiles 7 / 11 / 21); the cap's counts (285 seen, 9 fresh). 3. Run 05's gate on the seen rows (`gate(rows, "L2")`: 0.290, largest overlap mel_ic_mean +0.555; stop if it fails). 4. Notes-side power (bound 2.47 pp). 5. `common.validate_match`. 6. `common.load_battery_outcomes`. 7. Counts. 8. Clustered SE, power. 9. β, halves, logit, verdict. 10. Reported. 11. `result.json`.

## What it cannot say
As the shared file. Also: fresh songs with a melody are a small, odd subset of the fresh songs; Hooktheory's octave field is the transcriber's choice; a clip is one section.
