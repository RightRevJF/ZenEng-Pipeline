# Run 07: hold-out log

26 November 2026. **The McGill hold-out was not used.** `studies/judging_data/mcgill_covers_discogs_HOLDOUT.json` was not read. Song 59, songs/p69 and studies/holdout59 were not read.

The only contact with the McGill set: `studies/harmony/billboard_sections.json` (notes and names, not outcomes) was read for artist and title, so that the 155 Lakh tracks (131 after the ambiguous-file rule) that are McGill songs could be **excluded before anything else** (`common._mcgill_keys`). No measure has passed, so no hold-out request is posted.
