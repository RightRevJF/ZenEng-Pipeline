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

## v2: the rerun under ZenEng v107 (a regression run; findings 286-295)

Same lyric, intake answers, form, key, tempo, chords; seed 20261491, calibration seed 20261492; the judges' weights not refitted.
Tables added from the tables artifact: zeneng_v104_line_in_time.json, zeneng_v105_kept_windows.json, zeneng_v105_song38_checks.json,
zeneng_v106_gate_limits.json (read, not refitted). Every v1 file is kept.

    PYTHONHASHSEED=0 python3 melody_v2_p38.py 3000 A      # gates only (276-278, 270, 264, 267): 219 survivors, order 2f9ce3d36fce
    PYTHONHASHSEED=0 python3 melody_v2_p38.py 3000 B      # full v107 (+282): 610 survivors, order d648725d3587
    PYTHONHASHSEED=0 python3 melody_v2_p38.py 3000 C      # B with 243 off: 702 survivors, order 3a6e5a3ea5af
    python3 tableb_v2_p38.py                              # fix 280: the seven unaudited gates on the 515 POP909 calibration pairs
    python3 readings_v2_p38.py                            # report items 1-9 (readings_v2.json)
    python3 riff_v2_p38.py; python3 build_v2_p38.py       # record from Run B's shortlist pick 45a09df333f6, no hand edits
    python3 demo_v2_p38.py; python3 engrave_v2_p38.py; python3 nashville_v2_p38.py
    python3 test_report_v2_p38.py; python3 consistency_v2_p38.py   # 55/55
    python3 fixlist_v2_p38.py                             # fixlist_v2.md

Each run reproduces its frozen order on a second run (code d3c2a04c325b). Every build is kept on file (`every` in melody_v2_*.pkl).
