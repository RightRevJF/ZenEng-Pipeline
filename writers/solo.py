"""writers/solo.py: Luthier's solo writer (a prototype for v8, built from the solos study, Part 29, the hook study, Part 30, and the
surprise rules 749.18 and 749.20). It writes the lead instrument's lines: the solo or jam, and fills in the voice's rests.

Trained on the Hooktheory clips labelled solo or instrumental (sections with 16 or more notes in major and Mixolydian keys and 4/4; Sheet Sage's release):
  pitch      a variable-order Markov model (orders 0-3, Witten-Bell) over scale degree with the bucketed interval from the last note
             (the viewpoint of the surprise study), so the line moves the way kept instrumental lines move;
  rhythm     the kept one-bar onset patterns on sixteenths, drawn by the level's target onsets a bar (kept quartiles: low level the 25th
             percentile, high the 75th);
  harmony    a note on beat 1 or 3 is a chord tone of the chord sounding at the kept rate for those beats;
  register   the line's centre climbs with the song's level (749.17's curve), inside the instrument's range.
Each eight-bar window is drawn many times and the draw kept whose cell recurrence (the hook study's measure) sits nearest the kept
solos' median and whose surprise per note is at or under the kept median (749.18); a two-bar phrase may return transposed, as kept
solos return their cells. Deterministic per seed."""
import gzip, json, collections, math, random, os
import numpy as np
SRC = "/home/claude/chrisdonahue/sheetsage-data/hooktheory/"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "solo_model.json")
IB = [(-99, -5), (-4, -3), (-2, -1), (0, 0), (1, 2), (3, 4), (5, 99)]
def ib(i): return next(k for k, (a, b) in enumerate(IB) if a <= i <= b)
def norm_section(s):
    s = (s or "").lower().strip()
    for k in ("solo", "instrumental"):
        if s.startswith(k): return k
    return None

def build_model():
    """Reads the Hooktheory clips once and keeps the counts the writer needs in solo_model.json (derived counts only)."""
    R = json.load(gzip.open(SRC + "Hooktheory_Raw.json.gz")); D = json.load(gzip.open(SRC + "Hooktheory.json.gz"))
    sec = {r["hash"]: (r.get("json_api") or {}).get("section") for r in R.values()}
    seqs, pats, onsets, ct_strong, ranges, recs = [], collections.Counter(), [], [0, 0], [], []
    for k, d in D.items():
        if norm_section(sec.get(d["hooktheory"]["id"])) is None: continue
        a = d["annotations"]; mel = sorted(a.get("melody") or [], key=lambda n: n["onset"])
        if len(mel) < 16 or not a.get("keys"): continue
        key = a["keys"][0]
        if (key.get("scale_degree_intervals") or [2, 2, 1, 2, 2, 2]) not in ([2, 2, 1, 2, 2, 2], [2, 2, 1, 2, 2, 1]): continue    # major and Mixolydian keys
        bpb = (a.get("meters") or [{"beats_per_bar": 4}])[0].get("beats_per_bar", 4)
        if bpb != 4: continue
        ton = key["tonic_pitch_class"]; harm = sorted(a.get("harmony") or [], key=lambda c: c["onset"])
        ps = [12 * n["octave"] + n["pitch_class"] for n in mel]; toks = []; prev = None
        for p in ps: toks.append(((p - ton) % 12) * 7 + (ib(p - prev) if prev is not None else 3)); prev = p
        seqs.append(toks); ranges.append(max(ps) - min(ps))
        bars = collections.defaultdict(set)
        for n in mel:
            q = int(round(n["onset"] * 4)); bars[q // 16].add(q % 16)
            if q % 8 == 0 and harm:
                c = [h for h in harm if h["onset"] <= n["onset"] + 1e-6]
                if c:
                    c = c[-1]; pcs = {(c["root_pitch_class"] + sum(c["root_position_intervals"][:j])) % 12 for j in range(len(c["root_position_intervals"]) + 1)}
                    ct_strong[0] += n["pitch_class"] in pcs; ct_strong[1] += 1
        for b, s in bars.items():
            pats["".join("x" if i in s else "." for i in range(16))] += 1; onsets.append(len(s))
        # cell recurrence, as the hook study reads it
        t = []
        for j in range(1, len(mel)):
            iv = max(-12, min(12, ps[j] - ps[j - 1])); t.append(iv)
        g = lambda n: [tuple(t[i:i + n]) for i in range(len(t) - n + 1)]
        vals = []
        for n in (3, 4, 5):
            gg = g(n)
            if gg: c_ = collections.Counter(gg); vals.append(sum(v for v in c_.values() if v > 1) / len(gg))
        recs.append(float(np.mean(vals)) if vals else 0.0)
    q = lambda v: [float(np.percentile(v, x)) for x in (25, 50, 75)]
    M = dict(clips=len(seqs), seqs=seqs, patterns=pats.most_common(400), onsets_a_bar=q(onsets), chord_tone_strong=ct_strong[0] / max(1, ct_strong[1]),
             range=q(ranges), recurrence=q(recs))
    json.dump(M, open(CACHE, "w")); return M

class VOM:
    def __init__(self, seqs, V=84, N=3):
        self.V, self.N = V, N; self.c = [collections.defaultdict(collections.Counter) for _ in range(N + 1)]
        for s in seqs:
            for i, x in enumerate(s):
                for n in range(N + 1):
                    if i - n < 0: break
                    self.c[n][tuple(s[i - n:i])][x] += 1
    def dist(self, ctx):
        p = np.full(self.V, 1.0 / self.V)
        for n in range(self.N + 1):
            if len(ctx) < n: break
            key = tuple(ctx[len(ctx) - n:]) if n else ()
            cnt = self.c[n].get(key)
            if not cnt: break
            v = np.zeros(self.V)
            for k_, c_ in cnt.items(): v[k_] = c_
            tot = v.sum(); types = (v > 0).sum(); lam = tot / (tot + types)
            p = lam * v / tot + (1 - lam) * p
        return p

class Solo:
    def __init__(self, tonic, chords, seed, lo=55, hi=86):
        self.M = json.load(open(CACHE)) if os.path.exists(CACHE) else build_model()
        self.vom = VOM(self.M["seqs"]); self.tonic = tonic; self.CH = chords; self.lo, self.hi = lo, hi
        self.rng = random.Random(f"solo {seed}"); self.pats = self.M["patterns"]
        self.ic_med = None
    def pattern(self, level):
        q = self.M["onsets_a_bar"]; lv = min(1, max(0, level))
        tgt = q[0] + (q[1] - q[0]) * lv * 2 if lv <= 0.5 else q[1] + (q[2] - q[1]) * (lv - 0.5) * 2
        near = [(p, c) for p, c in self.pats if abs(p.count("x") - tgt) <= 1.0]
        if not near: near = self.pats[:20]
        P, W = zip(*near); return self.rng.choices(P, W)[0]
    def pitch_from(self, tok, prev, centre):
        sd, b = divmod(tok, 7); pc = (self.tonic + sd) % 12; a, c = IB[b]
        cands = [p for p in range(self.lo, self.hi + 1) if p % 12 == pc]
        if prev is not None:
            inb = [p for p in cands if a <= p - prev <= c]
            if inb: cands = inb
        return min(cands, key=lambda p: (abs(p - centre) * 0.15 + (abs(p - prev) if prev is not None else 0)))
    def draw_bars(self, bars, level_at):
        """bars: list of (start tick, chord, chord2); 48 ticks a bar. Returns notes (on, dur, p) and their tokens."""
        out, toks, prev = [], [], None; ctx = []
        for j, (st, ch, ch2) in enumerate(bars):
            lv = level_at(j); pat = self.pattern(lv); centre = self.lo + (self.hi - self.lo) * (0.25 + 0.5 * lv)
            ons = [i for i, x in enumerate(pat) if x == "x"]
            for m, i in enumerate(ons):
                t = st + 3 * i; nxt = ons[m + 1] if m + 1 < len(ons) else 16; d = 3 * (nxt - i)
                chord = ch if i < 8 else ch2; pcs = self.CH[chord][1]
                p_ = self.vom.dist(ctx[-3:]).copy()
                if i % 8 == 0 and self.rng.random() < self.M["chord_tone_strong"]:            # a chord tone on beat 1 or 3 at the kept rate
                    mask = np.array([((self.tonic + k // 7) % 12) in pcs for k in range(84)]); p_ = p_ * mask
                    if p_.sum() == 0: p_ = self.vom.dist(ctx[-3:]).copy()
                tok = self.rng.choices(range(84), p_)[0]; p = self.pitch_from(tok, prev, centre)
                ctx.append(tok); toks.append(tok); prev = p; out.append((t, max(3, d - 1), p))
        return out, toks
    def ic(self, toks):
        s = 0.0
        for i, x in enumerate(toks): s += -math.log2(max(self.vom.dist(toks[max(0, i - 3):i])[x], 1e-12))
        return s / max(1, len(toks))
    def recurrence(self, notes):
        t = [max(-12, min(12, b[2] - a[2])) for a, b in zip(notes, notes[1:])]; vals = []
        for n in (3, 4, 5):
            gg = [tuple(t[i:i + n]) for i in range(len(t) - n + 1)]
            if gg: c_ = collections.Counter(gg); vals.append(sum(v for v in c_.values() if v > 1) / len(gg))
        return float(np.mean(vals)) if vals else 0.0
    def window(self, bars, level_at, tries=60):
        """the draw kept for an eight-bar window: recurrence nearest the kept median, surprise at or under the kept median; a two-bar
        phrase may return a step or a third away (the kept solos' returns)."""
        if self.ic_med is None:
            self.ic_med = float(np.median([self.ic(s[:60]) for s in self.M["seqs"][:300]]))
        rec_med = self.M["recurrence"][1]; best = None
        for k in range(tries):
            notes, toks = self.draw_bars(bars, level_at)
            if len(bars) >= 4 and self.rng.random() < 0.5:                                     # a phrase returns: bars 3-4 restate bars 1-2
                b0 = bars[0][0]; two = [n for n in notes if n[0] < b0 + 96]; shift = self.rng.choice((0, 0, 2, -2, 3, -3))
                rest = [n for n in notes if n[0] >= b0 + 192]
                notes = two + [(t + 96, d, self.fit(p + shift, bars[min(len(bars) - 1, (t + 96 - b0) // 48)])) for t, d, p in two] + rest
            ic_ = self.ic(toks); rc = self.recurrence(notes)
            sc = abs(rc - rec_med) + (max(0.0, ic_ - self.ic_med) * 0.2)
            if best is None or sc < best[0]: best = (sc, notes, dict(recurrence=round(rc, 3), ic=round(ic_, 3), kept_recurrence=round(rec_med, 3), kept_ic=round(self.ic_med, 3)))
        return best[1], best[2]
    def fit(self, p, bar):
        st, ch, ch2 = bar; scale = {(self.tonic + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}
        while p % 12 not in scale: p -= 1
        return max(self.lo, min(self.hi, p))
