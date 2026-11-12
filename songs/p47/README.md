# v116: songs 40, 42 and 43 again (fixes 355–364 ported, 359 not; findings from 365)

Words and music of all three songs: Jason Bryant. Same lyrics, intakes and seeds as their last runs (songs/p46). No new song.
The writer's choice on the port (Q1 A: 359 stays as v115; 364 groups kept windows into songs by adjacent same-year windows) is in log_v116.py.

    python3 gen_v116_p40.py            # melody_v116_p40.py: v116's 355-363 on songs/p46/melody_v115_p40.py
    python3 gen_p42_v116.py            # melody_v116_p42.py (seed 20261552)
    python3 gen_p43_v116.py            # melody_v116_p43.py (seed 20261553)
    bash run_v116.sh                   # each song 1000 main + 1000 control, each twice; all six orders reproduced;
                                       # then 356's diagnostics on song 43: ZE_OFF=348 and ZE_OFF=354
                                       # 40: 701 / 746, 4b1447040f6f / b9d46b6ec95e
                                       # 42: 759 / 796, 80e060723e2c / 1c4ded5ba440
                                       # 43: 798 / 819, a7c8c1fa5f14 / 0d9995e53e79
    ZE_OFF=348 python3 diag_v115_p43.py 1000 main _off348   # 356's diagnostics on v115's code (and ZE_OFF=354)
    python3 readings_v116.py melody_v116_p40 /home/claude/p47/melody_v116_p40 readings_v116_p40 /home/claude/p46/melody_v115_p40 /home/claude/p44/melody_v112_p40
    python3 readings_v116.py melody_v116_p42 /home/claude/p47/melody_v116_p42 readings_v116_p42 /home/claude/p46/melody_v115_p42 /home/claude/p44/melody_v112_p42
    python3 readings_v116.py melody_v116_p43 /home/claude/p47/melody_v116_p43 readings_v116_p43 /home/claude/p46/melody_v115_p43 /home/claude/p45/melody_p43
    python3 sep_v116.py sep_v116.json /home/claude/p47/melody_v116_p40 /home/claude/p47/melody_v116_p42 /home/claude/p47/melody_v116_p43   # 364
    python3 make_report_v116.py        # test_report_v116.md (findings 365-371 appended); fixlist_v116.md
    reads_v116.txt                     # 309: every file the three searches read (all committed)
