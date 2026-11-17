# Arrangement study for Luthier v8 (16 November 2026)

The report is a Doc: https://claude.ai/artifact/LKpemmb3kU5NWy4rPmnWTQ (after the audit https://claude.ai/artifact/4VpCZjhV64ua7EjPykjS1K
and the harmony study https://claude.ai/artifact/9vgkWHkjy3PyVMB9iKDkBJ).

Data (not in the repo): POP909 MIDI and beat files from raw.githubusercontent.com/music-x-lab/POP909-Dataset, with Dai, Zhang and
Dannenberg's human_label1.txt from raw.githubusercontent.com/Dsqvival/hierarchical-structure-analysis, in /home/claude/data/pop909;
LPD-5 cleansed (Zenodo 5646574) and Gold-Caps LMD-Matched (Zenodo 10178563) in /home/claude/data/lpd.

1. `pop909_texture.py` -> pop909_texture.json (texture by phrase role; paired B against A)
2. `lpd_genres.py` -> lpd_genres.json (a genre per Lakh song from the artist's top MSD term)
3. `lpd_band.py` -> lpd_band_rows.json (drums, bass, chordal parts, parts playing per song; 9,329 songs, up to 1,500 a genre, seed 56)
4. `lpd_band_tables.py` -> lpd_band_tables.json (by genre; the bass by tempo)
