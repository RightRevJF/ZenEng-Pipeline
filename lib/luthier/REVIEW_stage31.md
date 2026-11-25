# Review 31: Luthier v46 (Window 203, Module 27.127, Table HM)

25 November 2026, the songwriting session. Branch luthier-v8-stage1 at f586c6b, merged into main.

## Reproduced

- `song_from_lyric.py --check`: 11 records, every stamped table the table at hand.
- Songs 55, 54, 58 rerun from their lyric files (1000 builds, 12 drafts, PYTHONHASHSEED 0): their records byte for byte, the picks of Window 201 (42785ec6990c, b5e09eec154f, ff0af26e2610).
- Song 49 rerun: the record without the form, byte for byte.
- The trial by kept shares on song 49 (`trial_shares.py`, LUTHIER_VERSE_CLOSER=shares): `cap_shares_lyric49.json` byte for byte (350 live; rhythm scaling 0.634; words' fit 0.215; verse over chorus 1.53).
- The pools (`studies/soundness/neighbour.py` on songs 55, 54, 58, PYTHONHASHSEED 0): `neighbour.json` byte for byte, the same as `neighbour_v46.json`.
- Song 59's record changes only by losing the empty verse-closer block (no line was given one bar); its notes are unchanged.

## Rulings

1. **958 off by default (749.153): confirmed.** A lyric may still ask for it.
2. **The trial by kept shares: it fails by its frozen rule, and is not built.** Agreed in full. Three checks of six fail, and the guard. The cost in words' fit does not shrink with the lines taken (song 49: -0.049 with three lines, -0.040 with four under 958).
3. **Song 50 stays sealed: agreed.** Running it after the seen songs had failed could change nothing. The list was wrong about its tempo: the intake's last ruling is 88 (q = 88 swung, with the form); 76 was its first answer. Corrected (749.173).
4. **749.154, the reading of the whole fit: tested on the kept songs, and it does not hold** (`studies/pace_and_fit`, rule committed first, 43c1a84). At the same line-by-line fit, kept songs whose sections change pace more do not have a lower whole fit (-0.03, SE 0.05, p .53; without length in salience -0.02). Their whole fit is carried by their lines (beta 0.80, R squared 0.64). Song 49 under the form sits at a pace spread of about 0.21, inside the kept range (90th percentile 0.255), where kept songs lose nothing. So the words' check is not counting pace as misfit; the fall is in how the engine fills a line it gives one bar. 749.171 proposes the reading that would find it.
5. **749.169, the ledger: accepted.** The next test against a hold-out writes its line first: song 63 when 749.159 runs.
6. **loop_less stays a setting, not the default: agreed.** The research's two faces (run 04: songs that loop more were more often taken up at all, +1.19 points, p .018, a kill of the prediction; test 6, after seeing results, +1.00, p .044, a lead) and the fresh-songs test (same direction, not settled) do not yet say which way a writer should lean. The trial reads whether the setting does what it says; the default waits for fresh songs.
7. **Next, approved in this order.**
   - 749.159, the trial (960), with one of the two repairs chosen and written into the rule before any build: either filter the kept templates by their own repeat structure (the share of bars that return), or gate the written verse and bridge's chord repetition at or below the kept median. Hold-out: song 63, its ledger line first. Seen songs: 55, 54, 58, 60, 61, 62 (never 59).
   - Then the flagged patches of `lib/luthier/proposed_v47.py`, one at a time, each frozen before its run: `octave` (749.160), `title_stress` (749.162), `no_blue` (749.168), `vary_returns` (749.167), `region` (749.165, 749.170). `region` last: it costs the most survivors.
8. **The research runs 03 to 05: read; not rechecked here either.** None passes. What bears on the engine: the two faces of looping (run 04), which ruling 6 follows; the arrow of time (run 05, test 2, +0.84, p .035, unsettled; killed with the opposite sign on single-song artists, a comparison across artists); melody range (unsettled, and two-faced as looping is). Nothing goes into the engine from them. The McGill hold-out has been read twice; a fresh outcome needs a fresh hold-out before any of these leads is tested again.

## Next fix 959. Next finding 749.174.
