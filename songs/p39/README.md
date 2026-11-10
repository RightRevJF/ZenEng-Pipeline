# Song 39 — Fixed by Fall (ZenEng v103)

Words and music: Jason Bryant. Rock with a swagger: a shuffle in the verses, a straight rally march in the choruses; 4/4 at q = 108, E major, 90 bars, 3:20. One gritty baritone, double-tracked as two candidates in the last chorus.

Run, in order (PYTHONHASHSEED=0; tables from the v103 tables artifact into ./tables):

    python3 melody_p39.py 500 main      # seed 20261501, calibration seed 20261502
    python3 melody_p39.py 500 ctl       # control: 243 off
    python3 riff_p39.py                 # intro tune, fills, solo
    python3 build_p39.py                # song_record.pkl from the shortlist pick (255)
    python3 demo_p39.py; python3 engrave_p39.py; python3 nashville_p39.py
    python3 q1020_p39.py; python3 readings_p39.py; python3 songbook_p39.py; python3 test_report_p39.py
    python3 consistency_p39.py          # 56/56

Findings 269-273 are in findings.md.
