"""Fix 739: the nineteen readings the judge does not charge (the session's reader, checked against the kept figures in luthier_v7_tables.json)."""
import numpy as np, collections, json, sys
sys.path.insert(0, "/home/claude/p58")
import luthier_judge4 as J4, luthier_judge5 as J5
NAMES = ["most-repeating window, place for its density", "least-repeating window, place for its density", "spread between windows, share of moves",
         "longest run of one pitch, notes", "bars on a rhythm already sung", "distinct rhythms over bars", "moves by step (1 or 2 semitones)",
         "moves by leap (5 semitones or more)", "turns of direction, share of moves", "range, semitones", "distinct pitches", "pitch-class entropy, bits",
         "gaps of a sixteenth or less", "gaps of an eighth", "gaps of a quarter or more", "onsets off the eighth grid", "onsets on a bar's first beat",
         "bars of one pitch (3 notes or more)", "median pitch, the two largest sections, difference"]
def song(notes):
    ns = sorted(notes, key=lambda n: n[0]); return dict(t=np.array([int(n[0]) for n in ns]), p=np.array([int(n[1]) for n in ns]), sec=np.array([J5._lab(n[2]) for n in ns]))
def read(s):
    t, p = s["t"], s["p"]; d = np.diff(p); g = np.diff(t); W = J5.windows(s); pl = [J5._place(dd, r) for _, dd, r in W]; rr = [r for _, _, r in W]
    run = m = 1
    for a in d: run = run + 1 if a == 0 else 1; m = max(m, run)
    B = J4.barlist(s); seen = set(); h = 0
    for b in B: h += b[1] in seen; seen.add(b[1])
    nz = d[d != 0]; turns = np.sum(np.sign(nz[1:]) != np.sign(nz[:-1])) / max(1, len(nz) - 1)
    pc = np.bincount(p % 12, minlength=12) / len(p); ent = float(-(pc[pc > 0] * np.log2(pc[pc > 0])).sum())
    one = [len(set(b[2])) == 1 for b in B if len(b[2]) >= 3]
    by = collections.defaultdict(list); bb = collections.defaultdict(set)
    for x, tt, sc in zip(p, t, s["sec"]): by[J4.norm(sc)].append(x); bb[J4.norm(sc)].add(int(tt) // 48)
    big = sorted(by, key=lambda k: -len(bb[k]))[:2]
    return [max(pl) if len(pl) >= 2 else np.nan, min(pl) if len(pl) >= 2 else np.nan, (max(rr) - min(rr)) if len(rr) >= 2 else np.nan, m,
            h / len(B), len(seen) / len(B), float(np.mean((np.abs(d) >= 1) & (np.abs(d) <= 2))), float(np.mean(np.abs(d) >= 5)), float(turns),
            int(p.max() - p.min()), len(set(p.tolist())), ent, float(np.mean(g <= 3)), float(np.mean((g > 3) & (g <= 6))), float(np.mean(g >= 12)),
            float(np.mean(t % 6 != 0)), float(np.mean(t % 48 == 0)), float(np.mean(one)) if one else np.nan,
            abs(float(np.median(by[big[0]])) - float(np.median(by[big[1]]))) if len(big) == 2 else np.nan]
if __name__ == "__main__":
    T = json.load(open("/home/claude/p58/tables/luthier_v7_tables.json")); K = T[[k for k in T if k.startswith("739: what")][0]]
    X = np.array([read(s) for s in J4._KEPT], float)
    for j, nm in enumerate(NAMES):
        print(f"{nm:50s} mine {np.round(np.nanpercentile(X[:, j], [25, 50, 75]), 3)}  table {K[nm]['kept 25th, 50th, 75th (raw)']}")
