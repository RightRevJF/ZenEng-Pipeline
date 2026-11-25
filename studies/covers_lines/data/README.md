# Data for Design B (numbers and names only, no lyric text)

- `wasabi_english_meta.csv.gz`: 1,197,486 rows: id, artist, title, year, language, number of lines; the English songs of 8 lines or more in WASABI 2.0 (Buffa et al. 2021; Zenodo 5603369; CC BY-NC 4.0). Made by `make_wasabi_meta.py` (the data scout's, 25 November 2026) from the raw `song.json` member, then filtered to English and 8 lines or more.
- `dvi_cliques_writers.csv.gz`: 348,796 rows, one per Discogs-VI version clique (Araz, Serra & Bogdanov, ISMIR 2024; Zenodo 13983028): clique id, most common title, its four most credited writers and their ids, number of versions, number of distinct recording artists (first track of each version, names lowercased, Discogs' "(n)" suffix dropped), first year, genre. Made by `make_dvi_cliques.py` (the data scout's) from `main/Discogs-VI-20240701.jsonl`.
- `join.py` (one folder up) reads these two and reproduces `covers_join.csv` exactly.
