# 749.239, the first grammar (place and step): the held-out check. MISSED on both tables. The grammar is not used; the equation changes.

27 November 2026, 19:08 ET. Rule: PREDICTION_239_grammar.md (commit 0b696ab, before any code). Code: grammar.py (a study file; no engine code). Figures printed from grammar_fit_essen68.json and grammar_fit_pop34.json by the command that wrote this file.

One departure from the rule's letter, said plainly: the likelihood was climbed by L-BFGS, not plain gradient ascent. The likelihood is the same exact one and has one top, so the weights are the same; the stopping tolerance was the routine's (gradient under 0.00001), not "largest change under 0.0001".

## Essen 6/8
- Songs 907: fitted on 454, checked on 453. Windows fitted 5040; the fit converged (144 steps).
- Fitted level weights (finer places are the reference, 0): {"first beat": 3.4273, "beat": 3.2656, "division": 2.9837}; slopes for each note a bar more: {"first beat": 0.7195, "beat": 0.2646, "division": -0.0709}. Step weights are in grammar_fit_essen68.json.
- **(a)** inside the counted middle half in 11 of 12 cells: met.
- **(b)** counted windows carry 0.60 of the generated chance in 0 of 12 cells (lowest 0.035, highest 0.269): **missed**.
- **(c)** three of the top five shared in 0 of 12 cells: **missed**.
- One-bar rhythms, reported: (a) 8 of 8; (b) 7 of 8; (c) 3 of 8.

## Hooktheory pop 3/4
- Songs 267: fitted on 129, checked on 138. Windows fitted 2519; the fit converged (215 steps).
- Fitted level weights (finer places are the reference, 0): {"first beat": 5.5338, "beat": 2.9154, "division": 1.0557}; slopes for each note a bar more: {"first beat": -0.4196, "beat": -0.0849, "division": 0.1629}. Step weights are in grammar_fit_pop34.json.
- **(a)** inside the counted middle half in 9 of 11 cells: **missed**.
- **(b)** counted windows carry 0.60 of the generated chance in 3 of 11 cells (lowest 0.111, highest 0.765): **missed**.
- **(c)** three of the top five shared in 3 of 11 cells: **missed**.
- One-bar rhythms, reported: (a) 6 of 6; (b) 5 of 6; (c) 5 of 6.

## What the miss says
- The grammar gets the *averages* right: where onsets fall by level, cell by cell, in Essen. That is (a).
- It does not know which rhythms are the real ones. In Essen the windows people actually sang carry between a thirtieth and a quarter of its chance; the rest goes to rhythms nobody sang. A product of place and step is too loose a language: it knows letters, not words.
- **The one-bar reading is the lead.** For single bars the same weights put 0.60 of the chance on counted rhythms in 7 of 8 cells (Essen) and 5 of 6 (pop). The looseness is in how two bars are joined, not in the bar.
- I expected (b) to miss and gave Essen one chance in three overall. It missed by more than I thought.

## The next equation (its own rule file, before any code)
**Bars are the words; a window is two words.** The chance of a two-bar window is the counted share of its first bar's rhythm, times the chance of the second bar given the first: a fitted chance that the second bar repeats the first, and otherwise the counted share of the second bar's rhythm, with a fitted weight on how the two bars' note counts sit together. Bars never counted are supplied by this first grammar's one-bar form, which carries the chance well bar by bar but ranks the commonest bars poorly in Essen ((c) in 3 of 8), so its use for uncounted bars is checked too, not assumed. That extrapolates from what is known (bars, and how bars pair) to what is not (windows of a count never seen whole), and it is checked by the same (a), (b), (c).
