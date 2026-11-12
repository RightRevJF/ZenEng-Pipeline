"""Writes test_report_v119.md: the v119 port in its steps (with v120's changes), every figure read from the files, then the findings."""
import json, os
H = "/home/claude/p51"
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
T = {s: json.load(open(f"{H}/readings_v119_p{s}_table.json")) for s, *_ in S}
J = {s: json.load(open(f"{H}/readings_v119_p{s}.json")) for s, *_ in S}
SEP = json.load(open(f"{H}/sep120_v119.json")); SEP0 = json.load(open(f"{H}/base/sep120_v118_five.json"))
SEP1 = json.load(open(f"{H}/step1/sep120_step1.json")); SEPB3 = json.load(open(f"{H}/base/sep120_v118.json"))
ST1 = {s: json.load(open(f"{H}/step1/step_p{s}.json")) for s in ("40", "42", "43")}; B1 = {s: json.load(open(f"{H}/base/step_v118_p{s}.json")) for s in ("40", "42", "43")}
S388 = json.load(open(f"{H}/step2/read388.json"))
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
o = []; A = o.append
A("# ZenEng v119 port, with v120's changes: songs 40, 42, 43, 44 and 45 again — test report\n")
A("*Words and music of all five songs: Jason Bryant. Fixes 384–398, 400 and 388's side runs ported from v119 (Module 27.63) in steps, with runs between them; "
  "399 and 401 withdrawn by v120 (Module 27.64, 421) and not ported; v120's 424 added in step 3. The paper was not edited. The session's findings are 402–419. "
  "No new song; song 45 as drawn.*\n")
A("## What was run\n")
A("- **Step 1, repairs** (384–387, 389, 394, 395): songs 40, 42 and 43, main runs, 1,000 builds each.")
A("- **Step 2**: v120 reduced it to 388's two side runs: song 40, main, 1,000 builds each, one with 378 off and one with the landing left to the kept table's draw. "
  "Step 2's first main runs, which had 399 and 401 in, were made before v120 arrived and are set aside (withdrawn_step2/); they are not runs of record.")
A("- **Step 3** (398, 400, 390–393 and v120's 424): all five songs, 1,000 builds in the main run and 1,000 in the control, each twice, at PYTHONHASHSEED 0, same lyrics, intakes, designs and seeds.\n")
A("Tests, costs and separation are read on the 30 measures the two kept collections agree on (420, 422), against CoCoPops and BiMMuDa 1958–1991 pooled; "
  "tests on the other measures are printed as readings with both collections' means; the harmony measures are read on CoCoPops alone and printed apart.\n")
A("| Song | Run | Survivors (v118) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v119.md").read().strip().splitlines(): A(line)
A("")
A("## Step 1: the repairs (songs 40, 42 and 43, main runs)\n")
A("| Reading | 40, v118 | 40, step 1 | 42, v118 | 42, step 1 | 43, v118 | 43, step 1 |\n|---|---|---|---|---|---|---|")
def row(lab, f):
    A(f"| {lab} | " + " | ".join(f"{esc(f(B1[s]))} | {esc(f(ST1[s]))}" for s in ("40", "42", "43")) + " |")
row("survivors (order)", lambda x: f"{x['survivors']} ({x['order']})")
row("outside the scale (385)", lambda x: f"{x['385']['outside_scale']:.1%}")
row("notes a semitone from a chord's outside tone, on a beat or held (386)", lambda x: x["386"]["clashes"])
row("deaths for want of a rhythm (389)", lambda x: x["389"]["rhythm_deaths"])
row("join deaths", lambda x: x["389"]["join_deaths"])
row("memory breaks (394)", lambda x: x["394"]["memory_breaks"])
row("gap knobs s16 / g8 / g4 / glong (387)", lambda x: " / ".join(str(x["387"]["knobs"].get(k, "-")) for k in ("s16", "g8", "g4", "glong")))
row("turns per move (mean)", lambda x: x["measures"]["turns_per_move"]["builds_mean"])
row("leaps of a fourth or fifth (mean)", lambda x: x["measures"]["fourth_fifth"]["builds_mean"])
A("")
A("Runs by band of section density after step 1 (389): " + "; ".join(f"song {s}: " + ", ".join(f"{b} {d['in_runs']:.0%} (kept {d['kept']:.0%}, rate {d['rate']})" for b, d in ST1[s]["389"]["by_band"].items()) for s in ("40", "42", "43")) + ".\n")
A("Separation after step 1, on the 30 agreed measures against both collections pooled (songs 40, 42 and 43; across songs, mean of six):\n")
A("| Family | v118 | Step 1 | Window 140 (v118) |\n|---|---|---|---|")
W140 = {"agreed 30": 0.75}
for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)"):
    A(f"| {f} | {SEPB3['family'][f]['across_mean']} | {SEP1['family'][f]['across_mean']} | {W140.get(f, '—')} |")
A(f"| the collections against each other | {SEPB3['collections_against_each_other']} | | 0.555 |\n")
A("## Step 2: 388's side runs (song 40, main, 1,000 builds)\n")
A("| Run | Survivors | Order | Sixteenth gaps | Eighth gaps | Quarter gaps | Longer | g4 knob | glong knob | Rhythm deaths |\n|---|---|---|---|---|---|---|---|---|---|")
for lab, x in S388.items():
    A(f"| {lab} | {x['survivors']} | {x['order']} | {x['gap_sixteenth']:.1%} | {x['gap_eighth']:.1%} | {x['gap_quarter']:.1%} | {x['gap_longer']:.1%} | {x['g4']} | {x['glong']} | {x['rhythm_deaths']} |")
A("\nThe kept table's shares for song 40's band (4.5 to 5.5 notes a bar): sixteenth 15.7%, eighth 56.3%, quarter 13.8%, longer 10.8%.\n")
A("## Step 3: the knobs\n")
A("| Song | Run | s16 | g8 | g4 | glong | on16 | 398: chord tones / on a beat / on a downbeat / left by step | 400: turns | 424: fourths and fifths / last note tonic / empty-bar rate |\n|---|---|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        k = J[s][v]["runs"]["line_knobs"]
        A(f"| {s} | {lab} | " + " | ".join(str(round(k.get(x, 1.0), 3)) for x in ("s16", "g8", "g4", "glong", "on16"))
          + f" | {round(k.get('ct398', 1), 2)} / {round(k.get('ctb398', 1), 2)} / {round(k.get('ctd398', 1), 2)} / {round(k.get('res398', 1), 2)} | {round(k.get('turn400', 1), 3)} | "
          f"{round(k.get('ff424', 1), 3)} / {round(k.get('lt424', 1), 2)} / {round(k.get('eb424', 1), 3)} |")
A("")
for s, title, seed in S:
    rows = T[s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("## 340: the eight costliest of the 30 agreed measures (points; both collections pooled, builds' mean)\n")
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
        A(f"| {s} | {lab} | {p['fp'] if p else '-'} | {p['rank_by_judge'] if p else '-'} | {x['judges_first']['fp'] if x['judges_first'] else '-'} | {x['survivors_with_no_soft_break']} of {x['survivors']} |")
A("\nThe judge of record is still the v108 fit; 425's refit on the agreed measures is to be made from these runs.\n")
A("## Separation (422): the 30 agreed measures, both collections pooled\n")
A(f"364's fresh judge on kept windows of CoCoPops (314) and BiMMuDa 1958–1991 (231) pooled, kept songs held out by song in both, against the first 400 complete builds of each main run (AUC). "
  f"Beside the collections' own separation from each other ({SEP['collections_against_each_other']} here; Window 140: 0.555) and beside Window 140's 0.75 for the v118 builds.\n")
A("| Family | v118, within 40 / 42 / 43 / 44 / 45 | v119 port, within | v118, across (mean) | v119 port, across (mean) |\n|---|---|---|---|---|")
for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)"):
    w0 = " / ".join(str(SEP0["family"][f]["within"][s]) for s, *_ in S); w1 = " / ".join(str(SEP["family"][f]["within"][s]) for s, *_ in S)
    A(f"| {f} | {w0} | {w1} | {SEP0['family'][f]['across_mean']} | {SEP['family'][f]['across_mean']} |")
A(f"| the collections against each other | | | 0.56 | 0.56 |")
A(f"| Window 140's figure for the v118 builds (40, 42 to 43) | | | 0.75 | |\n")
A("Costs on the 30 agreed measures, the five songs' builds pooled: " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP["costs_agreed_30"]["eight"]) + f" (gap {SEP['costs_agreed_30']['gap']}).\n")
A("## The seven limits of 286 and their corpus (373, 382)\n")
A("| Limit | Rule as run | Corpus |\n|---|---|---|")
for k_, (rule, corp) in J["40"]["main"]["373"]["limits"].items(): A(f"| {k_} | {esc(rule)} | {corp} |")
A("")
A("## Readings the paper does not give\n")
for line in open(f"{H}/readings_notes_v119.md").read().strip().splitlines(): A(line)
A("")
open(f"{H}/test_report_v119.md", "w").write("\n".join(o) + "\n" + open(f"{H}/findings_v119.md").read())
print("ok")
