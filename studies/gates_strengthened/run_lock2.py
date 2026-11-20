import sys, pickle, importlib.util, json, re, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/arena2"); import arena2
from scipy.stats import rankdata, pearsonr
L2 = "/home/claude/arena2_locked/"; L1 = "/home/claude/arena_locked/"; out = {}
def load(name):
    sp = importlib.util.spec_from_file_location(name, f"/home/claude/arena2/candidates/{name}.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.CANDIDATES
def pooled(R): return sum(r * n for r, _, n in R.values()) / sum(n for _, _, n in R.values())
which = sys.argv[1:]
if "page" in which:
    T = pickle.load(open(L2 + "session_locked.pkl", "rb")); H = pd.read_pickle(L2 + "hymn_locked.pkl"); G = pickle.load(open(L2 + "gate_locked.pkl", "rb"))
    for c in load("page_gate"):
        if c["kind"] == "session":
            v = c["fn"]([{k: x[k] for k in x if k not in ("Gs", "tunebooks", "recordings", "n_settings", "half")} for x in T]); r = arena2.score_session(np.asarray(v, float), T)
            tb = arena2.score_session(np.asarray(v, float), [dict(x, Gs=x["tunebooks"]) for x in T]); rc = arena2.score_session(np.asarray(v, float), [dict(x, Gs=x["recordings"]) for x in T]); out[c["name"]] = dict(kind="session", score=r, tunebooks=tb[0], recordings=rc[0]); print(c["name"], "session locked:", r, "tunebooks", round(tb[0], 3), "recordings", round(rc[0], 3), flush=True)
        elif c["kind"] == "hymn":
            v = c["fn"](H.drop(columns=["n", "y", "half"])); r = arena2.score_hymns(np.asarray(v, float), H); out[c["name"]] = dict(kind="hymn", score=r); print(c["name"], "hymn locked:", r, flush=True)
        elif c["kind"] == "gate":
            v = c["fn"]([{k: x[k] for k in x if k not in ("charted", "half")} for x in G]); r = {s: arena2.score_gate(np.asarray(v, float), G, s) for s in ("lakh", "hooktheory")}; out[c["name"]] = dict(kind="gate", score=r); print(c["name"], "gate locked:", r, flush=True)
if "sound" in which:
    D = pd.read_pickle(L1 + "sound_locked.pkl").reset_index(drop=True); hand = D.drop(columns=[c for c in ("G", "love", "cover_rank", "peak", "cov0", "pop", "half", "h") if c in D.columns])
    for f in ("shell", "sound_gate", "devotion_gate"):
        for c in load(f):
            if c["kind"] != "sound": continue
            v = np.asarray(c["fn"](hand.copy()), float); R = arena2.score_sound(v, D); lo = arena2.score_sound(v, D, "love"); co = arena2.score_sound(v, D, "cover_rank"); out[c["name"]] = dict(kind="sound", file=f, stores={k: R[k] for k in R}, pooled=pooled(R), love=pooled(lo), covers=pooled(co)); print(f"{f:14} {c['name']:28} " + "  ".join(f"{k.split('_')[0]} {R[k][0]:+.3f}" for k in R) + f"  pooled {pooled(R):+.3f}  love {pooled(lo):+.3f} covers {pooled(co):+.3f}", flush=True)
if "devotion" in which:
    import pyarrow.parquet as pq
    P = "/tmp/claude-0/hspd/"; f = pq.ParquetFile(P + "hsp-l_acousticbrainz.parquet"); y = pd.read_csv(P + "hsp-l_uuid_year.csv")[["uuid", "year"]]; u = f.read(columns=["uuid", "lastfm_listener_count", "lastfm_playcount"]).to_pandas(); u = u.merge(y, on="uuid").drop_duplicates("uuid"); u = u[(u.lastfm_listener_count >= 50) & (u.lastfm_playcount > 0) & (u.year > 1900)]; u["half"] = [int(hashlib.md5(x.encode()).hexdigest(), 16) % 2 for x in u.uuid]; keep = set(u.uuid[u.half == 1])
    cols = [c for c in f.schema.names if c not in ("lastfm_listener_count", "lastfm_playcount", "peakPos", "weeks", "__index_level_0__", "msd_id", "file_hl", "file_ll", "item")]; parts = []
    for i in range(f.num_row_groups):
        t = f.read_row_group(i, columns=cols).to_pandas(); parts.append(t[t.uuid.isin(keep)])
    X = pd.concat(parts, ignore_index=True).drop_duplicates("uuid"); d = X[["uuid", "highlevel.genre_dortmund.value", "highlevel.genre_rosamerica.value"]].merge(u, on="uuid"); X = X.set_index("uuid").loc[d.uuid].reset_index()
    d["breadth"] = np.log(d.lastfm_listener_count); d["ppl"] = np.log(d.lastfm_playcount) - d.breadth; GEN = np.c_[pd.get_dummies(d["highlevel.genre_dortmund.value"]).values[:, 1:].astype(float), pd.get_dummies(d["highlevel.genre_rosamerica.value"]).values[:, 1:].astype(float)]
    for c in load("devotion_gate"):
        if c["kind"] != "devotion": continue
        v = np.asarray(c["fn"](X.copy()), float); v = np.where(np.isfinite(v), v, np.nanmedian(v)); C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.breadth), GEN]; res = lambda q: q - C @ np.linalg.lstsq(C, q, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(d.ppl))); C2 = np.c_[np.ones(len(d)), rankdata(d.year), GEN]; res2 = lambda q: q - C2 @ np.linalg.lstsq(C2, q, rcond=None)[0]; rb = pearsonr(res2(rankdata(v)), res2(rankdata(d.breadth)))[0]
        out[c["name"]] = dict(kind="devotion", score=(float(r), float(p), len(d)), with_breadth=float(rb)); print(c["name"], "devotion locked:", round(float(r), 3), "n", len(d), "| same reading against breadth", round(float(rb), 3), flush=True)
json.dump(out, open(f"lock2_{'_'.join(which)}.json", "w"), indent=1, default=float)
