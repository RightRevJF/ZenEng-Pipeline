# Run 12, round 1: the Listener

28 November 2026. Stance: expectation, surprise, memory, exposure; what makes a musician want to learn a song by ear. **No outcome was opened** (no `load_outcomes`, no covers, FIT, HOLDOUT or `data/*.json` file; `fitness/fit.json` not opened). Notes-side checks only, about 2.5 minutes of compute. Code: `run12/experiments/measures/m_listener.py` (clips), `run12/experiments/measures/lakh_listener_pi.py` (Lakh; writes only `/home/claude/dl/run12/listener_pi_lakh.json`).

## Proposals (about 400 words)

**L12-1 PI3: the past tells the future (physics vector 2; Lakh whole songs).**
- *Mechanism.* Worth learning when the first minute pays for the rest: the hook returns.
- *Mathematics (Bialek, Nemenman & Tishby 2001; prediction is extrapolation).* S(N) ≈ hN + E: h is paid on every note, E is learned once. Subadditivity gives I(past_L; future_L) ≤ H(L) ≤ L·H1, so few pitch classes cap both: REP is a confounded read. Lasting songs should have high E at a given h.
- *Measure.* PI3c = 2H(3) − H(6) on skyline pitch-class events, minus its 10-shuffle mean. *Data:* 5,275 of run 07's Lakh songs (seen; no melody measure joined).
- *Prediction.* **+0.03** SD of y_foreign per SD, within artist, H1 and lnN held. Subsumption: the notes say **no** (within-artist r with H1 −0.29, R² on H1 + lnN 0.06), so H1 keeps at least two thirds of its coefficient with PI3c held.
- *Kill.* +0.03 lies outside β ± 1.96 SE.

**L12-2 PIC: the exposure-trained ear's context gain (vector 2; Hooktheory clips).**
- *Mechanism.* Clips are too short for block entropies; the corpus-trained ear stands in: how much do the last two notes tell about the next?
- *Measure.* Mean log2 p(d_t | d_t−2, d_t−1) − log2 p(d_t); Witten-Bell trigram on scale degrees, song left out. *Data:* 9,544 Hooktheory songs.
- *Prediction.* **+0.03**, ln_notes and pc_entropy held (reading: mel_ic_mean too).
- *Kill.* As L12-1.

**L12-3 Late wins (vector 1; card 1 Thm 2.6, card 2 Prop. 3.1).**
- *Mathematics (extrapolation).* The frozen fit finds no rich-get-richer (A → ∞): card 2's α = 0 case, where with K ≥ 2 popularity order converges almost surely to quality order; card 1's leaders fall only to fitter newcomers. So quality should show more in late covers than early ones.
- *Not FIT vs counts:* they correlate 0.985.
- *Which notes property.* One a coverer judges by ear, surviving re-arrangement: PI3c and H1 are stable between arrangers (0.65, 0.78); MIDI chord repetition agrees with Hooktheory's only 0.32.
- *Measure.* REP, PIC and PI3c. The outcome is z log(1 + covers at age ≥ 15), with covers at age ≤ 5 and first year held, on songs released by 2005.
- *Prediction.* REP **−0.03**, PIC and PI3c **+0.03**. On early covers alone, |β| ≤ 0.02.
- *Kill.* Prediction outside the range; "exposure, not quality" if |β_early| exceeds |β_late| by over 1.96 SE (artist bootstrap).
- *Power.* About 0.1 on ~1,700 Hooktheory songs (SE ~0.03): an estimate, unless frozen `fitness.py` (settings fixed) is applied to Lakh's Discogs groups and pooled.

## Check numbers (notes only)

| Key | Data | Songs | Stability | Largest overlaps | R² | Power (checks11) |
|---|---|---|---|---|---|---|
| **PI3c** | Lakh | 5,275 | **0.646** between two MIDI files (196 songs) | within artist: H1 −0.29, ch_rep −0.11, lnN +0.15 | 0.06 on H1 + lnN | — (Lakh SE about 0.017 in run 11; power about 0.2 at +0.03, α .01, my arithmetic) |
| **PIC** | clips | 9,544 | **0.273** clip 1 vs 2 (4,219) | mel_ic_mean −0.63, leap_share −0.59, step_share +0.41, int_entropy −0.38 | 0.47 on 13 | 0.29 at +0.03, ln_notes and pc_entropy held (fake SE 0.0135) |
| PIC_REL | clips | 9,544 | 0.293 | mel_ic_mean −0.68, leap_share −0.60 | 0.50 | 0.24 |

Power in the last column used 100 draws at α .05/6, without an artist share, so it is understated (run 11's lesson).

For reference, on Lakh: H1 has arrangement stability 0.781 and lnN 0.698.

**Dropped on the notes.** Each was tried in this pass.

| Key | Why dropped | Figures |
|---|---|---|
| PI1C (own-clip adjacent MI, shuffle-corrected) | unstable, and renames mel_rep | stability 0.184; mel_rep +0.66; R² 0.54 |
| Lakh PI2c | renamed by note count | lnN +0.54 within; R² 0.63 |
| Lakh E3c (finite-L excess entropy) | renamed by note count | lnN +0.49; R² 0.43 |
| Lakh PI4c and KEFF (PI4c − PI1c, read as the theorem's (K/2)·log-growth "parameter count") | stable (0.65), but bias-driven | correlation with H1 flips from −0.29 at L = 3 to +0.23 at L = 4 (8-grams saturate at log N) |
| Grid readings PIg4c / PIg8c (eighth grid with holds) | renamed: they carry duration | stability 0.59 / 0.68; PIg8c within-artist +0.33 with H1, −0.30 with ch_rep |

So L = 3 is the one window that is neither renamed nor saturated.

## Exact recipes

**PI3c (Lakh, `lakh_listener_pi.py`)**
1. *Skyline.* At every 12th step (an eighth note), take the highest pitch sounding on tracks 1, 2 and 4. Trim to the span from the first sounding step to the last.
2. *Events.* Drop rests and merge consecutive equal pitches. Map each event to pitch class mod 12. Block entropies are invariant to relabelling, so no key is needed.
3. *Block entropy.* H(L) is the plug-in entropy, in bits, of the overlapping L-blocks.
4. *PI3c.* Compute 2H(3) − H(6), then subtract the mean of the same quantity over 10 permutations of the events. The RNG seed is int(md5[:8], 16).
5. *Bounds.* A file needs at least 128 events. The song value is the mean over its files.
6. *Fixed choices, none fitted.* Skyline tracks, eighth grid, L = 3, 10 shuffles.

**PIC (clips, `m_listener.py`)**
1. *Sequence.* Scale degree (pitch − tonic) mod 12, repeat-free.
2. *Corpus.* Counts from every raw clip with a melody, minus all clips of the scored song.
3. *Model.* Unigram with add-one smoothing. Bigram and trigram use Witten-Bell interpolation: p = (c(h,x) + T(h)·p_lower)/(c(h) + T(h)).
4. *Score.* Mean over t ≥ 3. PIC_REL = PIC divided by the mean unigram surprisal.
5. *Song value.* As `C.song_values`.

**Commands run**
- `python3 lakh_listener_pi.py` (39 s)
- `cd run11/experiments && python3 checks11.py ../../run12/experiments/measures/m_listener.py 0.03 ln_notes,pc_entropy` (48 s, run twice)

## Against my own sign (labelled)
High PI3c is also the signature of copy-pasted choruses in a MIDI file. Arrangement stability of 0.65 says it is mostly the song's property, but not wholly. If covers reward "room to move", the sign could be negative. +0.03 is written down so that it can be killed.
