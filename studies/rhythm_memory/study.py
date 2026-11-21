"""What gives a kept song's rhythm its long memory? See PREDICTION.md. PYTHONHASHSEED=0 python3 studies/rhythm_memory/study.py [N] -> result.json"""
import sys, os, json, random, collections, numpy as np
from scipy.stats import spearmanr
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import kept_corpus as KC, scaling as SC
N = int(sys.argv[1]) if len(sys.argv) > 1 else 80; NAMES = ["slow change in how busy the singing is", "silence", "near answers", "far returns"]
def read(ons, bar=48):
    ons = sorted(int(t) for t in ons); t0 = ons[0] // bar; nb = ons[-1] // bar - t0 + 1; cnt = np.zeros(nb); by = collections.defaultdict(list)
    for t in ons: cnt[t // bar - t0] += 1; by[t // bar - t0].append(t % bar)
    w = [cnt[i:i + 4].mean() for i in range(0, nb - 3, 4)]; slow = float(np.std(w) / np.mean(w)) if len(w) >= 3 and np.mean(w) > 0 else np.nan
    last = {}; near = far = 0; sung = sorted(by)
    for b in sung:
        p = tuple(sorted(by[b]))
        if p in last:
            d = b - last[p]; near += d <= 8; far += d > 16
        last[p] = b
    g0 = ons[0] // 3; grid = np.zeros(ons[-1] // 3 - g0 + 1); grid[[t // 3 - g0 for t in ons]] = 1; a = SC.dfa(grid)
    return dict(rhythm_scaling=a["alpha"] if a else np.nan, **dict(zip(NAMES, [slow, float(np.mean(cnt == 0)), near / len(sung), far / len(sung)])))
K = [read(k["t"]) for k in KC.kept_songs()]; K = [r for r in K if not any(np.isnan(v) for v in r.values())]; y = np.array([r["rhythm_scaling"] for r in K]); rng = np.random.default_rng(0); out = dict(kept_songs=len(K), carries={}, luthier={})
print("kept songs", len(K), "rhythm scaling quartiles", np.round(np.percentile(y, (25, 50, 75)), 3))
for c in NAMES:
    x = np.array([r[c] for r in K]); r = float(spearmanr(x, y)[0]); sh = np.array([abs(spearmanr(x, rng.permutation(y))[0]) for _ in range(1000)])
    out["carries"][c] = dict(rank_correlation=round(r, 3), beats_share_of_shuffles=round(float(np.mean(sh < abs(r))), 3), carries=bool(abs(r) >= 0.30 and np.mean(sh < abs(r)) >= 0.99), kept_quartiles=[round(float(v), 3) for v in np.percentile(x, (25, 50, 75))])
    print(f"  {c:42} {r:+.3f}  carries: {out['carries'][c]['carries']}  kept quartiles {out['carries'][c]['kept_quartiles']}")
import metre_engine as M, song_from_lyric as SL
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    spec = json.load(open(os.path.join(ROOT, p + ".song.json")))["spec"]; L = json.load(open(os.path.join(ROOT, p + ".json"))); tg = spec["target"]; E = M.Engine(spec); rg = random.Random(31); rows = []
    for _ in range(N):
        c, err = E.build(rg)
        if err or E.gates(c): continue
        s = SL.melisma_notes(c["notes"], L, set(spec["scale"]), key="p", how=spec.get("how"), cap=tg.get("run"), share=tg.get("melisma_share"))[0]; rows.append(read([n["on"] for n in s]))
    med = {c: round(float(np.nanmedian([r[c] for r in rows])), 3) for c in ["rhythm_scaling"] + NAMES}
    place = {c: ("under the kept 25th" if med[c] < out["carries"][c]["kept_quartiles"][0] else "over the kept 75th" if med[c] > out["carries"][c]["kept_quartiles"][2] else "kept middle half") for c in NAMES}
    out["luthier"][tag] = dict(builds=len(rows), medians=med, place=place); print(tag, len(rows), med, place, flush=True)
T3 = ("55", "54", "58"); cause = []
for c in NAMES:
    v = out["carries"][c]
    if not v["carries"]: continue
    low_side = "under the kept 25th" if v["rank_correlation"] > 0 else "over the kept 75th"
    if sum(out["luthier"][t]["place"][c] == low_side for t in T3) >= 2: cause.append(c)
out["cause"] = cause; print("cause:", cause); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
