"""PREDICTION_counts_251.md: (a) lines sung again sorted by how their syllables stood against the source's kept notes; (b) the run repeated as the engine makes it, and K3, K5, K6 on the living builds, the old charge's half, and the pool.  python3 studies/other_metres/count_after_251.py LYRIC.json RECORD.song.json -> prints JSON. Counts; no note is changed."""
import os, sys, json, random, collections, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, pop_read as PR
M = PR.M; SL = PR.SL
def engine(L, R):
    sp = json.loads(json.dumps(R["spec"])); E = M.Engine(sp); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(sp["scale"]), key="p", how=sp.get("how"), cap=None, share=None, clash=None, relocate=False)[0]; return E, sp
def count_a(L, R, builds=400, seed=1):
    E, sp = engine(L, R); how = {}; inner = E.again
    def wrapped(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        floor = max(tmin, 0) if (sy[0][1] and not src_st0 and src[0][0] < 0) else tmin; keep = [(t, p) for t, p in src if t >= floor] or src[-1:]
        if E.S.get("again_refit"): keep = [(t, p) for t, p in keep if t <= slot - (12 if E.LE else E.BREATH)] or keep[:1]
        how[(sec, i)] = len(sy) - len(keep); return inner(rng, src, src_st0, sy, U, sec, i, tmin, slot)
    E.again = wrapped; G = collections.defaultdict(lambda: [0, 0, 0]); rng = random.Random(seed); n = 0; hooks = set(sp.get("hooks", ()))
    for _ in range(builds):
        how.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1
        for x in c["notes"]:
            if not x["stress"]: continue
            k = (x["sec"], x["line"]); made = E._made.get(k, "?"); keys = ["all"]
            if made in ("again", "818 again"):
                d = how.get(k); sort = "not seen" if d is None else "the same count" if d == 0 else ("%s, one to three %s" % (made, "more syllables" if d > 0 else "fewer syllables")) if abs(d) <= 3 else "more than three apart"
                keys += ["again and 818 together", made + ": " + (sort if d == 0 or d is None or abs(d) > 3 else sort.split(", ")[1]), "together: " + (sort if d == 0 or d is None or abs(d) > 3 else sort.split(", ")[1])]
            for key in keys: v = G[key]; v[0] += 1; v[1] += x["on"] % E.BAR == 0; v[2] += not E.on_beat(x["on"])
    tot = G["all"][0]; ag = G["again and 818 together"][0]
    return dict(living_builds=n, rows={k: dict(share_of_the_songs_stresses=round(v[0] / tot, 3), share_of_again_and_818_stresses=round(v[0] / ag, 3) if k != "all" else None, on_the_first_beat=round(v[1] / v[0], 3), off_the_beat=round(v[2] / v[0], 3)) for k, v in sorted(G.items())})
def count_b(L, R, N=1000):
    import luthier_judge7 as J7
    E, sp = engine(L, R); phr = sum(sum(v) for v in sp["slots"].values()); rng = random.Random(L.get("seed", 1)); alive = []
    for k in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        r = E.readings(c["notes"]); ch, dist = E.charge(r); c.update(readings=r, charge=ch, n=k); c["fp"] = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in c["notes"]]).encode()).hexdigest()[:12]; c["figs"] = PR.figs(E.as_sung(c["notes"]), phr); alive.append(c)
    J = J7.Judge7(sp.get("table") or sp["metre"].replace("/", "-") + "_sung")
    for c in alive: c["d7"] = J.distance(c["readings"])
    half = float(np.median([c["charge"] for c in alive])); first = [c for c in alive if c["charge"] <= half]; out_ = [c for c in alive if c["charge"] > half]; pool = [c for c in first if c["d7"] <= J.gate]
    fl = ((sp.get("target") or {}).get("choose_range") or sp.get("choose_range") or {}).get("floor"); nr = [c for c in pool if fl is None or c["readings"]["range"] >= fl]; pick = min(nr or pool, key=lambda c: c["n"])
    keys = ("first_beat_stress", "stress_off_the_beat", "commonest", "rhythm_again_in_sections")
    def desc(cs):
        return dict(builds=len(cs), median={k: round(float(np.median([c["figs"][k] for c in cs])), 3) for k in keys}, meeting_in_100={k: round(100 * float(np.mean([PR.met(k, c["figs"][k]) for c in cs])), 1) for k in keys}, meeting_every_figure_mark_in_100=round(100 * float(np.mean([all(PR.met(k, c["figs"][k]) for k in PR.MARK) for c in cs])), 1))
    good = [c for c in pool if all(PR.met(k, c["figs"][k]) for k in PR.MARK)]; byd = sorted(pool, key=lambda c: abs(c["d7"] - J.usual)); corr = lambda a, b: round(float(np.corrcoef(a, b)[0, 1]), 3)
    return dict(checks=dict(living=len(alive), living_in_the_record=R["melody"]["survivors"], pool=len(pool), pool_in_the_record=R["judge7"]["pass_the_gate"], pick=pick["fp"], pick_in_the_record=R["melody"]["pick"]),
                living=desc(alive), the_half_the_old_charge_keeps=desc(first), the_half_the_old_charge_removes=desc(out_), the_pool=desc(pool), the_pick=dict(order_built_among_the_pool=sorted(c["n"] for c in pool).index(pick["n"]) + 1, figs={k: round(pick["figs"][k], 3) for k in keys}, distance=round(pick["d7"], 3)),
                the_first_pool_build_meeting_every_mark=dict(order_built_among_the_pool=(sorted(c["n"] for c in pool).index(min(c["n"] for c in good)) + 1) if good else None, pool_builds_meeting_every_mark=len(good)),
                among_living_builds_correlation_with_the_old_charge={k: corr([c["charge"] for c in alive], [c["figs"][k] for c in alive]) for k in keys}, among_living_builds_correlation_with_the_judges_distance={k: corr([c["d7"] for c in alive], [c["figs"][k] for c in alive]) for k in keys})
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); print(json.dumps(dict(a=count_a(L, R), b=count_b(L, R)), indent=1))
