"""Writes test_report_v124.md: v124 Run 1 (the session's repairs and the new readings), every figure read from the files, then the findings."""
import json
H = "/home/claude/p52"; H1 = "/home/claude/p51"
S = (("40", "Song 40, Nothing Else on Earth", 20261511), ("42", "Song 42, Nothing Important", 20261552), ("43", "Song 43, Blue Movie", 20261553),
     ("44", "Song 44, Keeping Time", 20261554), ("45", "Song 45, Before It's Done (as drawn)", 20261555))
T = {s: json.load(open(f"{H}/readings_v124_p{s}_table.json")) for s, *_ in S}
J = {s: json.load(open(f"{H}/readings_v124_p{s}.json")) for s, *_ in S}
SEP = json.load(open(f"{H}/sep120_run1.json")); SEP0 = json.load(open(f"{H1}/base/sep120_v118_five.json")); SEP19 = json.load(open(f"{H1}/sep120_v119.json"))
NR = json.load(open(f"{H}/new_readings_v124.json")); RG = json.load(open(f"{H}/range_v124.json")); SD = json.load(open(f"{H}/side_v124.json"))
def esc(x): return str(x).replace("|", "/").replace("\n", " ")
def held(h): return "**no**" if h is False else "yes" if h is True else str(h)
def pc(x): return "-" if x is None else f"{x:.1%}"
def key(d, start): return next(v for k, v in d.items() if k.startswith(start))
o = []; A = o.append
A("# ZenEng v124 Run 1: the session's repairs and the new readings, songs 40, 42, 43, 44 and 45 — test report\n")
A("*Words and music of all five songs: Jason Bryant. The spec is ZenEng v124 (Modules 27.64–27.68, Windows 140–144). Ported as ruled: 405, 409, 412, 413, 414, 415, 417 and 419; "
  "428 withdraws 424's empty-bar rate. 402 and 403 were already in. Not ported: 404, 406 and 408 (Run 2), 410, 425 and 427. The paper was not edited. "
  "The session's new findings are numbered from 450. No new song; song 45 as drawn.*\n")
A("## What was run\n")
A("- All five songs, 1,000 builds in the main run and 1,000 in the control, each made twice, at PYTHONHASHSEED 0, with the same lyrics, intakes, designs and seeds as v119.")
A("- The predictions were written and pushed before the runs of record (predictions_run1.md). They are scored below.")
A("- Side runs (main, 1,000 builds), none a run of record:")
A("  - song 43 with 386 off and with 389 off (416);")
A("  - every song with 398 off and with 400 off (the range question);")
A("  - song 45 with 392 off, and with 413 off, 414 off and 428 off;")
A("  - song 45 with 267 reading the bridge's G before its raise (450).\n")
A("| Song | Run | Survivors (v119) | Order | Rerun order | Reproduced |\n|---|---|---|---|---|---|")
for s, title, seed in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        r = J[s][v]["runs"]; b = r.get("before", {})
        A(f"| {s} (seed {seed}) | {lab} | {r['survivors']} ({b.get('survivors', '-')}) | {r['order']} | {r['rerun_order']} | {'yes' if r['reproduced'] else '**no**'} |")
A("")
A("## The predictions, scored\n")
for line in open(f"{H}/predictions_scored.md").read().strip().splitlines(): A(line)
A("")
A("## How each fix was ported\n")
for line in open(f"{H}/port_notes_v124.md").read().strip().splitlines(): A(line)
A("")
A("## Deaths by cause (main runs; v119 in brackets)\n")
causes = {}
for s, *_ in S:
    for k, x in J[s]["main"]["runs"]["deaths"].items(): causes.setdefault(k, {})[s] = x
O19 = {s: json.load(open(f"{H1}/readings_v119_p{s}.json"))["main"]["runs"]["deaths"] for s, *_ in S}
A("| Cause | " + " | ".join(s for s, *_ in S) + " |\n|---|" + "---|" * len(S))
for k in sorted(causes, key=lambda k: -sum(causes[k].values())):
    A(f"| {esc(k)[:90]} | " + " | ".join(f"{causes[k].get(s, 0)} ({O19[s].get(k, 0)})" for s, *_ in S) + " |")
A("")
A("## The knobs (Run 1)\n")
A("| Song | Run | s16 | g8 | g4 | glong | on16 | 398: chord tones / on a beat / on a downbeat / left by step | 400: turns | 424: fourths and fifths / last note tonic |\n|---|---|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    for v, lab in (("main", "main"), ("ctl", "control")):
        k = J[s][v]["runs"]["line_knobs"]
        A(f"| {s} | {lab} | " + " | ".join(str(round(k.get(x, 1.0), 3)) for x in ("s16", "g8", "g4", "glong", "on16"))
          + f" | {round(k.get('ct398', 1), 2)} / {round(k.get('ctb398', 1), 2)} / {round(k.get('ctd398', 1), 2)} / {round(k.get('res398', 1), 2)} | {round(k.get('turn400', 1), 3)} | "
          f"{round(k.get('ff424', 1), 3)} / {round(k.get('lt424', 1), 2)} |")
A("")
A("## The ported repairs, song by song (main run; control in the table of tests)\n")
A("| Song | 405: drawable lines' runs by band (kept) | 405: lines | 409: last note on the tonic (walked share) | 412: deaths at 267 (v119; v118) | 413: free units' returns (pooled kept 16.4 / 30.1 / 19.4%) | 414: spans given up | 415: verse 2 share (bars read) | 419: clashes at the note |\n|---|---|---|---|---|---|---|---|---|")
for s, *_ in S:
    m = J[s]["main"]
    b405 = "; ".join(f"{b}: {d['drawable'][1]:.0%} of {d['drawable'][0]} ({d['kept']:.0%}); no room or fell back {d['no room or fell back'][1]:.0%}" for b, d in m["405"]["by_band"].items())
    ln = m["405"]["lines"]; ln_ = f"{ln.get('405: line drawable without runs', 0)} drawable, {ln.get('405: line fell back to runs', 0)} fell back, {ln.get('405: line with no room on the eighth grid', 0)} no room"
    fu = m["413"]["free_units"]; fu_ = " / ".join(pc(fu[k]["free_mean"]) for k in ("unit2_returns", "unit3_returns", "unit4_to_unit2"))
    s415 = f"{m['415']['share'][1]:.2f} ({m['415']['bars_read'][1]:.0%})" if m["415"].get("share") else m["415"].get("note", "-")
    A(f"| {s} | {b405} | {ln_} | {m['409']['last_note_tonic']:.1%} ({m['409']['walked_share']:.0%}) | {m['412']['deaths267']} ({m['412']['v119']}; {m['412']['v118']}) | {fu_} | "
      f"{m['414']['given_up']} ({m['414']['given_up_share']:.1%}) | {s415} | {m['419']['clashes']} of {m['419']['notes_read']} |")
A("")
A("Where the window's last note comes from (409; main run; windows, share on the tonic):\n")
for s, *_ in S:
    A(f"- **Song {s}:** " + "; ".join(f"{k} {n} ({t:.0%})" for k, (n, t) in J[s]["main"]["409"]["by_source"].items()))
A("")
A("Empty bars, printed (428; main run): " + "; ".join(f"song {s} {J[s]['main']['428']['empty_bars']} of eight" for s, *_ in S)
  + f" (CoCoPops {J['40']['main']['428']['cocopops']}, BiMMuDa {J['40']['main']['428']['bimmuda']}).\n")
for s, title, seed in S:
    rows = T[s]; nh = sum(1 for r in rows if r[5] is True); nt = sum(1 for r in rows if isinstance(r[5], bool)); nf = [r[0] for r in rows if r[5] is False]
    A(f"## The table of tests: {title}\n")
    A(f"Held in both the main run and the control: {nh} of {nt} with a test. " + (f"Not held: {', '.join(nf)}." if nf else "Every test held.") + "\n")
    A("| Fix | Test | Read against | Main | Control | Held? |\n|---|---|---|---|---|---|")
    for k, t, ka, a, b, h in rows: A(f"| {k} | {esc(t)} | {esc(ka)} | {esc(a)} | {esc(b)} | {held(h)} |")
    A("")
A("## Separation (422): the 30 agreed measures, both collections pooled\n")
A(f"This is 364's fresh judge, on the kept windows of CoCoPops (314) and BiMMuDa 1958–1991 (231) pooled, against the first 400 complete builds of each main run (AUC). Kept songs are held out by song in both collections. "
  f"The collections read {SEP['collections_against_each_other']} against each other here (Window 140: 0.555).\n")
A("| Family | v118, across | v119 step 3, across | Run 1, across | v118, 40/42/43 | v119, 40/42/43 | Run 1, 40/42/43 | Run 1, within 40 / 42 / 43 / 44 / 45 |\n|---|---|---|---|---|---|---|---|")
for f in ("agreed 30", "pitch (agreed)", "rhythm (agreed)", "form", "harmony (CoCoPops alone, apart)"):
    A(f"| {f} | {SEP0['family'][f]['across_mean']} | {SEP19['family'][f]['across_mean']} | {SEP['family'][f]['across_mean']} | {SEP0['family'][f]['across_mean_40_42_43']} | "
      f"{SEP19['family'][f]['across_mean_40_42_43']} | {SEP['family'][f]['across_mean_40_42_43']} | " + " / ".join(str(SEP["family"][f]["within"][s]) for s, *_ in S) + " |")
chk = SEP["family"]["agreed 30"]["across_mean_40_42_43"]
A(f"\n**Check: separation on the agreed measures at or under v118's 0.756 (songs 40, 42 and 43 across): {chk} — {'held' if chk <= 0.756 else '**not held**'}.**\n")
A("Costs on the 30 agreed measures, the five songs' builds pooled (points; kept mean, builds' mean): " + "; ".join(f"{e[0]} {e[1]} ({e[2]}, {e[3]})" for e in SEP["costs_agreed_30"]["eight"]) + f" (gap {SEP['costs_agreed_30']['gap']}).\n")
A("Each song's eight costliest, main run (340):\n")
for s, title, *_ in S:
    x = J[s]["main"]["340"]; A(f"- **{title}** (gap {x['gap']}): " + "; ".join(f"{e[0]} {e[1]} ({e[2]:.3f}, {e[3]:.3f})" for e in x["eight"]))
A("")
A("## The range question\n")
A(f"Window range (semitones) and pitch spread (sd), Verse 1 and Chorus 1 windows of each main run's survivors. Kept: range CoCoPops {RG['kept']['range']['cocopops']}, BiMMuDa {RG['kept']['range']['bimmuda']}, pooled {RG['kept']['range']['pooled']}; "
  f"spread {RG['kept']['pitch_sd']['cocopops']}, {RG['kept']['pitch_sd']['bimmuda']}, pooled {RG['kept']['pitch_sd']['pooled']}.\n")
runs = list(next(iter(RG["by_song"].values())).keys())
A("| Song | " + " | ".join(runs) + " |\n|---|" + "---|" * len(runs))
for s, d in RG["by_song"].items():
    A(f"| {s} | " + " | ".join(f"{d[k]['range']} / {d[k]['pitch_sd']}" if d[k] else "—" for k in runs) + " |")
A("| across the songs read | " + " | ".join(f"{RG['across songs read'][k]['range']} / {RG['across songs read'][k]['pitch_sd']} ({RG['across songs read'][k]['songs']})" for k in runs) + " |\n")
A("Range by window, verse / chorus (main runs):\n")
A("| Song | " + " | ".join(runs) + " |\n|---|" + "---|" * len(runs))
for s, d in RG["by_song"].items():
    A(f"| {s} | " + " | ".join(f"{d[k]['range verse']} / {d[k]['range chorus']}" if d[k] else "—" for k in runs) + " |")
x = SD.get("45_off392")
if x: A(f"\nSong 45 with 392 off (Run 1 code): range {x['range']} (verse {x['range_verse']}, chorus {x['range_chorus']}), spread {x['pitch_sd']}; survivors {x['survivors']}.")
A("")
A("## Side runs (none a run of record)\n")
A("| Run | Off | Survivors | Order | Memory breaks | Range (verse / chorus) | Spread | Deaths at 267 | Align deaths | Join deaths (line) | Rhythm deaths | Spans given up |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, x in SD.items():
    if not x or "survivors" not in x: continue
    A(f"| {k} | {x['off'] or ('267 before the raise' if x.get('diag450') else '—')} | {x['survivors']} | {x['order']} | {x['memory_breaks']} | {x['range']} ({x['range_verse']} / {x['range_chorus']}) | {x['pitch_sd']} | "
      f"{x['deaths'].get('returns related (267)', 0)} | {x['deaths'].get('align: the words do not fit the returning tune', 0)} | {x['deaths'].get('join: no held end and breath before the line (212)', 0)} | "
      f"{x['deaths'].get('rhythm: no placement', 0)} | {x['spans_given_up']} of {x['spans_drawn'] + x['spans_given_up']} |")
A(f"\nSong 43's memory breaks under v114: 13, spread 6.6 (416).\n")
A("## The new readings\n")
A(f"Read by new_readings_v124.py on each song's survivors, main and control (builds read: {NR['builds read (survivors, main and control) by song']}). It runs the studies' own code, with one chord a bar from the chart. "
  "The v118 builds' figures are the papers' (songs 40, 42 and 43; 44 and 45 in Window 143).\n")
r = key(NR, "426")
A("### 426: the six measures (Verse 1 and Chorus 1 windows)\n")
A("| Measure | CoCoPops | BiMMuDa | v118 builds | " + " | ".join(f"Run 1, {s}" for s, *_ in S) + " | Same side on every song |\n|---|---|---|---|" + "---|" * len(S) + "---|")
for m, x in r.items(): A(f"| {m} | {x['cocopops']} | {x['bimmuda']} | {x['v118_builds']} | " + " | ".join(f"{x['run1'][s]} ({x['side'].get(s, '-')})" for s, *_ in S) + f" | {x['same_side_on_every_song']} |")
r = key(NR, "431")
A("\n### 431: chord tones beside Billboard and Rolling Stone (first verse and chorus)\n")
A("| Measure | Billboard | Rolling Stone | v118 builds | " + " | ".join(f"Run 1, {s} (sd from BB / RS)" for s, *_ in S) + " |\n|---|---|---|---|" + "---|" * len(S))
for m, x in r.items(): A(f"| {m} | {x['billboard']} | {x['rolling_stone']} | {x['v118_builds']} | " + " | ".join(f"{x['run1'][s]} ({x['vs_billboard_sd'][s]} / {x['vs_rolling_stone_sd'][s]})" for s, *_ in S) + " |")
r = key(NR, "432")
A("\n### 432, 441, 442: the melody over the chord and the bass (readings only)\n")
A("| Measure | Billboard | Rolling Stone | Kept verse (q25, median, q75, mean) | Kept chorus | " + " | ".join(f"Run 1, {s}: verse / chorus" for s, *_ in S) + " |\n|---|---|---|---|---|" + "---|" * len(S))
for m, x in r.items():
    if not isinstance(x, dict) or "run1" not in x: continue
    A(f"| {m} | {x['billboard']} | {x['rolling_stone']} | {x['kept_quartiles'].get('verse', '-')} | {x['kept_quartiles'].get('chorus', '-')} | " + " | ".join(f"{x['run1'][s]['verse']} / {x['run1'][s]['chorus']}" for s, *_ in S) + " |")
aims_ = r["paper's aims (readings only for now)"]; cnb_ = r["chorus not below verse"]
A(f"\nThe paper's figures (readings for now): {aims_}. Chorus not below verse: {cnb_}.\n")
r = key(NR, "443")
A("### 443: melody against bass (printed; no rule or aim)\n")
cols = list(r["billboard"].keys())
A("| Body | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
for lab, d in (("Billboard", r["billboard"]), ("Rolling Stone", r["rolling_stone"]), ("v118 builds", r["v118_builds"])): A(f"| {lab} | " + " | ".join(str(d.get(c)) for c in cols) + " |")
for s, *_ in S: A(f"| Run 1, song {s} | " + " | ".join(str(r["run1"][s].get(c)) for c in cols) + " |")
r = key(NR, "433")
A("\n### 433: each section against kept sections of its kind\n")
A("Measures (of 27) whose song mean falls outside the kept middle half for its section:\n")
A("| Section | Kept windows | " + " | ".join(s for s, *_ in S) + " |\n|---|---|" + "---|" * len(S))
for sec, x in r.items(): A(f"| {sec} | {x['kept_windows']} | " + " | ".join(str(x["outside_the_kept_middle_half_by_song"].get(s, 0)) for s, *_ in S) + " |")
A("\nThe measures, verse 2 and the bridge (kept mean, middle half; Run 1 by song, sd from the kept mean):\n")
for sec in ("Verse 2", "Bridge"):
    A(f"**{sec}**\n")
    A("| Measure | Kept | Middle half | " + " | ".join(s for s, *_ in S) + " |\n|---|---|---|" + "---|" * len(S))
    for m, x in r[sec]["by_measure"].items(): A(f"| {m} | {x['kept']} | {x['middle_half']} | " + " | ".join(f"{x['run1'][s]} ({x['in_sd'].get(s, '-')})" for s, *_ in S) + " |")
    A("")
r = key(NR, "436")
A("### 436: the bridge beside kept bridges\n")
A("| Measure | Kept bridge: BB / RS (medians) | Kept verse: BB / RS | v118: bridge / verse | " + " | ".join(f"Run 1, {s}: bridge / verse" for s, *_ in S) + " |\n|---|---|---|---|" + "---|" * len(S))
for m, x in r.items():
    if not isinstance(x, dict) or "kept_bridge" not in x: continue
    kb = x["kept_bridge"]
    A(f"| {m} | {kb['billboard']} / {kb['rolling_stone']} ({kb['billboard_median']} / {kb['rolling_stone_median']}) | {x['kept_verse']['billboard']} / {x['kept_verse']['rolling_stone']} | "
      f"{x['v118_builds']['bridge']} / {x['v118_builds']['verse']} | " + " | ".join(f"{x['run1_bridge'][s]} / {x['run1_verse'][s]}" for s, *_ in S) + " |")
hk = [k for k in r if k.startswith("highest")][0]
A(f"\nThe bridge's highest note less verse 1's and chorus 1's (semitones, median): {r[hk]}. {r['note'].capitalize()}.\n")
r = key(NR, "437")
A("### 437: the later windows beside the first (pair)\n")
A("| Pair | Body | Bars of the same rhythm | Onsets shared | Pitch kept | Notes ratio | Bars all the same |\n|---|---|---|---|---|---|---|")
for k, x in r.items():
    for lab in ("billboard", "rolling_stone", "v118_builds"):
        d = x[lab]; A(f"| {k} | {lab.replace('_', ' ')} (mean, 25th, 75th) | {d['bars_same_rhythm']} | {d['onsets_shared']} | {d['pitch_kept']} | {d['notes_ratio']} | {d.get('bars all the same rhythm')} |")
    for s, d in x["run1"].items(): A(f"| {k} | Run 1, song {s} ({d['pairs']} pairs) | {d['bars_same_rhythm']} | {d['onsets_shared']} | {d['pitch_kept']} | {d['notes_ratio']} | {d['bars all the same rhythm']} |")
r = key(NR, "430")
A("\n### 430: the writer's edit, read measure by measure (song 45, Q16 A)\n")
A(r["note"] + "\n")
for sec in ("Chorus 1", "Verse 2"):
    x = r[sec]
    A(f"- **{sec}:** judge {x['judge_drawn']} drawn, {x['judge_edited']} edited. Moved toward kept: " + "; ".join(f"{m} {a} → {b} ({d})" for m, a, b, d in x["moved_most_down"])
      + ". Moved away: " + "; ".join(f"{m} {a} → {b} (+{d})" for m, a, b, d in x["moved_most_up"]) + ".")
A("")
A("## The seven limits of 286 and their corpus (373, 382)\n")
A("| Limit | Rule as run | Corpus |\n|---|---|---|")
for k_, (rule, corp) in J["40"]["main"]["373"]["limits"].items(): A(f"| {k_} | {esc(rule)} | {corp} |")
A("")
open(f"{H}/test_report_v124.md", "w").write("\n".join(o) + "\n" + open(f"{H}/findings_v124.md").read())
print("ok")
