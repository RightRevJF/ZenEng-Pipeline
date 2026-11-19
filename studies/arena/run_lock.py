import sys, glob, pickle, importlib.util, json, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/arena"); import arena
from scipy.stats import norm as Nm
LK = "/home/claude/arena_locked/"; T = pickle.load(open(LK + "tunes_locked.pkl", "rb")); S = pd.read_pickle(LK + "sound_locked.pkl").reset_index(drop=True); Hh = pd.read_pickle(LK + "hot100_locked.pkl").reset_index(drop=True); out = []
def stouffer(R): z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); return float(z), float(2 * Nm.sf(abs(z)))
for f in sorted(glob.glob("candidates/*.py")):
    sp = importlib.util.spec_from_file_location("c", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    for c in m.CANDIDATES:
        R = {}; extra = {}
        try:
            if c["kind"] == "tune":
                for st in (1, 2, 3):
                    X = [s for s in T if s["set"] == st]; v = []
                    for s in X:
                        try: v.append(float(c["fn"](s)))
                        except Exception: v.append(np.nan)
                    v = np.array(v)
                    if np.isfinite(v).sum() >= 50:
                        for tg in ("G_rank", "love", "cover_rank"):
                            r = arena.partial(v, [s[tg] for s in X], [[s["year"] for s in X], [sum(len(k) for k in s["clips"]) for s in X]])
                            if tg == "G_rank": R[f"set{st}"] = r
                            else: extra.setdefault(tg, []).append(round(r[0], 3))
            else:
                D = S if c["kind"] == "sound" else Hh; v = np.asarray(c["fn"](D.copy()), float); groups = [(k, (D.store == k).values) for k in ("mcgill_whole_recordings", "msd_previews")] if c["kind"] == "sound" else [("hot100", np.ones(len(D), bool))]
                for k, mk in groups:
                    if np.isfinite(v[mk]).sum() >= 50:
                        for tg in ("G", "love", "cover_rank"):
                            r = arena.partial(v[mk], D[tg].values[mk], [D.year.values[mk], D.peak.values[mk]])
                            if tg == "G": R[k] = r
                            else: extra.setdefault(tg, []).append(round(r[0], 3))
        except Exception as e: out.append(dict(file=f.split("/")[-1], name=c["name"], error=str(e)[:200])); print(c["name"], "ERROR", e); continue
        z, p = stouffer(list(R.values())); ok = all(np.sign(r[0]) == c["sign"] for r in R.values()) and p < .0031
        row = dict(file=f.split("/")[-1][:-3], name=c["name"], kind=c["kind"], sign=c["sign"], scores={k: (round(r[0], 3), round(r[1], 5), r[2]) for k, r in R.items()}, pooled_p=p, love=extra.get("love"), covers=extra.get("cover_rank"), verdict="PASS" if ok else "fail"); out.append(row)
        print(f'{row["file"]:18} {row["name"]:26} sign {c["sign"]:+d}  {row["scores"]}  pooled p {p:.2g}  love {row["love"]} covers {row["covers"]}  {row["verdict"]}', flush=True)
json.dump(out, open("lock_results.json", "w"), indent=1)
