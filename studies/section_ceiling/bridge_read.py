"""PREDICTION_bridge.md: why a bridge sits on one pitch.  N=300 python3 studies/section_ceiling/bridge_read.py -> bridge_read.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, kept_corpus as KC, make_kept_commonest_pitch as CP, song_from_lyric as SL, metre_engine as M
from scipy.stats import spearmanr
N = int(os.environ.get("N", "300")); OVER = json.load(open(os.path.join(HERE, "read.json")))["songs"]; out = dict(kept={}, songs={})
B = KC.table(); kd = []; kc = []
for s, g in B.groupby("song", sort=False):
    g = g[[CP.kind_b(x) is not None for x in g.section.values]].sort_values("abs_beat")
    if len(g) < 20: continue
    ch = [str(x) for x in g.roman.values]; bars = g.bar.nunique(); seq = [c for i, c in enumerate(ch) if i == 0 or c != ch[i - 1]]; kd.append(len(set(ch))); kc.append((len(seq) - 1) / max(1, bars))
out["kept"] = dict(bridges=len(kd), distinct_chords_10_25_50_75_90=[float(q) for q in np.percentile(kd, (10, 25, 50, 75, 90))], changes_a_bar_10_25_50_75_90=[round(float(q), 3) for q in np.percentile(kc, (10, 25, 50, 75, 90))], note="counted under sung notes only, so a chord with no note over it is missed, in kept and engine alike")
print(json.dumps(out["kept"]), flush=True)
for tag, stem in (("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59"), ("61", "songs/p71/lyric61"), ("66", "songs/p76/lyric66")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = json.loads(json.dumps(rec["spec"])); E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=None, relocate=False)[0]
    bsec = [s for s in E.SUNG if CP.kind_b(s)]; chs = [c for s in bsec for c in rec["chords"][s]]; seq = [c for i, c in enumerate(chs) if i == 0 or c != chs[i - 1]]; longest = collections.Counter(chs).most_common(1)[0][0]
    reg = {k: [E.reg(*x)[2] - E.reg(*x)[1] for x in E.KEYS if (CP.kind_b(x[0]) if k == "Bridge" else CP.kind(x[0]) == k)] for k in ("Verse", "Chorus", "Bridge")}; hows = collections.Counter(E.HOW.get(x, ["fresh"])[0] for x in E.KEYS if CP.kind_b(x[0]))
    rng = random.Random(L.get("seed", 1)); sh = {True: [], False: []}; ct = {"Bridge": [0, 0], "Verse": [0, 0]}; on_long = 0; nb = 0; under_chords = []
    for _ in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); bn = [n for n in s if CP.kind_b(n["sec"])]
        if len(bn) < 20: continue
        ps = [n["p"] for n in bn]; top, cnt = collections.Counter(ps).most_common(1)[0]; ret = bool(E.stats and False)
        fig = set((n["sec"], n["line"]) for n in bn); same = 0; byline = collections.defaultdict(list)
        for n in bn: byline[(n["sec"], n["line"])].append(n["p"])
        ls = list(byline.values()); ret = any(ls[i] == ls[j] for i in range(len(ls)) for j in range(i)) or any(E.HOW.get(k, ["fresh"])[0] in ("copy", "again") for k in byline)
        sh[ret].append(cnt / len(ps)); nb += 1; lt = [n for n in bn if n["p"] == top]; on_long += st.mean(n["p"] % 12 in E.chord_at(n["on"]) for n in lt) >= 0.5
        for n in s:
            k = "Bridge" if CP.kind_b(n["sec"]) else "Verse" if CP.kind(n["sec"]) == "Verse" else None
            if k: ct[k][0] += n["p"] % 12 in E.chord_at(n["on"]); ct[k][1] += 1
    out["songs"][tag] = dict(over_in_100=OVER[tag]["builds"]["Bridge"]["over_per_100"], bridge_bars=len(chs), distinct_chords=len(set(chs)), changes_a_bar=round((len(seq) - 1) / len(chs), 3), chords=seq, bridge_lines_by_how=dict(hows), register_width=dict(Verse=st.median(reg["Verse"]), Chorus=st.median(reg["Chorus"]), Bridge=st.median(reg["Bridge"])), builds=nb,
                             builds_with_a_returning_bridge_line=len(sh[True]), share_where_lines_return=round(st.median(sh[True]), 3) if sh[True] else None, share_where_none=round(st.median(sh[False]), 3) if sh[False] else None, commonest_pitch_is_a_chord_tone_where_sung=round(on_long / max(1, nb), 3), chord_tone_share=dict(Bridge=round(ct["Bridge"][0] / max(1, ct["Bridge"][1]), 3), Verse=round(ct["Verse"][0] / max(1, ct["Verse"][1]), 3)))
    print(tag, json.dumps(out["songs"][tag]), flush=True)
v = list(out["songs"].values()); rho = spearmanr([x["distinct_chords"] for x in v], [x["over_in_100"] for x in v]); rho2 = spearmanr([x["changes_a_bar"] for x in v], [x["over_in_100"] for x in v]); k25 = out["kept"]["distinct_chords_10_25_50_75_90"][1]
out["candidate_1"] = dict(kept_25th_distinct=k25, songs_under=sum(x["distinct_chords"] < k25 for x in v), rho_distinct=round(float(rho[0]), 3), rho_changes_a_bar=round(float(rho2[0]), 3)); out["candidate_1"]["named"] = bool(out["candidate_1"]["songs_under"] >= 3 and rho[0] <= -0.6)
out["candidate_2"] = dict(songs_higher_by_0_05=sum(1 for x in v if x["share_where_lines_return"] is not None and x["share_where_none"] is not None and x["share_where_lines_return"] - x["share_where_none"] >= 0.05)); out["candidate_2"]["named"] = out["candidate_2"]["songs_higher_by_0_05"] >= 4
out["candidate_3"] = dict(songs_narrower_by_3=sum(1 for x in v if min(x["register_width"]["Verse"], x["register_width"]["Chorus"]) - x["register_width"]["Bridge"] >= 3)); out["candidate_3"]["named"] = out["candidate_3"]["songs_narrower_by_3"] >= 4
print(json.dumps({k: out[k] for k in ("candidate_1", "candidate_2", "candidate_3")})); json.dump(out, open(os.path.join(HERE, "bridge_read.json"), "w"), indent=1)
