# Judging research, run 12

28 November 2026, the 10:17 ET pass. Published as the Doc "Judging research, run 12" (https://claude.ai/artifact/WwVjsqH8kJwerpNTJD4Eou); the fix list is the Doc "Proposed fix list: judging research, run 12" (https://claude.ai/artifact/KJhnaoRV2cvLNQv5ZRuiJE). The Doc is the full text; this file carries the same findings for the repository.

## Opening
This pass started Jason's first physics vector, fitness not luck: it built a song's "fitness" from the years of its covers alone (frozen at b0c7824 before any notes were joined), then tested notes measures against it and against plain cover counts. Nothing passed: one counted test was killed (predictive information on whole songs), two were unsettled (pitch-class entropy against fitness rather than counts; a corpus-trained context gain on clips), the rest were estimates. The main thing learned is about the outcome: covers do not breed covers (no rich-get-richer; confirmed with yearly age bins), so fitness is covers per year of opportunity, and the notes explain only a sliver of it.

## The experiments (rules ac5cb9b and 2d64143 before their results; K = 4, α .0125)

| Test | Prediction | Result | Verdict | Power |
|---|---|---|---|---|
| v1_rep: pitch-class entropy, fitness vs counts (Hooktheory) | −0.01 | −0.012 (SE 0.007, p .11) | Unsettled | 0.29 |
| pi3c_lakh: predictive information, whole songs | +0.03 | −0.011 (SE 0.021) | Killed | 0.24 |
| pic_hook: context gain of a trained ear (clips) | +0.03 | +0.015 (SE 0.013, p .23) | Unsettled | 0.59 |
| v1_chrep: chord repetition, fitness vs counts | −0.01 | −0.018 (SE 0.008, p .034) | Estimate | 0.19 |
| rep_lakh: pitch-class entropy, Lakh skyline | −0.02 | −0.022 (SE 0.021) | Estimate | 0.07 |
| fifths_lakh: fifths energy | +0.02 | +0.045 (SE 0.021, p .037) | Estimate (stopped at gate) | 0.07 |
| windows: early vs late covers (Hooktheory) | REP −0.02; ch_rep 0 | REP −0.036; ch_rep −0.24 (analytic SE 0.072) | Estimate | 0.06 |
| windows_lakh_after: ch_rep early vs late, Lakh (after seeing) | −0.12 | +0.006 (SE 0.097) | Estimate (unsettled) | ~0.2 |
| roughx_lakh: roughness of voicings | −0.01 | +0.015 (SE 0.024) | Estimate | 0.01 |
| canal_pilot: what two arrangers keep (notes only) | P1-P4 | three of four held | Pilot | — |
| fitness_finebins_after (cover timing only) | A still → ∞ | holds | not counted | — |

Each folder's RESULT.md has the details. windows_lakh_after ran twice (the first read the YouTube-matched Discogs subset; fixed to the written rule; both reported; NOTE_rerun.md).

## The mathematics
Freeman and Jordan [1]: a newcomer samples a few items weighted by their links and joins the fittest; one item keeps a fixed share only if newcomers compare more than two items on average. Our frozen model: chance of a cover in a year = fitness × (covers so far + A) × age curve × era. On 2,627 songs the best A ran to about two million: no rich-get-richer beyond differences between songs (gamma shape 0.66). Worked example: two 1975 songs with 10 covers each, one early-heavy, one late-heavy; without rich-get-richer they are equally fit.

## The physics
Vector 1: fitness = age-adjusted cover rate; notes against it unsettled (entropy) or estimate (chords). Vector 2: killed on whole songs, unsettled on clips. Vector 3: needs recordings aligned to notes (R12-3). Vector 4: roughness, wrong sign, an estimate; mostly register. Vector 5: pilot on 159 arranger pairs.

## The brainstorm
Nine methods (Geometer: fifths energy, Gaussian predictive information, thinning; Listener: block-entropy predictive information, trained-ear context gain, late wins; Inventor: proportional fitness, roughness, canalization), merged by the Skeptic into five families; all testable ones run. All four agents saw, before any join, that the fitness-vs-counts contest had become arithmetic once A → ∞; all proposed early-vs-late windows. See brainstorm.md.

## First principles
Obstacle: covers behave like one steady appeal per song; the notes explain a sliver; every allowed named song is spent. Way through (speculation): new named melodies; recordings aligned to notes; transcriptions of covers for invariants. See first_principles.md.

## Papers
1. Freeman & Jordan, Extensive condensation in a model of preferential attachment with fitness, arXiv:1812.06946. https://arxiv.org/abs/1812.06946
2. Gaeta, Garetto, Ruffo & Flammini (2022), Reconciling the quality vs popularity dichotomy in online cultural markets, ACM TOIS, arXiv:2204.13536. https://arxiv.org/abs/2204.13536

## Coming passes
Performer's field (data request R12-3); pooled windows (DATA.md); transcriptions of covers; love as an outcome. Paywalled: none.

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Lakh MIDI / LPD (CC BY 4.0); Discogs-VI 20240701 (CC BY-SA 4.0).
