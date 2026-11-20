"""Review 20: is the register's top a ceiling the tune presses against, or a peak it reaches? Share of notes on the tune's top note, kept against each song's builds (before melismas)."""
# Review 20 (Luthier v33). Run from the repo root with PYTHONHASHSEED=0.
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC, metre_engine as M
top = lambda p: float((np.asarray(p) == max(p)).mean())
K = [top(k["p"]) for k in KC.kept_songs()]; out = dict(kept_share_on_top_10_25_50_75_90=[round(float(x), 3) for x in np.percentile(K, (10, 25, 50, 75, 90))])
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); E = M.Engine(R["spec"]); rng = random.Random(3); sh, span, hit = [], [], []
    tops = {k: v[2] for k, v in R["spec"]["registers"].items()}
    for _ in range(100):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        p = [n["p"] for n in c["notes"]]; sh.append(top(p)); span.append(max(p) - min(p)); hit.append(max(p) >= max(tops.values()) - 1 or any(max([n["p"] for n in c["notes"] if E.KIND.get(n["sec"]) == k] or [0]) >= t for k, t in tops.items()))
    pk = [n["midi"] for n in R["melody"]["notes"] if n.get("melisma") != "second"]
    out[tag] = dict(builds=len(sh), share_on_top_quartiles=[round(float(x), 3) for x in np.percentile(sh, (25, 50, 75))], over_kept_90th=round(float(np.mean(np.array(sh) > out["kept_share_on_top_10_25_50_75_90"][4])), 2),
                    span_quartiles=[float(x) for x in np.percentile(span, (25, 50, 75))], reaches_a_register_top=round(float(np.mean(hit)), 2), registers=R["spec"]["registers"], pick_share_on_top=round(top(pk), 3), pick_span=max(pk) - min(pk), aim_range=R["spec"]["target"]["readings"]["range"])
    print(tag, out[tag], flush=True)
print(out["kept_share_on_top_10_25_50_75_90"])
os.makedirs(os.path.join(ROOT, "studies", "review20"), exist_ok=True); json.dump(out, open(os.path.join(ROOT, "studies", "review20", "ceiling.json"), "w"), indent=1)
