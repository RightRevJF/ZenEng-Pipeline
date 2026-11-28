# pi3c_lakh: predictive information of the melody skyline on whole Lakh songs (vector 2)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. I did not read `data/lakh_songs_discogs_run07.json`, did not call `common12.load_lakh`, and ran only a dry run on a synthetic outcome. Idea: **R12-L1 PI3 (Listener), with R12-G2 PRED (Geometer) as a reading (the Skeptic's Merge 2)**. **Status: COUNTED** (rank 2 of 3). K = 3, α = .05/3 = 0.0167.

## The measure (frozen; `build_lakh12.py` → `/home/claude/dl/run12/lakh_measures12.json`)
**PI3c**, the Listener's exact recipe (it reproduces `listener_pi_lakh.json` to the printed digit):
1. **Skyline.** At every eighth note (every 12th step of LPD-5 cleansed), take the highest pitch sounding on tracks 1, 2 and 4. Trim to the span from the first sounding eighth to the last.
2. **Events.** Drop rests, merge consecutive equal pitches, and map each event to its pitch class.
3. **PI3c.** Compute 2H(3) − H(6), the plug-in block entropies in bits, and subtract the mean of the same quantity over 10 permutations. The permutations are seeded with int(md5[:8], 16).
4. **Bounds.** A file needs at least 128 events.

**Near-duplicates are counted once.** Within a song, a file whose tracks-1-2-4 pitch-class profile has a min-over-rotations JSD below 1e-4 against an earlier kept file is dropped; 81 files were dropped this way. The song value is the mean over the kept files.

**Gate** (`measure_gates12.json`; written before outcomes):
- Two-file stability on non-duplicate pairs is **0.471** (135 pairs; the bar is 0.20).
- The largest |Spearman| with an existing measure is cv_w −0.17; with H1 it is under 0.17. The bar is 0.70.
- **Passes.**

## Songs
Run 07's within-artist Lakh songs (`lakh_notes_side.json`) with PI3c, H1, REPBAR and every control finite, restricted to artists with 2+ such songs: **5,093 songs, 1,481 artists**. **SEEN:** these songs were joined to y_foreign with eight chord measures in run 07 and with the melody-bass coupling in run 11. No melody or information measure has ever been joined to them.

## Outcome
**y_foreign** (run 07's rule): 100 if the song's Discogs-VI group holds a performer set that shares no name with the original artist, else 0. Rows where it is nan are dropped.

## Model and controls (`harness12.py`, kind `lakh`)
- OLS of z(y_foreign) on z(PI3c), with **artist fixed effects**.
- Run 07's controls: z(ln_chg), z(V), z(ln_bars) and five-year year bins.
- The Skeptic's Lakh controls: z(LNEV) (ln events), z(NPB) (distinct pitches per beat, tracks 1-4), z(ACT) (non-empty tracks) and z(NFILES) (MIDI files listed; a fame proxy).
- Frozen extras, as the Listener accepted in round 2: **z(H1)** (event pitch-class entropy) and **z(REPBAR)** (the share of non-empty 8-eighth skyline bars equal to an earlier bar).
- CR1 SEs by artist.
- **Second model:** a conditional logit (artist groups) of the binary y on the same columns, used for the sign only.
- **Halves:** md5(artist key) mod 2.

## Prediction
**β = +0.03 SD of z(y_foreign) per SD of PI3c**, within artist, with H1, ln events and the other controls held. Sign +: when the past of a melody tells more about its future, other artists take it up more.

## Verdict rules
- **Pass:** p < 0.0167, β > 0, both halves > 0, and the conditional logit > 0.
- **Killed:** +0.03 lies outside β̂ ± 1.96 SE (R07-3).
- **Unsettled:** otherwise.

## Power (power.json; fake outcomes on the real rows; within-artist share 0.46 of Lakh y_foreign from `outcome_side_shares.json`; 300 draws, seed 12)

| α | power | kill if true | kill if zero | median fake SE | n | artists |
|---|---|---|---|---|---|---|
| 0.0167 | **0.243** | 0.027 | 0.457 | 0.0168 | 5,093 | 1,481 |

## Readings (uncounted; frozen in spec.json)
1. **Subsumption** (the Listener's rule). Fit H1's β (controls plus REPBAR) without PI3c and then with it. The shrink is 1 − β_with/β_without. The Listener said H1 keeps at least two thirds (shrink ≤ 1/3). The reading counts only if H1 alone has p < .05 (the Skeptic's rule).
2. **G2 PRED** (Geometer). PI8 is the Gaussian predictive information of the held skyline: K = 32, Levinson-Durbin, with the bias 32·33/(4n) removed. It is fitted with REP_L, H8 (log innovation variance), EVLEN (mean event length) and REPBAR held. Predicted sign +.
3. **G2 subsumption.** REP_L's β with and without PI8, holding H8, EVLEN and REPBAR. The Geometer said the shrink is under 10%, and a shrink of 25% or more kills "mostly not". It counts only if REP_L alone has p < .05.

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run pi3c_lakh`

Credit: Lakh MIDI / LPD, CC BY 4.0; Discogs-VI 20240701, CC BY-SA 4.0.
