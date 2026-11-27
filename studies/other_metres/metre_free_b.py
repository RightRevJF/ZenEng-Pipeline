"""PREDICTION_b.md: checks that do not read the bar, by metre, in three references.  python3 studies/other_metres/metre_free_b.py -> metre_free_b.json"""
import os, sys, re, json, glob, zipfile, collections, runpy
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, page_gate as PG
T = PG.table(); PARTS = list(PG.PLAIN) + ["plainness", "commonest_pitch"]; LOW = {"plainness"}
def read(t, p):
    """t in quarters, p pitches, in order"""
    t = np.asarray(t, float); d = np.r_[np.diff(t), 1.0]; d = np.where(d > 0, d, 0.25); r = PG.read(p, d, T); o = {c: float(r[c]) for c in list(PG.PLAIN) + ["plainness"]}
    o["commonest_pitch"] = max(collections.Counter(p).values()) / len(p); o["leap"] = bool(any(abs(p[i] - p[i - 1]) > 12 and t[i] - t[i - 1] < 2 for i in range(1, len(p)))); return o
def essen(a):
    import atlas_build as AB
    abc, bar = a; ns = AB.notes_of(abc, bar)
    if not ns or len(ns) < 40: return None
    return read([x[0] / 12.0 for x in ns], [int(x[2]) for x in ns])
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def ewld(path):
    from lxml import etree
    try:
        z = zipfile.ZipFile(path); root = etree.fromstring(z.read([n for n in z.namelist() if n.endswith(".xml") and not n.startswith("META")][0])); parts = root.findall("part"); part = max(parts, key=lambda q: len(q.findall(".//lyric")))
    except Exception: return None
    div = 1; ts = None; t0 = 0.0; N = []; bars = collections.Counter()
    for m in part.findall("measure"):
        a = m.find("attributes")
        if a is not None:
            d = a.find("divisions"); div = int(float(d.text)) if d is not None else div; tm = a.find("time")
            if tm is not None and tm.find("beats") is not None:
                try: ts = f"{int(tm.find('beats').text)}/{int(tm.find('beat-type').text)}"
                except ValueError: pass
        pos = 0; end = 0
        for el in m:
            if el.tag == "backup": pos -= int(float(el.find("duration").text)); continue
            if el.tag == "forward": pos += int(float(el.find("duration").text)); continue
            if el.tag != "note" or el.find("grace") is not None or el.find("chord") is not None: continue
            du = el.find("duration"); dur = int(float(du.text)) if du is not None else 0; v = el.find("voice")
            if v is not None and v.text not in ("1", None): pos += dur; continue
            pt = el.find("pitch")
            if el.find("rest") is None and pt is not None and not any(x.get("type") == "stop" for x in el.findall("tie")):
                alt = pt.find("alter"); N.append((t0 + pos / div, 12 * (int(pt.find("octave").text) + 1) + STEP[pt.find("step").text] + (int(float(alt.text)) if alt is not None else 0)))
            pos += dur; end = max(end, pos)
        t0 += end / div; bars[ts] += 1
    if len(N) < 60 or not bars: return None
    N.sort(); return dict(metre=bars.most_common(1)[0][0], **read([n[0] for n in N], [n[1] for n in N]))
def summary(v, ref=None):
    o = dict(tunes=len(v), leap_in_100=round(100 * np.mean([x["leap"] for x in v]), 1))
    for c in PARTS: o[c] = [round(float(q), 3) for q in np.percentile([x[c] for x in v], (10, 25, 50, 75, 90))]
    if ref is None:
        rng = np.random.default_rng(0); idx = [rng.integers(0, len(v), len(v)) for _ in range(2000)]; o["ranges"] = {}
        for c in PARTS:
            a = np.array([x[c] for x in v]); o["ranges"][c] = dict(p10=[round(float(q), 3) for q in np.percentile([np.percentile(a[i], 10) for i in idx], (5, 95))], p90=[round(float(q), 3) for q in np.percentile([np.percentile(a[i], 90) for i in idx], (5, 95))])
        a = np.array([x["leap"] for x in v], float); o["ranges"]["leap_in_100"] = [round(float(q), 1) for q in np.percentile([100 * a[i].mean() for i in idx], (5, 95))]
    else:
        o["free"] = {}
        for c in PARTS:
            side = "p10" if c in LOW else "p90"; tail = o[c][0] if c in LOW else o[c][4]; lo, hi = ref["ranges"][c][side]; o["free"][c] = dict(median_in_middle_half=bool(ref[c][1] <= o[c][2] <= ref[c][3]), tail=side, tail_in_range=bool(lo <= tail <= hi)); o["free"][c]["free"] = o["free"][c]["median_in_middle_half"] and o["free"][c]["tail_in_range"]
        lo, hi = ref["ranges"]["leap_in_100"]; o["free"]["leap"] = dict(free=bool(lo <= o["leap_in_100"] <= hi))
    return o
if __name__ == "__main__":
    import atlas_build as AB
    out = {}; pool = Pool(2)
    E = {m: [x for x in pool.map(essen, [(abc, AB.METRES[m][0]) for abc in AB.tunes(m, "sung")], chunksize=20) if x] for m in ("4/4", "3/4", "6/8")}; ref = summary(E["4/4"]); out["Essen sung"] = {"4/4": ref, "3/4": summary(E["3/4"], ref), "6/8": summary(E["6/8"], ref)}; print("Essen", {m: len(v) for m, v in E.items()}, flush=True)
    W = collections.defaultdict(list)
    for x in pool.map(ewld, sorted(glob.glob("/home/claude/corpus/OpenEWLD/dataset/**/*.mxl", recursive=True)), chunksize=10):
        if x: W[x["metre"]].append(x)
    ref = summary(W["4/4"]); out["Lead sheets (OpenEWLD)"] = {"4/4": ref, **{m: summary(W[m], ref) for m in ("3/4", "6/8", "2/2") if len(W[m]) >= 5}}; print("EWLD", {m: len(v) for m, v in W.items()}, flush=True)
    ns = runpy.run_path(os.path.join(HERE, "metre_free.py")); P = collections.defaultdict(list)
    for s, g in ns["B"].groupby("song", sort=False):
        g = g.sort_values("abs_beat"); m = ns["bm"].get(str(s))
        if len(g) < 100 or m is None or (m == "4/4" and str(s) not in ns["KEPT"]): continue
        P[("Billboard", "compound" if m in ("12/8", "6/8") else m)].append(read(g.abs_beat.values, [int(q) for q in g.pitch.values]))
    for f in sorted(glob.glob(os.path.join(ROOT, "corpora", "CoCoPops", "RollingStone", "Data", "*.hum"))):
        N = ns["rs"](f); m = ns["metre_of"](f)
        if len(N) >= 100 and m: P[("Rolling Stone", "compound" if m in ("12/8", "6/8") else m)].append(read([n[0] for n in N], [n[1] for n in N]))
    kept = summary(P[("Billboard", "4/4")]); rs4 = summary(P[("Rolling Stone", "4/4")]); comp = P[("Billboard", "compound")] + P[("Rolling Stone", "compound")]
    out["Pop"] = {"4/4 kept (Billboard)": kept, "4/4 (Rolling Stone)": rs4, "compound, against the kept 4/4": summary(comp, kept), "compound, against Rolling Stone 4/4": summary(comp, rs4), "compound (Rolling Stone only), against Rolling Stone 4/4": summary(P[("Rolling Stone", "compound")], rs4)}
    json.dump(out, open(os.path.join(HERE, "metre_free_b.json"), "w"), indent=1)
    for src, d in out.items():
        for k, o in d.items():
            if "free" in o: print(src, "|", k, "|", o["tunes"], "| not free:", [c for c, f in o["free"].items() if not f["free"]])
