"""writers/band.py: Luthier's band writer (a prototype for v8, built from the arrangement study, Part 19, with Parts 9, 26, 28 and the
v7 research rules 749.14-749.21). Nobody arranges by hand: every texture is read from the kept tables.

What it decides, and from where:
  the level of each section   749.17 and 9.12: one song-wide curve. A section's base level is its role's kept piano density in POP909
                              (studies/arrangement/pop909_texture.json: intro, verse A, chorus B, instrumental, outro), scaled to 0-1;
                              each return of a role sits above the one before; the last chorus is the top; a section the form marks as
                              starting from silence ramps from nothing to its next section's level (749.19's breath and fresh re-entry).
  who plays                   the genre's kept parts (lpd_band_tables.json, by genre): drums, bass, the chordal parts the lane names; in
                              a ramping section the parts enter one at a time, evenly through its first half, chords first, drums last
                              but one, the lead last (kept intros: drums enter at bar 1, middle half 0 to 3).
  rhythm of each chordal part the genre's kept one-bar patterns on sixteenths for that instrument (piano for keyboards, guitar for
                              guitars): the pattern whose onsets a bar sit nearest the level's target, the target read along the kept
                              quartiles of onsets a bar (low level the 25th percentile, high the 75th); ties by kept share.
  voicing                     notes together from the kept quartiles (low level fewer), inside the kept register (low and high
                              quartiles), Module 9.14's low-interval limits, and under the voice while it sings (749.21: accompaniment
                              above the sung tune at most 2% of the time), each chord led to the nearest voicing of the next.
  drums                       the genre's kept kick and snare patterns (the commonest kick at low levels, busier ones higher); hats in
                              eighths (the kept share), ride at the top levels; a fill on a section's last bar (kept fill rate a few
                              bars in a hundred, flat across the eight-bar unit), a crash on its first; a light swing is the demo's.
  bass                        bass_v134.py's routine (the engine's own), every section, on the drums' kicks and the voice's rests.
The lead guitar's lines (fills and the jam) are writers/solo.py's.

    parts, report = write_band(rec, lane, seed)    rec: bars (sec, kind, k, n, start, chord, chord2), lead notes, form roles."""
import json, os, random, collections, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ARR = os.path.join(HERE, "..", "studies", "arrangement")
LPD = json.load(open(os.path.join(ARR, "lpd_band_tables.json")))["by_genre"]
TEX = json.load(open(os.path.join(ARR, "pop909_texture.json")))["by_role"]
DR = dict(kick=36, snare=38, rim=37, hat=42, ohat=46, ride=51, crash=49, tom_hi=48, tom_mid=45, tom_lo=41)
LOW914 = {1: 60, 2: 60, 3: 53, 4: 53, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}     # Module 9.14 (749.21)
ROLE_TEX = {"intro": "intro", "verse": "A", "chorus": "B", "bridge": "other sung", "solo": "instrumental", "outro": "outro", "tag": "B"}

def interp_q(q, x):
    """x in [0, 1] along a kept quartile triple: 0 -> 25th, 0.5 -> median, 1 -> 75th (clipped)."""
    lo, med, hi = q; x = min(1.0, max(0.0, x))
    return lo + (med - lo) * x * 2 if x <= 0.5 else med + (hi - med) * (x - 0.5) * 2

def levels(form, ramp=()):
    """form: list of (name, role, bars). Returns {name: (start level, end level)} on one curve (749.17)."""
    dens = {r: TEX[t]["piano_per_beat"][1] for r, t in ROLE_TEX.items()}
    lo_, hi_ = min(dens.values()), max(dens.values())
    base = {r: 0.25 + 0.5 * (d - lo_) / (hi_ - lo_) for r, d in dens.items()}
    seen = collections.Counter(); out = {}
    total = sum(b for _, _, b in form); pos = 0
    for nm, role, nb in form:
        lv = base[role] * (1 + 0.12 * seen[role]); seen[role] += 1
        out[nm] = [lv, lv]; pos += nb
    sung_ch = [nm for nm, r, _ in form if r == "chorus"]
    if sung_ch: out[sung_ch[-1]] = [1.0, 1.0]                                                   # the last chorus is the top
    top = max(v[0] for v in out.values())
    for nm in out: out[nm] = [v / top for v in out[nm]]
    names = [f[0] for f in form]
    for nm in ramp:                                                                             # from silence to the next section's level
        i = names.index(nm); nxt = out[names[i + 1]][0] if i + 1 < len(names) else 0.6
        out[nm] = [0.0, nxt]
    return {k: tuple(round(x, 3) for x in v) for k, v in out.items()}

def pattern_for(inst_rows, target):
    """the kept pattern (sixteenths) whose onsets a bar sit nearest the target; ties by kept share."""
    pats = [(p, w) for p, w in inst_rows if p.count("x") > 0]
    return min(pats, key=lambda pw: (abs(pw[0].count("x") - target), -pw[1]))[0]

class Band:
    def __init__(self, rec, lane, seed):
        self.rec = rec; self.lane = lane; self.rng = random.Random(f"band {seed}"); self.G = LPD[lane["genre"]]
        self.parts = collections.defaultdict(list); self.report = dict(genre=lane["genre"], sections={})
        self.CH = lane["chords"]                                                                 # name -> (root pc, set of pcs)
        self.voice = collections.defaultdict(list)                                               # sixteenth -> sung pitches
        for n in rec["lead"]:
            for t in range(n["on"], n["on"] + n["dur"], 3): self.voice[t // 3].append(n["midi"])
        self.prev = {}
    def ev(self, part, on, dur, p, vel, art=""):
        self.parts[part].append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=int(max(1, min(127, vel))), art=art))
    def tones(self, ch): return self.CH[ch][1]
    def root(self, ch): return self.CH[ch][0]
    def voicing(self, part, ch, n, lo, hi, cap):
        """n chord tones in [lo, hi], under cap (the voice), inside 9.14's limits, nearest the part's last voicing."""
        pcs = self.tones(ch); cands = []
        pool = [q for q in range(lo, min(hi, cap) + 1) if q % 12 in pcs]
        if len(pool) < n: pool = [q for q in range(lo - 5, min(hi, cap) + 1) if q % 12 in pcs]
        if not pool: pool = []
        def ok(v):
            return all(b - a >= 12 or a >= LOW914.get(b - a, 0) for a, b in zip(v, v[1:]))
        import itertools
        for v in itertools.combinations(pool[-9:], min(n, len(pool[-9:]))):
            if ok(v) and len({q % 12 for q in v}) >= min(n, len(pcs), 2): cands.append(list(v))
        if not cands:                                                                           # under a low voice: an open voicing (root,
            r0 = self.root(ch); fifth = (r0 + 7) % 12                                           # fifth, octave), which 9.14 allows lower,
            for base in range(min(hi, cap) - 19, 27, -1):                                       # or the root and its octave; else a rest
                if base % 12 != r0: continue
                for v in ([base, base + 7, base + 12], [base, base + 7], [base, base + 12], [base]):
                    if max(v) <= cap and ok(v) and v[0] >= 28: self.prev[part] = v; return v[: max(1, min(len(v), n))]
            return []
        last = self.prev.get(part)
        key = (lambda v: sum(abs(a - b) for a, b in zip(sorted(v), sorted(last))) if last and len(last) == len(v) else -sum(v) * 0.01)
        best = min(cands, key=lambda v: (key(v), -len({q % 12 for q in v}), -max(v)))
        self.prev[part] = best; return best
    def cap_at(self, t0, t1, default=127):
        sung = [p for s in range(t0 // 3, max(t0 // 3 + 1, t1 // 3)) for p in self.voice.get(s, [])]
        return (min(sung) - 1) if sung else default
    def chordal(self, part, inst, x, level, vel):
        G = self.G[inst]; tgt = interp_q(G["onsets_a_bar"], level); pat = pattern_for(G["rhythm"], tgt)
        n_tog = int(round(interp_q(G["together"], level))) + 1                                   # notes together (kept 'together' counts the
        lo, hi = int(G["low"][1]), int(G["high"][1])                                             # others above the lowest), the kept register
        ons = [i for i, c in enumerate(pat) if c == "x"]
        for j, i in enumerate(ons):
            nxt = ons[j + 1] if j + 1 < len(ons) else 16
            t = x["start"] + 3 * i; d = 3 * (nxt - i); held = G["held"][1]
            ch = x["chord"] if 3 * i < 24 else x["chord2"]
            if 3 * i < 24 <= 3 * nxt and x["chord2"] != x["chord"]: d = 24 - 3 * i            # the chord changes at the half bar
            cap = self.cap_at(t, t + d)
            vc = self.voicing(part, ch, n_tog, lo, hi, cap)
            if vc: self.ev(part, t, max(3, int(d * held)), vc, vel - (6 if i % 4 else 0))
            if 3 * i < 24 <= 3 * nxt and x["chord2"] != x["chord"]:
                cap2 = self.cap_at(x["start"] + 24, x["start"] + 3 * nxt)
                vc2 = self.voicing(part, x["chord2"], n_tog, lo, hi, cap2)
                if vc2: self.ev(part, x["start"] + 24, max(3, int((3 * nxt - 24) * held)), vc2, vel - 4)
        return pat
    def drums(self, x, level, vel, fill, crash, ride):
        D = self.G["drums"]; kicks = [p for p, w in D["kick"] if p.count("x")]
        kick = kicks[0] if level < 0.45 else min(kicks, key=lambda p: (abs(p.count("x") - (2 + 2 * level)), kicks.index(p)))
        snare = D["snare"][0][0]; st = x["start"]
        for i in range(16):
            t = st + 3 * i
            if fill and i >= 8:
                if i % 2 == 0: self.ev("drums", t, 3, DR[["snare", "snare", "tom_hi", "tom_mid", "tom_lo"][min(4, (i - 8) // 2 + (1 if i >= 12 else 0))]], vel - 4 + (i - 8))
                continue
            if kick[i] == "x": self.ev("drums", t, 3, DR["kick"], vel)
            if snare[i] == "x": self.ev("drums", t, 3, DR["snare"] if level >= 0.35 else DR["rim"], vel - (0 if level >= 0.35 else 10))
            if i % 2 == 0: self.ev("drums", t, 3, DR["ride" if ride else "hat"], vel - 24 + (6 if i % 4 == 0 else 0))
        if crash: self.ev("drums", st, 6, DR["crash"], vel + 6)
        return kick

def write_band(rec, lane, seed, ramp=(), entry=("organ", "bass", "drums", "rhythm", "lead")):
    """rec['bars'] in order; lane: genre, chords, parts {name: lpd instrument}; ramp: sections that build from silence."""
    B = Band(rec, lane, seed)
    form = []
    for x in rec["bars"]:
        if not form or form[-1][0] != x["sec"]: form.append([x["sec"], x["role"], 0])
        form[-1][2] += 1
    LV = levels([tuple(f) for f in form], ramp)
    B.report["levels"] = LV
    for x in rec["bars"]:
        sec, k, nb = x["sec"], x["k"], x["n"]; a, b = LV[sec]; lvl = a + (b - a) * (k / max(1, nb - 1))
        vel = int(56 + 40 * lvl)
        on = set(lane["parts"]) | {"drums", "bass", "lead"}                                     # drums and bass in every kept rock song (drums_share 0.94)
        if sec in ramp:                                                                          # the parts enter one at a time
            half = nb / 2; order = [p for p in entry if p in on or p in ("bass", "drums", "lead")]
            step = half / max(1, len(order) - 1)
            on = {p for j, p in enumerate(order) if k >= int(round(j * step))}
        if lvl <= 0.02 and sec in ramp: on = {order[0]}
        rep = B.report["sections"].setdefault(sec, dict(level=(a, b), patterns={}, kick=None, entries={}))
        for part, inst in lane["parts"].items():
            if part in on:
                rep["entries"].setdefault(part, k)
                pat = B.chordal(part, inst, x, max(0.05, lvl), vel - (8 if part == "organ" else 0))
                rep["patterns"].setdefault(part, pat)
        if "drums" in on:
            rep["entries"].setdefault("drums", k)
            kk = B.drums(x, lvl, vel, fill=(k == nb - 1 and sec not in ("Ending",)), crash=(k == 0 and lvl >= 0.4), ride=lvl >= 0.85)
            rep["kick"] = rep["kick"] or kk
        if "bass" in on: rep["entries"].setdefault("bass", k)
        if "lead" in on: rep["entries"].setdefault("lead", k)
    B.report["bass_entries"] = {s: r["entries"].get("bass") for s, r in B.report["sections"].items()}
    B.report["lead_entries"] = {s: r["entries"].get("lead") for s, r in B.report["sections"].items()}
    return B.parts, B.report
