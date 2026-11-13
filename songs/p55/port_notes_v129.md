Every fix is a whole-statement patch in gen_v129.py, gated by ON9() at ZE_PART=1. ZE_PART=0 reproduces Run 3: song 43 main, 9fab8a9e1e46, 872 survivors, matched.

- **500.** 465's class share is the product of the kept share for the line's notes and the kept share for its slot's beats (one bar 4, two bars 8, longer 12–16), over the kept classes' overall share. A class with a share that the slot cannot reach is counted by notes and slot.
- **501.** 414's seconds bound is off. For half its tries, a drawn line's onsets a beat between its first and last onset must lie in the kept 25th–75th for its notes (zeneng_v128_kept_lines.json). After that the bound is given up and counted.
- **502.** Song 45's chorus floor is the verse's median plus three, capped at the chorus top less three (Run 2's Part 2).
- **503.** One knob, ctb503, weighs a chord tone on the beat in the sing-again walk. It is aimed on unaimed builds at verse 1's chord tones on the beat in the same builds (the engine's windows).
- **504.** 452's band knobs are keyed by the line's own notes a bar: its syllables per slot bar times the song's notes to syllables in the judged windows, read on unaimed builds. The zigzag knob takes the band of the line being walked.
- **505.** 389's rate is held at one. The run weight (490) alone is aimed, on every section of the band, with this round's unaimed builds and the last round's pooled (60).
- **508.** A return or sung-again line that follows a designed line known ahead (song 45's FIXR) is fitted with the breath that line's last onset needs (GAP_MIN) in place of the open −12.
  - This is where song 45's joins before a copy died: the last chorus's first line is designed, and the return after it took a pickup from its source.
- **513.** After the inversions are drawn, each is tested on the finished chart. One with no step to a neighbouring change is taken back, and the test is repeated.
- **519.** The content judge of record is zeneng_v129_judge.json. The share of complete builds under the kept songs' 5th percentile (−0.72) is printed; 254's floor stays on the v108 judge.
- **520.** 455 is withdrawn (its weight was already one under 490). 408's width knob is gone from the knobs and the record, and S16B is out of the record. Turns stay with 400's knob, and 468 is kept. The window's range is printed beside each song's design and not aimed.
- **512.** A test that no kept song passes read as a build is read (0% in kept_pass_v129.json) is shown as a reading of the mean of builds, not as held or not held.
- **516.** 448's 35–59% of notes on a kick is read on the bars that have a kick.
- **517.** The bass's eight bars are A B A C A B D E: a third cell, D, in the second four bars, and its fill, E. The record's seed is new ("… v129").
- **518.** Not ported to these songs: their picks stand on the charts they were drawn on. It applies to the next song (522).
- **The reread (519).** Window 147's measures are kept for comparison with the earlier runs, but its window is now the engine's: every note sung in the eight bars, the chord at the note. Run 3 is read again the same way.
