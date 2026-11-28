# Run 10: hold-out log

27 November 2026, the 18:17 ET pass.

- **The McGill hold-out** (`studies/judging_data/mcgill_covers_discogs_HOLDOUT.json`): not read, not used. This pass used no chord data at all; its corpus is TheSession.org, which has no McGill songs.
- **Song 59** (`songs/p69`, `studies/holdout59`): not read.
- **This pass's own sealed split H** (4,317 TheSession tunes, sha256 of 'thesession:<tune_id>' first hex digit d to f): no measure was computed on it and no outcome was joined (`common10.load_outcomes` refuses split H; `build_cache10.py` computes splits A and C only). It is kept for run 11's frozen confirmations (first_principles.md, section 5).
- **Split C** (4,261 tunes) was joined four times this pass: three confirmations written before the join (629b8da) and one test written after seeing results (gap_full_C, rule d823e98). It is now seen.
- **One thing to state:** to size the design, the orchestrator printed the outcome files' row counts and the tunebook distribution (min 10, median 28) at 18:19 ET, before any measure existed. No measure was ever compared with an outcome before the predictions commit 641f966.
