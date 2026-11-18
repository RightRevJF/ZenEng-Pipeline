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

## Stage 2b (Luthier v10, Module 27.91, Window 167; fixes 770 to 777)

`gen_l10.py` makes a song's v10 engine from its v7 file (stages 1, 2a and 2b): `python3 lib/luthier/gen_l10.py /home/claude/p64`
writes `melody_l10_p64.py`; run files go to `runl10/`. Start the next song from an `l10` file.

**770.** The floor under a line's start is the least breath (18 twelfths), not the breath the line before drew. **771.** The first onset
by the first syllable's stress in the old draw and in 760's rule. **772.** A line sung again that opens on a stress drops its source's
pickup and splits a long note for each note lost. **773.** A line sung again fitted ahead gives way to the line before it.
**774.** The 75% long-note band (749.32) is not adopted: kept songs read 0.55 at the median (`kept2b.json`). `stage2b_results.json`
has songs 49, 50, 51, 54, 55 on v9 and v10: deaths for want of a placement 0 on all five; entries by stress 19 of 30 shares
within ten points (15 under v9). Song 54's median build stands lower on the judge of 715 (0.63 for 0.80); printed (777).

## Stage 2c (Luthier v11, Module 27.92, Window 168; fixes 780 to 786): the session's review taken in

`gen_l11.py` makes a song's v11 engine from its v7 file (stages 1 to 2c); run files go to `runl11/`. Start the next song from an `l11` file.

**780** (749.42, 749.43): the join before a line fitted ahead asks the least breath (18 twelfths), not a drawn breath; a line sung again
fitted ahead gives way and is drawn again; a copied line keeps the join its source kept; two fixed lines may join a beat (12 twelfths)
apart, the kept 5th percentile. **781** (749.41): a.m. and p.m. only as whole tokens. **782** (749.45): `slots.py 112 13 10 7 -- 2 2 1`.
**783** (749.35): the record's notes carry `moved386` as an eighth field. **784** (749.40, 749.45): the stale run logs of stages 1 to 2b
are removed; `runl11/` logs are from the committed engines; `stage*_results.json` hold the earlier stages' figures.
**785**: 749.44 (the chorus over the verse) goes to stage 6. `stage2c_results.json`: songs 49, 50, 51, 54, 55 on v10 and v11.

## Stage 3 (Luthier v12): the metre as a setting, and the hymn mode — fixes 790–796

`metre_engine.py` is a melody engine with no metre in it. A song is a spec file; a metre is its table in `tables/metre_atlas/`.

    python3 songs/p62/mkspec52.py && python3 lib/luthier/metre_engine.py songs/p62/spec52.json 3000   # song 52, 6/8
    python3 songs/p63/mkspec53.py && python3 lib/luthier/metre_engine.py songs/p63/spec53.json 3000   # song 53, 3/4, hymn mode ("mode": "hymn")

Each run writes `<spec>.run.json` (the pick's notes, readings, charge, deaths, every survivor's fingerprint) and is the same for a seed.
Results: `stage3_results.json`; the two specs in other metres: `stage3_other_metres.json`. Committed logs: `songs/p62/spec52.run.txt`, `songs/p63/spec53.run.txt`.

- 790 the engine (windows, entries by stress, weighted placement, least breath scaled to the bar, again, copy, deaths, pick by charge).
- 791 the hymn mode; 792 its frame's unit is half a bar where the kept hymns stress the mid-bar beat; 793 a floor under a kept width of nothing.
- 794 the sketch `songs/p63/gen34h.py` read its bars a beat late (`n["on"] + ... + 12`): its pick's charge 0.007 is 0.403 on true bars.
- 795 density is printed, not charged (749.7 stands). 796 to stage 5: the bass by metre (749.6), descant (749.12), choral documents (749.13), and moving the 4/4 songs onto this engine.

For the session to check: rerun both commands and compare with the logs; try a new song's spec in 6/8 or 3/4; read `Hymn.options` against hymn practice.
