import sys, json, pickle, re, collections, hashlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
src = open("/home/claude/zeneng/corpus/v43/transfer.py").read(); exec(src[:src.index("# hits")])
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower().replace("&", "and"))
def build(items):
    rows = []; seqs = []; meta = []
    for artist, title, charted, notes in items:
        p = [n[1] for n in notes]; t = [n[0] for n in notes]
        if len(p) < 40 or len(set(p)) < 4: continue
        d = list(np.diff(t)) + [1.0]
        if min(d) <= 0: continue
        rows.append(feats(p, d)); seqs.append(toks(p, d)); meta.append(dict(artist=artist, title=title, charted=float(charted), notes=len(p), h=int(hashlib.sha1(artist.encode()).hexdigest(), 16) % 2))
    f = pd.DataFrame(rows); m = pd.DataFrame(meta); f["ic"] = crossfit_ic(seqs, m.h.values); z = StandardScaler().fit_transform(f[F].fillna(f[F].median()).values); m["pred"] = R.predict(np.c_[z, z ** 2])
    for c in F: m["f_" + c] = f[c].fillna(f[c].median()).values
    return m
lk = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln)
    if not r.get("melody"): continue
    top = {}
    for s in r["melody"]["sections"]:
        for n in s["notes"]:
            if "off" in n: top[round(float(n["off"]), 3)] = max(top.get(round(float(n["off"]), 3), 0), int(n["p"]))
    ns = sorted(top.items()); k = (norm(r["artist"]), norm(r["title"]))
    if k not in lk or lk[k][1] < r["track_score"]: lk[k] = ((k[0], k[1], bool(r.get("bb")), ns), r["track_score"])
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); ht = [(s["artist"], s["title"], s.get("peak") is not None, max(s["clips"], key=len)) for s in G if s["src"] == "HT"]
out = {}
def fe(m, col, artist=True):
    if artist:
        g = m.groupby("artist").charted; m = m[(g.transform("min") == 0) & (g.transform("max") == 1)]
    a = pd.Categorical(m.artist).codes; X = np.c_[rankdata(m[col]), m.charted.values, rankdata(m.notes)]
    X = X - (pd.DataFrame(X).groupby(a).transform("mean").values if artist else X.mean(0)); res = lambda u: u - X[:, 2:] @ np.linalg.lstsq(X[:, 2:], u, rcond=None)[0]; x, y = res(X[:, 0]), res(X[:, 1]); r = float(np.corrcoef(x, y)[0, 1]); df = len(m) - (m.artist.nunique() if artist else 1) - 2; from scipy.stats import t as tt; p = float(2 * tt.sf(abs(r * np.sqrt(df / (1 - r * r))), df)); return r, p, len(m), int(m.artist.nunique()), int(m.charted.sum())
res = {}
for name, items in (("Lakh MIDI", [v[0] for v in lk.values()]), ("Hooktheory", ht)):
    m = build(items); res[name] = m; a = fe(m, "pred"); b = fe(m, "pred", False); out[name] = dict(within_artist=a, across=b); print(f"{name}: within artist {a[0]:+.3f} (p {a[1]:.2g}; {a[2]} songs, {a[3]} artists, {a[4]} charted) | not holding the artist {b[0]:+.3f} ({b[2]} songs)")
z = sum(np.sign(out[k]["within_artist"][0]) * Nm.isf(out[k]["within_artist"][1] / 2) * np.sqrt(out[k]["within_artist"][2]) for k in out) / np.sqrt(sum(out[k]["within_artist"][2] for k in out)); print("P pooled p", float(2 * Nm.sf(abs(z))))
print("parts within artist (Lakh, Hooktheory) and their session sign:")
for c in F:
    a, b = fe(res["Lakh MIDI"], "f_" + c), fe(res["Hooktheory"], "f_" + c); out[c] = (a[:2], b[:2]); print(f"   {c:11} {a[0]:+.3f} (p {a[1]:.2g})  {b[0]:+.3f} (p {b[1]:.2g})   session {np.sign(R.coef_[F.index(c)]):+.0f}")
json.dump(out, open("gate_results.json", "w"), indent=1, default=float)
