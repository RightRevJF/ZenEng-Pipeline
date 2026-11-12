# Song 45: Before It's Done (written on the v116 port; findings 375-379)

Words and music: Jason Bryant. A fingerpicked ballad, q = 72, 4/4; G major, the last chorus and the tag lifted a whole step to A in the record;
a man's middle voice (search row B2-D4; sung D3-E4); 56 bars, 3:07. Steel-string guitar (standard tuning, no capo, every note on its string and
fret) and a cello from verse 2. From the writer's book "You Will Wake" (read and used, not stored here); intake Q0-Q15 in intake.py.

    python3 gen_p45.py                 # melody_p45.py: song 45's constants and designs (Q14 A, Q15 A) on songs/p47/melody_v116_p40.py (376 patched)
    bash run45.sh                      # 1000 main + 1000 control, each twice (seed 20261555)
                                       # main 476 survivors, order d2ec0ab81d82; control 546, order 37097d8bd9f3
    reads_p45.txt                      # 309: every file the search reads (all committed)
    python3 diag_design_p45.py 1000 main _diag   # 377: the design gate's parts counted (diag/diag_design.txt; same order)
    python3 pick_p45.py                # 362: the judge's first with no soft break, 10c3fce99da2 -> melody_final.pkl
    python3 edit_p45.py                # Q16 A: the writer's hand edits (verse 2 line 1; chorus line 2 and its returns), evaluated again
    python3 build_p45.py               # the record: voice (lifted), guitar (strings and frets), cello
    python3 clash_p45.py               # 379: sung notes against a semitone in what is sounding
    python3 demo_p45.py; python3 engrave_p45.py; python3 nashville_p45.py
                                       # demo; lead sheet, voice-and-guitar score (notation + TAB), parts; number chart
    python3 consistency_p45.py         # 48/48
    songbook.md, test_report_p45.md    # findings 375-379 (also on the fix list after v116)
