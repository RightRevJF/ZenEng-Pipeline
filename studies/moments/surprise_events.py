"""Per-event surprise for the Hooktheory clips that are aligned to their video (beat times): for each melody note its beat, pitch,
IC and H; for each chord change its beat, IC and H; cross-fitted by video as in surprise_hooktheory.py. Writes clip_events.json."""
import gzip, json, sys
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH
D = json.load(gzip.open(SH.SRC)); clips = []
for k, c in D.items():
    yt = c.get("youtube") or {}
    if not yt.get("id"): continue
    al = (c.get("alignment") or {}).get("refined") or (c.get("alignment") or {}).get("user")
    if not al or len(al.get("beats", [])) < 2: continue
    a = c["annotations"]; tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0
    mel = sorted(a.get("melody") or [], key=lambda n: n["onset"]); ch = sorted(a.get("harmony") or [], key=lambda x: x["onset"])
    mt, ct = SH.tokens(c)
    if len(mt) < 12 or len(ct) < 4: continue
    chb = []; prev = None
    for x in ch:
        t = ((x["root_pitch_class"] - tonic) % 12) * 9 + SH.qual(x["root_position_intervals"])
        if t != prev: chb.append(x["onset"])
        prev = t
    clips.append(dict(k=k, vid=yt["id"], mt=mt, ct=ct, mel=[(n["onset"], n["offset"], 12 * n["octave"] + n["pitch_class"]) for n in mel], chb=chb,
                      beats=al["beats"], times=al["times"], nb=a["num_beats"], key_changes=len(a.get("keys") or []) > 1))
vids = sorted({c["vid"] for c in clips}); rng = np.random.default_rng(5); fold = {v: int(rng.integers(5)) for v in vids}
out = {}
for f in range(5):
    tr = [c for c in clips if fold[c["vid"]] != f]; te = [c for c in clips if fold[c["vid"]] == f]
    mm = SH.VOM(84).fit([c["mt"] for c in tr]); cm = SH.VOM(108).fit([c["ct"] for c in tr])
    for c in te:
        mi, mh = SH.score(mm, c["mt"]); ci, chh = SH.score(cm, c["ct"])
        out[c["k"]] = dict(vid=c["vid"], beats=c["beats"], times=c["times"], nb=c["nb"], key_changes=c["key_changes"],
                           mel=[(o, e, p, round(i, 3), round(h, 3)) for (o, e, p), i, h in zip(c["mel"], mi, mh)],
                           ch=[(b, round(i, 3), round(h, 3)) for b, i, h in zip(c["chb"], ci, chh)])
    print("fold", f, flush=True)
json.dump(out, open("/home/claude/shape/clip_events.json", "w"))
print(len(out), "aligned clips")
