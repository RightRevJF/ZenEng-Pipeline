# Song 36, version 3: regenerate the builds

ZenEng v95 (version row v129, last fix 211), lyric draft 5 (`lyric_v2.py`), tables `zeneng_v88_tables.json` (sha256 561355b1110d1d8e…, not in the repo).

```
PYTHONHASHSEED=0 python3 melody_v3_p36.py 500 main   # seed 20261473: 55 survivors, frozen order 0256c9241d20, pick 374966ffc8d9
PYTHONHASHSEED=0 python3 melody_v3_p36.py 500 ctl    # control (199, 201, 205, 206 off): 130 survivors, order bb074ba2bb43
PYTHONHASHSEED=0 python3 riff_v3.py                  # the instrumental hook (209), seed 20261474
python3 build_v3.py && python3 demo_v3.py && python3 engrave_v3.py && python3 nashville_v3.py
python3 readings_v3.py && python3 tests_v3.py && python3 songbook_v3.py && python3 test_report_v3.py && python3 consistency_v3.py   # 49/49
```

Code sha (melody_v3_p36.py + lyric_v2.py + melody_p36.py): 9a1169b02f02. Python 3.13.18, numpy 2.5.3. `show_v3.py k` prints survivor k syllable by syllable.
