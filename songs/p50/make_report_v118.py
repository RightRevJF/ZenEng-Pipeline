"""Writes test_report_v118.md from the readings of songs 40, 42, 43, 44 and 45 under v118 (every figure read from the files), then the findings."""
import json, re, os
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
H = "/home/claude/p50"
T = {s: json.load(open(f"{H}/readings_v118_p{s}_table.json")) for s, *_ in S}
J = {s: json.load(open(f"{H}/readings_v118_p{s}.json")) for s, *_ in S}
SEP = json.load(open(f"{H}/sep_v118.json")); SEP6 = json.load(open(f"{H}/sep_v116_true.json")); SEP5 = json.load(open(f"{H}/sep_v115_true.json"))
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
o = []; A = o.append
A("# ZenEng v118: songs 40, 42, 43, 44 and 45 again — test report\n")
A("*Words and music of all five songs: Jason Bryant. Fixes 365–383 ported (Windows 137 and 138, Modules 27.61 and 27.62) without editing the paper; findings numbered from 384. No new song. Song 45 as drawn, without the writer's hand edits.*\n")
A("## What was run\n")
A("v117's and v118's fixes were ported onto the v116 search as melody_v118_p40.py (gen_v118_p40.py), and songs 42, 43, 44 and 45 were built on it again from the same song constants, lyrics, intakes, designs and seeds "
  "(gen_p42_v118.py to gen_p45_v118.py). The new tables are on file in songs/p50/tables: the kept rhythm tables (372), the kept songs and modes (369), the yardstick (374), and the slot and surprisal counts (378, 382). "
  "Each song ran 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0. Song 43 ran twice more for 368 (main, 1,000): with fix 358 off and with fix 361 off. "
  "Each song is read beside its v116 runs (Table DQ; songs 44 and 45 beside their first runs, which were on the v116 port).\n")
A("| Song | Run | Survivors (v116) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v118.md").read().strip().splitlines(): A(line)
A("")
A("## The gap knobs (372)\n")
A("Every knob of 354, 355, 365 and 366 started at one. Final values; a knob more than a factor of two from one is marked.\n")
A("| Song | Run | s16 | g8 | g4 | glong | run (366's rate) | on16 |\n|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        k = J[s][v]["372"]["knobs"]
        A(f"| {s} | {lab} | " + " | ".join((f"**{k[x]['final']}**" if k[x]["past_a_factor_of_two"] else f"{k[x]['final']}") for x in ("s16", "g8", "g4", "glong", "run", "on16")) + " |")
A("")
for s, title, seed in S:
    rows = T[s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows:
        if k in ("369", "374"): a = b = "see Separability"; h = "below"
        A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("## Table DQ: v116 and v118 (main runs)\n")
A("| Reading | " + " | ".join(f"{s}, v116 | {s}, v118" for s, *_ in S) + " |\n|---|" + "---|" * (2 * len(S)))
for k in J["40"]["main"]["DQ"]["now"]:
    f = lambda x: f"{x:.1%}" if k.startswith("builds") and isinstance(x, float) else str(x)
    A(f"| {k} | " + " | ".join(f"{f(J[s]['main']['DQ']['before'][k]) if J[s]['main']['DQ']['before'] else '-'} | {f(J[s]['main']['DQ']['now'][k])}" for s, *_ in S) + " |")
A("")
A("## 340: the eight costliest measures (points; kept mean, builds' mean)\n")
for s, title, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        x = J[s][v]["340"]
        A(f"- **{title}, {lab}** (gap {x['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]:.3f}, {e[3]:.3f})" for e in x["eight"]))
A("")
x = J["43"]["main"]["359"]
A("## 359 on song 43 (369): against the 70 kept minor windows\n")
A(f"Gap against the minor means {x['gap_minor']} (against all 314 windows {x['gap_all']}). Outside the scale: builds {x['outside_scale']['builds']:.1%}, kept minor mean {x['outside_scale']['minor_mean']:.1%}; "
  f"cost {x['outside_scale']['cost_minor']} against the minor means ({x['outside_scale']['cost_all']} against all). The eight costliest against the minor means: "
  + "; ".join(f"{e[0]} {e[1]} ({e[2]:.3f}, {e[3]:.3f})" for e in x["eight_minor"]) + ". The judge of record is used (70 windows are too few to fit one); the costs are 340's fresh judge read against the minor means.\n")
A("## The pick (362)\n")
A("| Song | Run | Pick | Its rank on the judge | The judge's first | Survivors with no soft break |\n|---|---|---|---|---|---|")
for s, title, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        x = J[s][v]["362"]; p = x["pick"]
        A(f"| {s} | {lab} | {p['fp']} | {p['rank_by_judge']} | {x['judges_first']['fp']} | {x['survivors_with_no_soft_break']} of {x['survivors']} |")
A("\nNo recorded take is changed; nothing was re-recorded. Song 45's record keeps the writer's edits (Q16 A); this run is the engine's, as drawn (383: no hand edits here).\n")
A("## Separability (364, 369, 372, 374)\n")
A(f"A judge fitted fresh (340's) on kept windows against a run's builds, tested on held-out kept songs and held-out builds (AUC), the first 400 complete builds of each main run. Kept windows split by their true songs ({SEP['kept_songs']} songs, 369). "
  f"Beside the yardstick (374): kept 1958–1969 against 1980–1991, 0.57; the 1960s against the 1970s, 0.63.\n")
A("| Reading | Window 136 (v115) | This code on v115 | v116 | v118 |\n|---|---|---|---|---|")
W136 = {"40": 0.966, "42": 0.954, "43": 0.942}
for s, *_ in S: A(f"| within song {s} | {W136.get(s, '—')} | {SEP5['within'].get(s, '—')} | {SEP6['within'].get(s, '—')} | {SEP['within'].get(s, '—')} |")
A(f"| across songs, mean | 0.909 (three songs) | {SEP5['across_mean']} (three songs) | {SEP6['across_mean']} (five songs) | {SEP['across_mean']} (five songs) |")
A("| the yardstick | 0.57 and 0.63 | | | |\n")
A("## 368's diagnostic runs (song 43, main, 1,000; memory read with 373's limit, soft 0.12)\n")
x = J["43"]["main"].get("368", {})
if x:
    A("| Run | Survivors | Memory breaks | Order |\n|---|---|---|---|")
    A(f"| v114, read again | — | {x['v114']} | — |")
    A(f"| v118 as run | {J['43']['main']['runs']['survivors']} | {x['memory_breaks_now']} | {J['43']['main']['runs']['order']} |")
    for k_, d_ in x["diagnostics"].items(): A(f"| v118, {k_} off | {d_['survivors']} | {d_['memory']} | {d_['order']} |")
    A("")
A("## The seven limits of 286 and their corpus (373, 382)\n")
A("| Limit | Rule as run | Corpus |\n|---|---|---|")
for k_, (rule, corp) in J["40"]["main"]["373"]["limits"].items(): A(f"| {k_} | {esc(rule)} | {corp} |")
A("")
A("## Readings the paper does not give\n")
for line in open(f"{H}/readings_notes_v118.md").read().strip().splitlines(): A(line)
A("")
open(f"{H}/test_report_v118.md", "w").write("\n".join(o) + "\n" + open(f"{H}/findings_v118.md").read())
print("ok")
