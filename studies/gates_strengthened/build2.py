import sys, json, pickle, re, hashlib, collections, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/zeneng/corpus/v39"); import sabc
S = pd.read_pickle("/home/claude/zeneng/corpus/v39/session.pkl"); T = json.load(open("/home/claude/corpus/thesession/json/tunes.json")); first = {}; allset = collections.defaultdict(list)
for t in T:
    allset[t["tune_id"]].append(t)
    if t["tune_id"] not in first or int(t["setting_id"]) < int(first[t["tune_id"]]["setting_id"]): first[t["tune_id"]] = t
rows = []
for r in S.itertuples():
    t = first[str(r.tune_id)]; bars, tonic, md = sabc.parse(t["abc"], t["mode"]); rows.append(dict(tune_id=int(r.tune_id), name=r.name, type=r.type, mode=t["mode"], meter=t["meter"], tonic_pc=tonic, mode_family=md, bars=[[(p, d / 2) for p, d in b] for b in bars], n=int(r.n), n_settings=int(r.settings), tunebooks=int(r.tb), recordings=int(r.rc), Gs=float(r.Gs), half=int(r.half), abc=t["abc"]))
pickle.dump([x for x in rows if x["half"] == 0], open("session_open.pkl", "wb")); pickle.dump([x for x in rows if x["half"] == 1], open("/home/claude/arena2_locked/session_locked.pkl", "wb"))
H = pd.read_pickle("/home/claude/zeneng/corpus/v40/hymn.pkl"); H["half"] = [int(hashlib.md5(str(a).encode()).hexdigest(), 16) % 2 for a in H.tuneAuthNumber]; keep = ["tuneTitle", "tuneAuthNumber", "composers", "tuneKey", "incipit", "meter", "n", "y", "minor", "length", "born", "half"]; H[H.half == 0][keep].to_pickle("hymn_open.pkl"); H[H.half == 1][keep].to_pickle("/home/claude/arena2_locked/hymn_locked.pkl")
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower().replace("&", "and")); lk = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln)
    if not r.get("melody"): continue
    top = {}
    for s in r["melody"]["sections"]:
        for n in s["notes"]:
            if "off" in n: top[round(float(n["off"]), 3)] = max(top.get(round(float(n["off"]), 3), 0), int(n["p"]))
    k = (norm(r["artist"]), norm(r["title"]))
    if len(top) >= 40 and (k not in lk or lk[k]["track_score"] < r["track_score"]): lk[k] = dict(source="lakh", artist=k[0], title=k[1], charted=bool(r.get("bb")), notes=sorted(top.items()), track_score=r["track_score"])
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); ht = [dict(source="hooktheory", artist=s["artist"], title=s["title"], charted=s.get("peak") is not None, notes=max(s["clips"], key=len)) for s in G if s["src"] == "HT" and len(max(s["clips"], key=len)) >= 40]
gate = list(lk.values()) + ht
for g in gate: g["half"] = int(hashlib.sha1(g["artist"].encode()).hexdigest(), 16) % 2
pickle.dump([g for g in gate if g["half"] == 0], open("gate_open.pkl", "wb")); pickle.dump([g for g in gate if g["half"] == 1], open("/home/claude/arena2_locked/gate_locked.pkl", "wb"))
print("session", sum(x["half"] == 0 for x in rows), sum(x["half"] == 1 for x in rows), "| hymn", int((H.half == 0).sum()), int((H.half == 1).sum()), "| gate", sum(g["half"] == 0 for g in gate), sum(g["half"] == 1 for g in gate))
