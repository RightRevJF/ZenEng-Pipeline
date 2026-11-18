# Songs as pictures of themselves: results (18 November 2026)

Predictions: PREDICTION.md (committed 8f2d35c before measuring). Data: CoCoPops, 194 Rolling Stone 500 songs and 214 Billboard sample songs with
melody and chords; Luthier's songs 54, 55, 58. Code: ssm_lib.py, measure.py (measure.json), replicate_mcgill.py (replicate_mcgill.json).

| Prediction | Result | Held? |
|---|---|---|
| P1 architecture, Rolling Stone over Billboard | AUC 0.487 (p 0.66) | no |
| P2 centre | AUC 0.508 (p 0.78) | no |
| P3 frame | AUC 0.589 (p 0.002); but the same song in the two encodings reads alike only at rho 0.41 | yes, weakly trusted |
| P4 nesting | AUC 0.485 (p 0.58) | no |
| P5 Luthier under the 10th on architecture, over the 90th on weave | architecture at the 78th, 47th, 31st; weave at the 15th, 4th, 68th | no: the eye's "fabric" was wrong |
| P6 nothing past 0.15 against peak or weeks | nesting against Billboard peak 0.183 (p 0.007), weeks 0.170 (p 0.013); 0.203 (p 0.003) holding bars and sameness. Songs with nesting 5 peak at a median of 3; nesting 0-2 at 10 to 19 | no, and in the direction of "the same order at every scale" |

Not predicted: Rolling Stone songs repeat more overall (sameness AUC 0.65, p < 0.001; the two encodings agree at 0.92). Inside the Rolling Stone set,
higher-ranked songs show less architecture (-0.214, p 0.003).

Held-out check of nesting, chords alone (McGill songs not in CoCoPops, 525): 0.082 (p 0.061), the same direction, weaker. On the 214 CoCoPops songs,
chords alone give 0.04 where melody and chords give 0.18: if the signal is real, it lives in the melody.

Encoding check (12 songs in both sets): sameness, weave, nesting and architecture agree at rho 0.90 to 0.94; frame at 0.41.

Reading: 35 tests were run, so one at p 0.007 is a lead, not a finding. It is the first reading today that points where the writer's idea points.
The next test is nesting on melodies held out from this sample, with a finer measure, predicted first.
