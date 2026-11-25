"""One run of the engine with one of the v47 proposals on. See PREDICTION.md.
    python3 studies/proposed_v47/run.py songs/pNN/lyricNN.json N flag out.json [record_out.json]
flag: off | octave | title_stress | region | no_blue | loop_templates | loop_structure | loop_gate"""
import os, sys, json, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import proposed_v47 as P, chord_writer as C
f, N, flag, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
if os.path.basename(f).split(".")[0] in P.HOLDOUTS: raise SystemExit(f"{f} is a hold-out: not run")
def rep_of(bars):
    seq = []
    for t in bars:
        for x in (t.split() if isinstance(t, str) else t):
            if not seq or seq[-1] != x: seq.append(x)
    if len(seq) < 4: return None
    seen = set(); r = 0; n = len(seq) - 2
    for i in range(n): g = tuple(seq[i:i + 3]); r += g in seen; seen.add(g)
    return r / n
def kept_medians(songs, mode):
    S = C.sections(songs, mode); allS = C.sections(songs); med = {}
    for k in ("verse", "bridge", "chorus"):
        src = [b for kk, b, _, _ in S if kk == k]
        if len(src) < 30: src = [b for kk, b, _, _ in allS if kk == k]
        v = [r for r in (rep_of(b) for b in src) if r is not None]; ret = [1 - len(set(map(tuple, b))) / len(b) for b in src if len(b) >= 2]
        med[k] = dict(rep=st.median(v), returning=st.median(ret), src=src)
    return med
P.apply(octave=flag == "octave", region=flag == "region", title_stress=flag == "title_stress", no_blue=flag == "no_blue", loop_less=flag == "loop_templates")
if flag == "loop_structure":
    base_init = C.Writer.__init__
    def init(self, mode="major", songs=None, chromatic=1.0):
        songs = songs if songs is not None else json.load(open(C.DATA)); base_init(self, mode, songs, chromatic); med = kept_medians(songs, mode)
        for k in ("verse", "bridge"):
            if k in self.tmpl:
                keep = [C.pattern(b) for b in med[k]["src"] if len(b) >= 2 and 1 - len(set(map(tuple, b))) / len(b) <= med[k]["returning"]]
                if keep: self.tmpl[k] = keep
    C.Writer.__init__ = init
if flag == "loop_gate":
    base_init = C.Writer.__init__; base_sec = C.Writer.section
    def init(self, mode="major", songs=None, chromatic=1.0):
        songs = songs if songs is not None else json.load(open(C.DATA)); base_init(self, mode, songs, chromatic); self._loop_med = {k: v["rep"] for k, v in kept_medians(songs, mode).items()}
    def section(self, rng, k, n, prev=None, require=None, given=None, final=False, home=None):
        if k not in ("verse", "bridge") or given: return base_sec(self, rng, k, n, prev, require, given, final, home)
        best = None
        for _ in range(30):
            b = base_sec(self, rng, k, n, prev, require, given, final, home); r = rep_of(b); r = 0.0 if r is None else r
            if r <= self._loop_med[k]: return b
            if best is None or r < best[0]: best = (r, b)
        return best[1]
    C.Writer.__init__ = init; C.Writer.section = section
import song_from_lyric as SL
L = json.load(open(f)); rec = SL.write(L, N, 12)
if "error" in rec: json.dump(dict(song=os.path.basename(f), flag=flag, error=rec["error"], deaths=rec.get("deaths")), open(out, "w"), indent=1); print(rec["error"]); sys.exit(0)
m = rec["melody"]; ns = sorted(m["notes"], key=lambda n: n["on"]); syl = [n for n in ns if n.get("melisma") != "second"]; r = P.region_read([n["midi"] for n in syl]); hooks = set(rec["spec"].get("hooks", ()))
leaps = sum(1 for a, b in zip(ns, ns[1:]) if a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["midi"] - a["midi"]) > 12)
title = []
for h in sorted(hooks):
    sec, i = h.rsplit(":", 1); ln = [n for n in syl if n["sec"] == sec and n["line"] == int(i)]
    if ln: title.append(bool(max(ln, key=lambda n: n["dur"]).get("stress")))
tonic = rec["key"]["tonic_midi"]; reps = {}
for n_, k_, b_ in rec["form"]:
    if k_ in ("verse", "chorus", "bridge") and k_ not in reps and n_ in rec["roman"]: v = rep_of(rec["roman"][n_]); reps[k_] = None if v is None else round(v, 3)
res = dict(song=os.path.basename(f), flag=flag, builds=N, survivors=m["survivors"], deaths=dict(list(m["deaths"].items())[:6]), pick=m["pick"], key=rec["key"]["key"],
           words_fit=[v for k, v in rec["checks"].items() if k.startswith("the words' fit")][0], judge7=(rec.get("judge7") or {}).get("pick_distance"),
           region={k: (round(v, 3) if v is not None else None) for k, v in r.items()}, in_region=bool(P.in_region(r)), leaps_past_an_octave_in_a_line=leaps,
           title_lines=len(title), title_lines_longest_note_stressed=int(sum(title)), blue_song=rec["spec"].get("degrees", {}).get("blue_song"),
           lowered_thirds=sum(1 for n in ns if (n["midi"] - tonic) % 12 == 3) if L.get("mode", "major") == "major" else None, chord_repetition=reps, pool=((rec.get("judge7") or {}).get("gates_passed")))
if flag == "off":
    import copy; r2 = copy.deepcopy(rec); ch = P.vary_returns(r2); import word_weight as WW
    res["vary_returns"] = dict(changes=ch, words_fit_after=round(WW.fit([n for n in r2["melody"]["notes"] if n.get("melisma") != "second"], rec["bar"], rec["bar"] // 4, parts=True)["all"], 3))
json.dump(res, open(out, "w"), indent=1); print(json.dumps({k: v for k, v in res.items() if k not in ("deaths", "pool")}))
if len(sys.argv) > 5: json.dump(rec, open(sys.argv[5], "w"), indent=1, default=float)
