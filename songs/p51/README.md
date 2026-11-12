# songs/p51: the v119 port, with v120's changes — songs 40, 42, 43, 44 and 45 again

Words and music of all five songs: Jason Bryant.

Fixes 384–398, 400 and 388's side runs are ported from v119 (Module 27.63) in steps, without editing the paper, with runs between the steps.

- Fixes 399 and 401 are withdrawn by v120 (Module 27.64, 421) and are not ported.
- Fix 424 from v120 is added in step 3.
- Tests, costs and separation are read on the 30 agreed measures, against CoCoPops and BiMMuDa 1958–1991 pooled (420, 422).
- The session's findings are 402–419.
- No new song. Song 45 runs as drawn.

## Files

- **Generators.** `gen_v119.py` writes `melody_v119_p40.py` … `melody_v119_p45.py` from songs/p50's v118 files.
  - Every patch replaces whole statements, and each is matched once in each file.
  - Steps are switched by `ZE_STEP` (1, 2, 3). Step 1's runs reproduce from the final files.
- **The writer's choices.** `intake.py`: Q1 A for 386 against 267, and the v120 instruction.
- **Step 1** (`step1/`): songs 40, 42 and 43, main runs, read by `step_read.py`. The reproduction check is `run42_main_check.txt`.
- **Step 2** (`step2/`): 388's two side runs on song 40.
  - `withdrawn_step2/`: the first step-2 runs, made with 399 and 401 before v120 arrived. These are not runs of record.
- **Step 3.** `run_v119.sh` makes every song's main and control run twice, at `ZE_STEP=3`. The output is in `run4x_*.txt`.
- **Side runs** (`diag/`): song 45 with 392, 398, 400 or 424 off (finding 412).
- **Readings.**
  - `readings_v119.py` (with `readings_v119_block.py`) writes `readings_v119_p*.json` and `_table.json`.
  - `sep_v120.py` writes `sep120_v119.json`. The v118 figures are in `base/sep120_v118_five.json`.
  - `sep_v119.py` gives v119's 46-measure families, which v120 replaces.
- **Report.** `make_report_v119.py` writes `test_report_v119.md`, also as `test_report_v119.docx`. It reads `port_notes_v119.md`, `readings_notes_v119.md` and `findings_v119.md`.
- **Tables.** `tables/` holds every table the runs read, including `zeneng_v119_families.json`, `zeneng_v120_second_collection.json` and `zeneng_v120_bimmuda_windows.json`.

The `.pkl` outputs are not committed.
