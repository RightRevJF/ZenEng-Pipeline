# Song 43: Blue Movie (v113 and v114 ported; findings from 348)

Words and music: Jason Bryant. Up-tempo dance-pop, q = 118, four on the floor, straight, A minor, light tenor (row C3-A4), 80 bars.
The lyric is from the writer's sonnet (not stored here); intake Q1-Q18 in intake.py.

    python3 gen_v113_p40.py            # melody_v113_p40.py: v113's 338 on songs/p44/melody_v112_p40.py
    python3 gen_v114_p40.py            # melody_v114_p40.py: v114's 340-347 on it
    python3 gen_p43.py                 # melody_p43.py: song 43's constants, the chorus design (Q15 A) and its gate; the minor key read on C
    bash run43.sh                      # 1000 main + 1000 control, each twice (seed 20261553)
                                       # main 811 survivors, order df5dff409ad9; control 819, order e2d6fa8c04c5
    python3 readings_v114.py melody_p43 /home/claude/p45/melody_p43 readings_p43   # the table of tests of 310-347 (321)
    reads_p43.txt                      # 309: every file the search reads (all committed)
    python3 pick_p43.py                # Q18 A: the judge's first, dc24946f27cb -> melody_final.pkl (no hand edits)
    python3 build_p43.py; python3 demo_p43.py; python3 engrave_p43.py; python3 nashville_p43.py
    python3 consistency_p43.py         # 39/39
    songbook.md, test_report_p43.md, fixlist_v114.md   # findings 348-353
