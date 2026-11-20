import re, glob, collections, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
PC = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
def pc(s): return (PC[s[0]] + s.count("#") - s.count("b")) % 12
def qual(q):
    q = re.sub(r"[/(].*", "", q)
    return "min7" if q.startswith("min7") else "maj7" if q.startswith("maj7") else "min" if q.startswith("min") else "dom" if q[:1] in "79" or q in ("11", "13") else "dim" if "dim" in q else "aug" if "aug" in q else "sus" if "sus" in q else "maj"
songs = {}
for f in glob.glob("/home/claude/corpus/mcgill/billboard-2.0-salami_chords/*/salami_chords.txt"):
    sid = f.split("/")[-2]; ton = None; sec = None; by = collections.defaultdict(list)
    for ln in open(f, errors="ignore"):
        m = re.match(r"# tonic: (\S+)", ln)
        if m: ton = pc(m.group(1)); continue
        if ln.startswith("#") or "\t" not in ln: continue
        body = ln.split("\t", 1)[1]; m = re.match(r"\s*(?:[A-Z]'*, )?([a-z\- ]+), \|", body)
        if m: sec = m.group(1).strip()
        elif re.match(r"\s*[A-Z]'*, \|", body): pass
        for ch in re.findall(r"([A-G][#b]?):([^\s|]+)", body):
            if ton is not None and sec: by[sec].append(((pc(ch[0]) - ton) % 12, qual(ch[1])))
    if by: songs[sid] = by
cnt = collections.Counter(c for s in songs.values() for v in s.values() for c in v); N = sum(cnt.values()); ic = {c: -np.log2(n / N) for c, n in cnt.items()}; rows = []
for sid, by in songs.items():
    v = [ic[c] for k, cs in by.items() if k.startswith("verse") for c in cs]; ch = [ic[c] for k, cs in by.items() if k.startswith("chorus") for c in cs]; al = [ic[c] for cs in by.values() for c in cs]
    if len(v) >= 4 and len(ch) >= 4: rows.append(dict(sid=sid, drop=np.mean(v) - np.mean(ch), verse=np.mean(v), chorus=np.mean(ch), level=np.mean(al), variety=len({c for cs in by.values() for c in cs})))
R = pd.DataFrame(rows); M = pd.read_pickle("/home/claude/zeneng/corpus/v36/sound2_meta.pkl")[["sid", "G", "love", "cover_rank", "year", "peak", "half" if "half" in pd.read_pickle("/home/claude/zeneng/corpus/v36/sound2_meta.pkl").columns else "h"]]; d = M.merge(R, on="sid")
def part(x, c, tg):
    C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(x[c])), res(rankdata(x[tg]))); return round(float(r), 3), round(float(p), 4)
print("songs with marked verse and chorus", len(R), "| on the yardstick", len(d), "| share where the verse is the more surprising", round(float((d["drop"] > 0).mean()), 2)); out = {}
for c in ("drop", "verse", "chorus", "level", "variety"): out[c] = dict(G=part(d, c, "G"), love=part(d, c, "love"), covers=part(d, c, "cover_rank"), vs_peak=tuple(round(float(v), 3) for v in pearsonr(rankdata(d[c]), rankdata(-d.peak)))); print(f"   {c:8} G {out[c]['G']}  love {out[c]['love'][0]:+.3f}  covers {out[c]['covers'][0]:+.3f}  | with chart peak itself {out[c]['vs_peak'][0]:+.3f}")
json.dump(out, open("t7_results.json", "w"), indent=1)
