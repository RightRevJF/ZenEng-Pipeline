# lib/luthier: Luthier v8, stage 1 (Module 27.89, Window 165; fixes 750 to 753)

Made by Luthier's maintainer on 18 November 2026, at the writer's instruction to repair what it could itself.

| File | What it is |
|---|---|
| `gen_l8.py` | Makes a song's v8 engine from its v7 file: `python3 lib/luthier/gen_l8.py /home/claude/p64` writes `melody_l8_p64.py` and copies `luthier_judge6.py` beside it. Every patch must match once. |
| `luthier_judge6.py` | The pick until the judge is rebuilt (752). `pick(builds)` as `luthier_judge5`'s; `pick(builds, runs="kept")` uses the kept 75th percentile as the ceiling on runs instead of the writer's. |
| `luthier_v8_tables.json` | The rhythms 750 refuses, and the kept figures 752 uses. |

**750.** The kept-bar table (`luthier_v3_tables.json`, 652) holds three rhythms with one onset twice. A drawn bar that took one sang two
syllables on one onset, the first with no length (749.1, 749.26). The loader keeps only rhythms whose onsets rise strictly inside the bar.
**751.** A build with two notes on one onset, or a note of no length, is a death in `evaluate`.
**752.** The pick is `luthier_judge6`'s. **753.** `lib/carol/lyricsearch.py` reads `-in'` forms from `-ing`, `'n'`, `a.m.` and `p.m.`

Run: `PYTHONHASHSEED=0 python3 melody_l8_pNN.py 1000 main|ctl` (files go to `runl8/`). Every order differs from v7's, since three bars
have left the draw. Start the next song's engine from an `l8` file, or run `gen_l8.py` on its `l7` file.

## Stage 2a (Luthier v9, Module 27.90, Window 166; fixes 760 to 766)

| File | What it is |
|---|---|
| `gen_l9.py` | Makes a song's v9 engine from its v7 file (stage 1's patches, then stage 2a's): `python3 lib/luthier/gen_l9.py /home/claude/p64` writes `melody_l9_p64.py`; run files go to `runl9/`. |
| `slots.py` | 763: a line's slot proposed from its syllables and the tempo, in seconds (reads `studies/metre/metre_results.json`). Not yet applied to a song. |
| `stage2_results.json` | Songs 49, 50, 51, 54, 55 on stage 1 and stage 2a, main and control. |

**760.** A line the rhythm draw cannot place is set by weighted rules in the same window (kept shares of stressed and unstressed syllables
by place in the bar; the kept palette's gap shares; the sixteenth grid). **761.** No gap of three beats inside a drawn line of eight
syllables or fewer. **764.** A line leaves the next line room. **765.** The breath before a line gives way, down to 18 twelfths.
Deaths for want of a placement, a thousand builds: song 54 652/664 to 0/0; song 55 682/676 to 53/50; song 51 487/486 to 0/0; song 50
261/218 to 0/0; song 49 54/44 to 0/0. Start the next song from an `l9` file.
