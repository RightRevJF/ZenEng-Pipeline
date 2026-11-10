"""Song 37's readings (the brief's step 6): the pick, the builds (5th, median, 95th of every build the generator finished), the control
(224 off: every build aimed at the kept medians) and, as a probe for finding 225, a run with targets drawn from the kept 5th-95th.
Also the paper's tests for 212-224. Writes readings.pkl and readings.md."""
import sys, pickle, collections, numpy as np
sys.argv = [sys.argv[0], "1", "main"]; sys.path[:0] = ["/home/claude/p37"]
import melody_p37 as P
M = P.M; BAR, BEAT = P.BAR, P.BEAT
H = "/home/claude/p37"
R = {m: pickle.load(open(f"{H}/melody_{m}.pkl", "rb")) for m in ("main", "ctl", "wide")}
PK = {m: R[m]["alive"][0] for m in R}
REC = pickle.load(open(f"{H}/song_record.pkl", "rb"))
def pct(m, k): v = R[m]["spread"][k]; return tuple(float(x) for x in np.percentile(v, [5, 50, 95]))
def fmt(x, k):
    if k == "pct": return f"{100 * x:.0f}%"
    if k == "f3": return f"{x:.3f}"
    if k == "f2": return f"{x:.2f}"
    return f"{x:g}"
rows = [("Distance from the centre, 46 measures", "distance", "distance", "f3", "chart songs 0.086 · 0.176 · 0.351"),
        ("Measures outside both kept middle halves (of 56)", None, "outside_n", "n", "—"),
        ("Opening unit returns third (bar windows)", "unit3", "unit3", "pct", "kept 31% (chart) · 49% (grid)"),
        ("Opening unit repeated at once (bar windows)", "unit2", "unit2", "pct", "kept 17% · 28%"),
        ("Gaps of an eighth", "gap_eighth", "gap_eighth", "pct", "chart 32–47–62% · grid 27–44–61%"),
        ("Gaps of a quarter", "gap_quarter", "gap_quarter", "pct", "chart 6–15–28%"),
        ("Longest note over the median note", "lom", "lom", "n", "chart 2–3–4 · grid 2–3–5"),
        ("Notes a bar", "npb", "npb", "f2", "chart 2.94–3.75–4.63"),
        ("Chord tones on the beat", "ct_on", "ct_on", "pct", "chart 56–69–80%"),
        ("Chord tones off the beat", "ct_off", "ct_off", "pct", "chart 47–63–76%"),
        ("Pitch surprise (bits a note, whole song)", "pitch", "pitch", "f2", "chart 2.53–2.74–3.03"),
        ("Spread of notes bar to bar", "spread", "spread", "f2", "chart 1.20–1.62–2.12"),
        ("Bridge median over the verse's (semitones)", "bridge_median_minus_verse", "bridge_median_minus_verse", "n", "kept +2 (68% above)"),
        ("Bridge onsets a bar over the verse's", "bridge_onsets_ratio", "bridge_onsets_ratio", "f2", "kept 0.97 (0.78–1.21)")]
md = ["| Reading | Pick | Builds 5th · median · 95th | Control's pick | Control builds (median) | Probe (5th–95th draws), builds median | Kept |", "|---|---|---|---|---|---|---|"]
out = []
for lab, rk, sk, k, kept in rows:
    pv = len(PK["main"]["read"]["outside"]) if rk is None else PK["main"]["read"][rk]
    cv = len(PK["ctl"]["read"]["outside"]) if rk is None else PK["ctl"]["read"][rk]
    a, m, b = pct("main", sk)
    md.append(f"| {lab} | {fmt(pv, k)} | {fmt(a, k)} · {fmt(m, k)} · {fmt(b, k)} | {fmt(cv, k)} | {fmt(pct('ctl', sk)[1], k)} | {fmt(pct('wide', sk)[1], k)} | {kept} |")
    out.append(dict(label=lab, pick=pv, builds=(a, m, b), control=cv, control_median=pct("ctl", sk)[1], wide_median=pct("wide", sk)[1], kept=kept))
tc = {m: float(np.mean([x < 0.086 for x in R[m]["spread"]["distance"]])) for m in R}
inmid = {m: float(np.mean([0.133 <= x <= 0.228 for x in R[m]["spread"]["distance"]])) for m in R}
def flag(d): return "TOO CENTRAL" if d < 0.086 else ("FAR" if d > 0.351 else "inside the chart range")
# measures outside both: the pick's list; the share of builds outside on each measure
def outside_share(m):
    c = collections.Counter(k for o in R[m]["outs"] for k in o); n = len(R[m]["outs"])
    return {k: v / n for k, v in c.most_common()}
OS = {m: outside_share(m) for m in R}
omd = ["| Measure | The pick | Share of builds outside (run) | Control | Probe | Chart 25–50–75 | Grid 25–50–75 |", "|---|---|---|---|---|---|---|"]
pick_out = {k: (v, d) for k, v, d in PK["main"]["read"]["outside"]}
keys = sorted(set(list(pick_out) + [k for k, v in OS["main"].items() if v >= 0.2]), key=lambda k: -OS["main"].get(k, 0))
for k in keys:
    c = P.DM[k]["chart"]; g = P.DM[k]["grid"]
    pv = f"{pick_out[k][0]:g} ({pick_out[k][1]})" if k in pick_out else "inside"
    omd.append(f"| {k.replace('_', ' ')} | {pv} | {100 * OS['main'].get(k, 0):.0f}% | {100 * OS['ctl'].get(k, 0):.0f}% | {100 * OS['wide'].get(k, 0):.0f}% | {c[1]:g}–{c[2]:g}–{c[3]:g} | {g[1]:g}–{g[2]:g}–{g[3]:g} |")
dmd = ["| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |", "|---|---|---|---|---|"]
for g in list(dict.fromkeys(list(R["main"]["deaths"]) + list(R["ctl"]["deaths"]) + P.GATES)):
    dmd.append(f"| {g} | {R['main']['deaths'].get(g, 0)} | {R['main']['would'].get(g, '—') if g in P.GATES else '—'} | {R['ctl']['deaths'].get(g, 0)} | {R['ctl']['would'].get(g, '—') if g in P.GATES else '—'} |")
dmd.append(f"| **Survivors** | **{R['main']['survivors']} of {R['main']['made']}** | | **{R['ctl']['survivors']} of {R['ctl']['made']}** | |")
# targets: recorded per build (224), and how far the finished builds followed them
T = R["main"]["targets"]
def follow(tk, sk):
    tv = np.array([t[tk] for t in T]); fv = np.array(R["main"]["spread"][sk])
    return float(np.corrcoef(tv, fv)[0, 1]), float(np.mean(tv)), float(np.mean(fv))
FOL = {k: follow(k, s) for k, s in (("gap_eighth", "gap_eighth"), ("gap_quarter", "gap_quarter"), ("longest_over_median_note", "lom"), ("notes_per_bar", "npb"),
                                     ("chord_tones_on_beat", "ct_on"), ("chord_tones_off_beat", "ct_off"))}
# the paper's tests
notes = PK["main"]["notes"]; on = {n["on"] for n in notes}
summ = [n for n in notes if n["p"] == P.SUMMIT]
ends = PK["main"]["read"]["end_holds"]
lines_end_chorus = [n for n in notes if P.KIND[n["sec"]] == "Chorus" and int(n["line"].split(":")[1]) % 4 == 3]
last_by_line = {}
for n in notes: last_by_line[n["line"]] = n
chorus_last = [last_by_line[f"{s}:{i}"] for s in ("Chorus 1", "Chorus 2", "Last Chorus") for i in (3, 7)]
TST = dict(
    t212=dict(join_deaths=R["main"]["deaths"].get("join: no held end and breath before the line (212)", 0) + R["main"]["deaths"].get("join: no held end and breath before the copy (212)", 0), built=R["main"]["made"], survivors=R["main"]["survivors"], ctl_survivors=R["ctl"]["survivors"]),
    t213=dict(asked=True, unit2_builds_mean=float(np.mean(R["main"]["spread"]["unit2"])), unit2_pick=PK["main"]["read"]["unit2"], chorus_aabc_builds=None),
    t214=dict(ct_on_median=pct("main", "ct_on")[1], ct_off_median=pct("main", "ct_off")[1], iv=dict(repeat=pct("main", "iv_repeat")[1], step=pct("main", "iv_step")[1], larger=pct("main", "iv_larger")[1])),
    t215=dict(survivors_with=sum(1 for c in R["main"]["alive"] if any(P.tri(n["p"], M.chord_for(n, {m["on"] for m in c["notes"]})) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in c["notes"])), stored=len(R["main"]["alive"])),
    t216=dict(summits=[(n["sec"], n["line"], n["on"] // BAR + 1, n["on"] % BEAT == 0, M.chord_for(n, on)) for n in summ]),
    t217=dict(chorus_last_lines=[(n["line"], n["p"] % 12 == M.TONIC, M.chord_at(n["on"])) for n in chorus_last]),
    t218=dict(end_holds=ends, gap_eighth=pct("main", "gap_eighth"), lom=pct("main", "lom")),
    t219=dict(deaths_181=R["main"]["deaths"].get("returns related, on lines (181/219)", 0)),
    t220=dict(sections={nm: nb for nm, _, nb in P.FORM}, unit3_builds_mean=float(np.mean(R["main"]["spread"]["unit3"])), unit3_pick=PK["main"]["read"]["unit3"]),
    t221=dict(measures=sum(v["agree"] for v in P.DM.values()), file_sha=R["main"]["rerun"]["tables"]["v96"]),
    t222=dict(spread_pick=PK["main"]["read"]["spread"]),
    t223=dict(words={w: [x[1] for x in P.syl(w + " the")][:-1] for w in ("someday", "somewhere", "July", "radio", "microwave")}),
    t224=dict(distance_median=pct("main", "distance")[1], too_central=tc["main"], in_middle_half=inmid["main"]))
res = dict(md="\n".join(md), outside_md="\n".join(omd), deaths_md="\n".join(dmd), rows=out, too_central=tc, in_middle_half=inmid,
           distance={m: (PK[m]["read"]["distance"], flag(PK[m]["read"]["distance"])) for m in R}, pick={m: PK[m]["fp"] for m in R},
           comp={m: PK[m]["meas"]["composite"] for m in R}, survivors={m: R[m]["survivors"] for m in R}, order={m: R[m]["order_fp"] for m in R},
           rerun={m: R[m]["rerun"] for m in R}, plans=PK["main"]["meta"]["plans"], targets_pick=PK["main"]["meta"]["targets"], follow=FOL,
           outside_share=OS, pick_outside=PK["main"]["read"]["outside"], ctl_outside=PK["ctl"]["read"]["outside"], tests=TST)
pickle.dump(res, open(f"{H}/readings.pkl", "wb"))
open(f"{H}/readings.md", "w").write(res["md"] + "\n\n" + res["outside_md"] + "\n\n" + res["deaths_md"] + "\n")
print(res["md"]); print(); print(res["outside_md"]); print(); print(res["deaths_md"])
print("too central", tc, "in middle half", inmid); print("distance", res["distance"]); print("follow", FOL)
for k, v in TST.items(): print(k, v)
