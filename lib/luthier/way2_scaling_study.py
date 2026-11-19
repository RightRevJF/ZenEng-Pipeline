import sys, json, random, numpy as np
sys.path[:0] = ["/home/claude/zeneng/corpus/v20", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"]
def dfa(x, order=1, smin=4, nscales=14):
    x = np.asarray(x, float); n = len(x)
    if n < 64 or np.std(x) == 0: return None
    y = np.cumsum(x - x.mean()); smax = n // 4; S = np.unique(np.round(np.logspace(np.log10(smin), np.log10(smax), nscales)).astype(int)); F = []
    for s in S:
        m = n // s; segs = np.concatenate([y[:m * s].reshape(m, s), y[n - m * s:].reshape(m, s)]); t = np.arange(s); f2 = []
        for seg in segs: c = np.polyfit(t, seg, order); f2.append(np.mean((seg - np.polyval(c, t)) ** 2))
        F.append(np.sqrt(np.mean(f2)))
    S = S.astype(float); F = np.array(F); ok = F > 0
    if ok.sum() < 5: return None
    ls, lf = np.log(S[ok]), np.log(F[ok]); a = np.polyfit(ls, lf, 1)[0]; half = len(ls) // 2
    return dict(alpha=float(a), short=float(np.polyfit(ls[:half + 1], lf[:half + 1], 1)[0]), long=float(np.polyfit(ls[half:], lf[half:], 1)[0]), n=n)
def series(notes):
    """notes: [(onset twelfths, pitch, ...)]"""
    t = np.array([x[0] for x in notes]); p = np.array([x[1] for x in notes], float); ioi = np.diff(t).astype(float); ioi = np.minimum(ioi, 96)
    g0 = t.min() // 3; grid = np.zeros(int(t.max() // 3 - g0 + 1)); grid[(t // 3 - g0).astype(int)] = 1
    return {"pitch": p, "time between onsets": ioi, "onsets on the grid": grid}
def read(notes, rng):
    out = {}
    for k, x in series(notes).items():
        d = dfa(x)
        if d is None: continue
        xs = np.array(x); idx = list(range(len(xs))); rng.shuffle(idx); ds = dfa(xs[idx]); out[k] = dict(d, shuffled=ds["alpha"] if ds else None)
    return out
if __name__ == "__main__":
    import bench as B
    from scipy.stats import spearmanr, mannwhitneyu
    rng = random.Random(1); K = B.kept(); R = {}; rows = []
    for k in K: rows.append((k, read(k["notes"], rng)))
    q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]
    for s in ("pitch", "time between onsets", "onsets on the grid"):
        a = [r[s]["alpha"] for _, r in rows if s in r]; sh = [r[s]["shuffled"] for _, r in rows if s in r and r[s]["shuffled"] is not None]; gap = [abs(r[s]["long"] - r[s]["short"]) for _, r in rows if s in r]
        R[s] = dict(songs=len(a), kept_alpha=q(a), shuffled_alpha=q(sh), kept_short=q([r[s]["short"] for _, r in rows if s in r]), kept_long=q([r[s]["long"] for _, r in rows if s in r]), kept_bend=q(gap), notes_median=int(np.median([r[s]["n"] for _, r in rows if s in r])))
        G = [(k, r[s]) for k, r in rows if s in r and k["weeks"] == k["weeks"]]; al = np.array([x["alpha"] for _, x in G]); w = np.array([k["weeks"] for k, _ in G]); pk = -np.array([k["peak"] for k, _ in G])
        R[s]["grade"] = dict(songs=len(G), alpha_vs_weeks=[round(float(v), 3) for v in spearmanr(al, w)], alpha_vs_peak=[round(float(v), 3) for v in spearmanr(al, pk)], nearness_to_one_vs_weeks=[round(float(v), 3) for v in spearmanr(-np.abs(al - 1), w)], nearness_to_one_vs_peak=[round(float(v), 3) for v in spearmanr(-np.abs(al - 1), pk)])
    # damage: bars shuffled, a quarter of notes re-pitched
    sub = random.Random(2).sample(K, 60); d_sh = []; d_rp = []
    for k in sub:
        b = dfa(series(k["notes"])["pitch"]); s1 = dfa(series(B.shuffle_bars(k["notes"], rng))["pitch"]); s2 = dfa(series(B.repitch(k["notes"], 0.25, rng))["pitch"])
        if b and s1 and s2: d_sh.append(s1["alpha"] - b["alpha"]); d_rp.append(s2["alpha"] - b["alpha"])
    R["damage (pitch)"] = dict(songs=len(d_sh), bars_shuffled_change=q(d_sh), bars_shuffled_lower_share=round(float(np.mean(np.array(d_sh) < 0)), 2), quarter_repitched_change=q(d_rp), quarter_repitched_lower_share=round(float(np.mean(np.array(d_rp) < 0)), 2))
    # the engine's builds
    import metre_engine as M
    for f, name in (("/home/claude/rightrevjf/zeneng-pipeline/songs/p65/lyric55.song.json", "song 55"), ("/home/claude/rightrevjf/zeneng-pipeline/songs/p64/lyric54.song.json", "song 54")):
        rec = json.load(open(f)); E = M.Engine(rec["spec"]); r2 = random.Random(1); A = {"pitch": [], "time between onsets": [], "onsets on the grid": []}; bend = []
        n = 0
        while n < 60:
            c, err = E.build(r2)
            if err or E.gates(c): continue
            n += 1; rd = read([(x["on"], x["p"]) for x in c["notes"]], rng)
            for s in A:
                if s in rd: A[s].append(rd[s]["alpha"])
            if "pitch" in rd: bend.append(abs(rd["pitch"]["long"] - rd["pitch"]["short"]))
        R[name] = {s: q(v) for s, v in A.items()}; R[name]["pitch_bend"] = q(bend)
        kp = [r["pitch"]["alpha"] for _, r in rows if "pitch" in r]; R[name]["pitch: builds against kept (Mann-Whitney p)"] = float(mannwhitneyu(A["pitch"], kp).pvalue)
    json.dump(R, open("dfa_results.json", "w"), indent=1); print(json.dumps(R, indent=1))
