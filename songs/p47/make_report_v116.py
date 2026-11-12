"""Writes test_report_v115.md from the readings of songs 40, 42 and 43 under v115 (every figure read from the files)."""
import json
S = (("40", "Song 40, Nothing Else on Earth", 20261511, "v112"), ("42", "Song 42, Nothing Important", 20261552, "v112"), ("43", "Song 43, Blue Movie", 20261553, "v114"))
T = {s: json.load(open(f"/home/claude/p47/readings_v116_p{s}_table.json")) for s, *_ in S}
J = {s: json.load(open(f"/home/claude/p47/readings_v116_p{s}.json")) for s, *_ in S}
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
o = []; A = o.append
A("# ZenEng v116: songs 40, 42 and 43 again — test report\n")
A("*Words and music of all three songs: Jason Bryant. Fixes 355–364 ported (359 not: Q1 A); findings numbered from 365. No new song.*\n")
A("## What was run\n")
A("v116's fixes 355–363 were ported onto the v115 search as melody_v116_p40.py, and songs 42 and 43 were built on it again from the same song constants, lyrics, intakes and seeds (gen_p42_v116.py, gen_p43_v116.py). "
  "Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Song 43 ran twice more for 356 (main, 1,000): with fix 348 off (and 355, which amends it), and with fix 354 off. "
  "The same two switches were also run on v115's song 43 code, where the breaks were made. Every song is read beside v115 (Table DQ), and 356's counts beside v112 (songs 40 and 42) and v114 (song 43).\n")
A("Two fixes could not be ported as written. 359 needs the key of each kept window and 364 needs its song; the kept-window table has neither. The writer chose Q1 A: 359 stays as v115, with every cost read against all 314 windows, and 364 groups kept windows into songs by runs of adjacent windows with the same year (an inference, labelled).\n")
A("| Song | Run | Survivors (before) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, title, seed, _ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
for s, title, seed, bv in S:
    rows = T[s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("## Table DQ: v115 and v116 (main runs)\n")
A("| Reading | 40, v115 | 40, v116 | 42, v115 | 42, v116 | 43, v115 | 43, v116 |\n|---|---|---|---|---|---|---|")
for k in J["40"]["main"]["DQ"]["now"]:
    f = lambda x: f"{x:.1%}" if k.startswith("builds") and isinstance(x, float) else str(x)
    A(f"| {k} | " + " | ".join(f"{f(J[s]['main']['DQ']['before'][k])} | {f(J[s]['main']['DQ']['now'][k])}" for s, *_ in S) + " |")
A("")
A("## 340: the eight costliest measures (points; kept mean, builds' mean)\n")
for s, title, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        x = J[s][v]["340"]
        A(f"- **{title}, {lab}** (gap {x['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]:.3f}, {e[3]:.3f})" for e in x["eight"]))
A("")
A("## The pick (362)\n")
A("| Song | Run | Pick | Its rank on the judge | The judge's first | Survivors with no soft break |\n|---|---|---|---|---|---|")
for s, title, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        x = J[s][v]["362"]; p = x["pick"]
        A(f"| {s} | {lab} | {p['fp']} | {p['rank_by_judge']} | {x['judges_first']['fp']} | {x['survivors_with_no_soft_break']} of {x['survivors']} |")
A("\nSong 43's recorded take (v114, Q18 A) is unchanged; nothing was re-recorded.\n")
SEP = json.load(open("/home/claude/p47/sep_v116.json")); SEP5 = json.load(open("/home/claude/p47/sep_v115_check.json"))
A("## Separability (364)\n")
A(f"A judge fitted fresh (340's) on kept windows against a run's builds, tested on held-out kept songs and held-out builds (AUC), on the first 400 complete builds of each main run. Kept songs: {SEP['kept_songs_read']}, by the inferred grouping (Q1 A).\n")
A("| Reading | Window 136 (v115) | This code on v115 | v116 |\n|---|---|---|---|")
for s, w in (("40", 0.966), ("42", 0.954), ("43", 0.942)): A(f"| within song {s} | {w} | {SEP5['within'][s]} | {SEP['within'][s]} |")
A(f"| across songs, mean of six | 0.909 | {SEP5['across_mean']} | {SEP['across_mean']} |")
A("| across, by pairing | — | " + ", ".join(f"{k} {v}" for k, v in SEP5["across"].items()) + " | " + ", ".join(f"{k} {v}" for k, v in SEP["across"].items()) + " |\n")
A("## 356's diagnostic runs (song 43, main, 1,000)\n")
A("| Code | Run | Survivors | Rhythm-band breaks | Memory breaks | Order |\n|---|---|---|---|---|---|")
import re
def rd_(f):
    t = open(f).read(); g = lambda pat: (re.search(pat, t).group(1) if re.search(pat, t) else "0")
    return g(r"survivors (\d+)"), g(r"(\d+)  limit broken: rhythm band"), g(r"(\d+)  limit broken: memory"), g(r"order (\w+)")
for code, lab, f in (("v114", "as run", "/home/claude/p45/run43_main.txt"), ("v115", "as run", "/home/claude/p46/run43_main.txt"), ("v115", "348 off", "/home/claude/p47/run43v115_main_off348.txt"),
                     ("v115", "354 off", "/home/claude/p47/run43v115_main_off354.txt"), ("v116", "as run", "/home/claude/p47/run43_main.txt"), ("v116", "348 (and 355) off", "/home/claude/p47/run43_main_off348.txt"),
                     ("v116", "354 off", "/home/claude/p47/run43_main_off354.txt")):
    a_, b_, c_, d_ = rd_(f); A(f"| {code} | {lab} | {a_} | {b_} | {c_} | {d_} |")
A("")
A("## Readings the paper does not give\n")
A("- **355.** The run knob weights a sixteenth-position onset followed by a sixteenth; it moves on a log scale ((0.31 / reading) to the fourth, between a tenth and ten times a round), since one weight acts across all of a line's paths. A second knob weights every onset on a sixteenth position toward the kept 9.4%.")
A("- **356.** The rhythm band's middle half is taken from a normal band fitted to 286's soft limits as its 5th and 95th percentiles: 1.98–2.53. The distinct lengths' middle half is the kept windows' quartiles. A stop freezes all four 354 knobs for the rest of the calibration.")
A("- **357.** A round past the third runs only if a knob moved at full step in the round before (the 1.6 cap, or the run knob's tenfold).")
A("- **358.** The passing note is a semitone move to a pitch class outside the scale, off the beat, one or two semitones from both neighbours. 215's tritone move after the walk leaves it alone, so a copied line keeps it too.")
A("- **360.** The refit draws the line again once, with any onset off the copy forbidden in the failed bars.")
A("- **361.** Song 40's sections are not all two-bar lines and take the bar grid; songs 42 and 43 are all two-bar lines and keep 350's line plans. A fresh line on a returning unit takes the earlier unit's onsets bar by bar, and its pitches where the chord allows them (else as the contour). A paired line (310) keeps its partner.")
A("- **The spread (337).** Song 40's survivors rose 602 → 701 (spread about 21); song 43's 722 → 798 (spread about 19).\n")
open("/home/claude/p47/test_report_v116.md", "w").write("\n".join(o) + "\n" + open("/home/claude/p47/findings_v116.md").read())
print("ok")
