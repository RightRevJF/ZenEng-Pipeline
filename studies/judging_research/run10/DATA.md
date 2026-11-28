# Run 10: data

27 November 2026, the 18:17 ET pass.

## Found and used this pass
- **TheSession.org data dump** (github.com/adactio/TheSession-data, `csv/` on main, fetched 27 November 2026 18:19 ET to /home/claude/dl/thesession, outside the repo): `tunes.csv` (55,838 settings of 23,199 tunes, ABC bodies, type, meter, mode, first-posting date, poster, composer), `tune_popularity.csv` (tunebook counts for the 11,807 tunes with 10 or more), `recordings.csv` (203,782 tracks: artist id, recording, tune id), `aliases.csv` (not used). Published by thesession.org for reuse; credit TheSession.org in anything derived.
- **Never joined by this project before.** Run 02 read McBride & Leroi's paper on the same site, but no experiment used the data. It breaks run 09's obstacle (every charted song with names spent) at the price of a new repertoire: Irish and related traditional dance tunes, melody only.
- **Parse:** `experiments/abcparse.py` (unit-tested), 99.24% of settings ok; report at /home/claude/dl/thesession/parse_report.md. Each tune is its first ok setting (the original posting), repeats expanded. 23,089 tunes with 16 or more notes.
- **Splits** (sha256 of 'thesession:<tune_id>', first hex digit): A 0 to 9 (14,511 tunes; this pass's tests), C a to c (4,261; confirmations, now seen), H d to f (4,317; sealed for run 11).
- **Outcomes:** y_cov = log(1 + distinct recording artists) (69% of tunes have at least one; mean 5.4 artists); y_love = log(tunebooks), only for tunes with 10 or more (about half of the tunes).
- **Notes-side cache:** /home/claude/dl/thesession/measures_run10.json (all proposals' measures and the 13 baselines, splits A and C; `experiments/build_cache10.py`). Not committed (it can be rebuilt from the scripts).

## Spent this pass (now seen)
- Split A, 14,511 tunes: eight frozen tests (641f966; results 629b8da).
- Split C, 4,261 tunes: three confirmations (rules 629b8da; results d823e98) and gap_full_C (after seeing results; rule d823e98, result e8eddd8).

## Still unseen
- **Split H** (4,317 TheSession tunes), sealed for run 11's frozen confirmations of GAP, core_ic and LOCK.
- **Future outcomes:** tunebook adds and recordings made after 27 November 2026 (a re-download of the same dump later gives a time-split outcome that today's notes cannot have been shaped by; first_principles.md, section 6).

## Still missing

| Idea | Missing file(s) |
|---|---|
| First-poster fixed effect (R10-S2) | Nothing missing: `username` is in tunes.csv; common10 must carry it before a test can freeze it |
| Lasting love as distinct from uptake | A time series of tunebook adds (TheSession has per-member tunebooks; the dump has only totals) |
| The late-window ii-V lead after July 2024 (R09-4) | A Discogs monthly release dump newer than July 2024, or a newer Discogs-VI (not reachable from here) |
| R02-breadth | `discogs_20240701_releases.xml.gz` (genres per release), data.discogs.com (not reachable) |
| W01-J6c the MusicLab ceiling | The MusicLab per-song data (Salganik, Dodds & Watts 2006) |
