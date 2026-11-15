"""Across metres: which readings hold steady and which depend on the metre; metres that differ only in notation; sung against instrumental."""
import json, glob, os
import numpy as np
T = {}
for f in glob.glob("/home/claude/atlas/tables/*_*.json"):
    if "hymns" in f: continue
    d = json.load(open(f))
    if d.get("tunes", 0) >= 20: T[(d["metre"], d["source"])] = d
PITCH = ["repeated notes", "moves by step", "moves by leap", "turns of direction", "range", "distinct pitches", "longest run of one pitch"]
RHY = ["notes a beat", "gaps of half a beat", "gaps of a third of a beat", "gaps of a beat or more", "onsets on the beat", "onsets on the bar's first beat", "distinct rhythms over bars"]
sung = sorted([k for k in T if k[1] == "sung"], key=lambda k: -T[k]["tunes"])
rows = {}
for k in sung:
    Q = T[k]["readings_quartiles"]; rows[k[0]] = {r: Q[r][1] for r in PITCH + RHY if r in Q}
def spread(r):
    v = [rows[m][r] for m in rows if r in rows[m]]; return (min(v), max(v), (max(v) - min(v)) / (np.mean(v) + 1e-9))
inv = {r: spread(r) for r in PITCH + RHY}
pairs = [("3/8", "3/4"), ("6/4", "6/8"), ("3/2", "3/4"), ("2/2", "2/4"), ("4/2", "4/4")]
pair_rows = {}
for a, b in pairs:
    if a in rows and b in rows:
        pair_rows[f"{a} vs {b}"] = {r: (round(rows[a][r], 3), round(rows[b][r], 3)) for r in ("notes a beat", "gaps of half a beat", "gaps of a beat or more", "onsets on the beat", "notes a bar")  if r in rows[a] or True for _ in [0] if r in rows[a] and r in rows[b]} if False else {r: (round(T[(a,'sung')]["readings_quartiles"][r][1], 3), round(T[(b,'sung')]["readings_quartiles"][r][1], 3)) for r in ("notes a beat", "gaps of half a beat", "gaps of a beat or more", "onsets on the beat", "notes a bar")}
si = {}
for m in ("6/8", "2/4", "3/4", "4/4", "2/2", "9/8"):
    if (m, "sung") in T and (m, "instrumental") in T:
        si[m] = {r: (round(T[(m, "sung")]["readings_quartiles"][r][1], 3), round(T[(m, "instrumental")]["readings_quartiles"][r][1], 3)) for r in ("notes a beat", "moves by step", "moves by leap", "repeated notes", "range", "gaps of half a beat")}
top = {f"{k[0]} {k[1]}": (T[k]["tunes"], T[k]["bar_rhythms"][:4], T[k]["bars_total"]) for k in T}
weights = {f"{k[0]} {k[1]}": T[k]["onset_weights"] for k in T}
json.dump(dict(medians={m: {r: round(v, 4) for r, v in d.items()} for m, d in rows.items()}, invariance={r: [round(x, 3) for x in v] for r, v in inv.items()}, notation_pairs=pair_rows, sung_vs_instrumental=si, top_bars=top, tunes={f"{k[0]} {k[1]}": T[k]["tunes"] for k in T}), open("/home/claude/atlas/tables/comparison.json", "w"))
print("tunes", {f"{k[0]} {k[1]}": T[k]["tunes"] for k in sorted(T)})
print("\nrelative spread across sung metres (max-min)/mean:")
for r, (a, b, s) in inv.items(): print(f"  {r}: {a:.3f} to {b:.3f}  spread {s:.2f}")
print("\nnotation pairs (median, a vs b):"); [print(" ", k, v) for k, v in pair_rows.items()]
print("\nsung vs instrumental:"); [print(" ", k, v) for k, v in si.items()]
