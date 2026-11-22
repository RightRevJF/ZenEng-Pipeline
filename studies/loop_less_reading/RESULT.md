# 749.159 step one: does the chord writer already loop less than kept songs? (22 November 2026)

No. It loops **more**, in every kind and both modes. By the rule written first, **the trial goes ahead**.

Script committed before the full run (`reading.py`); 1,000 sections drawn per kind and mode, seed 749159; `reading.json` reproduces byte for byte.

| | kept median | writer median | writer mean vs kept mean | p (Mann-Whitney) |
|---|---|---|---|---|
| major verse | 0.333 | **0.385** | 0.383 vs 0.316 | < .001 |
| major chorus | 0.333 | 0.357 | 0.355 vs 0.320 | < .001 |
| major bridge | 0.000 | **0.167** | 0.214 vs 0.185 | .018 |
| minor verse | 0.333 | **0.412** | 0.407 vs 0.359 | .013 |
| minor chorus | 0.375 | 0.429 | 0.430 vs 0.385 | .010 |
| minor bridge (35 kept) | 0.250 | 0.267 | 0.297 vs 0.269 | .57 |

(Kept sections read in the writer's vocabulary; the frozen-rule reading of the same sections gives medians within 0.03.)

**What it means.** The writer copies a kept section's pattern of repeats, but it is not the kept songs' equal: its sections loop more than the songs it learned from, chorus included. So the trial is not only a lean toward the covered end; part of it is bringing the writer back to the kept rate.

**One thing the trial's rule must change, before any build.** Half the major-key kept bridges never repeat a three-chord run (median 0.0), so "below the kept median" is empty for them. For the bridge, the trial draws from kept bridges **at or below** the median, and its check reads the bridge **at or below** the kept median. Verses unchanged.

**A second reading worth the maintainer's time, not the trial's.** The chorus loops more than kept choruses too (+0.03 to +0.05 on the mean). The trial leaves the chorus alone by design; whether the writer's excess there is wanted is a separate question.
