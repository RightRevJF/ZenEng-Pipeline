"""Luthier v13, stage 4 (Module 27.94; fixes 800-806): the chord writer.

The engine writes the chords. For each section of a form it takes
  800  the section's STRUCTURE from one kept section of that kind, whole: which bars repeat which (a b a b a b c d), nothing of its chords;
       and its CONTENT, bar by bar, from the kept bars of that kind and mode given the two bars before (a bar is one to four chords);
       a new bar looks one bar ahead when the next bar is a repeat, and the last bar is weighed by how kept sections of the kind end.
       Each section is one draw, not the likeliest of many: the writer is tested by whether its sections read as kept ones on songs held out.
  801  a returning section keeps its first's chords bar for bar; a longer return keeps them and draws its added bars.
  802  the join: a section's first bar is weighed by what kept songs play after the section before's last chord.
  803  the metre: a bar's chords fall on the metre's beats (one chord the bar, two the halves or the strong beats); nothing here names 4/4.
  804  the key (choose_key): the tonic that puts the melody inside the voice, then the lead instrument's kept keys.
  805  the chromatic setting: 0 writes inside the key, 1 at the kept rate, more leans out; a chord can be required.

    from chord_writer import Writer, choose_key
    W = Writer(mode="major"); plan = W.song([("Verse 1", "verse", 8), ("Chorus 1", "chorus", 8), ...], seed=1)
    python3 lib/luthier/chord_writer.py            # the held-out test: writes stage4_results.json

Data: McGill Billboard, 739 songs 1958-1991, CC0 (studies/harmony/billboard_sections.json). Deterministic for a seed."""
import json, random, collections, math, os, re, sys, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "..", "studies", "harmony", "billboard_sections.json")
KIND = {"verse": "verse", "chorus": "chorus", "refrain": "chorus", "bridge": "bridge", "pre-chorus": "pre", "prechorus": "pre", "pre chorus": "pre", "intro": "intro",
        "outro": "outro", "fadeout": "outro", "coda": "outro", "solo": "solo", "instrumental": "solo", "interlude": "solo"}
IN = {"major": {"I", "ii", "iii", "IV", "V", "vi", "viio"}, "minor": {"i", "iio", "bIII", "iv", "v", "bVI", "bVII", "V"}}
NAMES_S = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]; NAMES_F = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
DEG = {"I": 0, "II": 2, "III": 4, "IV": 5, "V": 7, "VI": 9, "VII": 11}; FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db", "Gb"}

CHROMATIC_BASE = {"major": 1.0, "minor": 1.0}
# 823 (749.51): kept songs differ in how far they leave the key (half of them hardly at all), so a song draws its own share from the kept songs of its mode,
# and the weight that gives that share is read from this table (the weight, and the mean share of bars from outside the key it gave over 60 written songs).
CHROMATIC_MAP = {"major": [(0, 0.0), (0.25, 0.074), (0.5, 0.11), (1, 0.171), (2, 0.252), (4, 0.39), (8, 0.434), (16, 0.553)],
                 "minor": [(0, 0.0), (0.25, 0.061), (0.5, 0.13), (1, 0.213), (2, 0.312), (4, 0.412), (8, 0.52), (16, 0.642)]}
def weight_for(share, mode):
    M_ = CHROMATIC_MAP[mode]
    for (c0, s0), (c1, s1) in zip(M_, M_[1:]):
        if share <= s1: return c0 + (c1 - c0) * (share - s0) / max(1e-9, s1 - s0)
    return M_[-1][0]
def norm(rn): return None if rn is None else re.sub(r"(5|sus\d?|add\d+|\+)$", "", rn)      # voicing marks folded into the chord; the band adds them back
def bars_of(sec):
    out = []
    for b in sec["bars"]:
        t = []
        for x in b["rn"]:
            x = norm(x)
            if x is not None and (not t or t[-1] != x): t.append(x)
        out.append(tuple(t))
    return out
def pattern(bars):
    seen = {}; return [seen.setdefault(b, len(seen)) for b in bars]
def sections(songs, mode=None):
    """(kind, bars, song index, place in the song) for every usable kept section"""
    out = []
    for si, so in enumerate(songs):
        if mode and so["mode"] != mode: continue
        for j, s in enumerate(so["sections"]):
            k = KIND.get(s["label"]); b = bars_of(s)
            if k and len(b) >= 2 and all(1 <= len(x) <= 4 for x in b): out.append((k, b, si, j))
    return out

def chord_repetition(bars):
    """the share of a section's chord 3-grams already heard earlier in it (a chord repeating the one before merged; None under four chords): the covers study's measure"""
    seq = []
    for t in bars:
        for x in t:
            if not seq or seq[-1] != x: seq.append(x)
    if len(seq) < 4: return None
    seen = set(); r = 0; n = len(seq) - 2
    for i in range(n): g = tuple(seq[i:i + 3]); r += g in seen; seen.add(g)
    return r / n
class VOM:
    """bars given the two bars before, Witten-Bell interpolated"""
    def __init__(self, seqs, new_only=False):
        self.c = collections.defaultdict(collections.Counter); self.voc = set()
        for s in seqs:
            s = ["<s>"] + list(s) + ["</s>"]; self.voc |= set(s)
            for i in range(1, len(s)):
                if new_only and s[i] != "</s>" and (s[i] in s[1:i] or (s.count(s[i]) > 1) != (new_only == "returns")): continue   # only bars new where they stand, that return later or that do not
                for n in range(0, 3):
                    if i - n < 0: break
                    self.c[tuple(s[i - n:i])][s[i]] += 1
        self.toks = sorted((x for x in self.voc if x not in ("<s>", "</s>")), key=str)
    def p(self, ctx, x):
        pr = 1 / max(1, len(self.voc))
        for n in range(0, 3):
            if n > len(ctx): break
            c = self.c.get(tuple(ctx[len(ctx) - n:]) if n else ())
            if not c: break
            t = sum(c.values()); lam = t / (t + len(c)); pr = lam * c[x] / t + (1 - lam) * pr
        return pr

class Writer:
    def __init__(self, mode="major", songs=None, chromatic=1.0):
        songs = songs if songs is not None else json.load(open(DATA)); self.mode = mode; self.chromatic = chromatic * CHROMATIC_BASE[mode]
        S = sections(songs, mode); allS = sections(songs); self.kinds = sorted({k for k, _, _, _ in S})
        self.vom = {k: VOM([b for kk, b, _, _ in S if kk == k]) for k in self.kinds}; self.new = {(k, r): VOM([b for kk, b, _, _ in S if kk == k], r) for k in self.kinds for r in ("returns", "once")}
        self.tmpl = {}
        for k in self.kinds:
            own = [pattern(b) for kk, b, _, _ in S if kk == k]; self.tmpl[k] = own if len(own) >= 30 else [pattern(b) for kk, b, _, _ in allS if kk == k]   # few sections in this mode: structures from both
        self.loop_less = False; self.rep_median = {}                                           # 960 (749.159): a setting. Each kind's kept median of chord repetition within a section, for the gate in section()
        for k in ("verse", "bridge"):
            src_ = [b for kk, b, _, _ in S if kk == k]; src_ = src_ if len(src_) >= 30 else [b for kk, b, _, _ in allS if kk == k]; v_ = [r for r in (chord_repetition(b) for b in src_) if r is not None]
            if v_: self.rep_median[k] = st.median(v_)
        self.setting = chromatic; self.kept_out = []
        for si in sorted({x[2] for x in S}):
            bars = [t for k, b, i, _ in S if i == si and k in ("verse", "chorus", "bridge", "pre") for t in b]
            if bars: self.kept_out.append(sum(1 / len(t) for t in bars for x in t if x not in IN[mode]) / len(bars))
        last_of = {}
        for k, b, si, j in S:
            if k in ("verse", "chorus", "bridge", "pre") and j >= last_of.get(si, (-1,))[0]: last_of[si] = (j, b[-1][-1])
        self.songend = collections.Counter(c for _, c in last_of.values()); self.kindend = {k: collections.Counter(b[-1][-1] for kk, b, _, _ in S if kk == k) for k in self.kinds}   # 822 (749.50): how kept songs end
        self.first = {k: collections.Counter(b[0][0] for kk, b, _, _ in S if kk == k) for k in self.kinds}
        self.join = collections.defaultdict(collections.Counter); by = collections.defaultdict(dict)
        for k, b, si, j in S: by[si][j] = (k, b)
        for si, d in by.items():
            for j, (k, b) in d.items():
                if j + 1 in d: k2, b2 = d[j + 1]; self.join[(k, k2, b[-1][-1])][b2[0][0]] += 1
        R = collections.defaultdict(list)                                                    # 809: the kept songs' readings of a whole song's chords, for the pick among drafts
        for si in {x[2] for x in S}:
            for q, v in self.readings([b for _, b, i, _ in S if i == si]).items(): R[q].append(v)
        self.Q = {q: [sorted(v)[int(len(v) * x)] for x in (0.25, 0.5, 0.75)] for q, v in R.items()}
    def readings(self, secs):
        bars = [t for b in secs for t in b]; flat = [x for t in bars for x in t]; n = len(bars); tonic = "I" if self.mode == "major" else "i"
        return {"tonic's share of the bars": sum(1 / len(t) for t in bars for x in t if x == tonic) / n, "distinct chords": len(set(flat)), "chord changes a bar": (sum(1 for a, c in zip(flat, flat[1:]) if a != c) + 1) / n,
                "share from outside the key": sum(1 / len(t) for t in bars for x in t if x not in IN[self.mode]) / n, "distinct bars over bars": len(set(bars)) / n,
                "sections opening on the tonic": sum(b[0][0] == tonic for b in secs) / len(secs)}
    def charge(self, secs):
        r = self.readings(secs); c = d = 0.0
        for q, (a, m, z) in self.Q.items():
            sp = (z - a) or (0.02 if m <= 1.5 else 1.0); d += abs(r[q] - m) / sp; c += max(0.0, a - r[q]) / sp + max(0.0, r[q] - z) / sp
        return c, d, r
    def out_of_key(self, tok): return any(x not in IN[self.mode] for x in tok)
    def template(self, rng, k, n):
        T = self.tmpl[k]; L = sorted({len(t) for t in T}, key=lambda x: (abs(x - n), x)); near = [t for t in T if len(t) == L[0]]; t = rng.choice(near)
        if len(t) >= n: return pattern(t[:n])
        return pattern([t[i % len(t)] for i in range(n)])                                    # a shorter kept section's structure, sung round again
    def section(self, rng, k, n, prev=None, require=None, given=None, final=False, home=None):
        """960 (749.159), where a lyric asks ("chords": "loop_less"): a verse or bridge is drawn again, 30 times at most, until its chord repetition (the share of its
        chord 3-grams already heard in it) is at or under the kept median for its kind; the least-looping draw where none is. Not a default: it did not pass its third
        check and has met no hold-out (studies/proposed_v47)."""
        if not self.loop_less or k not in self.rep_median or given: return self.section1(rng, k, n, prev, require, given, final, home)
        best = None
        for _ in range(30):
            b = self.section1(rng, k, n, prev, require, given, final, home); r = chord_repetition(b); r = 0.0 if r is None else r
            if r <= self.rep_median[k]: return b
            if best is None or r < best[0]: best = (r, b)
        return best[1]
    def section1(self, rng, k, n, prev=None, require=None, given=None, final=False, home=None):
        """one section of n bars; prev = (kind before, its last chord); given = bars already fixed (a return's prefix)"""
        V = self.vom[k]
        for _ in range(200):
            pat = self.template(rng, k, n) if not given else None; bars = list(given or []); lab = {}
            E_ = self.songend if final else self.kindend[k]; cstar = rng.choices(sorted(E_), [E_[c] for c in sorted(E_)])[0]
            if home is not None and rng.random() < home: cstar = "I" if self.mode == "major" else "i"                                  # 825: a song that ends cold ends on the tonic 81 times in a hundred             # 822: the section's last chord, drawn as kept sections (or kept songs) end
            if given: pat = pattern(list(given)) + [max(pattern(list(given))) + 1 + i for i in range(n - len(given))]
            for i in range(len(bars)): lab[pat[i]] = bars[i]
            for i in range(len(bars), n):
                if pat[i] in lab: bars.append(lab[pat[i]]); continue
                ctx = (["<s>"] + bars)[-2:]; used = set(lab.values()); cands = [t for t in V.toks if t not in used]; ws = []
                if pat[i] == pat[n - 1] and any(t[-1] == cstar for t in cands): cands = [t for t in cands if t[-1] == cstar]
                for t in cands:
                    w = self.new[(k, 'returns' if pat.count(pat[i]) > 1 else 'once')].p(ctx, t)                                                       # a new bar, given the two before: from kept bars that were new where they stood
                    if self.out_of_key(t): w *= max(self.chromatic, 0.5) if (require and require in t) else self.chromatic      # a required chord is not shut out by the song's own share
                    if i + 1 < n and pat[i + 1] in lab: w *= V.p((ctx + [t])[-2:], lab[pat[i + 1]]) / max(1e-9, V.p((), lab[pat[i + 1]]))      # looks ahead to the bar that returns
                    if i == n - 1: w *= V.p((ctx + [t])[-2:], "</s>") / max(1e-9, V.p((), "</s>"))                                            # how sections of this kind end
                    elif pat[i] == pat[n - 1]: w *= V.p([t], "</s>") / max(1e-9, V.p((), "</s>"))                                             # this bar will return as the section's last
                    if i == 0 and prev is not None:
                        J = self.join.get((prev[0], k, prev[1])); F = self.first[k]; pf = (F[t[0]] + 0.5) / (sum(F.values()) + 0.5 * len(F))
                        if J: w *= ((J[t[0]] + 5 * pf) / (sum(J.values()) + 5)) / pf                                                          # 802
                    ws.append(w)
                if sum(ws) <= 0: break
                t = rng.choices(cands, ws)[0]; lab[pat[i]] = t; bars.append(t)
            if len(bars) == n and (not require or any(require in b for b in bars)): return bars
        raise RuntimeError(f"no {k} of {n} bars")
    def song(self, form, seed=0, require=None):
        """form: [(name, kind, bars)]. A name's trailing number marks a return: 'Verse 2' returns 'Verse 1' (801). require: a chord some section must carry (805)."""
        rng = random.Random(seed); plan = {}; firsts = {}; prev = None
        self.chromatic = weight_for(rng.choice(self.kept_out) * self.setting, self.mode) if self.setting > 0 else 0.0           # 823: this song's own share from outside the key
        need = require; kinds = [k for _, k, _ in form]
        if require:                                                                           # the required chord goes where kept songs most often play it
            share = {k: sum(c[t] for ctx, c in self.vom[k].c.items() if ctx == () for t in c if t not in ("</s>",) and require in t) / max(1, sum(self.vom[k].c[()].values())) for k in set(kinds) if k in self.vom}
            where = max(sorted(share), key=lambda k: share[k])
        lastsung = max((i for i, (_, k, _) in enumerate(form) if k in ("verse", "chorus", "bridge", "pre")), default=-1)
        for fi, (name, k, n) in enumerate(form):
            k = k if k in self.vom else "verse"; base = re.sub(r"\s*\d+$", "", name); src = firsts.get(base); fin = fi == lastsung
            if src is not None: bars = list(src[:n]) if n <= len(src) else self.section(rng, k, n, prev, given=src, final=fin)
            else: bars = self.section(rng, k, n, prev, require=need if (need and k == where) else None, final=fin, home=0.81 if (fi == len(form) - 1 and k == "outro") else None); firsts[base] = bars; need = None if (need and k == where) else need
            plan[name] = bars; prev = (k, bars[-1][-1])
        return plan

def name(rn, tonic):
    m = re.match(r"(b|#)?(VII|III|IV|VI|II|V|I|vii|iii|iv|vi|ii|v|i)(o)?$", rn)
    if not m: return rn
    acc, r, dim = m.groups(); minor = tonic.endswith("m"); t = tonic[:-1] if minor else tonic; root = NAMES_S.index(t) if t in NAMES_S else NAMES_F.index(t)
    pc = (root + DEG[r.upper()] + (-1 if acc == "b" else 1 if acc == "#" else 0)) % 12; rel = (root + 3) % 12 if minor else root                  # 821 (749.52): a key's chords are spelled from its signature,
    flat = "b" in t or (t in ("D", "G", "C", "F") if minor else t == "F"); scale = {(rel + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}                                                  # a minor key's from its relative major's
    nm = (NAMES_F if flat else NAMES_S)[pc] if pc in scale else NAMES_S[pc] if len(NAMES_S[pc]) == 1 else (NAMES_F if (acc == "b" or flat) else NAMES_S)[pc]
    return nm + ("dim" if dim else "m" if r.islower() else "")
MAJOR_TONICS = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]; MINOR_TONICS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
def tonic_name(pc, mode="major"): return MAJOR_TONICS[pc % 12] if mode == "major" else MINOR_TONICS[pc % 12] + "m"
def tones(rn):
    """pitch classes above the tonic"""
    m = re.match(r"(b|#)?(VII|III|IV|VI|II|V|I|vii|iii|iv|vi|ii|v|i)(o)?$", rn); acc, r, dim = m.groups(); root = (DEG[r.upper()] + (-1 if acc == "b" else 1 if acc == "#" else 0)) % 12
    third = 3 if (r.islower() or dim) else 4; fifth = 6 if dim else 7; return sorted({root, (root + third) % 12, (root + fifth) % 12})
def place(bar, barlen, beats):
    """803: where a bar's chords begin, in twelfths: one chord the bar; two the halves (the mid-bar beat, or the last beat where the bar has three); more, beat by beat"""
    n = len(bar)
    if n == 1: return [0]
    if n == 2: return [0, barlen // 2 if barlen // 2 in beats else beats[-1]]
    b = list(beats) if len(beats) >= n else [round(i * barlen / n / 3) * 3 for i in range(n)]
    return ([0] + b[len(b) - n + 1:]) if len(b) >= n else b

VOICES = {"bass": (40, 60), "baritone": (43, 64), "tenor": (48, 69), "alto": (55, 74), "mezzo": (57, 77), "soprano": (60, 81)}       # comfortable sung range, MIDI
OPEN = {"major": ["G", "D", "A", "E", "C"], "minor": ["E", "A", "D", "B"]}                                                         # open-string guitar keys
def choose_key(low, high, voice="tenor", lead="guitar", mode="major", centre=None):
    """804. low, high: the melody's lowest and highest note in semitones above the tonic it was written on. Returns the ranked keys: those that put the whole melody
    inside the voice, nearest its middle first, the lead instrument's kept keys before the others (guitar: open-string keys, 65% of kept guitar songs; piano, strings,
    synthesizer: flat keys twice as often as guitar songs). A key that needs a capo for an open shape says so."""
    lo, hi = VOICES[voice]; out = []
    for pc in range(12):
        for octv in range(2, 7):
            t = 12 * octv + pc
            if t + low >= lo and t + high <= hi:
                nm = (MAJOR_TONICS if mode == "major" else MINOR_TONICS)[pc]; mid = abs((t + centre) - (lo + hi) / 2) if centre is not None else abs((t + low + t + high) / 2 - (lo + hi) / 2)      # 907 (749.84): with a centre given (the verse's median note), it is the verse that sits near the voice's middle, not the span's midpoint
                if lead == "guitar": fam = 0 if nm in OPEN[mode] else 1; capo = None if fam == 0 else min(((pc - NAMES_S.index(o)) % 12, o) for o in OPEN[mode])
                else: fam = 0 if ((NAMES_F[(pc + 3) % 12] if mode == "minor" else nm) in FLAT_KEYS or (nm == "C" and mode == "major") or (nm == "A" and mode == "minor")) else 1; capo = None
                out.append(dict(key=nm + ("m" if mode == "minor" else ""), tonic_midi=t, lowest=t + low, highest=t + high, from_middle=mid, instrument_key=fam == 0, capo=(f"capo {capo[0]}, {capo[1]} shapes" if capo and capo[0] <= 5 else None)))
    out.sort(key=lambda d: ((d["from_middle"] > 3) if centre is not None else False, not d["instrument_key"], d["from_middle"], d["key"])); return out      # 907: the instrument's keys first among the keys that put the verse within three semitones of the voice's middle

# ---- the held-out test
def tv(a, b):
    ta, tb = sum(a.values()), sum(b.values()); return 0.5 * sum(abs(a[k] / ta - b[k] / tb) for k in set(a) | set(b))
def measures(secs, mode):
    out = {}
    for k in sorted({x[0] for x in secs}):
        v = [b for kk, b in secs if kk == k]; flat = [[x for t in b for x in t] for b in v]
        def changes(b):
            s = [x for t in b for x in t]; return sum(1 for a, c in zip(s, s[1:]) if a != c) + 1
        def per(b):
            for p in (1, 2, 4, 8):
                if len(b) >= 2 * p and sum(b[i] == b[i + p] for i in range(len(b) - p)) >= 0.9 * (len(b) - p): return p
        out[k] = dict(n=len(v), first=collections.Counter(b[0][0] for b in v), last=collections.Counter(b[-1][-1] for b in v), chords=collections.Counter(x for f in flat for x in f),
                      bigrams=collections.Counter(p for f in flat for p in zip(f, f[1:]) if p[0] != p[1]), bars=collections.Counter(t for b in v for t in b),
                      distinct=st.median(len(set(f)) for f in flat), tonic=st.median(sum(1 / len(t) for t in b for x in t if x in ("I", "i")) / len(b) for b in v),
                      cpb=st.median(changes(b) / len(b) for b in v), out=st.mean(sum(1 / len(t) for t in b for x in t if x not in IN[mode]) / len(b) for b in v),
                      loops=sum(per(b) is not None for b in v) / len(v), distinct_bars=st.median(len(set(b)) / len(b) for b in v), any_out=sum(any(x not in IN[mode] for x in f) for f in flat) / len(v))
    return out
def compare(K, W):
    r = {}
    for k in K:
        if k not in W: continue
        a, b = K[k], W[k]; r[k] = dict(n=a["n"], **{m: round(tv(a[m], b[m]), 3) for m in ("first", "last", "chords", "bigrams", "bars")}, **{m: [round(a[m], 3), round(b[m], 3)] for m in ("distinct", "tonic", "cpb", "out", "any_out", "loops", "distinct_bars")})
    return r
if __name__ == "__main__":
    ALL = json.load(open(DATA)); res = {}; KS = ("verse", "chorus", "bridge", "pre")
    for mode in ("major", "minor"):
        songs = [s for s in ALL if s["mode"] == mode]; random.Random(56).shuffle(songs); cut = int(0.8 * len(songs)); tr, te = songs[:cut], songs[cut:]
        W = Writer(mode, tr); held = [(k, b) for k, b, _, _ in sections(te) if k in KS]; train = [(k, b) for k, b, _, _ in sections(tr) if k in KS]; rng = random.Random(1)
        wrote = [(k, W.section(rng, k, len(b))) for k, b in held]
        res[mode] = dict(written=compare(measures(held, mode), measures(wrote, mode)), floor=compare(measures(held, mode), measures(train, mode)))
        # the joins: written songs on the held-out songs' own forms
        J = collections.Counter(); JK = collections.Counter(); JF = collections.Counter()
        for si, so in enumerate(te):
            secs = [(KIND.get(s["label"]), bars_of(s)) for s in so["sections"]]; secs = [(k, b) for k, b in secs if k in W.vom and len(b) >= 2 and all(1 <= len(x) <= 4 for x in b)]
            if len(secs) < 2: continue
            plan = W.song([(f"{k} {i}x", k, len(b)) for i, (k, b) in enumerate(secs)], seed=si); pl = list(plan.values())
            for (k1, b1), (k2, b2), w1, w2 in zip(secs, secs[1:], pl, pl[1:]): JK[(b1[-1][-1], b2[0][0])] += 1; J[(w1[-1][-1], w2[0][0])] += 1
        for s in tr:
            secs = [bars_of(x) for x in s["sections"] if KIND.get(x["label"]) in W.vom]; secs = [b for b in secs if len(b) >= 2 and all(1 <= len(x) <= 4 for x in b)]
            for b1, b2 in zip(secs, secs[1:]): JF[(b1[-1][-1], b2[0][0])] += 1
        res[mode]["joins"] = dict(written=round(tv(JK, J), 3), floor=round(tv(JK, JF), 3), kept_top=JK.most_common(4), written_top=J.most_common(4))
        for k in KS:
            if k in res[mode]["written"]: print(mode, k, res[mode]["written"][k]); print("     floor", {m: res[mode]["floor"][k][m] for m in ("first", "last", "chords", "bigrams", "bars")})
        print(mode, "joins", res[mode]["joins"])
    path = os.path.join(HERE, "stage4_results.json"); old = json.load(open(path)) if os.path.exists(path) else {}; old.update(json.loads(json.dumps(res, default=str)))      # 824 (749.49): the test rewrites its own keys only
    json.dump(old, open(path, "w"), indent=1, default=str)
