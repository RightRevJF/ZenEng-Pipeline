"""The writer's choices on the v116 port (Jason Bryant). Every question, its options, the recommendation and the answer."""
LOG = [
    dict(q="Q1", asked="v116: fixes 359 and 364 can't be ported as written. 359 needs to know which 70 of the 314 kept windows are minor, and 364 needs "
                       "the song each kept window comes from (to hold out kept songs). The kept-window table in the repo has only year and section. "
                       "The other eight fixes port fine. How should I go?",
         options={"A": "Run now: port the other eight. 359 stays as v115, with costs read against all 314 and flagged. 364 groups kept songs by adjacent "
                       "same-year windows (my inference, labelled) (Recommended)",
                  "B": "Wait for the lists: get the minor flags and song IDs for the 314 windows from the other AI, then run everything as written",
                  "C": "Run without both: port the other eight only; 359 and 364 left out and flagged on the fix list"},
         recommended="A", answer="A"),
]
