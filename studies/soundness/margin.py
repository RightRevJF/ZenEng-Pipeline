"""Does a pass by three thousandths hold? The pick is the first build in order past the gates, so it is in effect one draw from the gated pool. For each 4/4
song: the engine's 1,000 builds (same seed and spec as song_from_lyric.py), the gates as the engine applies them (874's old charge, the joint gate, 913/914's
words gate read as sung), then each pool build's rhythm scaling and pitch scaling read as soundness.py reads them (as sung, melismas placed). The share of the
pool past the kept 10th (rhythm, low) and 90th (pitch, high) gives the chance that a fresh draw of the three songs leans past the bound. Also the kept bounds'
own uncertainty: the 10th and 90th by bootstrap over the 160 kept songs.
    python3 studies/soundness/margin.py songs/p65/lyric55.json songs/p64/lyric54.json songs/p68/lyric58.json   (PYTHONHASHSEED=0)"""
import sys, os, json, random, hashlib
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.dirname(os.path.abspath(__file__))]
if os.environ.get("MARGIN_TURNS_OF_FOUR"): sys.path.insert(0, os.environ["MARGIN_TURNS_OF_FOUR"])     # a trial: song_from_lyric with every turn four bars (749.95)
import song_from_lyric as SL; import metre_engine as M, word_weight as WW, scaling as SC     # song_from_lyric first, so a trial copy is the one loaded
class Got(Exception): pass
CAP = {}
def scal(ns):
    s = SC.series([(n["on"], n["p"]) for n in sorted(ns, key=lambda n: n["on"])]); a = SC.dfa(s["pitch"]); b = SC.dfa(s["onsets on the grid"]); return (a["alpha"] if a else None), (b["alpha"] if b else None)
def capture(self, N, seed):
    rng = random.Random(seed); alive = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        r = self.readings(c["notes"]); ch, dist = self.charge(r); c.update(readings=r, charge=ch, distance=dist, n=k); alive.append(c)
    import luthier_judge7 as J7; J = J7.Judge7(self.S.get("table") or self.S["metre"].replace("/", "-") + "_sung")
    for c in alive:
        c["d7"] = J.distance(c["readings"]); sung = self.as_sung(c["notes"]); f = WW.fit([x for x in sung if x.get("melisma") != "second"], self.BAR, self.BEAT, parts=True)
        c.update(f_all=f["all"], f_len=f["length"], f_ht=f["height"]); c["ps"], c["rs"] = scal(sung)
    half = float(np.median([c["charge"] for c in alive])); ok = [c for c in alive if c["charge"] <= half and c["d7"] <= J.gate]
    ml = float(np.median([c["f_len"] for c in alive])); mh = float(np.median([c["f_ht"] for c in alive]))
    pool = [c for c in ok if c["f_all"] >= self.WW["gate"] and c["f_len"] >= ml and c["f_ht"] >= mh] or ok
    pick = min(pool, key=lambda c: c["n"]); CAP.update(alive=alive, pool=pool, pick=pick); raise Got()
M.Engine.run = capture
import soundness as S
K = S.kept_rows(); rs_k = np.array([r["rhythm scaling"] for r in K.values()]); ps_k = np.array([r["pitch scaling"] for r in K.values()])
R10, P90 = float(np.percentile(rs_k, 10)), float(np.percentile(ps_k, 90)); rng = np.random.default_rng(1)
b10 = [float(np.percentile(rng.choice(rs_k, len(rs_k)), 10)) for _ in range(5000)]; b90 = [float(np.percentile(rng.choice(ps_k, len(ps_k)), 90)) for _ in range(5000)]
out = dict(kept=dict(rhythm_10th=round(R10, 3), rhythm_10th_bootstrap_5_95=[round(float(x), 3) for x in np.percentile(b10, (5, 95))], pitch_90th=round(P90, 3), pitch_90th_bootstrap_5_95=[round(float(x), 3) for x in np.percentile(b90, (5, 95))]), songs={})
for f in sys.argv[1:]:
    L = json.load(open(f))
    try: SL.write(L, 1000, 12)
    except Got: pass
    P = CAP["pool"]; pk = CAP["pick"]; rs = np.array([c["rs"] for c in P]); ps = np.array([c["ps"] for c in P])
    out["songs"][os.path.basename(f)] = dict(pool=len(P), pick_fp=hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in pk["notes"]]).encode()).hexdigest()[:12], pick_rhythm=round(pk["rs"], 3), pick_pitch=round(pk["ps"], 3),
        pool_rhythm_10_25_50_75_90=[round(float(x), 3) for x in np.percentile(rs, (10, 25, 50, 75, 90))], pool_rhythm_under_kept_10th=round(float(np.mean(rs < R10)), 3),
        pool_pitch_10_25_50_75_90=[round(float(x), 3) for x in np.percentile(ps, (10, 25, 50, 75, 90))], pool_pitch_over_kept_90th=round(float(np.mean(ps > P90)), 3))
    print(os.path.basename(f), json.dumps(out["songs"][os.path.basename(f)]), flush=True)
sh = [v["pool_rhythm_under_kept_10th"] for v in out["songs"].values()]; sp = [v["pool_pitch_over_kept_90th"] for v in out["songs"].values()]
out["chance_a_fresh_draw_leans"] = dict(rhythm_low=round(float(np.prod(sh)), 3), pitch_high=round(float(np.prod(sp)), 3), kept_songs_any_one_check=0.001)
print(json.dumps(out["kept"]), json.dumps(out["chance_a_fresh_draw_leans"]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "margin_turns_of_four.json" if os.environ.get("MARGIN_TURNS_OF_FOUR") else "margin.json"), "w"), indent=1)
