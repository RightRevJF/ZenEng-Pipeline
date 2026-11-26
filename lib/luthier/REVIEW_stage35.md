# Review 35: Luthier v50 (Window 207, Module 27.131, Table HQ)

25 November 2026, the songwriting session. Branch luthier-v8-stage1 at 0237615 (main merged in), merged into main.

## Reproduced

- `song_from_lyric.py --check`: 12 records, every stamped table the table at hand (`kept_octave_tail.json` among them).
- With fix 964 on (1000 builds, 12 drafts, PYTHONHASHSEED 0), each record byte for byte: song 54 (279 living; pick 526fa2538b7e), song 55 (293; 093dc0a9f48f), song 58 (366; b15e2868f9d3), and song 50 (243; 37d2002919cb).
- Every rule was committed before its run: the centre reading (39870bc, 17:37) before its result (92e0600, 17:41); the shared bin's checks (92e0600) before its result (56e4bf3, 18:12); the 240 draws (4939f82, 18:15) before theirs (623cc86, 18:29); song 50's four marks and its ledger line (fc3d70f, 18:42) before its run (ed8c8d7, 18:49).
- The ledger reads right: the conflict markers committed at fc3d70f are gone at ed8c8d7, and every line on both sides is kept. My own row for song 64 needed two words changed now that 749.191 is closed (done in this merge).
- Code read: 964 shares the ±12 bin in `pitches1()` (the octave its kept share, the pitches past it the rest between them); the plant (950) and the gate (959) are unchanged. A nit, no cost seen: where the octave above or below is not among a note's candidates (a clash rule took it), its share of the bin is not passed on to the pitches past it.

## Rulings

1. **749.191, the centre reading: accepted, and my proposal was wrong.** The lines that carry the planted peak sit as high against their top, and as far over their part, as kept songs' lines. The centre form is not tried. Closed.
2. **749.192 and fix 964: accepted, the best finding of the week.** The kept table's ±12 bins hold every interval of an octave or more, and the draw gave the whole bin to each such pitch. It is older than the plant, and it explains the gate (749.160), the plant's leaps (749.186) and why no choice among draws could mend them (749.189). A correction of the draw's reading of its own table, not a new idea.
3. **Building it on song 50's marks: agreed.** The seen songs held five marks of six. The sixth (the peak planted as often as v47) was shown, before song 50 was run, to measure the fault itself (749.193), and the writer ruled to spend song 50 on a mark written first in its place (the range kept). That is a changed mark, said plainly, met on a song nothing had touched. The seen songs' miss stays on the record.
4. **749.193: accepted.** Drawing until an outcome arrives selects for that outcome's easiest road. It is 749.181 again, in the melody; any redraw-until rule should be read for it from now on.
5. **Song 50 is spent.** The writer's word to the maintainer stands over my note that it stay sealed. Sealed now: songs 63 (the loop gate, 749.185), 64 and 65 (unreserved; 64's reservation ended with 749.191).
6. **Song 50's own look (749.195).** Its pools are 4 and 5 builds, and its chosen tune's words' fit fell from 0.399 to 0.209 with the builds behind it the same to three places. Before song 50 is made for real, read why this lyric leaves the engine so little to choose from.
7. **749.194, whether the octave gate is still wanted, goes to the writer.** With 964 and no gate, 6 to 15 builds in 100 hold such a leap (kept 17.5), and the gate passes over 18 to 54 in 1,000.

## Next fix 965. Next finding 749.197.
