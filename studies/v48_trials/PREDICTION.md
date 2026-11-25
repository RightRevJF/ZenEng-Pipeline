# Three trials for v48: checks written before any run

25 November 2026. The list is `songs/p68/fixlist_v48.md` (the session's, Review 32). Seen before writing: v47's results (`studies/proposed_v47`), and the kept quartiles of chord repetition that the code prints (verse median 0.333 and 75th 0.50 in major; bridge 0.0 and 0.357). Nothing has been run under any of the three forms. The forms are in the code behind switches that are off (`LUTHIER_OCTAVE`, `LUTHIER_TITLE`, `LUTHIER_LOOP`), so the engine as committed here is v47.

A thousand builds a song throughout. Words' fit is read on the builds' middle (749.175).

## 1. The octave gate as kept songs have it (749.176)

**Form.** A build may hold one leap past an octave inside a line in the whole song, and no more (`"one"`), in place of none.

**Checks (the session's), on songs 55, 54, 58:**
1. Living builds above v47's in each song (223, 256, 294).
2. A random pool pick fails the soundness rule with the upper end of its range under 5.4 in 100 (v46's).
3. No chosen tune holds more such leaps than the kept 90th (4.4 in a thousand notes).
4. Builds' middle words' fit within 0.02 of v47's (0.263, 0.218, 0.296).
5. The three-song soundness rule holds.

All five, or the ban stands.

**What I expect.** 1, 3, 4 and 5 to hold. Check 2 is the doubt: the ban took the pools from 39, 25, 39 to 24, 23, 22, and one leap allowed should give back most but not all of the builds. I put it at even.

## 2. Where a title line's longest note falls (749.177)

**The reading.** The kept songs (`kept_corpus.kept_songs()`, CoCoPops, 4/4). The title is read from the file's name; a title line is a sung line that holds the title's words in order. Syllables are weighed as the kept word table does (`make_kept_word_weight.tiers`): stressed, or weak (a weak syllable of a longer word, or a one-syllable function word). Lines with a word the lexicon does not hold are left out. The longest note is the first of the longest, as the engine's gate reads it. Each title line falls in one of four: **stressed**; **weak, the line's last syllable**; **weak, in the last word but not its last syllable**; **weak, before the last word**. Counted by line, and by song (the share of a song's title lines in each).

**Rule.** If "weak, before the last word" is under 10 title lines in 100 and under 10 in 100 by song at the median song... the second is always true where the first is, so: **under 10 lines in 100.** Then the narrower gate is tried: a build is passed over if a title line's longest note is on a weak syllable before the line's last word (`"inside"`). If the kept share is 10 or more, the gate is not tried and 961 stays a setting as it is.

**Checks for the gate (the session's), on songs 54, 49 and 62:**
1. Song 62's chosen tune has no title line with its longest note on a weak syllable before the last word.
2. In songs 54 and 49 the gate passes over no more than 5 of every 100 builds that live without it.

If both hold, I add two of my own before it can be a default, since four songs fooled us last time: the same 5 in 100 on songs 55 and 58; and the build's pool check (section 4). If the session's two hold and mine do not, the form replaces 961's as the setting and is not a default.

**What I expect.** The kept share before the last word to be small, 5 to 10 in 100, since kept lines end long. The gate to cost under 5 in 100 everywhere. I have been wrong about this gate once.

## 3. The gentler loop gate (749.178)

**Form.** A verse or bridge is drawn again (30 times at most) only if its chord repetition is over the kept 75th for its kind and mode; the others stand as drawn (`"gentle"`).

**Checks (the session's), on a thousand drafted sections a kind, major, as `studies/proposed_v47/drafts.py` drew them:**
1. The share of verses at or under the kept median between 45 and 60 in 100.
2. The share of verses that are plain loops within 5 points of the kept share (30 in 100; the stage 4 reading `loops`).
3. The stage 4 readings (first, last, chords, bigrams, bars; verse and bridge) no further from held-out kept sections than the unpatched writer's by more than 0.02.

Minor is reported and decides nothing (35 kept bridges).

**Then song 63, once,** only if all three hold: `songs/p73/lyric63.json` run by the engine as built for v48 with the form on. A single song cannot check a share; what it can check is that the form does on a fresh lyric what it did on the seen ones and breaks nothing:
- its chosen plan's verse and bridge are at or under the kept 75th;
- its pool is 10 builds or more, and its builds' middle words' fit is at or over the kept 10th (the words gate's own floor).

The ledger line goes into `studies/judging_data/README.md` with this commit. If the seen-song checks fail, song 63 is not run.

**Whatever happens, 960 stays a setting.** If the form passes on both it replaces the median form as what `"chords": "loop_less"` means. It becomes a default only when the covers question is settled.

**What I expect.** The unpatched writer has 45 verses in 100 at or under the median already. Trimming the top quarter should push that up a little, to 50 or 55, so check 1 should hold; check 2 should hold (the gate barely touches plain loops, which sit at the top of repetition, so it may cut them: this is the one I doubt); check 3 even.

## 4. The build

v48 is v47 with each form that passed. Before it is called built: the three-song soundness rule; pools of 10 or more and the pool standard (90 in 100); builds' middle words' fit within 0.02 of v47's; floor and ceiling; song 53 byte for byte; song 52 reported; song 59 read.
