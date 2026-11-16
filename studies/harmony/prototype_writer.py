"""Harmony study, part 3: can a section's chords be drawn from kept sequences and pass as kept? A prototype, not the engine.
A variable-order Markov model (orders 1-3, interpolated, Witten-Bell-style weights by context count) over each section kind's change
sequence (start and end marked), per mode, trained on 80% of the McGill songs (by song, seed 56); each change's length in beats drawn
from the kind's kept lengths. Read against the held-out 20%: first and last chord (total variation distance), distinct chords, the tonic's
share, changes a bar, out-of-key share, and the held-out log-loss per change against a unigram baseline. Writes prototype_results.json."""
import json, random, collections, math, statistics as st
from measure_billboard import S, KIND, beats, changes, IN
rng = random.Random(56); ids = sorted(so["id"] for so in S); rng.shuffle(ids); test = set(ids[: len(ids) // 5])
def seqs(split):
    D = collections.defaultdict(list)
    for so in S:
        if (so["id"] in test) != (split == "test"): continue
        for s in so["sections"]:
            k = KIND.get(s["label"]); ch = changes(beats(s))
            if k in ("verse", "chorus", "bridge", "pre") and ch: D[(k, so["mode"])].append(ch)
    return D
TR, TE = seqs("train"), seqs("test")
class VOM:
    def __init__(self, data, N=3):
        self.N = N; self.c = collections.defaultdict(collections.Counter); self.voc = set(); self.L = collections.Counter()
        for ch in data:
            s = ["<s>"] + [x for x, _ in ch] + ["</s>"]; self.voc |= set(s); self.L.update(d for _, d in ch)
            for i in range(1, len(s)):
                for n in range(0, N + 1):
                    if i - n < 0: break
                    self.c[tuple(s[i - n:i])][s[i]] += 1
    def p(self, ctx, x):
        pr = 1 / len(self.voc)
        for n in range(0, self.N + 1):
            if n > len(ctx): break
            h = tuple(ctx[len(ctx) - n:]) if n else ()
            c = self.c.get(h)
            if not c: break
            t = sum(c.values()); u = len(c); lam = t / (t + u)
            pr = lam * c[x] / t + (1 - lam) * pr
        return pr
    def draw(self, rng, cap=24):
        s = ["<s>"]
        while len(s) < cap:
            cand = [x for x in self.voc if x != "<s>"]; w = [self.p(s, x) for x in cand]
            x = rng.choices(cand, w)[0]
            if x == "</s>": break
            s.append(x)
        lens = list(self.L.elements())
        return [[x, rng.choice(lens)] for x in s[1:]]
def stats(chs, mode):
    out = collections.defaultdict(list)
    for ch in chs:
        if not ch: continue
        b = sum(d for _, d in ch) / 4; seq = [x for x, _ in ch]; tot = sum(d for _, d in ch)
        out["first"].append(seq[0]); out["last"].append(seq[-1]); out["distinct"].append(len(set(seq)))
        out["tonic"].append(sum(d for x, d in ch if x in ("I", "i")) / tot); out["cpb"].append(len(ch) / max(1, b))
        out["out"].append(sum(d for x, d in ch if x not in IN[mode]) / tot)
    return out
def tvd(a, b):
    ca, cb = collections.Counter(a), collections.Counter(b); na, nb = sum(ca.values()), sum(cb.values())
    return round(0.5 * sum(abs(ca[k] / na - cb[k] / nb) for k in set(ca) | set(cb)), 3)
res = {}
for key in sorted(TR):
    if len(TE.get(key, [])) < 15: continue
    m = VOM(TR[key]); mode = key[1]
    drawn = [m.draw(rng) for _ in range(1000)]
    uni = collections.Counter(x for ch in TR[key] for x, _ in ch); vs = list(uni); ws = [uni[v] for v in vs]
    base = [[[x, rng.choice(list(m.L.elements()))] for x in rng.choices(vs, ws, k=max(1, len(rng.choice(TR[key]))))] for _ in range(1000)]
    K, D, B = stats(TE[key], mode), stats(drawn, mode), stats(base, mode)
    ll = []; llu = []; tu = sum(uni.values())
    for ch in TE[key]:
        s = ["<s>"] + [x for x, _ in ch] + ["</s>"]
        for i in range(1, len(s)):
            ll.append(-math.log2(max(1e-9, m.p(s[:i], s[i])))); llu.append(-math.log2(max(1e-9, (uni.get(s[i], 0) + 0.5) / (tu + 0.5 * len(m.voc)))))
    med = lambda v: round(st.median(v), 3)
    res[f"{key[0]} ({mode})"] = dict(train=len(TR[key]), held_out=len(TE[key]),
        first_tvd=dict(model=tvd(D["first"], K["first"]), unigram=tvd(B["first"], K["first"])), last_tvd=dict(model=tvd(D["last"], K["last"]), unigram=tvd(B["last"], K["last"])),
        distinct=dict(kept=med(K["distinct"]), model=med(D["distinct"]), unigram=med(B["distinct"])), tonic=dict(kept=med(K["tonic"]), model=med(D["tonic"]), unigram=med(B["tonic"])),
        changes_a_bar=dict(kept=med(K["cpb"]), model=med(D["cpb"]), unigram=med(B["cpb"])), out_of_key=dict(kept=round(st.mean(K["out"]), 3), model=round(st.mean(D["out"]), 3)),
        bits_per_change=dict(model=round(st.mean(ll), 2), unigram=round(st.mean(llu), 2)),
        examples=[" ".join(x for x, _ in d) for d in drawn[:6]])
json.dump(res, open("prototype_results.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items(): print(k, {kk: vv for kk, vv in v.items() if kk != "examples"}, "\n   e.g.", v["examples"][:4])
