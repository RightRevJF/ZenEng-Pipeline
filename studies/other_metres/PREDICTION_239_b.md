# 749.239, the second equation (bars as words): the model, the bar and what is reported, before any code

27 November 2026, 19:25 ET. The first equation (place and step) missed its held-out check on both tables (RESULT_239_grammar.md). The songwriting session accepted this second one (19:14 ET) with three conditions, all taken below.

## The equation
A bar's rhythm is a word. A window of two bars is two words, A then B:

**P(A, B) = S(A) × T(B given A)**, and a window for a line of n syllables is drawn among the pairs whose onsets sum to n, their chances renormalised.

Every part is a counted share in the fitting half; nothing is set by us:
- **S(A)** = the share of first bars with A's note count, times A's share among bars of that count.
- **T(B given A)** = R × [B is A again] + (1 − R) × M × B's share among bars of its count (A itself left out and the rest renormalised).
  - **R** = the share of windows whose second bar repeats the first, counted for each note count of A.
  - **M** = among windows that do not repeat, the share whose second bar has B's note count, given A's note count. This is how the two counts sit together; the pickup bar followed by a full bar is in it.
- **The vocabulary is the bars as counted,** pickup bars included.
- **Bars never counted:** for each note count, a share U of its chance is held for bars not in the vocabulary, U = the bars of that count seen exactly once over all bars of that count (the Good-Turing reading of what has not been seen). Within U, a bar's chance is the first grammar's one-bar form, renormalised over uncounted bars. That form is checked here too and not assumed.
- **Three and four bars:** a first-order chain, S(A) × T(B given A) × T(C given B) and so on, the same parts.

## The held-out check: the same bar, the same split, both tables
Songs split by the same hash; fitted on one half; cells are the other half's two-bar windows of one count with 20 or more.
- **(a)** in at least 9 cells of 10, the generated share of onsets on a beat and on the first beat each inside the cell's counted middle half (one value: within one onset in n).
- **(b)** in every cell, the held-out half's counted windows carry at least 0.60 of the generated chance. *Settled:* the chance held for uncounted bars is part of the whole, so it counts against (b) unless a held-out window is made of such a bar, where the one-bar form's chance for it is used.
- **(c)** the generated five likeliest windows hold three of the held-out five commonest, in at least 8 cells of 10.
- *Settled for (a) and (c):* read over pairs of vocabulary bars, renormalised; the uncounted share is reported beside them.
- Deciding is on two-bar cells. **A table that passes gets the grammar; one that misses does not; if one passes and the other does not, it is used where it passes.**

## Reported
- (a), (b), (c) on three-bar cells (three bars in a row, 20 or more), the chain form. For (c) there, the search is over the fifteen commonest bars of each count and repeats, said as a limit of the report.
- U for each note count; and the check of the one-bar form on what it is used for: of its chance on uncounted bars of a count, the share carried by bars the held-out half does sing and the fitting half never did.
- R and M as fitted.

## What I expect
- **Essen 6/8:** (a) and (c) pass. (b) is close: I think the counted windows carry 0.5 to 0.7, lower in the thin cells at the edges (counts 3, 4, 13, 14). "Every cell" is a hard word. **One chance in three that Essen passes all three; two in three that it passes in the cells from 5 to 12, which are the ones lines use.**
- **Pop 3/4:** fewer songs, more rhythms. One chance in five.
- If (b) misses only in the thin cells, the next step is a question for the songwriting session about those cells, not a new equation. If it misses in the middle, the equation lacks something real, and the first place to look is the pair itself (a word's chance given the very word before, not just its count).
