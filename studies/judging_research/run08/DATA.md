# Run 08: data

27 November 2026, the 02:17 ET pass.

## Found and used tonight (the way through that run 07 named: chords rather than MIDI arrangements, with names)
- **ChoCo, the Chord Corpus v1.0.0** (de Berardinis, Meroño-Peñuela, Poltronieri & Presutti 2023; Zenodo 7706751, `smashub/choco-v1.0.0.zip`, 467 MB; the paper at Zenodo 11221563, CC BY 4.0). Partitions used: iReal Pro forum (33,840 charts) and playlists (2,048), Wikifonia (6,114 with chords). Parsed by `experiments/parse_choco.py` (Harte labels through mir_eval; the converter's "113" for 13 repaired) into a cache outside the repo.
- **Discogs-VI 20240701** `main.zip` (Zenodo 13983028, CC BY-SA 4.0), reduced by the maintainer's `cliques_versions.py` unchanged (348,796 cliques).
- **Hooktheory.json.gz** (sha256 917b7cd5…8e0c), downloaded but not read this pass (the seen Hooktheory songs were excluded by clique id from the pack's tables instead).
All raw downloads are in /home/claude/dl, outside the repo.

## The match (notes side first, `experiments/common.py build_design`)
- 42,002 charts; 6,095 with a stop artist ("Composer Unknown", "Traditional", arranger tags); 392 with under 8 chords.
- 22,290 charts matched a clique by title plus a name token found among the clique's **writers** (8,003 of 8,640 songs) or performers; 3,809 of them fell on seen cliques (Hooktheory pack, run 06 fresh, run 07 Lakh) and 244 on McGill hold-out songs, all dropped before anything was read.
- **8,640 songs**: 5,907 by 1,199 composers with two or more (the design of the first eight tests), 2,733 by single-song composers (`iiv_singletons`).
- The joined table: `studies/judging_research/data/choco_songs_discogs_run08.json` (3.4 MB; CC BY-SA 4.0 as derived from Discogs-VI; ChoCo CC BY 4.0).

## Lessons about the data (notes side)
- About half of same-title iReal pairs are exact copies (forum and playlist copies of one file); stability was measured on non-identical pairs only.
- Agreement between an iReal chart and a Wikifonia chart of the same song is lower (0.31 to 0.67 by measure) than between two iReal charts (0.60 to 0.81): the chart writer matters.
- iReal charts are written by the players whose recordings make the outcome (first principles, section 2).
- The composer key is the matched writer's whole name (`person_key`), so Rodgers with Hart and Rodgers with Hammerstein share "richardrodgers"; "georgegershwin" and "georgeandiragershwin" stay apart.

## Spent tonight (now seen)
- 5,907 within-composer ChoCo songs (rules e624a7e; results in b1b3512 and later).
- 2,733 single-composer ChoCo songs (`iiv_singletons`, rule b1b3512, results e913c96).
- Possible small overlap: run 07's 3,436 Lakh single-song-artist songs are in no committed table, so they could not be excluded by clique.

## Still unseen
- **542 songs** from ChoCo charts that matched nothing by title plus name, matched by title alone to exactly one clique (`posthoc08.title_only_rows`, counted from clique titles only). Power 0.04 for the ii-V lead: not run, kept.
- ChoCo's other partitions (Real Book, Band-in-a-Box, JAAH, Weimar, Isophonics, uspop2002, rock corpus, Chordify): not parsed; artist fields unchecked. Billboard is the McGill hold-out's source and must not be used.

## Still missing

| Idea | Missing file(s) |
|---|---|
| A confirmation of the ii-V lead outside the iReal community | Chord charts with title and composer written upstream of covering (published first-edition sheet music, a lead-sheet corpus not made by jazz players), several thousand songs. Not found on Zenodo or GitHub this pass. |
| R03-I1 melody transport | Wikifonia MusicXML melodies are in the ChoCo zip (`partitions/wikifonia/raw/*.mxl`) but not parsed yet: a parsing job, not a data request. |
| W01-J6c the MusicLab ceiling | The MusicLab per-song download and rating data (Salganik, Dodds & Watts 2006). |
| R02-breadth | `discogs_20240701_releases.xml.gz` (genres per release), from data.discogs.com (not reachable). |
