# A ceiling on the commonest pitch's share (749.134): the rule, written before it is run

**Seen before writing:** `studies/commonest_pitch/RESULT.md`: kept 90th 0.44 (verses), 0.474 (choruses); Luthier's chosen tunes over it in songs 54 and 58 (verse) and 55 and 58 (chorus). Review 27: a wider range did not spread song 58's verse. Pool sizes under v42: 47, 33, 72 (songs 55, 54, 58, as `neighbour.py` counts them).

**The change tried.** A build whose verses, pooled, or choruses, pooled, put more of their sung notes on one pitch than nine kept songs in ten is passed over: taken out of the pool. The choice is then as 954 makes it (the floor, then 872).

**Trial, outside the engine** (`neighbour.py`, the same thousand builds a song).

**The check.**
1. Every song keeps a pool: at least 10 builds in each of songs 55, 54, 58.
2. The pool standard holds: a random pick from the ceilinged pools passes the soundness rule 90 times in 100, and the neighbour choice does.
3. The three chosen tunes pass the soundness rule.
4. No chosen tune's words' fit is more than 0.02 under the tune chosen without the ceiling, unless that tune was over the ceiling.

**What I expect:** song 58's pool is cut hardest (its verses sit at 0.50), perhaps to under 10; if so the ceiling fails check 1 and the fault must be mended in the draw, not at the gate.
