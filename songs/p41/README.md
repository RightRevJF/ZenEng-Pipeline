# ZenEng v109: the port (fixes 298–309), tested on song 40, before song 41

    python3 limits_v109.py                                   # 300/301: realness out; the six of 286 read jointly (94.2%, no refit)
    for m in main ctl; do PYTHONHASHSEED=0 python3 melody_v109_p40.py 1000 $m; PYTHONHASHSEED=0 python3 melody_v109_p40.py 1000 $m _r; done
                                                             # main 476 survivors, order 6ad97e7695d1; control 398, order 4974bb2f8af1
    python3 readings_v109_p40.py                             # the tests of 298-309 -> port_report_v109.md (findings 310-313)
    python3 trace_opens.py melody_v109_p40.py 20 main _trace # 309: every file a run reads (all committed; setup.sh links songs/pNN)

# Song 41: The Water Used to Sing (default path, swung shuffle, q = 96, G major, 104 bars)

Words and music: Jason Bryant. Intake Q1-Q20 in intake.py; the locked lyric in lyric_locked.md and lyric_p41.py.

    bash run41.sh                                            # 1000 main + 1000 control, each twice (seed 20261521, code 2cb5717c5b99)
                                                             # main 615 survivors, order 615aa4e7f73d; control 660, order 83c59a365e29
    PYTHONHASHSEED=0 python3 pick_p41.py                     # 255's pick, 4767e10a1dce, no hand edits -> melody_final.pkl
    PYTHONHASHSEED=0 python3 riff_p41.py                     # the lick, the break solo, the fills, the last chorus's countermelody
    PYTHONHASHSEED=0 python3 build_p41.py                    # the song record
    python3 demo_p41.py; python3 engrave_p41.py; python3 nashville_p41.py
    PYTHONHASHSEED=0 python3 consistency_p41.py              # 44/44
    python3 trace_opens.py melody_p41.py 5 main _trace       # 309: reads_melody_p41.txt (all committed)

test_report.md: the run and findings 314-319. songbook.md: the musicians' songbook (Doc and Word).

## Song 41 made for real (the writer's Q21-Q25)

    PYTHONHASHSEED=0 python3 melody_p41d.py 1000 design       # twice: 504 survivors, order 33000bf520dd (designs: hook to D4, verses on D3,
                                                             # eighths only, E4 once on 'shine', 'It sings.' home to G3; the bridge under the verse)
    PYTHONHASHSEED=0 python3 pick_p41d.py                     # e6ba46e75684 (255's pick, read by ear against the shortlist), no hand edits
    PYTHONHASHSEED=0 python3 riff_p41d.py; PYTHONHASHSEED=0 python3 build_p41d.py
    python3 demo_p41d.py; python3 engrave_p41d.py; python3 nashville_p41d.py
    PYTHONHASHSEED=0 python3 consistency_p41d.py              # 47/47
