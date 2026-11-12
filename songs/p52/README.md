# songs/p52: ZenEng v124 Run 1

Words and music of all five songs: Jason Bryant. This folder is the session's repairs (405, 409, 412–415, 417, 419, and 428 withdrawing 424's empty-bar rate) on the v119 port (songs/p51), with v121–v123's readings. No new song.

## The files

- **The engine.**
  - `gen_v124.py` writes `melody_v124_p40.py` to `melody_v124_p45.py` from songs/p51's v119 files.
  - Each patch replaces whole statements, matched the stated number of times in each file (384).
  - `ZE_OFF` switches a fix off, for side runs only. `ZE_DIAG450=1` makes 267 read song 45's bridge G before its raise (finding 450), as a diagnostic only.
- **The runs.**
  - `run_v124.sh` makes the runs of record (five songs, main and control, each twice) and the first side runs. `run_v124b.sh` adds song 45's side runs with 392, 413 and 414 off; the 428-off run was made by hand the same way.
  - `run*.txt` hold each run's log, with its `rerun` record.
  - The `.pkl` files are not committed.
- **The predictions.** `predictions_run1.md` was committed and pushed before the runs (d6db58e). `predictions_scored.md` scores them.
- **The readings.**
  - `readings_v124.py` is readings_v119.py run with `readings_v119_block_for124.py` and `readings_v124_block.py`. It writes `readings_v124_p*.json` and `_table.json`.
  - `new_readings_v124.py` reads 426, 431–433, 436, 437, 441–443 and 430 with the studies' own code, from the v121–v123 tables. It writes `new_readings_v124.json`. 430 reads songs/p49's pick of record, `melody_final.pkl`.
  - `range_v124.py` writes `range_v124.json`, and `side_v124.py` writes `side_v124.json`.
  - `sep_v120.py` writes `sep120_run1.json`.
- **The report.** `make_report_v124.py` writes `test_report_v124.md`, also as `test_report_v124.docx`. It reads `port_notes_v124.md`, `predictions_scored.md` and `findings_v124.md` (findings 450–463).
- **The smoke runs.** `smoke/` holds the 40-build smoke runs of every patched path.
- **The writer's instruction** is logged in `intake.py`.
- **The tables** are in `tables/`. Every file a run reads outside this folder sits in songs/p36, p37, p40, p41, p49 and lib/ (traced with songs/p41/trace_opens.py).
