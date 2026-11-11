"""Writes test_report_v112.md from the readings of songs 40 and 42 under v112 (every figure read from the files)."""
import json
T = {s: json.load(open(f"/home/claude/p44/readings_v112_p{s}_table.json")) for s in ("40", "42")}
J = {s: json.load(open(f"/home/claude/p44/readings_v112_p{s}.json")) for s in ("40", "42")}
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
o = []; A = o.append
A("# ZenEng v112: songs 40 and 42 once more — test report\n")
A("*Words and music of both songs: Jason Bryant. Fixes 330–336 ported; findings numbered from 337. No new song.*\n")
A("## What was run\n")
A("v112's fixes 330–333 were ported onto the tested v111 search (songs/p43/melody_v111_p40.py) as melody_v112_p40.py, and song 42 was built on it again from the same song constants (gen_p42_v112.py). 334–336 are the report's: every tempo band's quartiles, each test named against its kept figure or marked a reading, and the floor's share a reading. Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Nothing blocked the port and no two fixes conflicted.\n")
A("| Song | Run | Survivors (v111) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, seed in (("40", 20261511), ("42", 20261552)):
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
for s, title in (("40", "Song 40, Nothing Else on Earth"), ("42", "Song 42, Nothing Important")):
    rows = T[s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("## Table DR again: v111 and v112 (main runs)\n")
A("| Reading | Song 40, v111 | Song 40, v112 | Song 42, v111 | Song 42, v112 | Kept |\n|---|---|---|---|---|---|")
KEPT = {"builds under the judge's floor": "5%", "content judge, median": "4.16 (25th 1.33)", "order judge, median": "1.58 (25th 0.05)", "likeness of bar rhythms between lines": "0.14 (0.04 to 0.23)",
        "arch term over the line's span": "0.23 (0.00 to 0.55)", "leaps past a fifth, verse, % of moves": "0 (75th 3.6)", "the song's sung range, semitones": "17 (14.5 to 22)", "range in eight bars, verse / chorus": "10 (8 to 13)"}
for k in J["40"]["main"]["DQ"]["now"]:
    f = lambda x: f"{x:.1%}" if k.startswith("builds") and isinstance(x, float) else str(x)
    A(f"| {k} | {f(J['40']['main']['DQ']['before'][k])} | {f(J['40']['main']['DQ']['now'][k])} | {f(J['42']['main']['DQ']['before'][k])} | {f(J['42']['main']['DQ']['now'][k])} | {KEPT.get(k, '—')} |")
for s in ("40", "42"):
    x = J[s]["main"]["336"]
A("")
A("## 336's readings (main run, control in brackets)\n")
A("| Reading | Song 40 | Song 42 | Kept |\n|---|---|---|---|")
def two(s, f): return f"{f(J[s]['main']['336'])} (control {f(J[s]['ctl']['336'])})"
for lab, fn, kept in (("builds under the floor", lambda x: f"{x['under_floor']:.1%}", "5%"), ("content judge, median", lambda x: str(x["content"]["median"]), "4.16"),
                      ("builds at the kept 25th / median, content", lambda x: f"{x['content']['at_kept_25th']:.1%} / {x['content']['at_kept_median']:.1%}", "75% / 50%"),
                      ("order judge, median", lambda x: str(x["order"]["median"]), "1.58"),
                      ("builds at the kept 25th / median, order", lambda x: f"{x['order']['at_kept_25th']:.1%} / {x['order']['at_kept_median']:.1%}", "75% / 50%"),
                      ("content measures (of 46) with the median outside the kept middle half", lambda x: str(x["outside_kept_middle_half"]), "—"),
                      ("heaviest single content give-away", lambda x: f"{x['heaviest_give_away'][0]} {x['heaviest_give_away'][1]}", "—")):
    A(f"| {lab} | {two('40', fn)} | {two('42', fn)} | {kept} |")
A("")
open("/home/claude/p44/test_report_v112.md", "w").write("\n".join(o) + "\n" + open("/home/claude/p44/findings_v112.md").read())
print("ok")
