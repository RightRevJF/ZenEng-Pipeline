# Why the pools grew sounder (749.137): result

**Range does not explain it. My expectation, and the session's guess, were wrong.** (`neighbour.py`, block `749.137`; `studies/soundness/neighbour_v43_without_the_peak.json` and `studies/pitch_ceiling/trial_neighbour_before_956.json`.)

| A random pick from the engine's pool fails the rule, in 100 | Range in the rule | Range left out |
|---|---|---|
| Without the planted peak (as Window 198) | 6.8 | 6.5 |
| With it | 2.5 | 2.3 |

Neighbour choice: 2.8 and 2.6 without the peak; 1.2 and 0.6 with it. The gap with range left out (4.2) is nearly all of the gap with it in (4.3).

**What the failures are.** In both engines every failure is one thing: all three songs' builds under the kept 10th of rhythm scaling at once (8.1 in 100 without the peak, 2.3 with). Three builds drawn at random are all under the 10th that often when about 43 pool builds in 100 are under it, and about 28 in 100, respectively. Range leans low in 30 pool builds in 100 without the peak and 18 with, and never fails the rule.

**What is not known.** The planted peak changes no rhythm. It changes which builds pass the lift gate and so which reach the pools (pool sizes 53, 43, 71 without; 47, 33, 72 with). So the pools hold fewer builds of very low rhythm scaling either because of which builds the gates now pass, or by chance: the two 90 in 100 ranges overlap (3.7 to 11.4 in Window 198; 0.6 to 5.0 in Window 199). I have not separated the two. The gain should not be counted as a mend of rhythm scaling: 90 pool builds in 100 are still under the kept 25th.
