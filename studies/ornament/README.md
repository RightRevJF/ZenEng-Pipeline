# Vocal ornament and expression

Report: the Doc "Vocal ornament and expression for Luthier v8" (https://claude.ai/artifact/Mdr5ay2zJo9VoBh11yVgr4).

- `ornament_corpora.py`: melisma (a syllable on two or more different pitches, ties merged) rates, lengths, phrase-end placement, shape and thirds of the song, plus grace notes per 100 notes, in PDMX English songs by category, OpenEWLD standards, and CoCoPops Billboard and Rolling Stone 200 (from ../words/sung_syllables.json, made by ../words/parse_words.py). Needs PDMX extracted by ../words/pdmx_words.py --extract. About 6 minutes on two cores. Writes `ornament_results.json`.
