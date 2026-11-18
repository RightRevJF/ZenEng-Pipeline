"""Fix 858: a bench for any judge, with no listeners. score_fn(notes) -> a number, HIGHER = WORSE, notes = [(onset twelfths, pitch, 'verse'|'chorus')].
  A  damage: each kept song re-pitched at random in 10, 25, 50 notes in a hundred (inside its own scale and range), its bars shuffled, and its rhythm flattened to even eighths;
     the judge should charge more for more damage.
  B  grade: across kept songs, the score against weeks on the chart and peak position (Spearman), and the top third against the bottom third (AUC)."""
import sys, json, random, numpy as np
sys.path.insert(0, "/home/claude/zeneng/corpus/nine"); import common as C
from scipy.stats import spearmanr
def kept():
    out = []
    for s, g in C.G.d.groupby("song", sort=False):
        if str(s) not in C.PT.SONGS: continue
        g = g.sort_values("abs_beat")
        if len(g) < 150: continue
        t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); p = g.pitch.values.astype(int)
        lab = ["chorus" if "horus" in str(x) else "verse" for x in g.section.values]
        keep = [i for i in range(len(t)) if i == 0 or t[i] > t[i - 1]]
        try: weeks = float(g.weeks.iloc[0]); peak = float(g.peak.iloc[0])
        except Exception: weeks = peak = float("nan")
        out.append(dict(song=str(s), notes=[(int(t[i]), int(p[i]), lab[i]) for i in keep], weeks=weeks, peak=peak, year=int(g.year.iloc[0]) if str(g.year.iloc[0]).isdigit() else None))
    return out
def repitch(notes, share, rng):
    ps = sorted({p for _, p, _ in notes}); out = []
    for t, p, l in notes: out.append((t, rng.choice(ps) if rng.random() < share else p, l))
    return out
def shuffle_bars(notes, rng):
    bars = {}
    for t, p, l in notes: bars.setdefault(t // 48, []).append((t % 48, p, l))
    keys = sorted(bars); perm = keys[:]; rng.shuffle(perm); out = []
    for k, src in zip(keys, perm):
        for x, p, l in bars[src]: out.append((k * 48 + x, p, l))
    return sorted(out)
def flatten(notes):
    out = []; t = notes[0][0] - notes[0][0] % 6
    for _, p, l in notes: out.append((t, p, l)); t += 6
    return out
def run(score_fn, name, K=None, n_damage=40, seed=1):
    K = K or kept(); rng = random.Random(seed); res = {"judge": name, "songs": len(K)}
    base = {k["song"]: score_fn(k["notes"]) for k in K}
    sub = rng.sample(K, min(n_damage, len(K))); lv = {"10": [], "25": [], "50": [], "bars shuffled": [], "rhythm flattened": []}; rho = []
    for k in sub:
        b = base[k["song"]]; sc = [b]
        for sh in (0.10, 0.25, 0.50):
            v = score_fn(repitch(k["notes"], sh, rng)); lv[str(int(sh * 100))].append(v - b); sc.append(v)
        lv["bars shuffled"].append(score_fn(shuffle_bars(k["notes"], rng)) - b); lv["rhythm flattened"].append(score_fn(flatten(k["notes"])) - b)
        rho.append(spearmanr([0, 10, 25, 50], sc).correlation)
    res["A: median rise in the score, by damage"] = {a: round(float(np.median(v)), 3) for a, v in lv.items()}; res["A: share of songs charged more, by damage"] = {a: round(float(np.mean(np.array(v) > 0)), 2) for a, v in lv.items()}
    res["A: damage against score, median Spearman within a song"] = round(float(np.nanmedian(rho)), 2); res["A: songs whose score rises at every step"] = round(float(np.mean([r > 0.99 for r in rho])), 2)
    G = [k for k in K if k["weeks"] == k["weeks"]]; s = np.array([base[k["song"]] for k in G]); w = np.array([k["weeks"] for k in G]); pk = np.array([k["peak"] for k in G])
    r1 = spearmanr(-s, w); r2 = spearmanr(-s, -pk); hi = s[w >= np.percentile(w, 67)]; lo = s[w <= np.percentile(w, 33)]; auc = float(np.mean([(a < b) + 0.5 * (a == b) for a in hi for b in lo]))
    res["B: goodness (minus the score) against weeks on the chart: Spearman, p"] = [round(float(r1.correlation), 3), round(float(r1.pvalue), 3)]; res["B: against peak position (higher is better)"] = [round(float(r2.correlation), 3), round(float(r2.pvalue), 3)]
    res["B: top third by weeks ranked over the bottom third (AUC; 0.5 is chance)"] = round(auc, 3); res["B: songs with a chart record"] = len(G)
    return res, base
if __name__ == "__main__":
    sys.path.insert(0, "/home/claude/zeneng/corpus/judge2"); import luthier_judge6 as J6
    K = kept(); out = {}
    r, b = run(lambda n: J6.score(n)["charge"], "luthier_judge6: the charge", K); out["charge"] = r; print(json.dumps(r, indent=1))
    r, b2 = run(lambda n: 1 - J6.score(n)["place among kept songs"], "luthier_judge6: one minus the place among kept songs", K); out["place"] = r; print(json.dumps(r, indent=1))
    json.dump(out, open("bench_judge6.json", "w"), indent=1)
