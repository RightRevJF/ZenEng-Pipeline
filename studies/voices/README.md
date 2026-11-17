# Harmony voices (duets, backing vocals, choirs)

Report: the Doc "Harmony voices for Luthier v8" (https://claude.ai/artifact/WfTuzxkKzyUPiCvhFn75Dz).

- `parse_parts.py`: every part of a MusicXML score (.mxl or .musicxml), voice 1, ties merged, absolute onsets from the first part's bars, lyric flags. Reads PDMX, OpenEWLD and the engine's own scores.
- `voices_pdmx.py`: lead against each other vocal part in PDMX (Zenodo 15571083, CC BY 4.0). Needs `/home/claude/data/pdmx` with PDMX.csv and the files extracted by `../words/pdmx_words.py --extract`. About 9 minutes on two cores. Writes `voices_pdmx_results.json`.
- `voices_pdmx_results.json`: by category (popular, folk, hymns and sacred, other classical) and texture (2 voices both with words, 2 voices one with words, 3 voices, 4+ voices): interval classes, side, v7's set, crossing, onset agreement, motion types, parallel fifths, octaves and unisons per 100 motions, presence by fifth of the song.

The "2 voices, one with words" group is noisy (part names alone decide that the second part is a voice) and is not used in the report.
