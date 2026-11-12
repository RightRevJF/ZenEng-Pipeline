"""v124 Run 1's side runs (none a run of record) beside the runs of record: survivors, order, deaths, memory breaks (373's limit, 0.12), window range
and pitch spread, unit returns, spans given up, and song 43's v114 memory figure (13, spread 6.6, finding 416).
Usage: python3 side_v124.py OUT.json"""
import sys, os, json, pickle, collections
import numpy as np
OUT = sys.argv[1]; H = "/home/claude/p52"
SIDE = [("43", "main", ""), ("43", "main", "_off386"), ("43", "main", "_off389"), ("45", "main", ""), ("45", "main", "_diag450"), ("45", "main", "_off392"), ("45", "main", "_off413"), ("45", "main", "_off414"), ("45", "main", "_off428")]
SIDE += [(s, "main", t) for s in ("40", "42", "43", "44", "45") for t in ("", "_off398", "_off400")]
def mem_b(D): return sum(1 for b in D["all"] if (b["info"].get("limits7") or {}).get("memory", 1.0) is not None and (b["info"].get("limits7") or {}).get("memory", 1.0) < 0.12)
def wm(D, m, w=("v", "c")):
    x = [b["read"][k][m] for b in D["all"] for k in w if b["read"][k] and b["read"][k].get(m) is not None and np.isfinite(b["read"][k][m])]; return round(float(np.mean(x)), 3) if x else None
R = {}
for s, m, t in dict.fromkeys(SIDE):
    p = f"{H}/melody_v124_p{s}_{m}{t}.pkl"
    if not os.path.exists(p): R[f"{s}{t or ' (record)'}"] = None; continue
    D = pickle.load(open(p, "rb")); st = D["stats"]
    R[f"{s}{t or ' (record)'}"] = dict(off=D["rerun"].get("off"), diag450=D["rerun"].get("diag450"), survivors=D["survivors"], order=D["order_fp"], deaths=dict(sorted(D["deaths"].items(), key=lambda kv: -kv[1])),
        memory_breaks=mem_b(D), range=wm(D, "range"), range_verse=wm(D, "range", ("v",)), range_chorus=wm(D, "range", ("c",)), pitch_sd=wm(D, "pitch_sd"),
        distinct_pitches=wm(D, "distinct_pitches"), chord_tones=wm(D, "chord_tones"), turns_per_move=wm(D, "turns_per_move"),
        unit_returns={k: wm(D, k) for k in ("unit2_returns", "unit3_returns", "unit4_to_unit2")},
        spans_given_up=st.get("378: span given up (nothing fitted inside it)", 0), spans_drawn=st.get("378: lines drawn to a span", 0),
        knobs={k: round(v, 3) for k, v in D["line_knobs"].items() if k in ("ct398", "ctb398", "ctd398", "res398", "turn400", "lt424", "ff424", "dpk")})
R["v114, song 43's memory breaks (416)"] = dict(breaks=13, spread=6.6)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if v and "survivors" in v: print(k, v["survivors"], v["order"], "mem", v["memory_breaks"], "range", v["range"], v["range_verse"], v["range_chorus"], "sd", v["pitch_sd"], "267", v["deaths"].get("returns related (267)", 0), "align", v["deaths"].get("align: the words do not fit the returning tune", 0), "join", v["deaths"].get("join: no held end and breath before the line (212)", 0))
