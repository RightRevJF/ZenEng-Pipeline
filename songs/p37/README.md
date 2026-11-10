# Song 37: Windows Down (ZenEng v96) — regenerate the builds

Tables (not in the repo): zeneng_v88_tables.json (sha256 561355b1…), zeneng_v96_discriminator_tables.json (1a2af952…), in `tables/`. Uses ../p36's melody_p36.py and engine.

```
PYTHONHASHSEED=0 python3 melody_p37.py 500 main   # seed 20261481: 153 survivors, frozen order 15ed5929f53d, pick 9a3e548d293f
PYTHONHASHSEED=0 python3 melody_p37.py 500 ctl    # control, 224 off: 109 survivors, order 4d23a255a8b9
PYTHONHASHSEED=0 python3 melody_p37.py 500 wide   # probe, targets from the kept 5th-95th: 147 survivors, order f04360d518e5
PYTHONHASHSEED=0 python3 riff_p37.py              # the instrumental hook and the solo (seeds +1, +2)
python3 build_p37.py && python3 demo_p37.py && python3 engrave_p37.py && python3 nashville_p37.py
python3 readings_p37.py && python3 songbook_p37.py && python3 test_report_p37.py && python3 consistency_p37.py   # 47/47
```
Code sha (melody_p37.py + lyric_p37.py + melody_p36.py): b1b68b67d425. Python 3.13.18, numpy 2.5.3. `show_p37.py k [mode]` prints survivor k syllable by syllable.
