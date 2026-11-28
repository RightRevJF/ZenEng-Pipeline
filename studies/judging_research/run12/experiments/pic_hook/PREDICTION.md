# pic_hook: the exposure-trained ear's context gain on Hooktheory clips (vector 2)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. No outcome was opened, and only a dry run on a synthetic outcome was made. Idea: **R12-L2 PIC (Listener)**. **Status: COUNTED** (rank 3 of 3). K = 3, α = .05/3 = 0.0167.

**Why it is counted although the Listener withdrew it.** The Listener withdrew PIC in round 2 for one reason: its power, computed from fake outcomes **without** the within-artist share, was 0.18. That is the error run 11 named. On the real rows with the share, its power at .05/3 is 0.587; with no share it is 0.173. It passes the gate, and the Skeptic's held set (step_share, mel_ic_mean) is frozen. The power rule (R06-5, run 08's K rule) therefore counts it. Jason may overrule this.

## The measure (frozen; `measures/m_listener.py`, key `PIC`; cache `/home/claude/dl/run12/hook_measures12.json` built by `build_hook12.py`)
For each clip:
1. Convert the melody (common11.melody) to scale degrees, (pitch − tonic) mod 12, with consecutive equal pitches merged.
2. **PIC** = the mean over notes t ≥ 3 of log2 p(d_t | d_{t−2}, d_{t−1}) − log2 p(d_t).
3. p is a Witten-Bell interpolated trigram → bigram → unigram (add-one) model, trained on every Hooktheory clip with a melody, minus all clips of the scored song (leave-one-song-out).

The song value is the n_mel-weighted mean over clips.

**Gate** (`measure_gates12.json`): clip-1 vs clip-2 stability **0.273** (4,219 pairs; bar 0.20). Largest overlap mel_ic_mean −0.627 (bar 0.70). **Passes.**

## Songs
Run 04's within-artist rows with PIC and every extra finite: **9,544 songs, 1,741 artists**. **SEEN** (re-spent): their outcome has been joined to chord measures and to run 11's melody measures, but never to PIC.

## Outcome
**y_foreign**, run 04's rule 4410a0e via `C5.load_outcomes`.

## Model and controls (`harness12.py`, kind `hook`)
- OLS of z(y_foreign) on z(PIC), with artist fixed effects and run 04's controls.
- Frozen extras: **z(step_share), z(mel_ic_mean)** (the Skeptic's) and **z(ln_notes), z(pc_entropy)** (the Listener's).
- CR1 SEs by artist.
- Conditional logit for the sign.
- Halves: md5(artist) mod 2.

## Prediction
**β = +0.03.** A melody whose last two notes tell an exposure-trained ear more about the next one is taken up more by other artists.

## Verdict rules
- **Pass:** p < 0.0167, β > 0, both halves > 0, and the conditional logit > 0.
- **Killed:** +0.03 lies outside β̂ ± 1.96 SE.
- **Unsettled:** otherwise.

## Power (power.json; 300 draws, seed 12)
Fake y has a within-artist share of 0.38. That is y's share in `outcome_side_shares.json`, the only Hooktheory extensive-margin share given. It agrees with run 11's realised REP SE of 0.011 against its no-share fake SE of 0.0151.

| α | power (share 0.38) | power (no share) | kill if true | kill if zero | median fake SE |
|---|---|---|---|---|---|
| 0.0167 | **0.587** | 0.173 | 0.030 | 0.810 | 0.0113 |

## Readings (uncounted)
- PIC_REL (PIC divided by the mean unigram surprisal), with the same extras; predicted sign +.
- PIC in its round-1 form (only ln_notes and pc_entropy held); predicted sign +.

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run pic_hook`

Credit: Hooktheory via Sheet Sage, CC BY-NC-SA 3.0; Discogs-VI 20240701, CC BY-SA 4.0.
