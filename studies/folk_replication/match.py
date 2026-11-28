"""Folk replication: the match, by PREDICTION.md, before any outcome is joined.
Reads measures.json.gz (repo) and clique_titles.jsonl (outside the repo; titles only, no counts). Writes matches.json
(per kept tune: clique id, step, half) and match_check_sample.json (the random hundred, for the eye check), and prints
the numbers matched and each test's power. Never opens clique_counts.json.
python3 -I match.py /home/claude/dl/discogsvi/clique_titles.jsonl"""
import sys, os, json, gzip, hashlib, collections, math
import numpy as np
from scipy.stats import norm as N
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import keys as K
ORDER = {"oneills": 0, "ryans": 1, "airds": 2, "essen": 3}
MEASURES = ["pc_entropy", "surprise", "different_pitches", "time_on_tonic", "five_note_share", "six_note_share", "leaps", "repeated_figures", "plainness"]
K_TESTS = 18; ALPHA = 0.05 / K_TESTS; RHO = 0.15

def half_of(k): return int(hashlib.md5(k.encode()).hexdigest(), 16) % 2

def power_one(n, rho, alpha, se):
    z = math.atanh(rho); return float(1 - N.cdf(N.ppf(1 - alpha) - z / se))

def power(n_test, n_conf, k_test, k_conf, rho=RHO):
    if min(n_test, n_conf) < 10: return dict(A=0.0, B=0.0)
    pa = power_one(n_test, rho, ALPHA, math.sqrt(1.06 / (n_test - 3))) * power_one(n_conf, rho, 0.05, math.sqrt(1.06 / (n_conf - 3)))
    pb = power_one(n_test, rho, ALPHA, 1 / math.sqrt(max(n_test - k_test - 3, 1))) * power_one(n_conf, rho, 0.05, 1 / math.sqrt(max(n_conf - k_conf - 3, 1)))
    return dict(A=pa, B=pb)

def mde(n_test, n_conf, k_test, k_conf, form):
    lo, hi = 0.0, 0.99
    for _ in range(60):
        m = (lo + hi) / 2; p = power(n_test, n_conf, k_test, k_conf, m)[form]
        lo, hi = (m, hi) if p < 0.5 else (lo, m)
    return hi

def pooled_groups(vals, min_n, into):
    c = collections.Counter(vals); return [v if c[v] >= min_n else into for v in vals]

def n_controls(rows):
    met = pooled_groups([r["metre"] for r in rows], 5, "other"); col = pooled_groups([r["collection"] for r in rows], 5, "oneills")
    return 2 + (len(set(met)) - 1) + (len(set(col)) - 1)

class Tee:
    def __init__(self, f): self.f = f; self.o = sys.stdout
    def write(self, s): self.o.write(s); self.f.write(s)
    def flush(self): self.o.flush(); self.f.flush()

def main(path):
    sys.stdout = Tee(open(os.path.join(HERE, "match_log.txt"), "w"))
    M = json.load(gzip.open(os.path.join(HERE, "measures.json.gz"), "rt"))["rows"]
    ex = collections.defaultdict(set); lo = collections.defaultdict(set); trad = {}; info = {}
    for line in open(path):
        c = json.loads(line); trad[c["id"]] = c["trad"]
        for k in c["ek"]: ex[k].add(c["id"])
        for k in c["lk"]: lo[k].add(c["id"])
        info[c["id"]] = dict(titles=c["titles"][:4], writers=c["writers"][:4], artists=c["artists"][:3], genres=c["genres"])
    steps = collections.Counter(); kept = {}
    for r in sorted(M, key=lambda r: (ORDER[r["collection"]], r["file"], int(r["x"]) if str(r["x"]).isdigit() else 10**9, r["x"])):
        ts = [t for t in r["titles"] if K.usable(t)]
        if not ts: steps["no usable title"] += 1; continue
        got = None
        for step, idx, kf in (("exact", ex, K.exact_key), ("loose", lo, K.loose_key)):
            cand = set().union(*[idx.get(kf(t), set()) for t in ts])
            if len(cand) == 1: got = (next(iter(cand)), step, False); break
            if len(cand) > 1:
                tc = [c for c in cand if trad[c]]
                got = (tc[0], step, True) if len(tc) == 1 else ("AMBIG", step, False); break
        if got is None: steps["unmatched"] += 1; continue
        if got[0] == "AMBIG": steps["ambiguous (" + got[1] + ")"] += 1; continue
        cid, step, tb = got
        if cid in kept: steps["clique already taken"] += 1; continue
        k0 = K.exact_key(ts[0])
        kept[cid] = dict(id=r["id"], clique=cid, step=step, tiebreak=tb, half=half_of(k0), key=k0, collection=r["collection"], metre=r["metre"], titles=r["titles"])
        steps["matched " + step + (" tie-broken" if tb else "")] += 1
    rows = list(kept.values()); json.dump(dict(rows=rows, steps=dict(steps)), open(os.path.join(HERE, "matches.json"), "w"), indent=0)
    print("tunes read", len(M)); [print(" ", k, v) for k, v in sorted(steps.items())]
    byid = {r["id"]: r for r in M}
    for form_rows, label in ((rows, "all matches"), ([r for r in rows if r["step"] == "exact"], "exact-title matches only")):
        t = [r for r in form_rows if r["half"] == 0]; c = [r for r in form_rows if r["half"] == 1]
        kt = n_controls([byid[r["id"]] for r in t]) if t else 0; kc = n_controls([byid[r["id"]] for r in c]) if c else 0
        print("\n%s: %d tunes; test half %d, confirm half %d" % (label, len(form_rows), len(t), len(c)))
        print("  by collection:", dict(collections.Counter(r["collection"] for r in form_rows)))
        print("  by metre:", dict(collections.Counter(r["metre"] for r in form_rows)))
        p = power(len(t), len(c), kt, kc)
        print("  power at a correlation of %.2f (test half at %.5f one-sided, times confirm half at .05): form A %.3f, form B %.3f" % (RHO, ALPHA, p["A"], p["B"]))
        if len(t) >= 10 and len(c) >= 10:
            print("  smallest correlation with power one half: form A %.3f, form B %.3f" % (mde(len(t), len(c), kt, kc, "A"), mde(len(t), len(c), kt, kc, "B")))
        print("  " + ("POWER UNDER ONE HALF: every test here is an estimate" if max(p.values()) < 0.5 else "power one half or more"))
    rng = np.random.default_rng(20261127); pick = rng.choice(len(rows), size=min(100, len(rows)), replace=False)
    sample = [dict(n=i + 1, tune_titles=rows[j]["titles"], collection=rows[j]["collection"], metre=rows[j]["metre"], step=rows[j]["step"], clique=rows[j]["clique"], **info[rows[j]["clique"]]) for i, j in enumerate(sorted(pick))]
    json.dump(sample, open(os.path.join(HERE, "match_check_sample.json"), "w"), indent=1, ensure_ascii=False)
    print("\nmatch check sample:", len(sample), "-> match_check_sample.json")

if __name__ == "__main__":
    main(sys.argv[1])
