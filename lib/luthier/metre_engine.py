"""Luthier v12, stage 3a (Module 27.93; fix 790): a melody engine in which the metre is a setting.

The 4/4 engine (melody_l11_pNN.py) holds the bar in its code and in every table. This engine holds neither: it reads a song's spec
(a JSON file: metre, key, chords by bar, the lyric's lines with their stresses, how each line is made, registers, designs and gates)
and the metre atlas (tables/metre_atlas/<metre>_sung.json: the bar, its beats, kept two-bar windows by syllable count, kept bars,
intervals, places in the bar, note lengths, and the kept quartiles of every reading). Nothing in it names a metre.

It carries the rules that were proved on the 4/4 engine in stages 1 and 2 and the session's 6/8 sketch (songs/p62/gen68.py):
  653/680  a line's rhythm is a kept window whole, for its count of syllables; pickups are the unstressed syllables before the first stress
  731/771  the first onset before, on or after the bar line at the kept shares for the first syllable's stress
  760      a line no kept window fits is set by weighted rules: places in the bar at the kept shares, stressed syllables toward the beats
  761      no gap of three-quarters of a bar inside a line of eight syllables or fewer set by rule
  770      the floor under a line's start is the least breath after the line before (three-eighths of a 4/4 bar's length, scaled to the bar)
  712/772  a line sung again takes its source's onsets and pitches fitted to its syllables; a stressed opening drops its source's pickup
  780      a copied line keeps the join its source kept
  751      two notes on one onset, or a note of no length, is a death
  650      each pitch drawn from the kept interval shares, chord tones weighted on the beats, inside the section's register
  730      the pick: the least charge on the kept quartiles of the metre (outside the middle half, in its widths), then nearest the medians

    python3 lib/luthier/metre_engine.py songs/p62/spec52.json 3000 [seed]      # writes <spec>.run.json beside the spec

A spec's 'how' gives each line one of: fresh; ["again", section, line]; ["copy", section, line]; ["design", [[onset, pitch, length], ...]].
Onsets are twelfths of a quarter note from the line's slot start. Every choice is deterministic for a seed."""
import json, random, sys, os, math, collections, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ATLAS = os.path.join(HERE, "..", "..", "tables", "metre_atlas")
ENTRY = {True: (0.20, 0.42, 0.38), False: (0.43, 0.10, 0.47)}          # 771: before, on, after the bar line, by the first syllable's stress
UNCHARGED = ("notes a bar", "notes a beat", "gaps of a sixteenth", "gaps of an eighth", "gaps of a quarter or more", "gaps of half a beat", "gaps of a third of a beat",
             "gaps of a beat or more", "gaps under a third of a beat", "range", "distinct pitches")   # set by the lyric's density and the designs: printed, not charged

def FLOOR(m): return 0.02 if m <= 1.5 else 1.0          # 793, as mended by 810 (749.47): ONLY where the kept songs all read alike is the width two points of share, or one count

class Engine:
    def __init__(self, spec):
        self.S = spec; T = json.load(open(os.path.join(ATLAS, (spec.get("table") or spec["metre"].replace("/", "-") + "_sung") + ".json"))); self.T = T      # 812: a spec may name its kept table
        self.BAR, self.BEATS = T["bar"], T["beats"]; self.BEAT = T["beat"] or min(b - a for a, b in zip(self.BEATS, self.BEATS[1:] + [self.BAR]))   # uneven metres: the shortest beat
        self.END, self.REST = 6, 12; self.BREATH = self.END + self.REST          # 844 (749.53; amends 770, 832): a line's last note is an eighth at least (kept 5th percentile) and a quarter's rest follows (kept 10th), in every metre
        self.WIN = {int(k): [(tuple(p), c) for p, c in v] for k, v in T["two_bar_windows"].items()}
        self.BARS = collections.defaultdict(list)
        for p, c in T["bar_rhythms"]: self.BARS[len(p)].append((tuple(p), c))
        self.IV = {int(k): v for k, v in T["intervals"].items()}; self.IVT = sum(self.IV.values())
        self.IV2 = {int(k): {int(j): c for j, c in v.items()} for k, v in T.get("interval_pairs", {}).items()}     # 817: where the table has them, a move is drawn given the move before
        self.OW = {int(k): v for k, v in T["onset_weights"].items()}; self.DUR = {int(k): v for k, v in T["durations"].items()}; self.DT = sum(self.DUR.values())
        self.Q = T["readings_quartiles"]; self.SCALE = set(spec["scale"]); self.CH = {k: set(v) for k, v in spec["chords"].items()}
        self.BAR0 = {}; self.CHORD = []; b = 0
        for sec, chs in spec["form"]: self.BAR0[sec] = b; self.CHORD += chs; b += len(chs)
        self.NBARS = b; self.SUNG = [s for s, _, _ in spec["sung"]]; self.KIND = {s: k for s, k, _ in spec["sung"]}; self.LINES = {s: [[(t, bool(st)) for t, st in ln] for ln in ls] for s, _, ls in spec["sung"]}
        self.SLOTS = {s: spec.get("slots", {}).get(s, [2] * len(self.LINES[s])) for s in self.SUNG}
        self.KEYS = [(s, i) for s in self.SUNG for i in range(len(self.LINES[s]))]; self.HOW = {tuple(k.rsplit(":", 1)): v for k, v in spec.get("how", {}).items()}
        self.HOW = {(s, int(i)): v for (s, i), v in self.HOW.items()}; self.stats = collections.Counter()
    # ---- the frame
    def line_start(self, sec, i): return (self.BAR0[sec] + sum(self.SLOTS[sec][:i])) * self.BAR
    def slot_len(self, sec, i): return self.SLOTS[sec][i] * self.BAR
    def chord_at(self, t):
        c = self.CHORD[max(0, min(self.NBARS - 1, t // self.BAR))]
        if isinstance(c, str): return self.CH[c]
        n = len(c); half = self.BAR // 2                                                     # 803: a bar of several chords: two on the halves (or the last beat), more beat by beat
        at = [0] if n == 1 else [0, half if half in self.BEATS else self.BEATS[-1]] if n == 2 else ([0] + self.BEATS[len(self.BEATS) - n + 1:] if len(self.BEATS) >= n else [round(i * self.BAR / n / 3) * 3 for i in range(n)])
        return self.CH[c[max(i for i, x in enumerate(at) if x <= max(0, t) % self.BAR)]]
    def on_beat(self, t): return (t % self.BAR) in self.BEATS
    def reg(self, sec, i):
        R = self.S["registers"]; return tuple(R.get(f"{sec}:{i}") or R.get(sec) or R[self.KIND[sec]])
    def ivp(self, d, last=None):
        d = max(-12, min(12, d)); row = self.IV2.get(max(-12, min(12, last))) if last is not None else None
        if row and sum(row.values()) >= 50: return (row.get(d, 0) + 12.5 * (self.IV.get(d, 0) + 0.5) / self.IVT) / (sum(row.values()) + 12.5)
        return (self.IV.get(d, 0) + 0.5) / self.IVT
    # ---- rhythm
    def stress_score(self, ons, sy):
        sc = 0.0
        for t, (_, st) in zip(ons, sy):
            b = t >= 0 and self.on_beat(t)
            sc += (1.5 if b else -0.6) if st else (-0.8 if (b and t % self.BAR == 0) else 0.0)
        if sy[-1][1] and not self.on_beat(ons[-1]): sc -= 1.0
        return sc
    def kept_windows(self, n, bars):
        if bars == 2: return self.WIN.get(n, [])
        if bars == 1: return self.BARS.get(n, [])
        return []
    def rhythm(self, rng, sy, tmin, slot, cap=None, hook=False):
        n = len(sy); lead = 0
        for x in sy:
            if x[1]: break
            lead += 1
        end = slot - self.BREATH if cap is None else min(slot - self.BREATH, cap); out = []; bars = slot // self.BAR; early = []
        for p in sorted({0, min(1, lead), min(2, lead)}):
            for w, c in self.kept_windows(n - p, bars):
                if w[-1] > end or (w[0] != 0 and p > 0): continue
                ons = [-6 * (p - j) for j in range(p)] + list(w)
                if ons[0] < tmin: continue
                e = ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]
                out.append((ons, math.log(c + 1) + (2.8 if hook else 1.4) * self.stress_score(ons, sy) + math.log(e)))        # 840: the title line's stresses pulled twice as hard to the beat
                if p == 0 and sy[0][1] and w[0] == 0 and self.S.get("early_entries"):               # 834: a line that opens on a stress may sing its kept window an eighth or a quarter early
                    for sh in (6, 12):
                        o2 = [x - sh for x in w]
                        if o2[0] >= tmin: early.append((o2, math.log(c + 1) + 1.4 * self.stress_score([x for x in w], sy)))
        if early and rng.random() < ENTRY[True][0]: out = early; self.stats["834: a stressed opening sung before the bar line"] += 1      # the entry's class first, at the kept share (771)
        if out:
            top = sorted(out, key=lambda x: -x[1])[:12]; ws = [math.exp(s - top[0][1]) for _, s in top]; self.stats["653: a line in a kept window"] += 1
            return rng.choices([o for o, _ in top], ws)[0]
        o = self.weighted(rng, sy, tmin, end)
        if o is not None: self.stats["760: a line set by the weighted rule"] += 1
        return o
    def weighted(self, rng, sy, tmin, end):
        """760: n onsets on the sixteenth grid in [tmin, end]: places at the kept shares, stressed syllables toward the beats, kept note lengths as gaps."""
        n = len(sy); P = list(range(int(-(-max(tmin, -12) // 3) * 3), int(end) + 1, 3)); m = len(P)
        if m < n: return None
        st = [s for _, s in sy]; cap = int(0.75 * self.BAR) if n <= 8 else 10 ** 6                  # 761
        def pw(t, s): w = self.OW.get(t % self.BAR, 0.002); return w * ((2.6 if self.on_beat(t) else 0.45) if s else (0.5 if self.on_beat(t) else 1.3))
        def gw(g): return (self.DUR.get(g, 0) + 1.0) / self.DT
        B = [[0.0] * m for _ in range(n)]
        for j in range(m): B[n - 1][j] = 1.0
        for k in range(n - 2, -1, -1):
            for j in range(m):
                B[k][j] = sum(gw(P[j2] - P[j]) * pw(P[j2], st[k + 1]) * B[k + 1][j2] for j2 in range(j + 1, m) if P[j2] - P[j] < cap)
        w0 = [pw(P[j], st[0]) * B[0][j] for j in range(m)]; cl = [0 if P[j] < 0 else 1 if P[j] == 0 else 2 for j in range(m)]
        if sum(w0) <= 0: return None
        mass = [sum(w for w, c in zip(w0, cl) if c == q) for q in range(3)]; q = rng.choices(range(3), [ENTRY[st[0]][q] if mass[q] > 0 else 0 for q in range(3)])[0]   # 771: the entry's class at the kept share, then the place
        w0 = [w if c == q else 0.0 for w, c in zip(w0, cl)]
        j = rng.choices(range(m), w0)[0]; out = [P[j]]
        for k in range(n - 1):
            c = [(j2, gw(P[j2] - P[j]) * pw(P[j2], st[k + 1]) * B[k + 1][j2]) for j2 in range(j + 1, m) if P[j2] - P[j] < cap]; c = [x for x in c if x[1] > 0]
            if not c: return None
            j = rng.choices([x[0] for x in c], [x[1] for x in c])[0]; out.append(P[j])
        return out
    # ---- pitches
    def pitches(self, rng, ons, U, sec, i, prev, avoid=None, end_off=None):
        mu, lo, hi = self.reg(sec, i); ps = []; last = None; sy = self.LINES[sec][i]
        DG = self.S.get("degrees"); DW = (DG["weights"].get(self.KIND[sec]) or DG["weights"]["all"]) if DG else None; ton = DG["tonic"] if DG else 0; blue = set(DG.get("blue", ())) if DG else set()
        WP = self.S.get("word_pitch")
        for k, t in enumerate(ons):
            ch = self.chord_at(U + t); cands = [p for p in range(lo, hi + 1) if (p % 12 in self.SCALE or (p - ton) % 12 in blue) and not (avoid and p % 12 in avoid)]; ws = []
            long_ = k == len(ons) - 1 or ons[k + 1] - t >= self.BEAT
            if self.S.get("clash_rule") and (long_ or not ch <= self.SCALE):                     # 808: over a chord from outside the key; 833: and under any chord on a note a beat long or more:
                c2 = [p for p in cands if p % 12 in ch or (p - ton) % 12 in blue or not ((p + 1) % 12 in ch or (p - 1) % 12 in ch)]       # no tone a semitone from a chord tone, unless a chord tone (846: or a blue note, which kept songs sing over the major third)
                cands = c2 or cands
            for p in cands:
                w = self.ivp(p - prev, last) if prev is not None else math.exp(-abs(p - mu) / 3)
                w *= (2.6 if p % 12 in ch else 0.3) if self.on_beat(U + t) else (1.3 if p % 12 in ch else 0.8)
                w *= math.exp(-((p - mu) ** 2) / 50)
                if len(ps) >= 2 and ps[-1] == ps[-2] == p: w = 0.0
                if DW: w *= DW.get(str((p - ton) % 12), 0.0)                                      # 846: the kept share of each degree of the scale, blue notes among them
                if WP and k > 0 and k < len(sy) and sy[k][0] == sy[k - 1][0] and sy[k][1] != sy[k - 1][1] and prev is not None:      # 847: inside a word, the stressed syllable against the other
                    up = (p > prev) if sy[k][1] else (p < prev); w *= WP[1] if p == prev else WP[0] if up else WP[2]
                if k == len(ons) - 1 and end_off is not None and p % 12 == end_off: w *= 0.05
                ws.append(w)
            if sum(ws) <= 0: return None
            p = rng.choices(cands, ws)[0]; last = (p - prev) if prev is not None else None; ps.append(p); prev = p
        return ps
    def again(self, rng, src, src_st0, sy, U, sec, i, tmin, slot):
        """712: the source's onsets and pitches fitted to new syllables; 772: a stressed opening drops its source's pickup."""
        floor = max(tmin, 0) if (sy[0][1] and not src_st0 and src[0][0] < 0) else tmin
        if floor != tmin: self.stats["772: a line sung again, stressed opening: its source's pickup dropped"] += 1
        keep = [(t, p) for t, p in src if t >= floor] or src[-1:]; on = [t for t, p in keep]; ps = [p for t, p in keep]; n = len(sy)
        while len(on) < n:
            gaps = [((on[j + 1] if j + 1 < len(on) else slot - 6) - on[j], j) for j in range(len(on))]; g, j = max(gaps)
            if g < 6: return None
            h = on[j] + (g // 2 // 3) * 3
            if h <= on[j]: return None
            nxt = ps[j + 1] if j + 1 < len(ps) else ps[j]; step = [q for q in (ps[j] + 1, ps[j] - 1, ps[j] + 2, ps[j] - 2) if q % 12 in self.SCALE]
            q = min(step, key=lambda q_: abs(q_ - nxt)) if (rng.random() < 0.6 or (j > 0 and ps[j - 1] == ps[j])) else ps[j]
            on.insert(j + 1, h); ps.insert(j + 1, q)
        while len(on) > n:
            gaps = [(on[j + 1] - on[j], j) for j in range(1, len(on) - 1)]
            if not gaps: return None
            g, j = min(gaps); del on[j]; del ps[j]
        out = []; mu, lo, hi = self.reg(sec, i)
        for t, p in zip(on, ps):
            ch = self.chord_at(U + t)
            j_ = on.index(t); long_ = j_ == len(on) - 1 or on[j_ + 1] - t >= self.BEAT
            if self.S.get("clash_rule") and long_ and p % 12 not in ch and ((p + 1) % 12 in ch or (p - 1) % 12 in ch):                 # 833, in a line sung again
                p = min((p + d for d in (-1, 1, -2, 2, -3, 3, -4, 4) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch and lo <= p + d <= hi), key=lambda q_: abs(q_ - p), default=p)
            if self.on_beat(U + t) and p % 12 not in ch: p = min((p + d for d in (-1, 1, -2, 2) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch), key=lambda q_: abs(q_ - p), default=p)
            while p > hi: p -= 12 if p - 12 >= lo else 1
            while p < lo: p += 1
            while p % 12 not in self.SCALE: p -= 1
            if self.S.get("clash_rule") and long_ and p % 12 not in ch and ((p + 1) % 12 in ch or (p - 1) % 12 in ch):                 # 833 again, after the register has moved the note
                p = min((p + d for d in (-1, 1, -2, 2, -3, 3, -4, 4) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch and lo <= p + d <= hi), key=lambda q_: abs(q_ - p), default=p)
            out.append((t, p))
        return out
    # ---- a build
    def tmin(self, lines, k):
        if k == 0: return -12
        ps, pj = self.KEYS[k - 1]; sec, i = self.KEYS[k]
        return max(-12, self.line_start(ps, pj) + lines[(ps, pj)][-1][0] + self.BREATH - self.line_start(sec, i))
    @staticmethod
    def runs_ok(ps): return all(not (ps[k] == ps[k + 1] == ps[k + 2] == ps[k + 3]) for k in range(len(ps) - 3))
    def build(self, rng):
        lines = {}; prev = None; plans = {}
        for name, opts in self.S.get("plans", {}).items(): plans[name] = rng.choice(opts)
        for k, (sec, i) in enumerate(self.KEYS):
            sy = self.LINES[sec][i]; U = self.line_start(sec, i); slot = self.slot_len(sec, i); how = self.HOW.get((sec, i), ["fresh"]); tm = self.tmin(lines, k)
            cap = None                                                                        # 816 (780, 773 carried): the line before a copied or designed line that comes in early gives way
            if k + 1 < len(self.KEYS):
                ns_, ni_ = self.KEYS[k + 1]; hn = self.HOW.get((ns_, ni_), ["fresh"]); f0 = None
                if hn[0] == "design": f0 = hn[1][0][0]
                elif hn[0] == "copy" and (hn[1], hn[2]) in lines: f0 = lines[(hn[1], hn[2])][0][0]
                if f0 is not None: cap = self.line_start(ns_, ni_) + f0 - self.BREATH - U
            if how[0] == "plan":                                                              # a line that returns an earlier line of its section under a drawn plan
                pl = plans[how[1]]; how = ["again", sec, pl.index(pl[i])] if pl.index(pl[i]) != i else ["fresh"]
            if how[0] == "design": lines[(sec, i)] = [(t, p) for t, p, d in how[1]]; prev = lines[(sec, i)][-1][1]; continue
            if how[0] == "copy":
                src = lines[(how[1], how[2])]
                if src[0][0] < tm and src[0][0] < tm - (self.BREATH - 12): return None, ("join before a copy (780)", sec, i)     # 780: two fixed lines a beat apart or more
                new = list(src)
                if sec in (self.S.get("vary_returns") or ()) and how[1] != sec and i != 0 and f"{sec}:{i}" not in self.S.get("hooks", ()) and len(new) > 2:      # 839 (749.8): a returning line, not the section's first nor the title's, lifts one held note
                    gaps = [(new[j + 1][0] - new[j][0]) if j + 1 < len(new) else min(24, slot - new[j][0] - self.REST) for j in range(len(new))]; st_ = [x[1] for x in sy]      # 856 (749.56): a note's sung length, the last note's as 844 leaves it
                    held = [j_ for j_ in range(len(new)) if gaps[j_] >= 12] or list(range(len(new)))
                    j = max(held, key=lambda j_: (st_[j_] if j_ < len(st_) else False, min(gaps[j_], 48), -j_)); t0, p0 = new[j]; ch = self.chord_at(U + t0); mu, lo, hi = self.reg(sec, i)
                    for q in (range(p0 + 1, p0 + (5 if j == len(new) - 1 else 4)) if gaps[j] >= 12 else ()):                                 # only a note a quarter long or more is lifted
                        if q % 12 in ch and q % 12 in self.SCALE and q <= hi and (j == 0 or abs(q - new[j - 1][1]) <= 7) and (j == len(new) - 1 or abs(new[j + 1][1] - q) <= 7):
                            trial = new[:j] + [(t0, q)] + new[j + 1:]
                            if self.runs_ok([p_ for _, p_ in trial]): new = trial; self.stats["839: a returning line lifts one held note"] += 1
                            break
                lines[(sec, i)] = new; prev = new[-1][1]; self.stats["780: a copied line keeps its source's join"] += 1; continue
            if how[0] == "again":
                src = lines[(how[1], how[2])]; r = self.again(rng, src, self.LINES[how[1]][how[2]][0][1], sy, U, sec, i, tm, slot)
                if r is not None and self.runs_ok([p for t, p in r]) and r[0][0] >= tm and (cap is None or r[-1][0] <= cap): lines[(sec, i)] = r; prev = r[-1][1]; continue
                self.stats["712: a line sung again that could not be fitted, drawn fresh"] += 1
            ons = None; bw = self.S.get("borrow")                                             # 818: a fresh line may sing an earlier line of its section again, or take its rhythm
            if bw and how[0] == "fresh":
                j = next((j for j in (i - 2, i - 1) if j >= 0 and self.HOW.get((sec, j), ["fresh"])[0] != "design"), None); x = rng.random()
                if j is not None and x < bw["figure"] + bw["rhythm"]:
                    r = self.again(rng, lines[(sec, j)], self.LINES[sec][j][0][1], sy, U, sec, i, tm, slot)
                    if r is not None and r[0][0] >= tm and (cap is None or r[-1][0] <= cap) and all(b2 > a2 for a2, b2 in zip([t for t, _ in r], [t for t, _ in r][1:])):
                        if x < bw["figure"] and self.runs_ok([p for t, p in r]): lines[(sec, i)] = r; prev = r[-1][1]; self.stats["818: a line sings an earlier line of its section again"] += 1; continue
                        ons = [t for t, _ in r]; self.stats["818: a line takes an earlier line's rhythm"] += 1
            if ons is None: ons = self.rhythm(rng, sy, tm, slot, cap, hook=f"{sec}:{i}" in self.S.get("hooks", ()))
            if ons is None: return None, ("rhythm: the syllables cannot fit the window", sec, i)
            rule = self.S.get("line_rules", {}).get(f"{sec}:{i}", {}); ps = None
            for _ in range(20):
                ps = self.pitches(rng, ons, U, sec, i, prev, avoid=set(rule.get("avoid", [])) or None, end_off=rule.get("end_off"))
                if ps and self.runs_ok(ps): break
                ps = None
            if ps is None: return None, ("pitch", sec, i)
            lines[(sec, i)] = list(zip(ons, ps)); prev = ps[-1]
        flat = []
        for (s, i) in self.KEYS:
            U = self.line_start(s, i)
            for k, (t, p) in enumerate(lines[(s, i)]): flat.append(dict(on=U + t, p=p, sec=s, line=i, syl=k, stress=self.LINES[s][i][k][1], text=self.LINES[s][i][k][0]))
        flat.sort(key=lambda n: n["on"])
        for j, n in enumerate(flat):
            nx = flat[j + 1]["on"] if j + 1 < len(flat) else n["on"] + 2 * self.BAR; last = j + 1 == len(flat) or (flat[j + 1]["sec"], flat[j + 1]["line"]) != (n["sec"], n["line"])
            how = self.HOW.get((n["sec"], n["line"]), ["fresh"]); dd = {t: d for t, p, d in how[1]} if how[0] == "design" else None
            n["dur"] = dd[n["on"] - self.line_start(n["sec"], n["line"])] if dd is not None else (max(self.END, min(nx - n["on"] - self.REST, 24)) if last else nx - n["on"])       # 832: a line's last note leaves the least breath
        for j in range(len(flat) - 1):
            if flat[j]["on"] + flat[j]["dur"] > flat[j + 1]["on"]: flat[j]["dur"] = flat[j + 1]["on"] - flat[j]["on"]
        return dict(notes=flat, plans=plans), None
    # ---- readings, gates, the pick
    def readings(self, notes):
        p = [n["p"] for n in notes]; iv = np.diff(p); bars = collections.defaultdict(list); BAR, BEAT = self.BAR, self.BEAT
        for n in notes: bars[n["on"] // BAR].append(n["on"] % BAR)
        pats = [tuple(v) for v in bars.values()]; best = run = 1
        for a, b in zip(p, p[1:]): run = run + 1 if a == b else 1; best = max(best, run)
        g = np.diff([n["on"] for n in notes]); gb = g / BEAT
        r = {"repeated notes": float(np.mean(iv == 0)), "moves by step": float(np.mean((abs(iv) >= 1) & (abs(iv) <= 2))), "moves by leap": float(np.mean(abs(iv) >= 5)),
             "turns of direction": sum(1 for a, b in zip(iv, iv[1:]) if a * b < 0) / max(1, int(np.sum(iv != 0)) - 1), "range": int(max(p) - min(p)), "distinct pitches": len(set(p)),
             "longest run of one pitch": best, "distinct rhythms over bars": len(set(pats)) / len(pats), "notes a bar": len(notes) / len(pats), "notes a beat": len(notes) / len(pats) / (BAR / BEAT),
             "onsets on the beat": float(np.mean([self.on_beat(n["on"]) for n in notes])), "onsets on the bar's first beat": float(np.mean([n["on"] % BAR == 0 for n in notes])),
             "gaps of a sixteenth": float(np.mean(g == 3)), "gaps of an eighth": float(np.mean(g == 6)), "gaps of a quarter or more": float(np.mean(g >= 12)),
             "gaps of half a beat": float(np.mean(np.isclose(gb, 0.5))), "gaps of a third of a beat": float(np.mean(np.isclose(gb, 1 / 3))), "gaps of a beat or more": float(np.mean(gb >= 1)), "gaps under a third of a beat": float(np.mean(gb < 1 / 3 - 1e-9))}
        seen_r = set(); seen_f = set(); nr = nf = 0; byb = collections.defaultdict(list)                  # 864: how much of the song comes back
        for n in notes: byb[n["on"] // BAR].append((n["on"] % BAR, n["p"]))
        for k_ in sorted(byb):
            v = byb[k_]; rh = tuple(x for x, _ in v); fig = (rh, tuple(b_[1] - a_[1] for a_, b_ in zip(v, v[1:]))); nr += rh in seen_r; nf += fig in seen_f; seen_r.add(rh); seen_f.add(fig)
        r["bars on a rhythm already sung"] = nr / len(byb); r["bars on a figure already sung"] = nf / len(byb)
        return {k: v for k, v in r.items() if k in self.Q}
    def directed(self, notes):
        """863: readings with a direction known in advance, each made so that more is better. Surprise is each note's bits under the kept moves (given the move before where the
        table has pairs). 'low surprise': minus the mean, counted only above the kept lower quartile where the table gives one (too much is bad; a little too little is harmless).
        'sure endings': the mean surprise of a line's other notes less that of its last note (endings more predictable than their lines)."""
        ic = []; last = None; fin = []
        for a, b in zip(notes, notes[1:]):
            d = b["p"] - a["p"]; ic.append(-math.log2(max(1e-9, self.ivp(d, last)))); last = d; fin.append((a["sec"], a["line"]) != (b["sec"], b["line"]))
        if not ic: return {"low surprise": 0.0, "sure endings": 0.0}
        endn = [x for x, f in zip(ic[:-1], fin[1:] + [True]) if f] + [ic[-1]]; inner = [x for x, f in zip(ic[:-1], fin[1:] + [True]) if not f]; floor = self.T.get("surprise_quartiles", [None])[0]; m = float(np.mean(ic))
        return {"low surprise": -(max(m, floor) if floor else m), "sure endings": float(np.mean(inner) - np.mean(endn)) if inner and endn else 0.0}
    def charge(self, r):
        c = d = 0.0
        for k, (a, m, z) in self.Q.items():
            if k not in r: continue
            sp = ((z - a) or FLOOR(m)); d += abs(r[k] - m) / sp
            if k in UNCHARGED: continue
            c += max(0.0, a - r[k]) / sp + max(0.0, r[k] - z) / sp
        return c, d
    def gates(self, c):
        ns = c["notes"]; by = collections.defaultdict(list)
        for n in ns: by[(n["sec"], n["line"])].append(n)
        if any(n["dur"] <= 0 for n in ns) or any(b["on"] <= a["on"] for a, b in zip(ns, ns[1:])): return "751: two notes on one onset, or a note of no length"
        if any(not self.runs_ok([n["p"] for n in v]) for v in by.values()): return "a run of four of one pitch in a line (749.2)"
        med = lambda sec, lines=None: float(np.median([n["p"] for n in ns if n["sec"] == sec and (lines is None or n["line"] in lines)]))
        for gte in self.S.get("gates", []):
            if gte["type"] == "median above" and med(gte["a"], gte.get("a_lines")) < med(gte["b"]) + gte["by"]: return "design: " + gte["name"]
            if gte["type"] == "top only in" and (max(n["p"] for n in ns) != gte["pitch"] or any(n["p"] >= gte["pitch"] and [n["sec"], n["line"]] not in gte["lines"] for n in ns)): return "design: " + gte["name"]
            if gte["type"] == "plan lift":                                                    # 838: the chorus's median over the verse's within two semitones of the song's plan
                v_ = [n["p"] for n in ns if self.KIND[n["sec"]] == "Verse"]; c_ = [n["p"] for n in ns if self.KIND[n["sec"]] == "Chorus"]
                if v_ and c_ and abs(float(np.median(c_)) - float(np.median(v_)) - gte["lift"]) > gte.get("within", 2): return "838: the chorus's lift is not the plan's"
            if gte["type"] == "hook beat":                                                    # 840: the title's stressed syllables on a beat, half of them at least (kept 73 in 100)
                hk = set(self.S.get("hooks", ())); h_ = [n for n in ns if n["stress"] and f"{n['sec']}:{n['line']}" in hk]
                if h_ and float(np.mean([self.on_beat(n["on"]) for n in h_])) < gte.get("at_least", 0.5): return "840: the title's stresses off the beat"
            if gte["type"] == "cap" and any(n["p"] > gte["pitch"] for n in ns if n["sec"] == gte["section"] and n["line"] in gte["lines"]): return "design: " + gte["name"]
        st = [n for n in ns if n["stress"] and self.HOW.get((n["sec"], n["line"]), ["fresh"])[0] != "design"]
        if st and np.mean([self.on_beat(n["on"]) for n in st]) < self.S.get("stressed on the beat, at least", 0.4): return "731: stressed syllables on the beat too few"
        return None
    def run(self, N, seed):
        rng = random.Random(seed); deaths = collections.Counter(); alive = []
        for k in range(N):
            c, err = self.build(rng)
            if err: deaths[f"{err[0]}"] += 1; continue
            f = self.gates(c)
            if f: deaths[f] += 1; continue
            r = self.readings(c["notes"]); ch, dist = self.charge(r); c.update(readings=r, charge=ch, distance=dist, n=k)
            c["fp"] = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in c["notes"]]).encode()).hexdigest()[:12]; alive.append(c)
        if not alive: return dict(made=N, survivors=0, deaths=dict(deaths), stats=dict(self.stats))
        least = min(c["charge"] for c in alive); near = [c for c in alive if c["charge"] <= least + 0.05]; pick = min(near, key=lambda c: c["distance"]); old_pick = pick["fp"]; j7 = None
        if self.S.get("judge") == 7:                                                         # 860-863: the gate, the place a kept song usually stands, then readings whose direction is known
            try:
                import luthier_judge7 as J7; J = J7.Judge7(self.S.get("table") or self.S["metre"].replace("/", "-") + "_sung")
            except Exception as e_: J = None; j7 = {"not used": str(e_)}
            if J is not None:
                for c in alive: c["d7"] = J.distance(c["readings"]); c["directed"] = self.directed(c["notes"])
                ok = [c for c in alive if c["d7"] <= J.gate]; band = [c for c in ok if J.band[0] <= c["d7"] <= J.band[1]]; pool = band or ok or alive
                names = list(pool[0]["directed"]); rk = {}
                for n_ in names:
                    v = sorted(pool, key=lambda c: -c["directed"][n_])
                    for r_, c in enumerate(v): rk[(c["fp"], n_)] = r_
                score = lambda c: sum(rk[(c["fp"], n_)] for n_ in names) / len(names)
                short = sorted(pool, key=lambda c: (score(c), c["fp"]))[:5] if band else [min(pool, key=lambda c: (abs(c["d7"] - J.usual) if ok else c["d7"], c["fp"]))]
                pick = short[0]
                j7 = dict(kept_songs=J.n, readings_read_together=J.names, gate=round(J.gate, 3), a_kept_songs_usual_distance=round(J.usual, 3), kept_middle_half=[round(x, 3) for x in J.band], builds=len(alive), pass_the_gate=len(ok), in_the_kept_middle_half=len(band),
                          builds_distance_quartiles=[round(float(x), 3) for x in np.quantile([c["d7"] for c in alive], (0.25, 0.5, 0.75))], pick_distance=round(pick["d7"], 3), pick_directed=pick["directed"],
                          pool="the kept middle half" if band else "past the gate" if ok else "no build passed the gate: the least distance", shortlist=[dict(fp=c["fp"], distance=round(c["d7"], 3), old_charge=round(c["charge"], 3), **{k_: round(v_, 3) for k_, v_ in c["directed"].items()}) for c in short],
                          the_old_pick=dict(fp=old_pick, distance=round(next(c["d7"] for c in alive if c["fp"] == old_pick), 3), passes=bool(next(c["d7"] for c in alive if c["fp"] == old_pick) <= J.gate)), withheld_reading_old_charge_of_the_pick=round(pick["charge"], 3), the_old_pick_notes=[[n["on"], n["p"], n["sec"]] for n in next(c["notes"] for c in alive if c["fp"] == old_pick)])
        st = [n for n in pick["notes"] if n["stress"]]; E = {True: [0, 0, 0], False: [0, 0, 0]}
        for c in alive:
            first = {}
            for n in c["notes"]: first.setdefault((n["sec"], n["line"]), n)
            for (s, i), n in first.items():
                e = n["on"] - self.line_start(s, i); E[bool(n["stress"])][0 if e < 0 else 1 if e == 0 else 2] += 1
        order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
        return dict(title=self.S.get("title"), metre=self.S["metre"], seed=seed, made=N, survivors=len(alive), order=order, deaths=dict(deaths.most_common()), stats=dict(self.stats),
                    pick=dict(fp=pick["fp"], charge=round(pick["charge"], 3), distance=round(pick["distance"], 2), plans=pick["plans"], readings=pick["readings"], notes=pick["notes"],
                              stressed_on_beat=float(np.mean([self.on_beat(n["on"]) for n in st]))),
                    kept_quartiles=self.Q, uncharged=[k for k in UNCHARGED if k in self.Q], median_build={k: float(np.median([c["readings"][k] for c in alive])) for k in alive[0]["readings"]},
                    median_charge=float(np.median([c["charge"] for c in alive])), builds_with_no_charge=int(sum(c["charge"] == 0 for c in alive)),
                    entries={"stressed openings before / on / after": [round(x / max(1, sum(E[True])), 3) for x in E[True]], "unstressed openings before / on / after": [round(x / max(1, sum(E[False])), 3) for x in E[False]]},
                    judge7=j7, survivors_list=[dict(fp=c["fp"], charge=round(c["charge"], 4), distance=round(c["distance"], 3)) for c in alive])

class Hymn:
    """791, the hymn mode (749.11): one tune for every stanza, its rhythm set by the text's metre and the metre's kept hymn bars, read against hymn tunes of that metre.
    The frame: each stressed syllable on a downbeat, bar after bar; unstressed syllables before the first stress are pickups, a beat each, before the bar line;
    a bar holding a stressed syllable and the unstressed ones after it takes a kept hymn bar that begins on the downbeat: with one unstressed syllable, the bar's last
    beat is that syllable's and everything before it the stressed one's; with more, they take the bar's last onsets, one each. More onsets than syllables are slurs
    (weighted by 'slur_share', two slurred bars a line at most); a slur's second note moves a step. A line's last syllable is held to the next line's first note.
    A hymn bar that would lengthen the unstressed syllable past the stressed one cannot be drawn by this rule. Every reading is charged."""
    def __init__(self, spec):
        self.S = spec; m = spec["metre"]; T = json.load(open(os.path.join(ATLAS, m.replace("/", "-") + "_sung.json"))); H = json.load(open(os.path.join(ATLAS, "hymns.json")))["by_metre"][m]
        self.BAR, self.BEATS, self.BEAT = T["bar"], T["beats"], T["beat"]; self.Q = H["readings_quartiles"]; self.NH = H["hymns"] if not isinstance(H["hymns"], list) else len(H["hymns"])
        half = self.BAR // 2; two = H["stress"]["primary"].get("strong beat", 0) >= 0.25 and half in self.BEATS             # 792: where the kept hymns put a quarter of their stresses on the mid-bar beat, the frame's unit is half a bar
        self.CELL = half if two else self.BAR; self.PER = self.BAR // self.CELL; self.PULSE = self.BEAT if self.BEAT < self.CELL else self.CELL // 3; hb = collections.Counter()
        for pat, c in H["bar_rhythms"]:
            if any(x % 3 for x in pat): continue
            for q in range(self.PER):
                cell = tuple(x - q * self.CELL for x in pat if q * self.CELL <= x < (q + 1) * self.CELL)
                if cell and cell[0] == 0: hb[cell] += c
        self.HB = sorted(hb.items(), key=lambda x: (-x[1], x[0])); self.LB = max(-(-sum(l["stress"]) // self.PER) for sec in spec["tune"] for l in sec["lines"])
        self.IV = {int(k): v for k, v in T["intervals"].items()}; self.IVT = sum(self.IV.values()); self.SCALE = set(spec["scale"]); self.CH = {k: set(v) for k, v in spec["chords"].items()}
        self.LO, self.HI = spec["compass"]; self.LEAP = spec.get("leap_max", 7); self.SLUR = spec.get("slur_share", 0.4); self.ONLY = {int(k): set(v) for k, v in spec.get("only_over", {}).items()}
        self.stats = collections.Counter(); self.SEC = spec["tune"]; self.B0 = {}; b = 0
        for sec in self.SEC: self.B0[sec["name"]] = b; b += sum(l.get("bars", self.LB) for l in sec["lines"])
    def ivp(self, d): return (self.IV.get(max(-12, min(12, d)), 0) + 0.5) / self.IVT
    def options(self, g):
        """the kept hymn bars that can carry a stressed syllable and g - 1 unstressed ones: [(notes, weight)], a note = (offset, which syllable of the group, slurred to the next)"""
        out = []; u = g - 1
        for pat, c in self.HB:
            k = len(pat)
            if k < g: continue
            if u == 0:
                if k > 2: continue
                own = [list(pat)]
            elif u == 1:
                a = [x for x in pat if x < self.CELL - self.PULSE]; z = [x for x in pat if x >= self.CELL - self.PULSE]
                if not a or not z: continue
                own = [a, z]
            else: own = [list(pat[:k - u])] + [[x] for x in pat[k - u:]]
            if any(len(o) > 2 for o in own): continue
            notes = [(x, w, j + 1 < len(o)) for w, o in enumerate(own) for j, x in enumerate(o)]
            out.append((notes, c * (self.SLUR if k > g else 1.0), k > g))
        return out
    def rhythm_line(self, rng, sec, li):
        ln = sec["lines"][li]; st = ln["stress"]; n = len(st); b0 = sum(l.get("bars", self.LB) for l in sec["lines"][:li]) * self.PER; lead = st.index(1); out = []; C = self.CELL
        for j in range(lead): out.append([b0 * C - (lead - j) * self.PULSE, self.PULSE, j, False, False])
        k = lead; bar = b0; slurs = 0
        while k < n:
            g = 1
            while k + g < n and not st[k + g]: g += 1
            if k + g >= n and g == 1: break                                                  # the line's last syllable, stressed: held
            opts = [o for o in self.options(g) if slurs + sum(x[2] for x in o[0]) <= 2]                    # 811 (749.48): two slurs a line, counted as slurs
            if ln.get("plain") is not None and k in ln["plain"]: opts = [o for o in opts if not o[2]]
            if not opts: return None
            notes, w, sl = rng.choices(opts, [o[1] for o in opts])[0]; slurs += sum(x[2] for x in notes)
            for j, (x, which, slur) in enumerate(notes): out.append([bar * C + x, (notes[j + 1][0] if j + 1 < len(notes) else C) - x, k + which, which == 0, slur])
            k += g; bar += 1
        if k < n: out.append([bar * C, C, n - 1, True, False])
        return out
    def draw_line(self, rng, rh, chs, prev, rule):
        ps = []; pin = {int(a): b for a, b in rule.get("pin", {}).items()}; lo, hi = rule.get("lo", self.LO), rule.get("hi", self.HI)
        first_pin = min((j for j, x in enumerate(rh) if x[2] in pin and x[0] % self.CELL == 0), default=len(rh))
        for j, (on, d, k, st, sl) in enumerate(rh):
            name = chs[min(len(chs) - 1, max(0, on) // self.BAR)]; ct = self.CH[name]; strong = on % self.CELL == 0
            if k in pin and strong: ps.append(pin[k]); continue
            cands = [p for p in range(lo, hi + 1) if p % 12 in self.SCALE and (p % 12 not in self.ONLY or name in self.ONLY[p % 12])]
            if j == len(rh) - 1 and "end" in rule: cands = [p for p in cands if p % 12 in rule["end"]]
            if strong and rule.get("rise") and ps and j < first_pin:
                last_down = max((ps[i] for i, x in enumerate(rh[:j]) if x[0] % self.CELL == 0), default=lo); cands = [p for p in cands if p >= last_down]
            ref = ps[-1] if ps else prev
            if j and rh[j - 1][4]: cands = [p for p in cands if 1 <= abs(p - ref) <= 2]         # a slur's second note: a step
            if not cands: return None
            w = [self.ivp(p - ref) * ((6.0 if p % 12 in ct else 0.05) if strong else (1.5 if p % 12 in ct else 1.0)) for p in cands]; ps.append(rng.choices(cands, w)[0])
        if any(abs(b - a) > self.LEAP for a, b in zip(ps, ps[1:])) or not Engine.runs_ok(ps): return None
        for a, b in rule.get("count", {}).items():
            if sum(p == int(a) for p in ps) != b: return None
        byk = {}
        for (on, d, k, st, sl), p in zip(rh, ps): byk.setdefault(k, p)
        for pr in rule.get("pairs", []):
            dlt = byk[pr["b"]] - byk[pr["a"]]
            if not (pr["min"] <= dlt <= pr["max"]): return None
        if "end_leap_max" in rule and abs(ps[-2] - ps[-1]) > rule["end_leap_max"]: return None
        return ps
    def build(self, rng):
        tune = []
        for sec in self.SEC:
            prev = sec["start"]; lines = []
            for li, ln in enumerate(sec["lines"]):
                rh = self.rhythm_line(rng, sec, li)
                if rh is None: return None, f"rhythm: {sec['name']} line {li + 1}"
                ps = None
                for _ in range(30):
                    ps = self.draw_line(rng, rh, sec["chords"], prev, ln.get("rule", {}))
                    if ps is not None: break
                if ps is None: return None, f"pitch: {sec['name']} line {li + 1}"
                lines.append([dict(on=self.B0[sec["name"]] * self.BAR + on, dur=d, syl=k, stress=bool(st), slur=bool(sl), p=p, sec=sec["name"], line=li) for (on, d, k, st, sl), p in zip(rh, ps)]); prev = ps[-1]
            tune += lines
        flat = [n for ln in tune for n in ln]
        for a, b in zip(flat, flat[1:]):
            if a["line"] != b["line"] or a["sec"] != b["sec"]: a["dur"] = max(self.BEAT, min(b["on"] - a["on"], 2 * self.BAR - self.BEAT))     # held to the next line's first note
        flat[-1]["dur"] = 2 * self.BAR - self.BEAT
        return flat, None
    def readings(self, ns):
        E = Engine.__new__(Engine); E.BAR, E.BEATS, E.BEAT, E.Q = self.BAR, self.BEATS, self.BEAT, self.Q; E.on_beat = lambda t: (t % self.BAR) in self.BEATS
        r = Engine.readings(E, ns); r["notes a beat"] = r["notes a bar"] / len(self.BEATS); return r
    def run(self, N, seed):
        rng = random.Random(seed); alive = []; deaths = collections.Counter()
        for k in range(N):
            t, err = self.build(rng)
            if err: deaths[err] += 1; continue
            if any(b["on"] <= a["on"] for a, b in zip(t, t[1:])) or any(n["dur"] <= 0 for n in t): deaths["751: two notes on one onset, or a note of no length"] += 1; continue
            r = self.readings(t); c = d = 0.0
            for q, (a, m, z) in self.Q.items():
                sp = ((z - a) or FLOOR(m)); d += abs(r[q] - m) / sp; c += max(0.0, a - r[q]) / sp + max(0.0, r[q] - z) / sp
            alive.append(dict(notes=t, readings=r, charge=c, distance=d, n=k, fp=hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in t]).encode()).hexdigest()[:12]))
        if not alive: return dict(made=N, survivors=0, deaths=dict(deaths), stats={})
        least = min(a["charge"] for a in alive); near = [a for a in alive if a["charge"] <= least + 0.05]; pick = min(near, key=lambda a: a["distance"])
        sy = [n for n in pick["notes"] if n["stress"]]
        return dict(title=self.S.get("title"), metre=self.S["metre"], mode="hymn", hymns_read_against=self.NH, seed=seed, made=N, survivors=len(alive), order=hashlib.sha1("".join(a["fp"] for a in alive).encode()).hexdigest()[:12],
                    deaths=dict(deaths.most_common()), stats=dict(self.stats), kept_quartiles=self.Q, uncharged=[], median_charge=float(np.median([a["charge"] for a in alive])), builds_with_no_charge=int(sum(a["charge"] == 0 for a in alive)),
                    median_build={k: float(np.median([a["readings"][k] for a in alive])) for k in alive[0]["readings"]}, entries={},
                    pick=dict(fp=pick["fp"], charge=round(pick["charge"], 3), distance=round(pick["distance"], 2), readings=pick["readings"], notes=pick["notes"], stressed_on_beat=float(np.mean([n["on"] % self.CELL == 0 for n in sy])), frame_unit=self.CELL),
                    survivors_list=[dict(fp=a["fp"], charge=round(a["charge"], 4), distance=round(a["distance"], 3)) for a in alive])

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 1000; seed = int(sys.argv[3]) if len(sys.argv) > 3 else spec.get("seed", 20261118)
    out = (Hymn(spec) if spec.get("mode") == "hymn" else Engine(spec)).run(N, seed); json.dump(out, open(sys.argv[1].replace(".json", "") + ".run.json", "w"), default=float)
    print(f"{out.get('title')} in {spec['metre']}: built {out['made']}, survivors {out['survivors']}, order {out.get('order')}; deaths {out['deaths']}")
    if out["survivors"]:
        pk = out["pick"]; print("pick", pk["fp"], "charge", pk["charge"], "distance", pk["distance"], "| median build's charge", round(out["median_charge"], 3), "| entries", out["entries"]); print("stats", out["stats"])
        for k, v in pk["readings"].items():
            a, m, z = out["kept_quartiles"][k]; print(f"  {k}: {round(v, 3)} (kept {round(a, 3)}, {round(m, 3)}, {round(z, 3)}){' *' if not (a <= v <= z) else ''}{' (not charged)' if k in out['uncharged'] else ''}")
