"""Writes test_report_v129.md: the v129 port on songs 40-45 (the last on these songs), against Run 3's runs of record, every check read on the
main and control runs together (485, 479), each test beside its kept pass rate (496), a test no kept song can pass read as a mean of builds only
(512), then the findings. Usage: python3 make_report_v129.py"""
import json, os, pickle
import numpy as np
H = "/home/claude/p55"; H3 = "/home/claude/p54"
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
R3P = {"40": "2", "42": "2", "43": "2", "44": "1", "45": "1"}
LAB = {"0": "Run 3", "1": "v129"}
J = {"0": {s: json.load(open(f"{H3}/part{R3P[s]}/readings_v128_p{s}.json")) for s, *_ in S}, "1": {s: json.load(open(f"{H}/part1/readings_v129_p{s}.json")) for s, *_ in S}}
T = {"0": {s: json.load(open(f"{H3}/part{R3P[s]}/readings_v128_p{s}_table.json")) for s, *_ in S}, "1": {s: json.load(open(f"{H}/part1/readings_v129_p{s}_table.json")) for s, *_ in S}}
SEP = {"0": (json.load(open(f"{H}/run3_sep.json")), json.load(open(f"{H}/run3_sep_ctl.json"))), "1": (json.load(open(f"{H}/part1/sep.json")), json.load(open(f"{H}/part1/sep_ctl.json")))}
RR = {m: json.load(open(f"{H}/reread_v129_{m}.json")) for m in ("main", "ctl")}
KP = json.load(open(f"{H}/kept_pass_v129.json")); BASS = json.load(open(f"{H}/records/bass_readings_v129.json")); BASS8 = json.load(open(f"{H3}/records/bass_readings_v128.json"))
PJ = json.load(open(f"{H}/tables/zeneng_v129_judge.json"))["findings"]["5. complete builds under the kept songs' fifth percentile (-0.72), by song"]
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else "—" if h is None else str(h)
def key(d, start): return next(v for k, v in d.items() if k.startswith(start))
def real(a0, a1, b0, b1):
    th = 2 * max(abs(a0 - a1), abs(b0 - b1)); ch = (b0 + b1) / 2 - (a0 + a1) / 2
    return f"{ch:+.3f} ({'real' if abs(ch) > th else 'not real'}; twice the difference {th:.3f})"
def kpr(t):
    x = KP.get(t)
    if not x: return "—"
    return f"{x['kept_pass']:.0%} of {x['songs']} kept songs" if x["kept_pass"] is not None else "no kept rate"
def held512(t, h):
    x = KP.get(t)
    if x and x["kept_pass"] == 0 and isinstance(h, bool): return f"a reading of the mean of builds (512; {'inside' if h else 'outside'} the band)"
    return held(h)
o = []; A = o.append
A("# ZenEng v129: the last port on songs 40–45 — test report\n")
A("*Words and music of all five songs: Jason Bryant. The spec is ZenEng v129 (Module 27.73). The session's 500–518 were ported once, with no new aims (521), onto Run 3's code of record: "
  "songs 40, 42 and 43 on their 438 charts (Run 3's Part 2), songs 44 and 45 on their own (Run 3's Part 1). All five songs were rerun, main and control, each made twice at the seeds of record, "
  "and every check is read on both draws (479). The paper was not edited. New findings are numbered from 530. This is the last report on these songs.*\n")
A("## What was run\n")
for line in open(f"{H}/what_was_run.md").read().strip().splitlines(): A(line)
A("")
A("## Survivors and orders\n")
A("| Song | Run | Run 3: survivors, order | v129: survivors, order, reproduced |\n|---|---|---|---|")
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        a, b = J["0"][s][v]["runs"], J["1"][s][v]["runs"]
        A(f"| {s} (seed {seed}) | {lab} | {a['survivors']}, {a['order']} | {b['survivors']}, {b['order']}, {'yes' if b['reproduced'] else '**no**'} |")
A("\nZE_PART=0 from the final files reproduces Run 3 (song 43 main: 9fab8a9e1e46, 872 survivors).\n")
if os.path.exists(f"{H}/predictions_scored_v129.md"):
    A("## The predictions, scored\n")
    for line in open(f"{H}/predictions_scored_v129.md").read().strip().splitlines(): A(line)
    A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v129.md").read().strip().splitlines(): A(line)
A("")
A("## Separation on both draws (479)\n")
A("The agreed 30 measures, both collections pooled, the first 400 complete builds of each run. Run 3 is read on its runs of record (songs 40, 42, 43 from Part 2; 44, 45 from Part 1). Main / control.\n")
fams = ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)")
A("| Family | Run 3, 40/42/43 | v129, 40/42/43 | Change | Run 3, five songs | v129, five songs | Change |\n|---|---|---|---|---|---|---|")
for f in fams:
    a, b = SEP["0"], SEP["1"]; g = lambda X, i, k: X[i]["family"][f][k]
    A(f"| {f} | {g(a,0,'across_mean_40_42_43')} / {g(a,1,'across_mean_40_42_43')} | {g(b,0,'across_mean_40_42_43')} / {g(b,1,'across_mean_40_42_43')} | {real(g(a,0,'across_mean_40_42_43'), g(a,1,'across_mean_40_42_43'), g(b,0,'across_mean_40_42_43'), g(b,1,'across_mean_40_42_43'))} | "
      f"{g(a,0,'across_mean')} / {g(a,1,'across_mean')} | {g(b,0,'across_mean')} / {g(b,1,'across_mean')} | {real(g(a,0,'across_mean'), g(a,1,'across_mean'), g(b,0,'across_mean'), g(b,1,'across_mean'))} |")
A("\nCosts on the 30, pooled (points; kept mean, builds' mean):\n")
for k in ("0", "1"):
    for i, lab in ((0, "main"), (1, "control")):
        A(f"- **{LAB[k]}, {lab}** (gap {SEP[k][i]['costs_agreed_30']['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP[k][i]["costs_agreed_30"]["eight"][:6]))
A("")
runs = ["run3", "v129"]
fv = {m: key(RR[m], "first verse and chorus") for m in RR}; mo = {m: key(RR[m], "the melody over chord") for m in RR}
A("## The first verse and chorus beside the kept songs (both draws)\n")
A("Window 147's measures, with the window taken the engine's way (519: every note sung in the eight bars, the chord at the note; song 43 on A minor). Main / control; the change of their mean, with 479's verdict.\n")
A("| Measure | Billboard | Rolling Stone | Run 3 | v129 | Change |\n|---|---|---|---|---|---|")
for m in list(fv["main"]) + list(mo["main"]):
    src = fv if m in fv["main"] else mo; r0, r1 = src["main"][m], src["ctl"][m]
    A(f"| {m} | {r0['billboard']} | {r0['rolling_stone']} | {r0['run3']} / {r1['run3']} | {r0['v129']} / {r1['v129']} | {real(r0['run3'], r1['run3'], r0['v129'], r1['v129'])} |")
v2 = {m: key(RR[m], "the second verse less the first") for m in RR}
A("\nThe second verse against the first, paired by build (434's test: under 0.15 kept sd on 20 of 27):\n")
A("| Run | Draw | Under 0.15, of 27 | By song | Chord tones on the beat, verse 1 / verse 2 | Pitch kept | Repeat, verse 1 / verse 2 | Step, verse 1 / verse 2 |\n|---|---|---|---|---|---|---|---|")
for v in runs:
    for m in ("main", "ctl"):
        x = v2[m][v]; q = x["verse 1 / verse 2 / kept verse 2"]; pk = x["pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)"]
        A(f"| {v} | {m} | {x['measures under 0.15 kept sd, of 27']} | {x['by song (of 27)']} | {x['chord tones on the beat, verse 1 / verse 2 (pooled)']} | {pk[2] if pk else '—'} | {q['repeat'][0]} / {q['repeat'][1]} | {q['step'][0]} / {q['step'][1]} |")
d = {m: RR[m]["at the windows' own density (kept, run)"] for m in RR}
A("\nAt the windows' own density (kept, main, control): " + "; ".join(f"**{v}** " + ", ".join(f"{b}: " + ", ".join(f"{mm} {d['main'][v][b][mm][0]}/{d['main'][v][b][mm][1]}/{d['ctl'][v][b][mm][1]}" for mm in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three")) for b in d["main"][v]) for v in runs) + ".\n")
A("## The judge of record (519)\n")
A("The content judge is zeneng_v129_judge.json, fitted on the engine's own reading of Run 3's builds. Complete builds under the kept songs' 5th percentile (−0.72, a kept song's mean over its windows); the floor stays on the v108 judge.\n")
A("| Song | Content mean, main / control | Under −0.72, main / control | The paper's figure (Run 3) |\n|---|---|---|---|")
for s, *_ in S:
    a, b = J["1"][s]["main"]["519"], J["1"][s]["ctl"]["519"]
    A(f"| {s} | {a['content_mean']} / {b['content_mean']} | {a['under_kept_song_5th']:.0%} / {b['under_kept_song_5th']:.0%} | {PJ[s]:.0%} |")
A("")
A("## The line's end and rate (500, 501), main runs\n")
for s, *_ in S:
    x = J["1"][s]["main"]["500"]; y = J["1"][s]["main"]["501"]
    A(f"**Song {s}.** 465: drawn {x['drawn']}, given up {x['given_up']} ({x['given_up'] / max(1, x['drawn']):.1%}); out of the slot's reach {x['out_of_reach_total']}: " + "; ".join(f"{k} {v}" for k, v in list(x["out_of_reach"].items())[:4]) +
      f". 501: inside {y['inside']}, redrawn {y['redrawn']}, given up {y['given_up']}.\n")
    A("| Notes, slot | Lines | Class 0 / 1 / 2 / 3+ | Kept (notes and slot) |\n|---|---|---|---|")
    for b, v in x["by_notes_and_slot"].items(): A(f"| {b} | {v['lines']} | {v['classes']} | {v['kept']} |")
    A("\n| Notes | Lines | Onsets a beat (25, 50, 75) | Kept |\n|---|---|---|---|")
    for b, v in y["by_notes"].items(): A(f"| {b} | {v['lines']} | {v['onsets_a_beat']} | {v['kept']} |")
    A("")
A("## Song 45 (502, 508), and the side run\n")
A("| Run | Survivors | Design deaths | Joins before a copy | Joins before a line | Align | Rhythm |\n|---|---|---|---|---|---|---|")
for lab, f in (("Run 3 (Part 1), main", f"{H3}/part1/melody_v128_p45_main.pkl"), ("Run 3 (Part 1), control", f"{H3}/part1/melody_v128_p45_ctl.pkl"), ("v129, main", f"{H}/part1/melody_v129_p45_main.pkl"),
               ("v129, control", f"{H}/part1/melody_v129_p45_ctl.pkl"), ("v129, main, 501 off", f"{H}/side/melody_v129_p45_main_off501.pkl")):
    if not os.path.exists(f): continue
    P_ = pickle.load(open(f, "rb")); dd = P_["deaths"]
    A(f"| {lab} | {P_['survivors']} | {sum(v for kk, v in dd.items() if kk.startswith('design'))} | {dd.get('join: no held end and breath before the copy (212)', 0)} | {dd.get('join: no held end and breath before the line (212)', 0)} | {dd.get('align: the words do not fit the returning tune', 0)} | {dd.get('rhythm: no placement', 0)} |")
A("")
A("## The second verse (503), the stream (504, 505) and the chart (513), main / control\n")
A("| Song | 503: verse 1 / verse 2 chord tones on the beat (knob) | 504: notes to syllables | 505: drawable runs (kept, (onsets, share)) | 513: inversions; taken back |\n|---|---|---|---|---|")
for s, *_ in S:
    a, b = J["1"][s]["main"], J["1"][s]["ctl"]
    t503 = f"{a['503'].get('verse1')} / {a['503'].get('verse2')} ({a['503'].get('knob')}); {b['503'].get('verse1')} / {b['503'].get('verse2')}" if "verse1" in a["503"] else "—"
    t513 = f"{a['513'].get('inversions')}; {a['513'].get('reverted')}" if "inversions" in a["513"] else a["513"]["note"]
    A(f"| {s} | {t503} | {a['504']['notes_to_syllables']} / {b['504']['notes_to_syllables']} | {esc(a['505']['drawable_runs'])} | {esc(t513)} |")
A("")
A("## The range beside each song's design (520: not aimed)\n")
A("| Song | Verse window, main / control | Chorus window, main / control | Kept | The design |\n|---|---|---|---|---|")
for s, *_ in S:
    a, b = J["1"][s]["main"]["520"]["range"], J["1"][s]["ctl"]["520"]["range"]
    A(f"| {s} | {a['verse']} / {b['verse']} | {a['chorus']} / {b['chorus']} | 10.9 | {a['design']} |")
A("")
A("## The bass (516, 517): the records of songs 40, 43 and 44 rebuilt again\n")
A("Each section's eight bars read with Window 144's measures() against the pop-and-rock quartiles. Hand-written (the records' own) → Run 3's routine → v129's routine. Window medians:\n")
ms = ("notes_per_bar", "pitch_classes_per_bar", "on_the_bars_first_note", "iv_repeat", "iv_step", "iv_octave", "bar_rhythm_same_as_last", "distinct_bar_rhythms", "kick_with_bass", "bass_with_kick", "bass_with_kick_kicked_bars", "into_the_bar_by_step_of_changes")
A("| Measure | Pop and rock (25, 50, 75) | " + " | ".join(f"Song {s}" for s in BASS) + " |\n|---|---|" + "---|" * len(BASS))
for m in ms:
    q = next((BASS[s]["new"][m]["pop_rock_quartiles"] for s in BASS if m in BASS[s]["new"] and BASS[s]["new"][m]["pop_rock_quartiles"]), None) or ("0 / 0.286 / 0.714 (all patterns)" if m == "into_the_bar_by_step_of_changes" else "—")
    A(f"| {m} | {q} | " + " | ".join(f"{BASS[s]['old'].get(m, {}).get('median', '—')} → {BASS8[s]['new'].get(m, {}).get('median', '—')} → {BASS[s]['new'].get(m, {}).get('median', '—')}" for s in BASS) + " |")
A("\nWindows passing every test (hand-written → Run 3 → v129): " + "; ".join(
    f"song {s} " + " → ".join(f"{sum(1 for w in X[s][k] if w.get('tests') and not any(v is False for v in w['tests'].values()))} of {sum(1 for w in X[s][k] if w.get('tests'))}" for X, k in ((BASS, 'windows_old'), (BASS8, 'windows_new'), (BASS, 'windows_new'))) for s in BASS) + ".\n")
A("| Test (v129) | " + " | ".join(f"Song {s}" for s in BASS) + " |\n|---|" + "---|" * len(BASS))
for t in BASS["40"]["new"]["tests: windows passing, of windows read"]:
    A(f"| {t} | " + " | ".join("{}/{}".format(*BASS[s]['new']['tests: windows passing, of windows read'].get(t, ['—', '—'])) for s in BASS) + " |")
A("| 440 the root at every change | " + " | ".join(f"{BASS[s]['root_at_changes']['new']:.0%} of {BASS[s]['root_at_changes']['changes']}" for s in BASS) + " |\n")
A("## Tests that moved (held in the main run and the control)\n")
allk = sorted({r[0] for k in ("0", "1") for s in T[k] for r in T[k][s]}, key=lambda x: int(x))
A("| Fix | Song | Run 3 | v129 |\n|---|---|---|---|")
for f in allk:
    for s, *_ in S:
        hs = [next((r[5] for r in T[k][s] if r[0] == f), None) for k in ("0", "1")]
        if str(hs[0]) != str(hs[1]): A(f"| {f} | {s} | {held512(f, hs[0])} | {held512(f, hs[1])} |")
A("")
for s, title, seed in S:
    rows = T["1"][s]; rd = [r for r in rows if not (KP.get(r[0]) and KP[r[0]]["kept_pass"] == 0)]
    nh = sum(1 for r in rd if r[5] is True); nt = sum(1 for r in rd if isinstance(r[5], bool)); nf = [r[0] for r in rd if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test that a kept song can pass. " + (f"Not held: {', '.join(nf)}." if nf else "Every such test held.") +
      " A test no kept song passes read as a build is read is a reading of the mean of builds only (512); the last column is the share of kept songs that pass (496).\n")
    A("| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |\n|---|---|---|---|---|---|---|")
    for kk, t, ka, a, b, h in rows: A(f"| {kk} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held512(kk, h)} | {kpr(kk)} |")
    A("")
A("## The kept pass rates (496, 512)\n")
A(KP["about"] + "\n")
A("| Test | Kept pass rate | How it is read |\n|---|---|---|")
for t, x in sorted(((t, x) for t, x in KP.items() if t != "about"), key=lambda kv: int(kv[0])): A(f"| {t} | {kpr(t)} | {esc(x['how'])} |")
A("")
open(f"{H}/test_report_v129.md", "w").write("\n".join(o) + "\n" + (open(f"{H}/findings_v129.md").read() if os.path.exists(f"{H}/findings_v129.md") else ""))
print("ok")
