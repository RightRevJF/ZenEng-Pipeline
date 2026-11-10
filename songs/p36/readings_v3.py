"""Version 3's readings (the brief's step 7): the pick, the run's builds (5th, median, 95th of every build that came out of the
generator), and the control's first pick (same seed and N, 199, 201, 205 and 206 off). Writes readings_v3.pkl and readings_v3.md."""
import sys, pickle, numpy as np
sys.argv = [sys.argv[0], "1", "main"]; sys.path[:0] = ["/home/claude/p36"]
import melody_v3_p36 as V
Mn = pickle.load(open("/home/claude/p36/melody_v3_main.pkl", "rb")); Ct = pickle.load(open("/home/claude/p36/melody_v3_ctl.pkl", "rb"))
P, C = Mn["alive"][0], Ct["alive"][0]
def q(k): v = Mn["spread"][k]; return np.percentile(v, 5), np.median(v), np.percentile(v, 95)
def qc(k): v = Ct["spread"][k]; return np.percentile(v, 5), np.median(v), np.percentile(v, 95)
pr, cr = P["read"], C["read"]
rows = [  # label, pick, builds key, control, chart/kept, v1
    ("Chord tones on the beat", pr["chord_on"], "chord_on", cr["chord_on"], "chart 69% (pop 72%)", "—", "pct"),
    ("Chord tones off the beat", pr["chord_off"], "chord_off", cr["chord_off"], "chart 62%", "—", "pct"),
    ("Sixteenth-note gaps, share", pr["sixteenth"], "sixteenth", cr["sixteenth"], "pop 2%", "38%", "pct"),
    ("Longest note over the median note (median of 8-bar windows)", pr["longest_over_median"], "longest_over_median", cr["longest_over_median"], "kept 3 (chart 2–4)", "9", "x"),
    ("Different note lengths per 8 bars (median of windows)", pr["lengths"], "lengths", cr["lengths"], "kept 4 (chart 3–5)", "7", "n"),
    ("Opening unit repeated at once, share of windows", pr["repeat_at_once"], "repeat_at_once", cr["repeat_at_once"], "kept 17–28%", "1%", "pct"),
    ("Stock designs, 8 bars", pr["stock8"], "stock8", cr["stock8"], "—", "—", "pct"),
    ("Stock designs, 16 bars", pr["stock16"], "stock16", cr["stock16"], "—", "—", "pct"),
    ("Pitch surprise (bits a note)", pr["pitch"], "pitch", cr["pitch"], "chart 2.53–2.74–3.03", "—", "f"),
    ("Repeated notes, share of intervals", pr["intervals"]["repeat"], "iv_repeat", cr["intervals"]["repeat"], "pop 27.6%", "23.7%", "pct"),
    ("Steps, share of intervals", pr["intervals"]["step"], "iv_step", cr["intervals"]["step"], "pop 42.6%", "47.3%", "pct"),
    ("Leaps past a fifth, share of intervals", pr["intervals"]["larger"], "iv_larger", cr["intervals"]["larger"], "pop 3.0%", "1.3%", "pct"),
    ("Exact bar repetition", pr["exact"], "exact", cr["exact"], "—", "—", "pct"),
    ("Spread of notes bar to bar (sd of onsets a bar)", pr["spread"], "spread", cr["spread"], "chart 1.20–1.62–2.12", "—", "f"),
    ("Bridge median over the verse's (semitones)", pr["bridge_median_minus_verse"], "bridge_median_minus_verse", cr["bridge_median_minus_verse"], "kept +2 (68% above)", "—", "f"),
    ("Bridge onsets a bar over the verse's", pr["bridge_onsets_ratio"], "bridge_onsets_ratio", cr["bridge_onsets_ratio"], "kept 0.97 (0.78–1.21)", "—", "f"),
    ("Distance from the centre (partial: 11 of 46 measures)", pr["distance"], "distance", cr["distance"], "chart 0.176 (0.086–0.351)", "—", "f3"),
]
def fmt(v, k):
    if k == "pct": return f"{100 * v:.0f}%"
    if k == "x": return f"{v:g}"
    if k == "n": return f"{v:g}"
    if k == "f3": return f"{v:.3f}"
    return f"{v:.2f}"
md = ["| Reading | Pick | Builds 5th · median · 95th | Control's pick | Builds of the control (median) | Kept / chart | Version 1 |", "|---|---|---|---|---|---|---|"]
out = []
for lab, pv, key, cv, kept, v1, k in rows:
    a, m, b = q(key); cm = qc(key)[1]
    md.append(f"| {lab} | {fmt(pv, k)} | {fmt(a, k)} · {fmt(m, k)} · {fmt(b, k)} | {fmt(cv, k)} | {fmt(cm, k)} | {kept} | {v1} |")
    out.append(dict(label=lab, pick=pv, builds=(a, m, b), control=cv, control_builds_median=cm, kept=kept, v1=v1))
br = lambda r: ("verse" if r["bridge_rel_verse"][0] else "") + (" chorus" if r["bridge_rel_chorus"][0] else "") or "neither"
md.append(f"| Bridge opening related to (27.31 read on lines) | {br(pr)} (onsets {pr['bridge_rel_verse'][1]:.2f}/{pr['bridge_rel_chorus'][1]:.2f}, contour {pr['bridge_rel_verse'][2]:.2f}/{pr['bridge_rel_chorus'][2]:.2f}) | related to either in {100 * np.mean(Mn['spread']['bridge_rel_any']):.0f}% of builds | {br(cr)} | {100 * np.mean(Ct['spread']['bridge_rel_any']):.0f}% | kept: neither 94% | — |")
d = P["read"]["distance"]
flag = "TOO CENTRAL" if d < 0.086 else ("FAR" if d > 0.351 else "inside")
dc = C["read"]["distance"]; flagc = "TOO CENTRAL" if dc < 0.086 else ("FAR" if dc > 0.351 else "inside")
gates = ["leaps: tritone or past an octave", "monotony run (166/196)", "summit placed (the writer's A)", "register (133)", "returns related, on lines (181/195)",
         "bridge opening unrelated (208)", "bridge above the verse (208)", "pitch band (153/182)", "rhythm band (163)", "pushed notes (159)", "density (159)",
         "sequence legs (148)", "key word on a chord tone (134)", "note lengths <= 5 per 8 bars (206)"]
dmd = ["| Cause | Run: deaths | Run: would fail | Control: deaths | Control: would fail |", "|---|---|---|---|---|"]
keys = list(dict.fromkeys(list(Mn["deaths"]) + list(Ct["deaths"]) + gates))
for g in keys:
    dmd.append(f"| {g} | {Mn['deaths'].get(g, 0)} | {Mn['would'].get(g, '—') if g in gates else '—'} | {Ct['deaths'].get(g, 0)} | {Ct['would'].get(g, '—') if g in gates else '—'} |")
dmd.append(f"| **Survivors** | **{Mn['survivors']} of {Mn['made']}** | | **{Ct['survivors']} of {Ct['made']}** | |")
res = dict(rows=out, md="\n".join(md), deaths_md="\n".join(dmd), pick=P["fp"], ctl_pick=C["fp"], distance=(d, flag), distance_ctl=(dc, flagc),
           comp=P["meas"]["composite"], comp_ctl=C["meas"]["composite"], plans=P["meta"]["plans"], ctl_plans=C["meta"]["plans"],
           main=dict(made=Mn["made"], survivors=Mn["survivors"], order=Mn["order_fp"], rerun=Mn["rerun"]), ctl=dict(made=Ct["made"], survivors=Ct["survivors"], order=Ct["order_fp"], rerun=Ct["rerun"]),
           aabc_ranks=[i + 1 for i, c in enumerate(Mn["alive"]) if c["meta"]["plans"]["ChorusHead"][:2] == ["A", "A"]],
           aabc_share=np.mean([c["meta"]["plans"]["ChorusHead"][:2] == ["A", "A"] for c in Mn["alive"]]))
pickle.dump(res, open("/home/claude/p36/readings_v3.pkl", "wb"))
open("/home/claude/p36/readings_v3.md", "w").write(res["md"] + "\n\n" + res["deaths_md"] + "\n")
print(res["md"]); print(); print(res["deaths_md"]); print("distance", d, flag, "ctl", dc, flagc, "comp", res["comp"], res["comp_ctl"], "AABC ranks", res["aabc_ranks"])
