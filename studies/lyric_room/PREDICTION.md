# A check of the lyric's room, before any music: the rule, written before it is run

**Why.** Rhythm scaling is low in Luthier's songs because the singing is the same busyness all through and rests too little (studies/rhythm_memory). Part of that is in the lyric: one that fills every bar, with verse and chorus lines of one length, cannot be given a kept song's rhythm by any setting. It should be caught when the lyric is locked, with the mouth tests, while the words can still change.

**What was looked at before this rule was written:** the rhythm study's result (songs 55, 54 and 58 under the kept 25th on slow change in busyness; 54 and 58 on silence; song 59 in the kept middle on both); each song's length in seconds and its syllables a line by section.

**The check (`lib/luthier/lyric_room.py`).** Given a locked lyric, it lays the song out as the engine will (the form, the slots) and draws forty quick tunes, no pick made and nothing kept. It reads three things as sung and sets each against the kept songs:

1. **room:** the share of bars in which nothing is sung;
2. **contrast:** the slow change in how busy the singing is, across windows of four bars;
3. rhythm scaling itself.

And it says in plain words what in the lyric is behind a low reading: how long the song runs against kept songs, and how long the verse's lines are against the chorus's.

**The rule: the check is good enough to use if all three hold.**

1. **It agrees with the long way.** For songs 55, 54, 58 and 59, its verdict on room and on contrast (under the kept 25th, or not) is the rhythm study's verdict in at least seven of the eight cases.
2. **It answers to the words.** Cut to its first two verses and choruses, song 54's lyric must read more room than whole, by at least 0.03.
3. **It is quick.** Under five minutes a lyric.

Song 60, which no study has read, is run and reported, and decides nothing.

If it passes it is added to what is run when a lyric is locked. It changes no song and no record.
