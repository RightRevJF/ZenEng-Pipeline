"""FIT: a song's intrinsic fitness from the TIMING of its covers alone (run 12, physics vector 1; Jason's word of 28 Nov 2026).
Written and frozen from the versions alone, before any notes measure is joined to it. It reads no notes and no notes measure.

Model (Price / Bianconi-Barabasi growth with aging, a gamma-mixed Poisson process in calendar years):
  covers of song i first released in year t (t = t0_i .. 2023):  n_it ~ Poisson( eta_i * (k_i(t-) + A) * g(age) * h(t) )
  k_i(t-)  = covers of i released before year t (preferential attachment: the rich get richer);
  A        = initial attractiveness (a song with no covers can still be found);
  g(age)   = aging, piecewise constant on age bins 0 | 1 | 2-3 | 4-7 | 8-15 | 16-31 | 32+  (g(0) = 1);
  h(t)     = the era's cover activity, piecewise constant on 5-year bins (before 1950 one bin; 2020-2023 one bin);
  eta_i    = the song's FITNESS, Gamma(shape r, rate r), mean 1.
The marginal likelihood integrates eta (Poisson-gamma), so A, g, h and r are fitted by maximum likelihood over ALL matched
Discogs-VI groups (2,915 cliques of the data pack, not only the test rows). Then each song's fitness is the posterior mean of log eta:
  FIT_i = digamma(r + N_i) - log(r + E_i),   N_i = sum_t n_it,   E_i = sum_t (k_i(t-) + A) g(age) h(t).
What FIT removes that a raw count keeps: (1) age and era exposure (a 2015 song has had less time); (2) the rich-get-richer
feedback (a cover that arrives when a song already has 20 is worth less evidence of fitness than one that arrives on a bare song);
(3) small-number luck (shrinkage toward the mean by r).
Covers: a version is a cover iff its performing-artist set shares no normalised name with the original artist's sets (run 04's
y_foreign rule; the original artist is the Hooktheory artist slug of the group's video). Versions with no year, or a year after
2023 (the dump is from July 2024), are dropped from the timing; how many is printed. t0_i = the group's first_year.
Reading (frozen, not counted): FIT_NOPA, the same model with no attachment term (mu = eta g h), so the attachment term's work shows.
Credit: Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0. Hooktheory artist slugs via Sheet Sage, CC BY-NC-SA 3.0.

Usage: python3 fitness.py  -> /home/claude/dl/run12/fitness.json (per video id: FIT, FIT_NOPA, N, E, t0, k_final) and fit.json here.
"""
import os, re, io, gzip, json, math, subprocess, hashlib
import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln, digamma

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/dl/run12/fitness.json"
LAST = 2023
AGE_EDGES = [0, 1, 2, 4, 8, 16, 32]          # bins [0,1),[1,2),[2,4),[4,8),[8,16),[16,32),[32,inf)
def era_bin(t): return 0 if t < 1950 else min(1 + (t - 1950) // 5, 15)   # 1950-54 -> 1, ..., 2020-23 -> 15
NERA = 16
GIT = lambda p: subprocess.run(["git", "-C", HERE, "show", f"origin/main:studies/judging_data/{p}"], check=True, capture_output=True).stdout
nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))

def age_bin(a): return int(np.searchsorted(AGE_EDGES, a, side="right") - 1)

def load():
    VC = json.loads(GIT("discogs_versions_matched.json"))["cliques"]
    S = json.load(gzip.open(io.BytesIO(GIT("hooktheory_surprise.json.gz"))))
    art = {}
    for c in S: art.setdefault(c["vid"], c["artist"])
    songs, dropped_noyear, dropped_late, noown = [], 0, 0, 0
    for cq, v in sorted(VC.items()):
        vid = v["video"]; a = nrm(art.get(vid, ""))
        sets = v["versions"]; own = [s for s, y, _ in sets if any(nrm(n) == a for n in s)]
        if not own: noown += 1; continue
        O = {nrm(n) for s in own for n in s}
        t0 = int(v["first_year"]); yrs = []
        for s, y, _ in sets:
            if len(s) == 0 or any(nrm(n) in O for n in s): continue
            if y is None: dropped_noyear += 1; continue
            if y > LAST: dropped_late += 1; continue
            yrs.append(max(int(y), t0))
        songs.append(dict(clique=cq, vid=vid, t0=t0, years=sorted(yrs)))
    return songs, dict(cliques=len(VC), songs=len(songs), no_own_set=noown, covers_no_year=dropped_noyear, covers_after_2023=dropped_late,
                       covers_timed=sum(len(s["years"]) for s in songs))

def design(songs):
    """per song: arrays over years t0..LAST of n_t, k_t- , age bin, era bin."""
    D = []
    for s in songs:
        T = np.arange(s["t0"], LAST + 1)
        if len(T) == 0: T = np.array([LAST])
        cnt = np.zeros(len(T)); 
        for y in s["years"]: cnt[min(y, LAST) - T[0]] += 1
        k = np.concatenate([[0], np.cumsum(cnt)[:-1]])
        D.append(dict(n=cnt, k=k, ab=np.array([age_bin(t - T[0]) for t in T]), eb=np.array([era_bin(t) for t in T])))
    return D

def unpack(th, pa):
    i = 0; lr = th[i]; i += 1
    lA = th[i] if pa else None; i += 1 if pa else 0
    lg = np.concatenate([[0.0], th[i:i + len(AGE_EDGES) - 1]]); i += len(AGE_EDGES) - 1
    lh = th[i:i + NERA]
    return lr, lA, lg, lh

def negll(th, D, pa):
    lr, lA, lg, lh = unpack(th, pa); r = math.exp(lr); A = math.exp(lA) if pa else None
    ll = 0.0
    for d in D:
        base = np.exp(lg[d["ab"]] + lh[d["eb"]]); m = (d["k"] + A) * base if pa else base
        N = d["n"].sum(); E = m.sum()
        ll += float((d["n"] * np.log(m)).sum()) + r * math.log(r) + gammaln(r + N) - gammaln(r) - (r + N) * math.log(r + E)
    return -ll

def fit(D, pa):
    th0 = np.concatenate([[0.0], [0.0] if pa else [], np.zeros(len(AGE_EDGES) - 1), np.full(NERA, -3.0)])
    res = minimize(negll, th0, args=(D, pa), method="L-BFGS-B", options=dict(maxiter=3000))
    return res

def scores(th, D, pa):
    lr, lA, lg, lh = unpack(th, pa); r = math.exp(lr); A = math.exp(lA) if pa else None
    out = []
    for d in D:
        base = np.exp(lg[d["ab"]] + lh[d["eb"]]); m = (d["k"] + A) * base if pa else base
        N = d["n"].sum(); E = m.sum(); out.append((float(digamma(r + N) - math.log(r + E)), float(N), float(E)))
    return out

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    songs, info = load(); D = design(songs); print(info, flush=True)
    rp = fit(D, True); rn = fit(D, False)
    lr, lA, lg, lh = unpack(rp.x, True)
    sp, sn = scores(rp.x, D, True), scores(rn.x, D, False)
    res = {s["vid"]: dict(FIT=a[0], FIT_NOPA=b[0], N=a[1], E=a[2], t0=s["t0"], clique=s["clique"]) for s, a, b in zip(songs, sp, sn)}
    json.dump(res, open(OUT, "w"))
    summ = dict(info=info, pa=dict(converged=bool(rp.success), negll=float(rp.fun), r=math.exp(lr), A=math.exp(lA),
                                    g=[float(math.exp(x)) for x in lg], h=[float(math.exp(x)) for x in lh]),
                nopa=dict(converged=bool(rn.success), negll=float(rn.fun), r=math.exp(unpack(rn.x, False)[0])),
                lr_test_pa_vs_nopa=float(2 * (rn.fun - rp.fun)),
                sha256_out=hashlib.sha256(open(OUT, "rb").read()).hexdigest())
    json.dump(summ, open(os.path.join(HERE, "fit.json"), "w"), indent=1)
    print(json.dumps(summ, indent=1))

if __name__ == "__main__":
    main()
