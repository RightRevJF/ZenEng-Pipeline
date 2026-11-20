"""The yardstick Jason set (Nov 2026): great = still loved long after release + covered by many artists. Critics left out.
 love   : Spotify track popularity as of 2021 (Hot 100 songs only), read against songs of the same release years
 covers : number of versions SecondHandSongs holds (SHS100K list: ~10,000 most-covered works), matched by title + any performer
python3 yardstick.py -> yardstick.pkl, yardstick_summary.json"""
import pickle, re, collections, json, numpy as np, pandas as pd
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb"))
# covers
W = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) < 4: continue
    w = W[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
byT = collections.defaultdict(list)
for k, w in W.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: byT[t].append(k)
# love
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx")[["Performer", "Song", "spotify_track_popularity"]].dropna()
S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); byS = collections.defaultdict(list)
for r in S.itertuples(): byS[r.t].append(r)
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int)
pop_year = {}
for r in B.itertuples():
    h = [x for x in byS.get(r.t, []) if x.a == r.a]
    if h: pop_year[(r.t, r.a)] = (max(x.spotify_track_popularity for x in h), r.year)
PY = pd.DataFrame([(p, y) for p, y in pop_year.values()], columns=["pop", "year"])
def love_rank(pop, year):       # share of Hot 100 songs released within 3 years that it beats
    m = PY[(PY.year - year).abs() <= 3]["pop"].values
    return float((m < pop).mean()) if len(m) > 30 else None
out = []
for s in G:
    t, a = s["title"], s["artist"]; r = dict(src=s["src"], id=s["id"], title=t, artist=a, year=s.get("year"), peak=s.get("peak"), weeks=s.get("weeks"), notes=sum(len(c) for c in s["clips"]))
    c = [k for k in byT.get(t, []) if a and len(a) >= 3 and any(a in p or (len(p) >= 4 and p in a) for p in W[k]["perf"])] if t else []
    r["covers"] = max((W[k]["n"] for k in c), default=None); r["title_in_shs"] = bool(byT.get(t))
    h = [x for x in byS.get(t, []) if a and (a in x.a or x.a in a)] if t else []
    r["pop"] = max((x.spotify_track_popularity for x in h), default=None)
    r["love"] = love_rank(r["pop"], r["year"]) if r["pop"] is not None and r["year"] else None
    out.append(r)
D = pd.DataFrame(out); pickle.dump(D, open("yardstick.pkl", "wb"))
print(len(D)); print(D.groupby("src").agg(n=("id", "size"), covers=("covers", "count"), pop=("pop", "count"), love=("love", "count"), both=("covers", lambda x: int((x.notna() & D.loc[x.index, "love"].notna()).sum()))))
print("covers quartiles", D.covers.dropna().quantile([.1, .25, .5, .75, .9]).tolist())
x = D.dropna(subset=["love"]); from scipy.stats import spearmanr
print("love vs peak", spearmanr(x.love, x.peak, nan_policy="omit")); print("love vs weeks", spearmanr(x.love, x.weeks, nan_policy="omit"))
x["cov0"] = x.covers.fillna(0); print("love vs covers(0 if absent)", spearmanr(x.love, x.cov0)); print("covers vs peak", spearmanr(x.cov0, x.peak, nan_policy="omit")); print("covers vs year", spearmanr(x.cov0, x.year))
y = x[x.year <= 2005]; print("<=2005:", len(y), "covered", int(y.covers.notna().sum()), "love>=.75", int((y.love >= .75).sum()), "both", int(((y.love >= .75) & y.covers.notna()).sum()))
print(y[(y.love >= .9) & (y.covers >= 20)].sort_values("covers", ascending=False)[["id", "year", "pop", "covers"]].head(15).to_string())
