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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import word_weight as WW_
HERE = os.path.dirname(os.path.abspath(__file__)); ATLAS = os.path.join(HERE, "..", "..", "tables", "metre_atlas")
ENTRY = {True: (0.20, 0.42, 0.38), False: (0.43, 0.10, 0.47)}          # 771: before, on, after the bar line, by the first syllable's stress
UNCHARGED = ("notes a bar", "notes a beat", "gaps of a sixteenth", "gaps of an eighth", "gaps of a quarter or more", "gaps of half a beat", "gaps of a third of a beat",
             "gaps of a beat or more", "gaps under a third of a beat", "range", "distinct pitches")   # set by the lyric's density and the designs: printed, not charged

def FLOOR(m): return 0.02 if m <= 1.5 else 1.0          # 793, as mended by 810 (749.47): ONLY where the kept songs all read alike is the width two points of share, or one count

class Engine:
    def __init__(self, spec):
        self.S = spec; T = json.load(open(os.path.join(ATLAS, (spec.get("table") or spec["metre"].replace("/", "-") + "_sung") + ".json"))); self.T = T      # 812: a spec may name its kept table
        self.BAR, self.BEATS = T["bar"], T["beats"]; self.BEAT = T["beat"] or min(b - a for a, b in zip(self.BEATS, self.BEATS[1:] + [self.BAR]))   # uneven metres: the shortest beat
        self.END, self.REST = 6, 12; self.rest_now = 12; self.BREATH = self.END + self.REST          # 844 (749.53; amends 770, 832): a line's last note is an eighth at least (kept 5th percentile) and a quarter's rest follows (kept 10th), in every metre
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
        self.SUNGB = {id(self.LINES[s_][i_]): b_ for s_, v_ in (spec.get("sung_bars") or {}).items() for i_, b_ in enumerate(v_)}; self._part = False      # trial (749.226)
        self.TENTRY = set(spec.get("title_entry") or ()); self._made = {}; self.RESTB = {id(self.LINES[k_.rsplit(":", 1)[0]][int(k_.rsplit(":", 1)[1])]): v_ for k_, v_ in (spec.get("title_entry_rest") or {}).items()}      # trial (749.232 changed)
        self.KEYS = [(s, i) for s in self.SUNG for i in range(len(self.LINES[s]))]; self.HOW = {tuple(k.rsplit(":", 1)): v for k, v in spec.get("how", {}).items()}
        self.HOW = {(s, int(i)): v for (s, i), v in self.HOW.items()}; self.stats = collections.Counter()
        self._runin = None; self.AIM = False; self.RUN = 3; self.RUNP = 2; self.MV = (1.0, 1.0, 50.0, 1.0)                                                # 926, 927
        self.TILT = None; tg = spec.get("target")                                               # 920 (749.94): the song is aimed at one kept song, not at the kept middle
        if tg:
            Q2 = dict(self.Q); t_ = tg["readings"]
            for k_ in tg.get("charged", ("repeated notes", "moves by step", "moves by leap")):
                if k_ in t_ and k_ in Q2: a_, m_, z_ = Q2[k_]; Q2[k_] = [t_[k_] - (m_ - a_), t_[k_], t_[k_] + (z_ - m_)]      # the charge's middle half, of the kept width, set about the kept song's own reading
            g_ = tg.get("power", 1.0); cl_ = lambda x: max(0.4, min(2.5, x)); self.Q = Q2; self.RUN = int(tg.get("run", 3)); self.AIM = True; self.RUNP = self.RUN; mv_ = tg.get("moves") or {}; self.MV = (float(mv_.get("step", 1.0)), float(mv_.get("leap", 1.0)), float(mv_.get("spread", 50.0)), float(mv_.get("repeat", 1.0)))
            self.TILT = tuple(cl_(((t_[k_] + 0.02) / (self.T["readings_quartiles"][k_][1] + 0.02)) ** g_) for k_ in ("repeated notes", "moves by step", "moves by leap"))
        self._rc = {}; self.ALLW = None
        if spec.get("all_windows") and T.get("two_bar_windows_all"):                             # 912: every kept rhythm may be drawn, at its kept share
            B_ = collections.defaultdict(list)
            for p_, c_ in T["bar_rhythms_all"]: B_[len(p_)].append((tuple(p_), c_))
            self.ALLW = ({int(k): [(tuple(p_), c_) for p_, c_ in v] for k, v in T["two_bar_windows_all"].items()}, B_)
        self.ENTRY = ENTRY; self.LE = None; self.gap_now = 12                                                     # 899 (749.76, 749.80): how kept lines end: the last syllable's length and the rest after it drawn together
        if spec.get("line_ends"):
            K_ = json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_line_ends.json"))); C_ = np.array(K_["counts_by_tier_G_D"], float); self.LE = dict(GV=K_["G_values"], DV=K_["D_values"], C=C_, Gw=[float(x) for x in C_.sum((0, 2))])
            if K_.get("entries_before_on_after_the_bar_line"): e_ = K_["entries_before_on_after_the_bar_line"]; self.ENTRY = {True: tuple(e_["stressed"]), False: tuple(e_["unstressed"])}      # 911 (749.89): 771's shares read from the kept table, tie starts read
        pg = spec.get("page_gate"); self.PG = None; self._figs = None                         # 922, 923 (Window 188): the page gate, a floor; and the tune's own short figures sung again
        if pg:
            import page_gate as PG_; self.PG = dict(T=PG_.table(), floor=pg.get("floor"), memory=float(pg.get("memory", 1.0)), mod=PG_)
        ww = spec.get("word_weight"); self.WW = None                                          # 879-881 (way 3): what the kept songs do with a word's weight
        if ww:
            K = WW_.table(); self.WW = dict(place=[[math.log(max(1e-4, K["place_share_by_tier"][a][j]) / K["place_share_all"][j]) for j in range(5)] for a in range(3)], pp=ww.get("place", 1.0), sp=ww.get("step", 1.0), gate=ww.get("gate"), cost=ww.get("again_cost", 1.0), fresh=ww.get("fresh", True), again=ww.get("again", True), lp=ww.get("length", 0.0), last=ww.get("last_note", False), short=ww.get("short_stress", 0.0),
                                            length=[[math.log(max(1e-4, K["length_share_by_tier"][a][j]) / K["length_share_all"][j]) for j in range(6)] for a in range(3)], fin=(K["last_note_lengths_twelfths"], K["last_note_length_share_by_tier"]),
                                            step=[[[K["step_down_level_up_from_tier_to_tier"][a][b][d] / K["step_down_level_up_all"][d] for d in range(3)] for b in range(3)] for a in range(3)])
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
        R = self.S["registers"]; r = tuple(R.get(f"{sec}:{i}") or R.get(sec) or R[self.KIND[sec]])
        lh = getattr(self, "_lh", None)                                                      # 749.201, a trial form (studies/line_heights): a line drawn about its own centre, the part's centre moved by the line's height in a kept contour
        if lh and f"{sec}:{i}" not in R and (sec, i) in lh: r = (max(r[1] + 2, min(r[2] - 2, r[0] + lh[(sec, i)])),) + r[1:]
        return r
    def draw_heights(self, rng):
        """749.201: for each sung part, one kept part's line heights (tables/kept_line_heights.json), of the same kind and the same number of lines where ten or more kept parts have it, else any of the kind read by place"""
        if not hasattr(self, "_LH"): self._LH = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tables", "kept_line_heights.json")))["contours"]
        out = {}
        for sec in self.SUNG:
            C = self._LH.get(self.KIND.get(sec)); n = len(self.LINES[sec])
            if not C or n < 2: continue
            same = [c for c in C if len(c) == n]; c = rng.choice(same if len(same) >= 10 else C)
            for i in range(n): out[(sec, i)] = c[i] if len(c) == n else c[int(round(i * (len(c) - 1) / (n - 1)))]
        return out
    def ivp(self, d, last=None):
        d = max(-12, min(12, d)); row = self.IV2.get(max(-12, min(12, last))) if last is not None else None
        if row and sum(row.values()) >= 50: return (row.get(d, 0) + 12.5 * (self.IV.get(d, 0) + 0.5) / self.IVT) / (sum(row.values()) + 12.5)
        return (self.IV.get(d, 0) + 0.5) / self.IVT
    # ---- rhythm
    def stress_score(self, ons, sy, table=None):
        sc = 0.0
        if self.WW and (self.WW["fresh"] if table is None else table):                                                                           # 879: each syllable's place in the bar scored by where kept songs sing a syllable of its weight (function word, weak syllable, stressed), over where they sing any
            tr_ = WW_.tier(sy)
            for t, a in zip(ons, tr_): sc += self.WW["pp"] * self.WW["place"][a][WW_.place(t, self.BAR, self.BEAT)]
            if self.WW["lp"]:                                                                 # 885: and the time each syllable is given before the next, by where kept songs give a syllable of its weight that long
                for k_ in range(len(ons) - 1): g_ = ons[k_ + 1] - ons[k_]; sc += self.WW["lp"] * self.WW["length"][tr_[k_]][0 if g_ <= 3 else 1 if g_ <= 6 else 2 if g_ <= 9 else 3 if g_ <= 12 else 4 if g_ <= 18 else 5]
            sc += self.weak_end(ons, sy)
            return sc
        sp_ = self.S.get("stress_place")
        if sp_:
            # trial (749.231): each syllable's place scored by where kept songs of this metre sing a syllable of its weight, over where they sing any (879's rule; the bar's first beat, another beat, off the beat)
            for t, (_, st) in zip(ons, sy): sc += sp_["weight"] * sp_["place"]["primary" if st else "unstressed"]["downbeat" if t % self.BAR == 0 else "beat" if self.on_beat(t) else "off the beat"]
            return sc + self.weak_end(ons, sy)
        for t, (_, st) in zip(ons, sy):
            b = t >= 0 and self.on_beat(t)
            sc += (1.5 if b else -0.6) if st else (-0.8 if (b and t % self.BAR == 0) else 0.0)
        if sy[-1][1] and not self.on_beat(ons[-1]): sc -= 1.0
        sc += self.weak_end(ons, sy)      # 871 (749.64): a line ending on a word's weak syllable gives the stressed one a quarter at least
        return sc
    def weak_end(self, ons, sy):
        """871 (749.64), widened by 890 (749.71): a line ending on a word's weak syllables gives that word's stressed syllable a quarter at least, whatever the word's length"""
        if len(sy) < 2 or sy[-1][1] or self.LE: return 0.0                                    # 901 (749.78): retired where the kept line ends stand: kept singers hold the weak syllable longer than the stressed one at 47 line ends in 100 (619 of them)
        j = len(sy) - 1
        while j > 0 and sy[j - 1][0] == sy[-1][0] and not sy[j][1]: j -= 1
        if j == len(sy) - 1 or not sy[j][1] or sy[j][0] != sy[-1][0]: return 0.0
        return 1.5 if ons[j + 1] - ons[j] >= 12 else -1.5
    def kept_windows(self, n, bars):
        if bars == 2: return self.WIN.get(n, [])
        if bars == 1: return self.BARS.get(n, [])
        return []
    def rhythm(self, rng, sy, tmin, slot, cap=None, hook=False, room=None):
        if self.RESTB and id(sy) in self.RESTB and not self._part and slot == self.RESTB[id(sy)][1] * self.BAR: slot = max(2, self.RESTB[id(sy)][0]) * self.BAR      # trial (749.232 changed): the line ahead of a title line is drawn in its sung bars; the bar more is rest
        if slot in (3 * self.BAR, 4 * self.BAR) and self.SUNGB.get(id(sy)) in (3, 4) and len(sy) >= 4:
            # trial (749.226): a four-bar phrase read as two windows; three sung bars are a two-bar window and a one-bar rhythm, the fourth bar left to the hold or the rest
            sb_ = self.SUNGB[id(sy)]; n1_ = (len(sy) + 1) // 2 if sb_ == 4 else int(round(2 * len(sy) / 3.0)); self._part = True
            try:
                a_ = self.rhythm(rng, sy[:n1_], tmin, 2 * self.BAR, hook=hook, room=3); b_ = self.rhythm(rng, sy[n1_:], 0, 2 * self.BAR if sb_ == 4 else self.BAR, None if cap is None else cap - 2 * self.BAR, hook=hook, room=None if (sb_ == 4 or slot == 3 * self.BAR) else 0) if a_ is not None else None
            finally: self._part = False
            if a_ is None or b_ is None or b_[0] < 0: return None
            self.stats["749.226: a four-bar phrase in two windows"] += 1; return list(a_) + [x_ + 2 * self.BAR for x_ in b_]
        n = len(sy); lead = 0
        for x in sy:
            if x[1]: break
            lead += 1
        room_ = (12 if self.LE else self.BREATH) if room is None else room; end = slot - room_ if cap is None else min(slot - room_, cap); out = []; bars = slot // self.BAR; early = []
        if bars == 2 and not self._part and self.S.get("one_bar_share") and rng.random() < self.S["one_bar_share"]:      # 876: the line sung in one bar of its two and the voice silent for the other, as kept songs leave whole bars empty
            o1 = self.rhythm(rng, sy, tmin, self.BAR, cap=min(self.BAR - self.END, cap if cap is not None else 10 ** 6), hook=hook) if n <= 10 else None
            if o1 is not None and o1[-1] < self.BAR - self.END + 1 and self.stats is not None:
                if o1[-1] <= self.BAR - self.END: self.stats["876: a line sung in one bar, the next bar silent"] += 1; return o1
        if self.ALLW and bars in (1, 2):                                                      # 912: the scores of every kept rhythm for this line are worked once and kept; no cut to the twelve best
            key_ = (id(sy), bars, hook)
            if key_ not in self._rc:
                M_ = []; E_ = []
                for p in sorted({0, min(1, lead), min(2, lead)}):
                    for w, c in (self.ALLW[0].get(n - p, []) if bars == 2 else self.ALLW[1].get(n - p, [])):
                        if w[0] != 0 and p > 0: continue
                        ons = [-6 * (p - j) for j in range(p)] + list(w); e = self.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]
                        M_.append((ons[0], w[-1], ons, math.log(c) + (2.8 if hook else 1.4) * self.stress_score(ons, sy) + math.log(e)))
                        if p == 0 and sy[0][1] and w[0] == 0 and self.S.get("early_entries"):
                            for sh in (6, 12): E_.append((w[0] - sh, w[-1], [x - sh for x in w], math.log(c) + 1.4 * self.stress_score(list(w), sy)))
                self._rc[key_] = (M_, E_)
            M_, E_ = self._rc[key_]; out = [(o, s_) for f, l, o, s_ in M_ if l <= end and f >= tmin]; early = [(o, s_) for f, l, o, s_ in E_ if l <= end and f >= tmin]
            if early and rng.random() < self.ENTRY[True][0]: out = early; self.stats["834: a stressed opening sung before the bar line"] += 1
            if out:
                top_ = max(s_ for _, s_ in out); self.stats["653: a line in a kept window"] += 1; return list(rng.choices([o for o, _ in out], [math.exp(s_ - top_) for _, s_ in out])[0])
            o = self.weighted(rng, sy, tmin, end)
            if o is not None: self.stats["760: a line set by the weighted rule"] += 1
            return o
        for p in sorted({0, min(1, lead), min(2, lead)}):
            for w, c in self.kept_windows(n - p, bars):
                if w[-1] > end or (w[0] != 0 and p > 0): continue
                ons = [-6 * (p - j) for j in range(p)] + list(w)
                if ons[0] < tmin: continue
                e = self.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]
                out.append((ons, math.log(c + 1) + (2.8 if hook else 1.4) * self.stress_score(ons, sy) + math.log(e)))        # 840: the title line's stresses pulled twice as hard to the beat
                if p == 0 and sy[0][1] and w[0] == 0 and self.S.get("early_entries"):               # 834: a line that opens on a stress may sing its kept window an eighth or a quarter early
                    for sh in (6, 12):
                        o2 = [x - sh for x in w]
                        if o2[0] >= tmin: early.append((o2, math.log(c + 1) + 1.4 * self.stress_score([x for x in w], sy)))
        if early and rng.random() < self.ENTRY[True][0]: out = early; self.stats["834: a stressed opening sung before the bar line"] += 1      # the entry's class first, at the kept share (771)
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
        if self.WW and self.WW["fresh"]:                                                      # 879: the rule's places too, by the syllable's weight
            tr = WW_.tier(sy); entry_st = st[0]; st = tr
            def pw(t, a): return self.OW.get(t % self.BAR, 0.002) * math.exp(self.WW["pp"] * self.WW["place"][a][WW_.place(t, self.BAR, self.BEAT)])
        else: entry_st = st[0]
        def gw(g): return (self.DUR.get(g, 0) + 1.0) / self.DT
        B = [[0.0] * m for _ in range(n)]
        for j in range(m): B[n - 1][j] = 1.0
        for k in range(n - 2, -1, -1):
            for j in range(m):
                B[k][j] = sum(gw(P[j2] - P[j]) * pw(P[j2], st[k + 1]) * B[k + 1][j2] for j2 in range(j + 1, m) if P[j2] - P[j] < cap)
        w0 = [pw(P[j], st[0]) * B[0][j] for j in range(m)]; cl = [0 if P[j] < 0 else 1 if P[j] == 0 else 2 for j in range(m)]
        if sum(w0) <= 0: return None
        mass = [sum(w for w, c in zip(w0, cl) if c == q) for q in range(3)]; q = rng.choices(range(3), [self.ENTRY[entry_st][q] if mass[q] > 0 else 0 for q in range(3)])[0]   # 771: the entry's class at the kept share, then the place
        w0 = [w if c == q else 0.0 for w, c in zip(w0, cl)]
        j = rng.choices(range(m), w0)[0]; out = [P[j]]
        for k in range(n - 1):
            c = [(j2, gw(P[j2] - P[j]) * pw(P[j2], st[k + 1]) * B[k + 1][j2]) for j2 in range(j + 1, m) if P[j2] - P[j] < cap]; c = [x for x in c if x[1] > 0]
            if not c: return None
            j = rng.choices([x[0] for x in c], [x[1] for x in c])[0]; out.append(P[j])
        return out
    # ---- pitches
    def pitches(self, rng, ons, U, sec, i, prev, avoid=None, end_off=None):
        # 950 (749.111): the song's peak planted as a note. The range the song's words ask is a top the draw seldom climbs to, so the builds spanned 14 or 15 semitones where 18 to 20 were asked.
        # Each fresh chorus line in turn keeps its own centre, has its top set to the peak (the floor plus the asked range, inside the parts' tops, on the scale) and is redrawn, 60 times at most,
        # until its highest stressed note is the peak; the first line that reaches it carries it. (studies/plant_the_peak, sixth trial.)
        pk = (self.S.get("target") or {}).get("peak")
        if not pk or getattr(self, "_peaked", True) or self.KIND.get(sec) != "Chorus": return self.pitches1(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
        R = self.S["registers"]; P = int(min(min(R[x][1] for x in ("Verse", "Chorus")) + round(pk["range"]), max(R[x][2] for x in ("Verse", "Chorus", "Bridge") if x in R)))
        while P % 12 not in self.SCALE: P -= 1
        key = f"{sec}:{i}"; had = R.get(key); base = self.reg(sec, i); R[key] = [base[0], base[1], P]; ps = None
        old_ = None                                                                           # 749.182, trial forms (studies/the_draw). climb: the carrying line holds no leap past an octave. "fallback": and where the song's last fresh chorus line cannot climb, the peak is planted the old way
        try:
            for _ in range(pk.get("tries", 60)):
                ps = self.pitches1(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off)
                if ps and max(ps) == P and any(q == P and self.LINES[sec][i][j][1] for j, q in enumerate(ps)):
                    if not pk.get("climb") or all(abs(b_ - a_) <= 12 for a_, b_ in zip(ps, ps[1:])): self._peaked = True; self.stats["950: the peak planted in a chorus line"] += 1; break
                    if old_ is None: old_ = ps
            else:
                if pk.get("climb") == "line" and old_ is not None:                              # third form: the way back in the carrying line itself. A climbing draw if any of the 60 climbs, else the first that reached the peak
                    ps = old_; self._peaked = True; self.stats["950: the peak planted in a chorus line"] += 1; self.stats["950: planted the old way, this line could not climb"] += 1
                elif pk.get("climb") == "fallback" and old_ is not None and (sec, i) == next((k_ for k_ in reversed(self.KEYS) if self.KIND.get(k_[0]) == "Chorus" and self.HOW.get(k_, ["fresh"])[0] == "fresh"), None):
                    ps = old_; self._peaked = True; self.stats["950: the peak planted in a chorus line"] += 1; self.stats["950: planted the old way, the last chorus line could not climb"] += 1
        finally:
            if had is None: R.pop(key, None)
            else: R[key] = had
        return ps
    def pitches1(self, rng, ons, U, sec, i, prev, avoid=None, end_off=None):
        mu, lo, hi = self.reg(sec, i); ps = []; last = None; sy = self.LINES[sec][i]
        DG = self.S.get("degrees"); DW = (DG["weights"].get(self.KIND[sec]) or DG["weights"]["all"]) if DG else None; ton = DG["tonic"] if DG else 0; blue = set(DG.get("blue", ())) if DG else set()
        WP = self.S.get("word_pitch"); TR = WW_.tier(sy) if (self.WW and self.WW["sp"]) else None
        for k, t in enumerate(ons):
            ch = self.chord_at(U + t); cands = [p for p in range(lo, hi + 1) if (p % 12 in self.SCALE or (p - ton) % 12 in blue) and not (avoid and p % 12 in avoid)]; ws = []
            long_ = k == len(ons) - 1 or ons[k + 1] - t >= self.BEAT
            if self.S.get("clash_rule") and (long_ or not ch <= self.SCALE):                     # 808: over a chord from outside the key; 833: and under any chord on a note a beat long or more:
                c2 = [p for p in cands if p % 12 in ch or (p - ton) % 12 in blue or not ((p + 1) % 12 in ch or (p - 1) % 12 in ch)]       # no tone a semitone from a chord tone, unless a chord tone (846: or a blue note, which kept songs sing over the major third)
                cands = c2 or cands
            OT_ = self.S.get("octave_tail") if prev is not None else None                       # 964 (749.192; studies/the_peak_line): the table's +12 and -12 bins hold every interval of an octave or more, and ivp() gave the whole bin to each such pitch.
            nb_ = {1: sum(1 for q in cands if q - prev > 12), -1: sum(1 for q in cands if prev - q > 12)} if OT_ else None      # With the form on the bin is shared: the octave takes its kept share of it and the pitches past it share the rest. Where a rule has removed the octave itself, its share is not passed on (749.196: counted at 10 to 19 notes in a thousand, and left so on purpose: the pitches past it keep their own kept odds)
            if OT_ and self.S.get("count_the_tail"):                                            # 749.196, for studies/song50_pool only: how often a side has pitches past the octave and no octave
                self._tail_n = getattr(self, "_tail_n", 0) + 1; self._tail_no_octave = getattr(self, "_tail_no_octave", 0) + sum(1 for sd_ in (1, -1) if nb_[sd_] and (prev + 12 * sd_) not in cands)
            LO_ = self.S.get("ladder_off")                                                      # 749.203, for studies/ladder only: the draw with named parts left out. Absent from every record; with it absent nothing here is reached
            for p in cands:
                if LO_ is not None: ws.append(self.ladder_weight(LO_, p, prev, last, mu, ch, U + t, ps, k, sy, DW, ton, WP, TR, OT_, nb_, end_off, len(ons))); continue
                w = self.ivp(p - prev, last) if prev is not None else math.exp(-abs(p - mu) / 3)
                if k == 0 and prev is not None and self.S.get("join_moves"): jm_ = self.S["join_moves"]; jm_ = jm_.get(self.KIND.get(sec)) or jm_["all"]; w = (jm_.get(str(max(-12, min(12, p - prev))), 0) + 0.5) / (sum(jm_.values()) + 12.5)      # 749.216, a trial (studies/borrow_kept), off: a fresh line's first note by the kept moves across a join. Absent from every record
                if OT_ and abs(p - prev) >= 12:
                    sd_ = 1 if p > prev else -1; sh_ = OT_["up" if sd_ > 0 else "down"]["octave_share"]; w *= sh_ if abs(p - prev) == 12 else (1 - sh_) / nb_[sd_]
                if "chord_tie" in self.S: w *= (self.S["chord_tie"]["on" if self.on_beat(U + t) else "off"] if p % 12 in ch else 1.0)      # 749.198, a trial form (studies/chord_tie): a chord tone favoured by the kept odds, on the beat and off it
                else: w *= (2.6 if p % 12 in ch else 0.3) if self.on_beat(U + t) else (1.3 if p % 12 in ch else 0.8)
                if "chord_pull" in self.S: w = w / ((2.6 if p % 12 in ch else 0.3) if self.on_beat(U + t) else (1.3 if p % 12 in ch else 0.8)) * ((2.6 if p % 12 in ch else 0.3) if self.on_beat(U + t) else (1.3 if p % 12 in ch else 0.8)) ** self.S["chord_pull"]      # for studies/one_pitch_verses only: the chord's pull at another strength
                w *= math.exp(-((p - mu) ** 2) / self.MV[2])                                         # 927: how closely a line keeps to its register
                if prev is not None and (self.MV[0] != 1.0 or self.MV[1] != 1.0 or self.MV[3] != 1.0): d0_ = abs(p - prev); w *= self.MV[0] if 1 <= d0_ <= 2 else self.MV[1] if d0_ >= 5 else self.MV[3] if d0_ == 0 else 1.0      # 936 (749.113): and a repeated note
                rn_ = 0
                for q_ in reversed(ps):
                    if q_ != p: break
                    rn_ += 1
                if rn_ == len(ps) and self._runin and self._runin[0] == p: rn_ += self._runin[1]              # the run carried in from the line before
                if rn_ >= self.RUNP: w = 0.0                # 926 (749.99): a pitch repeats no longer than the kept song's longest run (as before, where the song has no aim)
                if self._figs:                                                                    # 923: a note that completes a four-interval figure the song has already sung is favoured
                    tl = (self._figs[1] + ps)[-4:]
                    if len(tl) == 4 and tuple(max(-12, min(12, b_ - a_)) for a_, b_ in zip(tl, tl[1:] + [p])) in self._figs[0]: w *= self.PG["memory"]
                if self.TILT and prev is not None: d_ = abs(p - prev); w *= self.TILT[0] if d_ == 0 else self.TILT[1] if d_ <= 2 else self.TILT[2] if d_ >= 5 else 1.0      # 920: repeats, steps and leaps leaned toward the kept song's shares
                if DW: w *= DW.get(str((p - ton) % 12), 0.0)                                      # 846: the kept share of each degree of the scale, blue notes among them
                if WP and k > 0 and k < len(sy) and sy[k][0] == sy[k - 1][0] and sy[k][1] != sy[k - 1][1] and prev is not None:      # 847: inside a word, the stressed syllable against the other
                    up = (p > prev) if sy[k][1] else (p < prev); w *= WP[1] if p == prev else WP[0] if up else WP[2]
                elif TR and k > 0 and k < len(sy) and sy[k][0] != sy[k - 1][0] and prev is not None:                                  # 880: between two words, the step's direction at the kept share for their weights, over the kept share for any two
                    w *= self.WW["step"][TR[k - 1]][TR[k]][0 if p < prev else 1 if p == prev else 2] ** self.WW["sp"]
                if k == len(ons) - 1 and end_off is not None and p % 12 == end_off: w *= 0.05
                ws.append(w)
            if sum(ws) <= 0: return None
            p = rng.choices(cands, ws)[0]; last = (p - prev) if prev is not None else None; ps.append(p); prev = p
        return ps
    def ladder_weight(self, OFF, p, prev, last, mu, ch, at, ps, k, sy, DW, ton, WP, TR, OT_, nb_, end_off, n):
        """749.203 (studies/ladder): pitches1's weight for one candidate with the parts named in OFF left out: register, chord, moves, runs, memory, degrees, words, end_off. The kept intervals and fix 964 always stand."""
        w = self.ivp(p - prev, last) if prev is not None else (math.exp(-abs(p - mu) / 3) if "register" not in OFF else 1.0)
        if OT_ and abs(p - prev) >= 12:
            sd_ = 1 if p > prev else -1; sh_ = OT_["up" if sd_ > 0 else "down"]["octave_share"]; w *= sh_ if abs(p - prev) == 12 else (1 - sh_) / nb_[sd_]
        if "chord" not in OFF: w *= (2.6 if p % 12 in ch else 0.3) if self.on_beat(at) else (1.3 if p % 12 in ch else 0.8)
        if "register" not in OFF: w *= math.exp(-((p - mu) ** 2) / self.MV[2])
        if "moves" not in OFF and prev is not None and (self.MV[0] != 1.0 or self.MV[1] != 1.0 or self.MV[3] != 1.0): d0_ = abs(p - prev); w *= self.MV[0] if 1 <= d0_ <= 2 else self.MV[1] if d0_ >= 5 else self.MV[3] if d0_ == 0 else 1.0
        if "runs" not in OFF:
            rn_ = 0
            for q_ in reversed(ps):
                if q_ != p: break
                rn_ += 1
            if rn_ == len(ps) and self._runin and self._runin[0] == p: rn_ += self._runin[1]
            if rn_ >= self.RUNP: w = 0.0
        if "memory" not in OFF and self._figs:
            tl = (self._figs[1] + ps)[-4:]
            if len(tl) == 4 and tuple(max(-12, min(12, b_ - a_)) for a_, b_ in zip(tl, tl[1:] + [p])) in self._figs[0]: w *= self.PG["memory"]
        if "moves" not in OFF and self.TILT and prev is not None: d_ = abs(p - prev); w *= self.TILT[0] if d_ == 0 else self.TILT[1] if d_ <= 2 else self.TILT[2] if d_ >= 5 else 1.0
        if "degrees" not in OFF and DW: w *= DW.get(str((p - ton) % 12), 0.0)
        if "words" not in OFF:
            if WP and k > 0 and k < len(sy) and sy[k][0] == sy[k - 1][0] and sy[k][1] != sy[k - 1][1] and prev is not None:
                up = (p > prev) if sy[k][1] else (p < prev); w *= WP[1] if p == prev else WP[0] if up else WP[2]
            elif TR and k > 0 and k < len(sy) and sy[k][0] != sy[k - 1][0] and prev is not None:
                w *= self.WW["step"][TR[k - 1]][TR[k]][0 if p < prev else 1 if p == prev else 2] ** self.WW["sp"]
        if "end_off" not in OFF and k == n - 1 and end_off is not None and p % 12 == end_off: w *= 0.05
        return w
    @property
    def MOVE_ON(self):
        """939 (749.118): a split note in a line sung again moves on 6 times in 10 and takes the pitch before it 4; the repeat weight scales those odds, as it weighs a repeated note in a fresh line"""
        return 0.6 if self.MV[3] == 1.0 else 0.6 / (0.6 + 0.4 * self.MV[3])
    def again(self, rng, src, src_st0, sy, U, sec, i, tmin, slot):
        """712: the source's onsets and pitches fitted to new syllables; 772: a stressed opening drops its source's pickup."""
        floor = max(tmin, 0) if (sy[0][1] and not src_st0 and src[0][0] < 0) else tmin
        if floor != tmin: self.stats["772: a line sung again, stressed opening: its source's pickup dropped"] += 1
        keep = [(t, p) for t, p in src if t >= floor] or src[-1:]; on = [t for t, p in keep]; ps = [p for t, p in keep]; n = len(sy)
        if self.WW and self.WW["again"] and abs(len(on) - n) <= 3:                                               # 882: the new words choose how they sit on the old tune: which notes are split, dropped or led into, by where kept songs sing each syllable's weight
            def step_from(q0, nxt):
                st_ = [q for q in (q0 + 1, q0 - 1, q0 + 2, q0 - 2) if q % 12 in self.SCALE]; return min(st_, key=lambda q_: abs(q_ - nxt))
            def inserts(o, q):
                for j in range(len(o)):
                    g = (o[j + 1] if j + 1 < len(o) else slot - 6) - o[j]; h = o[j] + (g // 2 // 3) * 3
                    if g >= 6 and h > o[j]: yield o[:j + 1] + [h] + o[j + 1:], q[:j + 1] + [None] + q[j + 1:]
                if o[0] - 6 >= tmin: yield [o[0] - 6] + o, ["lead"] + q
            def deletes(o, q):
                for j in range(len(o) - 1): yield o[:j] + o[j + 1:], q[:j] + q[j + 1:]
            states = {tuple(on): (list(on), list(ps), 0)}; d = n - len(on)
            for _ in range(abs(d)):
                nxt_ = {}
                for o, q, c in states.values():
                    for o2, q2 in (inserts(o, q) if d > 0 else deletes(o, q)): nxt_.setdefault(tuple(o2), (o2, q2, c + 1))
                states = nxt_
            if d == 0:                                                                        # the same count: the tune as it was, or one note dropped and one split
                for o, q, c in list(states.values()):
                    for o1, q1 in deletes(o, q):
                        for o2, q2 in inserts(o1, q1): states.setdefault(tuple(o2), (o2, q2, 2))
            tr_a = WW_.tier(sy); short = lambda o: sum(1 for k2 in range(len(o) - 1) if tr_a[k2] == 2 and o[k2 + 1] - o[k2] <= 3)      # 891 (749.66): each stressed syllable left a sixteenth long is charged
            cands = [(self.stress_score(o, sy, True) - self.WW["cost"] * c - self.WW["short"] * short(o), -c, -k_, o, q) for k_, (o, q, c) in enumerate(states.values()) if o[0] >= tmin and all(y - x >= 3 for x, y in zip(o, o[1:]))]
            if not cands: return None
            _, c_, _, on, ps = max(cands, key=lambda x: x[:3]); c_ = -c_; ps = list(ps)                                                       # the best fit, each note split or dropped charged, so the tune is kept where the words allow
            if c_: self.stats["882: a line sung again, its notes fitted to the new words' weights"] += 1
            for j in range(len(ps)):
                if ps[j] == "lead":
                    f0 = next(q for q in ps[j + 1:] if q not in (None, "lead")); x = rng.random(); lv_ = 0.32 if self.MV[3] == 1.0 else 0.32 * self.MV[3] / (0.32 * self.MV[3] + 0.68); ps[j] = f0 if x < lv_ else step_from(f0, f0 - 12 if (x - lv_) / (1 - lv_) < 0.45 / 0.68 else f0 + 12)     # led into from below, level, or above at the kept shares for a light word before a stressed one
            for j in range(len(ps)):
                if ps[j] is None:
                    nx = next((q for q in ps[j + 1:] if q is not None), ps[j - 1]); ps[j] = step_from(ps[j - 1], nx) if (rng.random() < self.MOVE_ON or (j > 1 and ps[j - 2] == ps[j - 1])) else ps[j - 1]
        while len(on) < n:
            gaps = [((on[j + 1] if j + 1 < len(on) else slot - 6) - on[j], j) for j in range(len(on))]; g, j = max(gaps)
            if g < 6: return None
            h = on[j] + (g // 2 // 3) * 3
            if h <= on[j]: return None
            nxt = ps[j + 1] if j + 1 < len(ps) else ps[j]; step = [q for q in (ps[j] + 1, ps[j] - 1, ps[j] + 2, ps[j] - 2) if q % 12 in self.SCALE]
            q = min(step, key=lambda q_: abs(q_ - nxt)) if (rng.random() < self.MOVE_ON or (j > 0 and ps[j - 1] == ps[j])) else ps[j]
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
            if "chord_tie" not in self.S and not (getattr(self, "_818", False) and getattr(self, "_true", False)) and self.on_beat(U + t) and p % 12 not in ch: p = min((p + d for d in (-1, 1, -2, 2) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch), key=lambda q_: abs(q_ - p), default=p)
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
        return max(-12, self.line_start(ps, pj) + lines[(ps, pj)][-1][0] + (self.gap_now if self.LE else self.END + self.rest_now) - self.line_start(sec, i))      # 899: with the kept line ends, a line may begin a beat after the last began its last note (the kept 10th)
    @staticmethod
    def runs_ok(ps, cap=3):
        c = cap + 1; return all(len(set(ps[k:k + c])) > 1 for k in range(len(ps) - c + 1))      # 926: no run longer than the cap; 928 (749.105): the cap is the caller's own, three where none is given (the hymn engine, a song with no aim)
    def carry(self, lines, k):
        """929 (749.106): the run of one pitch the song is on when line k begins (an aimed song only)"""
        if not self.AIM or not k: return []
        sq = [p_ for kk_ in self.KEYS[max(0, k - 3):k] for _, p_ in lines[kk_]]; c = 0
        for q_ in reversed(sq):
            if q_ != sq[-1]: break
            c += 1
        return [sq[-1]] * min(c, self.RUN) if sq else []
    def line_ok(self, ps, lines, k): return self.runs_ok(self.carry(lines, k) + list(ps), self.RUN)
    def join(self, r, lines, k, sec, i):
        """929 (749.106): one test on every path that writes a line's pitches: the run carried in plus the line. Where a line that returns fails it at the join,
        its first note moves a scale step toward its next note (as 839 lifts a held note) rather than the line being drawn fresh. None if that does not mend it."""
        ps = [p for _, p in r]
        if self.line_ok(ps, lines, k): return r
        if not self.AIM or not self.runs_ok(ps, self.RUN): return None
        p0 = ps[0]; nxt = ps[1] if len(ps) > 1 else p0; mu, lo, hi = self.reg(sec, i); ch = self.chord_at(self.line_start(sec, i) + r[0][0])
        for dn in ((1, -1) if nxt >= p0 else (-1, 1)):
            q = p0 + dn
            while q % 12 not in self.SCALE: q += dn
            if lo <= q <= hi and (q % 12 in ch or not ((q + 1) % 12 in ch or (q - 1) % 12 in ch)) and self.line_ok([q] + ps[1:], lines, k):
                self.stats["929: a returning line's first note moves a step, to end a run at the join"] += 1; return [(r[0][0], q)] + list(r[1:])
        return None
    def build(self, rng):
        lines = {}; prev = None; plans = {}; self._figs = None; self._runin = None; self._peaked = False
        for name, opts in self.S.get("plans", {}).items(): plans[name] = rng.choice(opts)
        self._lh = self.draw_heights(rng) if self.S.get("line_heights") else None
        for k, (sec, i) in enumerate(self.KEYS):
            sy = self.LINES[sec][i]; U = self.line_start(sec, i); slot = self.slot_len(sec, i); how = self.HOW.get((sec, i), ["fresh"]); tm = self.tmin(lines, k)
            self._made[(sec, i)] = "fresh"                                                    # a record of how each line was made in this build, for studies; it changes no note
            cap = None                                                                        # 816 (780, 773 carried): the line before a copied or designed line that comes in early gives way
            if k + 1 < len(self.KEYS):
                ns_, ni_ = self.KEYS[k + 1]; hn = self.HOW.get((ns_, ni_), ["fresh"]); f0 = None
                if hn[0] == "design": f0 = hn[1][0][0]
                elif hn[0] == "copy" and (hn[1], hn[2]) in lines: f0 = lines[(hn[1], hn[2])][0][0]
                if f0 is not None: cap = self.line_start(ns_, ni_) + f0 - self.BREATH - U
            if cap is None and k + 2 < len(self.KEYS):                             # 935 (749.114): a short line squeezed between this line and a copied or designed line that comes in early: this line gives way too, so the short line has room
                (s1_, i1_), (s2_, i2_) = self.KEYS[k + 1], self.KEYS[k + 2]; h1_ = self.HOW.get((s1_, i1_), ["fresh"]); h2_ = self.HOW.get((s2_, i2_), ["fresh"]); f2_ = None
                if h1_[0] not in ("design", "copy") and self.slot_len(s1_, i1_) <= self.BAR:
                    if h2_[0] == "design": f2_ = h2_[1][0][0]
                    elif h2_[0] == "copy" and (h2_[1], h2_[2]) in lines: f2_ = lines[(h2_[1], h2_[2])][0][0]
                    if f2_ is not None:
                        cap2_ = self.line_start(s1_, i1_) + (self.line_start(s2_, i2_) + f2_ - self.BREATH - self.line_start(s1_, i1_)) - (len(self.LINES[s1_][i1_]) - 1) * 6 - 12 - U
                        cap = cap2_; self.stats["935: a limit set on a line before a short line before a copy (it binds only where the line would run late)"] += 1      # 938 (749.119): no longer asks that the song have an aim; where the line ends in time the limit changes nothing (songs 55, 54 and 58 build note for note the same with and without it)
            if f"{sec}:{i}" in self.TENTRY: cap = min(cap if cap is not None else 10 ** 6, slot - self.BAR)      # trial (749.232): the line ahead of a title line begins its last syllable on or before the first beat of its last bar
            lim_ = None                                                                        # 948: where the very next line copies this one, the furthest this line's last syllable may stand from its first
            if k + 1 < len(self.KEYS):
                hn2_ = self.HOW.get(self.KEYS[k + 1], ["fresh"])
                if hn2_[0] == "copy" and (hn2_[1], hn2_[2]) == (sec, i): lim_ = self.line_start(*self.KEYS[k + 1]) - U - (12 if self.LE else self.END + self.REST) + (self.BREATH - 12)
            if how[0] == "plan":                                                              # a line that returns an earlier line of its section under a drawn plan
                pl = plans[how[1]]; how = ["again", sec, pl.index(pl[i])] if pl.index(pl[i]) != i else ["fresh"]
            if how[0] == "design": lines[(sec, i)] = [(t, p) for t, p, d in how[1]]; prev = lines[(sec, i)][-1][1]; continue
            if how[0] == "copy":
                src = lines[(how[1], how[2])]
                if src[0][0] < tm and src[0][0] < tm - (self.BREATH - 12):                                                     # 780: two fixed lines a beat apart or more
                    if not self.S.get("copy_join"): return None, ("join before a copy (780)", sec, i)
                    how = ["again", how[1], how[2]]; self.stats["749.228: a copy that would begin too soon is sung again"] += 1      # trial (749.228)
            if how[0] == "copy":
                new = list(src)
                if self.S.get("copy_clash"):                                                      # 966 (749.223; studies/returning_clash): a copied line's long note that clashes under a chord other than its source's is moved to a chord tone, as again() does (833)
                    Us_ = self.line_start(how[1], how[2]); DG_ = self.S.get("degrees") or {}; bl_ = set(DG_.get("blue", ())); tn_ = DG_.get("tonic", 0); mu_, lo_, hi_ = self.reg(sec, i); nw_ = []
                    for j_, (t_, p_) in enumerate(new):
                        ch_ = self.chord_at(U + t_)
                        if (j_ == len(new) - 1 or new[j_ + 1][0] - t_ >= self.BEAT) and set(ch_) != set(self.chord_at(Us_ + t_)) and p_ % 12 not in ch_ and ((p_ + 1) % 12 in ch_ or (p_ - 1) % 12 in ch_) and (p_ - tn_) % 12 not in bl_:
                            q_ = min((p_ + d_ for d_ in (-1, 1, -2, 2, -3, 3, -4, 4) if (p_ + d_) % 12 in self.SCALE and (p_ + d_) % 12 in ch_ and lo_ <= p_ + d_ <= hi_), key=lambda x_: abs(x_ - p_), default=p_)
                            if q_ != p_: self.stats["966: a copied line's long note moved off a clash under another chord"] += 1; p_ = q_
                        nw_.append((t_, p_))
                    new = nw_
                if sec in (self.S.get("vary_returns") or ()) and how[1] != sec and i != 0 and f"{sec}:{i}" not in self.S.get("hooks", ()) and len(new) > 2:      # 839 (749.8): a returning line, not the section's first nor the title's, lifts one held note
                    gaps = [(new[j + 1][0] - new[j][0]) if j + 1 < len(new) else min(24, slot - new[j][0] - self.REST) for j in range(len(new))]; st_ = [x[1] for x in sy]      # 856 (749.56): a note's sung length, the last note's as 844 leaves it
                    held = [j_ for j_ in range(len(new)) if gaps[j_] >= 12] or list(range(len(new)))
                    j = max(held, key=lambda j_: (st_[j_] if j_ < len(st_) else False, min(gaps[j_], 48), -j_)); t0, p0 = new[j]; ch = self.chord_at(U + t0); mu, lo, hi = self.reg(sec, i)
                    for q in (range(p0 + 1, p0 + (5 if j == len(new) - 1 else 4)) if gaps[j] >= 12 else ()):                                 # only a note a quarter long or more is lifted
                        if q % 12 in ch and q % 12 in self.SCALE and q <= hi and (j == 0 or abs(q - new[j - 1][1]) <= 7) and (j == len(new) - 1 or abs(new[j + 1][1] - q) <= 7):
                            trial = new[:j] + [(t0, q)] + new[j + 1:]
                            if self.runs_ok([p_ for _, p_ in trial], self.RUN): new = trial; self.stats["839: a returning line lifts one held note"] += 1
                            break
                if self.AIM: new = self.join(new, lines, k, sec, i) or new                           # 929: a copy that would run past the cap at its join moves its first note (the whole-build gate stands behind it)
                lines[(sec, i)] = new; prev = new[-1][1]; self.stats["780: a copied line keeps its source's join"] += 1; self._made[(sec, i)] = "copy"; continue
            if how[0] == "again":
                src = lines[(how[1], how[2])]; r = self.again(rng, src, self.LINES[how[1]][how[2]][0][1], sy, U, sec, i, tm, slot)
                r = self.join(r, lines, k, sec, i) if r is not None else None                         # 929
                if r is not None and r[0][0] >= tm and (cap is None or r[-1][0] <= cap) and (lim_ is None or r[-1][0] - r[0][0] <= lim_): lines[(sec, i)] = r; prev = r[-1][1]; self._made[(sec, i)] = "again"; continue
                self.stats["712: a line sung again that could not be fitted, drawn fresh"] += 1
            ons = None; bw = self.S.get("borrow")
            if self.S.get("kept_rests") and how[0] in ("fresh", "plan") and k > 0 and not (self.S.get("title_nowait") and f"{sec}:{i}" in self.S.get("hooks", ())):               # 870; trial (749.235): a title line does not wait (749.58): the rest before this line drawn from the kept rests, where the slot leaves room
                if self.LE: self.gap_now = rng.choices(self.LE["GV"], self.LE["Gw"])[0]; tm2 = self.tmin(lines, k); self.gap_now = 12      # 899: the time from the last line's last syllable to this line, drawn from the kept, where the slot leaves room
                else: self.rest_now = rng.choices(self.S["kept_rests"][0], self.S["kept_rests"][1])[0]; tm2 = self.tmin(lines, k); self.rest_now = self.REST
                o2 = self.rhythm(rng, sy, tm2, slot, cap, hook=f"{sec}:{i}" in self.S.get("hooks", ())) if tm2 > tm else None
                if o2 is not None: ons = o2; self.stats["870: a line waits a kept rest"] += 1; self._made[(sec, i)] = "870 wait"                                             # 818: a fresh line may sing an earlier line of its section again, or take its rhythm
            if bw and how[0] == "fresh" and not (self.S.get("title_fresh") and f"{sec}:{i}" in self.S.get("hooks", ())):               # trial: a title line is drawn fresh, 818 does not apply
                j = next((j for j in (i - 2, i - 1) if j >= 0 and self.HOW.get((sec, j), ["fresh"])[0] != "design"), None); x = rng.random()
                if self.S.get("borrow_kept"): bk_ = self.S["borrow_kept"]; w_ = sec.lower().split(); pt_ = "other" if any(z.startswith("pre") for z in w_) else "Chorus" if ("chorus" in w_ or "refrain" in w_) else "Verse" if "verse" in w_ else "other"; bw = dict(rhythm=bw["rhythm"], figure=bk_["by_count"][pt_][min(3, abs(len(sy) - len(lines[(sec, j)])))] if (bk_.get("by_count") and j is not None) else bk_[pt_]); self._true = bool(bk_.get("true"))      # 749.207, a trial (studies/borrow_kept), off: the chance is the kept share of the part's lines that repeat a nearby line. Absent from every record
                if j is not None and x < bw["figure"] + bw["rhythm"]:
                    self._818 = True; r = self.again(rng, lines[(sec, j)], self.LINES[sec][j][0][1], sy, U, sec, i, tm, slot); self._818 = False
                    if r is not None and r[0][0] >= tm and (cap is None or r[-1][0] <= cap) and (lim_ is None or r[-1][0] - r[0][0] <= lim_) and all(b2 > a2 for a2, b2 in zip([t for t, _ in r], [t for t, _ in r][1:])):
                        r2_ = self.join(r, lines, k, sec, i) if x < bw["figure"] else None               # 929
                        if r2_ is not None: lines[(sec, i)] = r2_; prev = r2_[-1][1]; self.stats["818: a line sings an earlier line of its section again"] += 1; self._made[(sec, i)] = "818 again"; continue
                        ons = [t for t, _ in r]; self.stats["818: a line takes an earlier line's rhythm"] += 1; self._made[(sec, i)] = "818 rhythm"
            if ons is None: ons = self.rhythm(rng, sy, tm, slot, cap, hook=f"{sec}:{i}" in self.S.get("hooks", ()))
            self._runin = None
            if k and self.RUNP > 2:                                                             # 926: the run of one pitch the song is already on, counted across the lines
                sq0_ = [p_ for kk_ in self.KEYS[max(0, k - 3):k] for _, p_ in lines[kk_]]; c0_ = 0
                for q_ in reversed(sq0_):
                    if q_ != sq0_[-1]: break
                    c0_ += 1
                self._runin = (sq0_[-1], c0_) if sq0_ else None
            if self.PG and self.PG["memory"] != 1.0:                                           # 923: the figures sung so far, in the order the song is sung
                sq_ = [p_ for kk_ in self.KEYS[:k] for _, p_ in lines[kk_]]; iv_ = self.PG["mod"].ivs(sq_); self._figs = ({tuple(iv_[j_:j_ + 4]) for j_ in range(len(iv_) - 3)}, sq_[-4:]) if len(sq_) >= 5 else None
            if ons is not None and lim_ is not None:                                               # 948 (749.126): a line the very next line copies must leave that copy room: the copy begins where this line began, one slot on
                for _ in range(12):
                    if ons[-1] - ons[0] <= lim_: break
                    o3_ = self.rhythm(rng, sy, tm, slot, cap, hook=f"{sec}:{i}" in self.S.get("hooks", ()))
                    if o3_ is None: break
                    ons = o3_; self.stats["948: a line its own copy follows is drawn again to leave the copy room"] += 1
            if ons is None: return None, ("rhythm: the syllables cannot fit the window", sec, i)
            rule = self.S.get("line_rules", {}).get(f"{sec}:{i}", {}); ps = None
            for _ in range(20):
                ps = self.pitches(rng, ons, U, sec, i, prev, avoid=set(rule.get("avoid", [])) or None, end_off=rule.get("end_off"))
                if ps and self.line_ok(ps, lines, k): break
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
            n["dur"] = dd[n["on"] - self.line_start(n["sec"], n["line"])] if dd is not None else (max(self.END, min(nx - n["on"] - self.REST, 24 if n["stress"] else max(self.END, min(24, n["on"] - flat[j - 1]["on"]) if j and flat[j - 1]["text"] == n["text"] and flat[j - 1]["stress"] else 24))) if last else nx - n["on"])       # 832: a line's last note leaves the least breath
        if self.LE:                                                                           # 899 (749.76, 749.80; replaces 887 where the table stands): the last syllable's length drawn from the kept lengths for its weight
            GV, DV, C_ = self.LE["GV"], self.LE["DV"], self.LE["C"]; i0 = 0; ph0 = flat[0]["on"] if flat else 0                   # and for the time to the next line, so the note and the rest are drawn as a pair and a line may run on
            for j, n in enumerate(flat):
                if j + 1 == len(flat) or (flat[j + 1]["sec"], flat[j + 1]["line"]) != (n["sec"], n["line"]):
                    if self.HOW.get((n["sec"], n["line"]), ["fresh"])[0] != "design":
                        ln = flat[i0:j + 1]; tr_ = WW_.tier([(x["text"], x["stress"]) for x in ln])[-1]; G_ = (flat[j + 1]["on"] if j + 1 < len(flat) else n["on"] + 2 * self.BAR) - n["on"]; gi = min(range(len(GV)), key=lambda q: abs(GV[q] - G_))
                        w_ = C_[tr_][gi] if C_[tr_][gi].sum() >= 20 else C_[:, gi].sum(0); top = G_
                        nl_ = j + 1                                                               # 915 (749.92): look ahead: if this phrase and the whole next line would pass twelve beats, this line ends in a breath
                        while nl_ + 1 < len(flat) and (flat[nl_ + 1]["sec"], flat[nl_ + 1]["line"]) == (flat[j + 1]["sec"], flat[j + 1]["line"]) if j + 1 < len(flat) else False: nl_ += 1
                        ahead_ = (flat[nl_]["on"] + self.END - ph0) if j + 1 < len(flat) else 0
                        if (n["on"] - ph0 > 8 * self.BEAT or ahead_ > 12 * self.BEAT) and G_ >= 12: top = G_ - self.BEAT // 2          # 909 (749.88): a phrase already past eight beats ends in half a beat of rest at the least, so run-ons do not chain
                        ok_ = [(v, x) for v, x in zip(DV, w_) if v <= top and x > 0]
                        n["dur"] = rng.choices([v for v, _ in ok_], [x for _, x in ok_])[0] if ok_ else max(3, min(top, 6))
                    if j + 1 < len(flat) and flat[j + 1]["on"] - n["on"] - n["dur"] >= self.BEAT // 2: ph0 = flat[j + 1]["on"]      # a breath: the next phrase begins
                    i0 = j + 1
        elif self.WW and self.WW["last"]:                                                     # 887 (amends 832, 844): a line's last note takes a kept length for its syllable's weight, of those that leave the rest; it is no longer held as long as the rest allows
            V, SH = self.WW["fin"]; i0 = 0
            for j, n in enumerate(flat):
                if j + 1 == len(flat) or (flat[j + 1]["sec"], flat[j + 1]["line"]) != (n["sec"], n["line"]):
                    if self.HOW.get((n["sec"], n["line"]), ["fresh"])[0] != "design":
                        tr_ = WW_.tier([(x["text"], x["stress"]) for x in flat[i0:j + 1]])[-1]; room = (flat[j + 1]["on"] if j + 1 < len(flat) else n["on"] + 2 * self.BAR) - n["on"] - self.REST
                        ok_ = [(v, w) for v, w in zip(V, SH[tr_]) if self.END <= v <= (room if (n["stress"] or n["dur"] >= min(room, 24)) else n["dur"])]      # 871's cap on a weak last syllable stands
                        if ok_: n["dur"] = rng.choices([v for v, _ in ok_], [w for _, w in ok_])[0]
                    i0 = j + 1
        if self.SUNGB:
            # trial (749.226): a line of three sung bars holds its last note through the padded bar at the kept table's held-bar share; otherwise the bar rests
            for j, n in enumerate(flat):
                if (j + 1 == len(flat) or (flat[j + 1]["sec"], flat[j + 1]["line"]) != (n["sec"], n["line"])) and self.SUNGB.get(id(self.LINES[n["sec"]][n["line"]])) == 3 and self.SLOTS[n["sec"]][n["line"]] == 4 and rng.random() < self.S.get("held_bar_share", 0): n["dur"] = max(n["dur"], self.line_start(n["sec"], n["line"]) + 4 * self.BAR - self.BEAT - n["on"])
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
        if "pitch scaling" in self.Q:                                                        # 867: long-range order (detrended fluctuation analysis), where the kept table holds it
            import scaling as SC; S_ = SC.series([(n["on"], n["p"]) for n in notes]); a_ = SC.dfa(S_["pitch"]); b_ = SC.dfa(S_["onsets on the grid"])
            if a_: r["pitch scaling"] = a_["alpha"]
            if b_: r["rhythm scaling"] = b_["alpha"]
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
        out = {"low surprise": -(max(m, floor) if floor else m), "sure endings": float(np.mean(inner) - np.mean(endn)) if inner and endn else 0.0}
        if "pitch scaling" in self.Q:                                                        # 868: order across scales, counted up to the kept median and no further (a leap: no listening study is behind it)
            import scaling as SC; S_ = SC.series([(n["on"], n["p"]) for n in notes]); a_ = SC.dfa(S_["pitch"]); b_ = SC.dfa(S_["onsets on the grid"])
            out["order across scales, pitch"] = min(a_["alpha"], self.Q["pitch scaling"][1]) if a_ else 0.0; out["order across scales, rhythm"] = min(b_["alpha"], self.Q["rhythm scaling"][1]) if b_ else 0.0
        return out
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
        if any(not self.runs_ok([n["p"] for n in v], self.RUN) for v in by.values()): return "a run of four of one pitch in a line (749.2)"
        if self.S.get("target") and not self.runs_ok([n["p"] for n in (getattr(self, "as_sung", None) or (lambda x: x))(ns)], self.RUN): return "926: a run of one pitch longer than the kept song's longest, across the lines"
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
        if self.S.get("no_leap_past_an_octave") or self.S.get("title_stress"):                 # 959 (749.160), 961 (749.162): two gates from song 62, read on the notes as sung. Written by the songwriting session (lib/luthier/proposed_v47.py), tested in studies/proposed_v47
            sung_ = sorted((getattr(self, "as_sung", None) or (lambda x: x))(ns), key=lambda n: n["on"])
            lim_ = self.S.get("no_leap_past_an_octave")                                         # True: none (v47's ban). "one": one a song at most, as kept songs have them (749.176: a trial form, not built; it gave back 3 builds in a thousand, studies/v48_trials)
            if lim_ and sum(a_["sec"] == b_["sec"] and a_["line"] == b_["line"] and abs(b_["p"] - a_["p"]) > 12 for a_, b_ in zip(sung_, sung_[1:])) > (1 if lim_ == "one" else 0):
                return "959: a leap past an octave inside a line" if lim_ != "one" else "trial 749.176: more than one leap past an octave inside a line"                              # kept songs: 28 of 160 hold one anywhere; Luthier's builds held one about twice as often
            if self.S.get("title_stress"):
                for h_ in self.S.get("hooks", ()):
                    sec_, i_ = h_.rsplit(":", 1); ln_ = [n for n in sung_ if n["sec"] == sec_ and n["line"] == int(i_) and n.get("melisma") != "second"]
                    if not ln_: continue
                    top_ = max(ln_, key=lambda n: n["dur"])
                    if self.S["title_stress"] == "inside":                                      # 749.177: the narrower form, a trial, not built (it passed over 10 and 27 builds in 100 in songs 54 and 49). A build is passed over if the title line's longest note is a weak syllable with another word after it in the line; a weak syllable of the last word may be held (749.184: the comment made to say what the code does)
                        if not top_.get("stress") and any(n["text"] != ln_[-1]["text"] for n in ln_[ln_.index(top_):]): return "trial 749.177: the title line's longest note on a weak syllable before its last word"
                    elif not top_.get("stress"): return "961: the title line's longest note on an unstressed syllable"
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
        least = min(c["charge"] for c in alive); near = [c for c in alive if c["charge"] <= least + 0.05]; pick = min(near, key=lambda c: c["distance"]); old_pick = pick["fp"]; j7 = None; pgate = None; cgate = None; chose_ = None
        if self.S.get("judge") == 7:                                                         # 860-863: the gate, the place a kept song usually stands, then readings whose direction is known
            try:
                import luthier_judge7 as J7; J = J7.Judge7(self.S.get("table") or self.S["metre"].replace("/", "-") + "_sung")
            except Exception as e_: J = None; j7 = {"not used": str(e_)}
            if J is not None:
                for c in alive: c["d7"] = J.distance(c["readings"]); c["directed"] = self.directed(c["notes"])
                half = float(np.median([c["charge"] for c in alive])); first = [c for c in alive if c["charge"] <= half]                           # 874 (749.62): the old charge gates first: the least half of the builds
                ok = [c for c in first if c["d7"] <= J.gate]; band = ok; wgate = None; n_joint = len(ok)
                if self.WW and self.WW.get("gate") is not None:                                                                                     # 881: the words' gate: a build whose words fit its notes less well than nine kept songs in ten is passed over
                    sung_ = getattr(self, "as_sung", None)                                                                                         # 914 (749.91): the fit is read on the notes as sung, melismas placed, where the song's maker gives the engine the means
                    for c in alive: f_ = WW_.fit([x for x in (sung_(c["notes"]) if sung_ else c["notes"]) if x.get("melisma") != "second"], self.BAR, self.BEAT, parts=True); c["fit"] = f_["all"]; c["fit_len"] = f_["length"]; c["fit_h"] = f_["height"]
                    mf_ = float(np.median([c["fit"] for c in alive])); ml_ = float(np.median([c["fit_len"] for c in alive])); mh_ = float(np.median([c["fit_h"] for c in alive]))
                    ok2 = [c for c in ok if c["fit"] >= self.WW["gate"] and c["fit_len"] >= ml_ and c["fit_h"] >= mh_]      # 913 (749.90; amends 908): the better half by length and by height; the whole fit, a third of it place, is held only to the kept floor
                    wgate = dict(at_least=self.WW["gate"], the_builds_median_fit=round(mf_, 3), the_builds_median_fit_by_length=round(ml_, 3), the_builds_median_fit_by_height=round(mh_, 3), read="as sung" if sung_ else "before melismas", builds_fit_quartiles=[round(float(x), 3) for x in np.quantile([c["fit"] for c in alive], (0.25, 0.5, 0.75))], pass_among_all=int(sum(c["fit"] >= self.WW["gate"] for c in alive)), pass_after_the_other_gates=len(ok2))
                    if ok2: ok = ok2
                    else: wgate["no build past the joint gate also passed: the gate is waived"] = True
                n_words_ = len(ok)
                if self.PG and self.PG.get("floor") is not None and ok:                                                                           # 922: the page gate, a floor: a build less plain than nine kept tunes in ten is passed over
                    PGm = self.PG["mod"]
                    sung2_ = getattr(self, "as_sung", None)                                                                                        # 924 (749.102): read as sung, melismas placed, as the kept tunes in the table were
                    for c in ok:
                        ns_ = sorted((sung2_(c["notes"]) if sung2_ else c["notes"]), key=lambda n: n["on"]); on_ = [n["on"] for n in ns_]; c["page"] = PGm.read([n["p"] for n in ns_], [(b_ - a_) / float(self.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], self.PG["T"])
                    ok3 = [c for c in ok if c["page"]["plainness"] >= self.PG["floor"]]; pgate = dict(at_least=round(self.PG["floor"], 3), read_as="as sung" if sung2_ else "before melismas", every_build_read_as="as sung" if sung2_ else "before melismas", read=len(ok), passed=len(ok3), builds_plainness_quartiles=[round(float(x), 3) for x in np.quantile([c["page"]["plainness"] for c in ok], (0.25, 0.5, 0.75))], builds_figures_again_quartiles=[round(float(x), 3) for x in np.quantile([c["page"]["repeated_figures"] for c in ok], (0.25, 0.5, 0.75))], every_build_figures_again_quartiles=[round(float(x), 3) for x in np.quantile([PGm.figures_again([n["p"] for n in (sung2_(c["notes"]) if sung2_ else c["notes"])]) for c in alive], (0.25, 0.5, 0.75))], every_build_first_120_figures_again_quartiles=[round(float(x), 3) for x in np.quantile([PGm.figures_again([n["p"] for n in (sung2_(c["notes"]) if sung2_ else c["notes"])][:120]) for c in alive], (0.25, 0.5, 0.75))], kept_figures_again_quartiles=self.PG["T"]["percentiles_10_25_50_75_90"]["repeated_figures"][1:4], kept_first_120_quartiles=self.PG["T"]["percentiles_10_25_50_75_90"]["first_120_figures_again"][1:4])
                    if ok3: ok = ok3
                    else: pgate["no build past the other gates also passed: the floor is waived"] = True
                cgate = None
                if self.S.get("pitch_ceiling") and ok:                                                                                             # 956 (749.134): a ceiling on the commonest pitch's share. A part can sit on one pitch for half its notes with no long run; a build whose verses, pooled, or choruses, pooled, do so more than nine kept songs in ten is passed over. Read as sung
                    ce_ = self.S["pitch_ceiling"]; sung4_ = getattr(self, "as_sung", None); import make_kept_commonest_pitch as CPK_      # a part is told by its name, as the kept table tells it (a tag is not a chorus there)
                    def cp_(c, part):
                        ps_ = [n["p"] for n in (sung4_(c["notes"]) if sung4_ else c["notes"]) if (CPK_.kind_b(n["sec"]) if part == "Bridge" else CPK_.kind(n["sec"])) == part]; return max(collections.Counter(ps_).values()) / len(ps_) if len(ps_) >= 20 else 0.0
                    for c in ok: c["cp"] = {part: round(cp_(c, part), 3) for part in ce_}
                    ok5 = [c for c in ok if all(c["cp"][part] <= ce_[part] for part in ce_)]; cgate = dict(at_most=ce_, read=len(ok), passed=len(ok5))
                    if ok5: ok = ok5
                    else: cgate["no build past the other gates also passed: the ceiling is waived"] = True
                pool = ok or first                                                         # 873 (749.61): the gate, and no band
                names = list(pool[0]["directed"]); rk = {}
                for n_ in names:
                    v = sorted(pool, key=lambda c: -c["directed"][n_])
                    for r_, c in enumerate(v): rk[(c["fp"], n_)] = r_
                score = lambda c: sum(rk[(c["fp"], n_)] for n_ in names) / len(names)
                short = sorted(pool, key=lambda c: (score(c), c["fp"]))[:5]                                                                         # printed beside the pick, and chooses nothing (872)
                pick = min(pool, key=lambda c: c["n"]) if ok else min(pool, key=lambda c: (c["d7"], c["fp"]))
                cr_ = (self.S.get("target") or {}).get("choose_range") or self.S.get("choose_range") or None; chose_ = None
                if ok and isinstance(cr_, dict):                                                                                                    # 954 (749.135; amends 951): a floor, not a band. The words predict range loosely (held out by artist, sd 5 semitones), so the choice asks only that the tune be no narrower than the asking plus the kept 25th of range less the asking; above the floor 872 decides. Where no build clears it, the widest
                    fl_ = cr_["floor"]; nr_ = [c for c in pool if c["readings"]["range"] >= fl_]; first_ = pick
                    pick = min(nr_, key=lambda c: c["n"]) if nr_ else min(pool, key=lambda c: (-c["readings"]["range"], c["n"]))
                    chose_ = dict(asked=round(cr_["asked"], 1), floor=round(fl_, 2), builds_in_the_pool=len(pool), at_or_over_the_floor=len(nr_), the_first_build_past_the_gates_range=int(first_["readings"]["range"]), the_pick_range=int(pick["readings"]["range"]), the_pick_is_the_first_build_past_the_gates=bool(pick is first_))
                ka_ = self.S.get("key_asked")
                if ka_ and ka_.get("voice"):
                    # 968 (749.219): where the pick leaves the voice in the asked key, as sung, the next tune inside it is taken, in the pick's own order
                    sg_ = getattr(self, "as_sung", None) or (lambda x_: x_); V0_, V1_ = ka_["voice"]; tk_ = [12 * o_ + ka_["tonic_pc"] for o_ in range(1, 8)]
                    def in_(c_): ps_ = [n_["p"] - 60 for n_ in sg_(c_["notes"])]; return any(t_ + min(ps_) >= V0_ and t_ + max(ps_) <= V1_ for t_ in tk_)
                    nr2_ = [c_ for c_ in pool if c_["readings"]["range"] >= cr_["floor"]] if (ok and isinstance(cr_, dict)) else []
                    ord_ = sorted(nr2_ or pool, key=(lambda c_: c_["n"]) if ok else (lambda c_: (c_["d7"], c_["fp"])))
                    ins_ = [c_ for c_ in ord_ if in_(c_)]; self._key_pick = dict(the_first_pick_inside_the_voice=bool(in_(pick)), tunes_passed_over=0, in_the_pool_inside_the_voice=sum(1 for c_ in pool if in_(c_)), of=len(pool))
                    if not in_(pick) and ins_:
                        self._key_pick["tunes_passed_over"] = ord_.index(ins_[0]) if pick in ord_ else None; pick = ins_[0]
                        if chose_ is not None: chose_["the_pick_range"] = int(pick["readings"]["range"])
                    elif not in_(pick): self._key_pick["note"] = "no tune in the pool is inside the voice in the asked key: the engine's pick stands"
                j7 = dict(kept_songs=J.n, readings_read_together=J.names, gate=round(J.gate, 3), a_kept_songs_usual_distance=round(J.usual, 3), kept_middle_half=[round(x, 3) for x in J.band], builds=len(alive), pass_the_gate=len(ok), in_the_kept_middle_half=len(band),
                          builds_distance_quartiles=[round(float(x), 3) for x in np.quantile([c["d7"] for c in alive], (0.25, 0.5, 0.75))], pick_distance=round(pick["d7"], 3), pick_directed=pick["directed"], words_gate=wgate, pick_words_fit=WW_.fit(pick["notes"], self.BAR, self.BEAT, parts=True) if self.WW else None,
                          pool="past both gates: the old charge's least half, then the joint gate; the pick is the first of them in the order built" if ok else "no build passed the joint gate: the least distance among the old charge's least half", gates_passed=dict(old_charge_least_half=len(first), joint_gate=n_joint, words_gate=n_words_ if wgate else None), gates_removed=dict(old_charge=len(alive) - len(first), joint_gate=len(first) - n_joint, words_gate=(n_joint - n_words_) if wgate and not wgate.get("no build past the joint gate also passed: the gate is waived") else None), shortlist=[dict(fp=c["fp"], distance=round(c["d7"], 3), old_charge=round(c["charge"], 3), **{k_: round(v_, 3) for k_, v_ in c["directed"].items()}) for c in short],
                          the_old_pick=dict(fp=old_pick, distance=round(next(c["d7"] for c in alive if c["fp"] == old_pick), 3), passes=bool(next(c["d7"] for c in alive if c["fp"] == old_pick) <= J.gate)), withheld_reading_old_charge_of_the_pick=round(pick["charge"], 3), the_old_pick_notes=[[n["on"], n["p"], n["sec"]] for n in next(c["notes"] for c in alive if c["fp"] == old_pick)])
        if isinstance(j7, dict) and j7.get("builds") and chose_ is not None: j7["range_choice"] = chose_
        if isinstance(j7, dict) and j7.get("builds") and cgate is not None: j7["pitch_ceiling"] = cgate; j7["pick_commonest_pitch"] = pick.get("cp")
        if isinstance(j7, dict) and pgate is not None: j7["page_gate"] = pgate; j7["pick_page_gate"] = {k_: round(v_, 3) for k_, v_ in pick.get("page", {}).items()}; j7["gates_passed"]["page_floor"] = pgate["passed"] if not pgate.get("no build past the other gates also passed: the floor is waived") else pgate["read"]; j7["gates_removed"]["page_floor"] = pgate["read"] - j7["gates_passed"]["page_floor"]
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
