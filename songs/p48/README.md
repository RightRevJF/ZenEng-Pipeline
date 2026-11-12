# Song 44: Keeping Time (written on the v116 port; findings 372-374)

Words and music: Jason Bryant. Mid-tempo dance-pop, q = 112, four on the floor, straight; C minor verses, E-flat major chorus; a mezzo (row G3-D5); 80 bars, 2:51.
From the writer's essay "The Problem of the Other Mind" (read and used, not stored here); intake Q0-Q17 in intake.py.

    python3 gen_p44.py                 # melody_p44.py: song 44's constants and designs (Q16 A, Q17 C) on songs/p47/melody_v116_p40.py
    bash run44.sh                      # 1000 main + 1000 control, each twice (seed 20261554)
                                       # main 614 survivors, order 1a842f54b719; control 675, order 41eff94b050a
    reads_p44.txt                      # 309: every file the search reads (all committed)
    python3 pick_p44.py                # 362: the judge's first with no soft break, e8dc84c25324 -> melody_final.pkl (no hand edits)
    python3 build_p44.py; python3 demo_p44.py; python3 engrave_p44.py; python3 nashville_p44.py
    python3 consistency_p44.py         # 41/41
    songbook.md, test_report_p44.md    # findings 372-374 (also on the fix list after v116)
