# A key the writer asks for: the form and its marks, written first (749.219)

27 November 2026. The item is the songwriting session's, from song 66 (`songs/p68/fixlist_v53.md`): the engine draws the tune against a written tonic with its floor on that tonic, and chooses the key afterwards by where the tune fits the voice. So a key cannot be asked for: on song 66 the writer wanted A minor for a tenor, the engine's own run gave D minor, and a design gate that kept only tunes fitting a tenor over an A3 tonic let 86 builds of 4,000 live and passed 9 to the pool. Seen before writing: that entry, `songs/p76/design66.py`, the code of `plan()` and `chord_writer.choose_key()`, and the v53 records' keys. Nothing of this form has been run.

**The form.** A lyric may carry `"key"`, a tonic's name with `m` for the minor (`"Am"`, `"Bb"`). Where it does, and its mode is the lyric's:
1. The planned band of the tune (the lowest floor to the highest top of the parts' registers, as `plan()` leaves them) is placed in the voice: centred in the voice's comfortable range, kept inside it where it fits.
2. Of the asked tonic's octaves, the one nearest under that placement is the written tonic, and every register is moved by the difference, in semitones, so that the draw happens in the same place in the voice but against the asked tonic. On song 66 that should draw the tune about a fourth higher against its tonic than the engine's own run does, in the same notes of the tenor's range.
3. When the key is chosen after the pick, only the asked key is taken, at the octave that fits. Where the chosen tune does not fit the voice in the asked key, the engine's own key is used and the record says so.
Nothing is gated and no build is refused for the key. With no `"key"` in the lyric nothing changes: songs 54 and 55 byte for byte. A setting.

**Marks.**
- **K1 (the list's check).** Song 66 written through by v53 from a copy of its lyric with `"key": "Am"`, no design gate: living builds no fewer than 0.9 of the engine's own run of song 66 on v53 (read first, with no key asked; the list's 276 was v52's), pool 10 or more, the key in the record A minor, every note inside a tenor (C3 to A4).
- **K2 (it must work for any key, not only the one that prompted it).** Songs 55, 54 and 58, each asked for the key a tritone from its own v53 key (the farthest a key can be): the record carries the asked key; every note inside the voice; living builds no fewer than 0.8 of its v53 record's; pool 10 or more; the chosen tune at or over its floor.
- **K3.** Those three chosen tunes sound by the rule, or with no more leans than v53's three.
- **K4.** With no key asked, songs 54 and 55 byte for byte v53's.

**What I expect.** K1, K2, K4 met. The draw's rules are in pitch classes and intervals and do not care which degree the floor sits on, except two that do: the kept shares of each degree of the scale (846), which will now be drawn in another part of the register and so on other pitches, and the planted peak, whose top is set from the registers. I expect living builds within a tenth of each song's own. K3 I hold less firmly: a tune whose lowest notes are the fifth of the key and not its tonic may read differently on "time on the tonic" in the page gate, and one of three chosen tunes could move a reading.
