"""749.220, PREDICTION.md: the commonest pitch's share by section kind, kept songs, records and builds.  N=300 python3 studies/section_ceiling/read.py -> read.json"""
import os, sys, json, re, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, kept_corpus as KC, make_kept_commonest_pitch as CP, song_from_lyric as SL, metre_engine as M
KINDS = ("Verse", "Chorus", "Pre-chorus", "Bridge"); N = int(os.environ.get("N", "300"))
def kind(x):
    w = re.findall(r"[a-z]+", str(x).lower())
    if any(z.startswith("pre") for z in w): return "Pre-chorus"
    return "Bridge" if "bridge" in w else CP.kind(x)
def shares(ps, secs):
    o = {}
    for kd in KINDS:
        v = [p for p, x in zip(ps, secs) if kind(x) == kd]; s = CP.share(v)
        if s is not None: o[kd] = (s, len(v))
    return o
kept = {kd: [] for kd in KINDS}
for k in KC.kept_songs():
    for kd, v in shares(k["p"], k["sec"]).items(): kept[kd].append(v)
rng = np.random.default_rng(0); out = dict(kept={}, songs={})
for kd, v in kept.items():
    s = [a for a, _ in v]; r = [round(float(x), 3) for x in np.percentile([np.percentile(rng.choice(s, len(s)), 90) for _ in range(2000)], (5, 95))]
    out["kept"][kd] = dict(songs=len(s), p10_25_50_75_90=[round(float(x), 3) for x in np.percentile(s, (10, 25, 50, 75, 90))], p90_range=r, median_notes=st.median(b for _, b in v), line=r[1] if len(s) < 30 else round(float(np.percentile(s, 90)), 3))
print(json.dumps(out["kept"]), flush=True)
for tag, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59"), ("61", "songs/p71/lyric61"), ("66", "songs/p76/lyric66")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = json.loads(json.dumps(rec["spec"])); spec["copy_clash"] = True; spec["melisma_clear"] = "after"
    ns = rec["melody"]["notes"]; o = dict(record={kd: dict(share=round(a, 3), notes=b, over=bool(a > out["kept"][kd]["line"])) for kd, (a, b) in shares([n["midi"] for n in ns], [n.get("sec") for n in ns]).items()})
    E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=None, relocate=False)[0]
    r_ = random.Random(L.get("seed", 1)); B = collections.defaultdict(list); living = 0
    for _ in range(N):
        c, err = E.build(r_)
        if err or E.gates(c): continue
        living += 1; s = E.as_sung(c["notes"])
        for kd, (a, b) in shares([n["p"] for n in s], [n["sec"] for n in s]).items(): B[kd].append(a)
    o["living"] = living; o["builds"] = {kd: dict(median=round(st.median(v), 3), over_per_100=round(100 * sum(a > out["kept"][kd]["line"] for a in v) / len(v), 1)) for kd, v in B.items()}
    out["songs"][tag] = o; print(tag, json.dumps(o), flush=True)
out["named"] = {kd: dict(songs_with=sum(kd in o["builds"] for o in out["songs"].values()), songs_over_20=sum(o["builds"].get(kd, {}).get("over_per_100", 0) > 20 for o in out["songs"].values())) for kd in KINDS}
for kd, d in out["named"].items(): d["verdict"] = "described only" if d["songs_with"] < 3 else "named" if d["songs_over_20"] >= 3 else "not named"
print(json.dumps(out["named"])); json.dump(out, open(os.path.join(HERE, "read.json"), "w"), indent=1)
