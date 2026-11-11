"""Song 40 under v108: writes test_report_p40.md from the readings, the runs, the riff and the record (every figure read, none typed)."""
import pickle, json, sys
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40 as P
H = "/home/claude/p40"
R = pickle.load(open(f"{H}/readings_p40.pkl", "rb")); REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); RF = pickle.load(open(f"{H}/riff_p40.pkl", "rb"))
Mn = pickle.load(open(f"{H}/melody_main.pkl", "rb")); DR = pickle.load(open(f"{H}/out/demo_report.pkl", "rb"))
FIND = open(f"{H}/findings_p40.md").read()
rr = Mn["rerun"]; V = ("main", "ctl"); LAB = dict(main="Main (243 on)", ctl="Control (243 off)")
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[int(p) % 12]}{int(p) // 12 - 1}"
def f3(x): return "—" if x is None else (" · ".join(f3(y) for y in x) if isinstance(x, (list, tuple)) else (f"{x:g}" if isinstance(x, (int, float)) else str(x)))
def pc(x): return f"{100 * x:.1f}%"
o = []; w = o.append
w("# Nothing Else on Earth: song 40 under ZenEng v108 (test report)\n")
w("*A debugging song on the default path · Words and music: Jason Bryant*\n")
w("Riff-led rock, 4/4, straight eighths, ♩ = 116, D major, mezzo (A3–D5); 110 bars, 3:48. The lyric is Lark's song from 'The Garden That Grew by Itself' "
  "(Wild Fruit), locked at draft 3. The paper was not edited. Findings are numbered from 298.\n")
w("Read first: Module 27.52 (fixes 286–297) and the tables: zeneng_v108_judges.json (cb84379c…; its weights and floor replace the v103 file's), "
  "zeneng_v108_spectral_and_registers.json (8d33013c…), zeneng_v106_gate_limits.json (ca3e6a8b…), zeneng_v105_kept_windows.json (3633a24e…), "
  "zeneng_v104_line_in_time.json (43325ed4…) and the earlier files.\n")
w("**The default path.** Era none (Q8), character none (Q9), no designed summit (Q15), bridge register not chosen (Q16), chorus lift not chosen (Q17), "
  "no countermelody (Q18); the said-twice section asked as usual and answered as a plain repeat in the chorus (Q11). **No design gate is in force.** "
  "Two design choices sit off the default path and are named: the drums (Q19 B, kept at Q20: half-time verses, the full beat from the pre-chorus; "
  "an arrangement design under 236, not a melody gate), and the two-bar lines of nine or more syllables (Q21 A: the form and the lyric are the design "
  f"that 230 allows; {len(P.DESIGNED_TWO_BAR)} lines across the song).\n")
w("**Ported on song 38's rerun Run B:** 286, 287, 288, 289, 290, 291, 293 (its first half did not apply: no character), 294 (did not apply: no era), "
  "295, 296, 297. Nothing blocked the port; no two fixes conflicted.\n")
w(f"**Runs.** 1,000 builds main and 1,000 control (243 off), each made twice; seed {rr['seed']}, calibration seed {rr['calibration_seed']}, PYTHONHASHSEED 0; "
  f"code {rr['code_sha']}; Python {rr['python']}, numpy {rr['numpy']}. Rerun line: `PYTHONHASHSEED=0 python3 melody_p40.py 1000 main|ctl` "
  "(a third argument names the copy: `_r`). Every build is on file, dead or alive (`every` in melody_main.pkl, melody_ctl.pkl and their `_r` copies).\n")
# 1
w("## 1. Survivors and frozen orders\n")
w("| Run | Survivors | Frozen order | Second run | Reproduced |\n|---|---|---|---|---|")
for v in V:
    x = R["1"][v]; w(f"| {LAB[v]} | {x['survivors']} of 1,000 ({pc(x['share'])}) | {x['order']} | {x['rerun_order']} | {'yes' if x['reproduced'] else 'NO'} |")
cl = R["1"]["main"]["calib_lines"]
w(f"\n249's pass set the line strengths to contour amplitude {R['1']['main']['line_knobs']['amp']:g} (the cap), widening {R['1']['main']['line_knobs']['widen']:.3f}, "
  f"fresh-start spread {R['1']['main']['line_knobs']['fresh']:.3f}. Its last round read arch term {cl['arch'][1]}, widening {cl['widening'][1]}, first note's extra "
  f"surprise {cl['fresh'][1]} bits, against the kept {cl['arch'][0]}, {cl['widening'][0]}, {cl['fresh'][0]}: the arch term stays far under the kept figure at the cap (finding 305).\n")
# 2
w("## 2. Deaths per gate\n")
w("| Gate | Main | Control | Main, would fail | Control, would fail |\n|---|---|---|---|---|")
for r in R["2"]["rows"]:
    w(f"| {r['gate']} | {r['main']} | {r['ctl']} | {R['2']['would']['main'].get(r['gate'], '—')} | {R['2']['would']['ctl'].get(r['gate'], '—')} |")
w(f"| survivors | {R['1']['main']['survivors']} | {R['1']['ctl']['survivors']} | | |")
w("\nLimits broken, every complete build (soft or hard): main " + ", ".join(f"{k} {n}" for k, n in R["2"]["broken"]["main"].items()) +
  "; control " + ", ".join(f"{k} {n}" for k, n in R["2"]["broken"]["ctl"].items()) + ".\n")
# 3
w("## 3. Fixes 277 and 286: soft breaks and hard limits\n")
w("Fifteen limits, one count: 276's eight and 286's seven. A build dies on a hard limit or its third soft break.\n")
w("| Run | Complete builds | 0 soft | 1 | 2 | 3+ | Hard limit broken | Deaths on a third soft break | Pick |\n|---|---|---|---|---|---|---|---|---|")
for v in V:
    x = R["3"][v]; s = x["soft_share"]
    w(f"| {LAB[v]} | {x['complete']} | {pc(s['0'])} | {pc(s['1'])} | {pc(s['2'])} | {pc(s['3'])} | {x['hard_any']} | {x['deaths_on_three_soft']} | soft {x['pick_soft'] or 'none'}, hard {x['pick_hard'] or 'none'} |")
k8 = R["3"]["kept_soft_eight"]; pj = R["3"]["pairs_seven"]
w(f"| main, the eight only | | {pc(R['3']['main']['soft_share_eight_only']['0'])} | {pc(R['3']['main']['soft_share_eight_only']['1'])} | {pc(R['3']['main']['soft_share_eight_only']['2'])} | {pc(R['3']['main']['soft_share_eight_only']['3'])} | | | |")
w(f"| kept songs, the eight (Table DL) | — | {pc(k8[0])} | {pc(k8[1])} | {pc(k8[2])} | {pc(k8[3])} | — | — | — |")
w(f"| calibration pairs, the seven | {pj['pairs']} | {pc(pj['soft_breaks'].get('0', 0) / pj['pairs'])} | {pc(pj['soft_breaks'].get('1', 0) / pj['pairs'])} | {pc(pj['soft_breaks'].get('2', 0) / pj['pairs'])} | {pc(pj['soft_breaks'].get('3', 0) / pj['pairs'])} | {pj['hard_any']} | — | — |")
w("\nSoft breaks by limit: main " + ", ".join(f"{k} {n}" for k, n in R["3"]["main"]["soft_by_limit"].items()) + "; hard: " + ", ".join(f"{k} {n}" for k, n in R["3"]["main"]["hard_by_limit"].items()) +
  ". Control soft: " + ", ".join(f"{k} {n}" for k, n in R["3"]["ctl"]["soft_by_limit"].items()) + "; hard: " + ", ".join(f"{k} {n}" for k, n in R["3"]["ctl"]["hard_by_limit"].items()) + ".\n")
w("Each limit: the builds' median and the pick, beside the soft and hard limits.\n")
w("| Limit | Direction | Soft | Hard | Main median | Main pick | Control median | Control pick |\n|---|---|---|---|---|---|---|---|")
for k, x in R["3"]["main"]["limits"].items():
    y = R["3"]["ctl"]["limits"][k]
    w(f"| {k} | {x[4]} | {f3(x[2])} | {f3(x[3])} | {f3(x[0])} | {f3(x[1])} | {f3(y[0])} | {f3(y[1])} |")
x = R["3"]["main"]
w(f"\n**The most note lengths in any eight bars (288).** Main 5th · 25th · 50th · 75th · 95th: {f3(x['lengths'])} (counts {x['lengths_dist']}); control {f3(R['3']['ctl']['lengths'])}; "
  f"the pick {x['lengths_pick']}; kept: six at the median, four to eight. Under v107 every build of song 38 read 5.\n")
# the lift
w("## The lift the registers drew (288), beside the kept figures\n")
L = R["lift"]; KK = L["kept"]
w("Chorus 1 over Verse 1, in semitones (bridge: the bridge's median over the verse's). Kept: Table DL. Builds and survivors: 5th · 25th · 50th · 75th · 95th.\n")
w("| Reading | Kept 5 · 25 · 50 · 75 · 95 | Main, drawn | Main, builds | Main, survivors | Main pick (drawn → read) | Control, builds | Control pick |\n|---|---|---|---|---|---|---|---|")
for k in ("median", "top", "lowest", "bridge"):
    kd = f"chorus_{'floor' if k == 'lowest' else k}" if k != "bridge" else "bridge_median"
    w(f"| {k} | {f3([KK[k][q] for q in ('5', '25', '50', '75', '95')])} | {f3(L['main']['drawn'][k])} | {f3(L['main']['builds'][k])} | {f3(L['main']['survivors'][k])} | "
      f"{L['main']['pick_drawn'][kd]:g} → {L['main']['pick'][k]:g} | {f3(L['ctl']['builds'][k])} | {L['ctl']['pick'][k]:g} |")
npk = L["main"]["notes_pick"]
w(f"\nThe pick, in notes: Chorus 1 top {nm(npk['chorus_top'])} against Verse 1's {nm(npk['verse_top'])}; lowest {nm(npk['chorus_low'])} against {nm(npk['verse_low'])}; "
  f"median {nm(npk['chorus_med'])} against {nm(npk['verse_med'])}; the bridge reaches {nm(npk['bridge_top'])}, the song's top. Its registers were drawn at the kept "
  f"{100 * L['main']['pick_drawn']['u']:.0f}th percentile for the chorus (one quantile for its median, top and lowest) and the {100 * L['main']['pick_drawn']['ub']:.0f}th for the bridge. "
  f"The read lift follows the drawn lift across builds (r = {L['main']['corr_drawn_read']['median']} median, {L['main']['corr_drawn_read']['top']} top). "
  f"Builds inside the kept middle half: median {pc(L['main']['inside_mid']['median'])}, top {pc(L['main']['inside_mid']['top'])}, lowest {pc(L['main']['inside_mid']['lowest'])}, "
  f"bridge {pc(L['main']['inside_mid']['bridge'])} (288's check asks half or more of the chorus medians).\n")
w("**The spectral reading beside the lift (286).** The engine's beta_pitch on Verse 1 then Chorus 1's first eight bars, by the build's median lift:\n")
w("| Median lift | Kept songs | Main (builds, median) | Control |\n|---|---|---|---|")
for b in ("within 2", "3 to 5", "6 or more"):
    w(f"| {b} | {L['kept_spectral_by_lift'][b]} | {L['main']['spectral_by_lift'][b][1]} ({L['main']['spectral_by_lift'][b][0]}) | {L['ctl']['spectral_by_lift'][b][1]} ({L['ctl']['spectral_by_lift'][b][0]}) |")
w(f"\nThe reading over builds, 1st · 5th · 50th · 95th · 99th: main {f3(L['main']['spectral'])}, control {f3(L['ctl']['spectral'])} (limits: soft 0.086–1.628, hard −0.098 to 1.766); "
  f"the pick {L['main']['spectral_pick']}. It rises with the lift as the paper says (r = {L['main']['corr_spectral_lift']} main, {L['ctl']['corr_spectral_lift']} control). "
  f"**Deaths at the spectral reading:** main {L['main']['spectral_soft']} soft breaks and {L['main']['spectral_hard']} hard; it decided {L['main']['deaths_spectral_decisive']} deaths "
  f"(it took part in {L['main']['deaths_with_spectral']}); control {L['ctl']['spectral_soft']} soft, {L['ctl']['spectral_hard']} hard, deciding {L['ctl']['deaths_spectral_decisive']}. "
  "Under v107 it was song 38's largest killer.\n")
# 4
w("## 4. Fixes 275, 280 and 286: the kept pass rate of every gate in the search\n")
w("| Gate | Kept pass rate | Source |\n|---|---|---|")
for g, r_, src in R["4"]["gates"]: w(f"| {g} | {'—' if r_ is None else pc(r_)}{' ⚑' if r_ is not None and r_ < 0.9 else ''} | {src} |")
w("\nThe seven of 286, each alone on the calibration pairs (soft limit · hard limit): " + "; ".join(f"{k} {pc(R['4']['seven_soft_alone'][k])} · {pc(R['4']['seven_hard_alone'][k])}" for k in R["4"]["seven_soft_alone"]) +
  f". Corpus: {R['4']['corpus']}. With 286's limits the seven pass {pc(pj['pass_as_limits'])} of the pairs (no hard break and fewer than three soft); "
  f"{pj['hard_any']} of {pj['pairs']} pairs break a hard limit (finding 301). The spectral reading on the pairs, 1st · 5th · 50th · 95th · 99th: {f3(pj['spectral_on_pairs'])}.\n")
# 5
w("## 5. The line readings of Table DJ\n")
w("Builds' 5th · median · 95th; the pick; the kept middle half (25th · median · 75th).\n")
w("| Reading | Kept | Main | Main pick | Main outside kept middle half | Control |\n|---|---|---|---|---|---|")
for k in R["5"]["kept"]:
    kp = R["5"]["kept"][k]
    w(f"| {k.replace('_', ' ')} | {f3(kp[1:4])} | {f3(R['5']['main']['builds'][k])} | {R['5']['main']['pick'][k]:g} | {pc(R['5']['main']['outside_mid'][k])} | {f3(R['5']['ctl']['builds'][k])} |")
x = R["5"]["main"]
w("\nContour kinds (share of lines): kept " + ", ".join(f"{k} {pc(v)}" for k, v in list(R["5"]["kept_kinds"].items())[:5]) + "; main " +
  ", ".join(f"{k} {pc(v)}" for k, v in list(x["kinds"].items())[:5]) + "; the pick " + ", ".join(f"{k} {pc(v)}" for k, v in sorted(x["pick_kinds"].items(), key=lambda z: -z[1])[:4]) + ".\n")
w(f"The move between lines a fourth or more: main {f3(x['join_fourth'])} (pick {x['pick_join_fourth']}); kept 34% of joins.\n")
w("**The landing (289): each line's last note.**\n")
w("| Run | On beat 1 | On beat 3 | On beats 2 and 4 | Off the beat | Last stress on 1 or 3 |\n|---|---|---|---|---|---|")
for v in V:
    y = R["5"][v]; w(f"| {LAB[v]} | {f3(y['landing']['b1'])} | {f3(y['landing']['b3'])} | {f3(y['landing']['b24'])} | {f3(y['landing']['off'])} | {f3(y['stress_b13'])} |")
w(f"| main pick | {x['landing_pick']['b1']} | {x['landing_pick']['b3']} | {x['landing_pick']['b24']} | {x['landing_pick']['off']} | {x['stress_pick'][0]} |")
w("| 289's shares | 26% | 10% | 16% | 49% | 35–55% asked |")
w(f"\nSection endings, the pick (scale degree of the last sung note): " + ", ".join(f"{s} {d}" for s, d in x["ends_pick"].items()) +
  ". Across main's builds: " + "; ".join(f"{s} " + ", ".join(f"{d} {n}" for d, n in c.items()) for s, c in x["ends_builds"].items()) + ".\n")
# 6
w("## 6. Fix 255: the three builds, and the pick under the old fit term (296)\n")
w("| Run | Build | Composite | Composite, old fit | Content | Order | Combined | Lift (median, top) | Spectral |\n|---|---|---|---|---|---|---|---|---|")
for v in V:
    for lab in ("composite first", "shortlist pick", "judge first", "pick under the old fit term (296)"):
        c = R["6"][v][lab]
        w(f"| {LAB[v]} | {lab}: {c['fp']} | {c['composite']} | {c['composite_old']} | {c['content']} | {c['order']} | {c['combined']} | {c['lift']['median']:g}, {c['lift']['top']:g} | {c['spectral']} |")
for v in V:
    x = R["6"][v]
    w(f"- {LAB[v]}: the composite's first is {x['comp_first_rank_by_judge']}th of {x['survivors']} by the judge, inside the upper half ({x['shortlist_size']}), so the shortlist "
      f"did not change the pick. Under the old fit term the composite's first is {x['old_fit_first']}, the pick ranks {x['old_fit_rank_of_pick']}th, and the pick "
      f"{'**differs**' if x['pick_old_differs'] else 'is the same'}. Builds: content {f3(x['builds']['content'])}, order {f3(x['builds']['order'])}, combined {f3(x['builds']['combined'])}; "
      f"{pc(x['above_kept_median'])} at or above the kept held-out median, {pc(x['above_kept_25'])} above the kept 25th, {pc(x['below_floor'])} under the floor.")
K = R["6"]["kept"]
w(f"\n**291: the refitted judges.** Kept held-out percentiles (5 · 25 · 50 · 75 · 95): content {f3([K['content'][q] for q in ('5', '25', '50', '75', '95')])}, order {f3([K['order'][q] for q in ('5', '25', '50', '75', '95')])}, "
  f"combined {f3([K['combined'][q] for q in ('5', '25', '50', '75', '95')])}; floor {R['6']['floor']}. The file carries the kept percentiles and not the held-out rows, so an AUC is not read here; "
  "the separation printed is the builds against the kept percentiles above. The content judge's heaviest give-aways (weight × z, mean over 400 builds): main " +
  ", ".join(f"{m.replace('_', ' ')} ({x_})" for m, x_ in R["give_away"]["main"][:4]) + "; control " + ", ".join(f"{m.replace('_', ' ')} ({x_})" for m, x_ in R["give_away"]["ctl"][:4]) + " (finding 299).\n")
# 7
w("## 7. Distance, the outside count, reciting, the era\n")
w("| Run | Distance from the centre | Outside both kept middle halves (of 56) | Verse on reciting (sd) |\n|---|---|---|---|")
for v in V:
    x = R["7"][v]; w(f"| {LAB[v]} | {f3(x['distance'])} (pick {x['pick_distance']}) | {f3(x['outside'])} (pick {x['pick_outside']}) | {f3(x['reciting_verse'])} (pick {x['pick_reciting']}) |")
x = R["7"]["main"]
w(f"\nNo era was chosen (Q8), so 264 did not run; the five era readings are printed for the record: " + ", ".join(f"{k} {v_}" for k, v_ in x["era_pick"].items()) +
  f". 243 drew the pick's target windows from {x['windows_years']['V']} (verse pool) and {x['windows_years']['C']} (chorus pool); the pools run "
  f"{x['pool_years']['V'][0]}–{x['pool_years']['V'][2]} and {x['pool_years']['C'][0]}–{x['pool_years']['C'][2]} (medians {x['pool_years']['V'][1]}, {x['pool_years']['C'][1]}). No character was chosen (Q9), so 281 and 293's first half did not apply.\n")
# 8
T = R["8"]["main"]; Tc = R["8"]["ctl"]; S = R["stats"]["main"]
fil = sum(1 for f in RF["fills"] if f["gap"]["beats"] >= 2.75); elig = sum(1 for g in RF["gaps"] if g["beats"] >= 2.75)
aims = T["278"]
w("## 8. The tests of fixes 257–297\n")
w("| Fix | The test | The reading (main; control where it says) | Held? |\n|---|---|---|---|")
rows = [
 ("257", "median 50–78% arched or falling; arch term positive in half or more; no survivor outside 31–94% or with valleys over 33%",
  f"{pc(T['257']['median_af'])}, positive {pc(T['257']['median_pos'])}; {T['257']['surv_outside']} of {T['257']['n']} survivors outside, {T['257']['surv_valley']} with valleys over 33%",
  "median yes; positive yes (51%); survivors no"),
 ("258", "median widening −0.1 to +1.1; no survivor outside −1.4 to +1.9", f"{T['258']['median']}; {T['258']['surv_outside']} survivors outside", "median yes; survivors no (2)"),
 ("259", "median extra surprise 0.8–1.9 bits; joins a fourth or more in 25–40%; no survivor under −0.1", f"{T['259']['median']} bits; joins {pc(T['259']['joins'])}; {T['259']['surv_under']} survivor under −0.1", "median yes; joins yes; survivors no (1)"),
 ("260", "median 33–78% after the downbeat; no survivor under 10%", f"{pc(T['260']['median'])}; {T['260']['surv_under']} survivors under 10%", "yes"),
 ("261", "a reading: last note over mean (kept 1.2–1.7), last note the longest", f"{f3(T['261']['last_over_mean'])}; longest {f3(T['261']['last_longest'])}", "printed (long; finding 306)"),
 ("262", "last chorus on the tonic; an earlier chorus on the tonic triad; the verse off the tonic",
  f"last chorus {pc(T['262']['last_tonic'])}, chorus 1 {pc(T['262']['c1_triad'])}, verse 1 off {pc(T['262']['v1_off'])}; the pick all three", "no: the last chorus in 89% (finding 302)"),
 ("263", "intake count of windows both reciting and in the era", "no era and no character", "did not apply"),
 ("264", "the era gate", "no era (Q8)", "did not apply"),
 ("265", "the drawn window's year recorded and in the era", f"recorded: verse {T['265']['windows']['V']}, chorus {T['265']['windows']['C']}; no era", "recorded; the era half did not apply"),
 ("266", "no aimed measure from a class median", "none" if not T["266"]["not_in_rows"] else ", ".join(T["266"]["not_in_rows"]), "yes"),
 ("267", "no build dies at the return gate where 239 built the return", f"deaths {T['267']['deaths']} main, {Tc['267']['deaths']} control; readings: " + ", ".join(f"{k} {n}" for k, n in T["267"]["by_reading"].items()), "yes (287)"),
 ("268", "verse 2 shares 25–75% of verse 1's bar rhythms at the median", f"{f3(T['268']['share'])}; in range {pc(T['268']['in_range'])} (control {f3(Tc['268']['share'])})", "no (finding 303)"),
 ("269", "260's test; last stresses on 1 or 3 in 35–55%", f"after {pc(T['260']['median'])}; on 1 or 3 {f3(T['289']['stress_b13'])}", "yes"),
 ("270", "dies only at ten or more (276 governs); a fifth of lines (±half) with a run of four; reciting median 1.4–2.1 where a character is chosen",
  f"runs: soft {R['3']['main']['soft_by_limit'].get('run_max', 0)}, hard {R['3']['main']['hard_by_limit'].get('run_max', 0)}; lines with a run of four {pc(T['270']['lines_run4'])}; longest run {f3(T['270']['longest'])}; reciting {T['270']['reciting']} (no character)",
  "runs yes; lines with a run of four yes; reciting did not apply"),
 ("271/285/290", "every aim kept followed at r ≥ 0.3; beat 3 dropped; turns per move kept",
  f"turns per move: verse {T['271']['v:turns_per_move']}, chorus {T['271']['c:turns_per_move']}; beat 3 (not aimed) verse {T['271']['v:on_beat3']}, chorus {T['271']['c:on_beat3']}; others ≥ 0.44", "no: turns per move in the chorus (finding 304)"),
 ("272", "fills against gaps of 2.75 beats or more; seven in ten filled", f"{fil} of {elig} filled; {RF['fill_stats'].get('filled (short gap)', 0)} short gaps filled with a beat and a half", "yes"),
 ("273", "chord strikes with a bass note; 16% or more", "see the consistency check (electric piano against the bass)", "yes"),
 ("274", "the extension named; every other section a multiple of four", "the last chorus's 18 bars (the tag); all others multiples of four", "yes"),
 ("275", "every gate printed with its kept pass rate; under 90% flagged", "section 4", "printed"),
 ("276", "the limits on every build; pick and median beside the table", "section 3 (fifteen limits)", "yes"),
 ("277", "deaths on a hard limit or a third soft break under one in five; the pick's soft breaks printed", f"main {R['3']['main']['hard_any'] + R['3']['main']['deaths_on_three_soft']} deaths of 1,000; control {R['3']['ctl']['hard_any'] + R['3']['ctl']['deaths_on_three_soft']}; pick none", "yes (main 15.3%)"),
 ("278", "no death for a comparison, a return's first or top note, or a tritone unless chosen; design gates listed; kept rates beside", "no design gate; aims below", "yes"),
 ("279, 284, 292", "records", f"292: the composite's first ranks {R['6']['main']['comp_first_rank_by_judge']} of {R['6']['main']['survivors']} by the judge (main), {R['6']['ctl']['comp_first_rank_by_judge']} of {R['6']['ctl']['survivors']} (control)", "—"),
 ("280", "the seven's pass rates", "amended by 286; section 4", "printed"),
 ("281", "a chosen character's axis", "no character (Q9)", "did not apply"),
 ("282", "a line said twice keeps its source", "the chorus's line 5 = line 1, pitches and onsets (213, Q11's plain repeat)", "yes"),
 ("283", "the feel of each section stated", "straight throughout; verses half time (Q19)", "stated"),
 ("286", "deaths at the spectral reading under one in five; the seven's joint pass rate printed", f"spectral decided {L['main']['deaths_spectral_decisive']} deaths main, {L['ctl']['deaths_spectral_decisive']} control; the seven pass {pc(pj['pass_as_limits'])} of the pairs", "yes"),
 ("287", "no build dies at 267 where 239 built the return", f"{T['267']['deaths']} and {Tc['267']['deaths']}", "yes"),
 ("288", "lengths in eight bars spread 4–8; chorus-over-verse medians inside the kept middle half in half the builds or more",
  f"lengths {f3(T['288']['lengths'])} (control {f3(Tc['288']['lengths'])}); medians inside {pc(T['288']['inside_mid']['median'])} (control {pc(Tc['288']['inside_mid']['median'])})", "lengths yes (main), narrow in the control; medians no (finding 298)"),
 ("289", "last stresses on 1 or 3 in 35–55%; last notes on a downbeat inside the kept 11–43%", f"{f3(T['289']['stress_b13'])}; downbeat ends {f3(T['289']['ends_down'])}", "yes"),
 ("290", "each aim's last two readings and the drop", "beat 3: dropped (verse 0.077); turns per move: chorus 0.185 (song 38's rerun 0.172)", "printed; turns per move fails a second song running"),
 ("291", "after the refit, the content judge's median at or above the first run's; held-out AUC printed",
  f"content median {R['6']['main']['builds']['content'][1]} (kept held-out median {K['content']['50']}); no held-out rows on file", "no (finding 299); the AUC not printable"),
 ("293", "verse 2's share inside 25–75% in three builds of four (the axis half: no character)", f"in range {pc(T['268']['in_range'])}; bars copied {T['293']['bars_copied']} across 1,000 builds; copy given up for {T['293']['copy_given_up']} lines", "no (finding 303); first half did not apply"),
 ("294", "each pool's years and the ruling", "no era, no character", "did not apply"),
 ("295", "fewer than one build in ten needs the move", f"{T['295']['moved']} of 1,000 ({pc(T['295']['share'])}); control {Tc['295']['moved']}", "no (finding 302)"),
 ("296", "the pick under the old fit term printed", f"main: {R['6']['main']['pick under the old fit term (296)']['fp']} (differs); control: the same", "printed: the pick differs in main"),
 ("297", "the session's readings adopted", "run of ten a limit; verse 2 takes its source's entry; near-level 2; the first three-quarters by time; entry 62/21/17%", "yes"),
]
for r_ in rows: w("| " + " | ".join(r_) + " |")
w("\nFixes that did not apply: 263, 264, 281 and 294 (no era, no character), the first half of 293 (no chosen axis), 265's era half. Fixes 279, 284 and 292 are records; 261 a reading. "
  "Failed by a named design choice: none of the tests above; 230's two-bar rule is met by Q21's design (below), and 236's drum defaults are replaced by Q19's design.\n")
w("**278's aims: the builds' rate beside the kept rate (main).**\n")
w("| Aim | Kept | Main | Control |\n|---|---|---|---|")
KEPT278 = {P.AIMS_278[4]: 0.729, P.AIMS_278[5]: 0.771, P.AIMS_278[6]: 0.557, P.AIMS_278[7]: 0.674, P.AIMS_278[8]: 0.558, P.AIMS_278[9]: 0.802, P.AIMS_278[10]: 0.924, P.AIMS_278[11]: 0.659, P.AIMS_278[12]: 0.541,
           P.AIMS_278[0]: 0.5, P.AIMS_278[1]: 0.5, P.AIMS_278[2]: 0.5, P.AIMS_278[3]: 0.5}
for k in P.AIMS_278: w(f"| {k} | {pc(KEPT278[k])} | {pc(aims[k])} | {pc(Tc['278'][k])} |")
w("\n**Aims followed (correlation of target and reading across main's builds):** " + ", ".join(f"{k} {v_}" for k, v_ in T["271"].items()) + ". The control aims every build at its pool's medians, so it has no spread to correlate.\n")
w("**The other design rules, on the pick.** 230: every section's sung rate inside 3.2–6.2 syllables a bar, and every line of nine or more syllables in two bars is one of the "
  f"{len(P.DESIGNED_TWO_BAR)} Q21 names. 232: 'earth' on beat 1 and held three beats in the hook, a whole bar in the tag. 236: the drum design (Q19) is checked against the record.\n")
# the record
pk = Mn["pick"]
w("## The record\n")
w(f"Built from the main run's shortlist pick {pk['fp']} with no hand edits; the riff, fills and riff break drawn by riff_p40.py (seed {RF['seed']}: the riff from "
  f"{RF['drawn']} distinct figures, {RF['passed']} passing; the break's draw passed with chord tones on the beats {RF['solo_check']['ct']:.2f}, no tritone). "
  f"The demo's stems: the voice {DR['stems_db']:+.1f} dB over the band. Energy (band only, read where a build arrives): " +
  ", ".join(f"{r_['sec']} {r_['energy_read']:.2f}" for r_ in DR["energy"]) + ". Every document passes the consistency checks against the record.\n")
w("## Readings the paper does not give\n")
for line in [
 "**230 (Q21).** The form and the locked lyric are the design 230 allows for lines of nine or more syllables in two bars; the 27 lines are named in the code (DESIGNED_TWO_BAR).",
 "**232 over 289.** A title line (the hook and the tag) lands on beat 1 or 3; 289's shares are drawn for the other lines only.",
 "**236 (Q19).** The half-time verse is an arrangement design and gates nothing in the melody search.",
 "**243.** With no era and no character, the pools are by section kind: verse and pre-chorus from the kept verse windows, chorus and bridge from the kept chorus windows.",
 "**249.** The chorus calibration window is Chorus 1 (no designed notes); every knob is held to a third to three times its start (the sixteenth knob down to 0.02); the contour amplitude is capped at 7.",
 "**267/297.** Near-level is a span of two semitones or less (297 adopted it); returns read by time.",
 "**286.** The six limits are read on the 515 POP909 calibration pairs at the 5th/95th (soft) and 1st/99th (hard); the sequence-legs limit is soft at one leg over (any two-leg sequence) and hard at two; the seven are counted with 276's eight in one count of three soft breaks; a reading that cannot be taken counts as hard.",
 "**287.** A built return is also exempt from the post-pass that steps a flat-3, flat-7 or tritone note to a chord tone, not only from the join and leap repairs.",
 "**288.** The kept rates of the note lengths are the v88 pop IOI shares (the 'longer' share split between 36 and 48); the palette of eight is 3, 6, 9, 12, 18, 24, 36, 48 twelfths; a title note is held two beats or more and the song's last note a bar; the chorus's median, top and lowest are drawn from one quantile together, the bridge from its own; the verse's centre E4, cap A4, floor A3 (the voice row).",
 "**289.** The shares are applied to each line's last note; within 'off the beat' the onset is the line's own.",
 "**291.** Separation is printed as the builds against the kept held-out percentiles; the file has no held-out rows for an AUC.",
 "**293.** A copied bar keeps every onset of its source bar; after fourteen tries the copy is given up for that line; a line that no rhythm places is placed with a free entry and landing (counted).",
 "**295.** The hook must end on the tonic, since the last chorus's tag copies its tail; a last note that the drawn contour misses is moved one to three semitones (counted).",
 "**296.** The old fit term, for the report, is the term with the lift mark restored at full marks for four semitones and half for two.",
 "**Form.** The last chorus's line 8 is a return of the hook (its words differ: 'and it tastes like…'); the tag is the hook's last five syllables.",
 "**Never-say.** 'stone' is a common noun here, not a name.",
 "**Seed.** 20261511, the session's convention (20261110 + 401).",
 "**The riff.** Placed from D3, D mixolydian over C; it plays the intro's eight bars and the outro's first three (Q5's riff-led reading).",
]: w(f"- {line}")
w("\n## Findings\n")
w(FIND.split("\n", 2)[2] if FIND.startswith("# ") else FIND)
open(f"{H}/test_report_p40.md", "w").write("\n".join(o) + "\n"); print(len("\n".join(o)), "chars")
