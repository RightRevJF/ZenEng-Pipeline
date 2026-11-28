# Judging research, run 13: a supplemental trial of the new system

28 November 2026, about 12:00 to 12:30 ET, at Jason's word ("go ahead and do a supplemental trial of the new system now"). No paper was read. Rules came first for every outcome test: 6821d6b (plan and predictions), 98f80b8 (the formulas the search chose, frozen before the sealed half was read), 815f284 (the realness test's code, before its join).

## In three sentences
For the first time the research let the data propose the mathematics: a search over about 4,000 formulas on half the songs, checked once on the sealed other half, and a model that compares real hit melodies with our engine's own melodies. Both routes, separately, pointed at the same thing: real songs bring their rhythm figures back, and the engine does not. On the sealed half that lean held its direction at about 60% of the size but did not clear the bar; and a song that merely sounds more like a typical hit is not covered more (that test was killed, the other way).

## The tests

| Test | Prediction (first) | Result | Verdict |
|---|---|---|---|
| gap_engine: tell real songs from engine builds by notes | AUC ≥ 0.90; four numeric checks | AUC 0.969; 4 of 5 checks true | (no outcome) |
| realness_covers: least engine-like goes with covers | +0.02 | −0.023 (SE 0.011) | Killed |
| formula_search 1: rhythm repetition minus steps | +0.027 | +0.017 (SE 0.014, p .21) | Unsettled |
| formula_search 2: downbeat minus rhythm repetition | −0.026 | −0.001 | Estimate |
| formula_search 3: phrase range minus rhythm repetition | −0.023 | −0.007 | Estimate |

Each folder's RESULT.md has the details.

## What the engine's melodies lack (gap_engine)
Real songs reuse a few rhythms and move the pitch over long, wide phrases that echo bar to bar; the engine varies its rhythms, stops often, and sits on one pitch, repeating notes. Real against engine (median): repeated notes 0.18 against 0.39 of steps; commonest pitch 0.34 against 0.46 of the time; rhythm figures heard before 0.54 against 0.36; phrase range 9 against 5.7 semitones; notes a phrase 18 against 9; distinct note lengths 4 against 6; pitch echo one bar later +0.08 against −0.10. The engine's actual picks sit between, nearer the engine.

## The world-music branch
Its cross-cultural counts gave this trial's numeric predictions. Two held on pop: a phrase spans about 9 semitones (exactly 9 here), and rhythms repeat more than pitches (bar rhythms 0.40 against bar intervals 0.29). The engine's leaning on one pitch (its finding 10) shows plainly (0.46 against 0.34).

## What changes from here
The scheduled passes are rewritten around the new system (see the task's prompt): discovery by search with a sealed half; the engine-against-real comparison every pass; numeric predictions; the song as a peak; papers only every third pass.

## For the maintainer (proposed, rule first, nothing in the engine)
- **R13-1. The gap list as readings.** Read the kept songs' own figures for repeated notes, commonest pitch share, rhythm figures again, phrase range and notes a phrase (features13.py), then the engine's builds against them; report builds outside the kept 10th to 90th. No gate until a reading is agreed.
- **R13-2. Rhythm figures again: a lead.** The one variable that is both "real" and leaned toward uptake on a sealed half. It bears on 749.259 (a section remembers its bars) and the world-music branch's finding 6 (mixing the section's own rhythms with the table, about 2 to 1). A reading, not a gate.
- **R11-3 carried:** unseen named melodies, to confirm R13-2.

Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0); Lakh/LPD not used; the world-music branch (origin/world-music, 9a96330).
