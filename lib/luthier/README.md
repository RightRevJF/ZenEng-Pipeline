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

## Stage 4 (Luthier v13): the chord writer — fixes 800–809

    python3 lib/luthier/chord_writer.py                                  # the held-out test -> stage4_results.json
    python3 lib/luthier/write_song.py songs/p62/spec52.json 1000 12      # song 52: twelve chord drafts, the melody engine on each, the pick (809)

- 800 `chord_writer.py`: structure from one kept section whole, bars from kept bars given the two before, one draw a section. It replaces `writers/chords.py`,
  which on held-out songs left the key in 1 bar in 100 (kept 14), looped verses 7 in 100 (kept 26) and stood 0.41 from the kept in moves (kept sets: 0.18).
  That test is `/home/claude/zeneng/corpus/v12/test_writer.py` (copied here as `test_prototype_writer.py`).
- 801 returns keep their chords; 802 joins; 803 a bar's chords on the metre's beats (also in `metre_engine.chord_at`); 804 `choose_key`; 805 `chromatic=` and `require=`.
- 806 answers 749.46: the code mark differed because `songs/p36/melody_p36.py` on the maintainer's machine had `alive` where the repository has `alive[:40]` in its
  own `__main__` pickle line. No engine reads it. The maintainer's copy is now the repository's.
- 807 `write_song.py`; 808 the clash rule (`"clash_rule": true` in a spec); 809 the pick among chord drafts by kept chord readings.

Not met: 802's test (joins 0.25 from the kept against 0.21 between kept sets). Not proved: minor keys, bridges, pre-choruses (too few held-out sections).
For the session: rerun both commands; try `Writer("minor")`; say whether `writers/chords.py` should now call this writer or be retired.

## Stage 5a (Luthier v14): a song from its lyric, nothing chosen by hand — fixes 810–820

    python3 lib/luthier/song_from_lyric.py songs/p64/lyric54.json 1000 12     # also songs/p65/lyric55.json (4/4), songs/p62/lyric52.json (6/8)

Writes `<lyric>.song.json` (chords, melody, bass, key, readings, checks, flags), `.song.mid` and the log `.song.txt`. Results: `stage5a_results.json`.

- 810 answers 749.47 (the floor only where the kept width is nothing); 811 answers 749.48 (two slurs a line, counted as slurs). Song 53's pick is now
  940f349cbf60, charge 0.109; order c8b56170c542. Song 52 from its hand spec: 1308 survivors, order f4334c0710a7, pick 1b646bd13932 (816 removed its three join deaths).
- 812 `tables/metre_atlas/4-4_pop_sung.json` (the 159 kept songs; made by `pop_table.py`, which needs the maintainer's corpus); a spec's `"table"` names it.
- 813 bass by metre (in `song_from_lyric.bass`); 814 registers on the tonic (settings); 815 checks; 816 the line before a copied or designed line gives way;
  817 a move given the move before; 818 `"borrow": {"rhythm": 0, "figure": 0.6}`; 819 words not in the lexicon; 820 the command above.
- The 4/4 judge's reading of the metre engine's builds (`judge_read_4_4.py`, needs the maintainer's judge data): song 55 median place 0.56 (old engine 0.32),
  song 54 0.87 (old 0.82).

Stage 5b, not done: chordal parts and drums by metre, harmony voices, descant, choral pages, edges, solos, perception checks.
For the session: rerun the three commands against the `.song.txt` logs; write song 58 with this command and say what a person still had to type.

## Stage 5b (Luthier v15): the band; the review of stage 4 taken in — fixes 821–832

    python3 lib/luthier/chord_writer.py && python3 lib/luthier/write_song.py songs/p62/spec52.json 1000 12 && python3 lib/luthier/stage4_extras.py   # stage4_results.json, whole (824)
    python3 lib/luthier/song_from_lyric.py songs/p64/lyric54.json 1000 12        # now with the band: parts, levels, band checks, a five-track MIDI

- 821 answers 749.52 (`name`, `tonic_name`); 822 answers 749.50 (the last chord drawn first; the song's last sung section as kept songs end);
  823 answers 749.51 (a song draws its own share from outside the key; `CHROMATIC_MAP`); 824 answers 749.49 (`stage4_extras.py`).
- 825-832 `band.py`: edges, levels, drums, the chordal part, the harmony voice, the break, checks, and (in metre_engine) a line's last note leaves the least breath.
  A lyric file may set `"genre"` (default pop). Results: `stage5b_results.json`.
- These change every record since stage 4: song 52 from its lyric, songs 54 and 55, and the written-chords draft are all new; song 52 and 53 from their hand specs keep
  their picks (1b646bd13932, 940f349cbf60).

Not done: the solo writer (the break plays the verse's tune), drums by kept table outside 4/4, the band by genre, the descant (749.12), choral pages (749.13), roughness.
For the session: rerun; run `Writer("minor")` again on your forty songs; say whether the harmony voice and the break read right in song 58.

## Stage 5c (Luthier v16): what could be mended now — fixes 833–837

Same command as stage 5b. Results: `stage5c_results.json`.

- 833 the clash rule under every chord for a note a beat long or more (`metre_engine.pitches`, `again`; spec flag `clash_rule`).
- 834 a stressed opening may sing its kept window early, the class drawn first (spec flag `early_entries`).
- 835 the harmony voice's fitted weights (`band.HW`, `HOLD`, `WITH`, `STAY`); the check now reads kept shares over the six classes written, and counts parallel motion by class.
- 836 roughness as a reading (`band.checks`). 837 joins meet 802's test since 822.
- Songs 52 and 53 from their hand specs are unchanged (the two flags are off there).

## Stage 6a (Luthier v17): the song's plan, from kept songs — fixes 838–843

Same command. Results: `stage6a_results.json`; kept figures: `tables/register_plan.json` (made by `kept_plan.py`, which needs the maintainer's corpus).

- 838 the chorus's lift drawn from the kept songs' own (median 1 semitone; 46 in 100 have none), registers from the kept medians, a gate `{"type": "plan lift"}`.
  The old design "the chorus above the verse" is retired (749.34, 749.44).
- 839 (749.8) `vary_returns`: a section whose every line is copied lifts one held note a line. 840 `hooks`: the title's lines pulled to the beat.
- 841 rest share: no rule (the engine rests less than kept songs; 749.38 answered). 842 the break only inside the kept lengths. 843 the plan's readings in `checks`.
- Songs 52 and 53 from their hand specs are unchanged.

## After the review of 5b and 5c: fixes 844, 845 (to be written into Luthier v18 with stage 6b)

- 844 answers 749.53. A line's last note is an eighth at least and a quarter's rest follows it, in every metre (`self.END`, `self.REST`; kept line endings in
  `tables/kept_line_endings.json`: 5,837 endings, length 5th percentile an eighth, median a quarter; rest 10th percentile a quarter). The next line's floor is
  read from that. Songs 54, 55 and 52 from their lyrics: no line-final note under an eighth, no rest under a quarter, no sung phrase over eight seconds
  (song 52: median 3.7 s, longest 4.8 s; 409 of 1,000 builds survive, up from 157).
  This moves the breath in 6/8 and 3/4 from 12 to 18 twelfths, so song 52 from its hand spec is new: 2506 survivors, order d609db9d0ac1, pick 36cf66ee1827, 2.135.
  Song 53 (hymn mode) is unchanged.
- 845 answers 749.54. `spec52.written_chords.json`, its log and `stage4_results.json` are made again under the current engine; the stage 5a-6a song records too.
- Not changed: 822 in major on your 100 songs (54 against the kept 41). Noted; it is inside ten points on mine (45) and I will look at the draw of added bars in 6b.
