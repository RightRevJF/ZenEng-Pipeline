# Way 4 (surprising at first, inevitable after), with the other AI's ideas 2 and 5 folded in. Written before any surprise was computed (18 Nov 2026).

THE GRADED SET (graded.py; built first, nothing measured on it yet): 2,252 Hooktheory songs joined to the Hot 100 record (peak, weeks), of which 1,795
have 40 notes or more; 210 CoCoPops Billboard whole songs (peak, weeks); 194 Rolling Stone whole songs (the list's rank; 128 with a chart record);
318 BiMMuDa year-end top-five songs. The old record was 131 songs.

THE TWO LISTENERS. Each note is read as two symbols: the interval from the note before (clipped to an octave either way) and the time since the note before
(in sixteenths, capped at two bars). A variable-order model (orders 0 to 4, PPM method C, interpolated) gives each symbol a probability; surprise is minus log2.
  The STRANGER knows other songs and not this one: the model trained on every Hooktheory clip except clips of a song with the same title.
  The LEARNER is the stranger who has also heard this song up to the note in hand: the stranger's model mixed with the same kind of model trained on the song
  so far, each weighted by how sure it is (inverse entropy).
Per song: S = the stranger's mean surprise a note (pitch + rhythm bits); L = the learner's; GAIN = S - L; SHARE = GAIN / S (how much of the surprise the song
teaches away); LATE = the gain in the song's second half minus its first; END = the learner's surprise on a phrase's last note (a note followed by a rest of
two beats or more) minus on the other notes (under zero = endings are the surest notes).

PRIMARY SET: Hooktheory joined, 40 notes or more. Outcome: peak (reversed, higher = better) and weeks, each holding year and the count of notes (partial Spearman).
REPLICATION: CoCoPops Billboard whole songs, the same outcomes. THIRD: Rolling Stone against CoCoPops Billboard (which set, holding year), and rank inside the list.
A measure WORKS only if, on the primary set, its partial correlation with peak or with weeks is 0.10 or more in the predicted direction at p under 0.005
(ten tests), AND it has the same sign at 0.05 or more on the replication set. Anything less is not built into the engine.

F1. SHARE relates to faring better (over 0): the song that teaches its own surprises away does better. This is the claim itself.
F2. S alone relates to nothing (|rho| under 0.05): stage 7 found average surprise does not rank songs.
F3. Inverted U: songs whose S is nearest the median S fare better than songs at either end (minus |S - median| over 0).
F4. LATE over 0 relates to faring better: the gap grows as the song goes on.
F5. END under zero in three songs in four (a description of songs, not of grade), and no relation of END to grade.
F6. Rolling Stone songs have higher SHARE than CoCoPops Billboard songs (AUC over 0.55), holding year.
What I expect, honestly: F2 and F5 hold. F1 is the real test; on clips of 65 notes the learner has little to learn, so the primary set may be too short to
show it and the whole songs (CB, RS) may show it without the numbers to prove it. I put F1 holding by the rule above at one chance in five.
