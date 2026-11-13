"""Writes test_report_v127.md: v127 Run 2 by parts (the refit judge and Part 0 with Part 1; Part 2; Part 3), every figure read from the files, then
the findings. Parts not yet run are left out. Usage: python3 make_report_v127.py"""
import json, os
H = "/home/claude/p53"; H1 = "/home/claude/p52"
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
PARTS = [k for k in ("1", "2", "3") if os.path.exists(f"{H}/part{k}/sep.json")]
LAB = {"0": "Run 1", "1": "Part 1", "2": "Part 2", "3": "Part 3"}
J = {"0": {s: json.load(open(f"{H1}/readings_v124_p{s}.json")) for s, *_ in S}} | {k: {s: json.load(open(f"{H}/part{k}/readings_v127_p{s}.json")) for s, *_ in S} for k in PARTS}
T = {"0": {s: json.load(open(f"{H1}/readings_v124_p{s}_table.json")) for s, *_ in S}} | {k: {s: json.load(open(f"{H}/part{k}/readings_v127_p{s}_table.json")) for s, *_ in S} for k in PARTS}
SEP = {"0": json.load(open(f"{H}/part0_sep.json"))} | {k: json.load(open(f"{H}/part{k}/sep.json")) for k in PARTS}
RR = json.load(open(f"{H}/reread_v127.json"))
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
def key(d, start): return next(v for k, v in d.items() if k.startswith(start))
o = []; A = o.append
A("# ZenEng v127 Run 2: the refit judge and the session's adopted fixes, by parts — test report\n")
A("*Words and music of all five songs: Jason Bryant. The spec is ZenEng v127 (Modules 27.69–27.71). This run is on top of Run 1 (songs/p52), in parts, "
  "with a rerun of all five songs, main and control, at the same seeds after each part. The paper was not edited. New findings are numbered from 480. "
  "Run 1's 450–454 are the paper's 464–468.*\n")
A("## What was run\n")
for line in open(f"{H}/what_was_run.md").read().strip().splitlines(): A(line)
A("")
A("| Song | Run | " + " | ".join(f"{LAB[k]}: survivors, order, reproduced" for k in ["0"] + PARTS) + " |\n|---|---|" + "---|" * (1 + len(PARTS)))
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        A(f"| {s} (seed {seed}) | {lab} | " + " | ".join(f"{J[k][s][v]['runs']['survivors']}, {J[k][s][v]['runs']['order']}, {'yes' if J[k][s][v]['runs']['reproduced'] else '**no**'}" for k in ["0"] + PARTS) + " |")
A("")
for k in PARTS:
    A(f"## {LAB[k]}: the predictions, scored\n")
    for line in open(f"{H}/predictions_scored_part{k}.md").read().strip().splitlines(): A(line)
    A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v127.md").read().strip().splitlines(): A(line)
A("")
A("## The judge (470–473)\n")
A("The content judge of record is v126's refit (37 measures). The order judge and the combining are unchanged, and 254's floor stays on the v108 judge (471). Main runs:\n")
A("| Song | Part | Refit content, complete builds (v108 content) | Rank correlation | Under the kept 5th percentile (−0.51) | Floor deaths (v108) | Pick (refit) | v108's pick | v108's pick's rank under the refit | Refit pick's rank under v108 |\n|---|---|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    for k in PARTS:
        x = J[k][s]["main"]; a, b, c = x["470"], x["471"], x["472"]
        A(f"| {s} | {LAB[k]} | {a['refit_content_mean']} ({a['v108_content_mean']}) | {a['rank_correlation']} | {b['under_kept_5th']:.0%} | {b['floor_deaths_v108']} | {c['pick']} | {c.get('v108_pick')} | {c.get('v108_pick_rank_under_refit')} | {c.get('refit_pick_rank_under_v108')} |")
A("\nThe floor moves to the refit when the share under the kept 5th percentile is under a third on every song (471); it is not, so the floor stays.\n")
v2 = key(RR, "the second verse less the first")
A("## The second verse (434, 435), read as Window 147 reads it\n")
A("The first 400 complete builds of each main run, verse 2 paired with verse 1 by build, in kept verse 1 standard deviations (27 measures). Kept collections: Billboard 23 under 0.15, Rolling Stone 23.\n")
A("| Run | Pairs | Under 0.15 kept sd, of 27 (test: 20) | By song | Chord tones on the beat, verse 1 / verse 2 (test: within five points) | Pair: bars the same rhythm, onsets shared, pitch kept, notes ratio |\n|---|---|---|---|---|---|")
for v, x in v2.items():
    A(f"| {v} | {x['pairs']} | {x['measures under 0.15 kept sd, of 27']} | {x['by song (of 27)']} | {x['chord tones on the beat, verse 1 / verse 2 (pooled)']} | {x['pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)']} |")
A("\nThe largest differences, verse 2 less verse 1 (kept sd), each run:\n")
for v, x in v2.items(): A(f"- **{v}:** " + "; ".join(f"{m} {d}" for m, d in sorted(x["every measure (kept sd)"].items(), key=lambda kv: -abs(kv[1]))[:8]))
A("\nChord tones on the beat by song, verse 1 / verse 2: " + "; ".join(f"**{v}** {x['chord tones on the beat, verse 1 / verse 2 (by song)']}" for v, x in v2.items()) + ".\n")
A("## Each run against the one before: toward the kept songs or away\n")
A("Every reading of the first verse and chorus (Window 147's measures, beside Billboard and Rolling Stone), of the melody over the chord, and of verse 2 less verse 1. "
  "A reading moved toward kept when its distance from the kept mean (in kept sd) fell by more than 0.02.\n")
for k, x in key(RR, "moved toward").items():
    tw, aw = x["toward kept (measure, sd from kept before, after)"], x["away"]
    A(f"**{k}:** {len(tw)} toward, {len(aw)} away, {len(x['within 0.02 sd'])} unmoved.\n")
    A("- Toward: " + "; ".join(f"{m} ({a} → {b})" for m, a, b in tw))
    A("- Away: " + "; ".join(f"{m} ({a} → {b})" for m, a, b in aw) + "\n")
A("## Separation (422, 454): the 30 agreed measures, both collections pooled, and without each family\n")
fams = ["agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "agreed 30 without pitch (agreed)", "agreed 30 without rhythm (agreed)", "agreed 30 without form", "harmony (CoCoPops alone, apart)"]
A("| Family | " + " | ".join(f"{LAB[k]}, 40/42/43 across" for k in ["0"] + PARTS) + " | " + " | ".join(f"{LAB[k]}, five songs" for k in ["0"] + PARTS) + " |\n|---|" + "---|" * (2 * (1 + len(PARTS))))
for f in fams:
    A(f"| {f} | " + " | ".join(str(SEP[k]["family"][f]["across_mean_40_42_43"]) if f in SEP[k]["family"] else "—" for k in ["0"] + PARTS) + " | " + " | ".join(str(SEP[k]["family"][f]["across_mean"]) if f in SEP[k]["family"] else "—" for k in ["0"] + PARTS) + " |")
for k in PARTS:
    c = SEP[k]["family"]["agreed 30"]["across_mean_40_42_43"]
    A(f"\n**Check, {LAB[k]}: separation at or under Run 1's 0.719 on songs 40, 42 and 43: {c} — {'held' if c <= 0.719 else '**not held**'}.**")
CS = {k: json.load(open(f"{H}/ctlsep/sep_{n}.json")) for k, n in (("0", "run1"), ("1", "part1"), ("2", "part2"), ("3", "part3")) if os.path.exists(f"{H}/ctlsep/sep_{n}.json")}
if CS:
    A("\nThe same read on the control runs, separation's own spread (485):\n")
    A("| Family | " + " | ".join(f"{LAB[k]}, main / control, 40/42/43" for k in CS) + " | " + " | ".join(f"{LAB[k]}, main / control, five" for k in CS) + " |\n|---|" + "---|" * (2 * len(CS)))
    for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form"):
        A(f"| {f} | " + " | ".join(f"{SEP[k]['family'][f]['across_mean_40_42_43']} / {CS[k]['family'][f]['across_mean_40_42_43']}" for k in CS) + " | " + " | ".join(f"{SEP[k]['family'][f]['across_mean']} / {CS[k]['family'][f]['across_mean']}" for k in CS) + " |")
A("\nCosts on the 30, the five songs pooled (points; kept mean, builds' mean):\n")
for k in ["0"] + PARTS: A(f"- **{LAB[k]}** (gap {SEP[k]['costs_agreed_30']['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP[k]["costs_agreed_30"]["eight"]))
A("")
A("## Tests that moved, part by part (held in the main run and the control)\n")
allk = sorted({r[0] for k in ["0"] + PARTS for s, *_ in S for r in T[k][s]}, key=lambda x: int(x))
A("| Fix | Song | " + " | ".join(LAB[k] for k in ["0"] + PARTS) + " |\n|---|---|" + "---|" * (1 + len(PARTS)))
for f in allk:
    for s, *_ in S:
        hs = [next((r[5] for r in T[k][s] if r[0] == f), None) for k in ["0"] + PARTS]
        if len({str(h) for h in hs}) > 1: A(f"| {f} | {s} | " + " | ".join(held(h) for h in hs) + " |")
A("")
last = PARTS[-1]
for s, title, seed in S:
    rows = T[last][s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests after {LAB[last]}: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
if os.path.exists(f"{H}/kept_cannot_pass.md"):
    A("## Tests the kept songs themselves cannot pass\n")
    for line in open(f"{H}/kept_cannot_pass.md").read().strip().splitlines(): A(line)
    A("")
fv = key(RR, "first verse and chorus")
A("## The first verse and chorus, every measure beside Billboard and Rolling Stone (sd from the two collections' mean)\n")
runs = RR["runs"]
A("| Measure | Billboard | Rolling Stone | " + " | ".join(runs) + " |\n|---|---|---|" + "---|" * len(runs))
for m, r in list(fv.items()) + list(key(RR, "the melody over chord").items()):
    A(f"| {m} | {r['billboard']} | {r['rolling_stone']} | " + " | ".join(f"{r[v]} ({r[v + '_sd_from_kept']})" for v in runs) + " |")
A(f"\nThe chorus's first beat on the chord's third (Billboard 0.247, Rolling Stone 0.294): {key(RR, 'chorus first beat on the third (')}; by song (40, 42, 43, 44, 45): {key(RR, 'chorus first beat on the third, by song')}.\n")
A("At the windows' own density (kept figure, run): " + "; ".join(f"**{v}** " + ", ".join(f"{b}: " + ", ".join(f"{m} {d[m][0]}/{d[m][1]}" for m in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three")) for b, d in x.items()) for v, x in key(RR, "at the windows").items()) + ".\n")
open(f"{H}/test_report_v127.md", "w").write("\n".join(o) + "\n" + open(f"{H}/findings_v127.md").read())
print("ok", PARTS)
