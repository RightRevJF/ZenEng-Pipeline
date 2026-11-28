# windows_lakh_after: why there are two runs (written before the second run)

28 November 2026, about 11:42 ET.

The first run (result_first_run_YT_subset.json, kept unchanged) did not do what PREDICTION.md says. PREDICTION.md says the versions come from Discogs-VI 20240701 "by cliques_versions.py's reduction", which reads `main/Discogs-VI-20240701.jsonl` (the full set). The code took the first `.jsonl` member of main.zip, which is `main/Discogs-VI-YT-20240701.jsonl` (the YouTube-matched subset). So only 1,610 of 2,162 cliques were found, and each clique carried only its YouTube-matched versions.

What the first run gave (reported in full in RESULT.md): ch_rep Delta -0.114 (SE 0.116, p .32), halves -0.360 and +0.046: unsettled.

The fix changes one line (the member name) so the code matches the rule already written. No rule, prediction, control or threshold changes. **Declared before the second run: the second run is the verdict of record, because it is the one PREDICTION.md describes; both runs are reported.** The risk that a reader should weigh: I saw the first run's outcome before fixing the code.
