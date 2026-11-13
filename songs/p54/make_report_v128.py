"""Writes test_report_v128.md: v128 Run 3 by parts (Part 1, the clean-up; Part 2, the chart; Part 3, the bass), every figure read from the files,
each check read on the main and control runs together (485, 479), each test beside its kept pass rate (496), then the findings.
Usage: python3 make_report_v128.py"""
import json, os, pickle
import numpy as np
H = "/home/claude/p54"; H0 = "/home/claude/p53"
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
P2S = ("40", "42", "43")
PARTS = [k for k in ("1", "2") if os.path.exists(f"{H}/part{k}/sep.json")]
LAB = {"0": "Run 2 Part 3", "1": "Part 1", "2": "Part 2"}
def songs_of(k): return P2S if k == "2" else tuple(s for s, *_ in S)
J = {"0": {s: json.load(open(f"{H0}/part3/readings_v127_p{s}.json")) for s, *_ in S}} | {k: {s: json.load(open(f"{H}/part{k}/readings_v128_p{s}.json")) for s in songs_of(k)} for k in PARTS}
T = {"0": {s: json.load(open(f"{H0}/part3/readings_v127_p{s}_table.json")) for s, *_ in S}} | {k: {s: json.load(open(f"{H}/part{k}/readings_v128_p{s}_table.json")) for s in songs_of(k)} for k in PARTS}
SEP = {"0": (json.load(open(f"{H0}/part3/sep.json")), json.load(open(f"{H0}/ctlsep/sep_part3.json")))} | {k: (json.load(open(f"{H}/part{k}/sep.json")), json.load(open(f"{H}/part{k}/sep_ctl.json"))) for k in PARTS}
RR = {m: json.load(open(f"{H}/reread_v128_{m}.json")) for m in ("main", "ctl")}
RR2 = {m: json.load(open(f"{H}/reread_v128_p2_{m}.json")) for m in ("main", "ctl") if os.path.exists(f"{H}/reread_v128_p2_{m}.json")}
KP = json.load(open(f"{H}/kept_pass_v128.json")); C476 = json.load(open(f"{H}/check476.json")); BASS = json.load(open(f"{H}/records/bass_readings_v128.json")) if os.path.exists(f"{H}/records/bass_readings_v128.json") else None
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else "—" if h is None else str(h)
def key(d, start): return next(v for k, v in d.items() if k.startswith(start))
def real(a0, a1, b0, b1):
    """479: the change of the mean of the two draws, real only beyond twice the larger main-control difference."""
    th = 2 * max(abs(a0 - a1), abs(b0 - b1)); ch = (b0 + b1) / 2 - (a0 + a1) / 2
    return f"{ch:+.3f} ({'real' if abs(ch) > th else 'not real'}; twice the difference {th:.3f})"
def kpr(t):
    x = KP.get(t)
    if not x: return "—"
    return f"{x['kept_pass']:.0%} of {x['songs']} kept songs" if x["kept_pass"] is not None else "no kept rate"
o = []; A = o.append
A("# ZenEng v128 Run 3: the clean-up, the chart and the bass — test report\n")
A("*Words and music of all five songs: Jason Bryant. The spec is ZenEng v128 (Module 27.72). This run starts from Run 2's Part 3 code (songs/p53) and is in three parts: "
  "the clean-up with a rerun of all five songs, the chart with a rerun of songs 40, 42 and 43, and the bass with the records of songs 40, 43 and 44 rebuilt. "
  "Every rerun is main and control, each made twice at the seeds of record. Each check is read on both draws, and a change is called real only beyond twice their difference (479). "
  "The paper was not edited. New findings are numbered from 500.*\n")
A("## What was run\n")
for line in open(f"{H}/what_was_run.md").read().strip().splitlines(): A(line)
A("")
A("## The writer's choice (Q1)\n")
A("465 could not be ported as written: its class 0 (the last onset in the bar where the next line begins) lies outside a line's slot (310/327), "
  "and it is reached only through the next line's pickup, which 260's entry shares hold to 17%. The writer chose A: class 0 asks the next line to take a pickup, and classes 1 to 3 ask it not to.\n")
A("## Survivors and orders\n")
A("| Song | Run | " + " | ".join(f"{LAB[k]}: survivors, order, reproduced" for k in ["0"] + PARTS) + " |\n|---|---|" + "---|" * (1 + len(PARTS)))
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        A(f"| {s} (seed {seed}) | {lab} | " + " | ".join((f"{J[k][s][v]['runs']['survivors']}, {J[k][s][v]['runs']['order']}, {'yes' if J[k][s][v]['runs']['reproduced'] else '**no**'}" if s in J[k] else "—") for k in ["0"] + PARTS) + " |")
ck = f"{H}/check/melody_v128_p43_main_p1check.pkl"
if os.path.exists(ck):
    c_ = pickle.load(open(ck, "rb")); A(f"\nPart 1 from the final files (song 43, main, ZE_PART=1): order {c_['order_fp']}, {c_['survivors']} survivors — {'the same as' if c_['order_fp'] == J['1']['43']['main']['runs']['order'] else '**not** the same as'} Part 1's run of record.")
A("")
for k in PARTS:
    if os.path.exists(f"{H}/predictions_scored_part{k}.md"):
        A(f"## {LAB[k]}: the predictions, scored\n")
        for line in open(f"{H}/predictions_scored_part{k}.md").read().strip().splitlines(): A(line)
        A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v128.md").read().strip().splitlines(): A(line)
A("")
# ---- 485, 479: the checks on both draws
A("## Separation on both draws (485, 479)\n")
A("The agreed 30 measures, both collections pooled, the first 400 complete builds of each run. Main / control, and the change of their mean against the run before.\n")
fams = ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)")
A("| Family | " + " | ".join(f"{LAB[k]}, 40/42/43" for k in ["0"] + PARTS) + " | " + " | ".join(f"{LAB[k]}, five songs" for k in ["0"] + [p for p in PARTS if p != "2"]) + " |\n|---|" + "---|" * (1 + len(PARTS) + 1 + len([p for p in PARTS if p != "2"])))
for f in fams:
    row = [f"{SEP[k][0]['family'][f]['across_mean_40_42_43']} / {SEP[k][1]['family'][f]['across_mean_40_42_43']}" for k in ["0"] + PARTS]
    row += [f"{SEP[k][0]['family'][f]['across_mean']} / {SEP[k][1]['family'][f]['across_mean']}" for k in ["0"] + [p for p in PARTS if p != "2"]]
    A(f"| {f} | " + " | ".join(row) + " |")
A("")
prev = "0"
for k in PARTS:
    for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)"):
        a, b = SEP[prev], SEP[k]
        A(f"- **{LAB[k]} against {LAB[prev]}, {f}, songs 40, 42, 43:** " + real(a[0]["family"][f]["across_mean_40_42_43"], a[1]["family"][f]["across_mean_40_42_43"], b[0]["family"][f]["across_mean_40_42_43"], b[1]["family"][f]["across_mean_40_42_43"]))
    prev = k
A("\nCosts on the 30, pooled (points; kept mean, builds' mean), main / control:\n")
for k in ["0"] + PARTS:
    for i, lab in ((0, "main"), (1, "control")):
        A(f"- **{LAB[k]}, {lab}** (gap {SEP[k][i]['costs_agreed_30']['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP[k][i]["costs_agreed_30"]["eight"][:6]))
A("")
# ---- the reread, both draws
def rr_block(R, runs, title):
    A(f"## {title}\n")
    fv = {m: key(R[m], "first verse and chorus") for m in R}; mo = {m: key(R[m], "the melody over chord") for m in R}
    A("Window 147's measures (song 43 on A minor). Each cell: main / control; the last column the change of their mean against the run before, with 479's verdict.\n")
    A("| Measure | Billboard | Rolling Stone | " + " | ".join(runs) + " | Change |\n|---|---|---|" + "---|" * len(runs) + "---|")
    for m in list(fv["main"]) + list(mo["main"]):
        src = fv if m in fv["main"] else mo; r0, r1 = src["main"][m], src["ctl"][m]
        A(f"| {m} | {r0['billboard']} | {r0['rolling_stone']} | " + " | ".join(f"{r0[v]} / {r1[v]}" for v in runs) + f" | {real(r0[runs[-2]], r1[runs[-2]], r0[runs[-1]], r1[runs[-1]])} |")
    v2 = {m: key(R[m], "the second verse less the first") for m in R}
    A("\nThe second verse against the first, paired by build (434's test: under 0.15 kept sd on 20 of 27):\n")
    A("| Run | Draw | Under 0.15, of 27 | By song | Chord tones on the beat, verse 1 / verse 2 | Pitch kept | Repeat, verse 1 / verse 2 | Step, verse 1 / verse 2 |\n|---|---|---|---|---|---|---|---|")
    for v in runs:
        for m in ("main", "ctl"):
            x = v2[m][v]; q = x["verse 1 / verse 2 / kept verse 2"]; pk = x["pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)"]
            A(f"| {v} | {m} | {x['measures under 0.15 kept sd, of 27']} | {x['by song (of 27)']} | {x['chord tones on the beat, verse 1 / verse 2 (pooled)']} | {pk[2] if pk else '—'} | {q['repeat'][0]} / {q['repeat'][1]} | {q['step'][0]} / {q['step'][1]} |")
    A("\nThe largest differences, verse 2 less verse 1 (kept sd), main: " + "; ".join(f"**{v}** " + ", ".join(f"{mm} {d}" for mm, d in sorted(v2['main'][v]["every measure (kept sd)"].items(), key=lambda kv: -abs(kv[1]))[:6]) for v in runs) + ".\n")
    d = {m: R[m]["at the windows' own density (kept, run)"] for m in R}
    A("At the windows' own density (kept, main, control): " + "; ".join(f"**{v}** " + ", ".join(f"{b}: " + ", ".join(f"{mm} {d['main'][v][b][mm][0]}/{d['main'][v][b][mm][1]}/{d['ctl'][v][b][mm][1]}" for mm in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three")) for b in d["main"][v]) for v in runs) + ".\n")
    for m in ("main", "ctl"):
        for kk, x in key(R[m], "moved toward").items():
            A(f"**{kk} ({m}):** {len(x['toward kept (measure, sd from kept before, after)'])} toward kept, {len(x['away'])} away, {len(x['within 0.02 sd'])} unmoved.")
    A("")
rr_block(RR, ["r2p3", "part1"], "Part 1 against Run 2's Part 3, read as Window 147 reads it (both draws)")
if RR2: rr_block(RR2, ["part1", "part2"], "Part 2 against Part 1, songs 40, 42 and 43 (both draws; the chord at the note)")
# ---- the judge
A("## The judge (476, 477)\n")
A("The content judge of record is zeneng_v128_judge.json. Its table gives a kept mean of 1.53, an sd of 2.0 and a 25th percentile of 0.23, and no 5th percentile (finding 507). Main runs:\n")
A("| Song | Part | Content, complete builds (main / control) | Under the kept 25th | Under 1.53 − 1.645 sd | Pick | Score (mean of content and order) | v108's pick's rank under v128 | v128's pick's rank under v108 |\n|---|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    for k in PARTS:
        if s not in J[k]: continue
        a, b = J[k][s]["main"], J[k][s]["ctl"]
        A(f"| {s} | {LAB[k]} | {a['476']['content_mean']} / {b['476']['content_mean']} | {a['476']['under_kept_25th']:.0%} | {a['476']['under_normal_5th']:.0%} | {a['477']['pick']} | {a['477']['score']} | {a['472'].get('v108_pick_rank_under_refit')} | {a['472'].get('refit_pick_rank_under_v108')} |")
A("\n476's test, the engine's content score against the paper's on the same builds (Run 2's Part 2, main runs, every complete build):\n")
A("| Song | Engine: verse 1, verse 2, chorus 1 | Paper: verse 1, verse 2 | Verse 1 within 0.05 |\n|---|---|---|---|")
for s, *_ in S:
    x = C476[s]; A(f"| {s} | {x['engine']['Verse 1']}, {x['engine'].get('Verse 2')}, {x['engine']['Chorus 1']} | {x['paper_verse1_verse2'][0]}, {x['paper_verse1_verse2'][1]} | {held(x['verse1_within_0_05'])} |")
A(f"\nPooled (engine, paper): {C476['pooled']}.\n")
# ---- lines
A("## The line's end and rate (465, 458), main runs\n")
for s, *_ in S:
    x = J[PARTS[0]][s]["main"]["465"]; y = J[PARTS[0]][s]["main"]["458"]
    A(f"**Song {s}.** 465: drawn {x['drawn']}, held {x['held_to_end']}, given up {x['given_up']} ({x['given_up'] / max(1, x['drawn']):.1%}); no class the slot allows {x['no_class']}; the next line's entry given up {x['entry_given_up']}; "
      f"spans given up {x['spans_given_up']} of {x['span_lines']} ({x['spans_given_up'] / max(1, x['span_lines']):.1%}).\n")
    A("| Notes | Lines | Class 0 / 1 / 2 / 3+ | Kept | Beats to the next line (25, 50, 75) | Kept | Four beats or more | Kept | Notes a second (25, 50, 75) | Kept |\n|---|---|---|---|---|---|---|---|---|---|")
    for b, v in x["by_notes"].items():
        r8 = y["by_notes"].get(b)
        A(f"| {b} | {v['lines']} | {v['classes']} | {v['kept']} | {v['beats_to_next']} | {v['kept_beats']} | {v['four_beats_or_more']} | {v['kept_four']} | {r8['notes_a_second'] if r8 else '—'} | {r8['kept'] if r8 else '—'} |")
    A("")
# ---- the stream and song 45
A("## The stream (489, 490) and song 45's joins (494)\n")
A("| Song | Part 1 band knobs (equal gap, run, zigzag) | Run weights (490) | Drawable runs: band (kept, (onsets, share)) |\n|---|---|---|---|")
for s, *_ in S:
    x = J[PARTS[0]][s]["main"]
    A(f"| {s} | {esc({b: v for b, v in (x['489']['knobs'] or {}).items() if v != {'gs': 1.0, 'er': 1.0, 'zz': 1.0}})} | {esc(x['490']['knobs'])} | {esc(x['490']['drawable_runs'])} |")
A("\nSide runs, song 45, main (494):\n")
A("| Run | Survivors | Rhythm deaths | Joins before a copy | Joins before a line | Align | Design |\n|---|---|---|---|---|---|---|")
for lab, f in (("Run 2 Part 3", f"{H0}/part3/melody_v127_p45_main.pkl"), ("Part 1", f"{H}/part1/melody_v128_p45_main.pkl"), ("Part 1, 452 off", f"{H}/side/melody_v128_p45_main_p1off452.pkl"), ("Part 1, 455 off", f"{H}/side/melody_v128_p45_main_p1off455.pkl")):
    P_ = pickle.load(open(f, "rb")); d = P_["deaths"]
    A(f"| {lab} | {P_['survivors']} | {d.get('rhythm: no placement', 0)} | {d.get('join: no held end and breath before the copy (212)', 0)} | {d.get('join: no held end and breath before the line (212)', 0)} | {d.get('align: the words do not fit the returning tune', 0)} | {sum(v for kk, v in d.items() if kk.startswith('design'))} |")
A("")
# ---- Part 2: the charts
if "2" in PARTS:
    A("## Part 2: the charts (438, 440)\n")
    A("| Song | Two-change bars: before → drawn (target) | Held bars: before → drawn (target) | Changes | Inversions | Bass on the root at changes (main) |\n|---|---|---|---|---|---|")
    for s in P2S:
        P_ = pickle.load(open(f"{H}/part2/melody_v128_p{s}_main.pkl", "rb")); c = P_["rerun"]["chart438"]; x = J["2"][s]["main"].get("440", {})
        A(f"| {s} | {c['before']['two_or_more']} → {c['after']['two_or_more']} ({c['targets']['two_or_more']}{', none drawn' if c['targets']['none_drawn'] else ''}) | {c['before']['holding']} → {c['after']['holding']} ({c['targets']['holding']}) | {c['after']['changes']} | {', '.join(f'{a} bar {h // 2 + 1}: {n}' for a, h, n in c['inversions']) or 'none'} | {x.get('root_share', '—')} |")
    A("")
# ---- Part 3: the bass
if BASS:
    A("## Part 3: the bass (439, 444–449)\n")
    A("Each section's eight bars (a shorter section read whole), read with Window 144's measures() against the Lucerne quartiles for pop, rock, rock and roll, alternative and country (444). "
      "The old bass is the hand-written one of the song's record; the new is bass_v128.py's. Medians of the windows:\n")
    ms = ("notes_per_bar", "pitch_classes_per_bar", "on_the_bars_first_note", "iv_repeat", "iv_step", "iv_octave", "bar_rhythm_same_as_last", "distinct_bar_rhythms", "kick_with_bass", "bass_with_kick", "into_the_bar_by_step_of_changes", "bars_one_pitch_class")
    A("| Measure | Pop and rock (25, 50, 75) | " + " | ".join(f"Song {s}: old → new" for s in BASS) + " |\n|---|---|" + "---|" * len(BASS))
    for m in ms:
        q = next((BASS[s]["new"][m]["pop_rock_quartiles"] or BASS[s]["new"][m]["all_quartiles"] for s in BASS if m in BASS[s]["new"]), None) or ("0 / 0.286 / 0.714 (all patterns)" if m == "into_the_bar_by_step_of_changes" else None)
        A(f"| {m} | {q} | " + " | ".join(f"{BASS[s]['old'].get(m, {}).get('median', '—')} → {BASS[s]['new'].get(m, {}).get('median', '—')}" for s in BASS) + " |")
    A("\nThe tests, windows passing of windows read (old → new):\n")
    tk = list(BASS["40"]["new"]["tests: windows passing, of windows read"])
    A("| Test | " + " | ".join(f"Song {s}" for s in BASS) + " |\n|---|" + "---|" * len(BASS))
    for t in tk:
        A(f"| {t} | " + " | ".join(f"{BASS[s]['old']['tests: windows passing, of windows read'].get(t, ['—', '—'])[0]}/{BASS[s]['old']['tests: windows passing, of windows read'].get(t, ['—', '—'])[1]} → {BASS[s]['new']['tests: windows passing, of windows read'].get(t, ['—', '—'])[0]}/{BASS[s]['new']['tests: windows passing, of windows read'].get(t, ['—', '—'])[1]}" for s in BASS) + " |")
    A("| 440 the root at every change | " + " | ".join(f"{BASS[s]['root_at_changes']['old']:.0%} → {BASS[s]['root_at_changes']['new']:.0%} of {BASS[s]['root_at_changes']['changes']}" for s in BASS) + " |")
    A("| 449 no listener rating as a target | " + " | ".join("held (no rating read)" for s in BASS) + " |")
    A("\nNotes: " + "; ".join(f"song {s} {BASS[s]['notes']['old']} → {BASS[s]['notes']['new']}" for s in BASS) + ". Draws taken (the best of up to 60 a section) and windows still failing: " + "; ".join(f"**{s}** " + ", ".join(f"{sec} {a[0]}/{a[1]}" for sec, a in BASS[s]["tries_and_windows_failing"].items()) for s in BASS) + ".\n")
# ---- the tables of tests, with the kept pass rate (496)
A("## Tests that moved (held in the main run and the control)\n")
allk = sorted({r[0] for k in ["0"] + PARTS for s in T[k] for r in T[k][s]}, key=lambda x: int(x))
A("| Fix | Song | " + " | ".join(LAB[k] for k in ["0"] + PARTS) + " |\n|---|---|" + "---|" * (1 + len(PARTS)))
for f in allk:
    for s, *_ in S:
        hs = [next((r[5] for r in T[k][s] if r[0] == f), None) if s in T[k] else "—" for k in ["0"] + PARTS]
        if len({str(h) for h in hs if h != "—"}) > 1: A(f"| {f} | {s} | " + " | ".join(held(h) for h in hs) + " |")
A("")
for s, title, seed in S:
    last = "2" if (s in P2S and "2" in PARTS) else PARTS[0]
    rows = T[last][s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests after {LAB[last]}: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + " The last column is the share of kept songs that pass the test read the same way (496).\n")
    A("| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |\n|---|---|---|---|---|---|---|")
    for kk, t, ka, a, b, h in rows: A(f"| {kk} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} | {kpr(kk)} |")
    A("")
A("## The kept pass rates (496)\n")
A(KP["about"] + "\n")
A("| Test | Kept pass rate | How it is read |\n|---|---|---|")
for t, x in sorted(((t, x) for t, x in KP.items() if t != "about"), key=lambda kv: int(kv[0])):
    A(f"| {t} | {kpr(t)} | {esc(x['how'])} |")
A("")
open(f"{H}/test_report_v128.md", "w").write("\n".join(o) + "\n" + (open(f"{H}/findings_v128.md").read() if os.path.exists(f"{H}/findings_v128.md") else ""))
print("ok", PARTS)
