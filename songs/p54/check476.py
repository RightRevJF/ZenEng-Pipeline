"""476's test: the engine's content score (zeneng_v128_judge.json, every song in its own key) on Run 2 Part 2's builds (songs/p53/part2, main runs,
every complete build), by window, beside the paper's means (zeneng_v128_judge.json's findings: verse 1 by song; the sections pooled)."""
import sys, os, json, pickle, importlib, io, contextlib, numpy as np
os.environ["ZE_PART"] = "1"; sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p54", "/home/claude/p40"]
PAPER = json.load(open("/home/claude/p54/tables/zeneng_v128_judge.json"))["findings"]
pv = PAPER["2. the builds' verse 1 and verse 2 under the refit, by song: means, difference in kept sd"]; ps = PAPER["2. sections under the refit, builds pooled (kept verse 1 mean 1.54)"]
out = {}; pool = {"Verse 1": [], "Chorus 1": [], "Verse 2": []}
for s in ("40", "42", "43", "44", "45"):
    with contextlib.redirect_stdout(io.StringIO()): P = importlib.import_module(f"melody_v128_p{s}")
    DD = [pickle.load(open(f"/home/claude/p53/part2/melody_v127_p{s}_main.pkl", "rb"))]; r = {}
    for sec in ("Verse 1", "Verse 2", "Chorus 1"):
        if sec not in P.BAR0: continue
        v = []
        for c in [c_ for D in DD for c_ in D["every"]]:
            if c.get("partial"): continue
            ns = [dict(on=o, dur=d, p=p, sec=x, line=l) for o, d, p, x, l, st, sy in c["notes"]]
            N = P.win_N(ns, P.BAR0[sec]); f = P.feats(N, P.mton())
            if f: v.append(P.refit_score(f, N))
        r[sec] = round(float(np.mean(v)), 3); pool[sec] += v
    out[s] = dict(engine=r, paper_verse1_verse2=pv[s][:2], verse1_within_0_05=abs(r["Verse 1"] - pv[s][0]) <= 0.05)
    print(s, out[s])
out["pooled"] = {k: (round(float(np.mean(v)), 3), ps.get(k)) for k, v in pool.items() if v}
print(out["pooled"]); json.dump(out, open("/home/claude/p54/check476.json", "w"), indent=1)
