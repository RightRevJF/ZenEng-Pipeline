# 6/8 folk, step A (749.232 off on the two seen lyrics): result (27 Nov 2026). MISSED on both. Step B (the held-out lyric) did not run and is not spent.

22:18 ET. Rule: PREDICTION_held_out_6_8.md (commit 1d9e7d0, before any run). No code was changed. Figures printed from step_a_232_off.json and bridge_title_52.json by the command that wrote this file; both records carry the switches meant and a judge that ran.

| Pick; living median | Living; pool | Notes a bar | On the beat | First beat | 840 in ten | Title lines on time, in 100 | Silence before, eighths | 712 | |
|---|---|---|---|---|---|---|---|---|---|
| song 52 | 807; 205 | 3.88; 3.889 | 0.439; 0.423 | 0.236; 0.221 | 0.0 | {"Chorus 1:2": 100.0, "Chorus 2:2": 100.0, "Bridge:2": 18.4} | {"Chorus 1:2": 2.0, "Chorus 2:2": 2.0, "Bridge:2": 2.0} | 991 | **missed:** title lines on time |
| song 61's words | 816; 408 | 3.618; 3.596 | 0.45; 0.445 | 0.248; 0.246 | 0.0 | {"Chorus 1:7": 100.0, "Last Chorus:7": 94.2} | {"Chorus 1:7": 2.0, "Last Chorus:7": 2.0} | 577 | **missed:** notes a bar |

- **The silence mark is met with 749.232 off:** 2 eighths before every title line, against a mark of 3.
- **Song 52's bridge title line comes in late** in most builds. That is U2, missed.
- Song 61's words: notes a bar's living median is under 3.60 by a hair again, as it was once before tonight.

## Why the bridge title line is late: a count (400 builds each way)
- The bridge title line has 10 syllables and opens on an unstressed one (1 before its first stress). It wants a pickup: its light syllable before the bar line, its stress on the beat.
- **With 749.232 off,** the line ahead begins its last syllable at its last allowed place in every build ({"-18": 400}, twelfths against its slot's end), so the earliest the title line may begin is its bar line exactly ({"0": 400}). There is no room for the pickup. The title line's first onset: {"0": 68, "12": 326, "18": 2, "30": 4} (twelfths after its bar line; 0 is on time).
- **With 749.232 on** (the bar of rest), the earliest start is {"-12": 400} and the title line begins at {"-6": 400} in every build: a pickup of an eighth.
- So the bar of rest was doing one small thing, at the cost of a silence longer than anything in Essen: **leaving room for the title line's pickup.**

## The form that follows (its own rule, before any code)
The line ahead of a title line ends a pickup's length earlier: an eighth for each light syllable the title line opens on, two at most, as the engine's own pickups are sung. Where the title line opens on a stress, nothing changes. No bar of rest.

## My expectation
Two chances in three that both passed with 749.232 off: missed. I named 840 and first-beat onsets as the doubt; the miss was the title line's entry, which I said 749.237 had settled. It had settled it only with the rest in place.
