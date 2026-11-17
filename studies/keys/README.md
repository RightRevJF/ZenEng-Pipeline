# Key choice

Report: the Doc "Key choice for Luthier v8" (https://claude.ai/artifact/33a22MifajNw9xoU1pc57Q).

- `keys_corpora.py`: keys and modes in McGill Billboard (by lead instrument and era), BiMMuDa (by era and genre), and the notated key signatures of PDMX and OpenEWLD (left out of the report: user scores default to C). Writes `keys_results.json`.
- `tonic_in_range.py`: where the tonic sits in the sung range (5th to 95th percentile) in BiMMuDa full melodies and CoCoPops Billboard. Writes `tonic_in_range.json`.
