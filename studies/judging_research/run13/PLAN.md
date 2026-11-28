# Run 13: a supplemental trial of the new system (28 November 2026, about 12:30 ET)

Jason's word (28 Nov, live): the research has been emulative, not novel; "consider ways to improve... lead us to novel, not emulative, solutions". Answer agreed with him: (1) let the data propose the formula, with a sealed half; (2) compare great songs with the engine's own builds; (3) predict numbers, not directions; (4) a song as a peak; (5) passes that start from the notes, not from papers. He said "Yes. And go ahead and do a supplemental trial of the new system now. And remember to check the world music branch."

This trial runs (2) and (1), with (3)'s numeric predictions taken from the world-music branch (origin/world-music, reports/world_music/SUMMARY.md at 9a96330: rhythm repeats more than pitch, about 71% against 51% across 113 collections; a folk phrase spans about 9 semitones; heavy leaning on one pitch goes with chant, the engine's 0.39-0.42 against folk's 0.28). No paper is read for this trial.

One feature grammar (`experiments/features13.py`, about 60 notes-only features of a section's first 8 bars) serves all three tests. Engine builds come from the committed metre engine run read-only on the specs of eight spent or seen 4/4 songs (50, 54, 55, 58, 60, 61, 62, 66; never 49, 59 or any sealed song): `/home/claude/dl/run13/engine_builds.py`, 1,500 builds each, survivors kept. The engine is not changed.

Tests (K = 4 counted outcome tests, α = .05/4 = .0125): realness_covers (1) and formula_search's three confirmations (3). gap_engine reads no outcome (its checks are numeric predictions about notes).
