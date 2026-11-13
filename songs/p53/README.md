# songs/p53: ZenEng v127 Run 2

Words and music of all five songs: Jason Bryant. This is Run 2 of 3, on top of Run 1 (songs/p52). It adds the refit judge (470–473), Part 0 (464, 459), Part 1 (434, 435), Part 2 (452, 455, 406, 457) and Part 3 (408 with 468, 467, 461 with 450, 456), with a rerun of all five songs after each of Parts 1–3. 465 and 458 wait for their kept tables (Q1 A, finding 480). No new song.

## The files

- **The engine.**
  - `gen_v127.py` writes `melody_v127_p40.py` to `melody_v127_p45.py` from songs/p52, with the Part 2 and 3 patches from `gen_v127_parts23.py`.
  - `ZE_PART` (0–3) switches the parts. Each part's runs reproduce from the final files.
- **The runs.**
  - `run_v127.sh K` makes Part K's runs (five songs, main and control, each twice) into `partK/`. The `.pkl` files are not committed; `partK/run*.txt` hold the logs and `rerun` records.
  - `side_runs.sh` makes song 45's Part 2 side runs (406 off, 457 off) into `side/`.
  - `sep_ctl.sh` reads separation on the control runs (`ctlsep/`).
- **The predictions.** `predictions_partK.md` were each pushed before Part K's runs. `predictions_scored_partK.md` score them.
- **The readings** (`read_part.sh K PREV`):
  - `readings_v127.py`, which runs `readings_v119_block_for127.py`, `readings_v124_block_for127.py` and `readings_v127_block.py`, writes `partK/readings_v127_p*.json` and `_table.json`;
  - `sep_v127.py` (the agreed 30, and the 30 without each family) writes `partK/sep.json`; Run 1's is in `part0_sep.json`;
  - `reread_v127.py` (Window 147's reading, every run so far) writes `reread_v127.json`.
- **The report.** `make_report_v127.py` writes `test_report_v127.md`, also as `.docx`. It reads `what_was_run.md`, `port_notes_v127.md`, `kept_cannot_pass.md`, the scored predictions and `findings_v127.md` (findings 480–496).
- **The writer's instruction and Q1** are logged in `intake.py`.
- **The tables** are in `tables/`, including v124–v127 from the tables page.
