"""The writer's choices in the v119 port session (songs/p51). No new song; the songs' own intakes stand (songs p40-p49)."""
LOG = [
    dict(q="Q1", asked="Fixes 386 and 267 conflict, so I've stopped before the step-1 runs. In a 40-build smoke run of song 43, 386 moves "
                       "clashing notes in returning lines. Fix 267 then reads those lines as \"changed early\" and kills the build: 20 of 40 "
                       "builds died, against 3 of 40 with 386 off. How should I port 386?",
         options={"A": "Read 267 before (Recommended): 267 reads a return's pitches before 386's moves; the moves are made and printed.",
                  "B": "Move every occurrence: a note moved in a return is moved in its source and every occurrence of the tune.",
                  "C": "Fresh lines only: 386 moves notes only in fresh and sung-again lines; returning and copied lines keep their clashes, printed."},
         recommended="A", answer="A", answer_text="Read 267 before (Recommended)"),
    dict(q="(instruction)", asked="After v120 arrived, mid-port",
         answer_text="Stop before step 2. Do not port fixes 399 and 401; back them out if they are in. ZenEng v120 withdraws them. Step 2 is now only 388's side runs. "
                     "In step 3 add fix 424. Read tests, costs and separation only on the 30 measures listed in zeneng_v120_second_collection.json, against both kept "
                     "collections pooled (the second is zeneng_v120_bimmuda_windows.json). Your findings keep numbers 402-419; the paper's new fixes are 420-425."),
]
