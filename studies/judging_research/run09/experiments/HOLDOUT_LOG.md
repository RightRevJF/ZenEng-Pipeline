# Run 09: hold-out log

27 November 2026, the 10:17 ET pass.

- **The McGill hold-out** (`studies/judging_data/mcgill_covers_discogs_HOLDOUT.json`): not read, not used. Its songs were excluded from the design before anything was read: any clique whose title and a performer equal a McGill chart's (`studies/harmony/billboard_sections.json`, run 07's keys), and, for title-only matches, any clique whose title equals a McGill title (261 and 43 charts dropped). ChoCo's Billboard and Chordify partitions (the McGill source and Billboard ids) were not parsed.
- **Song 59** (`songs/p69`, `studies/holdout59`): not read.
- **One small thing to state:** to see the versions file's format, its first two lines were printed (cliques C-0000000 and C-0000001: artist sets and years). Neither clique is in any design of this pass. Nothing was used.
