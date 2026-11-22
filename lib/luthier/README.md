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

## Stage 6b (Luthier v18): the notes a style sings — fixes 844–851

Same command. Results: `stage6b_results.json`.

- 844, 845: see the section above (749.53, 749.54).
- 846 degrees of the scale by family and section (`spec["degrees"]`, from `studies/genre/genre_results.json`; `DEGREE_POWER = 0.5`); a song draws whether it sings
  blue notes (flat third, flat seventh), which are free of the clash rules. Major keys only.
- 847 `spec["word_pitch"]`: the stressed syllable of a word higher, level, lower (weights 3.0, 2.0, 0.2; kept 44 / 36 / 20).
- 848 `melismas()` after the pick: the song's share drawn from the kept quartiles; word-final syllables on notes a quarter long or more; the second note a scale step below.
- 849 readings in `checks`; 850 a gate `{"type": "hook beat"}`; 851 `again()` keeps a held note in its register without a clash.
- Not met and said so in Window 175: melismas at a line's end (55 to 64 in 100 against the kept 20 in the 4/4 songs); the word weight on song 52.
- Not done: 749.37, 749.12 (descant) and four-part hymns, 749.13.

## Stage 6c (Luthier v19): four parts and a descant — fixes 852–857

    python3 lib/luthier/metre_engine.py songs/p63/spec53.json 3000 && python3 lib/luthier/hymn_parts.py songs/p63/spec53.json    # spec53.parts.json, .parts.mid, .parts.txt

- 852 four parts under the hymn tune as a shortest path (no draw): ranges, order, spacing, root and third sounding, no parallel perfect intervals, least movement,
  a credit for each voice's motion against the tune at the kept share (`LAM`, `MOVE`, `BIAS`, fitted on song 53).
- 853 a descant over the last section (749.12). 854 checks. 855 every voice on the tune's times (the first part of 749.13).
- 856 answers 749.56: 839 lifts only a note a quarter long or more as sung. 857 answers 749.55: the song records are made again with the committed code.
- The chords are still the spec's, one a bar. Results: `stage6c_results.json`.

## Stage 7 (Luthier v20): the judge — fixes 858–866

    python3 lib/luthier/luthier_judge7.py                                   # the gate's figures for each kept table
    python3 lib/luthier/song_from_lyric.py songs/p64/lyric54.json 1000 12   # the pick is now judge 7's; the record's "judge7" block says how it was made

- 858 `judge_bench.py` (needs the maintainer's corpus): A, kept songs damaged by known amounts; B, the kept songs' chart record. Predictions first: `stage7_PREDICTION.md`.
- 859 the old judge answers damage (90 in 100 at a tenth of the notes) and does not rank kept songs (weeks -0.01, peak 0.09). It stays as a gate.
- 860 `luthier_judge7.py`: the gate reads a build's readings together against the kept songs' own (`tables/metre_atlas/kept_readings.json`, made by `kept_rows.py`).
- 861 the pick comes from the builds that stand where kept songs stand (the kept middle half of distance), not nearest the centre. 862 the record prints readings that did not choose.
- 863 `Engine.directed`: low surprise (one-sided) and sure endings, ranked and averaged at equal weight; a shortlist of five. 864 two readings of how much comes back.
- 865 `stage7_new_readings.py`: four readings tried against the chart record; chord rarity held weakly (0.11 on 731 songs; 0.07 held out), the rest did not. Results `stage7_results.json`.
- The research report: `reports/Vectors for judging great songs.md`; notes in `research_notes/Vectors for judging great songs/`.
- Side effect: the two new readings are in every kept table's quartiles, so the old two-sided charge of songs 52 and 53 from their hand specs changes in size (song 52: 3.315; pick unchanged).
- 866 not built: a chord judge beyond 809, a kept pop corpus outside 4/4, lyric rules, a second channel for musicians, a reading of form.

## Way 2: the same order at every scale — fixes 867, 868 (to be written into Luthier v21)

`scaling.py`: detrended fluctuation analysis of a song's pitch series and of its onsets on a sixteenth grid. Study: `way2_scaling_study.py`, predictions `way2_PREDICTION.md`,
results `way2_results.json`, `way2_confounds.json`.

- Kept pop songs: pitch alpha 0.79 / 0.90 / 1.00 (shuffled 0.53); onsets 0.61 / 0.66 / 0.72 (shuffled 0.51). The engine's builds: pitch 0.72 (song 55), 0.82 (song 54);
  onsets 0.46 to 0.48, under a shuffled series.
- Shuffling a kept song's bars lowers its pitch alpha in 87 songs in 100: the reading of form the stage-7 gate lacked.
- Against the chart record: pitch alpha 0.17 with weeks (0.12 holding year and length), within chance on 131 songs.
- 867 both exponents join the readings and the 4/4 pop gate. 868 both join the directed readings, counted up to the kept median.

## Luthier v21: the same order at every scale; the fix list for v21 — fixes 867–878

Same commands. Results: `stage8_results.json` (four songs, the scaling study, the descant). Slower now: each build's scaling is read (about four minutes a song at 1,000 builds).

- 867, 868 scaling (see the section above). 876, 877 where the voice stays out (`one_bar_share`; turns in `plan()`; kept figures in `tables/kept_silences.json`,
  `tables/kept_long_silences.json`): press a kept song's silences over a bar down to a bar and its rhythm exponent falls from 0.66 to 0.53.
- 869 answers 749.63 (slots); 870 answers 749.58 (`kept_rests`); 871 answers 749.64 (weak endings); 872-874 answer 749.60-749.62 (the pick: the old charge's least half,
  then the joint gate, then the first build in the order built; directed readings printed only); 875 answers 749.59 (melismas); 878 answers 749.57 (`sung_shifts`, `descant_shift`).
- Every committed record is new (four lyric songs, spec52 run and written chords, spec53 spec and parts, stage4_results.json). Song 53's tune pick is unchanged.
- Not met: rhythm exponent under the kept middle half on songs 54 and 58; the descant's summit at note 24 of 34, not in the last quarter; song 52 has no build past the joint gate.

## Luthier v22 — way 3: the marriage of tune and words (fixes 879–884)

The reading (`word_weight.py`, `tables/kept_word_weight.json`): a syllable's WEIGHT (0 function word, 0.4 weak syllable, 1 stressed) against its note's
SALIENCE (length, place in the bar, height in its line). The FIT is their rank correlation over the song. Kept songs: 0.20 / 0.29 / 0.38 by quartile,
10th percentile 0.09; 89 in 100 beat the same song with each line's words dealt again over its notes. Against the chart record: 0.03 (weeks), 0.00 (peak).
So it gates and does not choose (858). Predictions written first: `way3_PREDICTION.md`; results: `stage9_results.json`.

    python3 lib/luthier/song_from_lyric.py songs/p68/lyric58.json 1000 12    # 4/4 songs now read the words' weights; the record's checks print the fit

- 879 a fresh line's places scored by where kept songs sing each weight (replaces the hand-set stress scores in 4/4). Alone: no gain.
- 880 the step between two words leans as kept songs lean (function word to stressed syllable: up 45, level 32, down 23). Alone: small gain, in height.
- 881 the words' gate: fit at least the kept 10th, after the old charge's gate and the joint gate. `judge7.words_gate` in the record.
- 882 a line sung again (712/772/818) chooses which source notes are split, dropped or led into by 879's table; each change costs `again_cost` (8),
  so a line of the same count keeps its tune. Nearly all the gain is here: builds' median fit 0.18 / 0.08 / 0.16 -> 0.28 / 0.24 / 0.35 (songs 55, 54, 58).
  The cost is repetition: song 58's builds' median place under the old 4/4 judge 0.83 -> 0.62.
- 883 the fit and its parts in the record's checks. 884 the reading itself.
- spec: `"word_weight": {"place": 1.5, "step": 1.5, "again_cost": 8.0, "gate": 0.092}`; `"fresh": false` or `"again": false` switches a part off (used for the trials).
- Not done: length is not married (the picks' fit by length is about nothing); no kept table outside 4/4 (song 52 and hymns unchanged, flagged);
  the pick is still the first build past the gates.

## Luthier v23 — repairs after way 3 (fixes 885–889)

    python3 lib/luthier/song_from_lyric.py songs/p65/lyric55.json 1000 12    # also p64/lyric54, p68/lyric58, p62/lyric52

- 885 `metre_engine.stress_score`: a term for the time each syllable has before the next, by the kept shares for its weight (`tables/kept_word_weight.json`,
  `length_share_by_tier`); spec `word_weight.length` (2.0). Builds' fit by length 0.09 / 0.04 / 0.16 -> 0.16 / 0.12 / 0.12 (kept 0.13).
- 886 `song_from_lyric.melismas`: the share at line ends drawn to the kept odds (2.9 to 1) applied to the song's line ends; an eighth-long note inside a line may take one.
  At line ends: 64 / 38 / 65 -> 36 / 30 / 32 in a hundred.
- 887 `metre_engine.build`: a line's last note takes a kept length for its syllable's weight (`last_note_length_share_by_tier`), among those leaving the quarter's rest;
  spec `word_weight.last_note`. Rest after a line 12 / 12 / 15 -> 18 / 24 / 33 twelfths (kept 15, 24, 48). The short rests of 749.58 were long last notes.
- 888 `song_from_lyric.plan`, `band.edges(q=0)`: a turn only while the song stays inside the kept 75th of lengths; a song past it takes the kept lower quartiles of
  bars in and out. Seconds 253 / 317 / 343 -> 240 / 298 / 326. Cost: the picks' rhythm exponent fell on songs 55 and 54 (0.60, 0.56 -> 0.49, 0.50).
- 889 `band.arrange`: the harmony voice's class weights fitted to the song (ten rounds at most); record `harmony_fit`. Fourths 0.35 / 0.23 / 0.16 / 0.26 -> 0.12 / 0.11 / 0.11 / 0.14.
- Results: `stage10_results.json`. Studies beside this version, nothing built: `studies/way4/`, `studies/way2_again/`.
- Not done: songs 54 and 58 still long (the lyrics); no kept tables of words outside 4/4; the pick is still the first build past the gates.

## Luthier v24 — the session's fix list for v23 answered (fixes 890–898)

    python3 lib/luthier/song_from_lyric.py songs/p68/lyric58.json 0          # 894: at intake, how long the lyric will run; writes nothing
    python3 lib/luthier/song_from_lyric.py songs/p68/lyric58.json 1000 12    # also p65/lyric55, p64/lyric54, p62/lyric52
    python3 lib/luthier/make_kept_word_weight.py                             # 895: needs the kept corpus (kept_corpus.py says where to fetch it); rewrites the table byte for byte
    python3 lib/luthier/make_kept_returns.py                                 # 896: tables/kept_returns.json

| Finding | Fix | What was done |
|---|---|---|
| 749.66 | 891 | `again()`: each stressed syllable a return would leave a sixteenth is charged (`word_weight.short_stress`, 4). Builds: 14/11/10 -> 7/6/4 in 100 |
| 749.67 | 896 | measured: kept returning lines of another count keep 0.57/0.68/0.81 of their source's rhythm, 0.63/0.79/0.89 of its pitches; engine 0.78/0.72/0.83. `again_cost` stays 8 |
| 749.68 | 897 | `judge7.gates_removed` in the record. In 4/4 only the old charge takes builds away; the gates are not moved (858) |
| 749.69 | 894 | one length, after the form is final; the flag says how many lines fewer or what tempo; `... lyric.json 0` at intake |
| 749.70 | 895 | `kept_corpus.py`, `cocopops_parse.py`, `make_kept_word_weight.py`, `make_kept_returns.py`, `tables/kept_songs_4-4_pop.json`. The stageN_results.json files are still records of runs |
| 749.71 | 890 | `weak_end()`: 871 for a word of any length |
| 749.72 | 898 | `judge7.pick_words_fit` is the fit as sung; `word_weight.py`'s docstring matches the table |
| 749.73 | 892 | `band.arrange`: a guitar voiced in its own kept register, off the seconds either side of the sung notes. Under sung notes 0/3/3 -> 97/66/92 in 100 |
| 749.74 | 893 | harmony voice E2 to A5; above the lead only where below has no room |
| 749.75 | none | not built: POP909's last chorus is no denser than the first (median 0, positive in 49 of 100). Module 9.12 against a kept figure: the writer's to settle |
| 749.58 | 887 (v23) | 4/4: rest after a line 24 twelfths in all three songs; song 52 still 12 |
| 749.61 | none | carried: no kept pop corpus in 6/8 |

Results: `stage11_results.json`. Regression line: `lyric52/54/55/58.song.json` changed by 890–893 and are committed.

## Luthier v25 — how a line ends; the session's fix list for v25 answered (fixes 899–903)

    python3 lib/luthier/make_kept_line_ends.py                               # tables/kept_line_ends.json (needs the kept corpus)
    python3 lib/luthier/song_from_lyric.py songs/p68/lyric58.json 1000 12    # also p65/lyric55, p64/lyric54, p62/lyric52

| Finding | Fix | What was done |
|---|---|---|
| 749.76, 749.80 | 899 | `tables/kept_line_ends.json`: by the last syllable's weight and the time to the next line, the counts of each held length (5,242 kept lyric lines, read by the transcribers' capitals). `metre_engine.build` draws the held length from it (spec `line_ends`); a line may begin a beat after the last line's last syllable began; a fresh line's distance from the line before is drawn from the kept. Replaces 887 in 4/4. Builds: silences per 100 beats 13.9/12.3/13.0 -> 9.7/9.1/10.2 (kept 7.0, 9.1, 11.1); lines that run on 0 -> 0.30/0.26/0.22 (kept 0.27); line-final lengths within ten points of the kept at both ends for every weight |
| 749.78 | 901 | **answered against the finding.** In 619 kept line ends on a word's weak syllable, the weak syllable outlasts the stressed one in 47 of 100, and the stressed one is under a quarter in 72. 871 and 890 are retired where the kept table stands (`weak_end` returns nothing) |
| 749.79 | 900 | `band.voicing`: two notes of the chord where no three clear the voice. Guitar under sung notes 1.0 / 1.0 / 1.0 (song 52 0.96). "Accompaniment above the sung note" is printed for a piano only |
| 749.77 | none | not raised: read on syllables (the record's new check), song 54's pick 17/124 against a kept 0.12 inside lines; builds 0.06 to 0.08. The other lines' 0.05 is under the kept rate |
| 749.81 | 902 | each flag once. Only the whole fit is gated, not its parts (said in the paper) |
| 749.75 | 903 | the record prints Module 9.12 as kept songs meet it: the last chorus with its tag at least as long as the first. Songs 55, 54, 58: 20/16, 16/12, 16/14 bars. Nothing built |
| 749.61 | none | carried |

Results: `stage12_results.json`. The four `lyricNN.song.json` records changed and are committed. Not met: long distances between lines still short of the kept (a two-bar slot);
rest share under the kept middle half in the picks of songs 55 and 54; a fifth of song 54's strums are two notes.

## Luthier v26 — the kept corpus read whole (fixes 904–906)

The session's 749.82: `cocopops_parse.recip_dur` dropped every sung note that begins a tie (7,833 of them) and kept the tie's end in its place, so kept songs were read
squarer than they are. Mended (904), and every kept 4/4 table with a maker rebuilt (905):

    python3 lib/luthier/cocopops_parse.py corpora/CoCoPops/Billboard/Data    # corpora/cocopops_notes.csv.gz, tie starts read
    python3 lib/luthier/make_kept_4_4_tables.py      # tables/metre_atlas/4-4_pop_sung.json and the 4/4 rows of kept_readings.json (reproduces the old tables from the old parse in every field but `surprise_quartiles`, which differs in the third place: 749.87)
    python3 lib/luthier/make_kept_word_weight.py; python3 lib/luthier/make_kept_returns.py; python3 lib/luthier/make_kept_line_ends.py
    python3 lib/luthier/kept_plan.py                 # tables/register_plan.json (still on the maintainer's paths)

| Kept figure | Before | Tie starts read |
|---|---|---|
| onsets on the bar's first beat, share of all | 0.177 | 0.128 |
| onsets on the beat, by song (quartiles) | 0.43, 0.53, 0.59 | 0.38, 0.45, 0.53 |
| notes slurred to a syllable | 0.204 | 0.124 |
| the words' fit: 10th, quartiles | 0.092; 0.202, 0.291, 0.384 | 0.152; 0.248, 0.318, 0.402 |
| line-final function word held a half note or more | 0.353 | 0.18 |
| rest share inside sung sections (quartiles) | 0.21, 0.30, 0.39 | 0.14, 0.23, 0.33 |

- A record now carries `kept_tables`: the fingerprints of the tables it read.
- 906 (749.83): the phrase check splits at half a beat and prints the share over 12 beats beside the kept 0.042.
- The fitted constants (place 1.5, step 1.5, length 2.0, again cost 8, short stress 4) were tried on the builds against the new figures and stand.
- **Not rebuilt (no maker):** ENTRY (771), the 731 and 840 thresholds, WORD_PITCH (847), ONE_BAR (876), the counts of long silences (877); the old 4/4 judge's data.
  The session's studies that parse the corpus themselves (ornament 848, slots 869, degrees 846, breath, silences) were not checked for ties here.
- Results: `stage13_results.json`. All four `lyricNN.song.json` records and six tables changed and are committed.
- Way 2 again on the mended parse: pitch scaling against weeks 0.17, peak 0.18 on 165 new songs (`studies/way2_again/way2_again_results_tie_starts_read.json`).

## Luthier v27 — the session's fix list for v27 answered; every kept rhythm (fixes 907–912)

    python3 lib/luthier/kept_plan.py                 # 910: tables/register_plan.json, now from the kept corpus inside the repo
    python3 lib/luthier/make_kept_4_4_tables.py      # 912: the table now also holds every kept two-bar rhythm and bar
    python3 lib/luthier/make_kept_line_ends.py       # 911: also the entries (771) and stressed syllables on a beat by song (731)
    python3 lib/luthier/make_kept_word_weight.py     # 911: also 847's figure, recounted

| Finding | Fix | What was done |
|---|---|---|
| 749.84 | 907 | the lift drawn from the kept lifts the voice has room for; `choose_key(centre=...)` puts the verse's median within three semitones of the voice's middle, the instrument's keys first. Songs 55, 54: half a semitone off; song 58 (lift 9, the room) 3.5 |
| 749.85 | 908 | the words' fit gates at the builds' median, whole and by length, the kept 10th the floor (as 874 does for the old charge). Picks' fit 0.243/0.187/0.162 -> 0.429/0.303/0.377; by length 0.288/0.093/-0.017 -> 0.336/0.218/0.191 |
| 749.86 | 910 | `kept_plan.py` reads `kept_corpus`; `kept6a.json` removed. The table is rebuilt on the kept list (138 songs) |
| 749.87 | none | the README names the field; the step that differs was not found |
| 749.88 | 909 | a phrase past eight beats ends in half a beat of rest at the least. Over 12 beats: 0.082/0.057/0.077 -> 0.019/0.074/0.036 (kept 0.042); song 54 still over |
| 749.89 | 911 | ENTRY (771) and the 731 floor read from `kept_line_ends.json`; 847 recounted (0.416/0.382/0.202) and stands; ONE_BAR 0.09; 877 kept |
| (the paper's own) | 912 | `two_bar_windows_all`, `bar_rhythms_all`: every kept rhythm, drawn at its kept count times its score, no cut to twelve (spec `all_windows`). Builds' onsets on the beat 0.53/0.49/0.54 -> 0.50/0.47/0.51 (kept median 0.45) |
| 749.61 | none | carried |

Results: `stage14_results.json`. Not met: the picks' stressed syllables on a beat (0.72, 0.58, 0.82) over the kept middle half (908 leans that way); rest share low on songs 55 and 54.

## Luthier v28 — the beat let go; the session's fix list for v28 answered (fixes 913–915)

| Finding | Fix | What was done |
|---|---|---|
| 749.90 | 913 | `WORD_PLACE` 0.75 (it was fitted at 1.5 when twelve rhythms were on offer; 912 put hundreds on offer). The words' gate holds a build to its song's median by length and by height; the whole fit only to the kept 10th. Picks' stressed syllables on a beat 0.72/0.58/0.82 -> 0.55/0.50/0.60 (kept 0.45, 0.54, 0.66); onsets on the beat 0.54/0.48/0.54 -> 0.45/0.45/0.45 (kept median 0.45) |
| 749.91 | 914 | `song_from_lyric.melisma_notes` is 848's draw as a function of the notes; `Engine.as_sung` gives it to the words' gate, which reads every build with its melismas placed (`words_gate.read`: "as sung") |
| 749.92 | 915 | a line whose phrase, with the whole next line, would pass twelve beats ends in half a beat of rest. Over 12 beats 0.041 / 0 / 0; longest 17.0 / 10.5 / 10.0 (song 55 keeps one long line) |
| 749.61 | none | carried |

Results: `stage15_results.json`. The three 4/4 picks stand in the kept middle half on stressed syllables on a beat, onsets on the beat, the fit whole and by place and height, rest share, and the verse's place in the voice.
Not met: the rhythm exponent (0.54, 0.53, 0.51 against 0.61 to 0.72); song 55's fit by length (0.387) and longest phrase; songs 54 and 58 long.

## Luthier v29 — sound, by a stated rule (fixes 916–917)

    python3 studies/soundness/soundness.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json    # 917: after every version

The session's standard (`studies/soundness/SOUNDNESS.md`): 23 checks read alike on the 160 kept songs and the three 4/4 records. **Sound** = no check with all three songs beyond
the kept 10th or 90th on one side, and no more than two with all three beyond the kept 25th or 75th. Three kept songs drawn at random fail it 6.8 times in 100.

- 916 (749.93): the turns of 877 stay whatever the length, at two bars where the song would pass the kept 75th of lengths; the bars in and out are read again once the turns are in (888) and give way first.
  Rhythm scaling 0.546 / 0.547 / 0.532 -> 0.539 / 0.577 / 0.524 (kept 10th 0.574).
- **The engine is sound by the rule, narrowly**: one song is over the bound by three thousandths; rhythm scaling (low) and pitch scaling (high) are the two leans the rule allows.
- 749.94 (the songs sit nearer the kept middle than kept songs do: 9, 4, 6 checks outside the middle half against a kept 8, 10, 13) is an improvement, not mended here.
- From here a finding made while the rule holds is an improvement, not a fault. Results: `stage16_results.json`.

## Luthier v30 — sound on the pools (fixes 918–921)

    PYTHONHASHSEED=0 python3 studies/soundness/neighbour.py songs/p65/lyric55.json songs/p64/lyric54.json songs/p68/lyric58.json   # 921: the pools, after every version (about 15 minutes)
    python3 studies/soundness/soundness.py songs/p65/lyric55.song.json songs/p64/lyric54.song.json songs/p68/lyric58.song.json     # the three picks

v29's pass by 0.003 did not hold (the session's `margin.py`): the rule is now read on the pools too. **Sound** = the three picks pass, and a pick drawn at random from each song's gated pool passes at least 90 times in 100 (three kept songs: 93).

| Item | Fix | What was done |
|---|---|---|
| 749.95 | 918 | turns at the kept split (two bars 62, four bars 38) whatever the length, one of four bars at the least |
| 749.97 | 919 | `melisma_notes(how=...)`: a copied line takes its source's melismas; `FIGURE_BORROW` 0.8 |
| 749.94 | 920 | `spec["target"]`: one kept song drawn from the title's seed; its repeated-note, step and leap shares tilt the moves and centre the old charge's bounds for those readings; its range moves the tops. `AIM_REPEATS` (the share of lines sung again by the kept song's repetition) was tried and is off: it lowered rhythm scaling until the first picks leaned |
| 749.96 | 921 | adopted; `studies/soundness/neighbour_v30.json` is this version's pool reading (and two trial readings beside it) |

Pools: pass 93 in 100; a random pick outside the kept middle half on 19 song-checks (16 before the aim; three kept songs about 30; the check asks 21, not met).
Picks: sound; rhythm scaling 0.576 / 0.574 / 0.572, on the bound again, with the pools saying the engine does not lean past it (2 draws in 100).
Results: `stage17_results.json`.

## Luthier v31 — the page gate, a floor (fixes 922–923)

    python3 lib/luthier/make_kept_page_gate.py        # tables/kept_page_gate.json from the kept 4/4 tunes (needs the kept corpus: see kept_corpus.py)

Not an answer to a fix list. It comes from a day of studies on what makes a song last (`studies/`, each with its rule written first; summary in `studies/gates_strengthened/RESULT.md`).
Among songs that are already hits nothing on the written tune ranks them. Where the forgotten are counted (23,205 session tunes, 10,360 hymn tunes, and inside one artist's charted and uncharted songs) plainer, more foreseeable tunes are the ones kept. So it enters as a floor, not an aim.

| Fix | What was done |
|---|---|
| 922 | `page_gate.py`: surprise (bits per interval from the three before, under the kept tunes' counts), six- and five-note share, time on the tonic, different pitches and intervals, leaps, range, repeated notes, four-interval figures already sung; their mean, each against the kept mean and spread and turned the plain way, is a build's plainness. `Engine.run`: a build past the words' gate under the kept 10th percentile is passed over (waived if none is left). `judge7["page_gate"]`, `gates_passed["page_floor"]`, and the style checks carry the readings. 4/4 only. |
| 923 | `FIGURE_MEMORY = 8.0`: when a fresh line's notes are drawn, a note that completes a four-interval figure the song has already sung is favoured eightfold (`Engine._figs`). Tried at 1, 4, 8, 16. |

Picks: four-interval figures already sung 0.492 / 0.557 / 0.503 (0.385 / 0.465 / 0.465 before; kept quartiles 0.470, 0.560, 0.676). Sound on the picks and on the pools (99 draws in 100; `studies/soundness/neighbour_v31.json`).
Not met: song 55 still under the kept lower quartile on its builds; the opening 120 notes of each song; and the songs moved a little toward the kept middle (a random pool pick outside the middle half on 15 song-checks, 17 before).
Results: `stage18_results.json`. For review: is a floor the right use of a gate that grades nothing among hits (922)? Does the figure memory pull the songs toward the middle more than it is worth (923, against 749.94)?

## Luthier v32 (Window 189): the aimed song's own shape

Answers the session's list 749.98 to 749.104. Paper: `reports/Luthier_v32.docx` (builder `reports/make_luthier_v32_from_v31.py`), row v203, Module 27.113, Table GY. Results: `lib/luthier/stage19_results.json`, `studies/soundness/neighbour_v32.json`.

- 924 (749.102): the page floor reads each build as sung (`read_as` in the record).
- 925 (749.98): the plan's chorus lift is the aimed kept song's (`lifts` and `song_names` added to `tables/metre_atlas/kept_readings.json`; rows unchanged; 4-4_pop_sung.json byte for byte).
- 926 (749.99): one pitch repeats as long as the aimed song's longest run (3 to 10; `RUN_TOP`), counted across lines; a new gate tests the whole build as sung. Songs with no aim keep the old cap.
- 927 (749.100): tops set to the aimed song's range plus `RANGE_OVER` (1); centres follow at `CENTRE_FOLLOWS` (0.5); `MOVE_STEP` 1.2, `MOVE_LEAP` 1.6, `REG_SPREAD` 50 scaled by the aimed range.
- Study, not built (749.104): `studies/repeated_figures/` (where.py, pool.py, RESULT.md). Songs 55 and 54 repeat figures from far back (whole sections); the near answer within a bar or two is missing.
- Carried: 749.103 (two-sided variety 1.18 against kept 10.5; the rhythm checks do not yet follow the aimed song), 749.104's fix, 749.101, 749.61.
- Picks sound: 4, 4, 8 checks of 23 outside the kept middle half; the neighbour choice fails the rule 1.0 in 100 (1.3 before); a random pick from the engine's pool, 4.6 in 100 (label corrected in v36, 749.117).

Next: Luthier v33 (row v204), Window 190, Module 27.114 (anchor "27.113"), tables GZ…, fixes from 928.

## Luthier v33 (Window 190): a fault mended, and the run tested where it is made

Answers the session's list 749.105 to 749.109. Paper: `reports/Luthier_v33.docx` (builder `reports/make_luthier_v33_from_v32.py`), row v204, Module 27.114, Table GZ. Results: `lib/luthier/stage20_results.json`, `studies/soundness/neighbour_v33.json`, `studies/review19/aimpool.json` and `runs_v33.json` (rerun), `studies/v33_trials/`.

- 928 (749.105): the run cap is each engine's own (`self.RUN`, passed to `runs_ok(ps, cap)`; three by default). Song 53 builds again; `spec53.run.json` and `spec53.parts.json` byte for byte.
- 929 (749.106): `Engine.carry`, `line_ok`, `join`: the run carried in plus the line, tested on every path (fresh, copy, again, 818 borrow). A returning line that fails moves its first note a scale step. `melisma_notes(..., cap=)`: the step above, or not placed. Whole-build gate kept as a backstop: 0 deaths in each song (342, 647, 278 before).
- 930 (749.108): `MOVE_FIT = (80, 6)`: step and leap weights fitted per song on trial builds, read as sung; rounds in the record (`target.moves_fit`). Builds' steps 0.429, 0.552, 0.426 against aims 0.452, 0.595, 0.398; leaps on their aims.
- Tried, not adopted (749.109): `AIM_REPEATS = True` moved repeated bars by 0.03 and the neighbour choice failed the rule 7 in 100. See `studies/v33_trials/README.md`.
- Picks sound: 4, 7, 9 of 23 outside the kept middle half; the neighbour choice fails 0.3 in 100 (1.0 before); a random pick from the engine's pool, 2.6 in 100 (4.6 before) (label corrected in v36, 749.117).
- Carried: 749.109, 749.104's fix (now the one thing 749.104, 749.109 and 749.101 wait on), 749.103, 749.61, and the small thing (one record, two readings of repeated figures).

Next: Luthier v34 (row v205), Window 191, Module 27.115 (anchor "27.114"), tables HA…, fixes from 931.

## Luthier v34 (Window 191): the melismas from the aimed song; the fit bounded by the fresh lines

Answers the session's list 749.110 to 749.112. Paper: `reports/Luthier_v34.docx` (builder `reports/make_luthier_v34_from_v33.py`), row v205, Module 27.115, Table HA. Results: `lib/luthier/stage21_results.json`, `studies/soundness/neighbour_v34.json`, `studies/review19/aimpool.json` (rerun), `studies/plant_the_peak/`.

- 931 (749.112): `E.stats` cleared after the fit; `target.moves_fit.trial_builds` counts the fit's builds.
- 932 (749.110): `melismas` added to `tables/metre_atlas/kept_readings.json` (rows unchanged); `target.melisma_share` is the aimed song's, inside the kept 10th to 90th; `melisma_notes(..., share=)`. The fit reads the fresh lines' step and leap shares each round, holds a weight where they would leave the kept 10th to 90th, and keeps the best round inside (`target.moves_fit_kept_round`).
- 933: every build's repeated figures read as sung (`page_gate.every_build_read_as`).
- Tried outside the engine, not built (749.111): `studies/plant_the_peak/` (PREDICTION.md, trial.py, RESULT.md).
- Picks sound: 7, 7, 5 of 23 outside the kept middle half; the neighbour choice fails 0.5 in 100 (0.3 before); a random pick from the engine's pool, 2.5 in 100 (2.6 before) (label corrected in v36, 749.117); two-sided variety 1.82 (1.46 before).
- Finding: with the aimed song's melismas, song 58's builds' bars on a figure already sung rose 0.29 to 0.47 and song 54's 0.40 to 0.46; song 55's (more melismas) fell 0.40 to 0.31. A returning line does not get its melismas in the same places.
- Carried: 749.111 (place the peak note directly next time), 749.104's fix with the melismas carried, 749.109, 749.103, 749.101, 749.61.

Next: Luthier v35 (row v206), Window 192, Module 27.116 (anchor "27.115"), tables HB…, fixes from 934.

## Luthier v35 (Window 192): the hold-out

Song 59 (`songs/p69`) is the hold-out: read after every fix, never fitted to. Answers the session's list 749.113 to 749.116. Paper: `reports/Luthier_v35.docx` (builder `reports/make_luthier_v35_from_v34.py`), row v206, Module 27.116, Table HB. Results: `lib/luthier/stage22_results.json`, `studies/soundness/neighbour_v35.json`, `studies/review19/aimpool.json` and `studies/holdout59/` (rerun), `studies/v35_traces/`, `studies/plant_the_peak/` (second trial).

- 934 (749.115): `MOVE_FIT = (40, 6, 400)`: a round draws until 40 builds pass the gates, 400 tries at most; tries recorded.
- 935 (749.114): a line gives way to a short line (one bar or less) that stands before a copied or designed line coming in early. Song 59's rhythm deaths 500 to 52 in 1,000. The trace found one line at fault, not the long verse lines.
- 936 (749.113): a repeat weight (`target.moves.repeat`, `Engine.MV[3]`) fitted with the step and leap weights; a round outside the kept band is followed by one halfway back. Builds' repeated notes 0.222, 0.215, 0.382, 0.225 against aims 0.158, 0.110, 0.373, 0.210.
- Tried outside the engine again, not built (749.111): `studies/plant_the_peak/RESULT2.md`. Helps wide aims, harms narrow.
- Picks sound; the neighbour choice fails 2.5 in 100 (0.5 before); a random pick from the engine's pool, 2.6 in 100 (2.5 before) (label corrected in v36, 749.117). Song 59 stands outside the kept middle half on 2 checks of 21 (3 before): still too central.
- Carried: 749.116 (band arrangement under the break), 749.111, 749.104's fix, 749.109, 749.103, 749.101, 749.61.

Next: Luthier v36 (row v207), Window 193, Module 27.117 (anchor "27.116"), tables HC…, fixes from 937.

## Luthier v36 (Window 193): two pool figures, rightly named

Answers the session's list 749.117 to 749.119. Paper: `reports/Luthier_v36.docx` (builder `reports/make_luthier_v36_from_v35.py`), row v207, Module 27.117, Table HC. Results: `lib/luthier/stage23_results.json`, `studies/soundness/neighbour_v36.json`, `studies/review19/aimpool.json` and `studies/holdout59/` (rerun), `studies/v36_trials/`.

- 937 (749.117): both pool figures under their own names (the neighbour choice; a random pick from the engine's pool). Windows 189 to 192 and their rows corrected in the paper; the v32 to v35 entries above corrected.
- 938 (749.119): 935 no longer asks for an aim; its stat is renamed (a limit set). It changes no build of songs 55, 54, 58 (`studies/v36_trials/cmp935.py`).
- 939 (749.118): `Engine.MOVE_ON` and the lead-in's level share scaled by the repeat weight in `again()`; the fit is a bisection between the last round inside the kept band and the nearest outside.
- Picks sound, no lean. The neighbour choice fails 1.3 in 100 (2.5 before); a random pick from the engine's pool 5.1 (2.6 before).
- Not met: 939's check (returning lines still repeat 0.10 and 0.05 over fresh lines in songs 55 and 54); 938's check on the random pool pick (5.1 against 2.5).
- Hold-out song 59: 3 checks of 21 outside the kept middle half (2 before); range 19 against 24.
- Carried: 749.116, 749.111 (third trial not run: needs a second practice song with a wide aim), 749.104's fix, 749.109, 749.103, 749.101, 749.61.

Next: Luthier v37 (row v208), Window 194, Module 27.118 (anchor "27.117"), tables HD…, fixes from 940.

## Luthier v37 (Window 194): the bar fit, tried and not built; the melismas carried

Answers the session's list 749.120 to 749.122 and takes 749.104 head on. Paper: `reports/Luthier_v37.docx` (builder `reports/make_luthier_v37_from_v36.py`), row v208, Module 27.118, Table HD. Results: `lib/luthier/stage24_results.json`, `studies/soundness/neighbour_v37.json`, `studies/review19/aimpool.json` and `studies/holdout59/` (rerun), `studies/bar_fit/`.

- 940 (749.120): `studies/soundness/neighbour.py` writes `ranges_90` (each pool resampled 200 times). The neighbour choice fails 1.5 in 100 (0.0 to 3.5); a random pick from the engine's pool 3.2 (1.2 to 6.1); from every living build 14.4 (11.3 to 16.1).
- 941 (749.121): each weight tested against its own band and bisected on its own; `FIT_EDGE = 0.03`. Song 54 keeps round 5; its builds' repeated notes 0.191 (kept 25th 0.210).
- 942 (749.104, second half): a line sung again takes its source's melismas (`melisma_notes`, `"copy"` or `"again"`). Song 52's record changes for this (28 melismas where it had 32; same pick, same notes before melismas).
- Tried outside the engine, not built (749.104 first half, with 749.122): the bar fit, `studies/bar_fit/RESULT.md`. Bars return (rhythm up 0.04 to 0.08) and the words' fit falls under the kept 10th in every song. The bars and the words trade; the next question is on the lyric's side.
- Picks sound, no lean. Hold-out song 59: 5 checks of 21 outside the kept middle half (3 before).
- Carried: 749.104 first half (as a lyric question), 749.109, 749.111 (needs a second wide-aim practice song), 749.116, 749.103 (read as the outcome), 749.101, 749.61.

Next: Luthier v38 (row v209), Window 195, Module 27.119 (anchor "27.118"), tables HE…, fixes from 943.

## Luthier v38 (Window 195): there was no fault of repetition

A window of measuring, done without a list. **No change to how songs are built; every record is v37's, byte for byte.** Paper: `reports/Luthier_v38.docx` (builder `reports/make_luthier_v38_from_v37.py`), row v209, Module 27.119, Table HE. Studies: `studies/verse_match/` (RESULT.md), `studies/bar_fit/` (PREDICTION3.md, trial3).

- The bar fit where the words allow: third trial, not built. Strict, the bars do not rise; with leave, the words' fit falls to 0.05 to 0.10.
- The lyric is not the fault (`match.py`): later verses match the first verse bar for bar as well as kept songs' do.
- The songs do not repeat too little (`near.py`): bars on a rhythm sung before 0.42, 0.56, 0.63, 0.48 against kept quartiles 0.45, 0.59, 0.69. The shortfall since v32 was against each song's own aimed song.
- 943 (749.109), the borrows fitted to the aimed song: passed its trial outside the engine on the second try and held on the hold-out; built in; **withdrawn**. In the engine the neighbour choice failed the rule 10.2 in 100 (4.0 to 18.5; v37 1.5, 0.0 to 3.5). More borrowing lowers rhythm scaling. `BORROW_FIT = None` (off); `BORROW_GRID`, `BORROW_WORDS` kept.
- Next study: how kept songs that repeat much keep a high rhythm scaling.

Next: Luthier v39 (row v210), Window 196, Module 27.120 (anchor "27.119"), tables HF…, fixes from 944.

## Luthier v39 (Window 196): the shape from the song

**No kept song is drawn any more.** Jason's ruling: other songs are a style guide, not a model; the engine decides from its theory; the writer may override. Paper: `reports/Luthier_v39.docx` (builder `reports/make_luthier_v39_from_v38.py`), row v210, Module 27.120, Table HF. Studies: `studies/words_to_shape/` (do the words decide the shape?), `studies/shape_from_the_song/` (the theory tested; the rule for adopting; RESULT.md).

- 944: `SHAPE_FROM = "the song"` in `song_from_lyric.py`. Range from the song's words (`lib/luthier/words_to_shape.py`, `tables/kept_words_to_shape.json`, made by `make_kept_words_to_shape.py`); movement at the kept middle; `"movement": "smooth" | "leaping" | "chant"` in the lyric file overrides; lift at the kept middle. `target.kept_song` is None; `target.from_its_words`, `target.words`, `target.movement` are new.
- Study: words predict bars sung again (+0.53, +0.46) and range (+0.44) on held-out songs; not movement.
- The paper's "verses step, choruses leap" does not hold in kept songs (44 in 100 each); struck.
- Picks sound. Neighbour choice 1.5 in 100 (0.5 to 5.5). Random pool pick 7.8 (4.1 to 11.4): worse than v37's 3.2 (1.2 to 6.1), inside the standard's bar. Cause: rhythm scaling low in every song.
- Repetition from the words (`BORROW_FIT_SONG`): tried, breaks the pools, off.
- The session's `aimpool.py` and `aimpool59.py` read a drawn kept song and no longer apply; `studies/shape_from_the_song/own.py` reads each song against its own asking.
- Song 60 under v39: `songs/p70/lyric60.v39.song.json` (the delivered record is untouched).
- Not answered here: the session's list for v39 (749.123 to 749.127).

Next: Luthier v40 (row v211), Window 197, Module 27.121 (anchor "27.120"), tables HG…, fixes from 945.

## Luthier v40 (Window 197): the lyric's room

No song and no record changes. Paper: `reports/Luthier_v40.docx` (builder `reports/make_luthier_v40_from_v39.py`), row v211, Module 27.121, Table HG. Studies: `studies/rhythm_memory/` (what carries rhythm scaling), `studies/lyric_room/` (the check's rule and result).

- Study: rhythm scaling is carried by slow change in how busy the singing is (+0.68) and by bars with nothing sung (+0.58); not by near or far repeats. Songs 55, 54, 58 sing at one busyness and rest little; songs 59 and 60 do not, and their rhythm scaling is in the kept middle.
- 945: **run when a lyric is locked, with the mouth tests, before any music:**

      python3 lib/luthier/lyric_room.py songs/pNN/lyricNN.json

  About two minutes. Writes `lyricNN.room.json`; prints room, contrast, rhythm scaling against the kept songs, and in plain words what in the lyric is behind a low reading. It advises; it does not refuse a lyric. Table: `tables/kept_rhythm_room.json` (`make_kept_rhythm_room.py`).
- Next trial (the engine's side): sections that differ in how busy they are; bars of rest between sections.

Next: Luthier v41 (row v212), Window 198, Module 27.122 (anchor "27.121"), tables HH…, fixes from 946.

## Luthier v41 (Window 198): the words measured one way

Answers the session's review of v39 (749.128, 749.129, 749.126, 749.124; 749.130 was answered in v40). Paper: `reports/Luthier_v41.docx` (builder `reports/make_luthier_v41_from_v40.py`), row v212, Module 27.122, Table HH. Results: `studies/shape_from_the_song/own.json` (v39's is `own_v39.json`), `studies/soundness/neighbour_v41.json`.

- 946 (749.128): `words_to_shape.kept_lines` ties each kept word to its notes; `tables/kept_words_to_shape.json` refitted; study rerun (`studies/words_to_shape/result.json`; first run `result_v39.json`). Asks now: range 18.0, 18.8, 19.9, 18.8; bars on a figure already sung 0.42, 0.39, 0.41, 0.45. The builds already sing their bars again about as often as their words ask.
- 947 (749.129): repeated notes at the genre family's middle (`repeated_notes_by_family` in the table; `studies/movement_by_family`). Steps and leaps do not differ by family.
- 948 (749.126): a line its own copy follows leaves the copy room. Song 60: join deaths 791 to 0; survivors 84 to 367 (`songs/p70/lyric60.v41.song.json`; the delivered record is untouched).
- 949 (749.124): `neighbour.py` ranges on 1,000 inner draws.
- Picks sound, no lean. Neighbour choice 3.0 in 100 (1.3 to 5.6); random pool pick 8.2 (3.7 to 11.4).
- Unmet: range. The words ask 18 to 20 semitones; the builds span 14 or 15. Next: plant the peak (749.111), rule first.

Next: Luthier v42 (row v213), Window 199, Module 27.123 (anchor "27.122"), tables HI…, fixes from 950.

## Luthier v42 (Window 199): the range the words ask

Mends the range (749.111) and answers Review 26 (749.131 to 749.134). Paper: `reports/Luthier_v42.docx` (builder `reports/make_luthier_v42_from_v41.py`), row v213, Module 27.123, Table HI. Results: `studies/plant_the_peak` (RESULT3 to RESULT6), `studies/choose_the_range`, `studies/commonest_pitch`, `studies/soundness/neighbour_v42.json`, `studies/shape_from_the_song/own.json`.

- 950 (749.111): the peak planted as a note. Each fresh chorus line in turn keeps its centre, has its top set to the peak (floor plus the asked range), and is redrawn (60 tries) until its highest stressed note is the peak; the first to reach it carries it (`Engine.pitches` wraps `pitches1`; `target.peak`; `PLANT_PEAK`). Three earlier forms failed: a line drawn in a raised register lifts the chorus's median and dies at 838. Builds' middle range 14, 15, 15, 15 to 17, 15, 17, 17 (songs 55, 54, 58, 59).
- 951: among the builds past every gate, the pick is the first whose range is within 2 semitones of the asking; else the nearest (`target.choose_range`; `CHOOSE_RANGE`; the record's `judge7.range_choice`). Chosen tunes: 17, 17, 19, 19, 19 (songs 55, 54, 58, 60, 59); 872 alone gave 17, 14, 11, 19, 19. Cost: song 54's words' fit 0.282 to 0.163 (kept floor 0.152).
- 952 (749.131, 749.133): `make_kept_words_to_shape.py` writes the family middles of repeated notes with bootstrap ranges and a shrunk middle (soul 0.207 to 0.232, country 0.335 to 0.329, others 0.319); the engine stops where a family is missing. Only song 60's asking moves.
- 953 (749.132): `lyric_room.py` stamps each room file with hashes of the engine's code and the kept tables; `python3 lib/luthier/lyric_room.py --check` lists stale files. All five room files reread.
- 749.134 studied, not mended: the commonest pitch's share is over the kept 90th (verse 0.44, chorus 0.474) in two chosen tunes of four, in verses (54: 0.53; 58: 0.50) and in choruses (55: 0.476; 58: 0.50). A floor is proposed, to be tried against the pool standard first.
- Picks sound; one lean past the quartiles (rhythm scaling, low). Neighbour choice 1.5 in 100 (0.1 to 2.9); random pool pick 2.7 (0.6 to 5.0). Songs 52 and 53 byte for byte as they were. Song 60 under this window: `songs/p70/lyric60.v42.song.json`.
- Unmet: song 54's builds no wider in the middle; fewer builds live (342, 309, 419, 376); why the pools grew sounder is untraced; rhythm scaling's engine side untried.

Next: Luthier v43 (row v214), Window 200, Module 27.124 (anchor "27.123"), tables HJ…, fixes from 954.

## Luthier v43 (Window 200): a floor and a ceiling

Answers Review 27 (749.135, 749.136, 749.137) and tries and builds the ceiling of 749.134. 749.138 (rhythm scaling in the engine) is not begun. Paper: `reports/Luthier_v43.docx` (builder `reports/make_luthier_v43_from_v42.py`), row v214, Module 27.124, Table HJ. Results: `studies/pitch_ceiling`, `studies/sounder_pools`, `studies/commonest_pitch/result.json`, `studies/soundness/neighbour_v43.json` (and `neighbour_v43_without_the_peak.json`).

- 954 (749.135; amends 951): the range a floor, not a band. The pick is the first build no narrower than the asking plus the kept 25th of range less the asking (-3.36; `range_less_the_asking_held_out` in `tables/kept_words_to_shape.json`, written by the maker from residuals held out by artist); 872 above it; the widest where none clears it. Record: `judge7.range_choice`.
- 955 (749.136): `python3 lib/luthier/song_from_lyric.py --check` reads every record's table stamps against the tables at hand (records named `.vNN.song.json` are not read). Run it and `lyric_room.py --check` in every window.
- 956 (749.134): a ceiling on the commonest pitch's share (`tables/kept_commonest_pitch.json`, maker `make_kept_commonest_pitch.py`; verse 0.44, chorus 0.474; a part told by its name). After the page gate a build over either is passed over; waived where none passes. `PITCH_CEILING`; record: `judge7.pitch_ceiling`, `judge7.pick_commonest_pitch`. Tried first (`studies/pitch_ceiling`): pools 47, 33, 72 to 39, 26, 39; pool standard held.
- 749.137: range does not explain the sounder pools (random pool pick 6.8 without the peak, 2.5 with; range left out 6.5, 2.3). Every failure is rhythm scaling under the kept 10th in all three songs. Gates or chance not separated (`studies/sounder_pools/RESULT.md`). `LUTHIER_PLANT_PEAK=0` is for that study only.
- Chosen tunes: range 17, 16, 19, 19, 19 and words' fit 0.278, 0.275, 0.307, 0.359, 0.32 (songs 55, 54, 58, 60, 59). Songs 55 and 58 changed tunes under the ceiling. Picks sound, one lean past the quartiles (rhythm scaling, low), 11 checks outside the middle half. Neighbour choice 2.5 in 100 (0.0 to 4.5); random pool pick 2.1 (0.1 to 5.5). Songs 52 and 53 byte for byte as they were. Song 60 under this window: `songs/p70/lyric60.v43.song.json`.
- Unmet: 749.138; song 54's builds no wider in the middle; smaller pools (38, 24, 39).

Next: Luthier v44 (row v215), Window 201, Module 27.125 (anchor "27.124"), tables HK…, fixes from 957.

## Luthier v44 (Window 201): the verse sung closer, tried

Answers Review 28 (749.139, 749.140, 749.141) and makes the first engine trial on rhythm scaling (749.138), which is one check short and not built. Paper: `reports/Luthier_v44.docx` (builder `reports/make_luthier_v44_from_v43.py`), row v215, Module 27.125, Table HK. Results: `studies/busy_sections`, `studies/sounder_pools` (RESULT2, `per_build.json`), `studies/weak_top_notes`, `studies/soundness/neighbour_v44.json` (and `_v44_without_the_peak`, `_v44_trial_verse_closer`, `_v44_trial_verse_closer_apart`).

- 957 (749.139): `make_kept_commonest_pitch.kind` tells a part by its exact name (a pre-chorus is neither verse nor chorus). Chorus ceiling 0.474 to 0.479; each ceiling printed with its range (verse 0.405 to 0.498; chorus 0.457 to 0.509). Song 55 takes back its tune of before the ceiling (range 17, words' fit 0.341); the others keep theirs.
- 749.140: read per build, the pools with and without the peak do not differ (46.6 and 51.5 in 100 under the kept 10th of rhythm scaling; as large in 49 shuffles in 100). The sounder pool figure of Windows 199 and 200 was song 55's small pool. `neighbour.py` now prints block `749.140` (per-build rhythm scaling, living builds, words' fit).
- 749.141: kept songs put 29 in 100 of top-note occurrences on weak syllables at the middle, 100 at the 90th; Luthier's 0 to 0.46. Not a fault by the rule; nothing built.
- 749.138, not built: `LUTHIER_VERSE_CLOSER=apart` (trial switch, off). Verse lines of 6 to 8 syllables given one bar, shortest first, none side by side, an even count, to the kept middle of notes a bar (4.59). Builds' rhythm scaling 0.592, 0.576, 0.555 to 0.678, 0.620, 0.592; builds 342, 309, 419 to 281, 304, 405; pools fail the rule 0.0 in 100; pool builds under the kept 25th 88 to 42 in 100. Misses one check written first: song 54's words' fit 0.221 to 0.193 (0.02 allowed).
- Chosen tunes: range 17, 16, 19, 19, 19; words' fit 0.341, 0.275, 0.307, 0.359, 0.32 (songs 55, 54, 58, 60, 59). Sound, one lean (rhythm scaling, low). Neighbour choice 2.0 in 100; random pool pick 2.2. Songs 52 and 53 byte for byte as they were. Song 60 under this window: `songs/p70/lyric60.v44.song.json`.

Next: Luthier v45 (row v216), Window 202, Module 27.126 (anchor "27.125"), tables HL…, fixes from 958.

## Luthier v45 (Window 202): the verse sung closer, built

Answers Review 29: builds 749.142, makes the hold-out of 749.143, fixes 749.145, studies 749.146. Not begun: 749.144, 749.147, the hymn items 749.148 to 749.152. Paper: `reports/Luthier_v45.docx` (builder `reports/make_luthier_v45_from_v44.py`), row v216, Module 27.126, Table HL. Results: `studies/busy_sections/RESULT_build.md`, `studies/lever_range`, `studies/soundness/neighbour_v45.json`, `studies/judging_checks`.

- 958 (749.142): `VERSE_CLOSER = "apart"` by default, 4/4 only; a lyric may set `"verse_closer": false`; `LUTHIER_VERSE_CLOSER=off` for studies. The record names the lines (`spec.verse_closer`). Songs 55, 54, 58: builds' rhythm scaling 0.678, 0.620, 0.592; chosen tunes' words' fit 0.347, 0.272, 0.357; sound with no lean; pools fail the rule 0.0 in 100.
- 749.143: song 49 (`songs/p59/lyric49.json`, from the locked lyric word for word) is a second hold-out, never fitted to. Records with the form (`lyric49.song.json`) and without (`lyric49.without_958.song.json`). With the form: rhythm scaling 0.612 to 0.668, bars unsung 0.083 to 0.207, **chosen tune's words' fit 0.326 to 0.210**, builds' middle 0.264 to 0.224. The hold-out disagrees on the words; put to the session.
- 749.146 (`studies/lever_range`; needs `studies/metre/lines_cocopops.py`'s lines from a clone of CoCoPops in `corpora/`): kept verse lines in one bar, in 100, at 6, 7, 8, 9 syllables: 28, 18, 9, 4. The range does not widen. The form takes 8-syllable lines as readily as 6-syllable ones; kept songs do not.
- 749.145: `neighbour.py` reads the ceiling from the kept table.
- Judging research (`studies/judging_checks`): sources of nights one and two checked; the chair's spectral gap reproduced and its split-half read (0.58); chord repetition against covers **within artists −0.042 (p .009)**, rule first, against −0.071 across artists. The raw data are in `/home/claude/dl/shape` and `/home/claude/shape` on the maintainer's machine, rebuilt by the scripts; a YouTube key is needed for views.
- **Not to be forgotten (the writer, 22 November): a trial of sections that loop less in the chord writer** (the judging research's J1), now that the within-artist test holds. Rule first; the reading in `studies/judging_checks/nights_1_2/loops.json` shows songs 58 and 60's verses over the kept 90th of repetition.

Next: Luthier v46 (row v217), Window 203, Module 27.127 (anchor "27.126"), tables HM…, fixes from 959.
