"""writers/chords.py: Luthier's chord writer (a prototype for v8, built from the harmony study, Part 18).

The engine writes the chords; nobody chooses them by hand. For each section of a song's form it draws candidate chord plans from a
variable-order Markov model (orders 0-3, interpolated, Witten-Bell weights) trained on the McGill Billboard sections of that kind
and mode (studies/harmony/billboard_sections.json, 739 songs 1958-1991), weighted toward the song's era, then keeps the candidate that
best fits the kept figures for that kind (interquartile ranges of distinct chords, tonic share, changes a bar and out-of-key share; the
kept first and last chords; a loop period kept sections use), with the musician channel's preference for harmony that moves (749.22:
changes a bar at or above the kept median) and the writer's style choice (for example a required bVII, the key question's answer).
Every choice is deterministic for a seed, and the scores of the top candidates are returned for the test report.

    from writers.chords import write_song
    plan, report = write_song(form, mode="major", tonic="E", era=(1965, 1979), require={"bVII"}, seed=...)

form: a list of (name, kind, bars), kind one of intro, verse, chorus, bridge, solo, outro, pre. Sections with the same name share
one plan (a second verse keeps the first's chords, as most kept songs do: returns_keep_chords in billboard_tables.json)."""
import json, random, collections, math, statistics as st, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "studies", "harmony", "billboard_sections.json")
KIND = {"verse": "verse", "chorus": "chorus", "refrain": "chorus", "bridge": "bridge", "pre-chorus": "pre", "prechorus": "pre",
        "pre chorus": "pre", "intro": "intro", "outro": "outro", "fadeout": "outro", "coda": "outro", "solo": "solo",
        "instrumental": "solo", "interlude": "solo"}
IN = {"major": {"I", "ii", "iii", "IV", "V", "vi", "viio"}, "minor": {"i", "iio", "bIII", "iv", "v", "bVI", "bVII", "V"}}
SHARP_KEYS = {"G", "D", "A", "E", "B", "F#", "C#"}
NAMES_S = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NAMES_F = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
DEG = {"I": 0, "II": 2, "III": 4, "IV": 5, "V": 7, "VI": 9, "VII": 11}

def norm(rn):
    """Fold voicing marks into the chord: I5 -> I, Vsus -> V (the sus is a voicing the band writer may add back)."""
    if rn is None: return None
    return re.sub(r"(5|sus\d?|add\d+|\+)$", "", rn)

def beats(sec):
    out = []
    for b in sec["bars"]:
        rn = [norm(x) for x in b["rn"]]; n = len(rn); per = 4 // n if n in (1, 2, 4) else None
        if per is None: out += rn; continue
        for x in rn: out += [x] * per
    return out

def changes(bts):
    ch = []
    for x in bts:
        if x is None: continue
        if ch and ch[-1][0] == x: ch[-1][1] += 1
        else: ch.append([x, 1])
    return ch

def period(bars):
    n = len(bars)
    for p in (1, 2, 4, 8):
        if n >= 2 * p and sum(bars[i] == bars[i + p] for i in range(n - p)) >= 0.9 * (n - p): return p
    return None

def to_bars(ch, nbars):
    """Change list (chord, beats) -> per-bar tuples of chords (4/4)."""
    bts = [x for x, d in ch for _ in range(d)][: 4 * nbars]
    return [tuple(dict.fromkeys(bts[4 * i: 4 * i + 4])) for i in range(nbars)]

class VOM:
    def __init__(self, data, N=3):
        self.N = N; self.c = collections.defaultdict(collections.Counter); self.voc = set()
        for ch, w in data:
            s = ["<s>"] + [x for x, _ in ch] + ["</s>"]; self.voc |= set(s)
            for i in range(1, len(s)):
                for n in range(0, N + 1):
                    if i - n < 0: break
                    self.c[tuple(s[i - n:i])][s[i]] += w
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
    def draw(self, rng, cap=16):
        s = ["<s>"]; cand = sorted(x for x in self.voc if x != "<s>")
        while len(s) < cap:
            x = rng.choices(cand, [self.p(s, y) for y in cand])[0]
            if x == "</s>": break
            s.append(x)
        return s[1:]
    def logp(self, seq):
        s = ["<s>"] + list(seq) + ["</s>"]
        return sum(math.log(self.p(s[:i], s[i])) for i in range(1, len(s))) / (len(s) - 1)

def q(v, a=25, b=75):
    v = sorted(v); n = len(v)
    if not n: return (None, None, None)
    return (v[int(n * a / 100)], v[n // 2], v[min(n - 1, int(n * b / 100))])

class Model:
    def __init__(self, mode="major", era=None, era_weight=3.0):
        S = json.load(open(DATA)); self.mode = mode
        self.data = collections.defaultdict(list); self.lens = collections.defaultdict(list); self.stats = collections.defaultdict(lambda: collections.defaultdict(list))
        for so in S:
            if so["mode"] != mode: continue
            yr = int((so["date"] or "0000")[:4] or 0); w = era_weight if era and era[0] <= yr <= era[1] else 1.0
            for s in so["sections"]:
                k = KIND.get(s["label"]);
                if not k or any(b.get("metre", "4/4") not in ("4/4",) for b in s["bars"]): continue
                ch = changes(beats(s))
                if not ch: continue
                self.data[k].append((ch, w)); self.lens[k] += [d for _, d in ch]
                if not (era and era[0] <= yr <= era[1]) and era: continue
                tot = sum(d for _, d in ch); seq = [x for x, _ in ch]; nb = len(s["bars"])
                st_ = self.stats[k]
                st_["distinct"].append(len(set(seq))); st_["tonic"].append(sum(d for x, d in ch if x in ("I", "i")) / tot)
                st_["cpb"].append(len(ch) / max(1, nb)); st_["out"].append(sum(d for x, d in ch if x not in IN[mode]) / tot)
                st_["first"].append(seq[0]); st_["last"].append(seq[-1]); st_["period"].append(period(to_bars(ch, nb)))
                st_["bars"].append(nb)
        self.vom = {k: VOM(v) for k, v in self.data.items()}
        self.q = {k: {m: q(v) for m, v in d.items() if m in ("distinct", "tonic", "cpb", "out", "bars")} for k, d in self.stats.items()}
        self.first = {k: collections.Counter(d["first"]) for k, d in self.stats.items()}
        self.last = {k: collections.Counter(d["last"]) for k, d in self.stats.items()}
        self.per = {k: collections.Counter(d["period"]) for k, d in self.stats.items()}

    def fit(self, seq, nbars, rng):
        """Give each chord of a drawn sequence a length so the plan fills nbars of 4/4, changes on beat 1 or 3, drawn from kept
        lengths (2, 4 or 8 beats here) and looped when the sequence is short, as kept sections loop."""
        L = [d for d in self.lens_k if d in (2, 4, 8)]
        out = []; tot = 0; i = 0; target = 4 * nbars
        while tot < target:
            x = seq[i % len(seq)]; d = rng.choice(L)
            d = min(d, target - tot)
            if out and out[-1][0] == x: out[-1][1] += d
            else: out.append([x, d])
            tot += d; i += 1
        return out

    def score(self, k, ch, nbars, require=()):
        qk = self.q[k]; seq = [x for x, _ in ch]; tot = sum(d for _, d in ch)
        m = dict(distinct=len(set(seq)), tonic=sum(d for x, d in ch if x in ("I", "i")) / tot, cpb=len(ch) / nbars,
                 out=sum(d for x, d in ch if x not in IN[self.mode]) / tot)
        pen = 0.0; why = []
        for key, v in m.items():
            lo, med, hi = qk[key]
            if v < lo - 1e-9: pen += 1; why.append(f"{key} {v:.2f} under the kept quartile {lo:.2f}")
            if v > hi + 1e-9: pen += 1; why.append(f"{key} {v:.2f} over the kept quartile {hi:.2f}")
        if m["cpb"] < qk["cpb"][1]: pen += 0.5; why.append("harmony moves less than the kept median (749.22)")
        f = self.first[k][seq[0]] / sum(self.first[k].values()); l = self.last[k][seq[-1]] / sum(self.last[k].values())
        if f < 0.05: pen += 1; why.append(f"first chord {seq[0]} rare here ({f:.0%})")
        if l < 0.05: pen += 1; why.append(f"last chord {seq[-1]} rare here ({l:.0%})")
        per = period(to_bars(ch, nbars))
        if self.per[k][per] / sum(self.per[k].values()) < 0.05: pen += 0.5; why.append(f"loop period {per} rare")
        lp = self.vom[k].logp(seq)
        return pen - 0.25 * lp, m, lp, why

    def section(self, k, nbars, rng, n=400, require=(), avoid=()):
        self.lens_k = self.lens[k]; best = []
        for _ in range(n):
            seq = self.vom[k].draw(rng)
            if not seq: continue
            pers = [p for p in self.per[k].elements()]; p = rng.choice(pers) if pers else None
            if p and nbars % p == 0 and nbars > p:
                unit = self.fit(seq, p, rng); ch = []
                for _ in range(nbars // p):
                    for x, d in unit:
                        if ch and ch[-1][0] == x: ch[-1][1] += d
                        else: ch.append([x, d])
                if rng.random() < 0.5:   # the last unit drawn fresh, as kept sections often turn at their end
                    tail = self.fit(self.vom[k].draw(rng) or seq, p, rng); bts = [x for x, d in ch for _ in range(d)][: 4 * (nbars - p)] + [x for x, d in tail for _ in range(d)]
                    ch = changes(bts)
            else:
                ch = self.fit(seq, nbars, rng)
            if tuple(x for x, _ in ch) in avoid: continue
            s, m, lp, why = self.score(k, ch, nbars, require)
            best.append((s, ch, m, lp, why))
        best.sort(key=lambda t: (t[0], str(t[1])))
        return best

def name(rn, tonic):
    """Roman numeral -> chord name in the key (E major: I E, ii F#m, bVII D)."""
    m = re.match(r"(b|#)?(VII|III|IV|VI|II|V|I|vii|iii|iv|vi|ii|v|i)(o|7)?$", rn)
    if not m: return rn
    acc, r, suf = m.groups(); deg = DEG[r.upper()] + (-1 if acc == "b" else 1 if acc == "#" else 0)
    root = (NAMES_S + NAMES_S).index(tonic) if tonic in NAMES_S else NAMES_F.index(tonic)
    pc = (root + deg) % 12; names = NAMES_S if tonic in SHARP_KEYS and acc != "b" else NAMES_F if acc == "b" else NAMES_S
    nm = names[pc]
    if acc == "b" and tonic in SHARP_KEYS and nm in ("Db", "Eb", "Gb", "Ab", "Bb"): nm = nm  # flats for lowered degrees (bVII in E is D)
    return nm + ("m" if r.islower() and suf != "o" else "dim" if suf == "o" else "") + ("7" if suf == "7" else "")

def write_song(form, mode="major", tonic="E", era=None, require=(), seed=0, n=400):
    """Write a chord plan for every section of the form. Returns (plan, report): plan maps a section name to per-bar chord-name tuples;
    report holds, per section, the chosen candidate's readings and the next two candidates for the test report."""
    rng = random.Random(seed); M = Model(mode, era); plan, rom, report = {}, {}, {}
    done = {}
    for nm, k, nb in form:
        if nm in done: continue
        avoid = {tuple(x for x, _ in c) for c in done.values()}
        cands = M.section(k, nb, rng, n=n, avoid=avoid)
        done[nm] = cands[0][1]
        report[nm] = dict(kind=k, bars=nb, chosen=[[x, d] for x, d in cands[0][1]], readings=cands[0][2], logp=round(cands[0][3], 3),
                          flags=cands[0][4], score=round(cands[0][0], 3), next=[dict(chords=[[x, d] for x, d in c[1]], score=round(c[0], 3), flags=c[4]) for c in cands[1:3]],
                          kept=M.q[k])
    # the song-wide style requirement (for example the bVII a key question asked for): if no section has it, rewrite the section
    # where it is commonest in kept songs with the best candidate that has it
    for req in require:
        if not any(req in [x for x, _ in c] for c in done.values()):
            share = {}
            for nm, k, nb in form:
                vs = [x for ch, _ in M.data[k] for x, _ in ch]; share[nm] = vs.count(req) / max(1, len(vs))
            for nm in sorted(share, key=lambda s: -share[s]):
                k, nb = next((k, nb) for n_, k, nb in form if n_ == nm)
                cands = [c for c in M.section(k, nb, random.Random(seed + 1), n=n * 3, avoid={tuple(x for x, _ in c) for s, c in done.items() if s != nm}) if req in [x for x, _ in c[1]]]
                if cands:
                    done[nm] = cands[0][1]; report[nm].update(chosen=[[x, d] for x, d in cands[0][1]], readings=cands[0][2], logp=round(cands[0][3], 3),
                                                             flags=cands[0][4] + [f"rewritten to carry the required {req}"], score=round(cands[0][0], 3))
                    break
    for nm, ch in done.items():
        nb = report[nm]["bars"]; rom[nm] = to_bars(ch, nb); plan[nm] = [tuple(name(x, tonic) for x in bar) for bar in rom[nm]]
    return plan, dict(sections=report, roman={k: [list(b) for b in v] for k, v in rom.items()}, seed=seed, era=era, mode=mode, tonic=tonic, require=list(require))

if __name__ == "__main__":
    form = [("Intro", "intro", 4), ("Verse", "verse", 8), ("Chorus", "chorus", 12), ("Bridge", "bridge", 14), ("Jam", "solo", 16), ("Outro", "outro", 4)]
    plan, rep = write_song(form, tonic="E", era=(1965, 1979), require={"bVII"}, seed=20261117)
    for k, v in plan.items(): print(k, " | ".join(" ".join(b) for b in v)); print("   ", rep["sections"][k]["flags"], rep["sections"][k]["score"])
