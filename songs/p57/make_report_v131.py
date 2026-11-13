"""Writes test_report_v131.md: song 47 (The Singer Doesn't Stop), written with dense verse lines on the v131 path; 527 at intake; 526 (the
judge that has not seen the song) before any refit; empty bars and the stream beside the kept figures; 525/540, 541, 542; the regression on
songs 40-46 (523); then the findings from 550. Usage: python3 make_report_v131.py"""
import json, os, pickle, re
import numpy as np
H = "/home/claude/p57"; H55 = "/home/claude/p55"
J = json.load(open(f"{H}/read/readings_v131_p47.json")); T = json.load(open(f"{H}/read/readings_v131_p47_table.json"))
J46 = json.load(open("/home/claude/p56/read/readings_v130_p46.json")); J9 = {s: json.load(open(f"{H55}/part1/readings_v129_p{s}.json")) for s in ("40", "42", "43", "44", "45")}
SEP = (json.load(open(f"{H}/read/sep.json")), json.load(open(f"{H}/read/sep_ctl.json"))); JU = json.load(open(f"{H}/read/judge526.json"))
RR = {m: json.load(open(f"{H}/read/reread_v131_{m}.json")) for m in ("main", "ctl")}; R47 = {m: json.load(open(f"{H}/read/reread_v131_47only_{m}.json")) for m in ("main", "ctl")}
KP = json.load(open(f"{H55}/kept_pass_v129.json")); K525 = json.load(open(f"{H}/tables/zeneng_v131_kept_slots.json"))
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); RUN = {m: pickle.load(open(f"{H}/run/melody_v131_p57_{m}.pkl", "rb")) for m in ("main", "ctl")}
REG = json.load(open(f"{H}/regress/regression.json"))
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else "—" if h is None else str(h)
def key(d, start): return next(v for k, v in d.items() if k.startswith(start))
def kpr(t):
    x = KP.get(t)
    if not x: return "—"
    return f"{x['kept_pass']:.0%} of {x['songs']} kept songs" if x["kept_pass"] is not None else "no kept rate"
def held512(t, h):
    x = KP.get(t)
    if x and x["kept_pass"] == 0 and isinstance(h, bool): return f"a reading of the mean of builds (512; {'inside' if h else 'outside'} the band)"
    return held(h)
o = []; A = o.append
A("# ZenEng v131: song 47, The Singer Doesn't Stop — test report\n")
A("*Words and music: Jason Bryant. The spec is ZenEng v131 (Module 27.75). 540, 541 and 542 were ported as proposed. 525 reads the kept endings by the slot's bars from zeneng_v131_kept_slots.json. 527 set each line's slot at intake against the kept slots for its syllables. 526 reads the new song first by a judge that has not seen it. At the other AI's suggestion, song 47 has dense, wordy verse lines: the case 534 still needed. Songs 40–46 were rerun only as a regression. The paper was not edited. New findings are numbered from 550.*\n")
A("## What was run\n")
for line in open(f"{H}/what_was_run.md").read().strip().splitlines(): A(line)
A("")
A("## Survivors and orders\n")
A("| Run | Survivors | Order | Made twice, the same |\n|---|---|---|---|")
for m, lab in (("main", "Song 47, main"), ("ctl", "Song 47, control")):
    r = J[m]["runs"]; A(f"| {lab} | {r['survivors']} | {r['order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("\nDeaths, main: " + "; ".join(f"{k} {v}" for k, v in RUN["main"]["deaths"].most_common()) + ".\n")
A("**Regression (523).** Each closed song rerun once from its file of record, against its order of record:\n")
A("| Song | Run | Order of record | Rerun | Reproduced |\n|---|---|---|---|---|")
for row in REG["rows"]: A(f"| {row['song']} | {row['run']} | {row['record']} ({row['record_survivors']}) | {row['rerun']} ({row['rerun_survivors']}) | {'yes' if row['same'] else '**no**'} |")
A(f"\n{REG['verdict']}\n")
A("## 527 at intake: each line's slot beside the kept slots for its syllables\n")
A("Every line has a two-bar slot (the writer's choice A). The share is that of kept lines with the same syllable count that take a two-bar slot (the file's table by syllables). A line is flagged only under a tenth.\n")
A("| Line | Syllables | Slot | Kept share of that slot | Flagged |\n|---|---|---|---|---|")
for s, i, n, nb, sh in RUN["main"]["rerun"]["room527"]: A(f"| {s}, line {i + 1} | {n} | {nb} bars | {sh:.0%} | {'**yes**' if sh < 0.10 else 'no'} |")
A("")
A("## 526: the song read first by a judge that has not seen it\n")
A("The judge of record's 37 measures; median fill (the fitting set's), z-scored, L2 logistic with C = 0.3, the kept and build sides weighted alike. Windows: the first verse's and first chorus's first eight bars, the engine's own reading. Kept side: CoCoPops and BiMMuDa 1958–1991 (zeneng_v131_kept_windows.json, 545 windows of 285 pieces), split in half by piece, fitted on one half and tested on the other, eight splits. Song 47 is scored by a judge fitted on songs 40–46; each earlier song by a judge refitted on the other five. AUC (0.5 is none), mean ± spread, main / control.\n")
A("| Song | Separation by a judge that has not seen it | The standing judge: content mean | Under −0.72 |\n|---|---|---|---|")
ms = {m: JU["draws"][m]["mean and spread"] for m in ("main", "ctl")}
def stand(s):
    if s == "47": a, b = J["main"]["519"], J["ctl"]["519"]
    elif s == "46": a, b = J46["main"]["519"], J46["ctl"]["519"]
    else: a, b = J9[s]["main"]["519"], J9[s]["ctl"]["519"]
    return f"{a['content_mean']} / {b['content_mean']}", f"{a['under_kept_song_5th']:.0%} / {b['under_kept_song_5th']:.0%}"
for s in ("47", "40", "42", "43", "44", "45", "46"):
    k = next(x for x in ms["main"] if x.startswith(s + " ")); a, b = ms["main"][k], ms["ctl"][k]; st = stand(s)
    A(f"| {s}{' (fitted on 40–46)' if s == '47' else ' (fitted on the other five)'} | {a[0]} ± {a[1]} / {b[0]} ± {b[1]} | {st[0]} | {st[1]} |")
A("\nNo refit was made before these were printed. Beside them, separation within the song on the agreed 30 (a judge fitted on the song's own builds), song 47 beside 40, 42 and 43, main / control:\n")
A("| Family | Within: 47 | Within: 40 / 42 / 43 | Across, 47's pairs | Across, 40/42/43 among themselves |\n|---|---|---|---|---|")
for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)"):
    c = []
    for i in (0, 1):
        a = SEP[i]["family"][f]; pr = [v for k, v in a["across"].items() if "47" in k]
        c.append((a["within"]["47"], f"{a['within']['40']} / {a['within']['42']} / {a['within']['43']}", round(float(np.mean(pr)), 3), a["across_mean_40_42_43"]))
    A(f"| {f} | {c[0][0]} / {c[1][0]} | {c[0][1]}; {c[1][1]} | {c[0][2]} / {c[1][2]} | {c[0][3]} / {c[1][3]} |")
A("")
A("## Empty bars and the stream beside the kept figures (527)\n")
fv = {m: key(R47[m], "first verse and chorus") for m in R47}
A("Window 147's measures on song 47's first verse and chorus (the engine's window), main / control, beside the kept songs and song 46.\n")
A("| Measure | Billboard | Rolling Stone | Song 47 | Song 46 (main) |\n|---|---|---|---|---|")
fv46 = key(json.load(open("/home/claude/p56/read/reread_v130_46only_main.json")), "first verse and chorus")
for m_ in ("empty_bars", "gap_same_as_before", "equal_gap_run_max", "gap_entropy", "gap_eighth", "notes_per_bar", "most_onsets_in_a_beat", "range", "turns_per_move", "last_note_tonic", "zigzag_of_three"):
    r0, r1 = fv["main"][m_], fv["ctl"][m_]
    A(f"| {m_} | {r0['billboard']} | {r0['rolling_stone']} | {r0['v131']} / {r1['v131']} | {fv46[m_]['v130'] if m_ in fv46 else '—'} |")
A("\nAt the windows' own density (song 47 alone; kept, main, control):\n")
A("| Band | Measure | Kept | Main | Control | Windows |\n|---|---|---|---|---|---|")
dm, dc = R47["main"]["at the windows' own density (kept, run)"]["v131"], R47["ctl"]["at the windows' own density (kept, run)"]["v131"]
for b in dm:
    for mm in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three", "gap_eighth", "turns_per_move", "range"):
        A(f"| {b} | {mm} | {dm[b][mm][0]} | {dm[b][mm][1]} | {dc.get(b, {}).get(mm, ['—', '—'])[1]} | {dm[b]['windows']} / {dc.get(b, {}).get('windows', 0)} |")
A(f"\n505's drawable runs (kept, (onsets, share)): main {esc(J['main']['505']['drawable_runs'])}; control {esc(J['ctl']['505']['drawable_runs'])}. Run weights by band: main {esc(J['main']['505']['run_weights'])}.\n")
A("## 525 and 540: the ending classes by the slot's bars and the line's notes\n")
A("Drawn against zeneng_v131_kept_slots.json (by notes, two-bar slots). The readings table's own 'kept' column still shows v129's combined shares; the file's shares are the ones of record here.\n")
A("| Notes, slot | Lines, main / control | Classes 0 / 1 / 2 / 3+, main | Control | Kept (525) |\n|---|---|---|---|---|")
for b, v in J["main"]["500"]["by_notes_and_slot"].items():
    c = J["ctl"]["500"]["by_notes_and_slot"].get(b, {}); band = b.split(" notes")[0]; slot = b.split(", ")[1].split("-")[0]
    kk = K525["525: ending classes by slot bars and by NOTES in the line"][slot][band]["shares"]
    A(f"| {b} | {v['lines']} / {c.get('lines', '—')} | {v['classes']} | {c.get('classes', '—')} | {[round(x, 3) for x in kk]} |")
A("\nThe kept endings each slot could not reach, counted over the builds (main / control):\n")
A("| Slot | Main | Control |\n|---|---|---|")
om_, oc_ = RUN["main"]["rerun"]["out_of_reach524"], RUN["ctl"]["rerun"]["out_of_reach524"]
for k in sorted(set(om_) | set(oc_)): A(f"| {k.replace('524: ', '')} | {om_.get(k, 0)} | {oc_.get(k, 0)} |")
A("")
A("## 541: the second verse, main / control\n")
v2m, v2c = key(R47["main"], "the second verse")["v131"], key(R47["ctl"], "the second verse")["v131"]
A("| Draw | Verse 1 / verse 2, chord tones on the beat (engine's window) | 503's knob | Paired test, song 47 (of 27) |\n|---|---|---|---|")
for lab, m, v2 in (("Main", "main", v2m), ("Control", "ctl", v2c)):
    x = J[m]["503"]; A(f"| {lab} | {x['verse1']} / {x['verse2']} | {x['knob']} | {v2['measures under 0.15 kept sd, of 27']} |")
A("\nThe calibration's rounds (main): " + "; ".join(f"round {k + 1} {r.get('503 (verse 1, verse 2 unaimed, knob)')}" for k, r in enumerate(RUN['main']['calibration']) if r.get('503 (verse 1, verse 2 unaimed, knob)')) + ".\n")
A("## 542: 501's give-ups counted apart from 465's\n")
A("| Count | Main | Control |\n|---|---|---|")
g_m, g_c = RUN["main"]["rerun"]["giveups542"], RUN["ctl"]["rerun"]["giveups542"]
for k in sorted(set(g_m) | set(g_c)): A(f"| {k} | {g_m.get(k, 0)} | {g_c.get(k, 0)} |")
A("\n| Notes | Lines, main | Onsets a beat (25, 50, 75), main / control | Kept |\n|---|---|---|---|")
for b, v in J["main"]["501"]["by_notes"].items():
    c = J["ctl"]["501"]["by_notes"].get(b, {}); A(f"| {b} | {v['lines']} | {v['onsets_a_beat']} / {c.get('onsets_a_beat', '—')} | {v['kept']} |")
A("")
A("## The designs and the pick\n")
r317 = next(r for r in T if r[0] == "317")
_m3 = re.findall(r": ([0-9.]+)", r317[3]); _c3 = re.findall(r": ([0-9.]+)", r317[4])
A(f"- **The pick of record:** {REC['fp']}, the refit judge's first among the survivors with no soft break (362/472); judge {REC['judge']['combined']:.2f}, rank {REC['picked_from']['rank_by_composite']} of {RUN['main']['survivors']} by the composite. No hand edits. Lift: {REC['lift_reading']}.")
A(f"- **The design gates (317):** the hook, {float(_m3[0]):.1%} / {float(_c3[0]):.1%}; the bridge's build, {float(_m3[1]):.1%} / {float(_c3[1]):.1%} (main / control).")
A(f"- **The chart (438):** {esc(next(r for r in T if r[0] == '438')[3])}. 440: {esc(next(r for r in T if r[0] == '440')[3])}.")
A(f"- **The lift:** bars {REC['lift']['bars'][0] + 1}–{REC['lift']['bars'][-1] + 1} a whole step up in the record (voice and chords). The engine drew them in G under its search row's top, G4, so the held 'do' sounds A4.\n")
A("## The range (520: not aimed)\n")
A(f"Verse window {J['main']['520']['range']['verse']} / {J['ctl']['520']['range']['verse']}; chorus window {J['main']['520']['range']['chorus']} / {J['ctl']['520']['range']['chorus']} (kept 10.9).\n")
rows = T; rd = [r for r in rows if not (KP.get(r[0]) and KP[r[0]]["kept_pass"] == 0)]
nh = sum(1 for r in rd if r[5] is True); nt = sum(1 for r in rd if isinstance(r[5], bool)); nf = [r[0] for r in rd if r[5] is False]
A("## The table of tests: Song 47, The Singer Doesn't Stop\n")
A(f"Held in both the main run and the control: {nh} of {nt} with a test that a kept song can pass. " + (f"Not held: {', '.join(nf)}." if nf else "Every such test held.") +
  " Many tests name songs 40–46 in their wording; they are read here on song 47's runs. 311 reads the last chorus's last line (a return, 90.7% / 96.4% on the tonic); the song's last line, the tag's, is on the tonic in every complete build. 500's 'kept' column is v129's; 525's file is above.\n")
A("| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |\n|---|---|---|---|---|---|---|")
for kk, t, ka, a, b, h in rows: A(f"| {kk} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held512(kk, h)} | {kpr(kk)} |")
A("")
tail = open(f"{H}/findings_v131.md").read() + "\n" + open(f"{H}/report_tail_v131.md").read()
open(f"{H}/test_report_v131.md", "w").write("\n".join(o) + "\n" + tail)
print("ok")
