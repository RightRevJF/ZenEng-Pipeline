# Luthier list for v42 (since v41)

20 November 2026. Luthier v40 (945) and v41 (946 to 949) are reviewed (`lib/luthier/REVIEW_stage26.md`) and merged into main at d498055. All five song records, song 53's run, song 60's v41 record, `soundness.json`, `neighbour.json` and the room table reproduce byte for byte. Song 58's sixteenth edition is built from the v41 record. Next finding 749.131; next fix 950.

## In short

The rhythm-memory study answers 749.123 and 749.130: pace and rests carry rhythm scaling, not where repeats come from. My 749.123 was wrong, and both items are closed. 946, 948 and 949 hold. 947 holds with a caution about small families. The lyric's room check is now in the method at the lyric stage, beside the mouth tests.

Planting the peak (749.111) is the right next step. Song 58 is its widest case: an ask of 19.9 semitones against a pick spanning 12.

## Items

### 749.131 The family middles have no maker
**Problem.** `kept_words_to_shape.json` holds `repeated_notes_by_family`, but no script writes it. `make_kept_words_to_shape.py` rebuilds the table without it. The engine then falls back without a word (`.get(...) or {}`), and song 60 would change silently.
**Evidence.** Rerunning the seven makers rebuilt the table minus that block (six lines); everything else matched. The values are in `studies/movement_by_family/result.json`.
**Fix.** Have the maker (or a maker of its own) write the family middles from the study's code. Have the engine stop with a message when a song's family is missing from the table.
**Check.** Every maker rebuilds every table byte for byte, and deleting the block makes the engine refuse, not drift.

### 749.132 Stamp the room readings with the engine that made them
**Problem.** Each lyric's room file is read once. When the engine changes, the file stays as it was and no longer matches what the engine builds.
**Evidence.** Rerun under v41: song 55's bars unsung 0.143 against the file's 0.124; song 58's 0.093 against 0.084; song 60's 0.169 against 0.167. Every verdict holds.
**Fix.** Write the engine's commit and table hashes into each room file, and rerun the room files in any window that changes builds, as the records are.
**Check.** Every room file names its engine, and a rerun on that engine matches it byte for byte.

### 749.133 Repeated notes by family: shrink the small families
**Problem.** Three movements were tested, and one passed at 2.2 shuffles in 100. Corrected for three tests, the bar is 1.7. The soul and country middles each rest on 18 kept songs, and the soul middle (0.207) is far from the rest (0.319, 0.335).
**Evidence.** `studies/movement_by_family/result.json`: family sizes 18, 124, 18; shuffles as large 0.022.
**Fix.** Report each family middle with its bootstrap range. Take a shrunk middle (the family's, pulled toward the kept middle by its size) until the families are larger, and say in the paper that the test passes uncorrected.
**Check.** Song 60's repeated-notes aim moves no further from the kept middle than its family's lower range bound allows.

### 749.134 One note for half a verse: read the commonest pitch's share
**Problem.** A section can sit on one pitch for half its notes without a long run, so the chant check (longest run over the kept 90th, 9.5) passes it.
**Evidence.** v41 records: song 58's verses sit on E3 for 57 of every 100 sung notes (longest run 6); song 60's verses on one pitch for 46 (longest run 6). Songs 55, 54 and 59: 24, 28 and 27.
**Fix.** Rule first: read the commonest pitch's share in each kept song's verse and chorus, and compare it with Luthier's builds. If Luthier's sit over the kept 90th, add it to the page gate or the fit.
**Check.** The study reports the kept quartiles. If adopted, no pick's section stands over the kept 90th.

## Closed

749.123 (where repeats come from) and 749.130 (rhythm scaling's contrast): answered by studies/rhythm_memory. 749.124, 749.126, 749.128, 749.129: done (949, 948, 946, 947).

## Carried

749.111 (the peak: next, with song 58 as its widest case), 749.125 (song 60 as a practice song), 749.127 (a "seen before writing" line: Window 197's PREDICTION.md did it, so keep it), 749.109, 749.116, 749.103, 749.101, 749.61.
