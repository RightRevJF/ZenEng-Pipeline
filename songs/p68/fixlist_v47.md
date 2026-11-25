# Luthier list for v47 (since v46)

25 November 2026. Luthier v46 (958 off by default; the trial by kept shares, failed and not built; 749.154 read in the builds; song 50 sealed; the hold-out ledger) is reviewed (`lib/luthier/REVIEW_stage31.md`) and merged into main. Songs 55, 54, 58 and 49, the trial's song-49 figures and the pools reproduce byte for byte; both checks pass. Next finding 749.174; next fix 959.

## In short

The trial failed by its own rule, and stays off. Song 50 stays sealed, as you wrote.

Your reading of 749.154 was worth testing, and the kept songs answer it: a change of pace between sections costs kept songs nothing in the whole fit (-0.03, p .53). So the words' check is not marking pace as misfit. The fall under both forms comes from how the engine fills a line it gives one bar, and 749.171 asks for the reading that would show it.

Next, in order: the loop-less trial (749.159, with one repair chosen first, song 63 the hold-out, its ledger line first), then the flagged patches one at a time. loop_less stays a setting until fresh songs settle which way to lean.

## Items

### 749.171 What the engine does inside a line it gives one bar
**Problem.** Under 958 and the trial form, the lines given one bar fit better within themselves (song 49: 0.247 to 0.334), the other lines do not move, and the whole fit still falls (0.049). The kept songs say a change of pace does not lower the whole fit (749.172). So the cost is inside the one-bar lines, in a way the line-by-line fit does not catch.
**Evidence.** `studies/busy_sections/RESULT_shares.md` (749.154 table); `studies/pace_and_fit/RESULT.md`.
**Fix.** A reading, rule first, before any new form: in the builds, for lines given one bar, the spread of note lengths inside the line and where the weighty syllables fall in it (beat, length rank), against kept lines of the same syllable count sung in one bar. If the engine's one-bar lines give their weighty syllables no length at all where kept one-bar lines do, that is the lever.
**Check.** The reading on songs 49 and 54's living builds under the trial form, beside the kept table; the rule committed first.

### 749.172 Pace and the words' fit, on the kept songs
**Problem.** Window 203 proposed that the whole fit counts a change of pace against a song.
**Evidence.** `studies/pace_and_fit` (rule 43c1a84; result d8d44c4): 151 kept songs; at the same line fit, pace -0.032 (SE 0.050, p .53); without length -0.023; whole fit on line fit, beta 0.80, R squared 0.64.
**Fix.** None to the check. It stays as it is.
**Check.** Reproduce `studies/pace_and_fit/study.py` byte for byte.

### 749.173 Song 50's tempo
**Problem.** The list for v46 gave song 50's tempo as about 76. Its intake's last ruling is 88 (swung, with the form); 76 was the first answer.
**Fix.** `songs/p60/lyric50.json` stands at 88, as you made it.
**Check.** None.

## Carried, open

- 749.159 the loop-less trial (960): approved, with one repair chosen first; hold-out song 63; ledger line first.
- 749.160, 749.162, 749.165 to 749.168, 749.170: the flagged patches in `lib/luthier/proposed_v47.py`, approved one at a time in the order of Review 31, each frozen before its run.
- 749.144 song 58's bars of rest; 749.147 a short line in a long slot; the hymn items.
- The research leads of runs 03 to 05 (none passed): no engine change; a fresh hold-out before any is tested again.

## Closed

- 749.153: 958 off by default; the trial failed and is not built.
- 749.154: read in the builds (Window 203) and on the kept songs (749.172).
- 749.169: the ledger is in `studies/judging_data/README.md`.
