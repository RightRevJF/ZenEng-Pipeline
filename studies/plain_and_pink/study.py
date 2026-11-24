"""Plain and pink (749.166): melody surprise against the pitches' long-range order on the 167 kept songs, by the rule in PREDICTION.md.
    python3 studies/plain_and_pink/study.py -> result.json"""
import os, sys, json, collections, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC, page_gate as PG, scaling as SC
ks = list(KC.kept_songs(min_notes=100)); T = KC.table(); syl = {str(s): [str(x) if x == x else "" for x in g.sort_values("abs_beat").syl.values] for s, g in T.groupby("song", sort=False)}
seqs = [PG.ivs([int(x) for x in k["p"]]) for k in ks]; C = PG.counts(seqs)
def top3(p): return sum(v for _, v in collections.Counter(p).most_common(3)) / len(p)
def dfa(p, o): r = SC.dfa(p, order=o); return r["alpha"] if r else None
rows = []
for k, s in zip(ks, seqs):
    p = [int(x) for x in k["p"]]; sy = syl.get(str(k["song"]), []); att = [x for x, y in zip(p, sy) if y and y not in ("_", "-", "~")] if len(sy) == len(p) else None
    rows.append(dict(song=str(k["song"]), n=len(p), surprise=PG.surprise(s, C, minus=PG.counts([s])), dfa1=dfa(p, 1), dfa2=dfa(p, 2), top3=top3(p),
                     att_n=len(att) if att else None, att_dfa1=dfa(att, 1) if att and len(att) >= 64 else None, att_dfa2=dfa(att, 2) if att and len(att) >= 64 else None, att_top3=top3(att) if att else None))
ok = [r for r in rows if r["dfa1"] is not None and r["dfa2"] is not None]
def rho(a, b, R=ok):
    x = [(r[a], r[b]) for r in R if r[a] is not None and r[b] is not None]; v = spearmanr([u for u, _ in x], [w for _, w in x]); return dict(rho=round(float(v.statistic), 3), p=round(float(v.pvalue), 4), n=len(x))
q = lambda c, R=ok: [round(float(x), 3) for x in np.percentile([r[c] for r in R if r[c] is not None], (10, 25, 50, 75, 90))]
res = dict(songs=len(rows), read=len(ok), quantiles={c: q(c) for c in ("surprise", "dfa1", "dfa2", "top3", "att_dfa1", "att_dfa2", "att_top3")})
res["primary"] = rho("surprise", "dfa1"); r_ = res["primary"]["rho"]; p_ = res["primary"]["p"]
res["verdict"] = "they trade" if (r_ >= 0.20 and p_ < .05) else "they do not trade" if abs(r_) < 0.10 else ("weak" if r_ > 0 else "the other sign: plainer goes with pinker")
ms, md = np.median([r["surprise"] for r in ok]), np.median([r["dfa1"] for r in ok]); both = [r for r in ok if r["surprise"] <= ms and r["dfa1"] >= md]
res["both"] = dict(share=round(len(both) / len(ok), 3), n=len(both), region_exists=len(both) / len(ok) >= 0.20, dfa1=q("dfa1", both), dfa2=q("dfa2", both), top3=q("top3", both), surprise=q("surprise", both))
res["deciding_nothing"] = {f"{a} ~ {b}": rho(a, b) for a, b in (("surprise", "dfa2"), ("surprise", "top3"), ("dfa1", "top3"), ("dfa2", "top3"), ("surprise", "att_dfa1"), ("surprise", "att_dfa2"), ("att_dfa1", "att_top3"))}
# song 62 placed among the kept (every note)
def place(v, c): k_ = np.array([r[c] for r in ok]); return round(float((k_ < v).mean() * 100))
s62 = {}
for name, f in (("engine draw", "songs/p72/run/lyric62_off.song.json"), ("first edition", "songs/p72/out/first edition, corrected/record.json"), ("pink survivor", "songs/p72/run_d/lyric62_d.song.json")):
    fp = os.path.join(ROOT, f)
    if not os.path.exists(fp): continue
    R = json.load(open(fp)); mel = R["melody"]["notes"] if isinstance(R["melody"], dict) else R["melody"]; p = [n["midi"] for n in sorted(mel, key=lambda n: n["on"])]
    sv = PG.surprise(PG.ivs(p), C); s62[name] = dict(surprise=round(sv, 3), surprise_pct=place(sv, "surprise"), dfa1=round(dfa(p, 1), 3), dfa1_pct=place(dfa(p, 1), "dfa1"), dfa2=round(dfa(p, 2), 3), dfa2_pct=place(dfa(p, 2), "dfa2"), top3=round(top3(p), 3), top3_pct=place(top3(p), "top3"),
                    in_region=bool(sv <= ms and dfa(p, 1) >= md))
res["song_62"] = s62; res["region_rule"] = dict(surprise_at_most=round(float(ms), 3), dfa1_at_least=round(float(md), 3))
json.dump(dict(res, rows=rows), open(os.path.join(HERE, "result.json"), "w"), indent=1); print(json.dumps(res, indent=1))
