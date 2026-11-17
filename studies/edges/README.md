# Song edges (intros, endings)

Report: the Doc "Song edges for Luthier v8" (https://claude.ai/artifact/Fh1UcSKfZisqVde8ewz62m).

- `edges_billboard.py`: McGill Billboard (salami_chords.txt via ChoCo, Zenodo 7706751, at /home/claude/data/choco/...): per-song intro seconds and bars, the voice's entry, intro material and lead instrument, fade or cold ending, last section, outro length, last two chords, bookend. Writes `edges_billboard.json` (739 distinct songs).
- `edges_tables.py`: tables by period (1958-64 to 1985-91). Writes `edges_tables.json`.
- `edges_pop909.py`: POP909 intro and outro bars from human_label1.txt. Writes `edges_pop909.json`.
