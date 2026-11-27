"""PREDICTION_818_K3.md: two counts.  python3 studies/other_metres/counts_818_K3.py RECORD52.song.json LYRIC55.json RECORD55.song.json -> counts_818_K3.json"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
out = {}
# count 1
R = json.load(open(sys.argv[1])); sp = R["spec"]; E = M.Engine(sp); rng = random.Random(1); T = collections.defaultdict(lambda: [0, 0]); D = collections.Counter(); made = 0
for _ in range(1000):
    c, err = E.build(rng)
    if err: continue
    made += 1; g = E.gates(c); how = E._made.get(("Chorus 1", 2), "?"); U = E.line_start("Chorus 1", 2); o = min(n["on"] - U for n in c["notes"] if n["sec"] == "Chorus 1" and n["line"] == 2); T[how][0] += 1; T[how][1] += o <= 0; D[(how, "840" if (g or "").startswith("840") else "other")] += 1
fresh = [v for k, v in T.items() if not k.startswith("818")]; f_n = sum(v[0] for v in fresh); f_on = sum(v[1] for v in fresh); e_n = sum(v[0] for k, v in T.items() if k.startswith("818")); e_on = sum(v[1] for k, v in T.items() if k.startswith("818"))
out["count 1"] = dict(builds_made=made, by_how={k: dict(builds=v[0], on_time_in_100=round(100 * v[1] / v[0], 1), died_on_840=D[(k, "840")]) for k, v in sorted(T.items())}, made_by_818=dict(builds=e_n, on_time_in_100=round(100 * e_on / max(1, e_n), 1)), not_made_by_818=dict(builds=f_n, on_time_in_100=round(100 * f_on / max(1, f_n), 1)))
out["count 1"]["difference_in_points"] = round(out["count 1"]["not_made_by_818"]["on_time_in_100"] - out["count 1"]["made_by_818"]["on_time_in_100"], 1); out["count 1"]["separates_by_20"] = bool(out["count 1"]["difference_in_points"] >= 20)
print(json.dumps(out["count 1"]), flush=True)
# count 2
L = json.load(open(sys.argv[2])); R = json.load(open(sys.argv[3])); sp = R["spec"]; E = M.Engine(sp); BAR = E.BAR; tot = a_sum = b_sum = 0; nowin = 0; rows = []
def best(sy, W):
    """the most stressed syllables any kept window of this syllable count (with a pickup of none, one or two) puts on a first beat"""
    n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); m = None
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in W.get(n - p, []):
            if w[0] != 0 and p > 0: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w); v = sum(1 for o, x in zip(ons, sy) if x[1] and o % BAR == 0); m = v if m is None else max(m, v)
    return m
for sec, i in E.KEYS:
    sy = E.LINES[sec][i]; st = sum(1 for x in sy if x[1]); slot = E.SLOTS[sec][i]; sb = E.SUNGB.get(id(sy), slot); a = min(st, slot); tot += st; a_sum += a
    if slot == 4 and sb in (3, 4) and len(sy) >= 4:
        n1 = (len(sy) + 1) // 2 if sb == 4 else int(round(2 * len(sy) / 3.0)); x1 = best(sy[:n1], E.WIN); x2 = best(sy[n1:], E.WIN if sb == 4 else E.BARS); b = None if x1 is None or x2 is None else x1 + x2
    else: b = best(sy, E.WIN if slot == 2 else E.BARS if slot == 1 else {})
    if b is None: nowin += 1; b = a
    b_sum += b; rows.append((f"{sec}:{i}", len(sy), st, slot, sb, a, b))
rng = random.Random(L.get("seed", 1)); C = collections.Counter(); n_b = 300
for _ in range(n_b):
    c, err = E.build(rng)
    if err: C[(str(err[0]), f"{err[1]}:{err[2]}")] += 1
unm = []
for (msg, key), v in C.most_common(12):
    sec, i = key.rsplit(":", 1); sy = E.LINES[sec][int(i)]; unm.append(dict(line=key, why=msg, builds_in_300=v, syllables=len(sy), slot_bars=E.SLOTS[sec][int(i)], sung_bars=E.SUNGB.get(id(sy)), how=E.HOW.get((sec, int(i)), ["fresh"])[0]))
out["count 2"] = dict(stressed_syllables=tot, a_upper_bound=round(a_sum / tot, 3), b_within_kept_windows=round(b_sum / tot, 3), lines=len(rows), lines_with_no_kept_window=nowin, draw_living_median=0.241, mark=0.45, a_clears=bool(a_sum / tot >= 0.45), b_clears=bool(b_sum / tot >= 0.45), never_made_in_300=sum(C.values()), never_made_by_line=unm)
print(json.dumps(out["count 2"])); json.dump(out, open(os.path.join(HERE, "counts_818_K3.json"), "w"), indent=1)
