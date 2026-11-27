# Which 4/4 checks do not depend on the metre: a reading (27 Nov 2026, written before any run; nothing built)

The writer's direction: the engine is to write every metre as well as 4/4. The kept collection holds too few songs outside 4/4 for tables of their own (`COUNT.md`). This asks whether three of the 4/4 gates, none of which reads the bar, could stand as they are outside 4/4.

## The songs
- **Compound:** the kept melodies whose main metre is 12/8 or 6/8: Billboard (the notes table) and Rolling Stone (parsed here from the `.hum` grid; no words). About 42. A song of fewer than 100 notes is left out, as the page gate's table leaves it out.
- **3/4:** four songs; listed one by one, deciding nothing.
- **Same-source 4/4:** the Rolling Stone songs in 4/4 (about 168), read the same way. They are not in the kept tables (which are Billboard's), so they show what a different transcriber does to the figures apart from any metre.
- **The line:** the 4/4 kept tables as built.

## The checks, each read exactly as the engine's gate reads it
1. **The page gate's plainness** (922): `page_gate.read` under the 4/4 table; passed over if under the floor (the 4/4 kept 10th, so 10 kept 4/4 songs in 100 are under it by construction). Its ten parts are listed, deciding nothing.
2. **The commonest pitch's share** (956): verses pooled, choruses pooled, 20 notes or more; passed over if either is over its ceiling (the 4/4 kept 90ths).
3. **A leap past an octave inside a line** (959): lines split at onsets a half note apart; passed over if the song holds one. (Kept 4/4: 28 songs of 160 hold one anywhere.)

## The rule
For each check, the share of compound songs the 4/4 gate would pass over.
- **Borrowable on this evidence:** 20 in 100 or fewer for checks 1 and 2 (twice the 4/4 kept songs' own 10); for check 3, no more than the 4/4 kept songs' own share plus 10 points.
- **Over that:** if the same-source 4/4 songs are passed over as often (within 10 points of the compound songs from that source), the source differs and not the metre: **undecided**. Otherwise **not borrowable**: compound-time songs differ on it.
- Compound songs are read together and by source; the verdict is on the two sources together, and a split between sources is said.

"Borrowable" builds nothing. It would license a trial of that gate in 6/8 on song 52's lyric, with marks first.

## What I expect
All three borrowable. The compound songs are mostly slow ballads of the fifties and sixties, which I would guess plain, narrow and stepwise. The one in doubt is the Rolling Stone source under check 1, since its transcriptions may differ from Billboard's in ways the surprise count feels.
