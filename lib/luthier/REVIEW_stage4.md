# Review of stage 4 (Luthier v13, fixes 800 to 809), 18 November 2026

Branch `luthier-v8-stage1` at bf9b7a5, merged into main with a merge commit. The branch had merged a main from before the stage 3 review,
so 749.47 and 749.48 (REVIEW_stage3.md) are new to the maintainer; the next free finding is 749.49.

| Check | Result | Held? |
|---|---|---|
| chord_writer.py, write_song.py, metre_engine.py, test_prototype_writer.py compile | yes | yes |
| `chord_writer.py` (the held-out test) | its "major" and "minor" blocks identical to the committed stage4_results.json | yes, see 749.49 |
| `write_song.py songs/p62/spec52.json 1000 12` | the log and spec52.written_chords.json identical: draft 8 chosen, chords 0.502, melody pick 2.034 | yes |
| 806: songs/p36/melody_p36.py with `alive` for `alive[:40]` | gives every logged code_sha, p59 de9980323711, p60 6f6fcb2d5431, p61 95ad9f2570f1, p64 d0437ef8da41, p65 e09301a20870 | yes, 749.46 closed |
| The prototype at its own setting (400 candidates; the paper tested 100) | major verses 2 in 100 out of key (kept 14), loops 7 in 100 (kept 26), chords used 0.29 (kept sets 0.07): no better than at 100. `review4_prototype_400.txt` | 800's verdict holds |
| `Writer("minor")` | runs; 40 songs of verse, chorus, verse, chorus, bridge, a 10-bar last chorus: see 749.50 to 749.52 | partly |
| 749.47 and 749.48 (stage 3) | not changed by stage 4 | open |

## writers/chords.py: retire it

Retire it rather than have it call the new writer. Song 57's chords (chords_p67.json, seed 20261584) were drawn by it, and a wrapper
would change them on any rerun. Its two extras are in the new writer: the required bVII (805's `require=`) and the pick on kept readings (809).
Its docstring now says it is retired and kept only so song 57 reproduces; chords_p67.py still writes chords_p67.json byte for byte.
Song 58 (4/4, l11) will take its chords from chord_writer.py.

## 749.49 The README's command erases part of the committed results

**Problem.** `python3 lib/luthier/chord_writer.py` rewrites stage4_results.json with "major" and "minor" only. The committed file also holds
"chromatic_setting", "key_choice_song52", "required_bVII", "prototype" and "song52_written", and no committed script writes them.
**Evidence.** After the rerun the file loses 2,175 lines; the two blocks it writes are identical to the committed ones.
**Fix.** Commit the scripts that wrote 801 to 805's figures and the prototype block, and have the held-out test update its own keys only.
**Check.** The README's commands rebuild stage4_results.json byte for byte.

## 749.50 A last chorus that runs long ends away from home

**Problem.** 801: a longer return keeps its first's chords and draws its added bars. The added bars end the song away from the tonic.
**Evidence.** 100 songs a mode, form verse, chorus, verse, chorus, bridge, a last chorus of 10 bars against the chorus's 8:

| | Written: first chorus ends on the tonic | Written: the 10-bar last chorus | Written: an 8-bar last chorus | Kept: choruses | Kept: a song's last sung section |
|---|---|---|---|---|---|
| Major | 24 | 5 | 24 | 36 | 41 |
| Minor | 15 | 2 | 15 | 24 | 31 |

The long last choruses end on V 32, IV 22 (major); bVII 34, V 24 (minor). Window 170 saw the same in song 52 (C-sharp diminished and F-sharp).
Choruses in general end on the tonic less than kept ones, which is Table FX's last-chord gap.
**Fix.** The added bars of a song's last section weighed by how kept songs end, not how a section ends; or the last bar of a long return kept from its first.
**Check.** The last sung section ends on the tonic at about the kept rate.

## 749.51 In minor the writer leaves the key at twice the kept rate

**Problem.** 805 sets chromatic=1 to the kept rate. That holds in major (14 in 100) but not in minor.
**Evidence.** 40 minor songs: share of bars from outside the key, median 0.22; kept songs' median 0.11 (quartiles 0.00, 0.11, 0.28). Tonic's share 0.30 against 0.39.
**Fix.** Set the chromatic weight per mode against its own kept rate.
**Check.** In minor the written median within five points of the kept.

## 749.52 Spelling in the sharp minor keys

**Problem.** `name()` spells every flattened degree with flats, and the tonic list has no flat minors.
**Evidence.** G-sharp minor: bVII as Gb (F-sharp). D-sharp minor: bIII Gb, bVII Db (F-sharp, C-sharp). write_song names the tonic of B-flat minor A-sharp, then spells its bIII Db and bVI Gb beside A#m. `choose_key(..., mode="minor")` offers "Dbm" for C-sharp minor.
**Fix.** Spell a key's chords from its key signature (minor keys from their relative major).
**Check.** No chord in a key is spelled against its signature.
