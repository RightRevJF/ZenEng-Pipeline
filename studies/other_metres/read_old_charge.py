"""A read of the old charge (874) on a record: which readings it charges, against what band, and on living builds which readings carry the charge. python3 studies/other_metres/read_old_charge.py LYRIC.json RECORD.song.json [BUILDS] -> prints JSON. A read; no note is changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA
M = CA.M
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); E, sp = CA.engine(L, R); rng = random.Random(L.get("seed", 1)); tot = collections.defaultdict(float); hi = collections.Counter(); lo = collections.Counter(); n = 0; vals = collections.defaultdict(list)
    for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 400):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; r = E.readings(c["notes"])
        for k, (a, m, z) in E.Q.items():
            if k not in r or k in M.UNCHARGED: continue
            s_ = ((z - a) or M.FLOOR(m)); x = max(0.0, a - r[k]) / s_ + max(0.0, r[k] - z) / s_; tot[k] += x; hi[k] += r[k] > z; lo[k] += r[k] < a; vals[k].append(r[k])
    T = sum(tot.values())
    print(json.dumps(dict(table=sp.get("table"), the_band_is="the table's readings_quartiles: its 25th, 50th, 75th (the charge is the distance outside the 25th to 75th, over their spread)", table_source=json.load(open(os.path.join(M.ATLAS, (sp.get("table") or sp["metre"].replace("/", "-") + "_sung") + ".json"))).get("source"), uncharged=list(M.UNCHARGED), living_builds=n,
                          charged={k: dict(band_25_50_75=[round(x, 3) for x in E.Q[k]], builds_median=round(float(np.median(vals[k])), 3), share_of_builds_over_the_75th=round(hi[k] / n, 3), share_under_the_25th=round(lo[k] / n, 3), share_of_all_charge=round(tot[k] / T, 3)) for k in sorted(tot, key=lambda k: -tot[k])}), indent=1))
