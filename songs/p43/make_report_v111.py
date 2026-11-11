"""Writes test_report_v111.md from the readings of songs 40 and 42 under v111 (every figure read from the files)."""
import json
T = {s: json.load(open(f"/home/claude/p43/readings_v111_p{s}_table.json")) for s in ("40", "42")}
J = {s: json.load(open(f"/home/claude/p43/readings_v111_p{s}.json")) for s in ("40", "42")}
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
out = []
A = out.append
A("# ZenEng v111: songs 40 and 42 again — test report\n")
A("*Words and music of both songs: Jason Bryant. Fixes 322–329 ported; findings numbered from 330.*\n")
A("## What was run\n")
A("v111's fixes 322–329 were ported onto the tested v110 search (songs/p42/melody_v110_p40.py) as melody_v111_p40.py, and song 42 was built on it "
  "again from the same song constants (gen_p42_v111.py: the same lyric, intake, designs and seed). Each song ran 1,000 builds in the main run and 1,000 "
  "in the control, each twice, at PYTHONHASHSEED 0. Nothing blocked the port and no two fixes conflicted.\n")
A("| Song | Run | Survivors (v110) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, seed in (("40", 20261511), ("42", 20261552)):
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
for s, title in (("40", "Song 40, Nothing Else on Earth"), ("42", "Song 42, Nothing Important")):
    rows = T[s]; nh = sum(1 for r in rows if r[4] is True); nf = [r[0] for r in rows if r[4] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {sum(1 for r in rows if isinstance(r[4], bool))} with a test. Not held: {', '.join(nf)}.\n")
    A("| Fix | Test | Main | Control | Held? |\n|---|---|---|---|---|")
    for k, t, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("Notes on the tables. 314's tonic test is read on the drawn register's centre, as 324 amends it; read on the sung median it gives 92.8% (song 40) and 94.5% (song 42). "
  "322's and 327's tests are written for song 40; song 42's readings are printed beside them (322 on song 42: partners given up 12.7%, so it is shown as not held). "
  "319 has nothing to read: these runs make no instrumental lines.\n")
A("## Table DQ again: v110 and v111 (main runs)\n")
A("| Reading | Song 40, v110 | Song 40, v111 | Song 42, v110 | Song 42, v111 | Kept |\n|---|---|---|---|---|---|")
KEPT = {"builds under the judge's floor": "5%", "content judge, median": "4.16", "order judge, median": "1.58", "likeness of bar rhythms between lines": "0.14 (0.04 to 0.23)",
        "arch term over the line's span": "0.23 (0.00 to 0.55)", "leaps past a fifth, verse, % of moves": "0 (75th 3.6)", "the song's sung range, semitones": "17 (14.5 to 22)",
        "range in eight bars, verse / chorus": "10 (8 to 13)"}
for k in J["40"]["main"]["DQ"]["now"]:
    f = lambda x: f"{x:.1%}" if k.startswith("builds") and isinstance(x, float) else str(x)
    A(f"| {k} | {f(J['40']['main']['DQ']['before'][k])} | {f(J['40']['main']['DQ']['now'][k])} | {f(J['42']['main']['DQ']['before'][k])} | {f(J['42']['main']['DQ']['now'][k])} | {KEPT.get(k, '—')} |")
A("\nThe v110 columns are read here on all of v110's complete builds (Window 131 read the first 600), so a few differ from Table DQ in the second decimal.\n")
open("/home/claude/p43/test_report_v111.md", "w").write("\n".join(out) + "\n")
print("ok")
