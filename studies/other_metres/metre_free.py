"""PREDICTION_metre_free.md: three 4/4 gates read on kept songs outside 4/4.  python3 studies/other_metres/metre_free.py -> metre_free.json"""
import os, sys, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier")]
import numpy as np, pandas as pd, kept_corpus as KC, page_gate as PG, make_kept_commonest_pitch as CP, cocopops_parse as CPP
T = PG.table(); CE = json.load(open(os.path.join(ROOT, "tables", "kept_commonest_pitch.json")))["parts"]; KEPT = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json"))))
def metre_of(path):
    c = collections.Counter(); cur = None
    for line in open(path, errors="ignore"):
        m = re.match(r"\*M(\d+/\d+)", line)
        if m: cur = m.group(1)
        elif line.startswith("=") and cur: c[cur] += 1
    return c.most_common(1)[0][0] if c else None
def rs(path):
    R = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore") if l.strip() and not l.startswith("!!")]; head = next(r for r in R if r[0].startswith("**")); k = head.index("**kern"); t = 0.0; tb = None; sec = ""; out = []
    for r in R[R.index(head) + 1:]:
        if len(r) <= k: continue
        a = r[k]
        if a.startswith("*"):
            for x in r:
                m = re.match(r"\*tb(\d+)", x)
                if m: tb = int(m.group(1))
            if r[0].startswith("*>"): sec = r[0][2:]
            continue
        if a.startswith("!") or a.startswith("="): continue
        if not tb: return []
        if a not in (".", "") and "r" not in a and not a.startswith("]") and "_" not in a and CPP.kern_pitch(a) is not None: out.append((t, int(CPP.kern_pitch(a)), sec))
        t += 4.0 / tb
    return out
def read(N):
    """N: (time in quarters, pitch, section) in order"""
    t = np.array([n[0] for n in N], float); p = [n[1] for n in N]; d = np.r_[np.diff(t), 1.0]; d = np.where(d > 0, d, 0.25); r = PG.read(p, d, T); o = {c: round(float(r[c]), 4) for c in list(PG.PLAIN) + ["plainness"]}
    o["under_the_floor"] = bool(r["plainness"] < T["floor"]["plainness"])
    for part in ("Verse", "Chorus"):
        s = CP.share([q for q, (_, _, x) in zip(p, N) if CP.kind(x) == part]); o[part] = None if s is None else round(s, 3)
    o["over_a_ceiling"] = bool(any(o[part] is not None and o[part] > CE[part]["ceiling"] for part in ("Verse", "Chorus"))); o["a_ceiling_read"] = bool(o["Verse"] is not None or o["Chorus"] is not None)
    o["leap_past_an_octave_in_a_line"] = bool(any(abs(p[i] - p[i - 1]) > 12 and t[i] - t[i - 1] < 2 for i in range(1, len(p)))); o["notes"] = len(p); return o
songs = {}
B = KC.table(); BD = os.path.join(ROOT, "corpora", "CoCoPops", "Billboard", "Data"); bm = {}
for f in sorted(glob.glob(BD + "/*.hum")):
    if "**kern" in open(f, errors="ignore").read(): bm[os.path.basename(f).split(".")[0]] = metre_of(f)
for s, g in B.groupby("song", sort=False):
    g = g.sort_values("abs_beat"); m = bm.get(str(s))
    if len(g) < 100 or m is None or (m == "4/4" and str(s) not in KEPT): continue
    songs[str(s)] = dict(source="Billboard", metre=m, **read(list(zip(g.abs_beat.values, g.pitch.values.astype(int), g.section.values))))
for f in sorted(glob.glob(os.path.join(ROOT, "corpora", "CoCoPops", "RollingStone", "Data", "*.hum"))):
    N = rs(f); m = metre_of(f)
    if len(N) < 100 or m is None: continue
    songs[os.path.basename(f).split(".")[0]] = dict(source="Rolling Stone", metre=m, **read(N))
def grp(sel):
    v = [o for o in songs.values() if sel(o)]; c = [o for o in v if o["a_ceiling_read"]]
    return dict(songs=len(v), under_the_floor_in_100=round(100 * np.mean([o["under_the_floor"] for o in v]), 1) if v else None, ceiling_read=len(c), over_a_ceiling_in_100=round(100 * np.mean([o["over_a_ceiling"] for o in c]), 1) if c else None, leap_in_100=round(100 * np.mean([o["leap_past_an_octave_in_a_line"] for o in v]), 1) if v else None,
                medians={k: round(float(np.median([o[k] for o in v])), 3) for k in list(PG.PLAIN) + ["plainness"]} if v else None)
comp = lambda o: o["metre"] in ("12/8", "6/8")
out = dict(groups={"compound, both sources": grp(comp), "compound, Billboard": grp(lambda o: comp(o) and o["source"] == "Billboard"), "compound, Rolling Stone": grp(lambda o: comp(o) and o["source"] == "Rolling Stone"), "4/4 kept, Billboard": grp(lambda o: o["metre"] == "4/4" and o["source"] == "Billboard"), "4/4, Rolling Stone": grp(lambda o: o["metre"] == "4/4" and o["source"] == "Rolling Stone"), "3/4": grp(lambda o: o["metre"] == "3/4")},
           songs_outside_4_4={k: o for k, o in songs.items() if o["metre"] != "4/4"})
for k, v in out["groups"].items(): print(k, json.dumps(v))
json.dump(out, open(os.path.join(HERE, "metre_free.json"), "w"), indent=1)
