import sys, tarfile, json, pickle, numpy as np, pandas as pd
ids = set(pd.read_csv("/tmp/claude-0/hsp/msd_bb_matches.csv").msd_id); rows = []; n = 0
def flat(d):
    r = {}
    for sec in ("lowlevel", "rhythm", "tonal"):
        for k, v in d[sec].items():
            if isinstance(v, (int, float)): r[k] = float(v)
            elif isinstance(v, dict) and "mean" in v:
                if isinstance(v["mean"], (int, float)): r[k + ".mean"] = float(v["mean"]); r[k + ".var"] = float(np.log(v["var"] + 1e-12)) if isinstance(v.get("var"), (int, float)) else np.nan
                elif k in ("mfcc", "spectral_contrast_coeffs", "spectral_contrast_valleys"):
                    for i, x in enumerate(v["mean"]): r[f"{k}{i}"] = float(x)
            elif k in ("key_scale", "chords_scale"): r[k + "_minor"] = float(v == "minor")
    ap = d.get("metadata", {}).get("audio_properties", {}); r["gain"] = ap.get("replay_gain"); r["bitrate"] = ap.get("bit_rate"); r["length"] = ap.get("length"); return r
t = tarfile.open(fileobj=sys.stdin.buffer, mode="r|gz")
for m in t:
    n += 1
    if n % 100000 == 0: print(n, len(rows), flush=True)
    if not m.isfile() or not m.name.endswith(".lowlevel.json"): continue
    tid = m.name.split("/")[-1].split(".")[0]
    if tid not in ids: continue
    try: r = flat(json.load(t.extractfile(m))); r["msd_id"] = tid; rows.append(r)
    except Exception as e: pass
    if len(rows) % 500 == 0: pickle.dump(rows, open("pulled.pkl", "wb"))
pickle.dump(rows, open("pulled.pkl", "wb")); print("done", n, len(rows))
