# Trials for Luthier v36 (749.119): which fix moved the pools?

Run through `studies/soundness/neighbour.py` with a trial copy (as `studies/review21/README.md` describes). Failures of the soundness rule in 100:

| | Neighbour choice | Random pick from the engine's pool |
|---|---|---|
| v34 | 0.5 | 2.5 |
| v35 | 2.5 | 2.6 |
| v35 without 936 (the session's trial) | 4.8 | 5.4 |
| v35 without 935 (`neighbour_v35_no935.json`) | 2.5 | 2.6 |
| v35 with v34's fit sizes, 934 off (`neighbour_v35_no934.json`) | 1.8 | 8.0 |
| v36 | 1.3 | 5.1 |

- **935 changes nothing in songs 55, 54 and 58.** `cmp935.py` builds each song with and without it from the same draws: 60 builds of 60 are note for note the same. The limit is set and never binds. Only song 59 changes. (Run with the engine file as the first argument and a copy with 935 switched off as the second.)
- **No one fix accounts for the rise** in the neighbour choice. At 400 draws these are 2 to 20 failures and the trials move as much among themselves.
- `trace_v35.json`, `trace_v36.json`: where repeated notes are made (`studies/v35_traces/trace.py`), before and after 939.
