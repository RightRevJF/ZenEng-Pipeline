# Song 40 — Nothing Else on Earth (ZenEng v108)

Words and music: Jason Bryant. Riff-led rock, 4/4 straight eighths at q = 116, D major, mezzo (A3–D5), 110 bars, 3:48.
Lark's song from 'The Garden That Grew by Itself' (Wild Fruit; read and used, not copied here). A debugging song on the default path:
no era, character, summit, bridge register, lift or countermelody chosen; the chorus said twice as a plain repeat. Off the default path,
named: half-time verse drums (Q19, an arrangement design) and the two-bar long lines (Q21, 230's design). No design gate in force.

Tables (not in the repo) go in ./tables: the v108 judges and spectral/registers files plus the earlier ones (see the rerun record's
`tables` hashes). melody_p40.py also reads /home/claude/p36/melody_p36.py and /home/claude/p37/melody_p37.py (songs/p36, songs/p37).

Run, in order (PYTHONHASHSEED=0; seed 20261511, calibration seed 20261512):

    python3 limits286_p40.py                               # 286: six limits on the 515 POP909 pairs -> limits286.json (+ limits286_joint.json)
    for m in main ctl; do                                  # each run made twice; the third argument names the copy
      PYTHONHASHSEED=0 python3 melody_p40.py 1000 $m
      PYTHONHASHSEED=0 python3 melody_p40.py 1000 $m _r
    done                                                   # main 468 survivors, order 8922c963f670; control 570, order 52ad6487743f
    PYTHONHASHSEED=0 python3 riff_p40.py                   # the riff, fills, riff break
    PYTHONHASHSEED=0 python3 build_p40.py                  # song_record.pkl from the main run's shortlist pick 2fe2be999be7, no hand edits
    python3 demo_p40.py; python3 engrave_p40.py; python3 nashville_p40.py
    python3 readings_p40.py                                # the report's readings (readings_p40.json)
    python3 test_report_p40.py; python3 fixlist_p40.py     # test_report_p40.md, fixlist_p40.md (findings 298-307 in findings_p40.md)
    python3 consistency_p40.py                             # 65/65

Code sha 8275c26ef512 (melody_p40.py + lyric_p40.py + judges.py + melody_p36.py). show_pick.py prints a pick line by line.
