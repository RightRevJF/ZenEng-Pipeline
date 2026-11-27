# Run 09: data

27 November 2026, the 10:17 ET pass.

## Found and used this pass
- **ChoCo v1.0.0** (Zenodo 7706751, published 7 March 2023; CC BY 4.0), re-downloaded to a fresh machine. Run 08's parse was re-run unchanged (42,002 iReal Pro and Wikifonia charts, 41,206 with 8 or more chords, as in run 08). **New this pass** (`experiments/parse09.py`): the Band-in-a-Box internet corpus (4,989 files, titles only), the Real Book as Band-in-a-Box files (2,846; 609 with names), and charts transcribed from one recording: Isophonics (225), uspop2002 (195), rock corpus (200), Robbie Williams (62), JAAH (89), Weimar (456). Billboard and Chordify (the McGill source and Billboard ids), RWC-Pop (songs written for the database) and the classical and folk partitions were not parsed.
- **Discogs-VI 20240701** `main.zip` (Zenodo 13983028, CC BY-SA 4.0), reduced by the maintainer's `cliques_versions.py` unchanged (348,796 cliques).
- **JSIR** (github.com/MALerLab/JSIR at 1dd6b8b, CC BY-SA 4.0): 44 standards, lead sheets and 267 recordings' chords; card 2's notes-side check only.
- All raw downloads are in /home/claude/dl, outside the repo.

## The match (notes side first, `experiments/common09.py`)
32,827 charts considered (the new partitions plus run 08's iReal and Wikifonia charts that were not in run 08's design). Run 08's two rules, unchanged: title plus a writer or performer name where names exist (272 writer and 62 performer charts kept), else a unique title of two or more words (1,396 charts kept). Dropped before anything was read: 894 short charts, 5,313 stop or empty names (run 08's rule for its partitions, and stop names in the new ones), 6,392 charts of seen cliques, 304 McGill hold-out charts, 12,213 with no match, 3,382 with a non-unique title, 2,599 one-word titles.

**1,283 unseen songs**: 1,087 from charts, 191 transcribed from one recording, 5 both; 985 by title alone and 298 by title plus a name; 482 share a composer key with another song. By partition: BiaB 426, Real Book 360, iReal 459, Wikifonia 104, Weimar 66, Isophonics 41, uspop2002 30, JAAH 24, Robbie Williams 20, rock corpus 17.

The joined table: `studies/judging_research/data/choco_new_songs_discogs_run09.json` (0.55 MB; per song: clique, composer key, genre, match, provenance, partitions, chart ids, artist sets, first year, the frozen measures). CC BY-SA 4.0 as derived from Discogs-VI; ChoCo CC BY 4.0.

## Spent this pass (now seen)
- The 1,283 songs above (rules 379e219; results 687e735).
- Run 08's 8,565 seen songs were re-spent by three leads: `iiv_dres08`, `gap_writer08` (1,181 of them), and the two late-window leads, which for the first time read their artist sets split by year (2023 to 2024 against earlier; rules 4055742 and 780e2c2).
- Possible small overlap, as in run 08: run 07's 3,436 Lakh single-song-artist songs are in no committed table.

## Still unseen
**Nothing with chords and names on this machine.** Every ChoCo partition with matchable songs is now spent; what is left is Billboard (the hold-out's source), Chordify (Billboard ids), RWC-Pop, and classical and folk sets with no recordings to match.

## Still missing

| Idea | Missing file(s) |
|---|---|
| The late-window lead on artists after July 2024 (first principles, section 5) | A Discogs monthly data dump newer than July 2024 (`discogs_YYYYMM01_releases.xml.gz`, CC0, data.discogs.com: not reachable from here), or a newer Discogs-VI release |
| A powered confirmation of the ii-V lead on unseen jazz tunes | About 1,100 jazz tunes with title and composer from a chord source outside ChoCo (2,200 for power 0.8) |
| A confirmation outside jazz | Chord charts of pop, rock and folk songs with title and artist, several thousand, written by someone other than the covering community |
| CARC and TE (waiting) | Unseen songs (their recipes are frozen in `experiments/measures09.py`) |
| R02-breadth | `discogs_20240701_releases.xml.gz` (genres per release), from data.discogs.com (not reachable) |
| W01-J6c the MusicLab ceiling | The MusicLab per-song data (Salganik, Dodds & Watts 2006) |
