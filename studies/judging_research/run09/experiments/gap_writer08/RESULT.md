# gap_writer08: does the ii-V share in a chart written outside iReal predict covers? (LEAD on seen songs, not counted)

## The question
Run 08 found that tunes whose charts hold more ii-V moves (a ii chord stepping to a V chord) tend to have been covered by more artists. One worry is that this is a chart writer's habit, not the song: iReal Pro chart writers might add ii-Vs to much-recorded tunes. So we read the ii-V share from a chart written outside the iReal community (Real Book or Band-in-a-Box, "upstream") and also from the iReal charts of the same tune. GAP is the iReal share minus the upstream share. 1,181 of run 08's songs had both kinds of chart. These songs' outcomes were already opened in run 08, so this is a lead and is never counted. All figures are in standard-deviation units of covers per standard deviation of the measure.

## Predictions, written first
- Song story (the tune carries its ii-Vs whoever writes the chart): upstream +0.045, GAP about 0.
- Writer story (iReal writers add them): upstream +0.01 or less, GAP +0.03 or more.

## What came out
Main model (the frozen one; it held log of the number of iReal charts, which is itself close to a popularity measure and may sit on the path from covers to charts):
- Upstream: -0.041 (95% range -0.096 to +0.015, p .15).
- GAP: -0.048 (range -0.093 to -0.002, p .039; composer-clustered p .051).
- Frozen label: both stories excluded. The song story fails because +0.045 is above the upstream range; the writer story fails because the GAP range sits below +0.03.

Readings (these decide nothing; I applied the frozen exclusion rules by hand):
- Without the chart-count control: upstream +0.046 (range -0.014 to +0.106), GAP -0.012 (range -0.063 to +0.040). Song story not excluded; writer story not excluded.
- Upstream alone (with upstream controls): +0.064 (range +0.014 to +0.114, p .012). This excludes the writer story (its lower bound is above +0.01) and keeps the song story.
- iReal alone, same songs: +0.020 (range -0.034 to +0.074, p .47). Smaller than the upstream reading, and not distinguishable from zero.

## Plain reading
The outcome depends on whether the chart-count control is held. With it, both predictions miss and GAP is slightly negative. Without it, GAP is about zero and the upstream share is near the song story's +0.045. The upstream-alone and no-count readings point toward the song, not the iReal writer, but the main frozen model does not, and the negative GAP appears only when chart count is held, so I would not lean on it. The iReal reading predicting less than the upstream one is the opposite of what "iReal writers add ii-Vs to popular tunes" implies. The Poisson second model agrees in direction (upstream +0.142 alone, +0.118 without count; GAP -0.068 in the main model).

Power was low (0.21 for upstream, 0.12 for GAP), so the ranges are wide and no single reading is firm. Halves of the songs agree in sign for most readings but not for GAP without the count (-0.060 versus +0.043).

## What it cannot say
- These are seen songs; the pattern is a lead for the next unseen batch.
- Jazz-heavy tunes, the kind with both Real Book and iReal charts.
- "Outside iReal" is not "before covering": the Real Book was compiled from canonical recordings, and Band-in-a-Box files are user-made.
- Matching is by title only, so some charts may belong to a different song with the same name.

Source: result.json in this folder (labels: song_story_excluded true, writer_story_excluded true, "both stories excluded").
