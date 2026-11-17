# Metre study (16 November 2026)

For the Doc "Metre research for Luthier v8: bars, phrases and hypermeter" (https://claude.ai/artifact/4i2phRJCimMJTCPJo95Sqi).

Data (not kept here): CoCoPops Billboard, github.com/Computational-Cognitive-Musicology-Lab/CoCoPops (CC BY-NC 4.0; derived counts only),
cloned to /home/claude/data/cocopops/CoCoPops. Uses studies/tension/parse_cocopops.py for kern durations.

| Script | Writes | What |
| --- | --- | --- |
| lines_cocopops.py | cocopops_lines.json (not committed) | 9,313 sung lines in 198 songs in 4/4: syllables, start, slot, span, inner rests, section, bar length in seconds |
| metre_test.py | metre_results.json | slots by syllables and tempo, syllables a second, line starts in the four-bar group, pickups, one-bar lines, inner rests, odd sections |
