# rep_entropy_C: confirmation on split C of rep_entropy (which passed on split A)

Run 10, 27 November 2026. Written by the orchestrator under the confirmation rule the chair froze before any outcome (chair.md and every PREDICTION.md of this pass, commit 641f966): a counted test that passes on split A is re-run once on split C with the identical spec except split "C", predicted the same sign and size, at alpha .05 divided by the number of such confirmations (three passed on A: rep_entropy, irr_skel_retrace, core_typical, so alpha = .05/3 = 0.0167), with power computed on C before its outcome is joined. Split C (sha256 first hex digit a to c) has never been joined to any outcome. Split H stays sealed.

- **Measure, model, controls, halves, second model, readings:** exactly as in `../rep_entropy/PREDICTION.md` and `../rep_entropy/spec.json`; only `split` (now "C") and `alpha` differ (`spec.json` here).
- **Tunes:** split C tunes with the measure and extras defined: 4,261.
- **Prediction:** beta = -0.03 SD of z(y_cov) per SD (the frozen size from A's PREDICTION.md, not A's estimate). y_love: same sign, a reading.
- **Rules:** common10.verdict: pass = p < 0.0167, predicted sign, both halves, Poisson sign; killed if -0.03 lies outside the 95% range; otherwise unsettled. Counted only if power >= 0.2 (R06-5).

## Power on C (power.json; fake outcomes on the real C rows, before the outcome)

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.277** | 0.027 | 0.430 | 0.0173 | 4,261 |

**Status: COUNTED.** The confirmation's verdict is the finding for this measure; the A result alone is a lead.
