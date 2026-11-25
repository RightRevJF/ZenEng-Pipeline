# Review 32: Luthier v47 (Window 204, Module 27.128, Table HN)

25 November 2026, the songwriting session. Branch luthier-v8-stage1 at bea3935 (main merged in), merged into main.

## Reproduced

- `song_from_lyric.py --check`: 11 records, every stamped table the table at hand (9 under earlier versions' names not read).
- Songs 55, 54, 58 rerun from their lyric files (1000 builds, 12 drafts, PYTHONHASHSEED 0): their records byte for byte. Living builds 223, 256, 294; the octave gate passes over 69, 66, 111 tries; picks 867873b1e8c6, b71ab3ba9f1d, 3ba9b1ab8478.
- Song 52 rerun: its record byte for byte (22 living; the one note 962 lifts, "wall" G4 to B4).
- Song 49 rerun: its record byte for byte (287 living; pick a8cc10aec8f9).
- The pools (`studies/soundness/neighbour.py` on songs 55, 54, 58, PYTHONHASHSEED 0): `neighbour.json` byte for byte, the same as `neighbour_v47.json`.
- Code read: 959 and 961 in `Engine.gates()` on the notes as sung; 962 `vary_returns()` before the melismas and the checks, with the guard on the tune's highest note; 960's redraw in `Writer.section()`; 963 in the blue-note draw. Each matches Module 27.128 as written ("a scale step or more onto a chord tone": song 52's lift is a third, as the paper says it may be).
- Song 59's record read only as check 7 reads it; not rerun here.

## Rulings

1. **959 on by default: agreed.** It does what it says and costs nothing in the words. But it is a ban where kept songs allow one or two such leaps a song, and it leaves the pools nearer the bar than any window since v35: living builds down about 3 in 10, a random pool pick failing the rule 6.5 times in 100 with its range reaching 11.2, past the bar of 10. Your kept-shaped form (at most one such leap a song, the kept 90th) is approved as the next engine trial, rule first (749.176).
2. **962 on: agreed.** The tags returning note for note are left as they are: a tag is a repeat by design. Song 52's one note is accepted; no new edition of song 52 (it is the writer's to ask for).
3. **961 a setting, not a default: agreed, and the fault was mine.** I wrote it from song 62, whose long note fell inside a word; as a rule for every title it forbids a held feminine ending, which song 49's own intake asked for. The amendment was written before the second run and changes nothing but 961's default; the checks stood unchanged. Before 961 is tried again: read the kept songs for where a title line's longest note falls, and test the narrower form that was song 62's real fault: a weak syllable held longest *inside* a word or before the line's last word, a held last syllable allowed (749.177).
4. **749.175: agreed.** The builds' middle words' fit is the figure to check, to 0.02; the chosen tune's fit is reported beside it and decides nothing. This replaces my check of the chosen tune in every standing rule.
5. **960 stays a setting.** The gentler gate (redraw only verses and bridges over the kept 75th, so the writer's excess is trimmed and the kept spread kept) is approved, rule first, with song 63 as its hold-out and its ledger line written first (749.178). It is the one test that may spend song 63.
6. **The region gate not built: agreed.** The finding stands (749.170); the remedy is in the draw (fewer notes piled on three pitches), carried.
7. **Review 31's items read: agreed.** 749.154 withdrawn; song 50 sealed; loop_less a setting.

## Next fix 964. Next finding 749.179.
