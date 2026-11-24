"""Proposed for v47, from the writer's side (24 November 2026): flagged patches for the maintainer to test and keep or drop. Nothing changes the engine
unless apply() is called. Each flag names its finding on the list for v46 (songs/p68/fixlist_v46.md) and is read on songs 58, 60, 61 and 62 only
(never on 59, 50 or 63: hold-outs).
    import proposed_v47 as P; P.apply(octave=True, region=True, title_stress=True, no_blue=True, loop_less=False)
    python3 lib/luthier/proposed_v47_trial.py songs/p71/lyric61.json 3000 --all     # a run with the flags, and its readings
  octave       749.160  a gate: no leap past an octave between two sung notes of one line (the planted peak once landed Eb3 Ab4 Db3 Eb4 inside a word)
  region       749.165, 749.170  a gate: the tune inside the kept region where plain and pink both hold, read on the sung syllables (melisma notes out):
               surprise at most the kept median (3.18 bits an interval), pitch DFA order 1 at least 0.95 and order 2 at least 1.05, the three commonest
               pitches at most 69% of the notes. Read together: a surprise ceiling alone whitened song 62 (749.161, 749.165)
  title_stress 749.162  a gate: on each line that sings the title, the longest note falls on a stressed syllable
  no_blue      749.168  the blue-note draw (846) turned off for this song (for styles such as chamber pop, hymn, art song)
  loop_less    749.159  the trial (proposed 960): verse and bridge structures (800) drawn only from kept sections of that kind and mode whose within-section
               chord repetition is at or below the kept median of the kind (the research check's measure in the writer's vocabulary); chorus unchanged
  vary_returns 749.167  not a flag: a function on a finished record; a section that returns note for note gets lines 2 onward each lifting their longest
               held note a scale step onto a chord tone (839's lift, made sure rather than left to chance)"""
import os, sys, json, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REGION = dict(surprise_max=None, dfa1_min=0.95, dfa2_min=1.05, top3_max=0.69)      # surprise_max: the kept median from tables/kept_page_gate.json
HOLDOUTS = {"lyric59", "lyric50", "lyric63"}
_applied = {}
def _sung(self, c): return sorted((getattr(self, "as_sung", None) or (lambda x: x))(c["notes"]), key=lambda n: n["on"])
def region_read(pitches):
    import page_gate as PG, scaling as SC
    T = PG.table(); p = [int(x) for x in pitches]; a1 = SC.dfa(p, order=1); a2 = SC.dfa(p, order=2)
    return dict(surprise=PG.surprise(PG.ivs(p), T["_C"]), dfa1=a1["alpha"] if a1 else None, dfa2=a2["alpha"] if a2 else None,
                top3=sum(v for _, v in collections.Counter(p).most_common(3)) / len(p))
def in_region(r):
    import page_gate as PG
    smax = REGION["surprise_max"] if REGION["surprise_max"] is not None else PG.table()["percentiles_10_25_50_75_90"]["surprise"][2]
    return r["surprise"] <= smax and r["dfa1"] is not None and r["dfa1"] >= REGION["dfa1_min"] and r["dfa2"] is not None and r["dfa2"] >= REGION["dfa2_min"] and r["top3"] <= REGION["top3_max"]
def apply(octave=False, region=False, title_stress=False, no_blue=False, loop_less=False):
    import metre_engine as M, song_from_lyric as SL, chord_writer as C
    if any((octave, region, title_stress)) and "gates" not in _applied:
        base = M.Engine.gates; _applied["gates"] = base
        def gates(self, c):
            e = base(self, c)
            if e: return e
            sung = _sung(self, c)
            if _applied.get("octave") and any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["p"] - a["p"]) > 12 for a, b in zip(sung, sung[1:])):
                return "v47 (749.160): a leap past an octave inside a line"
            if _applied.get("title_stress"):
                for h in self.S.get("hooks", ()):
                    sec, i = h.rsplit(":", 1); ln = [n for n in sung if n["sec"] == sec and n["line"] == int(i) and n.get("melisma") != "second"]
                    if ln and not max(ln, key=lambda n: n["dur"]).get("stress"): return "v47 (749.162): the title line's longest note on an unstressed syllable"
            if _applied.get("region"):
                r = region_read([n["p"] for n in sung if n.get("melisma") != "second"])
                if not in_region(r): return "v47 (749.165, 749.170): the tune outside the kept plain-and-pink region"
            return None
        M.Engine.gates = gates
    _applied.update(octave=octave, region=region, title_stress=title_stress)
    if no_blue and "plan" not in _applied:
        base_plan = SL.plan; _applied["plan"] = base_plan
        def plan(L):
            spec, form, flags = base_plan(L); dg = spec.get("degrees")
            if dg and dg.get("blue_song"):
                dg["blue"] = []; dg["blue_song"] = False
                for w in dg["weights"].values(): w.update({"3": 0.0, "10": 0.0})
                flags.append("v47 (749.168): the blue-note draw turned off for this song")
            return spec, form, flags
        SL.plan = plan
    if loop_less and "writer" not in _applied:
        base_init = C.Writer.__init__; _applied["writer"] = base_init
        def rep(bars):
            seq = []
            for t in bars:
                for x in t:
                    if not seq or seq[-1] != x: seq.append(x)
            if len(seq) < 4: return None
            seen = set(); r = 0; n = len(seq) - 2
            for i in range(n): g = tuple(seq[i:i + 3]); r += g in seen; seen.add(g)
            return r / n
        def init(self, mode="major", songs=None, chromatic=1.0):
            songs = songs if songs is not None else json.load(open(C.DATA)); base_init(self, mode, songs, chromatic)
            S = C.sections(songs, mode); allS = C.sections(songs); self.loop_less = {}
            for k in ("verse", "bridge"):
                if k not in self.tmpl: continue
                src = [b for kk, b, _, _ in S if kk == k]
                if len(src) < 30: src = [b for kk, b, _, _ in allS if kk == k]
                rs = [(rep(b), b) for b in src]; vals = [r for r, _ in rs if r is not None]
                if not vals: continue
                med = st.median(vals); keep = [C.pattern(b) for r, b in rs if r is not None and r <= med]
                if keep: self.tmpl[k] = keep; self.loop_less[k] = dict(kept_median=round(med, 3), templates=len(keep), of=len(rs))
        C.Writer.__init__ = init
def vary_returns(rec):
    """749.167 on a finished song record (song_from_lyric's): each section whose every line was copied from an earlier one has its lines 2 onward
    lift their longest held note (a beat or more) a scale step onto a chord tone, leaps kept within a fifth. Returns the list of changes."""
    import chord_writer as C
    B = rec["bar"]; BT = B // 4; tonic = rec["key"]["tonic_midi"]; scale = {(tonic + d) % 12 for d in (0, 2, 4, 5, 7, 9, 11)}
    how = rec.get("spec", {}).get("how", {}); start = {}; o = 0
    for n, k, b in rec["form"]: start[n] = o; o += b * B
    notes = rec["melody"]["notes"]; by = collections.defaultdict(list)
    for n in notes: by[(n["sec"], n["line"])].append(n)
    secs = {n for n, _, _ in rec["form"]}; out = []
    for sec in secs:
        lines = sorted(i for s_, i in by if s_ == sec)
        if not lines or not all(how.get(f"{sec}:{i}", ["fresh"])[0] == "copy" for i in lines): continue
        for i in lines[1:]:
            ln = sorted(by[(sec, i)], key=lambda n: n["on"]); held = [n for n in ln if n["dur"] >= BT]
            if not held: continue
            n = max(held, key=lambda n: (n.get("stress", False), n["dur"])); j = ln.index(n); bar = (n["on"] - start[sec]) // B
            rn = rec["roman"][sec][bar].split(); c_ = rn[0] if len(rn) == 1 or (n["on"] - start[sec]) % B < B // 2 else rn[1]; tones = {(t + tonic) % 12 for t in C.tones(c_)}
            for q in range(n["midi"] + 1, n["midi"] + 5):
                if q % 12 in scale and q % 12 in tones and (j == 0 or abs(q - ln[j - 1]["midi"]) <= 7) and (j == len(ln) - 1 or abs(ln[j + 1]["midi"] - q) <= 7):
                    out.append(dict(section=sec, line=i + 1, word=n["text"], was=n["midi"], now=q)); n["midi"] = q; break
    return out
