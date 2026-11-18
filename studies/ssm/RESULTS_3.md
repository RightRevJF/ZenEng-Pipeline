# Scaling (DFA) and compression: results (18 November 2026)

Predictions: PREDICTION_3.md (committed 7da7db8 before measuring). Code: scaling_compression.py (scaling_compression.json). Melody alone.
Melodies are near 1/f in pitch in every set (DFA alpha medians 0.90, 0.91, 0.91) and near white in rhythm (about 0.50).

| Prediction | Result | Held? |
|---|---|---|
| S1 Rolling Stone closer to 1/f than Billboard | pitch AUC 0.464 (p 0.22); rhythm 0.496 | no |
| S2 inside Billboard, closeness to 1/f against peak or weeks past 0.15 | pitch: peak 0.183 (p 0.007), weeks 0.161 (p 0.018); 0.183 holding the number of notes. Rhythm 0.07 | yes, pitch |
| S3 inside BiMMuDa (top five only), against year-end position | 0.021 (p 0.72) | no |
| K1 a compression sweet spot in Billboard | thirds' median peaks 5.5, 9, 10 (the most compressible third best); square term p 0.85 | no |
| K2 Rolling Stone more compressible | AUC 0.432 (p 0.019): less compressible, against the prediction; compression tracks melody length (-0.68) | no |
| K3 a sweet spot in BiMMuDa | square term p 0.43 | no |

Not predicted (after the fact, so a pointer only): BiMMuDa's top-five hits sit closer to 1/f in pitch than the Billboard songs that peaked below no. 20
(AUC 0.573, p 0.074), as do Billboard songs that peaked in the top ten (0.601, p 0.026).

Reading: in the Billboard sample two independent readings each relate to peak at about 0.18: nesting (RESULTS.md) and closeness to 1/f in pitch
(here). They do not correlate with each other (-0.03), and each keeps its size with the other held. Neither is confirmed on held-out songs; the
held-out set has only top-five hits, so its range is narrow. The fair test is a held-out sample that includes songs that charted low.
