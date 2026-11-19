# Review 13: Luthier v26 (fixes 904–906)

Branch `luthier-v8-stage1` at e72102c, main merged in. Reviewed on a fresh clone of CoCoPops, parsed with the v26 `cocopops_parse.py`.

## The makers, byte for byte

| Maker | Output | Reproduced |
|---|---|---|
| `cocopops_parse.py` | `corpora/cocopops_notes.csv.gz` (66,668 notes; 7,833 tie starts now read) | yes, and identical to the session's own tie-aware parse (`studies/kept_checks/parse_ties.py`) |
| `make_kept_4_4_tables.py` | `metre_atlas/4-4_pop_sung.json`, `metre_atlas/kept_readings.json` | yes, byte for byte |
| `make_kept_word_weight.py` | `kept_word_weight.json` | yes |
| `make_kept_returns.py` | `kept_returns.json` | yes |
| `make_kept_line_ends.py` | `kept_line_ends.json` | yes |
| `kept_plan.py` | `register_plan.json` | **cannot run here**: it imports `common` from `/home/claude/zeneng/corpus/nine`, which is not in the repo (749.86) |

`make_kept_4_4_tables.py` on the old parse (main's `cocopops_parse.py`) gives main's tables back except the `source` text and `surprise_quartiles`: main [2.73, 2.956, 3.146], remade [2.741, 2.963, 3.152]. Small, but "reproduces the old tables" is not quite true of that field (749.87).

The song reruns (54, 55, 58 and 52 by `song_from_lyric.py`; 52 and 53 by `metre_engine.py`; 53's hymn parts; stage 4's chord writer and `write_song.py`) all reproduce the committed records byte for byte. `git status` is clean after them.

## 904, 905, 906

- **904.** `recip_dur` strips `[({&` before the length. Checked on Chiquitita ("sor-row": 0.5 then 0.5 tied to 2.0) and against the full parse. Holds.
- **905.** All four records carry `kept_tables`, and every fingerprint matches the committed table's SHA-1. The 6/8 record lists its own metre table. Holds. One gap: `register_plan.json` is fingerprinted but cannot be remade outside the maintainer's box, and it now sets the key (749.84, 749.86).
- **906.** `band.checks` splits phrases at half a beat and prints the share over 12 beats beside the kept 0.042. The maker clips each note at the next onset and counts the 160 kept 4/4 songs. My `phrases.py` (206 songs, all metres, unclipped) gives 0.046. Same reading. Holds as a print. It does not steer anything, and all three 4/4 picks now sit at about twice the kept share (749.88).

`stage13_results.json` agrees with the reruns on every field I checked.

## The studies: which read a parse that dropped tie starts

| Study | Parser | Dropped tie starts? | Rerun |
|---|---|---|---|
| ornament (848), part 1 | MusicXML (ties merged by music21) | no | not needed |
| ornament (848), part 2 | `studies/words/parse_words.py` | no: length by `re.search`, so `[8B` reads as an eighth; a token ending `]` or `_` is added to the note before it | not needed |
| metre / slots (869) | `studies/metre/lines_cocopops.py`, length from `tension/parse_cocopops.kern_dur` (`[\[\(\{&]*(\d+)`) | no | not needed |
| genre / degrees (846) | `tension/cocopops_bars.json` from the same `kern_dur` | no | not needed |
| hooks (the 0.73 behind 840) | `studies/hooks/hooks_titles.parse` (allows `[`; continuations join the word) | no: "sorrow" in Chiquitita reads as 61, 59, then 59 tied over | not needed |
| breath by onsets (arc, spectrum, return, rates) | `studies/ssm/ssm_lib.kern_dur` (`\[?(\d+)`) | no | not needed |
| silences | `corpora/cocopops_notes.csv.gz` (the maintainer's parse) | **yes** | rerun |
| phrases | the same file, but every reported run had `LUTHIER_COCOPOPS_NOTES` on the tie-aware parse | effectively no | rerun; identical |
| last chorus | `corpora/cocopops_notes.csv.gz` | **yes** | rerun |
| kept checks (line ends, returns, 901 recount) | both parses, side by side | reported both | not needed |

Before and after, ties read:

| Reading | Old parse | Ties read |
|---|---|---|
| silences of a beat or more per 100 beats (quartiles) | 7.0, 9.1, 11.1 | 6.7, 8.5, 10.4 |
| median silence, beats (quartiles) | 1.5, 2.0, 3.0 | 1.5, 2.0, 3.0 |
| phrases over 12 beats, breath at half a beat | 0.046 | 0.046 |
| last chorus over first: notes added (median; quartiles) | 7; 0, 32 | 7; 0, 34 |
| last chorus over first: beats sung (median; quartiles) | 6.75; 0, 38.7 | 8.0; 0, 40.5 |
| last chorus over first: mean pitch (median; share up) | 0.09; 0.56 | 0.08; 0.57 |
| last chorus over first: loudness (median; share up) | 0.44; 0.66 | 0.47; 0.63 |

No conclusion changes. Last choruses are still longer and louder than first choruses, and no higher. On the v26 records the silences read 9.1 (54), 7.1 (55) and 9.8 (58), all inside the new kept quartiles. Breaths by onsets: 9.3, 10.2 and 7.4 a minute (human median 7).

Two of the constants listed as not rebuilt can be recounted from the mended corpus with one definition on both parses (`studies/kept_checks/silence_counts.py`). 877 is unchanged: silences of two bars or more number 1, 2, 3 per song by quartile, either way. 876 falls by about a tenth: a silence of one bar to two, per eight bars, has median 0.386 on the old parse and 0.35 with ties read. ENTRY (771) and WORD_PITCH (847) need the stress spine, which the notes table does not carry.

## Nits

- `kept6a.json` at the repo root is `kept_plan.py`'s output, committed by mistake.
- The README says the session's studies "were not checked for ties". They are now: see the table above.

## Merged

`origin/luthier-v8-stage1` into main, no fast-forward.
