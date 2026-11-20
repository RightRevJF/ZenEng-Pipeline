# Plant the peak (749.111): the rule, written before the trial

**The idea (the songwriting session's).** A song's range is set today by a hard top the draw is cut at, and the tune seldom reaches it (song 55) or presses against it (song 58). Instead, in the section where the aimed kept song first reaches its top, the first line drawn fresh sings its highest stressed note at the floor plus the aimed range. Lines that return carry it.

**Trial, outside the engine.** `trial.py` wraps the engine's pitch draw; nothing in `lib/luthier` changes. Two forms:

- A: the planted line's register is raised so it reaches the peak; every part's top is the peak.
- B: as A, but every other fresh line's top is two semitones under the peak, so only the planted line and its returns sing it.

**The check (the session's), on 100 tries per song:**

1. the builds' span within 2 semitones of the aim in at least half the builds;
2. the share of notes on the top note inside the kept 10th to 90th (0.3 to 8.7 in 100) in 9 builds in 10.

A form passes if it meets both in all three songs. If neither passes, the idea is not built as it stands.
