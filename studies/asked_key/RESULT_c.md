# A key the writer asks for, third run: the result (749.219; fix 968, a setting)

27 November 2026. Marks in `PREDICTION_c.md`, the songwriting session's, committed before the run. `records_c.json`.

**All five marks are met. Built as fix 968: a setting, acting only where a lyric carries `"key"`.**

| | 66 asked Am | 55 asked Db | 54 asked Ab | 58 asked Db |
|---|---|---|---|---|
| C4. Key in the record (the engine's own) | Am (Dm) | Db (G) | Ab (D) | Db (G) |
| C1. The pool | 18 | 23 | 24 | 35 |
| C2. Lowest to highest note (the voice) | 48 to 67 (48 to 69) | 44 to 61 (43 to 64) | 49 to 68 (48 to 69) | 46 to 63 (43 to 64) |
| Chosen tune's range (floor) | 19 (16.0) | 17 (14.6) | 19 (15.4) | 17 (16.6) |
| *Reported:* living builds (the song's own) | 229 (276) | 233 (308) | 290 (279) | 410 (314) |
| *Reported:* tunes the pick passed over; pool tunes inside the voice | 1; 12 of 18 | 0; 19 of 23 | 0; 24 of 24 | 3; 19 of 35 |
| *Reported:* builds' middle words' fit (own) | 0.264 (0.260) | 0.260 (0.249) | 0.208 (0.216) | 0.306 (0.304) |

- **C1 met:** pools 18, 23, 24, 35.
- **C2 met:** every note of every chosen tune is inside its voice. In songs 66 and 58 the tune the engine would have chosen left the voice by a semitone, and the pick took the next one inside it (one and three tunes passed over).
- **C3 met:** the three tritone-key tunes are sound with no lean (v53's three have one).
- **C4 met.** **C5 met:** with no `"key"`, songs 54 and 55 written through are byte for byte v53's.

**What an asked key costs, reported and not gated** (the songwriting session's ruling, written before this run: the engine's own run takes the key that suits the tune, so another key must cost something; a setting's cost is stated, as with 965). Living builds against the song's own: 0.83, 0.76, 1.04, 1.31. The pool against the song's own: 18 of 33, 23 of 33, 24 of 22, 35 of 20. And between a third and nearly half of a pool's tunes can sit outside the voice in the asked key (6 of 18; 16 of 35), which is what the pick rule is for.

**For song 66 this replaces the design gate:** 229 living builds in 1,000 and a pool of 18, against 86 in 4,000 and a pool of 9.

**Built.** `song_from_lyric.plan()` (the registers moved; `spec.key_asked`), `metre_engine.run()` (the pick inside the voice), `song_from_lyric.write()` (only the asked key taken). A key not in the lyric's mode, or not a key's name, is flagged and ignored. Where no tune in the pool is inside the voice in the asked key the engine's pick stands and the record says so; where the chosen tune fits the voice in no octave of the asked key, the engine's own key is used and flagged.
