# The hook study (17 November 2026)

What makes a chorus stick, measured for Luthier v8. Doc: https://claude.ai/artifact/NnkTkwF3cFxbtZjrz2NSLn

- `hooks_hooktheory.py`: features of 22,407 Hooktheory sections joined to their section names (self-repetition, typical cells,
  surprise, the main 4-note cell, uniqueness points with and without rhythm). Writes `hooks_clips.json.gz` (derived numbers only).
- `hooks_analyse.py`: chorus against verse in the same song (2,839 songs), and intro, pre-chorus and bridge. `hooks_hooktheory_results.json`.
- `hooks_catchiest.py`: the 14 Hooktheory songs among the 20 that Hooked on Music players recognised fastest. `hooks_catchiest_results.json`.
- `hooks_titles.py`: where the title falls in 214 CoCoPops Billboard hits (no lyrics kept). `hooks_titles_rows.json`, `hooks_titles_results.json`.
- `hooks_our_songs.py`, `hooks_our_titles.py`: songs 52 to 56 against the same measures. `hooks_our_songs.json`, `hooks_our_titles.json`.

Run order: hooks_hooktheory.py (about 15 minutes), hooks_analyse.py, hooks_catchiest.py, hooks_titles.py, hooks_our_songs.py, hooks_our_titles.py.
Data: Hooktheory via Sheet Sage (/home/claude/chrisdonahue/sheetsage-data, CC BY-NC-SA); CoCoPops at /home/claude/data/cocopops.
