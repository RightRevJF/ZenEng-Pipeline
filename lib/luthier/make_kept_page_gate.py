"""922 (Window 188): tables/kept_page_gate.json from the kept 4/4 pop tunes. python3 lib/luthier/make_kept_page_gate.py"""
import os, json, numpy as np
import kept_corpus as KC, page_gate as PG
HERE = os.path.dirname(os.path.abspath(__file__)); rows = []; seqs = []; names = []
for k in KC.kept_songs(min_notes=100):
    p = [int(x) for x in k["p"]]; t = np.asarray(k["t"], float) / 12.0; d = np.r_[np.diff(t), 1.0]; d = np.where(d > 0, d, 0.25); r = PG.parts(p, d); s = PG.ivs(p); r["_s"] = s; r["first_120_figures_again"] = PG.figures_again(p[:120]) if len(p) >= 120 else None
    # passages: the tune between rests of six beats or more
    cuts = [0] + [i for i in range(1, len(p)) if t[i] - t[i - 1] >= 6] + [len(p)]; w = [PG.figures_again(p[a:b]) for a, b in zip(cuts, cuts[1:]) if b - a >= 24]; r["within_passage_figures_again"] = float(np.mean(w)) if w else None
    rows.append(r); seqs.append(s); names.append(k["song"])
C = PG.counts(seqs)
for r in rows: r["surprise"] = PG.surprise(r["_s"], C, minus=PG.counts([r["_s"]]))               # each kept tune read with its own counts taken out
P = list(PG.PLAIN); mean = {c: float(np.mean([r[c] for r in rows])) for c in P}; sd = {c: float(np.std([r[c] for r in rows])) for c in P}
for r in rows: r["plainness"] = float(np.mean([PG.PLAIN[c] * (r[c] - mean[c]) / sd[c] for c in P]))
q = lambda c: [round(float(x), 4) for x in np.percentile([r[c] for r in rows if r.get(c) is not None], (10, 25, 50, 75, 90))]
T = {"source": f"{len(rows)} kept 4/4 songs (CoCoPops Billboard), the sung tune; made by lib/luthier/make_kept_page_gate.py", "songs": len(rows), "context_intervals": PG.K,
     "what": "the parts of the page gate (studies/session_lab, hymn_lab, gate, gates_strengthened) on the kept tunes; surprise is mean bits per interval, each kept tune read with its own counts taken out",
     "plain_side": PG.PLAIN, "mean": mean, "sd": sd, "percentiles_10_25_50_75_90": {c: q(c) for c in P + ["plainness", "first_120_figures_again", "within_passage_figures_again"]},
     "floor": {"plainness": q("plainness")[0], "note": "the kept 10th percentile: a tune under it is less plain than nine kept tunes in ten"},
     "kept_values": {c: [round(float(r[c]), 4) for r in rows] for c in P + ["plainness"]},
     "interval_counts": [{",".join(str(x) for x in k): v for k, v in C[0][j].items()} for j in range(PG.K + 1)]}
json.dump(T, open(os.path.join(HERE, "..", "..", "tables", "kept_page_gate.json"), "w"), separators=(",", ":"))
for c in P + ["plainness", "first_120_figures_again", "within_passage_figures_again"]: print(f"{c:30} {T['percentiles_10_25_50_75_90'][c]}")
print("songs", len(rows), "| table bytes", os.path.getsize(os.path.join(HERE, "..", "..", "tables", "kept_page_gate.json")))
