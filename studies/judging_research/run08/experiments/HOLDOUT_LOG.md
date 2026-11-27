# Run 08: hold-out log

27 November 2026. **No hold-out was used.** The McGill hold-out's songs were removed from the ChoCo design by clique (a clique whose title equals a McGill chart's title and whose performers include its artist, from `studies/harmony/billboard_sections.json`): 244 charts dropped before anything was read. `mcgill_covers_discogs_HOLDOUT.json` was not opened. ChoCo's Billboard partition (the McGill charts' source) was not parsed. Song 59, songs/p69 and studies/holdout59 were not read.

## A slip, stated (04:20 ET)
While looking for the latest Luthier fix list on origin/main, a version sort picked `songs/p69/fixlist_v35.md` (song 59's folder) as "latest", and its first 30 lines were printed (the v35 list of 20 November: song 59's hold-out readings summary). That breaks the rule never to read song 59's folders. Nothing from it was used in any test, measure or proposal; no song-59 outcome or record file was opened. The real latest list, `songs/p68/fixlist_v53.md`, was read instead. Reported in the thread post.
