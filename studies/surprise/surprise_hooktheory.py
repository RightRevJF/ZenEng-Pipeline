"""Surprise against expectation on the Hooktheory clips (melody and chords, CC BY-NC-SA via Sheet Sage).

An IDyOM-style long-term model in Python: variable-order Markov chains (orders 0 to 3) blended by Witten-Bell interpolation,
trained on the other songs (5 folds by YouTube video, so a song never predicts itself). For every event it gives the information
content (IC = -log2 p, how surprising the event is) and the entropy of the prediction (H, how uncertain the moment was).
Viewpoints: melody = scale degree from the tonic with the interval from the last note (bucketed); chords = root from the tonic with
the chord's quality. Per clip: mean IC, mean H, and the Cheung et al. (2019) term, -mean(zIC * zH): high where surprises come in
certain moments and plain events in uncertain ones. Also within-clip repetition (share of 4-grams heard earlier in the clip).
Writes hooktheory_surprise.json, one record per clip."""
import gzip, json, collections, math
import numpy as np
SRC = "/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz"
IB = [(-99, -5), (-4, -3), (-2, -1), (0, 0), (1, 2), (3, 4), (5, 99)]
def ib(i): return next(k for k, (a, b) in enumerate(IB) if a <= i <= b)
def qual(iv):
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)
def tokens(clip):
    a = clip["annotations"]; tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0
    mel = []; prev = None
    for n in sorted(a.get("melody") or [], key=lambda n: n["onset"]):
        p = 12 * n["octave"] + n["pitch_class"]; sd = (n["pitch_class"] - tonic) % 12
        mel.append(sd * 7 + (ib(p - prev) if prev is not None else 3)); prev = p
    ch = []
    for c in sorted(a.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((c["root_pitch_class"] - tonic) % 12) * 9 + qual(c["root_position_intervals"])
        if not ch or ch[-1] != t: ch.append(t)
    return mel, ch
class VOM:
    def __init__(self, V, order=3):
        self.V, self.N = V, order; self.c = [collections.defaultdict(lambda: np.zeros(V, np.float32)) for _ in range(order + 1)]
    def fit(self, seqs):
        for s in seqs:
            for i, x in enumerate(s):
                for n in range(self.N + 1):
                    if i - n < 0: break
                    self.c[n][tuple(s[i - n:i])][x] += 1
        return self
    def dist(self, ctx):
        p = np.full(self.V, 1.0 / self.V)
        for n in range(self.N + 1):
            if len(ctx) < n: break
            key = tuple(ctx[len(ctx) - n:]) if n else ()
            if key not in self.c[n]: break
            cnt = self.c[n][key]; tot = cnt.sum(); types = (cnt > 0).sum()
            lam = tot / (tot + types) if tot > 0 else 0.0
            p = lam * cnt / tot + (1 - lam) * p
        return p
def score(model, s):
    ic, h = [], []
    for i, x in enumerate(s):
        p = model.dist(s[max(0, i - model.N):i])
        ic.append(-math.log2(max(p[x], 1e-12))); nz = p[p > 0]; h.append(float(-(nz * np.log2(nz)).sum()))
    return ic, h
def repetition(s, n=4):
    seen = set(); rep = 0; tot = 0
    for i in range(len(s) - n + 1):
        g = tuple(s[i:i + n]); tot += 1
        if g in seen: rep += 1
        seen.add(g)
    return rep / tot if tot else 0.0
if __name__ == "__main__":
    D = json.load(gzip.open(SRC))
    clips = []
    for k, c in D.items():
        if not c.get("youtube") or not c["youtube"].get("id"): continue
        mel, ch = tokens(c)
        if len(mel) < 12 or len(ch) < 4: continue
        clips.append(dict(k=k, vid=c["youtube"]["id"], artist=c["hooktheory"]["artist"], song=c["hooktheory"]["song"], mel=mel, ch=ch, beats=c["annotations"]["num_beats"]))
    vids = sorted({c["vid"] for c in clips}); rng = np.random.default_rng(5); fold = {v: int(rng.integers(5)) for v in vids}
    out = []
    for f in range(5):
        tr = [c for c in clips if fold[c["vid"]] != f]; te = [c for c in clips if fold[c["vid"]] == f]
        mm = VOM(84).fit([c["mel"] for c in tr]); cm = VOM(108).fit([c["ch"] for c in tr])
        for c in te:
            mi, mh = score(mm, c["mel"]); ci, chh = score(cm, c["ch"])
            out.append(dict(k=c["k"], vid=c["vid"], artist=c["artist"], song=c["song"], beats=c["beats"], n_mel=len(c["mel"]), n_ch=len(c["ch"]),
                            mel_ic=mi, mel_h=mh, ch_ic=ci, ch_h=chh, mel_rep=repetition(c["mel"]), ch_rep=repetition(c["ch"], 3)))
        print("fold", f, len(te), flush=True)
    # corpus-wide z of IC and H, then the per-clip summaries
    for v in ("mel", "ch"):
        IC = np.concatenate([o[f"{v}_ic"] for o in out]); H = np.concatenate([o[f"{v}_h"] for o in out])
        mi, si, mh, sh = IC.mean(), IC.std(), H.mean(), H.std()
        for o in out:
            ic, h = np.array(o.pop(f"{v}_ic")), np.array(o.pop(f"{v}_h"))
            o[f"{v}_ic_mean"] = float(ic.mean()); o[f"{v}_h_mean"] = float(h.mean())
            o[f"{v}_cheung"] = float(-np.mean(((ic - mi) / si) * ((h - mh) / sh)))
            o[f"{v}_ic_sd"] = float(ic.std())
    json.dump(out, open("/home/claude/shape/hooktheory_surprise.json", "w"))
    print(len(out), "clips;", len({o["vid"] for o in out}), "videos")
    for v in ("mel", "ch"): print(v, "IC mean %.2f bits, H mean %.2f bits" % (np.mean([o[f"{v}_ic_mean"] for o in out]), np.mean([o[f"{v}_h_mean"] for o in out])))
