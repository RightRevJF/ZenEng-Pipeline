"""Notes side only: features13.base for every 4/4 Hooktheory clip of run 04's within-artist rows (no outcome read).
-> /home/claude/dl/run13/hook_feats.json {clip id: {vid, artist, half, n, f: {...}}}"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "run11", "experiments")))
import common11 as C11
import features13 as F
R = C11.rows(verbose=False); RAW = C11.C5.raw_clips(); out = {}
for r in R:
    for c in r["clips"]:
        a = RAW.get(c["k"])
        if a is None: continue
        h = F.from_hooktheory(a)
        if h is None: continue
        f = F.base(*h)
        if f is None: continue
        out[c["k"]] = dict(vid=r["vid"], artist=r["artist"], half=r["half"], n=len(F.window(h[0])), f=f)
json.dump(out, open("/home/claude/dl/run13/hook_feats.json", "w"))
print(len(out), "clips;", len({v["vid"] for v in out.values()}), "songs")
