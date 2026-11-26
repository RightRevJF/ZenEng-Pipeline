# Luthier list for v51 (since v50)

25 November 2026. Luthier v50 (fix 964: the octave bin shared as kept songs share it, on by default; song 50 spent on it) is reviewed (`lib/luthier/REVIEW_stage35.md`) and merged into main. Songs 54, 55, 58 and 50 reproduce byte for byte under 964; the check passes. Next finding 749.197; next fix 965.

## In short

You found the real fault: the kept table's ±12 bins hold every interval of an octave or more, and the draw gave the whole bin to each such pitch (749.192). Fix 964 corrects it, and the leaps fall to the kept rate with no gate. It is the best finding of the week. My centre proposal (749.191) was wrong, and the reading showed it.

Building 964 on song 50's marks, written first and set by the writer's ruling, is agreed. 749.193 (drawing until an outcome arrives selects for its easiest road) is a rule to read every redraw by.

Song 50 is spent. Sealed now: 63 (the loop gate), 64 and 65 (unreserved). The writer has ruled that the octave gate stays (749.194).

## Items

### 749.194 Is the octave gate still wanted? (for the writer)
**Problem.** With 964 and no gate, 6 to 15 builds in 100 hold a leap past an octave inside a line (kept: 17.5 songs in 100). The gate (959) now passes over 18 to 54 builds in 1,000, where it passed over 66 to 119 before 964.
**Options.** Keep the ban as it is (cheap now; strictly safer than kept songs); make it a setting, off by default (the engine then leaps about as often as kept songs, never more); or a test of taking it off, rule first, read both ways, with a sealed song.
**Ruled (the writer, 25 November): keep the ban.** 959 stays on by default; no change is tried. Closed.

### 749.195 Song 50's small pools
**Problem.** Song 50's pools are 4 builds (v47) and 5 (964), under the standard of 10, and its chosen tune's words' fit fell from 0.399 to 0.209 with the builds behind it the same to three places (0.248 both).
**Fix.** A reading first, rule committed before it: which gates and which part of the choice leave song 50 so few builds (its wide asked range in a low voice is the likely cause), and whether the choice among so few reads the words' fit as one draw (749.175).
**Check.** Written with the reading. Before song 50 is made for real.

### 749.196 A nit in 964
**Problem.** Where the octave above or below a note is not among its candidates (a clash rule took it), the octave's share of the ±12 bin is not passed on to the pitches past it, so that bin is under-weighted for that note.
**Fix.** When there is no octave candidate, give the pitches past it the whole bin's share between them; or leave it and say so.
**Check.** Count how often it happens over 1,000 builds of songs 55, 54, 58; if under 1 note in 1,000, leave it.

## Addendum: song 50's pool read, and the nit (luthier-v8-stage1 at 3155238)

Both readings had their rules committed first (5ca43f5, 19:44) and change no notes (song 54 byte for byte, checked here).

- **749.195, answered: the pitch ceiling (956) takes song 50's pool.** 5 of 29 builds pass it (the eight other songs 0.44 to 0.74). The verses of the folk songs read (50, 58, 49) put about half their notes on one mid-span pitch, against a kept ceiling of 0.44. Accepted. The chosen tunes' words' fit is a draw (inside the builds' quartiles): accepted.
- **749.196, ruled: leave it.** The maintainer is right and my nit was wrong in substance: where a rule removes the octave, the pitches past it keep their own kept odds, and passing them the octave's share would offer them the whole bin again (749.192 in small). My line of 1 in 1,000 was the wrong test. Putting it to the session rather than overriding the rule silently was right. Closed.

### 749.197 Folk verses that pile on one pitch (reading first)
**Problem.** The verses of songs marked folk (50, 58, 49, and 61) put about half their notes on one pitch; 956 passes most of those builds over, and song 50 is left a pool of 5.
**Fix.** A reading first, rule committed before it: how kept folk songs' verses spread their repeated notes over pitches, against what fix 952's folk share of repeated notes makes the draw do. Then a change to the draw if it is named, with its marks written first and read both ways.
**Check.** Written with the reading. Songs 58, 49 and 61 are where it shows; song 50 before it is made for real.

Next finding 749.198; next fix 965.

## Carried, open

- 749.185 the loop gate with a chance (song 63 reserved).
- 749.171 inside a one-bar line; rhythm scaling leans low.
- 749.144, 749.147, 749.148 to 749.152 (hymns), 749.163, 749.165 and 749.170 (the region).

## Closed

- 749.182 (the leaps: 749.186, mended by 964), 749.189 and 749.191 (the plant's line and its centre: not the fault), 749.192 (fix 964), 749.193.
