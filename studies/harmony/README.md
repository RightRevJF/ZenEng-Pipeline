# Harmony study for Luthier v8 (16 November 2026)

The report is a Doc: https://claude.ai/artifact/9vgkWHkjy3PyVMB9iKDkBJ (the audit it follows: https://claude.ai/artifact/4VpCZjhV64ua7EjPykjS1K).

Data (not in the repo): ChoCo v1.0.0 from Zenodo record 7706751 (`smashub/choco-v1.0.0.zip`, 467 MB), unzipped to
/home/claude/data/choco. The McGill Billboard raw files are `partitions/billboard/raw/original/*/salami_chords.txt` (CC0);
the Rolling Stone 200 analyses are `partitions/rock-corpus/raw/rs200_harmony/*_dt.har`.

1. `parse_billboard.py` -> billboard_sections.json (739 songs, 7,099 sections, Roman numerals on the tonic, mode per song)
2. `measure_billboard.py` -> billboard_tables.json (by section kind and mode; joins; returns; decades)
3. `prototype_writer.py` -> prototype_results.json (a variable-order Markov writer, 80/20 by song, seed 56, against a frequency baseline)
4. `rs200.py` -> rs200_tables.json (the replication)
