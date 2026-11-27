# late_momentum08: late_window08 with recent momentum held. AFTER SEEING RESULTS (late_window08's result was seen)

Run 09, 27 November 2026, written by the orchestrator after `late_window08` gave +0.051 (SE 0.012). Seen songs; a lead, never in K (K stays 1). Its question: is late_window08's lead only momentum (tunes being recorded a lot just before the charts were collected)?

**Songs, outcome, model:** exactly as `late_window08/PREDICTION.md` (8,565 run 08 songs; y_new = standardised log(1 + artist sets first dated 2023 or 2024); OLS HC1; halves by composer; Poisson on n_new), with ONE added column: z(log(1 + n_recent)), n_recent = artist sets first dated 2018 to 2022, beside z(log(1 + n_prior)) (2022 or earlier, as before).

**Prediction:** +0.03 SD per SD of IIV (unchanged; recent momentum is expected to take some of +0.051, not all).

**Rules (a lead):** supported if p < .05, β > 0, both halves > 0, Poisson > 0; not supported if +0.03 lies outside β ± 1.96 SE; otherwise unsettled. Also reported, deciding nothing: the coefficient of the recent-momentum column, and the non-jazz reading.

**Power:** as late_window08 (0.68 without the outcome-built columns; lower in truth).
