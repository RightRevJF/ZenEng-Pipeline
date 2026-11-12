# songs/p50: ZenEng v118, songs 40, 42, 43, 44 and 45 run again

Words and music of all five songs: Jason Bryant.

This folder ports fixes 365–383 (v117's and v118's) onto the v116 search, without editing the paper. Songs 40, 42, 43, 44 and 45 were run again with the same lyrics, intakes, designs and seeds. Song 45 runs as drawn, without the hand edits. There is no new song.

## Files

- **The search, songs 40–45**
  - `gen_v118_p40.py` patches `songs/p47/melody_v116_p40.py` into `melody_v118_p40.py`.
  - `gen_p42_v118.py` … `gen_p45_v118.py` make `melody_v118_p42.py` … `melody_v118_p45.py`.
- **Runs**
  - `run_v118.sh`: every run of record, 1,000 builds each, main and control, each twice, at PYTHONHASHSEED 0.
  - Output: `run4x_*.txt`. Song 43's 368 runs (358 off, 361 off): `run43_main_off*.txt`.
  - `diag/`: 300-build side runs. Song 45 as run, with 366 off and with 378 off. Songs 40 and 43 as run, with 381 off and with 375 off.
- **Tables**
  - `tables/`: the v111–v118 tables.
  - `zeneng_v117_kept_rhythm_tables.json`: 372.
  - `zeneng_v117_kept_songs_and_modes.json`: 369.
  - `zeneng_v117_yardstick.json`: 374.
  - `zeneng_v118_slot_and_surprisal.json`: 378 and 382.
- **Readings**
  - `readings_v118.py` writes `readings_v118_p*.json` and `_table.json`.
  - `sep_v118.py` writes `sep_v118.json`, plus `sep_v115_true.json` and `sep_v116_true.json` for v115 and v116.
- **Report**
  - `make_report_v118.py` writes `test_report_v118.md` from `port_notes_v118.md`, `readings_notes_v118.md` and `findings_v118.md`.
  - The report is also in Word: `test_report_v118.docx`.

To rerun: `bash run_v118.sh`, then `python3 readings_v118.py 40` (and 42, 43, 44, 45), `python3 sep_v118.py` and `python3 make_report_v118.py`. The `.pkl` outputs are not committed.
