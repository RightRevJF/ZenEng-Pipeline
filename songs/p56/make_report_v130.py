"""Writes test_report_v130.md: song 46 (Dry Ground), the next song (522) on the default path, read by every reading of Windows 141-149
beside songs 40, 42 and 43 on both draws; the open items 530, 531, 524, 534 and 538; the regression on songs 40-45 (523); then the
findings from 540. Usage: python3 make_report_v130.py"""
import json, os, pickle, re
import numpy as np
H = "/home/claude/p56"; H55 = "/home/claude/p55"
J = json.load(open(f"{H}/read/readings_v130_p46.json")); T = json.load(open(f"{H}/read/readings_v130_p46_table.json"))
J9 = {s: json.load(open(f"{H55}/part1/readings_v129_p{s}.json")) for s in ("40", "42", "43")}
SEP = (json.load(open(f"{H}/read/sep.json")), json.load(open(f"{H}/read/sep_ctl.json")))
RR = {m: json.load(open(f"{H}/read/reread_v130_{m}.json")) for m in ("main", "ctl")}
R46 = {m: json.load(open(f"{H}/read/reread_v130_46only_{m}.json")) for m in ("main", "ctl")}
KP = json.load(open(f"{H55}/kept_pass_v129.json")); BASS = json.load(open(f"{H}/records/bass_readings_v130.json"))
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); RUN = {m: pickle.load(open(f"{H}/run/melody_v130_p56_{m}.pkl", "rb")) for m in ("main", "ctl")}
SIDE = {m: pickle.load(open(f"{H}/side/melody_v130_p56_{m}_off501.pkl", "rb")) for m in ("main", "ctl")}
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
A("# ZenEng v130: song 46, Dry Ground (the next song, 522) — test report\n")
A("*Words and music: Jason Bryant. The spec is ZenEng v130 (Module 27.74). Song 46 was written on the default path: drawn on a 438 chart with 440's step tested on the finished chart, its bass written by the routine, its record built from both. It is read by every reading of Windows 141–149 beside songs 40, 42 and 43, on both draws (479). 530, 531 and 538 were adopted as proposed and 524 is the form's rule. Songs 40–45 are closed (523) and were rerun only as a regression. The paper was not edited. New findings are numbered from 540.*\n")
A("## What was run\n")
for line in open(f"{H}/what_was_run.md").read().strip().splitlines(): A(line)
A("")
A("## Survivors and orders\n")
A("| Run | Survivors | Order | Made twice, the same |\n|---|---|---|---|")
for m, lab in (("main", "Song 46, main"), ("ctl", "Song 46, control")):
    r = J[m]["runs"]; A(f"| {lab} | {r['survivors']} | {r['order']} | {'yes' if r['reproduced'] else '**no**'} |")
for m, lab in (("main", "Song 46, main, 501 off"), ("ctl", "Song 46, control, 501 off")): A(f"| {lab} | {SIDE[m]['survivors']} | {SIDE[m]['order_fp']} | (a side run) |")
A("\n**Regression (523).** Each closed song rerun once from its v129 file, against its order of record:\n")
A("| Song | Run | Order of record (v129) | Rerun | Reproduced |\n|---|---|---|---|---|")
for row in REG["rows"]: A(f"| {row['song']} | {row['run']} | {row['record']} ({row['record_survivors']}) | {row['rerun']} ({row['rerun_survivors']}) | {'yes' if row['same'] else '**no**'} |")
A(f"\n{REG['verdict']}\n")
A("## How the v130 rules went in\n")
A("- **524 (the form gives a line room).** Q11 A laid out the form: every line of nine syllables or more has a slot of three bars or more (12 lines; none flagged, since the lyric allowed it everywhere). Verse and pre-chorus 2-2-3-3 (10 bars), chorus 2-2-3-3-2-4 (16), bridge 3-3-3-3 (12), sung outro 3-3-2-4 (12): 120 bars. The run counts, for each slot, the kept endings (465's classes, 500's shares) it cannot reach, and prints them below.")
A("- **530.** 503's knob takes the full step (×0.6 or ×1.6) each round while verse 2's chord tones on the beat are more than two points from verse 1's; within two points it stays.")
A("- **531.** 501's bound is the kept 5th–95th percentile of onsets a beat (OB501's outer pair) in place of the middle half.")
A("- **538.** In bass_v130.py: in a section with four kicks a bar, each cell of the plan (A B A C A B D E) keeps its own figure of intervals and its own articulation (legato; short off-beats; staccato; accented off-beats), with B's and D's figures and articulations drawn apart from A's.")
A("- **The song.** gen_v130.py writes melody_v130_p56.py from song 43's v129 file, patching whole statements (each asserted to match once): the form, plan, slots, lyric, the sung outro (in the verse's register, ending on the tonic), and the design (Q12 A). The design: \"water\" on the chorus's high note through 329's carrier, \"flood\" ending on the tonic and landing by the slot's third downbeat so it can hold two bars, and the last chorus's copy taking the falsetto B4 (outside the row, exempt from the range death, pinned). The four-line pre-chorus takes the verse's line plans. A smoke run (20 builds) passed before the runs of record.\n")
A("## The song's design and the pick\n")
pk = J["main"]; r352 = next(r for r in T if r[0] == "352"); r317 = next(r for r in T if r[0] == "317")
A(f"- **The pick of record:** {REC['fp']}, the refit judge's first among the survivors with no soft break (362/472); judge {REC['judge']['combined']:.2f}, rank {REC['picked_from']['rank_by_composite']} of {RUN['main']['survivors']} by the composite. No hand edits.")
A(f"- **The lift:** median {REC['lift']['median']}, top {REC['lift']['top']}, lowest {REC['lift']['lowest']}, bridge {REC['lift']['bridge']} (546).")
_m3 = re.findall(r": ([0-9.]+)\}", r317[3]); _c3 = re.findall(r": ([0-9.]+)\}", r317[4])
A(f"- **The design gate (317, Q12 A):** complete builds passing, main {float(_m3[0]):.1%} (spread {float(_m3[1]):.1%}), control {float(_c3[0]):.1%} (spread {float(_c3[1]):.1%}); nine in ten held. Design deaths {RUN['main']['deaths'].get(next(k for k in RUN['main']['deaths'] if k.startswith('design')), 0)} / {RUN['ctl']['deaths'].get(next(k for k in RUN['ctl']['deaths'] if k.startswith('design')), 0)}.")
A(f"- **The chart (438):** {esc(next(r for r in T if r[0] == '438')[3])}. 440: {esc(next(r for r in T if r[0] == '440')[3])}.\n")
A("## 524: the slots and the endings they cannot reach (main / control)\n")
A("| Line | Syllables | Slot (bars) |\n|---|---|---|")
for s, i, n, nb in RUN["main"]["rerun"]["room524"]: A(f"| {s}, line {i + 1} | {n} | {nb} |")
A("\nThe kept endings each slot cannot reach, counted over the builds (a line counted once each time it is drawn):\n")
A("| Slot | Main | Control |\n|---|---|---|")
om_, oc_ = RUN["main"]["rerun"]["out_of_reach524"], RUN["ctl"]["rerun"]["out_of_reach524"]
for k in sorted(set(om_) | set(oc_)): A(f"| {k.replace('524: ', '')} | {om_.get(k, 0)} | {oc_.get(k, 0)} |")
A("\n500's classes by notes and slot against the kept shares (532's check: each within ten points):\n")
A("| Notes, slot | Lines, main / control | Classes 0 / 1 / 2 / 3+, main | Control | Kept |\n|---|---|---|---|---|")
for b, v in J["main"]["500"]["by_notes_and_slot"].items():
    c = J["ctl"]["500"]["by_notes_and_slot"].get(b, {}); A(f"| {b} | {v['lines']} / {c.get('lines', '—')} | {v['classes']} | {c.get('classes', '—')} | {v['kept']} |")
A("")
A("## 530: the second verse, main / control\n")
v2m = key(R46["main"], "the second verse")["v130"]; v2c = key(R46["ctl"], "the second verse")["v130"]
A("| Draw | Verse 1 / verse 2, chord tones on the beat | 503's knob | Paired test, song 46 (under 0.15 kept sd, of 27) | Pair: same rhythm, onsets shared, pitch kept |\n|---|---|---|---|---|")
for lab, m, v2 in (("Main", "main", v2m), ("Control", "ctl", v2c)):
    x = J[m]["503"]; A(f"| {lab} | {x['verse1']} / {x['verse2']} | {x['knob']} | {v2['measures under 0.15 kept sd, of 27']} | {v2['pair (bars the same rhythm, onsets shared, pitch kept, notes ratio)'][:3]} |")
A("\nBeside songs 40, 42 and 43 (v129, read the same way; verse 1 / verse 2, by song): main " + "; ".join(f"{s} {v}" for s, v in key(RR["main"], "the second verse")["v130"]["chord tones on the beat, verse 1 / verse 2 (by song)"].items()) +
  "; control " + "; ".join(f"{s} {v}" for s, v in key(RR["ctl"], "the second verse")["v130"]["chord tones on the beat, verse 1 / verse 2 (by song)"].items()) + ".\n")
A("The calibration's rounds (main): " + "; ".join(f"round {k + 1} {r.get('503 (verse 1, verse 2 unaimed, knob)')}" for k, r in enumerate(RUN['main']['calibration']) if r.get('503 (verse 1, verse 2 unaimed, knob)')) + ".\n")
A("## 531: the line's rate (501), and the side runs\n")
A("| Run | 501 inside | Redrawn | Given up (with 465) | Joins before a line | Joins before a copy | Survivors |\n|---|---|---|---|---|---|---|")
for lab, D in (("Main", RUN["main"]), ("Control", RUN["ctl"]), ("Main, 501 off", SIDE["main"]), ("Control, 501 off", SIDE["ctl"])):
    st = D["stats"]; dd = D["deaths"]
    A(f"| {lab} | {st.get('501: line inside the kept onsets a beat', '—')} | {st.get('501: outside the kept onsets a beat, redrawn', '—')} | {st.get('465: class given up for a line', 0)} | {dd.get('join: no held end and breath before the line (212)', 0)} | {dd.get('join: no held end and breath before the copy (212)', 0)} | {D['survivors']} |")
A("\n| Notes | Lines, main | Onsets a beat (25, 50, 75), main / control | Kept |\n|---|---|---|---|")
for b, v in J["main"]["501"]["by_notes"].items():
    c = J["ctl"]["501"]["by_notes"].get(b, {}); A(f"| {b} | {v['lines']} | {v['onsets_a_beat']} / {c.get('onsets_a_beat', '—')} | {v['kept']} |")
A("")
A("## 534: the stream at the windows' own density (song 46 alone)\n")
A("| Band | Measure | Kept | Main | Control | Windows, main / control |\n|---|---|---|---|---|---|")
dm, dc = R46["main"]["at the windows' own density (kept, run)"]["v130"], R46["ctl"]["at the windows' own density (kept, run)"]["v130"]
for b in dm:
    for mm in ("equal_gap_run_max", "gap_same_as_before", "zigzag_of_three", "gap_eighth", "turns_per_move", "range"):
        A(f"| {b} | {mm} | {dm[b][mm][0]} | {dm[b][mm][1]} | {dc.get(b, {}).get(mm, ['—', '—'])[1]} | {dm[b]['windows']} / {dc.get(b, {}).get('windows', 0)} |")
A(f"\n505's drawable runs (kept, (onsets, share)): main {esc(J['main']['505']['drawable_runs'])}; control {esc(J['ctl']['505']['drawable_runs'])}. 504's notes to syllables: {J['main']['504']['notes_to_syllables']} / {J['ctl']['504']['notes_to_syllables']}.\n")
A("## Separation on both draws (479), song 46 beside songs 40, 42 and 43\n")
A("The agreed 30 measures, both collections pooled, the first 400 complete builds of each run. Songs 40, 42 and 43 are their v129 runs of record. Main / control.\n")
A("| Family | Within: 46 | Within: 40 / 42 / 43 | Across, 46's pairs | Across, 40/42/43 among themselves | Across, all four |\n|---|---|---|---|---|---|")
for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)"):
    cells = []
    for i in (0, 1):
        a = SEP[i]["family"][f]; pr = [v for k, v in a["across"].items() if "46" in k]
        cells.append((a["within"]["46"], f"{a['within']['40']} / {a['within']['42']} / {a['within']['43']}", round(float(np.mean(pr)), 3), a["across_mean_40_42_43"], a["across_mean"]))
    A(f"| {f} | {cells[0][0]} / {cells[1][0]} | {cells[0][1]}; {cells[1][1]} | {cells[0][2]} / {cells[1][2]} | {cells[0][3]} / {cells[1][3]} | {cells[0][4]} / {cells[1][4]} |")
A("\nCosts on the 30, pooled over the four songs (points; kept mean, builds' mean):\n")
for i, lab in ((0, "main"), (1, "control")): A(f"- **{lab}** (gap {SEP[i]['costs_agreed_30']['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP[i]["costs_agreed_30"]["eight"][:6]))
A("")
A("## The first verse and chorus beside the kept songs (both draws)\n")
A("Window 147's measures, with the window taken the engine's way (519: every note sung in the eight bars, the chord at the note; songs 43 and 46 on A minor). Each song's mean, main / control.\n")
fv = {m: key(RR[m], "first verse and chorus") for m in RR}; mo = {m: key(RR[m], "the melody over chord") for m in RR}
A("| Measure | Billboard | Rolling Stone | Song 46 | Song 40 | Song 42 | Song 43 |\n|---|---|---|---|---|---|---|")
for m in list(fv["main"]) + list(mo["main"]):
    src = fv if m in fv["main"] else mo; r0, r1 = src["main"][m], src["ctl"][m]; a0, a1 = r0["v130_by_song"], r1["v130_by_song"]   # order 40, 42, 43, 46
    A(f"| {m} | {r0['billboard']} | {r0['rolling_stone']} | {a0[3]} / {a1[3]} | {a0[0]} / {a1[0]} | {a0[1]} / {a1[1]} | {a0[2]} / {a1[2]} |")
A("")
A("## The judge of record (519)\n")
A("| Song | Content mean, main / control | Under −0.72, main / control |\n|---|---|---|")
A(f"| 46 | {J['main']['519']['content_mean']} / {J['ctl']['519']['content_mean']} | {J['main']['519']['under_kept_song_5th']:.0%} / {J['ctl']['519']['under_kept_song_5th']:.0%} |")
for s in ("40", "42", "43"): A(f"| {s} (v129) | {J9[s]['main']['519']['content_mean']} / {J9[s]['ctl']['519']['content_mean']} | {J9[s]['main']['519']['under_kept_song_5th']:.0%} / {J9[s]['ctl']['519']['under_kept_song_5th']:.0%} |")
A("")
A("## The range beside the design (520: not aimed)\n")
A("| Song | Verse window, main / control | Chorus window, main / control | Kept | The design |\n|---|---|---|---|---|")
A(f"| 46 | {J['main']['520']['range']['verse']} / {J['ctl']['520']['range']['verse']} | {J['main']['520']['range']['chorus']} / {J['ctl']['520']['range']['chorus']} | 10.9 | Q12 A: the falsetto B4 once, in the last chorus (outside these windows) |")
for s in ("40", "42", "43"): A(f"| {s} (v129) | {J9[s]['main']['520']['range']['verse']} / {J9[s]['ctl']['520']['range']['verse']} | {J9[s]['main']['520']['range']['chorus']} / {J9[s]['ctl']['520']['range']['chorus']} | 10.9 | {J9[s]['main']['520']['range']['design'] or 'none'} |")
A("")
A("## The bass (538): song 46's record, v129's routine beside v130's\n")
A("Each section's eight bars read with Window 144's measures() against the pop-and-rock quartiles. Window medians, v129's routine → v130's (the record):\n")
ms = ("notes_per_bar", "pitch_classes_per_bar", "on_the_bars_first_note", "iv_repeat", "iv_step", "iv_octave", "bar_rhythm_same_as_last", "distinct_bar_rhythms", "kick_with_bass", "bass_with_kick_kicked_bars", "into_the_bar_by_step_of_changes")
a_, b_ = BASS["v129 routine (538 off)"], BASS["v130 routine (538), the record"]
A("| Measure | Pop and rock (25, 50, 75) | Song 46 |\n|---|---|---|")
for m in ms:
    q = (b_["summary"].get(m, {}) or {}).get("pop_rock_quartiles") or "—"
    A(f"| {m} | {q} | {a_['summary'].get(m, {}).get('median', '—')} → {b_['summary'].get(m, {}).get('median', '—')} |")
A("\n| Window | Four kicks a bar | Onset rhythms | Onsets and lengths | Rhythm and figure | Every test passed |\n|---|---|---|---|---|---|")
for wa, wb in zip(a_["windows"], b_["windows"]):
    if not wb.get("tests"): continue
    ca, cb = wa["cells538"], wb["cells538"]
    A(f"| {wb['sec']}, bar {wb['bar'] + 1} | {'yes' if wb['four'] else 'no'} | {ca['rhythms']} → {cb['rhythms']} | {ca['rhythm_and_articulation']} → {cb['rhythm_and_articulation']} | {ca['rhythm_and_figure']} → {cb['rhythm_and_figure']} | {'yes' if not any(v is False for v in wa['tests'].values()) else 'no'} → {'yes' if not any(v is False for v in wb['tests'].values()) else 'no'} |")
A("\n| Test | v129's routine | v130's (the record) |\n|---|---|---|")
for t in b_["summary"]["tests: windows passing, of windows read"]:
    A(f"| {t} | {'{}/{}'.format(*a_['summary']['tests: windows passing, of windows read'].get(t, ['—', '—']))} | {'{}/{}'.format(*b_['summary']['tests: windows passing, of windows read'][t])} |")
A(f"| 440 the root at every change | {a_['root_at_changes'][0]:.0%} of {a_['root_at_changes'][1]} | {b_['root_at_changes'][0]:.0%} of {b_['root_at_changes'][1]} |\n")
rows = T; rd = [r for r in rows if not (KP.get(r[0]) and KP[r[0]]["kept_pass"] == 0)]
nh = sum(1 for r in rd if r[5] is True); nt = sum(1 for r in rd if isinstance(r[5], bool)); nf = [r[0] for r in rd if r[5] is False]
A("## The table of tests: Song 46, Dry Ground\n")
A(f"Held in both the main run and the control: {nh} of {nt} with a test that a kept song can pass. " + (f"Not held: {', '.join(nf)}." if nf else "Every such test held.") +
  " Many tests name songs 40–45 in their wording; they are read here on song 46's runs. A test no kept song passes read as a build is read is a reading of the mean of builds only (512); the last column is the share of kept songs that pass (496).\n")
A("| Fix | Test | Read against | Main | Control | Held? | Kept pass rate |\n|---|---|---|---|---|---|---|")
for kk, t, ka, a, b, h in rows: A(f"| {kk} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held512(kk, h)} | {kpr(kk)} |")
A("")
A("## The kept pass rates (496, 512)\n")
A(KP["about"] + "\n")
A("| Test | Kept pass rate | How it is read |\n|---|---|---|")
for t, x in sorted(((t, x) for t, x in KP.items() if t != "about"), key=lambda kv: int(kv[0])): A(f"| {t} | {kpr(t)} | {esc(x['how'])} |")
A("")
tail = open(f"{H}/findings_v130.md").read() + "\n" + open(f"{H}/report_tail_v130.md").read()
open(f"{H}/test_report_v130.md", "w").write("\n".join(o) + "\n" + tail)
print("ok")
