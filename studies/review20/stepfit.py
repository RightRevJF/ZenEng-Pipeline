"""Review 20. (a) Why 930's step weight runs to its limit: steps as sung, before melismas, and inside freshly drawn lines, at three step weights.
# Review 20 (Luthier v33). Run from the repo root with PYTHONHASHSEED=0.
(b) Why song 55 spans 15 against 19: where its builds' highest and lowest notes fall against the registers' tops and floors."""
import sys, os, json, random, collections, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) if "studies" in os.path.abspath(__file__) else "/home/claude/zeneng-pipeline"
sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import song_from_lyric as SL, metre_engine as M
REC = {"54": "songs/p64/lyric54", "55": "songs/p65/lyric55", "58": "songs/p68/lyric58"}
def share(ps, lo, hi):
    iv = [abs(b - a) for a, b in zip(ps, ps[1:])]; return float(np.mean([lo <= x <= hi for x in iv])) if iv else float("nan")
def engine(tag):
    R = json.load(open(os.path.join(ROOT, REC[tag] + ".song.json"))); L = json.load(open(os.path.join(ROOT, REC[tag] + ".json"))); spec = R["spec"]
    E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=spec["target"]["run"])[0]
    fresh = {}; orig = E.pitches
    def rec_p(rng, ons, U, sec, i, prev, avoid=None, end_off=None):
        ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off); fresh[(sec, i)] = ps; return ps
    E.pitches = rec_p; return E, fresh, spec
out = {"a": {}, "b": {}}; N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
for tag in ("58", "54"):
    E, fresh, spec = engine(tag); base = E.MV
    for sw in (0.3, 1.2, 3.0, 6.0):
        E.MV = (sw, base[1], base[2]); rng = random.Random(5); rows = []
        for _ in range(N):
            fresh.clear(); c, err = E.build(rng)
            if err or E.gates(c): continue
            ns = sorted(c["notes"], key=lambda n: n["on"]); sung = sorted(E.as_sung(ns), key=lambda n: n["on"])
            by = collections.defaultdict(list)
            for n in ns: by[(n["sec"], n["line"])].append(n["p"])
            fr = [v for k, v in by.items() if fresh.get(k) == v]; ot = [v for k, v in by.items() if fresh.get(k) != v]
            fiv = [abs(b - a) for v in fr for a, b in zip(v, v[1:])]; oiv = [abs(b - a) for v in ot for a, b in zip(v, v[1:])]
            rows.append(dict(sung=share([n["p"] for n in sung], 1, 2), before=share([n["p"] for n in ns], 1, 2), fresh_lines=float(np.mean([1 <= x <= 2 for x in fiv])) if fiv else np.nan,
                             other_lines=float(np.mean([1 <= x <= 2 for x in oiv])) if oiv else np.nan, notes_in_fresh_lines=sum(map(len, fr)) / len(ns),
                             melisma_seconds=sum(1 for n in sung if n.get("melisma") == "second") / len(sung), repeats_before=share([n["p"] for n in ns], 0, 0), thirds_fourths_before=share([n["p"] for n in ns], 3, 4)))
        o = {k: round(float(np.nanmedian([r[k] for r in rows])), 3) for k in rows[0]}; o["builds"] = len(rows); out["a"][f"{tag} step weight {sw}"] = o; print(tag, sw, o, flush=True)
E, fresh, spec = engine("55"); rng = random.Random(5); hi_, lo_, top_sec = [], [], collections.Counter(); reg = spec["registers"]
for _ in range(N):
    c, err = E.build(rng)
    if err or E.gates(c): continue
    ns = c["notes"]; t = max(ns, key=lambda n: n["p"]); b = min(ns, key=lambda n: n["p"]); hi_.append(t["p"]); lo_.append(b["p"]); top_sec[E.KIND.get(t["sec"], t["sec"])] += 1
out["b"] = dict(registers=reg, highest_note_quartiles=[float(x) for x in np.percentile(hi_, (25, 50, 75))], lowest_note_quartiles=[float(x) for x in np.percentile(lo_, (25, 50, 75))],
                span_quartiles=[float(x) for x in np.percentile(np.array(hi_) - np.array(lo_), (25, 50, 75))], highest_note_in=dict(top_sec), builds=len(hi_), aim_range=spec["target"]["readings"]["range"])
print("55", out["b"], flush=True)
os.makedirs(os.path.join(ROOT, "studies", "review20"), exist_ok=True); json.dump(out, open(os.path.join(ROOT, "studies", "review20", "stepfit.json"), "w"), indent=1)
