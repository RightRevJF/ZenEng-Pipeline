"""PREDICTION_tables_3_4.md: 3/4 tables from Wikifonia lead sheets, with a steadiness test by composer-split halves.  python3 studies/other_metres/tables_3_4.py -> tables_3_4.json"""
import os, sys, re, json, glob, hashlib, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); ATLAS = os.path.join(ROOT, "tables", "metre_atlas"); sys.path[:0] = [ATLAS]
import numpy as np
import mxl_tables as MX, atlas_build as AB, hymn_atlas as HA
M = "3/4"; BL = 36; BEATS = [0, 12, 24]
def one(path):
    s = MX.song(path)
    if not s: return None
    bars = collections.Counter(m["ts"] for m in s["measures"]); notes = sum(1 for m in s["measures"] for n in m["notes"] if n["p"] is not None and not n["tie"])
    if not bars or bars.most_common(1)[0][0] != M or notes < 60 or s["n_syl"] < 0.5 * notes: return None
    try: root = MX.load(path); harm = len(root.findall(".//harmony")); idn = " ".join((e.text or "") for e in root.findall("identification/*"))
    except Exception: return None
    if harm < 8: return None
    ns = []; b = 0
    for m in s["measures"]:
        if m["ts"] != M or not m["div"]: continue
        k = 12 / m["div"]; shift = BL - int(round(m["len"] * k)) if (m["implicit"] and m["len"] * k < BL) else 0
        for n in m["notes"]:
            on = int(round(n["pos"] * k)) + shift; d = max(1, int(round(n["dur"] * k)))
            if n["p"] is None or n["tie"] or on < 0 or on >= BL or on % 3: continue
            ns.append(dict(on=b * BL + on, dur=d, p=n["p"], syl=n["syl"], joins=n["joins"]))
        b += 1
    if len(ns) < 60: return None
    comp = os.path.basename(path).rsplit(" - ", 1)[0].strip().lower(); R = AB.readings([[n["on"], n["dur"], n["p"]] for n in ns], BL, BEATS, 12); bars_ = collections.defaultdict(list)
    for n in ns: bars_[n["on"] // BL].append(n["on"] % BL)
    BAR = collections.Counter(tuple(v) for v in bars_.values()); WIN = collections.Counter(tuple(v) + tuple(o + BL for o in bars_[b_ + 1]) for b_, v in bars_.items() if b_ + 1 in bars_); S = collections.Counter()
    if s["english"]:
        for w in HA.stanza_words([dict(on=n["on"], syl=n["syl"], joins=n["joins"]) for n in ns if n["syl"]]):
            st = HA.word_stresses("".join(x["syl"] for x in w), len(w))
            if st is None: continue
            for x, s_ in zip(w, st): pos = x["on"] % BL; S[(["unstressed", "primary", "secondary"][s_], "downbeat" if pos == 0 else "beat" if pos in BEATS else "off the beat")] += 1
    yr = re.findall(r"\b(1[89]\d\d|20[01]\d)\b", idn + " " + comp)
    return dict(ns=[[n["on"], n["dur"], n["p"]] for n in ns], comp=comp, half=int(hashlib.md5(comp.encode()).hexdigest(), 16) % 2, R=R, BAR=BAR, WIN=WIN, S=S, english=s["english"], year=int(yr[0]) if yr else None)
def table(v):
    BAR = sum((x["BAR"] for x in v), collections.Counter()); WIN = sum((x["WIN"] for x in v), collections.Counter()); S = sum((x["S"] for x in v), collections.Counter()); tb = sum(BAR.values()); tw = sum(WIN.values()); st = {}
    for cls in ("primary", "unstressed"):
        t = sum(c for (a, l), c in S.items() if a == cls); st[cls] = dict({l: round(S[(cls, l)] / t, 3) for l in ("downbeat", "beat", "off the beat")}, syllables=t) if t else {}
    return dict(songs=len(v), english=sum(x["english"] for x in v), readings_quartiles={k: [round(float(np.percentile([x["R"][k] for x in v], q)), 4) for q in (25, 50, 75)] for k in v[0]["R"]}, bars_total=tb, bar_rhythms={k: c / tb for k, c in BAR.items()}, windows_total=tw, two_bar_windows={k: c / tw for k, c in WIN.items()}, stress=st)
def top_corr(a, b, key, n=20):
    ks = [k for k, _ in sorted(((k, a[key].get(k, 0) + b[key].get(k, 0)) for k in set(a[key]) | set(b[key])), key=lambda x: -x[1])[:n]]; return round(float(np.corrcoef([a[key].get(k, 0) for k in ks], [b[key].get(k, 0) for k in ks])[0, 1]), 3)
def out_table(t, n=20): return dict(t, bar_rhythms=[[list(k), round(c, 4)] for k, c in sorted(t["bar_rhythms"].items(), key=lambda x: -x[1])[:n]], two_bar_windows=[[list(k), round(c, 4)] for k, c in sorted(t["two_bar_windows"].items(), key=lambda x: -x[1])[:n]])
if __name__ == "__main__":
    out = {}
    for name, pat in (("Wikifonia", "/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl"), ("OpenEWLD", "/home/claude/corpus/OpenEWLD/dataset/**/*.mxl")):
        with Pool(2) as pool: V = [x for x in pool.map(one, sorted(glob.glob(pat, recursive=True)), chunksize=20) if x]
        if name == "OpenEWLD":
            for x in V: x["comp"] = "e"
        A = [x for x in V if x["half"] == 0]; B = [x for x in V if x["half"] == 1]; T = table(V); o = dict(all=out_table(T), composers=len(set(x["comp"] for x in V)), with_a_year=sum(x["year"] is not None for x in V), years_quartiles=[int(q) for q in np.percentile([x["year"] for x in V if x["year"]], (25, 50, 75))] if any(x["year"] for x in V) else None)
        if name == "Wikifonia":
            ta, tb = table(A), table(B); o["halves"] = dict(songs=[len(A), len(B)], bar_rhythms_top20_corr=top_corr(ta, tb, "bar_rhythms"), two_bar_windows_top20_corr=top_corr(ta, tb, "two_bar_windows"), stressed_on_downbeat=[ta["stress"]["primary"]["downbeat"], tb["stress"]["primary"]["downbeat"]], notes_a_beat_median=[ta["readings_quartiles"]["notes a beat"][1], tb["readings_quartiles"]["notes a beat"][1]])
            h = o["halves"]; o["steady"] = dict(bar_rhythms=h["bar_rhythms_top20_corr"] >= 0.9, two_bar_windows=h["two_bar_windows_top20_corr"] >= 0.8, stress=abs(h["stressed_on_downbeat"][0] - h["stressed_on_downbeat"][1]) <= 0.03, notes_a_beat=abs(h["notes_a_beat_median"][0] - h["notes_a_beat_median"][1]) <= 0.05)
        out[name] = o; print(name, len(V), o.get("halves"), o.get("steady"), "years", o["with_a_year"], o["years_quartiles"], flush=True)
    json.dump(out, open(os.path.join(HERE, "tables_3_4.json"), "w"), indent=1)
