"""Run 12, the Listener's clip measures (notes only; deterministic; no fitted settings). Recipes in run12/round1_listener.md.

Sequence: C.melody(a); scale degree d = (pitch - tonic_pc) mod 12; consecutive equal pitches merged (repeat-free, as run 11's
SETTLE and the Lakh skyline events); rests ignored.
PI1C : own-clip predictive information at window 1, I(x_t ; x_t+1) plug-in (bits) minus the mean of 20 shuffles of the same
       sequence (seed from the clip's notes). The only window a ~47-note clip supports.
PIC  : corpus-trained predictive information: mean over notes t >= 3 of log2 p(d_t | d_t-2, d_t-1) - log2 p(d_t), where p is
       a Witten-Bell interpolated trigram -> bigram -> unigram (add-one) model on all Hooktheory clips with a melody, with the
       clip's whole SONG removed from the counts (leave-one-song-out; songs from C.rows(), other clips leave only themselves).
       = how much the exposure-trained ear's use of context pays on this melody. Witten-Bell has no free setting.
PIC_REL: PIC / (mean -log2 p(d_t)) : the share of the melody's surprise the context removes.
"""
import os, sys, hashlib
import numpy as np
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "run11", "experiments")))
import common11 as C

KEYS = ["PI1C", "PIC", "PIC_REL"]


def _seq(mel):
    p = mel["pitch"]; t = mel["tonic_pc"]
    s = [p[0]] + [b for a, b in zip(p, p[1:]) if b != a]
    return [(x - t) % 12 for x in s]


def _counts(s):
    c = [defaultdict(int), defaultdict(int), defaultdict(int)]
    for i, x in enumerate(s):
        c[0][(x,)] += 1
        if i >= 1: c[1][(s[i - 1], x)] += 1
        if i >= 2: c[2][(s[i - 2], s[i - 1], x)] += 1
    return c


_M = None
def _model():
    global _M
    if _M is None:
        RAW = C.C5.raw_clips(); song_of = {}
        for r in C.rows():
            for c in r["clips"]: song_of[c["k"]] = r.get("key") or r.get("song") or id(r)
        tot = [defaultdict(int) for _ in range(3)]; by_song = defaultdict(lambda: [defaultdict(int) for _ in range(3)])
        obj_song = {}
        for k in sorted(RAW):
            m = C.melody(RAW[k])
            if m is None: continue
            cs = _counts(_seq(m)); sid = song_of.get(k, ("clip", k)); obj_song[id(RAW[k])] = sid
            for o in range(3):
                for g, v in cs[o].items(): tot[o][g] += v; by_song[sid][o][g] += v
        _M = (tot, by_song, obj_song)
    return _M


def _p(x, ctx, tot, own):
    def c(o, g): return tot[o].get(g, 0) - own[o].get(g, 0)
    n0 = sum(c(0, (y,)) for y in range(12)); p = (c(0, (x,)) + 1) / (n0 + 12)
    p0 = p
    for o in (1, 2):
        h = ctx[-o:]; cnt = [c(o, h + (y,)) for y in range(12)]; n = sum(cnt); T = sum(1 for v in cnt if v > 0)
        if n > 0: p = (cnt[x] + T * p) / (n + T)
    return p, p0


def _mi1(s):
    s = np.asarray(s); a, b = s[:-1], s[1:]; n = len(a)
    j = np.bincount(a * 12 + b, minlength=144) / n; pa = np.bincount(a, minlength=12) / n; pb = np.bincount(b, minlength=12) / n
    m = j > 0
    return float((j[m] * np.log2(j[m] / np.outer(pa, pb).ravel()[m])).sum())


def clip_measure(mel, a):
    s = _seq(mel)
    if len(s) < 8: return None
    seed = int(hashlib.md5(str(mel["pitch"]).encode()).hexdigest()[:8], 16); rng = np.random.default_rng(seed)
    sh = np.mean([_mi1(list(rng.permutation(s))) for _ in range(20)])
    tot, by_song, obj_song = _model(); own = by_song[obj_song[id(a)]] if id(a) in obj_song else [{}, {}, {}]
    gain, ic0 = [], []
    for i in range(2, len(s)):
        p, p0 = _p(s[i], tuple(s[i - 2:i]), tot, own); gain.append(np.log2(p) - np.log2(p0)); ic0.append(-np.log2(p0))
    pic = float(np.mean(gain))
    return dict(PI1C=_mi1(s) - sh, PIC=pic, PIC_REL=pic / float(np.mean(ic0)))
