# A ceiling on the commonest pitch's share (749.134): result

**Passes; built as fix 956.** (Trial: `trial_neighbour_before_956.json`, block `749.134`, the thousand builds a song of Window 200 before the ceiling.)

| | Song 55 | Song 54 | Song 58 |
|---|---|---|---|
| Pool, without the ceiling; under it | 47; 39 | 33; 26 | 72; 39 |
| Living builds under the ceiling, in 100 | 70 | 76 | 38 |

1. **Every song keeps a pool of 10:** 39, 26, 39. Met.
2. **The pool standard:** a random pick from the ceilinged pools fails the rule 2.6 times in 100 (2.4 without); the neighbour choice 2.1 (1.3). Met.
3. **The chosen tunes sound:** yes. Met.
4. **Words' fit:** songs 55 and 54 keep their tunes in the trial; song 58's tune was over the ceiling (0.497 in verse and chorus) and its new one fits at 0.307 (0.361). Met, by the exception written first.

**Against what I expected:** I thought song 58's pool might fall under 10. It keeps 39.

**Built, and one thing changed in the building.** The trial told a part by the engine's own kind, where a tag counts as a chorus. The kept table tells a part by its name, and a tag is not a chorus there. The engine now reads as the table does (`make_kept_commonest_pitch.kind`). By that reading song 55's old tune was over in the chorus (0.476 against 0.474), so song 55's tune changes too: range 17, words' fit 0.278 (0.341).

In the engine (1,000 builds a song): pools 38, 24, 39 (as `neighbour.py` counts); a random pool pick fails the rule 2.1 times in 100 (0.1 to 5.5), the neighbour choice 2.5 (0.0 to 4.5). No chosen tune of the five is over the kept 90th in either part (`studies/commonest_pitch/result.json`, read again).
