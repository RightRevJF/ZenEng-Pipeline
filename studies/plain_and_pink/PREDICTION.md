# Plain and pink: do kept songs manage both? (749.166) The rule, written before any reading

24 November 2026. Nothing below has been computed on the kept songs before this file was committed.

**The question.** On song 62, holding the sung line plain (melody surprise at or under the kept median) whitened its pitches (DFA orders 1 and 2 fell; three pitches carried 79% of the notes), and a pink line came out restless. Do the kept songs trade the two, or do many manage both?

**Songs.** The 167 kept 4/4 pop songs with 100 notes or more (`lib/luthier/kept_corpus.py`, `kept_songs(min_notes=100)`), the set behind `tables/kept_page_gate.json`.

**Measures (per song, on the sung notes in order).**
- Surprise: the page gate's (`lib/luthier/page_gate.py`), mean bits per interval, each song read with its own counts taken out, as `make_kept_page_gate.py` does.
- Pitch DFA: `lib/luthier/scaling.py` `dfa`, order 1 and order 2, on the pitch series.
- Three-pitch share: the share of notes on the song's three commonest pitches.
- Read twice: on every note, and on the notes that start a syllable (melisma notes left out), as the writer's scorer reads attacks. The every-note reading is primary.

**The rule.**
- **They trade** if Spearman's rho between surprise and DFA-1 is +0.20 or more with p < .05 (more surprise goes with pinker pitches).
- **They do not trade** if |rho| < 0.10.
- **Weak** in between, or the other sign (plainer goes with pinker), reported as found.
- **A region where both hold exists** if at least 20% of kept songs have surprise at or under the kept median and DFA-1 at or over the kept median. Its quartiles of DFA-1, DFA-2 and three-pitch share are then the band the gates should use.
- Also reported, deciding nothing: rho for DFA-2 and for the three-pitch share against surprise and against DFA-1; the same on syllable attacks; where song 62's engine draw, first edition and pink survivor fall (percentiles).

**What I expect.** A weak trade: rho about +0.1 to +0.25, and a region holding about 15% to 25% of the kept songs. Held loosely.

**What it cannot say.** Kept songs are chart hits, 4/4, and transcribed by ear; DFA on a few hundred notes is noisy.
