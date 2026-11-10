# Song 38 — Stay Tuned (ZenEng v103)

Words and music: Jason Bryant. Rock (Who-style), 4/4 at q = 132, A major, 114 bars, 3:27. Idea worked out with the writer first, then the engine.

Run, in order (PYTHONHASHSEED=0; tables from the v103 tables artifact into ./tables):

    python3 melody_p38.py 3000 main      # seed 20261491, calibration seed 20261492
    python3 melody_p38.py 3000 ctl       # control: 243 off
    python3 riff_p38.py                  # intro tune, fills, solo, countermelody
    python3 build_p38.py                 # song_record.pkl from the shortlist pick (255)
    python3 demo_p38.py; python3 engrave_p38.py; python3 nashville_p38.py
    python3 q1020_p38.py; python3 readings_p38.py; python3 songbook_p38.py; python3 test_report_p38.py
    python3 consistency_p38.py           # 59/59

judges.py carries 27.47 (fixes 252-255) with the selector file's weights; it reproduces song 37's check values.
Findings 257-268 are in findings.md.
