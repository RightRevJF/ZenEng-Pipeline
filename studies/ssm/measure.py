"""Measure the readings named in PREDICTION.md on 410 CoCoPops songs and Luthier's songs; test P1-P6. python3 measure.py -> measure.json"""
import sys, os, glob, re, json
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import ssm_lib as L
C = "/home/claude/data/cocopops/CoCoPops"; P = "/home/claude/zeneng-pipeline/songs"
def lagprof(M):
    n = len(M); return np.array([np.mean(np.diagonal(M, k)) for k in range(1, n // 2 + 1)])
def readings(M):
    n = len(M); Lp = lagprof(M); r = {}
    mark = np.zeros(n, bool)
    for k in range(8, n):
        d = np.diagonal(M, k) >= 0.8; i = 0
        while i < len(d):
            if d[i]:
                j = i
                while j < len(d) and d[j]: j += 1
                if j - i >= 4: mark[i:j] = True; mark[i + k:j + k] = True
                i = j
            else: i += 1
    r["architecture"] = float(mark.mean())
    med = np.median(Lp); r["nesting"] = int(sum(1 for k in (2, 4, 8, 16, 32) if k + 1 <= len(Lp) and Lp[k - 1] > max(Lp[k - 2], Lp[k]) and Lp[k - 1] > med))
    short = Lp[0:3].mean(); long_ = Lp[7:32].mean() if len(Lp) > 8 else np.nan; r["weave"] = float(short / long_) if long_ and long_ > 0 else np.nan
    vals = []
    for w in range(4, 9):
        for s in range(0, n - w + 1):
            inside = np.zeros(n, bool); inside[s:s + w] = True
            vals.append(((s + w / 2) / n, 1 - M[np.ix_(inside, ~inside)].mean()))
    allv = np.array([v for _, v in vals]); mid = [v for c, v in vals if 0.35 <= c <= 0.85]
    r["centre"] = float(max(mid) - np.median(allv)) if mid else np.nan
    best = 0.0
    for s in range(max(8, n - 16), n - 7):
        best = max(best, float(np.mean([M[j, s + j] for j in range(8)])))
    r["frame"] = best
    off = M[~np.eye(n, dtype=bool)]; r["sameness"] = float(off.mean()); r["bars"] = n
    return r
def norm(t): return re.sub(r"[^a-z]", "", t.lower())
def _study():
    pass
def main():
    songs = []
    for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
        for f in sorted(glob.glob(os.path.join(C, pat))):
            s = L.read_hum(f)
            if sum(len(b["mel"]) for b in s["bars"]) < 40 or len(s["bars"]) < 24: continue
            r = readings(L.ssm(s)); r.update(group=grp, title=s["title"], artist=s["artist"], file=os.path.basename(f))
            m = re.match(r"\d+", str(s.get("peak") or "")); r["peak"] = int(m.group(0)) if m else None
            m = re.match(r"\d+", str(s.get("rs_rank") or "")); r["rs_rank"] = int(m.group(0)) if m else None
            meta = {x.group(1): x.group(2) for x in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(f, errors="ignore")) if x}
            m = re.match(r"\d+", meta.get("BillboardWeeksOnChart", "")); r["weeks"] = int(m.group(0)) if m else None
            songs.append(r)
    eng = []
    for f, nm in ((P + "/p64/lyric54.song.json", "song 54"), (P + "/p65/lyric55.song.json", "song 55"), (P + "/p68/lyric58.song.json", "song 58")):
        r = readings(L.ssm(L.read_record(f))); r.update(group="Luthier", title=nm); eng.append(r)
    K = ("architecture", "nesting", "weave", "centre", "frame", "sameness", "bars")
    A = lambda k, g: np.array([s[k] for s in songs if s["group"] == g and s[k] == s[k]], float)
    res = dict(n={g: sum(1 for s in songs if s["group"] == g) for g in ("RS", "BB")}, auc={}, medians={}, billboard_peak={}, billboard_weeks={}, rs_rank={}, luthier={}, overlap=[])
    for k in K:
        a, b = A(k, "RS"), A(k, "BB"); u = mannwhitneyu(a, b); res["auc"][k] = [round(float(u.statistic / (len(a) * len(b))), 3), round(float(u.pvalue), 4)]
        res["medians"][k] = [round(float(np.median(a)), 3), round(float(np.median(b)), 3)]
        bb = [s for s in songs if s["group"] == "BB" and s["peak"] and s[k] == s[k]]
        res["billboard_peak"][k] = [round(float(x), 3) for x in spearmanr([s[k] for s in bb], [-s["peak"] for s in bb])]
        bw = [s for s in bb if s["weeks"]]; res["billboard_weeks"][k] = [round(float(x), 3) for x in spearmanr([s[k] for s in bw], [s["weeks"] for s in bw])]
        rs = [s for s in songs if s["group"] == "RS" and s["rs_rank"] and s[k] == s[k]]; res["rs_rank"][k] = [round(float(x), 3) for x in spearmanr([s[k] for s in rs], [-s["rs_rank"] for s in rs])]
    hum = {k: np.array([s[k] for s in songs if s[k] == s[k]], float) for k in K}
    for e in eng: res["luthier"][e["title"]] = {k: [round(float(e[k]), 3), round(float((hum[k] < e[k]).mean() * 100), 1)] for k in K if e[k] == e[k]}
    byt = {}
    for s in songs: byt.setdefault(norm(s["title"]), []).append(s)
    for t, v in byt.items():
        gs = {s["group"] for s in v}
        if gs == {"RS", "BB"}: res["overlap"].append({s["group"]: {k: round(float(s[k]), 3) for k in K} for s in v} | {"title": v[0]["title"]})
    json.dump(dict(res=res, songs=songs, luthier=eng), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "measure.json"), "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))

if __name__ == "__main__": main()
