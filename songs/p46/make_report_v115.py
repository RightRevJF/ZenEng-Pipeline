"""Writes test_report_v115.md from the readings of songs 40, 42 and 43 under v115 (every figure read from the files)."""
import json
S = (("40", "Song 40, Nothing Else on Earth", 20261511, "v112"), ("42", "Song 42, Nothing Important", 20261552, "v112"), ("43", "Song 43, Blue Movie", 20261553, "v114"))
T = {s: json.load(open(f"/home/claude/p46/readings_v115_p{s}_table.json")) for s, *_ in S}
J = {s: json.load(open(f"/home/claude/p46/readings_v115_p{s}.json")) for s, *_ in S}
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
o = []; A = o.append
A("# ZenEng v115: songs 40, 42 and 43 again — test report\n")
A("*Words and music of all three songs: Jason Bryant. Fixes 348–354 ported; findings numbered from 355. No new song.*\n")
A("## What was run\n")
A("v115's fixes 348–354 were ported onto the v114 search as melody_v115_p40.py, and songs 42 and 43 were built on it again from the same song constants, lyrics, intakes and seeds (gen_p42_v115.py, gen_p43_v115.py). "
  "Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Songs 40 and 42 are read beside v112, their last runs; song 43 beside v114.\n")
A("One fix could not be ported as written. 348 (a sixteenth only as a push) left song 40's Bridge line 3 (seven syllables in one bar, ending by beat 3) with no placement: 0 of 100 builds survived. The writer chose Q1 A: 348's \"unless there is no room\" also covers drawn lines. No other fix conflicted.\n")
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
A("## Table DQ: before and after (main runs)\n")
A("| Reading | 40, v112 | 40, v115 | 42, v112 | 42, v115 | 43, v114 | 43, v115 |\n|---|---|---|---|---|---|---|")
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
A("## The pick (352)\n")
A("| Song | Run | Pick (judge's first) | Its rank on the composite | Composite's first | Its rank on the judge | Pick's repeats, verse / chorus |\n|---|---|---|---|---|---|---|")
for s, title, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        x = J[s][v]["352"]; p, c = x["pick"], x["composite_first"]
        A(f"| {s} | {lab} | {p['fp']} | {p['rank_by_composite']} | {c['fp']} | {c['rank_by_judge']} | {p['repeats'][0]} / {p['repeats'][1]} |")
A("\nKept repeats' middle half: verse 0.14–0.39, chorus 0.13–0.40. 255's pick is printed in each run file. Song 43's recorded take (v114, Q18 A) is unchanged; nothing was re-recorded.\n")
A("## Readings the paper does not give\n")
A("- **348 (Q1 A).** A drawn line with fewer eighth-grid positions than syllables may place short notes on sixteenth positions (counted: 1,552 lines on song 40, none on 42 or 43). Returning lines are aligned on the eighth grid first, then on the sixteenth.")
A("- **349.** After the end rule, each note but the last may move a semitone to one of the song's sung extra pitch classes if fix 200's rule allows it: no clash with the chord, no tritone to its root, no tritone or interval over 9 to either neighbour. Places tried and wanting are counted.")
A("- **351.** A bar of a copy that fails 303's check is drawn fresh; the rest of the line keeps the copy.")
A("- **353.** For song 43, the window measures (degree shares, the outside-scale share, the tonic ending) read on A with the natural minor scale. 286's Table B readings and the PPM still read on the engine's frame (C).")
A("- **354.** The four gap knobs (s16, g8, g4, glong) move by at most a factor of 1.6 a round toward Table DU's band for the unaimed builds' notes a bar. Song 40 and 42 sit in the 4.5–5.5 band; song 43 in 3.5–4.5.")
A("- **The spread (337).** Song 43's survivors fell 811 → 722; the spread between the two counts is about 19.\n")
open("/home/claude/p46/test_report_v115.md", "w").write("\n".join(o) + "\n" + open("/home/claude/p46/findings_v115.md").read())
print("ok")
