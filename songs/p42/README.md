# ZenEng v110: the port (fixes 310-321), tested on song 40, before song 42

    python3 gen_v110_p40.py                                  # writes melody_v110_p40.py from songs/p41/melody_v109_p40.py
    bash run_port.sh                                         # song 40: 1000 main + 1000 control, each twice (seed 20261511)
                                                             # main 505 survivors, order 3c9c4f2da558; control 537, order 30ba2486b5e4
    python3 readings_v110.py melody_v110_p40 /home/claude/p42/melody_v110_p40 readings_v110_p40 /home/claude/p41/melody_v109_p40
                                                             # 321: the table of tests of 310-321 -> readings_v110_p40_table.json
    reads_v110_p40.txt                                       # 309: every file the search reads (all committed)

# Song 42: Nothing Important (v110, default path, straight feel)

Words and music: Jason Bryant. A piano ballad, straight eighths, q = 76, B-flat major, alto (row F3-D5), 68 bars.

    intake.py                                                # every intake choice (Q1-Q15), the never-say list, the designs
    lyric_draft1.md, lyric_draft2.md, lyric_locked.md        # the drafts and the locked lyric; lyric_p42.py holds it for the engine
    python3 gen_p42.py                                       # writes melody_p42.py from melody_v110_p40.py (song 42's key, form, plans, design gate)
    bash run42.sh                                            # 1000 main + 1000 control, each twice (seed 20261552)
                                                             # main 567 survivors, order 5614d9557a76; control 595, order 46d4320fd85a
    python3 readings_v110.py melody_p42 /home/claude/p42/melody_p42 readings_p42
                                                             # 321: the table of tests of 310-321 on song 42's own runs
    reads_p42.txt                                            # 309: every file the search reads (all committed)
    python3 pick_p42.py                                      # 255's pick 389da0041c48 -> melody_final.pkl (no hand edits)
    python3 riff_p42.py; python3 build_p42.py                # intro figure and cello counter; the record -> song_record.pkl
    python3 demo_p42.py; python3 engrave_p42.py; python3 nashville_p42.py
    python3 consistency_p42.py                               # 39/39
    songbook.md, test_report.md, fixlist_v110.md             # findings 322-328
    python3 q1020_p42.py                                     # 10.20 slots; blind pick B, the middle slot (Q16)
