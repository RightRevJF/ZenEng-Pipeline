# The loop gate with a chance on sealed song 63: the result (749.185; fix 965)

26 November 2026. Marks in `PREDICTION_song63.md`, committed with the ledger row (a89334a) before song 63 was run by anything. Run once with `LUTHIER_LOOP=chance`; the setting from the switch, the lyric file untouched. Record `lyric63.chance.song.json` (a test record).

**Both deciding marks hold, the first at its edge. The form is built as fix 965: what `"chords": "loop_less"` means, a setting and not a default.**

| Mark | The form | |
|---|---|---|
| 1. The pool, 10 builds or more | **10** | holds, exactly |
| 2. The builds' middle words' fit at or over the words gate's floor (0.152) | 0.361 | holds |
| 3. The plan one the form could have made | verse 0.111 (kept 75th 0.5), bridge 0.100 (kept 75th 0.357) | as it should be |

**Said plainly: mark 1 holds with nothing to spare.** After the marked run, and deciding nothing, I ran song 63 on v50 without the form (`lyric63.v50.song.json`): living builds 176 and pool 14, against 104 and 10 with the form. The form does not touch the melody. What changed is the chord plan: the two runs choose different chord drafts (draft 7 and draft 9 of 12), because with the form on the drafts themselves differ, and the melody's builds live or die on the plan they are given (deaths at the chorus's lift 413, at the join before a copy 243). So on this song the chords the form led to are harder on the melody than the ones v50 chose. One song cannot say whether that is the form or the draw of the drafts; the drafts' check (a thousand sections a kind) found the form's sections as near kept sections as the unpatched writer's or nearer. It is recorded here because a pool of exactly 10 is not a comfortable pass.

Song 63 is in the gospel family, where the songwriting session notes vamps are part of the style; its verse and bridge were under the kept 75th as first drawn, so in the chosen plan the form redrew nothing that I can see from the record.

**Song 63 is spent.** It is a seen song from here on. Whether it should ask for chords that loop less when it is made for the writer is his choice; this test does not decide it.

**Built.** Fix 965: `lib/luthier/chord_writer.py` `section()`; `lib/luthier/song_from_lyric.py` sets it where a lyric has `"chords": "loop_less"`; `tables/loop_chance.json` stamped into such a song's record. `LUTHIER_LOOP=median` and `=gentle` remain for studies (the two forms that failed). No lyric in the repository asks for `loop_less`, so no record changes; songs 54 and 55 are byte for byte v50's.
